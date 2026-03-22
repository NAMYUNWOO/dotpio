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

## 2026-03-19 16:13:40 KST
- Task: M5 post-RC sustain - add one-command weekly sustain runner (anti-exploit + snapshot + regression).
- Commit: HEAD (this run)
- Files: `scripts/run_weekly_sustain.sh`, `logs/playtests/rc_checklist.md`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `bash -n scripts/run_weekly_sustain.sh` ✅
  - `bash scripts/run_weekly_sustain.sh` ✅
- Decisions:
  - Added executable sustain entrypoint that runs anti-exploit report refresh, weekly snapshot generation, and weekly delta regression in one command.
  - Updated RC sustain checklist to reference the one-command runner while retaining explicit regression row visibility.
- Follow-up:
  - Next sustain cadence item: wire `bash scripts/run_weekly_sustain.sh` into external weekly scheduler/cron environment and monitor decision drift.

## 2026-03-19 16:44:20 KST
- Task: M5 post-RC sustain - scheduler wiring helper for weekly sustain runner.
- Commit: HEAD (this run)
- Files: `scripts/install_weekly_sustain_cron.sh`, `logs/playtests/rc_checklist.md`, `logs/economy_weekly_snapshot.md`, `logs/economy_weekly_snapshot.json`, `ACTION_ITEMS.md`, `TASKS.md`, `logs/teams/_summary.md`
- Verification:
  - `bash -n scripts/install_weekly_sustain_cron.sh` ✅
  - `bash scripts/install_weekly_sustain_cron.sh` ✅ (dry-run preview)
  - `bash scripts/run_weekly_sustain.sh` ✅
- Decisions:
  - Added cron installer helper with managed marker (`DOTPIO_WEEKLY_SUSTAIN`) so weekly sustain scheduling can be upserted without manual crontab editing.
  - Default schedule is Monday 09:00 KST via `CRON_TZ=Asia/Seoul`, with CLI/env overrides for hour/minute/day.
  - RC checklist now includes scheduler dry-run command as a post-RC sustain guardrail.
- Follow-up:
  - Next sustain action: run installer with `--apply` on deployment host when weekly automation ownership is confirmed.

## 2026-03-19 17:13:53 KST
- Task: M5 post-RC sustain - add regression coverage for weekly scheduler installer CLI behavior.
- Commit: HEAD (this run)
- Files: `scripts/regression_weekly_cron_installer.py`, `logs/playtests/rc_checklist.md`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `python3 -m py_compile scripts/regression_weekly_cron_installer.py` ✅
  - `python3 scripts/regression_weekly_cron_installer.py` ✅
- Decisions:
  - Added deterministic regression coverage for cron installer dry-run output, CLI schedule override reflection, and invalid arg rejection.
  - Kept regression in no-mutation mode (no `--apply`) so CI/local validation can run safely without touching host crontab.
- Follow-up:
  - Run this regression in weekly sustain cadence alongside `scripts/run_weekly_sustain.sh` to detect installer CLI drift early.

## 2026-03-19 18:14:29 KST
- Task: M5 post-RC sustain - add safe apply-mode test hook for weekly cron installer.
- Commit: HEAD (this run)
- Files: `scripts/install_weekly_sustain_cron.sh`, `scripts/regression_weekly_cron_installer.py`, `logs/playtests/rc_checklist.md`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `bash -n scripts/install_weekly_sustain_cron.sh` ✅
  - `python3 -m py_compile scripts/regression_weekly_cron_installer.py` ✅
  - `python3 scripts/regression_weekly_cron_installer.py` ✅
- Decisions:
  - Installer now supports `CRONTAB_BIN` override so apply-mode behavior can be tested in sandbox/mocked environments without touching host crontab.
  - Apply path keeps managed-marker upsert semantics (replace existing marker entry, keep exactly one managed row).
- Follow-up:
  - Next sustain hardening candidate: expose optional `--log-path` override for multi-instance deployments sharing one repo clone.

## 2026-03-19 18:43:17 KST
- Task: M5 post-RC sustain - add optional cron log-path override for multi-instance deployments.
- Commit: HEAD (this run)
- Files: `scripts/install_weekly_sustain_cron.sh`, `scripts/regression_weekly_cron_installer.py`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `bash -n scripts/install_weekly_sustain_cron.sh` ✅
  - `python3 -m py_compile scripts/regression_weekly_cron_installer.py` ✅
  - `python3 scripts/regression_weekly_cron_installer.py` ✅
- Decisions:
  - Added `--log-path` CLI flag and `SUSTAIN_CRON_LOG_PATH` env override while preserving default `logs/weekly_sustain_cron.log` behavior.
  - Cron installer now supports per-deployment log sink routing without changing runner path or managed marker semantics.
- Follow-up:
  - Next sustain hardening candidate: optional log-rotation helper/check for long-lived cron logs.

## 2026-03-19 19:15:15 KST
- Task: M5 post-RC sustain - add size-based weekly sustain cron log rotation guard.
- Commit: 01f471d
- Files: `scripts/rotate_log_if_needed.sh`, `scripts/install_weekly_sustain_cron.sh`, `scripts/regression_weekly_cron_installer.py`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `bash -n scripts/rotate_log_if_needed.sh` ✅
  - `bash -n scripts/install_weekly_sustain_cron.sh` ✅
  - `python3 -m py_compile scripts/regression_weekly_cron_installer.py` ✅
  - `python3 scripts/regression_weekly_cron_installer.py` ✅
  - `bash scripts/install_weekly_sustain_cron.sh --minute 15 --hour 6 --dow 2 --tz UTC --log-path /tmp/dotpio-weekly.log --max-log-size-mb 12` (dry-run preview) ✅
- Decisions:
  - Added `scripts/rotate_log_if_needed.sh` as a pre-run guard that rotates the cron log once it reaches a configurable MB threshold.
  - Cron installer now wires `--max-log-size-mb` / `SUSTAIN_CRON_MAX_LOG_SIZE_MB` into the managed command to prevent unbounded sustain-log growth.
- Follow-up:
  - Consider retention pruning policy (e.g., keep latest N rotated files) if long-lived nodes accumulate many rotation artifacts.

## 2026-03-19 19:44:44 KST
- Task: M5 post-RC sustain - add rotated weekly sustain-log retention policy (keep-latest-N pruning + regression).
- Commit: HEAD (this run)
- Files: `scripts/rotate_log_if_needed.sh`, `scripts/install_weekly_sustain_cron.sh`, `scripts/regression_weekly_cron_installer.py`, `scripts/regression_rotate_log_retention.py`, `logs/playtests/rc_checklist.md`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `bash -n scripts/rotate_log_if_needed.sh` ✅
  - `bash -n scripts/install_weekly_sustain_cron.sh` ✅
  - `python3 -m py_compile scripts/regression_weekly_cron_installer.py scripts/regression_rotate_log_retention.py` ✅
  - `python3 scripts/regression_weekly_cron_installer.py` ✅
  - `python3 scripts/regression_rotate_log_retention.py` ✅
  - `bash scripts/install_weekly_sustain_cron.sh --minute 15 --hour 6 --dow 2 --tz UTC --log-path /tmp/dotpio-weekly.log --max-log-size-mb 12 --retain-rotated-logs 4` (dry-run preview) ✅
- Decisions:
  - Rotation helper now supports `retain-rotated` keep-latest-N pruning after each rotate event to prevent long-term rotated-log disk creep.
  - Cron installer now exposes `--retain-rotated-logs` / `SUSTAIN_CRON_RETAIN_ROTATED_LOGS` and wires retention into the managed schedule command.
- Follow-up:
  - Consider optional age-based retention (days) only if operators request time-window semantics beyond keep-latest-N.

## 2026-03-19 20:15:40 KST
- Task: M5 post-RC sustain - add optional max-age-days pruning window for rotated weekly sustain logs.
- Commit: HEAD (this run)
- Files: `scripts/rotate_log_if_needed.sh`, `scripts/install_weekly_sustain_cron.sh`, `scripts/regression_weekly_cron_installer.py`, `scripts/regression_rotate_log_retention.py`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `bash -n scripts/rotate_log_if_needed.sh` ✅
  - `bash -n scripts/install_weekly_sustain_cron.sh` ✅
  - `python3 -m py_compile scripts/regression_weekly_cron_installer.py scripts/regression_rotate_log_retention.py` ✅
  - `python3 scripts/regression_weekly_cron_installer.py` ✅
  - `python3 scripts/regression_rotate_log_retention.py` ✅
  - `bash scripts/install_weekly_sustain_cron.sh --minute 15 --hour 6 --dow 2 --tz UTC --log-path /tmp/dotpio-weekly.log --max-log-size-mb 12 --retain-rotated-logs 4 --max-rotated-age-days 14` (dry-run preview) ✅
- Decisions:
  - Rotation helper now accepts optional `max-age-days` and prunes stale rotated logs even when no new rotation occurs in the current run.
  - Cron installer now exposes `--max-rotated-age-days` / `SUSTAIN_CRON_MAX_ROTATED_AGE_DAYS` and wires the value into the managed rotation command.
  - Regression suite now covers CLI rendering/validation for age token and fixture-based stale-file pruning behavior.
- Follow-up:
  - Next sustain hardening candidate: add lightweight audit command to report current cron rotate policy from managed entry.

## 2026-03-19 20:41:00 KST
- Task: M5 post-RC sustain - add weekly cron policy audit command for managed DOTPIO entry introspection.
- Commit: `0a0bd4d`
- Files: `scripts/audit_weekly_sustain_cron.sh`, `scripts/regression_weekly_cron_audit.py`, `logs/playtests/rc_checklist.md`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `bash -n scripts/audit_weekly_sustain_cron.sh` ✅
  - `python3 -m py_compile scripts/regression_weekly_cron_audit.py` ✅
  - `python3 scripts/regression_weekly_cron_audit.py` ✅
  - `python3 scripts/regression_weekly_cron_installer.py` ✅
  - `python3 scripts/regression_rotate_log_retention.py` ✅
  - `bash scripts/install_weekly_sustain_cron.sh --minute 15 --hour 6 --dow 2 --tz UTC --log-path /tmp/dotpio-weekly.log --max-log-size-mb 12 --retain-rotated-logs 4 --max-rotated-age-days 14` ✅ (dry-run preview)
  - `bash scripts/audit_weekly_sustain_cron.sh` ✅ expected failure when managed entry is absent (`[ERROR] Managed weekly sustain entry not found ...`)
- Decisions:
  - Added an audit helper that reads `crontab -l`, enforces a single managed marker entry, and prints parsed schedule + rotate policy fields (`log_path`, `max_log_size_mb`, `retain_rotated_logs`, `max_rotated_age_days`) for operator visibility.
  - Added regression coverage for both parse success and managed-entry-missing failure path using an injected fake `crontab` binary.
  - Linked audit helper/regression into RC sustain checklist so weekly operations include policy introspection checks.
- Follow-up:
  - Next sustain hardening candidate: add optional JSON output mode for machine-readable audit ingestion.

## 2026-03-19 21:14:52 KST
- Task: M5 post-RC sustain - add machine-readable JSON output mode for weekly cron policy audit helper.
- Commit: HEAD (this run)
- Files: `scripts/audit_weekly_sustain_cron.sh`, `scripts/regression_weekly_cron_audit.py`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `bash -n scripts/audit_weekly_sustain_cron.sh` ✅
  - `python3 -m py_compile scripts/regression_weekly_cron_audit.py` ✅
  - `python3 scripts/regression_weekly_cron_audit.py` ✅
  - `python3 scripts/regression_weekly_cron_installer.py` ✅
- Decisions:
  - `scripts/audit_weekly_sustain_cron.sh` now supports `--format text|json` while preserving existing text output as default.
  - JSON mode emits a stable machine-readable payload (`status`, schedule fields, rotation policy fields, raw managed entry) for automation ingestion.
  - Regression coverage now asserts JSON success payload shape and invalid format rejection in addition to existing missing-entry failure handling.
- Follow-up:
  - Next sustain hardening candidate: add optional `--pretty` JSON formatting toggle for operator readability without changing default compact JSON.

## 2026-03-19 23:47:05 KST
- Task: P1 mission variety pack (+5 objective variants) minimal vertical slice.
- Commit: `HEAD (this run)`
- Files: `src/run_missions.lua`, `main.lua`, `scripts/regression_mission_variety_pack.lua`, `POST_RC_BACKLOG.md`, `ACTION_ITEMS.md`, `TASKS.md`
- Verification:
  - `luac -p src/run_missions.lua main.lua scripts/regression_run_missions.lua scripts/regression_unlock_flags.lua scripts/regression_run_summary.lua scripts/regression_mission_variety_pack.lua` ✅
  - `lua scripts/regression_run_missions.lua` ✅
  - `lua scripts/regression_unlock_flags.lua` ✅
  - `lua scripts/regression_run_summary.lua` ✅
  - `lua scripts/regression_mission_variety_pack.lua` ✅
