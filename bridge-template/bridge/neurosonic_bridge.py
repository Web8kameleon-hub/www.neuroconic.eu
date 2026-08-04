#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEUROSONIC BRIDGE - Lidhje me Neurosonic Core (Python)
Per cdo repo Python ne ekosistem.

Bridge = komunikim modular me ekosistemin
Pulse = sinjali i gjalle i repo-s
"""

import json
import time
import hashlib
import urllib.request
import urllib.error
import os
import sys
from typing import Dict, Any, Optional


class NeurosonicBridge:
    """
    Bridge per komunikim me Neurosonic Core.

    Perdoret nga: Kloud, clisonix.com, ultrathinking-web, etj.
    """

    def __init__(self, repo_name: str, repo_url: str = "", port: int = 9001):
        self.repo_name = repo_name
        self.repo_url = repo_url or f"https://github.com/Web8kameleon-hub/{repo_name}"
        self.core_url = "http://localhost:8765"
        self.core_api = "https://neurosonic.eu/api"
        self.port = port
        self.status = "initialized"
        self.last_pulse: Optional[Dict[str, Any]] = None
        self.bridge_id = hashlib.sha256(
            f"{repo_name}{time.time()}".encode()
        ).hexdigest()[:16]

    def connect(self) -> bool:
        """Lidhu me Neurosonic Core"""
        try:
            payload = json.dumps(
                {
                    "bridge_id": self.bridge_id,
                    "repo": self.repo_name,
                    "url": self.repo_url,
                    "port": self.port,
                    "bridge_version": "1.0",
                    "language": "python",
                }
            ).encode()
            req = urllib.request.Request(
                f"{self.core_url}/api/bridge/register",
                data=payload,
                headers={"Content-Type": "application/json"},
            )
            response = urllib.request.urlopen(req, timeout=5)
            if response.status == 200:
                self.status = "connected"
                return True
        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            ConnectionRefusedError,
            TimeoutError,
        ):
            self.status = "offline"
        return False

    def send_pulse(self, commit: str = "", status: str = "active") -> Dict[str, Any]:
        """Dergo sinjalin Pulse ne Neurosonic Core"""
        pulse = {
            "bridge_id": self.bridge_id,
            "repo": self.repo_name,
            "status": status,
            "commit": commit
            or os.popen('git log -1 --format="%H"').read().strip()[:12],
            "timestamp": time.time(),
            "datetime": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "uptime": self._get_uptime(),
            "hash": hashlib.sha256(
                f"{self.repo_name}{time.time()}{status}".encode()
            ).hexdigest()[:16],
        }
        self.last_pulse = pulse
        return pulse

    def check_health(self) -> Dict[str, Any]:
        """Kontrollo shendetin e bridge"""
        return {
            "bridge_id": self.bridge_id,
            "repo": self.repo_name,
            "status": self.status,
            "connected": self.status == "connected",
            "last_pulse": self.last_pulse,
            "core_url": self.core_url,
            "port": self.port,
        }

    def _get_uptime(self) -> float:
        """Kthe uptime ne sekonda"""
        if self.last_pulse:
            return time.time() - self.last_pulse["timestamp"]
        return 0.0

    def get_status_badge(self) -> str:
        """Kthe badge status per README"""
        colors = {"connected": "brightgreen", "offline": "red", "initialized": "yellow"}
        color = colors.get(self.status, "lightgrey")
        return f"![Bridge](https://img.shields.io/badge/Bridge-{self.status}-{color})"

    def __repr__(self) -> str:
        return f"<NeurosonicBridge {self.repo_name} ({self.status})>"


class Pulse:
    """
    Pulse - Sinjali i gjalle i repo-s.
    Perdoret ne CI/CD dhe local monitoring.
    """

    def __init__(self, repo_name: str):
        self.repo_name = repo_name
        self.beats = []
        self.alive = True

    def beat(self, status: str = "ok") -> Dict[str, Any]:
        """Nje rrahje zemre"""
        pulse = {
            "repo": self.repo_name,
            "status": status,
            "timestamp": time.time(),
            "datetime": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "beat_number": len(self.beats) + 1,
        }
        self.beats.append(pulse)
        return pulse

    def get_stats(self) -> Dict[str, Any]:
        """Statistika te Pulse"""
        total = len(self.beats)
        if total == 0:
            return {"total_beats": 0, "alive": self.alive}
        last_beat = self.beats[-1]
        time_since_last = time.time() - last_beat["timestamp"]
        return {
            "total_beats": total,
            "alive": time_since_last < 300,  # 5 minuta
            "last_beat": last_beat["datetime"],
            "seconds_since_last": time_since_last,
            "status": "healthy" if time_since_last < 300 else "critical",
        }


# Test i shpejte
if __name__ == "__main__":
    bridge = NeurosonicBridge("test-repo", port=9001)
    print(f"Bridge ID: {bridge.bridge_id}")
    print(f"Status: {bridge.status}")
    print(f"Badge: {bridge.get_status_badge()}")

    pulse = Pulse("test-repo")
    for i in range(3):
        p = pulse.beat()
        print(f"Pulse #{p['beat_number']}: {p['status']}")
        time.sleep(0.1)

    stats = pulse.get_stats()
    print(f"Pulse Stats: {stats}")
    print("Bridge + Pulse: OK")
