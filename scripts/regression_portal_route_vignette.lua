-- Regression: portal route vignette experiment flag.
-- Run: DOTPIO_EXPERIMENT_ROUTE_VIGNETTE_ASCII=1 lua scripts/regression_portal_route_vignette.lua

package.path = package.path .. ";./?.lua;./?/init.lua"

local Portal = require("src.portal")

local function expect(condition, message)
    if not condition then
        error(message, 2)
    end
end

Portal.resetCooldown()
Portal._setRouteTagOverride("07", "SPIKE")

local mapStub = {
    currentMap = "06",
    portals = {
        { name = "gate", x = 1, y = 1, targetMap = "07", targetPortal = "06" },
    },
    getPortalAt = function(x, y)
        if x == 1 and y == 1 then
            return { name = "gate", x = 1, y = 1, targetMap = "07", targetPortal = "06" }
        end
        return nil
    end,
}

Portal.check(1, 1, mapStub)
expect(Portal.hasPendingTransition(), "portal transition should be pending")

local detailed = Portal.getTransitionPrompt(220, { threatTier = "HIGH" })
expect(type(detailed) == "string" and detailed ~= "", "detailed prompt should be generated")
expect(detailed:find("ROUTE VIGNETTE:%^%^%^", 1, false), "detailed prompt should include SPIKE route vignette token when experiment enabled")

local compact = Portal.getTransitionPrompt(72, { threatTier = "HIGH" })
expect(type(compact) == "string" and compact ~= "", "compact prompt should be generated")
expect(compact:find("RV:%^%^%^", 1, false), "compact prompt should include compact route vignette token when experiment enabled")

Portal.cancelTransition()
Portal._setRouteTagOverride("07", nil)

print("[PASS] portal route vignette regression validated")
