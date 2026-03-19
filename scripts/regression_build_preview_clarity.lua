-- Regression: build preview exposes expected output category metadata
-- Run: lua scripts/regression_build_preview_clarity.lua

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

Items.loadFromJson()

local inv = Inventory.new()
inv.currentDir = inv.root

local seeded = 0
for _, itemId in ipairs(Items.allItemIds) do
    local def = Items.get(itemId)
    if itemId ~= "builder_scroll" and def and (def.category == "weapon" or def.category == "armor" or def.category == "shield") then
        local ok, err = Inventory.addItem(inv, itemId, 1)
        expect(ok, "Failed to seed item " .. itemId .. ": " .. tostring(err))
        seeded = seeded + 1
        if seeded >= 3 then break end
    end
end
expect(seeded >= 2, "Need at least 2 non-builder files for build preview")

local okBuilder, errBuilder = Inventory.addItem(inv, "builder_scroll", 8)
expect(okBuilder, "Failed to seed BUILDER.SRL: " .. tostring(errBuilder))

local player = {inventory = inv, recalcStats = function() end}
InventoryUI.open(player, {items = {}})
InventoryUI.keypressed("f9")

local plan = InventoryUI.debugGetBuildPreviewPlan()
expect(plan ~= nil, "Expected build preview plan to be available")
expect(type(plan.expectedCategory) == "string" and #plan.expectedCategory > 0, "Expected non-empty expectedCategory")
expect(plan.expectedCategory ~= "?", "Expected category should not be unknown marker")

print(string.format("[PASS] build preview clarity regression validated (expectedCategory=%s)", plan.expectedCategory))
