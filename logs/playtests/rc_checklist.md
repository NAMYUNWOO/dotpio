# DOTPIO Release Candidate Checklist (M5)

Last updated: 2026-03-19 (KST)
Branch: `feature/ai-disassemble-builder`
Owner: QA lane

## Usage
- Run this checklist top-to-bottom before tagging an RC.
- Mark each row `[x]` only when command exits cleanly and artifact is refreshed.
- Record blocker IDs in the blocker triage table before re-running.

## Release Gates (must-pass)
- [ ] No infinite farm loop in SRL economy
- [ ] 30-minute session keeps progression momentum
- [ ] New player can complete one build within 5 minutes
- [ ] No crash/progression blocker in default flow

## Regression Matrix

### 1) Combat & Core Loop
- [ ] 30-minute core loop checklist
  - Command: `python3 scripts/regression_30min_loop_checklist.py`
  - Artifact: `logs/playtests/loop_30min_checklist.md`
  - Covers: progression momentum, combat/build/disasm flow stability
- [ ] Enemy behavior variant sanity
  - Command: `lua scripts/regression_enemy_behavior_variants.lua`
  - Artifact: command output (pass/fail)
  - Covers: encounter diversity and combat behavior profile safety

### 2) Inventory / Build / Disassemble
- [ ] Drop -> pickup regression
  - Command: `lua scripts/regression_drop_pickup.lua`
  - Covers: world pickup reliability + inventory capacity failure path
- [ ] Build preview/confirm gate
  - Command: `lua scripts/regression_build_preview_confirm.lua`
  - Covers: explicit material/SRL consumption before build
- [ ] BUILDER.SRL affordance copy
  - Command: `lua scripts/regression_builder_srl_affordance.lua`
  - Covers: player-facing SRL requirement clarity
- [ ] Split stack interaction
  - Command: `lua scripts/regression_split_stack.lua`
  - Covers: partial stack split guardrails
- [ ] Disassembly caps fairness
  - Command: `lua scripts/regression_disassembly_caps.lua`
  - Covers: salvage cap and size-tier budget envelope
- [ ] SRL spam suppression curve
  - Command: `lua scripts/regression_srl_cost_curve.lua`
  - Covers: anti-spam build cost curve
- [ ] Anti-exploit loop detector
  - Commands:
    - `lua scripts/regression_anti_exploit_report.lua`
    - `lua scripts/economy_anti_exploit_report.lua`
  - Artifact: report output under `logs/` from report script
  - Covers: positive/flat-profit loop detection

### 3) Portal / World Progression
- [ ] map_01~04 progression route + portal validator
  - Command: `python3 scripts/regression_map_progression.py`
  - Artifact: `logs/playtests/map_01_04_progression_checklist.md`
- [ ] Full portal integrity check
  - Command: `python3 scripts/validate_portals.py`
  - Artifact: command output (pass/fail)

### 4) UX / Accessibility / Presentation
- [ ] Disabled action lock reasons
  - Command: `lua scripts/regression_action_menu_lock_reasons.lua`
- [ ] Onboarding hint flow (<5 min)
  - Command: `lua scripts/regression_onboarding_hints.lua`
- [ ] Keyboard-only usability checklist
  - Command: `python3 scripts/regression_keyboard_usability_checklist.py`
  - Artifact: `logs/playtests/keyboard_only_usability_checklist.md`
- [ ] Refresh launch screenshots
  - Command: `bash scripts/capture_screenshots.sh`
  - Artifacts:
    - `screenshots/screenshot-map04.png`
    - `screenshots/screenshot-inventory-dos.png`

## Blocker Triage (critical blockers must be zero)
| ID | Area | Symptom | Severity | Owner | Status | Fix Commit |
| --- | --- | --- | --- | --- | --- | --- |
| (fill) | | | critical/high/medium | | open/fixed | |

## RC Sign-off
- [ ] Systems sign-off
- [ ] World sign-off
- [ ] AI Content sign-off
- [ ] UX sign-off
- [ ] QA sign-off
- [ ] Release tag created

Sign-off note:
- Date (KST):
- Candidate tag:
- Final blocker count:
- Notes:
