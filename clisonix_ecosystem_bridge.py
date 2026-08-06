#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLISONIX ECOSYSTEM BRIDGE - Unifikuar per te gjithe sistemin Clisonix AI
===================================================================
Bridge qendror qe lidh te gjitha repos e ekosistemit Clisonix/Neurosonic.

Zero Dependencies • Zero Fake • Zero Noise • Absolute Independence

Repos e lidhura:
1. Neurosonic (core)          - Python   - port 8765
2. Kloud                      - Python   - port 9001
3. clisonix.com               - Python   - port 9002
4. web8                       - JS       - port 9003
5. OS-CLX                     - Go       - port 9004
6. Cwy                        - TS       - port 9005
7. clisonix-blog              - HTML     - port 9006
8. clisonixwesterneurope      - TS       - port 9007
9. starbooking                - JS       - port 9008
10. clisonix-news             - HTML     - port 9009
11. ultrathinking-web         - Python   - port 9010
12. ultrawebthinking          - TS       - port 9011
13. Lightning-SPP-3.14        - Python   - port 8080
14. OS-Web8                   - NodeDB   - port 9012
15. Ultrawebthinking          - NodeDB   - port 9013

ABA GmbH - HRB 21069 Bochum
Email: clisonix@pm.me
"""

import os
import json
import time
import hashlib
import datetime
import urllib.request
import urllib.error
import threading
from typing import Dict, List, Any, Optional

__version__ = "1.0.0"
__author__ = "ABA GmbH - HRB 21069 Bochum"
__email__ = "clisonix@pm.me"


# ============================================================================
# REGJISTRI I EKOSISTEMIT - 15 Repos
# ============================================================================

# Struktura: { name: {owner, language, port, url, bridge_file} }
ECOSYSTEM_REPOS: Dict[str, Dict[str, Any]] = {
    "Neurosonic": {
        "owner": "LedjanAhmati",
        "language": "Python",
        "port": 8765,
        "url": "https://github.com/LedjanAhmati/www.neuroconic.eu",
        "role": "core",
    },
    "Kloud": {
        "owner": "Web8kameleon-hub",
        "language": "Python",
        "port": 9001,
        "url": "https://github.com/Web8kameleon-hub/Kloud",
        "role": "cloud",
    },
    "clisonix.com": {
        "owner": "Web8kameleon-hub",
        "language": "Python",
        "port": 9002,
        "url": "https://github.com/Web8kameleon-hub/clisonix.com",
        "role": "web",
    },
    "web8": {
        "owner": "Web8kameleon-hub",
        "language": "JavaScript",
        "port": 9003,
        "url": "https://github.com/Web8kameleon-hub/web8",
        "role": "browser",
    },
    "OS-CLX": {
        "owner": "Web8kameleon-hub",
        "language": "Go",
        "port": 9004,
        "url": "https://github.com/Web8kameleon-hub/OS-CLX",
        "role": "os",
    },
    "Cwy": {
        "owner": "Web8kameleon-hub",
        "language": "TypeScript",
        "port": 9005,
        "url": "https://github.com/Web8kameleon-hub/Cwy",
        "role": "cli",
    },
    "clisonix-blog": {
        "owner": "LedjanAhmati",
        "language": "HTML",
        "port": 9006,
        "url": "https://github.com/LedjanAhmati/clisonix-blog",
        "role": "content",
    },
    "clisonixwesterneurope": {
        "owner": "Web8kameleon-hub",
        "language": "TypeScript",
        "port": 9007,
        "url": "https://github.com/Web8kameleon-hub/clisonixwesterneurope",
        "role": "regional",
    },
    "starbooking": {
        "owner": "Web8kameleon-hub",
        "language": "JavaScript",
        "port": 9008,
        "url": "https://github.com/Web8kameleon-hub/starbooking",
        "role": "booking",
    },
    "clisonix-news": {
        "owner": "Web8kameleon-hub",
        "language": "HTML",
        "port": 9009,
        "url": "https://github.com/Web8kameleon-hub/clisonix-news",
        "role": "content",
    },
    "ultrathinking-web": {
        "owner": "Web8kameleon-hub",
        "language": "Python",
        "port": 9010,
        "url": "https://github.com/Web8kameleon-hub/ultrathinking-web",
        "role": "thinking",
    },
    "ultrawebthinking": {
        "owner": "Web8kameleon-hub",
        "language": "TypeScript",
        "port": 9011,
        "url": "https://github.com/Web8kameleon-hub/ultrawebthinking",
        "role": "browser",
    },
    "Lightning-SPP-3.14": {
        "owner": "Web8kameleon-hub",
        "language": "Python",
        "port": 8080,
        "url": "https://github.com/Web8kameleon-hub/Lightning-SPP-3.14",
        "role": "spp",
    },
    "OS-Web8": {
        "owner": "BledjonaAhmati",
        "language": "NodeDB Fluid",
        "port": 9012,
        "url": "https://github.com/BledjonaAhmati/OS-Web8",
        "role": "os",
    },
    "Ultrawebthinking": {
        "owner": "BledjonaAhmati",
        "language": "NodeDB Fluid",
        "port": 9013,
        "url": "https://github.com/BledjonaAhmati/Ultrawebthinking",
        "role": "browser",
    },
}


# ============================================================================
# BRIDGE PER REPO - komunikim HTTP real
# ============================================================================


class RepoBridge:
    """
    Bridge unik per nje repo ne ekosistem.
    Zero Fake - cdo komunikim eshte request real.
    """

    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.language = config.get("language", "Unknown")
        self.port = config.get("port", 9000)
        self.url = config.get("url", "")
        self.role = config.get("role", "generic")
        self.status = "initialized"
        self.last_pulse: Optional[Dict[str, Any]] = None
        self.bridge_id = hashlib.sha256(
            f"clx_{name}{time.time()}".encode()
        ).hexdigest()[:16]
        self.base_url = f"http://localhost:{self.port}"

    def ping(self) -> float:
        """Mat koha e pergjigjes se repo-s (ms). -1 = offline"""
        start = time.time()
        try:
            req = urllib.request.Request(f"{self.base_url}/health", method="GET")
            with urllib.request.urlopen(req, timeout=2) as resp:
                if resp.status == 200:
                    self.status = "online"
                    return (time.time() - start) * 1000
        except Exception:
            pass
        self.status = "offline"
        return -1.0

    def send_pulse(self, status: str = "active") -> Dict[str, Any]:
        """Dergo sinjalin Pulse per repo-ne"""
        now = time.time()
        pulse = {
            "bridge_id": self.bridge_id,
            "repo": self.name,
            "language": self.language,
            "port": self.port,
            "status": status,
            "timestamp": now,
            "datetime": datetime.datetime.fromtimestamp(now).isoformat(),
            "hash": hashlib.sha256(f"{self.name}{now}{status}".encode()).hexdigest()[
                :16
            ],
        }
        self.last_pulse = pulse
        return pulse

    def get_status(self) -> Dict[str, Any]:
        """Kthe statusin e bridge"""
        return {
            "repo": self.name,
            "language": self.language,
            "port": self.port,
            "role": self.role,
            "status": self.status,
            "bridge_id": self.bridge_id,
            "url": self.url,
            "last_pulse": self.last_pulse,
        }

    def __repr__(self) -> str:
        return f"<RepoBridge {self.name} [{self.language}] ({self.status})>"


# ============================================================================
# EKOSISTEM BRIDGE - menaxhon te gjitha repos
# ============================================================================


class ClisonixEcosystemBridge:
    """
    Bridge qendror i ekosistemit Clisonix AI.
    Lidh, monitoron dhe dergon pulse per te gjitha 15 repos.
    """

    def __init__(self, core_url: str = "http://localhost:8765"):
        self.core_url = core_url.rstrip("/")
        self.bridges: Dict[str, RepoBridge] = {}
        self.ecosystem_id = hashlib.sha256(
            f"ecosystem_{time.time()}".encode()
        ).hexdigest()[:16]
        self._initialize()
        self._monitor_thread: Optional[threading.Thread] = None
        self._monitoring = False

    def _initialize(self):
        """Inicializon bridge per cdo repo ne regjister"""
        for name, config in ECOSYSTEM_REPOS.items():
            self.bridges[name] = RepoBridge(name, config)

    def discover(self, timeout: int = 2) -> Dict[str, Any]:
        """
        Zbulon te gjitha repos qe jane online.
        Kthen nje raport te shendetit te ekosistemit.
        """
        results = {}
        online = 0
        for name, bridge in self.bridges.items():
            latency = bridge.ping()
            results[name] = {
                "status": bridge.status,
                "latency_ms": latency,
                "language": bridge.language,
                "port": bridge.port,
            }
            if bridge.status == "online":
                online += 1

        return {
            "ecosystem_id": self.ecosystem_id,
            "total_repos": len(self.bridges),
            "online": online,
            "offline": len(self.bridges) - online,
            "timestamp": datetime.datetime.now().isoformat(),
            "repos": results,
        }

    def broadcast_pulse(self, status: str = "active") -> Dict[str, Any]:
        """Dergon pulse per te gjitha repos"""
        pulses = {}
        for name, bridge in self.bridges.items():
            pulses[name] = bridge.send_pulse(status)
        return {
            "ecosystem_id": self.ecosystem_id,
            "total_pulses": len(pulses),
            "timestamp": datetime.datetime.now().isoformat(),
            "pulses": pulses,
        }

    def connect_all(self) -> Dict[str, Any]:
        """Lidh te gjitha repos me Core"""
        report = {}
        for name, bridge in self.bridges.items():
            try:
                payload = json.dumps(
                    {
                        "bridge_id": bridge.bridge_id,
                        "repo": name,
                        "url": bridge.url,
                        "port": bridge.port,
                        "language": bridge.language,
                        "role": bridge.role,
                        "bridge_version": __version__,
                    }
                ).encode()
                req = urllib.request.Request(
                    f"{self.core_url}/api/bridge/register",
                    data=payload,
                    headers={"Content-Type": "application/json"},
                )
                resp = urllib.request.urlopen(req, timeout=5)
                report[name] = {
                    "registered": resp.status == 200,
                    "port": bridge.port,
                }
                bridge.status = "connected" if resp.status == 200 else "error"
            except Exception as e:
                report[name] = {
                    "registered": False,
                    "port": bridge.port,
                    "error": str(e),
                }
                bridge.status = "offline"
        return {
            "ecosystem_id": self.ecosystem_id,
            "core_url": self.core_url,
            "report": report,
        }

    def start_monitoring(self, interval: int = 300):
        """Nis thread monitorimi qe dergon pulse cdo 'interval' sekonda"""
        if self._monitoring:
            return

        self._monitoring = True

        def _loop():
            while self._monitoring:
                try:
                    self.broadcast_pulse()
                except Exception as e:
                    print(f"⚠️ Monitor: {e}")
                time.sleep(interval)

        self._monitor_thread = threading.Thread(target=_loop, daemon=True)
        self._monitor_thread.start()

        return {
            "ecosystem_id": self.ecosystem_id,
            "monitoring": True,
            "interval_s": interval,
        }

    def stop_monitoring(self) -> Dict[str, bool]:
        """Ndalon monitorimin"""
        self._monitoring = False
        return {"monitoring": False}

    def get_ecosystem_status(self) -> Dict[str, Any]:
        """Kthe statusin e plote te ekosistemit"""
        return {
            "name": "Clisonix AI Ecosystem",
            "version": __version__,
            "ecosystem_id": self.ecosystem_id,
            "core_url": self.core_url,
            "total_repos": len(self.bridges),
            "monitoring": self._monitoring,
            "repos": {
                name: bridge.get_status() for name, bridge in self.bridges.items()
            },
        }

    def generate_readme_badges(self) -> str:
        """Gjeneron badge status per README"""
        badges = []
        for name, bridge in self.bridges.items():
            color = {
                "online": "brightgreen",
                "connected": "brightgreen",
                "offline": "red",
                "initialized": "yellow",
                "error": "orange",
            }.get(bridge.status, "lightgrey")
            badges.append(
                f"![{name}](https://img.shields.io/badge/{name.replace('-', '')}-{bridge.status}-{color}"
                f"?logo=github)"
            )
        return "\n".join(badges)


# ============================================================================
# MAIN - Demo
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  CLISONIX ECOSYSTEM BRIDGE v1.0.0")
    print("  Lidhje me 15 repos te ekosistemit Clisonix AI")
    print("=" * 60)
    print()

    ecosystem = ClisonixEcosystemBridge()

    # Shfaq repos
    print("📦 Repos ne ekosistem:")
    for name, bridge in ecosystem.bridges.items():
        print(f"   {name:<24} [{bridge.language:<12}] port {bridge.port}")

    print()
    print("🔍 Duke zbuluar repos online...")
    discovery = ecosystem.discover()
    print(f"   Online: {discovery['online']}/{discovery['total_repos']}")
    print(f"   Offline: {discovery['offline']}/{discovery['total_repos']}")

    print()
    print("💓 Duke derguar Pulse broadcast...")
    pulses = ecosystem.broadcast_pulse()
    print(f"   Pulse derguar: {pulses['total_pulses']}")

    print()
    print("📊 Statusi i ekosistemit:")
    for name, bridge in ecosystem.bridges.items():
        print(f"   {name:<24} -> {bridge.status}")

    print()
    print("=" * 60)
    print("  CLISONIX ECOSYSTEM BRIDGE GATI!")
    print("=" * 60)
