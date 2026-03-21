# Combat Team Log


### 2026-03-19 23:59 KST
- Task: Mission momentum bonus payout experiment (objective completion streak SRL micro-reward).
- Decision: Logged lane impact for streak-based reward model (1,1,2 SRL) with reward cap and no duplicate payout on already-complete objectives.
- Evidence: `src/run_missions.lua`, `main.lua`, `scripts/regression_mission_momentum.lua` (+ mission regressions).
- Follow-up: Monitor telemetry for early-run SRL inflation and tune reward curve if low-tier churn increases.

## 2026-03-20 00:26 KST — cross-lane sync note
- Context: World/System completed map_03~07 identity metadata + encounter rhythm profile wiring.
- Impact: No content schema break; existing flows remain stable with differentiated pacing.
- Follow-up: Validate player readability and portal landmark cues in upcoming portal reposition task.

## 2026-03-20 00:58 KST
- Cross-lane note: World portal reposition pass completed for map_03~07 with validator/regression green.
- Impact: traversal landmarks and fallback routes are clearer; no economy/combat/UI schema changes required in this patch.
- Follow-up: monitor playtest readability feedback and tune labels/cues if confusion persists.

## 2026-03-20 01:28:00 KST
- Task: P2 backlog item `Add weekly sustain audit JSON pretty mode`.
- Commit: HEAD (pending)
- Files:
  - `scripts/audit_weekly_sustain_cron.sh`
  - `scripts/regression_weekly_cron_audit.py`
  - `POST_RC_BACKLOG.md`
- Verification:
  - `python3 -m py_compile scripts/regression_weekly_cron_audit.py` ✅
  - `python3 scripts/regression_weekly_cron_audit.py` ✅
- Decisions:
  - Added `--pretty` flag for `--format json` to emit indented, human-readable audit payload while keeping compact JSON default stable.
  - Added guardrail: `--pretty` rejects non-JSON formats to avoid ambiguous output modes.
- Follow-up:
  - Next P2 priority: `Add sustain health dashboard markdown report`.

## 2026-03-20 01:59:00 KST
- Task: P2 backlog item `Add sustain health dashboard markdown report`.
- Commit: HEAD (pending)
- Files:
  - scripts/sustain_health_dashboard.py
  - scripts/regression_sustain_health_dashboard.py
  - scripts/run_weekly_sustain.sh
  - logs/playtests/rc_checklist.md
  - POST_RC_BACKLOG.md
  - logs/sustain_health_dashboard.md
- Verification:
  - `python3 -m py_compile scripts/sustain_health_dashboard.py scripts/regression_sustain_health_dashboard.py` ✅
  - `python3 scripts/regression_sustain_health_dashboard.py` ✅
  - `bash scripts/run_weekly_sustain.sh` ✅
- Decisions:
  - Weekly sustain runner now emits a single markdown dashboard rollup (economy safety, telemetry freshness, scheduler audit signal).
  - Dashboard consumes cron audit JSON when available and degrades gracefully to warning when managed cron entry is absent.
- Follow-up:
  - Next P2 priority: `Add automatic stale-branch/report drift check`.

## 2026-03-20 02:26 KST — P2 stale-branch/report drift guardrail handoff
- Combat lane verified no combat tuning deltas are involved in this operations-focused task.
- Decision: keep combat regressions out of this checker to avoid duplicate signal noise; checker remains branch/report freshness only.
- Follow-up: none.

## 2026-03-20 03:00 KST — P2 sustain dashboard JSON mode handoff
- Combat lane verified no combat behavior/balance changes in this ops task.
- Decision: keep regression scope focused on dashboard output contracts (markdown + json) to avoid unrelated combat churn.
- Follow-up: none.

## 2026-03-20 03:29 KST — P2 sustain dashboard trend classification handoff
- Combat lane verified no combat tuning/code changes in this ops task.
- Decision: combat pipeline remains unchanged; only sustain dashboard contract updated.
- Follow-up: none.

## 2026-03-20 03:58 KST — cross-lane handoff
- Combat lane impact review: no combat logic/balance adjustments in this task.
- Decision: streak display is HUD/readout only; momentum reward curve (1,1,2) remains unchanged.
- Follow-up: none.

