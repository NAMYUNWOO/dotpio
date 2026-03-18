# TASKS

See project-level plans:
- `PROJECT_PLAN.md` (milestones/release gates)
- `ACTION_ITEMS.md` (detailed execution backlog)

## Immediate (current sprint focus)
- [ ] Implement map item pickup flow for dropped items
  - [ ] Add pickup interaction (`G` key) for item on player tile
  - [ ] Add inventory-full failure feedback message
  - [ ] Mark picked world item as collected/remove from map entity list
  - [ ] Add DOS help text for pickup key
  - [ ] Add regression test scenario: drop -> pick up -> verify count
