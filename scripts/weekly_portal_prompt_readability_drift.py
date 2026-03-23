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

ROUTE_VIBE_PATTERNS = {
    "CALM": ("ROUTE VIBE:CALM", "VIBE:C"),
    "EDGE": ("ROUTE VIBE:EDGE", "VIBE:E"),
    "DOOM": ("ROUTE VIBE:DOOM", "VIBE:D"),
}


def count_route_vibes_in_line(line: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for vibe, patterns in ROUTE_VIBE_PATTERNS.items():
        counts[vibe] = sum(line.count(pattern) for pattern in patterns)
    return counts


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

def route_action_pacing_from_signals(*, action_guard: str, action_stability: str, pressure_lag: str) -> tuple[str, dict[str, str]]:
    if action_guard == "LOCK":
        pace = "BRAKE"
        reason = "guard-locked"
    elif action_stability == "LOCKED" and pressure_lag == "FAST":
        pace = "ACCEL"
        reason = "locked-and-fast-lag"
    elif action_stability == "LOCKED":
        pace = "STEADY"
        reason = "locked-stable"
    elif pressure_lag == "SLOW":
        pace = "BRAKE"
        reason = "slow-lag-watch"
    else:
        pace = "STEADY"
        reason = "default-steady"

    return pace, {
        "actionGuard": action_guard,
        "actionStability": action_stability,
        "pressureLag": pressure_lag,
        "reason": reason,
    }


def pace_drift_from_prior(*, current_pace: str, prior_json_path: Path) -> tuple[int, dict[str, str | int | bool]]:
    pace_score = {"BRAKE": -1, "STEADY": 0, "ACCEL": 1}
    current_score = pace_score.get(current_pace, 0)

    prior_loaded = False
    prior_pace = "NONE"
    prior_score = 0

    if prior_json_path.is_file():
        try:
            prior = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_pace = str(prior.get("actionPace", "NONE") or "NONE").upper()
            prior_score = pace_score.get(prior_pace, 0)
            prior_loaded = True
        except Exception:
            prior_loaded = False
            prior_pace = "NONE"
            prior_score = 0

    drift = current_score - prior_score

    if not prior_loaded:
        reason = "no-prior-pace"
    elif drift > 0:
        reason = "pace-accelerated"
    elif drift < 0:
        reason = "pace-decelerated"
    else:
        reason = "pace-stable"

    return drift, {
        "currentPace": current_pace,
        "currentScore": current_score,
        "priorPace": prior_pace,
        "priorScore": prior_score,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def action_pace_window_from_signals(
    *,
    action_pace: str,
    action_guard: str,
    pace_drift: int,
) -> tuple[str, dict[str, str | int]]:
    """Compact go/no-go pacing window token for operator triage."""
    pace = str(action_pace).upper()
    guard = str(action_guard).upper()
    drift = int(pace_drift)

    if guard == "LOCK" or (pace == "BRAKE" and drift <= 0):
        window = "CLOSE"
        reason = "guard-or-brake-closing-window"
    elif pace == "ACCEL" and drift >= 0 and guard == "SOFT":
        window = "OPEN"
        reason = "accelerating-under-soft-guard"
    else:
        window = "HOLD"
        reason = "maintain-current-pace-window"

    return window, {
        "actionPace": pace,
        "actionGuard": guard,
        "paceDrift": drift,
        "reason": reason,
    }


def action_pace_window_confidence_from_signals(
    *,
    action_pace_window: str,
    action_stability: str,
    pace_drift: int,
    pace_drift_signals: dict[str, str | int | bool],
) -> tuple[str, dict[str, str | int | bool]]:
    """Confidence for ACTION PACE WINDOW from stability + drift continuity."""
    window = str(action_pace_window).upper()
    stability = str(action_stability).upper()
    drift = int(pace_drift)
    prior_loaded = bool(pace_drift_signals.get("priorLoaded", False))
    continuity = "STABLE" if drift == 0 else ("SHIFT" if abs(drift) == 1 else "SWING")

    if not prior_loaded:
        confidence = "LOW"
        reason = "no-prior-window-drift"
    elif stability == "LOCKED" and continuity == "STABLE":
        confidence = "HIGH"
        reason = "locked-stability-and-stable-drift"
    elif window in {"OPEN", "CLOSE"} and stability == "WATCH" and continuity == "SWING":
        confidence = "LOW"
        reason = "watch-stability-with-drift-swing"
    elif continuity == "SHIFT" or stability == "WATCH":
        confidence = "MID"
        reason = "moderate-drift-continuity"
    else:
        confidence = "MID"
        reason = "default-window-confidence"

    return confidence, {
        "actionPaceWindow": window,
        "actionStability": stability,
        "paceDrift": drift,
        "driftContinuity": continuity,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def action_pace_why_from_signals(
    *,
    action_pace: str,
    action_guard: str,
    action_stability: str,
    pressure_lag: str,
    pace_drift: int,
) -> tuple[str, dict[str, str | int | bool]]:
    """Prototype compact rationale token for ACTION PACE behind experiment flag."""
    flag_name = "DOTPIO_EXPERIMENT_ACTION_PACE_WHY"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    pace = str(action_pace).upper()
    guard = str(action_guard).upper()
    stability = str(action_stability).upper()
    lag = str(pressure_lag).upper()

    if not flag_enabled:
        why = "FLAG OFF"
        reason = "flag-disabled"
    elif pace == "BRAKE" and guard == "LOCK":
        why = "LOCK BRAKE"
        reason = "guard-lock-forced-brake"
    elif pace == "BRAKE" and lag == "SLOW":
        why = "LAG BRAKE"
        reason = "slow-pressure-lag-brake"
    elif pace == "ACCEL" and stability == "LOCKED" and lag == "FAST":
        why = "WINDOW PUSH"
        reason = "locked-stability-with-fast-lag"
    elif pace == "STEADY" and stability == "LOCKED":
        why = "LOCK HOLD"
        reason = "locked-stability-steady-pace"
    elif pace == "STEADY" and pace_drift > 0:
        why = "EASE UP"
        reason = "pace-accelerating-into-steady"
    elif pace == "STEADY" and pace_drift < 0:
        why = "SETTLE"
        reason = "pace-cooling-into-steady"
    else:
        why = "WATCH FLOW"
        reason = "default-watch-state"

    return why, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "actionPace": pace,
        "actionGuard": guard,
        "actionStability": stability,
        "pressureLag": lag,
        "paceDrift": int(pace_drift),
        "reason": reason,
    }


def action_pace_alt_window_from_signals(
    *,
    action_pace_window: str,
    route_sandbox: str,
    sandbox_target: str,
    sandbox_readiness: str,
) -> tuple[str, dict[str, str | bool]]:
    """Prototype fallback window cue when CLOSE pace can still run via sandbox lane."""
    flag_name = "DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    window = str(action_pace_window).upper()
    sandbox = str(route_sandbox).upper()
    target = str(sandbox_target).upper()
    readiness = str(sandbox_readiness).upper()

    if not flag_enabled:
        alt_window = "FLAG OFF"
        reason = "flag-disabled"
    elif window != "CLOSE":
        alt_window = "PRIMARY OPEN"
        reason = "primary-window-not-closed"
    elif sandbox != "ON":
        alt_window = "WAIT SANDBOX"
        reason = "sandbox-not-armed"
    elif target in {"NONE", "MIXED"}:
        alt_window = "NO ALT LANE"
        reason = "sandbox-target-not-actionable"
    elif readiness == "ARMED":
        alt_window = f"PROBE {target}"
        reason = "closed-primary-with-armed-sandbox-lane"
    elif readiness == "PRIMED":
        alt_window = f"STAGE {target}"
        reason = "closed-primary-with-primed-sandbox-lane"
    else:
        alt_window = f"PREP {target}"
        reason = "closed-primary-with-idle-sandbox-lane"

    return alt_window, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "actionPaceWindow": window,
        "routeSandbox": sandbox,
        "sandboxTarget": target,
        "sandboxReadiness": readiness,
        "reason": reason,
    }


def action_pace_alt_window_confidence_from_signals(
    *,
    action_pace_alt_window: str,
    action_pace_alt_window_signals: dict[str, str | bool],
    action_pace_window_confidence: str,
) -> tuple[str, dict[str, str | bool]]:
    """Confidence for fallback pacing window suggestion when enabled."""
    alt_window = str(action_pace_alt_window).upper()
    base_conf = str(action_pace_window_confidence).upper()
    flag_enabled = bool(action_pace_alt_window_signals.get("flagEnabled", False))
    sandbox = str(action_pace_alt_window_signals.get("routeSandbox", "OFF")).upper()
    target = str(action_pace_alt_window_signals.get("sandboxTarget", "NONE")).upper()
    readiness = str(action_pace_alt_window_signals.get("sandboxReadiness", "IDLE")).upper()

    if not flag_enabled:
        confidence = "LOW"
        reason = "fallback-window-flag-disabled"
    elif alt_window.startswith("PROBE") and readiness == "ARMED" and target not in {"NONE", "MIXED"}:
        confidence = "HIGH"
        reason = "armed-actionable-sandbox-target"
    elif alt_window.startswith("STAGE") and sandbox == "ON" and target not in {"NONE", "MIXED"}:
        confidence = "MID"
        reason = "primed-sandbox-target-needs-staging"
    elif alt_window in {"WAIT SANDBOX", "NO ALT LANE"}:
        confidence = "LOW"
        reason = "fallback-not-actionable"
    elif base_conf == "LOW":
        confidence = "LOW"
        reason = "primary-window-confidence-low"
    else:
        confidence = "MID"
        reason = "default-fallback-confidence"

    return confidence, {
        "actionPaceAltWindow": alt_window,
        "actionPaceWindowConfidence": base_conf,
        "flagEnabled": flag_enabled,
        "routeSandbox": sandbox,
        "sandboxTarget": target,
        "sandboxReadiness": readiness,
        "reason": reason,
    }


def action_pace_alt_window_fit_from_signals(
    *,
    action_pace_alt_window: str,
    action_pace_alt_window_signals: dict[str, str | bool],
    pressure_band: str,
) -> tuple[str, dict[str, str | bool]]:
    """Pressure-aware fit guidance for fallback pacing lane behind experiment flag."""
    flag_name = "DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_FIT"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    alt_window = str(action_pace_alt_window).upper()
    pressure = str(pressure_band).upper()
    sandbox = str(action_pace_alt_window_signals.get("routeSandbox", "OFF")).upper()
    target = str(action_pace_alt_window_signals.get("sandboxTarget", "NONE")).upper()
    readiness = str(action_pace_alt_window_signals.get("sandboxReadiness", "IDLE")).upper()
    actionable = alt_window.startswith("PROBE") or alt_window.startswith("STAGE")

    if not flag_enabled:
        fit = "OFF"
        reason = "flag-disabled"
    elif alt_window in {"WAIT SANDBOX", "NO ALT LANE", "FLAG OFF"} or target in {"NONE", "MIXED"}:
        fit = "TENSE" if pressure in {"MID", "HIGH"} else "EVEN"
        reason = "fallback-lane-not-actionable"
    elif actionable and pressure == "LOW":
        fit = "SAFE"
        reason = "actionable-fallback-under-low-pressure"
    elif actionable and pressure == "MID" and readiness == "ARMED":
        fit = "SAFE"
        reason = "armed-fallback-absorbs-mid-pressure"
    elif pressure == "HIGH" and readiness != "ARMED":
        fit = "TENSE"
        reason = "high-pressure-without-armed-fallback"
    elif pressure == "HIGH":
        fit = "EVEN"
        reason = "armed-fallback-mitigates-high-pressure"
    else:
        fit = "EVEN"
        reason = "default-fallback-fit"

    return fit, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "actionPaceAltWindow": alt_window,
        "routeSandbox": sandbox,
        "sandboxTarget": target,
        "sandboxReadiness": readiness,
        "pressureBand": pressure,
        "reason": reason,
    }


def action_pace_alt_window_why_from_signals(
    *,
    action_pace_alt_window: str,
    action_pace_alt_window_confidence: str,
    action_pace_alt_window_fit: str,
    action_pace_alt_window_signals: dict[str, str | bool],
) -> tuple[str, dict[str, str | bool]]:
    """Prototype compact rationale token for fallback pacing handoff."""
    flag_name = "DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_WHY"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    alt_window = str(action_pace_alt_window).upper()
    confidence = str(action_pace_alt_window_confidence).upper()
    fit = str(action_pace_alt_window_fit).upper()
    target = str(action_pace_alt_window_signals.get("sandboxTarget", "NONE")).upper()
    readiness = str(action_pace_alt_window_signals.get("sandboxReadiness", "IDLE")).upper()
    sandbox = str(action_pace_alt_window_signals.get("routeSandbox", "OFF")).upper()

    if not flag_enabled:
        why = "FLAG OFF"
        reason = "flag-disabled"
    elif alt_window == "FLAG OFF":
        why = "ALT FLAG OFF"
        reason = "alt-window-flag-disabled"
    elif alt_window == "PRIMARY OPEN":
        why = "PRIMARY HOLD"
        reason = "primary-window-still-actionable"
    elif alt_window == "WAIT SANDBOX":
        why = "ARM SANDBOX"
        reason = "sandbox-not-armed"
    elif alt_window == "NO ALT LANE":
        why = "PICK ALT LANE"
        reason = "sandbox-target-not-actionable"
    elif fit == "SAFE" and confidence == "HIGH" and alt_window.startswith("PROBE"):
        why = "PROBE NOW"
        reason = "high-confidence-safe-probe"
    elif fit == "SAFE" and alt_window.startswith("STAGE"):
        why = "STAGE THEN GO"
        reason = "safe-fit-with-primed-lane"
    elif fit == "TENSE" and confidence == "LOW":
        why = "HOLD FALLBACK"
        reason = "tense-fit-low-confidence"
    elif fit == "TENSE" and readiness != "ARMED":
        why = "WAIT ARM"
        reason = "tense-fit-without-armed-readiness"
    elif fit == "EVEN" and target in {"ALT", "PRESSURE", "PORTAL"}:
        why = f"PROBE {target}"
        reason = "even-fit-actionable-lane"
    else:
        why = "WATCH ALT"
        reason = "default-fallback-watch"

    return why, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "actionPaceAltWindow": alt_window,
        "actionPaceAltWindowConfidence": confidence,
        "actionPaceAltWindowFit": fit,
        "routeSandbox": sandbox,
        "sandboxTarget": target,
        "sandboxReadiness": readiness,
        "reason": reason,
    }


def action_pace_alt_window_urgency_from_signals(
    *,
    action_pace_alt_window: str,
    action_pace_alt_window_confidence: str,
    action_pace_alt_window_fit: str,
    action_pace_alt_window_why: str,
) -> tuple[str, dict[str, str | bool]]:
    """Prototype urgency band for fallback pacing handoff."""
    flag_name = "DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_URGENCY"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    alt_window = str(action_pace_alt_window).upper()
    confidence = str(action_pace_alt_window_confidence).upper()
    fit = str(action_pace_alt_window_fit).upper()
    why = str(action_pace_alt_window_why).upper()

    if not flag_enabled:
        urgency = "OFF"
        reason = "flag-disabled"
    elif alt_window in {"WAIT SANDBOX", "NO ALT LANE", "FLAG OFF"} or why in {"ARM SANDBOX", "PICK ALT LANE", "ALT FLAG OFF"}:
        urgency = "LATER"
        reason = "fallback-not-actionable-yet"
    elif fit == "SAFE" and confidence == "HIGH" and (alt_window.startswith("PROBE") or why == "PROBE NOW"):
        urgency = "NOW"
        reason = "high-confidence-safe-probe-window"
    elif fit == "SAFE" and confidence in {"MID", "HIGH"}:
        urgency = "SOON"
        reason = "safe-fit-needs-short-staging"
    elif fit == "EVEN" and confidence == "HIGH":
        urgency = "SOON"
        reason = "balanced-fit-with-strong-confidence"
    elif fit == "TENSE":
        urgency = "LATER"
        reason = "tense-fit-defers-action"
    else:
        urgency = "SOON"
        reason = "default-moderate-urgency"

    return urgency, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "actionPaceAltWindow": alt_window,
        "actionPaceAltWindowConfidence": confidence,
        "actionPaceAltWindowFit": fit,
        "actionPaceAltWindowWhy": why,
        "reason": reason,
    }


def action_pace_alt_window_urgency_drift_from_prior(
    *,
    current_action_pace_alt_window_urgency: str,
    prior_json_path: Path,
) -> tuple[int, dict[str, str | int | bool]]:
    """Compare current/prior fallback urgency band and emit signed drift delta."""
    urgency_scores = {"OFF": 0, "LATER": 1, "SOON": 2, "NOW": 3}

    current_urgency = str(current_action_pace_alt_window_urgency).upper()
    current_score = urgency_scores.get(current_urgency, 0)
    prior_urgency = "OFF"
    prior_score = urgency_scores[prior_urgency]
    prior_loaded = False

    if prior_json_path.is_file():
        try:
            prior = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_urgency = str(prior.get("actionPaceAltWindowUrgency", prior_urgency)).upper()
            prior_score = urgency_scores.get(prior_urgency, 0)
            prior_loaded = True
        except (json.JSONDecodeError, OSError, ValueError):
            prior_loaded = False

    drift = current_score - prior_score

    if not prior_loaded:
        drift = 0
        reason = "no-prior-urgency-band"
    elif drift > 0:
        reason = "urgency-escalated"
    elif drift < 0:
        reason = "urgency-deescalated"
    else:
        reason = "urgency-stable"

    return drift, {
        "currentUrgency": current_urgency,
        "currentScore": current_score,
        "priorUrgency": prior_urgency,
        "priorScore": prior_score,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def action_pace_alt_window_step_from_signals(
    *,
    action_pace_alt_window: str,
    action_pace_alt_window_confidence: str,
    action_pace_alt_window_fit: str,
    action_pace_alt_window_urgency: str,
    action_pace_alt_window_signals: dict[str, str | bool],
) -> tuple[str, dict[str, str | bool]]:
    """Prototype compact one-action fallback step token for operator nudges."""
    flag_name = "DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_STEP"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    alt_window = str(action_pace_alt_window).upper()
    confidence = str(action_pace_alt_window_confidence).upper()
    fit = str(action_pace_alt_window_fit).upper()
    urgency = str(action_pace_alt_window_urgency).upper()
    target = str(action_pace_alt_window_signals.get("sandboxTarget", "NONE")).upper()
    readiness = str(action_pace_alt_window_signals.get("sandboxReadiness", "IDLE")).upper()
    sandbox = str(action_pace_alt_window_signals.get("routeSandbox", "OFF")).upper()

    if not flag_enabled:
        step = "FLAG OFF"
        reason = "flag-disabled"
    elif alt_window == "FLAG OFF":
        step = "ENABLE"
        reason = "alt-window-flag-disabled"
    elif alt_window == "PRIMARY OPEN":
        step = "HOLD"
        reason = "primary-window-still-open"
    elif sandbox != "ON" or alt_window == "WAIT SANDBOX":
        step = "ARM"
        reason = "sandbox-not-armed"
    elif target in {"NONE", "MIXED"} or alt_window == "NO ALT LANE":
        step = "PICK"
        reason = "sandbox-target-not-actionable"
    elif urgency == "NOW" and fit == "SAFE" and confidence in {"MID", "HIGH"}:
        step = "PROBE"
        reason = "safe-immediate-probe-window"
    elif urgency in {"SOON", "NOW"} and readiness == "PRIMED":
        step = "STAGE"
        reason = "primed-lane-needs-staging"
    elif fit == "TENSE" or urgency == "LATER":
        step = "WAIT"
        reason = "fallback-temporarily-tense"
    elif target == "PRESSURE":
        step = "SHED"
        reason = "pressure-target-guidance"
    elif target == "PORTAL":
        step = "SHIFT"
        reason = "portal-target-guidance"
    elif target == "ALT":
        step = "PROBE"
        reason = "alternate-lane-probe-guidance"
    else:
        step = "WATCH"
        reason = "default-fallback-observe"

    return step, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "actionPaceAltWindow": alt_window,
        "actionPaceAltWindowConfidence": confidence,
        "actionPaceAltWindowFit": fit,
        "actionPaceAltWindowUrgency": urgency,
        "routeSandbox": sandbox,
        "sandboxTarget": target,
        "sandboxReadiness": readiness,
        "reason": reason,
    }


def action_pace_alt_window_step_drift_from_prior(
    *,
    current_action_pace_alt_window_step: str,
    prior_json_path: Path,
) -> tuple[int, dict[str, str | int | bool]]:
    """Compare current/prior fallback step token and emit signed drift delta."""
    step_scores = {
        "FLAG OFF": 0,
        "ENABLE": 1,
        "HOLD": 2,
        "WATCH": 3,
        "ARM": 4,
        "PICK": 5,
        "WAIT": 6,
        "STAGE": 7,
        "SHIFT": 8,
        "SHED": 9,
        "PROBE": 10,
    }

    current_step = str(current_action_pace_alt_window_step).upper()
    current_score = step_scores.get(current_step, 0)
    prior_step = "FLAG OFF"
    prior_score = step_scores[prior_step]
    prior_loaded = False

    if prior_json_path.is_file():
        try:
            prior = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_step = str(prior.get("actionPaceAltWindowStep", prior_step)).upper()
            prior_score = step_scores.get(prior_step, 0)
            prior_loaded = True
        except (json.JSONDecodeError, OSError, ValueError):
            prior_loaded = False

    drift = current_score - prior_score

    if not prior_loaded:
        drift = 0
        reason = "no-prior-step-token"
    elif drift > 0:
        reason = "step-escalated"
    elif drift < 0:
        reason = "step-deescalated"
    else:
        reason = "step-stable"

    return drift, {
        "currentStep": current_step,
        "currentScore": current_score,
        "priorStep": prior_step,
        "priorScore": prior_score,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }



