#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEUROSONIC GENOME - ZGJEROHET
Paketat që shtojnë aftësi pa prekur DNA-në.

NGI (Neurosonic Genome Index) - Indeksi i unifikuar i paketave.
"""

import hashlib
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class GenomePackage:
    """Një paketë në Genome"""

    id: str
    name: str
    description: str
    version: str
    author: str
    dependencies: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    category: str = "core"
    installed: bool = True
    installed_at: float = 0.0


class NeurosonicGenome:
    """
    Genome e Neurosonic - përmban të gjitha paketat e instaluara.

    Karakteristikat:
    - Zgjerohet (shtohen paketa të reja)
    - Varësitë kontrollohen
    - NGI indeks unik
    - Kategorizim automatik
    """

    def __init__(self):
        self.name = "Neurosonic Genome v1.0"
        self.packages: Dict[str, GenomePackage] = {}
        self._init_core_packages()
        print(f"📦 {self.name} inicializuar")
        print(f"   {len(self.packages)} paketa themelore")

    def _init_core_packages(self):
        """Inicializon paketat themelore të Genome-së"""
        core_packages = [
            # CORE - Bërthama
            GenomePackage(
                "NGI-CORE-0001",
                "CLX Kernel",
                "Runtime themelor i sistemit",
                "1.0.0",
                "Neurosonic Labs",
                dependencies=[],
                capabilities=["runtime", "scheduler", "memory_manager"],
                category="core",
            ),
            GenomePackage(
                "NGI-CORE-0002",
                "NodeDB Fluid",
                "Database adaptiv",
                "1.0.0",
                "Neurosonic Labs",
                dependencies=["NGI-CORE-0001"],
                capabilities=["storage", "query", "sync"],
                category="core",
            ),
            GenomePackage(
                "NGI-CORE-0003",
                "Internal Auth",
                "Autentifikim i brendshëm",
                "1.0.0",
                "Neurosonic Labs",
                dependencies=["NGI-CORE-0001"],
                capabilities=["auth", "token", "session"],
                category="core",
            ),
            # AI - Inteligjenca
            GenomePackage(
                "NGI-AI-0004",
                "CLX LLM",
                "Model gjuhësor",
                "1.0.0",
                "Neurosonic Labs",
                dependencies=["NGI-CORE-0001"],
                capabilities=["llm", "reasoning", "generation"],
                category="ai",
            ),
            GenomePackage(
                "NGI-AI-0005",
                "CLX.I (LLaVA)",
                "Model vizual",
                "1.0.0",
                "Neurosonic Labs",
                dependencies=["NGI-AI-0004"],
                capabilities=["vision", "ocr", "image_analysis"],
                category="ai",
            ),
            GenomePackage(
                "NGI-AI-0006",
                "Reasoning Engine",
                "Arsyetim logjik",
                "1.0.0",
                "Neurosonic Labs",
                dependencies=["NGI-AI-0004"],
                capabilities=["logic", "planning", "reflection"],
                category="ai",
            ),
            # MEMORY - Kujtesa
            GenomePackage(
                "NGI-MEM-0007",
                "HVO Memory Base",
                "Baza e memories HVO",
                "1.0.0",
                "Neurosonic Labs",
                dependencies=["NGI-CORE-0001"],
                capabilities=["horizontal", "vertical", "orbital"],
                category="memory",
            ),
            GenomePackage(
                "NGI-MEM-0008",
                "Resonance Memory",
                "Kujtesë me peshë prioritare",
                "1.0.0",
                "Neurosonic Labs",
                dependencies=["NGI-MEM-0007"],
                capabilities=["resonance", "weighting"],
                category="memory",
            ),
            GenomePackage(
                "NGI-MEM-0009",
                "Stigma Memory",
                "Mësim nga eksperienca",
                "1.0.0",
                "Neurosonic Labs",
                dependencies=["NGI-MEM-0007"],
                capabilities=["stigma", "experience"],
                category="memory",
            ),
            # AGENTS - Agjentët
            GenomePackage(
                "NGI-AGENT-0045",
                "Research Agent",
                "Agjent kërkimi",
                "1.0.0",
                "Neurosonic Labs",
                dependencies=["NGI-AI-0004"],
                capabilities=["research", "web_search", "verification"],
                category="agent",
            ),
            GenomePackage(
                "NGI-AGENT-0046",
                "Country Agent",
                "Agjent për shtete",
                "1.0.0",
                "Neurosonic Labs",
                dependencies=["NGI-AGENT-0045"],
                capabilities=["country_data", "open_data", "local_laws"],
                category="agent",
            ),
            GenomePackage(
                "NGI-AGENT-0047",
                "Security Agent",
                "Agjent sigurie",
                "1.0.0",
                "Neurosonic Labs",
                dependencies=["NGI-CORE-0001"],
                capabilities=["ddos", "ids", "encryption"],
                category="agent",
            ),
            # SECURITY - Siguria
            GenomePackage(
                "NGI-SEC-0012",
                "Security Fabric",
                "Shtresa e sigurisë",
                "1.0.0",
                "Neurosonic Labs",
                dependencies=["NGI-CORE-0001"],
                capabilities=["zero_trust", "encryption", "audit"],
                category="security",
            ),
            GenomePackage(
                "NGI-SEC-0013",
                "DDoS Shield",
                "Mbrojtje nga sulmet",
                "1.0.0",
                "Neurosonic Labs",
                dependencies=["NGI-SEC-0012"],
                capabilities=["ddos", "rate_limit", "blacklist"],
                category="security",
            ),
            # TIDE - Batica/Zbatica
            GenomePackage(
                "NGI-TIDE-0034",
                "Tide Engine",
                "Kontroll i ritmit",
                "1.0.0",
                "Neurosonic Labs",
                dependencies=["NGI-CORE-0001"],
                capabilities=["load_balancing", "adaptive_flow"],
                category="tide",
            ),
            GenomePackage(
                "NGI-TIDE-0035",
                "SSE Stream Engine",
                "Transmetim i shpejtë",
                "1.0.0",
                "Neurosonic Labs",
                dependencies=["NGI-TIDE-0034"],
                capabilities=["streaming", "chunks", "real_time"],
                category="tide",
            ),
            # LIGHTNING - Integrimi Lightning SPP 3.14
            GenomePackage(
                "NGI-LIGHTNING-1001",
                "Lightning SPP Bridge",
                "Bridge me Lightning SPP 3.14",
                "1.0.0",
                "Neurosonic Labs",
                dependencies=["NGI-CORE-0001"],
                capabilities=[
                    "scan",
                    "process",
                    "print",
                    "tidewave",
                    "resonance",
                    "stigma",
                ],
                category="lightning",
            ),
            GenomePackage(
                "NGI-LIGHTNING-1002",
                "Lightning Pipeline",
                "Pipeline i plotë Scan-Process-Print",
                "1.0.0",
                "Neurosonic Labs",
                dependencies=["NGI-LIGHTNING-1001"],
                capabilities=["pipeline", "batch", "hybrid"],
                category="lightning",
            ),
            GenomePackage(
                "NGI-LIGHTNING-1003",
                "Lightning Profiles",
                "Profile për Medical, Mobile, IoT, Cloud, Desktop",
                "1.0.0",
                "Neurosonic Labs",
                dependencies=["NGI-LIGHTNING-1001"],
                capabilities=["profiles", "optimization", "device_adaptation"],
                category="lightning",
            ),
        ]

        now = time.time()
        for pkg in core_packages:
            pkg.installed_at = now
            self.packages[pkg.id] = pkg

    def get_package(self, package_id: str) -> Optional[Dict]:
        """Merr një paketë nga Genome"""
        pkg = self.packages.get(package_id)
        if pkg:
            return {
                "id": pkg.id,
                "name": pkg.name,
                "description": pkg.description,
                "version": pkg.version,
                "author": pkg.author,
                "dependencies": pkg.dependencies,
                "capabilities": pkg.capabilities,
                "category": pkg.category,
            }
        return None

    def add_package(self, package: GenomePackage) -> Dict[str, Any]:
        """Shton një paketë të re në Genome"""
        # Kontrollo nëse ekziston
        if package.id in self.packages:
            return {"success": False, "message": f"Package {package.id} already exists"}

        # Kontrollo varësitë
        for dep_id in package.dependencies:
            if dep_id not in self.packages:
                return {
                    "success": False,
                    "message": f"Dependency {dep_id} not found for {package.id}",
                }

        # Shto paketën
        package.installed_at = time.time()
        self.packages[package.id] = package
        return {
            "success": True,
            "message": f"Package {package.name} v{package.version} installed",
        }

    def remove_package(self, package_id: str) -> Dict[str, Any]:
        """Heq një paketë nga Genome"""
        if package_id not in self.packages:
            return {"success": False, "message": f"Package {package_id} not found"}

        # Kontrollo nëse ka varësi nga paketa të tjera
        for pkg_id, pkg in self.packages.items():
            if package_id in pkg.dependencies:
                return {
                    "success": False,
                    "message": f"Cannot remove {package_id}: dependency of {pkg_id}",
                }

        del self.packages[package_id]
        return {"success": True, "message": f"Package {package_id} removed"}

    def get_packages_by_category(self) -> Dict[str, List[str]]:
        """Kthen paketat e grupuara sipas kategorisë"""
        categories = {}
        for pkg_id, pkg in self.packages.items():
            if pkg.category not in categories:
                categories[pkg.category] = []
            categories[pkg.category].append(pkg_id)
        return categories

    def get_stats(self) -> Dict[str, Any]:
        """Statistika të Genome-së"""
        categories = self.get_packages_by_category()
        return {
            "total_packages": len(self.packages),
            "categories": {cat: len(pkgs) for cat, pkgs in categories.items()},
            "package_ids": list(self.packages.keys()),
        }


# Test i shpejtë
if __name__ == "__main__":
    genome = NeurosonicGenome()
    print(f"\n📊 Statistikat: {genome.get_stats()}")
    print(f"✅ Genome gati!")
