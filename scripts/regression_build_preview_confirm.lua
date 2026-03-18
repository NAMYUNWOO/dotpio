-- Regression: F9 build preview/confirm gate behavior
-- Run: lua scripts/regression_build_preview_confirm.lua

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
local AiDescribe = require("src.ai_describe")

local function fail(msg)
    io.stderr:write("[FAIL] " .. msg .. "\n")
    os.exit(1)
end

local function expect(condition, msg)
    if not condition then fail(msg) end
end

local function nonBuilderTotal(inv)
    local total = 0
    for _, node in ipairs(inv.root.children) do
        if node.type == "file" and node.itemId ~= "builder_scroll" then
            total = total + (node.count or 1)
        end
    end
    return total
end

Items.loadFromJson()

local inv = Inventory.new()
inv.currentDir = inv.root

local seeded = {}
for _, itemId in ipairs(Items.allItemIds) do
    if itemId ~= "builder_scroll" then
        seeded[#seeded + 1] = itemId
        local ok, err = Inventory.addItem(inv, itemId, 1)
        expect(ok, "Failed to seed item " .. itemId .. ": " .. tostring(err))
        if #seeded >= 4 then break end
    end
end
expect(#seeded >= 3, "Need at least 3 non-builder items for build test")

local okBuilder, errBuilder = Inventory.addItem(inv, "builder_scroll", 8)
expect(okBuilder, "Failed to seed BUILDER.SRL: " .. tostring(errBuilder))

local player = {inventory = inv, recalcStats = function() end}
InventoryUI.open(player, {items = {}})

local originalGenerateBuild = AiDescribe.generateBuild
AiDescribe.generateBuild = function(folderName, componentIds)
    return seeded[1], "regression output"
end

local builderBeforePrompt = Inventory.countItemById(inv, "builder_scroll")
local filesBeforePrompt = nonBuilderTotal(inv)

InventoryUI.keypressed("f9")

local builderAfterPrompt = Inventory.countItemById(inv, "builder_scroll")
local filesAfterPrompt = nonBuilderTotal(inv)
expect(builderAfterPrompt == builderBeforePrompt, "F9 preview should not consume SRL before confirm")
expect(filesAfterPrompt == filesBeforePrompt, "F9 preview should not consume components before confirm")

InventoryUI.keypressed("return")

local builderAfterConfirm = Inventory.countItemById(inv, "builder_scroll")
local filesAfterConfirm = nonBuilderTotal(inv)
expect(builderAfterConfirm < builderBeforePrompt, "Build confirm should consume SRL")
expect(filesAfterConfirm < filesBeforePrompt, "Build confirm should consume build components")

AiDescribe.generateBuild = originalGenerateBuild

print("[PASS] build preview/confirm regression validated")