## 2026-03-20 04:29 KST
- Task: Combat systems unchanged in this cycle.
- Commit: HEAD (this run)
- Verification: Indirect via mission regressions passing (`scripts/regression_run_missions.lua`).
- Decisions:
  - No enemy behavior/damage pacing modifications were required for momentum variety bonus.

## 2026-03-20 04:59 KST
- Task: Combat lane impact check for mission-pack flavor tag feature.
- Verification: `lua scripts/regression_run_missions.lua` ✅
- Decisions:
  - No combat behavior/damage pacing changes; update is UI metadata only.

## 2026-03-20 05:29 KST
- Task: P1 combat experiment `Add berserker desperation behavior (low-HP speed/damage spike) with regression coverage`.
- Commit: HEAD (this run)
- Files: `src/enemy_ai.lua`, `src/entities.lua`, `scripts/regression_enemy_behavior_variants.lua`, `POST_RC_BACKLOG.md`
- Verification:
  - `luac -p src/enemy_ai.lua src/entities.lua scripts/regression_enemy_behavior_variants.lua` ✅
  - `lua scripts/regression_enemy_behavior_variants.lua` ✅
- Decisions:
  - Added new `berserker` archetype that flips into desperation mode at low HP for faster cadence + higher damage.
  - Kept desperation deterministic (`hp <= 2`) and reversible through profile fields to allow quick rebalance/rollback.
- Follow-up:
  - Next experiment candidate: telegraph desperation state in HUD/combat log for readability testing.

## 2026-03-20 05:44 KST
- Task: P1 combat readability experiment — telegraph berserker desperation state.
- Commit: HEAD (this run)
- Files: `src/enemy_ai.lua`, `main.lua`, `scripts/regression_enemy_behavior_variants.lua`, `POST_RC_BACKLOG.md`, `TASKS.md`
- Verification:
  - `luac -p src/enemy_ai.lua main.lua scripts/regression_enemy_behavior_variants.lua` ✅
  - `lua scripts/regression_enemy_behavior_variants.lua` ✅
- Decisions:
  - Added one-shot transition signal (`justEnteredDesperation`) so readability cues fire only on state change, not every frame.
  - Kept combat tuning unchanged; this slice focuses strictly on threat telegraph clarity.
- Follow-up:
  - Next experiment candidate: one-turn pre-lunge tell before desperation attacks.

## 2026-03-20 06:02 KST
- Task: P1 combat readability/fairness experiment — one-turn pre-lunge tell for berserker desperation attacks.
- Commit: HEAD (this run)
- Files: `src/enemy_ai.lua`, `src/entities.lua`, `main.lua`, `src/hud.lua`, `scripts/regression_enemy_behavior_variants.lua`, `TASKS.md`, `POST_RC_BACKLOG.md`
- Verification:
  - `lua scripts/regression_enemy_behavior_variants.lua` ✅
  - `luac -p src/enemy_ai.lua src/entities.lua src/hud.lua main.lua` ✅
- Decisions:
  - Desperate berserkers now telegraph once (`desperationLungePrimed`) before each lunge hit window.
  - Telegraph consumes an attack turn and emits runtime event `berserker_lunge_telegraph` for status/HUD readability.
- Follow-up:
  - Balance-check if one-turn wind-up over-nerfs berserker pressure on higher-tier maps.

## 2026-03-20 06:30 KST — P1 combat fairness follow-up: berserker post-lunge recovery
- Decision: berserker desperation chain now enforces a one-turn recovery window immediately after lunge impact.
- Implementation: enemy AI tracks `desperationRecoveryPending`; attack cadence becomes telegraph -> lunge hit -> recovery pause.
- Verification: `luac -p src/enemy_ai.lua src/entities.lua main.lua scripts/regression_enemy_behavior_variants.lua` and `lua scripts/regression_enemy_behavior_variants.lua`.
- Follow-up: if combat pacing gets too forgiving, tune recovery cadence by profile flag rather than removing readability window.

## 2026-03-20 06:58 KST — HUD berserker recovery counter readability slice
- Added HUD-facing combat threat counter signal for berserker post-lunge recovery state (`desperationRecoveryPending`).
- Decision: keep recovery indicator gated behind active desperation to avoid noisy baseline HUD.
- Verification coupled with HUD regression script for counter semantics.

