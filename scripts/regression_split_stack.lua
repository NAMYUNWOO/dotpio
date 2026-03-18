-- Regression: inventory stack split behavior
-- Run: lua scripts/regression_split_stack.lua

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

local ok, err = Inventory.addItem(inv, "builder_scroll", 4)
expect(ok, "Failed to seed builder stack: " .. tostring(err))

local stackNode = nil
for _, child in ipairs(inv.root.children) do
    if child.type == "file" and child.itemId == "builder_scroll" then
        stackNode = child
        break
    end
end
expect(stackNode ~= nil, "BUILDER.SRL stack should exist")
expect(stackNode.count == 4, string.format("Expected stack count 4, got %s", tostring(stackNode.count)))

local splitOk, splitErr = Inventory.splitStack(inv, stackNode, 1)
expect(splitOk, "Split should succeed: " .. tostring(splitErr))
expect(stackNode.count == 3, string.format("Original stack should become 3, got %d", stackNode.count))

local stacks = {}
for _, child in ipairs(inv.root.children) do
    if child.type == "file" and child.itemId == "builder_scroll" then
        stacks[#stacks + 1] = child.count
    end
end

table.sort(stacks)
expect(#stacks == 2, string.format("Expected 2 builder stacks after split, got %d", #stacks))
expect(stacks[1] == 1 and stacks[2] == 3, string.format("Expected split counts {1,3}, got {%s,%s}", tostring(stacks[1]), tostring(stacks[2])))

local totalItems = Inventory.countItemById(inv, "builder_scroll")
expect(totalItems == 4, string.format("Total builder count should remain 4, got %d", totalItems))

local failOk = Inventory.splitStack(inv, stackNode, 3)
expect(failOk == false, "Split with full stack count should fail")

print("[PASS] stack split regression validated")
