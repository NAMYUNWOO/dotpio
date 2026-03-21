#!/usr/bin/env python3
"""Regression checks for weekly_portal_prompt_readability_drift.py."""
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

from weekly_portal_prompt_readability_drift import sandbox_cooloff_from_prior

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "weekly_portal_prompt_readability_drift.py"


def run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=cwd, check=True, stdout=subprocess.DEVNULL)


def run_output(cmd: list[str], cwd: Path) -> str:
    return subprocess.check_output(cmd, cwd=cwd, text=True)


def commit_all(repo: Path, message: str) -> None:
    run(["git", "add", "-A"], repo)
    run(["git", "commit", "-m", message], repo)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="portal-prompt-drift-reg-") as td:
        repo = Path(td)
        run(["git", "init"], repo)
        run(["git", "config", "user.email", "reg@example.com"], repo)
        run(["git", "config", "user.name", "Regression Bot"], repo)

        (repo / "src").mkdir(parents=True, exist_ok=True)
        (repo / "src" / "portal.lua").write_text(
            'return "PORTAL READY -> ENTER:JUMP  NEXT ROUTE:SAFE  COACH:LOW PRESSURE  PRESSURE:1"\n',
            encoding="utf-8",
        )
        commit_all(repo, "feat: add detailed portal prompt")

        (repo / "src" / "portal.lua").write_text(
            'return "PORTAL READY -> ENTER:JUMP  NEXT:SAFE  COACH:LOW  P:1  ALT:RISK  ADEL:-1  AP:LOW"\n',
            encoding="utf-8",
        )
        commit_all(repo, "feat: compact portal prompt")

        out_json = repo / "out.json"
        out_md = repo / "out.md"

        run_output(
            [
                "python3",
                str(SCRIPT),
                "--since-days",
                "3650",
                "--max-commits",
                "20",
                "--out-json",
                str(out_json),
                "--out-md",
                str(out_md),
            ],
            repo,
        )

        payload = json.loads(out_json.read_text(encoding="utf-8"))
        assert payload["checkedCommits"] >= 2, payload
        assert payload["portalPromptCommits"] >= 2, payload
        assert payload["totals"]["added"]["compact"] > 0, payload
        assert payload["totals"]["added"]["detailed"] > 0, payload
        assert payload["modeTrend"] in {"COMPACT", "DETAILED", "BALANCED"}, payload
        assert payload["pressureBand"] in {"LOW", "MID", "HIGH"}, payload
        assert payload["driftRisk"] in {"LOW", "MID", "HIGH"}, payload
        assert set(payload["driftRiskSignals"].keys()) == {"score", "imbalance", "pressureChurn"}, payload
        assert payload["laneFocus"] in {"PORTAL", "ALT", "PRESSURE", "MIXED"}, payload
        assert set(payload["laneFocusScores"].keys()) == {"portal", "alt", "pressure"}, payload
        assert isinstance(payload.get("focusStreak"), int) and payload["focusStreak"] >= 0, payload
        assert isinstance(payload.get("focusShift"), str) and "->" in payload["focusShift"], payload
        assert payload.get("focusVolatility") in {"STEADY", "SWING"}, payload
        assert set(payload.get("focusVolatilitySignals", {}).keys()) == {"switches", "edges", "switchRatio"}, payload
        assert payload["routeAction"] in {"PORTAL_AUDIT", "ALT_TUNE", "PRESSURE_REBASE", "BALANCE_PASS", "WATCH"}, payload
        assert isinstance(payload["routeActionReason"], str) and payload["routeActionReason"], payload
        assert payload.get("routeActionConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("routeActionConfidenceSignals", {}).keys()) == {
            "topScore",
            "secondScore",
            "totalScore",
            "dominanceRatio",
            "focusSpread",
            "driftSpread",
        }, payload
        assert isinstance(payload.get("focusBalance"), str) and payload["focusBalance"].endswith("%"), payload
        assert set(payload.get("focusBalanceSignals", {}).keys()) == {
            "topScore",
            "totalScore",
            "dominanceRatio",
            "percent",
        }, payload
        assert payload.get("focusEntropy") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("focusEntropySignals", {}).keys()) == {
            "raw",
            "normalized",
            "maxEntropy",
            "totalScore",
        }, payload
        assert payload.get("actionGuard") in {"LOCK", "SOFT"}, payload
        assert set(payload.get("actionGuardSignals", {}).keys()) == {
            "armed",
            "reason",
            "driftRisk",
            "actionConfidence",
        }, payload
        assert isinstance(payload.get("laneLock"), str), payload
        assert set(payload.get("laneLockSignals", {}).keys()) == {"threshold", "armed", "lane", "streak"}, payload
        assert payload.get("routeSandbox") in {"ON", "OFF"}, payload
        assert set(payload.get("routeSandboxSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "laneLockArmed",
            "laneLock",
            "laneLockStreak",
            "threshold",
            "reason",
        }, payload
        assert payload.get("routeSandboxPlan") in {"SIMULATE", "PROBE", "PREPARE", "HOLD"}, payload
        assert set(payload.get("routeSandboxPlanSignals", {}).keys()) == {
            "routeSandbox",
            "actionGuard",
            "driftRisk",
            "reason",
        }, payload
        assert payload.get("sandboxTarget") in {"PORTAL", "ALT", "PRESSURE", "MIXED", "NONE"}, payload
        assert set(payload.get("sandboxTargetSignals", {}).keys()) == {
            "routeSandbox",
            "lane",
            "laneLockArmed",
            "laneLockStreak",
            "targetSource",
            "reason",
        }, payload
        assert payload.get("sandboxTargetSource") in {"LOCK", "MIXED", "NONE"}, payload
        assert payload.get("sandboxTargetConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("sandboxTargetConfidenceSignals", {}).keys()) == {
            "sandboxTarget",
            "routeActionConfidence",
            "laneLockArmed",
            "laneLockStreak",
            "reason",
        }, payload
        assert payload.get("sandboxReadiness") in {"IDLE", "PRIMED", "ARMED"}, payload
        assert set(payload.get("sandboxReadinessSignals", {}).keys()) == {
            "routeSandbox",
            "sandboxTargetConfidence",
            "actionGuard",
            "laneLockArmed",
            "laneLockStreak",
            "reason",
        }, payload
        assert isinstance(payload.get("sandboxTargetShift"), str) and "->" in payload["sandboxTargetShift"], payload
        assert set(payload.get("sandboxTargetShiftSignals", {}).keys()) == {
            "priorTarget",
            "currentTarget",
            "changed",
            "priorLoaded",
            "reason",
        }, payload
        assert isinstance(payload.get("sandboxCooloff"), int) and payload["sandboxCooloff"] >= 0, payload
        assert set(payload.get("sandboxCooloffSignals", {}).keys()) == {
            "active",
            "currentSandbox",
            "priorSandbox",
            "priorCooloff",
            "priorLoaded",
            "reason",
        }, payload
        assert payload["sandboxCooloffSignals"]["currentSandbox"] in {"ON", "OFF"}, payload
        assert payload.get("driftMomentum") in {"RISING", "COOLING", "FLAT"}, payload
        assert set(payload.get("driftMomentumSignals", {}).keys()) == {"recentAvg", "olderAvg", "delta", "recentCount", "olderCount"}, payload
        assert payload.get("actionStability") in {"LOCKED", "WATCH"}, payload
        assert set(payload.get("actionStabilitySignals", {}).keys()) == {
            "routeActionConfidence",
            "focusVolatility",
            "driftMomentum",
            "stableConfidence",
            "steadyFocus",
            "stableMomentum",
            "reason",
        }, payload
        assert payload.get("pressureLag") in {"FAST", "STABLE", "SLOW"}, payload
        assert set(payload.get("pressureLagSignals", {}).keys()) == {
            "pressureChurn",
            "driftMomentum",
            "driftDelta",
            "absDriftDelta",
        }, payload
        assert isinstance(payload.get("whatIfAlt"), str), payload
        assert set(payload.get("whatIfAltSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "currentLane",
            "altLane",
            "baselineRisk",
            "imbalance",
            "pressureChurn",
            "projectedRisk",
            "deltaRisk",
            "reason",
        }, payload
        assert payload.get("whatIfConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("whatIfConfidenceSignals", {}).keys()) == {
            "flagEnabled",
            "deltaRisk",
            "currentLane",
            "altLane",
            "routeActionConfidence",
            "reason",
        }, payload
        assert payload.get("whatIfAlign") in {"ALIGNED", "DIVERGED"}, payload
        assert set(payload.get("whatIfAlignSignals", {}).keys()) == {
            "flagEnabled",
            "routeAction",
            "routeActionLane",
            "altLane",
            "reason",
        }, payload
        assert payload.get("whatIfBand") in {"GAIN", "NEUTRAL", "LOSS"}, payload
        assert set(payload.get("whatIfBandSignals", {}).keys()) == {
            "flagEnabled",
            "deltaRisk",
            "currentLane",
            "altLane",
            "reason",
        }, payload
        assert payload.get("whatIfMagnitude") in {"SMALL", "MED", "LARGE"}, payload
        assert set(payload.get("whatIfMagnitudeSignals", {}).keys()) == {
            "flagEnabled",
            "deltaRisk",
            "absDeltaRisk",
            "reason",
        }, payload
        assert payload.get("whatIfFit") in {"SAFE", "EVEN", "TENSE"}, payload
        assert set(payload.get("whatIfFitSignals", {}).keys()) == {
            "flagEnabled",
            "pressureBand",
            "projectedRisk",
            "projectedBand",
            "reason",
        }, payload
        assert payload.get("whatIfFallback") in {"OFF", "NONE", "PORTAL", "ALT", "PRESSURE"}, payload
        assert set(payload.get("whatIfFallbackSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "whatIfAlign",
            "altLane",
            "routeAction",
            "routeActionLane",
            "reason",
        }, payload
        assert payload.get("whatIfFallbackConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("whatIfFallbackConfidenceSignals", {}).keys()) == {
            "flagEnabled",
            "fallback",
            "whatIfAlign",
            "deltaRisk",
            "routeActionConfidence",
            "reason",
        }, payload
        assert payload.get("whatIfFallbackFit") in {"SAFE", "EVEN", "TENSE"}, payload
        assert set(payload.get("whatIfFallbackFitSignals", {}).keys()) == {
            "flagEnabled",
            "fallback",
            "pressureBand",
            "baselineRisk",
            "projectedRisk",
            "projectedBand",
            "reason",
        }, payload
        assert isinstance(payload.get("whatIfFallbackWhy"), str), payload
        assert set(payload.get("whatIfFallbackWhySignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "fallback",
            "fallbackConfidence",
            "fallbackFit",
            "pressureBand",
            "reason",
        }, payload
        assert payload.get("whatIfFallbackAlign") in {"SYNC", "ASYNC"}, payload
        assert set(payload.get("whatIfFallbackAlignSignals", {}).keys()) == {
            "fallback",
            "laneFocus",
            "actionable",
            "reason",
        }, payload
        assert payload.get("whatIfFallbackMagnitude") in {"SMALL", "MED", "LARGE"}, payload
        assert set(payload.get("whatIfFallbackMagnitudeSignals", {}).keys()) == {
            "flagEnabled",
            "fallback",
            "deltaRisk",
            "absDeltaRisk",
            "reason",
        }, payload
        assert isinstance(payload.get("whatIfFallbackAlt2"), str), payload
        assert set(payload.get("whatIfFallbackAlt2Signals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "fallback",
            "fallbackLane",
            "portalScore",
            "altScore",
            "pressureScore",
            "topScore",
            "secondScore",
            "minTopScore",
            "minGap",
            "reason",
        }, payload
        assert payload.get("whatIfFallbackAlt2Confidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("whatIfFallbackAlt2ConfidenceSignals", {}).keys()) == {
            "flagEnabled",
            "alt2",
            "fallbackLane",
            "topScore",
            "secondScore",
            "scoreGap",
            "reason",
        }, payload
        assert payload.get("whatIfFallbackPlan") in {"PRIMARY", "SECONDARY", "HOLD"}, payload
        assert set(payload.get("whatIfFallbackPlanSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "fallback",
            "fallbackConfidence",
            "fallbackAlt2",
            "fallbackAlt2Confidence",
            "primaryActionable",
            "secondaryActionable",
            "reason",
        }, payload
        assert payload.get("whatIfFallbackPlanFit") in {"SAFE", "EVEN", "TENSE"}, payload
        assert set(payload.get("whatIfFallbackPlanFitSignals", {}).keys()) == {
            "plan",
            "planLane",
            "pressureBand",
            "projectedBand",
            "reason",
        }, payload
        assert isinstance(payload.get("whatIfFallbackPlanWhy"), str), payload
        assert set(payload.get("whatIfFallbackPlanWhySignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "plan",
            "planFit",
            "planReason",
            "reason",
        }, payload
        assert payload.get("whatIfSplit") in {"ON", "OFF"}, payload
        assert set(payload.get("whatIfSplitSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "primaryLane",
            "secondaryLane",
            "primaryConfidence",
            "secondaryConfidence",
            "lanesDiverged",
            "absDeltaRisk",
            "strongDelta",
            "strongConfidence",
            "reason",
        }, payload
        assert isinstance(payload.get("whatIfSplitLanes"), str), payload
        assert set(payload.get("whatIfSplitLanesSignals", {}).keys()) == {
            "primaryActionable",
            "secondaryActionable",
            "reason",
        }, payload
        assert payload.get("whatIfSplitConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("whatIfSplitConfidenceSignals", {}).keys()) == {
            "split",
            "flagEnabled",
            "primaryConfidence",
            "secondaryConfidence",
            "strongConfidence",
            "strongDelta",
            "reason",
        }, payload
        assert set(payload["pressureEdits"].keys()) == {"added", "removed", "net"}, payload
        assert "tokenTotals" in payload, payload
        assert "stickyTokens" in payload, payload
        assert set(payload["stickyTokens"].keys()) == {"count", "tokens"}, payload
        assert payload["stickyTokens"]["count"] == len(payload["stickyTokens"]["tokens"]), payload
        assert payload.get("anomalyPulse") in {"ON", "OFF"}, payload
        assert payload.get("anomalyConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("anomalyPulseSignals", {}).keys()) == {
            "stickyCount",
            "stickyThreshold",
            "pressureChurn",
            "pressureThreshold",
            "stickyMet",
            "pressureMet",
            "triggerCount",
            "stickyGap",
            "pressureGap",
            "combinedGap",
            "spike",
        }, payload
        assert isinstance(payload.get("topTokenMovers"), list), payload
        if payload["topTokenMovers"]:
            assert {"token", "net", "added", "removed"}.issubset(payload["topTokenMovers"][0].keys()), payload
        md_text = out_md.read_text(encoding="utf-8")
        assert "Token Totals" in md_text
        assert "Top Token Movers" in md_text
        assert "MODE TREND" in md_text
        assert "PRESSURE BAND" in md_text
        assert "DRIFT RISK" in md_text
        assert "FOCUS" in md_text
        assert "FOCUS STREAK" in md_text
        assert "FOCUS SHIFT" in md_text
        assert "FOCUS VOL" in md_text
        assert "ROUTE ACTION" in md_text
        assert "ACTION CONF" in md_text
        assert "FOCUS BAL" in md_text
        assert "FOCUS ENTROPY" in md_text
        assert "ACTION GUARD" in md_text
        assert "LANE LOCK" in md_text
        assert "ROUTE SANDBOX" in md_text
        assert "SANDBOX PLAN" in md_text
        assert "SANDBOX TARGET" in md_text
        assert "TARGET SRC" in md_text
        assert "SANDBOX TARGET CONF" in md_text
        assert "SANDBOX READY" in md_text
        assert "TARGET SHIFT" in md_text
        assert "SANDBOX COOLOFF" in md_text
        assert "DRIFT MOMENTUM" in md_text
        assert "ACTION STABILITY" in md_text
        assert "PRESSURE LAG" in md_text
        assert "WHAT-IF" in md_text
        assert "WHAT-IF CONF" in md_text
        assert "WHAT-IF ALIGN" in md_text
        assert "WHAT-IF BAND" in md_text
        assert "WHAT-IF MAG" in md_text
        assert "WHAT-IF FIT" in md_text
        assert "WHAT-IF FALLBACK" in md_text
        assert "WHAT-IF FALLBACK CONF" in md_text
        assert "WHAT-IF FALLBACK FIT" in md_text
        assert "WHAT-IF FALLBACK WHY" in md_text
        assert "WHAT-IF FALLBACK ALIGN" in md_text
        assert "WHAT-IF FALLBACK MAG" in md_text
        assert "WHAT-IF FALLBACK ALT2" in md_text
        assert "WHAT-IF FALLBACK ALT2 CONF" in md_text
        assert "WHAT-IF FALLBACK PLAN" in md_text
        assert "WHAT-IF PLAN FIT" in md_text
        assert "WHAT-IF PLAN WHY" in md_text
        assert "WHAT-IF SPLIT" in md_text
        assert "WHAT-IF SPLIT LANES" in md_text
        assert "WHAT-IF SPLIT CONF" in md_text
        assert "STICKY TOKENS" in md_text
        assert "ANOMALY" in md_text
        assert "ANOMALY CONF" in md_text
        assert "Sticky Tokens" in md_text

        cooloff_zero, signals_zero = sandbox_cooloff_from_prior(
            current_sandbox="OFF",
            prior_json_path=repo / "missing-prior.json",
        )
        assert cooloff_zero == 0, (cooloff_zero, signals_zero)
        assert signals_zero["reason"] == "no-prior-on-cycle", signals_zero

        prior_on = repo / "prior-on.json"
        prior_on.write_text(json.dumps({"routeSandbox": "ON", "sandboxCooloff": 0}), encoding="utf-8")
        cooloff_one, signals_one = sandbox_cooloff_from_prior(
            current_sandbox="OFF",
            prior_json_path=prior_on,
        )
        assert cooloff_one == 1, (cooloff_one, signals_one)
        assert signals_one["reason"] == "sandbox-just-disarmed", signals_one

        prior_cooling = repo / "prior-cooloff.json"
        prior_cooling.write_text(json.dumps({"routeSandbox": "OFF", "sandboxCooloff": 2}), encoding="utf-8")
        cooloff_three, signals_three = sandbox_cooloff_from_prior(
            current_sandbox="OFF",
            prior_json_path=prior_cooling,
        )
        assert cooloff_three == 3, (cooloff_three, signals_three)
        assert signals_three["reason"] == "cooloff-continuing", signals_three

    print("[PASS] weekly portal prompt readability drift regression checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
