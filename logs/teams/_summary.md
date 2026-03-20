# Team Logs Summary

Last updated: 2026-03-20 08:56 KST

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
