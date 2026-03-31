#!/usr/bin/env python3
"""Check lane coverage over recent completed backlog items.

Parses markdown checklist rows ("- [x] ...") and infers team lanes from the prefix
before the first colon (e.g. "Systems/QA Team"). Emits JSON summary and optional
markdown snippet for durable team logs.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

CHECKED_ROW_RE = re.compile(r"^\s*-\s*\[x\]\s+(.*)$", re.IGNORECASE)
LANE_PREFIX_RE = re.compile(r"^([A-Za-z\-/ ]+?)\s*:\s*")

CANONICAL_LANES = ["systems", "world", "ai-content", "combat", "design", "ux", "qa", "vfx"]

ALIAS_MAP = {
    "ai content": "ai-content",
    "ai-content": "ai-content",
    "system": "systems",
    "systems": "systems",
    "world": "world",
    "combat": "combat",
    "design": "design",
    "ux": "ux",
    "qa": "qa",
    "vfx": "vfx",
}


def normalize_lane(raw: str) -> str | None:
    raw = raw.strip().lower()
    return ALIAS_MAP.get(raw)


def infer_lanes(task_text: str) -> list[str]:
    match = LANE_PREFIX_RE.match(task_text)
    if not match:
        return []
    prefix = match.group(1).replace("team", "").strip().lower()
    chunks = [part.strip() for part in re.split(r"/|,|&| and ", prefix) if part.strip()]
    lanes = [normalize_lane(chunk) for chunk in chunks]
    return [lane for lane in lanes if lane]


def collect_recent_rows(markdown_text: str, max_items: int) -> list[str]:
    rows: list[str] = []
    for line in markdown_text.splitlines():
        m = CHECKED_ROW_RE.match(line)
        if m:
            rows.append(m.group(1).strip())
    return rows[-max_items:]


def build_report(rows: list[str], cap_ratio: float) -> dict:
    lane_counts = Counter()
    for row in rows:
        for lane in infer_lanes(row):
            lane_counts[lane] += 1

    total = len(rows)
    percentages = {
        lane: round((lane_counts.get(lane, 0) / total) * 100.0, 2) if total else 0.0
        for lane in CANONICAL_LANES
    }
    over_cap = sorted([lane for lane, pct in percentages.items() if pct > (cap_ratio * 100.0)])

    return {
        "recentCompletedItems": total,
        "capPercent": round(cap_ratio * 100.0, 2),
        "laneCounts": {lane: lane_counts.get(lane, 0) for lane in CANONICAL_LANES},
        "lanePercentages": percentages,
        "overCapLanes": over_cap,
        "status": "over-cap" if over_cap else "within-cap",
    }


def to_markdown(report: dict) -> str:
    rows = [
        "| lane | count | percent |",
        "|---|---:|---:|",
    ]
    for lane in CANONICAL_LANES:
        rows.append(f"| {lane} | {report['laneCounts'][lane]} | {report['lanePercentages'][lane]}% |")
    over_cap = ", ".join(report["overCapLanes"]) if report["overCapLanes"] else "none"
    return "\n".join(
        [
            "### Lane Coverage Guardrail",
            f"- status: **{report['status']}** (cap={report['capPercent']}%)",
            f"- recent completed items: **{report['recentCompletedItems']}**",
            f"- over-cap lanes: **{over_cap}**",
            "",
            *rows,
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backlog", required=True, type=Path)
    parser.add_argument("--max-items", type=int, default=10)
    parser.add_argument("--cap-ratio", type=float, default=0.40)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--md-out", type=Path)
    args = parser.parse_args()

    text = args.backlog.read_text(encoding="utf-8")
    rows = collect_recent_rows(text, max_items=args.max_items)
    report = build_report(rows, cap_ratio=args.cap_ratio)

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    else:
        print(json.dumps(report, indent=2))

    if args.md_out:
        args.md_out.parent.mkdir(parents=True, exist_ok=True)
        args.md_out.write_text(to_markdown(report) + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