- Decisions:
  - Reworked run missions from a fixed 3-objective prototype to rotating mission packs while keeping 3-visible-objective readability per run.
  - Added 5 new objective variants (`kills_5`, `pickup_4`, `build_2`, `search_2`, `inventory_3`) and event-key based progress tracking so multiple mission definitions can share gameplay triggers.
  - Wired new progress hooks for search completion and inventory-open events to support the new mission set without introducing new controls.
- Follow-up:
  - Next gameplay experiment candidate: objective-completion streak bonus (small BUILDER.SRL payout) to amplify mission momentum feedback.

### 2026-03-19 23:59 KST
- Task: Mission momentum bonus payout experiment (objective completion streak SRL micro-reward).
- Decision: Logged lane impact for streak-based reward model (1,1,2 SRL) with reward cap and no duplicate payout on already-complete objectives.
- Evidence: `src/run_missions.lua`, `main.lua`, `scripts/regression_mission_momentum.lua` (+ mission regressions).
- Follow-up: Monitor telemetry for early-run SRL inflation and tune reward curve if low-tier churn increases.

## 2026-03-20 00:26 KST — encounter profile plumbing for map identity
- Decision: Load optional `Map.metadata` from map files and let entity spawn consume `encounterProfile` for map-scoped pacing.
- Change: `src/entities.lua` now supports map-specific enemy count multiplier + variant bias weighting, with safe fallback when weights collapse.
- Verification: `lua scripts/regression_enemy_behavior_variants.lua` and profile regression passed.
- Follow-up: Revisit low/high multipliers after live telemetry snapshots.

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

## 2026-03-20 02:26 KST — P2 stale-branch/report drift guardrail
- Completed: automatic stale-branch/report drift check.
- Added `scripts/stale_branch_report_drift_check.py` to evaluate upstream drift (`ahead/behind`), branch commit age, and freshness of sustain artifacts.
- Decision: keep status as `ok|warn` (non-fatal) so weekly automation remains informative instead of brittle.
- Follow-up: consider escalating to hard fail in release-candidate-only pipeline if stale persists for >2 cycles.

## 2026-03-20 03:00 KST — P2 sustain dashboard JSON mode
- Completed: sustain health dashboard now emits structured JSON (`--format json`) with compact default and optional `--pretty` output.
- Decision: keep markdown as default surface; JSON is additive for automation and downstream parsing.
- Follow-up: if weekly governance expands, consume `logs/sustain_health_dashboard.json` in cross-repo monitoring.

## 2026-03-20 03:29 KST — P2 sustain dashboard trend classification
- Completed: added trend classifier (`improving|stable|degrading`) to sustain dashboard payload based on weekly deltas + economy safety signal.
- Decision: keep trend additive (non-gating) so existing GREEN/YELLOW/ORANGE/RED health scoring remains backward compatible.
- Follow-up: if trend remains degrading for >=2 cycles, consider auto-escalation in weekly ops policy.

## 2026-03-20 03:58 KST
- Task: P1 gameplay follow-up — expose mission pack id + momentum streak in mission HUD/run summary.
- Files: `src/hud.lua`, `src/run_summary.lua`, `scripts/regression_run_summary.lua`, `POST_RC_BACKLOG.md`
- Verification:
  - `luac -p src/hud.lua src/run_summary.lua scripts/regression_run_summary.lua scripts/regression_run_missions.lua` ✅
  - `lua scripts/regression_run_missions.lua` ✅
  - `lua scripts/regression_run_summary.lua` ✅
  - `lua scripts/regression_mission_momentum.lua` ✅
  - `lua scripts/regression_mission_variety_pack.lua` ✅
- Decisions:
  - Mission state metadata (`lastPackId`, `completionStreak`) is now surfaced directly in HUD and run summary to make run pacing legible.
  - Run summary snapshot now persists `missionPackId` + `momentumStreak` as durable context for post-run review.
- Follow-up:
  - Next gameplay experiment candidate: add mission-pack-specific bonus text/hints on objective completion.

## 2026-03-20 04:29 KST
- Task: P1 gameplay follow-up — mission momentum lane-switch variety bonus.
- Commit: HEAD (this run)
- Files: `src/run_missions.lua`, `main.lua`, `scripts/regression_mission_momentum.lua`, `POST_RC_BACKLOG.md`
- Verification:
  - `luac -p main.lua src/run_missions.lua scripts/regression_mission_momentum.lua` ✅
  - `lua scripts/regression_run_missions.lua` ✅
  - `lua scripts/regression_mission_momentum.lua` ✅
  - `lua scripts/regression_mission_variety_pack.lua` ✅
- Decisions:
  - Added a +1 BUILDER.SRL lane-switch variety bonus when consecutive completed objectives come from different mission lanes.
  - Kept original momentum curve (1/1/2) as base reward and layered variety bonus without changing objective progression logic.
- Follow-up:
  - Consider surfacing completion lane metadata in HUD if pacing telemetry needs deeper readability.

## 2026-03-20 04:59 KST
- Task: Injected/implemented new gameplay follow-up experiment — mission-pack flavor descriptors + HUD/run-summary tag surfacing.
- Files: `src/run_missions.lua`, `src/run_summary.lua`, `src/hud.lua`, `scripts/regression_run_summary.lua`, `scripts/regression_mission_variety_pack.lua`, `POST_RC_BACKLOG.md`
- Verification:
  - `luac -p src/run_missions.lua src/run_summary.lua src/hud.lua scripts/regression_run_summary.lua scripts/regression_mission_variety_pack.lua` ✅
  - `lua scripts/regression_run_summary.lua` ✅
  - `lua scripts/regression_run_missions.lua` ✅
  - `lua scripts/regression_mission_momentum.lua` ✅
  - `lua scripts/regression_mission_variety_pack.lua` ✅
- Decisions:
  - Mission pack rotation now carries stable flavor metadata (`flavorTag`, `flavorLabel`) alongside pack id.
  - HUD/run-summary now expose compact pacing context without changing reward/economy logic.
- Follow-up:
  - Consider mission-pack-specific bonus text hooks when objectives complete.

## 2026-03-20 05:29 KST
- Task: Combat experiment systems support for berserker desperation modifiers.
- Commit: HEAD (this run)
- Files: `src/enemy_ai.lua`, `src/entities.lua`
- Verification: `lua scripts/regression_enemy_behavior_variants.lua` ✅
- Decisions:
  - Enemy modifier refresh now composes synergy + desperation in one pass (`moveCd`, `atkCd`, `atkDmg`).
  - Added explicit base stat anchors (`baseAtkCd`) to avoid cumulative drift across updates.
- Follow-up: watch for low-HP burst overkill in early maps before increasing spawn chance.

## 2026-03-20 05:44 KST
- Task: Combat state-signal support for desperation readability slice.
- Commit: HEAD (this run)
- Files: `src/enemy_ai.lua`, `main.lua`
- Verification:
  - `luac -p src/enemy_ai.lua main.lua` ✅
  - `lua scripts/regression_enemy_behavior_variants.lua` ✅
- Decisions:
  - `syncCombatModifiers` now emits a transition-only `justEnteredDesperation` flag in addition to persistent `desperationActive`.
  - Runtime consumes and clears the flag after warning emission to avoid status spam.

## 2026-03-20 06:02 KST
- Task: Combat systems support for pre-lunge telegraph state machine.
- Files: `src/enemy_ai.lua`, `src/entities.lua`
- Verification: `lua scripts/regression_enemy_behavior_variants.lua` ✅
- Decisions:
  - Added deterministic berserker lunge window consumption helper (`consumeDesperationAttackWindow`).
  - Entities update now returns combat event counts (`hits`, `berserkerLungeTelegraphs`) for runtime consumers.

## 2026-03-20 06:30 KST — Enemy event plumbing update for recovery turns
- Decision: `Entities.update` now tracks `berserkerLungeRecoveries` event count alongside hit/telegraph events.
- Rationale: structured event output keeps combat telemetry/event consumers extensible.
- Follow-up: include recovery count in future combat telemetry snapshots if balancing requires data-driven tuning.

## 2026-03-20 06:58 KST — HUD berserker recovery counter readability slice
- No economy/system balance constants changed; combat readability-only slice confirmed no SRL loop impact.
- Follow-up: none.

## 2026-03-20 07:26 KST — Mission variety preview contract
- Decision: expose `nextVarietyLane` and `varietyBonusPreview` from `RunMissions.getState()` so HUD can surface upcoming lane-switch bonus without touching payout logic.
- Follow-up: if future packs add >3 lanes, keep hint as first unfinished alternate-lane objective for deterministic UI.

## 2026-03-20 07:56 KST — Mission variety mastery counter snapshot field
- Decision: added `varietyBonusCount` to mission runtime state and reset lifecycle to persist lane-switch mastery as a first-class stat.
- Implementation: increment only when lane-switch bonus payout triggers; expose through `RunMissions.getState()` for HUD/summary consumers.
- Verification: mission momentum + mission variety regressions PASS.

## 2026-03-20 08:28 KST — Combat pressure scoring policy
- Decision: introduced lightweight deterministic weighting model for berserker pressure readability (no economy/system balance impact).
- Follow-up: keep weights config-local until enough combat feedback warrants data-driven tuning.

## 2026-03-20 08:56 KST — No systems-economy delta
- This slice was HUD readability only; no SRL/economy logic changed.

## 2026-03-20 09:28 KST — Threat-tier color mapping helper
- Decision: added deterministic `HUD.getBerserkerThreatColor(score)` helper keyed by existing threat tiers to keep presentation logic centralized.
- System impact: UI-only; no SRL economy or mission payout changes.

## 2026-03-20 10:06 KST — Threat formula helper centralization
- Added reusable HUD helper methods (`getBerserkerThreatLegend`, `formatBerserkerThreatBreakdown`) to keep weighting semantics single-sourced.
- Scope remains presentation-only; no mission reward/economy constants touched.

## 2026-03-20 10:35 KST — Threat delta helper wiring
- Added deterministic HUD helpers for signed threat change (`getBerserkerThreatDelta`, `formatBerserkerThreatDelta`) so pacing signal math stays centralized/testable.
- Scope: presentation-only; no economy/progression constants changed.

## 2026-03-20 11:06 KST — Mission pressure-breaker dodge reward wiring
- Task: Systems/Combat mission-chain pressure breaker bonus.
- Decision: Reused `RunMissions.addProgress(..., context)` with `risingThreat` flag to emit deterministic `pressureBreakerDodgeCharge` reward metadata (1 charge).
- Implementation: `main.lua` now grants a short-lived dodge charge (6s TTL) when objective completion occurs during a rising-threat window.
- Follow-up: Keep charge value+TTL configurable if overclock room prototype also introduces burst survivability buffs.

## 2026-03-20 11:26 KST — Overclock hazard economy hook
- Task: Prototype SRL discount pulse in hazard room without changing baseline build-cost curve.
- Decision: Added `src/overclock_hazard.lua` and applied pulse-time discount through `src/inventory_ui.lua` build-cost plan hook (`OverclockHazard.applyBuildCost`).
- Balance guardrail: discount is temporary and floor-clamped (min build cost remains 1) to avoid zero-cost loops.

## 2026-03-20 12:01 KST — Weekly changelog drift detector rollout
- Completed backlog item: `QA/Systems: Add weekly changelog drift detector (code changes without corresponding team-log/report entry)`.
- Added `scripts/weekly_changelog_drift_check.py` + `scripts/regression_weekly_changelog_drift.py` and wired them into `scripts/run_weekly_sustain.sh` / RC sustain checklist.
- Verification: `python3 -m py_compile scripts/weekly_changelog_drift_check.py scripts/regression_weekly_changelog_drift.py`; `python3 scripts/regression_weekly_changelog_drift.py`; `bash scripts/run_weekly_sustain.sh`.
- Follow-up: next backlog priority is `Ops: Add sustain dashboard regression risk score (0~100) with threshold alert section`.

## 2026-03-20 13:05 KST
- Task: P2 Ops backlog — sustain dashboard regression risk score (0~100) + threshold alert section.
- Commit: HEAD (this run)
- Files: `scripts/sustain_health_dashboard.py`, `scripts/regression_sustain_health_dashboard.py`, `POST_RC_BACKLOG.md`
- Verification:
  - `python3 -m py_compile scripts/sustain_health_dashboard.py scripts/regression_sustain_health_dashboard.py` ✅
  - `python3 scripts/regression_sustain_health_dashboard.py` ✅
  - `bash scripts/run_weekly_sustain.sh` ✅
- Decisions:
  - Dashboard now emits `regressionRisk` payload with score/level/alert and fixed thresholds (`warnAt=30`, `alertAt=60`).
  - Markdown dashboard now includes a dedicated **Regression Risk** section with threshold alert status.
- Follow-up:
  - Backlog item marked done; queue next Game Director/Ops candidate.


## 2026-03-20 13:28 KST — Overclock hazard HUD countdown readability pass
- Decision: Overclock status hint now includes live seconds for active pulse (`OVERCLOCK HOT <n>s`) and cooldown (`OVERCLOCK CD <n>s`) to reduce timing ambiguity.
- Evidence: `lua scripts/regression_overclock_hazard.lua`; `luac -p src/overclock_hazard.lua`.
- Follow-up: Consider mirroring countdown near build preview panel for players who open inventory during hazard pulses.

## 2026-03-20 14:00 KST — Sustain dashboard regression-risk driver breakdown
- Decision: Added `regressionRisk.topDrivers` (top 3 contributors) to dashboard payload and markdown so ops reviews can immediately see what is driving score changes.
- Evidence: `python3 scripts/regression_sustain_health_dashboard.py`; `python3 scripts/sustain_health_dashboard.py --format json --pretty`.
- Follow-up: If risk repeatedly trends WARN/ALERT, add automated recommendation mapping each driver to a concrete remediation runbook step.

## 2026-03-20 14:29 KST — Risk score derivation for overclock hazards
- Added deterministic risk scoring from existing config values:
  - discount contribution: rounded `% * 10`
  - detect bonus contribution: integer detect bonus
  - movement pressure contribution: rounded `(1 - moveMul) * 10`
- Tier thresholds: LOW < 6, MED 6-9, HIGH >= 10.
- No gameplay balance knobs changed; display-only derivation.

## 2026-03-20 14:56 KST — overclock aggro-pressure legend follow-up
- Task: Add active-pulse HUD hint legend for overclock aggro pressure (`AGGRO DET:+n MOVE:+m%`).
- Decision: Keep mechanic unchanged; surface detect/move pressure explicitly in HOT hint for faster risk parsing.
- Evidence: `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua`; `lua scripts/regression_overclock_hazard.lua`.
- Follow-up: Observe readability during next map_07 playtest and adjust wording only if hint width becomes noisy.

## 2026-03-20 16:29 KST — Overclock warning scope decision
- Decision: Change is UI/readability-only; no economy/combat parameter adjustments.
- Follow-up: Keep hazard risk score formula unchanged to maintain telemetry continuity.

## 2026-03-20 16:55 KST — Overclock hot-zone kill bounty slice
- Task: Add pulse-capped overclock kill bounty reward to convert hazard combat pressure into immediate SRL upside.
- Decision: `OverclockHazard.consumeKillBonus(kills)` now awards `killBonusPerKill` SRL only while player is in-zone during active pulse, capped by `killBonusPulseCap` each pulse.
- Evidence: `luac -p main.lua src/overclock_hazard.lua maps/map_07.lua scripts/regression_overclock_hazard.lua`; `lua scripts/regression_overclock_hazard.lua`.
- Follow-up: Surface bounty cap progress (`BOUNTY:x/y`) in HOT hint for clearer reward budgeting.

## 2026-03-20 17:03 KST — Overclock HOT bounty progress token
- Task: Surface pulse-cap payout progress in HOT hint (`BOUNTY:x/y`) for overclock reward readability.
- Decision: Reuse `killBonusGrantedThisPulse` + `killBonusPulseCap` as canonical HUD token source to avoid duplicate counters/state drift.
- Evidence: `lua scripts/regression_overclock_hazard.lua`.
- Follow-up: If map variants need per-kill cap semantics later, keep HUD token as reward-units progress unless design explicitly requests kill-count mode.

## 2026-03-20 17:31 KST — Overclock next-pulse bounty budget readability
- Decision: READY/CD overclock HUD hints now include `NEXT BOUNTY:0/y` so players can pre-plan hot-zone reward windows before pulse activation.
- Scope: No combat/economy math changes; display-only hint extension around existing kill-bounty cap.
- Evidence: `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua` and `lua scripts/regression_overclock_hazard.lua` PASS.
- Follow-up: Add next Game Director experiment candidate (no unchecked backlog items remain).

## 2026-03-20 18:01 KST — Post-RC hazard readability wave 2: overclock risk-tier HUD color
- Task: Color-code overclock RISK tier token in HUD hint (LOW/MED/HIGH).
- Decision: Implemented tier-aware HUD color metadata from hazard module and threaded it through HUD auxiliary hint rendering with fallback color.
- Evidence: ; [PASS] overclock hazard regression validated.
- Follow-up: Queue next Post-RC gameplay/UX experiment candidate.

## 2026-03-20 18:31 KST — P1 hazard readability wave 3: overclock risk-factor breakdown token
- Task: Added compact HUD token "RISK SRC:Dx+DETy+MOVEz" across OVERCLOCK READY/HOT/CD hints.
- Decision: Expose risk component math (discount + detect + move) inline for fast tuning readability without changing hazard mechanics.
- Evidence: luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua; lua scripts/regression_overclock_hazard.lua (PASS).
- Follow-up: If HUD width pressure appears in smaller layouts, abbreviate token labels while keeping component values visible.

## 2026-03-20 19:03 KST — Overclock next-pulse ETA HUD token
- Task: Add `NEXT PULSE:<n>s` timing token to overclock READY/CD hint flow for clearer hazard re-entry planning.
- Scope: `src/overclock_hazard.lua`, `scripts/regression_overclock_hazard.lua`, backlog tracking docs.
- Verification: `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua` and `lua scripts/regression_overclock_hazard.lua` (PASS).
- Follow-up: pick next unchecked Post-RC gameplay readability experiment item.

## 2026-03-20 19:39 KST — Overclock pulse/recharge progress tokens
- Decision: Add explicit timing progress tokens to overclock HUD hints (`PULSE:%`, `RECHARGE:%`) to reduce cooldown timing guesswork.
- Scope: `src/overclock_hazard.lua`, `scripts/regression_overclock_hazard.lua`.
- Follow-up: Monitor whether compact line length remains readable at low resolutions.


## 2026-03-20 20:01 KST
- Task: P1 Hazard Readability Wave 6 - overclock risk-trend HUD token (RISK Δ:+n|-n).
- Decision: Kept risk-tier/score static and added state-aware delta signaling (+2 HOT, +1 IMMINENT in-zone cooldown, 0 otherwise) to preserve compact DOS readability.
- Evidence: `lua scripts/regression_overclock_hazard.lua` => PASS.
- Follow-up: Consider exposing token color metadata so RISK Δ can mirror rising/neutral/falling pressure semantics in a future wave.
## 2026-03-20 20:33 KST — P1 hazard readability wave 7: overclock zone-presence token
- Completed slice: added `ZONE:IN|OUT` token to overclock HUD hints (READY/HOT/CD/IMMINENT) for immediate hazard-context readability.
- Verification: `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua` and `lua scripts/regression_overclock_hazard.lua`.
- Follow-up: inject next Game Director experiment candidate (no unchecked backlog items remain).

## 2026-03-20 21:04:13 KST
- Task: Overclock hazard exposure-duration state tracking (`EXPOSED:<n>s`).
- Commit: HEAD (pending)
- Files: `src/overclock_hazard.lua`, `scripts/regression_overclock_hazard.lua`
- Verification:
  - `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua` ✅
  - `lua scripts/regression_overclock_hazard.lua` ✅
- Decisions:
  - Added `state.exposureSeconds` accumulator while player remains inside hazard rect.
  - Reset exposure to zero on zone exit to represent continuous commitment windows only.
  - Kept feature display-only (no economy/aggro parameter changes).
- Follow-up:
  - Continue validating no SRL loop impact in future hazard reward experiments.

## 2026-03-20 21:34 KST — Post-RC hazard readability wave 9 (`COMMIT` token)
- Completed item: overclock HUD hints now include `COMMIT:LOW|MID|HIGH` while player is in-zone (`ZONE:IN`), derived from continuous `EXPOSED` duration.
- Decision: commitment tier thresholds fixed at `LOW <5s`, `MID <12s`, `HIGH >=12s` for compact risk readability without tuning gameplay balance.
- Evidence: `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua` and `lua scripts/regression_overclock_hazard.lua` passed.
- Follow-up: if additional unchecked backlog item is needed next cycle, queue next hazard readability experiment candidate.

## 2026-03-20 22:01 KST — Post-RC hazard readability wave 10 follow-up (WINDOW token)
- Task: Add post-pulse relief burst token (`WINDOW:<n>s`) for out-of-zone cooldown readability.
- Scope: `src/overclock_hazard.lua`, `scripts/regression_overclock_hazard.lua`, `TASKS.md`, `POST_RC_BACKLOG.md`.
- Decision: Relief window now arms only when player disengages during HOT and pulse then expires while outside; token is shown only during out-of-zone cooldown and auto-expires.
- Evidence: `luac -p src/overclock_hazard.lua scripts/regression_overclock_hazard.lua`; `lua scripts/regression_overclock_hazard.lua` (PASS).
- Follow-up: Next unchecked backlog item is overclock dwell-bucket telemetry (`LOW|MID|HIGH`).

## 2026-03-20 22:35 KST — Overclock dwell-bucket telemetry shipped
- Task: Log overclock zone dwell buckets (`LOW|MID|HIGH`) per run for exposure-driven tuning evidence.
- Implemented runtime dwell accumulation in `src/overclock_hazard.lua` with threshold-aware split across LOW(<5s)/MID(<12s)/HIGH(>=12s).
- Added artifact writer `writeRunDwellArtifact()` emitting compact JSON/MD telemetry under `logs/playtests/`.
- Hooked run-reset flow to persist latest artifact (`logs/playtests/overclock_dwell_buckets_latest.{json,md}`).
- Follow-up: feed these buckets into weekly sustain dashboard once enough run samples accumulate.

## 2026-03-20 22:41 KST — Game Director slice: dwell snapshot plumbing
- Passed per-run dwell bucket snapshot (`LOW/MID/HIGH`) from `OverclockHazard` -> `RunSummary.open()`.
- Run reset now captures dwell snapshot before telemetry reset and persists latest artifact under `logs/playtests/overclock_dwell_buckets_latest.{json,md}`.

## 2026-03-20 23:03 KST — Overclock reward-efficiency token wired into run summary
- Added run-level overclock reward SRL telemetry in `src/overclock_hazard.lua` (`runRewardSrl`, `getRunRewardSrl`, reset semantics).
- `consumeKillBonus` now accumulates granted bounty into run telemetry for post-run efficiency analysis.
- Follow-up: use this token in multi-run trend combiner (next unchecked backlog item).

## 2026-03-20 23:33 KST — Multi-run overclock dwell trend combiner shipped
- Task: QA/Systems backlog item for balance-review cadence (`last N run medians`).
- Runtime change: run reset now persists timestamped dwell artifacts (`logs/playtests/overclock_dwell_buckets_run_YYYYmmdd_HHMMSS.{json,md}`) in addition to `latest`.
- Added combiner script `scripts/overclock_dwell_trend.py` to aggregate last-N run artifacts and emit median + exposure mix snapshot.
- Weekly sustain wiring: `scripts/run_weekly_sustain.sh` now generates dwell trend artifact (`--runs 7`) and runs dedicated regression.

## 2026-03-20 23:36 KST — Dwell-mix profile resolver added
- Added `resolveOverclockProfile(low, mid, high)` in `src/run_summary.lua`.
- Snapshot now carries `overclockProfile` alongside dwell and efficiency stats for post-run tuning coaching.
- Follow-up queued: trend-volatility token in multi-run combiner artifact.

## 2026-03-21 00:02 KST — P1 Game Director Cycle B follow-up: overclock dwell volatility token
- Task: Add trend-artifact volatility token (`VOL:STEADY|SWING`) for overclock dwell cadence triage.
- Scope: `scripts/overclock_dwell_trend.py`, `scripts/regression_overclock_dwell_trend.py`, `POST_RC_BACKLOG.md`.
- Decision: Classified volatility from run-to-run total-exposure relative deltas (`maxΔ>=45%` or `avgΔ>=30%` => `SWING`; else `STEADY`) to keep signal compact/reversible.
- Verification: `python3 -m py_compile scripts/overclock_dwell_trend.py scripts/regression_overclock_dwell_trend.py`; `python3 scripts/regression_overclock_dwell_trend.py`; `python3 scripts/overclock_dwell_trend.py --runs 3`.
- Follow-up: Remaining unchecked backlog item is `QA/UX Team: run-summary overclock analytics glossary row (DWELL/EFF/PROFILE)`.

