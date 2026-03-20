# Team Logs Summary

Last updated: 2026-03-21 00:02 KST

## Purpose
Compact decision memory for AI context efficiency.

## Loading policy
- Default load:
  1) `_summary.md`
  2) only recent tail from each team log (last 20~50 lines)
- Expanded load: pull older ranges only when a task explicitly needs history.

## Current key decisions
- Core fun: AI-generated disassemble/build loop with DOS-style inventory UX.
- Build economy: SRL is enforced as sink; repeated low-tier loops are penalized.
- Build requirement scales with folder/component quality and loop-risk signals.
- Disassemble is constrained by size-tier costs and salvage caps.
- map_04 and portal validation flow are integrated with validator checks.
- Dropped world items can now be picked up via `G` on player tile; pickup enforces inventory capacity and consumes map entity on success.
- Pickup affordance is now surfaced in both realtime HUD controls and inventory help dialog (`G:Pickup`).
- Drop->pickup regression is now scripted in `scripts/regression_drop_pickup.lua` to validate item count restoration + world item cleanup.
- Starter build-test loadout is now folder-seeded (`SCROLLS`/`POTIONS`/`WEAPONS`) with `BUILDER.SRL` baseline 18 and mixed-tier materials for stable smoke loops.
- Starter loadout sanity is scripted in `scripts/regression_starter_loadout.lua` (Player.init baseline check).
- Economy telemetry baseline now logs build/disassemble lock/fail/success events into `logs/economy_telemetry.ndjson` with input/output metadata and SRL envelope fields.
- Telemetry schema regression is scripted in `scripts/regression_economy_telemetry.lua`.
- Inventory stacks now support split interaction (`S`) via action menu/quick key with quantity dialog and guardrails.
- Stack split regression is scripted in `scripts/regression_split_stack.lua`.
- F9 build flow now requires preview/confirm before execution, showing planned component usage + SRL have/need to keep build consumption explicit.
- Build preview confirmation gate is covered by `scripts/regression_build_preview_confirm.lua`.
- BUILDER.SRL affordance copy is now explicit across action menu, lock/status messages, and F9 preview/help text (no generic SRL-only wording).
- BUILDER.SRL copy consistency is regression-covered in `scripts/regression_builder_srl_affordance.lua`.
- Anti-exploit monitoring now has a sliding-window analyzer (`src/economy_anti_exploit.lua`) and report generator (`scripts/economy_anti_exploit_report.lua`) that flags net-positive/flat-profit loops over N actions.
- Build SRL cost curve now applies stronger low-tier + salvage-ratio surcharges so cheap churn recipes stay expensive relative to premium recipes.
- SRL curve guardrail is covered by `scripts/regression_srl_cost_curve.lua` (expects low-tier spam fixture >=6 BUILDER.SRL and not cheaper than premium fixture).
- Disassembly salvage caps are now size-tiered for fairness (stack cap 1/2/3 and budget scale 35%/45%/55% with source-size clamp), regression-covered in `scripts/regression_disassembly_caps.lua`.
- map_01~04 progression validation is now scripted via `scripts/regression_map_progression.py`, which captures reachability/return-path checks + `validate_portals.py` output into `logs/playtests/map_01_04_progression_checklist.md`.
- M1 30-minute momentum gate now has a single scripted orchestrator `scripts/regression_30min_loop_checklist.py` that executes core-loop regressions and emits `logs/playtests/loop_30min_checklist.md` with PASS/FAIL summary.
- M2 map expansion started with new `maps/map_05.lua`; map_04 now exposes portal `05` (47,24) and map_05 provides reciprocal return portal `04` (1,13), validated by portal validator.
- M2 expansion now includes `maps/map_06.lua`; map_05 exposes portal `06` (47,24) and map_06 provides reciprocal return portal `05` (1,13), validated by portal validator.
- Enemy roster now includes behavior variants (`skirmisher`, `bruiser`, `sentinel`) with profile-driven move/aggro/flee/attack modifiers and weighted spawn mix for encounter diversity.
- Build synthesis now enforces rolling category diversity (window 6 / cap 3) and shifts saturated AI targets toward underused synergy categories.
- Diversity constraint behavior is regression-covered in `scripts/regression_build_category_diversity.lua`.
- Lootbox rewards are now map-tiered (01~02 consumable-heavy, 03~04 mixed gear, 05~06 gear/accessory weighted) via weighted category profiles in `src/entities.lua`.
- Tiered loot distribution is regression-covered in `scripts/regression_lootbox_rewards_by_tier.lua`.
- M3 run mission prototype now tracks three objective lanes (`kills`, `pickup`, `build`) in runtime state and surfaces checklist progress in HUD.
- Mission objective flow is regression-covered in `scripts/regression_run_missions.lua`.
- New unlock flag framework (`src/unlocks.lua`) now gates advanced build targets (`ring`, `wand`, `gem`) behind mission completion (`advanced_build_categories`) and surfaces unlock state in HUD/status copy.
- Unlock gating/regression is covered in `scripts/regression_unlock_flags.lua`.
- Fail-forward progression now computes capped carryover rewards from failed run state (BUILDER.SRL/coin/gem), reapplies them on next run reset, and is regression-covered in `scripts/regression_fail_forward_rewards.lua`.
- Run reset now opens a summary overlay with pre-reset mission snapshot, advanced schematic unlock status, and applied carryover details; regression-covered in `scripts/regression_run_summary.lua`.
- Progress/report protocol: commit + verification + next task on each run.
- DOS inventory terminology is now normalized around canonical labels (`Action Menu`, `Disasm`, `Drop`, `Build`), and build result status explicitly lists consumed materials (`USED: ...`).
- Disabled Action Menu entries now show inline lock reasons (`[LOCK: ...]`) for USE/EQUIP/DISASM/SPLIT constraints, with regression coverage in `scripts/regression_action_menu_lock_reasons.lua`.
- Added compact first-5-minute onboarding hint strip on HUD, progressing by early interactions (move/search/pickup/inventory/build) and expiring at 300s; covered by `scripts/regression_onboarding_hints.lua`.
- Keyboard-only usability pass now has scripted coverage (`scripts/regression_keyboard_shortcuts.lua`) plus generated checklist artifact (`logs/playtests/keyboard_only_usability_checklist.md`) via `scripts/regression_keyboard_usability_checklist.py`.
- M5 RC checklist artifact is now defined at `logs/playtests/rc_checklist.md`, mapping each release gate area to executable regression commands, evidence paths, blocker triage, and cross-team sign-off rows.
- M5 full regression matrix has been executed end-to-end (combat/inventory/build/disasm/portal); all scripted checks passed, screenshots regenerated, and blocker triage currently reports 0 critical/high blockers.
- M5 blocker-closure audit rerun (30-min loop + anti-exploit + portal integrity) also passed, confirming 0 critical/high blockers remain before launch packaging.
- Launch packaging now includes refreshed screenshot artifacts (`screenshots/screenshot-map04.png`, `screenshots/screenshot-inventory-dos.png`) and a root `CHANGELOG.md` (`0.5.0-rc.1`) for RC notes.
- Release candidate tag `0.5.0-rc.1` is now published on `feature/ai-disassemble-builder`, closing the final M5 unchecked item.
- Post-RC sustain now includes `scripts/economy_weekly_snapshot.py`, generating `logs/economy_weekly_snapshot.{md,json}` with a weekly SRL rebalance decision (`NO_CURVE_CHANGE`/`REBALANCE_REQUIRED`) gated by anti-exploit suspicious-window count.
- Weekly SRL snapshots now include delta signals vs previous snapshot (telemetry event count + total SRL spend), and schema stability is guarded by `scripts/regression_weekly_snapshot.py` (baseline null deltas + compare-mode zero/nonzero deltas).
- RC checklist command matrix now includes a dedicated Post-RC sustain guardrail row for `python3 scripts/regression_weekly_snapshot.py` so weekly telemetry reporting always verifies delta-schema compatibility.
- Weekly sustain operations now have a one-command runner (`bash scripts/run_weekly_sustain.sh`) that refreshes anti-exploit reports, regenerates weekly snapshot artifacts, and executes delta-schema regression in sequence.
- Scheduler handoff now includes `scripts/install_weekly_sustain_cron.sh` (dry-run/apply), with managed marker `DOTPIO_WEEKLY_SUSTAIN` and default weekly cadence Monday 09:00 KST.
- Weekly scheduler installer behavior is now regression-covered by `scripts/regression_weekly_cron_installer.py` (dry-run evidence, CLI override reflection, invalid arg rejection).
- Weekly cron installer now supports `CRONTAB_BIN` override so mocked apply-mode upsert behavior can be regression-tested safely without mutating host crontab; regression now asserts single-marker upsert semantics under `--apply`.
- RC checklist sign-off rows are now synchronized with actual release state: all lane sign-offs checked, release tag recorded as `0.5.0-rc.1` (`d82cab1`), and sign-off note includes auditable timestamp/hash.
- Weekly cron installer now supports configurable log sinks via `--log-path` / `SUSTAIN_CRON_LOG_PATH` (default still `logs/weekly_sustain_cron.log`), with regression coverage ensuring custom path rendering stays stable.
- Weekly sustain scheduler now includes size-based pre-run log rotation via `scripts/rotate_log_if_needed.sh`; installer exposes `--max-log-size-mb` / `SUSTAIN_CRON_MAX_LOG_SIZE_MB` and regression coverage checks rotate-command rendering + validation.
- Weekly sustain log rotation now enforces keep-latest-N retention pruning via `scripts/rotate_log_if_needed.sh <log> <max-size-mb> <retain-rotated>` to avoid rotated-log accumulation.
- Cron installer now exposes `--retain-rotated-logs` / `SUSTAIN_CRON_RETAIN_ROTATED_LOGS`, wiring retention policy directly into managed cron entries.
- Retention behavior is regression-covered by `scripts/regression_rotate_log_retention.py` (repeated over-threshold rotations + prune assertions).
- Weekly sustain log rotation now also supports optional age-based pruning (`max-age-days`) via rotate helper + cron installer (`--max-rotated-age-days` / `SUSTAIN_CRON_MAX_ROTATED_AGE_DAYS`), with regression coverage for stale-file deletion and CLI token rendering.
- Added `scripts/audit_weekly_sustain_cron.sh` to introspect the managed `DOTPIO_WEEKLY_SUSTAIN` cron entry and print parsed schedule + rotation policy fields; regression-covered by `scripts/regression_weekly_cron_audit.py` including missing-entry diagnostics.
- Weekly sustain cron audit helper now supports machine-readable output via `--format json` (default remains text), and regression coverage now validates JSON payload fields plus invalid-format rejection.
- Folder rows now use Enter -> Action Menu (`OPEN`/`BUILD`) as the primary build flow, with `B` quick action opening the same build preview/confirm gate; F9 remains as shortcut.
- `BUILDER.SRL` can no longer be directly consumed via `USE`; item Action Menu now shows a locked `USE` row with explicit build-only guidance (`B` or `Enter->BUILD`), and quick-use attempts emit matching status text.
- Regression coverage in `scripts/regression_action_menu_lock_reasons.lua` now asserts `BUILDER.SRL`-specific `USE` lock + guidance copy.
- Build preview dialog now includes an explicit `Expected category` line (derived from constrained component-category mix via `AiDescribe.debugConstrainBuildCategory`) so players can see projected output class before confirming material/SRL spend.
- Added `scripts/regression_build_preview_clarity.lua` to enforce preview-plan expected-category metadata presence while existing preview confirm/action-menu regressions stay green.
- Added `map_07` as a post-RC P1 world expansion with additional mid-lane collision barricades to create a tighter tactical choke pattern compared to map_06.
- Portal graph now includes a bidirectional `map_06` <-> `map_07` pair (`map_06` portal `07` at 47,13 to `map_07` portal `06`, reciprocal return path on `map_07`).
- Enemy roster now includes two P1 synergy archetypes: `warcaller` (nearby ally alert propagation on player sight) and `hunter` (proximity buff when a living warcaller is nearby), with regression coverage extended for synergy activation and ally-alert behavior.
- Run missions now support rotating 3-objective packs instead of a fixed prototype list, preserving HUD readability while varying run goals across resets.
- Mission variety pack now includes +5 new objective variants (`kills_5`, `pickup_4`, `build_2`, `search_2`, `inventory_3`) with shared event-key progress tracking.
- Gameplay hooks now increment mission progress on crate search completion and inventory-open actions, enabling the new mission variants without extra controls.
- Mission variety behavior is regression-covered by `scripts/regression_mission_variety_pack.lua` (catalog floor, pack rotation, and new objective inclusion assertions).

