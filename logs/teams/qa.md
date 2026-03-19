# QA Team Log


## 2026-03-18 23:15:00 KST
- Task: Sanity verification for pickup interaction implementation.
- Commit: HEAD (this run)
- Files checked: `main.lua`, `src/entities.lua`
- Verification:
  - `luac -p main.lua src/entities.lua` ✅
- Decisions:
  - No portal validator run (no map/portal changes).
  - No screenshot regen (no visible UI asset/layout change in this run).
- Follow-up:
  - Add scripted/manual regression checklist entry for drop->pickup->inventory count.

## 2026-03-18 23:44:52 KST
- Task: Verify pickup-hint UI update for M0 UX completion.
- Commit: 3a6b206
- Files checked: `src/hud.lua`, `src/inventory_ui.lua`, `screenshots/screenshot-map04.png`, `screenshots/screenshot-inventory-dos.png`
- Verification:
  - `luac -p src/hud.lua src/inventory_ui.lua` ✅
  - `bash scripts/capture_screenshots.sh` ✅
- Decisions:
  - No portal validator run (no map/portal data changes).
- Follow-up:
  - Execute next M0 regression scenario task (drop->pickup->count) with explicit repro checklist output.

## 2026-03-19 00:13:43 KST
- Task: M0 regression scenario automation for drop -> pickup -> inventory count validation.
- Commit: 3b11aa6
- Files: `scripts/regression_drop_pickup.lua`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `luac -p scripts/regression_drop_pickup.lua` ✅
  - `lua scripts/regression_drop_pickup.lua` ✅ (`[PASS] drop->pickup regression validated`)
- Decisions:
  - Added a headless Lua regression script with LOVE stubs to run in CI/shell without launching the game client.
  - Scenario explicitly validates both inventory count restoration and world-item cleanup after pickup.
- Follow-up:
  - Next M0 task: tune inventory build-test starter loadout for stable build/disassemble smoke runs.

## 2026-03-19 00:45:22 KST
- Task: Verify starter loadout tuning pass (M0 completion).
- Commit: HEAD (this run)
- Files checked: `src/player.lua`, `scripts/regression_starter_loadout.lua`
- Verification:
  - `luac -p src/player.lua scripts/regression_starter_loadout.lua` ✅
  - `lua scripts/regression_starter_loadout.lua` ✅
  - `lua scripts/regression_drop_pickup.lua` ✅
- Decisions:
  - No portal validator run (no map/portal changes).
  - No screenshot regen (no UI rendering/copy/layout changes).
- Follow-up:
  - Start M1 economy telemetry logging for build/disassemble events.

## 2026-03-19 01:14:09 KST
- Task: Verify M1 economy telemetry baseline (build/disassemble).
- Commit: HEAD (this run)
- Files checked: `src/economy_telemetry.lua`, `src/inventory_ui.lua`, `scripts/regression_economy_telemetry.lua`
- Verification:
  - `luac -p src/inventory_ui.lua src/economy_telemetry.lua scripts/regression_economy_telemetry.lua` ✅
  - `lua scripts/regression_economy_telemetry.lua` ✅
  - `lua scripts/regression_starter_loadout.lua` ✅
  - `lua scripts/regression_drop_pickup.lua` ✅
- Decisions:
  - No portal validator run (no map/portal data changes).
  - No screenshot regen (no visible UI rendering/copy/layout changes).
- Follow-up:
  - Continue with M1 stack split interaction + dedicated regression once implementation lands.

## 2026-03-19 01:46:07 KST
- Task: Verify M1 stack split interaction + regressions.
- Commit: 6819ccf
- Files checked: `src/inventory.lua`, `src/inventory_ui.lua`, `scripts/regression_split_stack.lua`
- Verification:
  - `luac -p src/inventory.lua src/inventory_ui.lua scripts/regression_split_stack.lua` ✅
  - `lua scripts/regression_split_stack.lua` ✅
  - `lua scripts/regression_economy_telemetry.lua` ✅
  - `lua scripts/regression_starter_loadout.lua` ✅
  - `lua scripts/regression_drop_pickup.lua` ✅
- Decisions:
  - Added dedicated split regression covering successful split, total-count invariance, and invalid full-stack split rejection.
  - No portal validator run (no map/portal changes).
- Follow-up:
  - Add regression coverage once build preview/confirm flow lands.

## 2026-03-19 02:14:58 KST
- Task: Verify M1 build preview/confirm gate behavior.
- Commit: ec0c770
- Files checked: `src/inventory_ui.lua`, `scripts/regression_build_preview_confirm.lua`
- Verification:
  - `luac -p src/inventory_ui.lua scripts/regression_build_preview_confirm.lua` ✅
  - `lua scripts/regression_build_preview_confirm.lua` ✅
  - `lua scripts/regression_split_stack.lua` ✅
  - `lua scripts/regression_economy_telemetry.lua` ✅
  - `lua scripts/regression_starter_loadout.lua` ✅
  - `lua scripts/regression_drop_pickup.lua` ✅
- Decisions:
  - Build resources are no longer consumed on initial F9 press; consumption occurs only after explicit confirm.
  - Screenshot refresh executed due visible inventory/help copy behavior update.
- Follow-up:
  - Add coverage for explicit SRL affordance copy once action-menu/F9 wording pass lands.

## 2026-03-19 02:44:44 KST
- Task: Verify M1 BUILDER.SRL affordance copy pass.
- Commit: HEAD (this run)
- Files checked: `src/inventory_ui.lua`, `scripts/regression_builder_srl_affordance.lua`
- Verification:
  - `luac -p src/inventory_ui.lua scripts/regression_builder_srl_affordance.lua` ✅
  - `lua scripts/regression_builder_srl_affordance.lua` ✅
  - `lua scripts/regression_build_preview_confirm.lua` ✅
  - `lua scripts/regression_split_stack.lua` ✅
  - `lua scripts/regression_economy_telemetry.lua` ✅
  - `lua scripts/regression_starter_loadout.lua` ✅
  - `lua scripts/regression_drop_pickup.lua` ✅