## 2026-03-21 00:32 KST — Cross-lane sync: run-summary overclock glossary row
- Synced backlog closure: compact glossary row for run-summary analytics tokens (`DWELL`, `EFF`, `PROFILE`) is now shipped.
- Evidence: `scripts/regression_run_summary.lua` PASS + HUD syntax check PASS.
- No lane-specific balance/system behavior change; readability/documentation-only increment.

## 2026-03-21 00:36 KST — Game Director Cycle C: coach cue resolver shipped
- Implemented `resolveOverclockCoachTip(profile, exposure, reward)` in `src/run_summary.lua`.
- New snapshot field: `overclockCoachTip` derived from profile + SRL/exposure efficiency envelope.
- Follow-up systems experiments queued: threat-linked momentum scaler (backlog).

## 2026-03-21 01:04 KST — Threat-linked momentum scaler prototype (experiment flag)
- Task: Prototype lane-switch variety bonus scaler under HIGH berserker threat (`+1 -> +2`) behind flag.
- Decision: Added env-gated flag `DOTPIO_EXPERIMENT_THREAT_LINKED_VARIETY_SCALER=1` in `src/run_missions.lua`.
- Implementation: when lane-switch objective completes and context `threatTier == HIGH`, payout scales to `laneSwitchBonusSrl=2`; default behavior remains `+1`.
- Follow-up: collect telemetry on payout frequency before considering default enable.

## 2026-03-21 01:34 KST — Overclock route-tag API surfaced for HUD consumption
- Added `getRouteTag`, `getRouteCallout`, `getRouteCalloutColor` in `src/overclock_hazard.lua`.
- Validation guardrails: only `SAFE|RISK|SPIKE` accepted; invalid/missing metadata resolves to nil.
- Keeps route messaging data-driven from map metadata.

## 2026-03-21 02:06 KST — Portal transition confirmation state + route preview token
- Reworked `src/portal.lua` flow from immediate warp to pending transition state.
- Added target-map route-tag resolver (metadata-driven with cache) and prompt token formatter: `NEXT ROUTE:<tag>`.
- Confirm/cancel API added (`confirmTransition`, `cancelTransition`) to keep transition behavior explicit and reversible.

## 2026-03-21 02:31 KST — Route-tag distribution checker shipped
- Added `src/route_tag_distribution.lua` analyzer to audit hazard-map `routeTag` coverage (`SAFE|RISK|SPIKE`).
- Added runner `scripts/check_route_tag_distribution.lua` writing artifacts:
  - `logs/playtests/route_tag_distribution.md`
  - `logs/playtests/route_tag_distribution.json`
- Decision: checker warns (does not hard-fail) when all hazard-enabled maps converge to one profile.

## 2026-03-21 03:06 KST — Route-tag density ledger artifact shipped
- Added `src/route_tag_density_ledger.lua` to compute portal-graph BFS depth buckets per start map.
- Counts `SAFE|RISK|SPIKE` tags by reachable depth and records per-depth reachable map roster.
- Added runner `scripts/check_route_tag_density_ledger.lua` emitting `logs/playtests/route_tag_density_ledger.{md,json}` for cadence review.

## 2026-03-21 03:35 KST — Game Director Cycle F systems note
- Candidate slate generated after full backlog closure (low/mid/high risk).
- Injected follow-up systems experiment: `PRESSURE:<n>` token derived from route tag + current threat tier (left queued as next unchecked item).
- No systems-balance mutation shipped in this slice; transition behavior remains display-only fallback mode.

## 2026-03-21 03:36 KST — Cycle G systems slice: transition pressure token
- Implemented route-pressure score plumbing in `src/portal.lua`.
- Formula: `PRESSURE = routeBase + threatOffset` (SAFE/RISK/SPIKE => 1/2/3, LOW/MED/HIGH => +0/+1/+2, clamp 1..5).
- `Portal.getTransitionPrompt(maxChars, context)` now accepts threat-tier context for deterministic prompt output.
- Compact fallback now carries pressure as `P:<n>` to preserve signal under tight copy budgets.

## 2026-03-21 04:12 KST — Portal transition prompt token-order linter + budget parser
- Task: QA/Design backlog closure for transition prompt readability order enforcement.
- Scope touched:
  - `src/portal_prompt_linter.lua`
  - `scripts/check_portal_prompt_token_order.lua`
  - `scripts/regression_portal_prompt_token_order.lua`
  - `POST_RC_BACKLOG.md`
- Decision: enforce prompt semantic order `ACTION -> ROUTE -> COACH -> PRESSURE` in sampled portal prompt variants and verify budget-selection behavior at configurable char limits.
- Verification: `luac -p src/portal_prompt_linter.lua scripts/check_portal_prompt_token_order.lua scripts/regression_portal_prompt_token_order.lua`, `lua scripts/regression_portal_prompt_token_order.lua`, `lua scripts/check_portal_prompt_token_order.lua`.
- Follow-up: next unchecked item is adaptive portal hint prototype (`ALT ROUTE:<SAFE|RISK|SPIKE>`).

## 2026-03-21 04:34 KST — Cycle H adaptive portal pressure-delta slice
- Decision: extend transition prompt guidance with `ALT DELTA:-n` so players can quantify expected pressure drop before jump.
- Implementation: portal pressure delta now compares current route pressure vs adaptive alternative under same threat tier (`src/portal.lua`).
- Verification: `lua scripts/regression_portal_route_preview.lua`, `lua scripts/regression_portal_prompt_compact_mode.lua`, `lua scripts/regression_portal_prompt_token_order.lua` (PASS).
- Follow-up: implement ALT selector v2 using reachable portal graph for true lowest-pressure branch suggestions.

## 2026-03-21 05:04 KST — Cycle H follow-up: route-aware ALT selector v2
- Completed backlog item: choose adaptive `ALT ROUTE` from lowest-pressure reachable portal branch on current map (not fixed one-step downgrade).
- Verification: [PASS] portal route preview transition prompt regression validated, [PASS] portal prompt compact-mode regression validated, [PASS] portal prompt token-order regression validated, [PASS] portal adaptive ALT selector v2 regression validated (all PASS).
- Follow-up: keep `QA/UX Team: portal prompt readability regression for adaptive ALT token budget/order under HIGH threat compact mode` as next unchecked priority.

## 2026-03-21 05:33 KST — Portal adaptive ALT compact-readability regression
- Decision: Added dedicated regression `scripts/regression_portal_prompt_adaptive_alt_readability.lua` to validate HIGH-threat compact prompt budget + token order with adaptive ALT tokens (`ALT`, `ADEL`).
- Evidence: `lua scripts/regression_portal_prompt_adaptive_alt_readability.lua` PASS, plus companion prompt regressions PASS.
- Follow-up: Keep this regression in portal readability validation set for future prompt-token changes.

## 2026-03-21 05:38 KST — Game Director Cycle I: ALT PLAN nudge experiment
- Ideas generated: (1) adaptive portal ALT PLAN nudge token (low-risk UX), (2) overclock retreat streak bonus (mid-risk systems), (3) portal readability drift digest automation (high-risk ops novelty).
- Selected experiment: (1) adaptive portal ALT PLAN nudge token for HIGH-pressure transitions.
- Implementation: Added experiment-flagged prompt token in `src/portal.lua` (`ALT PLAN:LOWER RISK` detailed / `AP:LOW` compact) gated by `DOTPIO_EXPERIMENT_ALT_PLAN_NUDGE`.
- Verification: `lua scripts/regression_portal_prompt_adaptive_alt_readability.lua`, `DOTPIO_EXPERIMENT_ALT_PLAN_NUDGE=1 lua scripts/regression_portal_alt_plan_nudge.lua`, `lua scripts/regression_portal_prompt_compact_mode.lua`, `lua scripts/regression_portal_prompt_token_order.lua`.
- Follow-up: Monitor readability impact in playtests before promoting flag default.

## 2026-03-21 06:03 KST
- Task: Prototype overclock retreat streak bonus (+1 temporary dodge after 2 consecutive safe disengages).
- Decision: Added retreat streak state machine in `src/overclock_hazard.lua` (`retreatDisengagePending`, `retreatStreak`) and bonus emit event `retreatStreakBonusDodgeCharges=1` on second consecutive safe pulse disengage.
- Follow-up: Keep bonus isolated to overclock pulse expiry-outside-zone path; no reward if player re-enters before expiry.
## 2026-03-21 06:33 KST — Weekly portal prompt readability drift digest shipped
- Completed support for weekly digest artifact: `logs/weekly_portal_prompt_readability_drift.{md,json}` via `scripts/weekly_portal_prompt_readability_drift.py`.
- Added regression coverage: `scripts/regression_weekly_portal_prompt_readability_drift.py`.
- Weekly sustain runner now executes digest + regression and reports generated artifacts.
- Verification: `python3 -m py_compile ...`, digest regression PASS, `bash scripts/run_weekly_sustain.sh` PASS.
- Follow-up: use digest trend in upcoming Game Director readability tuning cycles.

## 2026-03-21 06:36 KST — Game Director Cycle J slice (mode-trend token)
- Idea slate generated (low/mid/high risk); selected low-risk readability slice.
- Added `MODE TREND` token to weekly portal prompt drift digest (`COMPACT|DETAILED|BALANCED`).
- Artifacts/regression remain green after update.
- Follow-ups kept in backlog: pressure-band drift token, top-token movers section.


## 2026-03-21 07:01 KST — Game Director Cycle J slice (pressure-band drift token)
- Task: Implement backlog item `PRESSURE BAND:LOW|MID|HIGH` for weekly portal prompt readability digest.
- Decision: Extended `scripts/weekly_portal_prompt_readability_drift.py` to aggregate pressure-token edits (`PRESSURE:` + `P:`) and map net drift to `pressureBand` thresholds (LOW <3, MID 3~7, HIGH >=8 by |net|).
- Evidence: Digest artifacts now include JSON `pressureBand` + `pressureEdits` and markdown line `PRESSURE BAND` with +/-/net counts.
- Verification: `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py`; `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`; `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 14 --max-commits 200`.
- Follow-up: Remaining Cycle J item is top-token movers section for digest triage.

## 2026-03-21 07:44 KST — Cycle J follow-up: digest top-token movers shipped
- Completed backlog item: `Design/QA Team: Add digest top-token movers section (largest net ± token deltas) for readability triage`.
- Added per-token edit aggregation (`added/removed/net`) and top-movers ranking in weekly digest outputs.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` and `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 14 --max-commits 200` PASS.
- Follow-up: no unchecked items remain in ACTION_ITEMS/TASKS/POST_RC; next cycle should inject new Game Director experiments.

## 2026-03-21 08:03 KST — Game Director Cycle K slice: weekly drift-risk token
- Completed backlog item: `QA/UX Team: Add digest drift-risk token (DRIFT RISK:LOW|MID|HIGH)`.
- Durable decisions:
  - Added `drift_risk_from_signals` classifier in `scripts/weekly_portal_prompt_readability_drift.py` using compact-vs-detailed net imbalance plus pressure-token churn.
  - Weekly digest JSON now exposes `driftRisk` + `driftRiskSignals` (`score`, `imbalance`, `pressureChurn`).
  - Weekly digest markdown now surfaces compact triage line: `DRIFT RISK: <level>`.
- Verification set (PASS):
  - `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 14 --max-commits 200`
- Follow-up:
  - Remaining Cycle K backlog items: `STICKY TOKENS` persistence token, `FOCUS` lane-focus token.

## 2026-03-21 08:31 KST — Sticky token persistence digest metric
- Task: Added `stickyTokens` aggregate in weekly portal prompt readability drift digest.
- Decision: Define sticky token as token with both added>0 and removed>0 over window.
- Evidence: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` PASS; digest regenerated.
- Follow-up: Implement lane-focus routing token from top mover families.

## 2026-03-21 09:03 KST — Cycle L route-action token vertical slice
- Ideas generated:
  1) Low-risk UX: add digest route-action token (`ROUTE ACTION:*`) from `FOCUS + DRIFT RISK`.
  2) Mid-risk systems: add lane-focus streak metric across windows (`FOCUS STREAK:<n>`).
  3) High-risk novelty: add lane-focus transition handoff token (`FOCUS SHIFT:<FROM->TO>`).