## 2026-03-20 07:26 KST — Combat unaffected by mission preview update
- Scope check: no enemy behavior/timing/damage deltas.
- Follow-up: keep berserker readability counters independent from mission metadata row.

## 2026-03-20 07:56 KST — Combat unchanged by variety counter update
- Scope check: no enemy behavior/damage cadence changes.
- Follow-up: keep combat threat strip independent from mission metadata counters.

## 2026-03-20 08:28 KST — Berserker pressure readability index
- Decision: added weighted HUD threat index for desperate berserkers (`Threat = desperate*1 + lungePrimed*2 + recoveryPending*1`) to summarize short-term pressure.
- Evidence: `src/hud.lua`, `scripts/regression_hud_berserker_counters.lua`.
- Follow-up: monitor if threat weighting needs rebalance after more playtest telemetry.

## 2026-03-20 08:56 KST — Berserker threat tier readability
- Completed HUD readability follow-up: mapped weighted berserker threat score to discrete tiers (`LOW|MED|HIGH`).
- Decision: use stable thresholds `0-2=LOW`, `3-5=MED`, `>=6=HIGH` to keep pressure interpretation deterministic across runs.
- Follow-up: if combat pacing changes alter score distribution, retune thresholds with telemetry-backed percentile bands.

## 2026-03-20 09:28 KST — Combat readability color pass
- Decision: threat-tier line now color-codes semantic danger (`LOW` green / `MED` amber / `HIGH` red) while preserving existing compact text.
- Follow-up: if players overfocus on color-only signal, consider subtle glyph reinforcement in a later UX pass.

## 2026-03-20 10:06 KST — Threat formula legend follow-up
- Completed readability follow-up: exposed weighted threat formula directly in active berserker HUD strip via `THREAT = B + 2*L + R` breakdown line.
- Decision: keep formula live-computed from counters so score decomposition remains auditable during high-pressure turns.
- Follow-up: if line wraps on lower resolutions, collapse to compact token format (`T=B+2L+R`) behind config flag.

## 2026-03-20 10:35 KST — Threat pacing delta readability
- Added turn-over-turn threat delta row (`THREAT Δ`) under threat score/tier to expose pressure acceleration/deceleration in live combat.
- Decision: color delta by direction (up=warm, down=cool, flat=neutral) while retaining explicit signed text for accessibility.

## 2026-03-20 10:58 KST — Combat signal hooked into onboarding
- Wired berserker enrage/lunge events to mark onboarding `threat` milestone so players retire combat tutorial only after real threat exposure.
- Scope check: no enemy behavior/cadence tuning changes (signal-only integration).

## 2026-03-20 11:06 KST — Pressure-breaker dodge consumption on enemy attack
- Task: Make pressure-breaker reward materially affect combat pacing.
- Decision: Consume dodge charge at hit resolution in `EnemyAI.update` and return `dodged_player` event; preserve berserker lunge recovery sequencing even when hit is dodged.
- Result: Rising-threat objective clears create one short tactical escape window without suppressing enemy cadence.
- Follow-up: Validate stacked-charge readability if future tasks increase reward intensity.

## 2026-03-20 11:26 KST — Overclock aggro spike pressure profile
- Added global threat-pressure plumbing from hazard pulse into enemy AI (`EnemyAI.setThreatPressure`).
- During pulse, enemies receive aggro spike via faster move cadence multiplier + detect/chase range bonus.
- Intent: SRL discount window is explicitly high-risk; combat pressure rises during discount uptime.

## 2026-03-20 12:01 KST — Weekly changelog drift detector rollout
- Completed backlog item: `QA/Systems: Add weekly changelog drift detector (code changes without corresponding team-log/report entry)`.
- Added `scripts/weekly_changelog_drift_check.py` + `scripts/regression_weekly_changelog_drift.py` and wired them into `scripts/run_weekly_sustain.sh` / RC sustain checklist.
- Verification: `python3 -m py_compile scripts/weekly_changelog_drift_check.py scripts/regression_weekly_changelog_drift.py`; `python3 scripts/regression_weekly_changelog_drift.py`; `bash scripts/run_weekly_sustain.sh`.
- Follow-up: next backlog priority is `Ops: Add sustain dashboard regression risk score (0~100) with threshold alert section`.

