# Team Logs Summary

Last updated: 2026-03-20 01:28 KST

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
