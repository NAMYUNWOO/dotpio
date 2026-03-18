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

## 2026-03-19 01:46:07 KST
- Task: M1 stack split UX pass (action menu + quick key + help text).
- Commit: 6819ccf
- Files: `src/inventory_ui.lua`, `screenshots/screenshot-map04.png`, `screenshots/screenshot-inventory-dos.png`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `luac -p src/inventory_ui.lua` ✅
  - `bash scripts/capture_screenshots.sh` ✅ (inventory/map screenshots refreshed)
- Decisions:
  - Added `SPLIT [S]` action with locked-state copy (`SPLIT N/A (need stack x2+)`) so stack constraints are visible in-menu.
  - Updated realtime help bar and help dialog quick-key legend to include `S` split affordance.
  - Split dialog now requests quantity with explicit valid range to keep DOS flow predictable.
- Follow-up:
  - Align upcoming build preview/confirm UX with the same lock-reason verbosity style.

## 2026-03-19 02:14:58 KST
- Task: M1 build preview/confirm UX for F9 flow (consumed parts + SRL cost before execute).
- Commit: HEAD (this run)
- Files: `src/inventory_ui.lua`, `scripts/regression_build_preview_confirm.lua`, `screenshots/screenshot-map04.png`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `luac -p src/inventory_ui.lua scripts/regression_build_preview_confirm.lua` ✅
  - `lua scripts/regression_build_preview_confirm.lua` ✅
  - `bash scripts/capture_screenshots.sh` ✅
- Decisions:
  - F9 now opens a dedicated build preview/confirm dialog instead of executing immediately.
  - Preview includes folder, planned component count, SRL have/need, and compact component summary for material visibility.
  - Cancel path returns to browsing with explicit `BUILD CANCELED` status.
- Follow-up:
  - Next M1 UX priority: make BUILDER.SRL affordance explicit in action menu + F9 flow copy.
