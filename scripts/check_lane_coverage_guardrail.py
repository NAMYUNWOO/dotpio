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
TREND_SCORE_BAND_RE = re.compile(
    r"compatRowPolicySourceConfidenceTrendScoreBand(?:Alias)?\s*[:=]\s*([A-Z]+)"
)

CANONICAL_LANES = ["systems", "world", "ai-content", "combat", "design", "ux", "qa", "vfx"]

BUCKETS = {
    "combat-or-vfx": ["combat", "vfx"],
    "design-or-world": ["design", "world"],
    "systems-or-ops": ["systems", "qa"],
}

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


def collect_trend_score_band_snapshot(rows: list[str]) -> dict[str, int]:
    band_counts = {"CALM": 0, "EDGE": 0, "HEATED": 0}
    alias_to_band = {"C": "CALM", "E": "EDGE", "H": "HEATED"}

    for row in rows:
        for token in TREND_SCORE_BAND_RE.findall(row):
            normalized = token.strip().upper()
            if normalized in band_counts:
                band_counts[normalized] += 1
            elif normalized in alias_to_band:
                band_counts[alias_to_band[normalized]] += 1

    return band_counts


def collect_row_dominant_trend_bands(rows: list[str]) -> list[str | None]:
    """Resolve dominant trend-score band per row from full/alias tokens.

    Returns CALM/EDGE/HEATED when a strict single dominant band exists for the
    row, otherwise None.
    """
    alias_to_band = {"C": "CALM", "E": "EDGE", "H": "HEATED"}
    dominant: list[str | None] = []

    for row in rows:
        row_counts = {"CALM": 0, "EDGE": 0, "HEATED": 0}
        for token in TREND_SCORE_BAND_RE.findall(row):
            normalized = token.strip().upper()
            if normalized in row_counts:
                row_counts[normalized] += 1
            elif normalized in alias_to_band:
                row_counts[alias_to_band[normalized]] += 1

        ordered = sorted(row_counts.items(), key=lambda item: (-item[1], item[0]))
        if not ordered or ordered[0][1] <= 0:
            dominant.append(None)
            continue

        top_count = ordered[0][1]
        tied = [band for band, count in ordered if count == top_count]
        dominant.append(tied[0] if len(tied) == 1 else None)

    return dominant


def resolve_trend_score_band_dispatch_pressure_momentum(rows: list[str]) -> int:
    """Compute offline momentum score (0..100) from dominant-band drift windows."""
    dominant_bands = [band for band in collect_row_dominant_trend_bands(rows) if band]
    if len(dominant_bands) < 2:
        return 0

    transitions = 0
    weighted_transitions = 0.0
    weight_total = 0.0
    for idx in range(1, len(dominant_bands)):
        changed = dominant_bands[idx] != dominant_bands[idx - 1]
        if changed:
            transitions += 1
        # Later transitions count slightly more than early transitions.
        weight = idx
        weight_total += weight
        if changed:
            weighted_transitions += weight

    transition_ratio = transitions / max(1, len(dominant_bands) - 1)
    weighted_ratio = weighted_transitions / weight_total if weight_total else 0.0
    diversity_ratio = len(set(dominant_bands)) / 3.0

    momentum = (transition_ratio * 0.5) + (weighted_ratio * 0.35) + (diversity_ratio * 0.15)
    return max(0, min(100, int(round(momentum * 100))))


def resolve_trend_score_band_dispatch_pressure_momentum_band(momentum_score: int) -> str:
    if momentum_score >= 67:
        return "HIGH"
    if momentum_score >= 34:
        return "MID"
    return "LOW"


def resolve_trend_score_band_dispatch_pressure_momentum_band_alias(momentum_band: str) -> str:
    alias_map = {
        "LOW": "L",
        "MID": "M",
        "HIGH": "H",
    }
    return alias_map.get(momentum_band, "L")


def resolve_trend_score_band_dispatch_hint(score_band_snapshot: dict[str, int]) -> str:
    ordered = sorted(
        score_band_snapshot.items(),
        key=lambda item: (-item[1], item[0]),
    )
    if not ordered or ordered[0][1] <= 0:
        return "BALANCED"

    top_count = ordered[0][1]
    tied = [band for band, count in ordered if count == top_count]
    if len(tied) > 1:
        return "BALANCED"

    band_to_hint = {
        "CALM": "CALM_FOCUS",
        "EDGE": "EDGE_FOCUS",
        "HEATED": "HEATED_FOCUS",
    }
    return band_to_hint.get(tied[0], "BALANCED")


