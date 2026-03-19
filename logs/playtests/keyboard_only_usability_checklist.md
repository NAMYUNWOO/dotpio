# Keyboard-only Usability Checklist

Generated: 2026-03-19 11:43:30 KST

## Scripted pass/fail
- [x] keyboard shortcut wiring/help text coverage
  - [PASS] keyboard shortcut wiring/help regression validated
- [x] disabled actions keep explicit lock reasons
  - [PASS] action menu lock reason regression validated
- [x] onboarding strip still guides keyboard-first progression
  - regression_onboarding_hints: PASS
- [x] build preview/confirm keyboard flow remains available
  - [PASS] build preview/confirm regression validated

## Manual keyboard-only quick pass
- [ ] Start run without mouse input and complete move/search/pickup/inventory/build sequence.
- [ ] In inventory, use only keyboard to navigate panels, open Action Menu, and execute U/E/D/S/X quick actions.
- [ ] Confirm lock reasons are readable without attempting disabled actions.
- [ ] Confirm help dialog (F1) includes all critical keys (F1/F5/F9/Tab/I/G).
- [ ] Confirm inventory can be closed/reopened with keyboard (Esc/F10 + Tab/I) and gameplay resumes cleanly.

Result: PASS
