-- Enemy behavior variant regression
-- Run: lua scripts/regression_enemy_behavior_variants.lua

if not love then love = {} end
if not love.math then love.math = {} end
if not love.math.random then
    function love.math.random(a, b)
        if not a then return 0.5 end
        if not b then return 1 end
        return a
    end
end

local EnemyAI = require("src.enemy_ai")
local Entities = require("src.entities")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

local variantRoster = Entities.getEnemyBehaviorVariants()
expect(#variantRoster >= 4, "expected at least 4 spawn variants including baseline")

local byName = {}
for _, name in ipairs(variantRoster) do byName[name] = true end
expect(byName.skirmisher and byName.bruiser and byName.sentinel, "missing required behavior variants")

local probe = {
    raider = { x = 1, y = 1, behavior = "raider", hp = 3, alive = true },
    skirmisher = { x = 1, y = 1, behavior = "skirmisher", hp = 3, alive = true },
    bruiser = { x = 1, y = 1, behavior = "bruiser", hp = 3, alive = true },
    sentinel = { x = 1, y = 1, behavior = "sentinel", hp = 3, alive = true },
}

for _, enemy in pairs(probe) do EnemyAI.init(enemy, 1) end

expect(probe.skirmisher.moveCd < probe.raider.moveCd, "skirmisher should move faster than raider")
expect(probe.bruiser.atkDmg > probe.raider.atkDmg, "bruiser should hit harder than raider")
expect(probe.sentinel.leashRadius ~= nil, "sentinel should have leash radius")
expect(probe.skirmisher.retreatAfterHit == true, "skirmisher should retreat after hit")

print("[PASS] enemy behavior variants regression validated")
