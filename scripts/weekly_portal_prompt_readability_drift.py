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
DEFAULT_DMG_GLYPH_FX_REMAP_CANDIDATES_JSON = ROOT / "logs" / "playtests" / "dmg_glyph_fx_remap_candidates.json"
DEFAULT_DMG_GLYPH_FX_REMAP_CANDIDATES_MD = ROOT / "logs" / "playtests" / "dmg_glyph_fx_remap_candidates.md"
DEFAULT_AMBIENT_RAMP_WHY_AUTO_REMAP_PLAN_JSON = ROOT / "logs" / "playtests" / "ambient_ramp_why_auto_remap_plan.json"
DEFAULT_AMBIENT_RAMP_WHY_AUTO_REMAP_PLAN_MD = ROOT / "logs" / "playtests" / "ambient_ramp_why_auto_remap_plan.md"

PORTAL_PATH_HINTS = (
    "src/portal.lua",
    "src/portal_prompt_linter.lua",
    "src/portal_prompt_budget.lua",
    "src/combat.lua",
    "scripts/regression_portal_",
    "scripts/check_portal_prompt_",
    "scripts/regression_combat_damage_numbers.lua",
)

TOKEN_GROUPS = {
    "compact": ["NEXT:", "P:", "ALT:", "ADEL:", "AP:", "ALT STEP:", "ALT STEP CONF:", "ALT STEP WHY CONF:", "AWGMC:", "ALT WHY GLYPH:", "ALT WHY GLYPH MODE:", "AWGM:", "VTC:", "VTCR:", "VIBE TRAIL WHY:", "VTW:", "VTWC:", "VTCW:", "VTA:", "AMBIENT RAMP CONF:", "ARC:", "AMBIENT RAMP WHY:", "ARW:", "PULSE HEAT FX:", "ROUTE GLOW:", "ROUTE GLOW FX:", "RGFX:", "ROUTE GLOW CONF:", "RGC:", "ROUTE GLOW FX CONF:", "RGFXC:", "ROUTE GLOW FX CONF WHY:", "RGFXW:", "ROUTE GLOW FX CONF WHY RAIL:", "RGFXWR:", "RGFXWRM:", "RGFXWRI:", "RGFXWRI WHY:", "RGFXWRI WHY CONF:", "RGFXWRIWC:", "RGFXWRIU:", "RGFXWRIUP:", "RGFXWRIUFX:", "URG STACK:", "URG STACK RAIL:", "DMGNUM STACK CAP:", "DMGNUM LIFE:", "DMGNUM LIFE CONF:", "DMGNUM LIFE CONF Δ:", "DMGNUM LIFE TREND:", "DMGNUM LIFE TREND FX PULSE:", "DMGNUM LIFE TREND FX PULSE CONF:", "DMGNUM LIFE TREND FX PULSE REMAP PLAN:", "DMG COMBO:", "DMG COMBO CONF:", "DCR:", "DMG COMBO WINDOW RETUNE CONF:", "DCRC:", "DMG COMBO CHAIN COACH:", "DMG COMBO CONF COACH COPY SWAP REC:", "DMG COMBO CONF FX ACCENT:", "DCCSR:", "DCCST:", "DCCFX:", "DCCFXT:", "DCCFXV:", "PULSE REMAP MOMENTUM:", "PULSE REMAP MOMENTUM Δ:", "PULSE REMAP MOMENTUM SUPPRESS:", "PULSE REMAP SUPPRESS PLAN:", "PULSE REMAP SCENE MICROLINE VARIANT PACK:", "PULSE REMAP SCENE MICROLINE CADENCE:", "PRSMC:", "PULSE REMAP SCENE FX GLINT:", "PULSE REMAP SCENE COPY PALETTE REC:", "PRSCP:", "PRM:", "PRMS:", "PRSP:", "PRSMV:", "PRSMP:", "PRSMPP:", "PRSFX:", "PRPW:", "DMG GLYPH:", "DMG GLYPH FX LIVE:", "ARW AUTO PLAN:", "ARW APC:", "ARW AUTO PLAN CONF MOMENTUM:", "ARW MOMENTUM:", "ARW MOMENTUM ARC:", "ARW ARC PULSE:", "LPR HYS THR:", "LPR HYS WINDOW Δ:"],
    "detailed": ["NEXT ROUTE:", "PRESSURE:", "ALT ROUTE:", "ALT DELTA:", "ALT PLAN:", "ALT STEP:", "ALT STEP CONF:", "ALT STEP WHY CONF:", "ALT WHY GLYPH:", "ALT WHY GLYPH MODE:", "VIBE TRAIL CONF:", "VIBE TRAIL CONF RAIL:", "VIBE TRAIL WHY:", "VIBE TRAIL WHY CONF:", "VIBE TRAIL WHY CONF WHY:", "VIBE TRAIL ARC:", "AMBIENT RAMP CONF:", "ARC:", "AMBIENT RAMP WHY:", "ARW:", "PULSE HEAT FX:", "ROUTE GLOW:", "ROUTE GLOW FX:", "RGFX:", "ROUTE GLOW CONF:", "RGC:", "ROUTE GLOW FX CONF:", "RGFXC:", "ROUTE GLOW FX CONF WHY:", "RGFXW:", "ROUTE GLOW FX CONF WHY RAIL:", "RGFXWR:", "RGFXWRM:", "RGFXWRI:", "RGFXWRI WHY:", "ROUTE GLOW FX CONF WHY RAIL INTENSITY WHY CONF URGENCY:", "RGFXWRIUFX:", "URG STACK:", "URG STACK RAIL:", "DMGNUM STACK CAP:", "DMGNUM LIFE:", "DMGNUM LIFE CONF:", "DMGNUM LIFE CONF Δ:", "DMGNUM LIFE TREND:", "DMGNUM LIFE TREND FX PULSE:", "DMGNUM LIFE TREND FX PULSE CONF:", "DMGNUM LIFE TREND FX PULSE REMAP PLAN:", "DMG COMBO:", "DMG COMBO CONF:", "DCR:", "DMG COMBO WINDOW RETUNE CONF:", "DCRC:", "DMG COMBO CHAIN COACH:", "DMG COMBO CONF COACH COPY SWAP REC:", "DMG COMBO CONF FX ACCENT:", "DCCSR:", "DCCST:", "DCCFX:", "DCCFXT:", "DCCFXV:", "PULSE REMAP MOMENTUM:", "PULSE REMAP MOMENTUM Δ:", "PULSE REMAP MOMENTUM SUPPRESS:", "PULSE REMAP SUPPRESS PLAN:", "PULSE REMAP SCENE MICROLINE VARIANT PACK:", "PULSE REMAP SCENE MICROLINE CADENCE:", "PRSMC:", "PULSE REMAP SCENE FX GLINT:", "PULSE REMAP SCENE COPY PALETTE REC:", "PRSCP:", "PRM:", "PRMS:", "PRSP:", "PRSMV:", "PRSMP:", "PRSMPP:", "PRSFX:", "PRPW:", "DMG GLYPH:", "DMG GLYPH FX LIVE:", "AMBIENT RAMP WHY AUTO-REMAP PLAN:", "ARW ARC PULSE:", "LPR HYS THR:", "LPR HYS WINDOW Δ:"],
    "shared": ["ENTER:JUMP", "COACH:"],
}

TOKEN_CATALOG: list[str] = []
for _tokens in TOKEN_GROUPS.values():
    for _token in _tokens:
        if _token not in TOKEN_CATALOG:
            TOKEN_CATALOG.append(_token)

PRESSURE_TOKENS = ["PRESSURE:", "P:"]

TOKEN_FAMILIES = {
    "portal": ["ENTER:JUMP", "NEXT:", "NEXT ROUTE:", "COACH:", "VIBE TRAIL CONF:", "VIBE TRAIL CONF RAIL:", "VTC:", "VTCR:", "VIBE TRAIL WHY:", "VTW:", "VIBE TRAIL WHY CONF:", "VTWC:", "VIBE TRAIL WHY CONF WHY:", "VTCW:", "AMBIENT RAMP CONF:", "ARC:", "AMBIENT RAMP WHY:", "ARW:", "ROUTE GLOW:", "ROUTE GLOW FX:", "RGFX:", "ROUTE GLOW CONF:", "RGC:", "ROUTE GLOW FX CONF:", "RGFXC:", "ROUTE GLOW FX CONF WHY:", "RGFXW:", "ROUTE GLOW FX CONF WHY RAIL:", "RGFXWR:", "RGFXWRM:", "RGFXWRI:", "RGFXWRI WHY:", "RGFXWRI WHY CONF:", "RGFXWRIWC:", "RGFXWRIU:", "RGFXWRIUP:", "ROUTE GLOW FX CONF WHY RAIL INTENSITY WHY CONF URGENCY:", "RGFXWRIUFX:", "URG STACK:", "URG STACK RAIL:", "DMGNUM STACK CAP:", "DMGNUM LIFE:", "DMGNUM LIFE CONF:", "DMGNUM LIFE CONF Δ:", "DMGNUM LIFE TREND:", "DMGNUM LIFE TREND FX PULSE:", "DMGNUM LIFE TREND FX PULSE CONF:", "DMGNUM LIFE TREND FX PULSE REMAP PLAN:", "DMG COMBO:", "DMG COMBO CONF:", "DCR:", "DMG COMBO WINDOW RETUNE CONF:", "DCRC:", "DMG COMBO CHAIN COACH:", "DMG COMBO CONF COACH COPY SWAP REC:", "DMG COMBO CONF FX ACCENT:", "DCCSR:", "DCCST:", "DCCFX:", "DCCFXT:", "DCCFXV:", "PULSE REMAP MOMENTUM:", "PULSE REMAP MOMENTUM Δ:", "PULSE REMAP MOMENTUM SUPPRESS:", "PULSE REMAP SUPPRESS PLAN:", "PULSE REMAP SCENE MICROLINE VARIANT PACK:", "PULSE REMAP SCENE FX GLINT:", "PULSE REMAP SCENE COPY PALETTE REC:", "PRSCP:", "PRM:", "PRMS:", "PRSP:", "PRSMV:", "PRSMP:", "PRSMPP:", "PRSFX:", "PRPW:", "DMG GLYPH:", "DMG GLYPH FX LIVE:", "AMBIENT RAMP WHY AUTO-REMAP PLAN:", "ARW AUTO PLAN:", "ARW APC:", "ARW AUTO PLAN CONF MOMENTUM:", "ARW MOMENTUM:", "ARW MOMENTUM ARC:", "ARW ARC PULSE:", "LPR HYS THR:", "LPR HYS WINDOW Δ:"],
    "alt": ["ALT:", "ALT ROUTE:", "ALT DELTA:", "ADEL:", "ALT PLAN:", "AP:", "ALT STEP:", "ALT STEP CONF:", "ALT STEP WHY CONF:", "AWGMC:", "ALT WHY GLYPH:", "ALT WHY GLYPH MODE:", "AWGM:"],
    "pressure": ["PRESSURE:", "P:"],
}

TOKEN_ALIAS_FAMILIES = {
    "vibeTrailWhyAlias": ["VIBE TRAIL WHY:", "VTW:"],
    "vibeTrailWhyConfidenceAlias": ["VIBE TRAIL WHY CONF:", "VTWC:"],
    "vibeTrailWhyConfidenceWhyAlias": ["VIBE TRAIL WHY CONF WHY:", "VTCW:"],
    "vibeTrailWhyConfidenceWhyConfidenceAlias": ["VIBE TRAIL WHY CONF WHY CONF:", "VTCWC:"],
    "vibeTrailArcAlias": ["VIBE TRAIL ARC:", "VTA:"],
    "ambientRampConfidenceAlias": ["AMBIENT RAMP CONF:", "ARC:"],
    "ambientRampWhyAlias": ["AMBIENT RAMP WHY:", "ARW:"],
    "ambientRampWhyAutoRemapPlanAlias": ["AMBIENT RAMP WHY AUTO-REMAP PLAN:", "ARW AUTO PLAN:"],
    "ambientRampWhyAutoRemapConfidenceBandAlias": ["ARW APC:"],
    "ambientRampWhyAutoRemapConfidenceMomentumAlias": ["ARW AUTO PLAN CONF MOMENTUM:"],
    "ambientRampWhyAutoRemapConfidenceMomentumCompactAlias": ["ARW MOMENTUM:"],
    "ambientRampWhyAutoRemapMomentumArcAlias": ["ARW MOMENTUM ARC:"],
    "ambientRampWhyAutoRemapMomentumArcPulseAlias": ["ARW ARC PULSE:"],
    "pulseHeatFxAlias": ["PULSE HEAT FX:"],
    "routeGlowFxAlias": ["ROUTE GLOW FX:", "RGFX:"],
    "routeGlowAlias": ["ROUTE GLOW:"],
    "routeGlowConfidenceAlias": ["ROUTE GLOW CONF:", "RGC:"],
    "routeGlowFxConfidenceAlias": ["ROUTE GLOW FX CONF:", "RGFXC:"],
    "routeGlowFxConfidenceWhyAlias": ["ROUTE GLOW FX CONF WHY:", "RGFXW:"],
    "routeGlowFxConfidenceWhyRailAlias": ["ROUTE GLOW FX CONF WHY RAIL:", "RGFXWR:"],
    "routeGlowFxConfidenceWhyRailMode": ["RGFXWRM:"],
    "routeGlowFxConfidenceWhyRailIntensity": ["RGFXWRI:"],
    "routeGlowFxConfidenceWhyRailIntensityWhy": ["RGFXWRI WHY:"],
    "routeGlowFxConfidenceWhyRailIntensityWhyConfidenceAlias": ["RGFXWRI WHY CONF:", "RGFXWRIWC:"],
    "routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyAlias": ["ROUTE GLOW FX CONF WHY RAIL INTENSITY WHY CONF URGENCY:", "RGFXWRIU:"],
    "routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyParityCompactAlias": ["RGFXWRIUP:"],
    "routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyDetailed": ["ROUTE GLOW FX CONF WHY RAIL INTENSITY WHY CONF URGENCY:"],
    "routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyFxAlias": ["RGFXWRIUFX:"],
    "urgencyStackTierAlias": ["URG STACK:"],
    "urgencyStackRailAlias": ["URG STACK RAIL:"],
    "dmgnumStackCapAlias": ["DMGNUM STACK CAP:"],
    "dmgnumLifeAlias": ["DMGNUM LIFE:"],
    "dmgnumLifeConfidenceAlias": ["DMGNUM LIFE CONF:"],
    "dmgnumLifeConfidenceDeltaAlias": ["DMGNUM LIFE CONF Δ:"],
    "dmgnumLifeTrendAlias": ["DMGNUM LIFE TREND:"],
    "dmgnumLifeTrendFxPulseAlias": ["DMGNUM LIFE TREND FX PULSE:"],
    "dmgnumLifeTrendFxPulseConfidenceAlias": ["DMGNUM LIFE TREND FX PULSE CONF:"],
    "dmgnumLifeTrendFxPulseRemapPlanAlias": ["DMGNUM LIFE TREND FX PULSE REMAP PLAN:"],
    "dmgComboAlias": ["DMG COMBO:"],
    "dmgComboConfidenceAlias": ["DMG COMBO CONF:"],
    "dmgComboRetuneAlias": ["DCR:", "DMG COMBO WINDOW RETUNE REC:"],
    "dmgComboRetuneConfidenceAlias": ["DCRC:", "DMG COMBO WINDOW RETUNE CONF:"],
    "dmgComboChainCoachAlias": ["DMG COMBO CHAIN COACH:"],
    "dmgComboConfidenceCoachAlias": ["DMG COMBO CONF COACH REC:", "DCCR:"],
    "dmgComboConfidenceCoachSceneArcAlias": ["DMG COMBO CONF COACH SCENE ARC:", "DCCSA:"],
    "dmgComboConfidenceFxAccentAlias": ["DMG COMBO CONF FX ACCENT:", "DCCFX:"],
    "dmgComboConfidenceFxAccentTrendAlias": ["DCCFXT:"],
    "dmgComboConfidenceFxAccentVolatilityAlias": ["DCCFXV:"],
    "dmgComboConfidenceCoachCopySwapRecommendationAlias": ["DMG COMBO CONF COACH COPY SWAP REC:", "DCCSR:"],
    "dmgComboConfidenceCoachCopySwapTrendAlias": ["DCCST:"],
    "pulseRemapMomentumAlias": ["PULSE REMAP MOMENTUM:", "PRM:"],
    "pulseRemapMomentumSuppressionAlias": ["PULSE REMAP MOMENTUM SUPPRESS:", "PRMS:"],
    "pulseRemapSuppressionPlanAlias": ["PULSE REMAP SUPPRESS PLAN:", "PRSP:"],
    "pulseRemapSceneMicrolineVariantPackAlias": ["PULSE REMAP SCENE MICROLINE VARIANT PACK:"],
    "pulseRemapSceneMicrolineVariantPackSelectionAlias": ["PRSMV:"],
    "pulseRemapSceneMicrolineStylePolicyAlias": ["PULSE REMAP SCENE MICROLINE STYLE POLICY:", "PRSMP:"],
    "pulseRemapSceneMicrolineStylePostureAlias": ["PULSE REMAP SCENE MICROLINE STYLE POSTURE:", "PRSMPP:"],
    "pulseRemapSceneMicrolineCadenceAlias": ["PULSE REMAP SCENE MICROLINE CADENCE:", "PRSMC:"],
    "pulseRemapSceneFxGlintAlias": ["PULSE REMAP SCENE FX GLINT:", "PRSFX:"],
    "pulseRemapSceneCopyPaletteRecommendationAlias": ["PULSE REMAP SCENE COPY PALETTE REC:", "PRSCP:"],
    "pulseRemapSuppressionPostureWarningAlias": ["PRPW:"],
    "dmgGlyphAlias": ["DMG GLYPH:"],
    "dmgGlyphFxLiveAlias": ["DMG GLYPH FX LIVE:"],
    "lanePriorityHysteresisThresholdAlias": ["LPR HYS THR:"],
    "lanePriorityHysteresisWindowDeltaAlias": ["LPR HYS WINDOW Δ:"],
    "lanePriorityHysteresisFloorRecommendationAlias": ["LPR HYS FLOOR REC:", "LPR HYS FLOOR:"],
    "lanePriorityHysteresisFloorFamilyTrendAlias": ["LPR HYS FLOOR FAMILY TREND:", "LPR HF T:"],
    "lanePriorityRecommendationConfidenceGuardAlias": ["LPRCG:", "LANE PRIORITY REC CONF GUARD:"],
    "lanePriorityRecommendationConfidenceGuardThresholdAlias": ["LPRCG THRESH:"],
    "lanePriorityRecommendationConfidenceGuardCoachAlias": ["LPRCG COACH:", "LPRCGC:"],
    "lanePriorityRecommendationConfidenceGuardCoachPackAlias": ["LPRCG COACH PACK:", "LPRCGCP:"],
    "lanePriorityRecommendationConfidenceGuardCoachCopyAlias": ["LPRCG COACH COPY:", "LPRCGCN:"],
    "lanePriorityRecommendationConfidenceGuardCoachCopyWhy": ["LPRCG COACH COPY WHY:"],
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
    p.add_argument("--out-fx-remap-candidates-json", type=Path, default=DEFAULT_DMG_GLYPH_FX_REMAP_CANDIDATES_JSON)
    p.add_argument("--out-fx-remap-candidates-md", type=Path, default=DEFAULT_DMG_GLYPH_FX_REMAP_CANDIDATES_MD)
    p.add_argument("--out-ambient-why-auto-remap-plan-json", type=Path, default=DEFAULT_AMBIENT_RAMP_WHY_AUTO_REMAP_PLAN_JSON)
    p.add_argument("--out-ambient-why-auto-remap-plan-md", type=Path, default=DEFAULT_AMBIENT_RAMP_WHY_AUTO_REMAP_PLAN_MD)
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


def token_family_coverage(token_totals: dict[str, dict[str, int]]) -> dict[str, dict[str, object]]:
    families: dict[str, dict[str, object]] = {}
    for family, aliases in TOKEN_ALIAS_FAMILIES.items():
        added = sum(token_totals["added"].get(alias, 0) for alias in aliases)
        removed = sum(token_totals["removed"].get(alias, 0) for alias in aliases)
        net = sum(token_totals["net"].get(alias, 0) for alias in aliases)
        aliases_touched = [
            alias
            for alias in aliases
            if token_totals["added"].get(alias, 0) > 0 or token_totals["removed"].get(alias, 0) > 0
        ]
        families[family] = {
            "aliases": aliases,
            "aliasesTouched": aliases_touched,
            "aliasesTouchedCount": len(aliases_touched),
            "added": added,
            "removed": removed,
            "net": net,
            "churn": added + removed,
            "coverage": f"{len(aliases_touched)}/{len(aliases)}",
        }
    return families


def lane_bucket_age_hours(rows: list[dict[str, object]], *, now_utc: datetime) -> dict[str, object]:
    """Return 24h freshness ages for lane cadence buckets from touched commits.

    Buckets follow Team Operating Protocol cadence: combat/vfx, design/world, systems/ops.
    """
    bucket_alias_families = {
        "combat/vfx": [
            "pulseHeatFxAlias",
            "dmgnumStackCapAlias",
            "dmgnumLifeAlias",
            "dmgnumLifeConfidenceAlias",
            "dmgnumLifeConfidenceDeltaAlias",
            "dmgnumLifeTrendAlias",
            "dmgComboAlias",
            "dmgGlyphAlias",
            "dmgGlyphFxLiveAlias",
            "routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyFxAlias",
        ],
        "design/world": [
            "vibeTrailWhyAlias",
            "vibeTrailWhyConfidenceAlias",
            "vibeTrailWhyConfidenceWhyAlias",
            "vibeTrailWhyConfidenceWhyConfidenceAlias",
            "vibeTrailArcAlias",
            "ambientRampConfidenceAlias",
            "ambientRampWhyAlias",
            "routeGlowAlias",
            "routeGlowFxAlias",
            "routeGlowConfidenceAlias",
            "routeGlowFxConfidenceAlias",
            "routeGlowFxConfidenceWhyAlias",
            "routeGlowFxConfidenceWhyRailAlias",
            "routeGlowFxConfidenceWhyRailMode",
            "routeGlowFxConfidenceWhyRailIntensity",
            "routeGlowFxConfidenceWhyRailIntensityWhy",
            "routeGlowFxConfidenceWhyRailIntensityWhyConfidenceAlias",
            "routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyAlias",
            "routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyParityCompactAlias",
            "routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyDetailed",
            "urgencyStackTierAlias",
            "urgencyStackRailAlias",
        ],
        "systems/ops": [
            "ambientRampWhyAutoRemapPlanAlias",
            "ambientRampWhyAutoRemapConfidenceBandAlias",
            "ambientRampWhyAutoRemapConfidenceMomentumAlias",
            "ambientRampWhyAutoRemapConfidenceMomentumCompactAlias",
            "ambientRampWhyAutoRemapMomentumArcAlias",
        ],
    }

    freshest: dict[str, datetime | None] = {bucket: None for bucket in bucket_alias_families}
    for row in rows:
        if not row.get("touchedPortalPrompt"):
            continue
        committed_at = str(row.get("committedAt", "")).strip()
        if not committed_at:
            continue
        try:
            committed_dt = datetime.fromisoformat(committed_at.replace("Z", "+00:00")).astimezone(timezone.utc)
        except ValueError:
            continue
        token_edits = row.get("tokenEdits")
        if not isinstance(token_edits, dict):
            continue
        added = token_edits.get("added", {})
        removed = token_edits.get("removed", {})
        if not isinstance(added, dict) or not isinstance(removed, dict):
            continue

        for bucket, families in bucket_alias_families.items():
            touched_bucket = False
            for family in families:
                aliases = TOKEN_ALIAS_FAMILIES.get(family, [])
                if any(int(added.get(alias, 0)) > 0 or int(removed.get(alias, 0)) > 0 for alias in aliases):
                    touched_bucket = True
                    break
            if touched_bucket and (freshest[bucket] is None or committed_dt > freshest[bucket]):
                freshest[bucket] = committed_dt

    age_hours: dict[str, int] = {}
    for bucket, latest in freshest.items():
        if latest is None:
            age_hours[bucket] = 999
            continue
        delta = now_utc - latest
        age_hours[bucket] = max(0, int(delta.total_seconds() // 3600))

    cadence_ok = all(age_hours[bucket] <= 24 for bucket in bucket_alias_families)
    compact = f"SYSTEMS/OPS {age_hours['systems/ops']}H | DESIGN/WORLD {age_hours['design/world']}H | COMBAT/VFX {age_hours['combat/vfx']}H"
    return {
        "token": f"LANE BUCKET AGE:{compact}",
        "status": "OK" if cadence_ok else "GAP",
        "ageHours": age_hours,
        "maxAgeHours": max(age_hours.values()) if age_hours else 999,
        "windowHours": 24,
    }


def lane_bucket_age_drift(*, current_max_age_hours: int, prior_json_path: Path) -> tuple[int, dict[str, object]]:
    prior_loaded = False
    prior_max_age = current_max_age_hours
    if prior_json_path.exists():
        try:
            prior_payload = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_max_age = int(prior_payload.get("laneBucketAgeMaxHours", current_max_age_hours) or current_max_age_hours)
            prior_loaded = True
        except (json.JSONDecodeError, OSError, ValueError, TypeError):
            prior_max_age = current_max_age_hours
    drift = current_max_age_hours - prior_max_age
    return drift, {
        "currentMaxAgeHours": current_max_age_hours,
        "priorMaxAgeHours": prior_max_age,
        "priorLoaded": prior_loaded,
    }


def lane_cadence_recency_from_age_drift(*, lane_bucket_age: dict[str, object], lane_bucket_age_delta: int) -> tuple[str, dict[str, object]]:
    max_age_hours = int(lane_bucket_age.get("maxAgeHours", 999) or 999)
    status = "OK" if max_age_hours <= 24 and lane_bucket_age_delta <= 0 else "WARN"
    token = f"LANE CADENCE RECENCY:{status.lower()}"

    if status == "OK":
        reason = "all-lanes-fresh-and-nonregressing"
    elif max_age_hours > 24 and lane_bucket_age_delta > 0:
        reason = "lane-gap-and-regressing"
    elif max_age_hours > 24:
        reason = "lane-gap-persistent"
    else:
        reason = "freshness-regressing"

    return token, {
        "status": status,
        "maxAgeHours": max_age_hours,
        "deltaHours": int(lane_bucket_age_delta),
        "windowHours": int(lane_bucket_age.get("windowHours", 24) or 24),
        "reason": reason,
    }




def lane_cadence_miss_risk(*, lane_bucket_age: dict[str, object], lane_bucket_age_delta: int) -> tuple[str, dict[str, object]]:
    max_age_hours = int(lane_bucket_age.get("maxAgeHours", 999) or 999)
    window_hours = int(lane_bucket_age.get("windowHours", 24) or 24)

    if max_age_hours <= window_hours and lane_bucket_age_delta <= 0:
        risk = "LOW"
        reason = "all-lanes-fresh-and-stable"
    elif max_age_hours > (window_hours + 12) or (max_age_hours > window_hours and lane_bucket_age_delta > 0):
        risk = "HIGH"
        reason = "stale-lane-gap-escalating"
    else:
        risk = "MID"
        reason = "freshness-drift-watch"

    return f"LANE CADENCE MISS RISK:{risk}", {
        "risk": risk,
        "maxAgeHours": max_age_hours,
        "deltaHours": int(lane_bucket_age_delta),
        "windowHours": window_hours,
        "reason": reason,
    }

def lane_bucket_age_alias(*, lane_bucket_age: dict[str, object]) -> tuple[str, dict[str, object]]:
    flag_name = "DOTPIO_EXPERIMENT_LANE_BUCKET_AGE_ALIAS"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    age_hours = lane_bucket_age.get("ageHours", {})
    if not isinstance(age_hours, dict):
        age_hours = {}

    systems = int(age_hours.get("systems/ops", 999) or 999)
    design = int(age_hours.get("design/world", 999) or 999)
    combat = int(age_hours.get("combat/vfx", 999) or 999)
    token = f"LBA:{systems}/{design}/{combat}"

    return (token if flag_enabled else "OFF"), {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "systemsOpsHours": systems,
        "designWorldHours": design,
        "combatVfxHours": combat,
    }

def lane_cadence_miss_risk_alias(*, lane_cadence_miss_risk_signals: dict[str, object]) -> tuple[str, dict[str, object]]:
    flag_name = "DOTPIO_EXPERIMENT_LANE_CADENCE_MISS_RISK_ALIAS"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    risk = str(lane_cadence_miss_risk_signals.get("risk", "MID") or "MID").upper()
    alias_map = {
        "LOW": "L",
        "MID": "M",
        "HIGH": "H",
    }
    alias = alias_map.get(risk, "M")
    token = f"LCMR:{alias}"

    return (token if flag_enabled else "OFF"), {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "risk": risk,
        "alias": alias,
    }


def lane_priority_hysteresis_floor_recommendation_from_lcmr_streak(
    *,
    lane_cadence_miss_risk_signals: dict[str, object],
    prior_json_path: Path,
) -> tuple[str, dict[str, object]]:
    """Offline-only recommendation to hold/raise hysteresis floor from LCMR streak memory."""
    current_risk = str(lane_cadence_miss_risk_signals.get("risk", "MID") or "MID").upper()
    current_delta = int(lane_cadence_miss_risk_signals.get("deltaHours", 0) or 0)

    prior_loaded = False
    prior_risk = "UNKNOWN"
    prior_high_streak = 0

    if prior_json_path.exists():
        try:
            prior_payload = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_risk_token = str(prior_payload.get("laneCadenceMissRisk", "") or "")
            if ":" in prior_risk_token:
                prior_risk = prior_risk_token.split(":", 1)[1].strip().upper()
            prior_high_streak = int(prior_payload.get("laneCadenceMissRiskHighStreak", 0) or 0)
            prior_loaded = True
        except (json.JSONDecodeError, OSError, TypeError, ValueError):
            prior_loaded = False

    prior_volatility_regime = "UNKNOWN"
    if prior_loaded:
        prior_regime_token = str(prior_payload.get("lanePriorityVolatilityRegimeMemory", "") or "")
        if ":" in prior_regime_token:
            prior_volatility_regime = prior_regime_token.split(":", 1)[1].strip().upper()

    high_streak = prior_high_streak + 1 if current_risk == "HIGH" else 0
    strong_momentum = current_risk == "HIGH" and current_delta > 0

    threshold_by_regime = {
        "CALM": 1,
        "SWING": 2,
        "SPIKE": 3,
    }
    threshold = threshold_by_regime.get(prior_volatility_regime, 2)
    if strong_momentum and threshold > 1:
        threshold -= 1

    if high_streak >= threshold or strong_momentum:
        recommendation = "RAISE"
        reason = "lcmr-streak-cleared-adaptive-threshold"
    else:
        recommendation = "HOLD"
        reason = "lcmr-streak-below-adaptive-threshold"

    return f"LPR HYS FLOOR REC:{recommendation}", {
        "offlineOnly": True,
        "currentRisk": current_risk,
        "priorRisk": prior_risk,
        "currentDeltaHours": current_delta,
        "priorLoaded": prior_loaded,
        "priorHighStreak": prior_high_streak,
        "highStreak": high_streak,
        "streakThreshold": threshold,
        "streakThresholdByRegime": threshold_by_regime,
        "priorVolatilityRegime": prior_volatility_regime,
        "strongMomentum": strong_momentum,
        "recommendation": recommendation,
        "reason": reason,
    }


def resolve_lane_priority_hysteresis_floor_recommendation_alias(*, recommendation_token: str) -> tuple[str, dict[str, object]]:
    flag_name = "DOTPIO_EXPERIMENT_LANE_PRIORITY_HYSTERESIS_FLOOR_REC_ALIAS"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    rec_upper = str(recommendation_token or "LPR HYS FLOOR REC:HOLD").upper()
    if rec_upper.endswith(":RAISE"):
        alias = "R"
    else:
        alias = "H"

    token = f"LPR HYS FLOOR:{alias}"
    return (token if flag_enabled else "OFF"), {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "recommendation": rec_upper,
        "alias": alias,
    }


def resolve_lane_priority_recommendation_compact_alias(recommendation: str) -> tuple[str, dict[str, object]]:
    flag_name = "DOTPIO_EXPERIMENT_LANE_PRIORITY_REC_ALIAS"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    alias_map = {
        "BALANCED": "BAL",
        "SYSTEMS/OPS": "SYS",
        "DESIGN/WORLD": "DW",
        "COMBAT/VFX": "CV",
    }
    alias = alias_map.get(str(recommendation).upper(), "UNK")
    token = f"LPR:{alias}"
    return (token if flag_enabled else "OFF"), {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "recommendation": str(recommendation).upper(),
        "alias": alias,
    }


def resolve_lane_priority_hysteresis_alias(*, hysteresis_applied: bool) -> tuple[str, dict[str, object]]:
    flag_name = "DOTPIO_EXPERIMENT_LANE_PRIORITY_HYSTERESIS_ALIAS"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}
    alias = "H" if hysteresis_applied else "S"
    token = f"LPR HYS:{alias}"
    return (token if flag_enabled else "OFF"), {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "hysteresisApplied": hysteresis_applied,
        "alias": alias,
    }


def resolve_lane_priority_hysteresis_rail(*, confidence: str, hysteresis_applied: bool, score_gap: int, threshold: int) -> tuple[str, dict[str, object]]:
    flag_name = "DOTPIO_EXPERIMENT_LANE_PRIORITY_HYSTERESIS_RAIL"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    confidence_upper = str(confidence or "LOW").upper()
    close_gap_threshold = max(2, int(threshold or 0) // 3)
    if hysteresis_applied or confidence_upper == "LOW" or int(score_gap or 0) <= close_gap_threshold:
        rail = "SPIKE"
        reason = "hysteresis-applied-or-low-confidence-gap"
    else:
        rail = "STEADY"
        reason = "confidence-stable-gap-clear"

    token = f"LPR HYS RAIL:{rail}"
    return (token if flag_enabled else "OFF"), {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "confidence": confidence_upper,
        "hysteresisApplied": bool(hysteresis_applied),
        "scoreGap": int(score_gap or 0),
        "threshold": int(threshold or 0),
        "closeGapThreshold": close_gap_threshold,
        "rail": rail,
        "reason": reason,
    }


def resolve_lane_priority_hysteresis_threshold_tuning(
    *,
    lane_priority_recommendation_signals: dict[str, object],
    prior_json_path: Path,
) -> tuple[str, dict[str, object]]:
    """Offline-only recommendation for hysteresis threshold tuning from lane-age volatility windows.

    Includes adaptive floor/ceiling learning based on prior-window volatility outcomes.
    """
    momentum_hours_raw = lane_priority_recommendation_signals.get("momentumHours", {})
    momentum_hours = momentum_hours_raw if isinstance(momentum_hours_raw, dict) else {}
    momentum_values = [int(v or 0) for v in momentum_hours.values()]
    volatility_span = (max(momentum_values) - min(momentum_values)) if momentum_values else 0
    max_abs_momentum = max((abs(v) for v in momentum_values), default=0)

    current_age_raw = lane_priority_recommendation_signals.get("currentAgeHours", {})
    current_age_hours = current_age_raw if isinstance(current_age_raw, dict) else {}
    age_values = [int(v or 0) for v in current_age_hours.values()]
    age_spread = (max(age_values) - min(age_values)) if age_values else 0

    base_threshold = int(lane_priority_recommendation_signals.get("hysteresisThreshold", 12) or 12)

    prior_floor = 8
    prior_ceiling = 18
    prior_loaded = False
    prior_regime = "SWING"
    try:
        if prior_json_path.exists():
            prior_payload = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_tuning = prior_payload.get("lanePriorityHysteresisThresholdTuningSignals", {})
            if isinstance(prior_tuning, dict):
                prior_floor = int(prior_tuning.get("adaptiveFloor", prior_floor) or prior_floor)
                prior_ceiling = int(prior_tuning.get("adaptiveCeiling", prior_ceiling) or prior_ceiling)
                prior_loaded = True

            prior_regime_token = str(prior_payload.get("lanePriorityVolatilityRegimeMemory", "") or "")
            if ":" in prior_regime_token:
                prior_regime = prior_regime_token.split(":", 1)[1].strip().upper() or "SWING"
    except (json.JSONDecodeError, OSError, TypeError, ValueError):
        prior_loaded = False

    floor = max(6, min(14, prior_floor))
    ceiling = max(floor + 4, min(24, prior_ceiling))
    learning_reason = "baseline floor/ceiling window"

    high_volatility = max_abs_momentum >= 24 or volatility_span >= 18 or age_spread >= 36
    low_volatility = max_abs_momentum <= 4 and volatility_span <= 6 and age_spread <= 12

    if high_volatility:
        current_regime = "SPIKE"
    elif low_volatility:
        current_regime = "CALM"
    else:
        current_regime = "SWING"

    if (prior_regime == "CALM" and current_regime == "SPIKE") or (prior_regime == "SPIKE" and current_regime == "CALM"):
        regime_memory = "SWING"
        regime_reason = "hard regime flip damped through swing memory"
    else:
        regime_memory = current_regime
        regime_reason = "regime memory follows current volatility"

    step_sizes = {
        "CALM": {"raise_floor": 1, "raise_ceiling": 1, "lower_floor": 2, "lower_ceiling": 2},
        "SWING": {"raise_floor": 1, "raise_ceiling": 2, "lower_floor": 1, "lower_ceiling": 1},
        "SPIKE": {"raise_floor": 2, "raise_ceiling": 3, "lower_floor": 0, "lower_ceiling": 0},
    }
    steps = step_sizes.get(regime_memory, step_sizes["SWING"])

    if high_volatility:
        floor = min(floor + steps["raise_floor"], 14)
        ceiling = min(max(ceiling + steps["raise_ceiling"], floor + 4), 24)
        learning_reason = "high volatility widened window using regime step-size memory"
    elif low_volatility:
        floor = max(floor - steps["lower_floor"], 6)
        ceiling = max(min(ceiling - steps["lower_ceiling"], 24), floor + 4)
        learning_reason = "low volatility tightened window using regime step-size memory"

    tuned_threshold = max(floor, min(ceiling, base_threshold))
    mode = "HOLD"
    reason = "volatility signals near baseline; keep hysteresis threshold"

    if high_volatility:
        tuned_threshold = min(ceiling, max(base_threshold + 4, floor))
        mode = "RAISE"
        reason = "lane-age volatility is high; raise threshold to suppress flapping"
    elif low_volatility:
        tuned_threshold = max(floor, min(base_threshold - 2, ceiling))
        mode = "LOWER"
        reason = "lane-age volatility is calm; lower threshold for quicker adaptation"

    return f"LPR HYS THRESH REC:{mode}", {
        "offlineOnly": True,
        "baseThreshold": base_threshold,
        "recommendedThreshold": tuned_threshold,
        "mode": mode,
        "maxAbsMomentumHours": max_abs_momentum,
        "momentumVolatilitySpanHours": volatility_span,
        "ageSpreadHours": age_spread,
        "adaptiveFloor": floor,
        "adaptiveCeiling": ceiling,
        "priorAdaptiveWindowLoaded": prior_loaded,
        "volatilityRegime": current_regime,
        "priorVolatilityRegime": prior_regime,
        "volatilityRegimeMemory": regime_memory,
        "volatilityRegimeReason": regime_reason,
        "stepSizes": {
            "raiseFloor": steps["raise_floor"],
            "raiseCeiling": steps["raise_ceiling"],
            "lowerFloor": steps["lower_floor"],
            "lowerCeiling": steps["lower_ceiling"],
        },
        "learningReason": learning_reason,
        "reason": reason,
    }


def resolve_lane_priority_hysteresis_threshold_compact_alias(*, recommendation: str) -> tuple[str, dict[str, object]]:
    flag_name = "DOTPIO_EXPERIMENT_LANE_PRIORITY_HYSTERESIS_THRESHOLD_ALIAS"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    mode_upper = str(recommendation or "LPR HYS THRESH REC:HOLD").upper()
    alias_map = {
        "LPR HYS THRESH REC:LOWER": "L",
        "LPR HYS THRESH REC:HOLD": "H",
        "LPR HYS THRESH REC:RAISE": "R",
    }
    alias = alias_map.get(mode_upper, "H")
    token = f"LPR HYS THR:{alias}"
    return (token if flag_enabled else "OFF"), {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "recommendation": mode_upper,
        "alias": alias,
    }


def resolve_lane_priority_hysteresis_window_band(*, tuning_signals: dict[str, object]) -> tuple[str, dict[str, object]]:
    """Classify adaptive hysteresis floor/ceiling span for quick offline triage."""
    floor = int(tuning_signals.get("adaptiveFloor", 8) or 8)
    ceiling = int(tuning_signals.get("adaptiveCeiling", 18) or 18)
    span = max(0, ceiling - floor)

    if span <= 8:
        band = "TIGHT"
        reason = "adaptive window is narrow for fast recommendation shifts"
    elif span >= 12:
        band = "WIDE"
        reason = "adaptive window is wide to suppress lane-priority flapping"
    else:
        band = "BASE"
        reason = "adaptive window remains near baseline spread"

    return f"LPR HYS WINDOW:{band}", {
        "adaptiveFloor": floor,
        "adaptiveCeiling": ceiling,
        "span": span,
        "band": band,
        "reason": reason,
    }


def resolve_lane_priority_hysteresis_window_delta(*, current_band: str, prior_json_path: Path) -> tuple[str, int, dict[str, object]]:
    """Compare adaptive-window band against prior digest for compact stability drift triage."""
    band_score = {"TIGHT": -1, "BASE": 0, "WIDE": 1}
    current_band_upper = str(current_band or "BASE").upper()
    current_score = band_score.get(current_band_upper, 0)

    prior_loaded = False
    prior_band = current_band_upper
    prior_score = current_score
    if prior_json_path.exists():
        try:
            prior_payload = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_token = str(prior_payload.get("lanePriorityHysteresisWindowBand", "") or "")
            prior_band = prior_token.split(":", 1)[1].strip().upper() if ":" in prior_token else current_band_upper
            prior_score = band_score.get(prior_band, current_score)
            prior_loaded = True
        except (json.JSONDecodeError, OSError, TypeError, ValueError):
            prior_loaded = False
            prior_band = current_band_upper
            prior_score = current_score

    delta = current_score - prior_score
    token = f"LPR HYS WINDOW Δ:{delta:+d}"
    signals = {
        "currentBand": current_band_upper,
        "priorBand": prior_band,
        "currentScore": current_score,
        "priorScore": prior_score,
        "delta": delta,
        "priorLoaded": prior_loaded,
    }
    return token, delta, signals


def lane_priority_recommendation_from_bucket_age_momentum(
    *,
    age_hours: dict[str, int],
    prior_json_path: Path,
) -> tuple[str, dict[str, object]]:
    prior_loaded = False
    prior_age_hours: dict[str, int] = {
        "systems/ops": int(age_hours.get("systems/ops", 999) or 999),
        "design/world": int(age_hours.get("design/world", 999) or 999),
        "combat/vfx": int(age_hours.get("combat/vfx", 999) or 999),
    }
    if prior_json_path.exists():
        try:
            prior_payload = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_age_raw = prior_payload.get("laneBucketAgeHours", {})
            if isinstance(prior_age_raw, dict):
                for lane in prior_age_hours:
                    prior_age_hours[lane] = int(prior_age_raw.get(lane, prior_age_hours[lane]) or prior_age_hours[lane])
            prior_loaded = True
        except (json.JSONDecodeError, OSError, TypeError, ValueError):
            prior_loaded = False

    current_age_hours = {
        lane: int(age_hours.get(lane, 999) or 999)
        for lane in prior_age_hours
    }
    momentum_hours = {
        lane: current_age_hours[lane] - prior_age_hours[lane]
        for lane in current_age_hours
    }
    momentum_boost = {
        lane: max(0, momentum_hours[lane]) * 2
        for lane in current_age_hours
    }
    priority_scores = {
        lane: current_age_hours[lane] + momentum_boost[lane]
        for lane in current_age_hours
    }

    worst_age = max(current_age_hours.values()) if current_age_hours else 0
    stale_lanes = [lane for lane, hours in current_age_hours.items() if hours > 24]
    hottest_lane = max(priority_scores, key=priority_scores.get) if priority_scores else "systems/ops"

    if worst_age <= 24 and all(delta <= 0 for delta in momentum_hours.values()):
        recommendation_raw = "BALANCED"
        reason = "all lane buckets are within 24h and momentum is non-increasing"
    elif stale_lanes:
        recommendation_raw = hottest_lane.upper()
        reason = "stale lane bucket requires offline priority intervention"
    else:
        recommendation_raw = hottest_lane.upper()
        reason = "bucket-age momentum is rising and should be preemptively prioritized"

    prior_recommendation = "UNKNOWN"
    if prior_loaded:
        try:
            prior_payload = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_recommendation = str(prior_payload.get("lanePriorityRecommendation", "UNKNOWN") or "UNKNOWN").upper()
        except (json.JSONDecodeError, OSError, TypeError, ValueError):
            prior_recommendation = "UNKNOWN"

    recommendation = recommendation_raw
    hysteresis_applied = False
    hysteresis_reason = "no prior recommendation available"
    hysteresis_score_gap = 0
    hysteresis_threshold = 12

    lane_scores_upper = {lane.upper(): score for lane, score in priority_scores.items()}
    prior_known_lane = prior_recommendation in lane_scores_upper
    raw_known_lane = recommendation_raw in lane_scores_upper
    severe_staleness = worst_age >= 72

    if not prior_loaded:
        hysteresis_reason = "no prior digest window; hysteresis skipped"
    elif prior_recommendation == recommendation_raw:
        hysteresis_reason = "recommendation unchanged from prior window"
    elif prior_known_lane and raw_known_lane and not severe_staleness:
        hysteresis_score_gap = lane_scores_upper[recommendation_raw] - lane_scores_upper[prior_recommendation]
        if hysteresis_score_gap < hysteresis_threshold:
            recommendation = prior_recommendation
            hysteresis_applied = True
            hysteresis_reason = "held prior lane recommendation to suppress flapping"
        else:
            hysteresis_reason = "new lane recommendation cleared hysteresis threshold"
    elif severe_staleness:
        hysteresis_reason = "severe staleness bypassed hysteresis suppression"
    else:
        hysteresis_reason = "prior/raw recommendation pair not eligible for lane hysteresis"

    return recommendation, {
        "offlineOnly": True,
        "priorLoaded": prior_loaded,
        "priorRecommendation": prior_recommendation,
        "rawRecommendation": recommendation_raw,
        "hysteresisApplied": hysteresis_applied,
        "hysteresisThreshold": hysteresis_threshold,
        "hysteresisScoreGap": hysteresis_score_gap,
        "hysteresisReason": hysteresis_reason,
        "currentAgeHours": current_age_hours,
        "priorAgeHours": prior_age_hours,
        "momentumHours": momentum_hours,
        "momentumBoost": momentum_boost,
        "priorityScores": priority_scores,
        "staleLanes": [lane.upper() for lane in stale_lanes],
        "worstAgeHours": worst_age,
        "reason": reason,
    }


def lane_priority_recommendation_confidence(
    *,
    lane_priority_recommendation: str,
    lane_priority_recommendation_signals: dict[str, object],
) -> tuple[str, dict[str, object]]:
    worst_age_hours = int(lane_priority_recommendation_signals.get("worstAgeHours", 0) or 0)
    momentum_hours_raw = lane_priority_recommendation_signals.get("momentumHours", {})
    momentum_hours = momentum_hours_raw if isinstance(momentum_hours_raw, dict) else {}
    max_momentum = max((int(v or 0) for v in momentum_hours.values()), default=0)
    momentum_gap = max_momentum

    if str(lane_priority_recommendation).upper() == "BALANCED":
        confidence = "HIGH"
        reason = "all lane buckets are fresh and momentum is stable"
    elif worst_age_hours >= 72 or momentum_gap >= 24:
        confidence = "HIGH"
        reason = "lane priority signal is strongly separated by age/momentum"
    elif worst_age_hours >= 36 or momentum_gap >= 12:
        confidence = "MID"
        reason = "lane priority signal has moderate separation"
    else:
        confidence = "LOW"
        reason = "lane priority signal is weakly separated"

    return confidence, {
        "recommendation": str(lane_priority_recommendation).upper(),
        "worstAgeHours": worst_age_hours,
        "momentumGapHours": momentum_gap,
        "maxMomentumHours": max_momentum,
        "reason": reason,
    }


def lane_priority_recommendation_confidence_guard(
    *,
    confidence: str,
    floor_family_trend_signals: dict[str, object],
    lane_priority_hysteresis_threshold_tuning_signals: dict[str, object],
    prior_json_path: Path,
) -> tuple[str, dict[str, object]]:
    """Offline-only confidence guard when floor-family trend conflicts with volatility regime across windows."""
    trend = str(floor_family_trend_signals.get("trend", "FLAT") or "FLAT").upper()
    regime = str(lane_priority_hysteresis_threshold_tuning_signals.get("volatilityRegimeMemory", "SWING") or "SWING").upper()

    diverged = (
        (trend == "UP" and regime == "CALM")
        or (trend == "DOWN" and regime == "SPIKE")
        or (regime == "SWING" and trend in {"UP", "DOWN"})
    )

    prior_streak = 0
    prior_loaded = False
    if prior_json_path.exists():
        try:
            prior_payload = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_signals = prior_payload.get("lanePriorityRecommendationConfidenceGuardSignals", {})
            if isinstance(prior_signals, dict):
                prior_streak = int(prior_signals.get("divergenceStreak", 0) or 0)
                prior_loaded = True
        except (json.JSONDecodeError, OSError, TypeError, ValueError):
            prior_streak = 0
            prior_loaded = False

    swing_memory_active = regime == "SWING" and str(
        lane_priority_hysteresis_threshold_tuning_signals.get("volatilityRegimeReason", "") or ""
    ).strip().lower() in {
        "memory-hold-from-prior-regime",
        "memory-smooth-regime-shift",
    }
    divergence_threshold = 3 if swing_memory_active else 2
    threshold_policy = "SWING_MEMORY_GUARD_RAISED" if swing_memory_active else "BASELINE"

    divergence_streak = prior_streak + 1 if diverged else 0
    guard_applied = divergence_streak >= divergence_threshold

    confidence_order = ["LOW", "MID", "HIGH"]
    confidence_upper = str(confidence or "LOW").upper()
    confidence_idx = confidence_order.index(confidence_upper) if confidence_upper in confidence_order else 0

    if guard_applied:
        guarded_confidence = confidence_order[max(0, confidence_idx - 1)]
        reason = "floor-trend-regime-divergence-streak-triggered-confidence-guard"
    else:
        guarded_confidence = confidence_upper
        reason = "divergence-streak-below-adaptive-threshold"

    return guarded_confidence, {
        "baseConfidence": confidence_upper,
        "guardedConfidence": guarded_confidence,
        "trend": trend,
        "volatilityRegime": regime,
        "diverged": diverged,
        "priorStreak": prior_streak,
        "divergenceStreak": divergence_streak,
        "divergenceThreshold": divergence_threshold,
        "thresholdPolicy": threshold_policy,
        "guardApplied": guard_applied,
        "priorLoaded": prior_loaded,
        "reason": reason,
        "offlineOnly": True,
    }


def resolve_lane_priority_recommendation_confidence_guard_alias(*, guard_signals: dict[str, object]) -> tuple[str, dict[str, object]]:
    """Compact alias for confidence-guard action (`LPRCG:<H|A>`) for dense digest scans."""
    flag_name = "DOTPIO_EXPERIMENT_LANE_PRIORITY_REC_CONF_GUARD_ALIAS"
    flag_enabled = os.environ.get(flag_name, "").strip().lower() in {"1", "true", "yes", "on"}

    action = "APPLY" if bool(guard_signals.get("guardApplied", False)) else "HOLD"
    alias = "A" if action == "APPLY" else "H"
    token = f"LPRCG:{alias}"
    return (token if flag_enabled else "FLAG OFF"), {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "action": action,
        "alias": alias,
    }


def lane_priority_recommendation_confidence_guard_threshold_token(*, guard_signals: dict[str, object]) -> tuple[str, dict[str, object]]:
    """Compact threshold token for digest scanability (`LPRCG THRESH:<n>`)."""
    threshold = int(guard_signals.get("divergenceThreshold", 2) or 2)
    threshold = min(5, max(1, threshold))
    policy = str(guard_signals.get("thresholdPolicy", "BASELINE") or "BASELINE").upper()
    return f"LPRCG THRESH:{threshold}", {
        "threshold": threshold,
        "policy": policy,
    }


def lane_priority_recommendation_confidence_guard_persistence_coach(
    *,
    guard_signals: dict[str, object],
    prior_json_path: Path,
) -> tuple[str, dict[str, object]]:
    """Offline coaching cue when `LPRCG` stays APPLY across consecutive digest windows."""
    prior_streak = 0
    prior_loaded = False
    if prior_json_path.exists():
        try:
            prior_payload = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_signals = prior_payload.get("lanePriorityRecommendationConfidenceGuardPersistenceCoachSignals", {})
            if isinstance(prior_signals, dict):
                prior_streak = int(prior_signals.get("consecutiveApplyWindows", 0) or 0)
                prior_loaded = True
        except (json.JSONDecodeError, OSError, TypeError, ValueError):
            prior_streak = 0
            prior_loaded = False

    guard_action = "APPLY" if bool(guard_signals.get("guardApplied", False)) else "HOLD"
    consecutive_apply_windows = prior_streak + 1 if guard_action == "APPLY" else 0

    if guard_action == "APPLY" and consecutive_apply_windows >= 2:
        cue = "LPRCG COACH:STABILIZE"
        reason = "guard-remains-apply-across-consecutive-windows"
    elif guard_action == "APPLY":
        cue = "LPRCG COACH:WATCH"
        reason = "guard-apply-is-fresh-this-window"
    else:
        cue = "LPRCG COACH:RESET"
        reason = "guard-not-applied-this-window"

    return cue, {
        "guardAction": guard_action,
        "priorConsecutiveApplyWindows": prior_streak,
        "consecutiveApplyWindows": consecutive_apply_windows,
        "triggered": guard_action == "APPLY" and consecutive_apply_windows >= 2,
        "priorLoaded": prior_loaded,
        "reason": reason,
        "offlineOnly": True,
    }


def lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack(
    *,
    coach_signals: dict[str, object],
    guard_signals: dict[str, object],
    prior_json_path: Path,
) -> tuple[str, dict[str, object]]:
    """Offline adaptive coach-copy variant-pack policy from sustained `LPRCG:APPLY` streak depth."""
    prior_pack = "BASELINE"
    prior_regime = "CALM"
    prior_loaded = False
    if prior_json_path.exists():
        try:
            prior_payload = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_signals = prior_payload.get("lanePriorityRecommendationConfidenceGuardPersistenceCoachVariantPackSignals", {})
            if isinstance(prior_signals, dict):
                prior_pack = str(prior_signals.get("pack", "BASELINE") or "BASELINE").upper()
                prior_regime = str(prior_signals.get("volatilityRegime", "CALM") or "CALM").upper()
                prior_loaded = True
        except (json.JSONDecodeError, OSError, TypeError, ValueError):
            prior_pack = "BASELINE"
            prior_regime = "CALM"
            prior_loaded = False

    streak = int(coach_signals.get("consecutiveApplyWindows", 0) or 0)
    action = str(coach_signals.get("guardAction", "HOLD") or "HOLD").upper()
    regime = str(guard_signals.get("volatilityRegime", "CALM") or "CALM").upper()
    regime_changed = prior_loaded and regime != prior_regime

    if action != "APPLY":
        pack = "BASELINE"
        reason = "guard-not-applied"
    elif streak >= 4 or (regime == "SPIKE" and streak >= 2):
        pack = "ANCHOR"
        reason = "sustained-apply-streak-or-spike-pressure"
    elif streak >= 2 or regime_changed:
        pack = "ADAPTIVE"
        reason = "apply-streak-building-or-regime-transition"
    else:
        pack = "BASELINE"
        reason = "fresh-apply-window"

    token = f"LPRCG COACH PACK:{pack}"
    return token, {
        "pack": pack,
        "priorPack": prior_pack,
        "guardAction": action,
        "consecutiveApplyWindows": streak,
        "volatilityRegime": regime,
        "priorVolatilityRegime": prior_regime,
        "regimeChanged": regime_changed,
        "priorLoaded": prior_loaded,
        "reason": reason,
        "offlineOnly": True,
    }


def lane_priority_recommendation_confidence_guard_persistence_coach_copy_narrative_line(
    *,
    pack_signals: dict[str, object],
    guard_signals: dict[str, object],
) -> tuple[str, dict[str, object]]:
    """Offline narrative coach-copy line derived from coach-pack + volatility regime transitions."""
    pack = str(pack_signals.get("pack", "BASELINE") or "BASELINE").upper()
    action = str(pack_signals.get("guardAction", "HOLD") or "HOLD").upper()
    regime = str(pack_signals.get("volatilityRegime", "CALM") or "CALM").upper()
    prior_regime = str(pack_signals.get("priorVolatilityRegime", "CALM") or "CALM").upper()
    regime_changed = bool(pack_signals.get("regimeChanged", False))
    consecutive = int(pack_signals.get("consecutiveApplyWindows", 0) or 0)
    divergence_streak = int(guard_signals.get("divergenceStreak", 0) or 0)

    if action != "APPLY":
        line = "RESET BASELINE HOLD"
        reason = "guard-hold"
    elif pack == "ANCHOR" and regime == "SPIKE":
        line = "ANCHOR CORE DURING SPIKE"
        reason = "anchor-pack-with-spike-regime"
    elif pack == "ANCHOR":
        line = "ANCHOR CORE KEEP RHYTHM"
        reason = "anchor-pack"
    elif pack == "ADAPTIVE" and regime_changed:
        line = f"ADAPT TO {regime} REGIME"
        reason = "adaptive-pack-with-regime-transition"
    elif pack == "ADAPTIVE":
        line = "ADAPTIVE WATCH KEEP FLEX"
        reason = "adaptive-pack-stable-regime"
    else:
        line = "BASELINE WATCH NEXT WINDOW"
        reason = "baseline-pack"

    token = f"LPRCG COACH COPY:{line}"
    return token, {
        "pack": pack,
        "guardAction": action,
        "volatilityRegime": regime,
        "priorVolatilityRegime": prior_regime,
        "regimeChanged": regime_changed,
        "consecutiveApplyWindows": consecutive,
        "divergenceStreak": divergence_streak,
        "reason": reason,
        "offlineOnly": True,
    }




def lane_priority_recommendation_confidence_guard_persistence_coach_copy_why_token(
    *,
    coach_copy_signals: dict[str, object],
) -> tuple[str, dict[str, object]]:
    """Flag-gated rationale shorthand for coach-copy narrative context (`LPRCG COACH COPY WHY:<short>`)."""
    flag_name = "DOTPIO_EXPERIMENT_LANE_PRIORITY_REC_CONF_GUARD_COACH_COPY_WHY"
    flag_enabled = os.environ.get(flag_name, "").strip().lower() in {"1", "true", "yes", "on"}

    reason = str(coach_copy_signals.get("reason", "baseline-pack") or "baseline-pack").strip().lower()
    mapping = {
        "guard-hold": "HOLD RESET",
        "anchor-pack-with-spike-regime": "SPIKE ANCHOR",
        "anchor-pack": "ANCHOR RHYTHM",
        "adaptive-pack-with-regime-transition": "REGIME SHIFT",
        "adaptive-pack-stable-regime": "FLEX WATCH",
        "baseline-pack": "BASELINE WATCH",
    }
    short = mapping.get(reason, "BASELINE WATCH")
    token = f"LPRCG COACH COPY WHY:{short}"
    return (token if flag_enabled else "FLAG OFF"), {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "reason": reason,
        "short": short,
        "offlineOnly": True,
    }


def resolve_lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_alias(
    *,
    pack_token: str,
) -> tuple[str, dict[str, object]]:
    """Compact alias for guard-persistence coach-pack token (`LPRCGCP:<B|A|N>`)."""
    flag_name = "DOTPIO_EXPERIMENT_LANE_PRIORITY_REC_CONF_GUARD_COACH_PACK_ALIAS"
    flag_enabled = os.environ.get(flag_name, "").strip().lower() in {"1", "true", "yes", "on"}

    alias_map = {
        "LPRCG COACH PACK:BASELINE": "B",
        "LPRCG COACH PACK:ADAPTIVE": "A",
        "LPRCG COACH PACK:ANCHOR": "N",
    }
    alias = alias_map.get(pack_token, "B")
    token = f"LPRCGCP:{alias}"
    return (token if flag_enabled else "FLAG OFF"), {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "packToken": pack_token,
        "alias": alias,
    }


def resolve_lane_priority_recommendation_confidence_guard_persistence_coach_copy_alias(
    *,
    coach_copy_token: str,
) -> tuple[str, dict[str, object]]:
    """Compact alias for guard-persistence coach-copy narrative (`LPRCGCN:<R|B|A|N>`)."""
    flag_name = "DOTPIO_EXPERIMENT_LANE_PRIORITY_REC_CONF_GUARD_COACH_COPY_ALIAS"
    flag_enabled = os.environ.get(flag_name, "").strip().lower() in {"1", "true", "yes", "on"}

    alias = "B"
    if "RESET BASELINE HOLD" in coach_copy_token:
        alias = "R"
    elif "ANCHOR CORE" in coach_copy_token:
        alias = "N"
    elif "ADAPT" in coach_copy_token:
        alias = "A"

    token = f"LPRCGCN:{alias}"
    return (token if flag_enabled else "FLAG OFF"), {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "coachCopyToken": coach_copy_token,
        "alias": alias,
    }


def resolve_lane_priority_recommendation_confidence_guard_persistence_coach_alias(
    *,
    coach_token: str,
) -> tuple[str, dict[str, object]]:
    """Compact alias for guard-persistence coaching cue (`LPRCGC:<R|W|S>`)."""
    flag_name = "DOTPIO_EXPERIMENT_LANE_PRIORITY_REC_CONF_GUARD_COACH_ALIAS"
    flag_enabled = os.environ.get(flag_name, "").strip().lower() in {"1", "true", "yes", "on"}

    alias_map = {
        "LPRCG COACH:RESET": "R",
        "LPRCG COACH:WATCH": "W",
        "LPRCG COACH:STABILIZE": "S",
    }
    alias = alias_map.get(coach_token, "W")
    token = f"LPRCGC:{alias}"
    return (token if flag_enabled else "FLAG OFF"), {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "coachToken": coach_token,
        "alias": alias,
    }


def pulse_heat_fx_compact_budget_drift(
    *,
    pulse_heat_fx_family: dict[str, object],
    compact_net: int,
) -> tuple[str, dict[str, object]]:
    churn = int(pulse_heat_fx_family.get("churn", 0) or 0)
    net = int(pulse_heat_fx_family.get("net", 0) or 0)
    compact_pressure = abs(compact_net)

    if churn == 0:
        level = "STABLE"
        reason = "no pulse-heat-fx churn in window"
    elif abs(net) >= 3 or (churn >= 6 and compact_pressure >= 8):
        level = "SPIKE"
        reason = "pulse-heat-fx churn is likely competing with compact prompt budget"
    elif abs(net) >= 1 or churn >= 3:
        level = "WATCH"
        reason = "pulse-heat-fx churn is noticeable in compact prompt budget"
    else:
        level = "STABLE"
        reason = "pulse-heat-fx churn remains minor in compact prompt budget"

    return level, {
        "reason": reason,
        "compactNet": compact_net,
        "familyNet": net,
        "familyChurn": churn,
        "absFamilyNet": abs(net),
        "absCompactNet": compact_pressure,
    }


def route_glow_fx_compact_budget_drift(
    *,
    route_glow_fx_family: dict[str, object],
    compact_net: int,
) -> tuple[str, dict[str, object]]:
    churn = int(route_glow_fx_family.get("churn", 0) or 0)
    net = int(route_glow_fx_family.get("net", 0) or 0)
    compact_pressure = abs(compact_net)

    if churn == 0:
        level = "STABLE"
        reason = "no route-glow-fx churn in window"
    elif abs(net) >= 3 or (churn >= 6 and compact_pressure >= 8):
        level = "SPIKE"
        reason = "route-glow-fx churn is likely competing with compact prompt budget"
    elif abs(net) >= 1 or churn >= 3:
        level = "WATCH"
        reason = "route-glow-fx churn is noticeable in compact prompt budget"
    else:
        level = "STABLE"
        reason = "route-glow-fx churn remains minor in compact prompt budget"

    return level, {
        "reason": reason,
        "compactNet": compact_net,
        "familyNet": net,
        "familyChurn": churn,
        "absFamilyNet": abs(net),
        "absCompactNet": compact_pressure,
    }


def route_glow_fx_conf_why_rail_mode_compact_budget_drift(
    *,
    route_glow_fx_conf_why_rail_mode_family: dict[str, object],
    compact_net: int,
) -> tuple[str, dict[str, object]]:
    churn = int(route_glow_fx_conf_why_rail_mode_family.get("churn", 0) or 0)
    net = int(route_glow_fx_conf_why_rail_mode_family.get("net", 0) or 0)
    compact_pressure = abs(compact_net)

    if churn == 0:
        level = "STABLE"
        reason = "no route-glow rationale rail-mode churn in window"
    elif abs(net) >= 3 or (churn >= 4 and compact_pressure >= 8):
        level = "SPIKE"
        reason = "rail-mode churn is likely competing with compact prompt budget"
    elif abs(net) >= 1 or churn >= 2:
        level = "WATCH"
        reason = "rail-mode churn is noticeable in compact prompt budget"
    else:
        level = "STABLE"
        reason = "rail-mode churn remains minor in compact prompt budget"

    return level, {
        "reason": reason,
        "compactNet": compact_net,
        "familyNet": net,
        "familyChurn": churn,
        "absFamilyNet": abs(net),
        "absCompactNet": compact_pressure,
    }


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



def alt_step_confidence_drift_from_prior(
    *,
    current_alt_step_confidence: str,
    prior_json_path: Path,
) -> tuple[int, dict[str, str | int | bool]]:
    """Compare current/prior fallback micro-cue confidence and emit signed drift delta."""
    confidence_scores = {"LOW": 0, "MID": 1, "HIGH": 2}

    current_confidence = str(current_alt_step_confidence).upper()
    current_score = confidence_scores.get(current_confidence, 0)
    prior_confidence = "LOW"
    prior_score = confidence_scores[prior_confidence]
    prior_loaded = False

    if prior_json_path.is_file():
        try:
            prior = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_confidence = str(prior.get("altStepConfidence", prior_confidence)).upper()
            prior_score = confidence_scores.get(prior_confidence, 0)
            prior_loaded = True
        except (json.JSONDecodeError, OSError, ValueError):
            prior_loaded = False

    drift = current_score - prior_score

    if not prior_loaded:
        drift = 0
        reason = "no-prior-alt-step-confidence"
    elif drift > 0:
        reason = "alt-step-confidence-increased"
    elif drift < 0:
        reason = "alt-step-confidence-decreased"
    else:
        reason = "alt-step-confidence-stable"

    return drift, {
        "currentAltStepConfidence": current_confidence,
        "currentScore": current_score,
        "priorAltStepConfidence": prior_confidence,
        "priorScore": prior_score,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def alt_step_why_confidence_drift_from_prior(
    *,
    action_pace_alt_window_why: str,
    action_pace_alt_window_confidence: str,
    action_pace_alt_window_fit: str,
    prior_json_path: Path,
) -> tuple[int, dict[str, str | int | bool]]:
    """Compare current/prior fallback-rationale confidence and emit signed drift delta."""
    confidence_scores = {"LOW": 0, "MID": 1, "HIGH": 2}

    why = str(action_pace_alt_window_why).upper()
    base_conf = str(action_pace_alt_window_confidence).upper()
    fit = str(action_pace_alt_window_fit).upper()

    if why in {"FLAG OFF", "ALT FLAG OFF", "PICK ALT LANE", "ARM SANDBOX"}:
        current_confidence = "LOW"
    elif why in {"PROBE NOW", "PRIMARY HOLD"} and base_conf == "HIGH":
        current_confidence = "HIGH"
    elif fit == "SAFE" and base_conf in {"MID", "HIGH"}:
        current_confidence = "HIGH"
    elif fit == "TENSE" and base_conf == "LOW":
        current_confidence = "LOW"
    else:
        current_confidence = "MID" if base_conf in {"MID", "HIGH"} else "LOW"

    current_score = confidence_scores.get(current_confidence, 0)
    prior_confidence = "LOW"
    prior_score = confidence_scores[prior_confidence]
    prior_loaded = False

    if prior_json_path.is_file():
        try:
            prior = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_confidence = str(prior.get("altStepWhyConfidenceDriftSignals", {}).get("currentAltStepWhyConfidence", prior_confidence)).upper()
            prior_score = confidence_scores.get(prior_confidence, 0)
            prior_loaded = True
        except (json.JSONDecodeError, OSError, ValueError, AttributeError, TypeError):
            prior_loaded = False

    drift = current_score - prior_score

    if not prior_loaded:
        drift = 0
        reason = "no-prior-alt-step-why-confidence"
    elif drift > 0:
        reason = "alt-step-why-confidence-increased"
    elif drift < 0:
        reason = "alt-step-why-confidence-decreased"
    else:
        reason = "alt-step-why-confidence-stable"

    return drift, {
        "currentAltStepWhy": why,
        "currentAltStepWhyConfidence": current_confidence,
        "currentScore": current_score,
        "priorAltStepWhyConfidence": prior_confidence,
        "priorScore": prior_score,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def alt_why_glyph_drift_from_prior(
    *,
    current_alt_why_glyph_net: int,
    prior_json_path: Path,
) -> tuple[int, dict[str, int | bool | str]]:
    """Compare current/prior ALT WHY GLYPH net activity and emit signed drift delta."""
    current_net = int(current_alt_why_glyph_net)
    prior_net = 0
    prior_loaded = False

    if prior_json_path.is_file():
        try:
            prior = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_net = int(prior.get("altWhyGlyphDriftSignals", {}).get("currentAltWhyGlyphNet", prior_net))
            prior_loaded = True
        except (json.JSONDecodeError, OSError, ValueError, TypeError, AttributeError):
            prior_loaded = False

    drift = current_net - prior_net

    if not prior_loaded:
        drift = 0
        reason = "no-prior-alt-why-glyph-net"
    elif drift > 0:
        reason = "alt-why-glyph-net-increased"
    elif drift < 0:
        reason = "alt-why-glyph-net-decreased"
    else:
        reason = "alt-why-glyph-net-stable"

    return drift, {
        "currentAltWhyGlyphNet": current_net,
        "priorAltWhyGlyphNet": prior_net,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def alt_why_glyph_mode_drift_from_prior(
    *,
    current_alt_why_glyph_mode_net: int,
    prior_json_path: Path,
) -> tuple[int, dict[str, int | bool | str]]:
    """Compare current/prior ALT WHY GLYPH MODE net activity and emit signed drift delta."""
    current_net = int(current_alt_why_glyph_mode_net)
    prior_net = 0
    prior_loaded = False

    if prior_json_path.is_file():
        try:
            prior = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_net = int(prior.get("altWhyGlyphModeDriftSignals", {}).get("currentAltWhyGlyphModeNet", prior_net))
            prior_loaded = True
        except (json.JSONDecodeError, OSError, ValueError, TypeError, AttributeError):
            prior_loaded = False

    drift = current_net - prior_net

    if not prior_loaded:
        drift = 0
        reason = "no-prior-alt-why-glyph-mode-net"
    elif drift > 0:
        reason = "alt-why-glyph-mode-net-increased"
    elif drift < 0:
        reason = "alt-why-glyph-mode-net-decreased"
    else:
        reason = "alt-why-glyph-mode-net-stable"

    return drift, {
        "currentAltWhyGlyphModeNet": current_net,
        "priorAltWhyGlyphModeNet": prior_net,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def alt_why_glyph_mode_confidence_from_signals(
    *,
    alt_why_glyph_mode_drift: int,
    alt_why_glyph_mode_drift_signals: dict[str, int | bool | str],
) -> tuple[str, dict[str, int | bool | str]]:
    """Confidence band for ALT WHY GLYPH MODE drift readability token."""
    drift = int(alt_why_glyph_mode_drift)
    current_net = abs(int(alt_why_glyph_mode_drift_signals.get("currentAltWhyGlyphModeNet", 0)))
    prior_loaded = bool(alt_why_glyph_mode_drift_signals.get("priorLoaded", False))
    abs_drift = abs(drift)

    if not prior_loaded:
        confidence = "LOW"
        reason = "no-prior-glyph-mode-window"
    elif abs_drift >= 3 and current_net >= 2:
        confidence = "HIGH"
        reason = "strong-drift-with-persistent-glyph-mode-net"
    elif abs_drift >= 1 or current_net >= 1:
        confidence = "MID"
        reason = "moderate-drift-or-nonzero-glyph-mode-net"
    else:
        confidence = "LOW"
        reason = "flat-drift-and-net"

    return confidence, {
        "altWhyGlyphModeDrift": drift,
        "absAltWhyGlyphModeDrift": abs_drift,
        "currentAltWhyGlyphModeNet": int(alt_why_glyph_mode_drift_signals.get("currentAltWhyGlyphModeNet", 0)),
        "priorAltWhyGlyphModeNet": int(alt_why_glyph_mode_drift_signals.get("priorAltWhyGlyphModeNet", 0)),
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def alt_why_glyph_mode_confidence_drift_from_prior(
    *,
    current_alt_why_glyph_mode_confidence: str,
    prior_json_path: Path,
) -> tuple[int, dict[str, str | int | bool]]:
    """Compare current/prior ALT WHY GLYPH MODE confidence and emit signed drift delta."""
    confidence_scores = {"LOW": 0, "MID": 1, "HIGH": 2}

    current_confidence = str(current_alt_why_glyph_mode_confidence).upper()
    current_score = confidence_scores.get(current_confidence, 0)
    prior_confidence = "LOW"
    prior_score = confidence_scores[prior_confidence]
    prior_loaded = False

    if prior_json_path.is_file():
        try:
            prior = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_confidence = str(prior.get("altWhyGlyphModeConfidence", prior_confidence)).upper()
            prior_score = confidence_scores.get(prior_confidence, 0)
            prior_loaded = True
        except (json.JSONDecodeError, OSError, ValueError, TypeError, AttributeError):
            prior_loaded = False

    drift = current_score - prior_score

    if not prior_loaded:
        drift = 0
        reason = "no-prior-alt-why-glyph-mode-confidence"
    elif drift > 0:
        reason = "alt-why-glyph-mode-confidence-increased"
    elif drift < 0:
        reason = "alt-why-glyph-mode-confidence-decreased"
    else:
        reason = "alt-why-glyph-mode-confidence-stable"

    return drift, {
        "currentAltWhyGlyphModeConfidence": current_confidence,
        "currentScore": current_score,
        "priorAltWhyGlyphModeConfidence": prior_confidence,
        "priorScore": prior_score,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def alt_why_glyph_mode_confidence_why_from_signals(
    *,
    alt_why_glyph_mode_confidence: str,
    alt_why_glyph_mode_confidence_drift: int,
    alt_why_glyph_mode_confidence_signals: dict[str, int | bool | str],
) -> tuple[str, dict[str, int | bool | str]]:
    """Prototype compact rationale token for ALT WHY GLYPH MODE confidence band."""
    flag_name = "DOTPIO_EXPERIMENT_ALT_WHY_GLYPH_MODE_CONF_WHY"
    flag_value = os.environ.get(flag_name, "")
    flag_enabled = flag_value.strip().lower() in {"1", "true", "yes", "on"}

    confidence = str(alt_why_glyph_mode_confidence).upper()
    drift = int(alt_why_glyph_mode_confidence_drift)
    net = int(alt_why_glyph_mode_confidence_signals.get("currentAltWhyGlyphModeNet", 0))
    abs_drift = int(alt_why_glyph_mode_confidence_signals.get("absAltWhyGlyphModeDrift", abs(drift)))
    prior_loaded = bool(alt_why_glyph_mode_confidence_signals.get("priorLoaded", False))

    if not flag_enabled:
        why = "FLAG OFF"
        reason = "flag-disabled"
    elif not prior_loaded:
        why = "SEED BASE"
        reason = "no-prior-window"
    elif confidence == "HIGH" and drift > 0:
        why = "SPIKE VERIFY"
        reason = "high-confidence-rising-drift"
    elif confidence == "HIGH":
        why = "HOLD SPIKE"
        reason = "high-confidence-stable-or-cooling"
    elif confidence == "MID" and abs_drift >= 2:
        why = "TREND WATCH"
        reason = "mid-confidence-strong-drift"
    elif confidence == "MID":
        why = "WATCH MODE"
        reason = "mid-confidence-default"
    elif abs_drift == 0 and net == 0:
        why = "LOW SIGNAL"
        reason = "flat-drift-and-net"
    else:
        why = "QUIET WATCH"
        reason = "low-confidence-with-some-activity"

    return why, {
        "flagName": flag_name,
        "flagEnabled": flag_enabled,
        "altWhyGlyphModeConfidence": confidence,
        "altWhyGlyphModeConfidenceDrift": drift,
        "absAltWhyGlyphModeDrift": abs_drift,
        "currentAltWhyGlyphModeNet": net,
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


def route_pulse_link_mode_fit_drift_from_prior(
    *,
    current_route_pulse_link_mode_fit: str,
    prior_json_path: Path,
) -> tuple[int, dict[str, str | int | bool]]:
    """Track route pulse-link mode fit drift against prior digest window."""
    score_map = {"RESET": 0, "WATCH": 1, "SYNC": 2, "BREAK": 3}
    current_fit = str(current_route_pulse_link_mode_fit).upper()
    current_score = score_map.get(current_fit, 0)

    prior_fit = "WATCH"
    prior_score = score_map[prior_fit]
    prior_loaded = False

    if prior_json_path.is_file():
        try:
            prior = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_fit = str(prior.get("routePulseLinkModeFit", prior_fit)).upper()
            prior_score = score_map.get(prior_fit, 0)
            prior_loaded = True
        except (json.JSONDecodeError, OSError, TypeError, ValueError):
            prior_loaded = False
            prior_fit = "WATCH"
            prior_score = score_map[prior_fit]

    drift = current_score - prior_score
    if drift > 0:
        reason = "fit-intensified"
    elif drift < 0:
        reason = "fit-deescalated"
    elif prior_loaded:
        reason = "fit-stable"
    else:
        reason = "no-prior-fit"

    return drift, {
        "currentFit": current_fit,
        "currentScore": current_score,
        "priorFit": prior_fit,
        "priorScore": prior_score,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def route_pulse_token_priority_from_signals(
    *,
    route_pulse_link_mode_fit_drift: int,
    prior_json_path: Path,
) -> tuple[str, dict[str, str | int | bool]]:
    """Emit compact pulse-token priority mode with drift guard to avoid noisy flips."""
    env_name = "DOTPIO_EXPERIMENT_ROUTE_PULSE_TOKEN_PRIORITY"
    raw_mode = os.environ.get(env_name)
    configured_mode = str(raw_mode or "").upper()
    if configured_mode not in {"FIT-FIRST", "MODE-FIRST"}:
        configured_mode = "OFF"

    prior_mode = "OFF"
    prior_loaded = False
    if prior_json_path.is_file():
        try:
            prior = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_mode = str(prior.get("routePulseTokenPriority", prior_mode)).upper()
            if prior_mode not in {"FIT-FIRST", "MODE-FIRST", "OFF"}:
                prior_mode = "OFF"
            prior_loaded = True
        except (json.JSONDecodeError, OSError, TypeError, ValueError):
            prior_loaded = False

    drift = int(route_pulse_link_mode_fit_drift)
    guard_held = (
        prior_loaded
        and configured_mode in {"FIT-FIRST", "MODE-FIRST"}
        and prior_mode in {"FIT-FIRST", "MODE-FIRST"}
        and configured_mode != prior_mode
        and drift == 0
    )

    if guard_held:
        mode = prior_mode
        reason = "guard-held-prior-mode"
    else:
        mode = configured_mode
        if mode == "OFF":
            reason = "priority-mode-disabled"
        elif prior_loaded and mode != prior_mode:
            reason = "priority-mode-shift-accepted"
        elif prior_loaded:
            reason = "priority-mode-stable"
        else:
            reason = "priority-mode-initialized"

    return mode, {
        "envName": env_name,
        "configuredMode": configured_mode,
        "routePulseLinkModeFitDrift": drift,
        "priorMode": prior_mode,
        "priorLoaded": prior_loaded,
        "guardHeld": guard_held,
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


def rgfxwri_why_conf_policy_recommendation(
    *,
    drift_risk: str,
    family_totals: dict[str, int],
) -> tuple[str, dict[str, object]]:
    churn = int(family_totals.get("churn", 0))
    net = int(family_totals.get("net", 0))
    coverage = str(family_totals.get("coverage", "0/0"))

    if drift_risk == "HIGH" or churn >= 6:
        recommendation = "FREEZE"
        rationale = "high-risk-high-churn"
        guidance = "Prefer MID baseline; require rail/rationale corroboration before HIGH wording."
    elif drift_risk == "MID" or churn >= 3:
        recommendation = "GUARDED"
        rationale = "moderate-drift"
        guidance = "Keep deterministic LOW/MID/HIGH mapping; only emit HIGH on sustained SPIKE/LOCK context."
    else:
        recommendation = "RELAXED"
        rationale = "stable-window"
        guidance = "Maintain current deterministic copy and monitor weekly churn before tightening."

    signals: dict[str, object] = {
        "driftRisk": drift_risk,
        "familyChurn": churn,
        "familyNet": net,
        "familyCoverage": coverage,
        "rationale": rationale,
        "offlineOnly": True,
        "guidance": guidance,
    }
    return recommendation, signals


def ambient_ramp_confidence_recommendation_from_trends(
    *,
    drift_risk: str,
    ambient_ramp_confidence_family: dict[str, int],
    pressure_band: str,
) -> tuple[str, dict[str, object]]:
    """Recommend offline-only ambient-ramp confidence posture from drift + churn trends."""
    churn = int(ambient_ramp_confidence_family.get("churn", 0))
    net = int(ambient_ramp_confidence_family.get("net", 0))
    coverage = str(ambient_ramp_confidence_family.get("coverage", "0/0"))

    if drift_risk == "HIGH" or pressure_band == "HIGH" or churn >= 4:
        recommendation = "PIN_HIGH_CONF"
        rationale = "high-risk-or-high-pressure"
        guidance = "Hold deterministic ARC mapping; treat LOW confidence copy as default until pressure/churn cools."
    elif drift_risk == "MID" or pressure_band == "MID" or churn >= 2:
        recommendation = "GUARD_HIGH_CONF"
        rationale = "mixed-risk-window"
        guidance = "Keep HIGH confidence sparse; prefer MID unless CALM/SAFE context is strongly corroborated."
    else:
        recommendation = "ALLOW_BALANCED_CONF"
        rationale = "stable-low-pressure-window"
        guidance = "Maintain current deterministic confidence wording with weekly churn monitoring."

    signals: dict[str, object] = {
        "driftRisk": drift_risk,
        "pressureBand": pressure_band,
        "ambientRampConfidenceChurn": churn,
        "ambientRampConfidenceNet": net,
        "ambientRampConfidenceCoverage": coverage,
        "rationale": rationale,
        "offlineOnly": True,
        "guidance": guidance,
    }
    return recommendation, signals


def ambient_ramp_why_recommendation_from_trends(
    *,
    drift_risk: str,
    ambient_ramp_why_family: dict[str, int],
    pressure_band: str,
) -> tuple[str, dict[str, object]]:
    """Recommend offline-only ambient-rationale copy posture from drift + pressure trends."""
    churn = int(ambient_ramp_why_family.get("churn", 0))
    net = int(ambient_ramp_why_family.get("net", 0))
    coverage = str(ambient_ramp_why_family.get("coverage", "0/0"))

    if drift_risk == "HIGH" or pressure_band == "HIGH" or churn >= 4:
        recommendation = "HOLD_SAFE_WHY"
        rationale = "high-risk-or-high-pressure"
        guidance = "Prefer SAFE LOCK rationale defaults; only emit pressure-forward rationale under sustained corroboration."
    elif drift_risk == "MID" or pressure_band == "MID" or churn >= 2:
        recommendation = "PRESSURE_GATED_WHY"
        rationale = "mixed-risk-window"
        guidance = "Allow PRESSURE HOLD rationale only when pressure band remains MID/HIGH with stable confidence context."
    else:
        recommendation = "OPEN_CONTEXTUAL_WHY"
        rationale = "stable-low-pressure-window"
        guidance = "Keep deterministic SAFE/PRESSURE rationale mapping and monitor churn weekly before tightening."

    signals: dict[str, object] = {
        "driftRisk": drift_risk,
        "pressureBand": pressure_band,
        "ambientRampWhyChurn": churn,
        "ambientRampWhyNet": net,
        "ambientRampWhyCoverage": coverage,
        "rationale": rationale,
        "offlineOnly": True,
        "guidance": guidance,
    }
    return recommendation, signals



def ambient_ramp_why_recommendation_confidence_from_signals(
    *,
    recommendation: str,
    recommendation_signals: dict[str, object],
) -> tuple[str, dict[str, object]]:
    """Confidence tier for offline ambient-rationale recommendation handoff."""
    churn = int(recommendation_signals.get("ambientRampWhyChurn", 0))
    drift_risk = str(recommendation_signals.get("driftRisk", "LOW"))
    pressure_band = str(recommendation_signals.get("pressureBand", "LOW"))

    if recommendation == "OPEN_CONTEXTUAL_WHY" and drift_risk == "LOW" and pressure_band == "LOW" and churn <= 1:
        confidence = "HIGH"
        rationale = "stable-low-pressure-window"
    elif recommendation == "PRESSURE_GATED_WHY" and drift_risk != "HIGH" and churn <= 3:
        confidence = "MID"
        rationale = "mixed-window-controlled-churn"
    elif recommendation == "HOLD_SAFE_WHY" and (drift_risk == "HIGH" or pressure_band == "HIGH"):
        confidence = "MID"
        rationale = "defensive-posture-under-pressure"
    else:
        confidence = "LOW"
        rationale = "volatile-or-ambiguous-window"

    return confidence, {
        "recommendation": recommendation,
        "driftRisk": drift_risk,
        "pressureBand": pressure_band,
        "ambientRampWhyChurn": churn,
        "rationale": rationale,
        "offlineOnly": True,
    }


def ambient_ramp_why_recommendation_confidence_streak_from_prior(
    *,
    current_confidence: str,
    prior_json_path: Path,
) -> tuple[int, dict[str, object]]:
    """Track consecutive windows with unchanged AMBIENT RAMP WHY REC CONF."""
    current = str(current_confidence).strip().upper() or "LOW"
    prior_confidence = current
    prior_streak = 0
    prior_loaded = False

    if prior_json_path.is_file():
        try:
            prior_payload = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_confidence = str(prior_payload.get("ambientRampWhyRecommendationConfidence", current)).strip().upper() or current
            prior_streak = int(prior_payload.get("ambientRampWhyRecommendationConfidenceStreak", 0) or 0)
            prior_loaded = True
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    if prior_loaded and prior_confidence == current:
        streak = max(1, prior_streak) + 1
        reason = "confidence-streak-extended"
    else:
        streak = 1
        reason = "confidence-streak-reset"

    suppress_threshold = 3
    suppress = streak >= suppress_threshold and current in {"LOW", "HIGH"}

    return streak, {
        "currentConfidence": current,
        "priorConfidence": prior_confidence,
        "priorStreak": prior_streak,
        "priorLoaded": prior_loaded,
        "threshold": suppress_threshold,
        "suppress": suppress,
        "reason": reason,
    }


def ambient_ramp_why_recommendation_parity_summary(
    *,
    recommendation: str,
    confidence: str,
    recommendation_signals: dict[str, object],
) -> tuple[str, dict[str, object]]:
    """Compact parity summary for ambient-rationale recommendation lane in token-family digest."""
    churn = int(recommendation_signals.get("ambientRampWhyChurn", 0))
    net = int(recommendation_signals.get("ambientRampWhyNet", 0))
    pressure_band = str(recommendation_signals.get("pressureBand", "LOW"))

    if confidence == "HIGH" and recommendation == "OPEN_CONTEXTUAL_WHY" and churn <= 1:
        summary = "SYNC"
        rationale = "stable-open-context-window"
    elif confidence == "MID" and churn <= 3 and pressure_band != "HIGH":
        summary = "WATCH"
        rationale = "moderate-churn-mixed-context"
    else:
        summary = "LOCK"
        rationale = "high-pressure-or-volatile-window"

    signals: dict[str, object] = {
        "recommendation": recommendation,
        "confidence": confidence,
        "ambientRampWhyChurn": churn,
        "ambientRampWhyNet": net,
        "pressureBand": pressure_band,
        "rationale": rationale,
    }
    return summary, signals


def ambient_ramp_why_auto_remap_plan_from_signals(
    *,
    recommendation: str,
    confidence: str,
    parity: str,
    recommendation_signals: dict[str, object],
    confidence_streak: int = 1,
    suppress_candidates: bool = False,
) -> tuple[str, dict[str, object], list[dict[str, object]]]:
    """Build offline-only ambient rationale auto-remap plan candidates for sandbox review."""
    drift_risk = str(recommendation_signals.get("driftRisk", "LOW"))
    pressure_band = str(recommendation_signals.get("pressureBand", "LOW"))
    churn = int(recommendation_signals.get("ambientRampWhyChurn", 0))
    net = int(recommendation_signals.get("ambientRampWhyNet", 0))

    candidates = [
        {
            "baseRank": 1,
            "plan": "HOLD_SAFE_BASELINE",
            "summary": "Keep ambient rationale on SAFE-first deterministic wording with no runtime remap coupling.",
            "when": "Use by default in HIGH drift, HIGH pressure, or parity LOCK windows.",
            "risk": "LOW",
            "offlineOnly": True,
            "changeScope": "digest + sandbox notes only",
        },
        {
            "baseRank": 2,
            "plan": "SHADOW_PRESSURE_REMIX",
            "summary": "Draft offline pressure-gated rationale remap table for manual review before any runtime use.",
            "when": "Use in MID risk windows when recommendation is PRESSURE_GATED_WHY and confidence is not LOW.",
            "risk": "MID",
            "offlineOnly": True,
            "changeScope": "sandbox artifact + playtest checklist",
        },
        {
            "baseRank": 3,
            "plan": "LIMITED_CONTEXT_EXPANSION",
            "summary": "Prepare small contextual rationale variants for CALM windows with rollback checklist.",
            "when": "Use only in LOW drift + LOW pressure windows with HIGH confidence and SYNC parity.",
            "risk": "MID",
            "offlineOnly": True,
            "changeScope": "sandbox draft variants (no runtime wiring)",
        },
    ]

    plan_by_recommendation = {
        "HOLD_SAFE_WHY": "HOLD_SAFE_BASELINE",
        "PRESSURE_GATED_WHY": "SHADOW_PRESSURE_REMIX",
        "OPEN_CONTEXTUAL_WHY": "LIMITED_CONTEXT_EXPANSION",
    }

    recommendation_rank = {
        "HOLD_SAFE_BASELINE": 3 if recommendation == "HOLD_SAFE_WHY" else 1,
        "SHADOW_PRESSURE_REMIX": 3 if recommendation == "PRESSURE_GATED_WHY" else 1,
        "LIMITED_CONTEXT_EXPANSION": 3 if recommendation == "OPEN_CONTEXTUAL_WHY" else 1,
    }
    confidence_bias = {
        "HOLD_SAFE_BASELINE": 2 if confidence == "LOW" else 0,
        "SHADOW_PRESSURE_REMIX": 1 if confidence == "MID" else 0,
        "LIMITED_CONTEXT_EXPANSION": 2 if confidence == "HIGH" else -1,
    }
    parity_bias = {
        "HOLD_SAFE_BASELINE": 2 if parity == "LOCK" else 0,
        "SHADOW_PRESSURE_REMIX": 1 if parity == "WATCH" else 0,
        "LIMITED_CONTEXT_EXPANSION": 1 if parity == "SYNC" else -1,
    }
    drift_bias = {
        "HOLD_SAFE_BASELINE": 2 if drift_risk == "HIGH" else 0,
        "SHADOW_PRESSURE_REMIX": 1 if drift_risk == "MID" else 0,
        "LIMITED_CONTEXT_EXPANSION": 1 if drift_risk == "LOW" else -1,
    }
    pressure_bias = {
        "HOLD_SAFE_BASELINE": 2 if pressure_band == "HIGH" else 0,
        "SHADOW_PRESSURE_REMIX": 1 if pressure_band == "MID" else 0,
        "LIMITED_CONTEXT_EXPANSION": 1 if pressure_band == "LOW" else -1,
    }
    churn_bias = {
        "HOLD_SAFE_BASELINE": 1 if churn >= 4 else 0,
        "SHADOW_PRESSURE_REMIX": 1 if 2 <= churn <= 5 else 0,
        "LIMITED_CONTEXT_EXPANSION": 1 if churn <= 2 and net >= 0 else -1,
    }

    for candidate in candidates:
        plan = str(candidate["plan"])
        score = (
            recommendation_rank.get(plan, 0)
            + confidence_bias.get(plan, 0)
            + parity_bias.get(plan, 0)
            + drift_bias.get(plan, 0)
            + pressure_bias.get(plan, 0)
            + churn_bias.get(plan, 0)
        )
        candidate["score"] = score

    candidates.sort(key=lambda c: (int(c.get("score", 0)), -int(c.get("baseRank", 99))), reverse=True)
    for i, candidate in enumerate(candidates, start=1):
        candidate["rank"] = i

    if suppress_candidates:
        candidates = [candidate for candidate in candidates if str(candidate.get("plan", "")) == "HOLD_SAFE_BASELINE"]
        if not candidates:
            candidates = [{
                "baseRank": 1,
                "plan": "HOLD_SAFE_BASELINE",
                "summary": "Keep ambient rationale on SAFE-first deterministic wording with no runtime remap coupling.",
                "when": "Confidence streak suppression active.",
                "risk": "LOW",
                "offlineOnly": True,
                "changeScope": "digest + sandbox notes only",
                "score": 0,
                "rank": 1,
            }]

    selected_plan = str(candidates[0]["plan"]) if candidates else plan_by_recommendation.get(recommendation, "HOLD_SAFE_BASELINE")
    if confidence == "LOW" or parity == "LOCK" or suppress_candidates:
        selected_plan = "HOLD_SAFE_BASELINE"

    rationale = "drift-aware-candidate-rerank"
    if suppress_candidates:
        rationale = "confidence-streak-suppression"
    elif selected_plan == "HOLD_SAFE_BASELINE" and (confidence == "LOW" or parity == "LOCK"):
        rationale = "safety-lock-from-confidence-or-parity"

    signals: dict[str, object] = {
        "recommendation": recommendation,
        "confidence": confidence,
        "parity": parity,
        "driftRisk": drift_risk,
        "pressureBand": pressure_band,
        "ambientRampWhyChurn": churn,
        "ambientRampWhyNet": net,
        "offlineOnly": True,
        "rationale": rationale,
        "nextAction": "Generate sandbox table + review notes; keep runtime contract unchanged.",
        "rerankPolicy": "drift-aware-offline-candidate-priority",
        "candidateCount": len(candidates),
        "confidenceStreak": int(confidence_streak),
        "candidateSuppressed": bool(suppress_candidates),
    }
    return selected_plan, signals, candidates


def ambient_ramp_why_auto_remap_plan_alias(plan: str) -> str:
    alias_map = {
        "HOLD_SAFE_BASELINE": "HOLD",
        "SHADOW_PRESSURE_REMIX": "SHADOW",
        "LIMITED_CONTEXT_EXPANSION": "OPEN",
    }
    return alias_map.get(plan, "HOLD")


def ambient_ramp_auto_remap_confidence_band_alias(confidence: str) -> str:
    alias_map = {"LOW": "L", "MID": "M", "HIGH": "H"}
    return alias_map.get(str(confidence).strip().upper(), "L")


def ambient_ramp_auto_remap_confidence_momentum_alias(recommendation: str) -> str:
    alias_map = {"FREEZE": "F", "WATCH": "W", "ALLOW": "A"}
    return alias_map.get(str(recommendation).strip().upper(), "W")


def ambient_ramp_auto_remap_momentum_arc(
    *,
    recommendation: str,
    pressure_band: str,
    drift_risk: str,
    momentum_score: int,
) -> tuple[str, dict[str, object]]:
    """Compact ambient momentum arc token for digest summary triage."""
    rec = str(recommendation).strip().upper() or "WATCH"
    pressure = str(pressure_band).strip().upper() or "LOW"
    drift = str(drift_risk).strip().upper() or "LOW"
    score = int(momentum_score)

    if rec == "FREEZE" or pressure == "HIGH" or drift == "HIGH" or score >= 70:
        arc = "TENSE"
        reason = "freeze-or-high-risk-pressure"
    else:
        arc = "CALM"
        reason = "stable-momentum-window"

    return arc, {
        "recommendation": rec,
        "pressureBand": pressure,
        "driftRisk": drift,
        "momentumScore": score,
        "reason": reason,
    }


def ambient_ramp_auto_remap_momentum_arc_pulse_alias(momentum_arc: str) -> tuple[str, dict[str, str]]:
    """Compact pulse alias for ARW momentum arc readability in digest summary."""
    arc = str(momentum_arc).strip().upper() or "CALM"
    alias_map = {
        "CALM": "SOFT",
        "TENSE": "HOT",
    }
    pulse = alias_map.get(arc, "LIVE")
    reason = "arc-mapped-to-pulse-tier" if arc in alias_map else "fallback-live-tier"
    return pulse, {"momentumArc": arc, "reason": reason}


def ambient_ramp_auto_remap_confidence_momentum_freeze_recommendation(
    *,
    current_confidence: str,
    confidence_drift: int,
    confidence_streak: int,
    plan_drift: int,
    plan_signals: dict[str, object],
) -> tuple[str, dict[str, object]]:
    """Offline-only recommendation to freeze remap when confidence momentum oscillates."""
    parity = str(plan_signals.get("parity", "LOCK")).upper()
    drift_risk = str(plan_signals.get("driftRisk", "LOW")).upper()
    suppress = bool(plan_signals.get("candidateSuppressed", False))
    oscillating = confidence_drift != 0 and confidence_streak <= 1
    elevated = abs(plan_drift) >= 1 or drift_risk == "HIGH"

    if parity == "LOCK" or suppress:
        recommendation = "FREEZE"
        reason = "lock-or-candidate-suppressed"
    elif oscillating and elevated:
        recommendation = "FREEZE"
        reason = "oscillating-confidence-with-drift"
    elif oscillating:
        recommendation = "WATCH"
        reason = "oscillating-confidence-low-drift"
    else:
        recommendation = "ALLOW"
        reason = "stable-confidence-momentum"

    return recommendation, {
        "currentConfidence": str(current_confidence).upper(),
        "confidenceDrift": int(confidence_drift),
        "confidenceStreak": int(confidence_streak),
        "planDrift": int(plan_drift),
        "parity": parity,
        "driftRisk": drift_risk,
        "candidateSuppressed": suppress,
        "oscillating": oscillating,
        "offlineOnly": True,
        "reason": reason,
    }


def ambient_ramp_auto_remap_confidence_momentum_score(
    *,
    recommendation: str,
    confidence_drift: int,
    confidence_streak: int,
    plan_drift: int,
    plan_signals: dict[str, object],
) -> tuple[int, dict[str, object]]:
    """Offline dampening score (0-100) from confidence oscillation and drift pressure."""
    drift_risk = str(plan_signals.get("driftRisk", "LOW")).upper()
    parity = str(plan_signals.get("parity", "LOCK")).upper()
    candidate_suppressed = bool(plan_signals.get("candidateSuppressed", False))

    base_by_recommendation = {"FREEZE": 85, "WATCH": 60, "ALLOW": 35}
    base = base_by_recommendation.get(str(recommendation).upper(), 50)

    score = base
    score += min(abs(int(confidence_drift)) * 8, 24)
    score += min(abs(int(plan_drift)) * 6, 18)
    if int(confidence_streak) <= 1:
        score += 8
    elif int(confidence_streak) >= 4:
        score -= 8

    if drift_risk == "HIGH":
        score += 10
    elif drift_risk == "MID":
        score += 5

    if parity == "LOCK":
        score += 6
    if candidate_suppressed:
        score += 6

    score = max(0, min(100, score))
    return score, {
        "recommendation": str(recommendation).upper(),
        "base": base,
        "confidenceDrift": int(confidence_drift),
        "confidenceStreak": int(confidence_streak),
        "planDrift": int(plan_drift),
        "driftRisk": drift_risk,
        "parity": parity,
        "candidateSuppressed": candidate_suppressed,
    }


def ambient_ramp_why_auto_remap_rationale_short(*, selected_plan: str, plan_signals: dict[str, object]) -> str:
    """Compact shorthand for offline ambient auto-remap rationale handoff."""
    rationale = str(plan_signals.get("rationale", "")).strip().lower()
    recommendation = str(plan_signals.get("recommendation", "")).strip().upper()
    parity = str(plan_signals.get("parity", "")).strip().upper()

    if "safety-lock" in rationale or parity == "LOCK":
        return "SAFE_LOCK"
    if selected_plan == "SHADOW_PRESSURE_REMIX" or recommendation == "PRESSURE_GATED_WHY":
        return "PRESSURE_HOLD"
    if selected_plan == "LIMITED_CONTEXT_EXPANSION" or recommendation == "OPEN_CONTEXTUAL_WHY":
        return "OPEN_WINDOW"
    return "SAFE_LOCK"


def ambient_ramp_why_auto_remap_plan_drift_from_prior(
    *,
    current_plan: str,
    prior_json_path: Path,
) -> tuple[int, dict[str, object]]:
    """Track selected ambient auto-remap plan drift versus prior digest window."""
    plan_scores = {
        "HOLD_SAFE_BASELINE": 0,
        "SHADOW_PRESSURE_REMIX": 1,
        "LIMITED_CONTEXT_EXPANSION": 2,
    }

    current = str(current_plan).strip().upper() or "HOLD_SAFE_BASELINE"
    prior = current
    prior_loaded = False

    if prior_json_path.is_file():
        try:
            prior_payload = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior = str(prior_payload.get("ambientRampWhyAutoRemapPlan", current)).strip().upper() or current
            prior_loaded = True
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    current_score = plan_scores.get(current, 0)
    prior_score = plan_scores.get(prior, current_score)
    drift = current_score - prior_score

    if drift > 0:
        reason = "auto-plan-expanded-vs-prior-window"
    elif drift < 0:
        reason = "auto-plan-tightened-vs-prior-window"
    else:
        reason = "auto-plan-held-vs-prior-window"

    return drift, {
        "currentPlan": current,
        "currentScore": current_score,
        "priorPlan": prior,
        "priorScore": prior_score,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def ambient_ramp_why_auto_remap_plan_confidence_from_signals(
    *,
    selected_plan: str,
    plan_signals: dict[str, object],
    plan_drift: int,
    plan_drift_signals: dict[str, object],
) -> tuple[str, dict[str, object]]:
    """Resolve confidence tier for ambient auto-remap plan selection readability."""
    drift_risk = str(plan_signals.get("driftRisk", "LOW"))
    recommendation_conf = str(plan_signals.get("confidence", "LOW"))
    parity = str(plan_signals.get("parity", "LOCK"))
    pressure_band = str(plan_signals.get("pressureBand", "LOW"))
    prior_loaded = bool(plan_drift_signals.get("priorLoaded", False))

    if parity == "LOCK" or recommendation_conf == "LOW":
        confidence = "HIGH"
        rationale = "safety-locked-plan-selection"
    elif drift_risk == "LOW" and pressure_band == "LOW" and recommendation_conf == "HIGH" and abs(plan_drift) <= 1:
        confidence = "HIGH"
        rationale = "stable-low-pressure-window"
    elif drift_risk == "HIGH" and abs(plan_drift) >= 2 and prior_loaded:
        confidence = "LOW"
        rationale = "high-drift-large-plan-shift"
    else:
        confidence = "MID"
        rationale = "guarded-offline-selection"

    return confidence, {
        "selectedPlan": selected_plan,
        "recommendationConfidence": recommendation_conf,
        "parity": parity,
        "driftRisk": drift_risk,
        "pressureBand": pressure_band,
        "planDrift": int(plan_drift),
        "priorLoaded": prior_loaded,
        "rationale": rationale,
    }


def ambient_ramp_why_auto_remap_plan_confidence_drift_from_prior(
    *,
    current_confidence: str,
    prior_json_path: Path,
) -> tuple[int, dict[str, object]]:
    """Track ARW AUTO PLAN confidence tier drift versus prior digest window."""
    score_map = {
        "LOW": 0,
        "MID": 1,
        "HIGH": 2,
    }

    current = str(current_confidence).strip().upper() or "LOW"
    prior = current
    prior_loaded = False

    if prior_json_path.is_file():
        try:
            prior_payload = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior = str(prior_payload.get("ambientRampWhyAutoRemapPlanConfidence", current)).strip().upper() or current
            prior_loaded = True
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    current_score = score_map.get(current, 0)
    prior_score = score_map.get(prior, current_score)
    drift = current_score - prior_score

    if drift > 0:
        reason = "auto-plan-confidence-increased-vs-prior-window"
    elif drift < 0:
        reason = "auto-plan-confidence-decreased-vs-prior-window"
    else:
        reason = "auto-plan-confidence-held-vs-prior-window"

    return drift, {
        "currentConfidence": current,
        "currentScore": current_score,
        "priorConfidence": prior,
        "priorScore": prior_score,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def urgency_stack_pruning_order_recommendation_from_trends(
    *,
    drift_risk: str,
    parity_compact_family: dict[str, int],
    urgency_fx_family: dict[str, int],
    urgency_detailed_family: dict[str, int],
) -> tuple[str, dict[str, object]]:
    """Recommend offline urgency-stack pruning order from weekly churn trends."""
    parity_churn = int(parity_compact_family.get("churn", 0))
    fx_churn = int(urgency_fx_family.get("churn", 0))
    detailed_churn = int(urgency_detailed_family.get("churn", 0))

    parity_net = int(parity_compact_family.get("net", 0))
    fx_net = int(urgency_fx_family.get("net", 0))
    detailed_net = int(urgency_detailed_family.get("net", 0))

    if drift_risk == "HIGH" or parity_churn >= 4:
        recommendation = "PARITY>FX>DETAIL"
        rationale = "protect-core-detailed-under-high-drift"
        guidance = "Prune RGFXWRIUP first, then RGFXWRIUFX, keep detailed urgency token longest."
    elif fx_churn > parity_churn and fx_net >= parity_net:
        recommendation = "FX>PARITY>DETAIL"
        rationale = "fx-churn-dominant"
        guidance = "Trim RGFXWRIUFX before RGFXWRIUP when FX churn dominates this window."
    else:
        recommendation = "PARITY>FX>DETAIL"
        rationale = "default-deterministic-order"
        guidance = "Keep deterministic parity-first stack pruning unless drift trends clearly invert."

    signals: dict[str, object] = {
        "driftRisk": drift_risk,
        "parityCompactChurn": parity_churn,
        "urgencyFxChurn": fx_churn,
        "urgencyDetailedChurn": detailed_churn,
        "parityCompactNet": parity_net,
        "urgencyFxNet": fx_net,
        "urgencyDetailedNet": detailed_net,
        "rationale": rationale,
        "offlineOnly": True,
        "guidance": guidance,
    }
    return recommendation, signals


def urgency_stack_rail_recommendation_from_trends(
    *,
    drift_risk: str,
    urgency_stack_rail_family: dict[str, int],
    urgency_stack_tier_family: dict[str, int],
) -> tuple[str, dict[str, object]]:
    """Recommend offline urgency-stack rail posture from weekly churn trends."""
    rail_churn = int(urgency_stack_rail_family.get("churn", 0))
    rail_net = int(urgency_stack_rail_family.get("net", 0))
    rail_coverage = str(urgency_stack_rail_family.get("coverage", "0/0"))

    tier_churn = int(urgency_stack_tier_family.get("churn", 0))
    tier_net = int(urgency_stack_tier_family.get("net", 0))

    if drift_risk == "HIGH" or rail_churn >= 4:
        recommendation = "STEADY-FIRST"
        rationale = "high-risk-or-rail-churn"
        guidance = "Favor STEADY rail under pressure until rail churn cools below alert threshold."
    elif rail_net > tier_net and rail_churn >= 2:
        recommendation = "SPIKE-WHEN-CONFIRMED"
        rationale = "rail-leading-churn-window"
        guidance = "Permit SPIKE rail only with corroborating urgency-stack tier + parity cues."
    else:
        recommendation = "BALANCED"
        rationale = "stable-rail-window"
        guidance = "Keep deterministic STEADY/SPIKE mapping; monitor weekly churn before tightening."

    signals: dict[str, object] = {
        "driftRisk": drift_risk,
        "urgencyStackRailChurn": rail_churn,
        "urgencyStackRailNet": rail_net,
        "urgencyStackRailCoverage": rail_coverage,
        "urgencyStackTierChurn": tier_churn,
        "urgencyStackTierNet": tier_net,
        "rationale": rationale,
        "offlineOnly": True,
        "guidance": guidance,
    }
    return recommendation, signals




def damage_glyph_shape_remap_recommendation_from_trends(
    *,
    drift_risk: str,
    dmg_glyph_family: dict[str, int],
    urgency_stack_rail_family: dict[str, int],
) -> tuple[str, dict[str, object]]:
    """Recommend offline-only glyph-shape remap posture from digest churn trends."""
    glyph_churn = int(dmg_glyph_family.get("churn", 0))
    glyph_net = int(dmg_glyph_family.get("net", 0))
    glyph_coverage = str(dmg_glyph_family.get("coverage", "0/0"))

    rail_churn = int(urgency_stack_rail_family.get("churn", 0))
    rail_net = int(urgency_stack_rail_family.get("net", 0))

    if drift_risk == "HIGH" or glyph_churn >= 4:
        recommendation = "PIN_BANDS"
        rationale = "high-risk-or-glyph-churn"
        guidance = "Hold current BASIC/SPIKE/OVERDRIVE mapping; avoid shape remap changes until churn cools."
    elif rail_churn >= 3 and rail_net > 0:
        recommendation = "RAIL_SYNC"
        rationale = "rail-pressure-sync-window"
        guidance = "Prototype remap candidates that emphasize rail-aligned transitions while preserving deterministic band thresholds."
    else:
        recommendation = "MICRO_TUNE"
        rationale = "stable-glyph-window"
        guidance = "Allow small offline glyph-shape tuning proposals; keep runtime mapping unchanged pending validation."

    signals: dict[str, object] = {
        "driftRisk": drift_risk,
        "dmgGlyphChurn": glyph_churn,
        "dmgGlyphNet": glyph_net,
        "dmgGlyphCoverage": glyph_coverage,
        "urgencyStackRailChurn": rail_churn,
        "urgencyStackRailNet": rail_net,
        "rationale": rationale,
        "offlineOnly": True,
        "guidance": guidance,
    }
    return recommendation, signals


def damage_glyph_fx_remap_recommendation_from_trends(
    *,
    drift_risk: str,
    dmg_glyph_fx_live_family: dict[str, int],
    dmg_glyph_family: dict[str, int],
) -> tuple[str, dict[str, object]]:
    """Recommend offline-only glyph-FX remap posture from drift risk and glyph-family churn."""
    fx_churn = int(dmg_glyph_fx_live_family.get("churn", 0))
    fx_net = int(dmg_glyph_fx_live_family.get("net", 0))
    fx_coverage = str(dmg_glyph_fx_live_family.get("coverage", "0/0"))

    glyph_churn = int(dmg_glyph_family.get("churn", 0))
    glyph_net = int(dmg_glyph_family.get("net", 0))

    if drift_risk == "HIGH" or fx_churn >= 4:
        recommendation = "HOLD_FX"
        rationale = "high-risk-or-fx-churn"
        guidance = "Keep CALM/SPARK/BLAZE mapping pinned; collect one more stable digest window before proposing FX remap."
    elif glyph_churn >= 3 and glyph_net > 0:
        recommendation = "SYNC_WITH_GLYPH"
        rationale = "glyph-churn-sync-window"
        guidance = "Draft offline FX remap candidates that track glyph-band momentum without changing runtime defaults."
    else:
        recommendation = "MICRO_TUNE_FX"
        rationale = "stable-fx-window"
        guidance = "Allow small offline-only FX remap suggestions; keep live mapping unchanged until validated."

    signals: dict[str, object] = {
        "driftRisk": drift_risk,
        "dmgGlyphFxLiveChurn": fx_churn,
        "dmgGlyphFxLiveNet": fx_net,
        "dmgGlyphFxLiveCoverage": fx_coverage,
        "dmgGlyphChurn": glyph_churn,
        "dmgGlyphNet": glyph_net,
        "rationale": rationale,
        "offlineOnly": True,
        "guidance": guidance,
    }
    return recommendation, signals


def damage_glyph_fx_remap_confidence_from_signals(
    *,
    drift_risk: str,
    dmg_glyph_fx_remap_recommendation_signals: dict[str, object],
) -> tuple[str, dict[str, object]]:
    """Score confidence for offline glyph-FX remap recommendations."""
    fx_churn = int(dmg_glyph_fx_remap_recommendation_signals.get("dmgGlyphFxLiveChurn", 0))
    glyph_churn = int(dmg_glyph_fx_remap_recommendation_signals.get("dmgGlyphChurn", 0))
    churn_score = fx_churn + glyph_churn

    if drift_risk == "HIGH" or churn_score >= 7:
        confidence = "LOW"
        rationale = "high-risk-or-high-churn"
    elif drift_risk == "MID" or churn_score >= 4:
        confidence = "MID"
        rationale = "mixed-risk-window"
    else:
        confidence = "HIGH"
        rationale = "stable-low-churn-window"

    return confidence, {
        "driftRisk": drift_risk,
        "dmgGlyphFxLiveChurn": fx_churn,
        "dmgGlyphChurn": glyph_churn,
        "churnScore": churn_score,
        "rationale": rationale,
    }


def dmgnum_life_trend_fx_pulse_remap_recommendation_from_trends(
    *,
    drift_risk: str,
    pressure_band: str,
    lane_cadence_recency: str,
    pulse_family: dict[str, int],
    pulse_confidence_family: dict[str, int],
) -> tuple[str, dict[str, object]]:
    """Recommend offline pulse-intensity remap posture from drift risk + cadence pressure bands."""
    pulse_churn = int(pulse_family.get("churn", 0))
    pulse_net = int(pulse_family.get("net", 0))
    pulse_coverage = str(pulse_family.get("coverage", "0/0"))

    pulse_conf_churn = int(pulse_confidence_family.get("churn", 0))
    pulse_conf_net = int(pulse_confidence_family.get("net", 0))
    pulse_conf_coverage = str(pulse_confidence_family.get("coverage", "0/0"))

    if drift_risk == "HIGH" or pressure_band == "HIGH" or lane_cadence_recency == "warn" or pulse_conf_churn >= 4:
        recommendation = "HOLD_PULSE_CONF"
        rationale = "high-risk-or-cadence-pressure"
        guidance = "Keep COAST/RUSH/BURST confidence mapping pinned while cadence pressure cools."
    elif pulse_churn >= 3 or (pulse_conf_churn >= 2 and pulse_net > 0):
        recommendation = "MICRO_TUNE_PULSE_CONF"
        rationale = "active-pulse-churn-window"
        guidance = "Draft offline confidence remap candidates; do not couple changes to runtime debug defaults yet."
    else:
        recommendation = "SYNC_WITH_TREND"
        rationale = "stable-pulse-window"
        guidance = "Keep deterministic confidence mapping and only align wording with trend-FX telemetry deltas."

    signals: dict[str, object] = {
        "driftRisk": drift_risk,
        "pressureBand": pressure_band,
        "laneCadenceRecency": lane_cadence_recency,
        "dmgnumLifeTrendFxPulseChurn": pulse_churn,
        "dmgnumLifeTrendFxPulseNet": pulse_net,
        "dmgnumLifeTrendFxPulseCoverage": pulse_coverage,
        "dmgnumLifeTrendFxPulseConfChurn": pulse_conf_churn,
        "dmgnumLifeTrendFxPulseConfNet": pulse_conf_net,
        "dmgnumLifeTrendFxPulseConfCoverage": pulse_conf_coverage,
        "rationale": rationale,
        "offlineOnly": True,
        "guidance": guidance,
    }
    return recommendation, signals


def pulse_remap_momentum_from_trends(
    *,
    recommendation: str,
    recommendation_signals: dict[str, object],
    remap_plan_family: dict[str, int],
) -> tuple[str, dict[str, object]]:
    """Prototype offline pulse-remap confidence momentum posture from remap-plan churn + cadence signals."""
    plan_churn = int(remap_plan_family.get("churn", 0))
    plan_net = int(remap_plan_family.get("net", 0))
    plan_coverage = str(remap_plan_family.get("coverage", "0/0"))
    drift_risk = str(recommendation_signals.get("driftRisk", "LOW"))
    pressure_band = str(recommendation_signals.get("pressureBand", "LOW"))
    cadence = str(recommendation_signals.get("laneCadenceRecency", "ok"))

    freeze_bias = 0
    if recommendation == "HOLD_PULSE_CONF":
        freeze_bias += 2
    elif recommendation == "MICRO_TUNE_PULSE_CONF":
        freeze_bias += 1

    if drift_risk == "HIGH":
        freeze_bias += 2
    elif drift_risk == "MID":
        freeze_bias += 1

    if pressure_band == "HIGH":
        freeze_bias += 1
    if cadence == "warn":
        freeze_bias += 1
    if plan_churn >= 3:
        freeze_bias += 1

    if freeze_bias >= 5:
        momentum = "FREEZE"
        rationale = "high-risk-or-plan-churn"
    elif freeze_bias >= 3 or (plan_churn >= 2 and plan_net > 0):
        momentum = "WATCH"
        rationale = "monitor-remap-window"
    else:
        momentum = "ALLOW"
        rationale = "stable-remap-window"

    signals: dict[str, object] = {
        "recommendation": recommendation,
        "driftRisk": drift_risk,
        "pressureBand": pressure_band,
        "laneCadenceRecency": cadence,
        "planChurn": plan_churn,
        "planNet": plan_net,
        "planCoverage": plan_coverage,
        "freezeBias": freeze_bias,
        "rationale": rationale,
        "offlineOnly": True,
    }
    return momentum, signals


def resolve_pulse_remap_momentum_alias(momentum: str) -> str:
    mapping = {
        "FREEZE": "F",
        "WATCH": "W",
        "ALLOW": "A",
    }
    return f"PRM:{mapping.get(momentum, 'W')}"


def resolve_pulse_remap_momentum_suppression_alias(suppression: str) -> str:
    mapping = {
        "SUPPRESS": "S",
        "ARM": "A",
        "OFF": "O",
    }
    return f"PRMS:{mapping.get(suppression, 'A')}"


def resolve_pulse_remap_suppression_plan_alias(plan: str) -> str:
    mapping = {
        "HOLD": "H",
        "ARM": "A",
        "LOCK": "L",
    }
    return f"PRSP:{mapping.get(plan, 'A')}"


def resolve_pulse_remap_scene_microline_variant_pack_selection_alias(selected_mode: str) -> str:
    mapping = {
        "PRIMARY": "PRI",
        "ALTERNATE": "ALT",
        "FALLBACK": "FBK",
    }
    return f"PRSMV:{mapping.get(selected_mode, 'ALT')}"


def resolve_pulse_remap_scene_microline_cadence_alias(cadence: str) -> str:
    mapping = {
        "RISE": "R",
        "HOLD": "H",
        "COOL": "C",
    }
    return f"PRSMC:{mapping.get(cadence, 'H')}"


def resolve_pulse_remap_scene_microline_style_policy_alias(policy: str) -> str:
    mapping = {
        "ANCHOR": "A",
        "BLEND": "B",
        "DIVERSIFY": "D",
    }
    return f"PRSMP:{mapping.get(policy, 'B')}"


def resolve_pulse_remap_scene_microline_style_posture_alias(posture: str) -> str:
    mapping = {
        "CALM": "C",
        "WARN": "W",
        "ALERT": "A",
    }
    return f"PRSMPP:{mapping.get(posture, 'W')}"


def resolve_pulse_remap_scene_fx_glint_alias(glint: str) -> str:
    mapping = {
        "SOFT": "S",
        "VOID": "V",
        "SPIKE": "P",
    }
    return f"PRSFX:{mapping.get(glint, 'V')}"


def resolve_pulse_remap_scene_copy_palette_recommendation_alias(palette: str) -> str:
    mapping = {
        "COOL": "C",
        "ASH": "A",
        "SCAR": "S",
    }
    return f"PRSCP:{mapping.get(palette, 'A')}"


def pulse_remap_suppression_escalation_plan_from_signals(
    *,
    suppression: str,
    suppression_signals: dict[str, object],
    momentum: str,
    drift_risk: str,
    lane_cadence_recency: str,
) -> tuple[str, dict[str, object]]:
    """Offline escalation recommendation for repeated pulse-remap suppression windows."""
    current_suppression = str(suppression).strip().upper() or "ARM"
    current_momentum = str(momentum).strip().upper() or "WATCH"
    current_drift_risk = str(drift_risk).strip().upper() or "MID"
    current_lane_cadence = str(lane_cadence_recency).strip().lower() or "ok"
    freeze_streak = max(0, int(suppression_signals.get("freezeStreak", 0) or 0))

    if current_suppression == "SUPPRESS" and (freeze_streak >= 4 or current_drift_risk == "HIGH"):
        plan = "LOCK"
        reason = "suppression-streak-or-high-risk-demands-lock"
    elif current_suppression in {"SUPPRESS", "ARM"} or current_momentum == "FREEZE":
        plan = "ARM"
        reason = "suppression-pressure-building"
    else:
        plan = "HOLD"
        reason = "suppression-pressure-stable"

    if current_lane_cadence == "warn" and plan == "LOCK":
        reason = "cadence-warn-keeps-lock-until-rebalanced"

    return plan, {
        "suppression": current_suppression,
        "momentum": current_momentum,
        "freezeStreak": freeze_streak,
        "driftRisk": current_drift_risk,
        "laneCadenceRecency": current_lane_cadence,
        "offlineOnly": True,
        "reason": reason,
    }


def pulse_remap_scene_flavor_from_signals(
    *,
    suppression_plan: str,
    suppression_plan_signals: dict[str, object],
    pressure_band: str,
) -> tuple[str, dict[str, object]]:
    """Prototype scene-reactive flavor mapping for pulse-remap suppression readability copy."""
    plan = str(suppression_plan).strip().upper() or "ARM"
    drift_risk = str(suppression_plan_signals.get("driftRisk", "MID")).strip().upper() or "MID"
    cadence = str(suppression_plan_signals.get("laneCadenceRecency", "ok")).strip().lower() or "ok"
    current_pressure = str(pressure_band).strip().upper() or "MID"

    if plan == "LOCK" or drift_risk == "HIGH":
        flavor = "LOCK"
        reason = "lock-plan-or-high-drift-risk"
    elif plan == "ARM" or current_pressure == "HIGH":
        flavor = "BRACE"
        reason = "arming-window-or-high-pressure"
    else:
        flavor = "CALM"
        reason = "stable-hold-window"

    return flavor, {
        "suppressionPlan": plan,
        "driftRisk": drift_risk,
        "pressureBand": current_pressure,
        "laneCadenceRecency": cadence,
        "reason": reason,
        "offlineOnly": True,
    }


def pulse_remap_scene_microline_from_signals(
    *,
    suppression_plan: str,
    scene_flavor: str,
    scene_confidence: str,
    lane_cadence_recency: str,
    suppression_plan_family_trend_signals: dict[str, object],
) -> tuple[str, dict[str, object]]:
    """Prototype scene-reactive microline copy from suppression-plan cadence memory (offline-only)."""
    plan = str(suppression_plan).strip().upper() or "ARM"
    flavor = str(scene_flavor).strip().upper() or "BRACE"
    confidence = str(scene_confidence).strip().upper() or "MED"
    cadence = str(lane_cadence_recency).strip().lower() or "ok"
    cadence_trend = str(suppression_plan_family_trend_signals.get("trend", "FLAT")).strip().upper() or "FLAT"
    prior_loaded = bool(suppression_plan_family_trend_signals.get("priorLoaded", False))
    prior_net = int(suppression_plan_family_trend_signals.get("priorNet", 0) or 0)
    current_net = int(suppression_plan_family_trend_signals.get("currentNet", 0) or 0)
    cadence_memory = (
        f"{cadence_trend}:{prior_net:+d}->{current_net:+d}"
        if prior_loaded
        else f"{cadence_trend}:cold-start"
    )

    if plan == "LOCK" and cadence == "warn":
        microline = "Lock the pulse; cadence debt is still hot."
        reason = "lock-with-cadence-warning"
    elif plan == "LOCK":
        microline = "Lock the pulse and let the route settle before remap chatter."
        reason = "lock-plan-stability"
    elif plan == "ARM" and cadence == "warn":
        microline = "Brace the pulse; cadence memory says hold the line."
        reason = "arm-plan-cadence-warning"
    elif plan == "ARM" and cadence_trend == "UP":
        microline = "Brace softly; suppression pressure is rising window to window."
        reason = "arm-plan-uptrend"
    elif flavor == "CALM" and confidence == "LOW":
        microline = "Calm window confirmed; keep narration lean and steady."
        reason = "calm-low-risk-window"
    else:
        microline = "Pulse stays watchful while cadence memory normalizes."
        reason = "default-watchful-window"

    return microline, {
        "suppressionPlan": plan,
        "sceneFlavor": flavor,
        "sceneConfidence": confidence,
        "laneCadenceRecency": cadence,
        "cadenceTrend": cadence_trend,
        "cadenceMemory": cadence_memory,
        "reason": reason,
        "offlineOnly": True,
    }


def pulse_remap_scene_microline_variant_pack_from_signals(
    *,
    suppression_plan: str,
    scene_flavor: str,
    scene_confidence: str,
    lane_cadence_recency: str,
    suppression_plan_family_trend_signals: dict[str, object],
) -> tuple[dict[str, str], dict[str, object]]:
    """Prototype dual-line narrative microline variant pack with confidence-aware fallback (offline-only)."""
    plan = str(suppression_plan).strip().upper() or "ARM"
    flavor = str(scene_flavor).strip().upper() or "BRACE"
    confidence = str(scene_confidence).strip().upper() or "MED"
    cadence = str(lane_cadence_recency).strip().lower() or "ok"
    cadence_trend = str(suppression_plan_family_trend_signals.get("trend", "FLAT")).strip().upper() or "FLAT"

    primary = "Pulse stays watchful while cadence memory normalizes."
    alternate = "Keep route narration tight while suppression posture settles."
    fallback = "Cadence memory uncertain; defaulting to steady suppression callout."

    if plan == "LOCK":
        primary = "Lockline A: Anchor the pulse and let route noise collapse."
        alternate = "Lockline B: Hold the lock posture until cadence debt cools."
    elif plan == "ARM":
        primary = "Armline A: Brace the route; suppression posture is engaging."
        alternate = "Armline B: Keep pressure readable while cadence catches up."
    elif flavor == "CALM":
        primary = "Calmline A: Keep pulse narration soft and route cues clear."
        alternate = "Calmline B: Let low-pressure pacing carry the handoff."

    if cadence == "warn" and confidence in {"MED", "HIGH"}:
        alternate = "Warning line: Cadence warning active—prefer conservative suppression wording."

    selected = fallback if confidence == "LOW" else (alternate if cadence_trend == "UP" else primary)
    selected_mode = "FALLBACK" if selected == fallback else ("ALTERNATE" if selected == alternate else "PRIMARY")

    return {
        "primary": primary,
        "alternate": alternate,
        "fallback": fallback,
        "selected": selected,
        "selectedMode": selected_mode,
    }, {
        "suppressionPlan": plan,
        "sceneFlavor": flavor,
        "sceneConfidence": confidence,
        "laneCadenceRecency": cadence,
        "cadenceTrend": cadence_trend,
        "selectedMode": selected_mode,
        "reason": "low-confidence-fallback" if selected_mode == "FALLBACK" else "confidence-aware-dual-line-selection",
        "offlineOnly": True,
    }


def pulse_remap_scene_microline_style_diversification_policy_from_signals(
    *,
    suppression_plan: str,
    scene_confidence: str,
    lane_cadence_recency: str,
    suppression_plan_family_trend_signals: dict[str, object],
) -> tuple[str, dict[str, object]]:
    """Prototype offline microline-style diversification policy from cadence-memory volatility windows."""
    plan = str(suppression_plan).strip().upper() or "ARM"
    confidence = str(scene_confidence).strip().upper() or "MED"
    cadence = str(lane_cadence_recency).strip().lower() or "ok"
    trend = str(suppression_plan_family_trend_signals.get("trend", "FLAT")).strip().upper() or "FLAT"
    prior_loaded = bool(suppression_plan_family_trend_signals.get("priorLoaded", False))
    prior_net = int(suppression_plan_family_trend_signals.get("priorNet", 0) or 0)
    current_net = int(suppression_plan_family_trend_signals.get("currentNet", 0) or 0)
    volatility = abs(current_net - prior_net)

    if plan == "LOCK" or cadence == "warn" or volatility >= 3:
        policy = "ANCHOR"
        reason = "lock-or-volatile-cadence-memory"
    elif trend == "DOWN" and cadence == "ok" and confidence in {"LOW", "MED"} and volatility <= 1:
        policy = "DIVERSIFY"
        reason = "cooling-cadence-window-supports-style-expansion"
    else:
        policy = "BLEND"
        reason = "moderate-cadence-memory-window"

    return policy, {
        "suppressionPlan": plan,
        "sceneConfidence": confidence,
        "laneCadenceRecency": cadence,
        "cadenceTrend": trend,
        "priorNet": prior_net,
        "currentNet": current_net,
        "cadenceVolatility": volatility,
        "priorLoaded": prior_loaded,
        "reason": reason,
        "offlineOnly": True,
    }


def pulse_remap_scene_microline_style_policy_smoothed_from_prior(
    *,
    policy: str,
    policy_signals: dict[str, object],
    prior_json_path: Path,
) -> tuple[str, dict[str, object]]:
    """Offline-only volatility smoothing guard for style-policy oscillation control."""
    current_policy = str(policy).strip().upper() or "BLEND"
    volatility = int(policy_signals.get("cadenceVolatility", 0) or 0)

    prior_policy = current_policy
    prior_loaded = False
    if prior_json_path.is_file():
        try:
            prior_payload = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_policy = str(
                prior_payload.get(
                    "pulseRemapSceneMicrolineStylePolicySmoothed",
                    prior_payload.get("pulseRemapSceneMicrolineStyleDiversificationPolicy", current_policy),
                )
            ).strip().upper() or current_policy
            prior_loaded = True
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    if prior_loaded and current_policy != prior_policy and volatility <= 1:
        smoothed_policy = prior_policy
        reason = "hold-prior-policy-on-low-volatility"
    else:
        smoothed_policy = current_policy
        reason = "adopt-current-policy"

    return smoothed_policy, {
        "currentPolicy": current_policy,
        "priorPolicy": prior_policy,
        "priorLoaded": prior_loaded,
        "cadenceVolatility": volatility,
        "reason": reason,
        "offlineOnly": True,
    }


def pulse_remap_scene_microline_style_policy_posture_hook_from_signals(
    *,
    smoothed_policy: str,
    style_policy_family_trend_signals: dict[str, object],
    lane_cadence_recency: str,
) -> tuple[str, dict[str, object]]:
    """Offline-only posture hook from style-policy smoothing + family drift context."""
    policy = str(smoothed_policy).strip().upper() or "BLEND"
    trend = str(style_policy_family_trend_signals.get("trend", "FLAT")).strip().upper() or "FLAT"
    current_net = int(style_policy_family_trend_signals.get("currentNet", 0) or 0)
    prior_net = int(style_policy_family_trend_signals.get("priorNet", 0) or 0)
    cadence = str(lane_cadence_recency).strip().lower() or "ok"

    if policy == "ANCHOR" and (trend == "UP" or cadence == "warn"):
        posture = "ALERT"
        reason = "anchor-policy-under-rising-or-warning-cadence"
    elif policy == "DIVERSIFY" and trend == "DOWN" and cadence == "ok":
        posture = "CALM"
        reason = "diversify-policy-in-cooling-cadence-window"
    else:
        posture = "WARN"
        reason = "mixed-style-policy-signals"

    return posture, {
        "smoothedPolicy": policy,
        "styleTrend": trend,
        "currentNet": current_net,
        "priorNet": prior_net,
        "laneCadenceRecency": cadence,
        "reason": reason,
        "offlineOnly": True,
    }


def pulse_remap_scene_microline_cadence_from_signals(
    *,
    suppression_plan: str,
    scene_confidence: str,
    lane_cadence_recency: str,
    suppression_plan_family_trend_signals: dict[str, object],
) -> tuple[str, dict[str, object]]:
    """Offline-only cadence posture for scene microline handoff readability."""
    plan = str(suppression_plan).strip().upper() or "ARM"
    confidence = str(scene_confidence).strip().upper() or "MED"
    cadence = str(lane_cadence_recency).strip().lower() or "ok"
    cadence_trend = str(suppression_plan_family_trend_signals.get("trend", "FLAT")).strip().upper() or "FLAT"

    if plan == "LOCK" or (confidence == "HIGH" and cadence in {"warn", "gap"}):
        cadence_posture = "RISE"
        reason = "lock-or-high-confidence-warning"
    elif cadence_trend == "DOWN" and cadence == "ok":
        cadence_posture = "COOL"
        reason = "downtrend-with-healthy-cadence"
    else:
        cadence_posture = "HOLD"
        reason = "default-hold-window"

    return cadence_posture, {
        "suppressionPlan": plan,
        "sceneConfidence": confidence,
        "laneCadenceRecency": cadence,
        "cadenceTrend": cadence_trend,
        "reason": reason,
        "offlineOnly": True,
    }


def pulse_remap_scene_fx_glint_from_signals(
    *,
    style_posture: str,
    suppression_warning: str,
    scene_confidence: str,
) -> tuple[str, dict[str, object]]:
    """Offline-only VFX readability cue from style posture + warning pressure."""
    posture = str(style_posture).strip().upper() or "WARN"
    warning = str(suppression_warning).strip().upper() or "CAUTION"
    confidence = str(scene_confidence).strip().upper() or "MED"

    if posture == "CALM" and warning == "STEADY":
        glint = "SOFT"
        reason = "calm-posture-steady-warning"
    elif posture == "ALERT" or warning == "ALERT" or confidence == "HIGH":
        glint = "SPIKE"
        reason = "alert-or-high-confidence-risk"
    else:
        glint = "VOID"
        reason = "mixed-mid-pressure-signals"

    return glint, {
        "stylePosture": posture,
        "suppressionWarning": warning,
        "sceneConfidence": confidence,
        "reason": reason,
        "offlineOnly": True,
    }


def pulse_remap_scene_copy_palette_recommendation_from_signals(
    *,
    scene_flavor: str,
    scene_confidence: str,
    scene_fx_glint: str,
    style_posture: str,
) -> tuple[str, dict[str, object]]:
    """Offline-only scene-copy palette cue derived from scene flavor + glint posture."""
    flavor = str(scene_flavor).strip().upper() or "BRACE"
    confidence = str(scene_confidence).strip().upper() or "MED"
    glint = str(scene_fx_glint).strip().upper() or "VOID"
    posture = str(style_posture).strip().upper() or "WARN"

    if glint == "SPIKE" or flavor == "LOCK":
        palette = "SCAR"
        reason = "high-pressure-glint-or-lock-flavor"
    elif glint == "SOFT" and posture == "CALM" and confidence in {"LOW", "MED"}:
        palette = "COOL"
        reason = "calm-soft-glint-window"
    else:
        palette = "ASH"
        reason = "balanced-mid-pressure-default"

    return palette, {
        "sceneFlavor": flavor,
        "sceneConfidence": confidence,
        "sceneFxGlint": glint,
        "stylePosture": posture,
        "reason": reason,
        "offlineOnly": True,
    }


def pulse_remap_momentum_drift_from_prior(
    *,
    current_momentum: str,
    prior_json_path: Path,
) -> tuple[int, dict[str, object]]:
    """Track pulse-remap momentum drift against prior digest window."""
    score_map = {
        "FREEZE": -1,
        "WATCH": 0,
        "ALLOW": 1,
    }

    current = str(current_momentum).strip().upper() or "WATCH"
    prior = current
    prior_loaded = False

    if prior_json_path.is_file():
        try:
            prior_payload = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior = str(prior_payload.get("pulseRemapMomentumRecommendation", current)).strip().upper() or current
            prior_loaded = True
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    current_score = score_map.get(current, 0)
    prior_score = score_map.get(prior, current_score)
    drift = current_score - prior_score

    if drift > 0:
        reason = "pulse-remap-momentum-relaxed-vs-prior-window"
    elif drift < 0:
        reason = "pulse-remap-momentum-tightened-vs-prior-window"
    else:
        reason = "pulse-remap-momentum-held-vs-prior-window"

    return drift, {
        "currentMomentum": current,
        "currentScore": current_score,
        "priorMomentum": prior,
        "priorScore": prior_score,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def pulse_remap_momentum_streak_suppression_from_prior(
    *,
    current_momentum: str,
    prior_json_path: Path,
) -> tuple[str, dict[str, object]]:
    """Prototype offline suppression policy when FREEZE repeats across digest windows."""
    current = str(current_momentum).strip().upper() or "WATCH"
    prior = current
    prior_streak = 0
    prior_loaded = False

    if prior_json_path.is_file():
        try:
            prior_payload = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior = str(prior_payload.get("pulseRemapMomentumRecommendation", current)).strip().upper() or current
            prior_streak = max(0, int(prior_payload.get("pulseRemapMomentumFreezeStreak", 0) or 0))
            prior_loaded = True
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    if current == "FREEZE":
        freeze_streak = prior_streak + 1 if prior_loaded and prior == "FREEZE" else 1
    else:
        freeze_streak = 0

    threshold = 2
    suppress = current == "FREEZE" and freeze_streak >= threshold
    if suppress:
        policy = "SUPPRESS"
        reason = "freeze-streak-threshold-met"
    elif current == "FREEZE":
        policy = "ARM"
        reason = "freeze-streak-building"
    else:
        policy = "OFF"
        reason = "momentum-not-freeze"

    return policy, {
        "currentMomentum": current,
        "priorMomentum": prior,
        "priorLoaded": prior_loaded,
        "priorFreezeStreak": prior_streak,
        "freezeStreak": freeze_streak,
        "threshold": threshold,
        "suppress": suppress,
        "offlineOnly": True,
        "reason": reason,
    }


def pulse_remap_suppression_family_trend_from_prior(
    *,
    current_family_totals: dict[str, int],
    prior_json_path: Path,
) -> tuple[int, dict[str, object]]:
    """Track PRMS family net drift against prior digest window for triage."""
    current_net = int(current_family_totals.get("net", 0) or 0)
    prior_net = 0
    prior_loaded = False

    if prior_json_path.is_file():
        try:
            prior_payload = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_families = prior_payload.get("tokenFamilyTotals", {})
            prior_family = prior_families.get("pulseRemapMomentumSuppressionAlias", {}) if isinstance(prior_families, dict) else {}
            prior_net = int(prior_family.get("net", 0) or 0)
            prior_loaded = True
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    drift = current_net - prior_net
    if drift > 0:
        trend = "UP"
        reason = "suppression-family-net-increased-vs-prior-window"
    elif drift < 0:
        trend = "DOWN"
        reason = "suppression-family-net-decreased-vs-prior-window"
    else:
        trend = "FLAT"
        reason = "suppression-family-net-unchanged-vs-prior-window"

    return drift, {
        "trend": trend,
        "currentNet": current_net,
        "priorNet": prior_net,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def pulse_remap_suppression_plan_family_trend_from_prior(
    *,
    current_family_totals: dict[str, int],
    prior_json_path: Path,
) -> tuple[int, dict[str, object]]:
    """Track PRSP family net drift against prior digest window for lane-cadence guardrails."""
    current_net = int(current_family_totals.get("net", 0) or 0)
    prior_net = 0
    prior_loaded = False

    if prior_json_path.is_file():
        try:
            prior_payload = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_families = prior_payload.get("tokenFamilyTotals", {})
            prior_family = prior_families.get("pulseRemapSuppressionPlanAlias", {}) if isinstance(prior_families, dict) else {}
            prior_net = int(prior_family.get("net", 0) or 0)
            prior_loaded = True
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    drift = current_net - prior_net
    if drift > 0:
        trend = "UP"
        reason = "suppression-plan-family-net-increased-vs-prior-window"
    elif drift < 0:
        trend = "DOWN"
        reason = "suppression-plan-family-net-decreased-vs-prior-window"
    else:
        trend = "FLAT"
        reason = "suppression-plan-family-net-unchanged-vs-prior-window"

    return drift, {
        "trend": trend,
        "currentNet": current_net,
        "priorNet": prior_net,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def pulse_remap_scene_microline_cadence_family_trend_from_prior(
    *,
    current_family_totals: dict[str, int],
    prior_json_path: Path,
) -> tuple[int, dict[str, object]]:
    """Track PRSMC family net drift against prior digest window for cadence triage."""
    current_net = int(current_family_totals.get("net", 0) or 0)
    prior_net = 0
    prior_loaded = False

    if prior_json_path.is_file():
        try:
            prior_payload = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_families = prior_payload.get("tokenFamilyTotals", {})
            prior_family = prior_families.get("pulseRemapSceneMicrolineCadenceAlias", {}) if isinstance(prior_families, dict) else {}
            prior_net = int(prior_family.get("net", 0) or 0)
            prior_loaded = True
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    drift = current_net - prior_net
    if drift > 0:
        trend = "UP"
        reason = "scene-microline-cadence-family-net-increased-vs-prior-window"
    elif drift < 0:
        trend = "DOWN"
        reason = "scene-microline-cadence-family-net-decreased-vs-prior-window"
    else:
        trend = "FLAT"
        reason = "scene-microline-cadence-family-net-unchanged-vs-prior-window"

    return drift, {
        "trend": trend,
        "currentNet": current_net,
        "priorNet": prior_net,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def combo_confidence_coach_copy_swap_recommendation_family_trend_from_prior(
    *,
    current_family_totals: dict[str, int],
    prior_json_path: Path,
    prior_family_key: str = "dmgComboConfidenceCoachCopySwapRecommendationAlias",
) -> tuple[int, dict[str, object]]:
    """Track copy-swap recommendation family net drift against prior digest window."""
    current_net = int(current_family_totals.get("net", 0) or 0)
    prior_net = 0
    prior_loaded = False
    prior_trend = "FLAT"

    if prior_json_path.is_file():
        try:
            prior_payload = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_families = prior_payload.get("tokenFamilyTotals", {})
            prior_family = prior_families.get(prior_family_key, {}) if isinstance(prior_families, dict) else {}
            prior_net = int(prior_family.get("net", 0) or 0)
            prior_signals = prior_payload.get("comboConfidenceCoachCopySwapRecommendationFamilyTrendSignals", {})
            if isinstance(prior_signals, dict):
                prior_trend = str(prior_signals.get("trend", "FLAT") or "FLAT").upper()
            prior_loaded = True
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    raw_drift = current_net - prior_net
    if raw_drift > 0:
        trend = "UP"
        reason = "combo-confidence-copy-swap-family-net-increased-vs-prior-window"
    elif raw_drift < 0:
        trend = "DOWN"
        reason = "combo-confidence-copy-swap-family-net-decreased-vs-prior-window"
    else:
        trend = "FLAT"
        reason = "combo-confidence-copy-swap-family-net-unchanged-vs-prior-window"

    hysteresis_applied = False
    hysteresis_threshold = 1
    if prior_loaded and prior_trend in {"UP", "DOWN"} and trend in {"UP", "DOWN"} and prior_trend != trend and abs(raw_drift) <= hysteresis_threshold:
        trend = "FLAT"
        reason = "copy-swap-trend-hysteresis-suppressed-small-direction-flip"
        hysteresis_applied = True

    return raw_drift, {
        "trend": trend,
        "currentNet": current_net,
        "priorNet": prior_net,
        "priorLoaded": prior_loaded,
        "priorTrend": prior_trend,
        "hysteresisApplied": hysteresis_applied,
        "hysteresisThreshold": hysteresis_threshold,
        "reason": reason,
    }


def combo_confidence_fx_accent_family_trend_from_prior(
    *,
    current_family_totals: dict[str, int],
    prior_json_path: Path,
    volatility_regime: str = "CALM",
) -> tuple[int, dict[str, object]]:
    """Track DCCFX/combo-confidence-fx-accent family net drift against prior digest window."""
    current_net = int(current_family_totals.get("net", 0) or 0)
    prior_net = 0
    prior_loaded = False
    prior_trend = "FLAT"

    if prior_json_path.is_file():
        try:
            prior_payload = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_families = prior_payload.get("tokenFamilyTotals", {})
            prior_family = prior_families.get("dmgComboConfidenceFxAccentAlias", {}) if isinstance(prior_families, dict) else {}
            prior_net = int(prior_family.get("net", 0) or 0)
            prior_trend_payload = prior_payload.get("comboConfidenceFxAccentFamilyTrendSignals", {})
            if isinstance(prior_trend_payload, dict):
                prior_trend = str(prior_trend_payload.get("trend", "FLAT") or "FLAT").upper()
            prior_loaded = True
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    drift = current_net - prior_net
    raw_drift = drift
    if raw_drift > 0:
        trend = "UP"
        reason = "combo-confidence-fx-accent-family-net-increased-vs-prior-window"
    elif raw_drift < 0:
        trend = "DOWN"
        reason = "combo-confidence-fx-accent-family-net-decreased-vs-prior-window"
    else:
        trend = "FLAT"
        reason = "combo-confidence-fx-accent-family-net-unchanged-vs-prior-window"

    regime = str(volatility_regime or "CALM").upper()
    threshold_by_regime = {
        "SPIKE": 3,
        "SWING": 2,
        "CALM": 1,
    }
    hysteresis_threshold = threshold_by_regime.get(regime, 1)
    hysteresis_applied = False
    if (
        prior_loaded
        and prior_trend in {"UP", "DOWN"}
        and trend in {"UP", "DOWN"}
        and prior_trend != trend
        and abs(raw_drift) <= hysteresis_threshold
    ):
        trend = "FLAT"
        reason = "fx-accent-trend-hysteresis-suppressed-small-direction-flip"
        hysteresis_applied = True

    if not prior_loaded:
        recommendation = "ALLOW"
        recommendation_reason = "no-prior-window"
    elif trend == "FLAT" and raw_drift != 0:
        recommendation = "HOLD"
        recommendation_reason = "hysteresis-suppressed-direction-flip"
    elif abs(raw_drift) >= hysteresis_threshold + 2:
        recommendation = "ALLOW"
        recommendation_reason = "drift-cleared-hysteresis-buffer"
    elif regime in {"SWING", "SPIKE"}:
        recommendation = "HOLD"
        recommendation_reason = "volatile-regime-prefers-stability"
    else:
        recommendation = "ALLOW"
        recommendation_reason = "calm-regime-allows-adaptation"

    magnitude = abs(raw_drift)
    if magnitude >= hysteresis_threshold + 2:
        confidence = "HIGH"
        confidence_reason = "drift-magnitude-clearly-above-threshold"
    elif magnitude >= hysteresis_threshold:
        confidence = "MID"
        confidence_reason = "drift-magnitude-near-threshold"
    else:
        confidence = "LOW"
        confidence_reason = "drift-magnitude-below-threshold"

    return drift, {
        "trend": trend,
        "currentNet": current_net,
        "priorNet": prior_net,
        "priorLoaded": prior_loaded,
        "priorTrend": prior_trend,
        "rawDrift": raw_drift,
        "volatilityRegime": regime,
        "hysteresisApplied": hysteresis_applied,
        "hysteresisThreshold": hysteresis_threshold,
        "trendHysteresisRecommendation": recommendation,
        "trendHysteresisRecommendationReason": recommendation_reason,
        "trendHysteresisConfidence": confidence,
        "trendHysteresisConfidenceReason": confidence_reason,
        "reason": reason,
        "offlineOnly": True,
    }


def pulse_remap_scene_fx_glint_family_trend_from_prior(
    *,
    current_family_totals: dict[str, int],
    prior_json_path: Path,
) -> tuple[int, dict[str, object]]:
    """Track PRSFX/glint family net drift against prior digest window."""
    current_net = int(current_family_totals.get("net", 0) or 0)
    prior_net = 0
    prior_loaded = False

    if prior_json_path.is_file():
        try:
            prior_payload = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_families = prior_payload.get("tokenFamilyTotals", {})
            prior_family = prior_families.get("pulseRemapSceneFxGlintAlias", {}) if isinstance(prior_families, dict) else {}
            prior_net = int(prior_family.get("net", 0) or 0)
            prior_loaded = True
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    drift = current_net - prior_net
    if drift > 0:
        trend = "UP"
        reason = "scene-fx-glint-family-net-increased-vs-prior-window"
    elif drift < 0:
        trend = "DOWN"
        reason = "scene-fx-glint-family-net-decreased-vs-prior-window"
    else:
        trend = "FLAT"
        reason = "scene-fx-glint-family-net-unchanged-vs-prior-window"

    return drift, {
        "trend": trend,
        "currentNet": current_net,
        "priorNet": prior_net,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def lane_priority_hysteresis_floor_family_trend_from_prior(
    *,
    current_family_totals: dict[str, int],
    prior_json_path: Path,
) -> tuple[int, dict[str, object]]:
    """Track LPR HYS FLOOR REC/HYS FLOOR family net drift against prior digest window."""
    current_net = int(current_family_totals.get("net", 0) or 0)
    prior_net = 0
    prior_loaded = False

    if prior_json_path.is_file():
        try:
            prior_payload = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_families = prior_payload.get("tokenFamilyTotals", {})
            prior_family = prior_families.get("lanePriorityHysteresisFloorRecommendationAlias", {}) if isinstance(prior_families, dict) else {}
            prior_net = int(prior_family.get("net", 0) or 0)
            prior_loaded = True
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    drift = current_net - prior_net
    if drift > 0:
        trend = "UP"
        reason = "lane-hys-floor-family-net-increased-vs-prior-window"
    elif drift < 0:
        trend = "DOWN"
        reason = "lane-hys-floor-family-net-decreased-vs-prior-window"
    else:
        trend = "FLAT"
        reason = "lane-hys-floor-family-net-unchanged-vs-prior-window"

    return drift, {
        "trend": trend,
        "currentNet": current_net,
        "priorNet": prior_net,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def pulse_remap_scene_copy_palette_recommendation_family_trend_from_prior(
    *,
    current_family_totals: dict[str, int],
    prior_json_path: Path,
) -> tuple[int, dict[str, object]]:
    """Track PRSCP/copy-palette family net drift against prior digest window."""
    current_net = int(current_family_totals.get("net", 0) or 0)
    prior_net = 0
    prior_loaded = False

    if prior_json_path.is_file():
        try:
            prior_payload = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_families = prior_payload.get("tokenFamilyTotals", {})
            prior_family = prior_families.get("pulseRemapSceneCopyPaletteRecommendationAlias", {}) if isinstance(prior_families, dict) else {}
            prior_net = int(prior_family.get("net", 0) or 0)
            prior_loaded = True
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    drift = current_net - prior_net
    if drift > 0:
        trend = "UP"
        reason = "scene-copy-palette-family-net-increased-vs-prior-window"
    elif drift < 0:
        trend = "DOWN"
        reason = "scene-copy-palette-family-net-decreased-vs-prior-window"
    else:
        trend = "FLAT"
        reason = "scene-copy-palette-family-net-unchanged-vs-prior-window"

    return drift, {
        "trend": trend,
        "currentNet": current_net,
        "priorNet": prior_net,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def pulse_remap_scene_microline_style_policy_family_trend_from_prior(
    *,
    current_family_totals: dict[str, int],
    prior_json_path: Path,
) -> tuple[int, dict[str, object]]:
    """Track PRSMP/style-policy family net drift against prior digest window."""
    current_net = int(current_family_totals.get("net", 0) or 0)
    prior_net = 0
    prior_loaded = False

    if prior_json_path.is_file():
        try:
            prior_payload = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_families = prior_payload.get("tokenFamilyTotals", {})
            prior_family = prior_families.get("pulseRemapSceneMicrolineStylePolicyAlias", {}) if isinstance(prior_families, dict) else {}
            prior_net = int(prior_family.get("net", 0) or 0)
            prior_loaded = True
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    drift = current_net - prior_net
    if drift > 0:
        trend = "UP"
        reason = "scene-microline-style-policy-family-net-increased-vs-prior-window"
    elif drift < 0:
        trend = "DOWN"
        reason = "scene-microline-style-policy-family-net-decreased-vs-prior-window"
    else:
        trend = "FLAT"
        reason = "scene-microline-style-policy-family-net-unchanged-vs-prior-window"

    return drift, {
        "trend": trend,
        "currentNet": current_net,
        "priorNet": prior_net,
        "priorLoaded": prior_loaded,
        "reason": reason,
    }


def combo_window_retune_recommendation_from_trends(
    *,
    combo_family: dict[str, object],
    pressure_band: str,
    drift_risk: str,
    lane_cadence_recency: str,
) -> tuple[str, dict[str, object]]:
    """Offline-only combo-window retune recommendation from churn + pressure context."""
    combo_churn = int(combo_family.get("churn", 0) or 0)
    combo_net = int(combo_family.get("net", 0) or 0)
    if combo_churn >= 4 or drift_risk == "HIGH":
        recommendation = "TIGHTEN"
        rationale = "high-combo-churn-or-high-drift"
    elif pressure_band == "HIGH" or lane_cadence_recency == "warn":
        recommendation = "HOLD"
        rationale = "high-pressure-or-lane-recency-warn"
    else:
        recommendation = "EXPAND"
        rationale = "stable-combo-window-signals"
    signals = {
        "rationale": rationale,
        "comboChurn": combo_churn,
        "comboNet": combo_net,
        "pressureBand": pressure_band,
        "driftRisk": drift_risk,
        "laneCadenceRecency": lane_cadence_recency,
        "offlineOnly": True,
    }
    return recommendation, signals




def combo_window_retune_confidence_from_signals(
    *,
    recommendation: str,
    recommendation_signals: dict[str, object],
) -> tuple[str, dict[str, object]]:
    """Confidence band for combo-window retune recommendation (offline digest only)."""
    combo_churn = int(recommendation_signals.get("comboChurn", 0) or 0)
    combo_net = int(recommendation_signals.get("comboNet", 0) or 0)
    drift_risk = str(recommendation_signals.get("driftRisk", "LOW") or "LOW")
    pressure_band = str(recommendation_signals.get("pressureBand", "LOW") or "LOW")

    if drift_risk == "HIGH" or combo_churn >= 4:
        confidence = "LOW"
        rationale = "high-drift-or-high-churn"
    elif recommendation == "HOLD" or pressure_band == "HIGH" or combo_churn >= 2 or abs(combo_net) >= 2:
        confidence = "MID"
        rationale = "moderate-pressure-or-signal-variance"
    else:
        confidence = "HIGH"
        rationale = "stable-combo-retune-signals"

    return confidence, {
        "rationale": rationale,
        "recommendation": recommendation,
        "comboChurn": combo_churn,
        "comboNet": combo_net,
        "driftRisk": drift_risk,
        "pressureBand": pressure_band,
        "offlineOnly": True,
    }


def combo_chain_narrative_coach_line_from_signals(
    *,
    combo_window_retune_recommendation: str,
    combo_window_retune_confidence: str,
    combo_window_retune_recommendation_signals: dict[str, object],
) -> tuple[str, dict[str, object]]:
    """Offline-only narrative coach line tied to combo-window retune + pressure trend."""
    recommendation = str(combo_window_retune_recommendation).upper()
    confidence = str(combo_window_retune_confidence).upper()
    pressure_band = str(combo_window_retune_recommendation_signals.get("pressureBand", "LOW") or "LOW").upper()
    drift_risk = str(combo_window_retune_recommendation_signals.get("driftRisk", "LOW") or "LOW").upper()
    lane_cadence_recency = str(combo_window_retune_recommendation_signals.get("laneCadenceRecency", "ok") or "ok").lower()

    if recommendation == "TIGHTEN":
        line = "LOCK CHAINS, CASH BURSTS."
        reason = "tighten-retune-prioritizes-secure-finish-rhythm"
    elif recommendation == "HOLD" and pressure_band == "HIGH":
        line = "HOLD RHYTHM, BAIT THE SPIKE."
        reason = "hold-retune-under-high-pressure"
    elif recommendation == "HOLD":
        line = "KEEP TEMPO, SCAN FOR OPENINGS."
        reason = "hold-retune-under-moderate-pressure"
    else:
        line = "EXTEND STRING, FARM MOMENTUM."
        reason = "expand-retune-with-stable-pressure"

    if confidence == "LOW" and recommendation != "TIGHTEN":
        line = "KEEP IT CLEAN, NO GREED."
        reason = "low-confidence-guardrail-copy"
    elif drift_risk == "HIGH" and recommendation != "TIGHTEN":
        line = "SHORT CHAINS, RESET EARLY."
        reason = "high-drift-risk-guardrail-copy"
    elif lane_cadence_recency == "warn" and recommendation == "EXPAND":
        line = "EXTEND LIGHT, WATCH ROTATION."
        reason = "expand-retune-with-lane-cadence-warning"

    return line, {
        "reason": reason,
        "recommendation": recommendation,
        "confidence": confidence,
        "pressureBand": pressure_band,
        "driftRisk": drift_risk,
        "laneCadenceRecency": lane_cadence_recency,
        "offlineOnly": True,
    }


def combo_confidence_coach_recommendation_from_signals(
    *,
    combo_family: dict[str, object],
    combo_confidence_family: dict[str, object],
    pressure_band: str,
    drift_risk: str,
) -> tuple[str, dict[str, object]]:
    """Offline-only coach recommendation from kill-heat volatility + pressure drift."""
    combo_churn = int(combo_family.get("churn", 0) or 0)
    combo_net = int(combo_family.get("net", 0) or 0)
    conf_churn = int(combo_confidence_family.get("churn", 0) or 0)
    conf_net = int(combo_confidence_family.get("net", 0) or 0)

    kill_heat_volatility = combo_churn + conf_churn + abs(combo_net) + abs(conf_net)

    if drift_risk == "HIGH" or kill_heat_volatility >= 9:
        recommendation = "GUARD"
        reason = "high-pressure-drift-or-high-kill-heat-volatility"
    elif pressure_band == "HIGH" or kill_heat_volatility >= 5:
        recommendation = "STEADY"
        reason = "moderate-volatility-or-high-pressure"
    else:
        recommendation = "SURGE"
        reason = "low-volatility-and-stable-pressure"

    return recommendation, {
        "reason": reason,
        "killHeatVolatility": kill_heat_volatility,
        "comboChurn": combo_churn,
        "comboNet": combo_net,
        "comboConfidenceChurn": conf_churn,
        "comboConfidenceNet": conf_net,
        "pressureBand": pressure_band,
        "driftRisk": drift_risk,
        "offlineOnly": True,
    }

def combo_confidence_coach_scene_arc_from_signals(
    *,
    recommendation: str,
    pressure_band: str,
    drift_risk: str,
) -> tuple[str, dict[str, object]]:
    """Design/world-facing offline scene-arc cue from combo-confidence coach posture."""
    if recommendation == "GUARD" or drift_risk == "HIGH":
        scene_arc = "ASH"
        reason = "guardrail-or-high-drift"
    elif recommendation == "STEADY" or pressure_band == "HIGH":
        scene_arc = "IRON"
        reason = "steady-pressure-bridge"
    else:
        scene_arc = "EMBER"
        reason = "surge-low-drift-push"

    return scene_arc, {
        "reason": reason,
        "recommendation": recommendation,
        "pressureBand": pressure_band,
        "driftRisk": drift_risk,
        "offlineOnly": True,
    }


def combo_confidence_fx_accent_from_signals(
    *,
    scene_arc: str,
    fallback_narrative_signals: dict[str, object],
    prior_json_path: Path | None = None,
) -> tuple[str, dict[str, object]]:
    """Offline combat/vfx accent token for combo-confidence coaching readability."""
    volatility_regime = str(fallback_narrative_signals.get("volatilityRegime", "CALM") or "CALM").upper()
    recommendation = str(fallback_narrative_signals.get("recommendation", "STEADY") or "STEADY").upper()

    if scene_arc == "ASH":
        accent = "SMOKE"
        reason = "ash-scene-arc-default-smoke-accent"
    elif scene_arc == "IRON":
        accent = "STEEL"
        reason = "iron-scene-arc-default-steel-accent"
    else:
        accent = "EMBER"
        reason = "ember-scene-arc-default-ember-accent"

    if volatility_regime == "SPIKE" and recommendation == "GUARD":
        accent = "SMOKE"
        reason = "spike-guard-keeps-smoke-accent"
    elif volatility_regime == "SWING" and accent == "EMBER":
        accent = "STEEL"
        reason = "swing-regime-tempers-ember-to-steel"

    prior_accent = ""
    if prior_json_path and prior_json_path.exists():
        try:
            prior_payload = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_accent = str(prior_payload.get("comboConfidenceFxAccent", "") or "").upper()
        except Exception:
            prior_accent = ""

    hysteresis_applied = False
    if volatility_regime == "SWING" and prior_accent in {"STEEL", "EMBER"} and accent in {"STEEL", "EMBER"} and prior_accent != accent:
        accent = prior_accent
        reason = f"swing-hysteresis-holds-prior-{prior_accent.lower()}"
        hysteresis_applied = True

    return accent, {
        "reason": reason,
        "sceneArc": scene_arc,
        "volatilityRegime": volatility_regime,
        "recommendation": recommendation,
        "priorAccent": prior_accent or "NONE",
        "hysteresisApplied": hysteresis_applied,
        "offlineOnly": True,
    }


def combo_confidence_coach_recommendation_streak_from_prior(
    *,
    current_recommendation: str,
    prior_json_path: Path,
) -> tuple[int, int, dict[str, object]]:
    """Track recommendation streak + drift delta for offline fallback narrative pacing."""
    prior_recommendation = ""
    prior_streak = 0

    if prior_json_path.exists():
        try:
            prior_payload = json.loads(prior_json_path.read_text(encoding="utf-8"))
            prior_recommendation = str(prior_payload.get("comboConfidenceCoachRecommendation", "") or "").upper()
            prior_streak = int(prior_payload.get("comboConfidenceCoachRecommendationStreak", 0) or 0)
        except Exception:
            prior_recommendation = ""
            prior_streak = 0

    if prior_recommendation == current_recommendation and prior_streak > 0:
        current_streak = prior_streak + 1
        reason = "same-recommendation-streak-extended"
    else:
        current_streak = 1
        reason = "recommendation-shift-reset"

    streak_drift = current_streak - prior_streak
    signals = {
        "reason": reason,
        "currentRecommendation": current_recommendation,
        "priorRecommendation": prior_recommendation or "NONE",
        "priorStreak": prior_streak,
        "currentStreak": current_streak,
        "streakDrift": streak_drift,
        "offlineOnly": True,
    }
    return current_streak, streak_drift, signals


def combo_confidence_coach_fallback_narrative_from_signals(
    *,
    recommendation: str,
    recommendation_streak: int,
    recommendation_streak_drift: int,
    recommendation_signals: dict[str, object],
) -> tuple[str, dict[str, object]]:
    """Offline fallback narrative line tied to recommendation streak drift + volatility regime."""
    kill_heat_volatility = int(recommendation_signals.get("killHeatVolatility", 0) or 0)
    if kill_heat_volatility >= 9:
        volatility_regime = "SPIKE"
    elif kill_heat_volatility >= 5:
        volatility_regime = "SWING"
    else:
        volatility_regime = "CALM"

    if recommendation == "GUARD" or volatility_regime == "SPIKE":
        line = "LOCK YOUR BREATH. BANK SAFE HITS."
        reason = "guard-or-spike-volatility-regime"
    elif recommendation == "STEADY" or volatility_regime == "SWING":
        line = "HOLD THE DRUMBEAT. CUT WHEN IT OPENS."
        reason = "steady-with-swing-volatility-regime"
    else:
        line = "KEEP PRESSURE CLEAN. CASH THE HEAT."
        reason = "surge-with-calm-volatility-regime"

    if recommendation_streak >= 3 and recommendation_streak_drift > 0:
        line = f"{line} SAME CALL x{recommendation_streak}."
        reason = "streak-rising-lock-in-reminder"
    elif recommendation_streak_drift < 0:
        line = "NEW READ. RESET THE RHYTHM FIRST."
        reason = "streak-drop-reset-reminder"

    return line, {
        "reason": reason,
        "recommendation": recommendation,
        "recommendationStreak": recommendation_streak,
        "recommendationStreakDrift": recommendation_streak_drift,
        "volatilityRegime": volatility_regime,
        "killHeatVolatility": kill_heat_volatility,
        "offlineOnly": True,
    }




def combo_confidence_coach_copy_swap_recommendation_from_signals(
    *,
    prsmc_family: dict[str, object],
    prsmc_family_trend_signals: dict[str, object],
    lane_cadence_miss_risk_signals: dict[str, object],
    coach_recommendation: str,
) -> tuple[str, dict[str, object]]:
    """Offline-only cadence-reactive coach-copy swap recommendation from PRSMC churn + lane miss risk."""
    churn = int(prsmc_family.get("churn", 0) or 0)
    net = int(prsmc_family.get("net", 0) or 0)
    trend = str(prsmc_family_trend_signals.get("trend", "FLAT") or "FLAT").upper()
    miss_risk = str(lane_cadence_miss_risk_signals.get("risk", "MID") or "MID").upper()
    cadence_status = str(lane_cadence_miss_risk_signals.get("status", "GAP") or "GAP").upper()

    if miss_risk == "HIGH" or (trend == "UP" and churn >= 3):
        rec = "SWAP_NOW"
        reason = "high-miss-risk-or-rising-prsmc-churn"
    elif miss_risk == "MID" or churn >= 2 or abs(net) >= 2:
        rec = "ARM_SWAP"
        reason = "mid-risk-or-prsmc-imbalance"
    else:
        rec = "HOLD_COPY"
        reason = "stable-prsmc-and-low-miss-risk"

    if coach_recommendation == "GUARD" and rec == "HOLD_COPY":
        rec = "ARM_SWAP"
        reason = "guard-posture-biases-preemptive-swap-arm"

    return rec, {
        "reason": reason,
        "prsmcChurn": churn,
        "prsmcNet": net,
        "prsmcTrend": trend,
        "laneCadenceMissRisk": miss_risk,
        "laneCadenceStatus": cadence_status,
        "coachRecommendation": coach_recommendation,
        "offlineOnly": True,
    }


def main() -> int:
    args = parse_args()
    root = args.repo_root.resolve()
    now_dt = datetime.now(timezone.utc)
    now = now_dt.isoformat().replace("+00:00", "Z")

    revs = git(root, "rev-list", f"--since={args.since_days}.days", f"--max-count={args.max_commits}", "HEAD")
    commits = [c for c in revs.splitlines() if c.strip()]
    rows = [commit_stats(root, c) for c in commits]
    touched = [r for r in rows if r["touchedPortalPrompt"]]
    lane_bucket_age = lane_bucket_age_hours(rows, now_utc=now_dt)
    lane_bucket_age_delta, lane_bucket_age_drift_signals = lane_bucket_age_drift(
        current_max_age_hours=int(lane_bucket_age["maxAgeHours"]),
        prior_json_path=args.out_json,
    )
    lane_cadence_recency, lane_cadence_recency_signals = lane_cadence_recency_from_age_drift(
        lane_bucket_age=lane_bucket_age,
        lane_bucket_age_delta=lane_bucket_age_delta,
    )
    lane_cadence_miss_risk_token, lane_cadence_miss_risk_signals = lane_cadence_miss_risk(
        lane_bucket_age=lane_bucket_age,
        lane_bucket_age_delta=lane_bucket_age_delta,
    )
    lane_bucket_age_compact_alias, lane_bucket_age_compact_alias_signals = lane_bucket_age_alias(
        lane_bucket_age=lane_bucket_age,
    )
    lane_cadence_miss_risk_alias_token, lane_cadence_miss_risk_alias_signals = lane_cadence_miss_risk_alias(
        lane_cadence_miss_risk_signals=lane_cadence_miss_risk_signals,
    )
    lane_priority_hysteresis_floor_recommendation, lane_priority_hysteresis_floor_recommendation_signals = lane_priority_hysteresis_floor_recommendation_from_lcmr_streak(
        lane_cadence_miss_risk_signals=lane_cadence_miss_risk_signals,
        prior_json_path=args.out_json,
    )
    lane_priority_hysteresis_floor_recommendation_alias, lane_priority_hysteresis_floor_recommendation_alias_signals = resolve_lane_priority_hysteresis_floor_recommendation_alias(
        recommendation_token=lane_priority_hysteresis_floor_recommendation,
    )
    lane_priority_recommendation, lane_priority_recommendation_signals = lane_priority_recommendation_from_bucket_age_momentum(
        age_hours={
            "systems/ops": int(lane_bucket_age["ageHours"].get("systems/ops", 999) or 999),
            "design/world": int(lane_bucket_age["ageHours"].get("design/world", 999) or 999),
            "combat/vfx": int(lane_bucket_age["ageHours"].get("combat/vfx", 999) or 999),
        },
        prior_json_path=args.out_json,
    )
    lane_priority_recommendation_compact_alias, lane_priority_recommendation_compact_alias_signals = resolve_lane_priority_recommendation_compact_alias(
        lane_priority_recommendation,
    )
    lane_priority_recommendation_confidence_level, lane_priority_recommendation_confidence_signals = lane_priority_recommendation_confidence(
        lane_priority_recommendation=lane_priority_recommendation,
        lane_priority_recommendation_signals=lane_priority_recommendation_signals,
    )
    lane_priority_hysteresis_compact_alias, lane_priority_hysteresis_compact_alias_signals = resolve_lane_priority_hysteresis_alias(
        hysteresis_applied=bool(lane_priority_recommendation_signals.get("hysteresisApplied", False)),
    )
    lane_priority_hysteresis_rail, lane_priority_hysteresis_rail_signals = resolve_lane_priority_hysteresis_rail(
        confidence=lane_priority_recommendation_confidence_level,
        hysteresis_applied=bool(lane_priority_recommendation_signals.get("hysteresisApplied", False)),
        score_gap=int(lane_priority_recommendation_signals.get("hysteresisScoreGap", 0) or 0),
        threshold=int(lane_priority_recommendation_signals.get("hysteresisThreshold", 0) or 0),
    )
    lane_priority_hysteresis_threshold_tuning, lane_priority_hysteresis_threshold_tuning_signals = resolve_lane_priority_hysteresis_threshold_tuning(
        lane_priority_recommendation_signals=lane_priority_recommendation_signals,
        prior_json_path=args.out_json,
    )
    lane_priority_hysteresis_threshold_compact_alias, lane_priority_hysteresis_threshold_compact_alias_signals = resolve_lane_priority_hysteresis_threshold_compact_alias(
        recommendation=lane_priority_hysteresis_threshold_tuning,
    )
    lane_priority_hysteresis_window_band, lane_priority_hysteresis_window_band_signals = resolve_lane_priority_hysteresis_window_band(
        tuning_signals=lane_priority_hysteresis_threshold_tuning_signals,
    )
    lane_priority_hysteresis_window_delta_token, lane_priority_hysteresis_window_delta, lane_priority_hysteresis_window_delta_signals = resolve_lane_priority_hysteresis_window_delta(
        current_band=str(lane_priority_hysteresis_window_band_signals.get("band", "BASE")),
        prior_json_path=args.out_json,
    )

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
    token_family_totals = token_family_coverage(token_totals)
    pulse_heat_fx_compact_budget_drift_level, pulse_heat_fx_compact_budget_drift_signals = pulse_heat_fx_compact_budget_drift(
        pulse_heat_fx_family=token_family_totals["pulseHeatFxAlias"],
        compact_net=totals["net"]["compact"],
    )
    route_glow_fx_compact_budget_drift_level, route_glow_fx_compact_budget_drift_signals = route_glow_fx_compact_budget_drift(
        route_glow_fx_family=token_family_totals["routeGlowFxAlias"],
        compact_net=totals["net"]["compact"],
    )
    route_glow_fx_conf_why_rail_mode_compact_budget_drift_level, route_glow_fx_conf_why_rail_mode_compact_budget_drift_signals = route_glow_fx_conf_why_rail_mode_compact_budget_drift(
        route_glow_fx_conf_why_rail_mode_family=token_family_totals["routeGlowFxConfidenceWhyRailMode"],
        compact_net=totals["net"]["compact"],
    )
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
    rgfxwri_why_conf_policy, rgfxwri_why_conf_policy_signals = rgfxwri_why_conf_policy_recommendation(
        drift_risk=drift_risk,
        family_totals=token_family_totals["routeGlowFxConfidenceWhyRailIntensityWhyConfidenceAlias"],
    )
    ambient_ramp_confidence_recommendation, ambient_ramp_confidence_recommendation_signals = ambient_ramp_confidence_recommendation_from_trends(
        drift_risk=drift_risk,
        ambient_ramp_confidence_family=token_family_totals["ambientRampConfidenceAlias"],
        pressure_band=pressure_band,
    )
    ambient_ramp_why_recommendation, ambient_ramp_why_recommendation_signals = ambient_ramp_why_recommendation_from_trends(
        drift_risk=drift_risk,
        ambient_ramp_why_family=token_family_totals["ambientRampWhyAlias"],
        pressure_band=pressure_band,
    )
    ambient_ramp_why_recommendation_confidence, ambient_ramp_why_recommendation_confidence_signals = ambient_ramp_why_recommendation_confidence_from_signals(
        recommendation=ambient_ramp_why_recommendation,
        recommendation_signals=ambient_ramp_why_recommendation_signals,
    )
    ambient_ramp_why_recommendation_parity, ambient_ramp_why_recommendation_parity_signals = ambient_ramp_why_recommendation_parity_summary(
        recommendation=ambient_ramp_why_recommendation,
        confidence=ambient_ramp_why_recommendation_confidence,
        recommendation_signals=ambient_ramp_why_recommendation_signals,
    )
    ambient_ramp_why_recommendation_confidence_streak, ambient_ramp_why_recommendation_confidence_streak_signals = ambient_ramp_why_recommendation_confidence_streak_from_prior(
        current_confidence=ambient_ramp_why_recommendation_confidence,
        prior_json_path=args.out_json,
    )
    ambient_ramp_why_auto_remap_plan, ambient_ramp_why_auto_remap_plan_signals, ambient_ramp_why_auto_remap_plan_candidates = ambient_ramp_why_auto_remap_plan_from_signals(
        recommendation=ambient_ramp_why_recommendation,
        confidence=ambient_ramp_why_recommendation_confidence,
        parity=ambient_ramp_why_recommendation_parity,
        recommendation_signals=ambient_ramp_why_recommendation_signals,
        confidence_streak=ambient_ramp_why_recommendation_confidence_streak,
        suppress_candidates=bool(ambient_ramp_why_recommendation_confidence_streak_signals.get("suppress", False)),
    )
    ambient_ramp_why_auto_remap_plan_compact = ambient_ramp_why_auto_remap_plan_alias(ambient_ramp_why_auto_remap_plan)
    ambient_ramp_why_auto_remap_why = ambient_ramp_why_auto_remap_rationale_short(
        selected_plan=ambient_ramp_why_auto_remap_plan,
        plan_signals=ambient_ramp_why_auto_remap_plan_signals,
    )
    ambient_ramp_why_auto_remap_plan_drift, ambient_ramp_why_auto_remap_plan_drift_signals = ambient_ramp_why_auto_remap_plan_drift_from_prior(
        current_plan=ambient_ramp_why_auto_remap_plan,
        prior_json_path=args.out_json,
    )
    ambient_ramp_why_auto_remap_plan_confidence, ambient_ramp_why_auto_remap_plan_confidence_signals = ambient_ramp_why_auto_remap_plan_confidence_from_signals(
        selected_plan=ambient_ramp_why_auto_remap_plan,
        plan_signals=ambient_ramp_why_auto_remap_plan_signals,
        plan_drift=ambient_ramp_why_auto_remap_plan_drift,
        plan_drift_signals=ambient_ramp_why_auto_remap_plan_drift_signals,
    )
    ambient_ramp_why_auto_remap_plan_confidence_drift, ambient_ramp_why_auto_remap_plan_confidence_drift_signals = ambient_ramp_why_auto_remap_plan_confidence_drift_from_prior(
        current_confidence=ambient_ramp_why_auto_remap_plan_confidence,
        prior_json_path=args.out_json,
    )
    arw_apc_flag_name = "DOTPIO_EXPERIMENT_ARW_APC_ALIAS"
    arw_apc_flag_enabled = os.environ.get(arw_apc_flag_name, "").strip().lower() in {"1", "true", "yes", "on"}
    ambient_ramp_why_auto_remap_plan_confidence_band_alias = ambient_ramp_auto_remap_confidence_band_alias(
        ambient_ramp_why_auto_remap_plan_confidence
    )
    ambient_ramp_why_auto_remap_plan_confidence_momentum_freeze_recommendation, ambient_ramp_why_auto_remap_plan_confidence_momentum_freeze_signals = ambient_ramp_auto_remap_confidence_momentum_freeze_recommendation(
        current_confidence=ambient_ramp_why_auto_remap_plan_confidence,
        confidence_drift=ambient_ramp_why_auto_remap_plan_confidence_drift,
        confidence_streak=ambient_ramp_why_recommendation_confidence_streak,
        plan_drift=ambient_ramp_why_auto_remap_plan_drift,
        plan_signals=ambient_ramp_why_auto_remap_plan_signals,
    )
    arw_momentum_flag_name = "DOTPIO_EXPERIMENT_ARW_MOMENTUM_ALIAS"
    arw_momentum_flag_enabled = os.environ.get(arw_momentum_flag_name, "").strip().lower() in {"1", "true", "yes", "on"}
    ambient_ramp_why_auto_remap_plan_confidence_momentum_alias = ambient_ramp_auto_remap_confidence_momentum_alias(
        ambient_ramp_why_auto_remap_plan_confidence_momentum_freeze_recommendation
    )
    ambient_ramp_why_auto_remap_plan_confidence_momentum_score, ambient_ramp_why_auto_remap_plan_confidence_momentum_score_signals = ambient_ramp_auto_remap_confidence_momentum_score(
        recommendation=ambient_ramp_why_auto_remap_plan_confidence_momentum_freeze_recommendation,
        confidence_drift=ambient_ramp_why_auto_remap_plan_confidence_drift,
        confidence_streak=ambient_ramp_why_recommendation_confidence_streak,
        plan_drift=ambient_ramp_why_auto_remap_plan_drift,
        plan_signals=ambient_ramp_why_auto_remap_plan_signals,
    )
    arw_momentum_arc_flag_name = "DOTPIO_EXPERIMENT_ARW_MOMENTUM_ARC"
    arw_momentum_arc_flag_enabled = os.environ.get(arw_momentum_arc_flag_name, "").strip().lower() in {"1", "true", "yes", "on"}
    ambient_ramp_why_auto_remap_momentum_arc, ambient_ramp_why_auto_remap_momentum_arc_signals = ambient_ramp_auto_remap_momentum_arc(
        recommendation=ambient_ramp_why_auto_remap_plan_confidence_momentum_freeze_recommendation,
        pressure_band=pressure_band,
        drift_risk=drift_risk,
        momentum_score=ambient_ramp_why_auto_remap_plan_confidence_momentum_score,
    )
    arw_arc_pulse_flag_name = "DOTPIO_EXPERIMENT_ARW_MOMENTUM_ARC_PULSE_ALIAS"
    arw_arc_pulse_flag_enabled = os.environ.get(arw_arc_pulse_flag_name, "").strip().lower() in {"1", "true", "yes", "on"}
    ambient_ramp_why_auto_remap_momentum_arc_pulse, ambient_ramp_why_auto_remap_momentum_arc_pulse_signals = ambient_ramp_auto_remap_momentum_arc_pulse_alias(
        ambient_ramp_why_auto_remap_momentum_arc
    )
    urgency_stack_pruning_order_recommendation, urgency_stack_pruning_order_recommendation_signals = urgency_stack_pruning_order_recommendation_from_trends(
        drift_risk=drift_risk,
        parity_compact_family=token_family_totals["routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyParityCompactAlias"],
        urgency_fx_family=token_family_totals["routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyFxAlias"],
        urgency_detailed_family=token_family_totals["routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyDetailed"],
    )
    urgency_stack_rail_recommendation, urgency_stack_rail_recommendation_signals = urgency_stack_rail_recommendation_from_trends(
        drift_risk=drift_risk,
        urgency_stack_rail_family=token_family_totals["urgencyStackRailAlias"],
        urgency_stack_tier_family=token_family_totals["urgencyStackTierAlias"],
    )
    dmg_glyph_shape_remap_recommendation, dmg_glyph_shape_remap_recommendation_signals = damage_glyph_shape_remap_recommendation_from_trends(
        drift_risk=drift_risk,
        dmg_glyph_family=token_family_totals["dmgGlyphAlias"],
        urgency_stack_rail_family=token_family_totals["urgencyStackRailAlias"],
    )
    dmg_glyph_fx_remap_recommendation, dmg_glyph_fx_remap_recommendation_signals = damage_glyph_fx_remap_recommendation_from_trends(
        drift_risk=drift_risk,
        dmg_glyph_fx_live_family=token_family_totals["dmgGlyphFxLiveAlias"],
        dmg_glyph_family=token_family_totals["dmgGlyphAlias"],
    )
    dmg_glyph_fx_remap_confidence, dmg_glyph_fx_remap_confidence_signals = damage_glyph_fx_remap_confidence_from_signals(
        drift_risk=drift_risk,
        dmg_glyph_fx_remap_recommendation_signals=dmg_glyph_fx_remap_recommendation_signals,
    )
    combo_window_retune_recommendation, combo_window_retune_recommendation_signals = combo_window_retune_recommendation_from_trends(
        combo_family=token_family_totals["dmgComboAlias"],
        pressure_band=pressure_band,
        drift_risk=drift_risk,
        lane_cadence_recency=lane_cadence_recency,
    )
    combo_window_retune_confidence, combo_window_retune_confidence_signals = combo_window_retune_confidence_from_signals(
        recommendation=combo_window_retune_recommendation,
        recommendation_signals=combo_window_retune_recommendation_signals,
    )
    combo_chain_narrative_coach_line, combo_chain_narrative_coach_line_signals = combo_chain_narrative_coach_line_from_signals(
        combo_window_retune_recommendation=combo_window_retune_recommendation,
        combo_window_retune_confidence=combo_window_retune_confidence,
        combo_window_retune_recommendation_signals=combo_window_retune_recommendation_signals,
    )
    combo_confidence_coach_recommendation, combo_confidence_coach_recommendation_signals = combo_confidence_coach_recommendation_from_signals(
        combo_family=token_family_totals["dmgComboAlias"],
        combo_confidence_family=token_family_totals["dmgComboConfidenceAlias"],
        pressure_band=pressure_band,
        drift_risk=drift_risk,
    )
    combo_confidence_coach_recommendation_streak, combo_confidence_coach_recommendation_streak_drift, combo_confidence_coach_recommendation_streak_signals = combo_confidence_coach_recommendation_streak_from_prior(
        current_recommendation=combo_confidence_coach_recommendation,
        prior_json_path=args.out_json,
    )
    combo_confidence_coach_fallback_narrative, combo_confidence_coach_fallback_narrative_signals = combo_confidence_coach_fallback_narrative_from_signals(
        recommendation=combo_confidence_coach_recommendation,
        recommendation_streak=combo_confidence_coach_recommendation_streak,
        recommendation_streak_drift=combo_confidence_coach_recommendation_streak_drift,
        recommendation_signals=combo_confidence_coach_recommendation_signals,
    )
    combo_confidence_coach_scene_arc, combo_confidence_coach_scene_arc_signals = combo_confidence_coach_scene_arc_from_signals(
        recommendation=combo_confidence_coach_recommendation,
        pressure_band=pressure_band,
        drift_risk=drift_risk,
    )
    combo_confidence_fx_accent, combo_confidence_fx_accent_signals = combo_confidence_fx_accent_from_signals(
        scene_arc=combo_confidence_coach_scene_arc,
        fallback_narrative_signals=combo_confidence_coach_fallback_narrative_signals,
        prior_json_path=args.out_json,
    )
    dmg_combo_conf_fx_accent_alias_flag_name = "DOTPIO_EXPERIMENT_DMG_COMBO_CONF_FX_ACCENT_ALIAS"
    dmg_combo_conf_fx_accent_alias_flag_enabled = os.environ.get(dmg_combo_conf_fx_accent_alias_flag_name, "").strip().lower() in {"1", "true", "yes", "on"}
    dmg_combo_conf_fx_accent_alias = f"DCCFX:{combo_confidence_fx_accent[:1]}"
    dmg_combo_conf_coach_alias_flag_name = "DOTPIO_EXPERIMENT_DMG_COMBO_CONF_COACH_ALIAS"
    dmg_combo_conf_coach_alias_flag_enabled = os.environ.get(dmg_combo_conf_coach_alias_flag_name, "").strip().lower() in {"1", "true", "yes", "on"}
    dmg_combo_conf_coach_alias = f"DCCR:{combo_confidence_coach_recommendation[:1]}"
    dmg_combo_conf_coach_scene_arc_alias_flag_name = "DOTPIO_EXPERIMENT_DMG_COMBO_CONF_COACH_SCENE_ARC_ALIAS"
    dmg_combo_conf_coach_scene_arc_alias_flag_enabled = os.environ.get(dmg_combo_conf_coach_scene_arc_alias_flag_name, "").strip().lower() in {"1", "true", "yes", "on"}
    dmg_combo_conf_coach_scene_arc_alias = f"DCCSA:{combo_confidence_coach_scene_arc[:1]}"
    dmg_combo_conf_coach_copy_swap_alias_flag_name = "DOTPIO_EXPERIMENT_DMG_COMBO_CONF_COACH_COPY_SWAP_ALIAS"
    dmg_combo_conf_coach_copy_swap_alias_flag_enabled = os.environ.get(dmg_combo_conf_coach_copy_swap_alias_flag_name, "").strip().lower() in {"1", "true", "yes", "on"}
    dmg_combo_retune_alias_flag_name = "DOTPIO_EXPERIMENT_DMG_COMBO_RETUNE_ALIAS"
    dmg_combo_retune_alias_flag_enabled = os.environ.get(dmg_combo_retune_alias_flag_name, "").strip().lower() in {"1", "true", "yes", "on"}
    dmg_combo_retune_alias = f"DCR:{combo_window_retune_recommendation[:1]}"
    dmg_combo_retune_conf_alias_flag_name = "DOTPIO_EXPERIMENT_DMG_COMBO_RETUNE_CONF_ALIAS"
    dmg_combo_retune_conf_alias_flag_enabled = os.environ.get(dmg_combo_retune_conf_alias_flag_name, "").strip().lower() in {"1", "true", "yes", "on"}
    dmg_combo_retune_conf_alias = f"DCRC:{combo_window_retune_confidence[:1]}"
    dmgnum_life_trend_fx_pulse_remap_recommendation, dmgnum_life_trend_fx_pulse_remap_recommendation_signals = dmgnum_life_trend_fx_pulse_remap_recommendation_from_trends(
        drift_risk=drift_risk,
        pressure_band=pressure_band,
        lane_cadence_recency=lane_cadence_recency,
        pulse_family=token_family_totals["dmgnumLifeTrendFxPulseAlias"],
        pulse_confidence_family=token_family_totals["dmgnumLifeTrendFxPulseConfidenceAlias"],
    )
    pulse_remap_momentum_recommendation, pulse_remap_momentum_recommendation_signals = pulse_remap_momentum_from_trends(
        recommendation=dmgnum_life_trend_fx_pulse_remap_recommendation,
        recommendation_signals=dmgnum_life_trend_fx_pulse_remap_recommendation_signals,
        remap_plan_family=token_family_totals["dmgnumLifeTrendFxPulseRemapPlanAlias"],
    )
    pulse_remap_momentum_alias = resolve_pulse_remap_momentum_alias(pulse_remap_momentum_recommendation)
    pulse_remap_momentum_drift, pulse_remap_momentum_drift_signals = pulse_remap_momentum_drift_from_prior(
        current_momentum=pulse_remap_momentum_recommendation,
        prior_json_path=args.out_json,
    )
    pulse_remap_momentum_suppression, pulse_remap_momentum_suppression_signals = pulse_remap_momentum_streak_suppression_from_prior(
        current_momentum=pulse_remap_momentum_recommendation,
        prior_json_path=args.out_json,
    )
    pulse_remap_momentum_suppression_alias = resolve_pulse_remap_momentum_suppression_alias(pulse_remap_momentum_suppression)
    pulse_remap_momentum_alias_flag_name = "DOTPIO_EXPERIMENT_PULSE_REMAP_MOMENTUM_ALIAS"
    pulse_remap_momentum_alias_flag_enabled = os.environ.get(pulse_remap_momentum_alias_flag_name, "").strip().lower() in {"1", "true", "yes", "on"}
    pulse_remap_momentum_suppression_alias_flag_name = "DOTPIO_EXPERIMENT_PULSE_REMAP_MOMENTUM_SUPPRESSION_ALIAS"
    pulse_remap_momentum_suppression_alias_flag_enabled = os.environ.get(pulse_remap_momentum_suppression_alias_flag_name, "").strip().lower() in {"1", "true", "yes", "on"}
    pulse_remap_suppression_family_trend_drift, pulse_remap_suppression_family_trend_signals = pulse_remap_suppression_family_trend_from_prior(
        current_family_totals=token_family_totals["pulseRemapMomentumSuppressionAlias"],
        prior_json_path=args.out_json,
    )
    pulse_remap_suppression_plan_family_trend_drift, pulse_remap_suppression_plan_family_trend_signals = pulse_remap_suppression_plan_family_trend_from_prior(
        current_family_totals=token_family_totals["pulseRemapSuppressionPlanAlias"],
        prior_json_path=args.out_json,
    )
    pulse_remap_scene_microline_cadence_family_trend_drift, pulse_remap_scene_microline_cadence_family_trend_signals = pulse_remap_scene_microline_cadence_family_trend_from_prior(
        current_family_totals=token_family_totals["pulseRemapSceneMicrolineCadenceAlias"],
        prior_json_path=args.out_json,
    )
    combo_confidence_coach_copy_swap_recommendation, combo_confidence_coach_copy_swap_recommendation_signals = combo_confidence_coach_copy_swap_recommendation_from_signals(
        prsmc_family=token_family_totals["pulseRemapSceneMicrolineCadenceAlias"],
        prsmc_family_trend_signals=pulse_remap_scene_microline_cadence_family_trend_signals,
        lane_cadence_miss_risk_signals=lane_cadence_miss_risk_signals,
        coach_recommendation=combo_confidence_coach_recommendation,
    )
    dmg_combo_conf_coach_copy_swap_alias = f"DCCSR:{combo_confidence_coach_copy_swap_recommendation[:1]}"
    combo_confidence_fx_accent_family_trend_drift, combo_confidence_fx_accent_family_trend_signals = combo_confidence_fx_accent_family_trend_from_prior(
        current_family_totals=token_family_totals["dmgComboConfidenceFxAccentAlias"],
        prior_json_path=args.out_json,
        volatility_regime=str(combo_confidence_coach_fallback_narrative_signals.get("volatilityRegime", "CALM") or "CALM"),
    )
    combo_confidence_coach_copy_swap_recommendation_family_trend_drift, combo_confidence_coach_copy_swap_recommendation_family_trend_signals = combo_confidence_coach_copy_swap_recommendation_family_trend_from_prior(
        current_family_totals=token_family_totals["dmgComboConfidenceCoachCopySwapRecommendationAlias"],
        prior_json_path=args.out_json,
        prior_family_key="dmgComboConfidenceCoachCopySwapRecommendationAlias",
    )
    combo_confidence_coach_copy_swap_trend_alias_family_trend_drift, combo_confidence_coach_copy_swap_trend_alias_family_trend_signals = combo_confidence_coach_copy_swap_recommendation_family_trend_from_prior(
        current_family_totals=token_family_totals["dmgComboConfidenceCoachCopySwapTrendAlias"],
        prior_json_path=args.out_json,
        prior_family_key="dmgComboConfidenceCoachCopySwapTrendAlias",
    )
    dmg_combo_conf_coach_copy_swap_trend_alias_flag_name = "DOTPIO_EXPERIMENT_DMG_COMBO_CONF_COACH_COPY_SWAP_TREND_ALIAS"
    dmg_combo_conf_coach_copy_swap_trend_alias_flag_enabled = os.environ.get(dmg_combo_conf_coach_copy_swap_trend_alias_flag_name, "").strip().lower() in {"1", "true", "yes", "on"}
    copy_swap_trend = str(combo_confidence_coach_copy_swap_recommendation_family_trend_signals.get("trend", "FLAT")).upper()
    combo_confidence_fx_accent_trend = str(combo_confidence_fx_accent_family_trend_signals.get("trend", "FLAT")).upper()
    copy_swap_trend_alias_map = {"UP": "U", "DOWN": "D", "FLAT": "F"}
    dmg_combo_conf_coach_copy_swap_trend_alias = f"DCCST:{copy_swap_trend_alias_map.get(copy_swap_trend, 'F')}"
    dmg_combo_conf_fx_accent_trend_alias_flag_name = "DOTPIO_EXPERIMENT_DMG_COMBO_CONF_FX_ACCENT_TREND_ALIAS"
    dmg_combo_conf_fx_accent_trend_alias_flag_enabled = os.environ.get(dmg_combo_conf_fx_accent_trend_alias_flag_name, "").strip().lower() in {"1", "true", "yes", "on"}
    dmg_combo_conf_fx_accent_trend_alias = f"DCCFXT:{copy_swap_trend_alias_map.get(combo_confidence_fx_accent_trend, 'F')}"
    dmg_combo_conf_fx_accent_trend_hys_alias_flag_name = "DOTPIO_EXPERIMENT_DMG_COMBO_CONF_FX_ACCENT_TREND_HYS_ALIAS"
    dmg_combo_conf_fx_accent_trend_hys_alias_flag_enabled = os.environ.get(dmg_combo_conf_fx_accent_trend_hys_alias_flag_name, "").strip().lower() in {"1", "true", "yes", "on"}
    trend_hys_rec_alias_map = {"HOLD": "H", "ALLOW": "A"}
    trend_hys_conf_alias_map = {"LOW": "L", "MID": "M", "HIGH": "H"}
    dmg_combo_conf_fx_accent_trend_hys_alias = (
        f"DCCFXH:{trend_hys_rec_alias_map.get(combo_confidence_fx_accent_family_trend_signals['trendHysteresisRecommendation'], 'H')}"
        f"{trend_hys_conf_alias_map.get(combo_confidence_fx_accent_family_trend_signals['trendHysteresisConfidence'], 'M')}"
    )
    dmg_combo_conf_fx_accent_volatility_alias_flag_name = "DOTPIO_EXPERIMENT_DMG_COMBO_CONF_FX_ACCENT_VOLATILITY_ALIAS"
    dmg_combo_conf_fx_accent_volatility_alias_flag_enabled = os.environ.get(dmg_combo_conf_fx_accent_volatility_alias_flag_name, "").strip().lower() in {"1", "true", "yes", "on"}
    volatility_alias_map = {"CALM": "C", "SWING": "S", "SPIKE": "P"}
    dmg_combo_conf_fx_accent_volatility_alias = f"DCCFXV:{volatility_alias_map.get(str(combo_confidence_fx_accent_signals.get('volatilityRegime', 'CALM')).upper(), 'C')}"
    pulse_remap_scene_microline_style_policy_family_trend_drift, pulse_remap_scene_microline_style_policy_family_trend_signals = pulse_remap_scene_microline_style_policy_family_trend_from_prior(
        current_family_totals=token_family_totals["pulseRemapSceneMicrolineStylePolicyAlias"],
        prior_json_path=args.out_json,
    )
    pulse_remap_scene_fx_glint_family_trend_drift, pulse_remap_scene_fx_glint_family_trend_signals = pulse_remap_scene_fx_glint_family_trend_from_prior(
        current_family_totals=token_family_totals["pulseRemapSceneFxGlintAlias"],
        prior_json_path=args.out_json,
    )
    pulse_remap_scene_copy_palette_recommendation_family_trend_drift, pulse_remap_scene_copy_palette_recommendation_family_trend_signals = pulse_remap_scene_copy_palette_recommendation_family_trend_from_prior(
        current_family_totals=token_family_totals["pulseRemapSceneCopyPaletteRecommendationAlias"],
        prior_json_path=args.out_json,
    )
    lane_priority_hysteresis_floor_family_trend_drift, lane_priority_hysteresis_floor_family_trend_signals = lane_priority_hysteresis_floor_family_trend_from_prior(
        current_family_totals=token_family_totals["lanePriorityHysteresisFloorRecommendationAlias"],
        prior_json_path=args.out_json,
    )
    lane_priority_hysteresis_floor_family_trend_alias_flag_name = "DOTPIO_EXPERIMENT_LANE_PRIORITY_HYSTERESIS_FLOOR_FAMILY_TREND_ALIAS"
    lane_priority_hysteresis_floor_family_trend_alias_flag_enabled = os.environ.get(lane_priority_hysteresis_floor_family_trend_alias_flag_name, "").strip().lower() in {"1", "true", "yes", "on"}
    lane_priority_hysteresis_floor_family_trend_alias_map = {"UP": "U", "FLAT": "F", "DOWN": "D"}
    lane_priority_hysteresis_floor_family_trend_alias = (
        f"LPR HF T:{lane_priority_hysteresis_floor_family_trend_alias_map.get(str(lane_priority_hysteresis_floor_family_trend_signals.get('trend', 'FLAT')).upper(), 'F')}"
    )
    lane_priority_recommendation_confidence_level, lane_priority_recommendation_confidence_guard_signals = lane_priority_recommendation_confidence_guard(
        confidence=lane_priority_recommendation_confidence_level,
        floor_family_trend_signals=lane_priority_hysteresis_floor_family_trend_signals,
        lane_priority_hysteresis_threshold_tuning_signals=lane_priority_hysteresis_threshold_tuning_signals,
        prior_json_path=args.out_json,
    )
    lane_priority_recommendation_confidence_guard_alias, lane_priority_recommendation_confidence_guard_alias_signals = resolve_lane_priority_recommendation_confidence_guard_alias(
        guard_signals=lane_priority_recommendation_confidence_guard_signals,
    )
    lane_priority_recommendation_confidence_guard_threshold, lane_priority_recommendation_confidence_guard_threshold_signals = lane_priority_recommendation_confidence_guard_threshold_token(
        guard_signals=lane_priority_recommendation_confidence_guard_signals,
    )
    lane_priority_recommendation_confidence_guard_persistence_coach_token, lane_priority_recommendation_confidence_guard_persistence_coach_signals = lane_priority_recommendation_confidence_guard_persistence_coach(
        guard_signals=lane_priority_recommendation_confidence_guard_signals,
        prior_json_path=args.out_json,
    )
    lane_priority_recommendation_confidence_guard_persistence_coach_alias, lane_priority_recommendation_confidence_guard_persistence_coach_alias_signals = resolve_lane_priority_recommendation_confidence_guard_persistence_coach_alias(
        coach_token=lane_priority_recommendation_confidence_guard_persistence_coach_token,
    )
    lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_token, lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_signals = lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack(
        coach_signals=lane_priority_recommendation_confidence_guard_persistence_coach_signals,
        guard_signals=lane_priority_recommendation_confidence_guard_signals,
        prior_json_path=args.out_json,
    )
    lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_alias, lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_alias_signals = resolve_lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_alias(
        pack_token=lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_token,
    )
    lane_priority_recommendation_confidence_guard_persistence_coach_copy_narrative, lane_priority_recommendation_confidence_guard_persistence_coach_copy_narrative_signals = lane_priority_recommendation_confidence_guard_persistence_coach_copy_narrative_line(
        pack_signals=lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_signals,
        guard_signals=lane_priority_recommendation_confidence_guard_signals,
    )
    lane_priority_recommendation_confidence_guard_persistence_coach_copy_alias, lane_priority_recommendation_confidence_guard_persistence_coach_copy_alias_signals = resolve_lane_priority_recommendation_confidence_guard_persistence_coach_copy_alias(
        coach_copy_token=lane_priority_recommendation_confidence_guard_persistence_coach_copy_narrative,
    )
    lane_priority_recommendation_confidence_guard_persistence_coach_copy_why, lane_priority_recommendation_confidence_guard_persistence_coach_copy_why_signals = lane_priority_recommendation_confidence_guard_persistence_coach_copy_why_token(
        coach_copy_signals=lane_priority_recommendation_confidence_guard_persistence_coach_copy_narrative_signals,
    )
    pulse_remap_suppression_escalation_plan, pulse_remap_suppression_escalation_plan_signals = pulse_remap_suppression_escalation_plan_from_signals(
        suppression=pulse_remap_momentum_suppression,
        suppression_signals=pulse_remap_momentum_suppression_signals,
        momentum=pulse_remap_momentum_recommendation,
        drift_risk=drift_risk,
        lane_cadence_recency=lane_cadence_recency,
    )
    pulse_remap_suppression_scene_flavor, pulse_remap_suppression_scene_flavor_signals = pulse_remap_scene_flavor_from_signals(
        suppression_plan=pulse_remap_suppression_escalation_plan,
        suppression_plan_signals=pulse_remap_suppression_escalation_plan_signals,
        pressure_band=pressure_band,
    )
    if pulse_remap_suppression_escalation_plan == "LOCK" or drift_risk == "HIGH":
        pulse_remap_scene_confidence = "HIGH"
        pulse_remap_scene_confidence_reason = "lock-or-high-drift-risk"
    elif pulse_remap_suppression_escalation_plan == "ARM" or pressure_band == "RAISE":
        pulse_remap_scene_confidence = "MED"
        pulse_remap_scene_confidence_reason = "arm-or-raise-pressure"
    else:
        pulse_remap_scene_confidence = "LOW"
        pulse_remap_scene_confidence_reason = "hold-without-elevated-drift"
    pulse_remap_scene_confidence_signals = {
        "suppressionPlan": pulse_remap_suppression_escalation_plan,
        "driftRisk": drift_risk,
        "pressureBand": pressure_band,
        "reason": pulse_remap_scene_confidence_reason,
        "offlineOnly": True,
    }
    pulse_remap_suppression_scene_microline, pulse_remap_suppression_scene_microline_signals = pulse_remap_scene_microline_from_signals(
        suppression_plan=pulse_remap_suppression_escalation_plan,
        scene_flavor=pulse_remap_suppression_scene_flavor,
        scene_confidence=pulse_remap_scene_confidence,
        lane_cadence_recency=lane_cadence_recency,
        suppression_plan_family_trend_signals=pulse_remap_suppression_plan_family_trend_signals,
    )
    pulse_remap_scene_microline_variant_pack, pulse_remap_scene_microline_variant_pack_signals = pulse_remap_scene_microline_variant_pack_from_signals(
        suppression_plan=pulse_remap_suppression_escalation_plan,
        scene_flavor=pulse_remap_suppression_scene_flavor,
        scene_confidence=pulse_remap_scene_confidence,
        lane_cadence_recency=lane_cadence_recency,
        suppression_plan_family_trend_signals=pulse_remap_suppression_plan_family_trend_signals,
    )
    pulse_remap_scene_microline_style_diversification_policy, pulse_remap_scene_microline_style_diversification_policy_signals = pulse_remap_scene_microline_style_diversification_policy_from_signals(
        suppression_plan=pulse_remap_suppression_escalation_plan,
        scene_confidence=pulse_remap_scene_confidence,
        lane_cadence_recency=lane_cadence_recency,
        suppression_plan_family_trend_signals=pulse_remap_suppression_plan_family_trend_signals,
    )
    pulse_remap_scene_microline_style_policy_smoothed, pulse_remap_scene_microline_style_policy_smoothed_signals = pulse_remap_scene_microline_style_policy_smoothed_from_prior(
        policy=pulse_remap_scene_microline_style_diversification_policy,
        policy_signals=pulse_remap_scene_microline_style_diversification_policy_signals,
        prior_json_path=args.out_json,
    )
    pulse_remap_scene_microline_style_policy_posture_hook, pulse_remap_scene_microline_style_policy_posture_hook_signals = pulse_remap_scene_microline_style_policy_posture_hook_from_signals(
        smoothed_policy=pulse_remap_scene_microline_style_policy_smoothed,
        style_policy_family_trend_signals=pulse_remap_scene_microline_style_policy_family_trend_signals,
        lane_cadence_recency=lane_cadence_recency,
    )
    pulse_remap_scene_microline_style_policy_alias = resolve_pulse_remap_scene_microline_style_policy_alias(
        pulse_remap_scene_microline_style_diversification_policy
    )
    pulse_remap_scene_microline_style_policy_alias_flag_name = "DOTPIO_EXPERIMENT_PULSE_REMAP_SCENE_MICROLINE_STYLE_POLICY_ALIAS"
    pulse_remap_scene_microline_style_policy_alias_flag_enabled = os.environ.get(
        pulse_remap_scene_microline_style_policy_alias_flag_name,
        "",
    ).strip().lower() in {"1", "true", "yes", "on"}
    pulse_remap_scene_microline_style_posture_alias = resolve_pulse_remap_scene_microline_style_posture_alias(
        pulse_remap_scene_microline_style_policy_posture_hook
    )
    pulse_remap_scene_microline_style_posture_alias_flag_name = "DOTPIO_EXPERIMENT_PULSE_REMAP_SCENE_MICROLINE_STYLE_POSTURE_ALIAS"
    pulse_remap_scene_microline_style_posture_alias_flag_enabled = os.environ.get(
        pulse_remap_scene_microline_style_posture_alias_flag_name,
        "",
    ).strip().lower() in {"1", "true", "yes", "on"}
    pulse_remap_scene_microline_cadence, pulse_remap_scene_microline_cadence_signals = pulse_remap_scene_microline_cadence_from_signals(
        suppression_plan=pulse_remap_suppression_escalation_plan,
        scene_confidence=pulse_remap_scene_confidence,
        lane_cadence_recency=lane_cadence_recency,
        suppression_plan_family_trend_signals=pulse_remap_suppression_plan_family_trend_signals,
    )
    pulse_remap_scene_microline_cadence_alias = resolve_pulse_remap_scene_microline_cadence_alias(
        pulse_remap_scene_microline_cadence
    )
    pulse_remap_scene_microline_cadence_alias_flag_name = "DOTPIO_EXPERIMENT_PULSE_REMAP_SCENE_MICROLINE_CADENCE_ALIAS"
    pulse_remap_scene_microline_cadence_alias_flag_enabled = os.environ.get(
        pulse_remap_scene_microline_cadence_alias_flag_name,
        "",
    ).strip().lower() in {"1", "true", "yes", "on"}
    pulse_remap_scene_microline_variant_pack_selection_alias = resolve_pulse_remap_scene_microline_variant_pack_selection_alias(
        pulse_remap_scene_microline_variant_pack.get("selectedMode", "ALTERNATE")
    )
    pulse_remap_scene_microline_variant_pack_selection_alias_flag_name = "DOTPIO_EXPERIMENT_PULSE_REMAP_SCENE_MICROLINE_VARIANT_PACK_SELECTION_ALIAS"
    pulse_remap_scene_microline_variant_pack_selection_alias_flag_enabled = os.environ.get(
        pulse_remap_scene_microline_variant_pack_selection_alias_flag_name,
        "",
    ).strip().lower() in {"1", "true", "yes", "on"}
    if pulse_remap_suppression_escalation_plan == "LOCK" or pulse_remap_scene_confidence == "HIGH":
        pulse_remap_suppression_posture_warning = "ALERT"
        pulse_remap_suppression_posture_warning_reason = "lock-plan-or-high-confidence-risk"
    elif pulse_remap_suppression_escalation_plan == "ARM" or pulse_remap_momentum_suppression == "SUPPRESS":
        pulse_remap_suppression_posture_warning = "CAUTION"
        pulse_remap_suppression_posture_warning_reason = "arming-or-suppression-pressure"
    else:
        pulse_remap_suppression_posture_warning = "STEADY"
        pulse_remap_suppression_posture_warning_reason = "hold-window-steady"
    pulse_remap_suppression_posture_warning_alias = {
        "STEADY": "PRPW:S",
        "CAUTION": "PRPW:C",
        "ALERT": "PRPW:A",
    }.get(pulse_remap_suppression_posture_warning, "PRPW:C")
    pulse_remap_suppression_posture_warning_flag_name = "DOTPIO_EXPERIMENT_PULSE_REMAP_SUPPRESSION_POSTURE_WARNING"
    pulse_remap_suppression_posture_warning_flag_enabled = os.environ.get(
        pulse_remap_suppression_posture_warning_flag_name,
        "",
    ).strip().lower() in {"1", "true", "yes", "on"}
    pulse_remap_suppression_posture_warning_signals = {
        "suppressionPlan": pulse_remap_suppression_escalation_plan,
        "suppression": pulse_remap_momentum_suppression,
        "sceneConfidence": pulse_remap_scene_confidence,
        "driftRisk": drift_risk,
        "pressureBand": pressure_band,
        "reason": pulse_remap_suppression_posture_warning_reason,
        "offlineOnly": True,
    }
    pulse_remap_suppression_posture_warning_alias_signals = {
        "flagName": pulse_remap_suppression_posture_warning_flag_name,
        "flagEnabled": pulse_remap_suppression_posture_warning_flag_enabled,
    }
    pulse_remap_scene_fx_glint, pulse_remap_scene_fx_glint_signals = pulse_remap_scene_fx_glint_from_signals(
        style_posture=pulse_remap_scene_microline_style_policy_posture_hook,
        suppression_warning=pulse_remap_suppression_posture_warning,
        scene_confidence=pulse_remap_scene_confidence,
    )
    pulse_remap_scene_fx_glint_alias = resolve_pulse_remap_scene_fx_glint_alias(pulse_remap_scene_fx_glint)
    pulse_remap_scene_fx_glint_alias_flag_name = "DOTPIO_EXPERIMENT_PULSE_REMAP_SCENE_FX_GLINT_ALIAS"
    pulse_remap_scene_fx_glint_alias_flag_enabled = os.environ.get(
        pulse_remap_scene_fx_glint_alias_flag_name,
        "",
    ).strip().lower() in {"1", "true", "yes", "on"}
    pulse_remap_scene_copy_palette_recommendation, pulse_remap_scene_copy_palette_recommendation_signals = pulse_remap_scene_copy_palette_recommendation_from_signals(
        scene_flavor=pulse_remap_suppression_scene_flavor,
        scene_confidence=pulse_remap_scene_confidence,
        scene_fx_glint=pulse_remap_scene_fx_glint,
        style_posture=pulse_remap_scene_microline_style_policy_posture_hook,
    )
    pulse_remap_scene_copy_palette_recommendation_alias = resolve_pulse_remap_scene_copy_palette_recommendation_alias(
        pulse_remap_scene_copy_palette_recommendation
    )
    pulse_remap_scene_copy_palette_recommendation_alias_flag_name = "DOTPIO_EXPERIMENT_PULSE_REMAP_SCENE_COPY_PALETTE_REC_ALIAS"
    pulse_remap_scene_copy_palette_recommendation_alias_flag_enabled = os.environ.get(
        pulse_remap_scene_copy_palette_recommendation_alias_flag_name,
        "",
    ).strip().lower() in {"1", "true", "yes", "on"}
    pulse_remap_suppression_escalation_plan_alias = resolve_pulse_remap_suppression_plan_alias(pulse_remap_suppression_escalation_plan)
    pulse_remap_suppression_plan_alias_flag_name = "DOTPIO_EXPERIMENT_PULSE_REMAP_SUPPRESSION_PLAN_ALIAS"
    pulse_remap_suppression_plan_alias_flag_enabled = os.environ.get(pulse_remap_suppression_plan_alias_flag_name, "").strip().lower() in {"1", "true", "yes", "on"}

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
    alt_why_glyph_drift, alt_why_glyph_drift_signals = alt_why_glyph_drift_from_prior(
        current_alt_why_glyph_net=token_totals["net"].get("ALT WHY GLYPH:", 0),
        prior_json_path=args.out_json,
    )
    alt_why_glyph_mode_drift, alt_why_glyph_mode_drift_signals = alt_why_glyph_mode_drift_from_prior(
        current_alt_why_glyph_mode_net=token_totals["net"].get("ALT WHY GLYPH MODE:", 0),
        prior_json_path=args.out_json,
    )
    alt_why_glyph_mode_confidence, alt_why_glyph_mode_confidence_signals = alt_why_glyph_mode_confidence_from_signals(
        alt_why_glyph_mode_drift=alt_why_glyph_mode_drift,
        alt_why_glyph_mode_drift_signals=alt_why_glyph_mode_drift_signals,
    )
    alt_why_glyph_mode_confidence_drift, alt_why_glyph_mode_confidence_drift_signals = alt_why_glyph_mode_confidence_drift_from_prior(
        current_alt_why_glyph_mode_confidence=alt_why_glyph_mode_confidence,
        prior_json_path=args.out_json,
    )
    alt_why_glyph_mode_confidence_why, alt_why_glyph_mode_confidence_why_signals = alt_why_glyph_mode_confidence_why_from_signals(
        alt_why_glyph_mode_confidence=alt_why_glyph_mode_confidence,
        alt_why_glyph_mode_confidence_drift=alt_why_glyph_mode_confidence_drift,
        alt_why_glyph_mode_confidence_signals=alt_why_glyph_mode_confidence_signals,
    )
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
    alt_step_confidence_drift, alt_step_confidence_drift_signals = alt_step_confidence_drift_from_prior(
        current_alt_step_confidence=action_pace_alt_window_confidence,
        prior_json_path=args.out_json,
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
    alt_step_why_confidence_drift, alt_step_why_confidence_drift_signals = alt_step_why_confidence_drift_from_prior(
        action_pace_alt_window_why=action_pace_alt_window_why,
        action_pace_alt_window_confidence=action_pace_alt_window_confidence,
        action_pace_alt_window_fit=action_pace_alt_window_fit,
        prior_json_path=args.out_json,
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
    route_pulse_link_mode_fit_drift, route_pulse_link_mode_fit_drift_signals = route_pulse_link_mode_fit_drift_from_prior(
        current_route_pulse_link_mode_fit=route_pulse_link_mode_fit,
        prior_json_path=args.out_json,
    )
    route_pulse_token_priority, route_pulse_token_priority_signals = route_pulse_token_priority_from_signals(
        route_pulse_link_mode_fit_drift=route_pulse_link_mode_fit_drift,
        prior_json_path=args.out_json,
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

    fx_remap_candidates = [
        {
            "rank": 1,
            "mode": "HOLD_FX",
            "summary": "Pin CALM/SPARK/BLAZE mapping and defer runtime remap edits.",
            "when": "Use during HIGH drift or high FX churn windows.",
            "risk": "LOW",
            "offlineOnly": True,
        },
        {
            "rank": 2,
            "mode": "MICRO_TUNE_FX",
            "summary": "Draft small offline FX remap options that keep glyph-band thresholds unchanged.",
            "when": "Use in stable windows with moderate churn.",
            "risk": "MID",
            "offlineOnly": True,
        },
        {
            "rank": 3,
            "mode": "SYNC_WITH_GLYPH",
            "summary": "Draft offline FX remap candidates aligned to glyph-band momentum shifts.",
            "when": "Use when glyph churn rises while drift risk is not HIGH.",
            "risk": "MID",
            "offlineOnly": True,
        },
    ]
    selected_fx_remap_candidate = next(
        (candidate for candidate in fx_remap_candidates if candidate["mode"] == dmg_glyph_fx_remap_recommendation),
        fx_remap_candidates[0],
    )
    fx_remap_candidates_payload = {
        "generatedAt": now,
        "window": {
            "sinceDays": args.since_days,
            "maxCommits": args.max_commits,
            "checkedCommits": len(rows),
            "touchedCommits": len(touched),
        },
        "recommendation": {
            "mode": dmg_glyph_fx_remap_recommendation,
            "confidence": dmg_glyph_fx_remap_confidence,
            "signals": dmg_glyph_fx_remap_recommendation_signals,
            "confidenceSignals": dmg_glyph_fx_remap_confidence_signals,
        },
        "selectedCandidate": selected_fx_remap_candidate,
        "candidates": fx_remap_candidates,
    }

    args.out_fx_remap_candidates_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_fx_remap_candidates_json.write_text(
        json.dumps(fx_remap_candidates_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    fx_candidate_md = [
        "# DMG Glyph FX Remap Candidates",
        "",
        f"- GeneratedAt(UTC): {now}",
        f"- Recommendation: **{dmg_glyph_fx_remap_recommendation}**",
        f"- Confidence: **{dmg_glyph_fx_remap_confidence}**",
        f"- Rationale: {dmg_glyph_fx_remap_recommendation_signals['rationale']}",
        f"- Guidance: {dmg_glyph_fx_remap_recommendation_signals['guidance']}",
        "",
        "## Candidate Table",
        "",
        "| Rank | Mode | Risk | Offline Only | Summary | When to use |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for candidate in fx_remap_candidates:
        fx_candidate_md.append(
            f"| {candidate['rank']} | {candidate['mode']} | {candidate['risk']} | {str(candidate['offlineOnly']).upper()} | {candidate['summary']} | {candidate['when']} |"
        )
    fx_candidate_md.extend([
        "",
        f"- Selected candidate this window: **{selected_fx_remap_candidate['mode']}**",
    ])
    args.out_fx_remap_candidates_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_fx_remap_candidates_md.write_text("\n".join(fx_candidate_md).strip() + "\n", encoding="utf-8")

    ambient_why_auto_remap_payload = {
        "generatedAt": now,
        "window": {
            "sinceDays": args.since_days,
            "maxCommits": args.max_commits,
            "checkedCommits": len(rows),
            "touchedCommits": len(touched),
        },
        "recommendation": {
            "ambientRampWhyRecommendation": ambient_ramp_why_recommendation,
            "ambientRampWhyRecommendationConfidence": ambient_ramp_why_recommendation_confidence,
            "ambientRampWhyRecommendationConfidenceStreak": ambient_ramp_why_recommendation_confidence_streak,
            "ambientRampWhyRecommendationConfidenceStreakSignals": ambient_ramp_why_recommendation_confidence_streak_signals,
            "ambientRampWhyRecommendationParity": ambient_ramp_why_recommendation_parity,
        },
        "selectedPlan": ambient_ramp_why_auto_remap_plan,
        "selectedPlanCompact": ambient_ramp_why_auto_remap_plan_compact,
        "selectedPlanWhyCompact": ambient_ramp_why_auto_remap_why,
        "selectedPlanSignals": ambient_ramp_why_auto_remap_plan_signals,
        "candidates": ambient_ramp_why_auto_remap_plan_candidates,
    }
    args.out_ambient_why_auto_remap_plan_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_ambient_why_auto_remap_plan_json.write_text(
        json.dumps(ambient_why_auto_remap_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    ambient_why_plan_md = [
        "# Ambient Ramp Why Auto-Remap Sandbox Plan",
        "",
        f"- GeneratedAt(UTC): {now}",
        f"- Recommendation: **{ambient_ramp_why_recommendation}**",
        f"- Recommendation Confidence: **{ambient_ramp_why_recommendation_confidence}**",
        f"- Recommendation Parity: **{ambient_ramp_why_recommendation_parity}**",
        f"- Selected Plan: **{ambient_ramp_why_auto_remap_plan}**",
        f"- Compact Alias: **ARW AUTO PLAN:{ambient_ramp_why_auto_remap_plan_compact}**",
        f"- Compact Rationale: **ARW AUTO WHY:{ambient_ramp_why_auto_remap_why}**",
        f"- Rationale: {ambient_ramp_why_auto_remap_plan_signals['rationale']}",
        f"- Next Action: {ambient_ramp_why_auto_remap_plan_signals['nextAction']}",
        "",
        "## Candidate Table",
        "",
        "| Rank | Plan | Risk | Offline Only | Scope | Summary | When to use |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for candidate in ambient_ramp_why_auto_remap_plan_candidates:
        ambient_why_plan_md.append(
            f"| {candidate['rank']} | {candidate['plan']} | {candidate['risk']} | {str(candidate['offlineOnly']).upper()} | {candidate['changeScope']} | {candidate['summary']} | {candidate['when']} |"
        )
    ambient_why_plan_md.extend([
        "",
        "- Safety note: artifact is digest/sandbox guidance only; runtime ambient rationale mapping remains unchanged.",
    ])
    args.out_ambient_why_auto_remap_plan_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_ambient_why_auto_remap_plan_md.write_text("\n".join(ambient_why_plan_md).strip() + "\n", encoding="utf-8")

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
        "rgfxwriWhyConfPolicyRecommendation": rgfxwri_why_conf_policy,
        "rgfxwriWhyConfPolicyRecommendationSignals": rgfxwri_why_conf_policy_signals,
        "ambientRampConfidenceRecommendation": ambient_ramp_confidence_recommendation,
        "ambientRampConfidenceRecommendationSignals": ambient_ramp_confidence_recommendation_signals,
        "ambientRampWhyRecommendation": ambient_ramp_why_recommendation,
        "ambientRampWhyRecommendationSignals": ambient_ramp_why_recommendation_signals,
        "ambientRampWhyRecommendationConfidence": ambient_ramp_why_recommendation_confidence,
        "ambientRampWhyRecommendationConfidenceSignals": ambient_ramp_why_recommendation_confidence_signals,
        "ambientRampWhyRecommendationConfidenceStreak": ambient_ramp_why_recommendation_confidence_streak,
        "ambientRampWhyRecommendationConfidenceStreakSignals": ambient_ramp_why_recommendation_confidence_streak_signals,
        "ambientRampWhyRecommendationParity": ambient_ramp_why_recommendation_parity,
        "ambientRampWhyRecommendationParitySignals": ambient_ramp_why_recommendation_parity_signals,
        "ambientRampWhyAutoRemapPlan": ambient_ramp_why_auto_remap_plan,
        "ambientRampWhyAutoRemapPlanCompact": ambient_ramp_why_auto_remap_plan_compact,
        "ambientRampWhyAutoRemapWhyCompact": ambient_ramp_why_auto_remap_why,
        "ambientRampWhyAutoRemapPlanSignals": ambient_ramp_why_auto_remap_plan_signals,
        "ambientRampWhyAutoRemapPlanDrift": ambient_ramp_why_auto_remap_plan_drift,
        "ambientRampWhyAutoRemapPlanDriftSignals": ambient_ramp_why_auto_remap_plan_drift_signals,
        "ambientRampWhyAutoRemapPlanConfidence": ambient_ramp_why_auto_remap_plan_confidence,
        "ambientRampWhyAutoRemapPlanConfidenceSignals": ambient_ramp_why_auto_remap_plan_confidence_signals,
        "ambientRampWhyAutoRemapPlanConfidenceDrift": ambient_ramp_why_auto_remap_plan_confidence_drift,
        "ambientRampWhyAutoRemapPlanConfidenceDriftSignals": ambient_ramp_why_auto_remap_plan_confidence_drift_signals,
        "ambientRampWhyAutoRemapConfidenceBandAlias": ambient_ramp_why_auto_remap_plan_confidence_band_alias,
        "ambientRampWhyAutoRemapConfidenceBandAliasSignals": {"flagName": arw_apc_flag_name, "flagEnabled": arw_apc_flag_enabled},
        "ambientRampWhyAutoRemapConfidenceMomentumFreezeRecommendation": ambient_ramp_why_auto_remap_plan_confidence_momentum_freeze_recommendation,
        "ambientRampWhyAutoRemapConfidenceMomentumFreezeRecommendationSignals": ambient_ramp_why_auto_remap_plan_confidence_momentum_freeze_signals,
        "ambientRampWhyAutoRemapConfidenceMomentumAlias": ambient_ramp_why_auto_remap_plan_confidence_momentum_alias,
        "ambientRampWhyAutoRemapConfidenceMomentumAliasSignals": {"flagName": arw_momentum_flag_name, "flagEnabled": arw_momentum_flag_enabled},
        "ambientRampWhyAutoRemapConfidenceMomentumScore": ambient_ramp_why_auto_remap_plan_confidence_momentum_score,
        "ambientRampWhyAutoRemapConfidenceMomentumScoreSignals": ambient_ramp_why_auto_remap_plan_confidence_momentum_score_signals,
        "ambientRampWhyAutoRemapMomentumArc": ambient_ramp_why_auto_remap_momentum_arc,
        "ambientRampWhyAutoRemapMomentumArcSignals": ambient_ramp_why_auto_remap_momentum_arc_signals,
        "ambientRampWhyAutoRemapMomentumArcAliasSignals": {"flagName": arw_momentum_arc_flag_name, "flagEnabled": arw_momentum_arc_flag_enabled},
        "ambientRampWhyAutoRemapMomentumArcPulseAlias": ambient_ramp_why_auto_remap_momentum_arc_pulse,
        "ambientRampWhyAutoRemapMomentumArcPulseAliasSignals": ambient_ramp_why_auto_remap_momentum_arc_pulse_signals,
        "ambientRampWhyAutoRemapMomentumArcPulseAliasFlagSignals": {"flagName": arw_arc_pulse_flag_name, "flagEnabled": arw_arc_pulse_flag_enabled},
        "urgencyStackPruningOrderRecommendation": urgency_stack_pruning_order_recommendation,
        "urgencyStackPruningOrderRecommendationSignals": urgency_stack_pruning_order_recommendation_signals,
        "urgencyStackRailRecommendation": urgency_stack_rail_recommendation,
        "urgencyStackRailRecommendationSignals": urgency_stack_rail_recommendation_signals,
        "dmgGlyphShapeRemapRecommendation": dmg_glyph_shape_remap_recommendation,
        "dmgGlyphShapeRemapRecommendationSignals": dmg_glyph_shape_remap_recommendation_signals,
        "dmgGlyphFxRemapRecommendation": dmg_glyph_fx_remap_recommendation,
        "dmgGlyphFxRemapRecommendationSignals": dmg_glyph_fx_remap_recommendation_signals,
        "dmgGlyphFxRemapConfidence": dmg_glyph_fx_remap_confidence,
        "dmgGlyphFxRemapConfidenceSignals": dmg_glyph_fx_remap_confidence_signals,
        "dmgnumLifeTrendFxPulseRemapRecommendation": dmgnum_life_trend_fx_pulse_remap_recommendation,
        "dmgnumLifeTrendFxPulseRemapRecommendationSignals": dmgnum_life_trend_fx_pulse_remap_recommendation_signals,
        "pulseRemapMomentumRecommendation": pulse_remap_momentum_recommendation,
        "pulseRemapMomentumRecommendationSignals": pulse_remap_momentum_recommendation_signals,
        "pulseRemapMomentumDrift": pulse_remap_momentum_drift,
        "pulseRemapMomentumDriftSignals": pulse_remap_momentum_drift_signals,
        "pulseRemapMomentumSuppression": pulse_remap_momentum_suppression,
        "pulseRemapMomentumSuppressionSignals": pulse_remap_momentum_suppression_signals,
        "pulseRemapMomentumFreezeStreak": int(pulse_remap_momentum_suppression_signals.get("freezeStreak", 0)),
        "pulseRemapMomentumSuppressionAlias": pulse_remap_momentum_suppression_alias,
        "pulseRemapMomentumSuppressionAliasSignals": {"flagName": pulse_remap_momentum_suppression_alias_flag_name, "flagEnabled": pulse_remap_momentum_suppression_alias_flag_enabled},
        "pulseRemapSuppressionFamilyTrendDrift": pulse_remap_suppression_family_trend_drift,
        "pulseRemapSuppressionFamilyTrendSignals": pulse_remap_suppression_family_trend_signals,
        "pulseRemapSuppressionPlanFamilyTrendDrift": pulse_remap_suppression_plan_family_trend_drift,
        "pulseRemapSuppressionPlanFamilyTrendSignals": pulse_remap_suppression_plan_family_trend_signals,
        "pulseRemapSceneMicrolineCadenceFamilyTrendDrift": pulse_remap_scene_microline_cadence_family_trend_drift,
        "pulseRemapSceneMicrolineCadenceFamilyTrendSignals": pulse_remap_scene_microline_cadence_family_trend_signals,
        "pulseRemapSceneMicrolineStylePolicyFamilyTrendDrift": pulse_remap_scene_microline_style_policy_family_trend_drift,
        "pulseRemapSceneMicrolineStylePolicyFamilyTrendSignals": pulse_remap_scene_microline_style_policy_family_trend_signals,
        "pulseRemapSceneFxGlintFamilyTrendDrift": pulse_remap_scene_fx_glint_family_trend_drift,
        "pulseRemapSceneFxGlintFamilyTrendSignals": pulse_remap_scene_fx_glint_family_trend_signals,
        "pulseRemapSceneCopyPaletteRecommendationFamilyTrendDrift": pulse_remap_scene_copy_palette_recommendation_family_trend_drift,
        "pulseRemapSceneCopyPaletteRecommendationFamilyTrendSignals": pulse_remap_scene_copy_palette_recommendation_family_trend_signals,
        "pulseRemapSuppressionEscalationPlan": pulse_remap_suppression_escalation_plan,
        "pulseRemapSuppressionEscalationPlanSignals": pulse_remap_suppression_escalation_plan_signals,
        "pulseRemapSuppressionSceneFlavor": pulse_remap_suppression_scene_flavor,
        "pulseRemapSuppressionSceneFlavorSignals": pulse_remap_suppression_scene_flavor_signals,
        "pulseRemapSceneConfidence": pulse_remap_scene_confidence,
        "pulseRemapSceneConfidenceSignals": pulse_remap_scene_confidence_signals,
        "pulseRemapSuppressionSceneMicroline": pulse_remap_suppression_scene_microline,
        "pulseRemapSuppressionSceneMicrolineSignals": pulse_remap_suppression_scene_microline_signals,
        "pulseRemapSceneMicrolineVariantPack": pulse_remap_scene_microline_variant_pack,
        "pulseRemapSceneMicrolineVariantPackSignals": pulse_remap_scene_microline_variant_pack_signals,
        "pulseRemapSceneMicrolineVariantPackSelectionAlias": pulse_remap_scene_microline_variant_pack_selection_alias,
        "pulseRemapSceneMicrolineVariantPackSelectionAliasSignals": {
            "flagName": pulse_remap_scene_microline_variant_pack_selection_alias_flag_name,
            "flagEnabled": pulse_remap_scene_microline_variant_pack_selection_alias_flag_enabled,
        },
        "pulseRemapSceneMicrolineStyleDiversificationPolicy": pulse_remap_scene_microline_style_diversification_policy,
        "pulseRemapSceneMicrolineStyleDiversificationPolicySignals": pulse_remap_scene_microline_style_diversification_policy_signals,
        "pulseRemapSceneMicrolineStylePolicySmoothed": pulse_remap_scene_microline_style_policy_smoothed,
        "pulseRemapSceneMicrolineStylePolicySmoothedSignals": pulse_remap_scene_microline_style_policy_smoothed_signals,
        "pulseRemapSceneMicrolineStylePolicyPostureHook": pulse_remap_scene_microline_style_policy_posture_hook,
        "pulseRemapSceneMicrolineStylePolicyPostureHookSignals": pulse_remap_scene_microline_style_policy_posture_hook_signals,
        "pulseRemapSceneMicrolineStylePostureAlias": pulse_remap_scene_microline_style_posture_alias,
        "pulseRemapSceneMicrolineStylePostureAliasSignals": {
            "flagName": pulse_remap_scene_microline_style_posture_alias_flag_name,
            "flagEnabled": pulse_remap_scene_microline_style_posture_alias_flag_enabled,
        },
        "pulseRemapSceneMicrolineStylePolicyAlias": pulse_remap_scene_microline_style_policy_alias,
        "pulseRemapSceneMicrolineStylePolicyAliasSignals": {
            "flagName": pulse_remap_scene_microline_style_policy_alias_flag_name,
            "flagEnabled": pulse_remap_scene_microline_style_policy_alias_flag_enabled,
        },
        "pulseRemapSceneMicrolineCadence": pulse_remap_scene_microline_cadence,
        "pulseRemapSceneMicrolineCadenceSignals": pulse_remap_scene_microline_cadence_signals,
        "pulseRemapSceneMicrolineCadenceAlias": pulse_remap_scene_microline_cadence_alias,
        "pulseRemapSceneMicrolineCadenceAliasSignals": {
            "flagName": pulse_remap_scene_microline_cadence_alias_flag_name,
            "flagEnabled": pulse_remap_scene_microline_cadence_alias_flag_enabled,
        },
        "pulseRemapSuppressionPostureWarning": pulse_remap_suppression_posture_warning,
        "pulseRemapSuppressionPostureWarningSignals": pulse_remap_suppression_posture_warning_signals,
        "pulseRemapSuppressionPostureWarningAlias": pulse_remap_suppression_posture_warning_alias,
        "pulseRemapSuppressionPostureWarningAliasSignals": pulse_remap_suppression_posture_warning_alias_signals,
        "pulseRemapSceneFxGlint": pulse_remap_scene_fx_glint,
        "pulseRemapSceneFxGlintSignals": pulse_remap_scene_fx_glint_signals,
        "pulseRemapSceneFxGlintAlias": pulse_remap_scene_fx_glint_alias,
        "pulseRemapSceneFxGlintAliasSignals": {
            "flagName": pulse_remap_scene_fx_glint_alias_flag_name,
            "flagEnabled": pulse_remap_scene_fx_glint_alias_flag_enabled,
        },
        "pulseRemapSceneCopyPaletteRecommendation": pulse_remap_scene_copy_palette_recommendation,
        "pulseRemapSceneCopyPaletteRecommendationSignals": pulse_remap_scene_copy_palette_recommendation_signals,
        "pulseRemapSceneCopyPaletteRecommendationAlias": pulse_remap_scene_copy_palette_recommendation_alias,
        "pulseRemapSceneCopyPaletteRecommendationAliasSignals": {
            "flagName": pulse_remap_scene_copy_palette_recommendation_alias_flag_name,
            "flagEnabled": pulse_remap_scene_copy_palette_recommendation_alias_flag_enabled,
        },
        "pulseRemapSuppressionEscalationPlanAlias": pulse_remap_suppression_escalation_plan_alias,
        "pulseRemapSuppressionEscalationPlanAliasSignals": {"flagName": pulse_remap_suppression_plan_alias_flag_name, "flagEnabled": pulse_remap_suppression_plan_alias_flag_enabled},
        "pulseRemapMomentumAlias": pulse_remap_momentum_alias,
        "pulseRemapMomentumAliasSignals": {"flagName": pulse_remap_momentum_alias_flag_name, "flagEnabled": pulse_remap_momentum_alias_flag_enabled},
        "laneBucketAge": lane_bucket_age["token"],
        "laneBucketAgeStatus": lane_bucket_age["status"],
        "laneBucketAgeHours": lane_bucket_age["ageHours"],
        "laneBucketAgeWindowHours": lane_bucket_age["windowHours"],
        "laneBucketAgeMaxHours": lane_bucket_age["maxAgeHours"],
        "laneBucketAgeDrift": lane_bucket_age_delta,
        "laneBucketAgeDriftSignals": lane_bucket_age_drift_signals,
        "laneCadenceRecency": lane_cadence_recency,
        "laneCadenceRecencySignals": lane_cadence_recency_signals,
        "laneCadenceMissRisk": lane_cadence_miss_risk_token,
        "laneCadenceMissRiskSignals": lane_cadence_miss_risk_signals,
        "laneCadenceMissRiskAlias": lane_cadence_miss_risk_alias_token,
        "laneCadenceMissRiskAliasSignals": lane_cadence_miss_risk_alias_signals,
        "lanePriorityHysteresisFloorRecommendation": lane_priority_hysteresis_floor_recommendation,
        "lanePriorityHysteresisFloorRecommendationSignals": lane_priority_hysteresis_floor_recommendation_signals,
        "lanePriorityHysteresisFloorRecommendationAlias": lane_priority_hysteresis_floor_recommendation_alias,
        "lanePriorityHysteresisFloorRecommendationAliasSignals": lane_priority_hysteresis_floor_recommendation_alias_signals,
        "lanePriorityHysteresisFloorFamilyTrendDrift": lane_priority_hysteresis_floor_family_trend_drift,
        "lanePriorityHysteresisFloorFamilyTrendSignals": lane_priority_hysteresis_floor_family_trend_signals,
        "lanePriorityHysteresisFloorFamilyTrendAlias": lane_priority_hysteresis_floor_family_trend_alias,
        "lanePriorityHysteresisFloorFamilyTrendAliasSignals": {
            "flagName": lane_priority_hysteresis_floor_family_trend_alias_flag_name,
            "flagEnabled": lane_priority_hysteresis_floor_family_trend_alias_flag_enabled,
            "trend": lane_priority_hysteresis_floor_family_trend_signals["trend"],
            "alias": lane_priority_hysteresis_floor_family_trend_alias,
        },
        "laneCadenceMissRiskHighStreak": lane_priority_hysteresis_floor_recommendation_signals["highStreak"],
        "laneBucketAgeCompactAlias": lane_bucket_age_compact_alias,
        "laneBucketAgeCompactAliasSignals": lane_bucket_age_compact_alias_signals,
        "lanePriorityRecommendation": lane_priority_recommendation,
        "lanePriorityRecommendationSignals": lane_priority_recommendation_signals,
        "lanePriorityRecommendationConfidence": lane_priority_recommendation_confidence_level,
        "lanePriorityRecommendationConfidenceSignals": lane_priority_recommendation_confidence_signals,
        "lanePriorityRecommendationConfidenceGuardSignals": lane_priority_recommendation_confidence_guard_signals,
        "lanePriorityRecommendationConfidenceGuardAlias": lane_priority_recommendation_confidence_guard_alias,
        "lanePriorityRecommendationConfidenceGuardAliasSignals": lane_priority_recommendation_confidence_guard_alias_signals,
        "lanePriorityRecommendationConfidenceGuardThreshold": lane_priority_recommendation_confidence_guard_threshold,
        "lanePriorityRecommendationConfidenceGuardThresholdSignals": lane_priority_recommendation_confidence_guard_threshold_signals,
        "lanePriorityRecommendationConfidenceGuardPersistenceCoach": lane_priority_recommendation_confidence_guard_persistence_coach_token,
        "lanePriorityRecommendationConfidenceGuardPersistenceCoachSignals": lane_priority_recommendation_confidence_guard_persistence_coach_signals,
        "lanePriorityRecommendationConfidenceGuardPersistenceCoachAlias": lane_priority_recommendation_confidence_guard_persistence_coach_alias,
        "lanePriorityRecommendationConfidenceGuardPersistenceCoachAliasSignals": lane_priority_recommendation_confidence_guard_persistence_coach_alias_signals,
        "lanePriorityRecommendationConfidenceGuardPersistenceCoachVariantPack": lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_token,
        "lanePriorityRecommendationConfidenceGuardPersistenceCoachVariantPackSignals": lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_signals,
        "lanePriorityRecommendationConfidenceGuardPersistenceCoachVariantPackAlias": lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_alias,
        "lanePriorityRecommendationConfidenceGuardPersistenceCoachVariantPackAliasSignals": lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_alias_signals,
        "lanePriorityRecommendationConfidenceGuardPersistenceCoachCopyNarrative": lane_priority_recommendation_confidence_guard_persistence_coach_copy_narrative,
        "lanePriorityRecommendationConfidenceGuardPersistenceCoachCopyNarrativeSignals": lane_priority_recommendation_confidence_guard_persistence_coach_copy_narrative_signals,
        "lanePriorityRecommendationConfidenceGuardPersistenceCoachCopyAlias": lane_priority_recommendation_confidence_guard_persistence_coach_copy_alias,
        "lanePriorityRecommendationConfidenceGuardPersistenceCoachCopyAliasSignals": lane_priority_recommendation_confidence_guard_persistence_coach_copy_alias_signals,
        "lanePriorityRecommendationConfidenceGuardPersistenceCoachCopyWhy": lane_priority_recommendation_confidence_guard_persistence_coach_copy_why,
        "lanePriorityRecommendationConfidenceGuardPersistenceCoachCopyWhySignals": lane_priority_recommendation_confidence_guard_persistence_coach_copy_why_signals,
        "lanePriorityRecommendationCompactAlias": lane_priority_recommendation_compact_alias,
        "lanePriorityRecommendationCompactAliasSignals": lane_priority_recommendation_compact_alias_signals,
        "lanePriorityHysteresisCompactAlias": lane_priority_hysteresis_compact_alias,
        "lanePriorityHysteresisCompactAliasSignals": lane_priority_hysteresis_compact_alias_signals,
        "lanePriorityHysteresisRail": lane_priority_hysteresis_rail,
        "lanePriorityHysteresisRailSignals": lane_priority_hysteresis_rail_signals,
        "lanePriorityHysteresisThresholdTuning": lane_priority_hysteresis_threshold_tuning,
        "lanePriorityHysteresisThresholdTuningSignals": lane_priority_hysteresis_threshold_tuning_signals,
        "lanePriorityVolatilityRegimeMemory": f"LPR VOL REGIME:{lane_priority_hysteresis_threshold_tuning_signals['volatilityRegimeMemory']}",
        "lanePriorityVolatilityRegimeMemorySignals": {
            "currentRegime": lane_priority_hysteresis_threshold_tuning_signals["volatilityRegime"],
            "priorRegime": lane_priority_hysteresis_threshold_tuning_signals["priorVolatilityRegime"],
            "memoryRegime": lane_priority_hysteresis_threshold_tuning_signals["volatilityRegimeMemory"],
            "reason": lane_priority_hysteresis_threshold_tuning_signals["volatilityRegimeReason"],
            "stepSizes": lane_priority_hysteresis_threshold_tuning_signals["stepSizes"],
        },
        "lanePriorityHysteresisThresholdCompactAlias": lane_priority_hysteresis_threshold_compact_alias,
        "lanePriorityHysteresisThresholdCompactAliasSignals": lane_priority_hysteresis_threshold_compact_alias_signals,
        "lanePriorityHysteresisWindowBand": lane_priority_hysteresis_window_band,
        "lanePriorityHysteresisWindowBandSignals": lane_priority_hysteresis_window_band_signals,
        "lanePriorityHysteresisWindowDelta": lane_priority_hysteresis_window_delta_token,
        "lanePriorityHysteresisWindowDeltaValue": lane_priority_hysteresis_window_delta,
        "lanePriorityHysteresisWindowDeltaSignals": lane_priority_hysteresis_window_delta_signals,
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
        "altStepConfidence": action_pace_alt_window_confidence,
        "altStepConfidenceDrift": alt_step_confidence_drift,
        "altStepConfidenceDriftSignals": alt_step_confidence_drift_signals,
        "altStepWhyConfidenceDrift": alt_step_why_confidence_drift,
        "altStepWhyConfidenceDriftSignals": alt_step_why_confidence_drift_signals,
        "altWhyGlyphDrift": alt_why_glyph_drift,
        "altWhyGlyphDriftSignals": alt_why_glyph_drift_signals,
        "altWhyGlyphModeDrift": alt_why_glyph_mode_drift,
        "altWhyGlyphModeDriftSignals": alt_why_glyph_mode_drift_signals,
        "altWhyGlyphModeConfidence": alt_why_glyph_mode_confidence,
        "altWhyGlyphModeConfidenceSignals": alt_why_glyph_mode_confidence_signals,
        "altWhyGlyphModeConfidenceDrift": alt_why_glyph_mode_confidence_drift,
        "altWhyGlyphModeConfidenceDriftSignals": alt_why_glyph_mode_confidence_drift_signals,
        "altWhyGlyphModeConfidenceWhy": alt_why_glyph_mode_confidence_why,
        "altWhyGlyphModeConfidenceWhySignals": alt_why_glyph_mode_confidence_why_signals,
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
        "routePulseLinkModeFitDrift": route_pulse_link_mode_fit_drift,
        "routePulseLinkModeFitDriftSignals": route_pulse_link_mode_fit_drift_signals,
        "routePulseTokenPriority": route_pulse_token_priority,
        "routePulseTokenPrioritySignals": route_pulse_token_priority_signals,
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
        "tokenFamilyTotals": token_family_totals,
        "comboWindowRetuneRecommendation": combo_window_retune_recommendation,
        "comboWindowRetuneRecommendationSignals": combo_window_retune_recommendation_signals,
        "comboWindowRetuneAlias": dmg_combo_retune_alias if dmg_combo_retune_alias_flag_enabled else "FLAG OFF",
        "comboWindowRetuneAliasSignals": {"flagName": dmg_combo_retune_alias_flag_name, "flagEnabled": dmg_combo_retune_alias_flag_enabled, "recommendation": combo_window_retune_recommendation, "alias": dmg_combo_retune_alias},
        "comboWindowRetuneConfidence": combo_window_retune_confidence,
        "comboWindowRetuneConfidenceSignals": combo_window_retune_confidence_signals,
        "comboWindowRetuneConfidenceAlias": dmg_combo_retune_conf_alias if dmg_combo_retune_conf_alias_flag_enabled else "FLAG OFF",
        "comboWindowRetuneConfidenceAliasSignals": {"flagName": dmg_combo_retune_conf_alias_flag_name, "flagEnabled": dmg_combo_retune_conf_alias_flag_enabled, "confidence": combo_window_retune_confidence, "alias": dmg_combo_retune_conf_alias},
        "comboChainNarrativeCoachLine": combo_chain_narrative_coach_line,
        "comboChainNarrativeCoachLineSignals": combo_chain_narrative_coach_line_signals,
        "comboConfidenceCoachRecommendation": combo_confidence_coach_recommendation,
        "comboConfidenceCoachRecommendationSignals": combo_confidence_coach_recommendation_signals,
        "comboConfidenceCoachRecommendationStreak": combo_confidence_coach_recommendation_streak,
        "comboConfidenceCoachRecommendationStreakDrift": combo_confidence_coach_recommendation_streak_drift,
        "comboConfidenceCoachRecommendationStreakSignals": combo_confidence_coach_recommendation_streak_signals,
        "comboConfidenceCoachFallbackNarrative": combo_confidence_coach_fallback_narrative,
        "comboConfidenceCoachFallbackNarrativeSignals": combo_confidence_coach_fallback_narrative_signals,
        "comboConfidenceCoachAlias": dmg_combo_conf_coach_alias if dmg_combo_conf_coach_alias_flag_enabled else "FLAG OFF",
        "comboConfidenceCoachAliasSignals": {"flagName": dmg_combo_conf_coach_alias_flag_name, "flagEnabled": dmg_combo_conf_coach_alias_flag_enabled, "recommendation": combo_confidence_coach_recommendation, "alias": dmg_combo_conf_coach_alias},
        "comboConfidenceCoachSceneArc": combo_confidence_coach_scene_arc,
        "comboConfidenceCoachSceneArcSignals": combo_confidence_coach_scene_arc_signals,
        "comboConfidenceFxAccent": combo_confidence_fx_accent,
        "comboConfidenceFxAccentSignals": combo_confidence_fx_accent_signals,
        "comboConfidenceFxAccentAlias": dmg_combo_conf_fx_accent_alias if dmg_combo_conf_fx_accent_alias_flag_enabled else "FLAG OFF",
        "comboConfidenceFxAccentAliasSignals": {"flagName": dmg_combo_conf_fx_accent_alias_flag_name, "flagEnabled": dmg_combo_conf_fx_accent_alias_flag_enabled, "accent": combo_confidence_fx_accent, "alias": dmg_combo_conf_fx_accent_alias},
        "comboConfidenceFxAccentFamilyTrendDrift": combo_confidence_fx_accent_family_trend_drift,
        "comboConfidenceFxAccentFamilyTrendSignals": combo_confidence_fx_accent_family_trend_signals,
        "comboConfidenceFxAccentTrendHysteresisRecommendation": combo_confidence_fx_accent_family_trend_signals["trendHysteresisRecommendation"],
        "comboConfidenceFxAccentTrendHysteresisRecommendationSignals": {
            "recommendation": combo_confidence_fx_accent_family_trend_signals["trendHysteresisRecommendation"],
            "reason": combo_confidence_fx_accent_family_trend_signals["trendHysteresisRecommendationReason"],
            "volatilityRegime": combo_confidence_fx_accent_family_trend_signals["volatilityRegime"],
            "hysteresisThreshold": combo_confidence_fx_accent_family_trend_signals["hysteresisThreshold"],
            "hysteresisApplied": combo_confidence_fx_accent_family_trend_signals["hysteresisApplied"],
            "rawDrift": combo_confidence_fx_accent_family_trend_signals["rawDrift"],
            "offlineOnly": True,
        },
        "comboConfidenceFxAccentTrendHysteresisConfidence": combo_confidence_fx_accent_family_trend_signals["trendHysteresisConfidence"],
        "comboConfidenceFxAccentTrendHysteresisConfidenceSignals": {
            "confidence": combo_confidence_fx_accent_family_trend_signals["trendHysteresisConfidence"],
            "reason": combo_confidence_fx_accent_family_trend_signals["trendHysteresisConfidenceReason"],
            "hysteresisThreshold": combo_confidence_fx_accent_family_trend_signals["hysteresisThreshold"],
            "rawDrift": combo_confidence_fx_accent_family_trend_signals["rawDrift"],
            "offlineOnly": True,
        },
        "comboConfidenceFxAccentTrendHysteresisAlias": dmg_combo_conf_fx_accent_trend_hys_alias if dmg_combo_conf_fx_accent_trend_hys_alias_flag_enabled else "FLAG OFF",
        "comboConfidenceFxAccentTrendHysteresisAliasSignals": {
            "flagName": dmg_combo_conf_fx_accent_trend_hys_alias_flag_name,
            "flagEnabled": dmg_combo_conf_fx_accent_trend_hys_alias_flag_enabled,
            "recommendation": combo_confidence_fx_accent_family_trend_signals["trendHysteresisRecommendation"],
            "confidence": combo_confidence_fx_accent_family_trend_signals["trendHysteresisConfidence"],
            "alias": dmg_combo_conf_fx_accent_trend_hys_alias,
        },
        "comboConfidenceCoachCopySwapRecommendation": combo_confidence_coach_copy_swap_recommendation,
        "comboConfidenceCoachCopySwapRecommendationAlias": dmg_combo_conf_coach_copy_swap_alias if dmg_combo_conf_coach_copy_swap_alias_flag_enabled else "FLAG OFF",
        "comboConfidenceCoachCopySwapRecommendationAliasSignals": {"flagName": dmg_combo_conf_coach_copy_swap_alias_flag_name, "flagEnabled": dmg_combo_conf_coach_copy_swap_alias_flag_enabled, "recommendation": combo_confidence_coach_copy_swap_recommendation, "alias": dmg_combo_conf_coach_copy_swap_alias},
        "comboConfidenceCoachCopySwapRecommendationSignals": combo_confidence_coach_copy_swap_recommendation_signals,
        "comboConfidenceCoachCopySwapRecommendationFamilyTrendDrift": combo_confidence_coach_copy_swap_recommendation_family_trend_drift,
        "comboConfidenceCoachCopySwapRecommendationFamilyTrendSignals": combo_confidence_coach_copy_swap_recommendation_family_trend_signals,
        "comboConfidenceCoachCopySwapRecommendationTrendAlias": dmg_combo_conf_coach_copy_swap_trend_alias if dmg_combo_conf_coach_copy_swap_trend_alias_flag_enabled else "FLAG OFF",
        "comboConfidenceCoachCopySwapRecommendationTrendAliasSignals": {"flagName": dmg_combo_conf_coach_copy_swap_trend_alias_flag_name, "flagEnabled": dmg_combo_conf_coach_copy_swap_trend_alias_flag_enabled, "trend": copy_swap_trend, "alias": dmg_combo_conf_coach_copy_swap_trend_alias},
        "comboConfidenceFxAccentTrendAlias": dmg_combo_conf_fx_accent_trend_alias if dmg_combo_conf_fx_accent_trend_alias_flag_enabled else "FLAG OFF",
        "comboConfidenceFxAccentTrendAliasSignals": {"flagName": dmg_combo_conf_fx_accent_trend_alias_flag_name, "flagEnabled": dmg_combo_conf_fx_accent_trend_alias_flag_enabled, "trend": combo_confidence_fx_accent_trend, "alias": dmg_combo_conf_fx_accent_trend_alias},
        "comboConfidenceFxAccentVolatilityAlias": dmg_combo_conf_fx_accent_volatility_alias if dmg_combo_conf_fx_accent_volatility_alias_flag_enabled else "FLAG OFF",
        "comboConfidenceFxAccentVolatilityAliasSignals": {"flagName": dmg_combo_conf_fx_accent_volatility_alias_flag_name, "flagEnabled": dmg_combo_conf_fx_accent_volatility_alias_flag_enabled, "volatilityRegime": combo_confidence_fx_accent_signals["volatilityRegime"], "alias": dmg_combo_conf_fx_accent_volatility_alias},
        "comboConfidenceCoachSceneArcAlias": dmg_combo_conf_coach_scene_arc_alias if dmg_combo_conf_coach_scene_arc_alias_flag_enabled else "FLAG OFF",
        "comboConfidenceCoachSceneArcAliasSignals": {"flagName": dmg_combo_conf_coach_scene_arc_alias_flag_name, "flagEnabled": dmg_combo_conf_coach_scene_arc_alias_flag_enabled, "sceneArc": combo_confidence_coach_scene_arc, "alias": dmg_combo_conf_coach_scene_arc_alias},
        "pulseHeatFxCompactBudgetDrift": pulse_heat_fx_compact_budget_drift_level,
        "pulseHeatFxCompactBudgetDriftSignals": pulse_heat_fx_compact_budget_drift_signals,
        "routeGlowFxCompactBudgetDrift": route_glow_fx_compact_budget_drift_level,
        "routeGlowFxCompactBudgetDriftSignals": route_glow_fx_compact_budget_drift_signals,
        "routeGlowFxConfWhyRailModeCompactBudgetDrift": route_glow_fx_conf_why_rail_mode_compact_budget_drift_level,
        "routeGlowFxConfWhyRailModeCompactBudgetDriftSignals": route_glow_fx_conf_why_rail_mode_compact_budget_drift_signals,
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
        f"- RGFXWRI WHY CONF POLICY REC: **{rgfxwri_why_conf_policy}** ({rgfxwri_why_conf_policy_signals['rationale']}; churn={rgfxwri_why_conf_policy_signals['familyChurn']} net={rgfxwri_why_conf_policy_signals['familyNet']} coverage={rgfxwri_why_conf_policy_signals['familyCoverage']} offlineOnly={rgfxwri_why_conf_policy_signals['offlineOnly']})",
        f"- AMBIENT RAMP CONF REC: **{ambient_ramp_confidence_recommendation}** ({ambient_ramp_confidence_recommendation_signals['rationale']}; churn={ambient_ramp_confidence_recommendation_signals['ambientRampConfidenceChurn']} net={ambient_ramp_confidence_recommendation_signals['ambientRampConfidenceNet']} coverage={ambient_ramp_confidence_recommendation_signals['ambientRampConfidenceCoverage']} pressure={ambient_ramp_confidence_recommendation_signals['pressureBand']} offlineOnly={ambient_ramp_confidence_recommendation_signals['offlineOnly']})",
        f"- AMBIENT RAMP WHY REC: **{ambient_ramp_why_recommendation}** ({ambient_ramp_why_recommendation_signals['rationale']}; churn={ambient_ramp_why_recommendation_signals['ambientRampWhyChurn']} net={ambient_ramp_why_recommendation_signals['ambientRampWhyNet']} coverage={ambient_ramp_why_recommendation_signals['ambientRampWhyCoverage']} pressure={ambient_ramp_why_recommendation_signals['pressureBand']} offlineOnly={ambient_ramp_why_recommendation_signals['offlineOnly']})",
        f"- AMBIENT RAMP WHY REC CONF: **{ambient_ramp_why_recommendation_confidence}** ({ambient_ramp_why_recommendation_confidence_signals['rationale']}; rec={ambient_ramp_why_recommendation_confidence_signals['recommendation']} churn={ambient_ramp_why_recommendation_confidence_signals['ambientRampWhyChurn']} drift={ambient_ramp_why_recommendation_confidence_signals['driftRisk']} pressure={ambient_ramp_why_recommendation_confidence_signals['pressureBand']})",
        f"- AMBIENT RAMP WHY REC PARITY: **{ambient_ramp_why_recommendation_parity}** ({ambient_ramp_why_recommendation_parity_signals['rationale']}; rec={ambient_ramp_why_recommendation_parity_signals['recommendation']} conf={ambient_ramp_why_recommendation_parity_signals['confidence']} churn={ambient_ramp_why_recommendation_parity_signals['ambientRampWhyChurn']} net={ambient_ramp_why_recommendation_parity_signals['ambientRampWhyNet']:+d} pressure={ambient_ramp_why_recommendation_parity_signals['pressureBand']})",
        f"- AMBIENT RAMP WHY AUTO-REMAP PLAN: **{ambient_ramp_why_auto_remap_plan}** ({ambient_ramp_why_auto_remap_plan_signals['rationale']}; rec={ambient_ramp_why_auto_remap_plan_signals['recommendation']} conf={ambient_ramp_why_auto_remap_plan_signals['confidence']} parity={ambient_ramp_why_auto_remap_plan_signals['parity']} drift={ambient_ramp_why_auto_remap_plan_signals['driftRisk']} pressure={ambient_ramp_why_auto_remap_plan_signals['pressureBand']} offlineOnly={ambient_ramp_why_auto_remap_plan_signals['offlineOnly']})",
        f"- ARW AUTO PLAN: **{ambient_ramp_why_auto_remap_plan_compact}** (full={ambient_ramp_why_auto_remap_plan})",
        f"- ARW AUTO WHY: **{ambient_ramp_why_auto_remap_why}** (offline compact rationale shorthand)",
        f"- ARW AUTO PLAN Δ: **{ambient_ramp_why_auto_remap_plan_drift:+d}** ({ambient_ramp_why_auto_remap_plan_drift_signals['reason']}; current={ambient_ramp_why_auto_remap_plan_drift_signals['currentPlan']}({ambient_ramp_why_auto_remap_plan_drift_signals['currentScore']}) prior={ambient_ramp_why_auto_remap_plan_drift_signals['priorPlan']}({ambient_ramp_why_auto_remap_plan_drift_signals['priorScore']}) loaded={ambient_ramp_why_auto_remap_plan_drift_signals['priorLoaded']})",
        f"- ARW AUTO PLAN CONF: **{ambient_ramp_why_auto_remap_plan_confidence}** ({ambient_ramp_why_auto_remap_plan_confidence_signals['rationale']}; recConf={ambient_ramp_why_auto_remap_plan_confidence_signals['recommendationConfidence']} parity={ambient_ramp_why_auto_remap_plan_confidence_signals['parity']} driftRisk={ambient_ramp_why_auto_remap_plan_confidence_signals['driftRisk']} pressure={ambient_ramp_why_auto_remap_plan_confidence_signals['pressureBand']} Δ={ambient_ramp_why_auto_remap_plan_confidence_signals['planDrift']:+d})",
        f"- ARW AUTO PLAN CONF Δ: **{ambient_ramp_why_auto_remap_plan_confidence_drift:+d}** ({ambient_ramp_why_auto_remap_plan_confidence_drift_signals['reason']}; current={ambient_ramp_why_auto_remap_plan_confidence_drift_signals['currentConfidence']}({ambient_ramp_why_auto_remap_plan_confidence_drift_signals['currentScore']}) prior={ambient_ramp_why_auto_remap_plan_confidence_drift_signals['priorConfidence']}({ambient_ramp_why_auto_remap_plan_confidence_drift_signals['priorScore']}) loaded={ambient_ramp_why_auto_remap_plan_confidence_drift_signals['priorLoaded']})",
        f"- ARW APC: **{ambient_ramp_why_auto_remap_plan_confidence_band_alias if arw_apc_flag_enabled else 'FLAG OFF'}** (flag={arw_apc_flag_name} enabled={arw_apc_flag_enabled} conf={ambient_ramp_why_auto_remap_plan_confidence})",
        f"- ARW AUTO PLAN CONF MOMENTUM: **{ambient_ramp_why_auto_remap_plan_confidence_momentum_freeze_recommendation}** ({ambient_ramp_why_auto_remap_plan_confidence_momentum_freeze_signals['reason']}; oscillating={ambient_ramp_why_auto_remap_plan_confidence_momentum_freeze_signals['oscillating']} streak={ambient_ramp_why_auto_remap_plan_confidence_momentum_freeze_signals['confidenceStreak']} confΔ={ambient_ramp_why_auto_remap_plan_confidence_momentum_freeze_signals['confidenceDrift']:+d} planΔ={ambient_ramp_why_auto_remap_plan_confidence_momentum_freeze_signals['planDrift']:+d} driftRisk={ambient_ramp_why_auto_remap_plan_confidence_momentum_freeze_signals['driftRisk']} offlineOnly={ambient_ramp_why_auto_remap_plan_confidence_momentum_freeze_signals['offlineOnly']})",
        f"- ARW MOMENTUM: **{ambient_ramp_why_auto_remap_plan_confidence_momentum_alias if arw_momentum_flag_enabled else 'FLAG OFF'}** (flag={arw_momentum_flag_name} enabled={arw_momentum_flag_enabled} full={ambient_ramp_why_auto_remap_plan_confidence_momentum_freeze_recommendation})",
        f"- ARW MOMENTUM SCORE: **{ambient_ramp_why_auto_remap_plan_confidence_momentum_score}** (base={ambient_ramp_why_auto_remap_plan_confidence_momentum_score_signals['base']} confΔ={ambient_ramp_why_auto_remap_plan_confidence_momentum_score_signals['confidenceDrift']:+d} planΔ={ambient_ramp_why_auto_remap_plan_confidence_momentum_score_signals['planDrift']:+d} streak={ambient_ramp_why_auto_remap_plan_confidence_momentum_score_signals['confidenceStreak']} driftRisk={ambient_ramp_why_auto_remap_plan_confidence_momentum_score_signals['driftRisk']} parity={ambient_ramp_why_auto_remap_plan_confidence_momentum_score_signals['parity']})",
        f"- ARW MOMENTUM ARC: **{ambient_ramp_why_auto_remap_momentum_arc if arw_momentum_arc_flag_enabled else 'FLAG OFF'}** (flag={arw_momentum_arc_flag_name} enabled={arw_momentum_arc_flag_enabled} reason={ambient_ramp_why_auto_remap_momentum_arc_signals['reason']} rec={ambient_ramp_why_auto_remap_momentum_arc_signals['recommendation']} pressure={ambient_ramp_why_auto_remap_momentum_arc_signals['pressureBand']} drift={ambient_ramp_why_auto_remap_momentum_arc_signals['driftRisk']} score={ambient_ramp_why_auto_remap_momentum_arc_signals['momentumScore']})",
        f"- ARW ARC PULSE: **{ambient_ramp_why_auto_remap_momentum_arc_pulse if arw_arc_pulse_flag_enabled else 'FLAG OFF'}** (flag={arw_arc_pulse_flag_name} enabled={arw_arc_pulse_flag_enabled} arc={ambient_ramp_why_auto_remap_momentum_arc} reason={ambient_ramp_why_auto_remap_momentum_arc_pulse_signals['reason']})",
        f"- AMBIENT RAMP WHY REC CONF STREAK: **{ambient_ramp_why_recommendation_confidence_streak}** (suppress={str(ambient_ramp_why_recommendation_confidence_streak_signals.get('suppress', False)).upper()} threshold={ambient_ramp_why_recommendation_confidence_streak_signals.get('threshold', 3)} reason={ambient_ramp_why_recommendation_confidence_streak_signals.get('reason', 'n/a')})",
        f"- URGENCY STACK PRUNING REC: **{urgency_stack_pruning_order_recommendation}** ({urgency_stack_pruning_order_recommendation_signals['rationale']}; parityChurn={urgency_stack_pruning_order_recommendation_signals['parityCompactChurn']} fxChurn={urgency_stack_pruning_order_recommendation_signals['urgencyFxChurn']} detailedChurn={urgency_stack_pruning_order_recommendation_signals['urgencyDetailedChurn']} offlineOnly={urgency_stack_pruning_order_recommendation_signals['offlineOnly']})",
        f"- URGENCY STACK RAIL REC: **{urgency_stack_rail_recommendation}** ({urgency_stack_rail_recommendation_signals['rationale']}; railChurn={urgency_stack_rail_recommendation_signals['urgencyStackRailChurn']} railNet={urgency_stack_rail_recommendation_signals['urgencyStackRailNet']} tierChurn={urgency_stack_rail_recommendation_signals['urgencyStackTierChurn']} offlineOnly={urgency_stack_rail_recommendation_signals['offlineOnly']})",
        f"- DMG GLYPH SHAPE REMAP REC: **{dmg_glyph_shape_remap_recommendation}** ({dmg_glyph_shape_remap_recommendation_signals['rationale']}; glyphChurn={dmg_glyph_shape_remap_recommendation_signals['dmgGlyphChurn']} glyphNet={dmg_glyph_shape_remap_recommendation_signals['dmgGlyphNet']} railChurn={dmg_glyph_shape_remap_recommendation_signals['urgencyStackRailChurn']} offlineOnly={dmg_glyph_shape_remap_recommendation_signals['offlineOnly']})",
        f"- DMG GLYPH FX REMAP REC: **{dmg_glyph_fx_remap_recommendation}** ({dmg_glyph_fx_remap_recommendation_signals['rationale']}; fxChurn={dmg_glyph_fx_remap_recommendation_signals['dmgGlyphFxLiveChurn']} fxNet={dmg_glyph_fx_remap_recommendation_signals['dmgGlyphFxLiveNet']} glyphChurn={dmg_glyph_fx_remap_recommendation_signals['dmgGlyphChurn']} offlineOnly={dmg_glyph_fx_remap_recommendation_signals['offlineOnly']})",
        f"- DMG GLYPH FX REMAP CONF: **{dmg_glyph_fx_remap_confidence}** ({dmg_glyph_fx_remap_confidence_signals['rationale']}; churnScore={dmg_glyph_fx_remap_confidence_signals['churnScore']} drift={dmg_glyph_fx_remap_confidence_signals['driftRisk']})",
        f"- DMGNUM LIFE TREND FX PULSE CONF REMAP REC: **{dmgnum_life_trend_fx_pulse_remap_recommendation}** ({dmgnum_life_trend_fx_pulse_remap_recommendation_signals['rationale']}; pulseChurn={dmgnum_life_trend_fx_pulse_remap_recommendation_signals['dmgnumLifeTrendFxPulseChurn']} pulseConfChurn={dmgnum_life_trend_fx_pulse_remap_recommendation_signals['dmgnumLifeTrendFxPulseConfChurn']} pressure={dmgnum_life_trend_fx_pulse_remap_recommendation_signals['pressureBand']} cadence={dmgnum_life_trend_fx_pulse_remap_recommendation_signals['laneCadenceRecency']} offlineOnly={dmgnum_life_trend_fx_pulse_remap_recommendation_signals['offlineOnly']})",
        f"- DMG COMBO WINDOW RETUNE REC: **{combo_window_retune_recommendation}** ({combo_window_retune_recommendation_signals['rationale']}; churn={combo_window_retune_recommendation_signals['comboChurn']} net={combo_window_retune_recommendation_signals['comboNet']:+d} pressure={combo_window_retune_recommendation_signals['pressureBand']} drift={combo_window_retune_recommendation_signals['driftRisk']} cadence={combo_window_retune_recommendation_signals['laneCadenceRecency']} offlineOnly={combo_window_retune_recommendation_signals['offlineOnly']})",
        f"- DCR: **{dmg_combo_retune_alias if dmg_combo_retune_alias_flag_enabled else "FLAG OFF"}** (flag={dmg_combo_retune_alias_flag_name} enabled={dmg_combo_retune_alias_flag_enabled} full={combo_window_retune_recommendation})",
        f"- DMG COMBO WINDOW RETUNE CONF: **{combo_window_retune_confidence}** ({combo_window_retune_confidence_signals['rationale']}; rec={combo_window_retune_confidence_signals['recommendation']} churn={combo_window_retune_confidence_signals['comboChurn']} net={combo_window_retune_confidence_signals['comboNet']:+d} drift={combo_window_retune_confidence_signals['driftRisk']} pressure={combo_window_retune_confidence_signals['pressureBand']} offlineOnly={combo_window_retune_confidence_signals['offlineOnly']})",
        f"- DCRC: **{dmg_combo_retune_conf_alias if dmg_combo_retune_conf_alias_flag_enabled else 'FLAG OFF'}** (flag={dmg_combo_retune_conf_alias_flag_name} enabled={dmg_combo_retune_conf_alias_flag_enabled} full={combo_window_retune_confidence})",
        f"- DMG COMBO CHAIN COACH: **{combo_chain_narrative_coach_line}** ({combo_chain_narrative_coach_line_signals['reason']}; rec={combo_chain_narrative_coach_line_signals['recommendation']} conf={combo_chain_narrative_coach_line_signals['confidence']} pressure={combo_chain_narrative_coach_line_signals['pressureBand']} drift={combo_chain_narrative_coach_line_signals['driftRisk']} cadence={combo_chain_narrative_coach_line_signals['laneCadenceRecency']} offlineOnly={combo_chain_narrative_coach_line_signals['offlineOnly']})",
        f"- DMG COMBO CONF COACH REC: **{combo_confidence_coach_recommendation}** ({combo_confidence_coach_recommendation_signals['reason']}; killHeatVol={combo_confidence_coach_recommendation_signals['killHeatVolatility']} comboChurn={combo_confidence_coach_recommendation_signals['comboChurn']} comboNet={combo_confidence_coach_recommendation_signals['comboNet']:+d} confChurn={combo_confidence_coach_recommendation_signals['comboConfidenceChurn']} confNet={combo_confidence_coach_recommendation_signals['comboConfidenceNet']:+d} pressure={combo_confidence_coach_recommendation_signals['pressureBand']} drift={combo_confidence_coach_recommendation_signals['driftRisk']} offlineOnly={combo_confidence_coach_recommendation_signals['offlineOnly']})",
        f"- DMG COMBO CONF COACH FALLBACK: **{combo_confidence_coach_fallback_narrative}** ({combo_confidence_coach_fallback_narrative_signals['reason']}; streak={combo_confidence_coach_fallback_narrative_signals['recommendationStreak']} streakDelta={combo_confidence_coach_fallback_narrative_signals['recommendationStreakDrift']:+d} regime={combo_confidence_coach_fallback_narrative_signals['volatilityRegime']} killHeatVol={combo_confidence_coach_fallback_narrative_signals['killHeatVolatility']} offlineOnly={combo_confidence_coach_fallback_narrative_signals['offlineOnly']})",
        f"- DCCR: **{dmg_combo_conf_coach_alias if dmg_combo_conf_coach_alias_flag_enabled else 'FLAG OFF'}** (flag={dmg_combo_conf_coach_alias_flag_name} enabled={dmg_combo_conf_coach_alias_flag_enabled} full={combo_confidence_coach_recommendation})",
        f"- DMG COMBO CONF COACH SCENE ARC: **{combo_confidence_coach_scene_arc}** ({combo_confidence_coach_scene_arc_signals['reason']}; rec={combo_confidence_coach_scene_arc_signals['recommendation']} pressure={combo_confidence_coach_scene_arc_signals['pressureBand']} drift={combo_confidence_coach_scene_arc_signals['driftRisk']} offlineOnly={combo_confidence_coach_scene_arc_signals['offlineOnly']})",
        f"- DMG COMBO CONF FX ACCENT: **{combo_confidence_fx_accent}** ({combo_confidence_fx_accent_signals['reason']}; sceneArc={combo_confidence_fx_accent_signals['sceneArc']} regime={combo_confidence_fx_accent_signals['volatilityRegime']} rec={combo_confidence_fx_accent_signals['recommendation']} offlineOnly={combo_confidence_fx_accent_signals['offlineOnly']})",
        f"- DMG COMBO CONF COACH COPY SWAP REC: **{combo_confidence_coach_copy_swap_recommendation}** ({combo_confidence_coach_copy_swap_recommendation_signals['reason']}; prsmcTrend={combo_confidence_coach_copy_swap_recommendation_signals['prsmcTrend']} prsmcChurn={combo_confidence_coach_copy_swap_recommendation_signals['prsmcChurn']} prsmcNet={combo_confidence_coach_copy_swap_recommendation_signals['prsmcNet']:+d} missRisk={combo_confidence_coach_copy_swap_recommendation_signals['laneCadenceMissRisk']} cadenceStatus={combo_confidence_coach_copy_swap_recommendation_signals['laneCadenceStatus']} coach={combo_confidence_coach_copy_swap_recommendation_signals['coachRecommendation']} offlineOnly={combo_confidence_coach_copy_swap_recommendation_signals['offlineOnly']})",
        f"- DCCSR: **{dmg_combo_conf_coach_copy_swap_alias if dmg_combo_conf_coach_copy_swap_alias_flag_enabled else 'FLAG OFF'}** (flag={dmg_combo_conf_coach_copy_swap_alias_flag_name} enabled={dmg_combo_conf_coach_copy_swap_alias_flag_enabled} full={combo_confidence_coach_copy_swap_recommendation})",
        f"- DCCSA: **{dmg_combo_conf_coach_scene_arc_alias if dmg_combo_conf_coach_scene_arc_alias_flag_enabled else 'FLAG OFF'}** (flag={dmg_combo_conf_coach_scene_arc_alias_flag_name} enabled={dmg_combo_conf_coach_scene_arc_alias_flag_enabled} full={combo_confidence_coach_scene_arc})",
        f"- DCCFX: **{dmg_combo_conf_fx_accent_alias if dmg_combo_conf_fx_accent_alias_flag_enabled else 'FLAG OFF'}** (flag={dmg_combo_conf_fx_accent_alias_flag_name} enabled={dmg_combo_conf_fx_accent_alias_flag_enabled} full={combo_confidence_fx_accent})",
        f"- PULSE REMAP MOMENTUM: **{pulse_remap_momentum_recommendation}** ({pulse_remap_momentum_recommendation_signals['rationale']}; rec={pulse_remap_momentum_recommendation_signals['recommendation']} driftRisk={pulse_remap_momentum_recommendation_signals['driftRisk']} pressure={pulse_remap_momentum_recommendation_signals['pressureBand']} cadence={pulse_remap_momentum_recommendation_signals['laneCadenceRecency']} planChurn={pulse_remap_momentum_recommendation_signals['planChurn']} planNet={pulse_remap_momentum_recommendation_signals['planNet']:+d} offlineOnly={pulse_remap_momentum_recommendation_signals['offlineOnly']})",
        f"- PULSE REMAP MOMENTUM Δ: **{pulse_remap_momentum_drift:+d}** ({pulse_remap_momentum_drift_signals['reason']}; current={pulse_remap_momentum_drift_signals['currentMomentum']}({pulse_remap_momentum_drift_signals['currentScore']:+d}) prior={pulse_remap_momentum_drift_signals['priorMomentum']}({pulse_remap_momentum_drift_signals['priorScore']:+d}) loaded={pulse_remap_momentum_drift_signals['priorLoaded']})",
        f"- PULSE REMAP MOMENTUM SUPPRESS: **{pulse_remap_momentum_suppression}** ({pulse_remap_momentum_suppression_signals['reason']}; streak={pulse_remap_momentum_suppression_signals['freezeStreak']} threshold={pulse_remap_momentum_suppression_signals['threshold']} suppress={str(pulse_remap_momentum_suppression_signals['suppress']).upper()} offlineOnly={pulse_remap_momentum_suppression_signals['offlineOnly']})",
        f"- PRMS: **{pulse_remap_momentum_suppression_alias if pulse_remap_momentum_suppression_alias_flag_enabled else 'FLAG OFF'}** (flag={pulse_remap_momentum_suppression_alias_flag_name} enabled={pulse_remap_momentum_suppression_alias_flag_enabled} full={pulse_remap_momentum_suppression})",
        f"- PULSE REMAP SUPPRESS PLAN: **{pulse_remap_suppression_escalation_plan}** ({pulse_remap_suppression_escalation_plan_signals['reason']}; suppression={pulse_remap_suppression_escalation_plan_signals['suppression']} momentum={pulse_remap_suppression_escalation_plan_signals['momentum']} streak={pulse_remap_suppression_escalation_plan_signals['freezeStreak']} driftRisk={pulse_remap_suppression_escalation_plan_signals['driftRisk']} cadence={pulse_remap_suppression_escalation_plan_signals['laneCadenceRecency']} offlineOnly={pulse_remap_suppression_escalation_plan_signals['offlineOnly']})",
        f"- PRSP: **{pulse_remap_suppression_escalation_plan_alias if pulse_remap_suppression_plan_alias_flag_enabled else 'FLAG OFF'}** (flag={pulse_remap_suppression_plan_alias_flag_name} enabled={pulse_remap_suppression_plan_alias_flag_enabled} full={pulse_remap_suppression_escalation_plan})",
        f"- PULSE REMAP SCENE: **{pulse_remap_suppression_scene_flavor}** ({pulse_remap_suppression_scene_flavor_signals['reason']}; plan={pulse_remap_suppression_scene_flavor_signals['suppressionPlan']} driftRisk={pulse_remap_suppression_scene_flavor_signals['driftRisk']} pressure={pulse_remap_suppression_scene_flavor_signals['pressureBand']} cadence={pulse_remap_suppression_scene_flavor_signals['laneCadenceRecency']} offlineOnly={pulse_remap_suppression_scene_flavor_signals['offlineOnly']})",
        f"- PULSE REMAP SCENE CONF: **{pulse_remap_scene_confidence}** ({pulse_remap_scene_confidence_signals['reason']}; plan={pulse_remap_scene_confidence_signals['suppressionPlan']} driftRisk={pulse_remap_scene_confidence_signals['driftRisk']} pressure={pulse_remap_scene_confidence_signals['pressureBand']} offlineOnly={pulse_remap_scene_confidence_signals['offlineOnly']})",
        f"- PULSE REMAP SCENE MICROLINE: **{pulse_remap_suppression_scene_microline}** ({pulse_remap_suppression_scene_microline_signals['reason']}; plan={pulse_remap_suppression_scene_microline_signals['suppressionPlan']} flavor={pulse_remap_suppression_scene_microline_signals['sceneFlavor']} conf={pulse_remap_suppression_scene_microline_signals['sceneConfidence']} cadence={pulse_remap_suppression_scene_microline_signals['laneCadenceRecency']} memory={pulse_remap_suppression_scene_microline_signals['cadenceMemory']} offlineOnly={pulse_remap_suppression_scene_microline_signals['offlineOnly']})",
        f"- PULSE REMAP SCENE MICROLINE VARIANT PACK: **{pulse_remap_scene_microline_variant_pack['selectedMode']}** (selected={pulse_remap_scene_microline_variant_pack['selected']} | primary={pulse_remap_scene_microline_variant_pack['primary']} | alt={pulse_remap_scene_microline_variant_pack['alternate']} | fallback={pulse_remap_scene_microline_variant_pack['fallback']} | reason={pulse_remap_scene_microline_variant_pack_signals['reason']} offlineOnly={pulse_remap_scene_microline_variant_pack_signals['offlineOnly']})",
        f"- PULSE REMAP SCENE MICROLINE STYLE POLICY: **{pulse_remap_scene_microline_style_diversification_policy}** ({pulse_remap_scene_microline_style_diversification_policy_signals['reason']}; plan={pulse_remap_scene_microline_style_diversification_policy_signals['suppressionPlan']} conf={pulse_remap_scene_microline_style_diversification_policy_signals['sceneConfidence']} cadence={pulse_remap_scene_microline_style_diversification_policy_signals['laneCadenceRecency']} trend={pulse_remap_scene_microline_style_diversification_policy_signals['cadenceTrend']} volatility={pulse_remap_scene_microline_style_diversification_policy_signals['cadenceVolatility']} prior={pulse_remap_scene_microline_style_diversification_policy_signals['priorNet']:+d} current={pulse_remap_scene_microline_style_diversification_policy_signals['currentNet']:+d} offlineOnly={pulse_remap_scene_microline_style_diversification_policy_signals['offlineOnly']})",
        f"- PULSE REMAP SCENE MICROLINE STYLE POLICY SMOOTH: **{pulse_remap_scene_microline_style_policy_smoothed}** ({pulse_remap_scene_microline_style_policy_smoothed_signals['reason']}; current={pulse_remap_scene_microline_style_policy_smoothed_signals['currentPolicy']} prior={pulse_remap_scene_microline_style_policy_smoothed_signals['priorPolicy']} volatility={pulse_remap_scene_microline_style_policy_smoothed_signals['cadenceVolatility']} loaded={pulse_remap_scene_microline_style_policy_smoothed_signals['priorLoaded']} offlineOnly={pulse_remap_scene_microline_style_policy_smoothed_signals['offlineOnly']})",
        f"- PULSE REMAP SCENE MICROLINE STYLE POSTURE: **{pulse_remap_scene_microline_style_policy_posture_hook}** ({pulse_remap_scene_microline_style_policy_posture_hook_signals['reason']}; policy={pulse_remap_scene_microline_style_policy_posture_hook_signals['smoothedPolicy']} trend={pulse_remap_scene_microline_style_policy_posture_hook_signals['styleTrend']} current={pulse_remap_scene_microline_style_policy_posture_hook_signals['currentNet']:+d} prior={pulse_remap_scene_microline_style_policy_posture_hook_signals['priorNet']:+d} cadence={pulse_remap_scene_microline_style_policy_posture_hook_signals['laneCadenceRecency']} offlineOnly={pulse_remap_scene_microline_style_policy_posture_hook_signals['offlineOnly']})",
        f"- PRSMPP: **{pulse_remap_scene_microline_style_posture_alias if pulse_remap_scene_microline_style_posture_alias_flag_enabled else 'FLAG OFF'}** (flag={pulse_remap_scene_microline_style_posture_alias_flag_name} enabled={pulse_remap_scene_microline_style_posture_alias_flag_enabled} posture={pulse_remap_scene_microline_style_policy_posture_hook})",
        f"- PULSE REMAP SCENE FX GLINT: **{pulse_remap_scene_fx_glint}** ({pulse_remap_scene_fx_glint_signals['reason']}; posture={pulse_remap_scene_fx_glint_signals['stylePosture']} warning={pulse_remap_scene_fx_glint_signals['suppressionWarning']} conf={pulse_remap_scene_fx_glint_signals['sceneConfidence']} offlineOnly={pulse_remap_scene_fx_glint_signals['offlineOnly']})",
        f"- PRSFX: **{pulse_remap_scene_fx_glint_alias if pulse_remap_scene_fx_glint_alias_flag_enabled else 'FLAG OFF'}** (flag={pulse_remap_scene_fx_glint_alias_flag_name} enabled={pulse_remap_scene_fx_glint_alias_flag_enabled} full={pulse_remap_scene_fx_glint})",
        f"- PULSE REMAP SCENE COPY PALETTE REC: **{pulse_remap_scene_copy_palette_recommendation}** ({pulse_remap_scene_copy_palette_recommendation_signals['reason']}; flavor={pulse_remap_scene_copy_palette_recommendation_signals['sceneFlavor']} glint={pulse_remap_scene_copy_palette_recommendation_signals['sceneFxGlint']} posture={pulse_remap_scene_copy_palette_recommendation_signals['stylePosture']} conf={pulse_remap_scene_copy_palette_recommendation_signals['sceneConfidence']} offlineOnly={pulse_remap_scene_copy_palette_recommendation_signals['offlineOnly']})",
        f"- PRSCP: **{pulse_remap_scene_copy_palette_recommendation_alias if pulse_remap_scene_copy_palette_recommendation_alias_flag_enabled else 'FLAG OFF'}** (flag={pulse_remap_scene_copy_palette_recommendation_alias_flag_name} enabled={pulse_remap_scene_copy_palette_recommendation_alias_flag_enabled} palette={pulse_remap_scene_copy_palette_recommendation})",
        f"- PRSMP: **{pulse_remap_scene_microline_style_policy_alias if pulse_remap_scene_microline_style_policy_alias_flag_enabled else 'FLAG OFF'}** (flag={pulse_remap_scene_microline_style_policy_alias_flag_name} enabled={pulse_remap_scene_microline_style_policy_alias_flag_enabled} full={pulse_remap_scene_microline_style_diversification_policy})",
        f"- PRSMV: **{pulse_remap_scene_microline_variant_pack_selection_alias if pulse_remap_scene_microline_variant_pack_selection_alias_flag_enabled else 'FLAG OFF'}** (flag={pulse_remap_scene_microline_variant_pack_selection_alias_flag_name} enabled={pulse_remap_scene_microline_variant_pack_selection_alias_flag_enabled} full={pulse_remap_scene_microline_variant_pack['selectedMode']})",
        f"- PULSE REMAP SCENE MICROLINE CADENCE: **{pulse_remap_scene_microline_cadence}** ({pulse_remap_scene_microline_cadence_signals['reason']}; plan={pulse_remap_scene_microline_cadence_signals['suppressionPlan']} conf={pulse_remap_scene_microline_cadence_signals['sceneConfidence']} cadence={pulse_remap_scene_microline_cadence_signals['laneCadenceRecency']} trend={pulse_remap_scene_microline_cadence_signals['cadenceTrend']} offlineOnly={pulse_remap_scene_microline_cadence_signals['offlineOnly']})",
        f"- PRSMC: **{pulse_remap_scene_microline_cadence_alias if pulse_remap_scene_microline_cadence_alias_flag_enabled else 'FLAG OFF'}** (flag={pulse_remap_scene_microline_cadence_alias_flag_name} enabled={pulse_remap_scene_microline_cadence_alias_flag_enabled} cadence={pulse_remap_scene_microline_cadence})",
        f"- PRPW: **{pulse_remap_suppression_posture_warning_alias if pulse_remap_suppression_posture_warning_flag_enabled else 'FLAG OFF'}** (flag={pulse_remap_suppression_posture_warning_flag_name} enabled={pulse_remap_suppression_posture_warning_flag_enabled} posture={pulse_remap_suppression_posture_warning}; reason={pulse_remap_suppression_posture_warning_signals['reason']})",
        f"- PRM: **{pulse_remap_momentum_alias if pulse_remap_momentum_alias_flag_enabled else 'FLAG OFF'}** (flag={pulse_remap_momentum_alias_flag_name} enabled={pulse_remap_momentum_alias_flag_enabled})",
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
        f"- ALT STEP CONF Δ: **{alt_step_confidence_drift:+d}** ({alt_step_confidence_drift_signals['reason']}; current={alt_step_confidence_drift_signals['currentAltStepConfidence']}({alt_step_confidence_drift_signals['currentScore']}) prior={alt_step_confidence_drift_signals['priorAltStepConfidence']}({alt_step_confidence_drift_signals['priorScore']}) loaded={alt_step_confidence_drift_signals['priorLoaded']})",
        f"- ALT STEP WHY CONF Δ: **{alt_step_why_confidence_drift:+d}** ({alt_step_why_confidence_drift_signals['reason']}; why={alt_step_why_confidence_drift_signals['currentAltStepWhy']} current={alt_step_why_confidence_drift_signals['currentAltStepWhyConfidence']}({alt_step_why_confidence_drift_signals['currentScore']}) prior={alt_step_why_confidence_drift_signals['priorAltStepWhyConfidence']}({alt_step_why_confidence_drift_signals['priorScore']}) loaded={alt_step_why_confidence_drift_signals['priorLoaded']})",
        f"- ALT WHY GLYPH Δ: **{alt_why_glyph_drift:+d}** ({alt_why_glyph_drift_signals['reason']}; currentNet={alt_why_glyph_drift_signals['currentAltWhyGlyphNet']} priorNet={alt_why_glyph_drift_signals['priorAltWhyGlyphNet']} loaded={alt_why_glyph_drift_signals['priorLoaded']})",
        f"- ALT WHY GLYPH MODE Δ: **{alt_why_glyph_mode_drift:+d}** ({alt_why_glyph_mode_drift_signals['reason']}; currentNet={alt_why_glyph_mode_drift_signals['currentAltWhyGlyphModeNet']} priorNet={alt_why_glyph_mode_drift_signals['priorAltWhyGlyphModeNet']} loaded={alt_why_glyph_mode_drift_signals['priorLoaded']})",
        f"- ALT WHY GLYPH MODE CONF: **{alt_why_glyph_mode_confidence}** ({alt_why_glyph_mode_confidence_signals['reason']}; drift={alt_why_glyph_mode_confidence_signals['altWhyGlyphModeDrift']:+d} |Δ|={alt_why_glyph_mode_confidence_signals['absAltWhyGlyphModeDrift']} currentNet={alt_why_glyph_mode_confidence_signals['currentAltWhyGlyphModeNet']} priorNet={alt_why_glyph_mode_confidence_signals['priorAltWhyGlyphModeNet']} loaded={alt_why_glyph_mode_confidence_signals['priorLoaded']})",
        f"- ALT WHY GLYPH MODE CONF Δ: **{alt_why_glyph_mode_confidence_drift:+d}** ({alt_why_glyph_mode_confidence_drift_signals['reason']}; current={alt_why_glyph_mode_confidence_drift_signals['currentAltWhyGlyphModeConfidence']}({alt_why_glyph_mode_confidence_drift_signals['currentScore']}) prior={alt_why_glyph_mode_confidence_drift_signals['priorAltWhyGlyphModeConfidence']}({alt_why_glyph_mode_confidence_drift_signals['priorScore']}) loaded={alt_why_glyph_mode_confidence_drift_signals['priorLoaded']})",
        f"- ALT WHY GLYPH MODE CONF WHY: **{alt_why_glyph_mode_confidence_why}** ({alt_why_glyph_mode_confidence_why_signals['reason']}; flag={alt_why_glyph_mode_confidence_why_signals['flagName']} enabled={alt_why_glyph_mode_confidence_why_signals['flagEnabled']} conf={alt_why_glyph_mode_confidence_why_signals['altWhyGlyphModeConfidence']} drift={alt_why_glyph_mode_confidence_why_signals['altWhyGlyphModeConfidenceDrift']:+d} |Δ|={alt_why_glyph_mode_confidence_why_signals['absAltWhyGlyphModeDrift']} net={alt_why_glyph_mode_confidence_why_signals['currentAltWhyGlyphModeNet']} loaded={alt_why_glyph_mode_confidence_why_signals['priorLoaded']})",
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
        f"- ROUTE PULSE LINK MODE FIT Δ: **{route_pulse_link_mode_fit_drift:+d}** ({route_pulse_link_mode_fit_drift_signals['reason']}; current={route_pulse_link_mode_fit_drift_signals['currentFit']}({route_pulse_link_mode_fit_drift_signals['currentScore']}) prior={route_pulse_link_mode_fit_drift_signals['priorFit']}({route_pulse_link_mode_fit_drift_signals['priorScore']}) loaded={route_pulse_link_mode_fit_drift_signals['priorLoaded']})",
        f"- ROUTE PULSE TOKEN PRIORITY: **{route_pulse_token_priority}** ({route_pulse_token_priority_signals['reason']}; configured={route_pulse_token_priority_signals['configuredMode']} drift={route_pulse_token_priority_signals['routePulseLinkModeFitDrift']:+d} prior={route_pulse_token_priority_signals['priorMode']} loaded={route_pulse_token_priority_signals['priorLoaded']} guard={route_pulse_token_priority_signals['guardHeld']})",
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
        f"- VTW FAMILY CHURN: **net {token_family_totals['vibeTrailWhyAlias']['net']:+d}** (added={token_family_totals['vibeTrailWhyAlias']['added']} removed={token_family_totals['vibeTrailWhyAlias']['removed']} churn={token_family_totals['vibeTrailWhyAlias']['churn']} coverage={token_family_totals['vibeTrailWhyAlias']['coverage']})",
        f"- VTWC FAMILY CHURN: **net {token_family_totals['vibeTrailWhyConfidenceAlias']['net']:+d}** (added={token_family_totals['vibeTrailWhyConfidenceAlias']['added']} removed={token_family_totals['vibeTrailWhyConfidenceAlias']['removed']} churn={token_family_totals['vibeTrailWhyConfidenceAlias']['churn']} coverage={token_family_totals['vibeTrailWhyConfidenceAlias']['coverage']})",
        f"- VTCW FAMILY CHURN: **net {token_family_totals['vibeTrailWhyConfidenceWhyAlias']['net']:+d}** (added={token_family_totals['vibeTrailWhyConfidenceWhyAlias']['added']} removed={token_family_totals['vibeTrailWhyConfidenceWhyAlias']['removed']} churn={token_family_totals['vibeTrailWhyConfidenceWhyAlias']['churn']} coverage={token_family_totals['vibeTrailWhyConfidenceWhyAlias']['coverage']})",
        f"- VTCWC FAMILY CHURN: **net {token_family_totals['vibeTrailWhyConfidenceWhyConfidenceAlias']['net']:+d}** (added={token_family_totals['vibeTrailWhyConfidenceWhyConfidenceAlias']['added']} removed={token_family_totals['vibeTrailWhyConfidenceWhyConfidenceAlias']['removed']} churn={token_family_totals['vibeTrailWhyConfidenceWhyConfidenceAlias']['churn']} coverage={token_family_totals['vibeTrailWhyConfidenceWhyConfidenceAlias']['coverage']})",
        f"- VTA FAMILY CHURN: **net {token_family_totals['vibeTrailArcAlias']['net']:+d}** (added={token_family_totals['vibeTrailArcAlias']['added']} removed={token_family_totals['vibeTrailArcAlias']['removed']} churn={token_family_totals['vibeTrailArcAlias']['churn']} coverage={token_family_totals['vibeTrailArcAlias']['coverage']})",
        f"- AMBIENT RAMP CONF FAMILY CHURN: **net {token_family_totals['ambientRampConfidenceAlias']['net']:+d}** (added={token_family_totals['ambientRampConfidenceAlias']['added']} removed={token_family_totals['ambientRampConfidenceAlias']['removed']} churn={token_family_totals['ambientRampConfidenceAlias']['churn']} coverage={token_family_totals['ambientRampConfidenceAlias']['coverage']})",
        f"- AMBIENT RAMP WHY FAMILY CHURN: **net {token_family_totals['ambientRampWhyAlias']['net']:+d}** (added={token_family_totals['ambientRampWhyAlias']['added']} removed={token_family_totals['ambientRampWhyAlias']['removed']} churn={token_family_totals['ambientRampWhyAlias']['churn']} coverage={token_family_totals['ambientRampWhyAlias']['coverage']})",
        f"- ARW AUTO PLAN FAMILY CHURN: **net {token_family_totals['ambientRampWhyAutoRemapPlanAlias']['net']:+d}** (added={token_family_totals['ambientRampWhyAutoRemapPlanAlias']['added']} removed={token_family_totals['ambientRampWhyAutoRemapPlanAlias']['removed']} churn={token_family_totals['ambientRampWhyAutoRemapPlanAlias']['churn']} coverage={token_family_totals['ambientRampWhyAutoRemapPlanAlias']['coverage']} drift={ambient_ramp_why_auto_remap_plan_drift:+d})",
        f"- ARW APC FAMILY CHURN: **net {token_family_totals['ambientRampWhyAutoRemapConfidenceBandAlias']['net']:+d}** (added={token_family_totals['ambientRampWhyAutoRemapConfidenceBandAlias']['added']} removed={token_family_totals['ambientRampWhyAutoRemapConfidenceBandAlias']['removed']} churn={token_family_totals['ambientRampWhyAutoRemapConfidenceBandAlias']['churn']} coverage={token_family_totals['ambientRampWhyAutoRemapConfidenceBandAlias']['coverage']})",
        f"- ARW AUTO PLAN CONF MOMENTUM FAMILY CHURN: **net {token_family_totals['ambientRampWhyAutoRemapConfidenceMomentumAlias']['net']:+d}** (added={token_family_totals['ambientRampWhyAutoRemapConfidenceMomentumAlias']['added']} removed={token_family_totals['ambientRampWhyAutoRemapConfidenceMomentumAlias']['removed']} churn={token_family_totals['ambientRampWhyAutoRemapConfidenceMomentumAlias']['churn']} coverage={token_family_totals['ambientRampWhyAutoRemapConfidenceMomentumAlias']['coverage']})",
        f"- ARW MOMENTUM FAMILY CHURN: **net {token_family_totals['ambientRampWhyAutoRemapConfidenceMomentumCompactAlias']['net']:+d}** (added={token_family_totals['ambientRampWhyAutoRemapConfidenceMomentumCompactAlias']['added']} removed={token_family_totals['ambientRampWhyAutoRemapConfidenceMomentumCompactAlias']['removed']} churn={token_family_totals['ambientRampWhyAutoRemapConfidenceMomentumCompactAlias']['churn']} coverage={token_family_totals['ambientRampWhyAutoRemapConfidenceMomentumCompactAlias']['coverage']})",
        f"- ARW MOMENTUM ARC FAMILY CHURN: **net {token_family_totals['ambientRampWhyAutoRemapMomentumArcAlias']['net']:+d}** (added={token_family_totals['ambientRampWhyAutoRemapMomentumArcAlias']['added']} removed={token_family_totals['ambientRampWhyAutoRemapMomentumArcAlias']['removed']} churn={token_family_totals['ambientRampWhyAutoRemapMomentumArcAlias']['churn']} coverage={token_family_totals['ambientRampWhyAutoRemapMomentumArcAlias']['coverage']})",
        f"- ARW ARC PULSE FAMILY CHURN: **net {token_family_totals['ambientRampWhyAutoRemapMomentumArcPulseAlias']['net']:+d}** (added={token_family_totals['ambientRampWhyAutoRemapMomentumArcPulseAlias']['added']} removed={token_family_totals['ambientRampWhyAutoRemapMomentumArcPulseAlias']['removed']} churn={token_family_totals['ambientRampWhyAutoRemapMomentumArcPulseAlias']['churn']} coverage={token_family_totals['ambientRampWhyAutoRemapMomentumArcPulseAlias']['coverage']})",
        f"- ARW AUTO PLAN CANDIDATE SUPPRESS: **{str(ambient_ramp_why_auto_remap_plan_signals.get('candidateSuppressed', False)).upper()}** (streak={ambient_ramp_why_auto_remap_plan_signals.get('confidenceStreak', 1)} threshold={ambient_ramp_why_recommendation_confidence_streak_signals.get('threshold', 3)})",
        f"- PULSE HEAT FX FAMILY CHURN: **net {token_family_totals['pulseHeatFxAlias']['net']:+d}** (added={token_family_totals['pulseHeatFxAlias']['added']} removed={token_family_totals['pulseHeatFxAlias']['removed']} churn={token_family_totals['pulseHeatFxAlias']['churn']} coverage={token_family_totals['pulseHeatFxAlias']['coverage']})",
        f"- ROUTE GLOW FX FAMILY CHURN: **net {token_family_totals['routeGlowFxAlias']['net']:+d}** (added={token_family_totals['routeGlowFxAlias']['added']} removed={token_family_totals['routeGlowFxAlias']['removed']} churn={token_family_totals['routeGlowFxAlias']['churn']} coverage={token_family_totals['routeGlowFxAlias']['coverage']})",
        f"- ROUTE GLOW CONF FAMILY CHURN: **net {token_family_totals['routeGlowConfidenceAlias']['net']:+d}** (added={token_family_totals['routeGlowConfidenceAlias']['added']} removed={token_family_totals['routeGlowConfidenceAlias']['removed']} churn={token_family_totals['routeGlowConfidenceAlias']['churn']} coverage={token_family_totals['routeGlowConfidenceAlias']['coverage']})",
        f"- ROUTE GLOW FX CONF FAMILY CHURN: **net {token_family_totals['routeGlowFxConfidenceAlias']['net']:+d}** (added={token_family_totals['routeGlowFxConfidenceAlias']['added']} removed={token_family_totals['routeGlowFxConfidenceAlias']['removed']} churn={token_family_totals['routeGlowFxConfidenceAlias']['churn']} coverage={token_family_totals['routeGlowFxConfidenceAlias']['coverage']})",
        f"- ROUTE GLOW FX CONF WHY FAMILY CHURN: **net {token_family_totals['routeGlowFxConfidenceWhyAlias']['net']:+d}** (added={token_family_totals['routeGlowFxConfidenceWhyAlias']['added']} removed={token_family_totals['routeGlowFxConfidenceWhyAlias']['removed']} churn={token_family_totals['routeGlowFxConfidenceWhyAlias']['churn']} coverage={token_family_totals['routeGlowFxConfidenceWhyAlias']['coverage']})",
        f"- ROUTE GLOW FX CONF WHY RAIL FAMILY CHURN: **net {token_family_totals['routeGlowFxConfidenceWhyRailAlias']['net']:+d}** (added={token_family_totals['routeGlowFxConfidenceWhyRailAlias']['added']} removed={token_family_totals['routeGlowFxConfidenceWhyRailAlias']['removed']} churn={token_family_totals['routeGlowFxConfidenceWhyRailAlias']['churn']} coverage={token_family_totals['routeGlowFxConfidenceWhyRailAlias']['coverage']})",
        f"- ROUTE GLOW FX CONF WHY RAIL MODE FAMILY CHURN: **net {token_family_totals['routeGlowFxConfidenceWhyRailMode']['net']:+d}** (added={token_family_totals['routeGlowFxConfidenceWhyRailMode']['added']} removed={token_family_totals['routeGlowFxConfidenceWhyRailMode']['removed']} churn={token_family_totals['routeGlowFxConfidenceWhyRailMode']['churn']} coverage={token_family_totals['routeGlowFxConfidenceWhyRailMode']['coverage']})",
        f"- ROUTE GLOW FX CONF WHY RAIL INTENSITY FAMILY CHURN: **net {token_family_totals['routeGlowFxConfidenceWhyRailIntensity']['net']:+d}** (added={token_family_totals['routeGlowFxConfidenceWhyRailIntensity']['added']} removed={token_family_totals['routeGlowFxConfidenceWhyRailIntensity']['removed']} churn={token_family_totals['routeGlowFxConfidenceWhyRailIntensity']['churn']} coverage={token_family_totals['routeGlowFxConfidenceWhyRailIntensity']['coverage']})",
        f"- RGFXWRI WHY FAMILY CHURN: **net {token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhy']['net']:+d}** (added={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhy']['added']} removed={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhy']['removed']} churn={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhy']['churn']} coverage={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhy']['coverage']})",
        f"- RGFXWRI WHY CONF FAMILY CHURN: **net {token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceAlias']['net']:+d}** (added={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceAlias']['added']} removed={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceAlias']['removed']} churn={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceAlias']['churn']} coverage={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceAlias']['coverage']})",
        f"- RGFXWRIU URGENCY FAMILY CHURN: **net {token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyAlias']['net']:+d}** (added={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyAlias']['added']} removed={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyAlias']['removed']} churn={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyAlias']['churn']} coverage={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyAlias']['coverage']})",
        f"- RGFXWRIUP URGENCY PARITY COMPACT FAMILY CHURN: **net {token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyParityCompactAlias']['net']:+d}** (added={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyParityCompactAlias']['added']} removed={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyParityCompactAlias']['removed']} churn={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyParityCompactAlias']['churn']} coverage={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyParityCompactAlias']['coverage']})",
        f"- URGENCY PARITY LABEL FAMILY CHURN: **net {token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyDetailed']['net']:+d}** (added={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyDetailed']['added']} removed={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyDetailed']['removed']} churn={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyDetailed']['churn']} coverage={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyDetailed']['coverage']})",
        f"- RGFXWRIUFX URGENCY FX FAMILY CHURN: **net {token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyFxAlias']['net']:+d}** (added={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyFxAlias']['added']} removed={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyFxAlias']['removed']} churn={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyFxAlias']['churn']} coverage={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyFxAlias']['coverage']})",
        f"- URG STACK FAMILY CHURN: **net {token_family_totals['urgencyStackTierAlias']['net']:+d}** (added={token_family_totals['urgencyStackTierAlias']['added']} removed={token_family_totals['urgencyStackTierAlias']['removed']} churn={token_family_totals['urgencyStackTierAlias']['churn']} coverage={token_family_totals['urgencyStackTierAlias']['coverage']})",
        f"- URG STACK RAIL FAMILY CHURN: **net {token_family_totals['urgencyStackRailAlias']['net']:+d}** (added={token_family_totals['urgencyStackRailAlias']['added']} removed={token_family_totals['urgencyStackRailAlias']['removed']} churn={token_family_totals['urgencyStackRailAlias']['churn']} coverage={token_family_totals['urgencyStackRailAlias']['coverage']})",
        f"- DMGNUM STACK CAP FAMILY CHURN: **net {token_family_totals['dmgnumStackCapAlias']['net']:+d}** (added={token_family_totals['dmgnumStackCapAlias']['added']} removed={token_family_totals['dmgnumStackCapAlias']['removed']} churn={token_family_totals['dmgnumStackCapAlias']['churn']} coverage={token_family_totals['dmgnumStackCapAlias']['coverage']})",
        f"- DMGNUM LIFE FAMILY CHURN: **net {token_family_totals['dmgnumLifeAlias']['net']:+d}** (added={token_family_totals['dmgnumLifeAlias']['added']} removed={token_family_totals['dmgnumLifeAlias']['removed']} churn={token_family_totals['dmgnumLifeAlias']['churn']} coverage={token_family_totals['dmgnumLifeAlias']['coverage']})",
        f"- DMGNUM LIFE CONF FAMILY CHURN: **net {token_family_totals['dmgnumLifeConfidenceAlias']['net']:+d}** (added={token_family_totals['dmgnumLifeConfidenceAlias']['added']} removed={token_family_totals['dmgnumLifeConfidenceAlias']['removed']} churn={token_family_totals['dmgnumLifeConfidenceAlias']['churn']} coverage={token_family_totals['dmgnumLifeConfidenceAlias']['coverage']})",
        f"- DMGNUM LIFE CONF Δ FAMILY CHURN: **net {token_family_totals['dmgnumLifeConfidenceDeltaAlias']['net']:+d}** (added={token_family_totals['dmgnumLifeConfidenceDeltaAlias']['added']} removed={token_family_totals['dmgnumLifeConfidenceDeltaAlias']['removed']} churn={token_family_totals['dmgnumLifeConfidenceDeltaAlias']['churn']} coverage={token_family_totals['dmgnumLifeConfidenceDeltaAlias']['coverage']})",
        f"- DMGNUM LIFE TREND FAMILY CHURN: **net {token_family_totals['dmgnumLifeTrendAlias']['net']:+d}** (added={token_family_totals['dmgnumLifeTrendAlias']['added']} removed={token_family_totals['dmgnumLifeTrendAlias']['removed']} churn={token_family_totals['dmgnumLifeTrendAlias']['churn']} coverage={token_family_totals['dmgnumLifeTrendAlias']['coverage']})",
        f"- DMGNUM LIFE TREND FX PULSE FAMILY CHURN: **net {token_family_totals['dmgnumLifeTrendFxPulseAlias']['net']:+d}** (added={token_family_totals['dmgnumLifeTrendFxPulseAlias']['added']} removed={token_family_totals['dmgnumLifeTrendFxPulseAlias']['removed']} churn={token_family_totals['dmgnumLifeTrendFxPulseAlias']['churn']} coverage={token_family_totals['dmgnumLifeTrendFxPulseAlias']['coverage']})",
        f"- DMGNUM LIFE TREND FX PULSE CONF FAMILY CHURN: **net {token_family_totals['dmgnumLifeTrendFxPulseConfidenceAlias']['net']:+d}** (added={token_family_totals['dmgnumLifeTrendFxPulseConfidenceAlias']['added']} removed={token_family_totals['dmgnumLifeTrendFxPulseConfidenceAlias']['removed']} churn={token_family_totals['dmgnumLifeTrendFxPulseConfidenceAlias']['churn']} coverage={token_family_totals['dmgnumLifeTrendFxPulseConfidenceAlias']['coverage']})",
        f"- DMGNUM LIFE TREND FX PULSE REMAP PLAN FAMILY CHURN: **net {token_family_totals['dmgnumLifeTrendFxPulseRemapPlanAlias']['net']:+d}** (added={token_family_totals['dmgnumLifeTrendFxPulseRemapPlanAlias']['added']} removed={token_family_totals['dmgnumLifeTrendFxPulseRemapPlanAlias']['removed']} churn={token_family_totals['dmgnumLifeTrendFxPulseRemapPlanAlias']['churn']} coverage={token_family_totals['dmgnumLifeTrendFxPulseRemapPlanAlias']['coverage']})",
        f"- DMG COMBO FAMILY CHURN: **net {token_family_totals['dmgComboAlias']['net']:+d}** (added={token_family_totals['dmgComboAlias']['added']} removed={token_family_totals['dmgComboAlias']['removed']} churn={token_family_totals['dmgComboAlias']['churn']} coverage={token_family_totals['dmgComboAlias']['coverage']})",
        f"- DMG COMBO CONF FAMILY CHURN: **net {token_family_totals['dmgComboConfidenceAlias']['net']:+d}** (added={token_family_totals['dmgComboConfidenceAlias']['added']} removed={token_family_totals['dmgComboConfidenceAlias']['removed']} churn={token_family_totals['dmgComboConfidenceAlias']['churn']} coverage={token_family_totals['dmgComboConfidenceAlias']['coverage']})",
        f"- DMG COMBO RETUNE + DCR FAMILY CHURN: **net {token_family_totals['dmgComboRetuneAlias']['net']:+d}** (added={token_family_totals['dmgComboRetuneAlias']['added']} removed={token_family_totals['dmgComboRetuneAlias']['removed']} churn={token_family_totals['dmgComboRetuneAlias']['churn']} coverage={token_family_totals['dmgComboRetuneAlias']['coverage']})",
        f"- DMG COMBO RETUNE CONF + DCRC FAMILY CHURN: **net {token_family_totals['dmgComboRetuneConfidenceAlias']['net']:+d}** (added={token_family_totals['dmgComboRetuneConfidenceAlias']['added']} removed={token_family_totals['dmgComboRetuneConfidenceAlias']['removed']} churn={token_family_totals['dmgComboRetuneConfidenceAlias']['churn']} coverage={token_family_totals['dmgComboRetuneConfidenceAlias']['coverage']})",
        f"- DMG COMBO CHAIN COACH FAMILY CHURN: **net {token_family_totals['dmgComboChainCoachAlias']['net']:+d}** (added={token_family_totals['dmgComboChainCoachAlias']['added']} removed={token_family_totals['dmgComboChainCoachAlias']['removed']} churn={token_family_totals['dmgComboChainCoachAlias']['churn']} coverage={token_family_totals['dmgComboChainCoachAlias']['coverage']})",
        f"- DMG COMBO CONF COACH REC + DCCR FAMILY CHURN: **net {token_family_totals['dmgComboConfidenceCoachAlias']['net']:+d}** (added={token_family_totals['dmgComboConfidenceCoachAlias']['added']} removed={token_family_totals['dmgComboConfidenceCoachAlias']['removed']} churn={token_family_totals['dmgComboConfidenceCoachAlias']['churn']} coverage={token_family_totals['dmgComboConfidenceCoachAlias']['coverage']})",
        f"- DCCSA FAMILY CHURN: **net {token_family_totals['dmgComboConfidenceCoachSceneArcAlias']['net']:+d}** (added={token_family_totals['dmgComboConfidenceCoachSceneArcAlias']['added']} removed={token_family_totals['dmgComboConfidenceCoachSceneArcAlias']['removed']} churn={token_family_totals['dmgComboConfidenceCoachSceneArcAlias']['churn']} coverage={token_family_totals['dmgComboConfidenceCoachSceneArcAlias']['coverage']})",
        f"- DCCFX FAMILY CHURN: **net {token_family_totals['dmgComboConfidenceFxAccentAlias']['net']:+d}** (added={token_family_totals['dmgComboConfidenceFxAccentAlias']['added']} removed={token_family_totals['dmgComboConfidenceFxAccentAlias']['removed']} churn={token_family_totals['dmgComboConfidenceFxAccentAlias']['churn']} coverage={token_family_totals['dmgComboConfidenceFxAccentAlias']['coverage']})",
        f"- DCCFX FAMILY TREND: **{combo_confidence_fx_accent_family_trend_signals['trend']}** (Δnet={combo_confidence_fx_accent_family_trend_drift:+d} currentNet={combo_confidence_fx_accent_family_trend_signals['currentNet']:+d} priorNet={combo_confidence_fx_accent_family_trend_signals['priorNet']:+d} loaded={combo_confidence_fx_accent_family_trend_signals['priorLoaded']} reason={combo_confidence_fx_accent_family_trend_signals['reason']})",
        f"- DCCFX TREND HYS: **{combo_confidence_fx_accent_family_trend_signals['trendHysteresisRecommendation']} / {combo_confidence_fx_accent_family_trend_signals['trendHysteresisConfidence']}** (reason={combo_confidence_fx_accent_family_trend_signals['trendHysteresisRecommendationReason']} confReason={combo_confidence_fx_accent_family_trend_signals['trendHysteresisConfidenceReason']} regime={combo_confidence_fx_accent_family_trend_signals['volatilityRegime']} thr={combo_confidence_fx_accent_family_trend_signals['hysteresisThreshold']} rawDrift={combo_confidence_fx_accent_family_trend_signals['rawDrift']:+d} applied={combo_confidence_fx_accent_family_trend_signals['hysteresisApplied']} offlineOnly={combo_confidence_fx_accent_family_trend_signals['offlineOnly']})",
        f"- DCCFXT: **{dmg_combo_conf_fx_accent_trend_alias if dmg_combo_conf_fx_accent_trend_alias_flag_enabled else 'FLAG OFF'}** (flag={dmg_combo_conf_fx_accent_trend_alias_flag_name} enabled={dmg_combo_conf_fx_accent_trend_alias_flag_enabled} trend={combo_confidence_fx_accent_trend})",
        f"- DCCFXH: **{dmg_combo_conf_fx_accent_trend_hys_alias if dmg_combo_conf_fx_accent_trend_hys_alias_flag_enabled else 'FLAG OFF'}** (flag={dmg_combo_conf_fx_accent_trend_hys_alias_flag_name} enabled={dmg_combo_conf_fx_accent_trend_hys_alias_flag_enabled} rec={combo_confidence_fx_accent_family_trend_signals['trendHysteresisRecommendation']} conf={combo_confidence_fx_accent_family_trend_signals['trendHysteresisConfidence']})",
        f"- DCCFXV: **{dmg_combo_conf_fx_accent_volatility_alias if dmg_combo_conf_fx_accent_volatility_alias_flag_enabled else 'FLAG OFF'}** (flag={dmg_combo_conf_fx_accent_volatility_alias_flag_name} enabled={dmg_combo_conf_fx_accent_volatility_alias_flag_enabled} regime={combo_confidence_fx_accent_signals['volatilityRegime']})",
        f"- DCCFXV FAMILY CHURN: **net {token_family_totals['dmgComboConfidenceFxAccentVolatilityAlias']['net']:+d}** (added={token_family_totals['dmgComboConfidenceFxAccentVolatilityAlias']['added']} removed={token_family_totals['dmgComboConfidenceFxAccentVolatilityAlias']['removed']} churn={token_family_totals['dmgComboConfidenceFxAccentVolatilityAlias']['churn']} coverage={token_family_totals['dmgComboConfidenceFxAccentVolatilityAlias']['coverage']})",
        f"- DCCSR FAMILY CHURN: **net {token_family_totals['dmgComboConfidenceCoachCopySwapRecommendationAlias']['net']:+d}** (added={token_family_totals['dmgComboConfidenceCoachCopySwapRecommendationAlias']['added']} removed={token_family_totals['dmgComboConfidenceCoachCopySwapRecommendationAlias']['removed']} churn={token_family_totals['dmgComboConfidenceCoachCopySwapRecommendationAlias']['churn']} coverage={token_family_totals['dmgComboConfidenceCoachCopySwapRecommendationAlias']['coverage']})",
        f"- DCCST FAMILY CHURN: **net {token_family_totals['dmgComboConfidenceCoachCopySwapTrendAlias']['net']:+d}** (added={token_family_totals['dmgComboConfidenceCoachCopySwapTrendAlias']['added']} removed={token_family_totals['dmgComboConfidenceCoachCopySwapTrendAlias']['removed']} churn={token_family_totals['dmgComboConfidenceCoachCopySwapTrendAlias']['churn']} coverage={token_family_totals['dmgComboConfidenceCoachCopySwapTrendAlias']['coverage']})",
        f"- DMG COMBO CONF COACH COPY SWAP REC FAMILY TREND: **{combo_confidence_coach_copy_swap_recommendation_family_trend_signals['trend']}** (Δnet={combo_confidence_coach_copy_swap_recommendation_family_trend_drift:+d} currentNet={combo_confidence_coach_copy_swap_recommendation_family_trend_signals['currentNet']:+d} priorNet={combo_confidence_coach_copy_swap_recommendation_family_trend_signals['priorNet']:+d} loaded={combo_confidence_coach_copy_swap_recommendation_family_trend_signals['priorLoaded']} reason={combo_confidence_coach_copy_swap_recommendation_family_trend_signals['reason']})",
        f"- DCCST: **{dmg_combo_conf_coach_copy_swap_trend_alias if dmg_combo_conf_coach_copy_swap_trend_alias_flag_enabled else 'FLAG OFF'}** (flag={dmg_combo_conf_coach_copy_swap_trend_alias_flag_name} enabled={dmg_combo_conf_coach_copy_swap_trend_alias_flag_enabled} trend={combo_confidence_coach_copy_swap_trend_alias_family_trend_signals['trend']})",
        f"- PULSE REMAP MOMENTUM FAMILY CHURN: **net {token_family_totals['pulseRemapMomentumAlias']['net']:+d}** (added={token_family_totals['pulseRemapMomentumAlias']['added']} removed={token_family_totals['pulseRemapMomentumAlias']['removed']} churn={token_family_totals['pulseRemapMomentumAlias']['churn']} coverage={token_family_totals['pulseRemapMomentumAlias']['coverage']})",
        f"- PULSE REMAP SUPPRESS FAMILY CHURN: **net {token_family_totals['pulseRemapMomentumSuppressionAlias']['net']:+d}** (added={token_family_totals['pulseRemapMomentumSuppressionAlias']['added']} removed={token_family_totals['pulseRemapMomentumSuppressionAlias']['removed']} churn={token_family_totals['pulseRemapMomentumSuppressionAlias']['churn']} coverage={token_family_totals['pulseRemapMomentumSuppressionAlias']['coverage']})",
        f"- PULSE REMAP SUPPRESS PLAN FAMILY CHURN: **net {token_family_totals['pulseRemapSuppressionPlanAlias']['net']:+d}** (added={token_family_totals['pulseRemapSuppressionPlanAlias']['added']} removed={token_family_totals['pulseRemapSuppressionPlanAlias']['removed']} churn={token_family_totals['pulseRemapSuppressionPlanAlias']['churn']} coverage={token_family_totals['pulseRemapSuppressionPlanAlias']['coverage']})",
        f"- PULSE REMAP SCENE MICROLINE VARIANT PACK FAMILY CHURN: **net {token_family_totals['pulseRemapSceneMicrolineVariantPackAlias']['net']:+d}** (added={token_family_totals['pulseRemapSceneMicrolineVariantPackAlias']['added']} removed={token_family_totals['pulseRemapSceneMicrolineVariantPackAlias']['removed']} churn={token_family_totals['pulseRemapSceneMicrolineVariantPackAlias']['churn']} coverage={token_family_totals['pulseRemapSceneMicrolineVariantPackAlias']['coverage']})",
        f"- PULSE REMAP SCENE MICROLINE STYLE POLICY + PRSMP FAMILY CHURN: **net {token_family_totals['pulseRemapSceneMicrolineStylePolicyAlias']['net']:+d}** (added={token_family_totals['pulseRemapSceneMicrolineStylePolicyAlias']['added']} removed={token_family_totals['pulseRemapSceneMicrolineStylePolicyAlias']['removed']} churn={token_family_totals['pulseRemapSceneMicrolineStylePolicyAlias']['churn']} coverage={token_family_totals['pulseRemapSceneMicrolineStylePolicyAlias']['coverage']})",
        f"- PULSE REMAP SCENE MICROLINE STYLE POSTURE + PRSMPP FAMILY CHURN: **net {token_family_totals['pulseRemapSceneMicrolineStylePostureAlias']['net']:+d}** (added={token_family_totals['pulseRemapSceneMicrolineStylePostureAlias']['added']} removed={token_family_totals['pulseRemapSceneMicrolineStylePostureAlias']['removed']} churn={token_family_totals['pulseRemapSceneMicrolineStylePostureAlias']['churn']} coverage={token_family_totals['pulseRemapSceneMicrolineStylePostureAlias']['coverage']})",
        f"- PULSE REMAP SCENE FX GLINT FAMILY CHURN: **net {token_family_totals['pulseRemapSceneFxGlintAlias']['net']:+d}** (added={token_family_totals['pulseRemapSceneFxGlintAlias']['added']} removed={token_family_totals['pulseRemapSceneFxGlintAlias']['removed']} churn={token_family_totals['pulseRemapSceneFxGlintAlias']['churn']} coverage={token_family_totals['pulseRemapSceneFxGlintAlias']['coverage']})",
        f"- PRSFX FAMILY TREND: **{pulse_remap_scene_fx_glint_family_trend_signals['trend']}** (Δnet={pulse_remap_scene_fx_glint_family_trend_drift:+d} currentNet={pulse_remap_scene_fx_glint_family_trend_signals['currentNet']:+d} priorNet={pulse_remap_scene_fx_glint_family_trend_signals['priorNet']:+d} loaded={pulse_remap_scene_fx_glint_family_trend_signals['priorLoaded']} reason={pulse_remap_scene_fx_glint_family_trend_signals['reason']})",
        f"- PRSCP FAMILY TREND: **{pulse_remap_scene_copy_palette_recommendation_family_trend_signals['trend']}** (Δnet={pulse_remap_scene_copy_palette_recommendation_family_trend_drift:+d} currentNet={pulse_remap_scene_copy_palette_recommendation_family_trend_signals['currentNet']:+d} priorNet={pulse_remap_scene_copy_palette_recommendation_family_trend_signals['priorNet']:+d} loaded={pulse_remap_scene_copy_palette_recommendation_family_trend_signals['priorLoaded']} reason={pulse_remap_scene_copy_palette_recommendation_family_trend_signals['reason']})",
        f"- PRMS FAMILY TREND: **{pulse_remap_suppression_family_trend_signals['trend']}** (Δnet={pulse_remap_suppression_family_trend_drift:+d} currentNet={pulse_remap_suppression_family_trend_signals['currentNet']:+d} priorNet={pulse_remap_suppression_family_trend_signals['priorNet']:+d} loaded={pulse_remap_suppression_family_trend_signals['priorLoaded']} reason={pulse_remap_suppression_family_trend_signals['reason']})",
        f"- PRSP FAMILY TREND: **{pulse_remap_suppression_plan_family_trend_signals['trend']}** (Δnet={pulse_remap_suppression_plan_family_trend_drift:+d} currentNet={pulse_remap_suppression_plan_family_trend_signals['currentNet']:+d} priorNet={pulse_remap_suppression_plan_family_trend_signals['priorNet']:+d} loaded={pulse_remap_suppression_plan_family_trend_signals['priorLoaded']} reason={pulse_remap_suppression_plan_family_trend_signals['reason']})",
        f"- PRSMC FAMILY TREND: **{pulse_remap_scene_microline_cadence_family_trend_signals['trend']}** (Δnet={pulse_remap_scene_microline_cadence_family_trend_drift:+d} currentNet={pulse_remap_scene_microline_cadence_family_trend_signals['currentNet']:+d} priorNet={pulse_remap_scene_microline_cadence_family_trend_signals['priorNet']:+d} loaded={pulse_remap_scene_microline_cadence_family_trend_signals['priorLoaded']} reason={pulse_remap_scene_microline_cadence_family_trend_signals['reason']})",
        f"- PRSMC FAMILY CHURN: **net {token_family_totals['pulseRemapSceneMicrolineCadenceAlias']['net']:+d}** (added={token_family_totals['pulseRemapSceneMicrolineCadenceAlias']['added']} removed={token_family_totals['pulseRemapSceneMicrolineCadenceAlias']['removed']} churn={token_family_totals['pulseRemapSceneMicrolineCadenceAlias']['churn']} coverage={token_family_totals['pulseRemapSceneMicrolineCadenceAlias']['coverage']})",
        f"- PRSMP FAMILY TREND: **{pulse_remap_scene_microline_style_policy_family_trend_signals['trend']}** (Δnet={pulse_remap_scene_microline_style_policy_family_trend_drift:+d} currentNet={pulse_remap_scene_microline_style_policy_family_trend_signals['currentNet']:+d} priorNet={pulse_remap_scene_microline_style_policy_family_trend_signals['priorNet']:+d} loaded={pulse_remap_scene_microline_style_policy_family_trend_signals['priorLoaded']} reason={pulse_remap_scene_microline_style_policy_family_trend_signals['reason']})",
        f"- DMG GLYPH FAMILY CHURN: **net {token_family_totals['dmgGlyphAlias']['net']:+d}** (added={token_family_totals['dmgGlyphAlias']['added']} removed={token_family_totals['dmgGlyphAlias']['removed']} churn={token_family_totals['dmgGlyphAlias']['churn']} coverage={token_family_totals['dmgGlyphAlias']['coverage']})",
        f"- DMG GLYPH FX LIVE FAMILY CHURN: **net {token_family_totals['dmgGlyphFxLiveAlias']['net']:+d}** (added={token_family_totals['dmgGlyphFxLiveAlias']['added']} removed={token_family_totals['dmgGlyphFxLiveAlias']['removed']} churn={token_family_totals['dmgGlyphFxLiveAlias']['churn']} coverage={token_family_totals['dmgGlyphFxLiveAlias']['coverage']})",
        f"- LPR HYS THR FAMILY CHURN: **net {token_family_totals['lanePriorityHysteresisThresholdAlias']['net']:+d}** (added={token_family_totals['lanePriorityHysteresisThresholdAlias']['added']} removed={token_family_totals['lanePriorityHysteresisThresholdAlias']['removed']} churn={token_family_totals['lanePriorityHysteresisThresholdAlias']['churn']} coverage={token_family_totals['lanePriorityHysteresisThresholdAlias']['coverage']})",
        f"- LPR HYS WINDOW Δ FAMILY CHURN: **net {token_family_totals['lanePriorityHysteresisWindowDeltaAlias']['net']:+d}** (added={token_family_totals['lanePriorityHysteresisWindowDeltaAlias']['added']} removed={token_family_totals['lanePriorityHysteresisWindowDeltaAlias']['removed']} churn={token_family_totals['lanePriorityHysteresisWindowDeltaAlias']['churn']} coverage={token_family_totals['lanePriorityHysteresisWindowDeltaAlias']['coverage']})",
        f"- LPR HYS FLOOR REC + LPR HYS FLOOR FAMILY CHURN: **net {token_family_totals['lanePriorityHysteresisFloorRecommendationAlias']['net']:+d}** (added={token_family_totals['lanePriorityHysteresisFloorRecommendationAlias']['added']} removed={token_family_totals['lanePriorityHysteresisFloorRecommendationAlias']['removed']} churn={token_family_totals['lanePriorityHysteresisFloorRecommendationAlias']['churn']} coverage={token_family_totals['lanePriorityHysteresisFloorRecommendationAlias']['coverage']})",
        f"- LPR HYS FLOOR FAMILY TREND: **{lane_priority_hysteresis_floor_family_trend_signals['trend']}** (Δnet={lane_priority_hysteresis_floor_family_trend_drift:+d} currentNet={lane_priority_hysteresis_floor_family_trend_signals['currentNet']:+d} priorNet={lane_priority_hysteresis_floor_family_trend_signals['priorNet']:+d} loaded={lane_priority_hysteresis_floor_family_trend_signals['priorLoaded']} reason={lane_priority_hysteresis_floor_family_trend_signals['reason']})",
        f"- LPR HF T: **{lane_priority_hysteresis_floor_family_trend_alias}** (flag={lane_priority_hysteresis_floor_family_trend_alias_flag_name} enabled={lane_priority_hysteresis_floor_family_trend_alias_flag_enabled} trend={lane_priority_hysteresis_floor_family_trend_signals['trend']})",
        f"- LANE CADENCE SUMMARY: **SYSTEMS/OPS {'OK' if (token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyFxAlias']['aliasesTouchedCount'] > 0 or token_family_totals['dmgGlyphAlias']['aliasesTouchedCount'] > 0 or token_family_totals['dmgGlyphFxLiveAlias']['aliasesTouchedCount'] > 0 or token_family_totals['dmgComboAlias']['aliasesTouchedCount'] > 0) else 'GAP'}** (RGFXWRIUFX coverage={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyFxAlias']['coverage']} churn={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyFxAlias']['churn']} | DMG GLYPH coverage={token_family_totals['dmgGlyphAlias']['coverage']} churn={token_family_totals['dmgGlyphAlias']['churn']} | DMG GLYPH FX LIVE coverage={token_family_totals['dmgGlyphFxLiveAlias']['coverage']} churn={token_family_totals['dmgGlyphFxLiveAlias']['churn']} | DMG COMBO coverage={token_family_totals['dmgComboAlias']['coverage']} churn={token_family_totals['dmgComboAlias']['churn']})",
        f"- LBA: **{lane_bucket_age_compact_alias}** (flag={lane_bucket_age_compact_alias_signals['flagName']} enabled={lane_bucket_age_compact_alias_signals['flagEnabled']} sys={lane_bucket_age_compact_alias_signals['systemsOpsHours']}h dw={lane_bucket_age_compact_alias_signals['designWorldHours']}h cv={lane_bucket_age_compact_alias_signals['combatVfxHours']}h)",
        f"- LANE BUCKET AGE: **{lane_bucket_age['token'].split(':', 1)[1]}** (status={lane_bucket_age['status']} window={lane_bucket_age['windowHours']}h)",
        f"- LANE BUCKET AGE Δ: **{lane_bucket_age_delta:+d}h** (currentMax={lane_bucket_age_drift_signals['currentMaxAgeHours']} priorMax={lane_bucket_age_drift_signals['priorMaxAgeHours']} loaded={lane_bucket_age_drift_signals['priorLoaded']})",
        f"- LANE CADENCE RECENCY: **{lane_cadence_recency}** (status={lane_cadence_recency_signals['status']} max={lane_cadence_recency_signals['maxAgeHours']}h Δ={lane_cadence_recency_signals['deltaHours']:+d}h window={lane_cadence_recency_signals['windowHours']}h reason={lane_cadence_recency_signals['reason']})",
        f"- LANE CADENCE MISS RISK: **{lane_cadence_miss_risk_token}** (risk={lane_cadence_miss_risk_signals['risk']} max={lane_cadence_miss_risk_signals['maxAgeHours']}h Δ={lane_cadence_miss_risk_signals['deltaHours']:+d}h window={lane_cadence_miss_risk_signals['windowHours']}h reason={lane_cadence_miss_risk_signals['reason']})",
        f"- LCMR: **{lane_cadence_miss_risk_alias_token}** (flag={lane_cadence_miss_risk_alias_signals['flagName']} enabled={lane_cadence_miss_risk_alias_signals['flagEnabled']} risk={lane_cadence_miss_risk_alias_signals['risk']} alias={lane_cadence_miss_risk_alias_signals['alias']})",
        f"- LANE PRIORITY REC: **{lane_priority_recommendation}** (reason={lane_priority_recommendation_signals['reason']} worstAge={lane_priority_recommendation_signals['worstAgeHours']}h offlineOnly={lane_priority_recommendation_signals['offlineOnly']})",
        f"- LPR: **{lane_priority_recommendation_compact_alias}** (flag={lane_priority_recommendation_compact_alias_signals['flagName']} enabled={lane_priority_recommendation_compact_alias_signals['flagEnabled']} rec={lane_priority_recommendation_compact_alias_signals['recommendation']} alias={lane_priority_recommendation_compact_alias_signals['alias']})",
        f"- LPR HYS: **{lane_priority_hysteresis_compact_alias}** (flag={lane_priority_hysteresis_compact_alias_signals['flagName']} enabled={lane_priority_hysteresis_compact_alias_signals['flagEnabled']} applied={lane_priority_hysteresis_compact_alias_signals['hysteresisApplied']} alias={lane_priority_hysteresis_compact_alias_signals['alias']})",
        f"- LPR HYS RAIL: **{lane_priority_hysteresis_rail}** (flag={lane_priority_hysteresis_rail_signals['flagName']} enabled={lane_priority_hysteresis_rail_signals['flagEnabled']} conf={lane_priority_hysteresis_rail_signals['confidence']} gap={lane_priority_hysteresis_rail_signals['scoreGap']} threshold={lane_priority_hysteresis_rail_signals['threshold']} reason={lane_priority_hysteresis_rail_signals['reason']})",
        f"- LANE PRIORITY REC CONF: **{lane_priority_recommendation_confidence_level}** (worstAge={lane_priority_recommendation_confidence_signals['worstAgeHours']}h momentumGap={lane_priority_recommendation_confidence_signals['momentumGapHours']}h reason={lane_priority_recommendation_confidence_signals['reason']})",
        f"- LANE PRIORITY REC CONF GUARD: **{'APPLY' if lane_priority_recommendation_confidence_guard_signals['guardApplied'] else 'HOLD'}** (base={lane_priority_recommendation_confidence_guard_signals['baseConfidence']} guarded={lane_priority_recommendation_confidence_guard_signals['guardedConfidence']} trend={lane_priority_recommendation_confidence_guard_signals['trend']} regime={lane_priority_recommendation_confidence_guard_signals['volatilityRegime']} streak={lane_priority_recommendation_confidence_guard_signals['divergenceStreak']} priorLoaded={lane_priority_recommendation_confidence_guard_signals['priorLoaded']} reason={lane_priority_recommendation_confidence_guard_signals['reason']})",
        f"- LPRCG: **{lane_priority_recommendation_confidence_guard_alias}** (flag={lane_priority_recommendation_confidence_guard_alias_signals['flagName']} enabled={lane_priority_recommendation_confidence_guard_alias_signals['flagEnabled']} action={lane_priority_recommendation_confidence_guard_alias_signals['action']})",
        f"- LPRCG THRESH: **{lane_priority_recommendation_confidence_guard_threshold}** (policy={lane_priority_recommendation_confidence_guard_threshold_signals['policy']})",
        f"- LPRCG COACH: **{lane_priority_recommendation_confidence_guard_persistence_coach_token}** (reason={lane_priority_recommendation_confidence_guard_persistence_coach_signals['reason']} action={lane_priority_recommendation_confidence_guard_persistence_coach_signals['guardAction']} consecutive={lane_priority_recommendation_confidence_guard_persistence_coach_signals['consecutiveApplyWindows']} priorLoaded={lane_priority_recommendation_confidence_guard_persistence_coach_signals['priorLoaded']} offlineOnly={lane_priority_recommendation_confidence_guard_persistence_coach_signals['offlineOnly']})",
        f"- LPRCGC: **{lane_priority_recommendation_confidence_guard_persistence_coach_alias}** (flag={lane_priority_recommendation_confidence_guard_persistence_coach_alias_signals['flagName']} enabled={lane_priority_recommendation_confidence_guard_persistence_coach_alias_signals['flagEnabled']} coach={lane_priority_recommendation_confidence_guard_persistence_coach_alias_signals['coachToken']} alias={lane_priority_recommendation_confidence_guard_persistence_coach_alias_signals['alias']})",
        f"- LPRCG COACH PACK: **{lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_token}** (reason={lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_signals['reason']} action={lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_signals['guardAction']} consecutive={lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_signals['consecutiveApplyWindows']} regime={lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_signals['volatilityRegime']} regimeChanged={lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_signals['regimeChanged']} priorLoaded={lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_signals['priorLoaded']} offlineOnly={lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_signals['offlineOnly']})",
        f"- LPRCGCP: **{lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_alias}** (flag={lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_alias_signals['flagName']} enabled={lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_alias_signals['flagEnabled']} pack={lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_alias_signals['packToken']} alias={lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_alias_signals['alias']})",
        f"- LPRCG COACH COPY: **{lane_priority_recommendation_confidence_guard_persistence_coach_copy_narrative}** (reason={lane_priority_recommendation_confidence_guard_persistence_coach_copy_narrative_signals['reason']} pack={lane_priority_recommendation_confidence_guard_persistence_coach_copy_narrative_signals['pack']} action={lane_priority_recommendation_confidence_guard_persistence_coach_copy_narrative_signals['guardAction']} regime={lane_priority_recommendation_confidence_guard_persistence_coach_copy_narrative_signals['volatilityRegime']} priorRegime={lane_priority_recommendation_confidence_guard_persistence_coach_copy_narrative_signals['priorVolatilityRegime']} regimeChanged={lane_priority_recommendation_confidence_guard_persistence_coach_copy_narrative_signals['regimeChanged']} consecutive={lane_priority_recommendation_confidence_guard_persistence_coach_copy_narrative_signals['consecutiveApplyWindows']} divergenceStreak={lane_priority_recommendation_confidence_guard_persistence_coach_copy_narrative_signals['divergenceStreak']} offlineOnly={lane_priority_recommendation_confidence_guard_persistence_coach_copy_narrative_signals['offlineOnly']})",
        f"- LPRCGCN: **{lane_priority_recommendation_confidence_guard_persistence_coach_copy_alias}** (flag={lane_priority_recommendation_confidence_guard_persistence_coach_copy_alias_signals['flagName']} enabled={lane_priority_recommendation_confidence_guard_persistence_coach_copy_alias_signals['flagEnabled']} coachCopy={lane_priority_recommendation_confidence_guard_persistence_coach_copy_alias_signals['coachCopyToken']} alias={lane_priority_recommendation_confidence_guard_persistence_coach_copy_alias_signals['alias']})",
        f"- LPRCG COACH COPY WHY: **{lane_priority_recommendation_confidence_guard_persistence_coach_copy_why}** (flag={lane_priority_recommendation_confidence_guard_persistence_coach_copy_why_signals['flagName']} enabled={lane_priority_recommendation_confidence_guard_persistence_coach_copy_why_signals['flagEnabled']} reason={lane_priority_recommendation_confidence_guard_persistence_coach_copy_why_signals['reason']} short={lane_priority_recommendation_confidence_guard_persistence_coach_copy_why_signals['short']} offlineOnly={lane_priority_recommendation_confidence_guard_persistence_coach_copy_why_signals['offlineOnly']})",
        f"- LPRCG + LANE PRIORITY REC CONF GUARD FAMILY CHURN: **net {token_family_totals['lanePriorityRecommendationConfidenceGuardAlias']['net']:+d}** (added={token_family_totals['lanePriorityRecommendationConfidenceGuardAlias']['added']} removed={token_family_totals['lanePriorityRecommendationConfidenceGuardAlias']['removed']} churn={token_family_totals['lanePriorityRecommendationConfidenceGuardAlias']['churn']} coverage={token_family_totals['lanePriorityRecommendationConfidenceGuardAlias']['coverage']})",
        f"- LPRCG COACH + LPRCGC FAMILY CHURN: **net {token_family_totals['lanePriorityRecommendationConfidenceGuardCoachAlias']['net']:+d}** (added={token_family_totals['lanePriorityRecommendationConfidenceGuardCoachAlias']['added']} removed={token_family_totals['lanePriorityRecommendationConfidenceGuardCoachAlias']['removed']} churn={token_family_totals['lanePriorityRecommendationConfidenceGuardCoachAlias']['churn']} coverage={token_family_totals['lanePriorityRecommendationConfidenceGuardCoachAlias']['coverage']})",
        f"- LPRCG COACH PACK + LPRCGCP FAMILY CHURN: **net {token_family_totals['lanePriorityRecommendationConfidenceGuardCoachPackAlias']['net']:+d}** (added={token_family_totals['lanePriorityRecommendationConfidenceGuardCoachPackAlias']['added']} removed={token_family_totals['lanePriorityRecommendationConfidenceGuardCoachPackAlias']['removed']} churn={token_family_totals['lanePriorityRecommendationConfidenceGuardCoachPackAlias']['churn']} coverage={token_family_totals['lanePriorityRecommendationConfidenceGuardCoachPackAlias']['coverage']})",
        f"- LPRCG COACH COPY + LPRCGCN FAMILY CHURN: **net {token_family_totals['lanePriorityRecommendationConfidenceGuardCoachCopyAlias']['net']:+d}** (added={token_family_totals['lanePriorityRecommendationConfidenceGuardCoachCopyAlias']['added']} removed={token_family_totals['lanePriorityRecommendationConfidenceGuardCoachCopyAlias']['removed']} churn={token_family_totals['lanePriorityRecommendationConfidenceGuardCoachCopyAlias']['churn']} coverage={token_family_totals['lanePriorityRecommendationConfidenceGuardCoachCopyAlias']['coverage']})",
        f"- LPRCG THRESH FAMILY CHURN: **net {token_family_totals['lanePriorityRecommendationConfidenceGuardThresholdAlias']['net']:+d}** (added={token_family_totals['lanePriorityRecommendationConfidenceGuardThresholdAlias']['added']} removed={token_family_totals['lanePriorityRecommendationConfidenceGuardThresholdAlias']['removed']} churn={token_family_totals['lanePriorityRecommendationConfidenceGuardThresholdAlias']['churn']} coverage={token_family_totals['lanePriorityRecommendationConfidenceGuardThresholdAlias']['coverage']})",
        f"- LANE PRIORITY REC HYSTERESIS: **{'HOLD' if lane_priority_recommendation_signals['hysteresisApplied'] else 'SHIFT'}** (prior={lane_priority_recommendation_signals['priorRecommendation']} raw={lane_priority_recommendation_signals['rawRecommendation']} gap={lane_priority_recommendation_signals['hysteresisScoreGap']} threshold={lane_priority_recommendation_signals['hysteresisThreshold']} reason={lane_priority_recommendation_signals['hysteresisReason']})",
        f"- LPR HYS THRESH REC: **{lane_priority_hysteresis_threshold_tuning}** (base={lane_priority_hysteresis_threshold_tuning_signals['baseThreshold']} rec={lane_priority_hysteresis_threshold_tuning_signals['recommendedThreshold']} floor={lane_priority_hysteresis_threshold_tuning_signals['adaptiveFloor']} ceil={lane_priority_hysteresis_threshold_tuning_signals['adaptiveCeiling']} priorWindow={lane_priority_hysteresis_threshold_tuning_signals['priorAdaptiveWindowLoaded']} volSpan={lane_priority_hysteresis_threshold_tuning_signals['momentumVolatilitySpanHours']} maxAbsMom={lane_priority_hysteresis_threshold_tuning_signals['maxAbsMomentumHours']} ageSpread={lane_priority_hysteresis_threshold_tuning_signals['ageSpreadHours']} learn={lane_priority_hysteresis_threshold_tuning_signals['learningReason']} reason={lane_priority_hysteresis_threshold_tuning_signals['reason']})",
        f"- LPR VOL REGIME: **{lane_priority_hysteresis_threshold_tuning_signals['volatilityRegimeMemory']}** (current={lane_priority_hysteresis_threshold_tuning_signals['volatilityRegime']} prior={lane_priority_hysteresis_threshold_tuning_signals['priorVolatilityRegime']} reason={lane_priority_hysteresis_threshold_tuning_signals['volatilityRegimeReason']} steps={lane_priority_hysteresis_threshold_tuning_signals['stepSizes']})",
        f"- LPR HYS THR: **{lane_priority_hysteresis_threshold_compact_alias}** (flag={lane_priority_hysteresis_threshold_compact_alias_signals['flagName']} enabled={lane_priority_hysteresis_threshold_compact_alias_signals['flagEnabled']} alias={lane_priority_hysteresis_threshold_compact_alias_signals['alias']} rec={lane_priority_hysteresis_threshold_compact_alias_signals['recommendation']})",
        f"- LPR HYS WINDOW: **{lane_priority_hysteresis_window_band}** (floor={lane_priority_hysteresis_window_band_signals['adaptiveFloor']} ceil={lane_priority_hysteresis_window_band_signals['adaptiveCeiling']} span={lane_priority_hysteresis_window_band_signals['span']} reason={lane_priority_hysteresis_window_band_signals['reason']})",
        f"- LPR HYS WINDOW Δ: **{lane_priority_hysteresis_window_delta:+d}** (current={lane_priority_hysteresis_window_delta_signals['currentBand']} prior={lane_priority_hysteresis_window_delta_signals['priorBand']} loaded={lane_priority_hysteresis_window_delta_signals['priorLoaded']})",
        f"- LPR HYS FLOOR REC: **{lane_priority_hysteresis_floor_recommendation}** (streak={lane_priority_hysteresis_floor_recommendation_signals['highStreak']} threshold={lane_priority_hysteresis_floor_recommendation_signals['streakThreshold']} currentRisk={lane_priority_hysteresis_floor_recommendation_signals['currentRisk']} priorRisk={lane_priority_hysteresis_floor_recommendation_signals['priorRisk']} Δ={lane_priority_hysteresis_floor_recommendation_signals['currentDeltaHours']:+d} strongMomentum={lane_priority_hysteresis_floor_recommendation_signals['strongMomentum']} reason={lane_priority_hysteresis_floor_recommendation_signals['reason']})",
        f"- LPR HYS FLOOR: **{lane_priority_hysteresis_floor_recommendation_alias}** (flag={lane_priority_hysteresis_floor_recommendation_alias_signals['flagName']} enabled={lane_priority_hysteresis_floor_recommendation_alias_signals['flagEnabled']} alias={lane_priority_hysteresis_floor_recommendation_alias_signals['alias']} rec={lane_priority_hysteresis_floor_recommendation_alias_signals['recommendation']})",
        f"- PULSE HEAT FX COMPACT-BUDGET DRIFT: **{pulse_heat_fx_compact_budget_drift_level}** ({pulse_heat_fx_compact_budget_drift_signals['reason']}; compactNet={pulse_heat_fx_compact_budget_drift_signals['compactNet']:+d} familyNet={pulse_heat_fx_compact_budget_drift_signals['familyNet']:+d} churn={pulse_heat_fx_compact_budget_drift_signals['familyChurn']})",
        f"- ROUTE GLOW FX COMPACT-BUDGET DRIFT: **{route_glow_fx_compact_budget_drift_level}** ({route_glow_fx_compact_budget_drift_signals['reason']}; compactNet={route_glow_fx_compact_budget_drift_signals['compactNet']:+d} familyNet={route_glow_fx_compact_budget_drift_signals['familyNet']:+d} churn={route_glow_fx_compact_budget_drift_signals['familyChurn']})",
        f"- ROUTE GLOW FX CONF WHY RAIL MODE COMPACT-BUDGET DRIFT: **{route_glow_fx_conf_why_rail_mode_compact_budget_drift_level}** ({route_glow_fx_conf_why_rail_mode_compact_budget_drift_signals['reason']}; compactNet={route_glow_fx_conf_why_rail_mode_compact_budget_drift_signals['compactNet']:+d} familyNet={route_glow_fx_conf_why_rail_mode_compact_budget_drift_signals['familyNet']:+d} churn={route_glow_fx_conf_why_rail_mode_compact_budget_drift_signals['familyChurn']})",
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
        "## Token Family Coverage",
        f"- VTW + VIBE TRAIL WHY: +{token_family_totals['vibeTrailWhyAlias']['added']} / -{token_family_totals['vibeTrailWhyAlias']['removed']} / net {token_family_totals['vibeTrailWhyAlias']['net']} (churn={token_family_totals['vibeTrailWhyAlias']['churn']} coverage={token_family_totals['vibeTrailWhyAlias']['coverage']})",
        f"- VTWC + VIBE TRAIL WHY CONF: +{token_family_totals['vibeTrailWhyConfidenceAlias']['added']} / -{token_family_totals['vibeTrailWhyConfidenceAlias']['removed']} / net {token_family_totals['vibeTrailWhyConfidenceAlias']['net']} (churn={token_family_totals['vibeTrailWhyConfidenceAlias']['churn']} coverage={token_family_totals['vibeTrailWhyConfidenceAlias']['coverage']})",
        f"- VTCW + VIBE TRAIL WHY CONF WHY: +{token_family_totals['vibeTrailWhyConfidenceWhyAlias']['added']} / -{token_family_totals['vibeTrailWhyConfidenceWhyAlias']['removed']} / net {token_family_totals['vibeTrailWhyConfidenceWhyAlias']['net']} (churn={token_family_totals['vibeTrailWhyConfidenceWhyAlias']['churn']} coverage={token_family_totals['vibeTrailWhyConfidenceWhyAlias']['coverage']})",
        f"- VTCWC + VIBE TRAIL WHY CONF WHY CONF: +{token_family_totals['vibeTrailWhyConfidenceWhyConfidenceAlias']['added']} / -{token_family_totals['vibeTrailWhyConfidenceWhyConfidenceAlias']['removed']} / net {token_family_totals['vibeTrailWhyConfidenceWhyConfidenceAlias']['net']} (churn={token_family_totals['vibeTrailWhyConfidenceWhyConfidenceAlias']['churn']} coverage={token_family_totals['vibeTrailWhyConfidenceWhyConfidenceAlias']['coverage']})",
        f"- VTA + VIBE TRAIL ARC: +{token_family_totals['vibeTrailArcAlias']['added']} / -{token_family_totals['vibeTrailArcAlias']['removed']} / net {token_family_totals['vibeTrailArcAlias']['net']} (churn={token_family_totals['vibeTrailArcAlias']['churn']} coverage={token_family_totals['vibeTrailArcAlias']['coverage']})",
        f"- ARC + AMBIENT RAMP CONF: +{token_family_totals['ambientRampConfidenceAlias']['added']} / -{token_family_totals['ambientRampConfidenceAlias']['removed']} / net {token_family_totals['ambientRampConfidenceAlias']['net']} (churn={token_family_totals['ambientRampConfidenceAlias']['churn']} coverage={token_family_totals['ambientRampConfidenceAlias']['coverage']})",
        f"- ARW + AMBIENT RAMP WHY: +{token_family_totals['ambientRampWhyAlias']['added']} / -{token_family_totals['ambientRampWhyAlias']['removed']} / net {token_family_totals['ambientRampWhyAlias']['net']} (churn={token_family_totals['ambientRampWhyAlias']['churn']} coverage={token_family_totals['ambientRampWhyAlias']['coverage']})",
        f"- ARW REC PARITY: {ambient_ramp_why_recommendation_parity} (rec={ambient_ramp_why_recommendation_parity_signals['recommendation']} conf={ambient_ramp_why_recommendation_parity_signals['confidence']} churn={ambient_ramp_why_recommendation_parity_signals['ambientRampWhyChurn']} net={ambient_ramp_why_recommendation_parity_signals['ambientRampWhyNet']:+d} pressure={ambient_ramp_why_recommendation_parity_signals['pressureBand']})",
        f"- ARW AUTO PLAN: {ambient_ramp_why_auto_remap_plan_compact} (full={ambient_ramp_why_auto_remap_plan})",
        f"- ARW AUTO WHY: {ambient_ramp_why_auto_remap_why} (offline shorthand)",
        f"- ARW APC: {ambient_ramp_why_auto_remap_plan_confidence_band_alias if arw_apc_flag_enabled else 'FLAG OFF'} (flag={arw_apc_flag_name} enabled={arw_apc_flag_enabled})",
        f"- ARW AUTO PLAN CONF MOMENTUM: {ambient_ramp_why_auto_remap_plan_confidence_momentum_freeze_recommendation} (reason={ambient_ramp_why_auto_remap_plan_confidence_momentum_freeze_signals['reason']} confΔ={ambient_ramp_why_auto_remap_plan_confidence_momentum_freeze_signals['confidenceDrift']:+d})",
        f"- ARW MOMENTUM: {ambient_ramp_why_auto_remap_plan_confidence_momentum_alias if arw_momentum_flag_enabled else 'FLAG OFF'} (flag={arw_momentum_flag_name} enabled={arw_momentum_flag_enabled})",
        f"- ARW MOMENTUM SCORE: {ambient_ramp_why_auto_remap_plan_confidence_momentum_score} (base={ambient_ramp_why_auto_remap_plan_confidence_momentum_score_signals['base']} confΔ={ambient_ramp_why_auto_remap_plan_confidence_momentum_score_signals['confidenceDrift']:+d})",
        f"- ARW MOMENTUM ARC: {ambient_ramp_why_auto_remap_momentum_arc if arw_momentum_arc_flag_enabled else 'FLAG OFF'} (flag={arw_momentum_arc_flag_name} enabled={arw_momentum_arc_flag_enabled} score={ambient_ramp_why_auto_remap_momentum_arc_signals['momentumScore']} pressure={ambient_ramp_why_auto_remap_momentum_arc_signals['pressureBand']})",
        f"- ARW ARC PULSE: {ambient_ramp_why_auto_remap_momentum_arc_pulse if arw_arc_pulse_flag_enabled else 'FLAG OFF'} (flag={arw_arc_pulse_flag_name} enabled={arw_arc_pulse_flag_enabled} arc={ambient_ramp_why_auto_remap_momentum_arc})",
        f"- ARW AUTO PLAN FAMILY: +{token_family_totals['ambientRampWhyAutoRemapPlanAlias']['added']} / -{token_family_totals['ambientRampWhyAutoRemapPlanAlias']['removed']} / net {token_family_totals['ambientRampWhyAutoRemapPlanAlias']['net']} (churn={token_family_totals['ambientRampWhyAutoRemapPlanAlias']['churn']} coverage={token_family_totals['ambientRampWhyAutoRemapPlanAlias']['coverage']} drift={ambient_ramp_why_auto_remap_plan_drift:+d})",
        f"- ARW APC FAMILY: +{token_family_totals['ambientRampWhyAutoRemapConfidenceBandAlias']['added']} / -{token_family_totals['ambientRampWhyAutoRemapConfidenceBandAlias']['removed']} / net {token_family_totals['ambientRampWhyAutoRemapConfidenceBandAlias']['net']} (churn={token_family_totals['ambientRampWhyAutoRemapConfidenceBandAlias']['churn']} coverage={token_family_totals['ambientRampWhyAutoRemapConfidenceBandAlias']['coverage']})",
        f"- ARW AUTO PLAN CONF MOMENTUM FAMILY: +{token_family_totals['ambientRampWhyAutoRemapConfidenceMomentumAlias']['added']} / -{token_family_totals['ambientRampWhyAutoRemapConfidenceMomentumAlias']['removed']} / net {token_family_totals['ambientRampWhyAutoRemapConfidenceMomentumAlias']['net']} (churn={token_family_totals['ambientRampWhyAutoRemapConfidenceMomentumAlias']['churn']} coverage={token_family_totals['ambientRampWhyAutoRemapConfidenceMomentumAlias']['coverage']})",
        f"- ARW MOMENTUM FAMILY: +{token_family_totals['ambientRampWhyAutoRemapConfidenceMomentumCompactAlias']['added']} / -{token_family_totals['ambientRampWhyAutoRemapConfidenceMomentumCompactAlias']['removed']} / net {token_family_totals['ambientRampWhyAutoRemapConfidenceMomentumCompactAlias']['net']} (churn={token_family_totals['ambientRampWhyAutoRemapConfidenceMomentumCompactAlias']['churn']} coverage={token_family_totals['ambientRampWhyAutoRemapConfidenceMomentumCompactAlias']['coverage']})",
        f"- ARW MOMENTUM ARC FAMILY: +{token_family_totals['ambientRampWhyAutoRemapMomentumArcAlias']['added']} / -{token_family_totals['ambientRampWhyAutoRemapMomentumArcAlias']['removed']} / net {token_family_totals['ambientRampWhyAutoRemapMomentumArcAlias']['net']} (churn={token_family_totals['ambientRampWhyAutoRemapMomentumArcAlias']['churn']} coverage={token_family_totals['ambientRampWhyAutoRemapMomentumArcAlias']['coverage']})",
        f"- ARW ARC PULSE FAMILY: +{token_family_totals['ambientRampWhyAutoRemapMomentumArcPulseAlias']['added']} / -{token_family_totals['ambientRampWhyAutoRemapMomentumArcPulseAlias']['removed']} / net {token_family_totals['ambientRampWhyAutoRemapMomentumArcPulseAlias']['net']} (churn={token_family_totals['ambientRampWhyAutoRemapMomentumArcPulseAlias']['churn']} coverage={token_family_totals['ambientRampWhyAutoRemapMomentumArcPulseAlias']['coverage']})",
        f"- PULSE HEAT FX: +{token_family_totals['pulseHeatFxAlias']['added']} / -{token_family_totals['pulseHeatFxAlias']['removed']} / net {token_family_totals['pulseHeatFxAlias']['net']} (churn={token_family_totals['pulseHeatFxAlias']['churn']} coverage={token_family_totals['pulseHeatFxAlias']['coverage']})",
        f"- ROUTE GLOW FX + RGFX: +{token_family_totals['routeGlowFxAlias']['added']} / -{token_family_totals['routeGlowFxAlias']['removed']} / net {token_family_totals['routeGlowFxAlias']['net']} (churn={token_family_totals['routeGlowFxAlias']['churn']} coverage={token_family_totals['routeGlowFxAlias']['coverage']})",
        f"- ROUTE GLOW CONF: +{token_family_totals['routeGlowConfidenceAlias']['added']} / -{token_family_totals['routeGlowConfidenceAlias']['removed']} / net {token_family_totals['routeGlowConfidenceAlias']['net']} (churn={token_family_totals['routeGlowConfidenceAlias']['churn']} coverage={token_family_totals['routeGlowConfidenceAlias']['coverage']})",
        f"- ROUTE GLOW FX CONF + RGFXC: +{token_family_totals['routeGlowFxConfidenceAlias']['added']} / -{token_family_totals['routeGlowFxConfidenceAlias']['removed']} / net {token_family_totals['routeGlowFxConfidenceAlias']['net']} (churn={token_family_totals['routeGlowFxConfidenceAlias']['churn']} coverage={token_family_totals['routeGlowFxConfidenceAlias']['coverage']})",
        f"- ROUTE GLOW FX CONF WHY + RGFXW: +{token_family_totals['routeGlowFxConfidenceWhyAlias']['added']} / -{token_family_totals['routeGlowFxConfidenceWhyAlias']['removed']} / net {token_family_totals['routeGlowFxConfidenceWhyAlias']['net']} (churn={token_family_totals['routeGlowFxConfidenceWhyAlias']['churn']} coverage={token_family_totals['routeGlowFxConfidenceWhyAlias']['coverage']})",
        f"- ROUTE GLOW FX CONF WHY RAIL + RGFXWR: +{token_family_totals['routeGlowFxConfidenceWhyRailAlias']['added']} / -{token_family_totals['routeGlowFxConfidenceWhyRailAlias']['removed']} / net {token_family_totals['routeGlowFxConfidenceWhyRailAlias']['net']} (churn={token_family_totals['routeGlowFxConfidenceWhyRailAlias']['churn']} coverage={token_family_totals['routeGlowFxConfidenceWhyRailAlias']['coverage']})",
        f"- RGFXWRM RAIL MODE: +{token_family_totals['routeGlowFxConfidenceWhyRailMode']['added']} / -{token_family_totals['routeGlowFxConfidenceWhyRailMode']['removed']} / net {token_family_totals['routeGlowFxConfidenceWhyRailMode']['net']} (churn={token_family_totals['routeGlowFxConfidenceWhyRailMode']['churn']} coverage={token_family_totals['routeGlowFxConfidenceWhyRailMode']['coverage']})",
        f"- RGFXWRI RAIL INTENSITY: +{token_family_totals['routeGlowFxConfidenceWhyRailIntensity']['added']} / -{token_family_totals['routeGlowFxConfidenceWhyRailIntensity']['removed']} / net {token_family_totals['routeGlowFxConfidenceWhyRailIntensity']['net']} (churn={token_family_totals['routeGlowFxConfidenceWhyRailIntensity']['churn']} coverage={token_family_totals['routeGlowFxConfidenceWhyRailIntensity']['coverage']})",
        f"- RGFXWRI WHY: +{token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhy']['added']} / -{token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhy']['removed']} / net {token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhy']['net']} (churn={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhy']['churn']} coverage={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhy']['coverage']})",
        f"- RGFXWRIWC + RGFXWRI WHY CONF: +{token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceAlias']['added']} / -{token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceAlias']['removed']} / net {token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceAlias']['net']} (churn={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceAlias']['churn']} coverage={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceAlias']['coverage']})",
        f"- RGFXWRIU + ROUTE GLOW FX CONF WHY RAIL INTENSITY WHY CONF URGENCY: +{token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyAlias']['added']} / -{token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyAlias']['removed']} / net {token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyAlias']['net']} (churn={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyAlias']['churn']} coverage={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyAlias']['coverage']})",
        f"- RGFXWRIUP URGENCY PARITY COMPACT: +{token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyParityCompactAlias']['added']} / -{token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyParityCompactAlias']['removed']} / net {token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyParityCompactAlias']['net']} (churn={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyParityCompactAlias']['churn']} coverage={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyParityCompactAlias']['coverage']})",
        f"- ROUTE GLOW FX CONF WHY RAIL INTENSITY WHY CONF URGENCY PARITY: +{token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyDetailed']['added']} / -{token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyDetailed']['removed']} / net {token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyDetailed']['net']} (churn={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyDetailed']['churn']} coverage={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyDetailed']['coverage']})",
        f"- RGFXWRIUFX URGENCY FX: +{token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyFxAlias']['added']} / -{token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyFxAlias']['removed']} / net {token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyFxAlias']['net']} (churn={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyFxAlias']['churn']} coverage={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyFxAlias']['coverage']})",
        f"- URG STACK: +{token_family_totals['urgencyStackTierAlias']['added']} / -{token_family_totals['urgencyStackTierAlias']['removed']} / net {token_family_totals['urgencyStackTierAlias']['net']} (churn={token_family_totals['urgencyStackTierAlias']['churn']} coverage={token_family_totals['urgencyStackTierAlias']['coverage']})",
        f"- URG STACK RAIL: +{token_family_totals['urgencyStackRailAlias']['added']} / -{token_family_totals['urgencyStackRailAlias']['removed']} / net {token_family_totals['urgencyStackRailAlias']['net']} (churn={token_family_totals['urgencyStackRailAlias']['churn']} coverage={token_family_totals['urgencyStackRailAlias']['coverage']})",
        f"- DMGNUM STACK CAP: +{token_family_totals['dmgnumStackCapAlias']['added']} / -{token_family_totals['dmgnumStackCapAlias']['removed']} / net {token_family_totals['dmgnumStackCapAlias']['net']} (churn={token_family_totals['dmgnumStackCapAlias']['churn']} coverage={token_family_totals['dmgnumStackCapAlias']['coverage']})",
        f"- DMGNUM LIFE: +{token_family_totals['dmgnumLifeAlias']['added']} / -{token_family_totals['dmgnumLifeAlias']['removed']} / net {token_family_totals['dmgnumLifeAlias']['net']} (churn={token_family_totals['dmgnumLifeAlias']['churn']} coverage={token_family_totals['dmgnumLifeAlias']['coverage']})",
        f"- DMGNUM LIFE CONF: +{token_family_totals['dmgnumLifeConfidenceAlias']['added']} / -{token_family_totals['dmgnumLifeConfidenceAlias']['removed']} / net {token_family_totals['dmgnumLifeConfidenceAlias']['net']} (churn={token_family_totals['dmgnumLifeConfidenceAlias']['churn']} coverage={token_family_totals['dmgnumLifeConfidenceAlias']['coverage']})",
        f"- DMGNUM LIFE CONF Δ: +{token_family_totals['dmgnumLifeConfidenceDeltaAlias']['added']} / -{token_family_totals['dmgnumLifeConfidenceDeltaAlias']['removed']} / net {token_family_totals['dmgnumLifeConfidenceDeltaAlias']['net']} (churn={token_family_totals['dmgnumLifeConfidenceDeltaAlias']['churn']} coverage={token_family_totals['dmgnumLifeConfidenceDeltaAlias']['coverage']})",
        f"- DMGNUM LIFE TREND: +{token_family_totals['dmgnumLifeTrendAlias']['added']} / -{token_family_totals['dmgnumLifeTrendAlias']['removed']} / net {token_family_totals['dmgnumLifeTrendAlias']['net']} (churn={token_family_totals['dmgnumLifeTrendAlias']['churn']} coverage={token_family_totals['dmgnumLifeTrendAlias']['coverage']})",
        f"- DMGNUM LIFE TREND FX PULSE: +{token_family_totals['dmgnumLifeTrendFxPulseAlias']['added']} / -{token_family_totals['dmgnumLifeTrendFxPulseAlias']['removed']} / net {token_family_totals['dmgnumLifeTrendFxPulseAlias']['net']} (churn={token_family_totals['dmgnumLifeTrendFxPulseAlias']['churn']} coverage={token_family_totals['dmgnumLifeTrendFxPulseAlias']['coverage']})",
        f"- DMGNUM LIFE TREND FX PULSE CONF: +{token_family_totals['dmgnumLifeTrendFxPulseConfidenceAlias']['added']} / -{token_family_totals['dmgnumLifeTrendFxPulseConfidenceAlias']['removed']} / net {token_family_totals['dmgnumLifeTrendFxPulseConfidenceAlias']['net']} (churn={token_family_totals['dmgnumLifeTrendFxPulseConfidenceAlias']['churn']} coverage={token_family_totals['dmgnumLifeTrendFxPulseConfidenceAlias']['coverage']})",
        f"- DMGNUM LIFE TREND FX PULSE REMAP PLAN: +{token_family_totals['dmgnumLifeTrendFxPulseRemapPlanAlias']['added']} / -{token_family_totals['dmgnumLifeTrendFxPulseRemapPlanAlias']['removed']} / net {token_family_totals['dmgnumLifeTrendFxPulseRemapPlanAlias']['net']} (churn={token_family_totals['dmgnumLifeTrendFxPulseRemapPlanAlias']['churn']} coverage={token_family_totals['dmgnumLifeTrendFxPulseRemapPlanAlias']['coverage']})",
        f"- DMG COMBO: +{token_family_totals['dmgComboAlias']['added']} / -{token_family_totals['dmgComboAlias']['removed']} / net {token_family_totals['dmgComboAlias']['net']} (churn={token_family_totals['dmgComboAlias']['churn']} coverage={token_family_totals['dmgComboAlias']['coverage']})",
        f"- DMG COMBO CONF: +{token_family_totals['dmgComboConfidenceAlias']['added']} / -{token_family_totals['dmgComboConfidenceAlias']['removed']} / net {token_family_totals['dmgComboConfidenceAlias']['net']} (churn={token_family_totals['dmgComboConfidenceAlias']['churn']} coverage={token_family_totals['dmgComboConfidenceAlias']['coverage']})",
        f"- DCR + DMG COMBO WINDOW RETUNE REC: +{token_family_totals['dmgComboRetuneAlias']['added']} / -{token_family_totals['dmgComboRetuneAlias']['removed']} / net {token_family_totals['dmgComboRetuneAlias']['net']} (churn={token_family_totals['dmgComboRetuneAlias']['churn']} coverage={token_family_totals['dmgComboRetuneAlias']['coverage']})",
        f"- DCRC + DMG COMBO WINDOW RETUNE CONF: +{token_family_totals['dmgComboRetuneConfidenceAlias']['added']} / -{token_family_totals['dmgComboRetuneConfidenceAlias']['removed']} / net {token_family_totals['dmgComboRetuneConfidenceAlias']['net']} (churn={token_family_totals['dmgComboRetuneConfidenceAlias']['churn']} coverage={token_family_totals['dmgComboRetuneConfidenceAlias']['coverage']})",
        f"- DMG COMBO CHAIN COACH: +{token_family_totals['dmgComboChainCoachAlias']['added']} / -{token_family_totals['dmgComboChainCoachAlias']['removed']} / net {token_family_totals['dmgComboChainCoachAlias']['net']} (churn={token_family_totals['dmgComboChainCoachAlias']['churn']} coverage={token_family_totals['dmgComboChainCoachAlias']['coverage']})",
        f"- DCCR + DMG COMBO CONF COACH REC: +{token_family_totals['dmgComboConfidenceCoachAlias']['added']} / -{token_family_totals['dmgComboConfidenceCoachAlias']['removed']} / net {token_family_totals['dmgComboConfidenceCoachAlias']['net']} (churn={token_family_totals['dmgComboConfidenceCoachAlias']['churn']} coverage={token_family_totals['dmgComboConfidenceCoachAlias']['coverage']})",
        f"- DCCSA + DMG COMBO CONF COACH SCENE ARC: +{token_family_totals['dmgComboConfidenceCoachSceneArcAlias']['added']} / -{token_family_totals['dmgComboConfidenceCoachSceneArcAlias']['removed']} / net {token_family_totals['dmgComboConfidenceCoachSceneArcAlias']['net']} (churn={token_family_totals['dmgComboConfidenceCoachSceneArcAlias']['churn']} coverage={token_family_totals['dmgComboConfidenceCoachSceneArcAlias']['coverage']})",
        f"- DCCFX + DMG COMBO CONF FX ACCENT: +{token_family_totals['dmgComboConfidenceFxAccentAlias']['added']} / -{token_family_totals['dmgComboConfidenceFxAccentAlias']['removed']} / net {token_family_totals['dmgComboConfidenceFxAccentAlias']['net']} (churn={token_family_totals['dmgComboConfidenceFxAccentAlias']['churn']} coverage={token_family_totals['dmgComboConfidenceFxAccentAlias']['coverage']})",
        f"- DCCFX FAMILY TREND: {combo_confidence_fx_accent_family_trend_signals['trend']} (Δnet={combo_confidence_fx_accent_family_trend_drift:+d} currentNet={combo_confidence_fx_accent_family_trend_signals['currentNet']:+d} priorNet={combo_confidence_fx_accent_family_trend_signals['priorNet']:+d} loaded={combo_confidence_fx_accent_family_trend_signals['priorLoaded']})",
        f"- DCCFX TREND HYS: {combo_confidence_fx_accent_family_trend_signals['trendHysteresisRecommendation']}/{combo_confidence_fx_accent_family_trend_signals['trendHysteresisConfidence']} (regime={combo_confidence_fx_accent_family_trend_signals['volatilityRegime']} thr={combo_confidence_fx_accent_family_trend_signals['hysteresisThreshold']} rawDrift={combo_confidence_fx_accent_family_trend_signals['rawDrift']:+d} applied={combo_confidence_fx_accent_family_trend_signals['hysteresisApplied']})",
        f"- DCCFXT ALIAS: {dmg_combo_conf_fx_accent_trend_alias if dmg_combo_conf_fx_accent_trend_alias_flag_enabled else 'FLAG OFF'} (trend={combo_confidence_fx_accent_trend} flag={dmg_combo_conf_fx_accent_trend_alias_flag_name} enabled={dmg_combo_conf_fx_accent_trend_alias_flag_enabled})",
        f"- DCCFXV ALIAS: {dmg_combo_conf_fx_accent_volatility_alias if dmg_combo_conf_fx_accent_volatility_alias_flag_enabled else 'FLAG OFF'} (regime={combo_confidence_fx_accent_signals['volatilityRegime']} flag={dmg_combo_conf_fx_accent_volatility_alias_flag_name} enabled={dmg_combo_conf_fx_accent_volatility_alias_flag_enabled})",
        "- DCCFXV LEGEND: C=CALM, S=SWING, P=SPIKE (scene-arc guidance: CALM=stabilize, SWING=monitor oscillation, SPIKE=pressure cue)",
        f"- DCCFXH ALIAS: {dmg_combo_conf_fx_accent_trend_hys_alias if dmg_combo_conf_fx_accent_trend_hys_alias_flag_enabled else 'FLAG OFF'} (rec={combo_confidence_fx_accent_family_trend_signals['trendHysteresisRecommendation']} conf={combo_confidence_fx_accent_family_trend_signals['trendHysteresisConfidence']} flag={dmg_combo_conf_fx_accent_trend_hys_alias_flag_name} enabled={dmg_combo_conf_fx_accent_trend_hys_alias_flag_enabled})",
        f"- DCCFXV + DMG COMBO CONF FX ACCENT VOLATILITY: +{token_family_totals['dmgComboConfidenceFxAccentVolatilityAlias']['added']} / -{token_family_totals['dmgComboConfidenceFxAccentVolatilityAlias']['removed']} / net {token_family_totals['dmgComboConfidenceFxAccentVolatilityAlias']['net']} (churn={token_family_totals['dmgComboConfidenceFxAccentVolatilityAlias']['churn']} coverage={token_family_totals['dmgComboConfidenceFxAccentVolatilityAlias']['coverage']})",
        f"- DCCSR + DMG COMBO CONF COACH COPY SWAP REC: +{token_family_totals['dmgComboConfidenceCoachCopySwapRecommendationAlias']['added']} / -{token_family_totals['dmgComboConfidenceCoachCopySwapRecommendationAlias']['removed']} / net {token_family_totals['dmgComboConfidenceCoachCopySwapRecommendationAlias']['net']} (churn={token_family_totals['dmgComboConfidenceCoachCopySwapRecommendationAlias']['churn']} coverage={token_family_totals['dmgComboConfidenceCoachCopySwapRecommendationAlias']['coverage']})",
        f"- DCCST: +{token_family_totals['dmgComboConfidenceCoachCopySwapTrendAlias']['added']} / -{token_family_totals['dmgComboConfidenceCoachCopySwapTrendAlias']['removed']} / net {token_family_totals['dmgComboConfidenceCoachCopySwapTrendAlias']['net']} (churn={token_family_totals['dmgComboConfidenceCoachCopySwapTrendAlias']['churn']} coverage={token_family_totals['dmgComboConfidenceCoachCopySwapTrendAlias']['coverage']})",
        f"- DMG COMBO CONF COACH COPY SWAP REC FAMILY TREND: {combo_confidence_coach_copy_swap_recommendation_family_trend_signals['trend']} (Δnet={combo_confidence_coach_copy_swap_recommendation_family_trend_drift:+d} currentNet={combo_confidence_coach_copy_swap_recommendation_family_trend_signals['currentNet']:+d} priorNet={combo_confidence_coach_copy_swap_recommendation_family_trend_signals['priorNet']:+d} loaded={combo_confidence_coach_copy_swap_recommendation_family_trend_signals['priorLoaded']})",
        f"- DCCST ALIAS: {dmg_combo_conf_coach_copy_swap_trend_alias if dmg_combo_conf_coach_copy_swap_trend_alias_flag_enabled else 'FLAG OFF'} (trend={combo_confidence_coach_copy_swap_trend_alias_family_trend_signals['trend']} flag={dmg_combo_conf_coach_copy_swap_trend_alias_flag_name} enabled={dmg_combo_conf_coach_copy_swap_trend_alias_flag_enabled})",
        f"- PRSMC + PULSE REMAP SCENE MICROLINE CADENCE: +{token_family_totals['pulseRemapSceneMicrolineCadenceAlias']['added']} / -{token_family_totals['pulseRemapSceneMicrolineCadenceAlias']['removed']} / net {token_family_totals['pulseRemapSceneMicrolineCadenceAlias']['net']} (churn={token_family_totals['pulseRemapSceneMicrolineCadenceAlias']['churn']} coverage={token_family_totals['pulseRemapSceneMicrolineCadenceAlias']['coverage']})",
        f"- PRM + PULSE REMAP MOMENTUM: +{token_family_totals['pulseRemapMomentumAlias']['added']} / -{token_family_totals['pulseRemapMomentumAlias']['removed']} / net {token_family_totals['pulseRemapMomentumAlias']['net']} (churn={token_family_totals['pulseRemapMomentumAlias']['churn']} coverage={token_family_totals['pulseRemapMomentumAlias']['coverage']})",
        f"- PRMS + PULSE REMAP MOMENTUM SUPPRESS: +{token_family_totals['pulseRemapMomentumSuppressionAlias']['added']} / -{token_family_totals['pulseRemapMomentumSuppressionAlias']['removed']} / net {token_family_totals['pulseRemapMomentumSuppressionAlias']['net']} (churn={token_family_totals['pulseRemapMomentumSuppressionAlias']['churn']} coverage={token_family_totals['pulseRemapMomentumSuppressionAlias']['coverage']})",
        f"- PRSP + PULSE REMAP SUPPRESS PLAN: +{token_family_totals['pulseRemapSuppressionPlanAlias']['added']} / -{token_family_totals['pulseRemapSuppressionPlanAlias']['removed']} / net {token_family_totals['pulseRemapSuppressionPlanAlias']['net']} (churn={token_family_totals['pulseRemapSuppressionPlanAlias']['churn']} coverage={token_family_totals['pulseRemapSuppressionPlanAlias']['coverage']})",
        f"- PRSMV + PULSE REMAP SCENE MICROLINE VARIANT PACK: +{token_family_totals['pulseRemapSceneMicrolineVariantPackSelectionAlias']['added']} / -{token_family_totals['pulseRemapSceneMicrolineVariantPackSelectionAlias']['removed']} / net {token_family_totals['pulseRemapSceneMicrolineVariantPackSelectionAlias']['net']} (churn={token_family_totals['pulseRemapSceneMicrolineVariantPackSelectionAlias']['churn']} coverage={token_family_totals['pulseRemapSceneMicrolineVariantPackSelectionAlias']['coverage']})",
        f"- PRSMP + PULSE REMAP SCENE MICROLINE STYLE POLICY: +{token_family_totals['pulseRemapSceneMicrolineStylePolicyAlias']['added']} / -{token_family_totals['pulseRemapSceneMicrolineStylePolicyAlias']['removed']} / net {token_family_totals['pulseRemapSceneMicrolineStylePolicyAlias']['net']} (churn={token_family_totals['pulseRemapSceneMicrolineStylePolicyAlias']['churn']} coverage={token_family_totals['pulseRemapSceneMicrolineStylePolicyAlias']['coverage']})",
        f"- PRSMPP + PULSE REMAP SCENE MICROLINE STYLE POSTURE: +{token_family_totals['pulseRemapSceneMicrolineStylePostureAlias']['added']} / -{token_family_totals['pulseRemapSceneMicrolineStylePostureAlias']['removed']} / net {token_family_totals['pulseRemapSceneMicrolineStylePostureAlias']['net']} (churn={token_family_totals['pulseRemapSceneMicrolineStylePostureAlias']['churn']} coverage={token_family_totals['pulseRemapSceneMicrolineStylePostureAlias']['coverage']})",
        f"- PRSFX + PULSE REMAP SCENE FX GLINT: +{token_family_totals['pulseRemapSceneFxGlintAlias']['added']} / -{token_family_totals['pulseRemapSceneFxGlintAlias']['removed']} / net {token_family_totals['pulseRemapSceneFxGlintAlias']['net']} (churn={token_family_totals['pulseRemapSceneFxGlintAlias']['churn']} coverage={token_family_totals['pulseRemapSceneFxGlintAlias']['coverage']})",
        f"- PRSCP + PULSE REMAP SCENE COPY PALETTE REC: +{token_family_totals['pulseRemapSceneCopyPaletteRecommendationAlias']['added']} / -{token_family_totals['pulseRemapSceneCopyPaletteRecommendationAlias']['removed']} / net {token_family_totals['pulseRemapSceneCopyPaletteRecommendationAlias']['net']} (churn={token_family_totals['pulseRemapSceneCopyPaletteRecommendationAlias']['churn']} coverage={token_family_totals['pulseRemapSceneCopyPaletteRecommendationAlias']['coverage']})",
        f"- PULSE REMAP SCENE: {pulse_remap_suppression_scene_flavor} (plan={pulse_remap_suppression_scene_flavor_signals['suppressionPlan']} driftRisk={pulse_remap_suppression_scene_flavor_signals['driftRisk']} pressure={pulse_remap_suppression_scene_flavor_signals['pressureBand']} cadence={pulse_remap_suppression_scene_flavor_signals['laneCadenceRecency']})",
        f"- PULSE REMAP SCENE CONF: {pulse_remap_scene_confidence} (plan={pulse_remap_scene_confidence_signals['suppressionPlan']} driftRisk={pulse_remap_scene_confidence_signals['driftRisk']} pressure={pulse_remap_scene_confidence_signals['pressureBand']} reason={pulse_remap_scene_confidence_signals['reason']})",
        f"- PULSE REMAP SCENE MICROLINE VARIANT PACK: {pulse_remap_scene_microline_variant_pack['selectedMode']} (selected={pulse_remap_scene_microline_variant_pack['selected']} reason={pulse_remap_scene_microline_variant_pack_signals['reason']} conf={pulse_remap_scene_microline_variant_pack_signals['sceneConfidence']} trend={pulse_remap_scene_microline_variant_pack_signals['cadenceTrend']})",
        f"- PULSE REMAP SCENE MICROLINE STYLE POLICY: {pulse_remap_scene_microline_style_diversification_policy} (plan={pulse_remap_scene_microline_style_diversification_policy_signals['suppressionPlan']} conf={pulse_remap_scene_microline_style_diversification_policy_signals['sceneConfidence']} cadence={pulse_remap_scene_microline_style_diversification_policy_signals['laneCadenceRecency']} trend={pulse_remap_scene_microline_style_diversification_policy_signals['cadenceTrend']} vol={pulse_remap_scene_microline_style_diversification_policy_signals['cadenceVolatility']} reason={pulse_remap_scene_microline_style_diversification_policy_signals['reason']})",
        f"- PULSE REMAP SCENE MICROLINE STYLE POLICY SMOOTH: {pulse_remap_scene_microline_style_policy_smoothed} (current={pulse_remap_scene_microline_style_policy_smoothed_signals['currentPolicy']} prior={pulse_remap_scene_microline_style_policy_smoothed_signals['priorPolicy']} volatility={pulse_remap_scene_microline_style_policy_smoothed_signals['cadenceVolatility']} reason={pulse_remap_scene_microline_style_policy_smoothed_signals['reason']})",
        f"- PULSE REMAP SCENE MICROLINE STYLE POSTURE: {pulse_remap_scene_microline_style_policy_posture_hook} (policy={pulse_remap_scene_microline_style_policy_posture_hook_signals['smoothedPolicy']} trend={pulse_remap_scene_microline_style_policy_posture_hook_signals['styleTrend']} current={pulse_remap_scene_microline_style_policy_posture_hook_signals['currentNet']:+d} prior={pulse_remap_scene_microline_style_policy_posture_hook_signals['priorNet']:+d} cadence={pulse_remap_scene_microline_style_policy_posture_hook_signals['laneCadenceRecency']} reason={pulse_remap_scene_microline_style_policy_posture_hook_signals['reason']})",
        f"- PRSMPP: {pulse_remap_scene_microline_style_posture_alias if pulse_remap_scene_microline_style_posture_alias_flag_enabled else 'FLAG OFF'} (posture={pulse_remap_scene_microline_style_policy_posture_hook} flag={pulse_remap_scene_microline_style_posture_alias_flag_name} enabled={pulse_remap_scene_microline_style_posture_alias_flag_enabled})",
        f"- PULSE REMAP SCENE FX GLINT: {pulse_remap_scene_fx_glint} (posture={pulse_remap_scene_fx_glint_signals['stylePosture']} warning={pulse_remap_scene_fx_glint_signals['suppressionWarning']} conf={pulse_remap_scene_fx_glint_signals['sceneConfidence']} reason={pulse_remap_scene_fx_glint_signals['reason']})",
        f"- PRSFX: {pulse_remap_scene_fx_glint_alias if pulse_remap_scene_fx_glint_alias_flag_enabled else 'FLAG OFF'} (glint={pulse_remap_scene_fx_glint} flag={pulse_remap_scene_fx_glint_alias_flag_name} enabled={pulse_remap_scene_fx_glint_alias_flag_enabled})",
        f"- PULSE REMAP SCENE COPY PALETTE REC: {pulse_remap_scene_copy_palette_recommendation} (flavor={pulse_remap_scene_copy_palette_recommendation_signals['sceneFlavor']} glint={pulse_remap_scene_copy_palette_recommendation_signals['sceneFxGlint']} posture={pulse_remap_scene_copy_palette_recommendation_signals['stylePosture']} conf={pulse_remap_scene_copy_palette_recommendation_signals['sceneConfidence']} reason={pulse_remap_scene_copy_palette_recommendation_signals['reason']})",
        f"- PRSCP: {pulse_remap_scene_copy_palette_recommendation_alias if pulse_remap_scene_copy_palette_recommendation_alias_flag_enabled else 'FLAG OFF'} (palette={pulse_remap_scene_copy_palette_recommendation} flag={pulse_remap_scene_copy_palette_recommendation_alias_flag_name} enabled={pulse_remap_scene_copy_palette_recommendation_alias_flag_enabled})",
        f"- PRSMP: {pulse_remap_scene_microline_style_policy_alias if pulse_remap_scene_microline_style_policy_alias_flag_enabled else 'FLAG OFF'} (policy={pulse_remap_scene_microline_style_diversification_policy} flag={pulse_remap_scene_microline_style_policy_alias_flag_name} enabled={pulse_remap_scene_microline_style_policy_alias_flag_enabled})",
        f"- PRSMV: {pulse_remap_scene_microline_variant_pack_selection_alias if pulse_remap_scene_microline_variant_pack_selection_alias_flag_enabled else 'FLAG OFF'} (selectedMode={pulse_remap_scene_microline_variant_pack['selectedMode']} flag={pulse_remap_scene_microline_variant_pack_selection_alias_flag_name} enabled={pulse_remap_scene_microline_variant_pack_selection_alias_flag_enabled})",
        f"- PULSE REMAP SCENE MICROLINE CADENCE: {pulse_remap_scene_microline_cadence} (plan={pulse_remap_scene_microline_cadence_signals['suppressionPlan']} conf={pulse_remap_scene_microline_cadence_signals['sceneConfidence']} cadence={pulse_remap_scene_microline_cadence_signals['laneCadenceRecency']} trend={pulse_remap_scene_microline_cadence_signals['cadenceTrend']} reason={pulse_remap_scene_microline_cadence_signals['reason']})",
        f"- PRSMC: {pulse_remap_scene_microline_cadence_alias if pulse_remap_scene_microline_cadence_alias_flag_enabled else 'FLAG OFF'} (cadence={pulse_remap_scene_microline_cadence} flag={pulse_remap_scene_microline_cadence_alias_flag_name} enabled={pulse_remap_scene_microline_cadence_alias_flag_enabled})",
        f"- PRPW: {pulse_remap_suppression_posture_warning_alias if pulse_remap_suppression_posture_warning_flag_enabled else 'FLAG OFF'} (posture={pulse_remap_suppression_posture_warning} reason={pulse_remap_suppression_posture_warning_signals['reason']} flag={pulse_remap_suppression_posture_warning_flag_name} enabled={pulse_remap_suppression_posture_warning_flag_enabled})",
        f"- PRMS FAMILY TREND: {pulse_remap_suppression_family_trend_signals['trend']} (Δnet={pulse_remap_suppression_family_trend_drift:+d} currentNet={pulse_remap_suppression_family_trend_signals['currentNet']:+d} priorNet={pulse_remap_suppression_family_trend_signals['priorNet']:+d} loaded={pulse_remap_suppression_family_trend_signals['priorLoaded']})",
        f"- PRSCP FAMILY TREND: {pulse_remap_scene_copy_palette_recommendation_family_trend_signals['trend']} (Δnet={pulse_remap_scene_copy_palette_recommendation_family_trend_drift:+d} currentNet={pulse_remap_scene_copy_palette_recommendation_family_trend_signals['currentNet']:+d} priorNet={pulse_remap_scene_copy_palette_recommendation_family_trend_signals['priorNet']:+d} loaded={pulse_remap_scene_copy_palette_recommendation_family_trend_signals['priorLoaded']})",
        f"- PRSP FAMILY TREND: {pulse_remap_suppression_plan_family_trend_signals['trend']} (Δnet={pulse_remap_suppression_plan_family_trend_drift:+d} currentNet={pulse_remap_suppression_plan_family_trend_signals['currentNet']:+d} priorNet={pulse_remap_suppression_plan_family_trend_signals['priorNet']:+d} loaded={pulse_remap_suppression_plan_family_trend_signals['priorLoaded']})",
        f"- PRSMC FAMILY TREND: {pulse_remap_scene_microline_cadence_family_trend_signals['trend']} (Δnet={pulse_remap_scene_microline_cadence_family_trend_drift:+d} currentNet={pulse_remap_scene_microline_cadence_family_trend_signals['currentNet']:+d} priorNet={pulse_remap_scene_microline_cadence_family_trend_signals['priorNet']:+d} loaded={pulse_remap_scene_microline_cadence_family_trend_signals['priorLoaded']})",
        f"- PRSMC FAMILY CHURN: net {token_family_totals['pulseRemapSceneMicrolineCadenceAlias']['net']:+d} (added={token_family_totals['pulseRemapSceneMicrolineCadenceAlias']['added']} removed={token_family_totals['pulseRemapSceneMicrolineCadenceAlias']['removed']} churn={token_family_totals['pulseRemapSceneMicrolineCadenceAlias']['churn']} coverage={token_family_totals['pulseRemapSceneMicrolineCadenceAlias']['coverage']})",
        f"- PRSMP FAMILY TREND: {pulse_remap_scene_microline_style_policy_family_trend_signals['trend']} (Δnet={pulse_remap_scene_microline_style_policy_family_trend_drift:+d} currentNet={pulse_remap_scene_microline_style_policy_family_trend_signals['currentNet']:+d} priorNet={pulse_remap_scene_microline_style_policy_family_trend_signals['priorNet']:+d} loaded={pulse_remap_scene_microline_style_policy_family_trend_signals['priorLoaded']})",
        f"- DMG GLYPH: +{token_family_totals['dmgGlyphAlias']['added']} / -{token_family_totals['dmgGlyphAlias']['removed']} / net {token_family_totals['dmgGlyphAlias']['net']} (churn={token_family_totals['dmgGlyphAlias']['churn']} coverage={token_family_totals['dmgGlyphAlias']['coverage']})",
        f"- DMG GLYPH FX LIVE: +{token_family_totals['dmgGlyphFxLiveAlias']['added']} / -{token_family_totals['dmgGlyphFxLiveAlias']['removed']} / net {token_family_totals['dmgGlyphFxLiveAlias']['net']} (churn={token_family_totals['dmgGlyphFxLiveAlias']['churn']} coverage={token_family_totals['dmgGlyphFxLiveAlias']['coverage']})",
        f"- LPR HYS THR: +{token_family_totals['lanePriorityHysteresisThresholdAlias']['added']} / -{token_family_totals['lanePriorityHysteresisThresholdAlias']['removed']} / net {token_family_totals['lanePriorityHysteresisThresholdAlias']['net']} (churn={token_family_totals['lanePriorityHysteresisThresholdAlias']['churn']} coverage={token_family_totals['lanePriorityHysteresisThresholdAlias']['coverage']})",
        f"- LPR HYS WINDOW Δ: +{token_family_totals['lanePriorityHysteresisWindowDeltaAlias']['added']} / -{token_family_totals['lanePriorityHysteresisWindowDeltaAlias']['removed']} / net {token_family_totals['lanePriorityHysteresisWindowDeltaAlias']['net']} (churn={token_family_totals['lanePriorityHysteresisWindowDeltaAlias']['churn']} coverage={token_family_totals['lanePriorityHysteresisWindowDeltaAlias']['coverage']})",
        f"- LPR HYS FLOOR REC + LPR HYS FLOOR: +{token_family_totals['lanePriorityHysteresisFloorRecommendationAlias']['added']} / -{token_family_totals['lanePriorityHysteresisFloorRecommendationAlias']['removed']} / net {token_family_totals['lanePriorityHysteresisFloorRecommendationAlias']['net']} (churn={token_family_totals['lanePriorityHysteresisFloorRecommendationAlias']['churn']} coverage={token_family_totals['lanePriorityHysteresisFloorRecommendationAlias']['coverage']})",
        f"- LPR HYS FLOOR FAMILY TREND: {lane_priority_hysteresis_floor_family_trend_signals['trend']} (Δnet={lane_priority_hysteresis_floor_family_trend_drift:+d} currentNet={lane_priority_hysteresis_floor_family_trend_signals['currentNet']:+d} priorNet={lane_priority_hysteresis_floor_family_trend_signals['priorNet']:+d} loaded={lane_priority_hysteresis_floor_family_trend_signals['priorLoaded']})",
        f"- LPR HF T: {lane_priority_hysteresis_floor_family_trend_alias} (flag={lane_priority_hysteresis_floor_family_trend_alias_flag_name}, enabled={lane_priority_hysteresis_floor_family_trend_alias_flag_enabled}, trend={lane_priority_hysteresis_floor_family_trend_signals['trend']})",
        f"- LANE CADENCE SUMMARY: SYSTEMS/OPS {'OK' if (token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyFxAlias']['aliasesTouchedCount'] > 0 or token_family_totals['dmgGlyphAlias']['aliasesTouchedCount'] > 0 or token_family_totals['dmgGlyphFxLiveAlias']['aliasesTouchedCount'] > 0 or token_family_totals['dmgComboAlias']['aliasesTouchedCount'] > 0) else 'GAP'} (RGFXWRIUFX coverage={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyFxAlias']['coverage']}, churn={token_family_totals['routeGlowFxConfidenceWhyRailIntensityWhyConfidenceUrgencyFxAlias']['churn']} | DMG GLYPH coverage={token_family_totals['dmgGlyphAlias']['coverage']}, churn={token_family_totals['dmgGlyphAlias']['churn']} | DMG GLYPH FX LIVE coverage={token_family_totals['dmgGlyphFxLiveAlias']['coverage']}, churn={token_family_totals['dmgGlyphFxLiveAlias']['churn']} | DMG COMBO coverage={token_family_totals['dmgComboAlias']['coverage']}, churn={token_family_totals['dmgComboAlias']['churn']})",
        f"- LBA: {lane_bucket_age_compact_alias} (flag={lane_bucket_age_compact_alias_signals['flagName']}, enabled={lane_bucket_age_compact_alias_signals['flagEnabled']}, sys={lane_bucket_age_compact_alias_signals['systemsOpsHours']}h, dw={lane_bucket_age_compact_alias_signals['designWorldHours']}h, cv={lane_bucket_age_compact_alias_signals['combatVfxHours']}h)",
        f"- LANE BUCKET AGE: {lane_bucket_age['token'].split(':', 1)[1]} (status={lane_bucket_age['status']}, window={lane_bucket_age['windowHours']}h)",
        f"- LANE BUCKET AGE Δ: {lane_bucket_age_delta:+d}h (currentMax={lane_bucket_age_drift_signals['currentMaxAgeHours']}, priorMax={lane_bucket_age_drift_signals['priorMaxAgeHours']}, loaded={lane_bucket_age_drift_signals['priorLoaded']})",
        f"- LANE CADENCE RECENCY: {lane_cadence_recency} (status={lane_cadence_recency_signals['status']}, max={lane_cadence_recency_signals['maxAgeHours']}h, Δ={lane_cadence_recency_signals['deltaHours']:+d}h, window={lane_cadence_recency_signals['windowHours']}h, reason={lane_cadence_recency_signals['reason']})",
        f"- LANE CADENCE MISS RISK: {lane_cadence_miss_risk_token} (risk={lane_cadence_miss_risk_signals['risk']}, max={lane_cadence_miss_risk_signals['maxAgeHours']}h, Δ={lane_cadence_miss_risk_signals['deltaHours']:+d}h, window={lane_cadence_miss_risk_signals['windowHours']}h, reason={lane_cadence_miss_risk_signals['reason']})",
        f"- LCMR: {lane_cadence_miss_risk_alias_token} (flag={lane_cadence_miss_risk_alias_signals['flagName']}, enabled={lane_cadence_miss_risk_alias_signals['flagEnabled']}, risk={lane_cadence_miss_risk_alias_signals['risk']}, alias={lane_cadence_miss_risk_alias_signals['alias']})",
        f"- LANE PRIORITY REC: {lane_priority_recommendation} (reason={lane_priority_recommendation_signals['reason']}, worstAge={lane_priority_recommendation_signals['worstAgeHours']}h, offlineOnly={lane_priority_recommendation_signals['offlineOnly']})",
        f"- LPR: {lane_priority_recommendation_compact_alias} (flag={lane_priority_recommendation_compact_alias_signals['flagName']}, enabled={lane_priority_recommendation_compact_alias_signals['flagEnabled']}, rec={lane_priority_recommendation_compact_alias_signals['recommendation']}, alias={lane_priority_recommendation_compact_alias_signals['alias']})",
        f"- LPR HYS: {lane_priority_hysteresis_compact_alias} (flag={lane_priority_hysteresis_compact_alias_signals['flagName']}, enabled={lane_priority_hysteresis_compact_alias_signals['flagEnabled']}, applied={lane_priority_hysteresis_compact_alias_signals['hysteresisApplied']}, alias={lane_priority_hysteresis_compact_alias_signals['alias']})",
        f"- LPR HYS RAIL: {lane_priority_hysteresis_rail} (flag={lane_priority_hysteresis_rail_signals['flagName']}, enabled={lane_priority_hysteresis_rail_signals['flagEnabled']}, conf={lane_priority_hysteresis_rail_signals['confidence']}, gap={lane_priority_hysteresis_rail_signals['scoreGap']}, threshold={lane_priority_hysteresis_rail_signals['threshold']}, reason={lane_priority_hysteresis_rail_signals['reason']})",
        f"- LANE PRIORITY REC CONF: {lane_priority_recommendation_confidence_level} (worstAge={lane_priority_recommendation_confidence_signals['worstAgeHours']}h, momentumGap={lane_priority_recommendation_confidence_signals['momentumGapHours']}h, reason={lane_priority_recommendation_confidence_signals['reason']})",
        f"- LANE PRIORITY REC CONF GUARD: {'APPLY' if lane_priority_recommendation_confidence_guard_signals['guardApplied'] else 'HOLD'} (base={lane_priority_recommendation_confidence_guard_signals['baseConfidence']}, guarded={lane_priority_recommendation_confidence_guard_signals['guardedConfidence']}, trend={lane_priority_recommendation_confidence_guard_signals['trend']}, regime={lane_priority_recommendation_confidence_guard_signals['volatilityRegime']}, streak={lane_priority_recommendation_confidence_guard_signals['divergenceStreak']}, priorLoaded={lane_priority_recommendation_confidence_guard_signals['priorLoaded']}, reason={lane_priority_recommendation_confidence_guard_signals['reason']})",
        f"- LPRCG: {lane_priority_recommendation_confidence_guard_alias} (flag={lane_priority_recommendation_confidence_guard_alias_signals['flagName']}, enabled={lane_priority_recommendation_confidence_guard_alias_signals['flagEnabled']}, action={lane_priority_recommendation_confidence_guard_alias_signals['action']})",
        f"- LPRCG THRESH: {lane_priority_recommendation_confidence_guard_threshold} (policy={lane_priority_recommendation_confidence_guard_threshold_signals['policy']})",
        f"- LPRCG COACH: {lane_priority_recommendation_confidence_guard_persistence_coach_token} (reason={lane_priority_recommendation_confidence_guard_persistence_coach_signals['reason']}, action={lane_priority_recommendation_confidence_guard_persistence_coach_signals['guardAction']}, consecutive={lane_priority_recommendation_confidence_guard_persistence_coach_signals['consecutiveApplyWindows']}, priorLoaded={lane_priority_recommendation_confidence_guard_persistence_coach_signals['priorLoaded']}, offlineOnly={lane_priority_recommendation_confidence_guard_persistence_coach_signals['offlineOnly']})",
        f"- LPRCGC: {lane_priority_recommendation_confidence_guard_persistence_coach_alias} (flag={lane_priority_recommendation_confidence_guard_persistence_coach_alias_signals['flagName']}, enabled={lane_priority_recommendation_confidence_guard_persistence_coach_alias_signals['flagEnabled']}, coach={lane_priority_recommendation_confidence_guard_persistence_coach_alias_signals['coachToken']}, alias={lane_priority_recommendation_confidence_guard_persistence_coach_alias_signals['alias']})",
        f"- LPRCG COACH PACK: {lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_token} (reason={lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_signals['reason']}, action={lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_signals['guardAction']}, consecutive={lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_signals['consecutiveApplyWindows']}, regime={lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_signals['volatilityRegime']}, regimeChanged={lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_signals['regimeChanged']}, priorLoaded={lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_signals['priorLoaded']}, offlineOnly={lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_signals['offlineOnly']})",
        f"- LPRCGCP: {lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_alias} (flag={lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_alias_signals['flagName']}, enabled={lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_alias_signals['flagEnabled']}, pack={lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_alias_signals['packToken']}, alias={lane_priority_recommendation_confidence_guard_persistence_coach_variant_pack_alias_signals['alias']})",
        f"- LPRCG COACH COPY: {lane_priority_recommendation_confidence_guard_persistence_coach_copy_narrative} (reason={lane_priority_recommendation_confidence_guard_persistence_coach_copy_narrative_signals['reason']}, pack={lane_priority_recommendation_confidence_guard_persistence_coach_copy_narrative_signals['pack']}, action={lane_priority_recommendation_confidence_guard_persistence_coach_copy_narrative_signals['guardAction']}, regime={lane_priority_recommendation_confidence_guard_persistence_coach_copy_narrative_signals['volatilityRegime']}, priorRegime={lane_priority_recommendation_confidence_guard_persistence_coach_copy_narrative_signals['priorVolatilityRegime']}, regimeChanged={lane_priority_recommendation_confidence_guard_persistence_coach_copy_narrative_signals['regimeChanged']}, consecutive={lane_priority_recommendation_confidence_guard_persistence_coach_copy_narrative_signals['consecutiveApplyWindows']}, divergenceStreak={lane_priority_recommendation_confidence_guard_persistence_coach_copy_narrative_signals['divergenceStreak']}, offlineOnly={lane_priority_recommendation_confidence_guard_persistence_coach_copy_narrative_signals['offlineOnly']})",
        f"- LPRCGCN: {lane_priority_recommendation_confidence_guard_persistence_coach_copy_alias} (flag={lane_priority_recommendation_confidence_guard_persistence_coach_copy_alias_signals['flagName']}, enabled={lane_priority_recommendation_confidence_guard_persistence_coach_copy_alias_signals['flagEnabled']}, coachCopy={lane_priority_recommendation_confidence_guard_persistence_coach_copy_alias_signals['coachCopyToken']}, alias={lane_priority_recommendation_confidence_guard_persistence_coach_copy_alias_signals['alias']})",
        f"- LPRCG COACH COPY WHY: {lane_priority_recommendation_confidence_guard_persistence_coach_copy_why} (flag={lane_priority_recommendation_confidence_guard_persistence_coach_copy_why_signals['flagName']}, enabled={lane_priority_recommendation_confidence_guard_persistence_coach_copy_why_signals['flagEnabled']}, reason={lane_priority_recommendation_confidence_guard_persistence_coach_copy_why_signals['reason']}, short={lane_priority_recommendation_confidence_guard_persistence_coach_copy_why_signals['short']}, offlineOnly={lane_priority_recommendation_confidence_guard_persistence_coach_copy_why_signals['offlineOnly']})",
        f"- LPRCG + LANE PRIORITY REC CONF GUARD: +{token_family_totals['lanePriorityRecommendationConfidenceGuardAlias']['added']} / -{token_family_totals['lanePriorityRecommendationConfidenceGuardAlias']['removed']} / net {token_family_totals['lanePriorityRecommendationConfidenceGuardAlias']['net']} (churn={token_family_totals['lanePriorityRecommendationConfidenceGuardAlias']['churn']} coverage={token_family_totals['lanePriorityRecommendationConfidenceGuardAlias']['coverage']})",
        f"- LPRCG COACH + LPRCGC: +{token_family_totals['lanePriorityRecommendationConfidenceGuardCoachAlias']['added']} / -{token_family_totals['lanePriorityRecommendationConfidenceGuardCoachAlias']['removed']} / net {token_family_totals['lanePriorityRecommendationConfidenceGuardCoachAlias']['net']} (churn={token_family_totals['lanePriorityRecommendationConfidenceGuardCoachAlias']['churn']} coverage={token_family_totals['lanePriorityRecommendationConfidenceGuardCoachAlias']['coverage']})",
        f"- LPRCG COACH PACK + LPRCGCP FAMILY CHURN: +{token_family_totals['lanePriorityRecommendationConfidenceGuardCoachPackAlias']['added']} / -{token_family_totals['lanePriorityRecommendationConfidenceGuardCoachPackAlias']['removed']} / net {token_family_totals['lanePriorityRecommendationConfidenceGuardCoachPackAlias']['net']} (churn={token_family_totals['lanePriorityRecommendationConfidenceGuardCoachPackAlias']['churn']} coverage={token_family_totals['lanePriorityRecommendationConfidenceGuardCoachPackAlias']['coverage']})",
        f"- LPRCG COACH COPY + LPRCGCN FAMILY CHURN: +{token_family_totals['lanePriorityRecommendationConfidenceGuardCoachCopyAlias']['added']} / -{token_family_totals['lanePriorityRecommendationConfidenceGuardCoachCopyAlias']['removed']} / net {token_family_totals['lanePriorityRecommendationConfidenceGuardCoachCopyAlias']['net']} (churn={token_family_totals['lanePriorityRecommendationConfidenceGuardCoachCopyAlias']['churn']} coverage={token_family_totals['lanePriorityRecommendationConfidenceGuardCoachCopyAlias']['coverage']})",
        f"- LPRCG THRESH FAMILY CHURN: +{token_family_totals['lanePriorityRecommendationConfidenceGuardThresholdAlias']['added']} / -{token_family_totals['lanePriorityRecommendationConfidenceGuardThresholdAlias']['removed']} / net {token_family_totals['lanePriorityRecommendationConfidenceGuardThresholdAlias']['net']} (churn={token_family_totals['lanePriorityRecommendationConfidenceGuardThresholdAlias']['churn']} coverage={token_family_totals['lanePriorityRecommendationConfidenceGuardThresholdAlias']['coverage']})",
        f"- LANE PRIORITY REC HYSTERESIS: {'HOLD' if lane_priority_recommendation_signals['hysteresisApplied'] else 'SHIFT'} (prior={lane_priority_recommendation_signals['priorRecommendation']}, raw={lane_priority_recommendation_signals['rawRecommendation']}, gap={lane_priority_recommendation_signals['hysteresisScoreGap']}, threshold={lane_priority_recommendation_signals['hysteresisThreshold']}, reason={lane_priority_recommendation_signals['hysteresisReason']})",
        f"- LPR HYS THRESH REC: {lane_priority_hysteresis_threshold_tuning} (base={lane_priority_hysteresis_threshold_tuning_signals['baseThreshold']}, rec={lane_priority_hysteresis_threshold_tuning_signals['recommendedThreshold']}, floor={lane_priority_hysteresis_threshold_tuning_signals['adaptiveFloor']}, ceil={lane_priority_hysteresis_threshold_tuning_signals['adaptiveCeiling']}, priorWindow={lane_priority_hysteresis_threshold_tuning_signals['priorAdaptiveWindowLoaded']}, volSpan={lane_priority_hysteresis_threshold_tuning_signals['momentumVolatilitySpanHours']}, maxAbsMom={lane_priority_hysteresis_threshold_tuning_signals['maxAbsMomentumHours']}, ageSpread={lane_priority_hysteresis_threshold_tuning_signals['ageSpreadHours']}, learn={lane_priority_hysteresis_threshold_tuning_signals['learningReason']}, reason={lane_priority_hysteresis_threshold_tuning_signals['reason']})",
        f"- LPR VOL REGIME: {lane_priority_hysteresis_threshold_tuning_signals['volatilityRegimeMemory']} (current={lane_priority_hysteresis_threshold_tuning_signals['volatilityRegime']}, prior={lane_priority_hysteresis_threshold_tuning_signals['priorVolatilityRegime']}, reason={lane_priority_hysteresis_threshold_tuning_signals['volatilityRegimeReason']}, steps={lane_priority_hysteresis_threshold_tuning_signals['stepSizes']})",
        f"- LPR HYS THR: {lane_priority_hysteresis_threshold_compact_alias} (flag={lane_priority_hysteresis_threshold_compact_alias_signals['flagName']}, enabled={lane_priority_hysteresis_threshold_compact_alias_signals['flagEnabled']}, alias={lane_priority_hysteresis_threshold_compact_alias_signals['alias']}, rec={lane_priority_hysteresis_threshold_compact_alias_signals['recommendation']})",
        f"- LPR HYS WINDOW: {lane_priority_hysteresis_window_band} (floor={lane_priority_hysteresis_window_band_signals['adaptiveFloor']}, ceil={lane_priority_hysteresis_window_band_signals['adaptiveCeiling']}, span={lane_priority_hysteresis_window_band_signals['span']}, reason={lane_priority_hysteresis_window_band_signals['reason']})",
        f"- LPR HYS WINDOW Δ: {lane_priority_hysteresis_window_delta:+d} (current={lane_priority_hysteresis_window_delta_signals['currentBand']}, prior={lane_priority_hysteresis_window_delta_signals['priorBand']}, loaded={lane_priority_hysteresis_window_delta_signals['priorLoaded']})",
        f"- LPR HYS FLOOR REC: {lane_priority_hysteresis_floor_recommendation} (streak={lane_priority_hysteresis_floor_recommendation_signals['highStreak']}, threshold={lane_priority_hysteresis_floor_recommendation_signals['streakThreshold']}, currentRisk={lane_priority_hysteresis_floor_recommendation_signals['currentRisk']}, priorRisk={lane_priority_hysteresis_floor_recommendation_signals['priorRisk']}, Δ={lane_priority_hysteresis_floor_recommendation_signals['currentDeltaHours']:+d}, strongMomentum={lane_priority_hysteresis_floor_recommendation_signals['strongMomentum']}, reason={lane_priority_hysteresis_floor_recommendation_signals['reason']})",
        f"- LPR HYS FLOOR: {lane_priority_hysteresis_floor_recommendation_alias} (flag={lane_priority_hysteresis_floor_recommendation_alias_signals['flagName']}, enabled={lane_priority_hysteresis_floor_recommendation_alias_signals['flagEnabled']}, alias={lane_priority_hysteresis_floor_recommendation_alias_signals['alias']}, rec={lane_priority_hysteresis_floor_recommendation_alias_signals['recommendation']})",
        f"- PULSE HEAT FX COMPACT-BUDGET DRIFT: {pulse_heat_fx_compact_budget_drift_level} (compactNet={pulse_heat_fx_compact_budget_drift_signals['compactNet']:+d}, familyNet={pulse_heat_fx_compact_budget_drift_signals['familyNet']:+d}, churn={pulse_heat_fx_compact_budget_drift_signals['familyChurn']})",
        f"- ROUTE GLOW FX COMPACT-BUDGET DRIFT: {route_glow_fx_compact_budget_drift_level} (compactNet={route_glow_fx_compact_budget_drift_signals['compactNet']:+d}, familyNet={route_glow_fx_compact_budget_drift_signals['familyNet']:+d}, churn={route_glow_fx_compact_budget_drift_signals['familyChurn']})",
        f"- ROUTE GLOW FX CONF WHY RAIL MODE COMPACT-BUDGET DRIFT: {route_glow_fx_conf_why_rail_mode_compact_budget_drift_level} (compactNet={route_glow_fx_conf_why_rail_mode_compact_budget_drift_signals['compactNet']:+d}, familyNet={route_glow_fx_conf_why_rail_mode_compact_budget_drift_signals['familyNet']:+d}, churn={route_glow_fx_conf_why_rail_mode_compact_budget_drift_signals['familyChurn']})",
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