- Decisions:
  - Added explicit regression for lock/status strings to prevent future copy drift away from `BUILDER.SRL` terminology.
  - Screenshot regen executed because visible inventory/help copy changed.
- Follow-up:
  - Reuse new affordance regression when touching action-menu/F9 copy in subsequent UX passes.

## 2026-03-19 03:14:05 KST
- Task: Verify M1 anti-exploit report implementation.
- Commit: HEAD (this run)
- Files checked: `src/economy_anti_exploit.lua`, `scripts/economy_anti_exploit_report.lua`, `scripts/regression_anti_exploit_report.lua`
- Verification:
  - `luac -p src/economy_anti_exploit.lua scripts/economy_anti_exploit_report.lua scripts/regression_anti_exploit_report.lua` ✅
  - `lua scripts/regression_anti_exploit_report.lua` ✅
  - `lua scripts/economy_anti_exploit_report.lua 20` ✅
  - `lua scripts/regression_economy_telemetry.lua` ✅
  - `lua scripts/regression_build_preview_confirm.lua` ✅
  - `lua scripts/regression_split_stack.lua` ✅
  - `lua scripts/regression_builder_srl_affordance.lua` ✅
- Decisions:
  - Added explicit regression scenario that injects flat-SRL/high-output windows and asserts suspicious loop flagging.
  - Report CLI now returns pass with empty baseline report when telemetry source is absent instead of hard-failing.
- Follow-up:
  - Add a fixture with net-positive SRL window once live telemetry from extended playtest is captured.

## 2026-03-19 03:44:56 KST
- Task: Validate M1 SRL cost-curve tuning regression coverage.
- Commit: 242f0db
- Files checked: `src/inventory_ui.lua`, `scripts/regression_srl_cost_curve.lua`
- Verification:
  - `luac -p src/inventory_ui.lua scripts/regression_srl_cost_curve.lua` ✅
  - `lua scripts/regression_srl_cost_curve.lua` ✅
  - `lua scripts/regression_build_preview_confirm.lua` ✅
  - `lua scripts/regression_economy_telemetry.lua` ✅
  - `lua scripts/regression_anti_exploit_report.lua` ✅
- Decisions:
  - Locked regression expectation that low-tier salvage-heavy recipes should stay high-cost (>=6 BUILDER.SRL) and not undercut premium recipes.
- Follow-up:
  - Add extended telemetry fixture once 30-minute loop runs are collected to validate live balance envelope.

## 2026-03-19 04:13:17 KST
- Task: Verify M1 disassembly salvage cap fairness tuning.
- Commit: HEAD (this run)
- Files checked: `src/ai_describe.lua`, `src/inventory_ui.lua`, `scripts/regression_disassembly_caps.lua`
- Verification:
  - `luac -p src/ai_describe.lua src/inventory_ui.lua scripts/regression_disassembly_caps.lua` ✅
  - `lua scripts/regression_disassembly_caps.lua` ✅
  - `lua scripts/regression_srl_cost_curve.lua` ✅
  - `lua scripts/regression_builder_srl_affordance.lua` ✅
  - `bash scripts/capture_screenshots.sh` ✅
- Decisions:
  - Locked tiered cap regression for tiny/medium/large source sizes to prevent future over-nerf/over-yield drift.
  - Screenshot refresh confirmed inventory help text update for new disassembly cap/budget guidance.
- Follow-up:
  - Add playtest fixture once map progression validation run executes, so cap tuning can be checked against full 30-minute loop logs.

## 2026-03-19 04:43:40 KST
- Task: QA verification for M1 map_01~04 progression validation.
- Commit: HEAD (this run)
- Files checked: `scripts/regression_map_progression.py`, `logs/playtests/map_01_04_progression_checklist.md`
- Verification:
  - `python3 -m py_compile scripts/regression_map_progression.py` ✅
  - `python3 scripts/regression_map_progression.py` ✅
  - Checklist artifact includes portal validator transcript + manual quick-pass checklist ✅
- Decisions:
  - Progression validation is now reproducible as a scripted QA artifact instead of ad-hoc command output.
- Follow-up:
  - Use the new checklist artifact as input baseline for the next 30-minute loop checklist run.

## 2026-03-19 05:13:00 KST
- Task: QA verification for M1 scripted 30-minute loop checklist pass.
- Commit: HEAD (this run)
- Files checked: `scripts/regression_30min_loop_checklist.py`, `logs/playtests/loop_30min_checklist.md`
- Verification:
  - `python3 -m py_compile scripts/regression_30min_loop_checklist.py` ✅
  - `python3 scripts/regression_30min_loop_checklist.py` ✅
  - Artifact result is `PASS` with all scripted checks marked complete ✅
- Decisions:
  - No screenshot regen (no UI/layout/copy changes in runtime views).
  - No direct portal validator command needed because the checklist invokes `scripts/regression_map_progression.py`, which already wraps validator coverage.
- Follow-up:
  - For M2 map work, re-run this checklist after map_05 lands to keep 30-minute loop gate trending green.

## 2026-03-19 05:43:40 KST
- Task: QA verification for M2 map_05 layout + portal links.
- Commit: `f1b32bf`
- Files checked: `maps/map_04.lua`, `maps/map_05.lua`, `logs/playtests/map_01_04_progression_checklist.md`
- Verification:
  - `luac -p maps/map_04.lua maps/map_05.lua` ✅
  - `python3 scripts/validate_portals.py` ✅ (new map wiring resolves)
  - `python3 scripts/regression_map_progression.py` ✅ (map_01~04 gate still passes)
- Decisions:
  - No screenshot regen required (no UI/copy/layout-facing screen changes).
- Follow-up:
  - Re-run portal validator and progression checklist after map_06 lands.

