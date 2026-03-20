-- Regression: adaptive ALT portal hint must remain readable under HIGH threat compact mode.
-- Validates compact-budget selection, token order, and adaptive ALT token presence.
-- Run: lua scripts/regression_portal_prompt_adaptive_alt_readability.lua

package.path = "./?.lua;./?/init.lua;" .. package.path

local Portal = require("src.portal")

local function fail(message)
    io.stderr:write("[FAIL] " .. tostring(message) .. "\n")
    os.exit(1)
end

local function expect(condition, message)
    if not condition then
        fail(message)
    end
end

local function tokenPositions(prompt)
    return {
        ACTION = prompt:find("ENTER:JUMP", 1, true),
        ROUTE = prompt:find("NEXT:", 1, true),
        COACH = prompt:find("COACH:", 1, true),
        PRESSURE = prompt:find("P:", 1, true),
        ALT = prompt:find("ALT:", 1, true),
        ALT_DELTA = prompt:find("ADEL:", 1, true),
    }
end

Portal.resetCooldown()
Portal.check(8, 8, {
    currentMap = "06",
    portals = {
        { targetMap = "07", targetPortal = "06" },
        { targetMap = "05", targetPortal = "06" },
    },
    getPortalAt = function(_, _)
        return { targetMap = "07", targetPortal = "06" }
    end,
})

local compactBudget = 86
local prompt = Portal.getTransitionPrompt(compactBudget, { threatTier = "HIGH" })
expect(type(prompt) == "string" and prompt ~= "", "prompt should be generated for pending portal transition")

-- Compact mode should be active and include adaptive ALT hinting.
expect(not prompt:find("NEXT ROUTE:", 1, true), "compact prompt should not include verbose NEXT ROUTE token")
expect(prompt:find("NEXT:SPIKE", 1, true), "compact prompt should include abbreviated NEXT route token")
expect(prompt:find("COACH:HIGH", 1, true), "compact prompt should include compact coach token")
expect(prompt:find("P:5", 1, true), "compact prompt should include compact pressure token")
expect(prompt:find("ALT:RISK", 1, true), "compact prompt should include adaptive ALT route token")
expect(prompt:find("ADEL:-1", 1, true), "compact prompt should include adaptive ALT delta token")
expect(#prompt <= compactBudget, string.format("compact prompt should respect budget (%d > %d)", #prompt, compactBudget))

local positions = tokenPositions(prompt)
for key, pos in pairs(positions) do
    expect(type(pos) == "number", string.format("missing required token `%s` in compact prompt", key))
end

expect(positions.ACTION < positions.ROUTE, "token order invalid: ACTION must appear before ROUTE")
expect(positions.ROUTE < positions.COACH, "token order invalid: ROUTE must appear before COACH")
expect(positions.COACH < positions.PRESSURE, "token order invalid: COACH must appear before PRESSURE")
expect(positions.PRESSURE < positions.ALT, "token order invalid: PRESSURE must appear before ALT")
expect(positions.ALT < positions.ALT_DELTA, "token order invalid: ALT must appear before ALT_DELTA")

Portal.cancelTransition()
print("[PASS] portal adaptive ALT readability regression validated (HIGH threat compact mode)")
