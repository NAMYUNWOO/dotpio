-- Regression: build output category diversity constraints
-- Run: lua scripts/regression_build_category_diversity.lua

if not love then love = {} end
if not love.filesystem then
    love.filesystem = {
        read = function(path)
            local f = assert(io.open(path, "r"))
            local s = f:read("*a")
            f:close()
            return s
        end,
    }
end
if not love.math then love.math = {} end
if not love.math.random then
    function love.math.random(a, b)
        if not a then return 0.5 end
        if not b then return 1 end
        return a
    end
end

local Items = require("src.items")
local AiDescribe = require("src.ai_describe")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

Items.loadFromJson()

local saturatedHistory = { "weapon", "weapon", "weapon", "armor", "weapon", "weapon" }
local shifted = AiDescribe.debugConstrainBuildCategory("weapon", { "weapon", "scroll" }, saturatedHistory)
expect(shifted.reason == "diversity-shift", "expected diversity shift when target is saturated")
expect(shifted.chosen ~= "weapon", "expected saturated target to move to another category")

local freshHistory = { "weapon", "armor", "ring" }
local keep = AiDescribe.debugConstrainBuildCategory("weapon", { "weapon", "bow" }, freshHistory)
expect(keep.reason == "target-ok", "expected target category to stay when not saturated")
expect(keep.chosen == "weapon", "expected chosen category to stay as weapon")

local unknown = AiDescribe.debugConstrainBuildCategory("nonexistent", { "unknown" }, saturatedHistory)
expect(unknown.chosen == "misc" or unknown.reason == "diversity-shift", "unknown categories should normalize safely")

local seeded = AiDescribe.debugResetBuildCategoryHistory({ "weapon", "weapon", "weapon", "weapon", "weapon", "weapon", "weapon" })
expect(seeded == 6, "history should clamp to rolling limit of 6")

print("[PASS] build category diversity regression validated")
