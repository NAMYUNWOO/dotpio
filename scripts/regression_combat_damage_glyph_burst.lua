-- Regression: damage-band glyph burst metadata (`DMG GLYPH:BASIC|SPIKE|OVERDRIVE`)
-- Run: DOTPIO_EXPERIMENT_DAMAGE_GLYPH_BURST=1 lua scripts/regression_combat_damage_glyph_burst.lua

local Combat = require("src.combat")
local Map = require("src.map")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

Map.load("01")
Combat.reset()

local enemy = { hp = 999, alive = true }
local function enemyAt(tx, ty)
    if tx == 2 and ty == 1 and enemy.alive then
        return 1, enemy
    end
    return nil, nil
end

local function latestBand()
    local nums = Combat.debugGetDamageNumbers()
    expect(#nums >= 1, "expected at least one damage number")
    return nums[#nums].glyphBand
end

-- BASIC: low-damage non-lethal hit
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
expect(latestBand() == "BASIC", "low non-lethal melee should map to BASIC glyph band")

-- SPIKE: mid-damage non-lethal hit
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
expect(latestBand() == "SPIKE", "mid non-lethal melee should map to SPIKE glyph band")

-- OVERDRIVE: lethal hit with high enough burst
enemy = { hp = 1, alive = true }
Combat.meleeAttack(spikePlayer, enemyAt)
expect(latestBand() == "OVERDRIVE", "lethal burst melee should map to OVERDRIVE glyph band")

print("[PASS] combat damage-glyph burst regression validated")
