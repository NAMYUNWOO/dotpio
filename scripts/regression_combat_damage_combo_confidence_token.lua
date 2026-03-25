-- Regression: combo confidence debug token (`DMG COMBO CONF:LOW|MID|HIGH`)
-- Run: DOTPIO_EXPERIMENT_DMG_COMBO_DEBUG=1 DOTPIO_EXPERIMENT_DMG_COMBO_CONF_DEBUG=1 lua scripts/regression_combat_damage_combo_confidence_token.lua

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

local function enemyFactory(hp)
    local enemy = { hp = hp, alive = true }
    return enemy, function(tx, ty)
        if tx == 2 and ty == 1 and enemy.alive then
            return 1, enemy
        end
        return nil, nil
    end
end

local player = {
    x = 1,
    y = 1,
    aimAngle = 0,
    effectiveStats = { str = 5, dex = 4, int = 3 },
    attackTimer = 0,
    attackDir = {0, 0},
}

expect(HUD.resolveDamageComboConfidenceToken() == "DMG COMBO CONF:LOW", "expected LOW confidence baseline")

for i = 1, 3 do
    local enemy, enemyAt = enemyFactory(1)
    Combat.meleeAttack(player, enemyAt)
    expect(enemy.alive == false, string.format("enemy %d should be slain", i))
end

local high = HUD.resolveDamageComboConfidenceToken()
expect(high == "DMG COMBO CONF:HIGH", string.format("expected HIGH confidence token, got %s", tostring(high)))

Combat.update(3.05, function() return nil, nil end)
local low = HUD.resolveDamageComboConfidenceToken()
expect(low == "DMG COMBO CONF:LOW", string.format("expected LOW confidence after cooldown, got %s", tostring(low)))

print("[PASS] combat damage combo confidence token regression validated")
