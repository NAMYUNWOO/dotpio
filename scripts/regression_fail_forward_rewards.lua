-- Regression: fail-forward carryover reward (currency/material)
-- Run: lua scripts/regression_fail_forward_rewards.lua

package.path = "./?.lua;./?/init.lua;" .. package.path

if not _G.love then _G.love = {} end
if not love.filesystem then love.filesystem = {} end
if not love.math then love.math = {} end

function love.filesystem.read(path)
    local f = assert(io.open(path, "r"))
    local content = f:read("*a")
    f:close()
    return content
end

function love.math.random(a, b)
    if a and b then return math.random(a, b) end
    if a then return math.random(a) end
    return math.random()
end

local Items = require("src.items")
local Inventory = require("src.inventory")
local FailForward = require("src.fail_forward")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

local function firstCategoryId(category)
    local ids = Items.getIdsByCategory(category)
    return (ids and ids[1]) or nil
end

Items.loadFromJson()

local inv = Inventory.new()
local coinId = firstCategoryId("coin")
local gemId = firstCategoryId("gem")
expect(coinId ~= nil, "coin item id should exist")
expect(gemId ~= nil, "gem item id should exist")

-- Seed extra run-state resources.
inv.currentDir = inv.root
Inventory.addItem(inv, "builder_scroll", 20)
Inventory.addItem(inv, coinId, 40)
Inventory.addItem(inv, gemId, 8)

local reward = FailForward.compute(inv, { doneCount = 2, total = 3 })
expect(reward.carrySrl == 6, "carry SRL formula/cap mismatch")
expect(reward.carryCoins == 8, "carry coin formula mismatch")
expect(reward.carryGems == 1, "carry gem formula mismatch")

local freshInv = Inventory.new()
local applied = FailForward.apply(freshInv, reward)

expect(applied.srl == 6, "applied SRL should match carry package")
expect(applied.coins == 8, "applied coins should match carry package")
expect(applied.gems == 1, "applied gems should match carry package")
expect(Inventory.countItemById(freshInv, "builder_scroll") == 6, "fresh inventory should receive carry SRL")
expect(Inventory.countItemById(freshInv, coinId) == 8, "fresh inventory should receive carry coins")
expect(Inventory.countItemById(freshInv, gemId) == 1, "fresh inventory should receive carry gem")

local status = FailForward.formatStatus(applied)
expect(status:find("CARRYOVER", 1, true) ~= nil, "status copy should mention carryover")

print("[PASS] fail-forward reward regression validated")