- Chosen experiment: idea #1 (minimal reversible vertical slice).
- Shipped: weekly digest now emits `routeAction` + `routeActionReason` in JSON and `ROUTE ACTION` line in markdown.
- Verification: py_compile PASS, digest regression PASS, live digest regeneration PASS.
- Follow-up: backlog carries remaining Cycle L items (focus streak, focus shift).
## 2026-03-21 09:35 KST — Cycle L close + Cycle M vertical slice
- Completed: Weekly portal prompt digest now includes `FOCUS STREAK:<n>` and `FOCUS SHIFT:<FROM->TO>` signals, then Game Director Cycle M experiment `FOCUS VOL:STEADY|SWING`.
- Decision: Define volatility from non-mixed lane-focus commit sequence switch ratio (`switches/edges`), with `SWING` threshold `>= 0.4`.
- Evidence: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` and `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120`.
- Follow-up: Cycle M backlog keeps `ACTION CONF` + `ANOMALY` items open.

## 2026-03-21 09:36 KST — Cycle M follow-up: route-action confidence scoring
- Task: Add route-action confidence token (`ACTION CONF:LOW|MID|HIGH`) derived from lane-focus dominance + drift spread.
- Implementation:
  - Added `route_action_confidence_from_signals(...)` in `scripts/weekly_portal_prompt_readability_drift.py`.
  - JSON now emits `routeActionConfidence` + `routeActionConfidenceSignals` (`topScore`, `secondScore`, `totalScore`, `dominanceRatio`, `focusSpread`, `driftSpread`).
  - Markdown digest now includes `ACTION CONF` line for operator triage.
- Verification:
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120`
- Commit: `1067216`
- Follow-up: anomaly pulse remains open; consider confidence-tiered anomaly state before enabling hard alerting.
## 2026-03-21 10:03 KST — Cycle M anomaly pulse prototype
- Completed: Added weekly digest anomaly pulse token `ANOMALY:ON|OFF` driven by simultaneous sticky-token and pressure-churn spikes.
- Decision: Use conservative trigger (`sticky >= 3` and `pressureChurn >= 5`) and expose thresholds/signals in JSON + markdown for auditability.
- Evidence: `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py`; `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`; `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120`.
- Follow-up: Next highest open item is Cycle N `ANOMALY CONF` tiering to reduce binary alert noise.

## 2026-03-21 10:33 KST — Digest anomaly confidence tiering
- Completed: anomaly classifier now returns pulse + confidence + richer diagnostics.
- Signals added: `stickyMet`, `pressureMet`, `triggerCount`, `stickyGap`, `pressureGap`, `combinedGap`.
- Rule: `HIGH` requires dual-threshold spike with strong overrun; `MID` for moderate dual-threshold or strong single-threshold pressure; else `LOW`.
- Follow-up: lane-lock persistence alert remains open.

## 2026-03-21 11:03 KST — Cycle N follow-up: lane-lock alert token
- Completed backlog item: Add digest lane-lock alert token (LANE LOCK:<lane>x<n>) for prolonged single-lane drift streaks.
- Implementation: scripts/weekly_portal_prompt_readability_drift.py now emits JSON laneLock/laneLockSignals and markdown LANE LOCK line (NONE when threshold not met; <LANE>x<STREAK> when armed).
- Verification: python3 scripts/regression_weekly_portal_prompt_readability_drift.py and weekly digest generation both PASS.
- Follow-up: ACTION_ITEMS/TASKS/POST_RC_BACKLOG now fully checked; next cycle should run Game Director review loop with new experiment injection.

## 2026-03-21 11:31 KST — Cycle O drift-momentum digest slice
- Completed: Added weekly digest token `DRIFT MOMENTUM:RISING|COOLING|FLAT` comparing older-vs-recent commit-window drift scores.
- Evidence: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`, `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120`.
- Follow-up: Evaluate unchecked Cycle O items (ACTION GUARD, FOCUS ENTROPY) next.

## 2026-03-21 12:03 KST — Cycle O follow-up: action guardrail token
- Added route-action guardrail resolver in weekly portal prompt digest.
- Rule: `ACTION GUARD:LOCK` only when `DRIFT RISK=HIGH` and `ACTION CONF=LOW`; otherwise `SOFT`.
- Signals persisted for auditability: `armed`, `reason`, `driftRisk`, `actionConfidence`.
- Follow-up: implement remaining Cycle O entropy token to close lane-spread visibility gap.

## 2026-03-21 12:31 KST — Cycle O close + Cycle P injection (autonomous)
- Completed: Added `FOCUS ENTROPY:LOW|MID|HIGH` token derived from normalized lane-score entropy in weekly portal prompt digest.
- Game Director review cycle:
  1) Low-risk UX idea: `FOCUS BAL:<n>%` lane-dominance readability token.
  2) Mid-risk systems idea: `PRESSURE LAG:FAST|STABLE|SLOW` from pressure churn vs drift momentum.
  3) High-risk novelty idea: `ROUTE SANDBOX:ON` experiment gate when sustained lane lock appears.
- Selected experiment: low-risk `FOCUS BAL:<n>%`.
- Implemented vertical slice: digest JSON/markdown now emits `focusBalance` + `focusBalanceSignals` and markdown `FOCUS BAL` line.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` PASS; `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120` PASS.
- Follow-up: Next queued items remain `PRESSURE LAG` and `ROUTE SANDBOX` in TASKS/POST_RC backlog (Cycle P).

## 2026-03-21 13:03 KST — Cycle P pressure-lag digest token
- Completed Post-RC Cycle P item: `PRESSURE LAG:FAST|STABLE|SLOW` in weekly portal prompt readability digest.
- Verification: `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py`; `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`; `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120 --out-json logs/weekly_portal_prompt_readability_drift.json --out-md logs/weekly_portal_prompt_readability_drift.md`.
- Follow-up: next highest unchecked backlog item is `ROUTE SANDBOX:ON` prototype (flag-gated sustained lane-lock sandbox mode).

## 2026-03-21 13:31 KST — Cycle P route sandbox prototype (weekly digest)
- Added experiment-gated digest token  via  with sustained lane-lock arming requirement.
- Verified regression and digest generation remain PASS ([PASS] weekly portal prompt readability drift regression checks, digest script run).
- Follow-up: keep flag OFF by default; enable only for controlled sandbox reviews.

## 2026-03-21 13:31 KST — Cycle P route sandbox prototype (weekly digest)
- Added experiment-gated digest token ROUTE SANDBOX:ON|OFF via DOTPIO_EXPERIMENT_ROUTE_SANDBOX with sustained lane-lock arming requirement.
- Verified regression and digest generation remain PASS (`python3 scripts/regression_weekly_portal_prompt_readability_drift.py`, digest script run).
- Follow-up: keep flag OFF by default; enable only for controlled sandbox reviews.

## 2026-03-21 14:33 KST — Cycle Q sandbox cooloff token
- Completed backlog item: `SANDBOX COOLOFF:<n>` (consecutive non-armed windows since last `ROUTE SANDBOX:ON`).
- Evidence:
  - `scripts/weekly_portal_prompt_readability_drift.py` now computes `sandboxCooloff` + `sandboxCooloffSignals` from prior digest JSON and emits markdown line `SANDBOX COOLOFF`.
  - `scripts/regression_weekly_portal_prompt_readability_drift.py` extended for payload/schema/markdown assertions and cooloff transition fixtures (`no prior`, `just disarmed`, `continuing`).
  - Fresh digest artifacts regenerated under `logs/weekly_portal_prompt_readability_drift.{json,md}`.
- Verification:
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` ✅
  - `python3 scripts/weekly_portal_prompt_readability_drift.py` ✅
- Follow-up: remaining unchecked Cycle Q item is `SANDBOX TARGET:<lane>` token.

## 2026-03-21 15:01 KST — Digest signal wiring for sandbox target lane
- Added `sandbox_target_from_signals()` to derive lane target from route-sandbox + lane-lock signals.
- Output contract:
  - Active sandbox + armed lane lock + non-mixed lane -> `PORTAL|ALT|PRESSURE`
  - Active sandbox + mixed lane lock -> `MIXED`
  - Sandbox OFF -> `NONE`
- JSON payload now includes `sandboxTarget` + `sandboxTargetSignals`.
- Follow-up: Revisit mapping if lane-family taxonomy expands beyond portal/alt/pressure.

## 2026-03-21 15:01 KST — Cycle R sandbox target confidence signal
- Added `sandbox_target_confidence_from_signals()`.
- Confidence mapping:
  - `NONE|MIXED` target => LOW
  - sustained armed lock + HIGH route confidence => HIGH
  - armed lock + MID/HIGH route confidence => MID
  - otherwise LOW
- JSON + markdown outputs now carry confidence token and signal rationale.

## 2026-03-21 15:33 KST — Cycle R sandbox target source token
- Completed backlog item: `TARGET SRC:LOCK|MIXED|NONE` for weekly portal prompt readability drift digest.
- Decision: expose derivation path directly from sandbox-target resolver (`LOCK` when lane-lock derived, `MIXED` when sandbox active without single-lane lock, `NONE` when sandbox inactive) for quick auditability.
- Implementation: `scripts/weekly_portal_prompt_readability_drift.py` now emits `sandboxTargetSource` in JSON, adds `targetSource` signal, and renders markdown line `TARGET SRC`.
- Verification: `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py`; `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`; digest regeneration PASS.
- Follow-up: next highest unchecked item is `TARGET SHIFT:<FROM->TO>` history token.

## 2026-03-21 15:38 KST — Cycle R closure: sandbox target history token
- Completed remaining Cycle R backlog item: `TARGET SHIFT:<FROM->TO>` in weekly portal prompt readability digest.
- Digest now emits JSON fields `sandboxTargetShift`, `sandboxTargetShiftSignals` and markdown row `TARGET SHIFT`.
- Shift semantics compare prior digest `sandboxTarget` to current target; emits stable `X->X` when unchanged and still reports prior-load/change signals for auditability.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`; `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120 ...` PASS.

## 2026-03-21 16:01 KST — Cycle S sandbox readiness token
- Decision: Added `SANDBOX READY:IDLE|PRIMED|ARMED` classification to weekly portal prompt digest using `ROUTE SANDBOX + SANDBOX TARGET CONF + ACTION GUARD + lane-lock armed` signals.
- Evidence: `scripts/weekly_portal_prompt_readability_drift.py`, `scripts/regression_weekly_portal_prompt_readability_drift.py`, refreshed weekly digest artifacts.
- Follow-up: implement `ACTION STABILITY:LOCKED|WATCH` token next to reduce retune whiplash in digest routing.

## 2026-03-21 16:33 KST — Cycle S digest stability token (`ACTION STABILITY`)
- Task: Add `ACTION STABILITY:LOCKED|WATCH` derived from `ACTION CONF + FOCUS VOL + DRIFT MOMENTUM` to reduce retune whiplash.
- Decision: Classified as `LOCKED` only when confidence is MID/HIGH, focus volatility is STEADY, and drift momentum is FLAT/COOLING; otherwise `WATCH`.
- Evidence:
  - Updated `scripts/weekly_portal_prompt_readability_drift.py` with `route_action_stability_from_signals`, JSON fields (`actionStability`, `actionStabilitySignals`), and markdown digest line.
  - Extended `scripts/regression_weekly_portal_prompt_readability_drift.py` assertions for new schema + markdown token.
  - Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` (PASS), `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120` (PASS).
- Follow-up: Remaining highest-priority unchecked item is Cycle S `WHAT-IF ALT:<lane> ΔRISK:<n>` experiment behind flag.

## 2026-03-21 17:01 KST — Cycle S what-if alt prototype (`WHAT-IF ALT`)
- Task: ship flagged digest what-if token `WHAT-IF ALT:<lane> ΔRISK:<n>` for low-cost alternate-lane planning.
- Implementation: added `what_if_alt_from_signals()` in `scripts/weekly_portal_prompt_readability_drift.py` with env flag `DOTPIO_EXPERIMENT_WHAT_IF_ALT`.
- Digest output: JSON now includes `whatIfAlt`, `whatIfAltSignals`; markdown adds `WHAT-IF` line with flag/status/current-alt/risk projection tuple.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` + digest regeneration pass.
- Follow-up: if enabled in sustain env, validate real-window usefulness of projected `ΔRISK` heuristic and tune coefficients if noisy.

## 2026-03-21 17:31 KST
- Task: Cycle T vertical slice — add digest `WHAT-IF CONF:LOW|MID|HIGH` token from flagged alt-lane projection + route confidence.
- Files: `scripts/weekly_portal_prompt_readability_drift.py`, `scripts/regression_weekly_portal_prompt_readability_drift.py`, `TASKS.md`, `POST_RC_BACKLOG.md`
- Decisions:
  - Confidence remains conservative (`LOW`) when experiment flag is off or no distinct alternate lane exists.
  - High confidence requires strong projected risk drop (`ΔRISK<=-3`) plus non-low route-action confidence.
