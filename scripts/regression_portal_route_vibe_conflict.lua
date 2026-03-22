-- Regression: portal route-vibe conflict warning experiment flag.
-- Run: DOTPIO_EXPERIMENT_ROUTE_VIBE_CONFLICT=1 lua scripts/regression_portal_route_vibe_conflict.lua

package.path = package.path .. ";./?.lua;./?/init.lua"

local Portal = require("src.portal")

local function expect(cond, msg)
    if not cond then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

local enabled = os.getenv("DOTPIO_EXPERIMENT_ROUTE_VIBE_CONFLICT")
expect(enabled == "1" or enabled == "true" or enabled == "on" or enabled == "yes", "set DOTPIO_EXPERIMENT_ROUTE_VIBE_CONFLICT=1 when running this regression")

Portal.resetCooldown()
Portal._setRouteTagOverride("70", "SAFE")
Portal.check(4, 4, {
    portals = {
        { targetMap = "70", targetPortal = "A" },
    },
    getPortalAt = function(_, _)
        return { targetMap = "70", targetPortal = "A" }
    end,
})

local detailedConflict = Portal.getTransitionPrompt(220, { threatTier = "HIGH" })
expect(detailedConflict:find("ROUTE VIBE:CALM", 1, true), "detailed prompt should preserve route vibe token")
expect(detailedConflict:find("VIBE CONFLICT:ON", 1, true), "detailed prompt should include conflict token when cues oppose")

local compactConflict = Portal.getTransitionPrompt(68, { threatTier = "HIGH" })
expect(compactConflict:find("VIBE:C", 1, true), "compact prompt should preserve compact route vibe token")
expect(compactConflict:find("VC:ON", 1, true), "compact prompt should include compact conflict token when cues oppose")

Portal.cancelTransition()
Portal._setRouteTagOverride("70", nil)

Portal.resetCooldown()
Portal._setRouteTagOverride("71", "RISK")
Portal.check(5, 5, {
    portals = {
        { targetMap = "71", targetPortal = "B" },
    },
    getPortalAt = function(_, _)
        return { targetMap = "71", targetPortal = "B" }
    end,
})

local alignedPrompt = Portal.getTransitionPrompt(220, { threatTier = "HIGH" })
expect(not alignedPrompt:find("VIBE CONFLICT:ON", 1, true), "aligned/nearby cues should not emit conflict token")

Portal.cancelTransition()
Portal._setRouteTagOverride("71", nil)

print("[PASS] portal route-vibe conflict regression validated")
