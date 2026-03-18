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
