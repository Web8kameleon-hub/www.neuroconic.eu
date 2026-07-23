#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEUROSONIC GENOME - ZGJEROHET
Aftësitë e sistemit. Shtohen ose hiqen pa prekur DNA-në.

Niveli 2 i Arkitekturës Neurosonic Trinity+ASI
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import datetime
import json


@dataclass
class GenomePackage:
    """Një paketë genome - zgjeron aftësitë e sistemit"""

    id: str
    name: str
    description: str
    version: str
    author: str
    dependencies: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    ngi_compatibility: List[str] = field(default_factory=list)
    installed_at: str = ""


class NeurosonicGenome:
    """Genome i Neurosonic - Zgjerohet me paketa"""

    def __init__(self):
        self.packages: Dict[str, GenomePackage] = {}
        self._load_core_packages()

    def _load_core_packages(self):
        """Ngarko paketat themelore"""
        core_packages = [
            GenomePackage(
                id="NGI-CORE-0001",
                name="CLX Kernel",
                description="Bërthama e Neurosonic - Runtime dhe Scheduler",
                version="1.0.0",
                author="Neurosonic",
                dependencies=[],
                capabilities=["runtime", "scheduler", "memory_manager", "node_manager"],
                ngi_compatibility=["DNA-ALL"],
            ),
            GenomePackage(
                id="NGI-CORE-0002",
                name="NodeDB Fluid",
                description="Database adaptiv që përshtatet me çdo strukturë",
                version="1.0.0",
                author="Neurosonic",
                dependencies=["NGI-CORE-0001"],
                capabilities=["json_storage", "backup", "search", "sync"],
                ngi_compatibility=["DNA-ALL"],
            ),
            GenomePackage(
                id="NGI-CORE-0003",
                name="Internal Auth",
                description="Autentifikim i brendshëm - pa OAuth",
                version="1.0.0",
                author="Neurosonic",
                dependencies=["NGI-CORE-0001"],
                capabilities=["token_auth", "role_management", "session_management"],
                ngi_compatibility=["DNA-ALL"],
            ),
            GenomePackage(
                id="NGI-AI-0004",
                name="CLX LLM",
                description="Large Language Model - tekst dhe arsyetim",
                version="1.0.0",
                author="Neurosonic",
                dependencies=["NGI-CORE-0001"],
                capabilities=[
                    "text_generation",
                    "reasoning",
                    "coding",
                    "scientific_analysis",
                ],
                ngi_compatibility=["DNA-ALL"],
            ),
            GenomePackage(
                id="NGI-AI-0005",
                name="CLX.I (LLaVA)",
                description="Vision Model - imazhe, video, dokumente",
                version="1.0.0",
                author="Neurosonic",
                dependencies=["NGI-CORE-0001", "NGI-AI-0004"],
                capabilities=[
                    "image_understanding",
                    "ocr",
                    "video_analysis",
                    "document_analysis",
                ],
                ngi_compatibility=["DNA-ALL"],
            ),
            GenomePackage(
                id="NGI-AI-0006",
                name="Reasoning Engine",
                description="Arsyetim logjik dhe analizë e thellë",
                version="1.0.0",
                author="Neurosonic",
                dependencies=["NGI-CORE-0001", "NGI-AI-0004"],
                capabilities=[
                    "logical_reasoning",
                    "planning",
                    "reflection",
                    "self_correction",
                ],
                ngi_compatibility=["DNA-ALL"],
            ),
            GenomePackage(
                id="NGI-MEM-0002",
                name="HVO Memory",
                description="Horizontal, Vertical, Orbital Memory",
                version="1.0.0",
                author="Neurosonic",
                dependencies=["NGI-CORE-0001"],
                capabilities=["hvo_memory", "resonance", "film", "stigma"],
                ngi_compatibility=["DNA-ALL"],
            ),
            GenomePackage(
                id="NGI-MEM-0007",
                name="Resonance Memory",
                description="Kujtim me peshë sipas rëndësisë",
                version="1.0.0",
                author="Neurosonic",
                dependencies=["NGI-MEM-0002"],
                capabilities=["weighted_memory", "priority_ranking"],
                ngi_compatibility=["DNA-ALL"],
            ),
            GenomePackage(
                id="NGI-AGENT-0045",
                name="Research Agent",
                description="Agjent kërkimi për web",
                version="1.0.0",
                author="Neurosonic",
                dependencies=["NGI-CORE-0001", "NGI-AI-0004"],
                capabilities=["web_search", "data_verification", "source_cross_check"],
                ngi_compatibility=["DNA-ALL"],
            ),
            GenomePackage(
                id="NGI-AGENT-0046",
                name="Country Agent",
                description="Agjent për shtet - lidhje me open data",
                version="1.0.0",
                author="Neurosonic",
                dependencies=["NGI-CORE-0001", "NGI-AI-0004"],
                capabilities=["open_data_access", "government_apis", "local_laws"],
                ngi_compatibility=["DNA-ALL"],
            ),
            GenomePackage(
                id="NGI-AGENT-0047",
                name="Protocol Agent",
                description="Krijim protokollesh të reja kur mungojnë",
                version="1.0.0",
                author="Neurosonic",
                dependencies=["NGI-CORE-0001"],
                capabilities=["protocol_generation", "standard_creation"],
                ngi_compatibility=["DNA-ALL"],
            ),
            GenomePackage(
                id="NGI-SEC-0012",
                name="Security Fabric",
                description="Siguria e sistemit - DDoS, Encryption, Zero Trust",
                version="1.0.0",
                author="Neurosonic",
                dependencies=["NGI-CORE-0001"],
                capabilities=[
                    "ddos_protection",
                    "encryption",
                    "zero_trust",
                    "audit_trail",
                ],
                ngi_compatibility=["DNA-ALL"],
            ),
            GenomePackage(
                id="NGI-COM-0023",
                name="SSE Engine",
                description="Streaming i shpejtë me Server-Sent Events",
                version="1.0.0",
                author="Neurosonic",
                dependencies=["NGI-CORE-0001"],
                capabilities=["sse_streaming", "real_time", "chunked_transfer"],
                ngi_compatibility=["DNA-ALL"],
            ),
            GenomePackage(
                id="NGI-COM-0024",
                name="Mesh Engine",
                description="Rrjet i shpërndarë node-to-node",
                version="1.0.0",
                author="Neurosonic",
                dependencies=["NGI-CORE-0001"],
                capabilities=["mesh_networking", "node_discovery", "p2p_communication"],
                ngi_compatibility=["DNA-ALL"],
            ),
            GenomePackage(
                id="NGI-TIDE-0030",
                name="Tide Engine",
                description="Batica/Zbatica - kontroll ritmi të rrjetit",
                version="1.0.0",
                author="Neurosonic",
                dependencies=["NGI-CORE-0001"],
                capabilities=[
                    "load_balancing",
                    "adaptive_flow",
                    "predictive_scaling",
                    "congestion_control",
                ],
                ngi_compatibility=["DNA-ALL"],
            ),
            GenomePackage(
                id="NGI-GOV-0050",
                name="Governance Engine",
                description="Qeverisje dhe zbatim rregullash",
                version="1.0.0",
                author="Neurosonic",
                dependencies=["NGI-CORE-0001"],
                capabilities=[
                    "policy_enforcement",
                    "compliance_check",
                    "audit",
                    "human_override",
                ],
                ngi_compatibility=["DNA-ALL"],
            ),
            GenomePackage(
                id="NGI-ECO-0060",
                name="Internal Economy",
                description="Ekonomi e brendshme - billing, wallet, license",
                version="1.0.0",
                author="Neurosonic",
                dependencies=["NGI-CORE-0001", "NGI-CORE-0003"],
                capabilities=["billing", "wallet", "license_management", "marketplace"],
                ngi_compatibility=["DNA-ALL"],
            ),
        ]

        now = datetime.datetime.now().isoformat()
        for pkg in core_packages:
            pkg.installed_at = now
            self.packages[pkg.id] = pkg

    def add_package(self, package: GenomePackage) -> Dict[str, Any]:
        """
        Shto një paketë të re.

        Args:
            package: Paketa për t'u shtuar

        Returns:
            Dict me status dhe mesazh
        """
        if package.id in self.packages:
            return {"success": False, "message": f"Package {package.id} already exists"}

        # Kontrollo nëse varësitë ekzistojnë
        for dep in package.dependencies:
            if dep not in self.packages:
                return {
                    "success": False,
                    "message": f"Dependency {dep} not found for {package.id}",
                }

        package.installed_at = datetime.datetime.now().isoformat()
        self.packages[package.id] = package
        return {
            "success": True,
            "message": f"Package {package.name} v{package.version} installed",
        }

    def remove_package(self, package_id: str) -> Dict[str, Any]:
        """
        Hiq një paketë.

        Args:
            package_id: ID e paketës për t'u hequr

        Returns:
            Dict me status dhe mesazh
        """
        if package_id not in self.packages:
            return {"success": False, "message": f"Package {package_id} not found"}

        # Kontrollo nëse ka varësi nga kjo paketë
        for pkg in self.packages.values():
            if package_id in pkg.dependencies:
                return {
                    "success": False,
                    "message": f"Cannot remove {package_id}: dependency of {pkg.id}",
                }

        removed = self.packages[package_id]
        del self.packages[package_id]
        return {"success": True, "message": f"Package {removed.name} removed"}

    def get_package(self, package_id: str) -> Dict[str, Any]:
        """Merr një paketë specifike"""
        if package_id in self.packages:
            pkg = self.packages[package_id]
            return {
                "id": pkg.id,
                "name": pkg.name,
                "description": pkg.description,
                "version": pkg.version,
                "author": pkg.author,
                "dependencies": pkg.dependencies,
                "capabilities": pkg.capabilities,
                "installed_at": pkg.installed_at,
            }
        return {}

    def list_packages(self) -> List[Dict[str, Any]]:
        """Listo të gjitha paketat"""
        return [self.get_package(pkg_id) for pkg_id in sorted(self.packages.keys())]

    def get_packages_by_category(self) -> Dict[str, List[Dict[str, Any]]]:
        """Grupon paketat sipas kategorisë (nga prefiksi NGI)"""
        categories = {
            "core": [],
            "ai": [],
            "memory": [],
            "agent": [],
            "security": [],
            "communication": [],
            "tide": [],
            "governance": [],
            "economy": [],
            "other": [],
        }

        category_map = {
            "NGI-CORE": "core",
            "NGI-AI": "ai",
            "NGI-MEM": "memory",
            "NGI-AGENT": "agent",
            "NGI-SEC": "security",
            "NGI-COM": "communication",
            "NGI-TIDE": "tide",
            "NGI-GOV": "governance",
            "NGI-ECO": "economy",
        }

        for pkg_id, pkg in self.packages.items():
            prefix = "-".join(pkg_id.split("-")[:2])
            category = category_map.get(prefix, "other")
            categories[category].append(self.get_package(pkg_id))

        return categories

    def get_stats(self) -> Dict[str, Any]:
        """Statistika të genome-së"""
        return {
            "total_packages": len(self.packages),
            "categories": {
                cat: len(pkgs) for cat, pkgs in self.get_packages_by_category().items()
            },
            "core_packages": len(
                [p for p in self.packages.values() if p.id.startswith("NGI-CORE")]
            ),
            "latest_package": max(
                (p.installed_at for p in self.packages.values()), default=""
            ),
        }


# Test i shpejtë
if __name__ == "__main__":
    genome = NeurosonicGenome()
    print(f"📦 Total packages: {genome.get_stats()['total_packages']}")
    print(f"\n📋 Package list:")
    for pkg in genome.list_packages():
        print(f"   {pkg['id']}: {pkg['name']} v{pkg['version']}")
