-- Regression: compact floating damage-number lifecycle confidence trend token (`DMGNUM LIFE TREND:UP|HOLD|DOWN`)
-- Run: DOTPIO_EXPERIMENT_DMGNUM_LIFE_CONF_DEBUG=1 DOTPIO_EXPERIMENT_DMGNUM_LIFE_CONF_DELTA_DEBUG=1 DOTPIO_EXPERIMENT_DMGNUM_LIFE_TREND_DEBUG=1 lua scripts/regression_combat_damage_number_life_trend_token.lua

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

local function expectTrend(expected)
    local token = HUD.resolveDamageNumberLifeTrendToken()
    expect(token == ("DMGNUM LIFE TREND:" .. expected), string.format("expected %s, got %s", expected, tostring(token)))
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

-- baseline starts at HOLD
expectTrend("HOLD")

-- Fresh hit remains HIGH confidence, so trend stays HOLD.
enemy = { hp = 999, alive = true }
Combat.meleeAttack(player, enemyAt)
expectTrend("HOLD")

-- Mid-fade transitions HIGH -> MID = DOWN.
Combat.update(0.30)
expectTrend("DOWN")

-- Late-fade transitions MID -> LOW = DOWN.
Combat.update(0.21)
expectTrend("DOWN")

-- Expire transitions LOW -> HIGH baseline = UP.
Combat.update(0.20)
expectTrend("UP")

print("[PASS] combat damage-number lifecycle trend token regression validated")
