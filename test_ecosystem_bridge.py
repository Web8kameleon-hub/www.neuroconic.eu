#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLISONIX ECOSYSTEM BRIDGE - TEST
Verifikon funksionalitetin e te gjithe ekosistemit te bridge-ve.
"""

import sys
import time
import json

passes = 0
fails = 0


def check(name, condition, detail=""):
    global passes, fails
    if condition:
        passes += 1
        print(f"  ✅ {name} {detail}")
    else:
        fails += 1
        print(f"  ❌ {name} {detail}")


def run_tests():
    print("=" * 60)
    print("  TEST: CLISONIX ECOSYSTEM BRIDGE")
    print("=" * 60)

    # ============ Modulet kryesore ============
    print("\n📦 1. Moduli importohet")
    import clisonix_ecosystem_bridge as m

    check("Import OK", hasattr(m, "ClisonixEcosystemBridge"))
    check(
        "15 repos ne regjister",
        len(m.ECOSYSTEM_REPOS) == 15,
        f"({len(m.ECOSYSTEM_REPOS)})",
    )
    check("Version 1.0.0", m.__version__ == "1.0.0")

    # ============ RepoBridge ============
    print("\n🔗 2. RepoBridge funksionon")
    from clisonix_ecosystem_bridge import RepoBridge

    bridge = RepoBridge("Kloud", m.ECOSYSTEM_REPOS["Kloud"])
    check("Bridge ID gjenerohet", len(bridge.bridge_id) == 16)
    check("Status inicial", bridge.status == "initialized")
    check(
        "Base URL", bridge.base_url == "http://localhost:9001", f"({bridge.base_url})"
    )

    pulse = bridge.send_pulse("active")
    check("Pulse dergohet", pulse["repo"] == "Kloud")
    check("Pulse ka hash", len(pulse["hash"]) == 16)
    check("Pulse ka timestamp", pulse["timestamp"] > 0)
    check("Last pulse ruhet", bridge.last_pulse is not None)

    status = bridge.get_status()
    check("Status ka repo", status["repo"] == "Kloud")
    check("Status ka language", status["language"] == "Python")
    check("Status ka role", status["role"] == "cloud")

    # ============ Ekosistem Bridge ============
    print("\n🌐 3. ClisonixEcosystemBridge funksionon")
    eco = m.ClisonixEcosystemBridge()
    check("Bridge per cdo repo", len(eco.bridges) == 15, f"({len(eco.bridges)})")
    check("Ecosystem ID", len(eco.ecosystem_id) == 16)

    # Pulse broadcast (pa ping per shpejtesi)
    pulses = eco.broadcast_pulse("active")
    check(
        "Broadcast pulse", pulses["total_pulses"] == 15, f"({pulses['total_pulses']})"
    )

    # Status pa ping
    status = eco.get_ecosystem_status()
    check("Status total_repos", status["total_repos"] == 15)
    check("Status ka repos", len(status["repos"]) == 15)
    check("Kloud ne status", "Kloud" in status["repos"])

    # Badges
    badges = eco.generate_readme_badges()
    check(
        "Badges gjenerohen",
        len(badges.split("\n")) == 15,
        f"({len(badges.split(chr(10)))} linja)",
    )

    # ============ Konfigurimi ============
    print("\n⚙️ 4. Konfigurimi i repos")
    langs = {cfg["language"] for cfg in m.ECOSYSTEM_REPOS.values()}
    check("Python ekziston", "Python" in langs)
    check("Go ekziston", "Go" in langs)
    check("TypeScript ekziston", "TypeScript" in langs)
    check("JavaScript ekziston", "JavaScript" in langs)
    check("HTML ekziston", "HTML" in langs)
    check("NodeDB Fluid ekziston", "NodeDB Fluid" in langs)

    # Portet unike
    ports = [cfg["port"] for cfg in m.ECOSYSTEM_REPOS.values()]
    check("Portet jane unike", len(set(ports)) == len(ports))

    # ============ Monitorimi ============
    print("\n💓 5. Monitorimi")
    started = eco.start_monitoring(interval=1)
    check("Monitorimi nis", started is not None and started["monitoring"])
    time.sleep(0.2)
    stopped = eco.stop_monitoring()
    check("Monitorimi ndalon", stopped["monitoring"] is False)

    # ============ Permbledhje ============
    print("\n" + "=" * 60)
    print(f"  REZULTATI: {passes} kaloi, {fails} deshtoi")
    print("=" * 60)
    return fails == 0


if __name__ == "__main__":
    ok = run_tests()
    sys.exit(0 if ok else 1)