## 2026-03-19 — Mission Momentum Bonus Experiment Shipped
- Completed backlog item: objective streak micro-reward for missions.
- Durable decision: mission objective completions now grant capped momentum payout in BUILDER.SRL using streak curve **1, 1, 2** (cap at streak 3+).
- Implementation notes:
  - `RunMissions.addProgress` now returns structured completion payload (`completedObjectiveIds`, `completionStreak`, `rewardSrl`).
  - Main loop consumes completion payload and applies `builder_scroll` payout immediately with DOS status messaging.
  - Inventory-full path is explicit (`... DROPPED (BAG FULL)`) to avoid silent reward loss.
- Verification:
  - `lua scripts/regression_run_missions.lua`
  - `lua scripts/regression_mission_momentum.lua`
  - `lua scripts/regression_mission_variety_pack.lua`
  - `luac -p main.lua src/run_missions.lua`
- Next recommended item (POST_RC_BACKLOG): `Add weekly sustain audit JSON pretty mode`.

## 2026-03-20 00:26 KST — Post-RC P1 map identity pass completed
- map_03~07 now carry explicit tactical identity metadata (`silhouette`, `laneStructure`, `encounterRhythm`) to prevent map feel drift.
- Runtime now reads `Map.metadata` and applies per-map encounter pacing through enemy count multipliers + behavior bias.
- Added regression guardrail: `scripts/regression_map_profile_distinctness.lua` ensures map_03~07 identity tags stay unique and encounter profile fields remain valid.
- Validation set: profile distinctness PASS, portal integrity PASS, map_01~04 progression PASS, enemy behavior regression PASS.
- Backlog state: `POST_RC_BACKLOG.md` P1 item “Redesign map_03~07 …” marked complete.
- Next priority: P1 portal repositioning with return-path + landmark rules.

## 2026-03-20 00:58 KST — P1 portal progression rules completed
- Completed backlog item: `World Team: Reposition portals with logical progression rules (clear return paths, risk/reward routing, landmark-based placement)`.
- Durable decisions:
  - map_03 portals were redistributed to three distinct landmarks (west-upper return, north apex progression, east-south fallback).
  - map_04 now serves as a hinge hub with explicit fallback (`map_01`) and forward push (`map_05`) at separated landmarks.
  - map_05~07 chain portals moved away from corner clustering to improve landmark legibility while preserving bidirectional progression.
- Verification set:
  - `luac -p maps/map_03.lua maps/map_04.lua maps/map_05.lua maps/map_06.lua maps/map_07.lua`
  - `python3 scripts/validate_portals.py`
  - `python3 scripts/regression_map_progression.py`
- Backlog update: `POST_RC_BACKLOG.md` P1 portal repositioning item marked done.
- Next priority item: P2 `Add weekly sustain audit JSON pretty mode`.

## 2026-03-20 01:28 KST — P2 weekly audit JSON pretty mode completed
- Completed backlog item: `Add weekly sustain audit JSON pretty mode`.
- Durable decision: `scripts/audit_weekly_sustain_cron.sh --format json --pretty` now emits indented JSON for operator readability while plain `--format json` remains compact/stable for machine consumers.
- Guardrail: `--pretty` is now explicitly rejected unless `--format json` is selected.
- Verification set:
  - `python3 -m py_compile scripts/regression_weekly_cron_audit.py`
  - `python3 scripts/regression_weekly_cron_audit.py`
- Backlog update: `POST_RC_BACKLOG.md` P2 pretty-mode item marked done.
- Next priority item: P2 `Add sustain health dashboard markdown report`.

## 2026-03-20 01:59 KST — P2 sustain health dashboard report completed
- Completed backlog item: `Add sustain health dashboard markdown report`.
- Durable decisions:
  - Added `scripts/sustain_health_dashboard.py` to generate `logs/sustain_health_dashboard.md` with a 3-signal health rollup (economy safety, telemetry freshness, scheduler audit).
  - `scripts/run_weekly_sustain.sh` now attempts cron audit capture (`logs/weekly_sustain_cron_audit.json`) and gracefully degrades to warning state when no managed cron entry exists.
  - Added regression guardrail `scripts/regression_sustain_health_dashboard.py` and linked dashboard commands into RC sustain checklist.
- Verification set:
  - `python3 -m py_compile scripts/sustain_health_dashboard.py scripts/regression_sustain_health_dashboard.py`
  - `python3 scripts/regression_sustain_health_dashboard.py`
  - `bash scripts/run_weekly_sustain.sh`
- Backlog update: `POST_RC_BACKLOG.md` P2 dashboard item marked done.
- Next priority item: P2 `Add automatic stale-branch/report drift check`.

