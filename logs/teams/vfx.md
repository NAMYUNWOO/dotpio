# VFX Team Log


## 2026-03-22 15:41 KST — Cycle AQ kickoff (first VFX lane shipment)
- Forced-lane experiment delivered to satisfy cadence gap: added portal transition FX intensity cue tied to route pressure.
- Token contract:
  - `FX:CALM` for low pressure,
  - `FX:FLICKER` for mid pressure,
  - `FX:SURGE` for high pressure,
  - compact fallback `FX:C|F|S`.
- Scope: text-mode VFX language only (no mechanical/stat changes), fully reversible.
- Verification: portal prompt regression suite PASS.
- Next VFX candidate queued: combat pressure pulse token (`BERSERK FX:PULSE`) for sustained rising threat.

## 2026-03-22 17:01 KST — Cycle AQ berserker FX pulse follow-up
- Task: Add BERSERK FX:PULSE warning token when THREAT delta stays positive for 2+ consecutive turns.
- Scope: main.lua, src/hud.lua, scripts/regression_hud_berserker_counters.lua.
- Decision: Centralized streak/trigger logic in HUD helpers (updateBerserkerThreatRiseStreak, shouldTriggerBerserkerFxPulse) for deterministic behavior and regression coverage.
- Evidence: lua scripts/regression_hud_berserker_counters.lua PASS; lua scripts/regression_enemy_behavior_variants.lua PASS.
- Follow-up: Next unchecked backlog item is ROUTE VIGNETTE glyph prototype behind flag.
