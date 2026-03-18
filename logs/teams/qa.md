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