## 2026-03-20 02:26 KST — P2 stale-branch/report drift check completed
- Completed backlog item: `Add automatic stale-branch/report drift check`.
- Durable decisions:
  - Added `scripts/stale_branch_report_drift_check.py` to emit `logs/stale_branch_report_drift.{md,json}` with combined branch freshness (upstream behind/ahead + commit age) and sustain-report freshness checks.
  - Drift checker prefers embedded JSON `generatedAt` and gracefully falls back to file mtime for markdown artifacts.
  - Weekly sustain runner now includes drift check + regression (`scripts/regression_stale_branch_report_drift.py`) in the one-command pipeline.
- Verification set:
  - `python3 -m py_compile scripts/stale_branch_report_drift_check.py scripts/regression_stale_branch_report_drift.py`
  - `python3 scripts/regression_stale_branch_report_drift.py`
  - `python3 scripts/stale_branch_report_drift_check.py`
- Backlog update: `POST_RC_BACKLOG.md` item marked done.
- Next priority item: none remaining in `POST_RC_BACKLOG.md` (all checked).

## 2026-03-20 03:00 KST — P2 sustain dashboard JSON mode completed
- Completed backlog item: `Add sustain health dashboard JSON output mode (compact + pretty) and wire weekly runner artifact output`.
- Durable decisions:
  - `scripts/sustain_health_dashboard.py` now supports `--format md|json` (default `md`) and optional `--pretty` for indented JSON output.
  - JSON payload schema is standardized around `overall`, `signals`, `weeklySnapshot`, and `schedulerPolicy` to support automation consumers.
  - `--pretty` is explicitly rejected unless `--format json` is selected to keep CLI behavior unambiguous.
  - Weekly sustain runner now publishes both dashboard artifacts: `logs/sustain_health_dashboard.md` and `logs/sustain_health_dashboard.json`.
- Verification set:
  - `python3 -m py_compile scripts/sustain_health_dashboard.py scripts/regression_sustain_health_dashboard.py`
  - `python3 scripts/regression_sustain_health_dashboard.py`
  - `bash scripts/run_weekly_sustain.sh`
- Backlog update: `POST_RC_BACKLOG.md` new P2 item marked done.
- Next priority item: none remaining in `POST_RC_BACKLOG.md` (all checked).

## 2026-03-20 03:29 KST — P2 sustain dashboard trend classification
- Completed task: Add sustain dashboard trend classification (`improving|stable|degrading`) with regression coverage.
- Durable decisions:
  - Added `overall.trend` to dashboard JSON; markdown now surfaces `Trend: **...**` directly under overall tier.
  - Trend is computed from weekly delta signals (events/SRL) and economy safety override (suspicious windows or curve-change decisions force `degrading`).
  - Health-tier scoring remains unchanged (trend is additive, non-breaking for existing consumers).
- Verification set:
  - `python3 -m py_compile scripts/sustain_health_dashboard.py scripts/regression_sustain_health_dashboard.py`
  - `python3 scripts/regression_sustain_health_dashboard.py`
  - `bash scripts/run_weekly_sustain.sh`
- Backlog update: `POST_RC_BACKLOG.md` P2 trend-classification item marked done.
- Next priority item: none remaining in `POST_RC_BACKLOG.md` (all checked).
- Mission HUD now surfaces compact pacing metadata (`PACK:<id>`, `STREAK:<n>`) directly under `RUN MISSIONS` for in-run readability.
- Run summary snapshots now persist mission metadata (`missionPackId`, `momentumStreak`) alongside objective/carryover details.
- Regression coverage extended in `scripts/regression_run_summary.lua` to lock mission metadata snapshot integrity.

## 2026-03-20 03:58 KST — P1 mission pacing readability metadata
- Completed backlog item: `Surface active mission-pack id + momentum streak in HUD/run-summary for clearer run pacing readability`.
- Durable decisions:
  - Added compact mission panel metadata row (`PACK`, `STREAK`) without changing mission/combat/economy logic.
  - Run summary now records pack id + streak so post-run reviews retain pacing context.
- Verification set:
  - `luac -p src/hud.lua src/run_summary.lua scripts/regression_run_summary.lua scripts/regression_run_missions.lua`
  - `lua scripts/regression_run_missions.lua`
  - `lua scripts/regression_run_summary.lua`
  - `lua scripts/regression_mission_momentum.lua`
  - `lua scripts/regression_mission_variety_pack.lua`
- Backlog update: `POST_RC_BACKLOG.md` P1 gameplay follow-up item marked done.
- Next priority item: none currently unchecked in `POST_RC_BACKLOG.md`.
- Mission momentum rewards now include a lane-switch variety bonus (+1 BUILDER.SRL) when consecutive objective completions come from different lanes, while preserving the base streak curve (1/1/2).
- Mission status messaging now annotates variety payouts with `[VARIETY +1]` (including bag-full drop path) for readable reward causality.

## 2026-03-20 04:29 KST — P1 mission momentum lane-switch variety bonus
- Completed backlog item: `Add mission momentum lane-switch variety bonus (+1 BUILDER.SRL on consecutive objective completions from different lanes)`.
- Durable decisions:
  - Added `lastCompletedLane` tracking in run mission state to detect lane alternation between objective completions.
  - Reward payload now exposes `baseRewardSrl`, `laneSwitchBonusSrl`, and total `rewardSrl` so downstream UX can explain payout composition.
  - Applied compact UX annotation `[VARIETY +1]` in mission reward status text without changing inventory/economy fundamentals.
- Verification set:
  - `luac -p main.lua src/run_missions.lua scripts/regression_mission_momentum.lua`
  - `lua scripts/regression_run_missions.lua`
  - `lua scripts/regression_mission_momentum.lua`
  - `lua scripts/regression_mission_variety_pack.lua`
- Backlog update: `POST_RC_BACKLOG.md` item marked done.
- Next priority item: none unchecked in tracked backlogs; next cycle should inject a fresh Game Director experiment candidate.
- Mission pack rotation now includes deterministic flavor metadata (`lastPackTag`, `lastPackLabel`) in mission state for pacing readability without altering objective logic.
- HUD mission panel now surfaces `PACK/TAG/STREAK`, and run summary snapshot now persists and displays `missionPackTag` + `missionPackLabel` (`PACE`) for post-run context.
- Regression coverage extended so mission variety/summary tests assert flavor metadata presence and snapshot integrity.

## 2026-03-20 04:59 KST — P1 gameplay follow-up: mission pack flavor descriptors
- Completed backlog item: `Add mission-pack flavor descriptors and surface compact tag in HUD/run-summary`.
- Durable decisions:
  - Default mission packs now define explicit flavor descriptors (`BASELINE/HUNT/FORGE/PIVOT`) plus short pacing labels.
  - Summary snapshot contract expanded with `missionPackTag` and `missionPackLabel` for durable run review context.
- Verification set:
  - `luac -p src/run_missions.lua src/run_summary.lua src/hud.lua scripts/regression_run_summary.lua scripts/regression_mission_variety_pack.lua`
  - `lua scripts/regression_run_summary.lua`
  - `lua scripts/regression_run_missions.lua`
  - `lua scripts/regression_mission_momentum.lua`
  - `lua scripts/regression_mission_variety_pack.lua`
- Backlog update: `POST_RC_BACKLOG.md` item marked done.
- Next priority item: none currently unchecked in tracked backlogs; inject next Game Director experiment in next cycle.

## 2026-03-20 05:29 KST — P1 combat experiment: berserker desperation behavior
- Completed backlog item: `Combat Team: Add berserker desperation behavior (low-HP speed/damage spike) with regression coverage`.
- Durable decisions:
  - Added new enemy archetype `berserker` to spawn roster and behavior catalog.
  - Enemy modifier sync now composes synergy and low-HP desperation in one deterministic pass (move cadence, attack cadence, attack damage).
  - Berserker desperation trigger is profile-driven (`hp <= 2`) to keep tuning/rollback low-risk.
- Verification set:
  - `luac -p src/enemy_ai.lua src/entities.lua scripts/regression_enemy_behavior_variants.lua`
  - `lua scripts/regression_enemy_behavior_variants.lua`
- Backlog update: `POST_RC_BACKLOG.md` combat experiment item marked done.
- Next priority item: none unchecked in `ACTION_ITEMS.md` / `TASKS.md` / `POST_RC_BACKLOG.md`; inject next Game Director experiment candidate next cycle.

## 2026-03-20 05:44 KST — P1 combat readability experiment: berserker telegraph
- Completed experiment slice: `UX/Combat Team: Telegraph berserker desperation state in HUD + combat status feed`.
- Durable decisions:
  - Enemy AI now exposes one-shot transition signal `justEnteredDesperation` when berserker low-HP mode first activates.
  - Runtime emits explicit warning status text only when enraging enemy is visible, then clears signal to prevent spam.
  - HUD now surfaces active desperate berserker count (`Berserk: n`) for persistent threat readability.
- Verification set:
  - `luac -p src/enemy_ai.lua main.lua src/hud.lua scripts/regression_enemy_behavior_variants.lua`
  - `lua scripts/regression_enemy_behavior_variants.lua`
