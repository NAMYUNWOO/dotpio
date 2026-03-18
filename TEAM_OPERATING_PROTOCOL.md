# TEAM_OPERATING_PROTOCOL

Last updated: 2026-03-18
Owner: Game Director (AI)
Applies to: `feature/ai-disassemble-builder`

## Purpose
Define how autonomous team agents receive work, execute, verify, and report without flow breaks.

## Cadence
- Every 30 min: progress check + next assignment
- Every 2 hours: quality gate review (bug/economy/UX)
- Daily close: summarize shipped commits + set next-day priorities

## Task Dispatch Format (mandatory)
Each request must include:
1. Task
2. Scope (files/systems)
3. DoD (definition of done)
4. Evidence required (commit/log/screenshot/test output)
5. Next hook (what starts immediately after completion)

## Team Lanes & Outputs
### Systems Team
- Focus: build/disassemble economy, SRL sinks/sources
- Output: tuned values + rationale + exploit check
- DoD: no infinite SRL growth loop

### World Team
- Focus: map progression + portal integrity
- Output: map changes + portal validation log
- DoD: portal validator passes, progression path intact

### AI Content Team
- Focus: generation quality + safety constraints
- Output: prompt/fallback updates + edge-case handling
- DoD: malformed/abusive outputs under threshold

### UX Team
- Focus: DOS UI clarity and action feedback
- Output: copy/UI diff + refreshed screenshots
- DoD: lock reasons and key actions are unambiguous

### QA Team
- Focus: regression scenarios + runtime stability
- Output: pass/fail table + repro steps
- DoD: critical blockers = 0

## Reporting Protocol (mandatory)
On every completed task, report in channel with:
1. Completed task
2. Commit hash
3. Changed files
4. Verification result
5. Next task

## Priority Rule
Always pick highest-priority unchecked item from:
1. `ACTION_ITEMS.md`
2. `TASKS.md` (current sprint immediates)

## Validation Gates Before Commit
- Syntax/lint checks for touched files
- Portal validation if map files changed
- Screenshot refresh if visible UI changed
- Do not commit secrets; keep `.env*` excluded

## Release Gates (must remain visible)
1. No infinite farm loop in SRL economy
2. 30-minute progression momentum remains positive
3. New player can complete one build within 5 minutes
4. No crash/progression blocker in default loop
