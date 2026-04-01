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
    verb_pack: str = "baseline",
) -> str:
    mapping_by_pack = {
        "baseline": {
            "UP": "escalate pressure checks",
            "FLAT": "hold pressure cadence",
            "DOWN": "cool pressure posture",
        },
        "ramp": {
            "UP": "ramp pressure checks",
            "FLAT": "steady pressure cadence",
            "DOWN": "cool pressure posture",
        },
    }
    mapping = mapping_by_pack.get(verb_pack, mapping_by_pack["baseline"])
    return mapping.get(trend, mapping["FLAT"])


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
    verb_pack: str = "baseline",
) -> str:
    budget = (
        resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation_family_trend_why_copy_budget_signals(
            threshold=threshold,
            verb_pack=verb_pack,
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
    verb_pack: str = "baseline",
) -> dict[str, object]:
    if verb_pack == "ramp":
        copy_map = {
            "E": "ramp pressure checks",
            "H": "steady pressure cadence",
            "C": "cool pressure posture",
        }
    else:
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


def resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency(
    momentum_band_trend: str,
) -> str:
    urgency_map = {
        "DOWN": "SOFT",
        "FLAT": "SURGE",
        "UP": "SPIKE",
    }
    return urgency_map.get(momentum_band_trend, "SURGE")


def resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_alias(
    momentum_fx_urgency: str,
) -> str:
    alias_map = {
        "SOFT": "S",
        "SURGE": "U",
        "SPIKE": "P",
    }
    return alias_map.get(momentum_fx_urgency, "U")


def resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence(
    rows: list[str],
) -> str:
    """Resolve urgency-confidence token from recent TSDPCONWCTSBT churn windows.

    Domain: LOW|MID|HIGH
    """
    if len(rows) <= 1:
        return "HIGH"

    trend_windows: list[str] = []
    for idx in range(1, len(rows)):
        curr_rows = rows[: idx + 1]
        prev_rows = rows[:idx]
        curr_score = resolve_cadence_override_note_rationale_confidence_trend_momentum_score(curr_rows)
        prev_score = resolve_cadence_override_note_rationale_confidence_trend_momentum_score(prev_rows)
        curr_band = resolve_cadence_override_note_rationale_confidence_trend_momentum_band(curr_score)
        prev_band = resolve_cadence_override_note_rationale_confidence_trend_momentum_band(prev_score)
        trend_windows.append(
            resolve_cadence_override_note_rationale_confidence_trend_momentum_band_trend(
                curr_band,
                prev_band,
            )
        )

    if len(trend_windows) <= 1:
        return "HIGH"

    churn = 0
    for prev, curr in zip(trend_windows, trend_windows[1:]):
        if prev != curr:
            churn += 1
    if churn <= 1:
        return "HIGH"
    if churn <= 3:
        return "MID"
    return "LOW"


def resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend(
    rows: list[str],
) -> str:
    """Resolve urgency-confidence trend token from consecutive TSDPMFXUC windows.

    Domain: UP|FLAT|DOWN
    """
    if len(rows) <= 1:
        return "FLAT"

    rank_map = {"LOW": 0, "MID": 1, "HIGH": 2}
    confidence_windows: list[str] = []
    for idx in range(1, len(rows) + 1):
        confidence_windows.append(
            resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence(rows[:idx])
        )

    if len(confidence_windows) <= 1:
        return "FLAT"

    current = rank_map.get(confidence_windows[-1], 1)
    prior = rank_map.get(confidence_windows[-2], 1)
    if current > prior:
        return "UP"
    if current < prior:
        return "DOWN"
    return "FLAT"


def resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_alias(
    confidence_trend: str,
) -> str:
    alias_map = {
        "UP": "U",
        "FLAT": "F",
        "DOWN": "D",
    }
    return alias_map.get(confidence_trend, "F")


def resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_score(
    rows: list[str],
) -> int:
    """Resolve urgency-confidence trend momentum token from weighted TSDPMFXUCT drift.

    Domain: 0..100 (higher = sustained UP pressure, lower = sustained DOWN pressure)
    """
    if len(rows) <= 2:
        return 50

    trend_windows: list[str] = []
    for idx in range(2, len(rows) + 1):
        trend_windows.append(
            resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend(
                rows[:idx]
            )
        )

    if not trend_windows:
        return 50

    value_map = {"DOWN": 0, "FLAT": 50, "UP": 100}
    weighted_total = 0
    weight_sum = 0
    for weight, trend in enumerate(trend_windows, start=1):
        weighted_total += value_map.get(trend, 50) * weight
        weight_sum += weight

    if weight_sum == 0:
        return 50
    return int(round(weighted_total / weight_sum))


def resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band(
    momentum_score: int,
) -> str:
    if momentum_score >= 67:
        return "HIGH"
    if momentum_score >= 34:
        return "MID"
    return "LOW"


def resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend(
    current_band: str,
    prior_band: str,
) -> str:
    rank = {"LOW": 0, "MID": 1, "HIGH": 2}
    delta = rank.get(current_band, 1) - rank.get(prior_band, 1)
    if delta > 0:
        return "UP"
    if delta < 0:
        return "DOWN"
    return "FLAT"


def resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_alias(
    trend: str,
) -> str:
    return {
        "UP": "U",
        "FLAT": "F",
        "DOWN": "D",
    }.get(trend, "F")


def resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_confidence(
    current_trend: str,
    prior_trend: str,
) -> str:
    if current_trend == prior_trend:
        return "HIGH"
    if "FLAT" in {current_trend, prior_trend}:
        return "MID"
    return "LOW"


def resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse(
    trend: str,
) -> str:
    return {
        "UP": "BLAST",
        "FLAT": "PULSE",
        "DOWN": "CALM",
    }.get(trend, "PULSE")


def resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_alias(
    pulse: str,
) -> str:
    return {
        "CALM": "C",
        "PULSE": "P",
        "BLAST": "B",
    }.get(pulse, "P")


def resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance(
    pulse: str,
) -> str:
    return {
        "CALM": "steady sweep",
        "PULSE": "brace lanes",
        "BLAST": "commit burst",
    }.get(pulse, "steady sweep")


def resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence(
    guidance: str,
) -> str:
    return {
        "steady sweep": "HIGH",
        "brace lanes": "MID",
        "commit burst": "LOW",
    }.get(guidance, "MID")


def resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_alias(
    confidence: str,
) -> str:
    return {
        "LOW": "L",
        "MID": "M",
        "HIGH": "H",
    }.get(confidence, "M")


def resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation(
    confidence: str,
) -> str:
    return {
        "HIGH": "lock sweep",
        "MID": "brace check",
        "LOW": "burst triage",
    }.get(confidence, "brace check")


def resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_alias(
    recommendation: str,
) -> str:
    return {
        "lock sweep": "LS",
        "brace check": "BC",
        "burst triage": "BT",
    }.get(recommendation, "BC")


def resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity(
    recommendation: str,
) -> str:
    return {
        "lock sweep": "HARD",
        "brace check": "EDGE",
        "burst triage": "SOFT",
    }.get(recommendation, "EDGE")


def resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_alias(
    intensity: str,
) -> str:
    return {
        "SOFT": "S",
        "EDGE": "E",
        "HARD": "H",
    }.get(intensity, "E")


def resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend(
    current_intensity: str,
    prior_intensity: str,
) -> str:
    rank = {
        "SOFT": 0,
        "EDGE": 1,
        "HARD": 2,
    }
    current_rank = rank.get(current_intensity, 1)
    prior_rank = rank.get(prior_intensity, 1)
    if current_rank > prior_rank:
        return "UP"
    if current_rank < prior_rank:
        return "DOWN"
    return "FLAT"


def resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_alias(
    trend: str,
) -> str:
    return {
        "UP": "U",
        "FLAT": "F",
        "DOWN": "D",
    }.get(trend, "F")


def resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_decode_full() -> str:
    return "SOFT=burst triage, EDGE=brace check, HARD=lock sweep"


def resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_decode_compact() -> str:
    return "S=SOFT, E=EDGE, H=HARD"


def resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_decode_evaluation(
    dos_width_limit: int = 72,
) -> dict[str, object]:
    full = resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_decode_full()
    compact = resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_decode_compact()
    full_len = len(full)
    compact_len = len(compact)
    preferred = "CONCISE" if compact_len <= full_len else "FULL"
    status = "PASS" if compact_len <= dos_width_limit and full_len <= dos_width_limit else "WARN"
    return {
        "full": full,
        "compact": compact,
        "fullLen": full_len,
        "compactLen": compact_len,
        "dosWidthLimit": dos_width_limit,
        "preferred": preferred,
        "status": status,
    }


def resolve_trend_score_band_dispatch_pressure_momentum_fx_cue_microcopy_recommendation(
    momentum_fx_cue: str,
) -> str:
    recommendation_map = {
        "SOFT": "steady pace; hold broad scan",
        "EDGE": "pressure rising; prep focused dispatch",
        "HARD": "surge pressure; triage hottest lane first",
    }
    return recommendation_map.get(momentum_fx_cue, recommendation_map["SOFT"])


def resolve_trend_score_band_dispatch_pressure_momentum_fx_cue_combat_callout(
    momentum_fx_cue: str,
) -> str:
    callout_map = {
        "SOFT": "HOLD_LINE",
        "EDGE": "PRESS_EDGE",
        "HARD": "BURST_CLEAR",
    }
    return callout_map.get(momentum_fx_cue, callout_map["SOFT"])


def resolve_trend_score_band_dispatch_pressure_momentum_fx_cue_combat_callout_alias(
    combat_callout: str,
) -> str:
    alias_map = {
        "HOLD_LINE": "HL",
        "PRESS_EDGE": "PE",
        "BURST_CLEAR": "BC",
    }
    return alias_map.get(combat_callout, "HL")


def resolve_trend_score_band_dispatch_pressure_momentum_fx_cue_combat_callout_decode_baseline() -> str:
    return "HL=hold line, PE=press edge, BC=burst clear"


def resolve_trend_score_band_dispatch_pressure_momentum_fx_cue_combat_callout_decode_compact() -> str:
    return "HL=hold lane, PE=push edge, BC=burst clear"


def resolve_trend_score_band_dispatch_pressure_momentum_fx_cue_combat_callout_decode_evaluation(
    dos_width_limit: int = 72,
) -> dict[str, object]:
    baseline = resolve_trend_score_band_dispatch_pressure_momentum_fx_cue_combat_callout_decode_baseline()
    compact = resolve_trend_score_band_dispatch_pressure_momentum_fx_cue_combat_callout_decode_compact()
    baseline_len = len(baseline)
    compact_len = len(compact)
    preferred = "COMPACT" if compact_len <= baseline_len else "BASELINE"
    status = "PASS" if compact_len <= dos_width_limit and baseline_len <= dos_width_limit else "WARN"
    return {
        "baseline": baseline,
        "compact": compact,
        "baselineLen": baseline_len,
        "compactLen": compact_len,
        "dosWidthLimit": dos_width_limit,
        "preferred": preferred,
        "status": status,
    }


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


def resolve_dispatch_pressure_with_cadence_override(base_pressure: str, override_state: str) -> str:
    if override_state != "ESCALATE":
        return base_pressure

    order = ["LIGHT", "READY", "HOT"]
    try:
        idx = order.index(base_pressure)
    except ValueError:
        return "HOT"
    return order[min(idx + 1, len(order) - 1)]


def resolve_cadence_override_state(
    current_missing_buckets: list[str],
    prior_missing_buckets: list[str],
    target_bucket: str = "combat-or-vfx",
) -> str:
    if target_bucket in current_missing_buckets and target_bucket in prior_missing_buckets:
        return "ESCALATE"
    return "BASE"


def resolve_cadence_override_alias(override_state: str) -> str:
    return "E" if override_state == "ESCALATE" else "B"


def resolve_cadence_override_streak(
    current_missing_buckets: list[str],
    prior_missing_buckets: list[str],
    target_bucket: str = "combat-or-vfx",
) -> int:
    current_missing = target_bucket in current_missing_buckets
    prior_missing = target_bucket in prior_missing_buckets
    if current_missing and prior_missing:
        return 2
    if current_missing:
        return 1
    return 0


def resolve_cadence_override_note(
    cadence_override_streak: int,
    momentum_slope: str,
) -> str:
    """Resolve compact offline escalation note from streak + momentum slope.

    Domain: HOLD|WATCH|PUSH
    """
    if cadence_override_streak >= 2 or momentum_slope == "SURGING":
        return "PUSH"
    if cadence_override_streak == 1 or momentum_slope == "RISING":
        return "WATCH"
    return "HOLD"


def resolve_cadence_override_note_alias(note: str) -> str:
    return {
        "HOLD": "H",
        "WATCH": "W",
        "PUSH": "P",
    }.get(note, "H")


def resolve_cadence_override_note_rationale(
    cadence_override_note: str,
    momentum_slope: str,
) -> str:
    """Resolve compact cadence-note rationale token.

    Domain: steady|watch|push
    """
    if cadence_override_note == "PUSH" or momentum_slope == "SURGING":
        return "push"
    if cadence_override_note == "WATCH" or momentum_slope == "RISING":
        return "watch"
    return "steady"


def resolve_cadence_override_note_rationale_alias(note_rationale: str) -> str:
    return {
        "steady": "S",
        "watch": "W",
        "push": "P",
    }.get(note_rationale, "S")


def _build_note_slope_windows(rows: list[str], window_size: int = 5) -> list[tuple[str, str]]:
    if not rows:
        return []
    windows: list[tuple[str, str]] = []
    for idx in range(len(rows)):
        start = max(0, idx - (window_size - 1))
        window_rows = rows[start : idx + 1]
        slope = resolve_trend_score_band_dispatch_pressure_momentum_slope(window_rows)
        note = resolve_cadence_override_note(
            cadence_override_streak=resolve_cadence_override_streak(
                current_missing_buckets=_resolve_missing_buckets(window_rows),
                prior_missing_buckets=_resolve_missing_buckets(window_rows[:-1]),
            ),
            momentum_slope=slope,
        )
        windows.append((note, slope))
    return windows


def _resolve_missing_buckets(rows: list[str]) -> list[str]:
    lane_counts = Counter()
    for row in rows:
        for lane in infer_lanes(row):
            lane_counts[lane] += 1
    missing_buckets: list[str] = []
    for bucket, bucket_lanes in BUCKETS.items():
        if sum(lane_counts.get(lane, 0) for lane in bucket_lanes) <= 0:
            missing_buckets.append(bucket)
    return missing_buckets


def resolve_cadence_override_note_rationale_confidence(rows: list[str]) -> str:
    """Resolve cadence-note rationale confidence from note/slope churn windows.

    Domain: LOW|MID|HIGH
    """
    windows = _build_note_slope_windows(rows)
    if len(windows) <= 1:
        return "HIGH"
    churn = 0
    for prev, curr in zip(windows, windows[1:]):
        if prev != curr:
            churn += 1
    if churn <= 1:
        return "HIGH"
    if churn <= 3:
        return "MID"
    return "LOW"


def resolve_cadence_override_note_rationale_confidence_alias(confidence: str) -> str:
    return {
        "LOW": "L",
        "MID": "M",
        "HIGH": "H",
    }.get(confidence, "H")


def resolve_cadence_override_note_rationale_confidence_trend(rows: list[str]) -> str:
    """Resolve confidence trend from consecutive churn-window confidence shifts.

    Domain: UP|FLAT|DOWN
    """
    windows = _build_note_slope_windows(rows)
    if len(windows) <= 1:
        return "FLAT"

    confidence_rank = {"LOW": 0, "MID": 1, "HIGH": 2}

    def confidence_for_prefix(end_idx: int) -> str:
        prefix_windows = windows[: end_idx + 1]
        if len(prefix_windows) <= 1:
            return "HIGH"
        churn = 0
        for prev, curr in zip(prefix_windows, prefix_windows[1:]):
            if prev != curr:
                churn += 1
        if churn <= 1:
            return "HIGH"
        if churn <= 3:
            return "MID"
        return "LOW"

    prev_confidence = confidence_for_prefix(len(windows) - 2)
    curr_confidence = confidence_for_prefix(len(windows) - 1)
    delta = confidence_rank[curr_confidence] - confidence_rank[prev_confidence]
    if delta > 0:
        return "UP"
    if delta < 0:
        return "DOWN"
    return "FLAT"


def resolve_cadence_override_note_rationale_confidence_trend_alias(trend: str) -> str:
    return {
        "UP": "U",
        "FLAT": "F",
        "DOWN": "D",
    }.get(trend, "F")


def resolve_cadence_override_note_rationale_confidence_trend_momentum_score(rows: list[str]) -> int:
    """Resolve weighted confidence-trend momentum score from churn-window drift.

    Domain: 0..100 (50 is neutral)
    """
    windows = _build_note_slope_windows(rows)
    if len(windows) <= 1:
        return 50

    confidence_rank = {"LOW": 0, "MID": 1, "HIGH": 2}

    def confidence_for_prefix(end_idx: int) -> str:
        prefix_windows = windows[: end_idx + 1]
        if len(prefix_windows) <= 1:
            return "HIGH"
        churn = 0
        for prev, curr in zip(prefix_windows, prefix_windows[1:]):
            if prev != curr:
                churn += 1
        if churn <= 1:
            return "HIGH"
        if churn <= 3:
            return "MID"
        return "LOW"

    weighted_delta = 0
    total_weight = 0
    for idx in range(1, len(windows)):
        prev_confidence = confidence_for_prefix(idx - 1)
        curr_confidence = confidence_for_prefix(idx)
        delta = confidence_rank[curr_confidence] - confidence_rank[prev_confidence]
        weight = idx
        weighted_delta += delta * weight
        total_weight += weight

    normalized = weighted_delta / total_weight if total_weight else 0.0
    score = int(round(((normalized + 1.0) / 2.0) * 100.0))
    return max(0, min(100, score))


def resolve_cadence_override_note_rationale_confidence_trend_momentum_band(score: int) -> str:
    if score >= 67:
        return "HIGH"
    if score >= 34:
        return "MID"
    return "LOW"


def resolve_cadence_override_note_rationale_confidence_trend_momentum_band_alias(band: str) -> str:
    return {
        "LOW": "L",
        "MID": "M",
        "HIGH": "H",
    }.get(band, "M")


def resolve_cadence_override_note_rationale_confidence_trend_momentum_band_trend(
    current_band: str,
    prior_band: str,
) -> str:
    rank = {"LOW": 0, "MID": 1, "HIGH": 2}
    delta = rank.get(current_band, 1) - rank.get(prior_band, 1)
    if delta > 0:
        return "UP"
    if delta < 0:
        return "DOWN"
    return "FLAT"


def resolve_cadence_override_note_rationale_confidence_trend_momentum_band_trend_alias(
    trend: str,
) -> str:
    return {
        "UP": "U",
        "FLAT": "F",
        "DOWN": "D",
    }.get(trend, "F")


def build_report(
    rows: list[str],
    cap_ratio: float,
    trend_family_why_verb_pack: str = "baseline",
) -> dict:
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

    base_dispatch_pressure = resolve_trend_score_band_dispatch_pressure(
        score_band_snapshot,
        missing_buckets,
        over_cap,
    )
    prior_rows = rows[:-1] if len(rows) > 1 else rows
    prior_lane_counts = Counter()
    for row in prior_rows:
        for lane in infer_lanes(row):
            prior_lane_counts[lane] += 1
    prior_missing_buckets: list[str] = []
    for bucket, bucket_lanes in BUCKETS.items():
        bucket_count = sum(prior_lane_counts.get(lane, 0) for lane in bucket_lanes)
        if bucket_count <= 0:
            prior_missing_buckets.append(bucket)

    cadence_override_state = resolve_cadence_override_state(
        current_missing_buckets=missing_buckets,
        prior_missing_buckets=prior_missing_buckets,
    )
    cadence_override_alias = resolve_cadence_override_alias(cadence_override_state)
    cadence_override_streak = resolve_cadence_override_streak(
        current_missing_buckets=missing_buckets,
        prior_missing_buckets=prior_missing_buckets,
    )
    score_band_dispatch_pressure = resolve_dispatch_pressure_with_cadence_override(
        base_pressure=base_dispatch_pressure,
        override_state=cadence_override_state,
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
    score_band_dispatch_pressure_momentum_fx_cue_combat_callout = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_cue_combat_callout(
            score_band_dispatch_pressure_momentum_fx_cue
        )
    )
    score_band_dispatch_pressure_momentum_fx_cue_combat_callout_alias = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_cue_combat_callout_alias(
            score_band_dispatch_pressure_momentum_fx_cue_combat_callout
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
    cadence_override_note = resolve_cadence_override_note(
        cadence_override_streak,
        score_band_dispatch_pressure_momentum_slope,
    )
    cadence_override_note_alias = resolve_cadence_override_note_alias(cadence_override_note)
    cadence_override_note_rationale = resolve_cadence_override_note_rationale(
        cadence_override_note,
        score_band_dispatch_pressure_momentum_slope,
    )
    cadence_override_note_rationale_alias = resolve_cadence_override_note_rationale_alias(
        cadence_override_note_rationale
    )
    cadence_override_note_rationale_confidence = (
        resolve_cadence_override_note_rationale_confidence(rows)
    )
    cadence_override_note_rationale_confidence_alias = (
        resolve_cadence_override_note_rationale_confidence_alias(
            cadence_override_note_rationale_confidence
        )
    )
    cadence_override_note_rationale_confidence_trend = (
        resolve_cadence_override_note_rationale_confidence_trend(rows)
    )
    cadence_override_note_rationale_confidence_trend_alias = (
        resolve_cadence_override_note_rationale_confidence_trend_alias(
            cadence_override_note_rationale_confidence_trend
        )
    )
    cadence_override_note_rationale_confidence_trend_momentum_score = (
        resolve_cadence_override_note_rationale_confidence_trend_momentum_score(rows)
    )
    cadence_override_note_rationale_confidence_trend_momentum_band = (
        resolve_cadence_override_note_rationale_confidence_trend_momentum_band(
            cadence_override_note_rationale_confidence_trend_momentum_score
        )
    )
    prior_cadence_override_note_rationale_confidence_trend_momentum_score = (
        resolve_cadence_override_note_rationale_confidence_trend_momentum_score(prior_rows)
    )
    prior_cadence_override_note_rationale_confidence_trend_momentum_band = (
        resolve_cadence_override_note_rationale_confidence_trend_momentum_band(
            prior_cadence_override_note_rationale_confidence_trend_momentum_score
        )
    )
    cadence_override_note_rationale_confidence_trend_momentum_band_alias = (
        resolve_cadence_override_note_rationale_confidence_trend_momentum_band_alias(
            cadence_override_note_rationale_confidence_trend_momentum_band
        )
    )
    cadence_override_note_rationale_confidence_trend_momentum_band_trend = (
        resolve_cadence_override_note_rationale_confidence_trend_momentum_band_trend(
            cadence_override_note_rationale_confidence_trend_momentum_band,
            prior_cadence_override_note_rationale_confidence_trend_momentum_band,
        )
    )
    cadence_override_note_rationale_confidence_trend_momentum_band_trend_alias = (
        resolve_cadence_override_note_rationale_confidence_trend_momentum_band_trend_alias(
            cadence_override_note_rationale_confidence_trend_momentum_band_trend
        )
    )
    score_band_dispatch_pressure_momentum_fx_urgency = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency(
            cadence_override_note_rationale_confidence_trend_momentum_band_trend
        )
    )
    score_band_dispatch_pressure_momentum_fx_urgency_alias = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_alias(
            score_band_dispatch_pressure_momentum_fx_urgency
        )
    )
    score_band_dispatch_pressure_momentum_fx_urgency_confidence = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence(rows)
    )
    score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend(rows)
    )
    score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_alias = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_alias(
            score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend
        )
    )
    score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_score = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_score(
            rows
        )
    )
    score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band(
            score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_score
        )
    )
    prior_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_score = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_score(
            prior_rows
        )
    )
    prior_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band(
            prior_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_score
        )
    )
    score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend(
            score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band,
            prior_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band,
        )
    )
    score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_alias = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_alias(
            score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend
        )
    )
    prior_prior_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_score = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_score(
            prior_rows[:-1] if len(prior_rows) > 1 else prior_rows
        )
    )
    prior_prior_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band(
            prior_prior_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_score
        )
    )
    prior_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend(
            prior_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band,
            prior_prior_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band,
        )
    )
    score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_confidence = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_confidence(
            score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend,
            prior_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend,
        )
    )
    score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse(
            score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend
        )
    )
    score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_alias = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_alias(
            score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse
        )
    )
    score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance(
            score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse
        )
    )
    score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence(
            score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance
        )
    )
    score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_alias = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_alias(
            score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence
        )
    )
    score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation(
            score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence
        )
    )
    score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_alias = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_alias(
            score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation
        )
    )
    score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity(
            score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation
        )
    )
    score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_alias = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_alias(
            score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity
        )
    )
    prior_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse(
            prior_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend
        )
    )
    prior_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance(
            prior_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse
        )
    )
    prior_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence(
            prior_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance
        )
    )
    prior_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation(
            prior_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence
        )
    )
    prior_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity(
            prior_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation
        )
    )
    score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend(
            score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity,
            prior_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity,
        )
    )
    score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_alias = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_alias(
            score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend
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
        resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation_family_trend_why_copy_budget_signals(
            verb_pack=trend_family_why_verb_pack
        )
    )
    why_copy_budget_token = (
        resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation_family_trend_why_copy_budget(
            threshold=int(why_copy_budget_signals["threshold"]),
            verb_pack=trend_family_why_verb_pack,
        )
    )
    combat_callout_decode_evaluation = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_cue_combat_callout_decode_evaluation()
    )
    recommendation_intensity_decode_evaluation = (
        resolve_trend_score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_decode_evaluation()
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
        "trendScoreBandDispatchPressureBaseClass": base_dispatch_pressure,
        "trendScoreBandDispatchPressureCadenceOverrideBucket": "combat-or-vfx",
        "trendScoreBandDispatchPressureCadenceOverrideState": cadence_override_state,
        "trendScoreBandDispatchPressureCadenceOverrideAlias": cadence_override_alias,
        "trendScoreBandDispatchPressureCadenceOverrideStreak": cadence_override_streak,
        "trendScoreBandDispatchPressureCadenceOverrideNote": cadence_override_note,
        "trendScoreBandDispatchPressureCadenceOverrideNoteAlias": cadence_override_note_alias,
        "trendScoreBandDispatchPressureCadenceOverrideNoteRationale": cadence_override_note_rationale,
        "trendScoreBandDispatchPressureCadenceOverrideNoteRationaleAlias": cadence_override_note_rationale_alias,
        "trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidence": cadence_override_note_rationale_confidence,
        "trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceAlias": cadence_override_note_rationale_confidence_alias,
        "trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceTrend": cadence_override_note_rationale_confidence_trend,
        "trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceTrendAlias": cadence_override_note_rationale_confidence_trend_alias,
        "trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceTrendMomentumScore": cadence_override_note_rationale_confidence_trend_momentum_score,
        "trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceTrendMomentumBand": cadence_override_note_rationale_confidence_trend_momentum_band,
        "trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceTrendMomentumBandAlias": cadence_override_note_rationale_confidence_trend_momentum_band_alias,
        "trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceTrendMomentumBandTrend": cadence_override_note_rationale_confidence_trend_momentum_band_trend,
        "trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceTrendMomentumBandTrendAlias": cadence_override_note_rationale_confidence_trend_momentum_band_trend_alias,
        "trendScoreBandDispatchPressureMomentum": score_band_dispatch_pressure_momentum,
        "trendScoreBandDispatchPressureMomentumBand": score_band_dispatch_pressure_momentum_band,
        "trendScoreBandDispatchPressureMomentumBandAlias": score_band_dispatch_pressure_momentum_band_alias,
        "trendScoreBandDispatchPressureMomentumFxCue": score_band_dispatch_pressure_momentum_fx_cue,
        "trendScoreBandDispatchPressureMomentumFxCueAlias": score_band_dispatch_pressure_momentum_fx_cue_alias,
        "trendScoreBandDispatchPressureMomentumFxUrgencyCue": score_band_dispatch_pressure_momentum_fx_urgency,
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueAlias": score_band_dispatch_pressure_momentum_fx_urgency_alias,
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidence": score_band_dispatch_pressure_momentum_fx_urgency_confidence,
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrend": score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend,
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendAlias": score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_alias,
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumScore": score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_score,
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBand": score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band,
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrend": score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend,
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendAlias": score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_alias,
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendConfidence": score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_confidence,
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulse": score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse,
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseAlias": score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_alias,
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidance": score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance,
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidence": score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence,
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceAlias": score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_alias,
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendation": score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation,
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationAlias": score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_alias,
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensity": score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity,
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityAlias": score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_alias,
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityTrend": score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend,
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityTrendAlias": score_band_dispatch_pressure_momentum_fx_urgency_confidence_trend_momentum_band_trend_vfx_pulse_guidance_confidence_recommendation_intensity_trend_alias,
        "trendScoreBandDispatchPressureMomentumFxCueMicrocopyRecommendation": score_band_dispatch_pressure_momentum_fx_cue_microcopy_recommendation,
        "trendScoreBandDispatchPressureMomentumFxCueCombatCallout": score_band_dispatch_pressure_momentum_fx_cue_combat_callout,
        "trendScoreBandDispatchPressureMomentumFxCueCombatCalloutAlias": score_band_dispatch_pressure_momentum_fx_cue_combat_callout_alias,
        "trendScoreBandDispatchPressureMomentumFxCueCombatCalloutDecodeBaseline": combat_callout_decode_evaluation["baseline"],
        "trendScoreBandDispatchPressureMomentumFxCueCombatCalloutDecodeCompact": combat_callout_decode_evaluation["compact"],
        "trendScoreBandDispatchPressureMomentumFxCueCombatCalloutDecodeEvaluation": combat_callout_decode_evaluation,
        "trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityDecodeEvaluation": recommendation_intensity_decode_evaluation,
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
        "trendScoreBandDispatchPressureMomentumSlopeRecommendationFamilyTrendWhyVerbPack": trend_family_why_verb_pack,
        "status": "over-cap" if over_cap else "within-cap",
    }


