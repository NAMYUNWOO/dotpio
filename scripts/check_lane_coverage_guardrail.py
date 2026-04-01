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
    return resolve_trend_score_band_dispatch_pressure_momentum_from_dominant_bands(dominant_bands)


def resolve_trend_score_band_dispatch_pressure_momentum_from_dominant_bands(
    dominant_bands: list[str],
) -> int:
    """Compute offline momentum score (0..100) from dominant-band sequence."""
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


def resolve_trend_score_band_dispatch_pressure_momentum_slope(rows: list[str]) -> str:
    """Compute offline momentum-slope label from prior-window momentum deltas.

    Domain is intentionally compact/deterministic: COOLING | RISING | SURGING.
    """
    dominant_bands = [band for band in collect_row_dominant_trend_bands(rows) if band]
    if len(dominant_bands) < 3:
        return "COOLING"

    rolling_scores: list[int] = []
    for end_idx in range(2, len(dominant_bands) + 1):
        rolling_scores.append(
            resolve_trend_score_band_dispatch_pressure_momentum_from_dominant_bands(
                dominant_bands[:end_idx]
            )
        )

    if len(rolling_scores) < 2:
        return "COOLING"

    last_delta = rolling_scores[-1] - rolling_scores[-2]
    prev_delta = rolling_scores[-2] - rolling_scores[-3] if len(rolling_scores) >= 3 else 0

    if last_delta >= 15 or (last_delta >= 8 and prev_delta > 0):
        return "SURGING"
    if last_delta > 0:
        return "RISING"
    return "COOLING"


def resolve_trend_score_band_dispatch_pressure_momentum_slope_alias(momentum_slope: str) -> str:
    alias_map = {
        "COOLING": "C",
        "RISING": "R",
        "SURGING": "S",
    }
    return alias_map.get(momentum_slope, "C")


def resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation(
    momentum_slope: str,
) -> str:
    recommendation_map = {
        "COOLING": "hold steady; validate calm-lane continuity",
        "RISING": "prep focused sweeps; stage next-lane handoff",
        "SURGING": "escalate triage; clamp hottest-lane drift",
    }
    return recommendation_map.get(momentum_slope, recommendation_map["COOLING"])


def resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation_state(
    momentum_slope: str,
) -> str:
    state_map = {
        "COOLING": "HOLD",
        "RISING": "PREP",
        "SURGING": "CLAMP",
    }
    return state_map.get(momentum_slope, "HOLD")


def resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation_alias(
    recommendation_state: str,
) -> str:
    alias_map = {
        "HOLD": "H",
        "PREP": "P",
        "CLAMP": "C",
    }
    return alias_map.get(recommendation_state, "H")


def resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation_family(
    recommendation_state: str,
) -> str:
    family_map = {
        "HOLD": "STABLE",
        "PREP": "READY",
        "CLAMP": "TRIAGE",
    }
    return family_map.get(recommendation_state, "STABLE")


def resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation_family_alias(
    recommendation_family: str,
) -> str:
    alias_map = {
        "STABLE": "S",
        "READY": "R",
        "TRIAGE": "T",
    }
    return alias_map.get(recommendation_family, "S")


def resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation_family_trend(
    current_family: str,
    prior_family: str,
) -> str:
    rank = {
        "STABLE": 0,
        "READY": 1,
        "TRIAGE": 2,
    }
    current_rank = rank.get(current_family, 0)
    prior_rank = rank.get(prior_family, 0)
    if current_rank > prior_rank:
        return "UP"
    if current_rank < prior_rank:
        return "DOWN"
    return "FLAT"


def resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation_family_trend_alias(
    trend: str,
) -> str:
    alias_map = {
        "UP": "U",
        "FLAT": "F",
        "DOWN": "D",
    }
    return alias_map.get(trend, "F")


def resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation_family_trend_why(
    trend: str,
) -> str:
    mapping = {
        "UP": "escalate pressure checks",
        "FLAT": "hold pressure cadence",
        "DOWN": "cool pressure posture",
    }
    return mapping.get(trend, "hold pressure cadence")


def resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation_family_trend_why_alias(
    trend: str,
) -> str:
    alias_map = {
        "UP": "E",
        "FLAT": "H",
        "DOWN": "C",
    }
    return alias_map.get(trend, "H")


def resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation_family_trend_why_copy_budget(
    threshold: int = 32,
) -> str:
    budget = (
        resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation_family_trend_why_copy_budget_signals(
            threshold=threshold
        )
    )
    lengths = budget["lengths"]
    max_len = budget["maxLen"]
    return (
        f"TSDPMSRFTWHYLEN:E{lengths['E']}|H{lengths['H']}|C{lengths['C']}|"
        f"MAX{max_len}/{threshold}"
    )


def resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation_family_trend_why_copy_budget_signals(
    threshold: int = 32,
) -> dict[str, object]:
    copy_map = {
        "E": "escalate pressure checks",
        "H": "hold pressure cadence",
        "C": "cool pressure posture",
    }
    lengths = {alias: len(text) for alias, text in copy_map.items()}
    max_len = max(lengths.values()) if lengths else 0
    return {
        "copyMap": copy_map,
        "lengths": lengths,
        "threshold": threshold,
        "maxLen": max_len,
    }


def build_momentum_band_progression_sparkline(rows: list[str]) -> str:
    """Build compact sparkline over rolling momentum-band progression for recent rows.

    Example output: LMMMHHHH (oldest -> newest).
    """
    dominant_bands = [band for band in collect_row_dominant_trend_bands(rows) if band]
    if len(dominant_bands) < 2:
        return "NA"

    aliases: list[str] = []
    for end_idx in range(2, len(dominant_bands) + 1):
        score = resolve_trend_score_band_dispatch_pressure_momentum_from_dominant_bands(
            dominant_bands[:end_idx]
        )
        band = resolve_trend_score_band_dispatch_pressure_momentum_band(score)
        aliases.append(resolve_trend_score_band_dispatch_pressure_momentum_band_alias(band))

    return "".join(aliases) if aliases else "NA"


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


def resolve_trend_score_band_dispatch_pressure_momentum_fx_cue(momentum_band: str) -> str:
    cue_map = {
        "LOW": "SOFT",
        "MID": "EDGE",
        "HIGH": "HARD",
    }
    return cue_map.get(momentum_band, "SOFT")


def resolve_trend_score_band_dispatch_pressure_momentum_fx_cue_alias(momentum_fx_cue: str) -> str:
    alias_map = {
        "SOFT": "S",
        "EDGE": "E",
        "HARD": "H",
    }
    return alias_map.get(momentum_fx_cue, "S")


