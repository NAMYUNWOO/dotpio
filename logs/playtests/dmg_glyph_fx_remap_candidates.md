# DMG Glyph FX Remap Candidates

- GeneratedAt(UTC): 2026-03-31T04:46:51.370470Z
- Recommendation: **MICRO_TUNE_FX**
- Confidence: **HIGH**
- Rationale: stable-fx-window
- Guidance: Allow small offline-only FX remap suggestions; keep live mapping unchanged until validated.

## Candidate Table

| Rank | Mode | Risk | Offline Only | Summary | When to use |
| --- | --- | --- | --- | --- | --- |
| 1 | HOLD_FX | LOW | TRUE | Pin CALM/SPARK/BLAZE mapping and defer runtime remap edits. | Use during HIGH drift or high FX churn windows. |
| 2 | MICRO_TUNE_FX | MID | TRUE | Draft small offline FX remap options that keep glyph-band thresholds unchanged. | Use in stable windows with moderate churn. |
| 3 | SYNC_WITH_GLYPH | MID | TRUE | Draft offline FX remap candidates aligned to glyph-band momentum shifts. | Use when glyph churn rises while drift risk is not HIGH. |

- Selected candidate this window: **MICRO_TUNE_FX**
