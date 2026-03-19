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
