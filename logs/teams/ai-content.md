# AI Content Team Log


## 2026-03-19 06:46:23 KST
- Task: M2 add enemy behavior variants (skirmisher/bruiser/sentinel) with spawn mix + regression coverage.
- Commit: `HEAD (this run)`
- Files changed:
  - `src/enemy_ai.lua`
  - `src/entities.lua`
  - `scripts/regression_enemy_behavior_variants.lua`
  - `ACTION_ITEMS.md`
  - `TASKS.md`
- Verification:
  - `luac -p src/enemy_ai.lua src/entities.lua scripts/regression_enemy_behavior_variants.lua` ✅
  - `lua scripts/regression_enemy_behavior_variants.lua` ✅
- Decisions:
  - Added data-driven AI behavior profiles so variants change movement/aggro/flee/attack cadence without branching per-map scripts.
  - Spawn now mixes weighted variants with differentiated HP pools to increase encounter diversity in M2 maps.
- Follow-up:
  - Next M2 priority is AI build output category diversity constraints; keep new enemy pressure in mind when tuning output rewards.

## 2026-03-19 07:13:57 KST
- Task: M2 expand AI build output category diversity constraints.
- Commit: `HEAD (this run)`
- Files changed:
  - `src/ai_describe.lua`
  - `scripts/regression_build_category_diversity.lua`
  - `ACTION_ITEMS.md`
  - `TASKS.md`
- Verification:
  - `luac -p src/ai_describe.lua scripts/regression_build_category_diversity.lua` ✅
  - `lua scripts/regression_build_category_diversity.lua` ✅
- Decisions:
  - Added rolling build-category diversity guardrail (window=6, cap=3) so repeated AI target categories are auto-shifted to underused synergy categories when saturated.
  - Added component-category -> build-category mapping to keep diversity shifts thematically consistent instead of random fallback.
  - Added debug/regression hooks to lock constraint behavior and history window bounds.
- Follow-up:
  - Next M2 priority is reward table tuning by map tier; run economy/loot validation together with diversity guardrails.

## 2026-03-19 07:43:35 KST
- Task: M2 reward table pass for lootbox contents by map tier.
- Commit: `HEAD (this run)`
- Files changed:
  - `src/entities.lua`
  - `scripts/regression_lootbox_rewards_by_tier.lua`
  - `ACTION_ITEMS.md`
  - `TASKS.md`
- Verification:
  - `luac -p src/entities.lua scripts/regression_lootbox_rewards_by_tier.lua` ✅
  - `lua scripts/regression_lootbox_rewards_by_tier.lua` ✅
  - `lua scripts/regression_build_category_diversity.lua` ✅
- Decisions:
  - Added map-tiered loot reward profiles (tier1=consumable-heavy, tier2=balanced gear ramp, tier3=gear/accessory weighted) for lootbox item generation.
  - Excluded synthetic system items from lootbox drops and added deterministic distribution regression to lock tier envelopes.
- Follow-up:
  - Next M3 priority: run mission prototype (3 objectives).