- Backlog update:
  - Marked telegraph experiment done in `POST_RC_BACKLOG.md` and `TASKS.md`.
  - Added next candidate: berserker pre-lunge tell (one-turn warning) as unchecked follow-up.

## 2026-03-20 06:02 KST — P1 combat readability/fairness experiment: berserker pre-lunge tell
- Completed backlog item: `Combat Team: Add one-turn pre-lunge tell for berserker desperation attacks (readability/fairness A/B)`.
- Durable decisions:
  - Berserker desperation attacks now run a deterministic two-step cadence: telegraph turn first, then lunge hit turn.
  - Enemy AI tracks `desperationLungePrimed`; runtime surfaces telegraph via status feed and HUD (`Lunge Tell: n`).
  - Combat event plumbing in `Entities.update` now reports lunge telegraph counts without changing non-berserker behavior paths.
- Verification set:
  - `lua scripts/regression_enemy_behavior_variants.lua`
  - `luac -p src/enemy_ai.lua src/entities.lua src/hud.lua main.lua`
- Backlog update:
  - Marked pre-lunge tell task done in `TASKS.md` and `POST_RC_BACKLOG.md`.
- Next priority item:
  - No unchecked items remain in `ACTION_ITEMS.md` / `TASKS.md` / `POST_RC_BACKLOG.md`; request next Game Director experiment injection.

## 2026-03-20 06:30 KST — P1 combat fairness follow-up: berserker post-lunge recovery
- Completed backlog item: `Combat Team: Add one-turn post-lunge recovery window for berserker desperation chain (readability/fairness follow-up)`.
- Durable decisions:
  - Berserker desperation cadence is now deterministic three-step: **telegraph -> lunge hit -> one-turn recovery**.
  - Enemy AI now tracks `desperationRecoveryPending`; recovery consumes one attack turn and then clears.
  - Runtime status feed now emits explicit recovery feedback (`BERSERKER RECOVERING: BRIEF BREATHER`) via new combat event `berserker_lunge_recovery`.
- Verification set:
  - `luac -p src/enemy_ai.lua src/entities.lua main.lua scripts/regression_enemy_behavior_variants.lua`
  - `lua scripts/regression_enemy_behavior_variants.lua`
- Backlog update:
  - Marked new P1 combat follow-up item done in `POST_RC_BACKLOG.md` and mirrored in `TASKS.md`.
- Next priority item:
  - No unchecked items remain in `ACTION_ITEMS.md` / `TASKS.md` / `POST_RC_BACKLOG.md`; inject next Game Director experiment candidate next cycle.

## 2026-03-20 06:58 KST — P1 combat readability follow-up: berserker recovery HUD counter
- Completed backlog item: `UX/Combat Team: Surface active berserker recovery-window count in HUD threat strip`.
- Durable decisions:
  - Refactored HUD combat-threat counting into `HUD.collectCombatThreatCounters(enemies)` to keep threat-strip semantics testable.
  - Added `Recovering: n` HUD row (amber) for berserkers with `desperationRecoveryPending`, shown only while desperation is active.
  - Threat hierarchy remains urgency-ordered: `Berserk` -> `Lunge Tell` -> `Recovering`.
- Verification set:
  - `luac -p src/hud.lua scripts/regression_hud_berserker_counters.lua scripts/regression_enemy_behavior_variants.lua`
  - `lua scripts/regression_hud_berserker_counters.lua`
  - `lua scripts/regression_enemy_behavior_variants.lua`
- Backlog update:
  - Marked new HUD recovery-counter item done in `POST_RC_BACKLOG.md` and `TASKS.md`.
- Next priority item:
  - No unchecked items remain in `ACTION_ITEMS.md` / `TASKS.md` / `POST_RC_BACKLOG.md`; next cycle should inject a fresh Game Director experiment candidate.

## 2026-03-20 07:26 KST — P1 gameplay experiment: mission variety bonus preview hint
- Completed backlog item: `UX/Systems Team: Add mission lane-switch preview hint in HUD so players can anticipate variety bonus (+1 BUILDER.SRL)`.
- Durable decisions:
  - `RunMissions.getState()` now exposes `nextVarietyLane` + `varietyBonusPreview` derived from unfinished alternate-lane objectives after the latest completion.
  - HUD mission metadata row now conditionally appends `NEXT:<lane> +1` when variety bonus is currently achievable.
  - Variety payout mechanics remain unchanged (preview-only readability pass).
- Verification set:
  - `luac -p src/run_missions.lua src/hud.lua scripts/regression_mission_variety_preview.lua`
  - `lua scripts/regression_mission_variety_preview.lua`
  - `lua scripts/regression_mission_momentum.lua`
  - `lua scripts/regression_mission_variety_pack.lua`
- Backlog update:
  - Marked new P1 gameplay experiment item done in `POST_RC_BACKLOG.md` and mirrored in `TASKS.md`.
- Next priority item:
  - No unchecked items remain in `ACTION_ITEMS.md` / `TASKS.md` / `POST_RC_BACKLOG.md`; inject next Game Director experiment candidate.

## 2026-03-20 07:56 KST — P1 gameplay readability follow-up: mission variety mastery counter
- Completed backlog item: `UX/Systems Team: Track and surface mission lane-switch variety bonus count in HUD/run-summary`.
- Durable decisions:
  - Added mission-state stat `varietyBonusCount` (increments only on lane-switch bonus payouts, resets on mission reset).
  - HUD mission metadata now includes compact `VAR:<n>` token next to `PACK/TAG/STREAK`.
  - Run summary snapshot now persists/displays `varietyBonusCount` for post-run pacing review.
- Verification set:
  - `luac -p src/run_missions.lua src/run_summary.lua src/hud.lua scripts/regression_mission_momentum.lua scripts/regression_run_summary.lua`
  - `lua scripts/regression_mission_momentum.lua`
  - `lua scripts/regression_run_summary.lua`
  - `lua scripts/regression_mission_variety_preview.lua`
  - `lua scripts/regression_mission_variety_pack.lua`
- Backlog update:
  - Marked new P1 gameplay experiment item done in `POST_RC_BACKLOG.md` and mirrored in `TASKS.md`.
- Next priority item:
  - No unchecked entries remain in `ACTION_ITEMS.md` / `TASKS.md` / `POST_RC_BACKLOG.md`; inject a fresh Game Director experiment candidate next cycle.

## 2026-03-20 08:28 KST — P1 combat readability follow-up: weighted berserker threat index
- Completed backlog item: `UX/Combat Team: Add weighted berserker threat index in HUD threat strip (THREAT:<n>)`.
- Durable decisions:
  - `HUD.collectCombatThreatCounters()` now computes `berserkerThreatScore` using weighted pressure formula: desperate +2(lunge primed) +1(recovery pending).
  - HUD threat strip now renders `Threat:<n>` below berserker count for faster danger scanning.
  - Top-left HUD panel height/help-row spacing adjusted to prevent text overlap while preserving existing counters.
- Verification set:
  - `luac -p src/hud.lua scripts/regression_hud_berserker_counters.lua`
  - `lua scripts/regression_hud_berserker_counters.lua`
- Backlog update:
  - Marked item done in `POST_RC_BACKLOG.md` and `TASKS.md`.
- Next priority item:
  - No unchecked entries remain in `ACTION_ITEMS.md` / `TASKS.md` / `POST_RC_BACKLOG.md`; inject a fresh Game Director experiment candidate.

## 2026-03-20 08:56 KST — P1 combat readability follow-up: threat tier label
- Completed backlog item: `UX/Combat Team: Add berserker threat-tier label (LOW|MED|HIGH) in HUD for score readability`.
- Durable decisions:
  - Added `HUD.getBerserkerThreatTier(score)` with deterministic thresholds: `LOW(0-2)`, `MED(3-5)`, `HIGH(>=6)`.
  - HUD threat-strip line now renders `Threat: <score> (<tier>)` to pair quantitative and qualitative danger cues.
  - Preserved existing compact combat rows (`Berserk`, `Lunge Tell`, `Recovering`) to avoid panel growth.
- Verification set:
  - `luac -p src/hud.lua scripts/regression_hud_berserker_counters.lua`
  - `lua scripts/regression_hud_berserker_counters.lua`
- Backlog update:
  - Marked new P1 item done in `POST_RC_BACKLOG.md` and mirrored in `TASKS.md`.
- Next priority item:
  - No unchecked entries remain in `ACTION_ITEMS.md` / `TASKS.md` / `POST_RC_BACKLOG.md`; inject a fresh Game Director experiment candidate next cycle.

