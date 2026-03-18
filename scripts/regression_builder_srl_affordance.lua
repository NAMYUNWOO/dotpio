-- Regression: BUILDER.SRL affordance copy appears on lock/status paths
-- Run: lua scripts/regression_builder_srl_affordance.lua

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
    if itemId ~= "builder_scroll" then
        local ok, err = Inventory.addItem(inv, itemId, 1)
        expect(ok, "Failed to seed item " .. itemId .. ": " .. tostring(err))
        seeded = seeded + 1
        if seeded >= 8 then break end
    end
end
expect(seeded >= 8, "Need at least 8 non-builder items for build-lock copy test")

local targetItem = nil
for _, node in ipairs(inv.root.children) do
    if node.type == "file" and node.itemId ~= "builder_scroll" and not node.isHeroFile then
        targetItem = node
        break
    end
end
expect(targetItem ~= nil, "Expected at least one disassemble target item")

local player = {inventory = inv, recalcStats = function() end}
InventoryUI.open(player, {items = {}})

local lastStatus = ""
local originalSetStatus = InventoryUI.setStatus
InventoryUI.setStatus = function(msg)
    lastStatus = msg or ""
    originalSetStatus(msg)
end

InventoryUI.disassembleItem(targetItem)
expect(lastStatus:find("BUILDER.SRL", 1, true) ~= nil, "Disassemble lock message should mention BUILDER.SRL")

InventoryUI.buildCurrentFolder()
expect(lastStatus:find("BUILDER.SRL", 1, true) ~= nil, "Build lock message should mention BUILDER.SRL")

InventoryUI.setStatus = originalSetStatus

print("[PASS] BUILDER.SRL affordance copy regression validated")
