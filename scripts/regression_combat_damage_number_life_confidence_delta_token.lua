-- Regression: compact floating damage-number lifecycle confidence drift token (`DMGNUM LIFE CONF Δ:+n|-n`)
-- Run: DOTPIO_EXPERIMENT_DMGNUM_LIFE_CONF_DEBUG=1 DOTPIO_EXPERIMENT_DMGNUM_LIFE_CONF_DELTA_DEBUG=1 lua scripts/regression_combat_damage_number_life_confidence_delta_token.lua

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

local function expectDelta(expected)
    local token = HUD.resolveDamageNumberLifeConfidenceDeltaToken()
    expect(token == ("DMGNUM LIFE CONF Δ:" .. expected), string.format("expected %s, got %s", expected, tostring(token)))
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

-- baseline starts at +0
expectDelta("+0")

-- Fresh hit remains HIGH confidence, so drift stays zero.
enemy = { hp = 999, alive = true }
Combat.meleeAttack(player, enemyAt)
expectDelta("+0")

-- Mid-fade transitions HIGH -> MID = -1.
Combat.update(0.30)
expectDelta("-1")

-- Late-fade transitions MID -> LOW = -1.
Combat.update(0.21)
expectDelta("-1")

-- Expire transitions LOW -> HIGH baseline = +2.
Combat.update(0.20)
expectDelta("+2")

print("[PASS] combat damage-number lifecycle confidence delta token regression validated")
