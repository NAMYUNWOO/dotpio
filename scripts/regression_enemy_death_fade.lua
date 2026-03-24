-- Enemy death-fade timer regression
-- Run: lua scripts/regression_enemy_death_fade.lua

if not love then love = {} end
if not love.math then love.math = {} end
if not love.math.random then
    function love.math.random(a, b)
        if not a then return 0.5 end
        if not b then return 1 end
        return a
    end
end

local Entities = require("src.entities")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

Entities.enemies = {
    {
        x = 5,
        y = 5,
        alive = false,
        deathTimer = 0.4,
        behavior = "raider",
        hp = 0,
        maxHp = 3,
    }
}

local events = Entities.update(0.1, { x = 1, y = 1 }, nil)
expect(events.hits == 0 and events.dodges == 0, "death-fade update should not emit combat events")
expect(Entities.enemies[1].deathTimer and Entities.enemies[1].deathTimer < 0.4, "death timer should decay while enemy is dead")
expect(Entities.enemyAt(5, 5) == nil, "dead enemy in fade state must stay non-interactive")

Entities.update(0.35, { x = 1, y = 1 }, nil)
expect(Entities.enemies[1].deathTimer == nil, "death timer should clear after fade window elapses")

print("[PASS] enemy death fade timer regression validated")
