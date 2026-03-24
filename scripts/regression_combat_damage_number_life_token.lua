-- Regression: compact floating damage-number lifecycle token (`DMGNUM LIFE:EARLY|MID|LATE`)
-- Run: DOTPIO_EXPERIMENT_DMGNUM_LIFE_DEBUG=1 lua scripts/regression_combat_damage_number_life_token.lua

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

local function expectLife(expected)
    local token = HUD.resolveDamageNumberLifeToken()
    expect(token == ("DMGNUM LIFE:" .. expected), string.format("expected %s, got %s", expected, tostring(token)))
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
expectLife("EARLY")

-- Fresh hit should be EARLY phase.
enemy = { hp = 999, alive = true }
Combat.meleeAttack(player, enemyAt)
expectLife("EARLY")

-- Mid-fade (about half-life) should map MID.
Combat.update(0.30)
expectLife("MID")

-- Late fade should map LATE.
Combat.update(0.21)
expectLife("LATE")

-- Expired numbers reset to baseline.
Combat.update(0.20)
expectLife("EARLY")

print("[PASS] combat damage-number lifecycle token regression validated")
