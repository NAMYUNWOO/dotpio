# Urgency Parity + Urgency FX Compact Prompt Budget Validation

Date: 2026-03-24 12:05 KST
Scope: Validate compact prompt budget impact when both urgency parity and urgency FX are enabled.

## Flags enabled
- `DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF_URGENCY=1`
- `DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF_URGENCY_PARITY=1`
- `DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF_URGENCY_FX=1`
- Supporting portal/vibe/route-glow flags required by regression harness.

## Verification commands
1. `... lua scripts/regression_portal_route_glow_fx_conf_why_rail_intensity_why_conf_urgency_parity.lua` ✅
2. `... lua scripts/regression_portal_route_glow_fx_conf_why_rail_intensity_why_conf_urgency_fx.lua` ✅
3. `... lua scripts/check_portal_prompt_copy_budget.lua 76` ✅

## Budget result
- Budget checker status: **WARN**
- Budget: **76 chars**
- Checked prompts: **20**
- Max observed: **87 chars** (`map_06 -> map_07 [SPIKE]`, +11)
- Over-budget prompts: **20/20**

Artifacts:
- `logs/playtests/portal_prompt_copy_budget.md`
- `logs/playtests/portal_prompt_copy_budget.json`

## Prompt snapshots (playtest capture)
(Generated via direct prompt render under enabled flags)

- SAFE (`len=411`)
  - `... RGFXWRIU:LOW  ROUTE GLOW FX CONF WHY RAIL INTENSITY WHY CONF URGENCY:LOW  RGFXWRIUFX:CALM`
- RISK (`len=414`)
  - `... RGFXWRIU:MID  ROUTE GLOW FX CONF WHY RAIL INTENSITY WHY CONF URGENCY:MID  RGFXWRIUFX:SPARK`
- SPIKE (`len=434`)
  - `... RGFXWRIU:HIGH  ROUTE GLOW FX CONF WHY RAIL INTENSITY WHY CONF URGENCY:HIGH  RGFXWRIUFX:BLAZE ...`

## QA/UX notes
- Urgency parity + urgency FX tokens render correctly and regressions stay green.
- Compact budget pressure remains unresolved at 76-char threshold when full token stack is active.
- Practical impact: prompt readability now depends on compact fallback/token-priority behavior rather than budget pass status.
