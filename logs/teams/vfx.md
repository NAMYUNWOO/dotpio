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

## 2026-03-22 21:46 KST — Cycle AV forced-lane slice (combat/vfx)
- Coverage check over the last 10 completed items returned **world/design dominance (10/10, 100%)**, breaching the 40% lane cap.
- Chosen vertical slice intentionally rebalanced into underrepresented lane: `BERSERK FX:FADE   [THREAT Δ:<n>]` now fires when a sustained rise streak (>=2) cools or drops.
- Scope: readability-only cooldown relief cue; no combat stat/economy changes.
- Evidence: `lua scripts/regression_hud_berserker_counters.lua`, `lua scripts/regression_enemy_behavior_variants.lua`, `luac -p main.lua src/hud.lua`.
- Follow-up queue injected: `LANE CADENCE:OK|GAP` watchdog (systems/ops), `VIBE DRIFT` escalation glyph (world/design).

## 2026-03-22 23:35 KST — Cross-lane note
- No VFX token additions in this slice.
- Action-pace digest line is ops-facing and does not alter player-facing FX cues.

## 2026-03-23 03:41 KST — Cycle BB combat/vfx cadence pulse shipped
- Forced-lane rebalance follow-up selected underrepresented combat/vfx lane and shipped flagged digest token `ACTION PACE ALT WINDOW PULSE:COOL|LIVE|HOT`.
- Added classifier `action_pace_alt_window_pulse_from_signals()` in `scripts/weekly_portal_prompt_readability_drift.py`.
- Token mapping: `HOT` for tense/deferred fallback windows, `LIVE` for safe immediate probes, `COOL` otherwise (`OFF` when flag disabled).
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` and flagged digest generation run PASS.

## 2026-03-23 09:45 KST — Director lane-cadence note
- 24h cadence check remains satisfied before this cycle: at least one combat/vfx item (`ACTION PACE ALT WINDOW PULSE`, `BERSERK FX:*`), one design/world item, and one systems/ops item were completed.
- Added readability parity cue for portal pulse states (`PULSE FIT:Y|W|B|R`, flag-gated) so compact prompts preserve pulse clarity without adding new VFX runtime effects.
- Next proposed combat/vfx experiment candidate: `PULSE FLARE:+` compact warning when mode=`X` and fit downgrades to `B/R`.

## 2026-03-23 10:04 KST
- Task: Cycle BG compact pulse-flare warning slice (`PULSE FLARE:+`) behind `DOTPIO_EXPERIMENT_ROUTE_PULSE_FLARE_PROMPT`.
- Decision: Emit compact flare token only when `PULSE MODE:X` and fit is downgrade band (`B|R`), preserving compact prompt budget and keeping default behavior unchanged when flag is off.
- Evidence: `src/portal.lua`, `scripts/regression_portal_prompt_pulse_flare.lua`, `scripts/regression_portal_prompt_pulse_mode.lua`, `scripts/regression_portal_prompt_pulse_fit.lua`.
- Verification: `DOTPIO_EXPERIMENT_ROUTE_PULSE_MODE_PROMPT=1 lua scripts/regression_portal_prompt_pulse_mode.lua`; `DOTPIO_EXPERIMENT_ROUTE_PULSE_FIT_PROMPT=1 lua scripts/regression_portal_prompt_pulse_fit.lua`; `DOTPIO_EXPERIMENT_ROUTE_PULSE_MODE_PROMPT=1 DOTPIO_EXPERIMENT_ROUTE_PULSE_FIT_PROMPT=1 DOTPIO_EXPERIMENT_ROUTE_PULSE_FLARE_PROMPT=1 lua scripts/regression_portal_prompt_pulse_flare.lua`.
- Follow-up: Next highest-priority unchecked item remains Systems/UX token-priority mode (`FIT-FIRST|MODE-FIRST`).

## 2026-03-23 11:12 KST — Lane checkpoint
- No VFX token behavior changes this cycle.
- Digest now tracks priority mode context adjacent to pulse/link signals for post-run review.

## 2026-03-23 15:41 KST — Cycle BN VFX cooldown readability
- Added fade-intensity readability tier for berserker pressure cooldown messaging:
  - `BERSERK FX:FADE(SOFT)` for mild drop
  - `BERSERK FX:FADE(HARD)` for high-pressure or steep drop releases.
- Goal: make post-spike VFX feedback feel less binary and improve threat-relief legibility.
- Implemented helper in HUD (`getBerserkerFxFadeTier`) to keep severity mapping deterministic and regression-testable.
