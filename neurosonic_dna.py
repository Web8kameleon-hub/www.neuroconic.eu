#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEUROSONIC DNA - I PANDrySHUESHëM
Kushtetuta, rregullat dhe identiteti i sistemit.

10 ligjet themelore + 43 rregulla të detajuara.
DNA nuk ndryshon kurrë pas inicializimit.
"""

import hashlib
import json
import time
from typing import Dict, List, Any, Optional


class NeurosonicDNA:
    """
    DNA e Neurosonic Trinity+ASI.

    Përmban:
    - 10 ligjet themelore (G001-G010)
    - 8 rregulla sigurie (SR001-SR008)
    - 5 rregulla data (DR001-DR005)
    - 4 rregulla API (AR001-AR004)
    - 6 rregulla memory (MR001-MR006)
    - 6 rregulla governance (GVR001-GVR006)
    - 5 rregulla quality (QR001-QR005)
    - 6 core values (CV001-CV006)
    """

    def __init__(self):
        self.name = "Neurosonic DNA v1.0"
        self.immutable = True
        self._created = time.time()
        self._hash = None

        # Inicializo rregullat
        self.rules = self._init_rules()

        # Gjenero hash-in e integritetit
        self._hash = self._compute_dna_hash()

        print(f"🧬 {self.name} inicializuar")
        print(f"   Hash: {self._hash}")

    def _init_rules(self) -> Dict[str, List[Dict]]:
        """Inicializon të gjitha rregullat e DNA-së"""
        return {
            "constitution": self._init_constitution_laws(),
            "security": self._init_security_rules(),
            "data": self._init_data_rules(),
            "api": self._init_api_rules(),
            "memory": self._init_memory_rules(),
            "governance": self._init_governance_rules(),
            "quality": self._init_quality_rules(),
            "core_values": self._init_core_values(),
        }

    def _init_constitution_laws(self) -> List[Dict]:
        return [
            {
                "id": "G001",
                "name": "Truth Law",
                "description": "Asnjë përgjigje e rreme. Çdo output ka burim të verifikueshëm.",
            },
            {
                "id": "G002",
                "name": "Privacy Law",
                "description": "Të dhënat e përdoruesit janë pronë e tij.",
            },
            {
                "id": "G003",
                "name": "Security Law",
                "description": "Kriptim në ruajtje dhe transmetim. Zero Trust.",
            },
            {
                "id": "G004",
                "name": "Modular Law",
                "description": "Çdo modul zëvendësohet pa prishur sistemin.",
            },
            {
                "id": "G005",
                "name": "Distributed Law",
                "description": "Çdo pajisje mund të bëhet Node.",
            },
            {
                "id": "G006",
                "name": "Memory Law",
                "description": "HVO memory: Horizontal, Vertical, Orbital, Resonance, Film, Stigma.",
            },
            {
                "id": "G007",
                "name": "Governance Law",
                "description": "Constitution mbi çdo modul. Human override.",
            },
            {
                "id": "G008",
                "name": "Economy Law",
                "description": "Internal auth, billing, wallet, license.",
            },
            {
                "id": "G009",
                "name": "Knowledge Law",
                "description": "Knowledge graph unik. Burime të verifikuara.",
            },
            {
                "id": "G010",
                "name": "Evolution Law",
                "description": "DNA nuk ndryshon. Genome zgjerohet. Evolution propozon.",
            },
        ]

    def _init_security_rules(self) -> List[Dict]:
        return [
            {"id": "SR001", "name": "Encryption at Rest", "mandatory": True},
            {"id": "SR002", "name": "Encryption in Transit", "mandatory": True},
            {"id": "SR003", "name": "Zero Trust Architecture", "mandatory": True},
            {"id": "SR004", "name": "DDoS Protection", "mandatory": True},
            {"id": "SR005", "name": "Audit Trail", "mandatory": True},
            {"id": "SR006", "name": "Internal Auth Only", "mandatory": True},
            {"id": "SR007", "name": "No External OAuth", "mandatory": True},
            {"id": "SR008", "name": "Immutable Logs", "mandatory": True},
        ]

    def _init_data_rules(self) -> List[Dict]:
        return [
            {"id": "DR001", "name": "User Data Ownership", "mandatory": True},
            {"id": "DR002", "name": "CUDM Compliance", "mandatory": True},
            {"id": "DR003", "name": "Source Verification", "mandatory": True},
            {"id": "DR004", "name": "Data Versioning", "mandatory": True},
            {"id": "DR005", "name": "Auto Cleanup", "mandatory": True},
        ]

    def _init_api_rules(self) -> List[Dict]:
        return [
            {"id": "AR001", "name": "Internal API First", "mandatory": True},
            {"id": "AR002", "name": "SSE Streaming Support", "mandatory": True},
            {"id": "AR003", "name": "CUDM Format Required", "mandatory": True},
            {"id": "AR004", "name": "Rate Limiting", "mandatory": True},
        ]

    def _init_memory_rules(self) -> List[Dict]:
        return [
            {"id": "MR001", "name": "HVO Base Required", "mandatory": True},
            {"id": "MR002", "name": "Resonance Memory", "mandatory": True},
            {"id": "MR003", "name": "Film Memory", "mandatory": True},
            {"id": "MR004", "name": "Stigma Memory", "mandatory": True},
            {"id": "MR005", "name": "Working Memory", "mandatory": True},
            {"id": "MR006", "name": "Long Term Memory", "mandatory": True},
        ]

    def _init_governance_rules(self) -> List[Dict]:
        return [
            {"id": "GVR001", "name": "Constitution Enforcement", "mandatory": True},
            {"id": "GVR002", "name": "Human Override Available", "mandatory": True},
            {"id": "GVR003", "name": "Emergency Stop", "mandatory": True},
            {"id": "GVR004", "name": "Policy Engine", "mandatory": True},
            {"id": "GVR005", "name": "Compliance Check", "mandatory": True},
            {"id": "GVR006", "name": "Audit Trail Active", "mandatory": True},
        ]

    def _init_quality_rules(self) -> List[Dict]:
        return [
            {"id": "QR001", "name": "Zero Hallucination", "mandatory": True},
            {"id": "QR002", "name": "3 Source Verification", "mandatory": True},
            {"id": "QR003", "name": "Hash Integrity", "mandatory": True},
            {"id": "QR004", "name": "Timestamp Required", "mandatory": True},
            {"id": "QR005", "name": "Confidence Score", "mandatory": True},
        ]

    def _init_core_values(self) -> List[Dict]:
        return [
            {"id": "CV001", "name": "Absolute Independence", "priority": 10},
            {"id": "CV002", "name": "Truth First", "priority": 9},
            {"id": "CV003", "name": "Privacy by Design", "priority": 8},
            {"id": "CV004", "name": "Modular Architecture", "priority": 7},
            {"id": "CV005", "name": "Distributed by Default", "priority": 6},
            {"id": "CV006", "name": "Human Centric", "priority": 10},
        ]

    def _compute_dna_hash(self) -> str:
        """Llogarit hash-in e integritetit të DNA-së"""
        data = json.dumps(self.rules, sort_keys=True, default=str)
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    def get_all_rules(self) -> Dict[str, List]:
        """Kthen të gjitha rregullat"""
        return self.rules

    def get_stats(self) -> Dict[str, int]:
        """Statistika të DNA-së"""
        total = sum(len(v) for v in self.rules.values())
        return {
            "total_rules": total,
            "constitution": len(self.rules["constitution"]),
            "security": len(self.rules["security"]),
            "data": len(self.rules["data"]),
            "api": len(self.rules["api"]),
            "memory": len(self.rules["memory"]),
            "governance": len(self.rules["governance"]),
            "quality": len(self.rules["quality"]),
            "core_values": len(self.rules["core_values"]),
        }

    def verify_module(self, module_id: str, module_config: Dict) -> Dict[str, Any]:
        """Verifikon nëse një modul përputhet me DNA-në"""
        violations = []

        # Kontrollo constitution
        required_constitution = [law["id"] for law in self.rules["constitution"]]
        provided_constitution = module_config.get("constitution_compatibility", [])
        for law_id in required_constitution:
            if law_id not in provided_constitution:
                violations.append(f"Missing constitution law: {law_id}")

        # Kontrollo security
        required_security = [rule["id"] for rule in self.rules["security"]]
        provided_security = module_config.get("security_compatibility", [])
        for rule_id in required_security:
            if rule_id not in provided_security:
                violations.append(f"Missing security rule: {rule_id}")

        # Kontrollo data
        required_data = [rule["id"] for rule in self.rules["data"]]
        provided_data = module_config.get("data_compatibility", [])
        for rule_id in required_data:
            if rule_id not in provided_data:
                violations.append(f"Missing data rule: {rule_id}")

        # Kontrollo API
        required_api = [rule["id"] for rule in self.rules["api"]]
        provided_api = module_config.get("api_compatibility", [])
        for rule_id in required_api:
            if rule_id not in provided_api:
                violations.append(f"Missing API rule: {rule_id}")

        return {
            "module_id": module_id,
            "compatible": len(violations) == 0,
            "violations": violations,
            "hash": hashlib.sha256(f"{module_id}{time.time()}".encode()).hexdigest()[
                :12
            ],
        }

    def verify_constitution_action(self, action: str, context: str) -> bool:
        """Verifikon nëse një veprim lejohet nga Kushtetuta"""
        # Ligji 2 (Privacy): user data nuk dërgohet jashtë pa autorizim
        if action == "send_to_external" and context == "module":
            return False
        if action == "send_to_external" and context == "api_public":
            return True

        # Ligji 3 (Security): kriptim i detyrueshëm
        if action == "send_unencrypted":
            return False

        # Ligji 2 (Privacy): përdoruesi mund të fshijë të dhënat e veta
        if action == "delete_user_data" and context == "user_self":
            return True
        if action == "delete_user_data" and context == "system":
            return False

        return True


# Test i shpejtë
if __name__ == "__main__":
    dna = NeurosonicDNA()
    print(f"\n📊 Statistikat: {dna.get_stats()}")
    print(f"🔐 Hash: {dna._hash}")
    print(f"✅ DNA gati!")
