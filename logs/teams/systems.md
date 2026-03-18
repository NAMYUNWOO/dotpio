# Systems Team Log


## 2026-03-18 23:15:00 KST
- Task: M0 pickup flow baseline (`G` key on player tile) with world-item consume and inventory-capacity guard.
- Commit: HEAD (this run)
- Files: `main.lua`, `src/entities.lua`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification: `luac -p main.lua src/entities.lua` (pass)
- Decisions:
  - Added `Entities.itemAt()` + `Entities.removeItem()` to keep pickup logic centralized.
  - Implemented pickup in `love.keypressed` (`g`) and route status messaging through `InventoryUI.setStatus`.
  - On successful pickup, item is flagged collected and removed from entity list to prevent duplicate pickup.
- Follow-up:
  - Add HUD/help hint for `G:Pickup` (M0 UX item).
  - Add explicit regression scenario for drop→pickup count validation.

## 2026-03-19 00:45:22 KST
- Task: M0 starter build/disassemble loadout tuning pass.
- Commit: HEAD (this run)
- Files: `src/player.lua`, `scripts/regression_starter_loadout.lua`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `luac -p src/player.lua scripts/regression_starter_loadout.lua` ✅
  - `lua scripts/regression_starter_loadout.lua` ✅ (`[PASS] starter loadout regression validated (BUILDER.SRL=18)`)
  - `lua scripts/regression_drop_pickup.lua` ✅ (guard regression still passing)
- Decisions:
  - Starter loadout now seeds by default folders (`SCROLLS`/`POTIONS`/`WEAPONS`) instead of dumping all files into root.
  - Increased initial `BUILDER.SRL` reserve to 18 and broadened mixed-category seeds for stable multi-step build/disassemble smoke loops.
  - Added a dedicated regression script to validate starter folder population + SRL baseline after `Player.init`.
- Follow-up:
  - Next highest priority: M1 telemetry logging for build/disassemble input/output/SRL.

## 2026-03-19 01:14:09 KST
- Task: M1 economy telemetry logging for build/disassemble (input/output/SRL envelope).
- Commit: HEAD (this run)
- Files: `src/economy_telemetry.lua`, `src/inventory_ui.lua`, `scripts/regression_economy_telemetry.lua`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `luac -p src/inventory_ui.lua src/economy_telemetry.lua scripts/regression_economy_telemetry.lua` ✅
  - `lua scripts/regression_economy_telemetry.lua` ✅
  - `lua scripts/regression_starter_loadout.lua` ✅
  - `lua scripts/regression_drop_pickup.lua` ✅
- Decisions:
  - Introduced shared telemetry writer module (`src/economy_telemetry.lua`) to centralize NDJSON append behavior.
  - Build/disassemble now emit telemetry on lock/fail/success paths with consistent SRL envelope fields (`srlBefore`, `srlSpent`, `srlAfter`/`srlRequired`) plus input/output metadata.
  - Added regression coverage that validates telemetry row schema for both build and disassemble events.
- Follow-up:
  - Next M1 item: stack split (partial quantity split) interaction in inventory.

## 2026-03-19 01:46:07 KST
- Task: M1 stack split (partial quantity) interaction in inventory.
- Commit: 6819ccf
- Files: `src/inventory.lua`, `src/inventory_ui.lua`, `scripts/regression_split_stack.lua`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `luac -p src/inventory.lua src/inventory_ui.lua scripts/regression_split_stack.lua` ✅
  - `lua scripts/regression_split_stack.lua` ✅
  - `lua scripts/regression_economy_telemetry.lua` ✅
  - `lua scripts/regression_starter_loadout.lua` ✅
  - `lua scripts/regression_drop_pickup.lua` ✅
- Decisions:
  - Added `Inventory.splitStack(inv, node, splitCount)` as shared stack-split primitive with guardrails (stackable-only, 1 <= split < current stack).
  - Inventory action menu and quick keys now include `S` split flow to create sibling stacks without changing total item count.
  - Split dialog defaults to half-stack and surfaces valid range to reduce invalid input churn.
