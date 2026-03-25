-- Regression: compact floating damage-number lifecycle trend FX token (`DMGNUM LIFE TREND FX:CALM|SPARK|BLAZE`)
-- Run: DOTPIO_EXPERIMENT_DMGNUM_LIFE_CONF_DEBUG=1 DOTPIO_EXPERIMENT_DMGNUM_LIFE_CONF_DELTA_DEBUG=1 DOTPIO_EXPERIMENT_DMGNUM_LIFE_TREND_DEBUG=1 DOTPIO_EXPERIMENT_DMGNUM_LIFE_TREND_FX_DEBUG=1 lua scripts/regression_combat_damage_number_life_trend_fx_token.lua

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

local function expectTrendFx(expected)
    local token = HUD.resolveDamageNumberLifeTrendFxToken()
    expect(token == ("DMGNUM LIFE TREND FX:" .. expected), string.format("expected %s, got %s", expected, tostring(token)))
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

-- baseline trend HOLD maps to SPARK.
expectTrendFx("SPARK")

-- Fresh hit confidence unchanged => HOLD => SPARK.
enemy = { hp = 999, alive = true }
Combat.meleeAttack(player, enemyAt)
expectTrendFx("SPARK")

-- Mid fade decreases confidence => DOWN => CALM.
Combat.update(0.30)
expectTrendFx("CALM")

-- Expire jumps LOW->HIGH => UP => BLAZE.
Combat.update(0.41)
expectTrendFx("BLAZE")

print("[PASS] combat damage-number lifecycle trend FX token regression validated")