def action_pace_alt_window_step_glyph_from_signals(
    *,
    action_pace_alt_window_step: str,
    action_pace_alt_window_urgency: str,
    action_pace_alt_window_fit: str,
) -> tuple[str, dict[str, str | bool]]:
    """Design-facing compact glyph companion for fallback step token."""
    flag_name = "DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_STEP_GLYPH"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    step = str(action_pace_alt_window_step).upper()
    urgency = str(action_pace_alt_window_urgency).upper()
    fit = str(action_pace_alt_window_fit).upper()

    if not flag_enabled:
        glyph = "OFF"
        reason = "flag-disabled"
    elif step in {"FLAG OFF", "ENABLE"}:
        glyph = "○"
        reason = "step-flag-disabled"
    elif step == "ARM":
        glyph = "◌"
        reason = "arm-sandbox-first"
    elif step in {"PROBE", "SHIFT", "SHED"} and urgency == "NOW" and fit == "SAFE":
        glyph = "✦"
        reason = "immediate-safe-action"
    elif step in {"STAGE", "PICK"} and urgency in {"SOON", "NOW"}:
        glyph = "◈"
        reason = "prepare-near-term-action"
    elif step in {"WAIT", "WATCH", "HOLD"} or fit == "TENSE" or urgency == "LATER":
        glyph = "◇"
        reason = "hold-pattern-guidance"
    else:
        glyph = "·"
        reason = "default-neutral-glyph"

    return glyph, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "actionPaceAltWindowStep": step,
        "actionPaceAltWindowUrgency": urgency,
        "actionPaceAltWindowFit": fit,
        "reason": reason,
    }


def action_pace_alt_window_pulse_from_signals(
    *,
    action_pace_alt_window_urgency: str,
    action_pace_alt_window_fit: str,
    action_pace_alt_window_confidence: str,
) -> tuple[str, dict[str, str | bool]]:
    """Combat/VFX pressure pulse readability token for fallback cadence guidance."""
    flag_name = "DOTPIO_EXPERIMENT_ACTION_PACE_ALT_WINDOW_PULSE"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    urgency = str(action_pace_alt_window_urgency).upper()
    fit = str(action_pace_alt_window_fit).upper()
    confidence = str(action_pace_alt_window_confidence).upper()

    if not flag_enabled:
        pulse = "OFF"
        reason = "flag-disabled"
    elif fit == "TENSE" or urgency == "LATER":
        pulse = "HOT"
        reason = "tense-or-deferred-fallback-window"
    elif urgency == "NOW" and fit == "SAFE" and confidence in {"MID", "HIGH"}:
        pulse = "LIVE"
        reason = "safe-immediate-fallback-window"
    else:
        pulse = "COOL"
        reason = "non-urgent-fallback-window"

    return pulse, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "actionPaceAltWindowUrgency": urgency,
        "actionPaceAltWindowFit": fit,
        "actionPaceAltWindowConfidence": confidence,
        "reason": reason,
    }

def action_pace_alt_window_pulse_drift_from_prior(
    *,
    current_action_pace_alt_window_pulse: str,
    prior_json_path: Path,
) -> tuple[int, dict[str, str | int | bool]]:
    """Compare current/prior pulse band and emit signed drift delta."""
    pulse_scores = {"OFF": 0, "COOL": 1, "LIVE": 2, "HOT": 3}

    current_pulse = str(current_action_pace_alt_window_pulse).upper()
    current_score = pulse_scores.get(current_pulse, 0)
    prior_pulse = "OFF"
    prior_score = pulse_scores[prior_pulse]
    prior_loaded = False

    if prior_json_path.is_file():
        try:
            prior = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_pulse = str(prior.get("actionPaceAltWindowPulse", prior_pulse)).upper()
            prior_score = pulse_scores.get(prior_pulse, 0)
            prior_loaded = True
        except (json.JSONDecodeError, OSError, ValueError):
            prior_loaded = False

    drift = current_score - prior_score

    if not prior_loaded:
        drift = 0
        reason = "no-prior-pulse-band"
    elif drift > 0:
        reason = "pulse-escalated"
    elif drift < 0:
        reason = "pulse-deescalated"
    else:
        reason = "pulse-stable"

    return drift, {
        "currentPulse": current_pulse,
        "currentScore": current_score,
        "priorPulse": prior_pulse,
        "priorScore": prior_score,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def route_pulse_link_from_signals(
    *,
    action_pace_alt_window_pulse: str,
    action_pace_alt_window_pulse_drift: int,
    action_pace_alt_window_fit: str,
) -> tuple[str, dict[str, str | int | bool]]:
    """Design/World bridge token to align portal handoff sharpness with fallback pulse cadence."""
    flag_name = "DOTPIO_EXPERIMENT_ROUTE_PULSE_LINK"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    pulse = str(action_pace_alt_window_pulse).upper()
    fit = str(action_pace_alt_window_fit).upper()
    drift = int(action_pace_alt_window_pulse_drift)

    if not flag_enabled:
        link = "OFF"
        reason = "flag-disabled"
    elif pulse == "HOT" or drift > 0 or fit == "TENSE":
        link = "SHARP"
        reason = "escalating-or-tense-pulse-context"
    else:
        link = "SOFT"
        reason = "steady-or-cooling-pulse-context"

    return link, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "actionPaceAltWindowPulse": pulse,
        "actionPaceAltWindowPulseDrift": drift,
        "actionPaceAltWindowFit": fit,
        "reason": reason,
    }


def route_pulse_link_confidence_from_signals(
    *,
    route_pulse_link: str,
    route_pulse_link_signals: dict[str, str | int | bool],
    action_pace_alt_window_confidence: str,
) -> tuple[str, dict[str, str | int | bool]]:
    """Trust score for pulse-aware portal handoff cue readability."""
    link = str(route_pulse_link).upper()
    pulse = str(route_pulse_link_signals.get("actionPaceAltWindowPulse", "OFF")).upper()
    drift = int(route_pulse_link_signals.get("actionPaceAltWindowPulseDrift", 0))
    fit = str(route_pulse_link_signals.get("actionPaceAltWindowFit", "EVEN")).upper()
    alt_conf = str(action_pace_alt_window_confidence).upper()

    if link == "OFF":
        confidence = "LOW"
        reason = "link-disabled"
    elif link == "SHARP" and pulse == "HOT" and alt_conf in {"MID", "HIGH"}:
        confidence = "HIGH"
        reason = "sharp-link-backed-by-hot-pulse"
    elif link == "SHARP" and (drift > 0 or fit == "TENSE"):
        confidence = "MID"
        reason = "sharp-link-backed-by-escalation-signals"
    elif link == "SOFT" and drift <= 0 and fit in {"SAFE", "EVEN"}:
        confidence = "MID"
        reason = "soft-link-backed-by-stable-signals"
    else:
        confidence = "LOW"
        reason = "link-signals-inconclusive"

    return confidence, {
        "routePulseLink": link,
        "actionPaceAltWindowPulse": pulse,
        "actionPaceAltWindowPulseDrift": drift,
        "actionPaceAltWindowFit": fit,
        "actionPaceAltWindowConfidence": alt_conf,
        "reason": reason,
    }


def route_pulse_link_streak_from_prior(
    *,
    current_route_pulse_link: str,
    prior_json_path: Path,
) -> tuple[int, dict[str, str | int | bool]]:
    """Track consecutive non-OFF route pulse link windows for persistence triage."""
    current_link = str(current_route_pulse_link).upper()
    prior_link = "OFF"
    prior_streak = 0
    prior_loaded = False

    if prior_json_path.is_file():
        try:
            prior = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_link = str(prior.get("routePulseLink", prior_link)).upper()
            prior_streak = int(prior.get("routePulseLinkStreak", prior_streak))
            prior_loaded = True
        except (json.JSONDecodeError, OSError, ValueError, TypeError):
            prior_loaded = False

    if current_link == "OFF":
        streak = 0
        reason = "link-off-reset"
    elif prior_loaded and current_link == prior_link:
        streak = max(1, prior_streak) + 1
        reason = "link-persistence-extended"
    else:
        streak = 1
        reason = "new-link-cycle"

    return streak, {
        "currentRoutePulseLink": current_link,
        "priorRoutePulseLink": prior_link,
        "priorStreak": prior_streak,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def route_pulse_link_mode_from_signals(
    *,
    route_pulse_link: str,
    route_pulse_link_streak: int,
    action_pace_alt_window_pulse_drift: int,
) -> tuple[str, dict[str, str | int | bool]]:
    """Classify pulse-link persistence into an operator-facing intensity mode."""
    link = str(route_pulse_link).upper()
    streak = max(0, int(route_pulse_link_streak))
    drift = int(action_pace_alt_window_pulse_drift)

    if link == "OFF":
        mode = "IDLE"
        reason = "link-disabled"
    elif link == "SHARP" and (drift > 0 or streak >= 3):
        mode = "SURGE"
        reason = "sharp-link-escalating-or-persistent"
    elif streak >= 2:
        mode = "SUSTAIN"
        reason = "link-persistence-building"
    else:
        mode = "IDLE"
        reason = "new-link-cycle"

    return mode, {
        "routePulseLink": link,
        "routePulseLinkStreak": streak,
        "actionPaceAltWindowPulseDrift": drift,
        "reason": reason,
    }


def route_pulse_link_mode_drift_from_prior(
    *,
    current_route_pulse_link_mode: str,
    prior_json_path: Path,
) -> tuple[int, dict[str, str | int | bool]]:
    """Track route pulse-link mode drift against prior digest window."""
    score_map = {"IDLE": 0, "SUSTAIN": 1, "SURGE": 2}
    current_mode = str(current_route_pulse_link_mode).upper()
    current_score = score_map.get(current_mode, 0)

    prior_mode = "IDLE"
    prior_score = 0
    prior_loaded = False

    if prior_json_path.is_file():
        try:
            prior = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_mode = str(prior.get("routePulseLinkMode", prior_mode)).upper()
            prior_score = score_map.get(prior_mode, 0)
            prior_loaded = True
        except (json.JSONDecodeError, OSError, TypeError, ValueError):
            prior_loaded = False
            prior_mode = "IDLE"
            prior_score = 0

    drift = current_score - prior_score
    if drift > 0:
        reason = "mode-intensified"
    elif drift < 0:
        reason = "mode-deescalated"
    elif prior_loaded:
        reason = "mode-stable"
    else:
        reason = "no-prior-mode"

    return drift, {
        "currentMode": current_mode,
        "currentScore": current_score,
        "priorMode": prior_mode,
        "priorScore": prior_score,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def route_pulse_link_mode_stability_streak_from_prior(
    *,
    current_route_pulse_link_mode: str,
    prior_json_path: Path,
) -> tuple[int, dict[str, str | int | bool]]:
    """Track consecutive windows where route pulse-link mode remains unchanged."""
    current_mode = str(current_route_pulse_link_mode).upper()

    prior_mode = "IDLE"
    prior_streak = 0
    prior_loaded = False

    if prior_json_path.is_file():
        try:
            prior = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_mode = str(prior.get("routePulseLinkMode", prior_mode)).upper()
            prior_streak = int(prior.get("routePulseLinkModeStabilityStreak", prior_streak))
            prior_loaded = True
        except (json.JSONDecodeError, OSError, TypeError, ValueError):
            prior_loaded = False
            prior_mode = "IDLE"
            prior_streak = 0

    if prior_loaded and current_mode == prior_mode:
        streak = max(1, prior_streak) + 1
        reason = "mode-stable-extended"
    else:
        streak = 1
        reason = "mode-reset" if prior_loaded else "no-prior-mode"

    return streak, {
        "currentMode": current_mode,
        "priorMode": prior_mode,
        "priorStreak": prior_streak,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def route_pulse_link_mode_why_from_signals(
    *,
    route_pulse_link_mode: str,
    route_pulse_link_mode_signals: dict[str, str | int | bool],
    route_pulse_link_mode_drift: int,
) -> tuple[str, dict[str, str | int | bool]]:
    """Emit compact rationale token for route pulse-link mode triage."""
    flag_name = "DOTPIO_EXPERIMENT_ROUTE_PULSE_LINK_MODE_WHY"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    mode = str(route_pulse_link_mode).upper()
    link = str(route_pulse_link_mode_signals.get("routePulseLink", "OFF")).upper()
    streak = int(route_pulse_link_mode_signals.get("routePulseLinkStreak", 0) or 0)
    drift = int(route_pulse_link_mode_drift)

    if not flag_enabled:
        why = "FLAG OFF"
        reason = "flag-disabled"
    elif mode == "SURGE" and drift > 0:
        why = "SHARP BUILD"
        reason = "surge-intensifying"
    elif mode == "SURGE":
        why = "SURGE HOLD"
        reason = "surge-persistent"
    elif mode == "SUSTAIN" and streak >= 3:
        why = "STAY SHARP"
        reason = "sustain-persistent"
    elif mode == "SUSTAIN":
        why = "LINK WARM"
        reason = "sustain-building"
    elif mode == "IDLE" and drift < 0:
        why = "COOLING OFF"
        reason = "mode-deescalated"
    elif mode == "IDLE" and link == "OFF":
        why = "LINK QUIET"
        reason = "link-disabled"
    else:
        why = "IDLE WATCH"
        reason = "idle-monitor"

    return why, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "routePulseLinkMode": mode,
        "routePulseLink": link,
        "routePulseLinkModeDrift": drift,
        "routePulseLinkStreak": streak,
        "reason": reason,
    }


def route_pulse_link_mode_fit_from_signals(
    *,
    route_pulse_link_mode: str,
    route_pulse_link_mode_drift: int,
    route_pulse_link_mode_stability_streak: int,
) -> tuple[str, dict[str, str | int]]:
    """Classify how stable the pulse-link mode handoff currently is."""
    mode = str(route_pulse_link_mode).upper()
    drift = int(route_pulse_link_mode_drift)
    streak = max(0, int(route_pulse_link_mode_stability_streak))

    if mode == "SURGE" and drift > 0:
        fit = "BREAK"
        reason = "surge-intensifying"
    elif mode == "IDLE" and drift < 0:
        fit = "RESET"
        reason = "mode-deescalated"
    elif streak >= 3:
        fit = "SYNC"
        reason = "mode-stable-multi-window"
    else:
        fit = "WATCH"
        reason = "mode-transition-not-yet-stable"

    return fit, {
        "routePulseLinkMode": mode,
        "routePulseLinkModeDrift": drift,
        "routePulseLinkModeStabilityStreak": streak,
        "reason": reason,
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


def what_if_split_escalate_pressure_from_signals(
    *,
    what_if_split_esc_state: str,
    what_if_split_esc_cool: int,
    pressure_band: str,
) -> tuple[str, dict[str, str | int | bool]]:
    """Estimate cooldown risk pressure band for split-escalation lifecycle."""
    flag_name = "DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_PRESSURE"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    rank_map = {"LOW": 0, "MID": 1, "HIGH": 2}
    band_map = {0: "LOW", 1: "MID", 2: "HIGH"}
    base_rank = rank_map.get(pressure_band, 0)

    if not flag_enabled:
        pressure = "LOW"
        adjusted_rank = 0
        reason = "flag-disabled"
    elif what_if_split_esc_state == "ARMED":
        adjusted_rank = base_rank
        pressure = band_map[adjusted_rank]
        reason = "escalation-armed-uses-current-pressure-band"
    elif what_if_split_esc_state == "COOLING":
        decay = 2 if what_if_split_esc_cool >= 3 else 1
        adjusted_rank = max(0, base_rank - decay)
        pressure = band_map[adjusted_rank]
        reason = "escalation-cooling-relieves-pressure-band"
    else:
        adjusted_rank = max(0, base_rank - 2)
        pressure = band_map[adjusted_rank]
        reason = "escalation-idle-minimized-pressure-band"

    return pressure, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "splitEscState": what_if_split_esc_state,
        "splitEscCool": what_if_split_esc_cool,
        "pressureBand": pressure_band,
        "baseRank": base_rank,
        "adjustedRank": adjusted_rank,
        "reason": reason,
    }


def what_if_split_escalate_recover_from_signals(
    *,
    what_if_split_esc_state: str,
    what_if_split_escalate_lanes: str,
) -> tuple[str, dict[str, str | bool]]:
    """Suggest post-escalation recovery lane behind experiment flag."""
    flag_name = "DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    lane_rank = {"PORTAL": 0, "ALT": 1, "PRESSURE": 2}
    lanes = [part.strip().upper() for part in str(what_if_split_escalate_lanes).split("/") if part.strip()]
    actionable = [lane for lane in lanes if lane in lane_rank]

    if not flag_enabled:
        recover = "OFF"
        reason = "flag-disabled"
    elif what_if_split_esc_state == "ARMED":
        recover = "NONE"
        reason = "escalation-active-no-recovery-route"
    elif not actionable:
        recover = "NONE"
        reason = "no-actionable-escalation-lanes"
    else:
        recover = sorted(actionable, key=lambda lane: (lane_rank[lane], lane))[0]
        reason = "lowest-pressure-recovery-lane"

    return recover, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "splitEscState": what_if_split_esc_state,
        "splitEscLanes": what_if_split_escalate_lanes,
        "reason": reason,
    }


def what_if_split_escalate_recover_confidence_from_signals(
    *,
    what_if_split_esc_recover: str,
    what_if_split_esc_state: str,
    what_if_split_esc_pressure: str,
    what_if_split_escalate_lanes: str,
) -> tuple[str, dict[str, str | int | bool]]:
    """Rate confidence for post-escalation recovery suggestion."""
    lane_parts = [part.strip().upper() for part in str(what_if_split_escalate_lanes).split("/") if part.strip()]
    actionable_lanes = [lane for lane in lane_parts if lane in {"PORTAL", "ALT", "PRESSURE"}]
    lane_divergence = len(set(actionable_lanes)) >= 2
    lane_count = len(actionable_lanes)
    pressure_rank = {"LOW": 0, "MID": 1, "HIGH": 2}.get(what_if_split_esc_pressure, 0)
    easing = what_if_split_esc_state in {"COOLING", "IDLE"}

    if what_if_split_esc_recover in {"OFF", "NONE"}:
        confidence = "LOW"
        reason = "no-recovery-lane"
    elif not easing:
        confidence = "LOW"
        reason = "recovery-not-in-easing-state"
    elif lane_divergence and what_if_split_esc_pressure == "LOW":
        confidence = "HIGH"
        reason = "divergent-lanes-with-low-pressure-easing"
    elif lane_count >= 1 and pressure_rank <= 1:
        confidence = "MID"
        reason = "actionable-recover-lane-under-manageable-pressure"
    else:
        confidence = "LOW"
        reason = "high-pressure-or-ambiguous-lane-context"

    return confidence, {
        "splitEscRecover": what_if_split_esc_recover,
        "splitEscState": what_if_split_esc_state,
        "splitEscPressure": what_if_split_esc_pressure,
        "splitEscLanes": what_if_split_escalate_lanes,
        "laneDivergence": lane_divergence,
        "laneCount": lane_count,
        "pressureRank": pressure_rank,
        "stateEasing": easing,
        "reason": reason,
    }


def what_if_split_escalate_recover_alt_from_signals(
    *,
    what_if_split_esc_recover: str,
    what_if_split_esc_state: str,
    what_if_split_escalate_lanes: str,
) -> tuple[str, dict[str, str | bool]]:
    """Suggest contingency recovery lane different from primary recover lane."""
    flag_name = "DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_ALT"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    lane_priority = ["PORTAL", "ALT", "PRESSURE"]
    lane_rank = {lane: idx for idx, lane in enumerate(lane_priority)}
    lanes = [part.strip().upper() for part in str(what_if_split_escalate_lanes).split("/") if part.strip()]
    actionable = sorted({lane for lane in lanes if lane in lane_rank}, key=lambda lane: lane_rank[lane])

    if not flag_enabled:
        recover_alt = "OFF"
        reason = "flag-disabled"
    elif what_if_split_esc_state == "ARMED":
        recover_alt = "NONE"
        reason = "escalation-active-no-recovery-fallback"
    elif what_if_split_esc_recover in {"OFF", "NONE"}:
        recover_alt = "NONE"
        reason = "no-primary-recovery-lane"
    else:
        alternatives = [lane for lane in actionable if lane != what_if_split_esc_recover]
        if alternatives:
            recover_alt = alternatives[0]
            reason = "secondary-lowest-pressure-recovery-lane"
        else:
            recover_alt = "NONE"
            reason = "no-secondary-recovery-lane"

    return recover_alt, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "splitEscRecover": what_if_split_esc_recover,
        "splitEscState": what_if_split_esc_state,
        "splitEscLanes": what_if_split_escalate_lanes,
        "reason": reason,
    }