## 2026-03-20 13:05 KST
- Task: P2 Ops backlog — sustain dashboard regression risk score (0~100) + threshold alert section.
- Commit: HEAD (this run)
- Files: `scripts/sustain_health_dashboard.py`, `scripts/regression_sustain_health_dashboard.py`, `POST_RC_BACKLOG.md`
- Verification:
  - `python3 -m py_compile scripts/sustain_health_dashboard.py scripts/regression_sustain_health_dashboard.py` ✅
  - `python3 scripts/regression_sustain_health_dashboard.py` ✅
  - `bash scripts/run_weekly_sustain.sh` ✅
- Decisions:
  - Dashboard now emits `regressionRisk` payload with score/level/alert and fixed thresholds (`warnAt=30`, `alertAt=60`).
  - Markdown dashboard now includes a dedicated **Regression Risk** section with threshold alert status.
- Follow-up:
  - Backlog item marked done; queue next Game Director/Ops candidate.


## 2026-03-20 13:28 KST — Overclock hazard HUD countdown readability pass
- Decision: Overclock status hint now includes live seconds for active pulse (`OVERCLOCK HOT <n>s`) and cooldown (`OVERCLOCK CD <n>s`) to reduce timing ambiguity.
- Evidence: `lua scripts/regression_overclock_hazard.lua`; `luac -p src/overclock_hazard.lua`.
- Follow-up: Consider mirroring countdown near build preview panel for players who open inventory during hazard pulses.

## 2026-03-20 14:00 KST — Sustain dashboard regression-risk driver breakdown
- Decision: Added `regressionRisk.topDrivers` (top 3 contributors) to dashboard payload and markdown so ops reviews can immediately see what is driving score changes.
- Evidence: `python3 scripts/regression_sustain_health_dashboard.py`; `python3 scripts/sustain_health_dashboard.py --format json --pretty`.
- Follow-up: If risk repeatedly trends WARN/ALERT, add automated recommendation mapping each driver to a concrete remediation runbook step.

## 2026-03-20 14:29 KST — Combat pressure communication sync
- Hazard hint now exposes a stable risk tier so combat pacing spikes from aggro pressure are telegraphed before engagement.
- No enemy behavior coefficients changed this pass.

## 2026-03-20 14:56 KST — overclock aggro-pressure legend follow-up
- Task: Add active-pulse HUD hint legend for overclock aggro pressure (`AGGRO DET:+n MOVE:+m%`).
- Decision: Keep mechanic unchanged; surface detect/move pressure explicitly in HOT hint for faster risk parsing.
- Evidence: `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua`; `lua scripts/regression_overclock_hazard.lua`.
- Follow-up: Observe readability during next map_07 playtest and adjust wording only if hint width becomes noisy.

## 2026-03-20 16:29 KST — Combat lane note
- Decision: No combat behavior tuning in this slice; aggro pressure model remains unchanged.
- Follow-up: Monitor whether imminent warning shifts player engagement timing with active aggro pulses.

## 2026-03-20 17:31 KST — Overclock next-pulse bounty budget readability
- Decision: READY/CD overclock HUD hints now include `NEXT BOUNTY:0/y` so players can pre-plan hot-zone reward windows before pulse activation.
- Scope: No combat/economy math changes; display-only hint extension around existing kill-bounty cap.
- Evidence: `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua` and `lua scripts/regression_overclock_hazard.lua` PASS.
- Follow-up: Add next Game Director experiment candidate (no unchecked backlog items remain).

## 2026-03-20 18:01 KST — Post-RC hazard readability wave 2: overclock risk-tier HUD color
- Task: Color-code overclock RISK tier token in HUD hint (LOW/MED/HIGH).
- Decision: Implemented tier-aware HUD color metadata from hazard module and threaded it through HUD auxiliary hint rendering with fallback color.
- Evidence: ; [PASS] overclock hazard regression validated.
- Follow-up: Queue next Post-RC gameplay/UX experiment candidate.

