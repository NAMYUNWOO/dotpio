# Ambient Ramp Why Auto-Remap Sandbox Plan

- GeneratedAt(UTC): 2026-03-25T08:06:06.793229Z
- Recommendation: **HOLD_SAFE_WHY**
- Recommendation Confidence: **MID**
- Recommendation Parity: **LOCK**
- Selected Plan: **HOLD_SAFE_BASELINE**
- Compact Alias: **ARW AUTO PLAN:HOLD**
- Compact Rationale: **ARW AUTO WHY:SAFE_LOCK**
- Rationale: safety-lock-from-confidence-or-parity
- Next Action: Generate sandbox table + review notes; keep runtime contract unchanged.

## Candidate Table

| Rank | Plan | Risk | Offline Only | Scope | Summary | When to use |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | HOLD_SAFE_BASELINE | LOW | TRUE | digest + sandbox notes only | Keep ambient rationale on SAFE-first deterministic wording with no runtime remap coupling. | Use by default in HIGH drift, HIGH pressure, or parity LOCK windows. |
| 2 | SHADOW_PRESSURE_REMIX | MID | TRUE | sandbox artifact + playtest checklist | Draft offline pressure-gated rationale remap table for manual review before any runtime use. | Use in MID risk windows when recommendation is PRESSURE_GATED_WHY and confidence is not LOW. |
| 3 | LIMITED_CONTEXT_EXPANSION | MID | TRUE | sandbox draft variants (no runtime wiring) | Prepare small contextual rationale variants for CALM windows with rollback checklist. | Use only in LOW drift + LOW pressure windows with HIGH confidence and SYNC parity. |

- Safety note: artifact is digest/sandbox guidance only; runtime ambient rationale mapping remains unchanged.
