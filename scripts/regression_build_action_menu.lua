-- Regression: folder action menu exposes build as primary flow and keeps preview confirm gate
-- Run: lua scripts/regression_build_action_menu.lua

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

local function nonBuilderTotalInDir(dir)
    local total = 0
    for _, node in ipairs(dir.children) do
        if node.type == "file" and node.itemId ~= "builder_scroll" then
            total = total + (node.count or 1)
        end
    end
    return total
end

Items.loadFromJson()

local inv = Inventory.new()
inv.currentDir = inv.root

local okFolder, folderErr = Inventory.createFolder(inv, "BUILD")
expect(okFolder, "Failed to create build folder: " .. tostring(folderErr))

local buildDir = nil
for _, child in ipairs(inv.root.children) do
    if child.type == "dir" and child.name == "BUILD" then
        buildDir = child
        break
    end
end
expect(buildDir ~= nil, "Expected BUILD folder node")

local seeded = {}
for _, itemId in ipairs(Items.allItemIds) do
    if itemId ~= "builder_scroll" then
        local ok, err = Inventory.addItem(inv, itemId, 1)
        expect(ok, "Failed to seed item " .. itemId .. ": " .. tostring(err))
        seeded[#seeded + 1] = itemId
        if #seeded >= 3 then break end
    end
end
expect(#seeded >= 3, "Need at least 3 non-builder items for build test")

for _, node in ipairs(inv.root.children) do
    if node.type == "file" and node.itemId ~= "builder_scroll" and not node.isHeroFile then
        local okMove, moveErr = Inventory.moveItem(inv, node, buildDir)
        expect(okMove, "Failed to move test item into BUILD folder: " .. tostring(moveErr))
    end
end

local okBuilder, errBuilder = Inventory.addItem(inv, "builder_scroll", 8)
expect(okBuilder, "Failed to seed BUILDER.SRL: " .. tostring(errBuilder))

local player = {inventory = inv, recalcStats = function() end}
InventoryUI.open(player, {items = {}})

local menu = InventoryUI.buildDirectoryActionMenu(buildDir)
local byAction = {}
for _, entry in ipairs(menu) do
    byAction[entry.action] = entry
end
expect(byAction.open_dir and byAction.open_dir.enabled, "Directory action menu should include OPEN")
expect(byAction.build_dir and byAction.build_dir.enabled, "Directory action menu should include enabled BUILD when requirements are met")

local originalGenerateBuild = AiDescribe.generateBuild
AiDescribe.generateBuild = function(folderName, componentIds)
    return seeded[1], "regression output"
end

inv.currentDir = buildDir
local builderBeforePrompt = Inventory.countItemById(inv, "builder_scroll")
local filesBeforePrompt = nonBuilderTotalInDir(buildDir)

InventoryUI.promptBuildPreview()

local builderAfterPrompt = Inventory.countItemById(inv, "builder_scroll")
local filesAfterPrompt = nonBuilderTotalInDir(buildDir)
expect(builderAfterPrompt == builderBeforePrompt, "Menu build preview should not consume SRL before confirm")
expect(filesAfterPrompt == filesBeforePrompt, "Menu build preview should not consume components before confirm")

InventoryUI.keypressed("return")

local builderAfterConfirm = Inventory.countItemById(inv, "builder_scroll")
local filesAfterConfirm = nonBuilderTotalInDir(buildDir)
expect(builderAfterConfirm < builderBeforePrompt, "Build confirm should consume SRL")
expect(filesAfterConfirm < filesBeforePrompt, "Build confirm should consume build components")

AiDescribe.generateBuild = originalGenerateBuild

print("[PASS] build action-menu primary flow regression validated")
