#!/usr/bin/env python3
"""Compare B1 and B2 pilot results for clean and noisy conditions."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


FILES = {
    "b1_clean_slots": ROOT / "outputs" / "b1_rule_based_slots" / "evaluation.json",
    "b1_noisy_slots": ROOT / "outputs" / "b1_rule_based_slots_noisy" / "evaluation.json",
    "b1_clean_req": ROOT / "outputs" / "b1_rule_based_requirements" / "evaluation.json",
    "b1_noisy_req": ROOT / "outputs" / "b1_rule_based_requirements_noisy" / "evaluation.json",
    "b2_clean_slots": ROOT / "outputs" / "b2_keyword_normalized_slots" / "evaluation.json",
    "b2_noisy_slots": ROOT / "outputs" / "b2_keyword_normalized_slots_noisy" / "evaluation.json",
    "b2_clean_req": ROOT / "outputs" / "b2_keyword_normalized_requirements" / "evaluation.json",
    "b2_noisy_req": ROOT / "outputs" / "b2_keyword_normalized_requirements_noisy" / "evaluation.json",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def summarize(slot_eval: dict, req_eval: dict) -> dict:
    return {
        "slot_f1": slot_eval["aggregate"]["overall_f1_macro"],
        "slot_functional_capability_f1": slot_eval["aggregate"]["per_slot"]["functional_capabilities"]["f1_macro"],
        "slot_security_f1": slot_eval["aggregate"]["per_slot"]["security_constraints"]["f1_macro"],
        "requirement_f1": req_eval["aggregate"]["overall_f1_macro"],
        "requirement_coverage": req_eval["aggregate"]["coverage_macro"],
        "hallucination_rate": req_eval["aggregate"]["hallucination_rate_macro"],
    }


def main() -> int:
    data = {name: load(path) for name, path in FILES.items()}
    payload = {
        "b1_clean": summarize(data["b1_clean_slots"], data["b1_clean_req"]),
        "b1_noisy": summarize(data["b1_noisy_slots"], data["b1_noisy_req"]),
        "b2_clean": summarize(data["b2_clean_slots"], data["b2_clean_req"]),
        "b2_noisy": summarize(data["b2_noisy_slots"], data["b2_noisy_req"]),
    }

    output_json = ROOT / "outputs" / "baseline_comparison_summary.json"
    output_md = ROOT / "outputs" / "baseline_comparison_summary.md"
    output_json.write_text(json.dumps(payload, indent=2))

    lines = [
        "# Baseline Comparison Summary",
        "",
        "| Baseline | Condition | Slot F1 | Capability F1 | Security F1 | Requirement F1 | Coverage | Hallucination |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for baseline in ["b1", "b2"]:
        for condition in ["clean", "noisy"]:
            item = payload[f"{baseline}_{condition}"]
            lines.append(
                f"| {baseline.upper()} | {condition} | {item['slot_f1']:.4f} | {item['slot_functional_capability_f1']:.4f} | {item['slot_security_f1']:.4f} | {item['requirement_f1']:.4f} | {item['requirement_coverage']:.4f} | {item['hallucination_rate']:.4f} |"
            )

    lines.extend(
        [
            "",
            "## Read This First",
            "",
            "- `B1` is the brittle lexical baseline.",
            "- `B2` adds normalization and paraphrase-aware keyword mapping for the fixed six-question dialogue flow.",
            "- The noisy condition is the meaningful one for this pilot because it exposes whether the slot extractor survives paraphrase.",
        ]
    )
    output_md.write_text("\n".join(lines) + "\n")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
