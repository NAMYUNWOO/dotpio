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

## 2026-03-19 21:31 KST
- Task: P0 replace F9-centric build flow with Enter->Action Menu primary flow.
- Commit: HEAD (this run)
- Files: `src/inventory_ui.lua`, `scripts/regression_build_action_menu.lua`, `POST_RC_BACKLOG.md`
- Verification:
  - `lua scripts/regression_build_action_menu.lua` ✅
  - `lua scripts/regression_build_preview_confirm.lua` ✅
  - `lua scripts/regression_builder_srl_affordance.lua` ✅
  - `lua scripts/regression_action_menu_lock_reasons.lua` ✅
- Decisions:
  - Enter on folder rows now opens a folder action menu (`OPEN` / `BUILD`) instead of immediately entering the folder.
  - Build is now first-class in the folder menu via `B` quick action; preview/confirm gate remains unchanged for safe execution.
  - F9 remains as a shortcut, but help copy now points to Enter+B as primary build flow.
- Follow-up:
  - Next P0: hide/disable `USE` for `BUILDER.SRL` and provide explicit build-only guidance.

## 2026-03-19 21:59 KST
- Task: P0 hide/disable `USE` for `BUILDER.SRL` and provide explicit build-only guidance.
- Commit: HEAD (this run)
- Files: `src/inventory_ui.lua`, `scripts/regression_action_menu_lock_reasons.lua`, `POST_RC_BACKLOG.md`
- Verification:
  - `lua scripts/regression_action_menu_lock_reasons.lua` ✅
  - `lua scripts/regression_builder_srl_affordance.lua` ✅
  - `lua scripts/regression_build_action_menu.lua` ✅
- Decisions:
  - Action Menu now hard-disables `USE [U]` on `BUILDER.SRL` with inline lock copy directing players to `B` or `Enter->BUILD`.
  - Direct `U` quick-use on `BUILDER.SRL` is blocked with explicit build-only status guidance.
- Follow-up:
  - Next P0: build preview panel clarity pass (materials consumed, SRL, expected category).

## 2026-03-19 22:29:59 KST
- Task: P0 build preview panel clarity pass (materials consumed, SRL, expected category).
- Commit: HEAD (this run)
- Files: `src/inventory_ui.lua`, `scripts/regression_build_preview_clarity.lua`, `POST_RC_BACKLOG.md`
- Verification:
  - `luac -p src/inventory_ui.lua scripts/regression_build_preview_clarity.lua scripts/regression_build_preview_confirm.lua scripts/regression_build_action_menu.lua` ✅
  - `lua scripts/regression_build_preview_clarity.lua` ✅
  - `lua scripts/regression_build_preview_confirm.lua` ✅
  - `lua scripts/regression_build_action_menu.lua` ✅
- Decisions:
  - Build preview dialog now includes explicit `Expected category` line derived from constrained component-category mix.
  - Existing materials-consumed and SRL cost copy was retained; spacing updated to keep confirmation prompt readable.
- Follow-up:
  - Next P1 candidate: add map_07 with tactical pattern and portal integration.

### 2026-03-19 23:59 KST
- Task: Mission momentum bonus payout experiment (objective completion streak SRL micro-reward).
- Decision: Logged lane impact for streak-based reward model (1,1,2 SRL) with reward cap and no duplicate payout on already-complete objectives.
- Evidence: `src/run_missions.lua`, `main.lua`, `scripts/regression_mission_momentum.lua` (+ mission regressions).
- Follow-up: Monitor telemetry for early-run SRL inflation and tune reward curve if low-tier churn increases.

## 2026-03-20 00:26 KST — cross-lane sync note
- Context: World/System completed map_03~07 identity metadata + encounter rhythm profile wiring.
- Impact: No content schema break; existing flows remain stable with differentiated pacing.
- Follow-up: Validate player readability and portal landmark cues in upcoming portal reposition task.

## 2026-03-20 00:58 KST
- Cross-lane note: World portal reposition pass completed for map_03~07 with validator/regression green.
- Impact: traversal landmarks and fallback routes are clearer; no economy/combat/UI schema changes required in this patch.
- Follow-up: monitor playtest readability feedback and tune labels/cues if confusion persists.

## 2026-03-20 01:28:00 KST
- Task: P2 backlog item `Add weekly sustain audit JSON pretty mode`.
- Commit: HEAD (pending)
- Files:
  - `scripts/audit_weekly_sustain_cron.sh`
  - `scripts/regression_weekly_cron_audit.py`
  - `POST_RC_BACKLOG.md`
- Verification:
  - `python3 -m py_compile scripts/regression_weekly_cron_audit.py` ✅
  - `python3 scripts/regression_weekly_cron_audit.py` ✅