def what_if_split_escalate_recover_alt_confidence_from_signals(
    *,
    what_if_split_esc_recover_alt: str,
    what_if_split_esc_state: str,
    what_if_split_esc_pressure: str,
    what_if_split_escalate_lanes: str,
) -> tuple[str, dict[str, str | int | bool]]:
    """Rate confidence for contingency recovery lane suggestion."""
    lane_parts = [part.strip().upper() for part in str(what_if_split_escalate_lanes).split("/") if part.strip()]
    actionable_lanes = [lane for lane in lane_parts if lane in {"PORTAL", "ALT", "PRESSURE"}]
    lane_divergence = len(set(actionable_lanes)) >= 2
    lane_count = len(actionable_lanes)
    pressure_rank = {"LOW": 0, "MID": 1, "HIGH": 2}.get(what_if_split_esc_pressure, 0)
    easing = what_if_split_esc_state in {"COOLING", "IDLE"}

    if what_if_split_esc_recover_alt in {"OFF", "NONE"}:
        confidence = "LOW"
        reason = "no-recovery-alt-lane"
    elif not easing:
        confidence = "LOW"
        reason = "recovery-alt-not-in-easing-state"
    elif lane_divergence and what_if_split_esc_pressure == "LOW":
        confidence = "HIGH"
        reason = "divergent-lanes-with-low-pressure-easing"
    elif lane_count >= 2 and pressure_rank <= 1:
        confidence = "MID"
        reason = "actionable-alt-lane-under-manageable-pressure"
    else:
        confidence = "LOW"
        reason = "high-pressure-or-ambiguous-alt-context"

    return confidence, {
        "splitEscRecoverAlt": what_if_split_esc_recover_alt,
        "splitEscState": what_if_split_esc_state,
        "splitEscPressure": what_if_split_esc_pressure,
        "splitEscLanes": what_if_split_escalate_lanes,
        "laneDivergence": lane_divergence,
        "laneCount": lane_count,
        "pressureRank": pressure_rank,
        "stateEasing": easing,
        "reason": reason,
    }


def what_if_split_escalate_recover_plan_from_signals(
    *,
    what_if_split_esc_recover: str,
    what_if_split_esc_recover_alt: str,
) -> tuple[str, dict[str, str | bool]]:
    """Choose recovery route decision token from primary/alt lane availability."""
    has_primary = what_if_split_esc_recover not in {"OFF", "NONE"}
    has_alt = what_if_split_esc_recover_alt not in {"OFF", "NONE"}

    if has_primary:
        plan = "PRIMARY"
        reason = "primary-recovery-lane-available"
    elif has_alt:
        plan = "ALT"
        reason = "fallback-alt-recovery-lane-available"
    else:
        plan = "HOLD"
        reason = "no-actionable-recovery-lanes"

    return plan, {
        "splitEscRecover": what_if_split_esc_recover,
        "splitEscRecoverAlt": what_if_split_esc_recover_alt,
        "hasPrimary": has_primary,
        "hasAlt": has_alt,
        "reason": reason,
    }


def what_if_split_escalate_recover_why_from_signals(
    *,
    what_if_split_esc_recover_plan: str,
    what_if_split_esc_recover_confidence: str,
    what_if_split_esc_pressure: str,
) -> tuple[str, dict[str, str | bool]]:
    """Provide short operator rationale for split-escalation recovery plan behind flag."""
    flag_name = "DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_WHY"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    if not flag_enabled:
        why = "FLAG OFF"
        reason = "flag-disabled"
    elif what_if_split_esc_recover_plan == "PRIMARY":
        if what_if_split_esc_recover_confidence == "HIGH" and what_if_split_esc_pressure == "LOW":
            why = "PRIMARY RELIEF"
            reason = "high-confidence-primary-lane-with-low-pressure"
        elif what_if_split_esc_pressure == "HIGH":
            why = "PRIMARY STABILIZE"
            reason = "primary-lane-selected-while-pressure-high"
        else:
            why = "PRIMARY STEADY"
            reason = "primary-lane-available-with-manageable-pressure"
    elif what_if_split_esc_recover_plan == "ALT":
        if what_if_split_esc_recover_confidence in {"MID", "HIGH"} and what_if_split_esc_pressure != "HIGH":
            why = "ALT SAFETY NET"
            reason = "alt-lane-available-with-manageable-pressure"
        else:
            why = "ALT CONTINGENCY"
            reason = "alt-lane-used-under-uncertain-or-high-pressure-context"
    else:
        why = "HOLD FOR SIGNAL"
        reason = "no-actionable-recovery-lane"

    return why, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "splitEscRecoverPlan": what_if_split_esc_recover_plan,
        "splitEscRecoverConfidence": what_if_split_esc_recover_confidence,
        "splitEscPressure": what_if_split_esc_pressure,
        "reason": reason,
    }


def what_if_split_escalate_recover_tempo_from_signals(
    *,
    what_if_split_esc_recover_plan: str,
    what_if_split_esc_recover_confidence: str,
    what_if_split_esc_pressure: str,
) -> tuple[str, dict[str, str]]:
    """Recommend operator execution tempo for split-escalation recovery plan."""
    if what_if_split_esc_recover_plan == "HOLD":
        tempo = "DEFER"
        reason = "no-actionable-recovery-plan"
    elif what_if_split_esc_recover_confidence == "HIGH" and what_if_split_esc_pressure == "LOW":
        tempo = "FAST"
        reason = "high-confidence-low-pressure-recovery"
    elif what_if_split_esc_pressure == "HIGH":
        tempo = "STEADY"
        reason = "high-pressure-needs-controlled-recovery"
    elif what_if_split_esc_recover_confidence == "LOW":
        tempo = "STEADY"
        reason = "low-confidence-needs-confirmation-pass"
    else:
        tempo = "STEADY"
        reason = "default-controlled-recovery"

    return tempo, {
        "splitEscRecoverPlan": what_if_split_esc_recover_plan,
        "splitEscRecoverConfidence": what_if_split_esc_recover_confidence,
        "splitEscPressure": what_if_split_esc_pressure,
        "reason": reason,
    }


def what_if_split_escalate_recover_veto_from_signals(
    *,
    what_if_split_esc_recover_confidence: str,
    what_if_split_esc_pressure: str,
    what_if_split_esc_recover_plan: str,
) -> tuple[str, dict[str, str | bool]]:
    """Emit flagged veto sentinel when recovery context is still unsafe."""
    flag_name = "DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    confidence_low = str(what_if_split_esc_recover_confidence).upper() == "LOW"
    pressure_high = str(what_if_split_esc_pressure).upper() == "HIGH"
    plan_actionable = str(what_if_split_esc_recover_plan).upper() in {"PRIMARY", "ALT"}

    if not flag_enabled:
        veto = "OFF"
        reason = "flag-disabled"
    elif confidence_low and pressure_high and plan_actionable:
        veto = "ON"
        reason = "low-confidence-under-high-pressure-with-actionable-plan"
    elif confidence_low and pressure_high:
        veto = "OFF"
        reason = "low-confidence-high-pressure-but-no-actionable-plan"
    else:
        veto = "OFF"
        reason = "confidence-or-pressure-not-in-veto-band"

    return veto, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "splitEscRecoverConfidence": str(what_if_split_esc_recover_confidence).upper(),
        "splitEscPressure": str(what_if_split_esc_pressure).upper(),
        "splitEscRecoverPlan": str(what_if_split_esc_recover_plan).upper(),
        "confidenceLow": confidence_low,
        "pressureHigh": pressure_high,
        "planActionable": plan_actionable,
        "reason": reason,
    }


def what_if_split_escalate_recover_veto_confidence_from_signals(
    *,
    what_if_split_esc_recover_veto: str,
    what_if_split_esc_recover_confidence: str,
    what_if_split_esc_pressure: str,
    what_if_split_esc_recover_plan: str,
) -> tuple[str, dict[str, str | bool]]:
    """Score trust level for split-escalation recovery veto recommendation."""
    veto_on = str(what_if_split_esc_recover_veto).upper() == "ON"
    confidence_low = str(what_if_split_esc_recover_confidence).upper() == "LOW"
    pressure_high = str(what_if_split_esc_pressure).upper() == "HIGH"
    plan_actionable = str(what_if_split_esc_recover_plan).upper() in {"PRIMARY", "ALT"}

    if veto_on and confidence_low and pressure_high and plan_actionable:
        token = "HIGH"
        reason = "all-veto-guard-signals-aligned"
    elif confidence_low and pressure_high:
        token = "MID"
        reason = "pressure-and-confidence-trigger-with-plan-gap"
    else:
        token = "LOW"
        reason = "veto-conditions-not-sustained"

    return token, {
        "splitEscRecoverVeto": str(what_if_split_esc_recover_veto).upper(),
        "splitEscRecoverConfidence": str(what_if_split_esc_recover_confidence).upper(),
        "splitEscPressure": str(what_if_split_esc_pressure).upper(),
        "splitEscRecoverPlan": str(what_if_split_esc_recover_plan).upper(),
        "confidenceLow": confidence_low,
        "pressureHigh": pressure_high,
        "planActionable": plan_actionable,
        "vetoOn": veto_on,
        "reason": reason,
    }


def what_if_split_escalate_recover_veto_why_from_signals(
    *,
    what_if_split_esc_recover_veto: str,
    what_if_split_esc_recover_veto_confidence: str,
    what_if_split_esc_pressure: str,
    what_if_split_esc_recover_plan: str,
) -> tuple[str, dict[str, str | bool]]:
    """Emit compact rationale token when veto sentinel is active (flagged)."""
    flag_name = "DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_WHY"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    veto_on = str(what_if_split_esc_recover_veto).upper() == "ON"
    veto_conf = str(what_if_split_esc_recover_veto_confidence).upper()
    pressure = str(what_if_split_esc_pressure).upper()
    plan = str(what_if_split_esc_recover_plan).upper()

    if not flag_enabled:
        token = "FLAG OFF"
        reason = "flag-disabled"
    elif not veto_on:
        token = "NO VETO"
        reason = "veto-not-armed"
    elif veto_conf == "HIGH" and pressure == "HIGH" and plan in {"PRIMARY", "ALT"}:
        token = "HIGH PRESSURE LOCK"
        reason = "veto-armed-under-high-pressure-actionable-plan"
    elif veto_conf in {"HIGH", "MID"}:
        token = "GUARD RISK"
        reason = "veto-armed-with-mid-high-confidence"
    else:
        token = "WATCH SIGNAL"
        reason = "veto-armed-with-low-confidence-context"

    return token, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "splitEscRecoverVeto": str(what_if_split_esc_recover_veto).upper(),
        "splitEscRecoverVetoConfidence": veto_conf,
        "splitEscPressure": pressure,
        "splitEscRecoverPlan": plan,
        "reason": reason,
    }


def what_if_split_escalate_recover_veto_cooloff_from_prior(
    *,
    current_split_esc_recover_veto: str,
    prior_json_path: Path,
) -> tuple[int, dict[str, str | int | bool]]:
    """Track cooldown windows after veto sentinel disarms (flagged experiment)."""
    flag_name = "DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_COOLOFF"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    current_veto = str(current_split_esc_recover_veto).upper()
    prior_veto = "OFF"
    prior_cooloff = 0
    prior_loaded = False

    if prior_json_path.is_file():
        try:
            prior = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_veto = str(prior.get("whatIfSplitEscRecoverVeto", prior_veto)).upper()
            prior_cooloff = int(prior.get("whatIfSplitEscRecoverVetoCooloff", 0))
            prior_loaded = True
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    if not flag_enabled:
        cooloff = 0
        active = False
        reason = "flag-disabled"
    elif current_veto == "ON":
        cooloff = 0
        active = False
        reason = "veto-currently-armed"
    elif prior_veto == "ON":
        cooloff = 1
        active = True
        reason = "veto-just-disarmed"
    elif prior_cooloff > 0:
        cooloff = prior_cooloff + 1
        active = True
        reason = "veto-remains-disarmed-in-cooloff-window"
    else:
        cooloff = 0
        active = False
        reason = "no-recent-veto-disarm"

    return cooloff, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "active": active,
        "currentVeto": current_veto,
        "priorVeto": prior_veto,
        "priorCooloff": prior_cooloff,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def what_if_split_escalate_recover_veto_state_from_signals(
    *,
    what_if_split_esc_recover_veto: str,
    what_if_split_esc_recover_veto_cooloff: int,
) -> tuple[str, dict[str, str | int | bool]]:
    """Classify veto lane state for quick triage (armed/cooling/idle)."""
    veto = str(what_if_split_esc_recover_veto).upper()
    cooloff = max(0, int(what_if_split_esc_recover_veto_cooloff))

    if veto == "ON":
        state = "ARMED"
        reason = "veto-sentinel-currently-armed"
    elif cooloff > 0:
        state = "COOLING"
        reason = "veto-disarmed-in-cooloff-window"
    else:
        state = "IDLE"
        reason = "no-active-veto-or-cooloff"

    return state, {
        "splitEscRecoverVeto": veto,
        "splitEscRecoverVetoCooloff": cooloff,
        "cooling": cooloff > 0,
        "reason": reason,
    }


def what_if_split_escalate_recover_veto_dwell_from_prior(
    *,
    current_split_esc_recover_veto_state: str,
    prior_json_path: Path,
) -> tuple[int, dict[str, str | int | bool]]:
    """Count consecutive ARMED windows for split-escalation recovery veto state."""
    current_state = str(current_split_esc_recover_veto_state).upper()
    prior_state = "IDLE"
    prior_dwell = 0
    prior_loaded = False

    if prior_json_path.is_file():
        try:
            prior = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_state = str(prior.get("whatIfSplitEscRecoverVetoState", prior_state)).upper()
            prior_dwell = max(0, int(prior.get("whatIfSplitEscRecoverVetoDwell", 0)))
            prior_loaded = True
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    if current_state == "ARMED":
        if prior_state == "ARMED" and prior_dwell > 0:
            dwell = prior_dwell + 1
            reason = "veto-remains-armed"
        else:
            dwell = 1
            reason = "veto-armed-new-streak"
    else:
        dwell = 0
        reason = "veto-not-armed"

    return dwell, {
        "currentState": current_state,
        "priorState": prior_state,
        "priorDwell": prior_dwell,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def what_if_split_escalate_recover_veto_release_from_prior(
    *,
    current_split_esc_recover_veto_state: str,
    prior_json_path: Path,
) -> tuple[str, dict[str, str | bool]]:
    """Emit flagged release cue token when veto state exits COOLING into IDLE."""
    flag_name = "DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_RELEASE"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    current_state = str(current_split_esc_recover_veto_state).upper()
    prior_state = "IDLE"
    prior_loaded = False

    if prior_json_path.is_file():
        try:
            prior = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_state = str(prior.get("whatIfSplitEscRecoverVetoState", prior_state)).upper()
            prior_loaded = True
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    if not flag_enabled:
        token = "FLAG OFF"
        reason = "flag-disabled"
    elif prior_state == "COOLING" and current_state == "IDLE":
        token = "COOLING CLEAR"
        reason = "veto-state-transitioned-cooling-to-idle"
    elif current_state == "COOLING":
        token = "COOLING"
        reason = "veto-state-still-cooling"
    elif current_state == "ARMED":
        token = "HOLD"
        reason = "veto-state-rearmed"
    else:
        token = "STABLE"
        reason = "no-cooling-to-idle-transition"

    return token, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "currentState": current_state,
        "priorState": prior_state,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def what_if_split_escalate_recover_veto_release_confidence_from_signals(
    *,
    what_if_split_esc_recover_veto_release: str,
    what_if_split_esc_recover_veto_state: str,
    what_if_split_esc_recover_veto_dwell: int,
) -> tuple[str, dict[str, str | int | bool]]:
    """Score trust for veto release cue readability token."""
    release = str(what_if_split_esc_recover_veto_release).upper()
    state = str(what_if_split_esc_recover_veto_state).upper()
    dwell = max(0, int(what_if_split_esc_recover_veto_dwell))

    if release == "COOLING CLEAR" and state == "IDLE":
        token = "HIGH"
        reason = "clean-cooling-to-idle-release-transition"
    elif release == "COOLING":
        token = "MID"
        reason = "release-pending-while-cooling"
    elif state == "ARMED" or dwell > 0:
        token = "LOW"
        reason = "release-not-trustworthy-during-armed-or-dwell"
    else:
        token = "LOW"
        reason = "no-release-transition-detected"

    return token, {
        "splitEscRecoverVetoRelease": release,
        "splitEscRecoverVetoState": state,
        "splitEscRecoverVetoDwell": dwell,
        "reason": reason,
    }


def what_if_split_escalate_recover_veto_release_route_from_signals(
    *,
    what_if_split_esc_recover_veto_release: str,
    what_if_split_esc_recover_veto_state: str,
    what_if_split_esc_recover: str,
    what_if_split_esc_recover_alt: str,
    what_if_split_esc_recover_plan: str,
) -> tuple[str, dict[str, str | bool]]:
    """Emit post-cooldown handoff route token for veto release transitions."""
    release = str(what_if_split_esc_recover_veto_release).upper()
    state = str(what_if_split_esc_recover_veto_state).upper()
    primary = str(what_if_split_esc_recover).upper()
    alt = str(what_if_split_esc_recover_alt).upper()
    plan = str(what_if_split_esc_recover_plan).upper()

    valid_lanes = {"PORTAL", "ALT", "PRESSURE"}
    primary_actionable = primary in valid_lanes
    alt_actionable = alt in valid_lanes

    if release == "COOLING CLEAR" and state == "IDLE":
        if plan == "PRIMARY" and primary_actionable:
            route = primary
            reason = "release-cleared-follow-primary-recovery-lane"
        elif plan == "ALT" and alt_actionable:
            route = alt
            reason = "release-cleared-follow-alt-recovery-lane"
        elif primary_actionable:
            route = primary
            reason = "release-cleared-fallback-primary-lane"
        elif alt_actionable:
            route = alt
            reason = "release-cleared-fallback-alt-lane"
        else:
            route = "NONE"
            reason = "release-cleared-no-actionable-lane"
    elif state == "COOLING":
        route = "HOLD"
        reason = "release-route-held-while-cooling"
    elif state == "ARMED":
        route = "HOLD"
        reason = "release-route-held-while-veto-armed"
    else:
        route = "NONE"
        reason = "no-release-route-available"

    return route, {
        "splitEscRecoverVetoRelease": release,
        "splitEscRecoverVetoState": state,
        "splitEscRecover": primary,
        "splitEscRecoverAlt": alt,
        "splitEscRecoverPlan": plan,
        "primaryActionable": primary_actionable,
        "altActionable": alt_actionable,
        "reason": reason,
    }


def what_if_split_escalate_recover_veto_release_tick_from_prior(
    *,
    current_split_esc_recover_veto_release: str,
    current_split_esc_recover_veto_state: str,
    prior_json_path: Path,
) -> tuple[int | str, dict[str, str | int | bool]]:
    """Count idle-window pacing ticks after veto release clears (flag-gated)."""
    flag_name = "DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_RELEASE_TICK"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    release = str(current_split_esc_recover_veto_release).upper()
    state = str(current_split_esc_recover_veto_state).upper()

    prior_loaded = False
    prior_tick = 0
    prior_state = "IDLE"
    prior_release = "STABLE"

    if prior_json_path.is_file():
        try:
            prior = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_tick_value = prior.get("whatIfSplitEscRecoverVetoReleaseTick", 0)
            if isinstance(prior_tick_value, int):
                prior_tick = max(0, prior_tick_value)
            prior_state = str(prior.get("whatIfSplitEscRecoverVetoState", prior_state)).upper()
            prior_release = str(prior.get("whatIfSplitEscRecoverVetoRelease", prior_release)).upper()
            prior_loaded = True
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    if not flag_enabled:
        tick: int | str = "FLAG OFF"
        reason = "flag-disabled"
    elif release == "COOLING CLEAR" and state == "IDLE":
        tick = 1
        reason = "release-cleared-idle-window-started"
    elif state == "IDLE" and prior_tick > 0:
        tick = prior_tick + 1
        reason = "release-idle-window-continuing"
    else:
        tick = 0
        reason = "no-active-release-idle-window"

    return tick, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "currentRelease": release,
        "currentState": state,
        "priorTick": prior_tick,
        "priorRelease": prior_release,
        "priorState": prior_state,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def what_if_split_escalate_recover_veto_release_tick_phase_from_signals(
    *,
    what_if_split_esc_recover_veto_release_tick: int | str,
) -> tuple[str, dict[str, str | int | bool]]:
    """Map veto release tick count to pacing phase labels."""
    if isinstance(what_if_split_esc_recover_veto_release_tick, str):
        token = what_if_split_esc_recover_veto_release_tick.upper()
        return token, {
            "tick": token,
            "reason": "non-numeric-tick-token-forwarded",
            "numeric": False,
        }

    tick = max(0, int(what_if_split_esc_recover_veto_release_tick))
    if tick == 0:
        phase = "IDLE"
        reason = "no-active-release-tick-window"
    elif tick <= 2:
        phase = "EARLY"
        reason = "release-window-just-opened"
    elif tick <= 4:
        phase = "MID"
        reason = "release-window-mid-pacing"
    else:
        phase = "LATE"
        reason = "release-window-late-pacing"

    return phase, {
        "tick": tick,
        "reason": reason,
        "numeric": True,
    }


def what_if_split_escalate_recover_veto_release_tick_cadence_from_signals(
    *,
    what_if_split_esc_recover_veto_release_tick: int | str,
    what_if_split_esc_recover_veto_release_tick_signals: dict[str, str | int | bool],
) -> tuple[str, dict[str, str | int | bool]]:
    """Classify release tick pacing cadence from current-vs-prior tick delta."""
    if isinstance(what_if_split_esc_recover_veto_release_tick, str):
        token = what_if_split_esc_recover_veto_release_tick.upper()
        return token, {
            "tick": token,
            "priorTick": int(what_if_split_esc_recover_veto_release_tick_signals.get("priorTick", 0) or 0),
            "delta": 0,
            "numeric": False,
            "reason": "non-numeric-tick-token-forwarded",
        }

    tick = max(0, int(what_if_split_esc_recover_veto_release_tick))
    prior_tick = max(0, int(what_if_split_esc_recover_veto_release_tick_signals.get("priorTick", 0) or 0))
    delta = tick - prior_tick

    if tick == 0:
        cadence = "STEADY"
        reason = "no-active-release-tick-window"
    elif delta >= 2:
        cadence = "ACCEL"
        reason = "tick-growth-jump-vs-prior-window"
    elif delta <= 0:
        cadence = "DECAY"
        reason = "tick-stalled-or-regressed-vs-prior-window"
    else:
        cadence = "STEADY"
        reason = "tick-growth-linear-vs-prior-window"

    return cadence, {
        "tick": tick,
        "priorTick": prior_tick,
        "delta": delta,
        "numeric": True,
        "reason": reason,
    }


def what_if_split_escalate_recover_veto_rearm_from_signals(
    *,
    what_if_split_esc_recover_veto_release_tick_phase: str,
    what_if_split_esc_pressure: str,
    what_if_split_esc_recover_veto_release_cadence: str,
) -> tuple[str, dict[str, str | bool]]:
    """Emit flagged auto-rearm watch cue when release pacing stays late under high pressure."""
    flag_name = "DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    phase = str(what_if_split_esc_recover_veto_release_tick_phase).upper()
    pressure = str(what_if_split_esc_pressure).upper()
    cadence = str(what_if_split_esc_recover_veto_release_cadence).upper()

    if not flag_enabled:
        token = "OFF"
        reason = "flag-disabled"
    elif phase != "LATE":
        token = "OFF"
        reason = "release-phase-not-late"
    elif pressure != "HIGH":
        token = "OFF"
        reason = "pressure-not-high"
    elif cadence in {"DECAY", "FLAG OFF"}:
        token = "OFF"
        reason = "release-cadence-not-rearm-prone"
    else:
        token = "WATCH"
        reason = "late-release-window-under-high-pressure"

    return token, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "releaseTickPhase": phase,
        "splitEscPressure": pressure,
        "releaseCadence": cadence,
        "reason": reason,
    }


