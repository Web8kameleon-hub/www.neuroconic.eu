#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEUROSONIC EVOLUTION ENGINE - PROPOZON, NUK NDRYSHON
Analizon arkitekturën, zbulon konflikte, sugjeron optimizime.

Niveli 3 i Arkitekturës Neurosonic Trinity+ASI
"""

import time
import datetime
import hashlib
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from neurosonic_dna import NeurosonicDNA
from neurosonic_genome import NeurosonicGenome


@dataclass
class EvolutionProposal:
    """Një propozim për evoluim"""

    id: str
    description: str
    timestamp: float
    status: str  # proposed, analyzing, approved, rejected
    analysis: Dict[str, Any] = field(default_factory=dict)
    votes_for: int = 0
    votes_against: int = 0


@dataclass
class ArchitectureAnalysis:
    """Analizë e arkitekturës"""

    dna_integrity: bool
    genome_coverage: Dict[str, Any]
    potential_conflicts: List[Dict[str, Any]]
    optimization_suggestions: List[str]
    timestamp: float


class NeurosonicEvolutionEngine:
    """
    Evolution Engine - propozon ndryshime, por nuk i zbaton.

    Funksionet:
    1. Analizon arkitekturën
    2. Zbulon konflikte
    3. Sugjeron optimizime
    4. Propozon rregulla të reja
    5. Krijon versione për shqyrtim

    DNA nuk ndryshon vetë. Evolution Engine VETËM propozon.
    """

    def __init__(self, dna: NeurosonicDNA, genome: NeurosonicGenome):
        self.dna = dna
        self.genome = genome
        self.proposals: List[EvolutionProposal] = []
        self.analysis_history: List[ArchitectureAnalysis] = []

    def analyze_architecture(self) -> Dict[str, Any]:
        """Analizon arkitekturën aktuale dhe kthen rezultate"""
        analysis = ArchitectureAnalysis(
            dna_integrity=self._check_dna_integrity(),
            genome_coverage=self._check_genome_coverage(),
            potential_conflicts=self._find_conflicts(),
            optimization_suggestions=self._suggest_optimizations(),
            timestamp=time.time(),
        )
        self.analysis_history.append(analysis)

        return {
            "dna_integrity": analysis.dna_integrity,
            "genome_coverage": analysis.genome_coverage,
            "potential_conflicts": analysis.potential_conflicts,
            "optimization_suggestions": analysis.optimization_suggestions,
            "timestamp": analysis.timestamp,
        }

    def propose_new_rule(
        self,
        description: str,
        category: str = "governance",
        impact_level: str = "medium",
    ) -> Dict[str, Any]:
        """
        Propozon një rregull të ri.

        Args:
            description: Përshkrimi i rregullit
            category: Kategoria (governance, security, data, api, memory)
            impact_level: Niveli i ndikimit (low, medium, high)

        Returns:
            Dict me propozimin e krijuar
        """
        proposal_id = f"PROP-{len(self.proposals) + 1:04d}"

        analysis = self._analyze_proposal(description, category, impact_level)

        proposal = EvolutionProposal(
            id=proposal_id,
            description=description,
            timestamp=time.time(),
            status="proposed",
            analysis=analysis,
        )
        self.proposals.append(proposal)

        return {
            "id": proposal_id,
            "description": description,
            "category": category,
            "impact_level": impact_level,
            "timestamp": datetime.datetime.fromtimestamp(
                proposal.timestamp
            ).isoformat(),
            "status": proposal.status,
            "analysis": analysis,
        }

    def create_new_version(self, changes: Dict) -> Dict[str, Any]:
        """
        Krijon një version të ri për shqyrtim.

        Args:
            changes: Ndryshimet e propozuara

        Returns:
            Dict me versionin e ri
        """
        version_num = f"v{len(self.analysis_history) + 1}.0"
        analysis = self._analyze_changes(changes)

        return {
            "version": version_num,
            "changes": changes,
            "analysis": analysis,
            "created": datetime.datetime.now().isoformat(),
            "requires_governance_approval": analysis["dna_impact"] != "none",
            "requires_human_override": analysis["dna_impact"] == "high",
        }

    def _check_dna_integrity(self) -> bool:
        """Kontrollon integritetin e DNA-së"""
        current_hash = self.dna._hash
        expected = self.dna._compute_dna_hash()
        return current_hash == expected

    def _check_genome_coverage(self) -> Dict[str, Any]:
        """Kontrollon mbulimin e Genome-së"""
        categories = self.genome.get_packages_by_category()
        missing_categories = []

        required_categories = ["core", "ai", "memory", "agent", "security", "lightning"]
        for cat in required_categories:
            if not categories.get(cat):
                missing_categories.append(cat)

        return {
            "total_packages": len(self.genome.packages),
            "categories": {cat: len(pkgs) for cat, pkgs in categories.items()},
            "missing_categories": missing_categories,
            "coverage_percent": (
                (len(required_categories) - len(missing_categories))
                / len(required_categories)
                * 100
            ),
        }

    def _find_conflicts(self) -> List[Dict[str, Any]]:
        """Gjen konflikte potenciale në arkitekturë"""
        conflicts = []
        packages = self.genome.packages

        # Kontrollo për varësi qarkulluese
        for pkg_id, pkg in packages.items():
            for dep_id in pkg.dependencies:
                if dep_id in packages:
                    dep_pkg = packages[dep_id]
                    if pkg_id in dep_pkg.dependencies:
                        conflicts.append(
                            {
                                "type": "circular_dependency",
                                "packages": [pkg_id, dep_id],
                                "severity": "high",
                                "description": f"Circular dependency between {pkg.name} and {dep_pkg.name}",
                            }
                        )

        # Kontrollo për kapacitete të dyfishta
        capability_map = {}
        for pkg_id, pkg in packages.items():
            for cap in pkg.capabilities:
                if cap in capability_map:
                    conflicts.append(
                        {
                            "type": "duplicate_capability",
                            "capability": cap,
                            "packages": [capability_map[cap], pkg_id],
                            "severity": "low",
                            "description": f"Duplicate capability '{cap}' in {capability_map[cap]} and {pkg_id}",
                        }
                    )
                else:
                    capability_map[cap] = pkg_id

        return conflicts

    def _suggest_optimizations(self) -> List[str]:
        """Sugjeron optimizime për arkitekturën"""
        suggestions = []
        packages = self.genome.packages
        total = len(packages)

        if total < 10:
            suggestions.append(
                "Core genome is small. Consider adding more foundational packages."
            )
        elif total > 50:
            suggestions.append(
                "Genome is large. Consider reviewing for unused packages."
            )

        # Lightning SPP optimizations
        suggestions.append(
            "⚡ Lightning SPP 3.14: Enable TideWave mode for balanced scan/process/print"
        )
        suggestions.append(
            "⚡ Lightning SPP 3.14: Use Hybrid mode for maximum AI enhancement"
        )
        suggestions.append(
            "⚡ Lightning SPP 3.14: Stigma print quality for premium output"
        )

        if total > 5:
            suggestions.append(
                "Consider reviewing Genome for unused or duplicate packages."
            )
            suggestions.append(
                "Memory usage can be optimized with compression algorithms."
            )
            suggestions.append("API response time can be improved with caching layer.")

        return suggestions

    def _analyze_proposal(
        self, description: str, category: str, impact_level: str
    ) -> Dict[str, Any]:
        """Analizon një propozim për ndryshim"""
        impact_scores = {"low": 0.3, "medium": 0.6, "high": 0.9}
        impact = impact_scores.get(impact_level, 0.5)

        dna_impact = "none"
        if category == "constitution":
            dna_impact = "high"
        elif category == "security":
            dna_impact = "medium"
        elif category == "data":
            dna_impact = "medium"

        return {
            "feasibility": 0.8 - (impact * 0.3),
            "impact": impact,
            "complexity": impact * 0.7,
            "dna_impact": dna_impact,
            "estimated_effort": f"{int(impact * 10)} days",
            "requires_governance": dna_impact != "none",
            "requires_human_override": dna_impact == "high",
        }

    def _analyze_changes(self, changes: Dict) -> Dict[str, Any]:
        """Analizon ndryshimet dhe ndikimin në sistem"""
        dna_impact = "none"
        genome_impact = "none"

        for change_type, items in changes.items():
            if change_type in ["modify_dna", "change_constitution"]:
                dna_impact = "high"
            elif change_type in ["add", "remove"]:
                genome_impact = "medium" if len(items) > 1 else "low"
            elif change_type == "update":
                genome_impact = "medium"

        return {
            "dna_impact": dna_impact,
            "genome_impact": genome_impact,
            "recommended": dna_impact == "none",
            "requires_governance_approval": dna_impact != "none",
            "requires_human_override": dna_impact == "high",
            "rollback_possible": genome_impact != "none",
        }

    def get_proposals_summary(self) -> List[Dict[str, Any]]:
        """Kthen përmbledhje të të gjitha propozimeve"""
        return [
            {
                "id": p.id,
                "description": p.description[:80] + "...",
                "timestamp": datetime.datetime.fromtimestamp(p.timestamp).isoformat(),
                "status": p.status,
                "feasibility": p.analysis.get("feasibility", 0),
            }
            for p in self.proposals
        ]

    def get_stats(self) -> Dict[str, Any]:
        """Statistika të Evolution Engine"""
        return {
            "total_proposals": len(self.proposals),
            "total_analyses": len(self.analysis_history),
            "approved_proposals": len(
                [p for p in self.proposals if p.status == "approved"]
            ),
            "rejected_proposals": len(
                [p for p in self.proposals if p.status == "rejected"]
            ),
            "pending_proposals": len(
                [p for p in self.proposals if p.status == "proposed"]
            ),
            "last_analysis": (
                datetime.datetime.fromtimestamp(
                    self.analysis_history[-1].timestamp
                ).isoformat()
                if self.analysis_history
                else "never"
            ),
        }


if __name__ == "__main__":
    from neurosonic_dna import NeurosonicDNA
    from neurosonic_genome import NeurosonicGenome

    print("=" * 70)
    print("🧬 NEUROSONIC EVOLUTION ENGINE")
    print("=" * 70)

    dna = NeurosonicDNA()
    genome = NeurosonicGenome()
    evolution = NeurosonicEvolutionEngine(dna, genome)

    print("\n🔍 Analiza e Arkitekturës:")
    analysis = evolution.analyze_architecture()
    print(f"   DNA Integrity: {'✅ OK' if analysis['dna_integrity'] else '❌ Problem'}")
    print(f"   Genome Coverage: {analysis['genome_coverage']['coverage_percent']:.0f}%")
    print("✅ Evolution Engine gati!")
