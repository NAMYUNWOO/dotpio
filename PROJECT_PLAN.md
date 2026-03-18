# DOTPIO Project Plan (Release-Oriented)

Last updated: 2026-03-18
Owner: Game Director (AI)
Branch: `feature/ai-disassemble-builder`

## Milestones

### M0. Immediate Stabilization (Now ~ 1 day)
Goal: remove blockers for core loop validation.

Definition of Done:
- Drop-to-map item can be picked up again (`G` key)
- Inventory full failure handling for pickup
- Build/disassemble test loadout available at start
- No critical crash on inventory/action menu flow

### M1. Core Loop Lock (1 week)
Goal: make 30-minute loop consistently fun.

Definition of Done:
- Loop is stable: explore -> fight -> loot -> disassemble/build -> power-up
- SRL economy no infinite growth exploits
- map_01~map_04 progression/portal flow validated

### M2. Content Sprint (1~2 weeks)
Goal: widen replay variety.

Definition of Done:
- +2~3 maps
- enemy pattern/elemental interactions expanded
- AI build/disassemble output diversity improved

### M3. Meta Progression (1 week)
Goal: give strong next-run motivation.

Definition of Done:
- run-level goals/missions
- unlockables for build options/material groups
- fail-forward progression reward

### M4. UX/Accessibility Polish (3~5 days)
Goal: remove confusion and friction.

Definition of Done:
- DOS UI copy consistent and actionable
- key guidance and lock reasons always visible
- first 5-minute onboarding clarity target met

### M5. Release Candidate & Launch (3~5 days)
Goal: shippable stable build.

Definition of Done:
- critical bugs = 0
- regression checklist pass
- release note/screenshot package complete

---

## Release Gates (Must-pass)
1. No infinite farm loop in SRL economy
2. 30-minute session keeps progression momentum
3. New player can complete one build within 5 minutes
4. No crash/progression blocker in default flow

---

## Team Lanes
- Systems: economy/build/disassemble
- World: map/progression/portal routing
- AI Content: generation quality + safeguards
- UX: DOS interactions/copy/status feedback
- QA: scripted + manual regressions

See also: `TEAM_OPERATING_PROTOCOL.md` for dispatch/report workflow.