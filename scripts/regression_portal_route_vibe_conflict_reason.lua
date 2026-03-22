-- Regression: portal route-vibe conflict reason token experiment flag.
-- Run: DOTPIO_EXPERIMENT_ROUTE_VIBE_CONFLICT=1 DOTPIO_EXPERIMENT_ROUTE_VIBE_CONFLICT_REASON=1 lua scripts/regression_portal_route_vibe_conflict_reason.lua

package.path = package.path .. ";./?.lua;./?/init.lua"

local Portal = require("src.portal")

local function expect(cond, msg)
    if not cond then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_VIBE_CONFLICT") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_VIBE_CONFLICT=1")
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_VIBE_CONFLICT_REASON") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_VIBE_CONFLICT_REASON=1")

Portal.resetCooldown()
Portal._setRouteTagOverride("72", "SAFE")
Portal.check(3, 3, {
    portals = {
        { targetMap = "72", targetPortal = "A" },
    },
    getPortalAt = function(_, _)
        return { targetMap = "72", targetPortal = "A" }
    end,
})

local detailed = Portal.getTransitionPrompt(240, { threatTier = "HIGH" })
expect(detailed:find("VIBE CONFLICT:ON", 1, true), "detailed prompt should include conflict token")
expect(detailed:find("VIBE WHY:CALMvsHIGH", 1, true), "detailed prompt should include conflict reason token")

local compact = Portal.getTransitionPrompt(70, { threatTier = "HIGH" })
expect(compact:find("VC:ON", 1, true), "compact prompt should include compact conflict token")
expect(compact:find("VCWHY:C/H", 1, true), "compact prompt should include compact conflict reason token")

Portal.cancelTransition()
Portal._setRouteTagOverride("72", nil)

print("[PASS] portal route-vibe conflict reason regression validated")
