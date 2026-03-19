# TASKS

Last updated: 2026-03-19

See project-level plans:
- `PROJECT_PLAN.md` (milestones/release gates)
- `ACTION_ITEMS.md` (detailed execution backlog)

## Immediate (current sprint focus)
- [x] Implement map item pickup flow for dropped items
  - [x] Add pickup interaction (`G` key) for item on player tile
  - [x] Add inventory-full failure feedback message
  - [x] Mark picked world item as collected/remove from map entity list
  - [x] Add DOS help text for pickup key
  - [x] Add regression test scenario: drop -> pick up -> verify count

- [x] Tune starter build/disassemble loadout for stable smoke-test baseline
  - [x] Seed balanced starter materials/equipment + BUILDER.SRL reserves by folder
  - [x] Add starter loadout regression script (`scripts/regression_starter_loadout.lua`)

- [x] Add economy telemetry baseline for build/disassemble (input/output/SRL envelope)
  - [x] Add shared telemetry writer module (`src/economy_telemetry.lua`)
  - [x] Emit build/disassemble telemetry for lock/fail/success paths in inventory workflow
  - [x] Add telemetry regression script (`scripts/regression_economy_telemetry.lua`)

- [x] Add anti-exploit loop report from economy telemetry
  - [x] Add analyzer module for sliding-window loop profit detection (`src/economy_anti_exploit.lua`)
  - [x] Add report generator script for JSON+Markdown outputs (`scripts/economy_anti_exploit_report.lua`)
  - [x] Add regression script for suspicious loop detection (`scripts/regression_anti_exploit_report.lua`)

- [x] Inventory UX improvements for build workflow
  - [x] Add item split/partial stack feature ("소분")
  - [x] Improve `BUILDER.SRL` use flow UX (action menu + F9 path)
  - [x] Build preview panel: consumed components + expected SRL cost
  - [x] Keep build material consumption explicit in confirmation/status copy

- [x] Economy tuning for low-tier build spam suppression
  - [x] Tune SRL build-cost curve to increase low-tier churn penalties without overtaxing premium recipes
  - [x] Tune disassembly salvage stack/size caps by item size tier for fairness

- [x] Validate map_01~04 progression with portal validator + playtest checklist
  - [x] Run portal wiring validator and capture output artifact
  - [x] Add scripted progression checklist artifact for map_01~04 routes

- [x] Add scripted 30-minute core-loop checklist and pass artifact
  - [x] Add a script that executes the core-loop regression suite and emits a checklist artifact
  - [x] Run it and capture pass evidence under `logs/playtests/`

## Next Up (M2 content sprint)
- [x] Design and implement map_05 layout + portal links
- [x] Design and implement map_06 layout + portal links
- [x] Add at least 3 enemy behavior variants
  - [x] Introduce variant archetypes with distinct combat/movement tendencies
  - [x] Assign variants during spawn so encounters mix behaviors per run
  - [x] Add regression coverage for variant roster/parameters
- [x] Expand AI build output category diversity constraints
  - [x] Add category-balance guardrails so generated build outputs cannot overconcentrate in one category
  - [x] Add regression coverage for diversity constraints
- [x] Add reward table pass for lootbox contents by map tier
  - [x] Add map-tier reward profile selection for lootbox generation
  - [x] Add regression coverage to validate tiered reward weighting envelope

## Next Up (M3 meta progression)
- [x] Add run mission prototype (3 objectives)
  - [x] Track run objective progress (combat/loot/build)
  - [x] Surface objective checklist in HUD
  - [x] Add regression coverage for objective completion flow
- [x] Add unlock flag framework for new build options
  - [x] Add shared unlock-state module with reset/debug helpers
  - [x] Gate advanced build target categories behind unlock flag
  - [x] Trigger unlock on run mission completion and surface status in HUD
  - [x] Add regression coverage for unlock flow + gated category pool

- [x] Add fail-forward reward (currency/material carryover)
  - [x] Compute carryover package from run inventory + mission completion state
  - [x] Apply carryover package on next run start and expose restart status copy
  - [x] Add regression coverage for carryover caps + reward application

- [x] Add summary screen for run result + unlock progress
  - [x] Present per-run mission completion snapshot at reset time
  - [x] Surface unlock status + fail-forward carryover details in summary copy
  - [x] Add regression coverage for summary snapshot formatting/state

## Next Up (M4 UX polish)
- [x] Finalize DOS terminology consistency (Menu/Action/Drop/Disasm/Build)
  - [x] Unify inventory help/status/action copy to canonical terms
  - [x] Keep build material consumption explicit in build preview/confirm/status copy
- [x] Add always-visible lock reason for all disabled actions
  - [x] Surface per-action lock reason text directly in Action Menu rows
  - [x] Add regression coverage for disabled action lock-reason labels
- [x] Add compact onboarding hint flow for first 5 minutes
  - [x] Show concise contextual hint strip without obscuring HUD
  - [x] Rotate/advance hints based on elapsed run time and first interactions
  - [x] Add regression coverage for hint window expiry and progression
- [x] Add keyboard-only usability pass checklist
  - [x] Add scripted keyboard-coverage regression for core inventory controls
  - [x] Generate keyboard-only usability checklist artifact under logs/playtests/

## Next Up (M5 RC/Launch)
- [x] Create RC checklist document
  - [x] Define release gate checklist rows for combat/inventory/build/disasm/portal regressions
  - [x] Link each row to concrete command + artifact path for pass evidence
  - [x] Include blocker triage and release sign-off section
- [x] Execute full regression (combat/inventory/build/disasm/portal)
  - [x] Run RC regression command matrix and record pass/fail evidence
  - [x] Update blocker triage + sign-off rows from latest results
- [x] Fix all critical blockers
  - [x] Re-run blocker-focused regression subset and confirm no critical/high failures
  - [x] Update blocker triage status in RC checklist
- [x] Capture launch screenshots + changelog
- [x] Tag release candidate

## Next Up (M5 Post-RC sustain)
- [x] Weekly SRL telemetry snapshot + rebalance decision log
  - [x] Generate weekly SRL telemetry summary artifact under `logs/`
  - [x] Run anti-exploit report and record rebalance/no-change decision with rationale
