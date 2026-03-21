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
    pressure_lag, pressure_lag_signals = pressure_latency_from_signals(
        pressure_churn=drift_risk_signals["pressureChurn"],
        drift_momentum=drift_momentum,
        drift_momentum_delta=drift_momentum_signals["delta"],
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
        "pressureLag": pressure_lag,
        "pressureLagSignals": pressure_lag_signals,
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
        f"- PRESSURE LAG: **{pressure_lag}** (churn={pressure_lag_signals['pressureChurn']} momentum={pressure_lag_signals['driftMomentum']} |Δ|={pressure_lag_signals['absDriftDelta']})",
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
