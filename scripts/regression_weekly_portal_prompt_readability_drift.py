#!/usr/bin/env python3
"""Regression checks for weekly_portal_prompt_readability_drift.py."""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path

from weekly_portal_prompt_readability_drift import (
    sandbox_cooloff_from_prior,
    what_if_split_cooloff_from_prior,
    what_if_split_escalate_cooloff_from_prior,
    what_if_split_escalate_recover_plan_from_signals,
    what_if_split_escalate_recover_why_from_signals,
    what_if_split_escalate_recover_tempo_from_signals,
    what_if_split_escalate_recover_veto_from_signals,
    what_if_split_escalate_recover_veto_confidence_from_signals,
    what_if_split_escalate_recover_veto_why_from_signals,
    what_if_split_escalate_recover_veto_cooloff_from_prior,
    what_if_split_escalate_recover_veto_state_from_signals,
    what_if_split_escalate_recover_veto_dwell_from_prior,
    what_if_split_escalate_recover_veto_release_from_prior,
    what_if_split_escalate_recover_veto_release_confidence_from_signals,
    what_if_split_escalate_recover_veto_release_route_from_signals,
    what_if_split_escalate_recover_veto_release_tick_from_prior,
    what_if_split_escalate_recover_veto_release_tick_phase_from_signals,
    what_if_split_escalate_recover_veto_release_tick_cadence_from_signals,
    what_if_split_escalate_recover_veto_rearm_from_signals,
    what_if_split_escalate_recover_veto_rearm_confidence_from_signals,
    what_if_split_escalate_recover_confidence_delta_from_prior,
)

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
        assert payload.get("whatIfSplitSafe") in {"ON", "OFF"}, payload
        assert set(payload.get("whatIfSplitSafeSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "split",
            "primaryConfidence",
            "secondaryConfidence",
            "primaryFit",
            "secondaryConfidenceGate",
            "splitArmed",
            "primarySafe",
            "secondarySafe",
            "reason",
        }, payload
        assert payload.get("whatIfSplitPosture") in {"SAFE", "WATCH", "HOLD"}, payload
        assert set(payload.get("whatIfSplitPostureSignals", {}).keys()) == {
            "split",
            "splitSafe",
            "splitConfidence",
            "reason",
        }, payload
        assert isinstance(payload.get("whatIfSplitCooloff"), int), payload
        assert set(payload.get("whatIfSplitCooloffSignals", {}).keys()) == {
            "active",
            "currentSplit",
            "priorSplit",
            "priorCooloff",
            "reason",
            "priorLoaded",
        }, payload
        assert payload.get("whatIfSplitEscalate") in {"ON", "OFF"}, payload
        assert set(payload.get("whatIfSplitEscalateSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "split",
            "splitArmed",
            "lanesDiverged",
            "planFit",
            "tenseFit",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscalateConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("whatIfSplitEscalateConfidenceSignals", {}).keys()) == {
            "splitEscalate",
            "splitConfidence",
            "planFit",
            "reason",
        }, payload
        assert isinstance(payload.get("whatIfSplitEscLanes"), str), payload
        assert set(payload.get("whatIfSplitEscLanesSignals", {}).keys()) == {
            "splitEscalate",
            "primaryActionable",
            "secondaryActionable",
            "lanesDiverged",
            "reason",
        }, payload
        assert isinstance(payload.get("whatIfSplitEscCool"), int), payload
        assert set(payload.get("whatIfSplitEscCoolSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "active",
            "currentSplitEscalate",
            "priorSplitEscalate",
            "priorCooloff",
            "reason",
            "priorLoaded",
        }, payload
        assert payload.get("whatIfSplitEscState") in {"ARMED", "COOLING", "IDLE"}, payload
        assert set(payload.get("whatIfSplitEscStateSignals", {}).keys()) == {
            "splitEscalate",
            "splitEscCool",
            "cooling",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscPressure") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("whatIfSplitEscPressureSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "splitEscState",
            "splitEscCool",
            "pressureBand",
            "baseRank",
            "adjustedRank",
            "reason",
        }, payload
        assert isinstance(payload.get("whatIfSplitEscRecover"), str), payload
        assert set(payload.get("whatIfSplitEscRecoverSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "splitEscState",
            "splitEscLanes",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscRecoverConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("whatIfSplitEscRecoverConfidenceSignals", {}).keys()) == {
            "splitEscRecover",
            "splitEscState",
            "splitEscPressure",
            "splitEscLanes",
            "laneDivergence",
            "laneCount",
            "pressureRank",
            "stateEasing",
            "reason",
        }, payload
        assert isinstance(payload.get("whatIfSplitEscRecoverAlt"), str), payload
        assert set(payload.get("whatIfSplitEscRecoverAltSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "splitEscRecover",
            "splitEscState",
            "splitEscLanes",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscRecoverAltConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("whatIfSplitEscRecoverAltConfidenceSignals", {}).keys()) == {
            "splitEscRecoverAlt",
            "splitEscState",
            "splitEscPressure",
            "splitEscLanes",
            "laneDivergence",
            "laneCount",
            "pressureRank",
            "stateEasing",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscRecoverPlan") in {"PRIMARY", "ALT", "HOLD"}, payload
        assert set(payload.get("whatIfSplitEscRecoverPlanSignals", {}).keys()) == {
            "splitEscRecover",
            "splitEscRecoverAlt",
            "hasPrimary",
            "hasAlt",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscRecoverWhy") in {
            "FLAG OFF",
            "PRIMARY RELIEF",
            "PRIMARY STABILIZE",
            "PRIMARY STEADY",
            "ALT SAFETY NET",
            "ALT CONTINGENCY",
            "HOLD FOR SIGNAL",
        }, payload
        assert set(payload.get("whatIfSplitEscRecoverWhySignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "splitEscRecoverPlan",
            "splitEscRecoverConfidence",
            "splitEscPressure",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscRecoverTempo") in {"FAST", "STEADY", "DEFER"}, payload
        assert set(payload.get("whatIfSplitEscRecoverTempoSignals", {}).keys()) == {
            "splitEscRecoverPlan",
            "splitEscRecoverConfidence",
            "splitEscPressure",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscRecoverVeto") in {"ON", "OFF"}, payload
        assert set(payload.get("whatIfSplitEscRecoverVetoSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "splitEscRecoverConfidence",
            "splitEscPressure",
            "splitEscRecoverPlan",
            "confidenceLow",
            "pressureHigh",
            "planActionable",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscRecoverVetoConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("whatIfSplitEscRecoverVetoConfidenceSignals", {}).keys()) == {
            "splitEscRecoverVeto",
            "splitEscRecoverConfidence",
            "splitEscPressure",
            "splitEscRecoverPlan",
            "confidenceLow",
            "pressureHigh",
            "planActionable",
            "vetoOn",
            "reason",
        }, payload
        assert isinstance(payload.get("whatIfSplitEscRecoverVetoDwell"), int) and payload["whatIfSplitEscRecoverVetoDwell"] >= 0, payload
        assert set(payload.get("whatIfSplitEscRecoverVetoDwellSignals", {}).keys()) == {
            "currentState",
            "priorState",
            "priorDwell",
            "priorLoaded",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscRecoverVetoReleaseRoute") in {"PORTAL", "ALT", "PRESSURE", "HOLD", "NONE"}, payload
        assert set(payload.get("whatIfSplitEscRecoverVetoReleaseRouteSignals", {}).keys()) == {
            "splitEscRecoverVetoRelease",
            "splitEscRecoverVetoState",
            "splitEscRecover",
            "splitEscRecoverAlt",
            "splitEscRecoverPlan",
            "primaryActionable",
            "altActionable",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscRecoverVetoReleaseCadence") in {"ACCEL", "STEADY", "DECAY", "FLAG OFF"}, payload
        assert set(payload.get("whatIfSplitEscRecoverVetoReleaseCadenceSignals", {}).keys()) == {
            "tick",
            "priorTick",
            "delta",
            "numeric",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscRecoverVetoRearm") in {"WATCH", "OFF"}, payload
        assert set(payload.get("whatIfSplitEscRecoverVetoRearmSignals", {}).keys()) == {
            "flagName",
            "flagEnabled",
            "releaseTickPhase",
            "splitEscPressure",
            "releaseCadence",
            "reason",
        }, payload
        assert payload.get("whatIfSplitEscRecoverVetoRearmConfidence") in {"LOW", "MID", "HIGH"}, payload
        assert set(payload.get("whatIfSplitEscRecoverVetoRearmConfidenceSignals", {}).keys()) == {
            "splitEscRecoverVetoRearm",
            "flagEnabled",
            "releaseTickPhase",
            "splitEscPressure",
            "releaseCadence",
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
        assert "WHAT-IF SPLIT SAFE" in md_text
        assert "WHAT-IF SPLIT POSTURE" in md_text
        assert "WHAT-IF SPLIT COOLOFF" in md_text
        assert "WHAT-IF SPLIT ESCALATE" in md_text
        assert "WHAT-IF SPLIT ESC CONF" in md_text
        assert "WHAT-IF SPLIT ESC LANES" in md_text
        assert "WHAT-IF SPLIT ESC COOL" in md_text
        assert "WHAT-IF SPLIT ESC STATE" in md_text
        assert "WHAT-IF SPLIT ESC PRESSURE" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER CONF" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER ALT" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER ALT CONF" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER PLAN" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER WHY" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER TEMPO" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO CONF" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO WHY" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO COOLOFF" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO STATE" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO DWELL" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO RELEASE" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO RELEASE CONF" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO RELEASE ROUTE" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO RELEASE TICK" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO RELEASE PHASE" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO RELEASE CADENCE" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO REARM" in md_text
        assert "WHAT-IF SPLIT ESC RECOVER VETO REARM CONF" in md_text
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

        split_cooloff_zero, split_signals_zero = what_if_split_cooloff_from_prior(
            current_split="OFF",
            prior_json_path=repo / "missing-split-prior.json",
        )
        assert split_cooloff_zero == 0, (split_cooloff_zero, split_signals_zero)
        assert split_signals_zero["reason"] == "no-prior-on-cycle", split_signals_zero

        split_prior_on = repo / "split-prior-on.json"
        split_prior_on.write_text(json.dumps({"whatIfSplit": "ON", "whatIfSplitCooloff": 0}), encoding="utf-8")
        split_cooloff_one, split_signals_one = what_if_split_cooloff_from_prior(
            current_split="OFF",
            prior_json_path=split_prior_on,
        )
        assert split_cooloff_one == 1, (split_cooloff_one, split_signals_one)
        assert split_signals_one["reason"] == "split-just-disarmed", split_signals_one

        split_prior_cooling = repo / "split-prior-cooloff.json"
        split_prior_cooling.write_text(json.dumps({"whatIfSplit": "OFF", "whatIfSplitCooloff": 2}), encoding="utf-8")
        split_cooloff_three, split_signals_three = what_if_split_cooloff_from_prior(
            current_split="OFF",
            prior_json_path=split_prior_cooling,
        )
        assert split_cooloff_three == 3, (split_cooloff_three, split_signals_three)
        assert split_signals_three["reason"] == "cooloff-continuing", split_signals_three

        prior_env = os.environ.get("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_COOL")
        try:
            os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_COOL"] = "0"
            esc_cool_disabled, esc_signals_disabled = what_if_split_escalate_cooloff_from_prior(
                current_split_escalate="OFF",
                prior_json_path=repo / "missing-esc-prior.json",
            )
            assert esc_cool_disabled == 0, (esc_cool_disabled, esc_signals_disabled)
            assert esc_signals_disabled["reason"] == "flag-disabled", esc_signals_disabled

            os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_COOL"] = "1"
            esc_prior_on = repo / "esc-prior-on.json"
            esc_prior_on.write_text(json.dumps({"whatIfSplitEscalate": "ON", "whatIfSplitEscCool": 0}), encoding="utf-8")
            esc_cool_one, esc_signals_one = what_if_split_escalate_cooloff_from_prior(
                current_split_escalate="OFF",
                prior_json_path=esc_prior_on,
            )
            assert esc_cool_one == 1, (esc_cool_one, esc_signals_one)
            assert esc_signals_one["reason"] == "split-escalation-just-disarmed", esc_signals_one

            esc_prior_cooling = repo / "esc-prior-cooloff.json"
            esc_prior_cooling.write_text(json.dumps({"whatIfSplitEscalate": "OFF", "whatIfSplitEscCool": 2}), encoding="utf-8")
            esc_cool_three, esc_signals_three = what_if_split_escalate_cooloff_from_prior(
                current_split_escalate="OFF",
                prior_json_path=esc_prior_cooling,
            )
            assert esc_cool_three == 3, (esc_cool_three, esc_signals_three)
            assert esc_signals_three["reason"] == "split-escalation-cooloff-continuing", esc_signals_three
        finally:
            if prior_env is None:
                os.environ.pop("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_COOL", None)
            else:
                os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_COOL"] = prior_env

        plan_primary, plan_primary_signals = what_if_split_escalate_recover_plan_from_signals(
            what_if_split_esc_recover="PORTAL",
            what_if_split_esc_recover_alt="ALT",
        )
        assert plan_primary == "PRIMARY", (plan_primary, plan_primary_signals)
        assert plan_primary_signals["reason"] == "primary-recovery-lane-available", plan_primary_signals

        plan_hold, plan_hold_signals = what_if_split_escalate_recover_plan_from_signals(
            what_if_split_esc_recover="NONE",
            what_if_split_esc_recover_alt="NONE",
        )
        assert plan_hold == "HOLD", (plan_hold, plan_hold_signals)
        assert plan_hold_signals["reason"] == "no-actionable-recovery-lanes", plan_hold_signals

        prior_recover_why_env = os.environ.get("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_WHY")
        try:
            os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_WHY"] = "0"
            why_off, why_off_signals = what_if_split_escalate_recover_why_from_signals(
                what_if_split_esc_recover_plan="PRIMARY",
                what_if_split_esc_recover_confidence="HIGH",
                what_if_split_esc_pressure="LOW",
            )
            assert why_off == "FLAG OFF", (why_off, why_off_signals)
            assert why_off_signals["reason"] == "flag-disabled", why_off_signals

            os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_WHY"] = "1"
            why_primary_relief, why_primary_relief_signals = what_if_split_escalate_recover_why_from_signals(
                what_if_split_esc_recover_plan="PRIMARY",
                what_if_split_esc_recover_confidence="HIGH",
                what_if_split_esc_pressure="LOW",
            )
            assert why_primary_relief == "PRIMARY RELIEF", (why_primary_relief, why_primary_relief_signals)
            assert why_primary_relief_signals["reason"] == "high-confidence-primary-lane-with-low-pressure", why_primary_relief_signals

            why_hold, why_hold_signals = what_if_split_escalate_recover_why_from_signals(
                what_if_split_esc_recover_plan="HOLD",
                what_if_split_esc_recover_confidence="LOW",
                what_if_split_esc_pressure="MID",
            )
            assert why_hold == "HOLD FOR SIGNAL", (why_hold, why_hold_signals)
            assert why_hold_signals["reason"] == "no-actionable-recovery-lane", why_hold_signals

            tempo_fast, tempo_fast_signals = what_if_split_escalate_recover_tempo_from_signals(
                what_if_split_esc_recover_plan="PRIMARY",
                what_if_split_esc_recover_confidence="HIGH",
                what_if_split_esc_pressure="LOW",
            )
            assert tempo_fast == "FAST", (tempo_fast, tempo_fast_signals)
            assert tempo_fast_signals["reason"] == "high-confidence-low-pressure-recovery", tempo_fast_signals

            tempo_defer, tempo_defer_signals = what_if_split_escalate_recover_tempo_from_signals(
                what_if_split_esc_recover_plan="HOLD",
                what_if_split_esc_recover_confidence="LOW",
                what_if_split_esc_pressure="MID",
            )
            assert tempo_defer == "DEFER", (tempo_defer, tempo_defer_signals)
            assert tempo_defer_signals["reason"] == "no-actionable-recovery-plan", tempo_defer_signals

            prior_veto_env = os.environ.get("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO")
            try:
                os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO"] = "0"
                veto_off, veto_off_signals = what_if_split_escalate_recover_veto_from_signals(
                    what_if_split_esc_recover_confidence="LOW",
                    what_if_split_esc_pressure="HIGH",
                    what_if_split_esc_recover_plan="PRIMARY",
                )
                assert veto_off == "OFF", (veto_off, veto_off_signals)
                assert veto_off_signals["reason"] == "flag-disabled", veto_off_signals

                os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO"] = "1"
                veto_on, veto_on_signals = what_if_split_escalate_recover_veto_from_signals(
                    what_if_split_esc_recover_confidence="LOW",
                    what_if_split_esc_pressure="HIGH",
                    what_if_split_esc_recover_plan="ALT",
                )
                assert veto_on == "ON", (veto_on, veto_on_signals)
                assert veto_on_signals["reason"] == "low-confidence-under-high-pressure-with-actionable-plan", veto_on_signals

                veto_hold, veto_hold_signals = what_if_split_escalate_recover_veto_from_signals(
                    what_if_split_esc_recover_confidence="LOW",
                    what_if_split_esc_pressure="HIGH",
                    what_if_split_esc_recover_plan="HOLD",
                )
                assert veto_hold == "OFF", (veto_hold, veto_hold_signals)
                assert veto_hold_signals["reason"] == "low-confidence-high-pressure-but-no-actionable-plan", veto_hold_signals

                veto_conf_high, veto_conf_high_signals = what_if_split_escalate_recover_veto_confidence_from_signals(
                    what_if_split_esc_recover_veto="ON",
                    what_if_split_esc_recover_confidence="LOW",
                    what_if_split_esc_pressure="HIGH",
                    what_if_split_esc_recover_plan="PRIMARY",
                )
                assert veto_conf_high == "HIGH", (veto_conf_high, veto_conf_high_signals)
                assert veto_conf_high_signals["reason"] == "all-veto-guard-signals-aligned", veto_conf_high_signals

                veto_conf_mid, veto_conf_mid_signals = what_if_split_escalate_recover_veto_confidence_from_signals(
                    what_if_split_esc_recover_veto="OFF",
                    what_if_split_esc_recover_confidence="LOW",
                    what_if_split_esc_pressure="HIGH",
                    what_if_split_esc_recover_plan="HOLD",
                )
                assert veto_conf_mid == "MID", (veto_conf_mid, veto_conf_mid_signals)
                assert veto_conf_mid_signals["reason"] == "pressure-and-confidence-trigger-with-plan-gap", veto_conf_mid_signals

                prior_veto_why_env = os.environ.get("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_WHY")
                try:
                    os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_WHY"] = "0"
                    veto_why_off, veto_why_off_signals = what_if_split_escalate_recover_veto_why_from_signals(
                        what_if_split_esc_recover_veto="ON",
                        what_if_split_esc_recover_veto_confidence="HIGH",
                        what_if_split_esc_pressure="HIGH",
                        what_if_split_esc_recover_plan="PRIMARY",
                    )
                    assert veto_why_off == "FLAG OFF", (veto_why_off, veto_why_off_signals)
                    assert veto_why_off_signals["reason"] == "flag-disabled", veto_why_off_signals

                    os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_WHY"] = "1"
                    veto_why_on, veto_why_on_signals = what_if_split_escalate_recover_veto_why_from_signals(
                        what_if_split_esc_recover_veto="ON",
                        what_if_split_esc_recover_veto_confidence="HIGH",
                        what_if_split_esc_pressure="HIGH",
                        what_if_split_esc_recover_plan="ALT",
                    )
                    assert veto_why_on == "HIGH PRESSURE LOCK", (veto_why_on, veto_why_on_signals)
                    assert veto_why_on_signals["reason"] == "veto-armed-under-high-pressure-actionable-plan", veto_why_on_signals
                finally:
                    if prior_veto_why_env is None:
                        os.environ.pop("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_WHY", None)
                    else:
                        os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_WHY"] = prior_veto_why_env

                prior_veto_cooloff_env = os.environ.get("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_COOLOFF")
                try:
                    os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_COOLOFF"] = "1"
                    veto_cooloff_prior = repo / "veto-cooloff-prior.json"
                    veto_cooloff_prior.write_text(json.dumps({"whatIfSplitEscRecoverVeto": "ON", "whatIfSplitEscRecoverVetoCooloff": 0}), encoding="utf-8")
                    veto_cooloff_one, veto_cooloff_one_signals = what_if_split_escalate_recover_veto_cooloff_from_prior(
                        current_split_esc_recover_veto="OFF",
                        prior_json_path=veto_cooloff_prior,
                    )
                    assert veto_cooloff_one == 1, (veto_cooloff_one, veto_cooloff_one_signals)
                    assert veto_cooloff_one_signals["reason"] == "veto-just-disarmed", veto_cooloff_one_signals

                    veto_cooloff_prior.write_text(json.dumps({"whatIfSplitEscRecoverVeto": "OFF", "whatIfSplitEscRecoverVetoCooloff": 2}), encoding="utf-8")
                    veto_cooloff_roll, veto_cooloff_roll_signals = what_if_split_escalate_recover_veto_cooloff_from_prior(
                        current_split_esc_recover_veto="OFF",
                        prior_json_path=veto_cooloff_prior,
                    )
                    assert veto_cooloff_roll == 3, (veto_cooloff_roll, veto_cooloff_roll_signals)
                    assert veto_cooloff_roll_signals["reason"] == "veto-remains-disarmed-in-cooloff-window", veto_cooloff_roll_signals

                    veto_state_armed, veto_state_armed_signals = what_if_split_escalate_recover_veto_state_from_signals(
                        what_if_split_esc_recover_veto="ON",
                        what_if_split_esc_recover_veto_cooloff=0,
                    )
                    assert veto_state_armed == "ARMED", (veto_state_armed, veto_state_armed_signals)

                    veto_state_cooling, veto_state_cooling_signals = what_if_split_escalate_recover_veto_state_from_signals(
                        what_if_split_esc_recover_veto="OFF",
                        what_if_split_esc_recover_veto_cooloff=2,
                    )
                    assert veto_state_cooling == "COOLING", (veto_state_cooling, veto_state_cooling_signals)
                    assert veto_state_cooling_signals["reason"] == "veto-disarmed-in-cooloff-window", veto_state_cooling_signals

                    veto_dwell_prior = repo / "veto-dwell-prior.json"
                    veto_dwell_prior.write_text(
                        json.dumps({"whatIfSplitEscRecoverVetoState": "ARMED", "whatIfSplitEscRecoverVetoDwell": 2}),
                        encoding="utf-8",
                    )
                    veto_dwell_roll, veto_dwell_roll_signals = what_if_split_escalate_recover_veto_dwell_from_prior(
                        current_split_esc_recover_veto_state="ARMED",
                        prior_json_path=veto_dwell_prior,
                    )
                    assert veto_dwell_roll == 3, (veto_dwell_roll, veto_dwell_roll_signals)
                    assert veto_dwell_roll_signals["reason"] == "veto-remains-armed", veto_dwell_roll_signals

                    veto_dwell_new, veto_dwell_new_signals = what_if_split_escalate_recover_veto_dwell_from_prior(
                        current_split_esc_recover_veto_state="ARMED",
                        prior_json_path=repo / "missing-veto-dwell-prior.json",
                    )
                    assert veto_dwell_new == 1, (veto_dwell_new, veto_dwell_new_signals)
                    assert veto_dwell_new_signals["priorLoaded"] is False, veto_dwell_new_signals
                    assert veto_dwell_new_signals["reason"] == "veto-armed-new-streak", veto_dwell_new_signals

                    veto_dwell_reset, veto_dwell_reset_signals = what_if_split_escalate_recover_veto_dwell_from_prior(
                        current_split_esc_recover_veto_state="COOLING",
                        prior_json_path=veto_dwell_prior,
                    )
                    assert veto_dwell_reset == 0, (veto_dwell_reset, veto_dwell_reset_signals)
                    assert veto_dwell_reset_signals["reason"] == "veto-not-armed", veto_dwell_reset_signals

                    prior_veto_release_env = os.environ.get("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_RELEASE")
                    try:
                        os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_RELEASE"] = "0"
                        veto_release_flag_off, veto_release_flag_off_signals = what_if_split_escalate_recover_veto_release_from_prior(
                            current_split_esc_recover_veto_state="IDLE",
                            prior_json_path=veto_dwell_prior,
                        )
                        assert veto_release_flag_off == "FLAG OFF", (veto_release_flag_off, veto_release_flag_off_signals)
                        assert veto_release_flag_off_signals["reason"] == "flag-disabled", veto_release_flag_off_signals

                        os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_RELEASE"] = "1"
                        veto_release_prior = repo / "veto-release-prior.json"
                        veto_release_prior.write_text(
                            json.dumps({"whatIfSplitEscRecoverVetoState": "COOLING"}),
                            encoding="utf-8",
                        )
                        veto_release_clear, veto_release_clear_signals = what_if_split_escalate_recover_veto_release_from_prior(
                            current_split_esc_recover_veto_state="IDLE",
                            prior_json_path=veto_release_prior,
                        )
                        assert veto_release_clear == "COOLING CLEAR", (veto_release_clear, veto_release_clear_signals)
                        assert veto_release_clear_signals["reason"] == "veto-state-transitioned-cooling-to-idle", veto_release_clear_signals

                        veto_release_cooling, veto_release_cooling_signals = what_if_split_escalate_recover_veto_release_from_prior(
                            current_split_esc_recover_veto_state="COOLING",
                            prior_json_path=veto_release_prior,
                        )
                        assert veto_release_cooling == "COOLING", (veto_release_cooling, veto_release_cooling_signals)
                        assert veto_release_cooling_signals["reason"] == "veto-state-still-cooling", veto_release_cooling_signals

                        veto_release_conf_high, veto_release_conf_high_signals = what_if_split_escalate_recover_veto_release_confidence_from_signals(
                            what_if_split_esc_recover_veto_release="COOLING CLEAR",
                            what_if_split_esc_recover_veto_state="IDLE",
                            what_if_split_esc_recover_veto_dwell=0,
                        )
                        assert veto_release_conf_high == "HIGH", (veto_release_conf_high, veto_release_conf_high_signals)
                        assert veto_release_conf_high_signals["reason"] == "clean-cooling-to-idle-release-transition", veto_release_conf_high_signals

                        veto_release_conf_mid, veto_release_conf_mid_signals = what_if_split_escalate_recover_veto_release_confidence_from_signals(
                            what_if_split_esc_recover_veto_release="COOLING",
                            what_if_split_esc_recover_veto_state="COOLING",
                            what_if_split_esc_recover_veto_dwell=0,
                        )
                        assert veto_release_conf_mid == "MID", (veto_release_conf_mid, veto_release_conf_mid_signals)
                        assert veto_release_conf_mid_signals["reason"] == "release-pending-while-cooling", veto_release_conf_mid_signals

                        veto_release_route_primary, veto_release_route_primary_signals = what_if_split_escalate_recover_veto_release_route_from_signals(
                            what_if_split_esc_recover_veto_release="COOLING CLEAR",
                            what_if_split_esc_recover_veto_state="IDLE",
                            what_if_split_esc_recover="PORTAL",
                            what_if_split_esc_recover_alt="ALT",
                            what_if_split_esc_recover_plan="PRIMARY",
                        )
                        assert veto_release_route_primary == "PORTAL", (veto_release_route_primary, veto_release_route_primary_signals)
                        assert veto_release_route_primary_signals["reason"] == "release-cleared-follow-primary-recovery-lane", veto_release_route_primary_signals

                        veto_release_route_hold, veto_release_route_hold_signals = what_if_split_escalate_recover_veto_release_route_from_signals(
                            what_if_split_esc_recover_veto_release="COOLING",
                            what_if_split_esc_recover_veto_state="COOLING",
                            what_if_split_esc_recover="PORTAL",
                            what_if_split_esc_recover_alt="ALT",
                            what_if_split_esc_recover_plan="PRIMARY",
                        )
                        assert veto_release_route_hold == "HOLD", (veto_release_route_hold, veto_release_route_hold_signals)
                        assert veto_release_route_hold_signals["reason"] == "release-route-held-while-cooling", veto_release_route_hold_signals

                        prior_veto_release_tick_env = os.environ.get("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_RELEASE_TICK")
                        try:
                            os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_RELEASE_TICK"] = "0"
                            veto_release_tick_flag_off, veto_release_tick_flag_off_signals = what_if_split_escalate_recover_veto_release_tick_from_prior(
                                current_split_esc_recover_veto_release="COOLING CLEAR",
                                current_split_esc_recover_veto_state="IDLE",
                                prior_json_path=veto_release_prior,
                            )
                            assert veto_release_tick_flag_off == "FLAG OFF", (veto_release_tick_flag_off, veto_release_tick_flag_off_signals)
                            assert veto_release_tick_flag_off_signals["reason"] == "flag-disabled", veto_release_tick_flag_off_signals

                            os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_RELEASE_TICK"] = "1"
                            veto_release_tick_start, veto_release_tick_start_signals = what_if_split_escalate_recover_veto_release_tick_from_prior(
                                current_split_esc_recover_veto_release="COOLING CLEAR",
                                current_split_esc_recover_veto_state="IDLE",
                                prior_json_path=veto_release_prior,
                            )
                            assert veto_release_tick_start == 1, (veto_release_tick_start, veto_release_tick_start_signals)
                            assert veto_release_tick_start_signals["reason"] == "release-cleared-idle-window-started", veto_release_tick_start_signals

                            veto_release_tick_prior = repo / "veto-release-tick-prior.json"
                            veto_release_tick_prior.write_text(
                                json.dumps(
                                    {
                                        "whatIfSplitEscRecoverVetoReleaseTick": 2,
                                        "whatIfSplitEscRecoverVetoRelease": "STABLE",
                                        "whatIfSplitEscRecoverVetoState": "IDLE",
                                    }
                                ),
                                encoding="utf-8",
                            )
                            veto_release_tick_continue, veto_release_tick_continue_signals = what_if_split_escalate_recover_veto_release_tick_from_prior(
                                current_split_esc_recover_veto_release="STABLE",
                                current_split_esc_recover_veto_state="IDLE",
                                prior_json_path=veto_release_tick_prior,
                            )
                            assert veto_release_tick_continue == 3, (veto_release_tick_continue, veto_release_tick_continue_signals)
                            assert veto_release_tick_continue_signals["reason"] == "release-idle-window-continuing", veto_release_tick_continue_signals

                            veto_release_tick_reset, veto_release_tick_reset_signals = what_if_split_escalate_recover_veto_release_tick_from_prior(
                                current_split_esc_recover_veto_release="HOLD",
                                current_split_esc_recover_veto_state="ARMED",
                                prior_json_path=veto_release_tick_prior,
                            )
                            assert veto_release_tick_reset == 0, (veto_release_tick_reset, veto_release_tick_reset_signals)
                            assert veto_release_tick_reset_signals["reason"] == "no-active-release-idle-window", veto_release_tick_reset_signals

                            veto_release_phase_idle, veto_release_phase_idle_signals = what_if_split_escalate_recover_veto_release_tick_phase_from_signals(
                                what_if_split_esc_recover_veto_release_tick=0,
                            )
                            assert veto_release_phase_idle == "IDLE", (veto_release_phase_idle, veto_release_phase_idle_signals)
                            assert veto_release_phase_idle_signals["reason"] == "no-active-release-tick-window", veto_release_phase_idle_signals

                            veto_release_phase_mid, veto_release_phase_mid_signals = what_if_split_escalate_recover_veto_release_tick_phase_from_signals(
                                what_if_split_esc_recover_veto_release_tick=3,
                            )
                            assert veto_release_phase_mid == "MID", (veto_release_phase_mid, veto_release_phase_mid_signals)
                            assert veto_release_phase_mid_signals["reason"] == "release-window-mid-pacing", veto_release_phase_mid_signals

                            veto_release_phase_flag_off, veto_release_phase_flag_off_signals = what_if_split_escalate_recover_veto_release_tick_phase_from_signals(
                                what_if_split_esc_recover_veto_release_tick="FLAG OFF",
                            )
                            assert veto_release_phase_flag_off == "FLAG OFF", (veto_release_phase_flag_off, veto_release_phase_flag_off_signals)
                            assert veto_release_phase_flag_off_signals["reason"] == "non-numeric-tick-token-forwarded", veto_release_phase_flag_off_signals

                            veto_release_cadence_accel, veto_release_cadence_accel_signals = what_if_split_escalate_recover_veto_release_tick_cadence_from_signals(
                                what_if_split_esc_recover_veto_release_tick=4,
                                what_if_split_esc_recover_veto_release_tick_signals={"priorTick": 1},
                            )
                            assert veto_release_cadence_accel == "ACCEL", (veto_release_cadence_accel, veto_release_cadence_accel_signals)
                            assert veto_release_cadence_accel_signals["reason"] == "tick-growth-jump-vs-prior-window", veto_release_cadence_accel_signals

                            veto_release_cadence_steady, veto_release_cadence_steady_signals = what_if_split_escalate_recover_veto_release_tick_cadence_from_signals(
                                what_if_split_esc_recover_veto_release_tick=3,
                                what_if_split_esc_recover_veto_release_tick_signals={"priorTick": 2},
                            )
                            assert veto_release_cadence_steady == "STEADY", (veto_release_cadence_steady, veto_release_cadence_steady_signals)
                            assert veto_release_cadence_steady_signals["reason"] == "tick-growth-linear-vs-prior-window", veto_release_cadence_steady_signals

                            veto_release_cadence_decay, veto_release_cadence_decay_signals = what_if_split_escalate_recover_veto_release_tick_cadence_from_signals(
                                what_if_split_esc_recover_veto_release_tick=2,
                                what_if_split_esc_recover_veto_release_tick_signals={"priorTick": 3},
                            )
                            assert veto_release_cadence_decay == "DECAY", (veto_release_cadence_decay, veto_release_cadence_decay_signals)
                            assert veto_release_cadence_decay_signals["reason"] == "tick-stalled-or-regressed-vs-prior-window", veto_release_cadence_decay_signals

                            veto_release_cadence_flag_off, veto_release_cadence_flag_off_signals = what_if_split_escalate_recover_veto_release_tick_cadence_from_signals(
                                what_if_split_esc_recover_veto_release_tick="FLAG OFF",
                                what_if_split_esc_recover_veto_release_tick_signals={"priorTick": 7},
                            )
                            assert veto_release_cadence_flag_off == "FLAG OFF", (veto_release_cadence_flag_off, veto_release_cadence_flag_off_signals)
                            assert veto_release_cadence_flag_off_signals["reason"] == "non-numeric-tick-token-forwarded", veto_release_cadence_flag_off_signals

                            prior_veto_rearm_env = os.environ.get("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM")
                            try:
                                os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM"] = "0"
                                veto_rearm_off, veto_rearm_off_signals = what_if_split_escalate_recover_veto_rearm_from_signals(
                                    what_if_split_esc_recover_veto_release_tick_phase="LATE",
                                    what_if_split_esc_pressure="HIGH",
                                    what_if_split_esc_recover_veto_release_cadence="STEADY",
                                )
                                assert veto_rearm_off == "OFF", (veto_rearm_off, veto_rearm_off_signals)
                                assert veto_rearm_off_signals["reason"] == "flag-disabled", veto_rearm_off_signals

                                os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM"] = "1"
                                veto_rearm_watch, veto_rearm_watch_signals = what_if_split_escalate_recover_veto_rearm_from_signals(
                                    what_if_split_esc_recover_veto_release_tick_phase="LATE",
                                    what_if_split_esc_pressure="HIGH",
                                    what_if_split_esc_recover_veto_release_cadence="STEADY",
                                )
                                assert veto_rearm_watch == "WATCH", (veto_rearm_watch, veto_rearm_watch_signals)
                                assert veto_rearm_watch_signals["reason"] == "late-release-window-under-high-pressure", veto_rearm_watch_signals

                                veto_rearm_decay, veto_rearm_decay_signals = what_if_split_escalate_recover_veto_rearm_from_signals(
                                    what_if_split_esc_recover_veto_release_tick_phase="LATE",
                                    what_if_split_esc_pressure="HIGH",
                                    what_if_split_esc_recover_veto_release_cadence="DECAY",
                                )
                                assert veto_rearm_decay == "OFF", (veto_rearm_decay, veto_rearm_decay_signals)
                                assert veto_rearm_decay_signals["reason"] == "release-cadence-not-rearm-prone", veto_rearm_decay_signals

                                veto_rearm_conf_high, veto_rearm_conf_high_signals = what_if_split_escalate_recover_veto_rearm_confidence_from_signals(
                                    what_if_split_esc_recover_veto_rearm=veto_rearm_watch,
                                    what_if_split_esc_recover_veto_rearm_signals=veto_rearm_watch_signals,
                                )
                                assert veto_rearm_conf_high == "HIGH", (veto_rearm_conf_high, veto_rearm_conf_high_signals)
                                assert veto_rearm_conf_high_signals["reason"] == "watch-cue-aligned-with-late-high-pressure-steady-cadence", veto_rearm_conf_high_signals

                                veto_rearm_conf_mid, veto_rearm_conf_mid_signals = what_if_split_escalate_recover_veto_rearm_confidence_from_signals(
                                    what_if_split_esc_recover_veto_rearm=veto_rearm_decay,
                                    what_if_split_esc_recover_veto_rearm_signals=veto_rearm_decay_signals,
                                )
                                assert veto_rearm_conf_mid == "MID", (veto_rearm_conf_mid, veto_rearm_conf_mid_signals)
                                assert veto_rearm_conf_mid_signals["reason"] == "watch-cue-suppressed-by-cadence-guard", veto_rearm_conf_mid_signals

                                veto_rearm_conf_low, veto_rearm_conf_low_signals = what_if_split_escalate_recover_veto_rearm_confidence_from_signals(
                                    what_if_split_esc_recover_veto_rearm=veto_rearm_off,
                                    what_if_split_esc_recover_veto_rearm_signals=veto_rearm_off_signals,
                                )
                                assert veto_rearm_conf_low == "LOW", (veto_rearm_conf_low, veto_rearm_conf_low_signals)
                                assert veto_rearm_conf_low_signals["reason"] == "flag-disabled", veto_rearm_conf_low_signals
                            finally:
                                if prior_veto_rearm_env is None:
                                    os.environ.pop("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM", None)
                                else:
                                    os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM"] = prior_veto_rearm_env
                        finally:
                            if prior_veto_release_tick_env is None:
                                os.environ.pop("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_RELEASE_TICK", None)
                            else:
                                os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_RELEASE_TICK"] = prior_veto_release_tick_env
                    finally:
                        if prior_veto_release_env is None:
                            os.environ.pop("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_RELEASE", None)
                        else:
                            os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_RELEASE"] = prior_veto_release_env
                finally:
                    if prior_veto_cooloff_env is None:
                        os.environ.pop("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_COOLOFF", None)
                    else:
                        os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_COOLOFF"] = prior_veto_cooloff_env
            finally:
                if prior_veto_env is None:
                    os.environ.pop("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO", None)
                else:
                    os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO"] = prior_veto_env

            recover_prior = repo / "recover-prior.json"
            recover_prior.write_text(json.dumps({"whatIfSplitEscRecoverConfidence": "LOW"}), encoding="utf-8")
            delta_up, delta_up_signals = what_if_split_escalate_recover_confidence_delta_from_prior(
                current_confidence="HIGH",
                prior_json_path=recover_prior,
            )
            assert delta_up == "+2", (delta_up, delta_up_signals)
            assert delta_up_signals["reason"] == "confidence-increased-vs-prior-window", delta_up_signals

            recover_prior.write_text(json.dumps({"whatIfSplitEscRecoverConfidence": "HIGH"}), encoding="utf-8")
            delta_down, delta_down_signals = what_if_split_escalate_recover_confidence_delta_from_prior(
                current_confidence="LOW",
                prior_json_path=recover_prior,
            )
            assert delta_down == "-2", (delta_down, delta_down_signals)
            assert delta_down_signals["reason"] == "confidence-decreased-vs-prior-window", delta_down_signals

            delta_flat, delta_flat_signals = what_if_split_escalate_recover_confidence_delta_from_prior(
                current_confidence="MID",
                prior_json_path=repo / "missing-recover-prior.json",
            )
            assert delta_flat == "+0", (delta_flat, delta_flat_signals)
            assert delta_flat_signals["priorLoaded"] is False, delta_flat_signals
            assert delta_flat_signals["reason"] == "confidence-unchanged-vs-prior-window", delta_flat_signals
        finally:
            if prior_recover_why_env is None:
                os.environ.pop("DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_WHY", None)
            else:
                os.environ["DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_WHY"] = prior_recover_why_env

    print("[PASS] weekly portal prompt readability drift regression checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