def resolve_trend_score_band_dispatch_hint_alias(dispatch_hint: str) -> str:
    alias_map = {
        "CALM_FOCUS": "C",
        "EDGE_FOCUS": "E",
        "HEATED_FOCUS": "H",
        "BALANCED": "B",
    }
    return alias_map.get(dispatch_hint, "B")


def resolve_trend_score_band_dispatch_pressure(
    score_band_snapshot: dict[str, int],
    missing_cadence_buckets: list[str],
    over_cap_lanes: list[str],
) -> str:
    total = sum(score_band_snapshot.values())
    dominant_count = max(score_band_snapshot.values()) if score_band_snapshot else 0
    dominant_ratio = (dominant_count / total) if total else 0.0

    if missing_cadence_buckets or over_cap_lanes or dominant_ratio >= 0.6:
        return "HOT"
    if dominant_ratio >= 0.45:
        return "READY"
    return "LIGHT"


def resolve_trend_score_band_dispatch_pressure_alias(dispatch_pressure: str) -> str:
    alias_map = {
        "LIGHT": "L",
        "READY": "R",
        "HOT": "H",
    }
    return alias_map.get(dispatch_pressure, "L")


def build_report(rows: list[str], cap_ratio: float) -> dict:
    lane_counts = Counter()
    for row in rows:
        for lane in infer_lanes(row):
            lane_counts[lane] += 1

    score_band_snapshot = collect_trend_score_band_snapshot(rows)
    score_band_alias = (
        f"C{score_band_snapshot['CALM']}"
        f"E{score_band_snapshot['EDGE']}"
        f"H{score_band_snapshot['HEATED']}"
    )
    score_band_dispatch_hint = resolve_trend_score_band_dispatch_hint(score_band_snapshot)
    score_band_dispatch_hint_alias = resolve_trend_score_band_dispatch_hint_alias(
        score_band_dispatch_hint
    )

    total = len(rows)
    percentages = {
        lane: round((lane_counts.get(lane, 0) / total) * 100.0, 2) if total else 0.0
        for lane in CANONICAL_LANES
    }
    over_cap = sorted([lane for lane, pct in percentages.items() if pct > (cap_ratio * 100.0)])

    underrepresented = sorted(
        CANONICAL_LANES,
        key=lambda lane: (lane_counts.get(lane, 0), lane),
    )

    forced_next_lanes: list[str] = []
    if over_cap:
        forced_next_lanes = [lane for lane in underrepresented if lane not in over_cap][:3]

    bucket_status = {}
    missing_buckets: list[str] = []
    for bucket, bucket_lanes in BUCKETS.items():
        bucket_count = sum(lane_counts.get(lane, 0) for lane in bucket_lanes)
        met = bucket_count > 0
        bucket_status[bucket] = {
            "lanes": bucket_lanes,
            "count": bucket_count,
            "met": met,
        }
        if not met:
            missing_buckets.append(bucket)

    score_band_dispatch_pressure = resolve_trend_score_band_dispatch_pressure(
        score_band_snapshot,
        missing_buckets,
        over_cap,
    )
    score_band_dispatch_pressure_alias = resolve_trend_score_band_dispatch_pressure_alias(
        score_band_dispatch_pressure
    )
    score_band_dispatch_pressure_momentum = resolve_trend_score_band_dispatch_pressure_momentum(rows)
    score_band_dispatch_pressure_momentum_band = (
        resolve_trend_score_band_dispatch_pressure_momentum_band(score_band_dispatch_pressure_momentum)
    )
    score_band_dispatch_pressure_momentum_band_alias = (
        resolve_trend_score_band_dispatch_pressure_momentum_band_alias(
            score_band_dispatch_pressure_momentum_band
        )
    )

    return {
        "recentCompletedItems": total,
        "capPercent": round(cap_ratio * 100.0, 2),
        "laneCounts": {lane: lane_counts.get(lane, 0) for lane in CANONICAL_LANES},
        "lanePercentages": percentages,
        "overCapLanes": over_cap,
        "underrepresentedLanes": underrepresented,
        "forcedNextLanes": forced_next_lanes,
        "bucketCadence": bucket_status,
        "missingCadenceBuckets": missing_buckets,
        "trendScoreBandSnapshot": score_band_snapshot,
        "trendScoreBandSnapshotAlias": score_band_alias,
        "trendScoreBandDispatchHint": score_band_dispatch_hint,
        "trendScoreBandDispatchHintAlias": score_band_dispatch_hint_alias,
        "trendScoreBandDispatchPressure": score_band_dispatch_pressure,
        "trendScoreBandDispatchPressureAlias": score_band_dispatch_pressure_alias,
        "trendScoreBandDispatchPressureMomentum": score_band_dispatch_pressure_momentum,
        "trendScoreBandDispatchPressureMomentumBand": score_band_dispatch_pressure_momentum_band,
        "trendScoreBandDispatchPressureMomentumBandAlias": score_band_dispatch_pressure_momentum_band_alias,
        "status": "over-cap" if over_cap else "within-cap",
    }