## 2026-03-19 06:12:51 KST
- Task: QA verification for M2 map_06 layout + portal links.
- Commit: HEAD (this run)
- Files checked: `maps/map_05.lua`, `maps/map_06.lua`, `logs/playtests/map_01_04_progression_checklist.md`
- Verification:
  - `luac -p maps/map_05.lua maps/map_06.lua` ✅
  - `python3 scripts/validate_portals.py` ✅ (new map wiring resolves)
  - `python3 scripts/regression_map_progression.py` ✅ (map_01~04 gate still passes)
- Decisions:
  - No screenshot regen required (no UI/copy/layout-facing screen changes).
- Follow-up:
  - Re-run full loop checklist once enemy variant work lands to confirm momentum gate remains green.

## 2026-03-19 07:13:57 KST
- Task: QA verification for M2 build category diversity constraints.
- Commit: `HEAD (this run)`
- Files checked: `src/ai_describe.lua`, `scripts/regression_build_category_diversity.lua`
- Verification:
  - `luac -p src/ai_describe.lua scripts/regression_build_category_diversity.lua` ✅
  - `lua scripts/regression_build_category_diversity.lua` ✅
- Decisions:
  - No screenshot regen required (runtime UI/copy/layout unchanged).
  - No portal validator required (map files untouched).
- Follow-up:
  - Pair next loot reward table pass with a regression that samples category distribution by map tier.

## 2026-03-19 07:43:35 KST
- Task: QA verification for M2 lootbox reward table pass by map tier.
- Commit: `HEAD (this run)`
- Files checked: `src/entities.lua`, `scripts/regression_lootbox_rewards_by_tier.lua`
- Verification:
  - `luac -p src/entities.lua scripts/regression_lootbox_rewards_by_tier.lua` ✅
  - `lua scripts/regression_lootbox_rewards_by_tier.lua` ✅
  - `lua scripts/regression_build_category_diversity.lua` ✅
- Decisions:
  - No screenshot regen required (UI/copy/layout unchanged).
  - No portal validator required (map files untouched).
- Follow-up:
  - Include loot-tier regression in next full 30-minute loop checklist rerun to ensure economy momentum remains stable.

## 2026-03-19 08:15:07 KST
- Task: QA verification for M3 run mission prototype.
- Commit: HEAD (this run)
- Files checked: `src/run_missions.lua`, `src/combat.lua`, `src/inventory_ui.lua`, `src/hud.lua`, `main.lua`, `scripts/regression_run_missions.lua`
- Verification:
  - `luac -p main.lua src/run_missions.lua src/hud.lua src/combat.lua src/inventory_ui.lua scripts/regression_run_missions.lua` ✅
  - `lua scripts/regression_run_missions.lua` ✅
  - `bash scripts/capture_screenshots.sh` ✅ (HUD mission panel reflected in refreshed artifacts)
- Decisions:
  - Regression covers objective progress and completion clamp behavior; no portal validator run required (map files untouched).
- Follow-up:
  - Add mission-progress checks into the 30-minute orchestrator regression after unlock/fail-forward systems are added.

## 2026-03-19 08:45:23 KST
- Task: QA verification for M3 unlock flag framework.
- Commit: HEAD (this run)
- Files checked: `src/unlocks.lua`, `src/ai_describe.lua`, `main.lua`, `src/hud.lua`, `scripts/regression_unlock_flags.lua`
- Verification:
  - `luac -p main.lua src/hud.lua src/ai_describe.lua src/unlocks.lua scripts/regression_unlock_flags.lua` ✅
  - `lua scripts/regression_run_missions.lua` ✅
  - `lua scripts/regression_build_category_diversity.lua` ✅
  - `lua scripts/regression_unlock_flags.lua` ✅
  - `bash scripts/capture_screenshots.sh` ✅
- Decisions:
  - Unlock regression asserts advanced categories remain gated pre-completion and become available post-mission completion.
  - No portal validator run required (map/portal files unchanged).
- Follow-up:
  - Extend unlock regression once fail-forward rewards/summaries start consuming unlock state.

## 2026-03-19 09:13:50 KST
- Task: QA verification for M3 fail-forward carryover rewards.
- Commit: `90cdfa9`
- Files checked: `main.lua`, `src/fail_forward.lua`, `scripts/regression_fail_forward_rewards.lua`
- Verification:
  - `luac -p main.lua src/fail_forward.lua scripts/regression_fail_forward_rewards.lua` ✅
  - `lua scripts/regression_fail_forward_rewards.lua` ✅
- Decisions:
  - Regression asserts carryover formula/caps and confirms rewards are applied to a fresh run inventory with status copy emitted.
  - No portal validator run required (map/portal files untouched).
  - No screenshot regen required (no persistent UI layout/copy asset change).
- Follow-up:
  - Add summary-screen regression coverage once M3 run result screen is implemented.

## 2026-03-19 09:44:22 KST
- Task: QA verification for M3 run summary screen + unlock progress.
- Commit: HEAD (this run)
- Files checked: `main.lua`, `src/hud.lua`, `src/run_summary.lua`, `scripts/regression_run_summary.lua`
- Verification:
  - `luac -p main.lua src/hud.lua src/run_summary.lua scripts/regression_run_summary.lua` ✅
  - `lua scripts/regression_run_summary.lua` ✅
  - `lua scripts/regression_fail_forward_rewards.lua` ✅
  - `bash scripts/capture_screenshots.sh` ✅
- Decisions:
  - Regression confirms summary snapshot immutability after open and validates close behavior.
  - No portal validator run required (map/portal files untouched).
- Follow-up:
  - Fold run-summary checks into 30-minute orchestrator if M4 onboarding flow changes restart semantics.

## 2026-03-19 10:13:54 KST
- Task: QA verification for M4 terminology consistency + build material explicitness.
- Commit: HEAD (this run)
- Files checked: `src/inventory_ui.lua`, `main.lua`, `screenshots/screenshot-map04.png`, `screenshots/screenshot-inventory-dos.png`
- Verification:
  - `luac -p src/inventory_ui.lua main.lua` ✅
  - `lua scripts/regression_build_preview_confirm.lua` ✅
  - `lua scripts/regression_builder_srl_affordance.lua` ✅
  - `bash scripts/capture_screenshots.sh` ✅
