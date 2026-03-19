local Inventory = require("src.inventory")
local Items = require("src.items")

local FailForward = {}

local function clamp(value, minValue, maxValue)
    if value < minValue then return minValue end
    if value > maxValue then return maxValue end
    return value
end

local function firstCategoryId(category)
    local ids = Items.getIdsByCategory(category)
    return (ids and ids[1]) or nil
end

local function findTopDir(inv, name)
    if not inv or not inv.root then return nil end
    for _, child in ipairs(inv.root.children or {}) do
        if child.type == "dir" and child.name == name then
            return child
        end
    end
    return nil
end

local function addToDir(inv, dirName, itemId, count)
    if not inv or not itemId or (count or 0) <= 0 then
        return 0
    end

    local originalDir = inv.currentDir
    inv.currentDir = findTopDir(inv, dirName) or inv.root

    local added = 0
    local remaining = math.floor(count)
    while remaining > 0 do
        local ok = Inventory.addItem(inv, itemId, 1)
        if not ok then
            break
        end
        added = added + 1
        remaining = remaining - 1
    end

    inv.currentDir = originalDir
    return added
end

function FailForward.compute(inv, missionState)
    if not inv then
        return nil
    end

    local missionsDone = (missionState and missionState.doneCount) or 0
    local missionsTotal = (missionState and missionState.total) or 0

    local builderCount = Inventory.countItemById(inv, "builder_scroll")
    local coinId = firstCategoryId("coin")
    local gemId = firstCategoryId("gem")

    local coinCount = coinId and Inventory.countItemById(inv, coinId) or 0
    local gemCount = gemId and Inventory.countItemById(inv, gemId) or 0

    local carrySrl = clamp(math.floor(builderCount * 0.2) + missionsDone, 0, 8)
    local carryCoins = clamp(math.floor(coinCount * 0.12) + missionsDone * 2, 0, 25)
    local carryGems = clamp(math.floor(gemCount * 0.2), 0, 3)

    if carrySrl <= 0 and carryCoins <= 0 and carryGems <= 0 then
        return {
            carrySrl = 0,
            carryCoins = 0,
            carryGems = 0,
            missionsDone = missionsDone,
            missionsTotal = missionsTotal,
            coinId = coinId,
            gemId = gemId,
        }
    end

    return {
        carrySrl = carrySrl,
        carryCoins = carryCoins,
        carryGems = carryGems,
        missionsDone = missionsDone,
        missionsTotal = missionsTotal,
        coinId = coinId,
        gemId = gemId,
    }
end

function FailForward.apply(inv, reward)
    if not inv or not reward then
        return { srl = 0, coins = 0, gems = 0 }
    end

    local appliedSrl = addToDir(inv, "SCROLLS", "builder_scroll", reward.carrySrl or 0)
    local appliedCoins = addToDir(inv, "POTIONS", reward.coinId, reward.carryCoins or 0)
    local appliedGems = addToDir(inv, "POTIONS", reward.gemId, reward.carryGems or 0)

    return {
        srl = appliedSrl,
        coins = appliedCoins,
        gems = appliedGems,
    }
end

function FailForward.formatStatus(applied)
    local srl = (applied and applied.srl) or 0
    local coins = (applied and applied.coins) or 0
    local gems = (applied and applied.gems) or 0

    if srl <= 0 and coins <= 0 and gems <= 0 then
        return "RUN RESET: NO CARRYOVER"
    end

    return string.format("RUN RESET: CARRYOVER +%d BUILDER.SRL +%d COIN +%d GEM", srl, coins, gems)
end

return FailForward