def to_markdown(report: dict, recent_rows: list[str] | None = None) -> str:
    _ = recent_rows
    score_band_snapshot = report.get("trendScoreBandSnapshot", {"CALM": 0, "EDGE": 0, "HEATED": 0})
    score_band_summary = (
        f"CALM={score_band_snapshot['CALM']}, "
        f"EDGE={score_band_snapshot['EDGE']}, "
        f"HEATED={score_band_snapshot['HEATED']}"
    )
    rows = [
        "| lane | count | percent |",
        "|---|---:|---:|",
    ]
    for lane in CANONICAL_LANES:
        rows.append(f"| {lane} | {report['laneCounts'][lane]} | {report['lanePercentages'][lane]}% |")
    over_cap = ", ".join(report["overCapLanes"]) if report["overCapLanes"] else "none"
    forced = ", ".join(report["forcedNextLanes"]) if report["forcedNextLanes"] else "none"
    missing_buckets = ", ".join(report["missingCadenceBuckets"]) if report["missingCadenceBuckets"] else "none"
    bucket_rows = [
        "",
        "| cadence bucket | lanes | count | status |",
        "|---|---|---:|---|",
    ]
    for bucket, details in report["bucketCadence"].items():
        lanes = "/".join(details["lanes"])
        status = "met" if details["met"] else "missing"
        bucket_rows.append(f"| {bucket} | {lanes} | {details['count']} | {status} |")

    return "\n".join(
        [
            "### Lane Coverage Guardrail",
            f"- status: **{report['status']}** (cap={report['capPercent']}%)",
            f"- recent completed items: **{report['recentCompletedItems']}**",
            f"- over-cap lanes: **{over_cap}**",
            f"- forced next lanes (if over-cap): **{forced}**",
            f"- cadence buckets missing: **{missing_buckets}**",
            f"- trend-score band snapshot (recent rows): **{score_band_summary}**",
            f"- trend-score band snapshot alias: **TSSB:{report.get('trendScoreBandSnapshotAlias', 'C0E0H0')}**",
            "- trend-score alias decode: **TSSB legend (C=calm, E=edge, H=heated)**",
            f"- trend-score dispatch hint (offline): **{report.get('trendScoreBandDispatchHint', 'BALANCED')}**",
            f"- trend-score dispatch hint alias: **TSDH:{report.get('trendScoreBandDispatchHintAlias', 'B')}**",
            f"- trend-score dispatch pressure (offline): **{report.get('trendScoreBandDispatchPressure', 'LIGHT')}**",
            f"- trend-score dispatch pressure alias: **TSDP:{report.get('trendScoreBandDispatchPressureAlias', 'L')}**",
            f"- trend-score dispatch-pressure momentum (offline): **{report.get('trendScoreBandDispatchPressureMomentum', 0)}**",
            f"- trend-score dispatch-pressure momentum band (offline): **{report.get('trendScoreBandDispatchPressureMomentumBand', 'LOW')}**",
            f"- trend-score dispatch-pressure momentum band alias: **TSDPM:{report.get('trendScoreBandDispatchPressureMomentumBandAlias', 'L')}**",
            "",
            *rows,
            *bucket_rows,
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
        args.md_out.write_text(to_markdown(report, recent_rows=rows) + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