- Decisions:
  - Existing build preview/affordance regressions still pass after terminology/copy normalization.
  - Screenshot refresh required and captured (visible inventory/help/status copy changes).
  - No portal validator run required (map/portal files unchanged).
- Follow-up:
  - Add/extend regression coverage once M4 always-visible lock reason work lands.

## 2026-03-19 10:45:09 KST
- Task: QA verification for M4 always-visible lock reason rollout.
- Commit: HEAD (this run)
- Files checked: `src/inventory_ui.lua`, `scripts/regression_action_menu_lock_reasons.lua`, `screenshots/screenshot-map04.png`
- Verification:
  - `luac -p src/inventory_ui.lua scripts/regression_action_menu_lock_reasons.lua` ✅
  - `lua scripts/regression_action_menu_lock_reasons.lua` ✅
  - `lua scripts/regression_builder_srl_affordance.lua` ✅
  - `lua scripts/regression_build_preview_confirm.lua` ✅
  - `bash scripts/capture_screenshots.sh` ✅
- Decisions:
  - New regression confirms disabled action rows retain explicit lock metadata for USE/DISASM/SPLIT.
  - Screenshot refresh performed due visible Action Menu copy changes.
  - No portal validator run required (map/portal files unchanged).
- Follow-up:
  - Add onboarding hint-flow regression once M4 onboarding implementation lands.

## 2026-03-19 11:14:50 KST
- Task: QA verification for M4 compact onboarding hint flow.
- Commit: HEAD (this run)
- Files checked: `main.lua`, `src/hud.lua`, `src/onboarding_hints.lua`, `scripts/regression_onboarding_hints.lua`, `screenshots/screenshot-map04.png`, `screenshots/screenshot-inventory-dos.png`
- Verification:
  - `luac -p main.lua src/hud.lua src/onboarding_hints.lua scripts/regression_onboarding_hints.lua` ✅
  - `lua scripts/regression_onboarding_hints.lua` ✅
  - `lua scripts/regression_action_menu_lock_reasons.lua` ✅
  - `lua scripts/regression_builder_srl_affordance.lua` ✅
  - `lua scripts/regression_build_preview_confirm.lua` ✅
  - `bash scripts/capture_screenshots.sh` ✅
- Decisions:
  - Added deterministic regression coverage for onboarding hint progression order and 5-minute expiry.
  - Screenshot refresh confirmed due visible HUD strip changes in map/inventory captures.
  - No portal validator run required (map/portal files unchanged).
- Follow-up:
  - Add checklist artifact when M4 keyboard-only usability pass is implemented.

## 2026-03-19 11:43:49 KST
- Task: QA verification for M4 keyboard-only usability pass checklist.
- Commit: HEAD (this run)
- Files checked: `scripts/regression_keyboard_shortcuts.lua`, `scripts/regression_keyboard_usability_checklist.py`, `logs/playtests/keyboard_only_usability_checklist.md`
- Verification:
  - `luac -p scripts/regression_keyboard_shortcuts.lua` ✅
  - `python3 -m py_compile scripts/regression_keyboard_usability_checklist.py` ✅
  - `lua scripts/regression_keyboard_shortcuts.lua` ✅
  - `python3 scripts/regression_keyboard_usability_checklist.py` ✅
- Decisions:
  - Scripted checks now verify keyboard binding coverage plus lock-reason/onboarding/build-preview keyboard flows in one checklist pass.
  - Generated deterministic artifact `logs/playtests/keyboard_only_usability_checklist.md` for release gate evidence.
  - No portal validator run required (map/portal files unchanged).
  - No screenshot refresh required (no UI rendering/layout source changed).
- Follow-up:
  - Start M5 RC checklist document and connect it to existing regression artifacts.

## 2026-03-19 12:12:53 KST
- Task: Create M5 RC checklist document with executable regression matrix.
- Commit: HEAD (this run)
- Files checked: `logs/playtests/rc_checklist.md`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `python3 -m py_compile scripts/regression_30min_loop_checklist.py scripts/regression_map_progression.py scripts/regression_keyboard_usability_checklist.py scripts/validate_portals.py` ✅
  - `lua scripts/regression_enemy_behavior_variants.lua` ✅
- Decisions:
  - Added release-candidate checklist artifact `logs/playtests/rc_checklist.md` with gate rows for combat/inventory/build/disasm/portal + explicit command/artifact mapping.
  - Included blocker triage table and cross-team RC sign-off section to standardize launch readiness reviews.
  - No portal/map source changes in this task; validator is referenced in checklist and syntax-verified only.
  - No screenshot refresh required in this run (checklist/documentation-only change).
- Follow-up:
  - Execute full M5 regression matrix from `logs/playtests/rc_checklist.md` and file blockers before fixing critical issues.

## 2026-03-19 12:44:12 KST
- Task: M5 full regression execution (combat/inventory/build/disasm/portal) from RC matrix.
- Commit: HEAD (this run)
- Files checked: `logs/playtests/rc_checklist.md`, `logs/playtests/loop_30min_checklist.md`, `logs/playtests/map_01_04_progression_checklist.md`, `logs/playtests/keyboard_only_usability_checklist.md`, `logs/economy_anti_exploit_report.json`, `logs/economy_anti_exploit_report.md`, `screenshots/screenshot-map04.png`, `screenshots/screenshot-inventory-dos.png`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `python3 scripts/regression_30min_loop_checklist.py` ✅
  - `lua scripts/regression_enemy_behavior_variants.lua` ✅
  - `lua scripts/regression_drop_pickup.lua` ✅
  - `lua scripts/regression_build_preview_confirm.lua` ✅
  - `lua scripts/regression_builder_srl_affordance.lua` ✅
  - `lua scripts/regression_split_stack.lua` ✅
  - `lua scripts/regression_disassembly_caps.lua` ✅
  - `lua scripts/regression_srl_cost_curve.lua` ✅
  - `lua scripts/regression_anti_exploit_report.lua` ✅
  - `lua scripts/economy_anti_exploit_report.lua` ✅
  - `python3 scripts/regression_map_progression.py` ✅
  - `python3 scripts/validate_portals.py` ✅
  - `lua scripts/regression_action_menu_lock_reasons.lua` ✅
  - `lua scripts/regression_onboarding_hints.lua` ✅
  - `python3 scripts/regression_keyboard_usability_checklist.py` ✅
  - `bash scripts/capture_screenshots.sh` ✅
