-- Regression: compact floating damage-number pulse remap-plan token (`DMGNUM LIFE TREND FX PULSE REMAP PLAN:HOLD|TUNE|SYNC`)
-- Run: DOTPIO_EXPERIMENT_DMGNUM_LIFE_CONF_DEBUG=1 DOTPIO_EXPERIMENT_DMGNUM_LIFE_CONF_DELTA_DEBUG=1 DOTPIO_EXPERIMENT_DMGNUM_LIFE_TREND_DEBUG=1 DOTPIO_EXPERIMENT_DMGNUM_LIFE_TREND_FX_PULSE_DEBUG=1 DOTPIO_EXPERIMENT_DMGNUM_LIFE_TREND_FX_PULSE_CONF_DEBUG=1 DOTPIO_EXPERIMENT_DMGNUM_LIFE_TREND_FX_PULSE_REMAP_PLAN_DEBUG=1 lua scripts/regression_combat_damage_number_life_trend_fx_pulse_remap_plan_token.lua

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
    local token = HUD.resolveDamageNumberLifeTrendFxPulseRemapPlanToken()
    expect(token == ("DMGNUM LIFE TREND FX PULSE REMAP PLAN:" .. expected), string.format("expected %s, got %s", expected, tostring(token)))
end

local enemy = { hp = 999, alive = true }
local function enemyAt(tx, ty)
    if tx == 2 and ty == 1 and enemy.alive then
        return 1, enemy
    end
    return nil, nil
end

local player = {
    x = 1,
    y = 1,
    aimAngle = 0,
    effectiveStats = { atk = 6, int = 6 },
    attackTimer = 0,
    attackDir = {0, 0},
}

-- Baseline pulse confidence LOW -> HOLD.
expectPlan("HOLD")

-- Mid fade confidence MID -> TUNE.
enemy = { hp = 999, alive = true }
Combat.meleeAttack(player, enemyAt)
Combat.update(0.30)
expectPlan("TUNE")

-- Late fade still MID confidence -> TUNE.
Combat.update(0.20)
expectPlan("TUNE")

-- Expire confidence HIGH -> SYNC.
Combat.update(0.11)
expectPlan("SYNC")

print("[PASS] combat damage-number lifecycle trend FX pulse remap-plan token regression validated")