## 2026-03-20 18:31 KST — P1 hazard readability wave 3: overclock risk-factor breakdown token
- Task: Added compact HUD token "RISK SRC:Dx+DETy+MOVEz" across OVERCLOCK READY/HOT/CD hints.
- Decision: Expose risk component math (discount + detect + move) inline for fast tuning readability without changing hazard mechanics.
- Evidence: luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua; lua scripts/regression_overclock_hazard.lua (PASS).
- Follow-up: If HUD width pressure appears in smaller layouts, abbreviate token labels while keeping component values visible.

## 2026-03-20 19:03 KST — Overclock next-pulse ETA HUD token
- Task: Add `NEXT PULSE:<n>s` timing token to overclock READY/CD hint flow for clearer hazard re-entry planning.
- Scope: `src/overclock_hazard.lua`, `scripts/regression_overclock_hazard.lua`, backlog tracking docs.
- Verification: `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua` and `lua scripts/regression_overclock_hazard.lua` (PASS).
- Follow-up: pick next unchecked Post-RC gameplay readability experiment item.

## 2026-03-20 19:39 KST — Combat readability impact (overclock timing)
- Decision: Added pulse/recharge progress tokens to support combat commit/withdraw decisions around overclock zones.
- Guardrail: No damage, aggro multiplier, or enemy behavior tuning in this patch.
- Follow-up: Pair with future threat-strip telemetry if timing misreads remain high.


## 2026-03-20 20:01 KST
- Task: P1 Hazard Readability Wave 6 - overclock risk-trend HUD token (RISK Δ:+n|-n).
- Decision: Kept risk-tier/score static and added state-aware delta signaling (+2 HOT, +1 IMMINENT in-zone cooldown, 0 otherwise) to preserve compact DOS readability.
- Evidence: `lua scripts/regression_overclock_hazard.lua` => PASS.
- Follow-up: Consider exposing token color metadata so RISK Δ can mirror rising/neutral/falling pressure semantics in a future wave.
## 2026-03-20 20:33 KST — P1 hazard readability wave 7: overclock zone-presence token
- Completed slice: added `ZONE:IN|OUT` token to overclock HUD hints (READY/HOT/CD/IMMINENT) for immediate hazard-context readability.
- Verification: `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua` and `lua scripts/regression_overclock_hazard.lua`.
- Follow-up: inject next Game Director experiment candidate (no unchecked backlog items remain).

## 2026-03-20 21:04 KST
- Task context: Overclock HUD readability update (`EXPOSED:<n>s`).
- Decision: Combat balance/behavior unchanged; token is informational only.
- Follow-up: Consider using exposure duration as an optional trigger input for future hazard-combat synergies.

## 2026-03-20 21:34 KST — Post-RC hazard readability wave 9 (`COMMIT` token)
- Completed item: overclock HUD hints now include `COMMIT:LOW|MID|HIGH` while player is in-zone (`ZONE:IN`), derived from continuous `EXPOSED` duration.
- Decision: commitment tier thresholds fixed at `LOW <5s`, `MID <12s`, `HIGH >=12s` for compact risk readability without tuning gameplay balance.
- Evidence: `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua` and `lua scripts/regression_overclock_hazard.lua` passed.
- Follow-up: if additional unchecked backlog item is needed next cycle, queue next hazard readability experiment candidate.

## 2026-03-20 22:01 KST — Post-RC hazard readability wave 10 follow-up (WINDOW token)
- Task: Add post-pulse relief burst token (`WINDOW:<n>s`) for out-of-zone cooldown readability.
- Scope: `src/overclock_hazard.lua`, `scripts/regression_overclock_hazard.lua`, `TASKS.md`, `POST_RC_BACKLOG.md`.
- Decision: Relief window now arms only when player disengages during HOT and pulse then expires while outside; token is shown only during out-of-zone cooldown and auto-expires.
- Evidence: `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua`; `lua scripts/regression_overclock_hazard.lua` (PASS).
- Follow-up: Next unchecked backlog item is overclock dwell-bucket telemetry (`LOW|MID|HIGH`).

## 2026-03-20 22:35 KST — Sync note
- No combat behavior/damage window tuning changes in this cycle.
- Existing overclock pressure behavior unchanged; only dwell telemetry was added.

## 2026-03-20 23:03 KST — No combat behavior tuning changes this slice
- Berserker/overclock combat mechanics unchanged.
- Task limited to reward telemetry snapshot + run-summary readability.

