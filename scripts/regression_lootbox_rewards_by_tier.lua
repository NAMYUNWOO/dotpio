-- Regression: lootbox rewards should follow map-tier envelopes
-- Run: lua scripts/regression_lootbox_rewards_by_tier.lua

if not love then love = {} end
if not love.filesystem then
    love.filesystem = {
        read = function(path)
            local f = assert(io.open(path, "r"))
            local s = f:read("*a")
            f:close()
            return s
        end,
    }
end
if not love.math then love.math = {} end

-- deterministic RNG for stable distribution checks
local seed = 0xC0FFEE
local function lcg()
    seed = (1103515245 * seed + 12345) % 2147483648
    return seed / 2147483648
end

function love.math.random(a, b)
    local r = lcg()
    if not a then return r end
    if not b then return math.floor(r * a) + 1 end
    return math.floor(r * (b - a + 1)) + a
end

local Items = require("src.items")
local Entities = require("src.entities")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

local function pct(count, total)
    if total <= 0 then return 0 end
    return (count / total) * 100
end

Items.loadFromJson()

local lowItems = Entities.debugSampleLootboxItems("01", 1200)
local midItems = Entities.debugSampleLootboxItems("03", 1200)
local highItems = Entities.debugSampleLootboxItems("06", 1200)

local function summarize(items)
    local out = { total = #items, byCategory = {} }
    for _, itemId in ipairs(items) do
        local def = Items.get(itemId)
        if def then
            out.byCategory[def.category] = (out.byCategory[def.category] or 0) + 1
        end
    end
    return out
end

local low = summarize(lowItems)
local mid = summarize(midItems)
local high = summarize(highItems)

local lowCombat = (low.byCategory.weapon or 0) + (low.byCategory.armor or 0) + (low.byCategory.shield or 0)
local highCombat = (high.byCategory.weapon or 0) + (high.byCategory.armor or 0) + (high.byCategory.shield or 0)

local lowConsumables = (low.byCategory.potion or 0) + (low.byCategory.food or 0) + (low.byCategory.scroll or 0)
local highAccessories = (high.byCategory.ring or 0) + (high.byCategory.necklace or 0) + (high.byCategory.crown or 0)

expect(low.total >= 1000, "low-tier sample size too small")
expect(mid.total >= 1000, "mid-tier sample size too small")
expect(high.total >= 1000, "high-tier sample size too small")

expect(pct(lowCombat, low.total) <= 20, "low-tier should not over-drop combat gear")
expect(pct(lowConsumables, low.total) >= 45, "low-tier should prioritize consumables")

expect(pct(highCombat, high.total) >= 25, "high-tier should increase combat gear rewards")
expect(pct(highAccessories, high.total) >= 12, "high-tier should include accessories/crown rewards")

print("[PASS] lootbox reward tier regression validated")
