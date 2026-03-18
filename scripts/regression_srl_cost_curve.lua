-- Regression: SRL cost curve tuning should penalize low-tier churn recipes.
-- Run: lua scripts/regression_srl_cost_curve.lua

package.path = "./?.lua;./?/init.lua;" .. package.path

_G.love = _G.love or {}
love.filesystem = love.filesystem or {}

function love.filesystem.read(path)
    local f = assert(io.open(path, "rb"))
    local data = f:read("*a")
    f:close()
    return data
end

local Items = require("src.items")
local Inventory = require("src.inventory")
local InventoryUI = require("src.inventory_ui")

local function fail(msg)
    io.stderr:write("[FAIL] " .. msg .. "\n")
    os.exit(1)
end

local function expect(condition, msg)
    if not condition then fail(msg) end
end

local function pickItems(predicate, n)
    local picked = {}
    for _, itemId in ipairs(Items.allItemIds) do
        if itemId ~= "builder_scroll" then
            local def = Items.get(itemId)
            if def and predicate(def) then
                picked[#picked + 1] = itemId
                if #picked >= n then break end
            end
        end
    end
    return picked
end

local function buildPlanFor(itemIds)
    local inv = Inventory.new()
    inv.currentDir = inv.root
    for _, itemId in ipairs(itemIds) do
        local ok, err = Inventory.addItem(inv, itemId, 1)
        expect(ok, "Failed to seed item " .. tostring(itemId) .. ": " .. tostring(err))
    end
    local consumed, builderCost, requiredCount = InventoryUI.debugGetBuildPlan(inv, inv.currentDir)
    return consumed, builderCost, requiredCount
end

Items.loadFromJson()

local lowTier = pickItems(function(def)
    return def.size <= 1 and def.stackable and (def.category == "coin" or def.category == "gem" or def.category == "potion" or def.category == "scroll" or def.category == "misc")
end, 3)
expect(#lowTier == 3, "Need 3 low-tier salvage-like items for regression")

local premium = pickItems(function(def)
    return def.size >= 3 and (not def.stackable) and (def.category == "weapon" or def.category == "armor" or def.category == "shield" or def.category == "robe" or def.category == "box")
end, 3)
expect(#premium == 3, "Need 3 premium non-stackable items for regression")

local lowConsumed, lowCost, lowRequired = buildPlanFor(lowTier)
local highConsumed, highCost, highRequired = buildPlanFor(premium)

expect(#lowConsumed >= lowRequired, "Low-tier recipe should be actionable in seeded fixture")
expect(lowCost >= 6, "Low-tier churn recipe should cost at least 6 BUILDER.SRL, got " .. tostring(lowCost))
expect(highCost >= 3, "Premium recipe unexpectedly too cheap, got " .. tostring(highCost))
expect(lowCost >= highCost, string.format("Low-tier churn should not be cheaper than premium recipe (low=%d high=%d)", lowCost, highCost))

print(string.format("[PASS] srl cost curve regression validated (low=%d high=%d)", lowCost, highCost))