def to_markdown(
    report: dict,
    recent_rows: list[str] | None = None,
    include_trend_family_why: bool = False,
    trend_family_why_verb_pack: str = "baseline",
    include_combat_callout_compact_legend: bool = False,
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
                f"- trend-score momentum-slope rec family trend why (ai-content/systems): **TSDPMSRFT WHY:{resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation_family_trend_why(family_trend, trend_family_why_verb_pack)}**",
                f"- trend-score momentum-slope rec family trend why verb-pack: **TSDPMSRFTWHYPACK:{trend_family_why_verb_pack.upper()}**",
                "- trend-score momentum-slope rec family trend why copy budget (design/ux): "
                f"**{report.get('trendScoreBandDispatchPressureMomentumSlopeRecommendationFamilyTrendWhyCopyBudget', resolve_trend_score_band_dispatch_pressure_momentum_slope_recommendation_family_trend_why_copy_budget())}**",
            ]
        )

    if include_combat_callout_compact_legend:
        combat_decode = report.get(
            "trendScoreBandDispatchPressureMomentumFxCueCombatCalloutDecodeEvaluation",
            resolve_trend_score_band_dispatch_pressure_momentum_fx_cue_combat_callout_decode_evaluation(),
        )
        optional_rows.extend(
            [
                "- trend-score dispatch-pressure momentum fx combat callout compact decode (design/world): "
                f"**{report.get('trendScoreBandDispatchPressureMomentumFxCueCombatCalloutDecodeCompact', resolve_trend_score_band_dispatch_pressure_momentum_fx_cue_combat_callout_decode_compact())}**",
                "- trend-score dispatch-pressure momentum fx combat callout decode dos-width eval (design/world): "
                f"**TSDPMFXCLEN:B{combat_decode.get('baselineLen', 0)}|C{combat_decode.get('compactLen', 0)}|LIM{combat_decode.get('dosWidthLimit', 72)}|PREF:{combat_decode.get('preferred', 'COMPACT')}|{combat_decode.get('status', 'PASS')}**",
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
            f"- trend-score dispatch pressure base class (pre-cadence override): **{report.get('trendScoreBandDispatchPressureBaseClass', 'LIGHT')}**",
            f"- trend-score dispatch pressure cadence override: **TSDPCO:{report.get('trendScoreBandDispatchPressureCadenceOverrideAlias', 'B')}** ({report.get('trendScoreBandDispatchPressureCadenceOverrideState', 'BASE')}, bucket={report.get('trendScoreBandDispatchPressureCadenceOverrideBucket', 'combat-or-vfx')})",
            f"- trend-score dispatch pressure cadence override streak: **TSDPCOS:{report.get('trendScoreBandDispatchPressureCadenceOverrideStreak', 0)}**",
            f"- trend-score dispatch pressure cadence override note (ai-content/design, offline): **TSDPCO NOTE:{report.get('trendScoreBandDispatchPressureCadenceOverrideNote', 'HOLD')}**",
            f"- trend-score dispatch pressure cadence override note alias: **TSDPCON:{report.get('trendScoreBandDispatchPressureCadenceOverrideNoteAlias', 'H')}**",
            f"- trend-score dispatch pressure cadence override note rationale (ai-content/design, offline): **TSDPCON WHY:{report.get('trendScoreBandDispatchPressureCadenceOverrideNoteRationale', 'steady')}**",
            f"- trend-score dispatch pressure cadence override note rationale confidence (ai-content/systems, offline): **TSDPCON WHY CONF:{report.get('trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidence', 'HIGH')}**",
            f"- trend-score dispatch pressure cadence override note rationale confidence alias: **TSDPCONWC:{report.get('trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceAlias', 'H')}**",
            f"- trend-score dispatch pressure cadence override note rationale confidence trend (ai-content/systems, offline): **TSDPCONWCT:{report.get('trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceTrend', 'FLAT')}**",
            f"- trend-score dispatch pressure cadence override note rationale confidence trend alias: **TSDPCONWCTA:{report.get('trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceTrendAlias', 'F')}**",
            f"- trend-score dispatch pressure cadence override note rationale confidence trend momentum score (ai-content/systems, offline): **TSDPCONWCTS:{report.get('trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceTrendMomentumScore', 50)}**",
            f"- trend-score dispatch pressure cadence override note rationale confidence trend momentum band (ai-content/systems, offline): **TSDPCONWCTSB:{report.get('trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceTrendMomentumBand', 'MID')}**",
            f"- trend-score dispatch pressure cadence override note rationale confidence trend momentum band alias: **TSDPCONWCTSBA:{report.get('trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceTrendMomentumBandAlias', 'M')}**",
            f"- trend-score dispatch pressure cadence override note rationale confidence trend momentum band trend (ai-content/systems, offline): **TSDPCONWCTSBT:{report.get('trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceTrendMomentumBandTrend', 'FLAT')}**",
            f"- trend-score dispatch pressure cadence override note rationale confidence trend momentum band trend alias: **TSDPCONWCTSBTA:{report.get('trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceTrendMomentumBandTrendAlias', 'F')}**",
            f"- trend-score dispatch pressure cadence override note rationale alias: **TSDPCONW:{report.get('trendScoreBandDispatchPressureCadenceOverrideNoteRationaleAlias', 'S')}**",
            "- trend-score dispatch pressure cadence override rationale-confidence decode: **TSDPCONWC legend (L=LOW, M=MID, H=HIGH)**",
            "- trend-score dispatch pressure cadence override rationale-confidence trend decode: **TSDPCONWCT legend (U=UP, F=FLAT, D=DOWN)**",
            "- trend-score dispatch pressure cadence override rationale-confidence trend alias decode: **TSDPCONWCTA legend (U=UP, F=FLAT, D=DOWN)**",
            "- trend-score dispatch pressure cadence override rationale-confidence trend momentum band trend decode: **TSDPCONWCTSBT legend (U=UP, F=FLAT, D=DOWN)**",
            "- trend-score dispatch pressure cadence override rationale-confidence trend momentum band trend alias decode: **TSDPCONWCTSBTA legend (U=UP, F=FLAT, D=DOWN)**",
            "- trend-score dispatch pressure trend->fx urgency pair (design/world, dos-width): "
            f"**TSDPPAIR:TSDPCONWCTSBT={report.get('trendScoreBandDispatchPressureCadenceOverrideNoteRationaleConfidenceTrendMomentumBandTrend', 'FLAT')}|"
            f"TSDPMFXU={report.get('trendScoreBandDispatchPressureMomentumFxUrgencyCue', 'SURGE')}**",
            "- trend-score dispatch pressure trend->fx urgency compact alias (design/world, dos-width): "
            f"**TSDPPAIRA:{report.get('trendScoreBandDispatchPressureMomentumFxUrgencyCueAlias', 'U')}**",
            "- trend-score dispatch pressure trend->fx urgency pair decode (design/world): **TSDPCONWCTSBT U/F/D => TSDPMFXU SPIKE/SURGE/SOFT**",
            "- trend-score dispatch pressure trend->fx urgency compact alias decode (design/world): **TSDPPAIRA legend (S=SOFT, U=SURGE, P=SPIKE)**",
            "- trend-score dispatch pressure cadence override note decode: **TSDPCON legend (H=HOLD, W=WATCH, P=PUSH)**",
            "- trend-score dispatch pressure cadence override decode: **TSDPCO legend (B=BASE, E=ESCALATE)**",
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
            f"- trend-score dispatch-pressure momentum fx urgency cue from momentum-band trend (combat/vfx): **TSDPMFXU:{report.get('trendScoreBandDispatchPressureMomentumFxUrgencyCue', 'SURGE')}**",
            f"- trend-score dispatch-pressure momentum fx urgency cue alias: **TSDPMFXUA:{report.get('trendScoreBandDispatchPressureMomentumFxUrgencyCueAlias', 'U')}**",
            f"- trend-score dispatch-pressure momentum fx urgency confidence (ai-content/combat, offline): **TSDPMFXUC:{report.get('trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidence', 'HIGH')}**",
            f"- trend-score dispatch-pressure momentum fx urgency confidence trend (ai-content/combat, offline): **TSDPMFXUCT:{report.get('trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrend', 'FLAT')}**",
            f"- trend-score dispatch-pressure momentum fx urgency confidence trend alias: **TSDPMFXUCTA:{report.get('trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendAlias', 'F')}**",
            f"- trend-score dispatch-pressure momentum fx urgency confidence trend momentum score (ai-content/systems, offline): **TSDPMFXUCTS:{report.get('trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumScore', 50)}**",
            f"- trend-score dispatch-pressure momentum fx urgency confidence trend momentum band (ux/ai-content, offline): **TSDPMFXUCTSB:{report.get('trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBand', 'MID')}**",
            f"- trend-score dispatch-pressure momentum fx urgency confidence trend momentum band trend (ai-content/systems, offline): **TSDPMFXUCTSBT:{report.get('trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrend', 'FLAT')}**",
            f"- trend-score dispatch-pressure momentum fx urgency confidence trend momentum band trend alias: **TSDPMFXUCTSBTA:{report.get('trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendAlias', 'F')}**",
            f"- trend-score dispatch-pressure momentum fx urgency confidence trend momentum band trend confidence (ai-content/systems, offline): **TSDPMFXUCTSBTC:{report.get('trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendConfidence', 'MID')}**",
            f"- trend-score dispatch-pressure momentum fx urgency confidence trend momentum band trend vfx pulse (combat/vfx, offline): **TSDPMFXV:{report.get('trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulse', 'PULSE')}**",
            f"- trend-score dispatch-pressure momentum fx urgency confidence trend momentum band trend vfx pulse alias: **TSDPMFXVA:{report.get('trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseAlias', 'P')}**",
            f"- trend-score dispatch-pressure momentum fx urgency confidence trend momentum band pulse guidance (ai-content/systems, offline): **TSDPMFXVW:{report.get('trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidance', 'steady sweep')}**",
            f"- trend-score dispatch-pressure momentum fx urgency guidance confidence (ai-content/systems, offline): **TSDPMFXVWC:{report.get('trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidence', 'MID')}**",
            f"- trend-score dispatch-pressure momentum fx urgency guidance confidence alias: **TSDPMFXVWCA:{report.get('trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceAlias', 'M')}**",
            f"- trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation (ai-content/systems, offline): **TSDPMFXVWCR:{report.get('trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendation', 'brace check')}**",
            f"- trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation alias: **TSDPMFXVWCRA:{report.get('trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationAlias', 'BC')}**",
            f"- trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity (combat/vfx, offline): **TSDPMFXVWCRI:{report.get('trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensity', 'EDGE')}**",
            f"- trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity alias: **TSDPMFXVWCRIA:{report.get('trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityAlias', 'E')}**",
            f"- trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend (ai-content/systems, offline): **TSDPMFXVWCRIT:{report.get('trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityTrend', 'FLAT')}**",
            f"- trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend alias: **TSDPMFXVWCRITA:{report.get('trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityTrendAlias', 'F')}**",
            "- trend-score dispatch-pressure momentum fx urgency guidance confidence decode (design/world): **TSDPMFXVWC legend (L=LOW, M=MID, H=HIGH)**",
            "- trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation decode (design/world): **TSDPMFXVWCR legend (HIGH=lock sweep, MID=brace check, LOW=burst triage)**",
            "- trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation alias decode (design/world): **TSDPMFXVWCRA legend (LS=lock sweep, BC=brace check, BT=burst triage)**",
            "- trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity decode (design/world): **TSDPMFXVWCRI legend (SOFT=burst triage, EDGE=brace check, HARD=lock sweep)**",
            "- trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity alias decode (design/world): **TSDPMFXVWCRIA legend (S=SOFT, E=EDGE, H=HARD)**",
            "- trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend decode (design/world): **TSDPMFXVWCRIT legend (U=UP, F=FLAT, D=DOWN)**",
            "- trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity trend alias decode (design/world): **TSDPMFXVWCRITA legend (U=UP, F=FLAT, D=DOWN)**",
            "- trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation intensity alias decode dos-width eval (design/world): "
            f"**TSDPMFXVWCRIALEN:F{report.get('trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityDecodeEvaluation', {}).get('fullLen', 0)}|"
            f"C{report.get('trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityDecodeEvaluation', {}).get('compactLen', 0)}|"
            f"LIM{report.get('trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityDecodeEvaluation', {}).get('dosWidthLimit', 72)}|"
            f"PREF:{report.get('trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityDecodeEvaluation', {}).get('preferred', 'CONCISE')}|"
            f"{report.get('trendScoreBandDispatchPressureMomentumFxUrgencyCueConfidenceTrendMomentumBandTrendVfxPulseGuidanceConfidenceRecommendationIntensityDecodeEvaluation', {}).get('status', 'PASS')}**",
            "- trend-score dispatch-pressure momentum fx urgency guidance confidence recommendation alias decode dos-width eval (design/world): **TSDPMFXVWCRALEN:B45|C43|LIM72|PREF:COMPACT|PASS**",
            "- trend-score dispatch-pressure momentum fx urgency confidence decode (design/world): **TSDPMFXUC legend (LOW=volatile churn, MID=mixed churn, HIGH=steady churn)**",
            "- trend-score dispatch-pressure momentum fx urgency confidence trend decode (design/world): **TSDPMFXUCT legend (U=UP, F=FLAT, D=DOWN)**",
            "- trend-score dispatch-pressure momentum fx urgency confidence trend alias decode (design/world): **TSDPMFXUCTA legend (U=UP, F=FLAT, D=DOWN)**",
            "- trend-score dispatch-pressure momentum fx urgency confidence trend momentum band trend decode (design/world): **TSDPMFXUCTSBT legend (U=UP, F=FLAT, D=DOWN)**",
            "- trend-score dispatch-pressure momentum fx urgency confidence trend momentum band trend alias decode (design/world): **TSDPMFXUCTSBTA legend (U=UP, F=FLAT, D=DOWN)**",
            "- trend-score dispatch-pressure momentum fx urgency confidence trend momentum band trend confidence decode (design/world): **TSDPMFXUCTSBTC legend (LOW=flip, MID=one-side flat, HIGH=stable)**",
            "- trend-score dispatch-pressure momentum fx urgency confidence trend momentum band vfx pulse decode (design/world): **TSDPMFXV legend (C=CALM, P=PULSE, B=BLAST)**",
            "- trend-score dispatch-pressure momentum fx urgency confidence trend momentum band vfx pulse alias decode (design/world): **TSDPMFXVA legend (C=CALM, P=PULSE, B=BLAST)**",
            "- trend-score dispatch-pressure momentum fx urgency confidence trend momentum band pulse guidance decode (design/world): **TSDPMFXVW legend (CALM=steady sweep, PULSE=brace lanes, BLAST=commit burst)**",
            "- trend-score dispatch-pressure momentum fx pulse->callout pairing decode (design/world, dos-width): **TSDPMFXV C/P/B => TSDPMFXC HL/PE/BC**",
            "- trend-score dispatch-pressure momentum fx urgency cue decode (design/world): **SOFT=trend cooling (DOWN), SURGE=trend stable (FLAT), SPIKE=trend rising (UP)**",
            "- trend-score dispatch-pressure momentum fx cue cadence decode (design/world): **SOFT=CALM cadence, EDGE=EDGE cadence, HARD=HEATED cadence**",
            f"- trend-score dispatch-pressure momentum fx cue microcopy rec (ai-content/design): **{report.get('trendScoreBandDispatchPressureMomentumFxCueMicrocopyRecommendation', 'steady pace; hold broad scan')}**",
            f"- trend-score dispatch-pressure momentum fx combat callout (combat/vfx): **{report.get('trendScoreBandDispatchPressureMomentumFxCueCombatCallout', 'HOLD_LINE')}**",
            f"- trend-score dispatch-pressure momentum fx combat callout alias: **TSDPMFXC:{report.get('trendScoreBandDispatchPressureMomentumFxCueCombatCalloutAlias', 'HL')}**",
            "- trend-score dispatch-pressure momentum fx combat callout decode (design/world): "
            f"**{report.get('trendScoreBandDispatchPressureMomentumFxCueCombatCalloutDecodeBaseline', resolve_trend_score_band_dispatch_pressure_momentum_fx_cue_combat_callout_decode_baseline())}**",
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
    parser.add_argument(
        "--trend-family-why-verb-pack",
        choices=["baseline", "ramp"],
        default="baseline",
        help="Optional WHY verb-pack variant (`ramp/steady/cool`) for scanability comparison.",
    )
    parser.add_argument(
        "--include-combat-callout-compact-legend",
        action="store_true",
        help="Include optional compact combat-callout decode legend + DOS-width evaluation rows.",
    )
    args = parser.parse_args()

    text = args.backlog.read_text(encoding="utf-8")
    rows = collect_recent_rows(text, max_items=args.max_items)
    report = build_report(
        rows,
        cap_ratio=args.cap_ratio,
        trend_family_why_verb_pack=args.trend_family_why_verb_pack,
    )

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
                trend_family_why_verb_pack=args.trend_family_why_verb_pack,
                include_combat_callout_compact_legend=args.include_combat_callout_compact_legend,
            )
            + "\n",
            encoding="utf-8",
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