- Verification: py_compile + weekly digest regression + digest artifact refresh all PASS.
- Next: implement Cycle T `WHAT-IF ALIGN` token.

## 2026-03-21 18:01 KST — Cycle T what-if alignment token
- Completed: Added digest token `WHAT-IF ALIGN:ALIGNED|DIVERGED` derived from `ALT LANE` vs `ROUTE ACTION` mapping.
- Evidence: `scripts/weekly_portal_prompt_readability_drift.py`, `scripts/regression_weekly_portal_prompt_readability_drift.py`.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` PASS.
- Follow-up: implement remaining Cycle T item `WHAT-IF BAND:GAIN|NEUTRAL|LOSS`.

## 2026-03-21 18:31 KST — Cycle U what-if magnitude token
- Task: Add `WHAT-IF MAG:SMALL|MED|LARGE` from `|ΔRISK|` so alternate-lane impact size is glanceable.
- Decision: Magnitude thresholds set to SMALL(0-1), MED(2-3), LARGE(>=4); flag-disabled defaults to SMALL for stable baseline semantics.
- Output: `scripts/weekly_portal_prompt_readability_drift.py` now emits `whatIfMagnitude` + `whatIfMagnitudeSignals` and markdown line `WHAT-IF MAG`.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` + `python3 scripts/weekly_portal_prompt_readability_drift.py` PASS.
- Follow-up: Cycle U remaining items are `WHAT-IF FIT` and flagged `WHAT-IF FALLBACK`.

## 2026-03-21 19:03 KST — WHAT-IF FIT token shipped
- Task: Added `WHAT-IF FIT:SAFE|EVEN|TENSE` in weekly portal readability digest.
- Decision: derive fit from projected what-if risk band (`LOW|MID|HIGH`) compared against current pressure band.
- Implementation: `scripts/weekly_portal_prompt_readability_drift.py` now emits `whatIfFit` + `whatIfFitSignals` (JSON + markdown).
- Follow-up: complete remaining Cycle U fallback-lane token behind flag.

## 2026-03-21 19:33 KST — Cycle U what-if fallback token (`WHAT-IF FALLBACK`) shipped
- Completed backlog item: prototype `WHAT-IF FALLBACK:<lane>` behind flag when what-if alternate lane diverges from route action.
- Implementation: `scripts/weekly_portal_prompt_readability_drift.py` now emits `whatIfFallback` + `whatIfFallbackSignals` and markdown line `WHAT-IF FALLBACK`.
- Flag contract: `DOTPIO_EXPERIMENT_WHAT_IF_FALLBACK` (OFF by default). When enabled + `WHAT-IF ALIGN:DIVERGED`, fallback resolves to route-action lane (`PORTAL|ALT|PRESSURE`), otherwise `NONE`.
- Verification: `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py`; `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`; `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120 --out-json logs/weekly_portal_prompt_readability_drift.json --out-md logs/weekly_portal_prompt_readability_drift.md`.
- Follow-up: All ACTION_ITEMS/TASKS/POST_RC items are checked; next cycle should run Game Director review loop (3 ideas -> 1 experiment -> slice).

## 2026-03-21 19:36 KST — Game Director Cycle V (ideas + selected vertical slice)
- Candidate ideas:
  1) Low-risk UX: `WHAT-IF FALLBACK CONF:LOW|MID|HIGH` from fallback divergence + route confidence.
  2) Mid-risk systems: `WHAT-IF FALLBACK FIT:SAFE|EVEN|TENSE` from fallback projection vs pressure band.
  3) High-risk novelty: flagged fallback rationale token `WHAT-IF FALLBACK WHY:<short>` for operator-facing diagnostics.
- Selected experiment: idea (1) fallback confidence token (minimal reversible slice).
- Implementation: `scripts/weekly_portal_prompt_readability_drift.py` now emits `whatIfFallbackConfidence` + signals and markdown `WHAT-IF FALLBACK CONF`.
- Verification: `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py`; `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`; `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120 --out-json logs/weekly_portal_prompt_readability_drift.json --out-md logs/weekly_portal_prompt_readability_drift.md`.
- Backlog update: Added Cycle V queue to `TASKS.md`/`POST_RC_BACKLOG.md`, marked fallback-confidence item done, left fallback-fit + fallback-why queued.

## 2026-03-21 20:01 KST — Cycle V fallback pressure-safety token shipped
- Completed `WHAT-IF FALLBACK FIT:SAFE|EVEN|TENSE` digest token implementation.
- Updated `scripts/weekly_portal_prompt_readability_drift.py` payload/markdown with fallback projection-vs-pressure fit + signals.
- Extended `scripts/regression_weekly_portal_prompt_readability_drift.py` schema + markdown assertions.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` PASS; digest regeneration PASS.
- Follow-up: remaining Cycle V unchecked item is `WHAT-IF FALLBACK WHY:<short>` behind flag.

## 2026-03-21 21:01 KST — Cycle W vertical slice: fallback-lane alignment token
- Completed backlog item: `WHAT-IF FALLBACK ALIGN:SYNC|ASYNC`.
- Durable decisions:
  - Added `what_if_fallback_alignment_from_signals(...)` in `scripts/weekly_portal_prompt_readability_drift.py`.
  - Alignment emits `SYNC` for no-actionable/mixed-focus safe states and `ASYNC` only when actionable fallback diverges from lane focus.
  - Digest now publishes JSON fields `whatIfFallbackAlign` / `whatIfFallbackAlignSignals` and markdown line `WHAT-IF FALLBACK ALIGN`.
- Verification:
  - `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py` ✅
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` ✅
  - `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120 --out-json logs/weekly_portal_prompt_readability_drift.json --out-md logs/weekly_portal_prompt_readability_drift.md` ✅
- Next priority item: Cycle W `WHAT-IF FALLBACK MAG:SMALL|MED|LARGE`.

## 2026-03-21 21:35 KST — Fallback impact sizing token shipped
- Decision: added digest classifier `WHAT-IF FALLBACK MAG:SMALL|MED|LARGE` based on fallback `|ΔRISK|` bands.
- Implementation: `scripts/weekly_portal_prompt_readability_drift.py` now computes `whatIfFallbackMagnitude` + signal payload.
- Follow-up: wire magnitude into dual-path planner once `DOTPIO_EXPERIMENT_WHAT_IF_FALLBACK_ALT2` is enabled in ops.

## 2026-03-21 21:58 KST — Cycle X vertical slice: ALT2 quality gate
- Completed backlog closure for Cycle W `WHAT-IF FALLBACK ALT2` and shipped follow-up quality gate in digest classifier.
- Durable decision:
  - `ALT2` now emits only when candidate lane-focus score is strong (`>=2`) and non-ambiguous vs next lane (`gap>=1`).
  - Otherwise emit `NONE` with explicit reasons (`secondary-score-too-low` / `secondary-ambiguity-gap`).
- Verification:
  - `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`
  - `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120 --out-json logs/weekly_portal_prompt_readability_drift.json --out-md logs/weekly_portal_prompt_readability_drift.md`

## 2026-03-21 22:04 KST — Cycle X follow-up: ALT2 confidence token shipped
- Implemented `WHAT-IF FALLBACK ALT2 CONF:LOW|MID|HIGH` in weekly portal digest via `what_if_fallback_alt2_confidence_from_signals(...)`.
- Confidence model keys off ALT2 quality-gate outputs (`topScore`, `secondScore`, `scoreGap`) and returns LOW when flag/fallback/secondary lane is not actionable.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` PASS.
- Next hook: complete remaining unchecked Cycle X item `WHAT-IF FALLBACK PLAN:PRIMARY|SECONDARY|HOLD`.

## 2026-03-21 22:33:50 KST
- Task: Game Director Cycle X finalization — dual-path merge hint token (`WHAT-IF FALLBACK PLAN`) behind experiment flag.
- Commit: HEAD (this run)
- Files: `scripts/weekly_portal_prompt_readability_drift.py`, `scripts/regression_weekly_portal_prompt_readability_drift.py`, `TASKS.md`, `POST_RC_BACKLOG.md`
- Verification:
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` ✅
  - `DOTPIO_EXPERIMENT_WHAT_IF_FALLBACK_PLAN=1 python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 50` ✅
- Decisions:
  - Added `WHAT-IF FALLBACK PLAN:PRIMARY|SECONDARY|HOLD` selector based on primary/secondary fallback actionability + confidence.
  - Kept behavior additive/reversible with `DOTPIO_EXPERIMENT_WHAT_IF_FALLBACK_PLAN` flag (disabled => `HOLD`).
- Follow-up:
  - Start next Game Director cycle (new idea triad) now that ACTION_ITEMS/TASKS/POST_RC backlog are fully checked.

## 2026-03-21 22:36:47 KST
- Task: Game Director Cycle Y selected experiment — merge-plan pressure-fit token (`WHAT-IF PLAN FIT`).
- Commit: HEAD (this run)
- Files: `scripts/weekly_portal_prompt_readability_drift.py`, `scripts/regression_weekly_portal_prompt_readability_drift.py`, `TASKS.md`, `POST_RC_BACKLOG.md`
- Verification:
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` ✅
  - `DOTPIO_EXPERIMENT_WHAT_IF_FALLBACK_PLAN=1 python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 50` ✅
- Decisions:
  - Added merge-plan pressure compatibility token (`SAFE|EVEN|TENSE`) to quantify selected plan vs current pressure band.

## 2026-03-21 23:08 KST
- Task: Game Director Cycle Y low-risk UX token slice (`WHAT-IF PLAN WHY`).
- Decision: Added plan-rationale resolver in weekly digest pipeline with short operator copy (`PRIMARY RELIEF`, `ALT2 STEADY`, `HOLD FOR SIGNAL`) behind flag `DOTPIO_EXPERIMENT_WHAT_IF_FALLBACK_PLAN_WHY`.
- Evidence: `scripts/weekly_portal_prompt_readability_drift.py`, `scripts/regression_weekly_portal_prompt_readability_drift.py`.
- Follow-up: remaining Cycle Y novelty item is split recommendation token (`WHAT-IF SPLIT:ON`).

## 2026-03-21 23:34 KST — Cycle Y novelty slice closure (`WHAT-IF SPLIT`)
- Completed backlog item: added flagged dual-route split recommendation token `WHAT-IF SPLIT:ON|OFF` in weekly portal readability digest.
- Decision: gate behind `DOTPIO_EXPERIMENT_WHAT_IF_SPLIT`; emit `ON` only when primary/secondary fallback lanes are both actionable, diverged, and pass confidence + |ΔRISK| threshold.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` ✅
- Follow-up: with TASKS + POST_RC backlog now fully checked, next cycle should start Game Director review loop (3 ideas -> pick 1 -> minimal vertical slice).

## 2026-03-21 23:36 KST — Game Director Cycle Z review + selected vertical slice
- Idea set:
  1) Low-risk UX: `WHAT-IF SPLIT CONF:LOW|MID|HIGH` trust token for split recommendation.
  2) Mid-risk systems: `WHAT-IF SPLIT LANES:<primary>/<secondary>` compact lane-pair handoff token.
  3) High-risk novelty: `WHAT-IF SPLIT SAFE:ON` gate when split recommendation avoids pressure escalation.
- Selected experiment: idea #1 (`WHAT-IF SPLIT CONF`) as minimal vertical slice.
- Implementation: Added `what_if_split_confidence_from_signals(...)` and emitted `whatIfSplitConfidence`/`whatIfSplitConfidenceSignals` in JSON plus markdown line `WHAT-IF SPLIT CONF`.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` ✅
- Next hook: implement Cycle Z remaining items (`WHAT-IF SPLIT LANES`, `WHAT-IF SPLIT SAFE`).

## 2026-03-22 00:03 KST — Cycle Z mid-risk slice closure (`WHAT-IF SPLIT LANES`)
- Completed backlog item: added compact route-pair handoff token `WHAT-IF SPLIT LANES:<primary>/<secondary>` to weekly portal readability digest.
- Files: `scripts/weekly_portal_prompt_readability_drift.py`, `scripts/regression_weekly_portal_prompt_readability_drift.py`, `TASKS.md`, `POST_RC_BACKLOG.md`.
- Verification:
  - `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py` ✅
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` ✅
- Next hook: implement remaining Cycle Z novelty item `WHAT-IF SPLIT SAFE:ON` behind flag.

