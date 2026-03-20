-- Regression: adaptive ALT selector v2 should pick lowest-pressure reachable branch.
-- Run: lua scripts/regression_portal_alt_selector_v2.lua

package.path = "./?.lua;./?/init.lua;" .. package.path

local Portal = require("src.portal")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

Portal.resetCooldown()
Portal._setRouteTagOverride("40", "SPIKE")
Portal._setRouteTagOverride("41", "RISK")
Portal._setRouteTagOverride("42", "SAFE")

local fakeMap = {
    currentMap = "39",
    portals = {
        { targetMap = "40", targetPortal = "A" },
        { targetMap = "41", targetPortal = "B" },
        { targetMap = "42", targetPortal = "C" },
    },
    getPortalAt = function(_, _)
        return { targetMap = "40", targetPortal = "A" }
    end,
}

Portal.check(5, 5, fakeMap)
expect(Portal.hasPendingTransition(), "portal transition should be pending")

local prompt = Portal.getTransitionPrompt(200, { threatTier = "HIGH" })
expect(type(prompt) == "string", "transition prompt should be string")
expect(prompt:find("NEXT ROUTE:SPIKE"), "primary route tag should match selected portal")
expect(prompt:find("ALT ROUTE:SAFE"), "selector v2 should choose lowest-pressure reachable branch")
expect(prompt:find("ALT DELTA:-2", 1, true), "selector v2 should expose pressure delta for chosen branch")

Portal.cancelTransition()
Portal._setRouteTagOverride("40", nil)
Portal._setRouteTagOverride("41", nil)
Portal._setRouteTagOverride("42", nil)

print("[PASS] portal adaptive ALT selector v2 regression validated")