def what_if_split_escalate_recover_veto_rearm_confidence_from_signals(
    *,
    what_if_split_esc_recover_veto_rearm: str,
    what_if_split_esc_recover_veto_rearm_signals: dict[str, str | bool],
) -> tuple[str, dict[str, str | bool]]:
    """Score trust for auto-rearm WATCH cue readability."""
    rearm = str(what_if_split_esc_recover_veto_rearm).upper()
    flag_enabled = bool(what_if_split_esc_recover_veto_rearm_signals.get("flagEnabled", False))
    phase = str(what_if_split_esc_recover_veto_rearm_signals.get("releaseTickPhase", "")).upper()
    pressure = str(what_if_split_esc_recover_veto_rearm_signals.get("splitEscPressure", "")).upper()
    cadence = str(what_if_split_esc_recover_veto_rearm_signals.get("releaseCadence", "")).upper()

    if not flag_enabled:
        confidence = "LOW"
        reason = "flag-disabled"
    elif rearm == "WATCH" and phase == "LATE" and pressure == "HIGH" and cadence == "STEADY":
        confidence = "HIGH"
        reason = "watch-cue-aligned-with-late-high-pressure-steady-cadence"
    elif rearm == "WATCH" and phase == "LATE" and pressure == "HIGH":
        confidence = "MID"
        reason = "watch-cue-active-but-cadence-non-steady"
    elif rearm == "OFF" and phase == "LATE" and pressure == "HIGH":
        confidence = "MID"
        reason = "watch-cue-suppressed-by-cadence-guard"
    else:
        confidence = "LOW"
        reason = "rearm-conditions-not-sustained"

    return confidence, {
        "splitEscRecoverVetoRearm": rearm,
        "flagEnabled": flag_enabled,
        "releaseTickPhase": phase,
        "splitEscPressure": pressure,
        "releaseCadence": cadence,
        "reason": reason,
    }


def what_if_split_escalate_recover_veto_rearm_why_from_signals(
    *,
    what_if_split_esc_recover_veto_rearm: str,
    what_if_split_esc_recover_veto_rearm_confidence: str,
    what_if_split_esc_pressure: str,
    what_if_split_esc_recover_veto_release_tick_phase: str,
) -> tuple[str, dict[str, str | bool]]:
    """Emit concise operator rationale token for auto-rearm WATCH cue behind flag."""
    flag_name = "DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_WHY"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    rearm = str(what_if_split_esc_recover_veto_rearm).upper()
    confidence = str(what_if_split_esc_recover_veto_rearm_confidence).upper()
    pressure = str(what_if_split_esc_pressure).upper()
    phase = str(what_if_split_esc_recover_veto_release_tick_phase).upper()

    if not flag_enabled:
        rationale = "FLAG OFF"
        reason = "flag-disabled"
    elif rearm != "WATCH":
        rationale = "NO WATCH CUE"
        reason = "rearm-watch-not-active"
    elif pressure == "HIGH" and confidence == "HIGH" and phase == "LATE":
        rationale = "HIGH PRESSURE REARM"
        reason = "watch-cue-confirmed-under-high-pressure"
    elif pressure == "HIGH" and confidence in {"MID", "HIGH"}:
        rationale = "PRESSURE STAY ALERT"
        reason = "watch-cue-active-with-elevated-pressure"
    elif confidence == "LOW":
        rationale = "LOW CONF HOLD"
        reason = "watch-cue-low-confidence-context"
    else:
        rationale = "WATCH WINDOW"
        reason = "watch-cue-active-default-rationale"

    return rationale, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "splitEscRecoverVetoRearm": rearm,
        "splitEscRecoverVetoRearmConfidence": confidence,
        "splitEscPressure": pressure,
        "releaseTickPhase": phase,
        "reason": reason,
    }




def what_if_split_escalate_recover_veto_rearm_cooloff_from_prior(
    *,
    current_split_esc_recover_veto_rearm: str,
    prior_json_path: Path,
) -> tuple[int, dict[str, str | int | bool]]:
    """Track OFF windows after WATCH cue disarms for rearm pacing follow-up (flag-gated)."""
    flag_name = "DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_COOLOFF"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    current_rearm = str(current_split_esc_recover_veto_rearm).upper()
    prior_rearm = "OFF"
    prior_cooloff = 0
    prior_loaded = False

    if prior_json_path.is_file():
        try:
            prior = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_rearm = str(prior.get("whatIfSplitEscRecoverVetoRearm", prior_rearm)).upper()
            prior_cooloff = max(0, int(prior.get("whatIfSplitEscRecoverVetoRearmCooloff", 0)))
            prior_loaded = True
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    if not flag_enabled:
        cooloff = 0
        active = False
        reason = "flag-disabled"
    elif current_rearm == "WATCH":
        cooloff = 0
        active = False
        reason = "rearm-watch-currently-armed"
    elif prior_rearm == "WATCH":
        cooloff = 1
        active = True
        reason = "rearm-watch-just-disarmed"
    elif prior_cooloff > 0:
        cooloff = prior_cooloff + 1
        active = True
        reason = "rearm-watch-remains-disarmed-in-cooloff-window"
    else:
        cooloff = 0
        active = False
        reason = "no-recent-rearm-watch-disarm"

    return cooloff, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "active": active,
        "currentRearm": current_rearm,
        "priorRearm": prior_rearm,
        "priorCooloff": prior_cooloff,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def what_if_split_escalate_recover_veto_rearm_cooloff_state_from_signals(
    *,
    what_if_split_esc_recover_veto_rearm: str,
    what_if_split_esc_recover_veto_rearm_cooloff: int,
) -> tuple[str, dict[str, str | int | bool]]:
    """Summarize rearm cooloff lifecycle into ACTIVE/IDLE for quick triage."""
    rearm = str(what_if_split_esc_recover_veto_rearm).upper()
    cooloff = max(0, int(what_if_split_esc_recover_veto_rearm_cooloff))

    if rearm == "WATCH" or cooloff > 0:
        state = "ACTIVE"
        reason = "watch-armed-or-cooloff-running"
    else:
        state = "IDLE"
        reason = "no-watch-and-no-cooloff"

    return state, {
        "splitEscRecoverVetoRearm": rearm,
        "splitEscRecoverVetoRearmCooloff": cooloff,
        "active": state == "ACTIVE",
        "reason": reason,
    }


def what_if_split_escalate_recover_veto_rearm_fit_from_signals(
    *,
    what_if_split_esc_recover_veto_rearm_cooloff_state: str,
    what_if_split_esc_recover_veto_rearm_cooloff: int,
    what_if_split_esc_pressure: str,
) -> tuple[str, dict[str, str | int | bool]]:
    """Classify pressure-relief fit during/after rearm cooloff windows."""
    state = str(what_if_split_esc_recover_veto_rearm_cooloff_state).upper()
    cooloff = max(0, int(what_if_split_esc_recover_veto_rearm_cooloff))
    pressure = str(what_if_split_esc_pressure).upper()

    if state == "ACTIVE" and pressure == "LOW":
        fit = "RELIEF"
        reason = "active-cooloff-with-low-pressure"
    elif state == "ACTIVE" and pressure == "MID":
        fit = "EVEN"
        reason = "active-cooloff-with-mid-pressure"
    elif state == "ACTIVE" and pressure == "HIGH":
        fit = "TENSE"
        reason = "active-cooloff-with-high-pressure"
    elif state == "IDLE" and cooloff == 0 and pressure == "LOW":
        fit = "RELIEF"
        reason = "idle-post-cooloff-low-pressure"
    elif pressure == "HIGH":
        fit = "TENSE"
        reason = "pressure-high-without-relief-window"
    else:
        fit = "EVEN"
        reason = "neutral-pressure-relief-balance"

    return fit, {
        "splitEscRecoverVetoRearmCooloffState": state,
        "splitEscRecoverVetoRearmCooloff": cooloff,
        "splitEscPressure": pressure,
        "reason": reason,
    }


def what_if_split_escalate_recover_veto_rearm_nudge_from_signals(
    *,
    what_if_split_esc_recover_veto_rearm: str,
    what_if_split_esc_recover_veto_rearm_confidence: str,
    what_if_split_esc_recover_veto_rearm_fit: str,
    what_if_split_esc_recover_veto_rearm_cooloff_state: str,
) -> tuple[str, dict[str, str | bool]]:
    """Emit a short operator nudge token for auto-rearm handoff when experiment flag is enabled."""
    flag_name = "DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_NUDGE"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    rearm = str(what_if_split_esc_recover_veto_rearm).upper()
    confidence = str(what_if_split_esc_recover_veto_rearm_confidence).upper()
    fit = str(what_if_split_esc_recover_veto_rearm_fit).upper()
    cooloff_state = str(what_if_split_esc_recover_veto_rearm_cooloff_state).upper()

    if not flag_enabled:
        nudge = "FLAG OFF"
        reason = "flag-disabled"
    elif rearm == "WATCH" and confidence == "HIGH" and fit == "TENSE":
        nudge = "HOLD DEFENSE"
        reason = "watch-armed-high-confidence-tense-fit"
    elif rearm == "WATCH" and confidence in {"MID", "HIGH"}:
        nudge = "STAY SHARP"
        reason = "watch-armed-with-actionable-confidence"
    elif cooloff_state == "ACTIVE" and fit == "RELIEF":
        nudge = "RESET READY"
        reason = "cooloff-active-with-relief-fit"
    elif cooloff_state == "ACTIVE" and fit == "EVEN":
        nudge = "PROBE CAREFUL"
        reason = "cooloff-active-with-even-fit"
    elif cooloff_state == "ACTIVE" and fit == "TENSE":
        nudge = "DELAY REARM"
        reason = "cooloff-active-with-tense-fit"
    else:
        nudge = "MONITOR LANE"
        reason = "idle-default-monitoring-state"

    return nudge, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "splitEscRecoverVetoRearm": rearm,
        "splitEscRecoverVetoRearmConfidence": confidence,
        "splitEscRecoverVetoRearmFit": fit,
        "splitEscRecoverVetoRearmCooloffState": cooloff_state,
        "reason": reason,
    }


def what_if_split_escalate_recover_veto_rearm_nudge_window_from_signals(
    *,
    what_if_split_esc_recover_veto_rearm: str,
    what_if_split_esc_recover_veto_rearm_cooloff_state: str,
) -> tuple[str, dict[str, str | bool]]:
    """Classify nudge timing window from rearm watch + cooloff-state context."""
    rearm = str(what_if_split_esc_recover_veto_rearm).upper()
    cooloff_state = str(what_if_split_esc_recover_veto_rearm_cooloff_state).upper()

    if rearm == "WATCH":
        window = "ARMED"
        reason = "watch-cue-active"
    elif cooloff_state == "ACTIVE":
        window = "COOLING"
        reason = "watch-disarmed-in-cooloff-window"
    else:
        window = "IDLE"
        reason = "no-watch-or-cooloff-window"

    return window, {
        "splitEscRecoverVetoRearm": rearm,
        "splitEscRecoverVetoRearmCooloffState": cooloff_state,
        "reason": reason,
    }


def what_if_split_escalate_recover_veto_rearm_nudge_confidence_from_signals(
    *,
    what_if_split_esc_recover_veto_rearm_nudge: str,
    what_if_split_esc_recover_veto_rearm_confidence: str,
    what_if_split_esc_recover_veto_rearm_fit: str,
) -> tuple[str, dict[str, str]]:
    """Classify trust level for rearm nudge token readability."""
    nudge = str(what_if_split_esc_recover_veto_rearm_nudge).upper()
    rearm_conf = str(what_if_split_esc_recover_veto_rearm_confidence).upper()
    fit = str(what_if_split_esc_recover_veto_rearm_fit).upper()

    if nudge == "FLAG OFF":
        confidence = "LOW"
        reason = "nudge-flag-disabled"
    elif nudge == "HOLD DEFENSE" and rearm_conf == "HIGH":
        confidence = "HIGH"
        reason = "high-urgency-nudge-backed-by-high-rearm-confidence"
    elif nudge in {"STAY SHARP", "DELAY REARM", "PROBE CAREFUL"} or rearm_conf == "MID":
        confidence = "MID"
        reason = "actionable-nudge-with-mid-confidence-context"
    elif nudge == "RESET READY" and fit == "RELIEF":
        confidence = "MID"
        reason = "recovery-nudge-under-relief-fit"
    else:
        confidence = "LOW"
        reason = "nudge-context-not-strong-enough"

    return confidence, {
        "splitEscRecoverVetoRearmNudge": nudge,
        "splitEscRecoverVetoRearmConfidence": rearm_conf,
        "splitEscRecoverVetoRearmFit": fit,
        "reason": reason,
    }


def what_if_split_escalate_recover_veto_rearm_nudge_why_from_signals(
    *,
    what_if_split_esc_recover_veto_rearm_nudge: str,
    what_if_split_esc_recover_veto_rearm_nudge_confidence: str,
    what_if_split_esc_recover_veto_rearm_nudge_window: str,
    what_if_split_esc_recover_veto_rearm_fit: str,
) -> tuple[str, dict[str, str | bool]]:
    """Emit concise rationale for auto-rearm nudge token when experiment flag is enabled."""
    flag_name = "DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_NUDGE_WHY"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    nudge = str(what_if_split_esc_recover_veto_rearm_nudge).upper()
    confidence = str(what_if_split_esc_recover_veto_rearm_nudge_confidence).upper()
    window = str(what_if_split_esc_recover_veto_rearm_nudge_window).upper()
    fit = str(what_if_split_esc_recover_veto_rearm_fit).upper()

    if not flag_enabled:
        rationale = "FLAG OFF"
        reason = "flag-disabled"
    elif nudge == "FLAG OFF":
        rationale = "NUDGE DISABLED"
        reason = "upstream-nudge-flag-disabled"
    elif nudge == "HOLD DEFENSE" and confidence == "HIGH":
        rationale = "PRESSURE HOLD"
        reason = "high-confidence-defensive-hold"
    elif window == "ARMED" and confidence in {"MID", "HIGH"}:
        rationale = "WATCH REARM"
        reason = "armed-window-with-actionable-confidence"
    elif window == "COOLING" and fit == "RELIEF":
        rationale = "RECOVER RESET"
        reason = "cooling-window-relief-fit"
    elif window == "COOLING":
        rationale = "COOLING CHECK"
        reason = "cooling-window-monitor-fit"
    else:
        rationale = "LANE MONITOR"
        reason = "idle-window-default-monitoring"

    return rationale, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "splitEscRecoverVetoRearmNudge": nudge,
        "splitEscRecoverVetoRearmNudgeConfidence": confidence,
        "splitEscRecoverVetoRearmNudgeWindow": window,
        "splitEscRecoverVetoRearmFit": fit,
        "reason": reason,
    }


def what_if_split_escalate_recover_veto_rearm_nudge_impact_from_signals(
    *,
    what_if_split_esc_recover_veto_rearm_nudge: str,
    what_if_split_esc_recover_veto_rearm_nudge_window: str,
    what_if_split_esc_recover_veto_rearm_fit: str,
) -> tuple[str, dict[str, str]]:
    """Compress nudge urgency into a compact impact band for operator pacing triage."""
    nudge = str(what_if_split_esc_recover_veto_rearm_nudge).upper()
    window = str(what_if_split_esc_recover_veto_rearm_nudge_window).upper()
    fit = str(what_if_split_esc_recover_veto_rearm_fit).upper()

    if nudge in {"HOLD DEFENSE", "DELAY REARM"} and window == "ARMED":
        impact = "DEFENSIVE"
        reason = "armed-window-with-high-guard-nudge"
    elif window == "COOLING" and fit in {"EVEN", "TENSE"}:
        impact = "DEFENSIVE"
        reason = "cooling-window-with-non-relief-fit"
    elif nudge in {"STAY SHARP", "PROBE CAREFUL", "RESET READY"}:
        impact = "CAUTIOUS"
        reason = "actionable-nudge-with-moderate-pressure"
    else:
        impact = "NEUTRAL"
        reason = "monitoring-or-flag-off-state"

    return impact, {
        "splitEscRecoverVetoRearmNudge": nudge,
        "splitEscRecoverVetoRearmNudgeWindow": window,
        "splitEscRecoverVetoRearmFit": fit,
        "reason": reason,
    }


def what_if_split_escalate_recover_veto_rearm_nudge_drift_from_prior(
    *,
    current_nudge_why: str,
    prior_json_path: Path,
) -> tuple[str, dict[str, str | bool]]:
    """Track whether nudge rationale changed versus prior digest window."""
    current = str(current_nudge_why).strip().upper() or "UNKNOWN"
    prior_loaded = False
    prior = current

    if prior_json_path.is_file():
        try:
            prior_payload = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior = str(prior_payload.get("whatIfSplitEscRecoverVetoRearmNudgeWhy", current)).strip().upper() or current
            prior_loaded = True
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    if current == prior:
        drift = "STABLE"
        reason = "nudge-rationale-unchanged-vs-prior-window"
    else:
        drift = "SHIFTING"
        reason = "nudge-rationale-changed-vs-prior-window"

    return drift, {
        "currentNudgeWhy": current,
        "priorNudgeWhy": prior,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def what_if_split_escalate_recover_veto_rearm_coach_from_signals(
    *,
    what_if_split_esc_recover: str,
    what_if_split_esc_recover_alt: str,
    what_if_split_esc_recover_plan: str,
) -> tuple[str, dict[str, str | bool]]:
    """Prototype dual-lane coach snapshot for contingency readability behind experiment flag."""
    flag_name = "DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_COACH"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    primary_lane = str(what_if_split_esc_recover).upper()
    backup_lane = str(what_if_split_esc_recover_alt).upper()
    plan = str(what_if_split_esc_recover_plan).upper()

    actionable = {"PORTAL", "ALT", "PRESSURE"}

    if not flag_enabled:
        coach = "FLAG OFF"
        reason = "flag-disabled"
    else:
        if plan == "ALT" and backup_lane in actionable:
            selected_primary = backup_lane
            reason = "plan-prefers-alt-lane"
        elif primary_lane in actionable:
            selected_primary = primary_lane
            reason = "plan-or-primary-lane-available"
        elif backup_lane in actionable:
            selected_primary = backup_lane
            reason = "fallback-to-alt-when-primary-unavailable"
        else:
            selected_primary = "NONE"
            reason = "no-actionable-recover-lanes"

        if selected_primary == primary_lane and backup_lane in actionable and backup_lane != selected_primary:
            selected_backup = backup_lane
        elif selected_primary == backup_lane and primary_lane in actionable and primary_lane != selected_primary:
            selected_backup = primary_lane
        else:
            selected_backup = "NONE"

        coach = f"{selected_primary}|{selected_backup}"

    return coach, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "splitEscRecover": primary_lane,
        "splitEscRecoverAlt": backup_lane,
        "splitEscRecoverPlan": plan,
        "reason": reason,
    }