def resolve_trend_score_band_dispatch_pressure_momentum_fx_cue_microcopy_recommendation(
    momentum_fx_cue: str,
) -> str:
    recommendation_map = {
        "SOFT": "steady pace; hold broad scan",
        "EDGE": "pressure rising; prep focused dispatch",
        "HARD": "surge pressure; triage hottest lane first",
    }
    return recommendation_map.get(momentum_fx_cue, recommendation_map["SOFT"])


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
    score_band_dispatch_pressure_momentum_fx_cue = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_cue(
            score_band_dispatch_pressure_momentum_band
        )
    )
    score_band_dispatch_pressure_momentum_fx_cue_alias = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_cue_alias(
            score_band_dispatch_pressure_momentum_fx_cue
        )
    )
    score_band_dispatch_pressure_momentum_fx_cue_microcopy_recommendation = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_cue_microcopy_recommendation(
            score_band_dispatch_pressure_momentum_fx_cue
        )
    )
    score_band_dispatch_pressure_momentum_band_sparkline = build_momentum_band_progression_sparkline(
        rows
    )
    score_band_dispatch_pressure_momentum_slope = (
        resolve_trend_score_band_dispatch_pressure_momentum_slope(rows)
    )
    score_band_dispatch_pressure_momentum_slope_alias = (
        resolve_trend_score_band_dispatch_pressure_momentum_slope_alias(
            score_band_dispatch_pressure_momentum_slope
        )
    )
    score_band_dispatch_pressure_momentum_slope_recommendation = (
        resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation(
            score_band_dispatch_pressure_momentum_slope
        )
    )
    score_band_dispatch_pressure_momentum_slope_recommendation_state = (
        resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation_state(
            score_band_dispatch_pressure_momentum_slope
        )
    )
    score_band_dispatch_pressure_momentum_slope_recommendation_alias = (
        resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation_alias(
            score_band_dispatch_pressure_momentum_slope_recommendation_state
        )
    )
    score_band_dispatch_pressure_momentum_slope_recommendation_family = (
        resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation_family(
            score_band_dispatch_pressure_momentum_slope_recommendation_state
        )
    )
    score_band_dispatch_pressure_momentum_slope_recommendation_family_alias = (
        resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation_family_alias(
            score_band_dispatch_pressure_momentum_slope_recommendation_family
        )
    )
    prior_rows = rows[:-1] if len(rows) > 1 else rows
    prior_momentum_slope = resolve_trend_score_band_dispatch_pressure_momentum_slope(prior_rows)
    prior_recommendation_state = (
        resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation_state(
            prior_momentum_slope
        )
    )
    prior_recommendation_family = (
        resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation_family(
            prior_recommendation_state
        )
    )
    score_band_dispatch_pressure_momentum_slope_recommendation_family_trend = (
        resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation_family_trend(
            score_band_dispatch_pressure_momentum_slope_recommendation_family,
            prior_recommendation_family,
        )
    )
    score_band_dispatch_pressure_momentum_slope_recommendation_family_trend_alias = (
        resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation_family_trend_alias(
            score_band_dispatch_pressure_momentum_slope_recommendation_family_trend
        )
    )
    why_copy_budget_signals = (
        resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation_family_trend_why_copy_budget_signals()
    )
    why_copy_budget_token = (
        resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation_family_trend_why_copy_budget(
            threshold=int(why_copy_budget_signals["threshold"])
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
        "trendScoreBandDispatchPressureMomentumFxCue": score_band_dispatch_pressure_momentum_fx_cue,
        "trendScoreBandDispatchPressureMomentumFxCueAlias": score_band_dispatch_pressure_momentum_fx_cue_alias,
        "trendScoreBandDispatchPressureMomentumFxCueMicrocopyRecommendation": score_band_dispatch_pressure_momentum_fx_cue_microcopy_recommendation,
        "trendScoreBandDispatchPressureMomentumBandSparkline": score_band_dispatch_pressure_momentum_band_sparkline,
        "trendScoreBandDispatchPressureMomentumSlope": score_band_dispatch_pressure_momentum_slope,
        "trendScoreBandDispatchPressureMomentumSlopeAlias": score_band_dispatch_pressure_momentum_slope_alias,
        "trendScoreBandDispatchPressureMomentumSlopeRecommendation": score_band_dispatch_pressure_momentum_slope_recommendation,
        "trendScoreBandDispatchPressureMomentumSlopeRecommendationState": score_band_dispatch_pressure_momentum_slope_recommendation_state,
        "trendScoreBandDispatchPressureMomentumSlopeRecommendationAlias": score_band_dispatch_pressure_momentum_slope_recommendation_alias,
        "trendScoreBandDispatchPressureMomentumSlopeRecommendationFamily": score_band_dispatch_pressure_momentum_slope_recommendation_family,
        "trendScoreBandDispatchPressureMomentumSlopeRecommendationFamilyAlias": score_band_dispatch_pressure_momentum_slope_recommendation_family_alias,
        "trendScoreBandDispatchPressureMomentumSlopeRecommendationFamilyTrend": score_band_dispatch_pressure_momentum_slope_recommendation_family_trend,
        "trendScoreBandDispatchPressureMomentumSlopeRecommendationFamilyTrendAlias": score_band_dispatch_pressure_momentum_slope_recommendation_family_trend_alias,
        "trendScoreBandDispatchPressureMomentumSlopeRecommendationFamilyTrendWhyCopyBudget": why_copy_budget_token,
        "trendScoreBandDispatchPressureMomentumSlopeRecommendationFamilyTrendWhyCopyBudgetSignals": why_copy_budget_signals,
        "status": "over-cap" if over_cap else "within-cap",
    }


def to_markdown(
    report: dict,
    recent_rows: list[str] | None = None,
    include_trend_family_why: bool = False,
) -> str:
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

    optional_rows: list[str] = []
    if include_trend_family_why:
        family_trend = report.get(
            "trendScoreBandDispatchPressureMomentumSlopeRecommendationFamilyTrend",
            "FLAT",
        )
        optional_rows.extend(
            [
                "- trend-score momentum-slope rec family trend decode variant (design/world): **TSDPMSRFT legend (U=escalate, F=hold, D=cool)**",
                f"- trend-score momentum-slope rec family trend why alias: **TSDPMSRFTWHYA:{resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation_family_trend_why_alias(family_trend)}**",
                "- trend-score momentum-slope rec family trend why alias decode: **TSDPMSRFTWHYA legend (E=escalate, H=hold, C=cool)**",
                f"- trend-score momentum-slope rec family trend why (ai-content/systems): **TSDPMSRFT WHY:{resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation_family_trend_why(family_trend)}**",
                "- trend-score momentum-slope rec family trend why copy budget (design/ux): "
                f"**{report.get('trendScoreBandDispatchPressureMomentumSlopeRecommendationFamilyTrendWhyCopyBudget', resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation_family_trend_why_copy_budget())}**",
            ]
        )

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
            "- trend-score dispatch-pressure momentum band progression (last-10 rolling): "
            f"**TSDPM-SPARK:{report.get('trendScoreBandDispatchPressureMomentumBandSparkline', 'NA')}**",
            "- trend-score momentum sparkline legend: **L=LOW, M=MID, H=HIGH (older->newer)**",
            f"- trend-score dispatch-pressure momentum slope (ai-content/systems): **{report.get('trendScoreBandDispatchPressureMomentumSlope', 'COOLING')}**",
            f"- trend-score dispatch-pressure momentum slope alias: **TSDPMS:{report.get('trendScoreBandDispatchPressureMomentumSlopeAlias', 'C')}**",
            f"- trend-score momentum-slope rec state alias: **TSDPMSR:{report.get('trendScoreBandDispatchPressureMomentumSlopeRecommendationAlias', 'H')}** ({report.get('trendScoreBandDispatchPressureMomentumSlopeRecommendationState', 'HOLD')})",
            "- trend-score momentum-slope rec decode: **TSDPMSR legend (H=HOLD, P=PREP, C=CLAMP)**",
            f"- trend-score momentum-slope rec family alias: **TSDPMSRF:{report.get('trendScoreBandDispatchPressureMomentumSlopeRecommendationFamilyAlias', 'S')}** ({report.get('trendScoreBandDispatchPressureMomentumSlopeRecommendationFamily', 'STABLE')})",
            "- trend-score momentum-slope rec family decode: **TSDPMSRF legend (S=STABLE, R=READY, T=TRIAGE)**",
            f"- trend-score momentum-slope rec family trend alias: **TSDPMSRFT:{report.get('trendScoreBandDispatchPressureMomentumSlopeRecommendationFamilyTrendAlias', 'F')}** ({report.get('trendScoreBandDispatchPressureMomentumSlopeRecommendationFamilyTrend', 'FLAT')})",
            "- trend-score momentum-slope rec family trend decode: **TSDPMSRFT legend (U=UP, F=FLAT, D=DOWN)**",
            f"- trend-score dispatch-pressure momentum slope rec (ai-content/systems): **{report.get('trendScoreBandDispatchPressureMomentumSlopeRecommendation', 'hold steady; validate calm-lane continuity')}**",
            f"- trend-score dispatch-pressure momentum fx cue (combat/vfx): **{report.get('trendScoreBandDispatchPressureMomentumFxCue', 'SOFT')}**",
            f"- trend-score dispatch-pressure momentum fx cue alias: **TSDPMFX:{report.get('trendScoreBandDispatchPressureMomentumFxCueAlias', 'S')}**",
            "- trend-score dispatch-pressure momentum fx cue cadence decode (design/world): **SOFT=CALM cadence, EDGE=EDGE cadence, HARD=HEATED cadence**",
            f"- trend-score dispatch-pressure momentum fx cue microcopy rec (ai-content/design): **{report.get('trendScoreBandDispatchPressureMomentumFxCueMicrocopyRecommendation', 'steady pace; hold broad scan')}**",
            *optional_rows,
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
    parser.add_argument(
        "--include-trend-family-why",
        action="store_true",
        help="Include optional TSDPMSRFT WHY rationale + decode variant rows in markdown output.",
    )
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
        args.md_out.write_text(
            to_markdown(
                report,
                recent_rows=rows,
                include_trend_family_why=args.include_trend_family_why,
            )
            + "\n",
            encoding="utf-8",
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
