# Team Development Logs

Purpose: preserve continuity and execution context across autonomous runs.

## Log files
- `systems.md` - economy/build/disassemble logic + balancing decisions
- `world.md` - maps/portals/progression routing changes
- `ai-content.md` - prompt/output constraints/fallback behavior
- `ux.md` - DOS UI wording/interaction/feedback decisions
- `qa.md` - regression scenarios, pass/fail, repro steps

## Entry template (append-only)
For every completed task, append:

- Date/Time (KST)
- Task (link to milestone/action item)
- Commit hash
- Files changed
- Verification performed
- Decision notes (why this approach)
- Risks / Follow-ups

## Rules
- Append-only. Do not rewrite history entries.
- Keep entries concise and technical.
- If a run changes multiple domains, add entries to each relevant team file.