- Decisions:
  - Updated RC checklist rows and release gates to PASS based on fresh command/artifact evidence.
  - Recorded blocker triage result as zero critical/high blockers for this sweep.
  - Marked M5 full regression as complete in `ACTION_ITEMS.md` and `TASKS.md`.
- Follow-up:
  - Next M5 priority item: fix any newly reported critical blockers (if discovered) and proceed to launch changelog/screenshot packaging + RC tag.

## 2026-03-19 13:12:39 KST
- Task: M5 fix-all-critical-blockers closure audit (blocker-focused rerun + triage update).
- Commit: HEAD (this run)
- Files: `ACTION_ITEMS.md`, `TASKS.md`, `logs/playtests/rc_checklist.md`
- Verification:
  - `python3 scripts/regression_30min_loop_checklist.py` ✅
  - `lua scripts/regression_anti_exploit_report.lua` ✅
  - `lua scripts/economy_anti_exploit_report.lua` ✅
  - `python3 scripts/validate_portals.py` ✅
- Decisions:
  - Confirmed no outstanding critical/high blockers after targeted rerun; kept blocker triage at 0 critical / 0 high.
  - Added blocker-audit row `RC-20260319-01` to RC checklist to preserve rerun evidence.
  - Marked "Fix all critical blockers" complete in both backlog trackers.
- Follow-up:
  - Next M5 item: capture launch screenshots + changelog, then create release candidate tag.

## 2026-03-19 13:43:27 KST
- Task: M5 capture launch screenshots + changelog packaging.
- Commit: HEAD (this run)
- Files: `CHANGELOG.md`, `screenshots/screenshot-map04.png`, `screenshots/screenshot-inventory-dos.png`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `bash scripts/capture_screenshots.sh` ✅
- Decisions:
  - Added root `CHANGELOG.md` with RC snapshot (`0.5.0-rc.1`) consolidating shipped M0~M5 deltas for release packaging.
  - Refreshed launch screenshot artifacts from scripted capture pipeline.
  - Marked "Capture launch screenshots + changelog" complete in both backlog trackers.
- Follow-up:
  - Next M5 priority item: tag release candidate.

## 2026-03-19 14:13:12 KST
- Task: M5 release candidate tagging (`0.5.0-rc.1`).
- Commit: HEAD (this run)
- Files: `ACTION_ITEMS.md`, `TASKS.md`, `logs/teams/qa.md`, `logs/teams/_summary.md`
- Verification:
  - `python3 scripts/validate_portals.py` ✅
  - `python3 scripts/regression_30min_loop_checklist.py` ✅
- Decisions:
  - Tagged current RC snapshot as `0.5.0-rc.1` to match launch changelog package.
  - Closed final unchecked M5 backlog item (`Tag release candidate`) in both trackers.
- Follow-up:
  - Next item: post-RC telemetry monitoring and bugfix hotlist only if new blockers are reported.

## 2026-03-19 15:14:28 KST
- Task: M5 sustain telemetry reporting hardening (week-over-week deltas + regression).
- Commit: HEAD (this run)
- Files: `scripts/economy_weekly_snapshot.py`, `scripts/regression_weekly_snapshot.py`, `logs/economy_weekly_snapshot.md`, `logs/economy_weekly_snapshot.json`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `python3 -m py_compile scripts/economy_weekly_snapshot.py scripts/regression_weekly_snapshot.py` ✅
  - `lua scripts/economy_anti_exploit_report.lua` ✅
  - `python3 scripts/economy_weekly_snapshot.py` ✅
  - `python3 scripts/regression_weekly_snapshot.py` ✅
- Decisions:
  - Added explicit regression coverage for weekly snapshot delta schema to guard sustain-report compatibility.
  - Kept anti-exploit gate in verification chain so weekly decision remains tied to suspicious-window count.
- Follow-up:
  - Next QA sustain check: include `scripts/regression_weekly_snapshot.py` in any future RC/sustain command matrix update.

## 2026-03-19 15:43:32 KST
- Task: M5 post-RC sustain - wire weekly snapshot delta regression into RC/sustain checklist matrix.
- Commit: HEAD (this run)
- Files: `logs/playtests/rc_checklist.md`, `scripts/regression_weekly_snapshot.py`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `python3 -m py_compile scripts/regression_weekly_snapshot.py scripts/economy_weekly_snapshot.py` ✅
  - `python3 scripts/regression_weekly_snapshot.py` ✅
- Decisions:
  - Added a dedicated Post-RC sustain guardrail row in RC checklist so weekly delta-schema regression stays in the standard command matrix.
  - Kept sustain verification bound to `scripts/regression_weekly_snapshot.py` to prevent snapshot format drift during weekly telemetry ops.
- Follow-up:
  - Next sustain priority: keep running weekly snapshot + delta regression and open rebalance work only when anti-exploit suspicious windows turn non-zero.

## 2026-03-19 16:13:40 KST
- Task: QA verification for weekly sustain one-command runner.
- Commit: HEAD (this run)
- Files checked: `scripts/run_weekly_sustain.sh`, `logs/playtests/rc_checklist.md`
- Verification:
  - `bash -n scripts/run_weekly_sustain.sh` ✅
  - `bash scripts/run_weekly_sustain.sh` ✅
