-- Regression: starter loadout tuning sanity
-- Run: lua scripts/regression_starter_loadout.lua

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
local Player = require("src.player")
local Inventory = require("src.inventory")

local function fail(msg)
    io.stderr:write("[FAIL] " .. msg .. "\n")
    os.exit(1)
end

local function expect(condition, msg)
    if not condition then fail(msg) end
end

local function dirByName(inv, name)
    for _, child in ipairs(inv.root.children) do
        if child.type == "dir" and child.name == name then
            return child
        end
    end
end

Items.loadFromJson()
Player.inventory = nil
Player.init(1, 1)

local inv = Player.inventory
expect(inv ~= nil, "Player inventory should be initialized")

local builderCount = Inventory.countItemById(inv, "builder_scroll")
expect(builderCount >= 18, string.format("Expected >=18 BUILDER.SRL, got %d", builderCount))

local scrollDir = dirByName(inv, "SCROLLS")
local potionDir = dirByName(inv, "POTIONS")
local weaponDir = dirByName(inv, "WEAPONS")
expect(scrollDir ~= nil and potionDir ~= nil and weaponDir ~= nil, "Default folders missing")

expect(#Inventory.getFilesInDir(scrollDir) >= 2, "SCROLLS should have starter files")
expect(#Inventory.getFilesInDir(potionDir) >= 4, "POTIONS should have mixed starter files")
expect(#Inventory.getFilesInDir(weaponDir) >= 10, "WEAPONS should have broad build candidates")

expect(inv.currentDir == inv.root, "Current directory should reset to root after seeding")

print(string.format("[PASS] starter loadout regression validated (BUILDER.SRL=%d)", builderCount))
