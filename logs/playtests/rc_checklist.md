# DOTPIO Release Candidate Checklist (M5)

Last updated: 2026-03-19 (KST)
Branch: `feature/ai-disassemble-builder`
Owner: QA lane

## Usage
- Run this checklist top-to-bottom before tagging an RC.
- Mark each row `[x]` only when command exits cleanly and artifact is refreshed.
- Record blocker IDs in the blocker triage table before re-running.

## Release Gates (must-pass)
- [x] No infinite farm loop in SRL economy
- [x] 30-minute session keeps progression momentum
- [x] New player can complete one build within 5 minutes
- [x] No crash/progression blocker in default flow

## Regression Matrix

### 1) Combat & Core Loop
- [x] 30-minute core loop checklist
  - Command: `python3 scripts/regression_30min_loop_checklist.py`
  - Artifact: `logs/playtests/loop_30min_checklist.md`
  - Covers: progression momentum, combat/build/disasm flow stability
- [x] Enemy behavior variant sanity
  - Command: `lua scripts/regression_enemy_behavior_variants.lua`
  - Artifact: command output (pass/fail)
  - Covers: encounter diversity and combat behavior profile safety

### 2) Inventory / Build / Disassemble
- [x] Drop -> pickup regression
  - Command: `lua scripts/regression_drop_pickup.lua`
  - Covers: world pickup reliability + inventory capacity failure path
- [x] Build preview/confirm gate
  - Command: `lua scripts/regression_build_preview_confirm.lua`
  - Covers: explicit material/SRL consumption before build
- [x] BUILDER.SRL affordance copy
  - Command: `lua scripts/regression_builder_srl_affordance.lua`
  - Covers: player-facing SRL requirement clarity
- [x] Split stack interaction
  - Command: `lua scripts/regression_split_stack.lua`
  - Covers: partial stack split guardrails
- [x] Disassembly caps fairness
  - Command: `lua scripts/regression_disassembly_caps.lua`
  - Covers: salvage cap and size-tier budget envelope
- [x] SRL spam suppression curve
  - Command: `lua scripts/regression_srl_cost_curve.lua`
  - Covers: anti-spam build cost curve
- [x] Anti-exploit loop detector
  - Commands:
    - `lua scripts/regression_anti_exploit_report.lua`
    - `lua scripts/economy_anti_exploit_report.lua`
  - Artifact: report output under `logs/` from report script
  - Covers: positive/flat-profit loop detection

### 3) Portal / World Progression
- [x] map_01~04 progression route + portal validator
  - Command: `python3 scripts/regression_map_progression.py`
  - Artifact: `logs/playtests/map_01_04_progression_checklist.md`
- [x] Full portal integrity check
  - Command: `python3 scripts/validate_portals.py`
  - Artifact: command output (pass/fail)

### 4) UX / Accessibility / Presentation
- [x] Disabled action lock reasons
  - Command: `lua scripts/regression_action_menu_lock_reasons.lua`
- [x] Onboarding hint flow (<5 min)
  - Command: `lua scripts/regression_onboarding_hints.lua`
- [x] Keyboard-only usability checklist
  - Command: `python3 scripts/regression_keyboard_usability_checklist.py`
  - Artifact: `logs/playtests/keyboard_only_usability_checklist.md`
- [x] Refresh launch screenshots
  - Command: `bash scripts/capture_screenshots.sh`
  - Artifacts:
    - `screenshots/screenshot-map04.png`
    - `screenshots/screenshot-inventory-dos.png`

### 5) Post-RC Sustain Guardrail
- [x] Weekly sustain one-command runner
  - Command: `bash scripts/run_weekly_sustain.sh`
  - Artifacts:
    - `logs/economy_anti_exploit_report.{md,json}`
    - `logs/economy_weekly_snapshot.{md,json}`
  - Covers: anti-exploit report refresh + weekly snapshot generation + schema regression in one pass
- [x] Weekly snapshot delta schema regression
  - Command: `python3 scripts/regression_weekly_snapshot.py`
  - Artifact: command output (pass/fail)
  - Covers: week-over-week delta compatibility for SRL telemetry sustain reporting
- [x] Weekly scheduler wiring helper (cron dry-run)
  - Command: `bash scripts/install_weekly_sustain_cron.sh`
  - Artifact: command output showing managed cron line + existing entry status
  - Covers: operational handoff path to install weekly sustain automation without manual cron editing
- [x] Weekly scheduler installer CLI regression
  - Command: `python3 scripts/regression_weekly_cron_installer.py`
  - Artifact: command output (pass/fail)
  - Covers: dry-run evidence format + CLI override reflection + invalid schedule arg rejection

## Blocker Triage (critical blockers must be zero)
| ID | Area | Symptom | Severity | Owner | Status | Fix Commit |
| --- | --- | --- | --- | --- | --- | --- |
| RC-20260319-00 | all | No critical/high blockers detected in full regression sweep | critical | QA | fixed | n/a |
| RC-20260319-01 | all | Blocker-focused rerun (loop/anti-exploit/portal) stayed clean; no critical/high blockers | critical | QA | fixed | n/a |

## RC Sign-off
- [x] Systems sign-off
- [x] World sign-off
- [x] AI Content sign-off
- [x] UX sign-off
- [x] QA sign-off
- [x] Release tag created

Sign-off note:
- Date (KST): 2026-03-19 17:41
- Candidate tag: `0.5.0-rc.1`
- Tag commit: `d82cab1`
- Final blocker count: 0 critical / 0 high
- Notes: Full RC regression matrix remained green at sign-off; candidate tag exists on branch history and lane logs confirm completion coverage across Systems/World/AI Content/UX/QA.
