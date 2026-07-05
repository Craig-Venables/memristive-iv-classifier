#!/usr/bin/env python3
"""
Classify a single IV sweep .txt file (no GUI).

Usage (from repo root):
    python examples/classify_single_sweep.py path/to/sweep.txt
    python examples/classify_single_sweep.py path/to/sweep.txt --level full
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Repo root on path
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from analysis import analyze_sweep  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify one IV sweep file")
    parser.add_argument("file", type=Path, help="Path to .txt sweep file")
    parser.add_argument(
        "--level",
        default="classification",
        choices=("basic", "classification", "full", "research"),
        help="Analysis level (default: classification)",
    )
    parser.add_argument("--json", action="store_true", help="Print full result as JSON")
    args = parser.parse_args()

    if not args.file.is_file():
        print(f"File not found: {args.file}", file=sys.stderr)
        return 1

    print(f"Analyzing: {args.file}")
    print(f"Level: {args.level}\n")

    result = analyze_sweep(
        file_path=str(args.file),
        analysis_level=args.level,
    )

    if args.json:
        print(json.dumps(result, indent=2, default=str))
        return 0

    clf = result.get("classification") or {}
    res = result.get("resistance_metrics") or {}

    print("=== Classification ===")
    print(f"  device_type:        {clf.get('device_type', 'N/A')}")
    print(f"  memristivity_score: {clf.get('memristivity_score', 'N/A')}")
    print(f"  confidence:         {clf.get('confidence', 'N/A')}")
    print(f"  forming_stage:      {clf.get('forming_stage', 'N/A')}")

    if res:
        print("\n=== Resistance ===")
        print(f"  Ron (mean):         {res.get('ron_mean', 'N/A')}")
        print(f"  Roff (mean):        {res.get('roff_mean', 'N/A')}")
        print(f"  switching_ratio:    {res.get('switching_ratio', 'N/A')}")

    warnings = result.get("warnings") or clf.get("warnings") or []
    if warnings:
        print("\n=== Warnings ===")
        for w in warnings:
            print(f"  - {w}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
