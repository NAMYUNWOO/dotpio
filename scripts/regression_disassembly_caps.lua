-- Regression: disassembly stack/size caps scale fairly by item size tiers.
-- Run: lua scripts/regression_disassembly_caps.lua

package.path = "./?.lua;./?/init.lua;" .. package.path

_G.love = _G.love or {}
love.thread = love.thread or {}
love.math = love.math or {}

function love.thread.getChannel()
    return {
        push = function() end,
        pop = function() return nil end,
    }
end

function love.thread.newThread()
    return {
        start = function() end,
        isRunning = function() return true end,
    }
end

function love.math.random(a, b)
    if a and b then return a end
    return 1
end

local AiDescribe = require("src.ai_describe")

local function fail(msg)
    io.stderr:write("[FAIL] " .. msg .. "\n")
    os.exit(1)
end

local function expect(cond, msg)
    if not cond then fail(msg) end
end

local tiny = AiDescribe.debugDisassemblyLimits(1)
local medium = AiDescribe.debugDisassemblyLimits(4)
local large = AiDescribe.debugDisassemblyLimits(8)

expect(tiny.stackCap == 1, "tiny stack cap should be 1")
expect(medium.stackCap == 2, "medium stack cap should be 2")
expect(large.stackCap == 3, "large stack cap should be 3")

expect(tiny.sizeBudget == 1, "tiny size budget should clamp to 1")
expect(medium.sizeBudget == 1, "size=4 budget should be floor(4*0.45)=1")
expect(large.sizeBudget == 4, "size=8 budget should be floor(8*0.55)=4")

expect(large.sizeBudget <= 7, "size budget must remain <= source-1 for size=8")

print(string.format("[PASS] disassembly cap regression validated (tiny=%d/%d medium=%d/%d large=%d/%d)",
    tiny.stackCap, tiny.sizeBudget,
    medium.stackCap, medium.sizeBudget,
    large.stackCap, large.sizeBudget
))
