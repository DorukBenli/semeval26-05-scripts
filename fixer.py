#!/usr/bin/env python3
"""
Reorder predictions JSONL to match the sample_id order in data/dev.json,
then replace "sample_id" with sequential "id" = 0..N-1.

Input:
  - predictions/predictions_gnll_contrastivetrain.jsonl  (JSONL: {"sample_id": "...", "prediction": ...})
  - data/dev.json                                       (JSON: dict keyed by "0","1",... each has "sample_id")

Output:
  - predictions/predictions_gnll_contrastivetrain.reordered.jsonl
    (JSONL: {"id": <int>, "prediction": <float>})
"""

import json
import os
import sys
from typing import Dict, List, Any


PRED_PATH = os.path.join("predictions", "predictions_gnll_contrastivetrain.jsonl")
DEV_PATH = os.path.join("data", "dev.json")
OUT_PATH = os.path.join("predictions", "predictions_gnll_contrastivetrain.reordered.jsonl")


def load_dev_sample_id_order(dev_path: str) -> List[str]:
    with open(dev_path, "r", encoding="utf-8") as f:
        dev_obj = json.load(f)  # preserves order of keys as in file (Python 3.7+)

    # dev_obj is expected to be a dict like {"0": {...}, "1": {...}, ...}
    order: List[str] = []
    for k, v in dev_obj.items():
        if not isinstance(v, dict) or "sample_id" not in v:
            raise ValueError(f"dev.json entry {k} missing 'sample_id'")
        order.append(str(v["sample_id"]))
    return order


def load_predictions(pred_path: str) -> Dict[str, Any]:
    pred_by_sample_id: Dict[str, Any] = {}
    with open(pred_path, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON on line {lineno} of {pred_path}: {e}") from e

            if "sample_id" not in obj or "prediction" not in obj:
                raise ValueError(f"Line {lineno} missing 'sample_id' or 'prediction': {obj}")

            sid = str(obj["sample_id"])
            if sid in pred_by_sample_id:
                raise ValueError(f"Duplicate sample_id {sid} in predictions (line {lineno})")
            pred_by_sample_id[sid] = obj["prediction"]
    return pred_by_sample_id


def main() -> int:
    dev_order = load_dev_sample_id_order(DEV_PATH)
    pred_map = load_predictions(PRED_PATH)

    missing = [sid for sid in dev_order if sid not in pred_map]
    if missing:
        print(f"[ERROR] {len(missing)} sample_id(s) from {DEV_PATH} not found in {PRED_PATH}.", file=sys.stderr)
        print(f"First 20 missing: {missing[:20]}", file=sys.stderr)
        return 1

    # Reorder + rewrite schema: {"id": i, "prediction": ...}
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as out:
        for i, sid in enumerate(dev_order):
            rec = {"id": i, "prediction": pred_map[sid]}
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"[OK] Wrote {len(dev_order)} lines to: {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
