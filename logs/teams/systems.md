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
