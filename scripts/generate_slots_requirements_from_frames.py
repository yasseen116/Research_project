#!/usr/bin/env python3
"""Derive slots and requirements deterministically from frame predictions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from frame_slot_utils import canonicalize_frames, derive_slots_from_frames, generate_requirements_from_frames, normalize_frame


ROOT = Path(__file__).resolve().parent.parent


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path.resolve())


def load_predictions(input_dir: Path) -> list[dict]:
    predictions = []
    for path in sorted(input_dir.glob("*.json")):
        if path.name in {"summary.json", "evaluation.json"} or path.name.endswith(".raw_response.json"):
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        if "sample_id" not in payload or "frames" not in payload:
            continue
        predictions.append(payload)
    return predictions


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--combined-dir", type=Path, required=True)
    parser.add_argument("--output-slot-dir", type=Path, required=True)
    parser.add_argument("--output-req-dir", type=Path, required=True)
    args = parser.parse_args()

    args.combined_dir.mkdir(parents=True, exist_ok=True)
    args.output_slot_dir.mkdir(parents=True, exist_ok=True)
    args.output_req_dir.mkdir(parents=True, exist_ok=True)
    summary = []

    for prediction in load_predictions(args.input_dir):
        frames = canonicalize_frames(
            [normalize_frame(frame, default_index=index) for index, frame in enumerate(prediction["frames"], start=1)]
        )
        slots = derive_slots_from_frames(frames)
        slot_prediction = {
            "sample_id": prediction["sample_id"],
            "method": f"{prediction['method']}__frame_to_slots_v1",
            "slots": slots,
        }
        requirement_prediction = generate_requirements_from_frames(
            sample_id=prediction["sample_id"],
            frames=frames,
            method=f"{prediction['method']}__frame_to_slots_v1__template_generation_v1",
        )
        combined_prediction = {
            "sample_id": prediction["sample_id"],
            "method": prediction["method"],
            "model": prediction.get("model"),
            "prompt_hash": prediction.get("prompt_hash"),
            "schema_hash": prediction.get("schema_hash"),
            "parse_status": prediction.get("parse_status"),
            "repair_attempted": prediction.get("repair_attempted", False),
            "usage": prediction.get("usage", {}),
            "error": prediction.get("error"),
            "frames": frames,
            "slots": slots,
            "requirements": requirement_prediction["requirements"],
        }

        combined_path = args.combined_dir / f"{prediction['sample_id']}.json"
        slots_path = args.output_slot_dir / f"{prediction['sample_id']}.json"
        req_path = args.output_req_dir / f"{prediction['sample_id']}.json"
        combined_path.write_text(json.dumps(combined_prediction, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        slots_path.write_text(json.dumps(slot_prediction, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        req_path.write_text(json.dumps(requirement_prediction, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        summary.append(
            {
                "sample_id": prediction["sample_id"],
                "combined_path": display_path(combined_path),
                "slot_path": display_path(slots_path),
                "requirement_path": display_path(req_path),
                "frame_count": len(frames),
                "functional_requirements": len(requirement_prediction["requirements"]["functional"]),
                "non_functional_requirements": len(requirement_prediction["requirements"]["non_functional"]),
            }
        )

    summary_path = args.combined_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
