#!/usr/bin/env python3
"""Neurosonic data intelligence components: SeltenDaten, PlirisDaten, SelfLearning."""

from __future__ import annotations

import json
import os
import time
from typing import Any


class SeltenDatenAnalyzer:
    """Zbulues i të dhënave të rralla bazuar në frekuencë."""

    def detect_rare(
        self,
        records: list[dict[str, Any]],
        key_fields: list[str] | None = None,
        rarity_threshold: float = 0.1,
        min_occurrences: int = 1,
    ) -> dict[str, Any]:
        total = len(records)
        if total == 0:
            return {
                "total_records": 0,
                "rare_count": 0,
                "threshold": rarity_threshold,
                "rare_items": [],
            }

        signatures: list[str] = []
        for record in records:
            if key_fields:
                compact = {field: record.get(field) for field in key_fields}
            else:
                compact = record
            signatures.append(json.dumps(compact, sort_keys=True, ensure_ascii=False))

        counts: dict[str, int] = {}
        for signature in signatures:
            counts[signature] = counts.get(signature, 0) + 1

        rare_items: list[dict[str, Any]] = []
        for index, record in enumerate(records):
            signature = signatures[index]
            occurrence = counts[signature]
            ratio = occurrence / total
            is_rare = occurrence <= min_occurrences or ratio <= rarity_threshold
            if is_rare:
                rare_items.append(
                    {
                        "index": index,
                        "record": record,
                        "occurrence": occurrence,
                        "frequency_ratio": ratio,
                        "rarity_score": round(1.0 - ratio, 6),
                    }
                )

        return {
            "total_records": total,
            "rare_count": len(rare_items),
            "threshold": rarity_threshold,
            "min_occurrences": min_occurrences,
            "rare_items": rare_items,
        }


class PlirisDatenFilter:
    """Filtron të dhëna që nuk kërkojnë protokolle shtesë."""

    def filter_protocol_free(self, records: list[dict[str, Any]]) -> dict[str, Any]:
        accepted: list[dict[str, Any]] = []
        rejected: list[dict[str, Any]] = []

        for index, record in enumerate(records):
            reasons: list[str] = []

            if bool(record.get("requires_additional_protocol", False)):
                reasons.append("requires_additional_protocol=true")
            if bool(record.get("protocol_required", False)):
                reasons.append("protocol_required=true")

            compliance = record.get("compliance", {})
            if isinstance(compliance, dict) and bool(
                compliance.get("requires_extra_protocol", False)
            ):
                reasons.append("compliance.requires_extra_protocol=true")

            classification = str(record.get("data_classification", "")).strip().lower()
            if classification in {"restricted", "secret", "regulated", "confidential"}:
                reasons.append(f"data_classification={classification}")

            if reasons:
                rejected.append(
                    {
                        "index": index,
                        "record": record,
                        "reasons": reasons,
                    }
                )
            else:
                accepted.append(
                    {
                        "index": index,
                        "record": record,
                    }
                )

        return {
            "total_records": len(records),
            "accepted_count": len(accepted),
            "rejected_count": len(rejected),
            "accepted": accepted,
            "rejected": rejected,
        }


class SelfLearningCycleManager:
    """Menaxhon ciklet e vetë-mësimit me engine real."""

    def __init__(self, storage_path: str | None = None):
        if storage_path is None:
            storage_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "memory",
                "self_learning_cycles.json",
            )
        self.storage_path = storage_path

    def _load_cycles(self) -> list[dict[str, Any]]:
        try:
            with open(self.storage_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        return []

    def _save_cycles(self, cycles: list[dict[str, Any]]) -> None:
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as file:
            json.dump(cycles, file, ensure_ascii=False, indent=2)

    def create_cycle(
        self,
        goal: str,
        context: dict[str, Any],
        llm_engine: str,
        engine_callback,
    ) -> dict[str, Any]:
        goal_clean = goal.strip()
        if not goal_clean:
            return {
                "success": False,
                "status": "error",
                "error": "Goal is empty",
                "timestamp": time.time(),
            }

        prompt = self._build_prompt(goal_clean, context)
        llm_result = engine_callback(prompt, llm_engine)

        cycle = {
            "id": f"cycle_{int(time.time() * 1000)}",
            "goal": goal_clean,
            "engine": llm_engine,
            "context": context,
            "result": llm_result,
            "timestamp": time.time(),
        }

        cycles = self._load_cycles()
        cycles.append(cycle)
        cycles = cycles[-500:]
        self._save_cycles(cycles)

        return {
            "success": True,
            "status": "completed" if llm_result.get("success") else "partial",
            "cycle": cycle,
            "total_cycles": len(cycles),
        }

    def get_cycles(self, limit: int = 20) -> dict[str, Any]:
        cycles = self._load_cycles()
        return {
            "total_cycles": len(cycles),
            "cycles": cycles[-max(1, limit):],
        }

    def _build_prompt(self, goal: str, context: dict[str, Any]) -> str:
        context_text = json.dumps(context, ensure_ascii=False, sort_keys=True)
        return (
            "Self-learning cycle for Neurosonic. "
            "Goal: "
            + goal
            + " | Context: "
            + context_text
            + " | Provide: plan, risks, measurable next actions, and validation criteria."
        )
