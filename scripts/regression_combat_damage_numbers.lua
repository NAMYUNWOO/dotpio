-- Combat floating damage-number lifecycle regression
-- Run: lua scripts/regression_combat_damage_numbers.lua

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

local enemy = { hp = 12, alive = true }
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
    effectiveStats = { str = 5, dex = 4, int = 3 },
    attackTimer = 0,
    attackDir = {0, 0},
}

Combat.meleeAttack(player, enemyAt)
local afterMelee = Combat.debugGetDamageNumbers()
expect(#afterMelee == 1, "melee hit should emit one floating damage number")
expect(afterMelee[1].magic == false, "melee hit damage number should be flagged non-magic")
expect(afterMelee[1].lethal == false, "non-lethal melee hit should not mark lethal damage number")
expect(afterMelee[1].amount >= 1, "melee floating damage amount should be positive")

Combat.update(0.31, enemyAt)
local midFade = Combat.debugGetDamageNumbers()
expect(#midFade == 1, "damage number should persist before full duration elapses")
expect(midFade[1].timer < afterMelee[1].timer, "damage number timer should decay over updates")

Combat.update(0.4, enemyAt)
expect(#Combat.debugGetDamageNumbers() == 0, "damage number should expire after duration")

local mage = {
    x = 1,
    y = 1,
    mp = 99,
    effectiveStats = { int = 10, str = 2, dex = 2 },
}
enemy = { hp = 99, alive = true }

Combat.castMagic(mage, 2, 1)
Combat.update(0.16, enemyAt)
local afterMagic = Combat.debugGetDamageNumbers()
expect(#afterMagic == 1, "magic projectile impact should emit one floating damage number")
expect(afterMagic[1].magic == true, "magic hit damage number should be flagged magic")
expect(afterMagic[1].lethal == false, "non-lethal magic hit should not mark lethal damage number")
expect(afterMagic[1].amount >= 1, "magic floating damage amount should be positive")

enemy = { hp = 1, alive = true }
Combat.meleeAttack(player, enemyAt)
local lethalMelee = Combat.debugGetDamageNumbers()
expect(#lethalMelee == 2, "lethal melee hit should append another damage number entry")
expect(lethalMelee[#lethalMelee].lethal == true, "lethal melee hit should mark floating number as lethal")

enemy = { hp = 1, alive = true }
Combat.castMagic(mage, 2, 1)
Combat.update(0.16, enemyAt)
local lethalMagic = Combat.debugGetDamageNumbers()
expect(lethalMagic[#lethalMagic].magic == true, "latest lethal magic hit should remain magic-typed")
expect(lethalMagic[#lethalMagic].lethal == true, "lethal magic hit should mark floating number as lethal")

print("[PASS] combat floating damage-number lifecycle regression validated")
