-- Regression: compact floating damage-number lifecycle confidence token (`DMGNUM LIFE CONF:LOW|MID|HIGH`)
-- Run: DOTPIO_EXPERIMENT_DMGNUM_LIFE_CONF_DEBUG=1 lua scripts/regression_combat_damage_number_life_confidence_token.lua

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

local function expectConfidence(expected)
    local token = HUD.resolveDamageNumberLifeConfidenceToken()
    expect(token == ("DMGNUM LIFE CONF:" .. expected), string.format("expected %s, got %s", expected, tostring(token)))
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

-- baseline with no active damage numbers
expectConfidence("HIGH")

-- Fresh hit should be HIGH confidence.
enemy = { hp = 999, alive = true }
Combat.meleeAttack(player, enemyAt)
expectConfidence("HIGH")

-- Mid-fade should map MID confidence.
Combat.update(0.30)
expectConfidence("MID")

-- Late fade should map LOW confidence.
Combat.update(0.21)
expectConfidence("LOW")

-- Expired numbers reset to baseline.
Combat.update(0.20)
expectConfidence("HIGH")

print("[PASS] combat damage-number lifecycle confidence token regression validated")
