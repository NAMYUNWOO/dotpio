# Team Logs Summary

Last updated: 2026-03-19 (KST)

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
- Progress/report protocol: commit + verification + next task on each run.