## 2026-03-20 09:28 KST — P1 combat readability follow-up: threat-tier color coding
- Completed backlog item: `UX/Combat Team: Color-code berserker threat-tier label in HUD (LOW=green, MED=amber, HIGH=red)`.
- Durable decisions:
  - Added `HUD.getBerserkerThreatColor(score)` to centralize tier-to-color mapping.
  - Threat row rendering now reuses existing `Threat: <score> (<tier>)` text while applying tier-specific color to reduce scan latency.
  - Kept explicit tier token in text to avoid color-only communication risk.
- Verification set:
  - `luac -p src/hud.lua scripts/regression_hud_berserker_counters.lua`
  - `lua scripts/regression_hud_berserker_counters.lua`
- Backlog update:
  - Marked item done in `POST_RC_BACKLOG.md` and mirrored in `TASKS.md`.
- Next priority item:
  - No unchecked entries remain in `ACTION_ITEMS.md` / `TASKS.md` / `POST_RC_BACKLOG.md`; inject next Game Director experiment candidate.

## 2026-03-20 10:06 KST — Post-RC Combat Readability: Threat formula legend
- Completed item:
  - `UX/Combat Team: Add compact berserker threat formula legend in HUD/combat status (THREAT = BERSERK + 2*LUNGE + RECOVER)`
- Product decisions:
  - Added reusable helpers in `src/hud.lua` for threat legend and weighted breakdown formatting.
  - HUD now shows live decomposition line when berserkers are active: `THREAT = <berserk> + 2*<lunge> + <recover> = <score>`.
  - Enrage combat status copy now includes compact teaching token: `[THREAT=B+2L+R]`.
- Verification set:
  - `luac -p main.lua src/hud.lua`
  - `lua scripts/regression_hud_berserker_counters.lua`
- Backlog sync:
  - Marked done in `POST_RC_BACKLOG.md`.
  - Added mirrored completed entry in `TASKS.md`.
- Next priority:
  - No unchecked entries remain in ACTION_ITEMS/TASKS/POST_RC; queue next Game Director experiment candidate (e.g., threat-aware onboarding micro-tip decay logic).

## 2026-03-20 10:35 KST — Berserker threat delta HUD slice
- Completed: Added turn-over-turn berserker threat delta indicator (`THREAT Δ:+n|-n`) in HUD combat strip.
- Durable decisions:
  - Keep delta math centralized in HUD helpers (`getBerserkerThreatDelta`, `formatBerserkerThreatDelta`) for deterministic testing.
  - Keep signed text visible even with directional colors (accessibility + log readability).
  - Persist compact layout by placing delta row directly below `Threat: <score> (<tier)`.
- Verification set:
  - `luac -p main.lua src/hud.lua`
  - `lua scripts/regression_hud_berserker_counters.lua`
- Backlog sync:
  - Marked completed in `POST_RC_BACKLOG.md` and mirrored in `TASKS.md`.
- Next priority:
  - No unchecked entries remain in ACTION_ITEMS/TASKS/POST_RC; queue next Game Director experiment candidate.

## 2026-03-20 10:58 KST — Game Director experiment: threat-aware onboarding micro-tip
- Completed vertical slice: after build onboarding milestone, HUD hint now teaches combat pressure model (`THREAT` + `THREAT Δ`) until first berserker threat event is observed.
- Durable decisions:
  - Added onboarding `threat` milestone in `src/onboarding_hints.lua` and state export.
  - Runtime marks milestone from berserker enrage/lunge signals in `main.lua` to avoid permanent tutorial copy.
  - Kept economy/combat mechanics untouched (UX-only reversible slice).
- Verification set:
  - `luac -p main.lua src/onboarding_hints.lua`
  - `lua scripts/regression_onboarding_hints.lua`
  - `lua scripts/regression_hud_berserker_counters.lua`
- Backlog sync:
  - Marked completed in `POST_RC_BACKLOG.md` and mirrored in `TASKS.md`.
  - Added next experiment candidates: pressure-breaker bonus, overclock hazard room.

## 2026-03-20 11:06 KST — Mission pressure-breaker bonus shipped
- Completed: Systems/Combat P1 experiment `mission-chain pressure breaker bonus`.
- Durable decisions:
  - `RunMissions.addProgress` now accepts optional context and emits `pressureBreakerDodgeCharge` on rising-threat completions.
  - Main loop tracks short rising-threat window from berserker threat-score delta and applies pressure-breaker dodge charge grants (6s TTL).
  - Enemy attack resolution consumes dodge charges before damage (`dodged_player`) while preserving berserker recovery flow.
  - HUD/status readability updated with `Dodge:<n>` + pressure-breaker trigger copy.
- Verification:
  - `luac -p main.lua src/run_missions.lua src/player.lua src/enemy_ai.lua src/entities.lua src/hud.lua`
  - `lua scripts/regression_mission_momentum.lua`
  - `lua scripts/regression_mission_pressure_breaker.lua`
  - `lua scripts/regression_hud_berserker_counters.lua`
  - `lua scripts/regression_enemy_behavior_variants.lua`
- Next priority: `World/Design Team: Add overclock hazard room prototype (SRL discount pulse + aggro spike risk)`.

## 2026-03-20 11:26 KST — Overclock hazard room prototype shipped
- Completed: `World/Design Team: Add overclock hazard room prototype (SRL discount pulse + aggro spike risk)`.
- Durable decisions:
  - New runtime module `src/overclock_hazard.lua` owns zone pulse/cooldown state, build-cost discount, and combat pressure profile.
  - `maps/map_07.lua` now defines prototype hazard room metadata in center contest zone.
  - Build-cost plan (`src/inventory_ui.lua`) applies temporary SRL discount during active pulse.
  - Enemy AI consumes hazard pressure (`EnemyAI.setThreatPressure`) to increase aggro via move-cadence + detection boost.
  - HUD/status now surface overclock state (`OVERCLOCK READY/HOT/CD`) and pulse activation/expiry messages.
- Verification:
  - `lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_mission_pressure_breaker.lua`
  - `luac -p src/overclock_hazard.lua src/entities.lua src/enemy_ai.lua src/inventory_ui.lua src/hud.lua main.lua maps/map_07.lua`
- Next priority: `P2 Ops — QA/Systems: weekly changelog drift detector`.

## 2026-03-20 12:01 KST — P2 weekly changelog drift detector completed
- Completed backlog item: `QA/Systems: Add weekly changelog drift detector (code changes without corresponding team-log/report entry)`.
- Durable decision: weekly sustain now audits recent code commits for same-commit evidence updates (team logs/playtest artifacts/changelog trackers) via `scripts/weekly_changelog_drift_check.py` with artifacts at `logs/weekly_changelog_drift.{md,json}`.
- Regression guardrail: `scripts/regression_weekly_changelog_drift.py` validates WARN on code-only commit and OK on code+evidence commit.
- Ops wiring: `scripts/run_weekly_sustain.sh` now runs detector + regression and includes drift artifacts in its output manifest.
- RC checklist matrix now includes a dedicated row for weekly changelog drift detection.
- Verification set:
  - `python3 -m py_compile scripts/weekly_changelog_drift_check.py scripts/regression_weekly_changelog_drift.py`
  - `python3 scripts/regression_weekly_changelog_drift.py`
  - `python3 scripts/weekly_changelog_drift_check.py`
  - `bash scripts/run_weekly_sustain.sh`
- Current detector status on branch: `WARN` (historical code commits in scan window without same-commit evidence updates), which is expected baseline before enforcement adoption.
- Next priority item (POST_RC_BACKLOG): `Ops: Add sustain dashboard regression risk score (0~100) with threshold alert section`.
- Sustain health dashboard now includes a computed `regressionRisk` block (0~100) with thresholded alert states (`OK`/`WARN`/`ALERT`) and fixed thresholds (`warnAt=30`, `alertAt=60`).
- Markdown dashboard includes a dedicated **Regression Risk** section so weekly ops reviews can spot escalating regression pressure without parsing raw signals.
- Overclock hazard HUD hint now includes explicit active-pulse and cooldown countdown seconds (`OVERCLOCK HOT <n>s`, `OVERCLOCK CD <n>s`) for better risk/reward timing readability while traversing map_07 hazard zones.
- Added sustain dashboard `regressionRisk.topDrivers` (top 3 weighted contributors) to both markdown and JSON outputs for faster root-cause scanning during weekly ops review.
- Regression coverage now asserts driver rendering in markdown and payload correctness in JSON (`trendStable` baseline case).
- Completed POST_RC item: `Ops: Add sustain dashboard regression-risk driver breakdown (top contributors) in markdown/json with regression coverage`.
- Next priority item: none currently unchecked in `POST_RC_BACKLOG.md` (needs new Game Director experiment injection).
- 2026-03-20 14:29 KST: Completed POST-RC hazard readability follow-up — overclock HUD hint now includes persistent `RISK:<tier>(<score>)` label in READY/HOT/CD states.
- Risk-tier derivation is display-only and computed from existing hazard knobs (`discountPct`, `aggroDetectBonus`, `aggroMoveMul`) to avoid content/schema churn.
- Regression coverage updated: `scripts/regression_overclock_hazard.lua` now asserts risk label presence across all hazard hint states.
- Verification pass: `lua scripts/regression_overclock_hazard.lua`, `luac -p src/overclock_hazard.lua`.
- Next priority: no unchecked items currently present in `POST_RC_BACKLOG.md` (requires new backlog injection).
- 2026-03-20 14:56 KST: Added active overclock pulse aggro-pressure legend in HUD hint (`AGGRO DET:+n MOVE:+m%`) so hazard risk is explicit beyond generic `AGGRO+` text.
- Change is readability-only: hazard mechanics, scoring, and map metadata remain unchanged.
- Regression coverage updated in `scripts/regression_overclock_hazard.lua` to assert detect/move legend tokens in HOT state.
- Verification pass: `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua`, `lua scripts/regression_overclock_hazard.lua`.