def what_if_split_escalate_recover_veto_rearm_coach_confidence_from_signals(
    *,
    what_if_split_esc_recover_veto_rearm_coach: str,
    what_if_split_esc_recover_veto_rearm_nudge_confidence: str,
    what_if_split_esc_recover_veto_rearm_fit: str,
) -> tuple[str, dict[str, str]]:
    """Classify trust level for dual-lane coach snapshot readability."""
    coach = str(what_if_split_esc_recover_veto_rearm_coach).upper()
    nudge_conf = str(what_if_split_esc_recover_veto_rearm_nudge_confidence).upper()
    fit = str(what_if_split_esc_recover_veto_rearm_fit).upper()

    if coach == "FLAG OFF":
        confidence = "LOW"
        reason = "coach-flag-disabled"
    elif coach.startswith("NONE"):
        confidence = "LOW"
        reason = "coach-has-no-actionable-primary-lane"
    elif "|NONE" not in coach and nudge_conf in {"MID", "HIGH"}:
        confidence = "HIGH"
        reason = "coach-provides-primary-and-backup-with-actionable-nudge-confidence"
    elif nudge_conf == "HIGH" and fit == "TENSE":
        confidence = "HIGH"
        reason = "coach-backed-by-high-confidence-under-tense-fit"
    elif nudge_conf in {"MID", "HIGH"}:
        confidence = "MID"
        reason = "coach-backed-by-actionable-nudge-confidence"
    else:
        confidence = "LOW"
        reason = "coach-context-not-strong-enough"

    return confidence, {
        "splitEscRecoverVetoRearmCoach": coach,
        "splitEscRecoverVetoRearmNudgeConfidence": nudge_conf,
        "splitEscRecoverVetoRearmFit": fit,
        "reason": reason,
    }


def what_if_split_escalate_recover_veto_rearm_coach_mode_from_signals(
    *,
    what_if_split_esc_recover_veto_rearm_coach: str,
) -> tuple[str, dict[str, str]]:
    """Classify coach lane posture from primary/backup lane mix."""
    coach = str(what_if_split_esc_recover_veto_rearm_coach).upper()

    if coach == "FLAG OFF":
        mode = "PRIMARY"
        reason = "coach-flag-disabled-default-primary-mode"
        primary = "FLAG OFF"
        backup = "NONE"
    else:
        primary, sep, backup = coach.partition("|")
        primary = primary.strip() or "NONE"
        backup = backup.strip() if sep else "NONE"
        backup = backup or "NONE"

        actionable = {"PORTAL", "ALT", "PRESSURE"}
        primary_actionable = primary in actionable
        backup_actionable = backup in actionable

        if primary_actionable and backup_actionable and primary != backup:
            mode = "BALANCED"
            reason = "coach-includes-distinct-primary-and-backup-lanes"
        elif primary in {"NONE", "FLAG OFF"} and backup_actionable:
            mode = "BACKUP"
            reason = "coach-primary-missing-but-backup-actionable"
        elif backup_actionable and primary == backup:
            mode = "PRIMARY"
            reason = "coach-backup-duplicates-primary-lane"
        elif primary_actionable:
            mode = "PRIMARY"
            reason = "coach-primary-lane-drives-guidance"
        elif backup_actionable:
            mode = "BACKUP"
            reason = "coach-falls-back-to-backup-lane"
        else:
            mode = "PRIMARY"
            reason = "coach-has-no-actionable-lanes-default-primary-mode"

    return mode, {
        "splitEscRecoverVetoRearmCoach": coach,
        "coachPrimaryLane": primary,
        "coachBackupLane": backup,
        "reason": reason,
    }


def what_if_split_escalate_recover_veto_rearm_coach_why_from_signals(
    *,
    what_if_split_esc_recover_veto_rearm_coach: str,
    what_if_split_esc_recover_veto_rearm_coach_mode: str,
    what_if_split_esc_recover_veto_rearm_coach_confidence: str,
) -> tuple[str, dict[str, str | bool]]:
    """Prototype concise rationale for coach fallback guidance behind experiment flag."""
    flag_name = "DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_COACH_WHY"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    coach = str(what_if_split_esc_recover_veto_rearm_coach).upper()
    mode = str(what_if_split_esc_recover_veto_rearm_coach_mode).upper()
    confidence = str(what_if_split_esc_recover_veto_rearm_coach_confidence).upper()

    if not flag_enabled:
        why = "FLAG OFF"
        reason = "flag-disabled"
    elif coach == "FLAG OFF":
        why = "COACH OFF"
        reason = "coach-token-disabled"
    elif coach.startswith("NONE"):
        why = "NO ACTION"
        reason = "coach-primary-not-actionable"
    elif mode == "BALANCED" and confidence == "HIGH":
        why = "DUAL COVER"
        reason = "balanced-coach-with-high-confidence"
    elif mode == "BACKUP":
        why = "BACKUP READY"
        reason = "coach-routing-through-backup-lane"
    elif confidence in {"MID", "HIGH"}:
        why = "PRIMARY HOLD"
        reason = "primary-lane-guidance-with-actionable-confidence"
    else:
        why = "MONITOR"
        reason = "coach-context-below-action-threshold"

    return why, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "splitEscRecoverVetoRearmCoach": coach,
        "splitEscRecoverVetoRearmCoachMode": mode,
        "splitEscRecoverVetoRearmCoachConfidence": confidence,
        "reason": reason,
    }


def what_if_split_escalate_recover_veto_rearm_coach_handoff_from_signals(
    *,
    what_if_split_esc_recover_veto_rearm_coach: str,
    what_if_split_esc_recover_veto_rearm_coach_mode: str,
    what_if_split_esc_recover_veto_rearm_coach_confidence: str,
) -> tuple[str, dict[str, str]]:
    """Classify if coach routing is locked, flexible, or unavailable."""
    coach = str(what_if_split_esc_recover_veto_rearm_coach).upper()
    mode = str(what_if_split_esc_recover_veto_rearm_coach_mode).upper()
    confidence = str(what_if_split_esc_recover_veto_rearm_coach_confidence).upper()

    if coach == "FLAG OFF" or coach.startswith("NONE"):
        handoff = "NONE"
        reason = "coach-not-actionable-for-route-handoff"
    elif mode == "BALANCED" and confidence in {"MID", "HIGH"}:
        handoff = "FLEX"
        reason = "dual-lane-coach-supports-flex-handoff"
    elif mode in {"PRIMARY", "BACKUP"} and confidence in {"MID", "HIGH"}:
        handoff = "LOCKED"
        reason = "single-lane-coach-ready-for-locked-handoff"
    elif confidence == "LOW":
        handoff = "NONE"
        reason = "coach-confidence-too-low-for-handoff"
    else:
        handoff = "FLEX"
        reason = "coach-available-with-limited-confidence"

    return handoff, {
        "splitEscRecoverVetoRearmCoach": coach,
        "splitEscRecoverVetoRearmCoachMode": mode,
        "splitEscRecoverVetoRearmCoachConfidence": confidence,
        "reason": reason,
    }


def what_if_split_escalate_recover_veto_rearm_coach_handoff_fit_from_signals(
    *,
    what_if_split_esc_recover_veto_rearm_coach_handoff: str,
    what_if_split_esc_pressure: str,
) -> tuple[str, dict[str, str]]:
    """Map coach handoff state + pressure context into SAFE/EVEN/TENSE."""
    handoff = str(what_if_split_esc_recover_veto_rearm_coach_handoff).upper()
    pressure = str(what_if_split_esc_pressure).upper()

    if handoff == "NONE" and pressure == "HIGH":
        fit = "TENSE"
        reason = "no-handoff-under-high-pressure"
    elif handoff == "NONE":
        fit = "EVEN"
        reason = "no-handoff-but-pressure-not-critical"
    elif handoff == "LOCKED" and pressure == "LOW":
        fit = "SAFE"
        reason = "locked-handoff-with-low-pressure"
    elif handoff == "LOCKED" and pressure == "HIGH":
        fit = "TENSE"
        reason = "locked-handoff-under-high-pressure"
    elif handoff == "FLEX" and pressure == "LOW":
        fit = "SAFE"
        reason = "flex-handoff-with-low-pressure"
    elif handoff == "FLEX" and pressure == "HIGH":
        fit = "TENSE"
        reason = "flex-handoff-under-high-pressure"
    else:
        fit = "EVEN"
        reason = "handoff-and-pressure-balanced"

    return fit, {
        "splitEscRecoverVetoRearmCoachHandoff": handoff,
        "splitEscPressure": pressure,
        "reason": reason,
    }


def what_if_split_escalate_recover_veto_rearm_coach_handoff_why_from_signals(
    *,
    what_if_split_esc_recover_veto_rearm_coach_handoff: str,
    what_if_split_esc_recover_veto_rearm_coach_handoff_fit: str,
    what_if_split_esc_recover_veto_rearm_coach_confidence: str,
) -> tuple[str, dict[str, str | bool]]:
    """Prototype concise rationale token for coach handoff guidance behind experiment flag."""
    flag_name = "DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_COACH_HANDOFF_WHY"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    handoff = str(what_if_split_esc_recover_veto_rearm_coach_handoff).upper()
    fit = str(what_if_split_esc_recover_veto_rearm_coach_handoff_fit).upper()
    confidence = str(what_if_split_esc_recover_veto_rearm_coach_confidence).upper()

    if not flag_enabled:
        why = "FLAG OFF"
        reason = "flag-disabled"
    elif handoff == "NONE":
        why = "HOLD LINE"
        reason = "no-coach-handoff-available"
    elif fit == "TENSE" and confidence == "HIGH":
        why = "LOCK FAST"
        reason = "high-confidence-handoff-under-pressure"
    elif handoff == "LOCKED" and confidence in {"MID", "HIGH"}:
        why = "COMMIT"
        reason = "locked-handoff-with-actionable-confidence"
    elif handoff == "FLEX" and fit == "SAFE":
        why = "SCOUT"
        reason = "flex-handoff-safe-for-probing"
    elif handoff == "FLEX":
        why = "HEDGE"
        reason = "flex-handoff-needs-balanced-follow-through"
    else:
        why = "MONITOR"
        reason = "fallback-monitoring-path"

    return why, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "splitEscRecoverVetoRearmCoachHandoff": handoff,
        "splitEscRecoverVetoRearmCoachHandoffFit": fit,
        "splitEscRecoverVetoRearmCoachConfidence": confidence,
        "reason": reason,
    }


