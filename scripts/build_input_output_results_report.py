#!/usr/bin/env python3
"""Create a readable file showing system inputs and generated requirements."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a readable report of dialogue inputs and generated requirements."
    )
    parser.add_argument(
        "--input-dir",
        default="synthetic/pilot_noisy",
        help="Directory containing the input dialogue samples.",
    )
    parser.add_argument(
        "--requirements-dir",
        default="outputs/b2_keyword_normalized_requirements_noisy",
        help="Directory containing generated requirement predictions.",
    )
    parser.add_argument(
        "--output-md",
        default="outputs/input_output_results_b2_noisy.md",
        help="Markdown output path.",
    )
    parser.add_argument(
        "--output-json",
        default="outputs/input_output_results_b2_noisy.json",
        help="JSON output path.",
    )
    parser.add_argument(
        "--system-label",
        default="B2 keyword-normalized baseline on noisy pilot dialogues",
        help="Human-readable label for the system used.",
    )
    return parser.parse_args()


def build_markdown(samples: list[dict], system_label: str) -> str:
    lines: list[str] = []
    lines.append("# Input To Requirements Results")
    lines.append("")
    lines.append(f"System: `{system_label}`")
    lines.append("")
    lines.append("This file shows exactly what was fed into the system and the requirements it produced.")
    lines.append("")

    for sample in samples:
        lines.append(f"## {sample['sample_id']}")
        lines.append("")
        lines.append(f"- Domain: `{sample['domain']}`")
        lines.append(f"- Split: `{sample['split']}`")
        lines.append(f"- Source dataset: `{sample['source_dataset']}`")
        lines.append(f"- Source document: `{sample['source_document_id']}`")
        lines.append("")
        lines.append("### Input Dialogue")
        lines.append("")
        for turn in sample["dialogue"]:
            lines.append(f"- `{turn['turn_id']}` `{turn['role']}`: {turn['text']}")
        lines.append("")
        lines.append("### Output Functional Requirements")
        lines.append("")
        if sample["requirements"]["functional"]:
            for item in sample["requirements"]["functional"]:
                lines.append(f"- `{item['id']}` {item['text']}")
        else:
            lines.append("- none")
        lines.append("")
        lines.append("### Output Non-Functional Requirements")
        lines.append("")
        if sample["requirements"]["non_functional"]:
            for item in sample["requirements"]["non_functional"]:
                lines.append(f"- `{item['id']}` `{item['category']}` {item['text']}")
        else:
            lines.append("- none")
        lines.append("")

    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()

    input_dir = ROOT / args.input_dir
    requirements_dir = ROOT / args.requirements_dir
    output_md = ROOT / args.output_md
    output_json = ROOT / args.output_json

    samples: list[dict] = []
    for input_path in sorted(input_dir.glob("*.json")):
        input_payload = load_json(input_path)
        if not isinstance(input_payload, dict) or "sample_id" not in input_payload:
            continue

        sample_id = input_payload["sample_id"]
        requirements_path = requirements_dir / f"{sample_id}.json"
        if not requirements_path.exists():
            continue

        requirements_payload = load_json(requirements_path)
        sample_record = {
            "sample_id": sample_id,
            "system_label": args.system_label,
            "domain": input_payload["metadata"]["domain"],
            "split": input_payload["metadata"]["split"],
            "source_dataset": input_payload["source"]["dataset"],
            "source_document_id": input_payload["source"]["document_id"],
            "dialogue": input_payload["dialogue"],
            "requirements": requirements_payload["requirements"],
        }
        samples.append(sample_record)

    output_payload = {
        "system_label": args.system_label,
        "sample_count": len(samples),
        "samples": samples,
    }

    output_md.write_text(build_markdown(samples, args.system_label), encoding="utf-8")
    output_json.write_text(json.dumps(output_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Wrote {output_md.relative_to(ROOT)} and {output_json.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
