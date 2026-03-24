-- Regression: compact combat debug token (`DMG GLYPH LIVE:BASIC|SPIKE|OVERDRIVE`)
-- Run: DOTPIO_EXPERIMENT_DMG_GLYPH_LIVE_DEBUG=1 lua scripts/regression_combat_damage_glyph_live_token.lua

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

local function expectLive(expected)
    local token = HUD.resolveDamageGlyphLiveToken()
    expect(token == ("DMG GLYPH LIVE:" .. expected), string.format("expected %s, got %s", expected, tostring(token)))
end

local enemy = { hp = 999, alive = true }
local function enemyAt(tx, ty)
    if tx == 2 and ty == 1 and enemy.alive then
        return 1, enemy
    end
    return nil, nil
end

-- default with no active numbers should still render BASIC baseline
expectLive("BASIC")

-- BASIC
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
expectLive("BASIC")

-- SPIKE
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
expectLive("SPIKE")

-- OVERDRIVE (lethal)
enemy = { hp = 1, alive = true }
Combat.meleeAttack(spikePlayer, enemyAt)
expectLive("OVERDRIVE")

print("[PASS] combat damage-glyph live token regression validated")