## 2026-03-22 00:33 KST — Cycle Z novelty closure (`WHAT-IF SPLIT SAFE`)
- Completed highest-priority unchecked backlog item by adding flagged token `WHAT-IF SPLIT SAFE:ON|OFF` to weekly portal readability digest.
- Added `what_if_split_safe_from_signals(...)` in `scripts/weekly_portal_prompt_readability_drift.py`.
- Gate contract: `DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_SAFE` (default OFF).
- Safe-mode `ON` requires: split armed, primary path non-escalating (`SAFE|EVEN` fit), ALT2 confidence gate (`MID|HIGH`), and both split confidences at least `MID`.
- Follow-up: since TASKS + POST_RC are now fully checked, next cycle should run Game Director review loop (3 ideas -> pick 1 -> vertical slice).

## 2026-03-22 01:01 KST — Game Director Cycle AA: split posture vertical slice
- Backlog lifecycle: set `WHAT-IF SPLIT POSTURE` to `[~]` before implementation, then promoted to `[x]` after verification in `TASKS.md` + `POST_RC_BACKLOG.md`.
- Idea slate generated:
  1) Low-risk UX (chosen): `WHAT-IF SPLIT POSTURE:SAFE|WATCH|HOLD`.
  2) Mid-risk systems: `WHAT-IF SPLIT COOLOFF:<n>` counter.
  3) High-risk novelty: flag-gated `WHAT-IF SPLIT ESCALATE:ON`.
- Implemented minimal vertical slice in `scripts/weekly_portal_prompt_readability_drift.py`:
  - Added `what_if_split_posture_from_signals(...)`.
  - Added JSON fields `whatIfSplitPosture` + `whatIfSplitPostureSignals`.
  - Added markdown digest row `WHAT-IF SPLIT POSTURE`.
- Regression updates: `scripts/regression_weekly_portal_prompt_readability_drift.py` now asserts new schema keys + markdown token.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` ✅
- Next hook: implement Cycle AA follow-ups (`SPLIT COOLOFF`, `SPLIT ESCALATE`).


## 2026-03-22 01:35 KST — Cycle AA follow-up closure (`WHAT-IF SPLIT COOLOFF`)
- Completed backlog item: added `WHAT-IF SPLIT COOLOFF:<n>` token to weekly portal readability digest.
- Decision: cooloff starts at 1 when split flips ON->OFF, increments while split stays OFF, resets to 0 on split ON.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` and `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py` passed.
- Follow-up: next unchecked item is flagged novelty `WHAT-IF SPLIT ESCALATE:ON`.

## 2026-03-22 02:03 KST
- Task: Game Director Cycle AA follow-up — split escalation sentinel prototype (`WHAT-IF SPLIT ESCALATE:ON`).
- Commit: HEAD (this run)
- Files: `scripts/weekly_portal_prompt_readability_drift.py`, `scripts/regression_weekly_portal_prompt_readability_drift.py`, `TASKS.md`, `POST_RC_BACKLOG.md`
- Verification:
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` ✅
  - `python3 scripts/weekly_portal_prompt_readability_drift.py --help` ✅
- Decisions:
  - Added flag-gated sentinel `DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESCALATE`.
  - Sentinel now turns `ON` only when split is armed, lanes remain divergent, and plan fit is `TENSE`.
- Follow-up:
  - Evaluate next unchecked Game Director injection item.

## 2026-03-22 02:12 KST
- Task: Game Director Cycle AB vertical slice — add `WHAT-IF SPLIT ESC CONF:LOW|MID|HIGH`.
- Commit: HEAD (this run)
- Files: `scripts/weekly_portal_prompt_readability_drift.py`, `scripts/regression_weekly_portal_prompt_readability_drift.py`, `TASKS.md`, `POST_RC_BACKLOG.md`
- Verification:
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` ✅
- Decisions:
  - Confidence maps from `(split escalate ON/OFF, split confidence, plan fit)` with conservative default LOW when escalation is OFF.
  - Token is additive and non-breaking to existing digest consumers.
- Follow-up:
  - Remaining Cycle AB backlog items: `ESC LANES`, flag-gated `ESC COOL`.

## 2026-03-22 02:36 KST
- Task: Cycle AB follow-up closure — split escalation readability/cooloff tokens (`WHAT-IF SPLIT ESC LANES`, `WHAT-IF SPLIT ESC COOL`).
- Files: `scripts/weekly_portal_prompt_readability_drift.py`, `scripts/regression_weekly_portal_prompt_readability_drift.py`, `TASKS.md`, `POST_RC_BACKLOG.md`.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` ✅, `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 30 --max-commits 50 --out-json /tmp/dotpio-weekly.json --out-md /tmp/dotpio-weekly.md` ✅.
- Decisions: Added explicit escalation route-pair token `WHAT-IF SPLIT ESC LANES:<primary>/<secondary>`; added flag-gated escalation cooloff counter `WHAT-IF SPLIT ESC COOL:<n>` (`DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_COOL`) with OFF->disarm lifecycle tracking from prior digest payload.
- Follow-up: ACTION_ITEMS has only tracking legend `- [ ] todo` remaining; next meaningful priority is to continue digest Game Director line when new actionable items are injected.

## 2026-03-22 03:04 KST — Game Director Cycle AC vertical slice closure (`WHAT-IF SPLIT ESC STATE`)
- Task: Add split escalation lifecycle state token for weekly portal prompt digest triage.
- Ideas generated:
  1) Low-risk UX (selected): `WHAT-IF SPLIT ESC STATE:ARMED|COOLING|IDLE`.
  2) Mid-risk systems: flag-gated `WHAT-IF SPLIT ESC PRESSURE:LOW|MID|HIGH` cooldown pressure band.
  3) High-risk novelty: flag-gated `WHAT-IF SPLIT ESC RECOVER:<lane>` post-escalation recovery route hint.
- Decision: Ship idea #1 as minimal vertical slice and inject #2/#3 as follow-up backlog candidates.
- Implementation: `scripts/weekly_portal_prompt_readability_drift.py` now emits JSON fields `whatIfSplitEscState` + `whatIfSplitEscStateSignals` and markdown line `WHAT-IF SPLIT ESC STATE`.
- Verification:
  - `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` ✅
  - `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 60` ✅
- Backlog lifecycle: marked Cycle AC state-token item `[~] -> [x]` in `TASKS.md` and `POST_RC_BACKLOG.md`; follow-up items remain unchecked.
- Next hook: implement Cycle AC mid/high experiments (`ESC PRESSURE`, `ESC RECOVER`) in subsequent loop.

## 2026-03-22 03:31 KST — Cycle AC follow-up: split escalation cooldown pressure-band token
- Completed task: Add  behind .
- Decision: token defaults to  with explicit  reason; when enabled, pressure derives from current pressure band with lifecycle-aware cooling decay (=base,  decays 1~2 steps,  minimized).
- Verification: py_compile + [PASS] weekly portal prompt readability drift regression checks + digest generation PASS.
- Next: implement remaining Cycle AC item  behind flag.

## 2026-03-22 03:33 KST — Cycle AC follow-up: split escalation cooldown pressure-band token (corrected log)
- Completed task: Add `WHAT-IF SPLIT ESC PRESSURE:LOW|MID|HIGH` behind `DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_PRESSURE`.
- Decision: token defaults to `LOW` with explicit `flag-disabled` reason; when enabled, pressure derives from current pressure band with lifecycle-aware cooling decay (`ARMED`=base, `COOLING` decays 1~2 steps, `IDLE` minimized).
- Verification: `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py` + `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` + weekly digest generation PASS.
- Next: implement remaining Cycle AC item `WHAT-IF SPLIT ESC RECOVER:<lane>` behind flag.

## 2026-03-22 03:41 KST — Game Director Cycle AD vertical slice: split escalation recovery hint
- Idea slate (L/M/H): (1) recovery hint lane token (chosen), (2) recovery confidence token, (3) dual-lane recovery fallback token.
- Shipped: weekly digest now emits WHAT-IF SPLIT ESC RECOVER:<lane> behind DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER; when enabled it suggests the lowest-pressure actionable lane from escalation lane-pair, otherwise OFF/NONE with explicit reason.
- Files: scripts/weekly_portal_prompt_readability_drift.py, scripts/regression_weekly_portal_prompt_readability_drift.py, TASKS.md, POST_RC_BACKLOG.md.
- Verification: python3 -m py_compile + python3 scripts/regression_weekly_portal_prompt_readability_drift.py + digest generation PASS.
- Backlog sync: Cycle AC recovery item closed; Cycle AD injected with recovery-confidence + recovery-alt follow-ups.

## 2026-03-22 04:01 KST — Cycle AD: Split Escalation Recovery Confidence
- Completed: Added WHAT-IF SPLIT ESC RECOVER CONF:LOW|MID|HIGH token derived from recovery lane availability, escalation lifecycle state, lane divergence, and pressure easing context.
- Decision: Confidence stays LOW when recover route is OFF/NONE or state is ARMED; rises to MID/HIGH only during easing (COOLING/IDLE) with actionable/divergent lanes and manageable pressure.
- Files: scripts/weekly_portal_prompt_readability_drift.py, scripts/regression_weekly_portal_prompt_readability_drift.py, TASKS.md, POST_RC_BACKLOG.md
- Verification: python3 scripts/regression_weekly_portal_prompt_readability_drift.py (PASS); python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py (PASS).
- Next: Implement WHAT-IF SPLIT ESC RECOVER ALT:<lane> prototype behind flag for contingency planning.

## 2026-03-22 04:33 KST — Cycle AD closure: split escalation recovery ALT fallback
- Completed `WHAT-IF SPLIT ESC RECOVER ALT:<lane>` prototype behind `DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_ALT`.
- Added secondary contingency lane selector that excludes primary recover lane and prefers lowest-pressure remaining lane (`PORTAL` > `ALT` > `PRESSURE`).
- Signal contract shipped in digest JSON/markdown:
  - `whatIfSplitEscRecoverAlt`
  - `whatIfSplitEscRecoverAltSignals`
- Follow-up: if operators want stronger fallback confidence semantics, add dedicated `RECOVER ALT CONF` token next cycle.

## 2026-03-22 04:41 KST — Cycle AE update
- Injected Game Director Cycle AE slate (3 ideas), shipped selected vertical slice: `WHAT-IF SPLIT ESC RECOVER ALT CONF`.
- Verification references: weekly portal readability regression + digest generation passed.
- Remaining Cycle AE queue: `RECOVER PLAN`, flagged `RECOVER WHY`.

## 2026-03-22 05:04 KST — Cycle AE systems slice closure (`WHAT-IF SPLIT ESC RECOVER PLAN`)
- Completed backlog item: added recovery route decision token `WHAT-IF SPLIT ESC RECOVER PLAN:PRIMARY|ALT|HOLD` derived from primary/alt recovery lane availability.
- Implementation: `scripts/weekly_portal_prompt_readability_drift.py` now emits `whatIfSplitEscRecoverPlan` + `whatIfSplitEscRecoverPlanSignals` and markdown digest line for operator handoff.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` PASS.
- Next hook: implement remaining Cycle AE item `WHAT-IF SPLIT ESC RECOVER WHY:<short>` behind flag.

## 2026-03-22 05:34 KST — Cycle AE closure (`WHAT-IF SPLIT ESC RECOVER WHY`)
- Completed task: Prototype `WHAT-IF SPLIT ESC RECOVER WHY:<short>` behind `DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_WHY`.
- Shipped in weekly digest pipeline with deterministic short rationale states (`FLAG OFF`, `PRIMARY RELIEF`, `PRIMARY STABILIZE`, `PRIMARY STEADY`, `ALT SAFETY NET`, `ALT CONTINGENCY`, `HOLD FOR SIGNAL`).
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` + `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py` passed.
- Follow-up: all ACTION_ITEMS/TASKS/POST_RC_BACKLOG currently checked; next cycle should run Game Director ideation/injection lane.

## 2026-03-22 05:38 KST — Game Director Cycle AF review + vertical slice
- Idea slate (3):
  1) Low-risk UX (selected): `WHAT-IF SPLIT ESC RECOVER TEMPO:FAST|STEADY|DEFER` (Scope S, rollback: remove digest row).
  2) Mid-risk systems: `WHAT-IF SPLIT ESC RECOVER ΔCONF:+n|-n` (Scope M, rollback: drop prior-window diff state).
  3) High-risk novelty: flag-gated `WHAT-IF SPLIT ESC RECOVER VETO:ON` under HIGH pressure + LOW confidence (Scope M/L, rollback: flag OFF).
- Selected experiment: #1 tempo token as minimal vertical slice.
- Implementation: weekly digest now emits JSON fields `whatIfSplitEscRecoverTempo` + `whatIfSplitEscRecoverTempoSignals` and markdown line `WHAT-IF SPLIT ESC RECOVER TEMPO`.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` and `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py` pass.
- Backlog injection: added Cycle AF entries to `TASKS.md` and `POST_RC_BACKLOG.md` with selected slice done and two follow-up candidates queued.

