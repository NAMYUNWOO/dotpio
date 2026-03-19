-- Regression: disabled action menu entries expose always-visible lock reasons
-- Run: lua scripts/regression_action_menu_lock_reasons.lua

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

local function findItemNode(dir, itemId)
    for _, child in ipairs(dir.children) do
        if child.type == "file" and child.itemId == itemId then
            return child
        end
    end
    return nil
end

Items.loadFromJson()

local inv = Inventory.new()
inv.currentDir = inv.root
local player = {inventory = inv}
InventoryUI.open(player, {items = {}})

-- Create an equippable non-consumable, non-stackable file with no BUILDER.SRL in bag.
local weaponIds = Items.getIdsByCategory("weapon")
expect(#weaponIds > 0, "Expected at least one weapon item id")
local testItemId = weaponIds[1]

local ok, err = Inventory.addItem(inv, testItemId, 1)
expect(ok, "Failed to seed test item: " .. tostring(err))
local gearNode = findItemNode(inv.root, testItemId)
expect(gearNode ~= nil, "Expected test weapon in inventory")

local menu = InventoryUI.buildActionMenu(gearNode)
expect(#menu >= 5, "Action menu should include core actions")

local byAction = {}
for _, entry in ipairs(menu) do
    byAction[entry.action] = entry
end

expect(byAction.use and not byAction.use.enabled, "USE should be disabled for non-consumable gear")
expect(byAction.use.label:find("LOCK:", 1, true) ~= nil, "USE disabled row should include inline LOCK reason")

expect(byAction.disassemble and byAction.disassemble.enabled == false, "DISASM should be disabled when BUILDER.SRL is missing")
expect(byAction.disassemble.label:find("LOCK:", 1, true) ~= nil, "DISASM disabled row should include inline LOCK reason")
expect(byAction.disassemble.label:find("BUILDER.SRL", 1, true) ~= nil, "DISASM lock reason should mention BUILDER.SRL")

expect(byAction.split and byAction.split.enabled == false, "SPLIT should be disabled for non-stackable item")
expect(byAction.split.label:find("LOCK:", 1, true) ~= nil, "SPLIT disabled row should include inline LOCK reason")

-- BUILDER.SRL should never be directly usable; it must guide player to BUILD flow.
local okBuilder, errBuilder = Inventory.addItem(inv, "builder_scroll", 1)
expect(okBuilder, "Failed to seed BUILDER.SRL: " .. tostring(errBuilder))
local builderNode = findItemNode(inv.root, "builder_scroll")
expect(builderNode ~= nil, "Expected BUILDER.SRL in inventory")

local builderMenu = InventoryUI.buildActionMenu(builderNode)
local builderByAction = {}
for _, entry in ipairs(builderMenu) do
    builderByAction[entry.action] = entry
end

expect(builderByAction.use and builderByAction.use.enabled == false, "USE should be disabled for BUILDER.SRL")
local builderUseLabelLower = string.lower(builderByAction.use.label or "")
expect(builderUseLabelLower:find("build%-only") ~= nil, "BUILDER.SRL USE lock should mention build-only guidance")
expect(builderUseLabelLower:find("b/enter%-%>build") ~= nil, "BUILDER.SRL USE lock should include B or Enter->BUILD guidance")

print("[PASS] action menu lock reason regression validated")