- Overclock hazard cooldown hint now shows in-zone near-ready warning token `IMMINENT:<n>s` during final 3 seconds before pulse re-arm; warning hides outside the hazard zone.
- Regression coverage for overclock hazard now asserts imminent warning visibility/hide behavior (`scripts/regression_overclock_hazard.lua`).

## 2026-03-20 16:29 KST — P1 hazard readability follow-up: pulse-imminent warning
- Completed backlog item: `UX/World Team: Add overclock pulse-imminent warning in cooldown HUD hint when standing in hazard zone (IMMINENT:<n>s)`.
- Durable decisions:
  - Show imminent warning only when player is inside hazard zone and cooldown is within 3 seconds.
  - Keep warning embedded in existing cooldown hint line to preserve DOS HUD compactness.
- Verification set:
  - `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_overclock_hazard.lua`
- Backlog update:
  - Marked new item done in `POST_RC_BACKLOG.md` and mirrored in `TASKS.md`.
- Next priority item:
  - No unchecked entries remain in ACTION_ITEMS/TASKS/POST_RC; inject fresh Game Director experiment candidate next cycle.
- Overclock hazard now supports pulse-capped hot-zone kill bounty rewards (`killBonusPerKill`, `killBonusPulseCap`) and runtime payout via `OverclockHazard.consumeKillBonus(kills)`.
- map_07 overclock metadata now sets baseline bounty tuning (`killBonusPerKill=1`, `killBonusPulseCap=3`).
- Overclock hazard regression now asserts kill bounty payout, pulse cap enforcement, and outside-zone no-reward behavior.

## 2026-03-20 16:55 KST — P1 hazard reward follow-up: hot-zone kill bounty
- Completed backlog item: `Systems/World Team: Add overclock hot-zone kill bounty (+BUILDER.SRL per kill, pulse-capped)`.
- Durable decisions:
  - Kill bounty awards only while player is inside active overclock pulse zone.
  - Payout is pulse-capped to keep reward additive without opening an infinite SRL loop.
  - Runtime status copy explains bonus trigger immediately (`OVERCLOCK BOUNTY...`).
- Verification set:
  - `luac -p main.lua src/overclock_hazard.lua maps/map_07.lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_overclock_hazard.lua`
- Backlog update:
  - Marked done in `POST_RC_BACKLOG.md` and `TASKS.md`.
  - Added next follow-up candidate: HOT-hint bounty progress token (`BOUNTY:x/y`).

## 2026-03-20 17:03 KST — P1 hazard reward follow-up: HOT bounty progress token
- Completed backlog item: `UX/Systems Team: Surface overclock bounty pulse cap progress in HUD hint (BOUNTY:x/y) during HOT state`.
- Durable decisions:
  - HOT hint now includes `BOUNTY:x/y` derived from pulse reward units granted vs per-pulse cap.
  - Token initializes at `0/cap` when pulse activates and updates as kills consume bounty budget.
  - Layout stays single-line DOS style (`discount / aggro legend / bounty`) to avoid HUD row growth.
- Verification set:
  - `lua scripts/regression_overclock_hazard.lua`
- Backlog update:
  - Marked item done in `POST_RC_BACKLOG.md` and mirrored done in `TASKS.md`.
- Next priority item:
  - No unchecked items currently remain in `POST_RC_BACKLOG.md`.

## 2026-03-20 17:31 KST — P1 hazard reward readability: READY/CD next-pulse bounty budget
- Completed backlog item: `UX/Systems Team: Surface next-pulse bounty budget token in READY/CD hints (NEXT BOUNTY:0/y) for reward planning`.
- Durable decisions:
  - Overclock READY and cooldown HUD hints now include `NEXT BOUNTY:0/y` so reward budget is legible before pulse activation.
  - This is display-only; kill-bounty payout/cap mechanics are unchanged.
  - Imminent cooldown warning (`IMMINENT`) now coexists with `NEXT BOUNTY` token in a single compact hint line.
- Verification set:
  - `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_overclock_hazard.lua`
- Backlog update:
  - Marked done in `POST_RC_BACKLOG.md` and mirrored done in `TASKS.md`.
- Next priority item:
  - No unchecked items remain in ACTION_ITEMS/TASKS/POST_RC; inject next Game Director experiment candidate next cycle.

## 2026-03-20 18:01 KST — P1 hazard readability wave 2: risk-tier color coding in overclock HUD hint
- Completed backlog item: `UX/World Team: Color-code overclock RISK tier in HUD hint (LOW=green, MED=amber, HIGH=red)`.
- Durable decisions:
  - Overclock hazard module now exposes tier-aware HUD color metadata (`getHudHintColor`) to keep risk semantics centralized.
  - HUD auxiliary threat hint renderer accepts optional per-hint RGBA color and falls back to existing amber tone when metadata is absent.
  - Risk-tier color mapping mirrors established threat readability palette: LOW green, MED amber, HIGH red.
- Verification set:
  - `luac -p main.lua src/hud.lua src/overclock_hazard.lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_overclock_hazard.lua`
- Backlog update:
  - Marked done in `POST_RC_BACKLOG.md` and mirrored done in `TASKS.md`.
- Next priority item:
  - ACTION_ITEMS/TASKS/POST_RC currently fully checked; inject next validated Game Director experiment candidate.
- Overclock HUD hints now include compact risk-factor breakdown token `RISK SRC:Dx+DETy+MOVEz` in READY/HOT/CD states so hazard tuning impact is legible in-run without opening configs.

## 2026-03-20 18:31 KST — P1 hazard readability wave 3: risk-factor breakdown token
- Completed backlog item: `UX/Systems Team: Add compact overclock risk-factor breakdown token in HUD hint (RISK SRC:Dx+DETy+MOVEz)`.
- Durable decisions:
  - Added `getRiskComponents` + `getRiskBreakdownToken` in `src/overclock_hazard.lua` so risk score internals remain centralized and testable.
  - OVERCLOCK READY/HOT/CD HUD hints now append `RISK SRC:Dx+DETy+MOVEz` alongside existing `RISK:<tier>(<score>)` token.
  - Change is readability-only (no hazard reward/aggro/economy tuning changes).
- Verification set:
  - `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_overclock_hazard.lua`
- Backlog update:
  - Marked done in `POST_RC_BACKLOG.md`.
- Next priority item:
  - ACTION_ITEMS/TASKS/POST_RC currently fully checked; inject next validated Game Director experiment candidate next cycle.

## 2026-03-20 19:03 KST — P1 hazard readability wave 4 (next-pulse ETA)
- Completed backlog item: `UX/World Team: Add overclock pulse ETA token in READY/CD HUD hints (NEXT PULSE:<n>s)`.
- Durable decisions:
  - Added `getNextPulseEtaToken()` helper in `src/overclock_hazard.lua` to standardize cooldown/ready timing copy.
  - READY and CD/IMMINENT hints now include `NEXT PULSE:<n>s` while HOT hint payload remains unchanged to preserve compact combat readability.
  - Regression guardrail extended in `scripts/regression_overclock_hazard.lua` to assert ETA token visibility in READY/CD/IMMINENT states.
- Verification set:
  - `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_overclock_hazard.lua`
- Backlog update: `POST_RC_BACKLOG.md` wave-4 item marked done.
- Next priority item: none currently unchecked in tracked backlogs; inject next Game Director experiment candidate.

## 2026-03-20 19:39 KST — P1 hazard readability wave 5 (pulse/recharge progress)
- Completed backlog item: `UX/World Team: Add pulse progress token in overclock HUD hints (PULSE:%/RECHARGE:%)`.
- Durable decisions:
  - Added reusable timing-format helpers in `src/overclock_hazard.lua` for pulse and cooldown progress percentages.
  - HOT hint now shows `PULSE:%`; READY/CD/IMMINENT hints now show `RECHARGE:%` while preserving existing risk/bounty/ETA tokens.
  - Regression updated in `scripts/regression_overclock_hazard.lua` to lock token visibility across state transitions.
