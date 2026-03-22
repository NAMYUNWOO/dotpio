-- Regression: conflict-aware coach override token experiment flag.
-- Run: DOTPIO_EXPERIMENT_ROUTE_VIBE_CONFLICT=1 DOTPIO_EXPERIMENT_ROUTE_VIBE_COACH_OVERRIDE=1 lua scripts/regression_portal_route_vibe_coach_override.lua

package.path = package.path .. ";./?.lua;./?/init.lua"

local Portal = require("src.portal")

local function expect(cond, msg)
    if not cond then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_VIBE_CONFLICT") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_VIBE_CONFLICT=1")
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_VIBE_COACH_OVERRIDE") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_VIBE_COACH_OVERRIDE=1")

Portal.resetCooldown()
Portal._setRouteTagOverride("72", "SPIKE")
Portal._setRouteTagOverride("73", "RISK")
Portal.check(3, 3, {
    portals = {
        { targetMap = "72", targetPortal = "A" },
        { targetMap = "73", targetPortal = "B" },
    },
    getPortalAt = function(_, _)
        return { targetMap = "72", targetPortal = "A" }
    end,
})

local detailed = Portal.getTransitionPrompt(240, { threatTier = "LOW" })
expect(detailed:find("VIBE CONFLICT:ON", 1, true), "detailed prompt should include conflict token")
expect(detailed:find("COACH OVERRIDE:DE%-ESCALATE"), "detailed prompt should include coach override token when adaptive ALT exists")

local compact = Portal.getTransitionPrompt(70, { threatTier = "LOW" })
expect(compact:find("VC:ON", 1, true), "compact prompt should include compact conflict token")
expect(compact:find("COVR:DEESC", 1, true), "compact prompt should include compact coach override token")

Portal.cancelTransition()
Portal._setRouteTagOverride("72", nil)
Portal._setRouteTagOverride("73", nil)

Portal.resetCooldown()
Portal._setRouteTagOverride("81", "SAFE")
Portal.check(4, 4, {
    portals = {
        { targetMap = "81", targetPortal = "A" },
    },
    getPortalAt = function(_, _)
        return { targetMap = "81", targetPortal = "A" }
    end,
})

local noAlt = Portal.getTransitionPrompt(240, { threatTier = "HIGH" })
expect(not noAlt:find("COACH OVERRIDE:DE%-ESCALATE"), "coach override token should not appear when adaptive ALT is unavailable")

Portal.cancelTransition()
Portal._setRouteTagOverride("81", nil)

print("[PASS] portal route-vibe coach override regression validated")
