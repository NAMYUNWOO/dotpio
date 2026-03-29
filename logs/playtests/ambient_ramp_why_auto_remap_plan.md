# Ambient Ramp Why Auto-Remap Sandbox Plan

- GeneratedAt(UTC): 2026-03-29T21:19:43.818963Z
- Recommendation: **OPEN_CONTEXTUAL_WHY**
- Recommendation Confidence: **HIGH**
- Recommendation Parity: **SYNC**
- Selected Plan: **LIMITED_CONTEXT_EXPANSION**
- Compact Alias: **ARW AUTO PLAN:OPEN**
- Compact Rationale: **ARW AUTO WHY:OPEN_WINDOW**
- Rationale: drift-aware-candidate-rerank
- Next Action: Generate sandbox table + review notes; keep runtime contract unchanged.

## Candidate Table

| Rank | Plan | Risk | Offline Only | Scope | Summary | When to use |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | LIMITED_CONTEXT_EXPANSION | MID | TRUE | sandbox draft variants (no runtime wiring) | Prepare small contextual rationale variants for CALM windows with rollback checklist. | Use only in LOW drift + LOW pressure windows with HIGH confidence and SYNC parity. |
| 2 | HOLD_SAFE_BASELINE | LOW | TRUE | digest + sandbox notes only | Keep ambient rationale on SAFE-first deterministic wording with no runtime remap coupling. | Use by default in HIGH drift, HIGH pressure, or parity LOCK windows. |
| 3 | SHADOW_PRESSURE_REMIX | MID | TRUE | sandbox artifact + playtest checklist | Draft offline pressure-gated rationale remap table for manual review before any runtime use. | Use in MID risk windows when recommendation is PRESSURE_GATED_WHY and confidence is not LOW. |

- Safety note: artifact is digest/sandbox guidance only; runtime ambient rationale mapping remains unchanged.
