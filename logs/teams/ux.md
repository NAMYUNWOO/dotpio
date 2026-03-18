# UX Team Log


## 2026-03-18 23:44:52 KST
- Task: M0 `G:Pickup` in-game hint surfacing (HUD + DOS help text).
- Commit: 3a6b206
- Files: `src/hud.lua`, `src/inventory_ui.lua`, `ACTION_ITEMS.md`, `TASKS.md`, `screenshots/screenshot-map04.png`, `screenshots/screenshot-inventory-dos.png`
- Verification:
  - `luac -p src/hud.lua src/inventory_ui.lua` ✅
  - `bash scripts/capture_screenshots.sh` ✅ (map + inventory screenshots regenerated)
- Decisions:
  - Added `G:Pickup` to realtime HUD controls so pickup affordance is visible outside inventory.
  - Added pickup key line to inventory help dialog for DOS-style key reference consistency.
- Follow-up:
  - Next M0 priority: add scripted regression scenario for drop -> pickup -> count validation.