## 2026-03-20 23:33 KST — No combat tuning changes this slice
- Overclock combat behavior values unchanged.
- Added only run-history telemetry persistence and trend combiner reporting.

## 2026-03-20 23:36 KST — Combat behavior unchanged (profile-only readout)
- No enemy tuning or overclock combat math changes.
- Added only post-run interpretation token from existing dwell telemetry.

## 2026-03-21 00:02 KST — P1 Game Director Cycle B follow-up: overclock dwell volatility token
- Task: Add trend-artifact volatility token (`VOL:STEADY|SWING`) for overclock dwell cadence triage.
- Scope: `scripts/overclock_dwell_trend.py`, `scripts/regression_overclock_dwell_trend.py`, `POST_RC_BACKLOG.md`.
- Decision: Classified volatility from run-to-run total-exposure relative deltas (`maxΔ>=45%` or `avgΔ>=30%` => `SWING`; else `STEADY`) to keep signal compact/reversible.
- Verification: `python3 -m py_compile scripts/overclock_dwell_trend.py scripts/regression_overclock_dwell_trend.py`; `python3 scripts/regression_overclock_dwell_trend.py`; `python3 scripts/overclock_dwell_trend.py --runs 3`.
- Follow-up: Remaining unchecked backlog item is `QA/UX Team: run-summary overclock analytics glossary row (DWELL/EFF/PROFILE)`.

## 2026-03-21 00:32 KST — Cross-lane sync: run-summary overclock glossary row
- Synced backlog closure: compact glossary row for run-summary analytics tokens (`DWELL`, `EFF`, `PROFILE`) is now shipped.
- Evidence: `scripts/regression_run_summary.lua` PASS + HUD syntax check PASS.
- No lane-specific balance/system behavior change; readability/documentation-only increment.

## 2026-03-21 00:36 KST — Game Director Cycle C sync
- Reviewed idea slate (UX coach cue / threat scaler / hazard route tags).
- This cycle shipped only low-risk coach cue slice; no lane runtime mechanics changed.
- Mid/high-risk experiments queued in backlog for future cycle.

## 2026-03-21 01:04 KST — Combat pressure hook for mission payout context
- Wired mission completion context to include live berserker threat tier (`LOW|MED|HIGH`) from HUD threat counters.
- This keeps experiment coupling explicit: combat pressure informs mission reward scaling only when flag is enabled.
- No enemy behavior tables changed; pacing risk is isolated to reward layer.

## 2026-03-21 01:34 KST — Combat lane note (no behavior tuning)
- Route-tag callout update does not modify enemy AI, damage, or pacing.
- Existing berserker threat strip remains source of combat pressure; route token is navigation-only context.

## 2026-03-21 02:06 KST — Combat lane note (no pacing/AI changes)
- Portal confirmation + route-preview prompt does not alter enemy behavior, threat math, or damage flow.
- Combat systems remain unchanged; regression reused to confirm no collateral break in hazard threat HUD data path.

## 2026-03-21 02:31 KST — Lane note (combat unchanged)
- Route-tag audit and portal coaching copy are non-combat changes.
- Berserker threat logic and pressure systems are untouched this cycle.

## 2026-03-21 03:06 KST — Combat lane note (no tuning changes)
- Added portal-route density analytics only; no combat behavior/damage/threat math modified.
- Combat balance impact is observational via richer routing telemetry.

## 2026-03-21 03:35 KST — Cross-lane combat note
- No combat pacing/math changes in this cycle.
- Added pending experiment candidate for future cycle: route-pressure token that may consume threat-tier context (`PRESSURE:<n>`), currently backlog-only.

## 2026-03-21 04:12 KST — Portal transition prompt token-order linter + budget parser
- Task: QA/Design backlog closure for transition prompt readability order enforcement.
- Scope touched:
  - `src/portal_prompt_linter.lua`
  - `scripts/check_portal_prompt_token_order.lua`
  - `scripts/regression_portal_prompt_token_order.lua`
  - `POST_RC_BACKLOG.md`