- Follow-up:
  - Next M1 item: build preview/confirm UX (consumed materials + SRL cost before execute).

## 2026-03-19 03:14:05 KST
- Task: M1 anti-exploit report (loop profit detection over N actions).
- Commit: HEAD (this run)
- Files: `src/economy_anti_exploit.lua`, `scripts/economy_anti_exploit_report.lua`, `scripts/regression_anti_exploit_report.lua`, `.gitignore`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `luac -p src/economy_anti_exploit.lua scripts/economy_anti_exploit_report.lua scripts/regression_anti_exploit_report.lua` ✅
  - `lua scripts/regression_anti_exploit_report.lua` ✅
  - `lua scripts/economy_anti_exploit_report.lua 20` ✅
  - `lua scripts/regression_economy_telemetry.lua` ✅
  - `lua scripts/regression_build_preview_confirm.lua` ✅
  - `lua scripts/regression_split_stack.lua` ✅
  - `lua scripts/regression_builder_srl_affordance.lua` ✅
- Decisions:
  - Added a sliding-window analyzer that flags suspicious loops when BUILDER.SRL is net-positive across N actions or flat with high output/input ratio.
  - Report generator now emits JSON + Markdown summaries and degrades gracefully when telemetry log is missing.
  - Ignored runtime telemetry/report artifacts in `.gitignore` to keep commits focused on source/docs.
- Follow-up:
  - Next M1 item: tune SRL cost curve for low-tier spam suppression.

## 2026-03-19 03:44:56 KST
- Task: M1 tune SRL cost curve for low-tier spam suppression.
- Commit: 242f0db
- Files: `src/inventory_ui.lua`, `scripts/regression_srl_cost_curve.lua`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `luac -p src/inventory_ui.lua scripts/regression_srl_cost_curve.lua` ✅
  - `lua scripts/regression_srl_cost_curve.lua` ✅
  - `lua scripts/regression_build_preview_confirm.lua` ✅
  - `lua scripts/regression_economy_telemetry.lua` ✅
  - `lua scripts/regression_anti_exploit_report.lua` ✅
- Decisions:
  - Reworked build SRL cost surcharges to scale with low average size + salvage-heavy compositions instead of only flat penalties.
  - Added two-step salvage-ratio surcharge and stronger low-tier surcharge to suppress cheap churn loops while keeping premium recipes in a lower cost band.
  - Added dedicated regression (`scripts/regression_srl_cost_curve.lua`) asserting low-tier spam fixtures remain expensive vs premium fixtures.
- Follow-up:
  - Next M1 item: tune salvage size/stack caps for fairness.

## 2026-03-19 04:13:17 KST
- Task: M1 tune salvage size/stack caps for fairness.
- Commit: HEAD (this run)
- Files: `src/ai_describe.lua`, `src/inventory_ui.lua`, `scripts/regression_disassembly_caps.lua`, `screenshots/screenshot-inventory-dos.png`, `screenshots/screenshot-map04.png`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `luac -p src/ai_describe.lua src/inventory_ui.lua scripts/regression_disassembly_caps.lua` ✅
  - `lua scripts/regression_disassembly_caps.lua` ✅
  - `lua scripts/regression_srl_cost_curve.lua` ✅
  - `lua scripts/regression_builder_srl_affordance.lua` ✅
  - `bash scripts/capture_screenshots.sh` ✅
- Decisions:
  - Replaced flat disassembly caps with size-tier fairness limits (tiny/medium/large => stack cap 1/2/3; budget scale 35%/45%/55%, clamped by `size-1`).
  - Added `AiDescribe.debugDisassemblyLimits` + dedicated regression to lock cap/budget expectations.
  - Updated help copy so disassembly constraints reflect tiered caps instead of stale fixed formulas.
- Follow-up:
  - Next M1 item: validate map_01~04 progression with portal validator + playtest checklist.