- Decisions:
  - Sustain guardrail commands now have a single deterministic entrypoint for weekly ops while preserving direct regression command visibility in checklist.
  - No screenshot regen required (non-UI scripting/docs update only).
- Follow-up:
  - Validate scheduler integration once weekly automation wiring is added outside repo.

## 2026-03-19 16:44:20 KST
- Task: QA verification for weekly sustain scheduler wiring helper.
- Commit: HEAD (this run)
- Files checked: `scripts/install_weekly_sustain_cron.sh`, `logs/playtests/rc_checklist.md`, `logs/economy_weekly_snapshot.md`, `logs/economy_weekly_snapshot.json`
- Verification:
  - `bash -n scripts/install_weekly_sustain_cron.sh` ✅
  - `bash scripts/install_weekly_sustain_cron.sh` ✅ (dry-run; no crontab mutation)
  - `bash scripts/run_weekly_sustain.sh` ✅
- Decisions:
  - Dry-run output now provides auditable cron line preview + existing managed-entry status before apply.
  - Sustain checklist includes scheduler handoff row so operations can verify cron wiring path alongside telemetry regressions.
- Follow-up:
  - Validate `--apply` behavior in target runtime host change window before enabling unattended weekly cadence.

## 2026-03-19 17:13:53 KST
- Task: QA verification for weekly scheduler installer CLI regression coverage.
- Commit: HEAD (this run)
- Files checked: `scripts/regression_weekly_cron_installer.py`, `logs/playtests/rc_checklist.md`
- Verification:
  - `python3 -m py_compile scripts/regression_weekly_cron_installer.py` ✅
  - `python3 scripts/regression_weekly_cron_installer.py` ✅
- Decisions:
  - RC/sustain matrix now explicitly guards scheduler installer UX contract (dry-run evidence + input validation) with a single scripted regression.
  - No screenshot regen required (non-UI scripting/docs update only).
- Follow-up:
  - Keep regression green when installer options or marker format evolve.

## 2026-03-19 17:43:35 KST
- Task: M5 post-RC sustain - sync RC checklist sign-off rows with shipped tag evidence.
- Commit: HEAD (this run)
- Files checked: `logs/playtests/rc_checklist.md`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `git tag --list 0.5.0-rc.1` ✅
  - `git rev-parse --short 0.5.0-rc.1` ✅ (`d82cab1`)
- Decisions:
  - RC checklist sign-off rows now reflect completed lane approvals and release-tag existence.
  - Added explicit tag hash + KST timestamp in sign-off note for auditable closure context.
- Follow-up:
  - Next sustain item: monitor weekly runner outputs and only reopen RC checklist if blocker triage regresses.

## 2026-03-19 18:14:29 KST
- Task: QA verification for cron installer mocked apply-mode regression.
- Commit: HEAD (this run)
- Files checked: `scripts/install_weekly_sustain_cron.sh`, `scripts/regression_weekly_cron_installer.py`, `logs/playtests/rc_checklist.md`
- Verification:
  - `bash -n scripts/install_weekly_sustain_cron.sh` ✅
  - `python3 -m py_compile scripts/regression_weekly_cron_installer.py` ✅
  - `python3 scripts/regression_weekly_cron_installer.py` ✅
- Decisions:
  - Regression now validates dry-run/override/invalid-arg flows plus mocked `--apply` upsert semantics with single-marker guarantee.
  - Host crontab remains untouched during regression by injecting fake crontab binary + isolated state file.
- Follow-up:
  - Keep mocked-apply checks green when cron marker format or installer write path changes.

## 2026-03-19 18:43:17 KST
- Task: QA verification for weekly cron installer custom log-path override.
- Commit: HEAD (this run)
- Files checked: `scripts/install_weekly_sustain_cron.sh`, `scripts/regression_weekly_cron_installer.py`
- Verification:
  - `bash -n scripts/install_weekly_sustain_cron.sh` ✅
  - `python3 -m py_compile scripts/regression_weekly_cron_installer.py` ✅
  - `python3 scripts/regression_weekly_cron_installer.py` ✅
- Decisions:
  - Regression now asserts schedule override output also includes custom `--log-path` rendering.
  - Existing mocked `--apply` upsert safeguards remain green with single-marker guarantee.
- Follow-up:
  - Keep CLI regression tokens updated if cron command composition changes.

## 2026-03-19 19:15:15 KST
- Task: QA verification for weekly sustain cron log rotation guard + installer rendering updates.
- Commit: 01f471d
- Files checked: `scripts/rotate_log_if_needed.sh`, `scripts/install_weekly_sustain_cron.sh`, `scripts/regression_weekly_cron_installer.py`
- Verification:
  - `bash -n scripts/rotate_log_if_needed.sh` ✅
  - `bash -n scripts/install_weekly_sustain_cron.sh` ✅
  - `python3 -m py_compile scripts/regression_weekly_cron_installer.py` ✅
  - `python3 scripts/regression_weekly_cron_installer.py` ✅
  - Dry-run cron preview includes rotate helper command + max-size threshold token ✅
- Decisions:
  - Regression now enforces `--max-log-size-mb` positive-int validation and command rendering for rotate helper invocation.
  - Mocked `--apply` upsert coverage remains intact (single managed marker guarantee).
- Follow-up:
  - Add targeted regression for rotate helper file-rotation behavior under threshold/over-threshold fixtures.

## 2026-03-19 19:44:44 KST
- Task: QA verification for sustain-log rotated-file retention pruning.
- Commit: HEAD (this run)
- Files checked: `scripts/rotate_log_if_needed.sh`, `scripts/install_weekly_sustain_cron.sh`, `scripts/regression_weekly_cron_installer.py`, `scripts/regression_rotate_log_retention.py`, `logs/playtests/rc_checklist.md`
- Verification:
  - `bash -n scripts/rotate_log_if_needed.sh` ✅
  - `bash -n scripts/install_weekly_sustain_cron.sh` ✅
  - `python3 -m py_compile scripts/regression_weekly_cron_installer.py scripts/regression_rotate_log_retention.py` ✅
  - `python3 scripts/regression_weekly_cron_installer.py` ✅
  - `python3 scripts/regression_rotate_log_retention.py` ✅
  - Cron dry-run preview contains rotate+retention command (`... rotate_log_if_needed.sh /tmp/dotpio-weekly.log 12 4 ...`) ✅