- Decision: enforce prompt semantic order `ACTION -> ROUTE -> COACH -> PRESSURE` in sampled portal prompt variants and verify budget-selection behavior at configurable char limits.
- Verification: `luac -p src/portal_prompt_linter.lua scripts/check_portal_prompt_token_order.lua scripts/regression_portal_prompt_token_order.lua`, `lua scripts/regression_portal_prompt_token_order.lua`, `lua scripts/check_portal_prompt_token_order.lua`.
- Follow-up: next unchecked item is adaptive portal hint prototype (`ALT ROUTE:<SAFE|RISK|SPIKE>`).

## 2026-03-21 04:34 KST — Threat-aware transition assist sync
- Transition prompt now surfaces `ALT DELTA:-n` derived with live threat-tier context.
- Combat readability impact hypothesis: players can better de-escalate after HIGH threat spikes by selecting safer branch with explicit pressure tradeoff.
- Follow-up: validate with run-level pacing telemetry once ALT selector v2 lands.

## 2026-03-21 05:04 KST — Cycle H follow-up: route-aware ALT selector v2
- Completed backlog item: choose adaptive `ALT ROUTE` from lowest-pressure reachable portal branch on current map (not fixed one-step downgrade).
- Verification: [PASS] portal route preview transition prompt regression validated, [PASS] portal prompt compact-mode regression validated, [PASS] portal prompt token-order regression validated, [PASS] portal adaptive ALT selector v2 regression validated (all PASS).
- Follow-up: keep `QA/UX Team: portal prompt readability regression for adaptive ALT token budget/order under HIGH threat compact mode` as next unchecked priority.

## 2026-03-21 05:33 KST — Portal adaptive ALT compact-readability regression
- Decision: Added dedicated regression `scripts/regression_portal_prompt_adaptive_alt_readability.lua` to validate HIGH-threat compact prompt budget + token order with adaptive ALT tokens (`ALT`, `ADEL`).
- Evidence: `lua scripts/regression_portal_prompt_adaptive_alt_readability.lua` PASS, plus companion prompt regressions PASS.
- Follow-up: Keep this regression in portal readability validation set for future prompt-token changes.

## 2026-03-21 05:38 KST — Game Director Cycle I: ALT PLAN nudge experiment
- Ideas generated: (1) adaptive portal ALT PLAN nudge token (low-risk UX), (2) overclock retreat streak bonus (mid-risk systems), (3) portal readability drift digest automation (high-risk ops novelty).
- Selected experiment: (1) adaptive portal ALT PLAN nudge token for HIGH-pressure transitions.
- Implementation: Added experiment-flagged prompt token in `src/portal.lua` (`ALT PLAN:LOWER RISK` detailed / `AP:LOW` compact) gated by `DOTPIO_EXPERIMENT_ALT_PLAN_NUDGE`.
- Verification: `lua scripts/regression_portal_prompt_adaptive_alt_readability.lua`, `DOTPIO_EXPERIMENT_ALT_PLAN_NUDGE=1 lua scripts/regression_portal_alt_plan_nudge.lua`, `lua scripts/regression_portal_prompt_compact_mode.lua`, `lua scripts/regression_portal_prompt_token_order.lua`.
- Follow-up: Monitor readability impact in playtests before promoting flag default.

## 2026-03-21 06:03 KST
- Task: Combat survivability experiment tied to overclock retreat behavior.
- Decision: Wired temporary dodge charge grant in `main.lua` when overclock module emits retreat streak bonus event.
- Evidence: Status copy `OVERCLOCK RETREAT STREAK: +1 DODGE (6s)` confirms live trigger path.
- Follow-up: Track whether dodge burst meaningfully changes death spikes in hazard-heavy maps.
## 2026-03-21 06:33 KST — Weekly portal prompt readability drift digest shipped
- Completed support for weekly digest artifact: `logs/weekly_portal_prompt_readability_drift.{md,json}` via `scripts/weekly_portal_prompt_readability_drift.py`.
- Added regression coverage: `scripts/regression_weekly_portal_prompt_readability_drift.py`.
- Weekly sustain runner now executes digest + regression and reports generated artifacts.
- Verification: `python3 -m py_compile ...`, digest regression PASS, `bash scripts/run_weekly_sustain.sh` PASS.
- Follow-up: use digest trend in upcoming Game Director readability tuning cycles.

