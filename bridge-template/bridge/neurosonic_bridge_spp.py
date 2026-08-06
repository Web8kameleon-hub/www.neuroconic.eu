#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEUROSONIC BRIDGE SPP - Lidhje me Lightning-SPP-3.14
Per repos PDF/Scan/Print ne ekosistem.

Perdoret nga: Lightning-SPP-3.14
"""

import json
import time
import hashlib
import urllib.request
import urllib.error
from typing import Dict, Any, Optional


class NeurosonicSPPBridge:
    """
    Bridge specifik per Lightning-SPP-3.14.
    Scan -> Process -> Print Engine.
    """

    def __init__(
        self,
        repo_name: str = "Lightning-SPP-3.14",
        spp_url: str = "http://localhost:8080",
        port: int = 8080,
    ):
        self.repo_name = repo_name
        self.spp_url = spp_url.rstrip("/")
        self.core_url = "http://localhost:8765"
        self.port = port
        self.status = "initialized"
        self.last_pulse: Optional[Dict[str, Any]] = None
        self.bridge_id = hashlib.sha256(
            f"spp_{repo_name}{time.time()}".encode()
        ).hexdigest()[:16]

    def check_spp_health(self) -> bool:
        """Kontrollo shendetin e Lightning SPP"""
        try:
            req = urllib.request.Request(f"{self.spp_url}/health", method="GET")
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read().decode())
                self.status = (
                    "connected" if data.get("status") == "healthy" else "offline"
                )
                return self.status == "connected"
        except Exception as e:
            self.status = "offline"
            return False

    def connect(self) -> bool:
        """Lidhu me SPP dhe regjistrohu ne Core"""
        spp_ok = self.check_spp_health()
        try:
            payload = json.dumps(
                {
                    "bridge_id": self.bridge_id,
                    "repo": self.repo_name,
                    "url": f"https://github.com/Web8kameleon-hub/{self.repo_name}",
                    "port": self.port,
                    "spp_health": spp_ok,
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
            return response.status == 200
        except Exception:
            self.status = "connected" if spp_ok else "offline"
            return spp_ok

    def send_pulse(self, status: str = "active") -> Dict[str, Any]:
        """Dergo sinjalin Pulse"""
        pulse = {
            "bridge_id": self.bridge_id,
            "repo": self.repo_name,
            "status": status,
            "spp_url": self.spp_url,
            "timestamp": time.time(),
            "datetime": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "hash": hashlib.sha256(
                f"{self.repo_name}{time.time()}{status}".encode()
            ).hexdigest()[:16],
        }
        self.last_pulse = pulse
        return pulse

    def get_status(self) -> Dict[str, Any]:
        """Kthe statusin e bridge"""
        return {
            "bridge_id": self.bridge_id,
            "repo": self.repo_name,
            "status": self.status,
            "connected": self.status == "connected",
            "spp_url": self.spp_url,
            "last_pulse": self.last_pulse,
            "port": self.port,
        }

    def __repr__(self) -> str:
        return f"<NeurosonicSPPBridge {self.repo_name} ({self.status})>"


if __name__ == "__main__":
    bridge = NeurosonicSPPBridge()
    print(f"Bridge ID: {bridge.bridge_id}")
    print(f"SPP Health: {bridge.check_spp_health()}")
    print(f"Status: {bridge.status}")
    pulse = bridge.send_pulse()
    print(f"Pulse: {pulse['status']} @ {pulse['datetime']}")
    print("SPP Bridge: OK")
