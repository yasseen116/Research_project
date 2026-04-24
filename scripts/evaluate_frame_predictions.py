#!/usr/bin/env python3
"""Evaluate predicted frame structures against gold samples."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from frame_slot_utils import FRAME_KINDS, flatten_frame, frame_consistency_score, normalize_frame


ROOT = Path(__file__).resolve().parent.parent


def prf(pred_items: set[str], gold_items: set[str]) -> dict:
    tp = len(pred_items & gold_items)
    fp = len(pred_items - gold_items)
    fn = len(gold_items - pred_items)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "tp": tp,
        "fp": fp,
        "fn": fn,
    }


def average(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def load_gold(gold_dir: Path) -> dict[str, dict]:
    gold = {}
    for path in sorted(gold_dir.glob("*.json")):
        if path.name in {"summary.json", "evaluation.json"} or path.name.startswith("template_"):
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or "sample_id" not in payload or "frames" not in payload:
            continue
        gold[payload["sample_id"]] = payload
    return gold


def load_predictions(pred_dir: Path) -> dict[str, dict]:
    predictions = {}
    for path in sorted(pred_dir.glob("*.json")):
        if path.name in {"summary.json", "evaluation.json"} or path.name.endswith(".raw_response.json"):
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or "sample_id" not in payload or "frames" not in payload:
            continue
        predictions[payload["sample_id"]] = payload
    return predictions


def frame_compliance(prediction: dict) -> float:
    frames = prediction.get("frames", [])
    if not isinstance(frames, list) or not frames:
        return 0.0

    checks = []
    for index, frame in enumerate(frames, start=1):
        if not isinstance(frame, dict):
            checks.append(False)
            continue
        normalized = normalize_frame(frame, default_index=index)
        checks.append(
            bool(
                normalized["frame_id"]
                and normalized["kind"] in FRAME_KINDS
                and isinstance(normalized["evidence_turns"], list)
                and normalized["status"] == "confirmed"
            )
        )
    return sum(checks) / len(checks)


def flatten_frames_by_kind(frames: list[dict]) -> dict[str, set[str]]:
    flattened = {kind: set() for kind in FRAME_KINDS}
    for index, frame in enumerate(frames, start=1):
        normalized = normalize_frame(frame, default_index=index)
        flattened[normalized["kind"]].add(flatten_frame(normalized))
    return flattened


def evaluate_sample(gold: dict, prediction: dict) -> dict:
    gold_by_kind = flatten_frames_by_kind(gold["frames"])
    pred_by_kind = flatten_frames_by_kind(prediction.get("frames", []))

    kind_scores = {}
    all_gold = set()
    all_pred = set()
    for kind in sorted(FRAME_KINDS):
        kind_scores[kind] = prf(pred_by_kind[kind], gold_by_kind[kind])
        all_gold.update({f"{kind}::{item}" for item in gold_by_kind[kind]})
        all_pred.update({f"{kind}::{item}" for item in pred_by_kind[kind]})

    return {
        "sample_id": gold["sample_id"],
        "kinds": kind_scores,
        "overall": prf(all_pred, all_gold),
        "dialogue_frame_consistency": frame_consistency_score(prediction.get("frames", [])),
        "compliance": frame_compliance(prediction),
    }


def aggregate(per_sample: list[dict]) -> dict:
    return {
        "overall_f1_macro": average([item["overall"]["f1"] for item in per_sample]),
        "overall_precision_macro": average([item["overall"]["precision"] for item in per_sample]),
        "overall_recall_macro": average([item["overall"]["recall"] for item in per_sample]),
        "dialogue_frame_consistency_macro": average(
            [item["dialogue_frame_consistency"] for item in per_sample]
        ),
        "compliance_macro": average([item["compliance"] for item in per_sample]),
        "per_kind": {
            kind: {
                "f1_macro": average([item["kinds"][kind]["f1"] for item in per_sample]),
                "precision_macro": average([item["kinds"][kind]["precision"] for item in per_sample]),
                "recall_macro": average([item["kinds"][kind]["recall"] for item in per_sample]),
            }
            for kind in sorted(FRAME_KINDS)
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gold-dir", type=Path, required=True)
    parser.add_argument("--pred-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    gold = load_gold(args.gold_dir)
    predictions = load_predictions(args.pred_dir)
    per_sample = []
    split_counts = Counter()

    for sample_id, gold_sample in gold.items():
        if sample_id not in predictions:
            raise SystemExit(f"Missing frame prediction for {sample_id}")
        per_sample.append(evaluate_sample(gold_sample, predictions[sample_id]))
        split_counts.update([gold_sample["metadata"]["split"]])

    payload = {
        "sample_count": len(per_sample),
        "split_counts": dict(split_counts),
        "aggregate": aggregate(per_sample),
        "per_sample": per_sample,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