## 2026-03-21 06:36 KST — Game Director Cycle J slice (mode-trend token)
- Idea slate generated (low/mid/high risk); selected low-risk readability slice.
- Added `MODE TREND` token to weekly portal prompt drift digest (`COMPACT|DETAILED|BALANCED`).
- Artifacts/regression remain green after update.
- Follow-ups kept in backlog: pressure-band drift token, top-token movers section.


## 2026-03-21 07:01 KST — Game Director Cycle J slice (pressure-band drift token)
- Task: Implement backlog item `PRESSURE BAND:LOW|MID|HIGH` for weekly portal prompt readability digest.
- Decision: Extended `scripts/weekly_portal_prompt_readability_drift.py` to aggregate pressure-token edits (`PRESSURE:` + `P:`) and map net drift to `pressureBand` thresholds (LOW <3, MID 3~7, HIGH >=8 by |net|).
- Evidence: Digest artifacts now include JSON `pressureBand` + `pressureEdits` and markdown line `PRESSURE BAND` with +/-/net counts.
- Verification: `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py`; `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`; `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 14 --max-commits 200`.
- Follow-up: Remaining Cycle J item is top-token movers section for digest triage.

## 2026-03-21 07:44 KST — Cycle J follow-up: digest top-token movers shipped
- Completed backlog item: `Design/QA Team: Add digest top-token movers section (largest net ± token deltas) for readability triage`.
- Added per-token edit aggregation (`added/removed/net`) and top-movers ranking in weekly digest outputs.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` and `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 14 --max-commits 200` PASS.
- Follow-up: no unchecked items remain in ACTION_ITEMS/TASKS/POST_RC; next cycle should inject new Game Director experiments.

## 2026-03-21 08:03 KST — Game Director Cycle K slice: weekly drift-risk token
- Completed backlog item: `QA/UX Team: Add digest drift-risk token (DRIFT RISK:LOW|MID|HIGH)`.
- Durable decisions:
  - Added `drift_risk_from_signals` classifier in `scripts/weekly_portal_prompt_readability_drift.py` using compact-vs-detailed net imbalance plus pressure-token churn.
  - Weekly digest JSON now exposes `driftRisk` + `driftRiskSignals` (`score`, `imbalance`, `pressureChurn`).
  - Weekly digest markdown now surfaces compact triage line: `DRIFT RISK: <level>`.
- Verification set (PASS):
  - `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 14 --max-commits 200`
- Follow-up:
  - Remaining Cycle K backlog items: `STICKY TOKENS` persistence token, `FOCUS` lane-focus token.

## 2026-03-21 08:31 KST — No combat tuning changes
- Task impact: None on combat systems.
- Decision: Combat telemetry unaffected; keep threat/overclock regressions unchanged.
- Follow-up: Monitor if lane-focus token recommends pressure-heavy prompt edits.

## 2026-03-21 09:03 KST — Cycle L route-action token vertical slice
- Ideas generated:
  1) Low-risk UX: add digest route-action token (`ROUTE ACTION:*`) from `FOCUS + DRIFT RISK`.
  2) Mid-risk systems: add lane-focus streak metric across windows (`FOCUS STREAK:<n>`).
  3) High-risk novelty: add lane-focus transition handoff token (`FOCUS SHIFT:<FROM->TO>`).
- Chosen experiment: idea #1 (minimal reversible vertical slice).
- Shipped: weekly digest now emits `routeAction` + `routeActionReason` in JSON and `ROUTE ACTION` line in markdown.
- Verification: py_compile PASS, digest regression PASS, live digest regeneration PASS.
- Follow-up: backlog carries remaining Cycle L items (focus streak, focus shift).
## 2026-03-21 09:35 KST — Cycle L close + Cycle M vertical slice
- Completed: Weekly portal prompt digest now includes `FOCUS STREAK:<n>` and `FOCUS SHIFT:<FROM->TO>` signals, then Game Director Cycle M experiment `FOCUS VOL:STEADY|SWING`.
- Decision: Define volatility from non-mixed lane-focus commit sequence switch ratio (`switches/edges`), with `SWING` threshold `>= 0.4`.
- Evidence: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` and `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120`.
- Follow-up: Cycle M backlog keeps `ACTION CONF` + `ANOMALY` items open.
