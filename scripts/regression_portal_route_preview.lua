-- Regression: portal transition prompt should include NEXT ROUTE token before confirm.
-- Run: lua scripts/regression_portal_route_preview.lua

package.path = "./?.lua;./?/init.lua;" .. package.path

local Portal = require("src.portal")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

local calls = {}
Portal.onLoad = function(targetMap, targetPortal)
    table.insert(calls, { targetMap = targetMap, targetPortal = targetPortal })
end

local fakeMap = {
    getPortalAt = function(_, _)
        return { targetMap = "07", targetPortal = "06" }
    end,
}

Portal.resetCooldown()
Portal.check(10, 10, fakeMap)
expect(Portal.hasPendingTransition(), "stepping onto portal should open transition prompt")

local prompt = Portal.getTransitionPrompt(160, { threatTier = "HIGH" })
expect(type(prompt) == "string", "transition prompt should be rendered")
expect(prompt:find("NEXT ROUTE:SPIKE"), "transition prompt should include target map route tag token")
expect(prompt:find("COACH:HIGH PRESSURE"), "transition prompt should include SPIKE route coaching token")
expect(prompt:find("PRESSURE:5"), "transition prompt should include high-pressure score token for SPIKE+HIGH")

local confirmed = Portal.confirmTransition()
expect(confirmed == true, "portal confirm should succeed when transition is pending")
expect(#calls == 1, "portal confirm should invoke onLoad exactly once")
expect(calls[1].targetMap == "07" and calls[1].targetPortal == "06", "portal confirm should pass target map + portal")
expect(not Portal.hasPendingTransition(), "portal prompt should clear after confirm")

Portal.resetCooldown()
Portal.check(10, 10, {
    getPortalAt = function(_, _)
        return { targetMap = "01", targetPortal = "02" }
    end,
})
local unknownPrompt = Portal.getTransitionPrompt(160, { threatTier = "LOW" })
expect(type(unknownPrompt) == "string" and unknownPrompt:find("NEXT ROUTE:UNKNOWN"), "transition prompt should fallback to UNKNOWN when route tag missing")
expect(unknownPrompt:find("COACH:NO DATA"), "transition prompt should fallback to NO DATA coaching token")
expect(unknownPrompt:find("PRESSURE:2"), "unknown route with low threat should keep neutral pressure token")
expect(Portal.cancelTransition() == true, "cancel should clear pending portal transition")
expect(not Portal.hasPendingTransition(), "portal prompt should close after cancel")

print("[PASS] portal route preview transition prompt regression validated")
