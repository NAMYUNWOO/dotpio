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

## 2026-03-19 05:13:00 KST
- Task: M1 scripted 30-minute loop checklist + pass artifact.
- Commit: HEAD (this run)
- Files: `scripts/regression_30min_loop_checklist.py`, `logs/playtests/loop_30min_checklist.md`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `python3 -m py_compile scripts/regression_30min_loop_checklist.py` ✅
  - `python3 scripts/regression_30min_loop_checklist.py` ✅ (`[PASS] 30-minute core loop checklist regression validated`)
- Decisions:
  - Added a single orchestrator regression that runs core-loop gates (starter loadout, build/disassemble telemetry, preview/confirm, SRL affordance, SRL curve, disassembly caps, anti-exploit, map progression).
  - The checklist now emits a durable playtest artifact at `logs/playtests/loop_30min_checklist.md` to track M1 momentum gate pass/fail in one place.
- Follow-up:
  - Next highest unchecked milestone item is M2 `Design and implement map_05 layout + portal links`.

## 2026-03-19 08:15:07 KST
- Task: M3 run mission prototype (3 objectives) with runtime progress tracking hooks.
- Commit: HEAD (this run)
- Files: `src/run_missions.lua`, `src/combat.lua`, `src/inventory_ui.lua`, `main.lua`, `scripts/regression_run_missions.lua`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `luac -p main.lua src/run_missions.lua src/combat.lua src/inventory_ui.lua scripts/regression_run_missions.lua` ✅
  - `lua scripts/regression_run_missions.lua` ✅
- Decisions:
  - Added run mission state module with 3 prototype objectives (`kills`, `pickup`, `build`) and clamped progress semantics.
  - Combat now exports kill deltas (`consumeKillCount`) so mission progression can track player eliminations without invasive enemy rewrites.
  - Inventory build flow exposes completion callback to increment mission progress only on successful AI build generation.
- Follow-up:
  - Next M3 item: add unlock flag framework for new build options.

## 2026-03-19 08:45:23 KST
- Task: M3 unlock flag framework for new build options.
- Commit: HEAD (this run)
- Files: `src/unlocks.lua`, `src/ai_describe.lua`, `main.lua`, `scripts/regression_unlock_flags.lua`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `luac -p main.lua src/ai_describe.lua src/unlocks.lua scripts/regression_unlock_flags.lua` ✅
  - `lua scripts/regression_build_category_diversity.lua` ✅
  - `lua scripts/regression_unlock_flags.lua` ✅
- Decisions:
  - Added shared unlock-state module with named flags and idempotent unlock semantics.
  - Build target category pool is now dynamic: baseline categories are always available, while `ring/wand/gem` unlock via `advanced_build_categories`.
  - AI build prompt now advertises only currently allowed target categories to keep generation aligned with unlocked progression.
- Follow-up:
  - Next M3 item: add fail-forward reward (currency/material carryover).

## 2026-03-19 09:13:50 KST
- Task: M3 fail-forward reward (currency/material carryover) on run reset.
- Commit: `90cdfa9`
- Files: `src/fail_forward.lua`, `main.lua`, `scripts/regression_fail_forward_rewards.lua`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `luac -p main.lua src/fail_forward.lua scripts/regression_fail_forward_rewards.lua` ✅
  - `lua scripts/regression_fail_forward_rewards.lua` ✅ (`[PASS] fail-forward reward regression validated`)
- Decisions:
  - Added a dedicated fail-forward module that computes capped carryover from run inventory + mission completion state (BUILDER.SRL/coin/gem).
  - Run reset (`R`) now snapshots carryover before inventory reset, applies rewards into starter folders on next run, and surfaces restart status copy.
  - Carryover is intentionally capped (SRL 8, coin 25, gem 3) to preserve anti-exploit economy constraints while still giving fail-forward momentum.
- Follow-up:
  - Next highest unchecked milestone item is M3 `Add summary screen for run result + unlock progress`.

## 2026-03-19 14:43:49 KST
- Task: M5 post-RC sustain - weekly SRL telemetry snapshot + rebalance decision log.
- Commit: HEAD (this run)
- Files: `scripts/economy_weekly_snapshot.py`, `logs/economy_weekly_snapshot.md`, `logs/economy_weekly_snapshot.json`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `python3 -m py_compile scripts/economy_weekly_snapshot.py` ✅
  - `lua scripts/economy_anti_exploit_report.lua` ✅
  - `python3 scripts/economy_weekly_snapshot.py` ✅
- Decisions:
  - Added weekly telemetry snapshot generator to summarize 7-day event/status/SRL spend metrics from ndjson economy logs.
  - Snapshot now records explicit rebalance decision (`NO_CURVE_CHANGE` vs `REBALANCE_REQUIRED`) using anti-exploit suspicious-window count as gate.
  - Current weekly decision is `NO_CURVE_CHANGE` (0 suspicious windows).
- Follow-up:
  - Next sustain item: schedule this snapshot in weekly cadence and revisit SRL curve only when suspicious windows become non-zero.

## 2026-03-19 15:14:28 KST
- Task: M5 post-RC sustain - add week-over-week delta signals to weekly SRL snapshot.
- Commit: HEAD (this run)
- Files: `scripts/economy_weekly_snapshot.py`, `scripts/regression_weekly_snapshot.py`, `logs/economy_weekly_snapshot.md`, `logs/economy_weekly_snapshot.json`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `python3 -m py_compile scripts/economy_weekly_snapshot.py scripts/regression_weekly_snapshot.py` ✅
  - `lua scripts/economy_anti_exploit_report.lua` ✅
  - `python3 scripts/economy_weekly_snapshot.py` ✅
  - `python3 scripts/regression_weekly_snapshot.py` ✅
- Decisions:
  - Weekly snapshot now supports CLI path overrides, enabling deterministic regression runs in temp outputs without mutating canonical artifacts.
  - Snapshot JSON/Markdown now include previous-snapshot comparison signals (event count + SRL spend deltas) for faster trend detection during sustain cadence.
  - Added schema regression that validates baseline (first run null deltas) and compare-mode (second run concrete deltas).
- Follow-up:
  - Next sustain task: wire this regression into any release/sustain checklist runner so weekly ops always gate on delta schema health.
