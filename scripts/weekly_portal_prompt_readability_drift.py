#!/usr/bin/env python3
"""Weekly digest for portal prompt readability drift across recent commits.

Tracks compact/detailed token activity from portal-prompt related code changes.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "logs" / "weekly_portal_prompt_readability_drift.json"
DEFAULT_MD = ROOT / "logs" / "weekly_portal_prompt_readability_drift.md"

PORTAL_PATH_HINTS = (
    "src/portal.lua",
    "src/portal_prompt_linter.lua",
    "src/portal_prompt_budget.lua",
    "scripts/regression_portal_",
    "scripts/check_portal_prompt_",
)

TOKEN_GROUPS = {
    "compact": ["NEXT:", "P:", "ALT:", "ADEL:", "AP:"],
    "detailed": ["NEXT ROUTE:", "PRESSURE:", "ALT ROUTE:", "ALT DELTA:", "ALT PLAN:"],
    "shared": ["ENTER:JUMP", "COACH:"],
}

TOKEN_CATALOG: list[str] = []
for _tokens in TOKEN_GROUPS.values():
    for _token in _tokens:
        if _token not in TOKEN_CATALOG:
            TOKEN_CATALOG.append(_token)

PRESSURE_TOKENS = ["PRESSURE:", "P:"]

TOKEN_FAMILIES = {
    "portal": ["ENTER:JUMP", "NEXT:", "NEXT ROUTE:", "COACH:"],
    "alt": ["ALT:", "ALT ROUTE:", "ALT DELTA:", "ADEL:", "ALT PLAN:", "AP:"],
    "pressure": ["PRESSURE:", "P:"],
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--since-days", type=int, default=7)
    p.add_argument("--max-commits", type=int, default=120)
    p.add_argument("--repo-root", type=Path, default=Path.cwd())
    p.add_argument("--out-json", type=Path, default=DEFAULT_JSON)
    p.add_argument("--out-md", type=Path, default=DEFAULT_MD)
    return p.parse_args()


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


def touched_portal_path(path: str) -> bool:
    return any(path.startswith(prefix) for prefix in PORTAL_PATH_HINTS)


def changed_files(root: Path, commit: str) -> list[str]:
    out = git(root, "show", "--name-only", "--pretty=format:", commit)
    return [line.strip() for line in out.splitlines() if line.strip()]


def count_tokens_in_line(line: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for group, tokens in TOKEN_GROUPS.items():
        counts[group] = sum(line.count(token) for token in tokens)
    return counts


def count_catalog_tokens_in_line(line: str) -> dict[str, int]:
    return {token: line.count(token) for token in TOKEN_CATALOG}


def pressure_band_from_net(net: int) -> str:
    magnitude = abs(net)
    if magnitude >= 8:
        return "HIGH"
    if magnitude >= 3:
        return "MID"
    return "LOW"


def drift_risk_from_signals(*, compact_net: int, detailed_net: int, pressure_net: int) -> tuple[str, dict[str, int]]:
    imbalance = abs(compact_net - detailed_net)
    pressure_churn = abs(pressure_net)
    score = imbalance + pressure_churn
    if score >= 12:
        level = "HIGH"
    elif score >= 5:
        level = "MID"
    else:
        level = "LOW"
    return level, {
        "score": score,
        "imbalance": imbalance,
        "pressureChurn": pressure_churn,
    }


def lane_focus_from_token_totals(token_totals: dict[str, dict[str, int]]) -> tuple[str, dict[str, int]]:
    family_scores = {
        family: sum(abs(token_totals["net"].get(token, 0)) for token in tokens)
        for family, tokens in TOKEN_FAMILIES.items()
    }
    max_score = max(family_scores.values(), default=0)
    if max_score == 0:
        return "MIXED", {"portal": 0, "alt": 0, "pressure": 0}

    leaders = [family for family, score in family_scores.items() if score == max_score]
    if len(leaders) != 1:
        return "MIXED", family_scores

    leader = leaders[0]
    lane = "MIXED"
    if leader == "portal":
        lane = "PORTAL"
    elif leader == "alt":
        lane = "ALT"
    elif leader == "pressure":
        lane = "PRESSURE"
    return lane, family_scores


def route_action_from_focus(*, lane_focus: str, drift_risk: str) -> tuple[str, str]:
    if drift_risk == "LOW":
        return "WATCH", "low drift risk"
    if lane_focus == "PORTAL":
        return "PORTAL_AUDIT", "portal-family tokens dominate top movers"
    if lane_focus == "ALT":
        return "ALT_TUNE", "alt-route tokens dominate top movers"
    if lane_focus == "PRESSURE":
        return "PRESSURE_REBASE", "pressure tokens dominate top movers"
    return "BALANCE_PASS", "mixed lane focus with non-low drift risk"


def lane_focus_from_token_net(token_net: dict[str, int]) -> str:
    family_scores = {
        family: sum(abs(token_net.get(token, 0)) for token in tokens)
        for family, tokens in TOKEN_FAMILIES.items()
    }
    max_score = max(family_scores.values(), default=0)
    if max_score == 0:
        return "MIXED"
    leaders = [family for family, score in family_scores.items() if score == max_score]
    if len(leaders) != 1:
        return "MIXED"
    return {
        "portal": "PORTAL",
        "alt": "ALT",
        "pressure": "PRESSURE",
    }[leaders[0]]


def focus_streak_and_shift(*, commit_focuses: list[str], aggregate_focus: str) -> tuple[int, str]:
    if not commit_focuses:
        return 0, f"{aggregate_focus}->{aggregate_focus}"

    streak = 0
    for focus in commit_focuses:
        if focus == aggregate_focus:
            streak += 1
        else:
            break

    previous_focus = aggregate_focus
    for focus in commit_focuses[streak:]:
        if focus != "MIXED":
            previous_focus = focus
            break

    return streak, f"{previous_focus}->{aggregate_focus}"


def focus_volatility_from_commits(commit_focuses: list[str]) -> tuple[str, dict[str, float]]:
    if len(commit_focuses) <= 1:
        return "STEADY", {"switches": 0, "edges": max(0, len(commit_focuses) - 1), "switchRatio": 0.0}

    switches = sum(1 for idx in range(1, len(commit_focuses)) if commit_focuses[idx] != commit_focuses[idx - 1])
    edges = len(commit_focuses) - 1
    ratio = switches / edges if edges else 0.0
    return ("SWING" if ratio >= 0.4 else "STEADY"), {
        "switches": switches,
        "edges": edges,
        "switchRatio": round(ratio, 3),
    }


def route_action_confidence_from_signals(
    *,
    lane_focus: str,
    lane_focus_scores: dict[str, int],
    drift_risk_signals: dict[str, int],
) -> tuple[str, dict[str, float | int]]:
    score_values = sorted(lane_focus_scores.values(), reverse=True)
    top_score = score_values[0] if score_values else 0
    second_score = score_values[1] if len(score_values) > 1 else 0
    total_score = sum(lane_focus_scores.values())
    dominance_ratio = (top_score / total_score) if total_score > 0 else 0.0
    focus_spread = top_score - second_score
    drift_spread = abs(drift_risk_signals["imbalance"] - drift_risk_signals["pressureChurn"])

    confidence = "LOW"
    if lane_focus != "MIXED" and total_score > 0:
        if dominance_ratio >= 0.7 and focus_spread >= 3 and drift_spread <= 3:
            confidence = "HIGH"
        elif dominance_ratio >= 0.5 and focus_spread >= 1 and drift_spread <= 8:
            confidence = "MID"

    return confidence, {
        "topScore": top_score,
        "secondScore": second_score,
        "totalScore": total_score,
        "dominanceRatio": round(dominance_ratio, 3),
        "focusSpread": focus_spread,
        "driftSpread": drift_spread,
    }


def lane_lock_from_focus(*, lane_focus: str, focus_streak: int) -> tuple[str, dict[str, int | str | bool]]:
    threshold = 3
    armed = lane_focus != "MIXED" and focus_streak >= threshold
    token = "NONE"
    if armed:
        token = f"{lane_focus}x{focus_streak}"
    return token, {
        "threshold": threshold,
        "armed": armed,
        "lane": lane_focus,
        "streak": focus_streak,
    }


def focus_balance_from_scores(lane_focus_scores: dict[str, int]) -> tuple[str, dict[str, int | float]]:
    values = sorted((max(0, v) for v in lane_focus_scores.values()), reverse=True)
    top_score = values[0] if values else 0
    total_score = sum(values)
    dominance_ratio = (top_score / total_score) if total_score > 0 else 0.0
    pct = int(round(dominance_ratio * 100))
    return f"{pct}%", {
        "topScore": top_score,
        "totalScore": total_score,
        "dominanceRatio": round(dominance_ratio, 3),
        "percent": pct,
    }


def focus_entropy_from_scores(lane_focus_scores: dict[str, int]) -> tuple[str, dict[str, float | int]]:
    values = [max(0, lane_focus_scores.get(key, 0)) for key in ("portal", "alt", "pressure")]
    total = sum(values)
    if total <= 0:
        return "LOW", {
            "raw": 0.0,
            "normalized": 0.0,
            "maxEntropy": round(math.log2(3), 3),
            "totalScore": 0,
        }

    probs = [value / total for value in values if value > 0]
    raw_entropy = -sum(p * math.log2(p) for p in probs)
    max_entropy = math.log2(3)
    normalized = raw_entropy / max_entropy if max_entropy > 0 else 0.0

    tier = "LOW"
    if normalized >= 0.67:
        tier = "HIGH"
    elif normalized >= 0.34:
        tier = "MID"

    return tier, {
        "raw": round(raw_entropy, 3),
        "normalized": round(normalized, 3),
        "maxEntropy": round(max_entropy, 3),
        "totalScore": total,
    }


def drift_momentum_from_commits(touched_rows: list[dict]) -> tuple[str, dict[str, float | int]]:
    if not touched_rows:
        return "FLAT", {
            "recentAvg": 0.0,
            "olderAvg": 0.0,
            "delta": 0.0,
            "recentCount": 0,
            "olderCount": 0,
        }

    chronological = list(reversed(touched_rows))
    scores = [
        abs(row["net"]["compact"] - row["net"]["detailed"]) + abs(row["pressureEdits"]["net"])
        for row in chronological
    ]

    split = max(1, len(scores) // 2)
    older = scores[:split]
    recent = scores[split:] if len(scores) > split else scores[:]

    older_avg = sum(older) / len(older) if older else 0.0
    recent_avg = sum(recent) / len(recent) if recent else 0.0
    delta = recent_avg - older_avg

    momentum = "FLAT"
    if delta >= 2.0:
        momentum = "RISING"
    elif delta <= -2.0:
        momentum = "COOLING"

    return momentum, {
        "recentAvg": round(recent_avg, 3),
        "olderAvg": round(older_avg, 3),
        "delta": round(delta, 3),
        "recentCount": len(recent),
        "olderCount": len(older),
    }


def route_action_stability_from_signals(
    *,
    route_action_confidence: str,
    focus_volatility: str,
    drift_momentum: str,
) -> tuple[str, dict[str, str | bool]]:
    stable_conf = route_action_confidence in {"MID", "HIGH"}
    stable_vol = focus_volatility == "STEADY"
    stable_momentum = drift_momentum in {"FLAT", "COOLING"}
    locked = stable_conf and stable_vol and stable_momentum

    if locked:
        reason = "confidence-volatility-momentum-aligned"
    else:
        reason = "retune-watch-needed"

    return ("LOCKED" if locked else "WATCH"), {
        "routeActionConfidence": route_action_confidence,
        "focusVolatility": focus_volatility,
        "driftMomentum": drift_momentum,
        "stableConfidence": stable_conf,
        "steadyFocus": stable_vol,
        "stableMomentum": stable_momentum,
        "reason": reason,
    }


def pressure_latency_from_signals(*, pressure_churn: int, drift_momentum: str, drift_momentum_delta: float) -> tuple[str, dict[str, int | str | float]]:
    abs_delta = abs(drift_momentum_delta)

    if pressure_churn >= 7 and drift_momentum == "RISING" and abs_delta >= 2.0:
        lag = "FAST"
    elif pressure_churn <= 2 and drift_momentum == "FLAT" and abs_delta <= 1.0:
        lag = "STABLE"
    elif pressure_churn >= 4 and drift_momentum in {"FLAT", "COOLING"}:
        lag = "SLOW"
    elif pressure_churn >= 6:
        lag = "FAST"
    else:
        lag = "STABLE"

    return lag, {
        "pressureChurn": pressure_churn,
        "driftMomentum": drift_momentum,
        "driftDelta": round(drift_momentum_delta, 3),
        "absDriftDelta": round(abs_delta, 3),
    }


def route_action_guardrail_from_signals(*, drift_risk: str, route_action_confidence: str) -> tuple[str, dict[str, str | bool]]:
    lock = drift_risk == "HIGH" and route_action_confidence == "LOW"
    token = "LOCK" if lock else "SOFT"
    return token, {
        "armed": lock,
        "reason": "high-drift-low-confidence" if lock else "default-soft-guardrail",
        "driftRisk": drift_risk,
        "actionConfidence": route_action_confidence,
    }


def what_if_alt_from_signals(
    *,
    lane_focus: str,
    lane_focus_scores: dict[str, int],
    drift_risk_signals: dict[str, int],
) -> tuple[str, dict[str, str | int | bool]]:
    flag_name = "DOTPIO_EXPERIMENT_WHAT_IF_ALT"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    ranked = sorted(
        ((name, int(max(0, score))) for name, score in lane_focus_scores.items()),
        key=lambda row: (row[1], row[0]),
        reverse=True,
    )
    current_lane = lane_focus if lane_focus in {"PORTAL", "ALT", "PRESSURE"} else "MIXED"

    lane_map = {"portal": "PORTAL", "alt": "ALT", "pressure": "PRESSURE"}
    alt_lane = "NONE"
    for family, _score in ranked:
        candidate = lane_map.get(family, "MIXED")
        if candidate != current_lane:
            alt_lane = candidate
            break
    if alt_lane == "NONE" and ranked:
        alt_lane = lane_map.get(ranked[0][0], "MIXED")

    imbalance = int(drift_risk_signals.get("imbalance", 0))
    pressure_churn = int(drift_risk_signals.get("pressureChurn", 0))
    baseline_risk = int(drift_risk_signals.get("score", imbalance + pressure_churn))

    projected_imbalance = max(0, imbalance - 2) if alt_lane in {"ALT", "PORTAL"} else max(0, imbalance - 1)
    projected_pressure = max(0, pressure_churn - 2) if alt_lane == "PRESSURE" else max(0, pressure_churn - 1)
    projected_risk = projected_imbalance + projected_pressure
    delta_risk = projected_risk - baseline_risk

    token = f"ALT:{alt_lane} ΔRISK:{delta_risk:+d}" if flag_enabled else "OFF"
    reason = "flag-enabled-alt-lane-projection" if flag_enabled else "flag-disabled"

    return token, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "currentLane": current_lane,
        "altLane": alt_lane,
        "baselineRisk": baseline_risk,
        "imbalance": imbalance,
        "pressureChurn": pressure_churn,
        "projectedRisk": projected_risk,
        "deltaRisk": delta_risk,
        "reason": reason,
    }


def what_if_confidence_from_signals(
    *,
    what_if_alt_signals: dict[str, str | int | bool],
    route_action_confidence: str,
) -> tuple[str, dict[str, str | int | bool]]:
    flag_enabled = bool(what_if_alt_signals.get("flagEnabled", False))
    delta_risk = int(what_if_alt_signals.get("deltaRisk", 0))
    current_lane = str(what_if_alt_signals.get("currentLane", "MIXED"))
    alt_lane = str(what_if_alt_signals.get("altLane", "NONE"))

    if not flag_enabled:
        confidence = "LOW"
        reason = "flag-disabled"
    elif alt_lane in {"NONE", "MIXED"} or alt_lane == current_lane:
        confidence = "LOW"
        reason = "no-distinct-alt-lane"
    elif delta_risk <= -3 and route_action_confidence in {"MID", "HIGH"}:
        confidence = "HIGH"
        reason = "strong-risk-drop-with-route-confidence"
    elif delta_risk <= -1:
        confidence = "MID"
        reason = "moderate-risk-drop"
    else:
        confidence = "LOW"
        reason = "weak-or-negative-impact"

    return confidence, {
        "flagEnabled": flag_enabled,
        "deltaRisk": delta_risk,
        "currentLane": current_lane,
        "altLane": alt_lane,
        "routeActionConfidence": route_action_confidence,
        "reason": reason,
    }


def what_if_alignment_from_signals(
    *,
    what_if_alt_signals: dict[str, str | int | bool],
    route_action: str,
) -> tuple[str, dict[str, str | bool]]:
    flag_enabled = bool(what_if_alt_signals.get("flagEnabled", False))
    alt_lane = str(what_if_alt_signals.get("altLane", "NONE"))

    route_action_lane = {
        "PORTAL_AUDIT": "PORTAL",
        "ALT_TUNE": "ALT",
        "PRESSURE_REBASE": "PRESSURE",
        "BALANCE_PASS": "MIXED",
        "WATCH": "MIXED",
    }.get(route_action, "MIXED")

    if not flag_enabled:
        alignment = "DIVERGED"
        reason = "flag-disabled"
    elif alt_lane in {"NONE", "MIXED"}:
        alignment = "DIVERGED"
        reason = "alt-lane-not-actionable"
    elif route_action_lane == "MIXED":
        alignment = "ALIGNED"
        reason = "route-action-mixed-accepts-alt-lane"
    elif alt_lane == route_action_lane:
        alignment = "ALIGNED"
        reason = "alt-lane-matches-route-action"
    else:
        alignment = "DIVERGED"
        reason = "alt-lane-mismatch-route-action"

    return alignment, {
        "flagEnabled": flag_enabled,
        "routeAction": route_action,
        "routeActionLane": route_action_lane,
        "altLane": alt_lane,
        "reason": reason,
    }


def what_if_impact_band_from_signals(
    *,
    what_if_alt_signals: dict[str, str | int | bool],
) -> tuple[str, dict[str, str | int | bool]]:
    flag_enabled = bool(what_if_alt_signals.get("flagEnabled", False))
    delta_risk = int(what_if_alt_signals.get("deltaRisk", 0))
    current_lane = str(what_if_alt_signals.get("currentLane", "MIXED"))
    alt_lane = str(what_if_alt_signals.get("altLane", "NONE"))

    if not flag_enabled:
        band = "NEUTRAL"
        reason = "flag-disabled"
    elif alt_lane in {"NONE", "MIXED"} or alt_lane == current_lane:
        band = "NEUTRAL"
        reason = "alt-lane-not-actionable"
    elif delta_risk <= -2:
        band = "GAIN"
        reason = "projected-risk-drop"
    elif delta_risk <= 0:
        band = "NEUTRAL"
        reason = "flat-or-marginal-change"
    else:
        band = "LOSS"
        reason = "projected-risk-increase"

    return band, {
        "flagEnabled": flag_enabled,
        "deltaRisk": delta_risk,
        "currentLane": current_lane,
        "altLane": alt_lane,
        "reason": reason,
    }


def what_if_magnitude_from_signals(
    *,
    what_if_alt_signals: dict[str, str | int | bool],
) -> tuple[str, dict[str, str | int | bool]]:
    flag_enabled = bool(what_if_alt_signals.get("flagEnabled", False))
    delta_risk = int(what_if_alt_signals.get("deltaRisk", 0))
    abs_delta = abs(delta_risk)

    if not flag_enabled:
        magnitude = "SMALL"
        reason = "flag-disabled"
    elif abs_delta >= 4:
        magnitude = "LARGE"
        reason = "large-risk-shift"
    elif abs_delta >= 2:
        magnitude = "MED"
        reason = "moderate-risk-shift"
    else:
        magnitude = "SMALL"
        reason = "small-risk-shift"

    return magnitude, {
        "flagEnabled": flag_enabled,
        "deltaRisk": delta_risk,
        "absDeltaRisk": abs_delta,
        "reason": reason,
    }


def what_if_pressure_fit_from_signals(
    *,
    what_if_alt_signals: dict[str, str | int | bool],
    pressure_band: str,
) -> tuple[str, dict[str, str | int | bool]]:
    flag_enabled = bool(what_if_alt_signals.get("flagEnabled", False))
    projected_risk = int(what_if_alt_signals.get("projectedRisk", 0))

    if projected_risk >= 12:
        projected_band = "HIGH"
    elif projected_risk >= 5:
        projected_band = "MID"
    else:
        projected_band = "LOW"

    band_rank = {"LOW": 0, "MID": 1, "HIGH": 2}
    projected_rank = band_rank.get(projected_band, 1)
    pressure_rank = band_rank.get(pressure_band, 1)

    if not flag_enabled:
        fit = "EVEN"
        reason = "flag-disabled"
    elif projected_rank < pressure_rank:
        fit = "SAFE"
        reason = "projected-risk-below-current-pressure-band"
    elif projected_rank > pressure_rank:
        fit = "TENSE"
        reason = "projected-risk-above-current-pressure-band"
    else:
        fit = "EVEN"
        reason = "projected-risk-matches-current-pressure-band"

    return fit, {
        "flagEnabled": flag_enabled,
        "pressureBand": pressure_band,
        "projectedRisk": projected_risk,
        "projectedBand": projected_band,
        "reason": reason,
    }


def what_if_lane_fallback_from_signals(
    *,
    what_if_alt_signals: dict[str, str | int | bool],
    what_if_align: str,
    route_action: str,
) -> tuple[str, dict[str, str | bool]]:
    flag_name = "DOTPIO_EXPERIMENT_WHAT_IF_FALLBACK"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    alt_lane = str(what_if_alt_signals.get("altLane", "NONE"))
    route_action_lane = {
        "PORTAL_AUDIT": "PORTAL",
        "ALT_TUNE": "ALT",
        "PRESSURE_REBASE": "PRESSURE",
        "BALANCE_PASS": "MIXED",
        "WATCH": "MIXED",
    }.get(route_action, "MIXED")

    if not flag_enabled:
        fallback = "OFF"
        reason = "flag-disabled"
    elif what_if_align != "DIVERGED":
        fallback = "NONE"
        reason = "alt-lane-aligned"
    elif route_action_lane in {"PORTAL", "ALT", "PRESSURE"}:
        fallback = route_action_lane
        reason = "route-action-lane-fallback"
    else:
        fallback = "NONE"
        reason = "no-actionable-route-lane"

    return fallback, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "whatIfAlign": what_if_align,
        "altLane": alt_lane,
        "routeAction": route_action,
        "routeActionLane": route_action_lane,
        "reason": reason,
    }


def what_if_fallback_confidence_from_signals(
    *,
    what_if_fallback: str,
    what_if_fallback_signals: dict[str, str | bool],
    what_if_alt_signals: dict[str, str | int | bool],
    route_action_confidence: str,
) -> tuple[str, dict[str, str | int | bool]]:
    flag_enabled = bool(what_if_fallback_signals.get("flagEnabled", False))
    align = str(what_if_fallback_signals.get("whatIfAlign", "DIVERGED"))
    delta_risk = int(what_if_alt_signals.get("deltaRisk", 0))

    if not flag_enabled:
        confidence = "LOW"
        reason = "flag-disabled"
    elif what_if_fallback in {"OFF", "NONE"}:
        confidence = "LOW"
        reason = "no-actionable-fallback"
    elif align != "DIVERGED":
        confidence = "LOW"
        reason = "fallback-not-needed"
    elif delta_risk <= -3 and route_action_confidence in {"MID", "HIGH"}:
        confidence = "HIGH"
        reason = "strong-risk-drop-with-route-confidence"
    elif delta_risk <= -1 or route_action_confidence in {"MID", "HIGH"}:
        confidence = "MID"
        reason = "moderate-signal-strength"
    else:
        confidence = "LOW"
        reason = "weak-signal-strength"

    return confidence, {
        "flagEnabled": flag_enabled,
        "fallback": what_if_fallback,
        "whatIfAlign": align,
        "deltaRisk": delta_risk,
        "routeActionConfidence": route_action_confidence,
        "reason": reason,
    }


def what_if_fallback_pressure_fit_from_signals(
    *,
    what_if_fallback: str,
    what_if_fallback_signals: dict[str, str | bool],
    what_if_alt_signals: dict[str, str | int | bool],
    pressure_band: str,
) -> tuple[str, dict[str, str | int | bool]]:
    flag_enabled = bool(what_if_fallback_signals.get("flagEnabled", False))
    baseline_risk = int(what_if_alt_signals.get("baselineRisk", 0))
    imbalance = int(what_if_alt_signals.get("imbalance", baseline_risk))
    pressure_churn = int(what_if_alt_signals.get("pressureChurn", 0))

    projected_risk = baseline_risk
    if what_if_fallback in {"PORTAL", "ALT", "PRESSURE"}:
        projected_imbalance = max(0, imbalance - 2) if what_if_fallback in {"ALT", "PORTAL"} else max(0, imbalance - 1)
        projected_pressure = max(0, pressure_churn - 2) if what_if_fallback == "PRESSURE" else max(0, pressure_churn - 1)
        projected_risk = projected_imbalance + projected_pressure
    projected_band = "LOW"
    if projected_risk >= 12:
        projected_band = "HIGH"
    elif projected_risk >= 5:
        projected_band = "MID"

    band_rank = {"LOW": 0, "MID": 1, "HIGH": 2}
    projected_rank = band_rank.get(projected_band, 1)
    pressure_rank = band_rank.get(pressure_band, 1)

    if not flag_enabled:
        fit = "EVEN"
        reason = "fallback-flag-disabled"
    elif what_if_fallback in {"OFF", "NONE"}:
        fit = "EVEN"
        reason = "no-actionable-fallback"
    elif projected_rank < pressure_rank:
        fit = "SAFE"
        reason = "fallback-projected-risk-below-current-pressure-band"
    elif projected_rank > pressure_rank:
        fit = "TENSE"
        reason = "fallback-projected-risk-above-current-pressure-band"
    else:
        fit = "EVEN"
        reason = "fallback-projected-risk-matches-current-pressure-band"

    return fit, {
        "flagEnabled": flag_enabled,
        "fallback": what_if_fallback,
        "pressureBand": pressure_band,
        "baselineRisk": baseline_risk,
        "projectedRisk": projected_risk,
        "projectedBand": projected_band,
        "reason": reason,
    }




def what_if_fallback_why_from_signals(
    *,
    what_if_fallback: str,
    what_if_fallback_signals: dict[str, str | bool],
    what_if_fallback_confidence: str,
    what_if_fallback_fit: str,
    what_if_alt_signals: dict[str, str | int | bool],
    pressure_band: str,
) -> tuple[str, dict[str, str | int | bool]]:
    flag_name = "DOTPIO_EXPERIMENT_WHAT_IF_FALLBACK_WHY"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    if not flag_enabled:
        why = "OFF"
        reason = "flag-disabled"
    elif what_if_fallback in {"OFF", "NONE"}:
        why = "NO-FALLBACK"
        reason = "no-actionable-fallback"
    else:
        delta_risk = int(what_if_alt_signals.get("deltaRisk", 0))
        align = str(what_if_fallback_signals.get("whatIfAlign", "DIVERGED"))
        if align != "DIVERGED":
            why = "ALIGN-OK"
            reason = "fallback-not-required"
        elif delta_risk <= -2:
            why = "RISK-DROP"
            reason = "fallback-projects-risk-drop"
        elif what_if_fallback_confidence == "LOW":
            why = "CONF-LOW"
            reason = "fallback-confidence-low"
        elif what_if_fallback_fit == "TENSE" or pressure_band == "HIGH":
            why = "PRESSURE"
            reason = "pressure-band-remains-high"
        else:
            why = "ROUTE-HANDOFF"
            reason = "fallback-routes-operator-handoff"

    return why, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "fallback": what_if_fallback,
        "fallbackConfidence": what_if_fallback_confidence,
        "fallbackFit": what_if_fallback_fit,
        "pressureBand": pressure_band,
        "reason": reason,
    }


def what_if_fallback_alignment_from_signals(
    *,
    what_if_fallback: str,
    lane_focus: str,
) -> tuple[str, dict[str, str | bool]]:
    actionable = what_if_fallback in {"PORTAL", "ALT", "PRESSURE"}

    if not actionable:
        align = "SYNC"
        reason = "no-actionable-fallback"
    elif lane_focus == "MIXED":
        align = "SYNC"
        reason = "lane-focus-mixed"
    elif what_if_fallback == lane_focus:
        align = "SYNC"
        reason = "fallback-matches-lane-focus"
    else:
        align = "ASYNC"
        reason = "fallback-diverges-from-lane-focus"

    return align, {
        "fallback": what_if_fallback,
        "laneFocus": lane_focus,
        "actionable": actionable,
        "reason": reason,
    }


def what_if_fallback_magnitude_from_signals(
    *,
    what_if_fallback: str,
    what_if_fallback_signals: dict[str, str | bool],
    what_if_alt_signals: dict[str, str | int | bool],
) -> tuple[str, dict[str, str | int | bool]]:
    flag_enabled = bool(what_if_fallback_signals.get("flagEnabled", False))
    delta_risk = int(what_if_alt_signals.get("deltaRisk", 0))
    abs_delta = abs(delta_risk)

    if not flag_enabled:
        magnitude = "SMALL"
        reason = "flag-disabled"
    elif what_if_fallback in {"OFF", "NONE"}:
        magnitude = "SMALL"
        reason = "no-actionable-fallback"
    elif abs_delta >= 4:
        magnitude = "LARGE"
        reason = "large-risk-shift"
    elif abs_delta >= 2:
        magnitude = "MED"
        reason = "moderate-risk-shift"
    else:
        magnitude = "SMALL"
        reason = "small-risk-shift"

    return magnitude, {
        "flagEnabled": flag_enabled,
        "fallback": what_if_fallback,
        "deltaRisk": delta_risk,
        "absDeltaRisk": abs_delta,
        "reason": reason,
    }


def what_if_fallback_alt2_from_signals(
    *,
    what_if_fallback: str,
    lane_focus_scores: dict[str, int],
) -> tuple[str, dict[str, str | int | bool]]:
    flag_name = "DOTPIO_EXPERIMENT_WHAT_IF_FALLBACK_ALT2"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    lane_candidates = ["PORTAL", "ALT", "PRESSURE"]
    fallback_lane = what_if_fallback if what_if_fallback in lane_candidates else "NONE"

    alt2_lane = "NONE"
    reason = "flag-disabled"
    top_score = 0
    second_score = 0
    min_top_score = 2
    min_gap = 1

    if flag_enabled:
        ranked = sorted(
            ((lane, int(lane_focus_scores.get(lane.lower(), 0))) for lane in lane_candidates),
            key=lambda row: (-row[1], row[0]),
        )
        viable_ranked = [(lane, score) for lane, score in ranked if lane != fallback_lane]

        if fallback_lane == "NONE":
            alt2_lane = "NONE"
            reason = "no-actionable-primary-fallback"
        elif not viable_ranked:
            alt2_lane = "NONE"
            reason = "no-secondary-lane-candidate"
        else:
            top_lane, top_score = viable_ranked[0]
            second_score = viable_ranked[1][1] if len(viable_ranked) > 1 else 0
            score_gap = top_score - second_score

            if top_score < min_top_score:
                alt2_lane = "NONE"
                reason = "secondary-score-too-low"
            elif score_gap < min_gap:
                alt2_lane = "NONE"
                reason = "secondary-ambiguity-gap"
            else:
                alt2_lane = top_lane
                reason = "lane-focus-ranked-secondary"

    return alt2_lane, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "fallback": what_if_fallback,
        "fallbackLane": fallback_lane,
        "portalScore": int(lane_focus_scores.get("portal", 0)),
        "altScore": int(lane_focus_scores.get("alt", 0)),
        "pressureScore": int(lane_focus_scores.get("pressure", 0)),
        "topScore": top_score,
        "secondScore": second_score,
        "minTopScore": min_top_score,
        "minGap": min_gap,
        "reason": reason,
    }


def what_if_fallback_alt2_confidence_from_signals(
    *,
    what_if_fallback_alt2: str,
    what_if_fallback_alt2_signals: dict[str, str | int | bool],
) -> tuple[str, dict[str, str | int | bool]]:
    flag_enabled = bool(what_if_fallback_alt2_signals.get("flagEnabled", False))
    fallback_lane = str(what_if_fallback_alt2_signals.get("fallbackLane", "NONE"))
    top_score = int(what_if_fallback_alt2_signals.get("topScore", 0))
    second_score = int(what_if_fallback_alt2_signals.get("secondScore", 0))
    score_gap = top_score - second_score

    if not flag_enabled:
        confidence = "LOW"
        reason = "flag-disabled"
    elif fallback_lane == "NONE":
        confidence = "LOW"
        reason = "no-primary-fallback"
    elif what_if_fallback_alt2 == "NONE":
        confidence = "LOW"
        reason = "no-actionable-secondary"
    elif top_score >= 4 and score_gap >= 2:
        confidence = "HIGH"
        reason = "strong-secondary-lane-signal"
    elif top_score >= 2 and score_gap >= 1:
        confidence = "MID"
        reason = "moderate-secondary-lane-signal"
    else:
        confidence = "LOW"
        reason = "weak-secondary-lane-signal"

    return confidence, {
        "flagEnabled": flag_enabled,
        "alt2": what_if_fallback_alt2,
        "fallbackLane": fallback_lane,
        "topScore": top_score,
        "secondScore": second_score,
        "scoreGap": score_gap,
        "reason": reason,
    }


def what_if_fallback_plan_from_signals(
    *,
    what_if_fallback: str,
    what_if_fallback_confidence: str,
    what_if_fallback_alt2: str,
    what_if_fallback_alt2_confidence: str,
) -> tuple[str, dict[str, str | bool]]:
    flag_name = "DOTPIO_EXPERIMENT_WHAT_IF_FALLBACK_PLAN"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    primary_actionable = what_if_fallback in {"PORTAL", "ALT", "PRESSURE"}
    secondary_actionable = what_if_fallback_alt2 in {"PORTAL", "ALT", "PRESSURE"}

    if not flag_enabled:
        plan = "HOLD"
        reason = "flag-disabled"
    elif primary_actionable and what_if_fallback_confidence in {"MID", "HIGH"}:
        plan = "PRIMARY"
        reason = "primary-fallback-actionable-with-confidence"
    elif secondary_actionable and what_if_fallback_alt2_confidence in {"MID", "HIGH"}:
        plan = "SECONDARY"
        reason = "secondary-fallback-actionable-with-confidence"
    elif primary_actionable:
        plan = "PRIMARY"
        reason = "primary-actionable-low-confidence"
    else:
        plan = "HOLD"
        reason = "no-actionable-fallback-plan"

    return plan, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "fallback": what_if_fallback,
        "fallbackConfidence": what_if_fallback_confidence,
        "fallbackAlt2": what_if_fallback_alt2,
        "fallbackAlt2Confidence": what_if_fallback_alt2_confidence,
        "primaryActionable": primary_actionable,
        "secondaryActionable": secondary_actionable,
        "reason": reason,
    }


def what_if_fallback_plan_fit_from_signals(
    *,
    what_if_fallback_plan: str,
    what_if_fallback_fit: str,
    what_if_fallback_alt2: str,
    what_if_alt_signals: dict[str, str | int | bool],
    pressure_band: str,
) -> tuple[str, dict[str, str | int]]:
    if what_if_fallback_plan == "PRIMARY":
        fit = what_if_fallback_fit
        reason = "inherits-primary-fallback-fit"
        lane = "PRIMARY"
        projected_band = str(what_if_fallback_fit)
    elif what_if_fallback_plan == "SECONDARY" and what_if_fallback_alt2 in {"PORTAL", "ALT", "PRESSURE"}:
        baseline_risk = int(what_if_alt_signals.get("baselineRisk", 0))
        imbalance = int(what_if_alt_signals.get("imbalance", baseline_risk))
        pressure_churn = int(what_if_alt_signals.get("pressureChurn", 0))

        projected_imbalance = max(0, imbalance - 2) if what_if_fallback_alt2 in {"ALT", "PORTAL"} else max(0, imbalance - 1)
        projected_pressure = max(0, pressure_churn - 2) if what_if_fallback_alt2 == "PRESSURE" else max(0, pressure_churn - 1)
        projected_risk = projected_imbalance + projected_pressure

        if projected_risk >= 12:
            projected_band = "HIGH"
        elif projected_risk >= 5:
            projected_band = "MID"
        else:
            projected_band = "LOW"

        band_rank = {"LOW": 0, "MID": 1, "HIGH": 2}
        projected_rank = band_rank.get(projected_band, 1)
        pressure_rank = band_rank.get(pressure_band, 1)
        if projected_rank < pressure_rank:
            fit = "SAFE"
        elif projected_rank > pressure_rank:
            fit = "TENSE"
        else:
            fit = "EVEN"
        reason = "secondary-projection-vs-pressure-band"
        lane = what_if_fallback_alt2
    else:
        fit = "EVEN"
        reason = "hold-or-no-actionable-secondary"
        lane = "HOLD"
        projected_band = pressure_band

    return fit, {
        "plan": what_if_fallback_plan,
        "planLane": lane,
        "pressureBand": pressure_band,
        "projectedBand": projected_band,
        "reason": reason,
    }


def what_if_fallback_plan_why_from_signals(
    *,
    what_if_fallback_plan: str,
    what_if_fallback_plan_signals: dict[str, str | bool],
    what_if_fallback_plan_fit: str,
) -> tuple[str, dict[str, str | bool]]:
    flag_name = "DOTPIO_EXPERIMENT_WHAT_IF_FALLBACK_PLAN_WHY"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    if not flag_enabled:
        why = "FLAG OFF"
        reason = "flag-disabled"
    elif what_if_fallback_plan == "PRIMARY":
        if what_if_fallback_plan_fit == "SAFE":
            why = "PRIMARY RELIEF"
            reason = "primary-plan-projects-safer-band"
        elif what_if_fallback_plan_fit == "TENSE":
            why = "PRIMARY PRESSURE"
            reason = "primary-plan-keeps-pressure-high"
        else:
            why = "PRIMARY STEADY"
            reason = "primary-plan-holds-current-band"
    elif what_if_fallback_plan == "SECONDARY":
        if what_if_fallback_plan_fit == "SAFE":
            why = "ALT2 RELIEF"
            reason = "secondary-plan-projects-safer-band"
        elif what_if_fallback_plan_fit == "TENSE":
            why = "ALT2 PRESSURE"
            reason = "secondary-plan-keeps-pressure-high"
        else:
            why = "ALT2 STEADY"
            reason = "secondary-plan-holds-current-band"
    else:
        why = "HOLD FOR SIGNAL"
        reason = "plan-hold-awaiting-stronger-signal"

    return why, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "plan": what_if_fallback_plan,
        "planFit": what_if_fallback_plan_fit,
        "planReason": str(what_if_fallback_plan_signals.get("reason", "unknown")),
        "reason": reason,
    }


def what_if_split_from_signals(
    *,
    what_if_fallback_plan_signals: dict[str, str | bool],
    what_if_alt_signals: dict[str, str | int | bool],
) -> tuple[str, dict[str, str | int | bool]]:
    flag_name = "DOTPIO_EXPERIMENT_WHAT_IF_SPLIT"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    primary_lane = str(what_if_fallback_plan_signals.get("fallback", "OFF"))
    secondary_lane = str(what_if_fallback_plan_signals.get("fallbackAlt2", "NONE"))
    primary_conf = str(what_if_fallback_plan_signals.get("fallbackConfidence", "LOW"))
    secondary_conf = str(what_if_fallback_plan_signals.get("fallbackAlt2Confidence", "LOW"))

    primary_actionable = primary_lane in {"PORTAL", "ALT", "PRESSURE"}
    secondary_actionable = secondary_lane in {"PORTAL", "ALT", "PRESSURE"}
    lanes_diverged = primary_lane != secondary_lane
    abs_delta_risk = abs(int(what_if_alt_signals.get("deltaRisk", 0)))
    strong_delta = abs_delta_risk >= 4
    strong_confidence = primary_conf in {"MID", "HIGH"} and secondary_conf in {"MID", "HIGH"}

    if not flag_enabled:
        split = "OFF"
        reason = "flag-disabled"
    elif not primary_actionable or not secondary_actionable:
        split = "OFF"
        reason = "missing-dual-actionable-routes"
    elif not lanes_diverged:
        split = "OFF"
        reason = "no-lane-divergence"
    elif strong_confidence and strong_delta:
        split = "ON"
        reason = "dual-route-divergence-strong"
    else:
        split = "OFF"
        reason = "divergence-below-threshold"

    return split, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "primaryLane": primary_lane,
        "secondaryLane": secondary_lane,
        "primaryConfidence": primary_conf,
        "secondaryConfidence": secondary_conf,
        "lanesDiverged": lanes_diverged,
        "absDeltaRisk": abs_delta_risk,
        "strongDelta": strong_delta,
        "strongConfidence": strong_confidence,
        "reason": reason,
    }


def what_if_split_lanes_from_signals(
    *,
    what_if_split_signals: dict[str, str | int | bool],
) -> tuple[str, dict[str, str | bool]]:
    primary_lane = str(what_if_split_signals.get("primaryLane", "OFF"))
    secondary_lane = str(what_if_split_signals.get("secondaryLane", "NONE"))

    primary_actionable = primary_lane in {"PORTAL", "ALT", "PRESSURE"}
    secondary_actionable = secondary_lane in {"PORTAL", "ALT", "PRESSURE"}

    if primary_actionable and secondary_actionable:
        lanes = f"{primary_lane}/{secondary_lane}"
        reason = "dual-lane-pair"
    elif primary_actionable:
        lanes = f"{primary_lane}/NONE"
        reason = "secondary-missing"
    else:
        lanes = "NONE/NONE"
        reason = "no-actionable-lanes"

    return lanes, {
        "primaryActionable": primary_actionable,
        "secondaryActionable": secondary_actionable,
        "reason": reason,
    }


def what_if_split_confidence_from_signals(
    *,
    what_if_split: str,
    what_if_split_signals: dict[str, str | int | bool],
) -> tuple[str, dict[str, str | int | bool]]:
    flag_enabled = bool(what_if_split_signals.get("flagEnabled", False))
    strong_confidence = bool(what_if_split_signals.get("strongConfidence", False))
    strong_delta = bool(what_if_split_signals.get("strongDelta", False))
    primary_conf = str(what_if_split_signals.get("primaryConfidence", "LOW"))
    secondary_conf = str(what_if_split_signals.get("secondaryConfidence", "LOW"))

    if not flag_enabled:
        confidence = "LOW"
        reason = "flag-disabled"
    elif what_if_split != "ON":
        confidence = "LOW"
        reason = "split-not-armed"
    elif primary_conf == "HIGH" and secondary_conf == "HIGH" and strong_delta:
        confidence = "HIGH"
        reason = "dual-high-confidence-with-strong-delta"
    elif strong_confidence:
        confidence = "MID"
        reason = "dual-confidence-above-threshold"
    else:
        confidence = "LOW"
        reason = "weak-dual-confidence"

    return confidence, {
        "split": what_if_split,
        "flagEnabled": flag_enabled,
        "primaryConfidence": primary_conf,
        "secondaryConfidence": secondary_conf,
        "strongConfidence": strong_confidence,
        "strongDelta": strong_delta,
        "reason": reason,
    }




def what_if_split_safe_from_signals(
    *,
    what_if_split: str,
    what_if_split_signals: dict[str, str | int | bool],
    what_if_fallback_fit: str,
    what_if_fallback_alt2_confidence: str,
) -> tuple[str, dict[str, str | bool]]:
    flag_name = "DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_SAFE"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    split_armed = what_if_split == "ON"
    primary_conf = str(what_if_split_signals.get("primaryConfidence", "LOW"))
    secondary_conf = str(what_if_split_signals.get("secondaryConfidence", "LOW"))
    primary_safe = what_if_fallback_fit in {"SAFE", "EVEN"}
    secondary_safe = what_if_fallback_alt2_confidence in {"MID", "HIGH"}

    if not flag_enabled:
        safe = "OFF"
        reason = "flag-disabled"
    elif not split_armed:
        safe = "OFF"
        reason = "split-not-armed"
    elif not primary_safe:
        safe = "OFF"
        reason = "primary-path-escalates-pressure"
    elif not secondary_safe:
        safe = "OFF"
        reason = "secondary-path-confidence-too-low"
    elif primary_conf in {"MID", "HIGH"} and secondary_conf in {"MID", "HIGH"}:
        safe = "ON"
        reason = "dual-path-non-escalating"
    else:
        safe = "OFF"
        reason = "dual-path-confidence-below-threshold"

    return safe, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "split": what_if_split,
        "primaryConfidence": primary_conf,
        "secondaryConfidence": secondary_conf,
        "primaryFit": what_if_fallback_fit,
        "secondaryConfidenceGate": what_if_fallback_alt2_confidence,
        "splitArmed": split_armed,
        "primarySafe": primary_safe,
        "secondarySafe": secondary_safe,
        "reason": reason,
    }


def what_if_split_posture_from_signals(
    *,
    what_if_split: str,
    what_if_split_safe: str,
    what_if_split_confidence: str,
) -> tuple[str, dict[str, str]]:
    if what_if_split != "ON":
        posture = "HOLD"
        reason = "split-not-armed"
    elif what_if_split_safe != "ON":
        posture = "HOLD"
        reason = "safety-gate-off"
    elif what_if_split_confidence == "HIGH":
        posture = "SAFE"
        reason = "safe-and-high-confidence"
    elif what_if_split_confidence == "MID":
        posture = "WATCH"
        reason = "safe-but-needs-monitoring"
    else:
        posture = "HOLD"
        reason = "safe-but-confidence-low"

    return posture, {
        "split": what_if_split,
        "splitSafe": what_if_split_safe,
        "splitConfidence": what_if_split_confidence,
        "reason": reason,
    }


def what_if_split_cooloff_from_prior(*, current_split: str, prior_json_path: Path) -> tuple[int, dict[str, str | int | bool]]:
    """Count consecutive OFF windows after split ON cycle.

    Returns (cooloff_count, signals_dict).
    - If current split is ON, cooloff resets to 0.
    - If prior digest had split ON and current is OFF, cooloff starts at 1.
    - If prior digest already had a split cooloff counter and current is still OFF, increment.
    """
    if current_split == "ON":
        return 0, {
            "active": False,
            "currentSplit": current_split,
            "priorSplit": "ON",
            "priorCooloff": 0,
            "reason": "split-active-no-cooloff",
            "priorLoaded": False,
        }

    prior_split = "OFF"
    prior_cooloff = 0
    prior_loaded = False
    if prior_json_path.exists():
        try:
            prior = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_split = str(prior.get("whatIfSplit", "OFF"))
            prior_cooloff = int(prior.get("whatIfSplitCooloff", 0) or 0)
            prior_loaded = True
        except (json.JSONDecodeError, OSError, ValueError, TypeError):
            prior_split = "OFF"
            prior_cooloff = 0
            prior_loaded = False

    if prior_split == "ON":
        cooloff = 1
        reason = "split-just-disarmed"
    elif prior_cooloff > 0:
        cooloff = prior_cooloff + 1
        reason = "cooloff-continuing"
    else:
        cooloff = 0
        reason = "no-prior-on-cycle"

    return cooloff, {
        "active": cooloff > 0,
        "currentSplit": current_split,
        "priorSplit": prior_split,
        "priorCooloff": prior_cooloff,
        "reason": reason,
        "priorLoaded": prior_loaded,
    }


def what_if_split_escalate_from_signals(
    *,
    what_if_split: str,
    what_if_split_signals: dict[str, str | int | bool],
    what_if_fallback_plan_fit: str,
) -> tuple[str, dict[str, str | int | bool]]:
    """Arm split escalation sentinel when divergent split stays tense."""
    flag_name = "DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESCALATE"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    split_armed = what_if_split == "ON"
    lanes_diverged = bool(what_if_split_signals.get("lanesDiverged", False))
    tense_fit = what_if_fallback_plan_fit == "TENSE"

    if not flag_enabled:
        escalate = "OFF"
        reason = "flag-disabled"
    elif not split_armed:
        escalate = "OFF"
        reason = "split-not-armed"
    elif not lanes_diverged:
        escalate = "OFF"
        reason = "split-lanes-not-divergent"
    elif not tense_fit:
        escalate = "OFF"
        reason = "fit-not-tense"
    else:
        escalate = "ON"
        reason = "divergent-split-under-tense-fit"

    return escalate, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "split": what_if_split,
        "splitArmed": split_armed,
        "lanesDiverged": lanes_diverged,
        "planFit": what_if_fallback_plan_fit,
        "tenseFit": tense_fit,
        "reason": reason,
    }


def what_if_split_escalate_confidence_from_signals(
    *,
    what_if_split_escalate: str,
    what_if_split_confidence: str,
    what_if_fallback_plan_fit: str,
) -> tuple[str, dict[str, str | bool]]:
    if what_if_split_escalate != "ON":
        conf = "LOW"
        reason = "escalation-not-armed"
    elif what_if_split_confidence == "HIGH" and what_if_fallback_plan_fit == "TENSE":
        conf = "HIGH"
        reason = "high-split-confidence-under-tense-fit"
    elif what_if_split_confidence in {"MID", "HIGH"}:
        conf = "MID"
        reason = "armed-with-moderate-confidence"
    else:
        conf = "LOW"
        reason = "armed-but-low-split-confidence"

    return conf, {
        "splitEscalate": what_if_split_escalate,
        "splitConfidence": what_if_split_confidence,
        "planFit": what_if_fallback_plan_fit,
        "reason": reason,
    }


def what_if_split_escalate_lanes_from_signals(
    *,
    what_if_split_escalate: str,
    what_if_split_signals: dict[str, str | int | bool],
) -> tuple[str, dict[str, str | bool]]:
    primary_lane = str(what_if_split_signals.get("primaryLane", "OFF"))
    secondary_lane = str(what_if_split_signals.get("secondaryLane", "NONE"))
    lanes_diverged = bool(what_if_split_signals.get("lanesDiverged", False))

    primary_actionable = primary_lane in {"PORTAL", "ALT", "PRESSURE"}
    secondary_actionable = secondary_lane in {"PORTAL", "ALT", "PRESSURE"}

    if what_if_split_escalate != "ON":
        lanes = "NONE/NONE"
        reason = "escalation-not-armed"
    elif not lanes_diverged:
        lanes = "NONE/NONE"
        reason = "split-lanes-not-divergent"
    elif primary_actionable and secondary_actionable:
        lanes = f"{primary_lane}/{secondary_lane}"
        reason = "escalation-dual-lane-pair"
    elif primary_actionable:
        lanes = f"{primary_lane}/NONE"
        reason = "escalation-secondary-missing"
    else:
        lanes = "NONE/NONE"
        reason = "escalation-no-actionable-lanes"

    return lanes, {
        "splitEscalate": what_if_split_escalate,
        "primaryActionable": primary_actionable,
        "secondaryActionable": secondary_actionable,
        "lanesDiverged": lanes_diverged,
        "reason": reason,
    }


def what_if_split_escalate_cooloff_from_prior(
    *,
    current_split_escalate: str,
    prior_json_path: Path,
) -> tuple[int, dict[str, str | int | bool]]:
    """Count OFF windows after split escalation disarms (flag-gated output token)."""
    flag_name = "DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_COOL"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    if not flag_enabled:
        return 0, {
            "flagName": flag_name,
            "flagEnabled": flag_enabled,
            "active": False,
            "currentSplitEscalate": current_split_escalate,
            "priorSplitEscalate": "OFF",
            "priorCooloff": 0,
            "reason": "flag-disabled",
            "priorLoaded": False,
        }

    if current_split_escalate == "ON":
        return 0, {
            "flagName": flag_name,
            "flagEnabled": flag_enabled,
            "active": False,
            "currentSplitEscalate": current_split_escalate,
            "priorSplitEscalate": "ON",
            "priorCooloff": 0,
            "reason": "split-escalation-active-no-cooloff",
            "priorLoaded": False,
        }

    prior_split_escalate = "OFF"
    prior_cooloff = 0
    prior_loaded = False
    if prior_json_path.exists():
        try:
            prior = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_split_escalate = str(prior.get("whatIfSplitEscalate", "OFF"))
            prior_cooloff = int(prior.get("whatIfSplitEscCool", 0) or 0)
            prior_loaded = True
        except (json.JSONDecodeError, OSError, ValueError, TypeError):
            prior_split_escalate = "OFF"
            prior_cooloff = 0
            prior_loaded = False

    if prior_split_escalate == "ON":
        cooloff = 1
        reason = "split-escalation-just-disarmed"
    elif prior_cooloff > 0:
        cooloff = prior_cooloff + 1
        reason = "split-escalation-cooloff-continuing"
    else:
        cooloff = 0
        reason = "no-prior-split-escalation-cycle"

    return cooloff, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "active": cooloff > 0,
        "currentSplitEscalate": current_split_escalate,
        "priorSplitEscalate": prior_split_escalate,
        "priorCooloff": prior_cooloff,
        "reason": reason,
        "priorLoaded": prior_loaded,
    }


def what_if_split_escalate_state_from_signals(
    *,
    what_if_split_escalate: str,
    what_if_split_esc_cool: int,
) -> tuple[str, dict[str, str | int | bool]]:
    """Summarize split-escalation lifecycle into one triage token."""
    if what_if_split_escalate == "ON":
        state = "ARMED"
        reason = "split-escalation-active"
    elif what_if_split_esc_cool > 0:
        state = "COOLING"
        reason = "split-escalation-cooloff-active"
    else:
        state = "IDLE"
        reason = "split-escalation-idle"

    return state, {
        "splitEscalate": what_if_split_escalate,
        "splitEscCool": what_if_split_esc_cool,
        "cooling": what_if_split_esc_cool > 0,
        "reason": reason,
    }


def anomaly_pulse_from_signals(
    *, sticky_count: int, pressure_churn: int
) -> tuple[str, str, dict[str, int | bool]]:
    sticky_threshold = 3
    pressure_threshold = 5
    sticky_met = sticky_count >= sticky_threshold
    pressure_met = pressure_churn >= pressure_threshold
    trigger_count = int(sticky_met) + int(pressure_met)
    sticky_gap = max(0, sticky_count - sticky_threshold)
    pressure_gap = max(0, pressure_churn - pressure_threshold)
    combined_gap = sticky_gap + pressure_gap
    is_spike = sticky_met and pressure_met

    anomaly_conf = "LOW"
    if is_spike:
        if combined_gap >= 6:
            anomaly_conf = "HIGH"
        elif combined_gap >= 2:
            anomaly_conf = "MID"
    elif trigger_count == 1:
        if sticky_gap >= 2 or pressure_gap >= 4:
            anomaly_conf = "MID"

    return ("ON" if is_spike else "OFF"), anomaly_conf, {
        "stickyCount": sticky_count,
        "stickyThreshold": sticky_threshold,
        "pressureChurn": pressure_churn,
        "pressureThreshold": pressure_threshold,
        "stickyMet": sticky_met,
        "pressureMet": pressure_met,
        "triggerCount": trigger_count,
        "stickyGap": sticky_gap,
        "pressureGap": pressure_gap,
        "combinedGap": combined_gap,
        "spike": is_spike,
    }


def route_sandbox_from_signals(*, lane_lock_signals: dict[str, int | str | bool]) -> tuple[str, dict[str, str | bool | int]]:
    flag_name = "DOTPIO_EXPERIMENT_ROUTE_SANDBOX"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}
    lane_lock_armed = bool(lane_lock_signals.get("armed", False))
    enabled = flag_enabled and lane_lock_armed

    if enabled:
        reason = "flag-enabled-with-sustained-lane-lock"
    elif flag_enabled:
        reason = "flag-enabled-but-lane-lock-not-armed"
    elif lane_lock_armed:
        reason = "lane-lock-armed-but-flag-disabled"
    else:
        reason = "flag-disabled-and-lane-lock-not-armed"

    return ("ON" if enabled else "OFF"), {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "laneLockArmed": lane_lock_armed,
        "laneLock": str(lane_lock_signals.get("lane", "MIXED")),
        "laneLockStreak": int(lane_lock_signals.get("streak", 0)),
        "threshold": int(lane_lock_signals.get("threshold", 0)),
        "reason": reason,
    }


def route_sandbox_plan_from_signals(*, route_sandbox: str, action_guard: str, drift_risk: str) -> tuple[str, dict[str, str]]:
    if route_sandbox == "ON" and action_guard == "LOCK":
        plan = "SIMULATE"
        reason = "sandbox-enabled-under-lock-guardrail"
    elif route_sandbox == "ON":
        plan = "PROBE"
        reason = "sandbox-enabled-soft-guardrail"
    elif drift_risk == "HIGH":
        plan = "PREPARE"
        reason = "high-risk-waiting-on-sandbox-flag"
    else:
        plan = "HOLD"
        reason = "no-sandbox-activation-needed"

    return plan, {
        "routeSandbox": route_sandbox,
        "actionGuard": action_guard,
        "driftRisk": drift_risk,
        "reason": reason,
    }


def sandbox_target_from_signals(*, route_sandbox: str, lane_lock_signals: dict[str, int | str | bool]) -> tuple[str, dict[str, str | bool | int]]:
    lane = str(lane_lock_signals.get("lane", "MIXED"))
    armed = bool(lane_lock_signals.get("armed", False))
    streak = int(lane_lock_signals.get("streak", 0))

    if route_sandbox == "ON" and armed and lane != "MIXED":
        target = lane
        target_source = "LOCK"
        reason = "sandbox-active-using-lane-lock-family"
    elif route_sandbox == "ON" and lane == "MIXED":
        target = "MIXED"
        target_source = "MIXED"
        reason = "sandbox-active-with-mixed-lane-lock"
    else:
        target = "NONE"
        target_source = "NONE"
        reason = "sandbox-inactive"

    return target, {
        "routeSandbox": route_sandbox,
        "lane": lane,
        "laneLockArmed": armed,
        "laneLockStreak": streak,
        "targetSource": target_source,
        "reason": reason,
    }


def sandbox_target_confidence_from_signals(
    *,
    sandbox_target: str,
    route_action_confidence: str,
    lane_lock_signals: dict[str, int | str | bool],
) -> tuple[str, dict[str, str | int | bool]]:
    streak = int(lane_lock_signals.get("streak", 0))
    armed = bool(lane_lock_signals.get("armed", False))

    if sandbox_target in {"NONE", "MIXED"}:
        confidence = "LOW"
        reason = "no-single-lane-target"
    elif route_action_confidence == "HIGH" and armed and streak >= 3:
        confidence = "HIGH"
        reason = "high-route-confidence-with-sustained-lock"
    elif route_action_confidence in {"MID", "HIGH"} and armed:
        confidence = "MID"
        reason = "armed-lane-lock-with-moderate-confidence"
    else:
        confidence = "LOW"
        reason = "insufficient-signal-strength"

    return confidence, {
        "sandboxTarget": sandbox_target,
        "routeActionConfidence": route_action_confidence,
        "laneLockArmed": armed,
        "laneLockStreak": streak,
        "reason": reason,
    }


def sandbox_readiness_from_signals(
    *,
    route_sandbox: str,
    sandbox_target_confidence: str,
    action_guard: str,
    lane_lock_signals: dict[str, int | str | bool],
) -> tuple[str, dict[str, str | bool | int]]:
    lane_lock_armed = bool(lane_lock_signals.get("armed", False))
    lane_lock_streak = int(lane_lock_signals.get("streak", 0))

    if route_sandbox == "ON" and sandbox_target_confidence in {"MID", "HIGH"} and lane_lock_armed:
        tier = "ARMED"
        reason = "sandbox-on-with-credible-target"
    elif lane_lock_armed or sandbox_target_confidence in {"MID", "HIGH"} or action_guard == "LOCK":
        tier = "PRIMED"
        reason = "preconditions-forming"
    else:
        tier = "IDLE"
        reason = "no-activation-pressure"

    return tier, {
        "routeSandbox": route_sandbox,
        "sandboxTargetConfidence": sandbox_target_confidence,
        "actionGuard": action_guard,
        "laneLockArmed": lane_lock_armed,
        "laneLockStreak": lane_lock_streak,
        "reason": reason,
    }


def sandbox_target_shift_from_prior(*, current_target: str, prior_json_path: Path) -> tuple[str, dict[str, str | bool]]:
    prior_target = current_target
    prior_loaded = False

    if prior_json_path.is_file():
        try:
            prior = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_target = str(prior.get("sandboxTarget", current_target))
            prior_loaded = True
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    shift = f"{prior_target}->{current_target}"
    changed = prior_target != current_target
    reason = "target-switched" if changed else "target-stable"
    if not prior_loaded:
        reason = "no-prior-target"

    return shift, {
        "priorTarget": prior_target,
        "currentTarget": current_target,
        "changed": changed,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }
def sandbox_cooloff_from_prior(*, current_sandbox: str, prior_json_path: Path) -> tuple[int, dict[str, str | int | bool]]:
    """Count consecutive non-armed digest windows since last ROUTE SANDBOX:ON cycle.

    Returns (cooloff_count, signals_dict).
    - If current sandbox is ON, cooloff resets to 0.
    - If prior digest had sandbox ON and current is OFF, cooloff starts at 1.
    - If prior digest already had a cooloff counter and current is still OFF, increment.
    """
    if current_sandbox == "ON":
        return 0, {
            "active": False,
            "currentSandbox": current_sandbox,
            "priorSandbox": "N/A",
            "priorCooloff": 0,
            "reason": "sandbox-active-no-cooloff",
        }

    prior_sandbox = "OFF"
    prior_cooloff = 0
    prior_loaded = False

    if prior_json_path.is_file():
        try:
            prior = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_sandbox = prior.get("routeSandbox", "OFF")
            prior_cooloff = prior.get("sandboxCooloff", 0)
            prior_loaded = True
        except (json.JSONDecodeError, KeyError, TypeError):
            pass

    if prior_sandbox == "ON":
        cooloff = 1
        reason = "sandbox-just-disarmed"
    elif prior_cooloff > 0:
        cooloff = prior_cooloff + 1
        reason = "cooloff-continuing"
    else:
        cooloff = 0
        reason = "no-prior-on-cycle"

    return cooloff, {
        "active": cooloff > 0,
        "currentSandbox": current_sandbox,
        "priorSandbox": prior_sandbox,
        "priorCooloff": prior_cooloff,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def commit_stats(root: Path, commit: str) -> dict:
    meta = git(root, "show", "-s", "--format=%H%n%ct%n%an%n%s", commit).splitlines()
    sha, ts, author = meta[0], int(meta[1]), meta[2]
    subject = meta[3] if len(meta) > 3 else ""
    files = changed_files(root, commit)
    portal_files = [p for p in files if touched_portal_path(p)]

    added = {k: 0 for k in TOKEN_GROUPS}
    removed = {k: 0 for k in TOKEN_GROUPS}
    token_added = {token: 0 for token in TOKEN_CATALOG}
    token_removed = {token: 0 for token in TOKEN_CATALOG}
    pressure_added = 0
    pressure_removed = 0

    if portal_files:
        patch = git(root, "show", "--pretty=format:", commit, "--", *portal_files)
        for raw in patch.splitlines():
            if raw.startswith("+++") or raw.startswith("---"):
                continue
            if raw.startswith("+"):
                line = raw[1:]
                c = count_tokens_in_line(line)
                c_tokens = count_catalog_tokens_in_line(line)
                for k, v in c.items():
                    added[k] += v
                for token, v in c_tokens.items():
                    token_added[token] += v
                pressure_added += sum(line.count(token) for token in PRESSURE_TOKENS)
            elif raw.startswith("-"):
                line = raw[1:]
                c = count_tokens_in_line(line)
                c_tokens = count_catalog_tokens_in_line(line)
                for k, v in c.items():
                    removed[k] += v
                for token, v in c_tokens.items():
                    token_removed[token] += v
                pressure_removed += sum(line.count(token) for token in PRESSURE_TOKENS)

    net = {k: added[k] - removed[k] for k in TOKEN_GROUPS}
    token_net = {token: token_added[token] - token_removed[token] for token in TOKEN_CATALOG}
    pressure_net = pressure_added - pressure_removed
    touched = bool(portal_files)
    mode = "neutral"
    if net["compact"] > net["detailed"]:
        mode = "compact"
    elif net["detailed"] > net["compact"]:
        mode = "detailed"

    return {
        "sha": sha,
        "shortSha": sha[:7],
        "author": author,
        "subject": subject,
        "committedAt": datetime.fromtimestamp(ts, tz=timezone.utc).isoformat().replace("+00:00", "Z"),
        "changedFiles": files,
        "portalFiles": portal_files,
        "touchedPortalPrompt": touched,
        "added": added,
        "removed": removed,
        "net": net,
        "dominantMode": mode,
        "laneFocus": lane_focus_from_token_net(token_net),
        "pressureEdits": {
            "added": pressure_added,
            "removed": pressure_removed,
            "net": pressure_net,
        },
        "tokenEdits": {
            "added": token_added,
            "removed": token_removed,
            "net": token_net,
        },
    }


def main() -> int:
    args = parse_args()
    root = args.repo_root.resolve()
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    revs = git(root, "rev-list", f"--since={args.since_days}.days", f"--max-count={args.max_commits}", "HEAD")
    commits = [c for c in revs.splitlines() if c.strip()]
    rows = [commit_stats(root, c) for c in commits]
    touched = [r for r in rows if r["touchedPortalPrompt"]]

    totals = {
        "added": {k: sum(r["added"][k] for r in touched) for k in TOKEN_GROUPS},
        "removed": {k: sum(r["removed"][k] for r in touched) for k in TOKEN_GROUPS},
        "net": {k: sum(r["net"][k] for r in touched) for k in TOKEN_GROUPS},
    }
    token_totals = {
        "added": {token: sum(r["tokenEdits"]["added"][token] for r in touched) for token in TOKEN_CATALOG},
        "removed": {token: sum(r["tokenEdits"]["removed"][token] for r in touched) for token in TOKEN_CATALOG},
        "net": {token: sum(r["tokenEdits"]["net"][token] for r in touched) for token in TOKEN_CATALOG},
    }

    compact_commits = sum(1 for r in touched if r["dominantMode"] == "compact")
    detailed_commits = sum(1 for r in touched if r["dominantMode"] == "detailed")
    neutral_commits = sum(1 for r in touched if r["dominantMode"] == "neutral")

    mode_trend = "BALANCED"
    if compact_commits > detailed_commits:
        mode_trend = "COMPACT"
    elif detailed_commits > compact_commits:
        mode_trend = "DETAILED"

    pressure_added = sum(r["pressureEdits"]["added"] for r in touched)
    pressure_removed = sum(r["pressureEdits"]["removed"] for r in touched)
    pressure_net = pressure_added - pressure_removed
    pressure_band = pressure_band_from_net(pressure_net)
    drift_risk, drift_risk_signals = drift_risk_from_signals(
        compact_net=totals["net"]["compact"],
        detailed_net=totals["net"]["detailed"],
        pressure_net=pressure_net,
    )

    token_movers = [
        {
            "token": token,
            "net": token_totals["net"][token],
            "added": token_totals["added"][token],
            "removed": token_totals["removed"][token],
        }
        for token in TOKEN_CATALOG
        if token_totals["net"][token] != 0
    ]
    token_movers.sort(key=lambda row: (abs(row["net"]), row["token"]), reverse=True)

    sticky_tokens = [
        token
        for token in TOKEN_CATALOG
        if token_totals["added"][token] > 0 and token_totals["removed"][token] > 0
    ]
    lane_focus, lane_focus_scores = lane_focus_from_token_totals(token_totals)
    commit_focuses = [r["laneFocus"] for r in touched if r["laneFocus"] != "MIXED"]
    focus_streak, focus_shift = focus_streak_and_shift(
        commit_focuses=commit_focuses,
        aggregate_focus=lane_focus,
    )
    focus_volatility, focus_volatility_signals = focus_volatility_from_commits(commit_focuses)
    route_action, route_action_reason = route_action_from_focus(
        lane_focus=lane_focus,
        drift_risk=drift_risk,
    )
    route_action_confidence, route_action_confidence_signals = route_action_confidence_from_signals(
        lane_focus=lane_focus,
        lane_focus_scores=lane_focus_scores,
        drift_risk_signals=drift_risk_signals,
    )
    focus_balance, focus_balance_signals = focus_balance_from_scores(lane_focus_scores)
    focus_entropy, focus_entropy_signals = focus_entropy_from_scores(lane_focus_scores)
    action_guard, action_guard_signals = route_action_guardrail_from_signals(
        drift_risk=drift_risk,
        route_action_confidence=route_action_confidence,
    )
    lane_lock, lane_lock_signals = lane_lock_from_focus(
        lane_focus=lane_focus,
        focus_streak=focus_streak,
    )
    route_sandbox, route_sandbox_signals = route_sandbox_from_signals(
        lane_lock_signals=lane_lock_signals,
    )
    route_sandbox_plan, route_sandbox_plan_signals = route_sandbox_plan_from_signals(
        route_sandbox=route_sandbox,
        action_guard=action_guard,
        drift_risk=drift_risk,
    )
    sandbox_target, sandbox_target_signals = sandbox_target_from_signals(
        route_sandbox=route_sandbox,
        lane_lock_signals=lane_lock_signals,
    )
    sandbox_target_confidence, sandbox_target_confidence_signals = sandbox_target_confidence_from_signals(
        sandbox_target=sandbox_target,
        route_action_confidence=route_action_confidence,
        lane_lock_signals=lane_lock_signals,
    )
    sandbox_readiness, sandbox_readiness_signals = sandbox_readiness_from_signals(
        route_sandbox=route_sandbox,
        sandbox_target_confidence=sandbox_target_confidence,
        action_guard=action_guard,
        lane_lock_signals=lane_lock_signals,
    )
    sandbox_target_shift, sandbox_target_shift_signals = sandbox_target_shift_from_prior(
        current_target=sandbox_target,
        prior_json_path=args.out_json,
    )
    sandbox_cooloff, sandbox_cooloff_signals = sandbox_cooloff_from_prior(
        current_sandbox=route_sandbox,
        prior_json_path=args.out_json,
    )
    drift_momentum, drift_momentum_signals = drift_momentum_from_commits(touched)
    action_stability, action_stability_signals = route_action_stability_from_signals(
        route_action_confidence=route_action_confidence,
        focus_volatility=focus_volatility,
        drift_momentum=drift_momentum,
    )
    pressure_lag, pressure_lag_signals = pressure_latency_from_signals(
        pressure_churn=drift_risk_signals["pressureChurn"],
        drift_momentum=drift_momentum,
        drift_momentum_delta=drift_momentum_signals["delta"],
    )
    what_if_alt, what_if_alt_signals = what_if_alt_from_signals(
        lane_focus=lane_focus,
        lane_focus_scores=lane_focus_scores,
        drift_risk_signals=drift_risk_signals,
    )
    what_if_confidence, what_if_confidence_signals = what_if_confidence_from_signals(
        what_if_alt_signals=what_if_alt_signals,
        route_action_confidence=route_action_confidence,
    )
    what_if_align, what_if_align_signals = what_if_alignment_from_signals(
        what_if_alt_signals=what_if_alt_signals,
        route_action=route_action,
    )
    what_if_band, what_if_band_signals = what_if_impact_band_from_signals(
        what_if_alt_signals=what_if_alt_signals,
    )
    what_if_magnitude, what_if_magnitude_signals = what_if_magnitude_from_signals(
        what_if_alt_signals=what_if_alt_signals,
    )
    what_if_fit, what_if_fit_signals = what_if_pressure_fit_from_signals(
        what_if_alt_signals=what_if_alt_signals,
        pressure_band=pressure_band,
    )
    what_if_fallback, what_if_fallback_signals = what_if_lane_fallback_from_signals(
        what_if_alt_signals=what_if_alt_signals,
        what_if_align=what_if_align,
        route_action=route_action,
    )
    what_if_fallback_confidence, what_if_fallback_confidence_signals = what_if_fallback_confidence_from_signals(
        what_if_fallback=what_if_fallback,
        what_if_fallback_signals=what_if_fallback_signals,
        what_if_alt_signals=what_if_alt_signals,
        route_action_confidence=route_action_confidence,
    )
    what_if_fallback_fit, what_if_fallback_fit_signals = what_if_fallback_pressure_fit_from_signals(
        what_if_fallback=what_if_fallback,
        what_if_fallback_signals=what_if_fallback_signals,
        what_if_alt_signals=what_if_alt_signals,
        pressure_band=pressure_band,
    )
    what_if_fallback_why, what_if_fallback_why_signals = what_if_fallback_why_from_signals(
        what_if_fallback=what_if_fallback,
        what_if_fallback_signals=what_if_fallback_signals,
        what_if_fallback_confidence=what_if_fallback_confidence,
        what_if_fallback_fit=what_if_fallback_fit,
        what_if_alt_signals=what_if_alt_signals,
        pressure_band=pressure_band,
    )
    what_if_fallback_align, what_if_fallback_align_signals = what_if_fallback_alignment_from_signals(
        what_if_fallback=what_if_fallback,
        lane_focus=lane_focus,
    )
    what_if_fallback_magnitude, what_if_fallback_magnitude_signals = what_if_fallback_magnitude_from_signals(
        what_if_fallback=what_if_fallback,
        what_if_fallback_signals=what_if_fallback_signals,
        what_if_alt_signals=what_if_alt_signals,
    )
    what_if_fallback_alt2, what_if_fallback_alt2_signals = what_if_fallback_alt2_from_signals(
        what_if_fallback=what_if_fallback,
        lane_focus_scores=lane_focus_scores,
    )
    what_if_fallback_alt2_confidence, what_if_fallback_alt2_confidence_signals = what_if_fallback_alt2_confidence_from_signals(
        what_if_fallback_alt2=what_if_fallback_alt2,
        what_if_fallback_alt2_signals=what_if_fallback_alt2_signals,
    )
    what_if_fallback_plan, what_if_fallback_plan_signals = what_if_fallback_plan_from_signals(
        what_if_fallback=what_if_fallback,
        what_if_fallback_confidence=what_if_fallback_confidence,
        what_if_fallback_alt2=what_if_fallback_alt2,
        what_if_fallback_alt2_confidence=what_if_fallback_alt2_confidence,
    )
    what_if_fallback_plan_fit, what_if_fallback_plan_fit_signals = what_if_fallback_plan_fit_from_signals(
        what_if_fallback_plan=what_if_fallback_plan,
        what_if_fallback_fit=what_if_fallback_fit,
        what_if_fallback_alt2=what_if_fallback_alt2,
        what_if_alt_signals=what_if_alt_signals,
        pressure_band=pressure_band,
    )
    what_if_fallback_plan_why, what_if_fallback_plan_why_signals = what_if_fallback_plan_why_from_signals(
        what_if_fallback_plan=what_if_fallback_plan,
        what_if_fallback_plan_signals=what_if_fallback_plan_signals,
        what_if_fallback_plan_fit=what_if_fallback_plan_fit,
    )
    what_if_split, what_if_split_signals = what_if_split_from_signals(
        what_if_fallback_plan_signals=what_if_fallback_plan_signals,
        what_if_alt_signals=what_if_alt_signals,
    )
    what_if_split_lanes, what_if_split_lanes_signals = what_if_split_lanes_from_signals(
        what_if_split_signals=what_if_split_signals,
    )
    what_if_split_confidence, what_if_split_confidence_signals = what_if_split_confidence_from_signals(
        what_if_split=what_if_split,
        what_if_split_signals=what_if_split_signals,
    )
    what_if_split_safe, what_if_split_safe_signals = what_if_split_safe_from_signals(
        what_if_split=what_if_split,
        what_if_split_signals=what_if_split_signals,
        what_if_fallback_fit=what_if_fallback_fit,
        what_if_fallback_alt2_confidence=what_if_fallback_alt2_confidence,
    )
    what_if_split_posture, what_if_split_posture_signals = what_if_split_posture_from_signals(
        what_if_split=what_if_split,
        what_if_split_safe=what_if_split_safe,
        what_if_split_confidence=what_if_split_confidence,
    )
    what_if_split_cooloff, what_if_split_cooloff_signals = what_if_split_cooloff_from_prior(
        current_split=what_if_split,
        prior_json_path=args.out_json,
    )
    what_if_split_escalate, what_if_split_escalate_signals = what_if_split_escalate_from_signals(
        what_if_split=what_if_split,
        what_if_split_signals=what_if_split_signals,
        what_if_fallback_plan_fit=what_if_fallback_plan_fit,
    )
    what_if_split_escalate_confidence, what_if_split_escalate_confidence_signals = what_if_split_escalate_confidence_from_signals(
        what_if_split_escalate=what_if_split_escalate,
        what_if_split_confidence=what_if_split_confidence,
        what_if_fallback_plan_fit=what_if_fallback_plan_fit,
    )
    what_if_split_escalate_lanes, what_if_split_escalate_lanes_signals = what_if_split_escalate_lanes_from_signals(
        what_if_split_escalate=what_if_split_escalate,
        what_if_split_signals=what_if_split_signals,
    )
    what_if_split_esc_cool, what_if_split_esc_cool_signals = what_if_split_escalate_cooloff_from_prior(
        current_split_escalate=what_if_split_escalate,
        prior_json_path=args.out_json,
    )
    what_if_split_esc_state, what_if_split_esc_state_signals = what_if_split_escalate_state_from_signals(
        what_if_split_escalate=what_if_split_escalate,
        what_if_split_esc_cool=what_if_split_esc_cool,
    )
    anomaly_pulse, anomaly_confidence, anomaly_pulse_signals = anomaly_pulse_from_signals(
        sticky_count=len(sticky_tokens),
        pressure_churn=drift_risk_signals["pressureChurn"],
    )

    status = "ok"
    if touched and totals["net"]["compact"] < 0 and totals["net"]["detailed"] > 0:
        status = "warn"

    payload = {
        "generatedAt": now,
        "status": status,
        "window": {"sinceDays": args.since_days, "maxCommits": args.max_commits},
        "checkedCommits": len(rows),
        "portalPromptCommits": len(touched),
        "dominantModeCommits": {
            "compact": compact_commits,
            "detailed": detailed_commits,
            "neutral": neutral_commits,
        },
        "modeTrend": mode_trend,
        "pressureBand": pressure_band,
        "driftRisk": drift_risk,
        "driftRiskSignals": drift_risk_signals,
        "laneFocus": lane_focus,
        "laneFocusScores": lane_focus_scores,
        "focusStreak": focus_streak,
        "focusShift": focus_shift,
        "focusVolatility": focus_volatility,
        "focusVolatilitySignals": focus_volatility_signals,
        "routeAction": route_action,
        "routeActionReason": route_action_reason,
        "routeActionConfidence": route_action_confidence,
        "routeActionConfidenceSignals": route_action_confidence_signals,
        "focusBalance": focus_balance,
        "focusBalanceSignals": focus_balance_signals,
        "focusEntropy": focus_entropy,
        "focusEntropySignals": focus_entropy_signals,
        "actionGuard": action_guard,
        "actionGuardSignals": action_guard_signals,
        "laneLock": lane_lock,
        "laneLockSignals": lane_lock_signals,
        "routeSandbox": route_sandbox,
        "routeSandboxSignals": route_sandbox_signals,
        "routeSandboxPlan": route_sandbox_plan,
        "routeSandboxPlanSignals": route_sandbox_plan_signals,
        "sandboxTarget": sandbox_target,
        "sandboxTargetSignals": sandbox_target_signals,
        "sandboxTargetSource": str(sandbox_target_signals.get("targetSource", "NONE")),
        "sandboxTargetConfidence": sandbox_target_confidence,
        "sandboxTargetConfidenceSignals": sandbox_target_confidence_signals,
        "sandboxReadiness": sandbox_readiness,
        "sandboxReadinessSignals": sandbox_readiness_signals,
        "sandboxTargetShift": sandbox_target_shift,
        "sandboxTargetShiftSignals": sandbox_target_shift_signals,
        "sandboxCooloff": sandbox_cooloff,
        "sandboxCooloffSignals": sandbox_cooloff_signals,
        "driftMomentum": drift_momentum,
        "driftMomentumSignals": drift_momentum_signals,
        "actionStability": action_stability,
        "actionStabilitySignals": action_stability_signals,
        "pressureLag": pressure_lag,
        "pressureLagSignals": pressure_lag_signals,
        "whatIfAlt": what_if_alt,
        "whatIfAltSignals": what_if_alt_signals,
        "whatIfConfidence": what_if_confidence,
        "whatIfConfidenceSignals": what_if_confidence_signals,
        "whatIfAlign": what_if_align,
        "whatIfAlignSignals": what_if_align_signals,
        "whatIfBand": what_if_band,
        "whatIfBandSignals": what_if_band_signals,
        "whatIfMagnitude": what_if_magnitude,
        "whatIfMagnitudeSignals": what_if_magnitude_signals,
        "whatIfFit": what_if_fit,
        "whatIfFitSignals": what_if_fit_signals,
        "whatIfFallback": what_if_fallback,
        "whatIfFallbackSignals": what_if_fallback_signals,
        "whatIfFallbackConfidence": what_if_fallback_confidence,
        "whatIfFallbackConfidenceSignals": what_if_fallback_confidence_signals,
        "whatIfFallbackFit": what_if_fallback_fit,
        "whatIfFallbackFitSignals": what_if_fallback_fit_signals,
        "whatIfFallbackWhy": what_if_fallback_why,
        "whatIfFallbackWhySignals": what_if_fallback_why_signals,
        "whatIfFallbackAlign": what_if_fallback_align,
        "whatIfFallbackAlignSignals": what_if_fallback_align_signals,
        "whatIfFallbackMagnitude": what_if_fallback_magnitude,
        "whatIfFallbackMagnitudeSignals": what_if_fallback_magnitude_signals,
        "whatIfFallbackAlt2": what_if_fallback_alt2,
        "whatIfFallbackAlt2Signals": what_if_fallback_alt2_signals,
        "whatIfFallbackAlt2Confidence": what_if_fallback_alt2_confidence,
        "whatIfFallbackAlt2ConfidenceSignals": what_if_fallback_alt2_confidence_signals,
        "whatIfFallbackPlan": what_if_fallback_plan,
        "whatIfFallbackPlanSignals": what_if_fallback_plan_signals,
        "whatIfFallbackPlanFit": what_if_fallback_plan_fit,
        "whatIfFallbackPlanFitSignals": what_if_fallback_plan_fit_signals,
        "whatIfFallbackPlanWhy": what_if_fallback_plan_why,
        "whatIfFallbackPlanWhySignals": what_if_fallback_plan_why_signals,
        "whatIfSplit": what_if_split,
        "whatIfSplitSignals": what_if_split_signals,
        "whatIfSplitLanes": what_if_split_lanes,
        "whatIfSplitLanesSignals": what_if_split_lanes_signals,
        "whatIfSplitConfidence": what_if_split_confidence,
        "whatIfSplitConfidenceSignals": what_if_split_confidence_signals,
        "whatIfSplitSafe": what_if_split_safe,
        "whatIfSplitSafeSignals": what_if_split_safe_signals,
        "whatIfSplitPosture": what_if_split_posture,
        "whatIfSplitPostureSignals": what_if_split_posture_signals,
        "whatIfSplitCooloff": what_if_split_cooloff,
        "whatIfSplitCooloffSignals": what_if_split_cooloff_signals,
        "whatIfSplitEscalate": what_if_split_escalate,
        "whatIfSplitEscalateSignals": what_if_split_escalate_signals,
        "whatIfSplitEscalateConfidence": what_if_split_escalate_confidence,
        "whatIfSplitEscalateConfidenceSignals": what_if_split_escalate_confidence_signals,
        "whatIfSplitEscLanes": what_if_split_escalate_lanes,
        "whatIfSplitEscLanesSignals": what_if_split_escalate_lanes_signals,
        "whatIfSplitEscCool": what_if_split_esc_cool,
        "whatIfSplitEscCoolSignals": what_if_split_esc_cool_signals,
        "whatIfSplitEscState": what_if_split_esc_state,
        "whatIfSplitEscStateSignals": what_if_split_esc_state_signals,
        "anomalyPulse": anomaly_pulse,
        "anomalyConfidence": anomaly_confidence,
        "anomalyPulseSignals": anomaly_pulse_signals,
        "pressureEdits": {
            "added": pressure_added,
            "removed": pressure_removed,
            "net": pressure_net,
        },
        "totals": totals,
        "tokenTotals": token_totals,
        "stickyTokens": {
            "count": len(sticky_tokens),
            "tokens": sticky_tokens,
        },
        "topTokenMovers": token_movers[:5],
        "commits": rows,
    }

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = [
        "# Weekly Portal Prompt Readability Drift Digest",
        "",
        f"- GeneratedAt(UTC): {now}",
        f"- Status: **{status.upper()}**",
        f"- Window: last {args.since_days} days (max {args.max_commits} commits)",
        f"- Checked commits: {len(rows)}",
        f"- Portal prompt commits: {len(touched)}",
        f"- Dominant mode commits: compact={compact_commits}, detailed={detailed_commits}, neutral={neutral_commits}",
        f"- MODE TREND: **{mode_trend}**",
        f"- PRESSURE BAND: **{pressure_band}** (edits +{pressure_added} / -{pressure_removed} / net {pressure_net})",
        f"- DRIFT RISK: **{drift_risk}** (score={drift_risk_signals['score']} | imbalance={drift_risk_signals['imbalance']} | pressure={drift_risk_signals['pressureChurn']})",
        f"- FOCUS: **{lane_focus}** (portal={lane_focus_scores['portal']} | alt={lane_focus_scores['alt']} | pressure={lane_focus_scores['pressure']})",
        f"- FOCUS STREAK: **{focus_streak}**",
        f"- FOCUS SHIFT: **{focus_shift}**",
        f"- FOCUS VOL: **{focus_volatility}** (switches={focus_volatility_signals['switches']}/{focus_volatility_signals['edges']} ratio={focus_volatility_signals['switchRatio']})",
        f"- ROUTE ACTION: **{route_action}** ({route_action_reason})",
        f"- ACTION CONF: **{route_action_confidence}** (dom={route_action_confidence_signals['dominanceRatio']} spread={route_action_confidence_signals['focusSpread']} driftSpread={route_action_confidence_signals['driftSpread']})",
        f"- FOCUS BAL: **{focus_balance}** (top={focus_balance_signals['topScore']} total={focus_balance_signals['totalScore']} dom={focus_balance_signals['dominanceRatio']})",
        f"- FOCUS ENTROPY: **{focus_entropy}** (norm={focus_entropy_signals['normalized']} raw={focus_entropy_signals['raw']} max={focus_entropy_signals['maxEntropy']})",
        f"- ACTION GUARD: **{action_guard}** ({action_guard_signals['reason']}; risk={action_guard_signals['driftRisk']} conf={action_guard_signals['actionConfidence']})",
        f"- LANE LOCK: **{lane_lock}** (threshold={lane_lock_signals['threshold']} lane={lane_lock_signals['lane']} streak={lane_lock_signals['streak']})",
        f"- ROUTE SANDBOX: **{route_sandbox}** ({route_sandbox_signals['reason']}; flag={route_sandbox_signals['flagName']} enabled={route_sandbox_signals['flagEnabled']} laneLock={route_sandbox_signals['laneLock']}x{route_sandbox_signals['laneLockStreak']})",
        f"- SANDBOX PLAN: **{route_sandbox_plan}** ({route_sandbox_plan_signals['reason']}; guard={route_sandbox_plan_signals['actionGuard']} risk={route_sandbox_plan_signals['driftRisk']})",
        f"- SANDBOX TARGET: **{sandbox_target}** ({sandbox_target_signals['reason']}; lane={sandbox_target_signals['lane']} armed={sandbox_target_signals['laneLockArmed']} streak={sandbox_target_signals['laneLockStreak']})",
        f"- TARGET SRC: **{sandbox_target_signals['targetSource']}** (sandbox={sandbox_target_signals['routeSandbox']} target={sandbox_target})",
        f"- SANDBOX TARGET CONF: **{sandbox_target_confidence}** ({sandbox_target_confidence_signals['reason']}; routeConf={sandbox_target_confidence_signals['routeActionConfidence']} lock={sandbox_target_confidence_signals['laneLockArmed']}x{sandbox_target_confidence_signals['laneLockStreak']})",
        f"- SANDBOX READY: **{sandbox_readiness}** ({sandbox_readiness_signals['reason']}; sandbox={sandbox_readiness_signals['routeSandbox']} conf={sandbox_readiness_signals['sandboxTargetConfidence']} guard={sandbox_readiness_signals['actionGuard']} lock={sandbox_readiness_signals['laneLockArmed']}x{sandbox_readiness_signals['laneLockStreak']})",
        f"- TARGET SHIFT: **{sandbox_target_shift}** ({sandbox_target_shift_signals['reason']}; changed={sandbox_target_shift_signals['changed']} priorLoaded={sandbox_target_shift_signals['priorLoaded']})",
        f"- SANDBOX COOLOFF: **{sandbox_cooloff}** ({sandbox_cooloff_signals['reason']}; active={sandbox_cooloff_signals['active']} prior={sandbox_cooloff_signals['priorSandbox']}:{sandbox_cooloff_signals['priorCooloff']})",
        f"- DRIFT MOMENTUM: **{drift_momentum}** (recent={drift_momentum_signals['recentAvg']} older={drift_momentum_signals['olderAvg']} delta={drift_momentum_signals['delta']})",
        f"- ACTION STABILITY: **{action_stability}** ({action_stability_signals['reason']}; conf={action_stability_signals['routeActionConfidence']} vol={action_stability_signals['focusVolatility']} momentum={action_stability_signals['driftMomentum']})",
        f"- PRESSURE LAG: **{pressure_lag}** (churn={pressure_lag_signals['pressureChurn']} momentum={pressure_lag_signals['driftMomentum']} |Δ|={pressure_lag_signals['absDriftDelta']})",
        f"- WHAT-IF: **{what_if_alt}** ({what_if_alt_signals['reason']}; flag={what_if_alt_signals['flagName']} enabled={what_if_alt_signals['flagEnabled']} current={what_if_alt_signals['currentLane']} alt={what_if_alt_signals['altLane']} risk={what_if_alt_signals['baselineRisk']}->{what_if_alt_signals['projectedRisk']})",
        f"- WHAT-IF CONF: **{what_if_confidence}** ({what_if_confidence_signals['reason']}; delta={what_if_confidence_signals['deltaRisk']} routeConf={what_if_confidence_signals['routeActionConfidence']} current={what_if_confidence_signals['currentLane']} alt={what_if_confidence_signals['altLane']})",
        f"- WHAT-IF ALIGN: **{what_if_align}** ({what_if_align_signals['reason']}; route={what_if_align_signals['routeAction']} lane={what_if_align_signals['routeActionLane']} alt={what_if_align_signals['altLane']})",
        f"- WHAT-IF BAND: **{what_if_band}** ({what_if_band_signals['reason']}; delta={what_if_band_signals['deltaRisk']} current={what_if_band_signals['currentLane']} alt={what_if_band_signals['altLane']} enabled={what_if_band_signals['flagEnabled']})",
        f"- WHAT-IF MAG: **{what_if_magnitude}** ({what_if_magnitude_signals['reason']}; delta={what_if_magnitude_signals['deltaRisk']} |Δ|={what_if_magnitude_signals['absDeltaRisk']} enabled={what_if_magnitude_signals['flagEnabled']})",
        f"- WHAT-IF FIT: **{what_if_fit}** ({what_if_fit_signals['reason']}; pressure={what_if_fit_signals['pressureBand']} projected={what_if_fit_signals['projectedBand']} risk={what_if_fit_signals['projectedRisk']} enabled={what_if_fit_signals['flagEnabled']})",
        f"- WHAT-IF FALLBACK: **{what_if_fallback}** ({what_if_fallback_signals['reason']}; flag={what_if_fallback_signals['flagName']} enabled={what_if_fallback_signals['flagEnabled']} align={what_if_fallback_signals['whatIfAlign']} route={what_if_fallback_signals['routeAction']}->{what_if_fallback_signals['routeActionLane']} alt={what_if_fallback_signals['altLane']})",
        f"- WHAT-IF FALLBACK CONF: **{what_if_fallback_confidence}** ({what_if_fallback_confidence_signals['reason']}; fallback={what_if_fallback_confidence_signals['fallback']} align={what_if_fallback_confidence_signals['whatIfAlign']} delta={what_if_fallback_confidence_signals['deltaRisk']} routeConf={what_if_fallback_confidence_signals['routeActionConfidence']} enabled={what_if_fallback_confidence_signals['flagEnabled']})",
        f"- WHAT-IF FALLBACK FIT: **{what_if_fallback_fit}** ({what_if_fallback_fit_signals['reason']}; fallback={what_if_fallback_fit_signals['fallback']} pressure={what_if_fallback_fit_signals['pressureBand']} projected={what_if_fallback_fit_signals['projectedBand']} risk={what_if_fallback_fit_signals['projectedRisk']} enabled={what_if_fallback_fit_signals['flagEnabled']})",
        f"- WHAT-IF FALLBACK WHY: **{what_if_fallback_why}** ({what_if_fallback_why_signals['reason']}; flag={what_if_fallback_why_signals['flagName']} enabled={what_if_fallback_why_signals['flagEnabled']} fallback={what_if_fallback_why_signals['fallback']} conf={what_if_fallback_why_signals['fallbackConfidence']} fit={what_if_fallback_why_signals['fallbackFit']} pressure={what_if_fallback_why_signals['pressureBand']})",
        f"- WHAT-IF FALLBACK ALIGN: **{what_if_fallback_align}** ({what_if_fallback_align_signals['reason']}; fallback={what_if_fallback_align_signals['fallback']} focus={what_if_fallback_align_signals['laneFocus']} actionable={what_if_fallback_align_signals['actionable']})",
        f"- WHAT-IF FALLBACK MAG: **{what_if_fallback_magnitude}** ({what_if_fallback_magnitude_signals['reason']}; fallback={what_if_fallback_magnitude_signals['fallback']} delta={what_if_fallback_magnitude_signals['deltaRisk']} |Δ|={what_if_fallback_magnitude_signals['absDeltaRisk']} enabled={what_if_fallback_magnitude_signals['flagEnabled']})",
        f"- WHAT-IF FALLBACK ALT2: **{what_if_fallback_alt2}** ({what_if_fallback_alt2_signals['reason']}; flag={what_if_fallback_alt2_signals['flagName']} enabled={what_if_fallback_alt2_signals['flagEnabled']} fallback={what_if_fallback_alt2_signals['fallbackLane']} scores=portal:{what_if_fallback_alt2_signals['portalScore']} alt:{what_if_fallback_alt2_signals['altScore']} pressure:{what_if_fallback_alt2_signals['pressureScore']})",
        f"- WHAT-IF FALLBACK ALT2 CONF: **{what_if_fallback_alt2_confidence}** ({what_if_fallback_alt2_confidence_signals['reason']}; alt2={what_if_fallback_alt2_confidence_signals['alt2']} fallback={what_if_fallback_alt2_confidence_signals['fallbackLane']} top={what_if_fallback_alt2_confidence_signals['topScore']} second={what_if_fallback_alt2_confidence_signals['secondScore']} gap={what_if_fallback_alt2_confidence_signals['scoreGap']} enabled={what_if_fallback_alt2_confidence_signals['flagEnabled']})",
        f"- WHAT-IF FALLBACK PLAN: **{what_if_fallback_plan}** ({what_if_fallback_plan_signals['reason']}; flag={what_if_fallback_plan_signals['flagName']} enabled={what_if_fallback_plan_signals['flagEnabled']} primary={what_if_fallback_plan_signals['fallback']}({what_if_fallback_plan_signals['fallbackConfidence']}) secondary={what_if_fallback_plan_signals['fallbackAlt2']}({what_if_fallback_plan_signals['fallbackAlt2Confidence']}))",
        f"- WHAT-IF PLAN FIT: **{what_if_fallback_plan_fit}** ({what_if_fallback_plan_fit_signals['reason']}; plan={what_if_fallback_plan_fit_signals['plan']} lane={what_if_fallback_plan_fit_signals['planLane']} pressure={what_if_fallback_plan_fit_signals['pressureBand']} projected={what_if_fallback_plan_fit_signals['projectedBand']})",
        f"- WHAT-IF PLAN WHY: **{what_if_fallback_plan_why}** ({what_if_fallback_plan_why_signals['reason']}; flag={what_if_fallback_plan_why_signals['flagName']} enabled={what_if_fallback_plan_why_signals['flagEnabled']} plan={what_if_fallback_plan_why_signals['plan']} fit={what_if_fallback_plan_why_signals['planFit']})",
        f"- WHAT-IF SPLIT: **{what_if_split}** ({what_if_split_signals['reason']}; flag={what_if_split_signals['flagName']} enabled={what_if_split_signals['flagEnabled']} lanes={what_if_split_signals['primaryLane']}->{what_if_split_signals['secondaryLane']} conf={what_if_split_signals['primaryConfidence']}/{what_if_split_signals['secondaryConfidence']} |Δ|={what_if_split_signals['absDeltaRisk']})",
        f"- WHAT-IF SPLIT LANES: **{what_if_split_lanes}** ({what_if_split_lanes_signals['reason']}; actionable={what_if_split_lanes_signals['primaryActionable']}/{what_if_split_lanes_signals['secondaryActionable']})",
        f"- WHAT-IF SPLIT CONF: **{what_if_split_confidence}** ({what_if_split_confidence_signals['reason']}; split={what_if_split_confidence_signals['split']} conf={what_if_split_confidence_signals['primaryConfidence']}/{what_if_split_confidence_signals['secondaryConfidence']} strong={what_if_split_confidence_signals['strongConfidence']} delta={what_if_split_confidence_signals['strongDelta']})",
        f"- WHAT-IF SPLIT SAFE: **{what_if_split_safe}** ({what_if_split_safe_signals['reason']}; flag={what_if_split_safe_signals['flagName']} enabled={what_if_split_safe_signals['flagEnabled']} split={what_if_split_safe_signals['split']} fit={what_if_split_safe_signals['primaryFit']} alt2Conf={what_if_split_safe_signals['secondaryConfidenceGate']})",
        f"- WHAT-IF SPLIT POSTURE: **{what_if_split_posture}** ({what_if_split_posture_signals['reason']}; split={what_if_split_posture_signals['split']} safe={what_if_split_posture_signals['splitSafe']} conf={what_if_split_posture_signals['splitConfidence']})",
        f"- WHAT-IF SPLIT COOLOFF: **{what_if_split_cooloff}** ({what_if_split_cooloff_signals['reason']}; active={what_if_split_cooloff_signals['active']} prior={what_if_split_cooloff_signals['priorSplit']}:{what_if_split_cooloff_signals['priorCooloff']})",
        f"- WHAT-IF SPLIT ESCALATE: **{what_if_split_escalate}** ({what_if_split_escalate_signals['reason']}; flag={what_if_split_escalate_signals['flagName']} enabled={what_if_split_escalate_signals['flagEnabled']} split={what_if_split_escalate_signals['split']} diverged={what_if_split_escalate_signals['lanesDiverged']} fit={what_if_split_escalate_signals['planFit']})",
        f"- WHAT-IF SPLIT ESC CONF: **{what_if_split_escalate_confidence}** ({what_if_split_escalate_confidence_signals['reason']}; escalate={what_if_split_escalate_confidence_signals['splitEscalate']} splitConf={what_if_split_escalate_confidence_signals['splitConfidence']} fit={what_if_split_escalate_confidence_signals['planFit']})",
        f"- WHAT-IF SPLIT ESC LANES: **{what_if_split_escalate_lanes}** ({what_if_split_escalate_lanes_signals['reason']}; escalate={what_if_split_escalate_lanes_signals['splitEscalate']} diverged={what_if_split_escalate_lanes_signals['lanesDiverged']} actionable={what_if_split_escalate_lanes_signals['primaryActionable']}/{what_if_split_escalate_lanes_signals['secondaryActionable']})",
        f"- WHAT-IF SPLIT ESC COOL: **{what_if_split_esc_cool}** ({what_if_split_esc_cool_signals['reason']}; flag={what_if_split_esc_cool_signals['flagName']} enabled={what_if_split_esc_cool_signals['flagEnabled']} active={what_if_split_esc_cool_signals['active']} prior={what_if_split_esc_cool_signals['priorSplitEscalate']}:{what_if_split_esc_cool_signals['priorCooloff']})",
        f"- WHAT-IF SPLIT ESC STATE: **{what_if_split_esc_state}** ({what_if_split_esc_state_signals['reason']}; escalate={what_if_split_esc_state_signals['splitEscalate']} cool={what_if_split_esc_state_signals['splitEscCool']} cooling={what_if_split_esc_state_signals['cooling']})",
        f"- STICKY TOKENS: **{len(sticky_tokens)}**",
        f"- ANOMALY: **{anomaly_pulse}** (sticky={anomaly_pulse_signals['stickyCount']}/{anomaly_pulse_signals['stickyThreshold']} pressure={anomaly_pulse_signals['pressureChurn']}/{anomaly_pulse_signals['pressureThreshold']})",
        f"- ANOMALY CONF: **{anomaly_confidence}** (triggers={anomaly_pulse_signals['triggerCount']} gap={anomaly_pulse_signals['combinedGap']})",
        "",
        "## Token Totals (added/removed/net)",
        f"- Compact: +{totals['added']['compact']} / -{totals['removed']['compact']} / net {totals['net']['compact']}",
        f"- Detailed: +{totals['added']['detailed']} / -{totals['removed']['detailed']} / net {totals['net']['detailed']}",
        f"- Shared: +{totals['added']['shared']} / -{totals['removed']['shared']} / net {totals['net']['shared']}",
        "",
        "## Top Token Movers (net ±)",
    ]
    if not token_movers:
        md.append("- No token deltas in this window.")
    else:
        for row in token_movers[:5]:
            md.append(
                f"- `{row['token']}` net {row['net']:+d} (added {row['added']}, removed {row['removed']})"
            )

    md.extend([
        "",
        "## Sticky Tokens",
    ])
    if not sticky_tokens:
        md.append("- None in this window.")
    else:
        md.append("- " + ", ".join(f"`{token}`" for token in sticky_tokens))

    md.extend([
        "",
        "## Commit-level digest",
    ])
    if not touched:
        md.append("- No portal prompt related commits in this window.")
    else:
        for r in touched:
            md.append(
                f"- `{r['shortSha']}` {r['subject']} | mode={r['dominantMode']} | "
                f"compact net={r['net']['compact']} detailed net={r['net']['detailed']} shared net={r['net']['shared']}"
            )

    args.out_md.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"[PASS] weekly portal prompt drift status={status} -> {args.out_json} {args.out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
