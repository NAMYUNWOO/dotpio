-- Regression: drop -> pickup -> count validation
-- Run: lua scripts/regression_drop_pickup.lua

package.path = "./?.lua;./?/init.lua;" .. package.path

_G.love = _G.love or {}
love.filesystem = love.filesystem or {}
love.math = love.math or {}

function love.filesystem.read(path)
    local f = assert(io.open(path, "rb"))
    local data = f:read("*a")
    f:close()
    return data
end

function love.math.random(a, b)
    if not a then return math.random() end
    if not b then return math.random(a) end
    return math.random(a, b)
end

local Items = require("src.items")
local Inventory = require("src.inventory")
local Entities = require("src.entities")

local function fail(msg)
    io.stderr:write("[FAIL] " .. msg .. "\n")
    os.exit(1)
end

local function expectEq(actual, expected, label)
    if actual ~= expected then
        fail(string.format("%s (expected=%s actual=%s)", label, tostring(expected), tostring(actual)))
    end
end

Items.loadFromJson()

local inv = Inventory.new()
local itemId = Items.allItemIds[1]
if not itemId then
    fail("No item ids loaded from item_tile_data.json")
end

local ok = Inventory.addItem(inv, itemId, 1)
if not ok then
    fail("Unable to seed test inventory")
end
expectEq(Inventory.countItemById(inv, itemId), 1, "seed count")

Entities.reset()
local def = Items.get(itemId)
Entities.items[#Entities.items + 1] = {
    x = 10,
    y = 10,
    collected = false,
    gid = def.gid,
    itemId = itemId,
}

-- simulate inventory drop semantics (inventory_ui.doDrop)
local droppedNode
for _, child in ipairs(inv.currentDir.children) do
    if child.type == "file" and child.itemId == itemId then
        droppedNode = child
        break
    end
end
if not droppedNode then
    fail("Could not find item node to drop")
end
Inventory.removeItem(inv, droppedNode, droppedNode.count)
expectEq(Inventory.countItemById(inv, itemId), 0, "count after drop")

-- simulate pickup semantics (main.tryPickupItem)
local idx, mapItem = Entities.itemAt(10, 10)
if not idx or not mapItem then
    fail("Dropped map item missing before pickup")
end
local pickupOk = Inventory.addItem(inv, mapItem.itemId, 1)
if not pickupOk then
    fail("Pickup addItem failed")
end
mapItem.collected = true
Entities.removeItem(idx)

expectEq(Inventory.countItemById(inv, itemId), 1, "count after pickup")
expectEq(#Entities.items, 0, "world item cleanup after pickup")

print(string.format("[PASS] drop->pickup regression validated for %s", itemId))