def what_if_split_escalate_recover_confidence_delta_from_prior(
    *,
    current_confidence: str,
    prior_json_path: Path,
) -> tuple[str, dict[str, str | int | bool]]:
    """Compare current recovery confidence against prior digest window."""
    score_map = {"LOW": 0, "MID": 1, "HIGH": 2}
    current = str(current_confidence).upper()
    current_score = score_map.get(current, 0)

    prior_loaded = False
    prior_confidence = current
    prior_score = current_score

    if prior_json_path.is_file():
        try:
            prior = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_confidence = str(prior.get("whatIfSplitEscRecoverConfidence", current)).upper()
            prior_score = score_map.get(prior_confidence, current_score)
            prior_loaded = True
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    delta = current_score - prior_score
    if delta > 0:
        delta_token = f"+{delta}"
        reason = "confidence-increased-vs-prior-window"
    elif delta < 0:
        delta_token = str(delta)
        reason = "confidence-decreased-vs-prior-window"
    else:
        delta_token = "+0"
        reason = "confidence-unchanged-vs-prior-window"

    return delta_token, {
        "currentConfidence": current,
        "currentScore": current_score,
        "priorConfidence": prior_confidence,
        "priorScore": prior_score,
        "delta": delta,
        "priorLoaded": prior_loaded,
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
    vibe_added = {vibe: 0 for vibe in ROUTE_VIBE_PATTERNS}
    vibe_removed = {vibe: 0 for vibe in ROUTE_VIBE_PATTERNS}
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
                c_vibes = count_route_vibes_in_line(line)
                for k, v in c.items():
                    added[k] += v
                for token, v in c_tokens.items():
                    token_added[token] += v
                for vibe, v in c_vibes.items():
                    vibe_added[vibe] += v
                pressure_added += sum(line.count(token) for token in PRESSURE_TOKENS)
            elif raw.startswith("-"):
                line = raw[1:]
                c = count_tokens_in_line(line)
                c_tokens = count_catalog_tokens_in_line(line)
                c_vibes = count_route_vibes_in_line(line)
                for k, v in c.items():
                    removed[k] += v
                for token, v in c_tokens.items():
                    token_removed[token] += v
                for vibe, v in c_vibes.items():
                    vibe_removed[vibe] += v
                pressure_removed += sum(line.count(token) for token in PRESSURE_TOKENS)

    net = {k: added[k] - removed[k] for k in TOKEN_GROUPS}
    token_net = {token: token_added[token] - token_removed[token] for token in TOKEN_CATALOG}
    vibe_net = {vibe: vibe_added[vibe] - vibe_removed[vibe] for vibe in ROUTE_VIBE_PATTERNS}
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
        "routeVibeEdits": {
            "added": vibe_added,
            "removed": vibe_removed,
            "net": vibe_net,
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
    route_vibe_totals = {
        "added": {
            vibe: sum(r["routeVibeEdits"]["added"][vibe] for r in touched)
            for vibe in ROUTE_VIBE_PATTERNS
        },
        "removed": {
            vibe: sum(r["routeVibeEdits"]["removed"][vibe] for r in touched)
            for vibe in ROUTE_VIBE_PATTERNS
        },
        "net": {
            vibe: sum(r["routeVibeEdits"]["net"][vibe] for r in touched)
            for vibe in ROUTE_VIBE_PATTERNS
        },
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
    action_pace, action_pace_signals = route_action_pacing_from_signals(
        action_guard=action_guard,
        action_stability=action_stability,
        pressure_lag=pressure_lag,
    )
    pace_drift, pace_drift_signals = pace_drift_from_prior(
        current_pace=action_pace,
        prior_json_path=args.out_json,
    )
    action_pace_window, action_pace_window_signals = action_pace_window_from_signals(
        action_pace=action_pace,
        action_guard=action_guard,
        pace_drift=pace_drift,
    )
    action_pace_window_confidence, action_pace_window_confidence_signals = action_pace_window_confidence_from_signals(
        action_pace_window=action_pace_window,
        action_stability=action_stability,
        pace_drift=pace_drift,
        pace_drift_signals=pace_drift_signals,
    )
    action_pace_alt_window, action_pace_alt_window_signals = action_pace_alt_window_from_signals(
        action_pace_window=action_pace_window,
        route_sandbox=route_sandbox,
        sandbox_target=sandbox_target,
        sandbox_readiness=sandbox_readiness,
    )
    action_pace_alt_window_confidence, action_pace_alt_window_confidence_signals = action_pace_alt_window_confidence_from_signals(
        action_pace_alt_window=action_pace_alt_window,
        action_pace_alt_window_signals=action_pace_alt_window_signals,
        action_pace_window_confidence=action_pace_window_confidence,
    )
    action_pace_alt_window_fit, action_pace_alt_window_fit_signals = action_pace_alt_window_fit_from_signals(
        action_pace_alt_window=action_pace_alt_window,
        action_pace_alt_window_signals=action_pace_alt_window_signals,
        pressure_band=pressure_band,
    )
    action_pace_alt_window_why, action_pace_alt_window_why_signals = action_pace_alt_window_why_from_signals(
        action_pace_alt_window=action_pace_alt_window,
        action_pace_alt_window_confidence=action_pace_alt_window_confidence,
        action_pace_alt_window_fit=action_pace_alt_window_fit,
        action_pace_alt_window_signals=action_pace_alt_window_signals,
    )
    action_pace_alt_window_urgency, action_pace_alt_window_urgency_signals = action_pace_alt_window_urgency_from_signals(
        action_pace_alt_window=action_pace_alt_window,
        action_pace_alt_window_confidence=action_pace_alt_window_confidence,
        action_pace_alt_window_fit=action_pace_alt_window_fit,
        action_pace_alt_window_why=action_pace_alt_window_why,
    )
    action_pace_alt_window_urgency_drift, action_pace_alt_window_urgency_drift_signals = action_pace_alt_window_urgency_drift_from_prior(
        current_action_pace_alt_window_urgency=action_pace_alt_window_urgency,
        prior_json_path=args.out_json,
    )
    action_pace_alt_window_step, action_pace_alt_window_step_signals = action_pace_alt_window_step_from_signals(
        action_pace_alt_window=action_pace_alt_window,
        action_pace_alt_window_confidence=action_pace_alt_window_confidence,
        action_pace_alt_window_fit=action_pace_alt_window_fit,
        action_pace_alt_window_urgency=action_pace_alt_window_urgency,
        action_pace_alt_window_signals=action_pace_alt_window_signals,
    )
    action_pace_alt_window_step_drift, action_pace_alt_window_step_drift_signals = action_pace_alt_window_step_drift_from_prior(
        current_action_pace_alt_window_step=action_pace_alt_window_step,
        prior_json_path=args.out_json,
    )
    action_pace_alt_window_step_glyph, action_pace_alt_window_step_glyph_signals = action_pace_alt_window_step_glyph_from_signals(
        action_pace_alt_window_step=action_pace_alt_window_step,
        action_pace_alt_window_urgency=action_pace_alt_window_urgency,
        action_pace_alt_window_fit=action_pace_alt_window_fit,
    )
    action_pace_alt_window_pulse, action_pace_alt_window_pulse_signals = action_pace_alt_window_pulse_from_signals(
        action_pace_alt_window_urgency=action_pace_alt_window_urgency,
        action_pace_alt_window_fit=action_pace_alt_window_fit,
        action_pace_alt_window_confidence=action_pace_alt_window_confidence,
    )
    action_pace_alt_window_pulse_drift, action_pace_alt_window_pulse_drift_signals = action_pace_alt_window_pulse_drift_from_prior(
        current_action_pace_alt_window_pulse=action_pace_alt_window_pulse,
        prior_json_path=args.out_json,
    )
    route_pulse_link, route_pulse_link_signals = route_pulse_link_from_signals(
        action_pace_alt_window_pulse=action_pace_alt_window_pulse,
        action_pace_alt_window_pulse_drift=action_pace_alt_window_pulse_drift,
        action_pace_alt_window_fit=action_pace_alt_window_fit,
    )
    route_pulse_link_confidence, route_pulse_link_confidence_signals = route_pulse_link_confidence_from_signals(
        route_pulse_link=route_pulse_link,
        route_pulse_link_signals=route_pulse_link_signals,
        action_pace_alt_window_confidence=action_pace_alt_window_confidence,
    )
    route_pulse_link_streak, route_pulse_link_streak_signals = route_pulse_link_streak_from_prior(
        current_route_pulse_link=route_pulse_link,
        prior_json_path=args.out_json,
    )
    route_pulse_link_mode, route_pulse_link_mode_signals = route_pulse_link_mode_from_signals(
        route_pulse_link=route_pulse_link,
        route_pulse_link_streak=route_pulse_link_streak,
        action_pace_alt_window_pulse_drift=action_pace_alt_window_pulse_drift,
    )
    route_pulse_link_mode_drift, route_pulse_link_mode_drift_signals = route_pulse_link_mode_drift_from_prior(
        current_route_pulse_link_mode=route_pulse_link_mode,
        prior_json_path=args.out_json,
    )
    route_pulse_link_mode_stability_streak, route_pulse_link_mode_stability_streak_signals = route_pulse_link_mode_stability_streak_from_prior(
        current_route_pulse_link_mode=route_pulse_link_mode,
        prior_json_path=args.out_json,
    )
    route_pulse_link_mode_why, route_pulse_link_mode_why_signals = route_pulse_link_mode_why_from_signals(
        route_pulse_link_mode=route_pulse_link_mode,
        route_pulse_link_mode_signals=route_pulse_link_mode_signals,
        route_pulse_link_mode_drift=route_pulse_link_mode_drift,
    )
    route_pulse_link_mode_fit, route_pulse_link_mode_fit_signals = route_pulse_link_mode_fit_from_signals(
        route_pulse_link_mode=route_pulse_link_mode,
        route_pulse_link_mode_drift=route_pulse_link_mode_drift,
        route_pulse_link_mode_stability_streak=route_pulse_link_mode_stability_streak,
    )
    action_pace_why, action_pace_why_signals = action_pace_why_from_signals(
        action_pace=action_pace,
        action_guard=action_guard,
        action_stability=action_stability,
        pressure_lag=pressure_lag,
        pace_drift=pace_drift,
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
    what_if_split_esc_pressure, what_if_split_esc_pressure_signals = what_if_split_escalate_pressure_from_signals(
        what_if_split_esc_state=what_if_split_esc_state,
        what_if_split_esc_cool=what_if_split_esc_cool,
        pressure_band=pressure_band,
    )
    what_if_split_esc_recover, what_if_split_esc_recover_signals = what_if_split_escalate_recover_from_signals(
        what_if_split_esc_state=what_if_split_esc_state,
        what_if_split_escalate_lanes=what_if_split_escalate_lanes,
    )
    what_if_split_esc_recover_confidence, what_if_split_esc_recover_confidence_signals = what_if_split_escalate_recover_confidence_from_signals(
        what_if_split_esc_recover=what_if_split_esc_recover,
        what_if_split_esc_state=what_if_split_esc_state,
        what_if_split_esc_pressure=what_if_split_esc_pressure,
        what_if_split_escalate_lanes=what_if_split_escalate_lanes,
    )
    what_if_split_esc_recover_alt, what_if_split_esc_recover_alt_signals = what_if_split_escalate_recover_alt_from_signals(
        what_if_split_esc_recover=what_if_split_esc_recover,
        what_if_split_esc_state=what_if_split_esc_state,
        what_if_split_escalate_lanes=what_if_split_escalate_lanes,
    )
    what_if_split_esc_recover_alt_confidence, what_if_split_esc_recover_alt_confidence_signals = what_if_split_escalate_recover_alt_confidence_from_signals(
        what_if_split_esc_recover_alt=what_if_split_esc_recover_alt,
        what_if_split_esc_state=what_if_split_esc_state,
        what_if_split_esc_pressure=what_if_split_esc_pressure,
        what_if_split_escalate_lanes=what_if_split_escalate_lanes,
    )
    what_if_split_esc_recover_plan, what_if_split_esc_recover_plan_signals = what_if_split_escalate_recover_plan_from_signals(
        what_if_split_esc_recover=what_if_split_esc_recover,
        what_if_split_esc_recover_alt=what_if_split_esc_recover_alt,
    )
    what_if_split_esc_recover_why, what_if_split_esc_recover_why_signals = what_if_split_escalate_recover_why_from_signals(
        what_if_split_esc_recover_plan=what_if_split_esc_recover_plan,
        what_if_split_esc_recover_confidence=what_if_split_esc_recover_confidence,
        what_if_split_esc_pressure=what_if_split_esc_pressure,
    )
    what_if_split_esc_recover_tempo, what_if_split_esc_recover_tempo_signals = what_if_split_escalate_recover_tempo_from_signals(
        what_if_split_esc_recover_plan=what_if_split_esc_recover_plan,
        what_if_split_esc_recover_confidence=what_if_split_esc_recover_confidence,
        what_if_split_esc_pressure=what_if_split_esc_pressure,
    )
    what_if_split_esc_recover_veto, what_if_split_esc_recover_veto_signals = what_if_split_escalate_recover_veto_from_signals(
        what_if_split_esc_recover_confidence=what_if_split_esc_recover_confidence,
        what_if_split_esc_pressure=what_if_split_esc_pressure,
        what_if_split_esc_recover_plan=what_if_split_esc_recover_plan,
    )
    what_if_split_esc_recover_veto_confidence, what_if_split_esc_recover_veto_confidence_signals = what_if_split_escalate_recover_veto_confidence_from_signals(
        what_if_split_esc_recover_veto=what_if_split_esc_recover_veto,
        what_if_split_esc_recover_confidence=what_if_split_esc_recover_confidence,
        what_if_split_esc_pressure=what_if_split_esc_pressure,
        what_if_split_esc_recover_plan=what_if_split_esc_recover_plan,
    )
    what_if_split_esc_recover_veto_why, what_if_split_esc_recover_veto_why_signals = what_if_split_escalate_recover_veto_why_from_signals(
        what_if_split_esc_recover_veto=what_if_split_esc_recover_veto,
        what_if_split_esc_recover_veto_confidence=what_if_split_esc_recover_veto_confidence,
        what_if_split_esc_pressure=what_if_split_esc_pressure,
        what_if_split_esc_recover_plan=what_if_split_esc_recover_plan,
    )
    what_if_split_esc_recover_veto_cooloff, what_if_split_esc_recover_veto_cooloff_signals = what_if_split_escalate_recover_veto_cooloff_from_prior(
        current_split_esc_recover_veto=what_if_split_esc_recover_veto,
        prior_json_path=args.out_json,
    )
    what_if_split_esc_recover_veto_state, what_if_split_esc_recover_veto_state_signals = what_if_split_escalate_recover_veto_state_from_signals(
        what_if_split_esc_recover_veto=what_if_split_esc_recover_veto,
        what_if_split_esc_recover_veto_cooloff=what_if_split_esc_recover_veto_cooloff,
    )
    what_if_split_esc_recover_veto_dwell, what_if_split_esc_recover_veto_dwell_signals = what_if_split_escalate_recover_veto_dwell_from_prior(
        current_split_esc_recover_veto_state=what_if_split_esc_recover_veto_state,
        prior_json_path=args.out_json,
    )
    what_if_split_esc_recover_veto_release, what_if_split_esc_recover_veto_release_signals = what_if_split_escalate_recover_veto_release_from_prior(
        current_split_esc_recover_veto_state=what_if_split_esc_recover_veto_state,
        prior_json_path=args.out_json,
    )
    what_if_split_esc_recover_veto_release_confidence, what_if_split_esc_recover_veto_release_confidence_signals = what_if_split_escalate_recover_veto_release_confidence_from_signals(
        what_if_split_esc_recover_veto_release=what_if_split_esc_recover_veto_release,
        what_if_split_esc_recover_veto_state=what_if_split_esc_recover_veto_state,
        what_if_split_esc_recover_veto_dwell=what_if_split_esc_recover_veto_dwell,
    )
    what_if_split_esc_recover_veto_release_route, what_if_split_esc_recover_veto_release_route_signals = what_if_split_escalate_recover_veto_release_route_from_signals(
        what_if_split_esc_recover_veto_release=what_if_split_esc_recover_veto_release,
        what_if_split_esc_recover_veto_state=what_if_split_esc_recover_veto_state,
        what_if_split_esc_recover=what_if_split_esc_recover,
        what_if_split_esc_recover_alt=what_if_split_esc_recover_alt,
        what_if_split_esc_recover_plan=what_if_split_esc_recover_plan,
    )
    what_if_split_esc_recover_veto_release_tick, what_if_split_esc_recover_veto_release_tick_signals = what_if_split_escalate_recover_veto_release_tick_from_prior(
        current_split_esc_recover_veto_release=what_if_split_esc_recover_veto_release,
        current_split_esc_recover_veto_state=what_if_split_esc_recover_veto_state,
        prior_json_path=args.out_json,
    )
    what_if_split_esc_recover_veto_release_tick_phase, what_if_split_esc_recover_veto_release_tick_phase_signals = what_if_split_escalate_recover_veto_release_tick_phase_from_signals(
        what_if_split_esc_recover_veto_release_tick=what_if_split_esc_recover_veto_release_tick,
    )
    what_if_split_esc_recover_veto_release_cadence, what_if_split_esc_recover_veto_release_cadence_signals = what_if_split_escalate_recover_veto_release_tick_cadence_from_signals(
        what_if_split_esc_recover_veto_release_tick=what_if_split_esc_recover_veto_release_tick,
        what_if_split_esc_recover_veto_release_tick_signals=what_if_split_esc_recover_veto_release_tick_signals,
    )
    what_if_split_esc_recover_veto_rearm, what_if_split_esc_recover_veto_rearm_signals = what_if_split_escalate_recover_veto_rearm_from_signals(
        what_if_split_esc_recover_veto_release_tick_phase=what_if_split_esc_recover_veto_release_tick_phase,
        what_if_split_esc_pressure=what_if_split_esc_pressure,
        what_if_split_esc_recover_veto_release_cadence=what_if_split_esc_recover_veto_release_cadence,
    )
    what_if_split_esc_recover_veto_rearm_confidence, what_if_split_esc_recover_veto_rearm_confidence_signals = what_if_split_escalate_recover_veto_rearm_confidence_from_signals(
        what_if_split_esc_recover_veto_rearm=what_if_split_esc_recover_veto_rearm,
        what_if_split_esc_recover_veto_rearm_signals=what_if_split_esc_recover_veto_rearm_signals,
    )
    what_if_split_esc_recover_veto_rearm_why, what_if_split_esc_recover_veto_rearm_why_signals = what_if_split_escalate_recover_veto_rearm_why_from_signals(
        what_if_split_esc_recover_veto_rearm=what_if_split_esc_recover_veto_rearm,
        what_if_split_esc_recover_veto_rearm_confidence=what_if_split_esc_recover_veto_rearm_confidence,
        what_if_split_esc_pressure=what_if_split_esc_pressure,
        what_if_split_esc_recover_veto_release_tick_phase=what_if_split_esc_recover_veto_release_tick_phase,
    )
    what_if_split_esc_recover_veto_rearm_cooloff, what_if_split_esc_recover_veto_rearm_cooloff_signals = what_if_split_escalate_recover_veto_rearm_cooloff_from_prior(
        current_split_esc_recover_veto_rearm=what_if_split_esc_recover_veto_rearm,
        prior_json_path=args.out_json,
    )
    what_if_split_esc_recover_veto_rearm_cooloff_state, what_if_split_esc_recover_veto_rearm_cooloff_state_signals = what_if_split_escalate_recover_veto_rearm_cooloff_state_from_signals(
        what_if_split_esc_recover_veto_rearm=what_if_split_esc_recover_veto_rearm,
        what_if_split_esc_recover_veto_rearm_cooloff=what_if_split_esc_recover_veto_rearm_cooloff,
    )
    what_if_split_esc_recover_veto_rearm_fit, what_if_split_esc_recover_veto_rearm_fit_signals = what_if_split_escalate_recover_veto_rearm_fit_from_signals(
        what_if_split_esc_recover_veto_rearm_cooloff_state=what_if_split_esc_recover_veto_rearm_cooloff_state,
        what_if_split_esc_recover_veto_rearm_cooloff=what_if_split_esc_recover_veto_rearm_cooloff,
        what_if_split_esc_pressure=what_if_split_esc_pressure,
    )
    what_if_split_esc_recover_veto_rearm_nudge, what_if_split_esc_recover_veto_rearm_nudge_signals = what_if_split_escalate_recover_veto_rearm_nudge_from_signals(
        what_if_split_esc_recover_veto_rearm=what_if_split_esc_recover_veto_rearm,
        what_if_split_esc_recover_veto_rearm_confidence=what_if_split_esc_recover_veto_rearm_confidence,
        what_if_split_esc_recover_veto_rearm_fit=what_if_split_esc_recover_veto_rearm_fit,
        what_if_split_esc_recover_veto_rearm_cooloff_state=what_if_split_esc_recover_veto_rearm_cooloff_state,
    )
    what_if_split_esc_recover_veto_rearm_nudge_window, what_if_split_esc_recover_veto_rearm_nudge_window_signals = what_if_split_escalate_recover_veto_rearm_nudge_window_from_signals(
        what_if_split_esc_recover_veto_rearm=what_if_split_esc_recover_veto_rearm,
        what_if_split_esc_recover_veto_rearm_cooloff_state=what_if_split_esc_recover_veto_rearm_cooloff_state,
    )
    what_if_split_esc_recover_veto_rearm_nudge_confidence, what_if_split_esc_recover_veto_rearm_nudge_confidence_signals = what_if_split_escalate_recover_veto_rearm_nudge_confidence_from_signals(
        what_if_split_esc_recover_veto_rearm_nudge=what_if_split_esc_recover_veto_rearm_nudge,
        what_if_split_esc_recover_veto_rearm_confidence=what_if_split_esc_recover_veto_rearm_confidence,
        what_if_split_esc_recover_veto_rearm_fit=what_if_split_esc_recover_veto_rearm_fit,
    )
    what_if_split_esc_recover_veto_rearm_nudge_why, what_if_split_esc_recover_veto_rearm_nudge_why_signals = what_if_split_escalate_recover_veto_rearm_nudge_why_from_signals(
        what_if_split_esc_recover_veto_rearm_nudge=what_if_split_esc_recover_veto_rearm_nudge,
        what_if_split_esc_recover_veto_rearm_nudge_confidence=what_if_split_esc_recover_veto_rearm_nudge_confidence,
        what_if_split_esc_recover_veto_rearm_nudge_window=what_if_split_esc_recover_veto_rearm_nudge_window,
        what_if_split_esc_recover_veto_rearm_fit=what_if_split_esc_recover_veto_rearm_fit,
    )
    what_if_split_esc_recover_veto_rearm_nudge_impact, what_if_split_esc_recover_veto_rearm_nudge_impact_signals = what_if_split_escalate_recover_veto_rearm_nudge_impact_from_signals(
        what_if_split_esc_recover_veto_rearm_nudge=what_if_split_esc_recover_veto_rearm_nudge,
        what_if_split_esc_recover_veto_rearm_nudge_window=what_if_split_esc_recover_veto_rearm_nudge_window,
        what_if_split_esc_recover_veto_rearm_fit=what_if_split_esc_recover_veto_rearm_fit,
    )
    what_if_split_esc_recover_veto_rearm_nudge_drift, what_if_split_esc_recover_veto_rearm_nudge_drift_signals = what_if_split_escalate_recover_veto_rearm_nudge_drift_from_prior(
        current_nudge_why=what_if_split_esc_recover_veto_rearm_nudge_why,
        prior_json_path=args.out_json,
    )
    what_if_split_esc_recover_veto_rearm_coach, what_if_split_esc_recover_veto_rearm_coach_signals = what_if_split_escalate_recover_veto_rearm_coach_from_signals(
        what_if_split_esc_recover=what_if_split_esc_recover,
        what_if_split_esc_recover_alt=what_if_split_esc_recover_alt,
        what_if_split_esc_recover_plan=what_if_split_esc_recover_plan,
    )
    what_if_split_esc_recover_veto_rearm_coach_confidence, what_if_split_esc_recover_veto_rearm_coach_confidence_signals = what_if_split_escalate_recover_veto_rearm_coach_confidence_from_signals(
        what_if_split_esc_recover_veto_rearm_coach=what_if_split_esc_recover_veto_rearm_coach,
        what_if_split_esc_recover_veto_rearm_nudge_confidence=what_if_split_esc_recover_veto_rearm_nudge_confidence,
        what_if_split_esc_recover_veto_rearm_fit=what_if_split_esc_recover_veto_rearm_fit,
    )
    what_if_split_esc_recover_veto_rearm_coach_mode, what_if_split_esc_recover_veto_rearm_coach_mode_signals = what_if_split_escalate_recover_veto_rearm_coach_mode_from_signals(
        what_if_split_esc_recover_veto_rearm_coach=what_if_split_esc_recover_veto_rearm_coach,
    )
    what_if_split_esc_recover_veto_rearm_coach_why, what_if_split_esc_recover_veto_rearm_coach_why_signals = what_if_split_escalate_recover_veto_rearm_coach_why_from_signals(
        what_if_split_esc_recover_veto_rearm_coach=what_if_split_esc_recover_veto_rearm_coach,
        what_if_split_esc_recover_veto_rearm_coach_mode=what_if_split_esc_recover_veto_rearm_coach_mode,
        what_if_split_esc_recover_veto_rearm_coach_confidence=what_if_split_esc_recover_veto_rearm_coach_confidence,
    )
    what_if_split_esc_recover_veto_rearm_coach_handoff, what_if_split_esc_recover_veto_rearm_coach_handoff_signals = what_if_split_escalate_recover_veto_rearm_coach_handoff_from_signals(
        what_if_split_esc_recover_veto_rearm_coach=what_if_split_esc_recover_veto_rearm_coach,
        what_if_split_esc_recover_veto_rearm_coach_mode=what_if_split_esc_recover_veto_rearm_coach_mode,
        what_if_split_esc_recover_veto_rearm_coach_confidence=what_if_split_esc_recover_veto_rearm_coach_confidence,
    )
    what_if_split_esc_recover_veto_rearm_coach_handoff_fit, what_if_split_esc_recover_veto_rearm_coach_handoff_fit_signals = what_if_split_escalate_recover_veto_rearm_coach_handoff_fit_from_signals(
        what_if_split_esc_recover_veto_rearm_coach_handoff=what_if_split_esc_recover_veto_rearm_coach_handoff,
        what_if_split_esc_pressure=what_if_split_esc_pressure,
    )
    what_if_split_esc_recover_veto_rearm_coach_handoff_why, what_if_split_esc_recover_veto_rearm_coach_handoff_why_signals = what_if_split_escalate_recover_veto_rearm_coach_handoff_why_from_signals(
        what_if_split_esc_recover_veto_rearm_coach_handoff=what_if_split_esc_recover_veto_rearm_coach_handoff,
        what_if_split_esc_recover_veto_rearm_coach_handoff_fit=what_if_split_esc_recover_veto_rearm_coach_handoff_fit,
        what_if_split_esc_recover_veto_rearm_coach_confidence=what_if_split_esc_recover_veto_rearm_coach_confidence,
    )
    what_if_split_esc_recover_confidence_delta, what_if_split_esc_recover_confidence_delta_signals = what_if_split_escalate_recover_confidence_delta_from_prior(
        current_confidence=what_if_split_esc_recover_confidence,
        prior_json_path=args.out_json,
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
        "actionPace": action_pace,
        "actionPaceSignals": action_pace_signals,
        "paceDrift": pace_drift,
        "paceDriftSignals": pace_drift_signals,
        "actionPaceWindow": action_pace_window,
        "actionPaceWindowSignals": action_pace_window_signals,
        "actionPaceWindowConfidence": action_pace_window_confidence,
        "actionPaceWindowConfidenceSignals": action_pace_window_confidence_signals,
        "actionPaceAltWindow": action_pace_alt_window,
        "actionPaceAltWindowSignals": action_pace_alt_window_signals,
        "actionPaceAltWindowConfidence": action_pace_alt_window_confidence,
        "actionPaceAltWindowConfidenceSignals": action_pace_alt_window_confidence_signals,
        "actionPaceAltWindowFit": action_pace_alt_window_fit,
        "actionPaceAltWindowFitSignals": action_pace_alt_window_fit_signals,
        "actionPaceAltWindowWhy": action_pace_alt_window_why,
        "actionPaceAltWindowWhySignals": action_pace_alt_window_why_signals,
        "actionPaceAltWindowUrgency": action_pace_alt_window_urgency,
        "actionPaceAltWindowUrgencySignals": action_pace_alt_window_urgency_signals,
        "actionPaceAltWindowUrgencyDrift": action_pace_alt_window_urgency_drift,
        "actionPaceAltWindowUrgencyDriftSignals": action_pace_alt_window_urgency_drift_signals,
        "actionPaceAltWindowStep": action_pace_alt_window_step,
        "actionPaceAltWindowStepSignals": action_pace_alt_window_step_signals,
        "actionPaceAltWindowStepDrift": action_pace_alt_window_step_drift,
        "actionPaceAltWindowStepDriftSignals": action_pace_alt_window_step_drift_signals,
        "actionPaceAltWindowStepGlyph": action_pace_alt_window_step_glyph,
        "actionPaceAltWindowStepGlyphSignals": action_pace_alt_window_step_glyph_signals,
        "actionPaceAltWindowPulse": action_pace_alt_window_pulse,
        "actionPaceAltWindowPulseSignals": action_pace_alt_window_pulse_signals,
        "actionPaceAltWindowPulseDrift": action_pace_alt_window_pulse_drift,
        "actionPaceAltWindowPulseDriftSignals": action_pace_alt_window_pulse_drift_signals,
        "routePulseLink": route_pulse_link,
        "routePulseLinkSignals": route_pulse_link_signals,
        "routePulseLinkConfidence": route_pulse_link_confidence,
        "routePulseLinkConfidenceSignals": route_pulse_link_confidence_signals,
        "routePulseLinkStreak": route_pulse_link_streak,
        "routePulseLinkStreakSignals": route_pulse_link_streak_signals,
        "routePulseLinkMode": route_pulse_link_mode,
        "routePulseLinkModeSignals": route_pulse_link_mode_signals,
        "routePulseLinkModeDrift": route_pulse_link_mode_drift,
        "routePulseLinkModeDriftSignals": route_pulse_link_mode_drift_signals,
        "routePulseLinkModeStabilityStreak": route_pulse_link_mode_stability_streak,
        "routePulseLinkModeStabilityStreakSignals": route_pulse_link_mode_stability_streak_signals,
        "routePulseLinkModeWhy": route_pulse_link_mode_why,
        "routePulseLinkModeWhySignals": route_pulse_link_mode_why_signals,
        "routePulseLinkModeFit": route_pulse_link_mode_fit,
        "routePulseLinkModeFitSignals": route_pulse_link_mode_fit_signals,
        "actionPaceWhy": action_pace_why,
        "actionPaceWhySignals": action_pace_why_signals,
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
        "whatIfSplitEscPressure": what_if_split_esc_pressure,
        "whatIfSplitEscPressureSignals": what_if_split_esc_pressure_signals,
        "whatIfSplitEscRecover": what_if_split_esc_recover,
        "whatIfSplitEscRecoverSignals": what_if_split_esc_recover_signals,
        "whatIfSplitEscRecoverConfidence": what_if_split_esc_recover_confidence,
        "whatIfSplitEscRecoverConfidenceSignals": what_if_split_esc_recover_confidence_signals,
        "whatIfSplitEscRecoverAlt": what_if_split_esc_recover_alt,
        "whatIfSplitEscRecoverAltSignals": what_if_split_esc_recover_alt_signals,
        "whatIfSplitEscRecoverAltConfidence": what_if_split_esc_recover_alt_confidence,
        "whatIfSplitEscRecoverAltConfidenceSignals": what_if_split_esc_recover_alt_confidence_signals,
        "whatIfSplitEscRecoverPlan": what_if_split_esc_recover_plan,
        "whatIfSplitEscRecoverPlanSignals": what_if_split_esc_recover_plan_signals,
        "whatIfSplitEscRecoverWhy": what_if_split_esc_recover_why,
        "whatIfSplitEscRecoverWhySignals": what_if_split_esc_recover_why_signals,
        "whatIfSplitEscRecoverTempo": what_if_split_esc_recover_tempo,
        "whatIfSplitEscRecoverTempoSignals": what_if_split_esc_recover_tempo_signals,
        "whatIfSplitEscRecoverVeto": what_if_split_esc_recover_veto,
        "whatIfSplitEscRecoverVetoSignals": what_if_split_esc_recover_veto_signals,
        "whatIfSplitEscRecoverVetoConfidence": what_if_split_esc_recover_veto_confidence,
        "whatIfSplitEscRecoverVetoConfidenceSignals": what_if_split_esc_recover_veto_confidence_signals,
        "whatIfSplitEscRecoverVetoWhy": what_if_split_esc_recover_veto_why,
        "whatIfSplitEscRecoverVetoWhySignals": what_if_split_esc_recover_veto_why_signals,
        "whatIfSplitEscRecoverVetoCooloff": what_if_split_esc_recover_veto_cooloff,
        "whatIfSplitEscRecoverVetoCooloffSignals": what_if_split_esc_recover_veto_cooloff_signals,
        "whatIfSplitEscRecoverVetoState": what_if_split_esc_recover_veto_state,
        "whatIfSplitEscRecoverVetoStateSignals": what_if_split_esc_recover_veto_state_signals,
        "whatIfSplitEscRecoverVetoDwell": what_if_split_esc_recover_veto_dwell,
        "whatIfSplitEscRecoverVetoDwellSignals": what_if_split_esc_recover_veto_dwell_signals,
        "whatIfSplitEscRecoverVetoRelease": what_if_split_esc_recover_veto_release,
        "whatIfSplitEscRecoverVetoReleaseSignals": what_if_split_esc_recover_veto_release_signals,
        "whatIfSplitEscRecoverVetoReleaseConfidence": what_if_split_esc_recover_veto_release_confidence,
        "whatIfSplitEscRecoverVetoReleaseConfidenceSignals": what_if_split_esc_recover_veto_release_confidence_signals,
        "whatIfSplitEscRecoverVetoReleaseRoute": what_if_split_esc_recover_veto_release_route,
        "whatIfSplitEscRecoverVetoReleaseRouteSignals": what_if_split_esc_recover_veto_release_route_signals,
        "whatIfSplitEscRecoverVetoReleaseTick": what_if_split_esc_recover_veto_release_tick,
        "whatIfSplitEscRecoverVetoReleaseTickSignals": what_if_split_esc_recover_veto_release_tick_signals,
        "whatIfSplitEscRecoverVetoReleaseTickPhase": what_if_split_esc_recover_veto_release_tick_phase,
        "whatIfSplitEscRecoverVetoReleaseTickPhaseSignals": what_if_split_esc_recover_veto_release_tick_phase_signals,
        "whatIfSplitEscRecoverVetoReleaseCadence": what_if_split_esc_recover_veto_release_cadence,
        "whatIfSplitEscRecoverVetoReleaseCadenceSignals": what_if_split_esc_recover_veto_release_cadence_signals,
        "whatIfSplitEscRecoverVetoRearm": what_if_split_esc_recover_veto_rearm,
        "whatIfSplitEscRecoverVetoRearmSignals": what_if_split_esc_recover_veto_rearm_signals,
        "whatIfSplitEscRecoverVetoRearmConfidence": what_if_split_esc_recover_veto_rearm_confidence,
        "whatIfSplitEscRecoverVetoRearmConfidenceSignals": what_if_split_esc_recover_veto_rearm_confidence_signals,
        "whatIfSplitEscRecoverVetoRearmWhy": what_if_split_esc_recover_veto_rearm_why,
        "whatIfSplitEscRecoverVetoRearmWhySignals": what_if_split_esc_recover_veto_rearm_why_signals,
        "whatIfSplitEscRecoverVetoRearmCooloff": what_if_split_esc_recover_veto_rearm_cooloff,
        "whatIfSplitEscRecoverVetoRearmCooloffSignals": what_if_split_esc_recover_veto_rearm_cooloff_signals,
        "whatIfSplitEscRecoverVetoRearmCooloffState": what_if_split_esc_recover_veto_rearm_cooloff_state,
        "whatIfSplitEscRecoverVetoRearmCooloffStateSignals": what_if_split_esc_recover_veto_rearm_cooloff_state_signals,
        "whatIfSplitEscRecoverVetoRearmFit": what_if_split_esc_recover_veto_rearm_fit,
        "whatIfSplitEscRecoverVetoRearmFitSignals": what_if_split_esc_recover_veto_rearm_fit_signals,
        "whatIfSplitEscRecoverVetoRearmNudge": what_if_split_esc_recover_veto_rearm_nudge,
        "whatIfSplitEscRecoverVetoRearmNudgeSignals": what_if_split_esc_recover_veto_rearm_nudge_signals,
        "whatIfSplitEscRecoverVetoRearmNudgeWindow": what_if_split_esc_recover_veto_rearm_nudge_window,
        "whatIfSplitEscRecoverVetoRearmNudgeWindowSignals": what_if_split_esc_recover_veto_rearm_nudge_window_signals,
        "whatIfSplitEscRecoverVetoRearmNudgeConfidence": what_if_split_esc_recover_veto_rearm_nudge_confidence,
        "whatIfSplitEscRecoverVetoRearmNudgeConfidenceSignals": what_if_split_esc_recover_veto_rearm_nudge_confidence_signals,
        "whatIfSplitEscRecoverVetoRearmNudgeWhy": what_if_split_esc_recover_veto_rearm_nudge_why,
        "whatIfSplitEscRecoverVetoRearmNudgeWhySignals": what_if_split_esc_recover_veto_rearm_nudge_why_signals,
        "whatIfSplitEscRecoverVetoRearmNudgeImpact": what_if_split_esc_recover_veto_rearm_nudge_impact,
        "whatIfSplitEscRecoverVetoRearmNudgeImpactSignals": what_if_split_esc_recover_veto_rearm_nudge_impact_signals,
        "whatIfSplitEscRecoverVetoRearmNudgeDrift": what_if_split_esc_recover_veto_rearm_nudge_drift,
        "whatIfSplitEscRecoverVetoRearmNudgeDriftSignals": what_if_split_esc_recover_veto_rearm_nudge_drift_signals,
        "whatIfSplitEscRecoverVetoRearmCoach": what_if_split_esc_recover_veto_rearm_coach,
        "whatIfSplitEscRecoverVetoRearmCoachSignals": what_if_split_esc_recover_veto_rearm_coach_signals,
        "whatIfSplitEscRecoverVetoRearmCoachConfidence": what_if_split_esc_recover_veto_rearm_coach_confidence,
        "whatIfSplitEscRecoverVetoRearmCoachConfidenceSignals": what_if_split_esc_recover_veto_rearm_coach_confidence_signals,
        "whatIfSplitEscRecoverVetoRearmCoachMode": what_if_split_esc_recover_veto_rearm_coach_mode,
        "whatIfSplitEscRecoverVetoRearmCoachModeSignals": what_if_split_esc_recover_veto_rearm_coach_mode_signals,
        "whatIfSplitEscRecoverVetoRearmCoachWhy": what_if_split_esc_recover_veto_rearm_coach_why,
        "whatIfSplitEscRecoverVetoRearmCoachWhySignals": what_if_split_esc_recover_veto_rearm_coach_why_signals,
        "whatIfSplitEscRecoverVetoRearmCoachHandoff": what_if_split_esc_recover_veto_rearm_coach_handoff,
        "whatIfSplitEscRecoverVetoRearmCoachHandoffSignals": what_if_split_esc_recover_veto_rearm_coach_handoff_signals,
        "whatIfSplitEscRecoverVetoRearmCoachHandoffFit": what_if_split_esc_recover_veto_rearm_coach_handoff_fit,
        "whatIfSplitEscRecoverVetoRearmCoachHandoffFitSignals": what_if_split_esc_recover_veto_rearm_coach_handoff_fit_signals,
        "whatIfSplitEscRecoverVetoRearmCoachHandoffWhy": what_if_split_esc_recover_veto_rearm_coach_handoff_why,
        "whatIfSplitEscRecoverVetoRearmCoachHandoffWhySignals": what_if_split_esc_recover_veto_rearm_coach_handoff_why_signals,
        "whatIfSplitEscRecoverConfidenceDelta": what_if_split_esc_recover_confidence_delta,
        "whatIfSplitEscRecoverConfidenceDeltaSignals": what_if_split_esc_recover_confidence_delta_signals,
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
        "routeVibeTotals": route_vibe_totals,
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
        f"- ACTION PACE: **{action_pace}** ({action_pace_signals['reason']}; guard={action_pace_signals['actionGuard']} stability={action_pace_signals['actionStability']} lag={action_pace_signals['pressureLag']})",
        f"- PACE DRIFT: **{pace_drift:+d}** ({pace_drift_signals['reason']}; current={pace_drift_signals['currentPace']}({pace_drift_signals['currentScore']}) prior={pace_drift_signals['priorPace']}({pace_drift_signals['priorScore']}) loaded={pace_drift_signals['priorLoaded']})",
        f"- ACTION PACE WINDOW: **{action_pace_window}** ({action_pace_window_signals['reason']}; pace={action_pace_window_signals['actionPace']} guard={action_pace_window_signals['actionGuard']} drift={action_pace_window_signals['paceDrift']:+d})",
        f"- ACTION PACE WINDOW CONF: **{action_pace_window_confidence}** ({action_pace_window_confidence_signals['reason']}; window={action_pace_window_confidence_signals['actionPaceWindow']} stability={action_pace_window_confidence_signals['actionStability']} continuity={action_pace_window_confidence_signals['driftContinuity']} drift={action_pace_window_confidence_signals['paceDrift']:+d} loaded={action_pace_window_confidence_signals['priorLoaded']})",
        f"- ACTION PACE ALT WINDOW: **{action_pace_alt_window}** ({action_pace_alt_window_signals['reason']}; flag={action_pace_alt_window_signals['flagName']} enabled={action_pace_alt_window_signals['flagEnabled']} primary={action_pace_alt_window_signals['actionPaceWindow']} sandbox={action_pace_alt_window_signals['routeSandbox']} target={action_pace_alt_window_signals['sandboxTarget']} ready={action_pace_alt_window_signals['sandboxReadiness']})",
        f"- ACTION PACE ALT WINDOW CONF: **{action_pace_alt_window_confidence}** ({action_pace_alt_window_confidence_signals['reason']}; base={action_pace_alt_window_confidence_signals['actionPaceWindowConfidence']} flag={action_pace_alt_window_confidence_signals['flagEnabled']} sandbox={action_pace_alt_window_confidence_signals['routeSandbox']} target={action_pace_alt_window_confidence_signals['sandboxTarget']} ready={action_pace_alt_window_confidence_signals['sandboxReadiness']})",
        f"- ACTION PACE ALT WINDOW FIT: **{action_pace_alt_window_fit}** ({action_pace_alt_window_fit_signals['reason']}; flag={action_pace_alt_window_fit_signals['flagName']} enabled={action_pace_alt_window_fit_signals['flagEnabled']} pressure={action_pace_alt_window_fit_signals['pressureBand']} sandbox={action_pace_alt_window_fit_signals['routeSandbox']} target={action_pace_alt_window_fit_signals['sandboxTarget']} ready={action_pace_alt_window_fit_signals['sandboxReadiness']})",
        f"- ACTION PACE ALT WINDOW WHY: **{action_pace_alt_window_why}** ({action_pace_alt_window_why_signals['reason']}; flag={action_pace_alt_window_why_signals['flagName']} enabled={action_pace_alt_window_why_signals['flagEnabled']} alt={action_pace_alt_window_why_signals['actionPaceAltWindow']} conf={action_pace_alt_window_why_signals['actionPaceAltWindowConfidence']} fit={action_pace_alt_window_why_signals['actionPaceAltWindowFit']} sandbox={action_pace_alt_window_why_signals['routeSandbox']} target={action_pace_alt_window_why_signals['sandboxTarget']} ready={action_pace_alt_window_why_signals['sandboxReadiness']})",
        f"- ACTION PACE ALT WINDOW URGENCY: **{action_pace_alt_window_urgency}** ({action_pace_alt_window_urgency_signals['reason']}; flag={action_pace_alt_window_urgency_signals['flagName']} enabled={action_pace_alt_window_urgency_signals['flagEnabled']} alt={action_pace_alt_window_urgency_signals['actionPaceAltWindow']} conf={action_pace_alt_window_urgency_signals['actionPaceAltWindowConfidence']} fit={action_pace_alt_window_urgency_signals['actionPaceAltWindowFit']} why={action_pace_alt_window_urgency_signals['actionPaceAltWindowWhy']})",
        f"- ACTION PACE ALT WINDOW URGENCY Δ: **{action_pace_alt_window_urgency_drift:+d}** ({action_pace_alt_window_urgency_drift_signals['reason']}; current={action_pace_alt_window_urgency_drift_signals['currentUrgency']}({action_pace_alt_window_urgency_drift_signals['currentScore']}) prior={action_pace_alt_window_urgency_drift_signals['priorUrgency']}({action_pace_alt_window_urgency_drift_signals['priorScore']}) loaded={action_pace_alt_window_urgency_drift_signals['priorLoaded']})",
        f"- ACTION PACE ALT WINDOW STEP: **{action_pace_alt_window_step}** ({action_pace_alt_window_step_signals['reason']}; flag={action_pace_alt_window_step_signals['flagName']} enabled={action_pace_alt_window_step_signals['flagEnabled']} alt={action_pace_alt_window_step_signals['actionPaceAltWindow']} conf={action_pace_alt_window_step_signals['actionPaceAltWindowConfidence']} fit={action_pace_alt_window_step_signals['actionPaceAltWindowFit']} urgency={action_pace_alt_window_step_signals['actionPaceAltWindowUrgency']} sandbox={action_pace_alt_window_step_signals['routeSandbox']} target={action_pace_alt_window_step_signals['sandboxTarget']} ready={action_pace_alt_window_step_signals['sandboxReadiness']})",
        f"- ACTION PACE ALT WINDOW STEP Δ: **{action_pace_alt_window_step_drift:+d}** ({action_pace_alt_window_step_drift_signals['reason']}; current={action_pace_alt_window_step_drift_signals['currentStep']}({action_pace_alt_window_step_drift_signals['currentScore']}) prior={action_pace_alt_window_step_drift_signals['priorStep']}({action_pace_alt_window_step_drift_signals['priorScore']}) loaded={action_pace_alt_window_step_drift_signals['priorLoaded']})",
        f"- ACTION PACE ALT WINDOW STEP GLYPH: **{action_pace_alt_window_step_glyph}** ({action_pace_alt_window_step_glyph_signals['reason']}; flag={action_pace_alt_window_step_glyph_signals['flagName']} enabled={action_pace_alt_window_step_glyph_signals['flagEnabled']} step={action_pace_alt_window_step_glyph_signals['actionPaceAltWindowStep']} urgency={action_pace_alt_window_step_glyph_signals['actionPaceAltWindowUrgency']} fit={action_pace_alt_window_step_glyph_signals['actionPaceAltWindowFit']})",
        f"- ACTION PACE ALT WINDOW PULSE: **{action_pace_alt_window_pulse}** ({action_pace_alt_window_pulse_signals['reason']}; flag={action_pace_alt_window_pulse_signals['flagName']} enabled={action_pace_alt_window_pulse_signals['flagEnabled']} urgency={action_pace_alt_window_pulse_signals['actionPaceAltWindowUrgency']} fit={action_pace_alt_window_pulse_signals['actionPaceAltWindowFit']} conf={action_pace_alt_window_pulse_signals['actionPaceAltWindowConfidence']})",
        f"- ACTION PACE ALT WINDOW PULSE Δ: **{action_pace_alt_window_pulse_drift:+d}** ({action_pace_alt_window_pulse_drift_signals['reason']}; current={action_pace_alt_window_pulse_drift_signals['currentPulse']}({action_pace_alt_window_pulse_drift_signals['currentScore']}) prior={action_pace_alt_window_pulse_drift_signals['priorPulse']}({action_pace_alt_window_pulse_drift_signals['priorScore']}) loaded={action_pace_alt_window_pulse_drift_signals['priorLoaded']})",
        f"- ROUTE PULSE LINK: **{route_pulse_link}** ({route_pulse_link_signals['reason']}; flag={route_pulse_link_signals['flagName']} enabled={route_pulse_link_signals['flagEnabled']} pulse={route_pulse_link_signals['actionPaceAltWindowPulse']} drift={route_pulse_link_signals['actionPaceAltWindowPulseDrift']:+d} fit={route_pulse_link_signals['actionPaceAltWindowFit']})",
        f"- ROUTE PULSE LINK CONF: **{route_pulse_link_confidence}** ({route_pulse_link_confidence_signals['reason']}; link={route_pulse_link_confidence_signals['routePulseLink']} pulse={route_pulse_link_confidence_signals['actionPaceAltWindowPulse']} drift={route_pulse_link_confidence_signals['actionPaceAltWindowPulseDrift']:+d} fit={route_pulse_link_confidence_signals['actionPaceAltWindowFit']} altConf={route_pulse_link_confidence_signals['actionPaceAltWindowConfidence']})",
        f"- ROUTE PULSE LINK STREAK: **{route_pulse_link_streak}** ({route_pulse_link_streak_signals['reason']}; current={route_pulse_link_streak_signals['currentRoutePulseLink']} prior={route_pulse_link_streak_signals['priorRoutePulseLink']} priorStreak={route_pulse_link_streak_signals['priorStreak']} loaded={route_pulse_link_streak_signals['priorLoaded']})",
        f"- ROUTE PULSE LINK MODE: **{route_pulse_link_mode}** ({route_pulse_link_mode_signals['reason']}; link={route_pulse_link_mode_signals['routePulseLink']} streak={route_pulse_link_mode_signals['routePulseLinkStreak']} drift={route_pulse_link_mode_signals['actionPaceAltWindowPulseDrift']:+d})",
        f"- ROUTE PULSE LINK MODE Δ: **{route_pulse_link_mode_drift:+d}** ({route_pulse_link_mode_drift_signals['reason']}; current={route_pulse_link_mode_drift_signals['currentMode']}({route_pulse_link_mode_drift_signals['currentScore']}) prior={route_pulse_link_mode_drift_signals['priorMode']}({route_pulse_link_mode_drift_signals['priorScore']}) loaded={route_pulse_link_mode_drift_signals['priorLoaded']})",
        f"- ROUTE PULSE LINK MODE STREAK: **{route_pulse_link_mode_stability_streak}** ({route_pulse_link_mode_stability_streak_signals['reason']}; current={route_pulse_link_mode_stability_streak_signals['currentMode']} prior={route_pulse_link_mode_stability_streak_signals['priorMode']} priorStreak={route_pulse_link_mode_stability_streak_signals['priorStreak']} loaded={route_pulse_link_mode_stability_streak_signals['priorLoaded']})",
        f"- ROUTE PULSE LINK MODE WHY: **{route_pulse_link_mode_why}** ({route_pulse_link_mode_why_signals['reason']}; flag={route_pulse_link_mode_why_signals['flagName']} enabled={route_pulse_link_mode_why_signals['flagEnabled']} mode={route_pulse_link_mode_why_signals['routePulseLinkMode']} link={route_pulse_link_mode_why_signals['routePulseLink']} drift={route_pulse_link_mode_why_signals['routePulseLinkModeDrift']:+d} streak={route_pulse_link_mode_why_signals['routePulseLinkStreak']})",
        f"- ROUTE PULSE LINK MODE FIT: **{route_pulse_link_mode_fit}** ({route_pulse_link_mode_fit_signals['reason']}; mode={route_pulse_link_mode_fit_signals['routePulseLinkMode']} drift={route_pulse_link_mode_fit_signals['routePulseLinkModeDrift']:+d} streak={route_pulse_link_mode_fit_signals['routePulseLinkModeStabilityStreak']})",
        f"- ACTION PACE WHY: **{action_pace_why}** ({action_pace_why_signals['reason']}; flag={action_pace_why_signals['flagName']} enabled={action_pace_why_signals['flagEnabled']} pace={action_pace_why_signals['actionPace']} guard={action_pace_why_signals['actionGuard']} stability={action_pace_why_signals['actionStability']} lag={action_pace_why_signals['pressureLag']} drift={action_pace_why_signals['paceDrift']:+d})",
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
        f"- WHAT-IF SPLIT ESC PRESSURE: **{what_if_split_esc_pressure}** ({what_if_split_esc_pressure_signals['reason']}; flag={what_if_split_esc_pressure_signals['flagName']} enabled={what_if_split_esc_pressure_signals['flagEnabled']} state={what_if_split_esc_pressure_signals['splitEscState']} cool={what_if_split_esc_pressure_signals['splitEscCool']} pressure={what_if_split_esc_pressure_signals['pressureBand']})",
        f"- WHAT-IF SPLIT ESC RECOVER: **{what_if_split_esc_recover}** ({what_if_split_esc_recover_signals['reason']}; flag={what_if_split_esc_recover_signals['flagName']} enabled={what_if_split_esc_recover_signals['flagEnabled']} state={what_if_split_esc_recover_signals['splitEscState']} lanes={what_if_split_esc_recover_signals['splitEscLanes']})",
        f"- WHAT-IF SPLIT ESC RECOVER CONF: **{what_if_split_esc_recover_confidence}** ({what_if_split_esc_recover_confidence_signals['reason']}; recover={what_if_split_esc_recover_confidence_signals['splitEscRecover']} state={what_if_split_esc_recover_confidence_signals['splitEscState']} pressure={what_if_split_esc_recover_confidence_signals['splitEscPressure']} lanes={what_if_split_esc_recover_confidence_signals['splitEscLanes']})",
        f"- WHAT-IF SPLIT ESC RECOVER ALT: **{what_if_split_esc_recover_alt}** ({what_if_split_esc_recover_alt_signals['reason']}; flag={what_if_split_esc_recover_alt_signals['flagName']} enabled={what_if_split_esc_recover_alt_signals['flagEnabled']} recover={what_if_split_esc_recover_alt_signals['splitEscRecover']} state={what_if_split_esc_recover_alt_signals['splitEscState']} lanes={what_if_split_esc_recover_alt_signals['splitEscLanes']})",
        f"- WHAT-IF SPLIT ESC RECOVER ALT CONF: **{what_if_split_esc_recover_alt_confidence}** ({what_if_split_esc_recover_alt_confidence_signals['reason']}; recoverAlt={what_if_split_esc_recover_alt_confidence_signals['splitEscRecoverAlt']} state={what_if_split_esc_recover_alt_confidence_signals['splitEscState']} pressure={what_if_split_esc_recover_alt_confidence_signals['splitEscPressure']} lanes={what_if_split_esc_recover_alt_confidence_signals['splitEscLanes']})",
        f"- WHAT-IF SPLIT ESC RECOVER PLAN: **{what_if_split_esc_recover_plan}** ({what_if_split_esc_recover_plan_signals['reason']}; primary={what_if_split_esc_recover_plan_signals['splitEscRecover']} alt={what_if_split_esc_recover_plan_signals['splitEscRecoverAlt']} hasPrimary={what_if_split_esc_recover_plan_signals['hasPrimary']} hasAlt={what_if_split_esc_recover_plan_signals['hasAlt']})",
        f"- WHAT-IF SPLIT ESC RECOVER WHY: **{what_if_split_esc_recover_why}** ({what_if_split_esc_recover_why_signals['reason']}; flag={what_if_split_esc_recover_why_signals['flagName']} enabled={what_if_split_esc_recover_why_signals['flagEnabled']} plan={what_if_split_esc_recover_why_signals['splitEscRecoverPlan']} conf={what_if_split_esc_recover_why_signals['splitEscRecoverConfidence']} pressure={what_if_split_esc_recover_why_signals['splitEscPressure']})",
        f"- WHAT-IF SPLIT ESC RECOVER TEMPO: **{what_if_split_esc_recover_tempo}** ({what_if_split_esc_recover_tempo_signals['reason']}; plan={what_if_split_esc_recover_tempo_signals['splitEscRecoverPlan']} conf={what_if_split_esc_recover_tempo_signals['splitEscRecoverConfidence']} pressure={what_if_split_esc_recover_tempo_signals['splitEscPressure']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO: **{what_if_split_esc_recover_veto}** ({what_if_split_esc_recover_veto_signals['reason']}; flag={what_if_split_esc_recover_veto_signals['flagName']} enabled={what_if_split_esc_recover_veto_signals['flagEnabled']} conf={what_if_split_esc_recover_veto_signals['splitEscRecoverConfidence']} pressure={what_if_split_esc_recover_veto_signals['splitEscPressure']} plan={what_if_split_esc_recover_veto_signals['splitEscRecoverPlan']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO CONF: **{what_if_split_esc_recover_veto_confidence}** ({what_if_split_esc_recover_veto_confidence_signals['reason']}; veto={what_if_split_esc_recover_veto_confidence_signals['splitEscRecoverVeto']} conf={what_if_split_esc_recover_veto_confidence_signals['splitEscRecoverConfidence']} pressure={what_if_split_esc_recover_veto_confidence_signals['splitEscPressure']} plan={what_if_split_esc_recover_veto_confidence_signals['splitEscRecoverPlan']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO WHY: **{what_if_split_esc_recover_veto_why}** ({what_if_split_esc_recover_veto_why_signals['reason']}; flag={what_if_split_esc_recover_veto_why_signals['flagName']} enabled={what_if_split_esc_recover_veto_why_signals['flagEnabled']} veto={what_if_split_esc_recover_veto_why_signals['splitEscRecoverVeto']} conf={what_if_split_esc_recover_veto_why_signals['splitEscRecoverVetoConfidence']} pressure={what_if_split_esc_recover_veto_why_signals['splitEscPressure']} plan={what_if_split_esc_recover_veto_why_signals['splitEscRecoverPlan']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO COOLOFF: **{what_if_split_esc_recover_veto_cooloff}** ({what_if_split_esc_recover_veto_cooloff_signals['reason']}; flag={what_if_split_esc_recover_veto_cooloff_signals['flagName']} enabled={what_if_split_esc_recover_veto_cooloff_signals['flagEnabled']} active={what_if_split_esc_recover_veto_cooloff_signals['active']} prior={what_if_split_esc_recover_veto_cooloff_signals['priorVeto']}:{what_if_split_esc_recover_veto_cooloff_signals['priorCooloff']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO STATE: **{what_if_split_esc_recover_veto_state}** ({what_if_split_esc_recover_veto_state_signals['reason']}; veto={what_if_split_esc_recover_veto_state_signals['splitEscRecoverVeto']} cooloff={what_if_split_esc_recover_veto_state_signals['splitEscRecoverVetoCooloff']} cooling={what_if_split_esc_recover_veto_state_signals['cooling']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO DWELL: **{what_if_split_esc_recover_veto_dwell}** ({what_if_split_esc_recover_veto_dwell_signals['reason']}; state={what_if_split_esc_recover_veto_dwell_signals['currentState']} prior={what_if_split_esc_recover_veto_dwell_signals['priorState']}:{what_if_split_esc_recover_veto_dwell_signals['priorDwell']} loaded={what_if_split_esc_recover_veto_dwell_signals['priorLoaded']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO RELEASE: **{what_if_split_esc_recover_veto_release}** ({what_if_split_esc_recover_veto_release_signals['reason']}; flag={what_if_split_esc_recover_veto_release_signals['flagName']} enabled={what_if_split_esc_recover_veto_release_signals['flagEnabled']} current={what_if_split_esc_recover_veto_release_signals['currentState']} prior={what_if_split_esc_recover_veto_release_signals['priorState']} loaded={what_if_split_esc_recover_veto_release_signals['priorLoaded']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO RELEASE CONF: **{what_if_split_esc_recover_veto_release_confidence}** ({what_if_split_esc_recover_veto_release_confidence_signals['reason']}; release={what_if_split_esc_recover_veto_release_confidence_signals['splitEscRecoverVetoRelease']} state={what_if_split_esc_recover_veto_release_confidence_signals['splitEscRecoverVetoState']} dwell={what_if_split_esc_recover_veto_release_confidence_signals['splitEscRecoverVetoDwell']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO RELEASE ROUTE: **{what_if_split_esc_recover_veto_release_route}** ({what_if_split_esc_recover_veto_release_route_signals['reason']}; release={what_if_split_esc_recover_veto_release_route_signals['splitEscRecoverVetoRelease']} state={what_if_split_esc_recover_veto_release_route_signals['splitEscRecoverVetoState']} plan={what_if_split_esc_recover_veto_release_route_signals['splitEscRecoverPlan']} primary={what_if_split_esc_recover_veto_release_route_signals['splitEscRecover']} alt={what_if_split_esc_recover_veto_release_route_signals['splitEscRecoverAlt']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO RELEASE TICK: **{what_if_split_esc_recover_veto_release_tick}** ({what_if_split_esc_recover_veto_release_tick_signals['reason']}; flag={what_if_split_esc_recover_veto_release_tick_signals['flagName']} enabled={what_if_split_esc_recover_veto_release_tick_signals['flagEnabled']} release={what_if_split_esc_recover_veto_release_tick_signals['currentRelease']} state={what_if_split_esc_recover_veto_release_tick_signals['currentState']} prior={what_if_split_esc_recover_veto_release_tick_signals['priorRelease']}:{what_if_split_esc_recover_veto_release_tick_signals['priorState']}:{what_if_split_esc_recover_veto_release_tick_signals['priorTick']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO RELEASE PHASE: **{what_if_split_esc_recover_veto_release_tick_phase}** ({what_if_split_esc_recover_veto_release_tick_phase_signals['reason']}; tick={what_if_split_esc_recover_veto_release_tick_phase_signals['tick']} numeric={what_if_split_esc_recover_veto_release_tick_phase_signals['numeric']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO RELEASE CADENCE: **{what_if_split_esc_recover_veto_release_cadence}** ({what_if_split_esc_recover_veto_release_cadence_signals['reason']}; tick={what_if_split_esc_recover_veto_release_cadence_signals['tick']} prior={what_if_split_esc_recover_veto_release_cadence_signals['priorTick']} delta={what_if_split_esc_recover_veto_release_cadence_signals['delta']} numeric={what_if_split_esc_recover_veto_release_cadence_signals['numeric']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO REARM: **{what_if_split_esc_recover_veto_rearm}** ({what_if_split_esc_recover_veto_rearm_signals['reason']}; flag={what_if_split_esc_recover_veto_rearm_signals['flagName']} enabled={what_if_split_esc_recover_veto_rearm_signals['flagEnabled']} phase={what_if_split_esc_recover_veto_rearm_signals['releaseTickPhase']} pressure={what_if_split_esc_recover_veto_rearm_signals['splitEscPressure']} cadence={what_if_split_esc_recover_veto_rearm_signals['releaseCadence']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO REARM CONF: **{what_if_split_esc_recover_veto_rearm_confidence}** ({what_if_split_esc_recover_veto_rearm_confidence_signals['reason']}; rearm={what_if_split_esc_recover_veto_rearm_confidence_signals['splitEscRecoverVetoRearm']} phase={what_if_split_esc_recover_veto_rearm_confidence_signals['releaseTickPhase']} pressure={what_if_split_esc_recover_veto_rearm_confidence_signals['splitEscPressure']} cadence={what_if_split_esc_recover_veto_rearm_confidence_signals['releaseCadence']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO REARM WHY: **{what_if_split_esc_recover_veto_rearm_why}** ({what_if_split_esc_recover_veto_rearm_why_signals['reason']}; flag={what_if_split_esc_recover_veto_rearm_why_signals['flagName']} enabled={what_if_split_esc_recover_veto_rearm_why_signals['flagEnabled']} rearm={what_if_split_esc_recover_veto_rearm_why_signals['splitEscRecoverVetoRearm']} conf={what_if_split_esc_recover_veto_rearm_why_signals['splitEscRecoverVetoRearmConfidence']} pressure={what_if_split_esc_recover_veto_rearm_why_signals['splitEscPressure']} phase={what_if_split_esc_recover_veto_rearm_why_signals['releaseTickPhase']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO REARM COOLOFF: **{what_if_split_esc_recover_veto_rearm_cooloff}** ({what_if_split_esc_recover_veto_rearm_cooloff_signals['reason']}; flag={what_if_split_esc_recover_veto_rearm_cooloff_signals['flagName']} enabled={what_if_split_esc_recover_veto_rearm_cooloff_signals['flagEnabled']} active={what_if_split_esc_recover_veto_rearm_cooloff_signals['active']} prior={what_if_split_esc_recover_veto_rearm_cooloff_signals['priorRearm']}:{what_if_split_esc_recover_veto_rearm_cooloff_signals['priorCooloff']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO REARM COOLOFF STATE: **{what_if_split_esc_recover_veto_rearm_cooloff_state}** ({what_if_split_esc_recover_veto_rearm_cooloff_state_signals['reason']}; rearm={what_if_split_esc_recover_veto_rearm_cooloff_state_signals['splitEscRecoverVetoRearm']} cooloff={what_if_split_esc_recover_veto_rearm_cooloff_state_signals['splitEscRecoverVetoRearmCooloff']} active={what_if_split_esc_recover_veto_rearm_cooloff_state_signals['active']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO REARM FIT: **{what_if_split_esc_recover_veto_rearm_fit}** ({what_if_split_esc_recover_veto_rearm_fit_signals['reason']}; state={what_if_split_esc_recover_veto_rearm_fit_signals['splitEscRecoverVetoRearmCooloffState']} cooloff={what_if_split_esc_recover_veto_rearm_fit_signals['splitEscRecoverVetoRearmCooloff']} pressure={what_if_split_esc_recover_veto_rearm_fit_signals['splitEscPressure']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE: **{what_if_split_esc_recover_veto_rearm_nudge}** ({what_if_split_esc_recover_veto_rearm_nudge_signals['reason']}; flag={what_if_split_esc_recover_veto_rearm_nudge_signals['flagName']} enabled={what_if_split_esc_recover_veto_rearm_nudge_signals['flagEnabled']} rearm={what_if_split_esc_recover_veto_rearm_nudge_signals['splitEscRecoverVetoRearm']} conf={what_if_split_esc_recover_veto_rearm_nudge_signals['splitEscRecoverVetoRearmConfidence']} fit={what_if_split_esc_recover_veto_rearm_nudge_signals['splitEscRecoverVetoRearmFit']} state={what_if_split_esc_recover_veto_rearm_nudge_signals['splitEscRecoverVetoRearmCooloffState']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE WINDOW: **{what_if_split_esc_recover_veto_rearm_nudge_window}** ({what_if_split_esc_recover_veto_rearm_nudge_window_signals['reason']}; rearm={what_if_split_esc_recover_veto_rearm_nudge_window_signals['splitEscRecoverVetoRearm']} cooloffState={what_if_split_esc_recover_veto_rearm_nudge_window_signals['splitEscRecoverVetoRearmCooloffState']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE CONF: **{what_if_split_esc_recover_veto_rearm_nudge_confidence}** ({what_if_split_esc_recover_veto_rearm_nudge_confidence_signals['reason']}; nudge={what_if_split_esc_recover_veto_rearm_nudge_confidence_signals['splitEscRecoverVetoRearmNudge']} rearmConf={what_if_split_esc_recover_veto_rearm_nudge_confidence_signals['splitEscRecoverVetoRearmConfidence']} fit={what_if_split_esc_recover_veto_rearm_nudge_confidence_signals['splitEscRecoverVetoRearmFit']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE WHY: **{what_if_split_esc_recover_veto_rearm_nudge_why}** ({what_if_split_esc_recover_veto_rearm_nudge_why_signals['reason']}; flag={what_if_split_esc_recover_veto_rearm_nudge_why_signals['flagName']} enabled={what_if_split_esc_recover_veto_rearm_nudge_why_signals['flagEnabled']} nudge={what_if_split_esc_recover_veto_rearm_nudge_why_signals['splitEscRecoverVetoRearmNudge']} conf={what_if_split_esc_recover_veto_rearm_nudge_why_signals['splitEscRecoverVetoRearmNudgeConfidence']} window={what_if_split_esc_recover_veto_rearm_nudge_why_signals['splitEscRecoverVetoRearmNudgeWindow']} fit={what_if_split_esc_recover_veto_rearm_nudge_why_signals['splitEscRecoverVetoRearmFit']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE IMPACT: **{what_if_split_esc_recover_veto_rearm_nudge_impact}** ({what_if_split_esc_recover_veto_rearm_nudge_impact_signals['reason']}; nudge={what_if_split_esc_recover_veto_rearm_nudge_impact_signals['splitEscRecoverVetoRearmNudge']} window={what_if_split_esc_recover_veto_rearm_nudge_impact_signals['splitEscRecoverVetoRearmNudgeWindow']} fit={what_if_split_esc_recover_veto_rearm_nudge_impact_signals['splitEscRecoverVetoRearmFit']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE DRIFT: **{what_if_split_esc_recover_veto_rearm_nudge_drift}** ({what_if_split_esc_recover_veto_rearm_nudge_drift_signals['reason']}; current={what_if_split_esc_recover_veto_rearm_nudge_drift_signals['currentNudgeWhy']} prior={what_if_split_esc_recover_veto_rearm_nudge_drift_signals['priorNudgeWhy']} loaded={what_if_split_esc_recover_veto_rearm_nudge_drift_signals['priorLoaded']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO REARM COACH: **{what_if_split_esc_recover_veto_rearm_coach}** ({what_if_split_esc_recover_veto_rearm_coach_signals['reason']}; flag={what_if_split_esc_recover_veto_rearm_coach_signals['flagName']} enabled={what_if_split_esc_recover_veto_rearm_coach_signals['flagEnabled']} primary={what_if_split_esc_recover_veto_rearm_coach_signals['splitEscRecover']} backup={what_if_split_esc_recover_veto_rearm_coach_signals['splitEscRecoverAlt']} plan={what_if_split_esc_recover_veto_rearm_coach_signals['splitEscRecoverPlan']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO REARM COACH CONF: **{what_if_split_esc_recover_veto_rearm_coach_confidence}** ({what_if_split_esc_recover_veto_rearm_coach_confidence_signals['reason']}; coach={what_if_split_esc_recover_veto_rearm_coach_confidence_signals['splitEscRecoverVetoRearmCoach']} nudgeConf={what_if_split_esc_recover_veto_rearm_coach_confidence_signals['splitEscRecoverVetoRearmNudgeConfidence']} fit={what_if_split_esc_recover_veto_rearm_coach_confidence_signals['splitEscRecoverVetoRearmFit']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO REARM COACH MODE: **{what_if_split_esc_recover_veto_rearm_coach_mode}** ({what_if_split_esc_recover_veto_rearm_coach_mode_signals['reason']}; coach={what_if_split_esc_recover_veto_rearm_coach_mode_signals['splitEscRecoverVetoRearmCoach']} primary={what_if_split_esc_recover_veto_rearm_coach_mode_signals['coachPrimaryLane']} backup={what_if_split_esc_recover_veto_rearm_coach_mode_signals['coachBackupLane']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO REARM COACH WHY: **{what_if_split_esc_recover_veto_rearm_coach_why}** ({what_if_split_esc_recover_veto_rearm_coach_why_signals['reason']}; flag={what_if_split_esc_recover_veto_rearm_coach_why_signals['flagName']} enabled={what_if_split_esc_recover_veto_rearm_coach_why_signals['flagEnabled']} coach={what_if_split_esc_recover_veto_rearm_coach_why_signals['splitEscRecoverVetoRearmCoach']} mode={what_if_split_esc_recover_veto_rearm_coach_why_signals['splitEscRecoverVetoRearmCoachMode']} conf={what_if_split_esc_recover_veto_rearm_coach_why_signals['splitEscRecoverVetoRearmCoachConfidence']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO REARM COACH HANDOFF: **{what_if_split_esc_recover_veto_rearm_coach_handoff}** ({what_if_split_esc_recover_veto_rearm_coach_handoff_signals['reason']}; coach={what_if_split_esc_recover_veto_rearm_coach_handoff_signals['splitEscRecoverVetoRearmCoach']} mode={what_if_split_esc_recover_veto_rearm_coach_handoff_signals['splitEscRecoverVetoRearmCoachMode']} conf={what_if_split_esc_recover_veto_rearm_coach_handoff_signals['splitEscRecoverVetoRearmCoachConfidence']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO REARM COACH HANDOFF FIT: **{what_if_split_esc_recover_veto_rearm_coach_handoff_fit}** ({what_if_split_esc_recover_veto_rearm_coach_handoff_fit_signals['reason']}; handoff={what_if_split_esc_recover_veto_rearm_coach_handoff_fit_signals['splitEscRecoverVetoRearmCoachHandoff']} pressure={what_if_split_esc_recover_veto_rearm_coach_handoff_fit_signals['splitEscPressure']})",
        f"- WHAT-IF SPLIT ESC RECOVER VETO REARM COACH HANDOFF WHY: **{what_if_split_esc_recover_veto_rearm_coach_handoff_why}** ({what_if_split_esc_recover_veto_rearm_coach_handoff_why_signals['reason']}; flag={what_if_split_esc_recover_veto_rearm_coach_handoff_why_signals['flagName']} enabled={what_if_split_esc_recover_veto_rearm_coach_handoff_why_signals['flagEnabled']} handoff={what_if_split_esc_recover_veto_rearm_coach_handoff_why_signals['splitEscRecoverVetoRearmCoachHandoff']} fit={what_if_split_esc_recover_veto_rearm_coach_handoff_why_signals['splitEscRecoverVetoRearmCoachHandoffFit']} conf={what_if_split_esc_recover_veto_rearm_coach_handoff_why_signals['splitEscRecoverVetoRearmCoachConfidence']})",
        f"- WHAT-IF SPLIT ESC RECOVER ΔCONF: **{what_if_split_esc_recover_confidence_delta}** ({what_if_split_esc_recover_confidence_delta_signals['reason']}; current={what_if_split_esc_recover_confidence_delta_signals['currentConfidence']} prior={what_if_split_esc_recover_confidence_delta_signals['priorConfidence']} loaded={what_if_split_esc_recover_confidence_delta_signals['priorLoaded']})",
        f"- STICKY TOKENS: **{len(sticky_tokens)}**",
        f"- ANOMALY: **{anomaly_pulse}** (sticky={anomaly_pulse_signals['stickyCount']}/{anomaly_pulse_signals['stickyThreshold']} pressure={anomaly_pulse_signals['pressureChurn']}/{anomaly_pulse_signals['pressureThreshold']})",
        f"- ANOMALY CONF: **{anomaly_confidence}** (triggers={anomaly_pulse_signals['triggerCount']} gap={anomaly_pulse_signals['combinedGap']})",
        f"- ROUTE VIBE DRIFT: **CALM {route_vibe_totals['net']['CALM']:+d} | EDGE {route_vibe_totals['net']['EDGE']:+d} | DOOM {route_vibe_totals['net']['DOOM']:+d}**",
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
        "## Route Vibe Drift (added/removed/net)",
        f"- CALM: +{route_vibe_totals['added']['CALM']} / -{route_vibe_totals['removed']['CALM']} / net {route_vibe_totals['net']['CALM']}",
        f"- EDGE: +{route_vibe_totals['added']['EDGE']} / -{route_vibe_totals['removed']['EDGE']} / net {route_vibe_totals['net']['EDGE']}",
        f"- DOOM: +{route_vibe_totals['added']['DOOM']} / -{route_vibe_totals['removed']['DOOM']} / net {route_vibe_totals['net']['DOOM']}",
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