- Decisions:
  - Regression coverage now includes repeated over-threshold rotation cycles and asserts keep-latest-N pruning outcome.
  - Installer CLI regression now validates `--retain-rotated-logs` rendering and non-negative integer validation.
- Follow-up:
  - Keep regression fixture sleep spacing if timestamp format/rotation granularity changes.

## 2026-03-19 20:15:40 KST
- Task: QA verification for age-based pruning on weekly sustain rotated logs.
- Commit: HEAD (this run)
- Files checked: `scripts/rotate_log_if_needed.sh`, `scripts/install_weekly_sustain_cron.sh`, `scripts/regression_weekly_cron_installer.py`, `scripts/regression_rotate_log_retention.py`
- Verification:
  - `bash -n scripts/rotate_log_if_needed.sh` ✅
  - `bash -n scripts/install_weekly_sustain_cron.sh` ✅
  - `python3 -m py_compile scripts/regression_weekly_cron_installer.py scripts/regression_rotate_log_retention.py` ✅
  - `python3 scripts/regression_weekly_cron_installer.py` ✅
  - `python3 scripts/regression_rotate_log_retention.py` ✅
  - Cron dry-run preview contains age token in rotate command (`... rotate_log_if_needed.sh /tmp/dotpio-weekly.log 12 4 14 ...`) ✅
- Decisions:
  - Age-prune regression mutates fixture mtime to assert stale rotated file deletion independent of size-triggered rotation path.
  - Installer regression now enforces explicit non-negative integer validation for `--max-rotated-age-days`.
- Follow-up:
  - Keep regression expected token in sync if rotate helper argument order changes.

## 2026-03-19 20:41:00 KST
- Task: QA verification for weekly sustain cron policy audit helper + regression.
- Commit: `0a0bd4d`
- Files checked: `scripts/audit_weekly_sustain_cron.sh`, `scripts/regression_weekly_cron_audit.py`, `scripts/regression_weekly_cron_installer.py`, `scripts/regression_rotate_log_retention.py`, `logs/playtests/rc_checklist.md`
- Verification:
  - `bash -n scripts/audit_weekly_sustain_cron.sh` ✅
  - `python3 -m py_compile scripts/regression_weekly_cron_audit.py scripts/regression_weekly_cron_installer.py scripts/regression_rotate_log_retention.py` ✅
  - `python3 scripts/regression_weekly_cron_audit.py` ✅
  - `python3 scripts/regression_weekly_cron_installer.py` ✅
  - `python3 scripts/regression_rotate_log_retention.py` ✅
  - `bash scripts/audit_weekly_sustain_cron.sh` ✅ expected error path when no managed marker exists in host crontab
- Decisions:
  - Audit regression now guards managed-entry parsing contract and missing-entry diagnostics without mutating host crontab state.
  - No portal validator run (no map/portal changes).
  - No screenshot regen (no UI rendering/copy/layout changes).
- Follow-up:
  - Keep audit parser regression fixtures aligned if managed cron command token order changes.

## 2026-03-19 21:14:52 KST
- Task: QA verification for weekly cron audit helper JSON output mode.
- Commit: HEAD (this run)
- Files checked: `scripts/audit_weekly_sustain_cron.sh`, `scripts/regression_weekly_cron_audit.py`, `scripts/regression_weekly_cron_installer.py`
- Verification:
  - `bash -n scripts/audit_weekly_sustain_cron.sh` ✅
  - `python3 -m py_compile scripts/regression_weekly_cron_audit.py` ✅
  - `python3 scripts/regression_weekly_cron_audit.py` ✅
  - `python3 scripts/regression_weekly_cron_installer.py` ✅
- Decisions:
  - JSON mode contract validated for parseable payload fields and numeric schedule/rotation values.
  - Unsupported output format now fails fast with explicit validation error text.
  - Missing managed-entry diagnostics remain unchanged and still covered.
- Follow-up:
  - Keep JSON payload keys stable to avoid breaking downstream automation parsers.

## 2026-03-19 21:31 KST
- Task: Verify P0 Enter->Action Menu primary build flow transition.
- Commit: HEAD (this run)
- Files checked: `src/inventory_ui.lua`, `scripts/regression_build_action_menu.lua`, `scripts/regression_build_preview_confirm.lua`
- Verification:
  - `lua scripts/regression_build_action_menu.lua` ✅
  - `lua scripts/regression_build_preview_confirm.lua` ✅
  - `lua scripts/regression_builder_srl_affordance.lua` ✅
  - `lua scripts/regression_action_menu_lock_reasons.lua` ✅
- Decisions:
  - Added dedicated regression coverage for folder action-menu build path to guard against re-centering on F9-only behavior.
  - No portal validator run (no map/portal changes).
- Follow-up:
  - Extend UI regression pack when `BUILDER.SRL` `USE` lock/guidance changes land.

## 2026-03-19 21:59 KST
- Task: Verify P0 `BUILDER.SRL` USE disable + build-only guidance.
- Commit: HEAD (this run)
- Files checked: `src/inventory_ui.lua`, `scripts/regression_action_menu_lock_reasons.lua`
- Verification:
  - `lua scripts/regression_action_menu_lock_reasons.lua` ✅
  - `lua scripts/regression_builder_srl_affordance.lua` ✅
  - `lua scripts/regression_build_action_menu.lua` ✅
- Decisions:
  - Regression now enforces that `USE` is disabled specifically for `BUILDER.SRL` and includes build-only path guidance.
  - No portal validator run (no map/portal edits).
  - No screenshot refresh required (copy/lock-state only, no layout change).
