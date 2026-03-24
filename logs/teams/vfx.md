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

## 2026-03-23 17:01 KST — Cycle BN vfx handoff
- Cross-surface tie-in shipped: berserker fade intensity now feeds portal cooloff trail semantics (`SOFT->CALM`, `HARD->ASH`).
- Verification: portal vibe-trail regression PASS under flag.

## 2026-03-23 21:41 KST — Cycle BT combat/vfx vertical slice (forced-lane)
- Coverage check (last 10 completed items): systems/ops=6, design/world=3, combat/vfx=1, ai-content=0, ux=0, qa=0.
- Lane cap breached (`systems/ops` 60% > 40%), so this cycle forced an underrepresented lane pick.
- Shipped compact pressure-fantasy cue `PULSE HEAT FX:CALM|SPARK|BLAZE` behind `DOTPIO_EXPERIMENT_PULSE_HEAT_FX`.
- Scope remains readability-only; no combat stats, AI cadence, economy, or routing logic changed.
- Verification: `DOTPIO_EXPERIMENT_PULSE_HEAT_CUE=1 DOTPIO_EXPERIMENT_PULSE_HEAT_FX=1 lua scripts/regression_portal_pulse_heat_fx.lua` PASS.

## 2026-03-24 00:34 KST — Route glow FX token prototype
- Added prompt-level VFX cue token `ROUTE GLOW FX` mapped to pulse-heat pressure state.
- Mapping: calm/warm retain tonal FX (`SOFT/SHARP`), hot elevates to `SURGE` for overdrive readability.

## 2026-03-24 00:37 KST — Cycle BV FX token compact mode
- Route glow FX token now supports compact alias for prompt-budget preservation without changing FX tier mapping.

## 2026-03-24 03:47 KST — Cycle BZ combat/vfx rail-mode readability slice (forced-lane rebalance)
- Coverage check (last 10 completed items by lane): systems=5, world=2, ux=2, combat/vfx=1, design=0, ai-content=0, qa=0.
- Lane cap breach detected (`systems` 50% > 40%), so experiment pick was forced into underrepresented lanes.
- Shipped compact pressure-readability token `RGFXWRM:LOCK|FLEX` behind `DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_MODE`.
- Mapping keeps VFX intent deterministic: `SPIKE+SURGE -> LOCK`; all other rail-present states -> `FLEX`.
- Follow-up candidate injected: `RGFXWRI:SOFT|HARD` intensity accent token for stronger overdrive fantasy.

## 2026-03-24 04:34 KST — Cycle BZ rail-intensity accent
- Added compact overdrive accent token `RGFXWRI:SOFT|HARD` behind `DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY`.
- Mapping aligns with rail lock semantics for stronger feel without changing routing logic: `LOCK=>HARD`, `FLEX=>SOFT`.
- Regression evidence: `scripts/regression_portal_route_glow_fx_conf_why_rail_intensity.lua` PASS.

## 2026-03-24 09:01 KST — Cycle CD vfx readability continuity
- New urgency token sits on top of existing route-glow confidence/intensity stack for faster cue parsing.
- No VFX tier mapping (`SOFT|HARD`, `CALM|SPARK|BLAZE`) changed in this cycle.


## 2026-03-24 09:41 KST — Cycle CE forced-lane combat/vfx slice
- Coverage rebalance trigger hit (`design/world` dominated last 10 completions), so this cycle forced combat/vfx execution.
- Added flag-gated urgency FX token `RGFXWRIUFX:CALM|SPARK|BLAZE` via `DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF_URGENCY_FX`.
- Deterministic mapping mirrors urgency tier only (`LOW->CALM`, `MID->SPARK`, `HIGH->BLAZE`) with no mechanics or damage model changes.

## 2026-03-24 13:45 KST
- VFX lane note: no new FX mappings this slice; digest now cleanly separates urgency parity compact alias churn (`RGFXWRIUP`) from urgency FX churn (`RGFXWRIUFX`).

## 2026-03-24 14:33 KST — Cycle CI hit-feedback readability pass
- Added floating hit-number visual feedback hook for both melee and magic impacts (drift + fade).
- Palette decision: melee = warm gold, magic = arcane violet for quick channel differentiation without extra glyph clutter.
- No camera shake or particle layering added in this slice to keep DOS readability stable.
- 2026-03-24 16:01 KST — Added corpse fade visual pass (pink-tinted sprite fade over 0.4s) so hit numbers and kill confirmation read as one beat. Follow-up: consider alternate tint per biome/theme.

## 2026-03-24 16:31 KST — Cycle CK (VFX sync)
- No new VFX token or rendering changes in this cycle.
- VFX lane remains available for next forced-lane rebalance if cadence drops.

## 2026-03-24 18:01 KST — Lethal floating-number readability
- Added lethal-hit emphasis style for floating numbers: red tint + exclamation suffix (`!`).
- Rationale: preserve quick kill-anchor readability after corpse-fade addition without increasing effect clutter.
- Validation path: `lua scripts/regression_combat_damage_numbers.lua` + `lua scripts/regression_enemy_death_fade.lua`.

## 2026-03-24 19:01 KST — DMG GLYPH burst prototype
- Added flag-gated floating-number glyph accents tied to burst band (`·`, `✦`, `✹`) under `DOTPIO_EXPERIMENT_DAMAGE_GLYPH_BURST`.
- Kept additive/reversible scope: default visuals unchanged when flag is off.
- Verified lethal accent (`!` + red tint) still composes with glyph output.

## 2026-03-24 19:12 KST — VFX sync
- No new runtime VFX logic in Cycle CN; this cycle added digest tracking for `DMG GLYPH:` churn to improve effect-lane auditability.

## 2026-03-24 20:05 KST — Cycle CN follow-up (DMG glyph remap policy)
- Synced on offline-only recommendation lane for `DMG GLYPH` shape remap policy derived from weekly digest trend signals.
- Outcome: policy surfaced in digest as `DMG GLYPH SHAPE REMAP REC` with deterministic recommendation bands and guidance; runtime combat mapping unchanged.
- Verification reference: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` PASS.
- Follow-up: monitor churn/risk windows; only consider runtime remap if recommendation remains stable across multiple windows.
