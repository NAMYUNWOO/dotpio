# TASKS

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

- [~] Inventory UX improvements for build workflow
  - [x] Add item split/partial stack feature ("소분")
  - [x] Improve `BUILDER.SRL` use flow UX (action menu + F9 path)
  - [x] Build preview panel: consumed components + expected SRL cost
  - [ ] Keep build material consumption explicit in confirmation/status copy

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