- Verification set:
  - `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_overclock_hazard.lua`
- Backlog update:
  - Marked wave-5 item done in `POST_RC_BACKLOG.md` and mirrored done state in `TASKS.md`.
- Next priority item:
  - No unchecked entries currently remain in ACTION_ITEMS/TASKS/POST_RC; queue next Game Director experiment candidate for injection.

## 2026-03-20 20:01 KST — Hazard Readability Wave 6
- Completed backlog item: `UX/World Team: Add overclock risk-trend token in READY/CD/HOT hints (RISK Δ:+n|-n)`.
- Durable decisions:
  - Added state-aware `RISK Δ` formatter in `src/overclock_hazard.lua` (+2 during HOT pulse, +1 while in-zone IMMINENT cooldown, 0 otherwise).
  - Kept existing `RISK:<tier>(score)` + `RISK SRC` tokens unchanged to preserve tuning readability while adding pressure-shift signal.
  - Applied token to READY/HOT/CD/IMMINENT copy paths with compact DOS-safe line format.
- Verification set:
  - `lua scripts/regression_overclock_hazard.lua`
- Backlog update:
  - Marked wave-6 item done in `POST_RC_BACKLOG.md` and mirrored subtask completion in `TASKS.md`.
- Next priority item:
  - No unchecked entries remain across ACTION_ITEMS/TASKS/POST_RC; inject next validated Game Director experiment candidate.

## 2026-03-20 20:33 KST — P1 hazard readability wave 7 (zone presence token)
- Completed backlog item: `UX/World Team: Add overclock zone-presence token in HUD hints (ZONE:IN|OUT)`.
- Durable decisions:
  - Added `getZonePresenceToken()` in `src/overclock_hazard.lua` driven by in-zone runtime state (`state.enteredZone`).
  - Overclock READY/HOT/CD/IMMINENT hints now include `ZONE:IN|OUT` while preserving existing risk/bounty/ETA/progress tokens.
  - Change is readability-only; no hazard balance/economy tuning adjustments.
- Verification set:
  - `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_overclock_hazard.lua`
- Backlog update:
  - Marked wave-7 item done in `POST_RC_BACKLOG.md` and mirrored done state in `TASKS.md`.
- Next priority item:
  - No unchecked entries remain in ACTION_ITEMS/TASKS/POST_RC; inject next validated Game Director experiment candidate.
- 2026-03-20 21:04 KST: Completed POST-RC P1 hazard readability wave 8 — overclock HUD hints now include `EXPOSED:<n>s` while player remains in-zone (`ZONE:IN`) across HOT/CD/IMMINENT states.
- Durable decision: exposure timer is continuous-in-zone only (accumulates inside, resets on exit) and is display-only with no hazard balance/economy changes.
- Regression coverage: `scripts/regression_overclock_hazard.lua` now asserts exposure token presence in-zone and absence out-of-zone.
- Verification pass: `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua`, `lua scripts/regression_overclock_hazard.lua`.

## 2026-03-20 21:34 KST — P1 hazard readability wave 9 (exposure commitment tier)
- Completed backlog item: `UX/World Team: Add overclock exposure commitment-tier token in HUD hints (COMMIT:LOW|MID|HIGH)`.
- Durable decisions:
  - Added exposure-tier helpers in `src/overclock_hazard.lua` with stable thresholds (`LOW <5s`, `MID <12s`, `HIGH >=12s`).
  - HUD hints now append `COMMIT:<tier>` alongside `EXPOSED:<n>s` during HOT/CD/IMMINENT in-zone states; token clears when player leaves zone (`ZONE:OUT`).
  - Change is readability-only (no economy/combat parameter changes).
- Verification set:
  - `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_overclock_hazard.lua`
- Backlog update:
  - Marked wave-9 done in `POST_RC_BACKLOG.md` and mirrored done state in `TASKS.md`.
- Next priority item:
  - No unchecked entries currently remain in ACTION_ITEMS/TASKS/POST_RC; inject next validated Game Director experiment candidate.

## 2026-03-20 21:42 KST — P1 hazard readability wave 10 (`RISK Δ` color semantics)
- Completed backlog item: `UX/World Team: Add overclock risk-delta color semantics in HUD hint (rising=red, cooling=green)`.
- Durable decisions:
  - `OverclockHazard.getHudHintColor()` now prioritizes delta-state color when `RISK Δ` is non-zero (red on rising pressure, green on cooling retreat).
  - During out-of-zone cooldown, hazard hint now emits `RISK Δ:-1` to make safe disengage timing explicit.
  - Neutral states keep existing risk-tier color mapping (LOW/MED/HIGH).
- Verification set:
  - `lua scripts/regression_overclock_hazard.lua`
  - `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua`
- Backlog update:
  - Marked wave-10 delta-color item done in `POST_RC_BACKLOG.md` and mirrored done state in `TASKS.md`.
  - Added next candidates: post-pulse relief `WINDOW` token and exposure dwell-bucket telemetry.
- Next priority item:
  - `UX/World Team: Add overclock pulse-end relief burst HUD token (WINDOW:<n>s)`.

## 2026-03-20 22:01 KST — P1 hazard readability wave 10 follow-up (`WINDOW` relief token)
- Completed backlog item: `UX/World Team: Add overclock pulse-end relief burst (+short WINDOW token) after exiting HOT zone to reward disengage timing`.
- Implementation notes:
  - Added relief-window state in `src/overclock_hazard.lua` (`pendingRelief`, `reliefTimer`, configurable `reliefWindowDuration`, default 3s).
  - Relief now arms on HOT-zone disengage and activates only after pulse expiry while player remains outside.
  - Cooldown hint now appends `WINDOW:<n>s` only in out-of-zone cooldown during active relief window; token expires automatically.
- Regression updates:
  - Extended `scripts/regression_overclock_hazard.lua` with relief-window visibility/expiry assertions.
- Verification:
  - `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_overclock_hazard.lua`
- Next priority:
  - `Systems/Telemetry Team: Log overclock zone dwell buckets (LOW|MID|HIGH) per run for exposure-driven tuning evidence`.

## 2026-03-20 22:35 KST — Overclock exposure dwell telemetry baseline
- Completed Post-RC hazard wave follow-up: per-run overclock exposure dwell buckets now tracked as `LOW|MID|HIGH` seconds in hazard runtime state.
- Decision: accumulate dwell using threshold-aware segmentation so long ticks crossing 5s/12s boundaries distribute correctly across buckets (avoids single-bucket misattribution).
- Runtime integration: latest per-run artifact now written on run reset (`R`) to `logs/playtests/overclock_dwell_buckets_latest.json` + `.md`.
- QA coverage: `scripts/regression_overclock_dwell_buckets.lua` validates bucket math + telemetry schema + total exposure aggregation.
- Impact hypothesis: gives tuning evidence for overclock commitment risk profile before adding dashboard-level trending.

## 2026-03-20 22:41 KST — Game Director review cycle executed
- Idea set (L/M/H risk) generated and backlog-injected under `POST_RC_BACKLOG.md` (Game Director Injection section).
- Implemented experiment: run-summary overclock dwell snapshot (`OVERCLOCK DWELL L/M/H`).
- Wiring: `OverclockHazard.getRunDwellBuckets()` snapshot is captured on reset and injected into `RunSummary` state.
- Verification: run summary + hazard + dwell telemetry regressions all PASS.
- Next candidates retained in backlog:
  - reward-efficiency token (`SRL/EXPOSED sec`)
  - multi-run dwell trend combiner artifact.

## 2026-03-20 23:03 KST — P1 Game Director injection: overclock reward-efficiency token
- Completed backlog item: `Systems/Design Team: Add overclock zone reward-efficiency token (SRL/EXPOSED sec) to run summary`.
- Durable decisions:
  - Overclock module now tracks per-run bounty reward total (`runRewardSrl`) and exposes `getRunRewardSrl()`.
  - Run summary snapshot now persists `overclockRewardSrl` and renders token: `OVERCLOCK EFF: <srl> SRL / <sec>s = <ratio> SRL/EXPOSED sec`.
  - Zero-exposure edge case renders `n/a` ratio to prevent divide-by-zero misinformation.
- Verification set:
  - `luac -p main.lua src/overclock_hazard.lua src/run_summary.lua src/hud.lua scripts/regression_run_summary.lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_run_summary.lua`
- Next priority item: `QA/Systems Team: Add multi-run dwell trend combiner artifact (last N run medians)`.

## 2026-03-20 23:33 KST — P1 Game Director injection: multi-run dwell trend combiner
- Completed backlog item: `QA/Systems Team: Add multi-run dwell trend combiner artifact (last N run medians)`.
- Durable decisions:
  - Persist per-reset timestamped dwell snapshots (`overclock_dwell_buckets_run_*.json`) alongside latest snapshot to build review history.
  - New combiner `scripts/overclock_dwell_trend.py` computes median LOW/MID/HIGH/TOTAL and aggregate mix% over last-N runs.
  - Weekly sustain runner now emits trend artifacts (`logs/playtests/overclock_dwell_trend.{md,json}`) and executes trend regression.
- Verification set:
  - `luac -p main.lua src/overclock_hazard.lua`
  - `python3 scripts/regression_overclock_dwell_trend.py`
  - `python3 scripts/overclock_dwell_trend.py --runs 3`
  - `lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_run_summary.lua`
- Next item: all listed backlog lanes are checked; trigger next Game Director review cycle (3 ideas -> choose 1 -> vertical slice).

## 2026-03-20 23:36 KST — Game Director Cycle B completed (3 ideas -> 1 slice)
- Candidate ideas:
  1) **Chosen (low-risk UX):** run-summary commitment profile token from dwell mix.
  2) Mid-risk systems: trend artifact volatility classifier (`VOL:STEADY|SWING`).
  3) High-risk UX density: analytics glossary row in run summary.
- Implemented slice: `src/run_summary.lua` now computes `overclockProfile` and `src/hud.lua` renders `OVERCLOCK PROFILE: ...` under efficiency line.
- Backlog updated in `POST_RC_BACKLOG.md`: chosen item marked done; remaining two ideas retained as open injections.
- Verification:
  - `luac -p main.lua src/run_summary.lua src/hud.lua src/overclock_hazard.lua scripts/regression_run_summary.lua`
  - `lua scripts/regression_run_summary.lua`
  - `lua scripts/regression_overclock_hazard.lua`
  - `python3 scripts/regression_overclock_dwell_trend.py`

## 2026-03-21 00:02 KST — P1 Game Director follow-up: dwell trend volatility token
- Completed backlog item: `Systems Team: Add overclock dwell trend volatility token (VOL:STEADY|SWING) to trend artifact`.
- Durable decisions:
  - `scripts/overclock_dwell_trend.py` now emits `volatility.level`, `volatility.token`, and compact diagnostics (`maxRelDeltaPct`, `avgRelDeltaPct`).
  - Volatility classification uses run-to-run total-exposure relative deltas with deterministic thresholds: `SWING` when `maxΔ>=45%` or `avgΔ>=30%`; otherwise `STEADY`.
  - Markdown trend report now includes a compact line: `Volatility: VOL:<level> (maxΔ ... , avgΔ ...)`.
- Verification set:
  - `python3 -m py_compile scripts/overclock_dwell_trend.py scripts/regression_overclock_dwell_trend.py`
  - `python3 scripts/regression_overclock_dwell_trend.py`
  - `python3 scripts/overclock_dwell_trend.py --runs 3`
- Backlog sync: marked the volatility token item done in `POST_RC_BACKLOG.md`.
- Next priority item: `QA/UX Team: Add compact run-summary tooltip glossary row for overclock analytics tokens (DWELL, EFF, PROFILE)`.

## 2026-03-21 00:32 KST — Post-RC backlog closure: run-summary overclock glossary row
- Closed remaining unchecked Post-RC item by shipping a compact glossary row in run summary:
  - `GLOSSARY: DWELL=EXPOSURE sec(L/M/H)  EFF=SRL/EXPOSED sec  PROFILE=COMMIT TIER`
- Files:
  - `src/hud.lua` (new glossary helper + rendered row)
  - `scripts/regression_run_summary.lua` (copy-stability assertion)
  - `POST_RC_BACKLOG.md` (item lifecycle `[ ] -> [~] -> [x]`)
- Verification:
  - `lua scripts/regression_run_summary.lua` PASS
  - `luac -p src/hud.lua` PASS
- State: ACTION_ITEMS/TASKS/POST_RC_BACKLOG all checked; next cycle should execute Game Director review loop (3 ideas -> pick 1 -> minimal vertical slice).

## 2026-03-21 00:36 KST — Game Director Cycle C executed (all prior backlogs completed)
- Idea slate generated:
  1) Low-risk UX: run-summary `COACH` cue from `PROFILE + EFF`
  2) Mid-risk systems: HIGH-threat objective clear boosts variety payout
  3) High-risk novelty: hazard route tags (`SAFE|RISK|SPIKE`) + HUD callout
- Chosen experiment: #1 (minimal vertical slice, reversible).
- Implementation:
  - `src/run_summary.lua`: added `resolveOverclockCoachTip(...)` and snapshot field `overclockCoachTip`.
  - `src/hud.lua`: renders `OVERCLOCK COACH: <tip>` line in run summary.
  - `scripts/regression_run_summary.lua`: added assertion for coach tip and kept glossary copy guard.
- Verification:
  - `lua scripts/regression_run_summary.lua` PASS
  - `luac -p src/run_summary.lua` PASS
  - `luac -p src/hud.lua` PASS
- Backlog updates (`POST_RC_BACKLOG.md`):
  - Coach cue task marked done.
  - Threat-scaler + hazard-route-tag tasks injected as next experiment candidates.

## 2026-03-21 01:04 KST — Game Director Cycle C follow-up: threat-linked momentum scaler prototype
- Completed Post-RC Cycle C item: `Systems/Combat Team: Prototype threat-linked momentum bonus scaler` behind experiment flag.
- Durable decisions:
  - Added env-gated experiment toggle `DOTPIO_EXPERIMENT_THREAT_LINKED_VARIETY_SCALER` in `src/run_missions.lua`.
  - Lane-switch variety bonus remains `+1` by default; scales to `+2` only when flag is ON and mission completion occurs at `THREAT LVL:HIGH`.
  - Mission progress context now receives live `threatTier` from combat threat counters.
  - UX status line explicitly labels scaled payout as `HIGH-THREAT SCALER`.
- Verification set (PASS):
  - `lua scripts/regression_mission_momentum.lua`
  - `DOTPIO_EXPERIMENT_THREAT_LINKED_VARIETY_SCALER=1 lua scripts/regression_mission_momentum.lua`
  - `lua scripts/regression_mission_pressure_breaker.lua`
- Next priority item: `World/Design Team: Prototype hazard room route tag (SAFE|RISK|SPIKE) in map metadata and HUD mini-callout for path planning`.

## 2026-03-21 01:34 KST — Game Director Cycle D (route-callout readability slice)
- Context: ACTION_ITEMS/TASKS/POST_RC backlog reached fully-checked state, triggering Game Director review cycle.
- Idea slate generated:
  1) Low-risk UX: route callout color semantics (`SAFE|RISK|SPIKE`).
  2) Mid-risk systems: portal transition route preview token (`NEXT ROUTE:<tag>`).
  3) High-risk QA/design: route-tag distribution drift checker across hazard maps.
- Selected experiment: #1 (low-risk, reversible, immediate readability gain).
- Shipped decisions:
  - Route tags are map-metadata-driven (`overclockHazard.routeTag`).
  - Hazard module now exposes `getRouteTag/getRouteCallout/getRouteCalloutColor` with strict tag validation.
  - HUD renders `ROUTE:<tag>` mini-callout near enemy strip and applies semantic colors (SAFE green / RISK amber / SPIKE red).
  - Berserker threat rows offset when route callout exists to avoid visual overlap.
- Verification set (PASS):
  - `luac -p main.lua src/hud.lua src/overclock_hazard.lua maps/map_07.lua`
  - `lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_run_summary.lua`
  - `lua scripts/regression_hud_berserker_counters.lua`
- Backlog injection status:
  - Done: route mini-callout color semantics.
  - Pending: portal hover route preview, route-tag distribution checker.
- Next priority item: `Systems/World Team: Add portal-hover route preview token (NEXT ROUTE:<tag>) in transition prompt before confirming map jump`.

## 2026-03-21 02:06 KST — Post-RC Cycle D follow-up shipped (portal route preview)
- Completed backlog item: `Systems/World Team: Add portal-hover route preview token (NEXT ROUTE:<tag>) in transition prompt before confirming map jump`.
- Gameplay/runtime decision: portal contact now opens a confirm/cancel transition prompt instead of immediate warp.
- Route preview token source: destination map metadata `overclockHazard.routeTag` (`SAFE|RISK|SPIKE`, fallback `UNKNOWN`).
- Evidence (PASS):
  - `luac -p main.lua src/portal.lua src/overclock_hazard.lua src/hud.lua`
  - `lua scripts/regression_overclock_hazard.lua`
  - `lua scripts/regression_portal_route_preview.lua`
- Backlog status:
  - Done: portal-hover route preview token.
  - Remaining top priority: route-tag distribution checker across hazard-enabled maps.