## 2026-03-22 06:12 KST — Cycle AF follow-up: split escalation recovery confidence delta
- Completed: Added `WHAT-IF SPLIT ESC RECOVER ΔCONF:+n|-n` token by comparing current recovery confidence tier against prior digest window.
- Decision: Use ordinal confidence scoring (`LOW=0`, `MID=1`, `HIGH=2`) and emit signed delta (`+n` / `-n`, zero as `+0`) with explicit `priorLoaded` signal for auditability.
- Files: scripts/weekly_portal_prompt_readability_drift.py, scripts/regression_weekly_portal_prompt_readability_drift.py, TASKS.md, POST_RC_BACKLOG.md
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` (PASS), `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py` (PASS)
- Next: implement flagged `WHAT-IF SPLIT ESC RECOVER VETO:ON` sentinel when pressure remains HIGH under low confidence.

## 2026-03-22 06:31 KST — Cycle AF/AG digest follow-up
- Task: Closed remaining Cycle AF unchecked item (`WHAT-IF SPLIT ESC RECOVER VETO:ON`) and executed Game Director review cycle because ACTION_ITEMS/TASKS/POST_RC were fully checked.
- Commit: pending (this run)
- Files: `scripts/weekly_portal_prompt_readability_drift.py`, `scripts/regression_weekly_portal_prompt_readability_drift.py`, `TASKS.md`, `POST_RC_BACKLOG.md`
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` ✅
- Decisions:
  - Added flag-gated veto sentinel `WHAT-IF SPLIT ESC RECOVER VETO:ON|OFF` (`DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO`) for HIGH-pressure + LOW-confidence recovery contexts.
  - Ran Game Director cycle ideas (low/mid/high), selected low-risk UX slice, and shipped `WHAT-IF SPLIT ESC RECOVER VETO CONF:LOW|MID|HIGH` for trust readability.
  - Injected Cycle AG backlog follow-ups (`VETO WHY`, `VETO COOLOFF`) as next queue items.
- Follow-up:
  - Highest-priority unchecked item now: `WHAT-IF SPLIT ESC RECOVER VETO WHY:<short>` (flag-gated).

## [2026-03-22 07:05 KST] Cycle AG - split escalation veto rationale/cooloff tokens
- Decision: Extended weekly portal prompt digest with  (flag: ) and  (flag: ).
- Evidence: updated , ; regression pass.
- Follow-up: continue next unchecked ACTION_ITEMS/TASKS priority item after Cycle AG closure.

## [2026-03-22 07:05 KST] Cycle AG - split escalation veto rationale/cooloff tokens
- Decision: Extended weekly portal prompt digest with WHAT-IF SPLIT ESC RECOVER VETO WHY (flag: DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_WHY) and WHAT-IF SPLIT ESC RECOVER VETO COOLOFF (flag: DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_COOLOFF).
- Evidence: updated scripts/weekly_portal_prompt_readability_drift.py and scripts/regression_weekly_portal_prompt_readability_drift.py; regression pass.
- Follow-up: continue next unchecked ACTION_ITEMS/TASKS priority item after Cycle AG closure.

## [2026-03-22 07:08 KST] Cycle AH - veto state token vertical slice
- Ideation (3): (1) veto state token (low-risk UX), (2) veto dwell token (mid-risk telemetry), (3) veto release cue token (high-risk novelty copy).
- Picked experiment: veto state token (`ARMED|COOLING|IDLE`) as minimal vertical slice.
- Verification: weekly portal digest regression pass with markdown/token assertions and state-signal unit checks.

## 2026-03-22 07:33 KST — Cycle AH follow-up: veto dwell token
- Task: Add `WHAT-IF SPLIT ESC RECOVER VETO DWELL:<n>` to count consecutive `ARMED` windows.
- Decision: Dwell increments only when current+prior veto state are both `ARMED`; resets to `0` on `COOLING/IDLE` to avoid stale streak carry.
- Evidence: `scripts/weekly_portal_prompt_readability_drift.py`, `scripts/regression_weekly_portal_prompt_readability_drift.py`; `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` PASS.
- Follow-up: Next unchecked backlog item is `WHAT-IF SPLIT ESC RECOVER VETO RELEASE:<short>` (flag-gated on `COOLING -> IDLE`).

## 2026-03-22 08:02 KST — Cycle AI: veto release confidence token
- Task: Add `WHAT-IF SPLIT ESC RECOVER VETO RELEASE CONF:LOW|MID|HIGH` to score trust for release cue transitions.
- Decision: Score HIGH only on clean `COOLING CLEAR + IDLE`, MID while still COOLING, LOW otherwise (ARMED/dwell/no transition) to avoid false release trust.
- Evidence: `scripts/weekly_portal_prompt_readability_drift.py`, `scripts/regression_weekly_portal_prompt_readability_drift.py`; `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` PASS.
- Follow-up: Remaining Cycle AI backlog items are release route token and release timer token.

## 2026-03-22 08:34 KST — Cycle AI follow-up: veto release route token
- Task: Add `WHAT-IF SPLIT ESC RECOVER VETO RELEASE ROUTE:<lane>` for post-cooldown handoff clarity.
- Decision: Route emits actionable lane only on `COOLING CLEAR -> IDLE` release transitions; otherwise `HOLD` (cooling/armed) or `NONE` when no actionable lane exists.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` (PASS) and `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 30 --out-json logs/weekly_portal_prompt_readability_drift.json --out-md logs/weekly_portal_prompt_readability_drift.md` (PASS).
- Next: remaining highest-priority unchecked item is `WHAT-IF SPLIT ESC RECOVER VETO RELEASE TICK:<n>` (flag-gated prototype).

## 2026-03-22 09:06 KST — Cycle AJ: veto release pacing phase token
- Task: Close highest-priority unchecked item by adding `WHAT-IF SPLIT ESC RECOVER VETO RELEASE PHASE:IDLE|EARLY|MID|LATE`.
- Decision: Chosen as low-risk UX slice after Game Director ideation (low/mid/high). Mapping is deterministic from release tick count and forwards non-numeric tokens (e.g., `FLAG OFF`) unchanged.
- Implementation: Updated `scripts/weekly_portal_prompt_readability_drift.py` payload/markdown plus regression coverage in `scripts/regression_weekly_portal_prompt_readability_drift.py`.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` PASS; `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py` PASS.
- Follow-up: Next highest-priority unchecked item is `WHAT-IF SPLIT ESC RECOVER VETO RELEASE CADENCE:ACCEL|STEADY|DECAY`.

## 2026-03-22 09:34 KST
- Task: Cycle AJ follow-up — add `WHAT-IF SPLIT ESC RECOVER VETO RELEASE CADENCE:ACCEL|STEADY|DECAY` derived from release tick deltas.
- Commit: HEAD (pending commit in this run)
- Files: `scripts/weekly_portal_prompt_readability_drift.py`, `scripts/regression_weekly_portal_prompt_readability_drift.py`, `TASKS.md`, `POST_RC_BACKLOG.md`
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` ✅
- Decisions:
  - Added cadence classifier based on current release tick vs prior tick (`delta >= 2` => `ACCEL`, `delta == 1` => `STEADY`, `delta <= 0` => `DECAY`, inactive window => `STEADY`).
  - Non-numeric tick tokens (e.g., `FLAG OFF`) are forwarded unchanged for compatibility.
- Follow-up:
  - Next highest unchecked item is auto-rearm warning token prototype (`WHAT-IF SPLIT ESC RECOVER VETO REARM:WATCH`).

## 2026-03-22 09:42 KST — Cycle AK: auto-rearm warning prototype
- Task: Add `WHAT-IF SPLIT ESC RECOVER VETO REARM:WATCH` behind flag for late release windows under sustained high pressure.
- Implementation: Added `what_if_split_escalate_recover_veto_rearm_from_signals` and wired payload + markdown digest emission.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` PASS; `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py` PASS.
- Follow-up: Add rearm confidence + rationale tokens before cooloff counter.

## 2026-03-22 10:04 KST — Cycle AK: auto-rearm confidence token
- Completed backlog item: `WHAT-IF SPLIT ESC RECOVER VETO REARM CONF:LOW|MID|HIGH`.
- Implementation: added `what_if_split_escalate_recover_veto_rearm_confidence_from_signals()` and wired JSON/markdown digest output fields.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` and `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py` passed.
- Follow-up: next unchecked item is rearm rationale token (`WHAT-IF SPLIT ESC RECOVER VETO REARM WHY:<short>`).

## 2026-03-22 10:35 KST — Cycle AK item 2 (rearm rationale token)
- Completed `WHAT-IF SPLIT ESC RECOVER VETO REARM WHY:<short>` vertical slice in weekly portal prompt readability digest.
- Evidence: updated rationale classifier + JSON/markdown wiring + regression coverage in `scripts/weekly_portal_prompt_readability_drift.py` and `scripts/regression_weekly_portal_prompt_readability_drift.py`.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` PASS.
- Follow-up: proceed to Cycle AK item 3 (`WHAT-IF SPLIT ESC RECOVER VETO REARM COOLOFF:<n>` behind flag).
## 2026-03-22 11:03 KST — Cycle AK: split escalation auto-rearm cooloff token
- Task: Prototype `WHAT-IF SPLIT ESC RECOVER VETO REARM COOLOFF:<n>` behind flag after WATCH disarms.
- Decision: Added flag-gated cooloff tracker `DOTPIO_EXPERIMENT_WHAT_IF_SPLIT_ESC_RECOVER_VETO_REARM_COOLOFF` that increments consecutive OFF windows after prior `WATCH` and resets when `WATCH` is active.
- Evidence: `scripts/weekly_portal_prompt_readability_drift.py`, `scripts/regression_weekly_portal_prompt_readability_drift.py`.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` PASS.
- Follow-up: If ACTION_ITEMS/TASKS/POST_RC are fully complete, run next Game Director idea injection cycle.
## 2026-03-22 11:08 KST — Cycle AL experiment slice (cooloff state)
- Ideation set: (1) cooloff state token, (2) pressure-relief fit token, (3) flagged rearm nudge token.
- Chosen experiment: #1 `WHAT-IF SPLIT ESC RECOVER VETO REARM COOLOFF STATE:ACTIVE|IDLE`.
- Implementation: added state reducer from rearm WATCH + cooloff counter; wired JSON payload + markdown digest row.
- Verification: `python3 scripts/regression_weekly_portal_prompt_readability_drift.py` PASS.
- Follow-up backlog injected: remaining Cycle AL items for FIT and NUDGE tokens are queued unchecked.

## 2026-03-22 11:33 KST — Cycle AL systems closure (rearm pressure-relief fit)
- Completed backlog item: `WHAT-IF SPLIT ESC RECOVER VETO REARM FIT:RELIEF|EVEN|TENSE` from cooloff + pressure context.
- Implementation: `scripts/weekly_portal_prompt_readability_drift.py` now emits `whatIfSplitEscRecoverVetoRearmFit` + `...Signals` and markdown row `WHAT-IF SPLIT ESC RECOVER VETO REARM FIT`.
- Rule: ACTIVE cooloff maps by pressure (`LOW->RELIEF`, `MID->EVEN`, `HIGH->TENSE`); IDLE + no cooloff + LOW remains `RELIEF`; HIGH without relief window remains `TENSE`.
- Verification: `python3 -m py_compile scripts/weekly_portal_prompt_readability_drift.py scripts/regression_weekly_portal_prompt_readability_drift.py`; `python3 scripts/regression_weekly_portal_prompt_readability_drift.py`; `python3 scripts/weekly_portal_prompt_readability_drift.py --since-days 7 --max-commits 120` (all PASS).
- Next priority item: `WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE:<short>` (flagged prototype).

## [2026-03-22 12:09 KST] Cycle AM - Nudge confidence vertical slice
- Task: Add `WHAT-IF SPLIT ESC RECOVER VETO REARM NUDGE CONF:LOW|MID|HIGH` token to weekly portal prompt readability digest.
- Decision: Confidence maps from nudge urgency + rearm confidence + relief fit to keep operator trust glanceable.
- Evidence: updated `scripts/weekly_portal_prompt_readability_drift.py`, `scripts/regression_weekly_portal_prompt_readability_drift.py`; regression + digest scripts passed.
- Follow-up: Remaining Cycle AM queue = nudge window token, flagged nudge rationale token.
