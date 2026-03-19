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
- Commit: ec0c770
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

## 2026-03-19 02:44:44 KST
- Task: M1 BUILDER.SRL affordance copy pass (action menu + F9 flow).
- Commit: HEAD (this run)
- Files: `src/inventory_ui.lua`, `scripts/regression_builder_srl_affordance.lua`, `screenshots/screenshot-map04.png`, `screenshots/screenshot-inventory-dos.png`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `luac -p src/inventory_ui.lua scripts/regression_builder_srl_affordance.lua` ✅
  - `lua scripts/regression_builder_srl_affordance.lua` ✅
  - `bash scripts/capture_screenshots.sh` ✅
- Decisions:
  - Action-menu disassemble labels and locked helper copy now spell out `BUILDER.SRL` explicitly (instead of generic `SRL`).
  - F9 affordance text, build preview dialog cost line, and status messages now consistently communicate `BUILDER.SRL` requirements.
  - Help dialog guidance updated so first-time users see `BUILDER.SRL` terminology on the build path.
- Follow-up:
  - Next UX item: keep build material consumption explicit in confirmation/status copy.

## 2026-03-19 08:15:07 KST
- Task: M3 mission checklist HUD prototype.
- Commit: HEAD (this run)
- Files: `src/hud.lua`, `main.lua`, `screenshots/screenshot-map04.png`, `screenshots/screenshot-inventory-dos.png`
- Verification:
  - `luac -p src/hud.lua main.lua` ✅
  - `bash scripts/capture_screenshots.sh` ✅
- Decisions:
  - Added always-visible mission panel with `RUN MISSIONS n/3` header and per-objective checklist rows (`[ ]/[x]`) to make meta goals readable during normal play.
  - Kept mission panel below base HP/MP HUD to avoid overlap with existing controls/help row and preserve DOS readability.
- Follow-up:
  - Fold unlock/progression affordance into this panel once M3 unlock flags land.

## 2026-03-19 08:45:23 KST
- Task: M3 unlock progression affordance pass in runtime HUD/status flow.
- Commit: HEAD (this run)
- Files: `src/hud.lua`, `main.lua`, `screenshots/screenshot-map04.png`, `screenshots/screenshot-inventory-dos.png`
- Verification:
  - `luac -p main.lua src/hud.lua` ✅
  - `bash scripts/capture_screenshots.sh` ✅
- Decisions:
  - Mission panel now includes explicit unlock row: `UNLOCK: ADVANCED SCHEMATICS [ON/OFF]`.
  - On first mission completion per run, status bar emits unlock confirmation copy for advanced build schematics.
- Follow-up:
  - Revisit panel height/content once M3 summary screen lands so mission+unlock info remains readable.

## 2026-03-19 09:44:22 KST
- Task: M3 run result summary screen + unlock progress overlay.
- Commit: HEAD (this run)
- Files: `main.lua`, `src/hud.lua`, `src/run_summary.lua`, `scripts/regression_run_summary.lua`, `screenshots/screenshot-map04.png`, `screenshots/screenshot-inventory-dos.png`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `luac -p main.lua src/hud.lua src/run_summary.lua scripts/regression_run_summary.lua` ✅
  - `lua scripts/regression_run_summary.lua` ✅
  - `lua scripts/regression_fail_forward_rewards.lua` ✅
  - `bash scripts/capture_screenshots.sh` ✅
- Decisions:
  - Pressing `R` now resets run state and opens a modal run summary with mission snapshot rows, unlock status, and carryover package details.
  - Summary snapshot is captured before mission reset so progress is preserved for review even after the new run starts.
  - Summary can be dismissed via `R`/`Enter`/`Esc` to keep keyboard-only UX flow intact.
- Follow-up:
  - Next UX priority: M4 DOS terminology consistency pass.

## 2026-03-19 10:13:54 KST
- Task: M4 DOS terminology consistency pass (Menu/Action/Drop/Disasm/Build) + explicit build material consumption copy.
- Commit: HEAD (this run)
- Files: `src/inventory_ui.lua`, `screenshots/screenshot-map04.png`, `screenshots/screenshot-inventory-dos.png`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `luac -p src/inventory_ui.lua main.lua` ✅
  - `lua scripts/regression_build_preview_confirm.lua` ✅
  - `lua scripts/regression_builder_srl_affordance.lua` ✅
  - `bash scripts/capture_screenshots.sh` ✅
