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

- [~] Inventory UX improvements for build workflow
  - [ ] Add item split/partial stack feature ("소분")
  - [ ] Improve `BUILDER.SRL` use flow UX (action menu + F9 path)
  - [ ] Build preview panel: consumed components + expected SRL cost
  - [ ] Keep build material consumption explicit in confirmation/status copy
