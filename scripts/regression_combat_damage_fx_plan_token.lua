-- Regression: compact combat FX remap-plan token (`DMG FX PLAN:HOLD_FX|MICRO_TUNE_FX|SYNC_WITH_GLYPH`)
-- Run: DOTPIO_EXPERIMENT_DMG_FX_PLAN_DEBUG=1 lua scripts/regression_combat_damage_fx_plan_token.lua

local Combat = require("src.combat")
local HUD = require("src.hud")
local Map = require("src.map")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

Map.load("01")
Combat.reset()

local function expectPlan(expected)
    local token = HUD.resolveDamageFxPlanToken()
    expect(token == ("DMG FX PLAN:" .. expected), string.format("expected %s, got %s", expected, tostring(token)))
end

local enemy = { hp = 999, alive = true }
local function enemyAt(tx, ty)
    if tx == 2 and ty == 1 and enemy.alive then
        return 1, enemy
    end
    return nil, nil
end

-- baseline (no active damage numbers)
expectPlan("HOLD_FX")

-- BASIC => HOLD_FX
local lowPlayer = {
    x = 1,
    y = 1,
    aimAngle = 0,
    effectiveStats = { atk = 1, int = 1 },
    attackTimer = 0,
    attackDir = {0, 0},
}
enemy = { hp = 999, alive = true }
Combat.meleeAttack(lowPlayer, enemyAt)
expectPlan("HOLD_FX")

-- SPIKE => MICRO_TUNE_FX
local spikePlayer = {
    x = 1,
    y = 1,
    aimAngle = 0,
    effectiveStats = { atk = 10, int = 10 },
    attackTimer = 0,
    attackDir = {0, 0},
}
enemy = { hp = 999, alive = true }
Combat.meleeAttack(spikePlayer, enemyAt)
expectPlan("MICRO_TUNE_FX")

-- OVERDRIVE (lethal) => SYNC_WITH_GLYPH
enemy = { hp = 1, alive = true }
Combat.meleeAttack(spikePlayer, enemyAt)
expectPlan("SYNC_WITH_GLYPH")

print("[PASS] combat damage FX plan token regression validated")