- Decisions:
  - Standardized inventory copy to canonical DOS terms: `Action Menu`, `Disasm`, `Drop`, `Build` across help bar/dialog + action labels.
  - Build confirmation/status copy now explicitly names consumed materials (`USED: ...`) so build resource spending stays visible after execution.
- Follow-up:
  - Next M4 priority: add always-visible lock reason for all disabled actions.

## 2026-03-19 10:45:09 KST
- Task: M4 always-visible lock reason for disabled action-menu actions.
- Commit: HEAD (this run)
- Files: `src/inventory_ui.lua`, `scripts/regression_action_menu_lock_reasons.lua`, `screenshots/screenshot-map04.png`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `luac -p src/inventory_ui.lua scripts/regression_action_menu_lock_reasons.lua` ✅
  - `lua scripts/regression_action_menu_lock_reasons.lua` ✅
  - `lua scripts/regression_builder_srl_affordance.lua` ✅
  - `lua scripts/regression_build_preview_confirm.lua` ✅
  - `bash scripts/capture_screenshots.sh` ✅
- Decisions:
  - Disabled Action Menu rows now include inline lock-reason text (`[LOCK: ...]`) so users can read constraints without attempting activation.
  - Footer help now points users to inline lock reasons instead of generic disabled-state wording.
  - Added regression coverage to pin lock-reason visibility for USE/DISASM/SPLIT disabled states.
- Follow-up:
  - Next M4 priority: compact onboarding hint flow for first 5 minutes.

## 2026-03-19 11:14:50 KST
- Task: M4 compact onboarding hint flow for first 5 minutes.
- Commit: HEAD (this run)
- Files: `main.lua`, `src/hud.lua`, `src/onboarding_hints.lua`, `scripts/regression_onboarding_hints.lua`, `screenshots/screenshot-map04.png`, `screenshots/screenshot-inventory-dos.png`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `luac -p main.lua src/hud.lua src/onboarding_hints.lua scripts/regression_onboarding_hints.lua` ✅
  - `lua scripts/regression_onboarding_hints.lua` ✅
  - `lua scripts/regression_action_menu_lock_reasons.lua` ✅
  - `lua scripts/regression_builder_srl_affordance.lua` ✅
  - `lua scripts/regression_build_preview_confirm.lua` ✅
  - `bash scripts/capture_screenshots.sh` ✅
- Decisions:
  - Added a compact HUD onboarding strip that stays active only during the first 5 minutes and avoids mission-panel overlap.
  - Hint flow now advances by first interactions (move/search/pickup/inventory/build) and then rotates compact loop tips by elapsed time.
  - Hooked onboarding completion events from real gameplay interactions (lootbox search open, pickup success, inventory open, build completion).
- Follow-up:
  - Next M4 priority: keyboard-only usability pass checklist.

## 2026-03-19 11:43:49 KST
- Task: M4 keyboard-only usability pass checklist.
- Commit: HEAD (this run)
- Files: `scripts/regression_keyboard_shortcuts.lua`, `scripts/regression_keyboard_usability_checklist.py`, `logs/playtests/keyboard_only_usability_checklist.md`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `luac -p scripts/regression_keyboard_shortcuts.lua` ✅
  - `python3 -m py_compile scripts/regression_keyboard_usability_checklist.py` ✅
  - `lua scripts/regression_keyboard_shortcuts.lua` ✅
  - `python3 scripts/regression_keyboard_usability_checklist.py` ✅
- Decisions:
  - Added a keyboard-focused regression that guards inventory key branches and key-binding copy in help/action rows.
  - Added checklist artifact generator for scripted PASS/FAIL + manual keyboard-only smoke checklist under `logs/playtests/`.
- Follow-up:
  - Next M5 priority: create RC checklist document.

## 2026-03-19 13:43:27 KST
- Task: M5 launch screenshot refresh for RC packaging.
- Commit: HEAD (this run)
- Files: `screenshots/screenshot-map04.png`, `screenshots/screenshot-inventory-dos.png`, `CHANGELOG.md`
- Verification:
  - `bash scripts/capture_screenshots.sh` ✅
- Decisions:
  - Kept scripted capture route as single source for release screenshots to avoid drift.
  - Published launch-facing changelog notes in `CHANGELOG.md` aligned with current DOS UI/flow.
- Follow-up:
  - Next UX-related launch step: none blocking; proceed to RC tag.
