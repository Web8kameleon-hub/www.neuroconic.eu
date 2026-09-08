#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate Neurosonic 30-day readiness scorecard."
    )
    parser.add_argument(
        "--input",
        default="docs/production/assessment/scorecard_input_template.json",
        help="Path to scorecard input JSON.",
    )
    parser.add_argument(
        "--output-json",
        default="docs/production/assessment/scorecard_result.json",
        help="Path to output JSON report.",
    )
    parser.add_argument(
        "--output-md",
        default="docs/production/assessment/scorecard_result.md",
        help="Path to output Markdown report.",
    )
    return parser.parse_args()


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Scorecard input must be a JSON object")
    return payload


def _validate_score(value: Any, field_name: str) -> float:
    try:
        score = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be numeric") from exc
    if score < 0 or score > 5:
        raise ValueError(f"{field_name} must be between 0 and 5")
    return score


def _compute_category_score(
    category_name: str,
    category_payload: dict[str, Any],
) -> dict[str, Any]:
    weight = float(category_payload.get("weight", 0))
    items = category_payload.get("items", {})
    if not isinstance(items, dict) or not items:
        raise ValueError(f"categories.{category_name}.items must be a non-empty object")

    normalized_scores: dict[str, float] = {}
    for item_name, value in items.items():
        normalized_scores[item_name] = _validate_score(
            value,
            f"categories.{category_name}.items.{item_name}",
        )

    average = sum(normalized_scores.values()) / len(normalized_scores)
    weighted_score = (average / 5.0) * weight

    return {
        "weight": weight,
        "average": round(average, 4),
        "weighted_score": round(weighted_score, 4),
        "items": normalized_scores,
    }


def _decision(total_score: float, hard_gates: dict[str, bool]) -> tuple[str, list[str]]:
    failed_gates = [name for name, passed in hard_gates.items() if not passed]
    if failed_gates:
        return "No-Go", failed_gates
    if total_score >= 80:
        return "Go", []
    if total_score >= 65:
        return "Conditional", []
    return "No-Go", []


def _to_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Neurosonic 30-Day Scorecard Result",
        "",
        f"- Project: `{report['meta'].get('project', 'unknown')}`",
        f"- Assessor: `{report['meta'].get('assessor', 'unknown')}`",
        f"- Date: `{report['meta'].get('date_utc', 'unknown')}`",
        f"- Total score: `{report['total_score']}` / `100`",
        f"- Decision: `{report['decision']}`",
    ]

    failed = report.get("failed_hard_gates", [])
    if failed:
        lines.append(f"- Failed hard gates: `{', '.join(failed)}`")

    lines.extend(
        [
            "",
            "## Category Breakdown",
            "",
            "| Category | Weight | Avg (0..5) | Weighted Score |",
            "| --- | ---: | ---: | ---: |",
        ]
    )

    for name, payload in report.get("categories", {}).items():
        lines.append(
            "| "
            f"{name} | "
            f"{payload['weight']} | "
            f"{payload['average']} | "
            f"{payload['weighted_score']} |"
        )

    lines.append("")
    return "\n".join(lines)


def evaluate(payload: dict[str, Any]) -> dict[str, Any]:
    categories = payload.get("categories", {})
    if not isinstance(categories, dict) or not categories:
        raise ValueError("categories must be a non-empty object")

    hard_gates = payload.get("hard_gates", {})
    if not isinstance(hard_gates, dict) or not hard_gates:
        raise ValueError("hard_gates must be a non-empty object")

    normalized_hard_gates: dict[str, bool] = {
        key: bool(value) for key, value in hard_gates.items()
    }

    category_results: dict[str, Any] = {}
    total_score = 0.0
    for category_name, category_payload in categories.items():
        if not isinstance(category_payload, dict):
            raise ValueError(f"categories.{category_name} must be an object")
        result = _compute_category_score(category_name, category_payload)
        category_results[category_name] = result
        total_score += result["weighted_score"]

    total_score = round(total_score, 4)
    decision, failed_hard_gates = _decision(total_score, normalized_hard_gates)

    return {
        "meta": payload.get("meta", {}),
        "total_score": total_score,
        "decision": decision,
        "hard_gates": normalized_hard_gates,
        "failed_hard_gates": failed_hard_gates,
        "categories": category_results,
    }


def main() -> int:
    args = _parse_args()
    input_path = Path(args.input)
    output_json_path = Path(args.output_json)
    output_md_path = Path(args.output_md)

    payload = _load_json(input_path)
    report = evaluate(payload)

    output_json_path.parent.mkdir(parents=True, exist_ok=True)
    output_json_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    output_md_path.parent.mkdir(parents=True, exist_ok=True)
    output_md_path.write_text(_to_markdown(report) + "\n", encoding="utf-8")

    print(f"Scorecard decision: {report['decision']}")
    print(f"Scorecard total: {report['total_score']}")
    print(f"JSON report: {output_json_path}")
    print(f"Markdown report: {output_md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
