# Team Logs Summary

Last updated: 2026-03-18 (KST)

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
- Progress/report protocol: commit + verification + next task on each run.
