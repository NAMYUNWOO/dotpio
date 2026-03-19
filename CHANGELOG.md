# Changelog

All notable changes to **dotpio** are documented in this file.

## [0.5.0-rc.1] - 2026-03-19

### Added
- World-item pickup interaction on player tile (`G`) with HUD/help affordance updates.
- Starter build/disassemble loadout seed for smoke-test stability.
- Economy telemetry stream for build/disassemble lock/fail/success events.
- Anti-exploit loop detector + report generator for SRL profit-loop auditing.
- Inventory stack split interaction (`S`) with quantity guardrails.
- Build preview/confirm gate showing material consumption + BUILDER.SRL need/have.
- New maps `map_05` and `map_06` with validated reciprocal portal wiring.
- Enemy behavior variants (`skirmisher`, `bruiser`, `sentinel`) and mixed spawn weighting.
- AI build category diversity constraints to prevent output over-concentration.
- Map-tiered lootbox reward profiles by progression depth.
- Run mission prototype (kills/pickup/build), unlock framework, and fail-forward carryover rewards.
- Run summary overlay showing mission/unlock/carryover outcomes.
- Compact first-5-minute onboarding hint strip and keyboard-only usability checklist artifact.
- RC checklist artifact and scripted regression matrix documentation.

### Changed
- SRL build-cost curve tuned to suppress low-tier churn exploits while preserving premium recipe viability.
- Disassembly salvage caps/budgets rebalanced by size tier.
- DOS terminology normalized across Action Menu/Drop/Disasm/Build copy.
- Disabled actions now expose explicit inline lock reasons.

### Fixed
- Drop-to-map item flow now supports reliable pickup and map-entity cleanup.
- Inventory-full pickup failures now surface clear player-facing feedback.
- Critical/high blockers found during RC prep were resolved; blocker-focused rerun stayed clean.

### Verification Snapshot
- Full RC regression matrix passed (combat / inventory / build / disasm / portal).
- Blocker-focused rerun passed (30-min loop, anti-exploit, portal integrity).
- Launch screenshots refreshed:
  - `screenshots/screenshot-map04.png`
  - `screenshots/screenshot-inventory-dos.png`
