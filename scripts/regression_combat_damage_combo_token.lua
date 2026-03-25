-- Regression: compact kill-combo cadence token (`DMG COMBO:<n>x<HOT|WARM|COLD>`)
-- Run: DOTPIO_EXPERIMENT_DMG_COMBO_DEBUG=1 lua scripts/regression_combat_damage_combo_token.lua

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

expect(HUD.resolveDamageComboToken() == "DMG COMBO:0xCOLD", "expected cold baseline token")

for i = 1, 3 do
    local enemy, enemyAt = enemyFactory(1)
    Combat.meleeAttack(player, enemyAt)
    expect(enemy.alive == false, string.format("enemy %d should be slain", i))
end

local hot = HUD.resolveDamageComboToken()
expect(hot == "DMG COMBO:3xHOT", string.format("expected hot combo token, got %s", tostring(hot)))

Combat.update(3.05, function() return nil, nil end)
local cooled = HUD.resolveDamageComboToken()
expect(cooled == "DMG COMBO:0xCOLD", string.format("expected combo reset token, got %s", tostring(cooled)))

print("[PASS] combat damage combo token regression validated")
