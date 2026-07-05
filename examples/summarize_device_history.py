#!/usr/bin/env python3
"""
Summarize device tracking history JSON (Sample GUI overlay rules).

Usage:
    python examples/summarize_device_history.py path/to/D94_A_1_history.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

# Inline minimal summarizer (same rules as Switchbox_GUI yield_source)
# Keeps example runnable without Switchbox_GUI import.


def summarize_device_from_history(
    history: dict | None,
    *,
    min_sweeps_for_confident: int = 2,
    mem_score_threshold: float = 60.0,
) -> dict:
    empty = {
        "measured": False,
        "sweep_count": 0,
        "display_status": "unmeasured",
        "best_mem_score": None,
        "latest_type": "unknown",
        "promising": False,
    }
    if not history:
        return empty

    measurements = history.get("all_measurements") or history.get("measurements") or []
    sweep_count = len(measurements)
    if sweep_count == 0:
        return empty

    scores: list[float] = []
    latest_type = "unknown"
    for m in measurements:
        clf = m.get("classification") or {}
        dt = clf.get("device_type")
        if isinstance(dt, str) and dt.strip():
            latest_type = dt.strip().lower()
        score = clf.get("memristivity_score")
        if score is not None:
            try:
                scores.append(float(score))
            except (TypeError, ValueError):
                pass

    best_mem_score = max(scores) if scores else None

    if sweep_count == 1:
        display_status = "pending"
    elif (
        sweep_count >= min_sweeps_for_confident
        and best_mem_score is not None
        and best_mem_score >= mem_score_threshold
    ):
        display_status = "memristive"
    else:
        display_status = latest_type if latest_type != "unknown" else "uncertain"

    promising = False
    if display_status != "memristive":
        if latest_type in ("rectifying", "memcapacitive"):
            promising = True
        elif best_mem_score is not None and 40 <= best_mem_score < mem_score_threshold:
            promising = True

    return {
        "measured": True,
        "sweep_count": sweep_count,
        "display_status": display_status,
        "best_mem_score": best_mem_score,
        "latest_type": latest_type,
        "promising": promising,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize device tracking history")
    parser.add_argument("history_file", type=Path, help="Path to *_history.json")
    args = parser.parse_args()

    if not args.history_file.is_file():
        print(f"File not found: {args.history_file}", file=sys.stderr)
        return 1

    with open(args.history_file, encoding="utf-8") as f:
        history = json.load(f)

    summary = summarize_device_from_history(history)
    device_id = history.get("device_id", args.history_file.stem.replace("_history", ""))

    print(f"Device: {device_id}")
    print(f"  sweep_count:     {summary['sweep_count']}")
    print(f"  display_status:  {summary['display_status']}")
    print(f"  best_mem_score:  {summary['best_mem_score']}")
    print(f"  latest_type:     {summary['latest_type']}")
    print(f"  promising:       {summary['promising']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
