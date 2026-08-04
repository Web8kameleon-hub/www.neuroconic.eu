#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEUROSONIC DNA - I PANDrySHUESHëM
Identiteti i sistemit. Ndryshon VETËM me Governance Approval.

Niveli 1 i Arkitekturës Neurosonic Trinity+ASI
"""

import hashlib
import datetime
import json
from typing import Dict, Any, List, Optional


class NeurosonicDNA:
    """Identiteti i sistemit - BIOS-i i Neurosonic"""

    # ========================================================================
    # CONSTITUTION - 10 LIGJET THEMELORE
    # ========================================================================

    CONSTITUTION = {
        "G001": {"name": "Truth Law", "text": "No Fake. No fabricated knowledge."},
        "G002": {
            "name": "Sovereignty Law",
            "text": "Maximum Independence. Zero vendor lock-in.",
        },
        "G003": {
            "name": "User Ownership Law",
            "text": "User owns User Data. User owns Identity.",
        },
        "G004": {
            "name": "Internal Infrastructure Law",
            "text": "Everything critical built internally.",
        },
        "G005": {
            "name": "Modular Law",
            "text": "Every component is a module. Every module can be replaced.",
        },
        "G006": {
            "name": "Distributed Law",
            "text": "No Central Brain. Every Device = Cognitive Node.",
        },
        "G007": {
            "name": "Security Law",
            "text": "Zero Trust. Encryption Everywhere.",
        },
        "G008": {
            "name": "Intelligence Law",
            "text": "Every intelligence passes through validation.",
        },
        "G009": {
            "name": "Knowledge Law",
            "text": "Unified Data Model. Knowledge Graph. Versioned Knowledge.",
        },
        "G010": {
            "name": "Evolution Law",
            "text": "System never stops evolving. Backward Compatible.",
        },
    }

    # ========================================================================
    # CORE VALUES - VLERAT THEMELORE
    # ========================================================================

    CORE_VALUES = {
        "truth": "Absolute commitment to truth and accuracy.",
        "independence": "No external dependencies. Self-sufficient.",
        "privacy": "User data is sacred. Never shared without consent.",
        "security": "Security by design. Zero Trust.",
        "transparency": "Every decision explainable. Every action auditable.",
        "human_centric": "AI serves humans. Human override always possible.",
    }

    # ========================================================================
    # SECURITY RULES - RREGULLAT E SIGURISË
    # ========================================================================

    SECURITY_RULES = {
        "SR001": "Zero Trust Architecture - verify everything.",
        "SR002": "Encryption at Rest - all data encrypted.",
        "SR003": "Encryption in Transit - all communication encrypted.",
        "SR004": "Immutable Audit Logs - no logs can be deleted.",
        "SR005": "AI Safety - all AI actions validated before execution.",
        "SR006": "Privacy by Design - privacy built into every component.",
        "SR007": "Human Override - humans can override any AI decision.",
        "SR008": "Emergency Stop - system can be shut down immediately.",
    }

    # ========================================================================
    # DATA RULES - RREGULLAT E TË DHËNAVE
    # ========================================================================

    DATA_RULES = {
        "DR001": "Unified Data Model - all modules use the same data format.",
        "DR002": "User Data Ownership - user owns their data.",
        "DR003": "Data Portability - data can be exported anytime.",
        "DR004": "Data Deletion - user can delete data anytime.",
        "DR005": "Data Sovereignty - data stored according to local laws.",
    }

    # ========================================================================
    # API RULES - RREGULLAT E API-VE
    # ========================================================================

    API_RULES = {
        "AR001": "Internal API - all internal communication via internal API.",
        "AR002": "External API - external communication via public API only.",
        "AR003": "Versioned API - all APIs versioned. No breaking changes.",
        "AR004": "Secure API - all API calls authenticated and encrypted.",
    }

    # ========================================================================
    # MEMORY RULES - RREGULLAT E MEMORIES
    # ========================================================================

    MEMORY_RULES = {
        "MR001": "HVO Memory - Horizontal, Vertical, Orbital.",
        "MR002": "Resonance Memory - weighted by importance.",
        "MR003": "Film Memory - process history stored.",
        "MR004": "Stigma Memory - learning from experience.",
        "MR005": "Working Memory - current task context.",
        "MR006": "Long Term Memory - permanent knowledge storage.",
    }

    # ========================================================================
    # GOVERNANCE RULES - RREGULLAT E QEVERISJES
    # ========================================================================

    GOVERNANCE_RULES = {
        "GR001": "Constitution Above All - no module violates constitution.",
        "GR002": "Policy Engine - all actions governed by policies.",
        "GR003": "Audit Trail - every action auditable.",
        "GR004": "Explainability - every AI decision explainable.",
        "GR005": "Human Oversight - critical decisions require human approval.",
        "GR006": "Emergency Protocols - defined procedures for emergencies.",
    }

    # ========================================================================
    # QUALITY RULES - RREGULLAT E CILËSISË
    # ========================================================================

    QUALITY_RULES = {
        "QR001": "Zero Fake - no fabricated information.",
        "QR002": "Zero Hallucination - all outputs verified.",
        "QR003": "Zero Noise - clean data only.",
        "QR004": "Source Verification - every fact has source.",
        "QR005": "Hash Verification - every response has hash.",
    }

    def __init__(self):
        self.name = "Neurosonic DNA v1.0"
        self.version = "1.0.0"
        self.immutable = True  # DNA nuk ndryshon automatikisht
        self.created = datetime.datetime.now().isoformat()
        self._hash = self._compute_dna_hash()

    def _compute_dna_hash(self) -> str:
        """Llogarit hash-in e DNA-së për verifikim integriteti"""
        all_rules = self.get_all_rules()
        hash_input = json.dumps(all_rules, sort_keys=True)
        return hashlib.sha256(hash_input.encode()).hexdigest()[:16]

    def get_all_rules(self) -> Dict[str, Any]:
        """Kthe të gjitha rregullat si dictionary"""
        return {
            "constitution": self.CONSTITUTION,
            "core_values": self.CORE_VALUES,
            "security": self.SECURITY_RULES,
            "data": self.DATA_RULES,
            "api": self.API_RULES,
            "memory": self.MEMORY_RULES,
            "governance": self.GOVERNANCE_RULES,
            "quality": self.QUALITY_RULES,
        }

    def verify_module(self, module_id: str, module_config: Dict) -> Dict[str, Any]:
        """
        Verifikon nëse moduli përputhet me DNA-në.

        Args:
            module_id: ID e modulit
            module_config: Konfigurimi i modulit

        Returns:
            Dict me rezultatin e verifikimit
        """
        results = {"module_id": module_id, "compatible": True, "violations": []}

        # Kontrollo përputhjen me Kushtetutën
        for gene_id in self.CONSTITUTION:
            if gene_id not in module_config.get("constitution_compatibility", []):
                results["violations"].append(
                    f"Mungon përputhja me Kushtetutën: {gene_id} - {self.CONSTITUTION[gene_id]['name']}"
                )
                results["compatible"] = False

        # Kontrollo përputhjen me sigurinë
        for rule_id in self.SECURITY_RULES:
            if rule_id not in module_config.get("security_compatibility", []):
                results["violations"].append(
                    f"Mungon rregulla sigurie: {rule_id} - {self.SECURITY_RULES[rule_id]}"
                )
                results["compatible"] = False

        # Kontrollo përputhjen me të dhënat
        for rule_id in self.DATA_RULES:
            if rule_id not in module_config.get("data_compatibility", []):
                results["violations"].append(
                    f"Mungon rregulla e të dhënave: {rule_id} - {self.DATA_RULES[rule_id]}"
                )
                results["compatible"] = False

        # Kontrollo përputhjen me API-të
        for rule_id in self.API_RULES:
            if rule_id not in module_config.get("api_compatibility", []):
                results["violations"].append(
                    f"Mungon rregulla API: {rule_id} - {self.API_RULES[rule_id]}"
                )
                results["compatible"] = False

        return results

    def verify_constitution_action(self, action: str, module: str) -> bool:
        """
        Kontrollon nëse një veprim specifik përputhet me Kushtetutën.

        Args:
            action: Veprimi që do të kryhet
            module: Moduli që kërkon veprimin

        Returns:
            True nëse veprimi lejohet, False nëse bllokohet
        """
        # Rregulli G002: SOVRANITETI - asnjë modul nuk dërgon të dhëna jashtë pa autorizim
        if "send_to_external" in action.lower() and module != "api_public":
            return False

        # Rregulli G003: USER OWNERSHIP - nuk lejohet fshirja e të dhënave pa autorizim
        if "delete_user_data" in action.lower() and module not in [
            "governance",
            "user_self",
        ]:
            return False

        # Rregulli G007: SECURITY - kriptimi është i detyrueshëm
        if "send_unencrypted" in action.lower():
            return False

        return True

    def get_core_values_summary(self) -> str:
        """Kthen përmbledhjen e vlerave themelore"""
        summary = "🧬 NEUROSONIC CORE VALUES:\n"
        for key, value in self.CORE_VALUES.items():
            summary += f"  • {key.upper()}: {value}\n"
        return summary

    def get_stats(self) -> Dict[str, Any]:
        """Statistika të DNA-së"""
        return {
            "name": self.name,
            "version": self.version,
            "immutable": self.immutable,
            "hash": self._hash,
            "created": self.created,
            "total_constitution_laws": len(self.CONSTITUTION),
            "total_core_values": len(self.CORE_VALUES),
            "total_security_rules": len(self.SECURITY_RULES),
            "total_data_rules": len(self.DATA_RULES),
            "total_api_rules": len(self.API_RULES),
            "total_memory_rules": len(self.MEMORY_RULES),
            "total_governance_rules": len(self.GOVERNANCE_RULES),
            "total_quality_rules": len(self.QUALITY_RULES),
            "total_rules": (
                len(self.CONSTITUTION)
                + len(self.CORE_VALUES)
                + len(self.SECURITY_RULES)
                + len(self.DATA_RULES)
                + len(self.API_RULES)
                + len(self.MEMORY_RULES)
                + len(self.GOVERNANCE_RULES)
                + len(self.QUALITY_RULES)
            ),
        }


# Test i shpejtë
if __name__ == "__main__":
    dna = NeurosonicDNA()
    print(dna.get_core_values_summary())
    print(f"📊 Stats: {json.dumps(dna.get_stats(), indent=2)}")