- Decisions:
  - Added `--pretty` flag for `--format json` to emit indented, human-readable audit payload while keeping compact JSON default stable.
  - Added guardrail: `--pretty` rejects non-JSON formats to avoid ambiguous output modes.
- Follow-up:
  - Next P2 priority: `Add sustain health dashboard markdown report`.

## 2026-03-20 01:59:00 KST
- Task: P2 backlog item `Add sustain health dashboard markdown report`.
- Commit: HEAD (pending)
- Files:
  - scripts/sustain_health_dashboard.py
  - scripts/regression_sustain_health_dashboard.py
  - scripts/run_weekly_sustain.sh
  - logs/playtests/rc_checklist.md
  - POST_RC_BACKLOG.md
  - logs/sustain_health_dashboard.md
- Verification:
  - `python3 -m py_compile scripts/sustain_health_dashboard.py scripts/regression_sustain_health_dashboard.py` ✅
  - `python3 scripts/regression_sustain_health_dashboard.py` ✅
  - `bash scripts/run_weekly_sustain.sh` ✅
- Decisions:
  - Weekly sustain runner now emits a single markdown dashboard rollup (economy safety, telemetry freshness, scheduler audit signal).
  - Dashboard consumes cron audit JSON when available and degrades gracefully to warning when managed cron entry is absent.
- Follow-up:
  - Next P2 priority: `Add automatic stale-branch/report drift check`.

## 2026-03-20 02:26 KST — P2 stale-branch/report drift guardrail handoff
- UX lane approved operator-facing copy style in drift report (`Status`, `Ahead/Behind`, per-report age days).
- Decision: preserve simple ok/warn wording to avoid ambiguity during weekly sustain triage.
- Follow-up: none.

## 2026-03-20 03:00 KST — P2 sustain dashboard JSON mode handoff
- UX lane approved output-mode UX: default markdown remains unchanged for existing workflow.
- Decision: explicit CLI error when `--pretty` is used without `--format json` for faster operator correction.
- Follow-up: none.

## 2026-03-20 03:29 KST — P2 sustain dashboard trend classification handoff
- UX lane approved plain-language trend labels over numeric scores.
- Decision: keep markdown phrasing concise (`Trend: **...**`) to reduce operator scan time.
- Follow-up: none.

## 2026-03-20 03:58 KST
- Task: Surface active mission pack id + momentum streak in mission HUD and run summary overlay.
- Files: `src/hud.lua`, `src/run_summary.lua`, `scripts/regression_run_summary.lua`, `POST_RC_BACKLOG.md`
- Verification:
  - `luac -p src/hud.lua src/run_summary.lua scripts/regression_run_summary.lua` ✅
  - `lua scripts/regression_run_summary.lua` ✅
- Decisions:
  - Mission panel now shows `PACK:<id> STREAK:<n>` under the mission header for in-run pacing feedback.
  - Run summary now includes the same metadata so players can correlate completion outcomes with the active mission pack.
- Follow-up:
  - If mission metadata expands, prioritize abbreviation to preserve DOS HUD readability.

## 2026-03-20 04:29 KST
- Task: Surface mission variety reward feedback in action status line.
- Commit: HEAD (this run)
- Files: `main.lua`
- Verification:
  - `luac -p main.lua` ✅
- Decisions:
  - Added inline suffix `[VARIETY +1]` to mission momentum status text (including bag-full path) to communicate why payout exceeded base curve.

## 2026-03-20 04:59 KST
- Task: UX clarity update for mission pacing context.
- Verification:
  - `lua scripts/regression_run_summary.lua` ✅
  - `lua scripts/regression_mission_variety_pack.lua` ✅
- Decisions:
  - Mission panel now shows `PACK/TAG/STREAK`; run summary includes `PACE` line for post-run readability.

## 2026-03-20 05:29 KST
- Cross-lane UX review: no HUD/menu copy updated in this patch.
- Decision: ship combat behavior first, then consider explicit desperation indicator/status text if playtests show surprise damage confusion.
- Follow-up: candidate backlog item for readability cue after combat telemetry review.

## 2026-03-20 05:44 KST
- Task: UX readability pass for berserker threat escalation.
- Files: `main.lua`, `src/hud.lua`
- Verification:
  - `luac -p main.lua src/hud.lua` ✅
- Decisions:
  - Added high-salience status line when visible berserker first enrages (`BERSERKER ENRAGED...`).
  - HUD now shows compact `Berserk: <n>` indicator to reduce surprise burst damage moments.
- Follow-up:
  - If playtests still show surprise hits, add a pre-lunge wind-up cue.