- Follow-up:
  - Add preview-copy assertion coverage when P0 build preview clarity pass lands.

## 2026-03-19 22:29:59 KST
- Task: Verify P0 build preview clarity pass (materials/SRL/expected category).
- Commit: HEAD (this run)
- Files checked: `src/inventory_ui.lua`, `scripts/regression_build_preview_clarity.lua`
- Verification:
  - `luac -p src/inventory_ui.lua scripts/regression_build_preview_clarity.lua scripts/regression_build_preview_confirm.lua scripts/regression_build_action_menu.lua` ✅
  - `lua scripts/regression_build_preview_clarity.lua` ✅
  - `lua scripts/regression_build_preview_confirm.lua` ✅
  - `lua scripts/regression_build_action_menu.lua` ✅
- Decisions:
  - Added dedicated regression guard to ensure build preview metadata always includes a non-empty expected output category.
  - Existing preview-confirm and action-menu build regressions remain green after dialog copy/layout change.
  - No portal validator run (no map/portal changes).
- Follow-up:
  - Keep extending preview assertions if expected-category policy gains rarity/confidence fields.

## 2026-03-19 22:58:37 KST
- Task: Verify map_07 addition and portal wiring.
- Commit: HEAD (this run)
- Files checked: `maps/map_06.lua`, `maps/map_07.lua`
- Verification:
  - `luac -p maps/map_06.lua maps/map_07.lua` ✅
  - `python3 scripts/validate_portals.py` ✅
  - `python3 scripts/regression_map_progression.py` ✅
- Decisions:
  - Portal validator remains green after adding seventh map and new cross-map portal pair.
  - Existing map_01~04 progression regression remains stable after post-RC map expansion.
- Follow-up:
  - Add dedicated map_05~07 path regression when more high-tier maps/archetypes are added.

## 2026-03-19 23:29:10 KST
- Task: QA verification for P1 enemy synergy archetypes (`warcaller`/`hunter`).
- Commit: HEAD (this run)
- Files checked: `src/enemy_ai.lua`, `src/entities.lua`, `scripts/regression_enemy_behavior_variants.lua`, `POST_RC_BACKLOG.md`
- Verification:
  - `lua scripts/regression_enemy_behavior_variants.lua` ✅
- Decisions:
  - Regression now covers roster expansion, hunter-without-warcaller baseline, hunter-with-warcaller buff activation, and warcaller ally-alert propagation.
  - No portal validator run required (map/portal files unchanged).
  - No screenshot regen required (no UI layout/copy change).
- Follow-up:
  - Keep synergy assertions in sync if archetype ranges/buff multipliers are retuned.

## 2026-03-19 23:47:05 KST
- Task: QA verification for mission variety pack vertical slice.
- Commit: HEAD (this run)
- Files checked: `src/run_missions.lua`, `main.lua`, `scripts/regression_mission_variety_pack.lua`
- Verification:
  - `luac -p src/run_missions.lua main.lua scripts/regression_run_missions.lua scripts/regression_unlock_flags.lua scripts/regression_run_summary.lua scripts/regression_mission_variety_pack.lua` ✅
  - `lua scripts/regression_run_missions.lua` ✅
  - `lua scripts/regression_unlock_flags.lua` ✅
  - `lua scripts/regression_run_summary.lua` ✅
  - `lua scripts/regression_mission_variety_pack.lua` ✅
- Decisions:
  - Legacy mission regressions remain green with rotating mission packs because first-cycle pack preserves baseline kill/pickup/build expectations.
  - New regression asserts objective catalog size floor (>=8), 4-pack rotation coverage, and inclusion of newly introduced search/inventory/build-2 variants.
  - No portal validator run required (map/portal files unchanged).
- Follow-up:
  - Add a future playtest assertion once mission rewards are attached (to verify streak/bonus economy side effects).

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
- Task: QA verification for P1 portal repositioning rules.
- Files checked: `maps/map_03.lua`, `maps/map_04.lua`, `maps/map_05.lua`, `maps/map_06.lua`, `maps/map_07.lua`
- Verification:
  - `luac -p maps/map_03.lua maps/map_04.lua maps/map_05.lua maps/map_06.lua maps/map_07.lua` ✅
  - `python3 scripts/validate_portals.py` ✅
  - `python3 scripts/regression_map_progression.py` ✅
- Decisions:
  - Portal target integrity/regression remains green after coordinate-only relocation.
  - No UI copy/layout changes; screenshot refresh not required.
- Follow-up: Keep regression_map_progression in sustain matrix as guard for future portal edits.

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

## 2026-03-20 02:26 KST — P2 stale-branch/report drift guardrail validated
- Added regression coverage: `scripts/regression_stale_branch_report_drift.py`.
- Validation set:
  - `python3 -m py_compile scripts/stale_branch_report_drift_check.py scripts/regression_stale_branch_report_drift.py`
  - `python3 scripts/regression_stale_branch_report_drift.py`
  - `python3 scripts/stale_branch_report_drift_check.py`
- Result: PASS, artifacts emitted under `logs/stale_branch_report_drift.{md,json}`.

## 2026-03-20 03:00 KST — P2 sustain dashboard JSON mode
- Validation set:
  - `python3 -m py_compile scripts/sustain_health_dashboard.py scripts/regression_sustain_health_dashboard.py`
  - `python3 scripts/regression_sustain_health_dashboard.py`
  - `bash scripts/run_weekly_sustain.sh`
- Result: PASS, emits `logs/sustain_health_dashboard.{md,json}` and preserves weekly sustain pipeline green state.

## 2026-03-20 03:29 KST — P2 sustain dashboard trend classification
- Validation set:
  - `python3 -m py_compile scripts/sustain_health_dashboard.py scripts/regression_sustain_health_dashboard.py`
  - `python3 scripts/regression_sustain_health_dashboard.py`
  - `bash scripts/run_weekly_sustain.sh`
- Result: PASS, trend field emitted in markdown/json while weekly sustain runner remains green.
