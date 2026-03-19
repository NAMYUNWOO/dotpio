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
