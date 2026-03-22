-- Regression: route-vibe drift alarm token experiment flag.
-- Run: DOTPIO_EXPERIMENT_ROUTE_VIBE_SYNC_HINT=1 DOTPIO_EXPERIMENT_ROUTE_VIBE_SNAPBACK=1 DOTPIO_EXPERIMENT_ROUTE_VIBE_CONFLICT=1 DOTPIO_EXPERIMENT_ROUTE_VIBE_DRIFT_ALARM=1 lua scripts/regression_portal_route_vibe_drift_alarm.lua

package.path = package.path .. ";./?.lua;./?/init.lua"

local Portal = require("src.portal")

local function expect(cond, msg)
    if not cond then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_VIBE_SYNC_HINT") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_VIBE_SYNC_HINT=1")
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_VIBE_SNAPBACK") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_VIBE_SNAPBACK=1")
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_VIBE_CONFLICT") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_VIBE_CONFLICT=1")
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_VIBE_DRIFT_ALARM") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_VIBE_DRIFT_ALARM=1")

local function buildMap(targetMap)
    return {
        portals = {
            { targetMap = targetMap, targetPortal = "A" },
        },
        getPortalAt = function(_, _)
            return { targetMap = targetMap, targetPortal = "A" }
        end,
    }
end

local function clearPortalTile()
    Portal.check(0, 0, {
        portals = {},
        getPortalAt = function(_, _)
            return nil
        end,
    })
end

Portal.resetCooldown()
Portal._setRouteTagOverride("91", "SAFE")
Portal._setRouteTagOverride("92", "RISK")

-- Build sync streak to threshold.
Portal.check(1, 1, buildMap("91"))
Portal.getTransitionPrompt(240, { threatTier = "LOW" })
Portal.confirmTransition()
clearPortalTile()

Portal.check(2, 2, buildMap("92"))
Portal.getTransitionPrompt(240, { threatTier = "MED" })
Portal.confirmTransition()
clearPortalTile()

Portal.check(3, 3, buildMap("91"))
Portal.getTransitionPrompt(240, { threatTier = "LOW" })
Portal.confirmTransition()
clearPortalTile()

-- Immediate post-threshold misalignment on SAFE + HIGH => conflict + snapback in same prompt.
Portal.check(4, 4, buildMap("91"))
local detailed = Portal.getTransitionPrompt(260, { threatTier = "HIGH" })
expect(detailed:find("VIBE CONFLICT:ON", 1, true), "detailed prompt should include conflict token")
expect(detailed:find("VIBE SNAPBACK:ON", 1, true), "detailed prompt should include snapback token")
expect(detailed:find("VIBE DRIFT:WIDE", 1, true), "detailed prompt should include drift alarm token when conflict+snapback co-occur")

local compact = Portal.getTransitionPrompt(70, { threatTier = "HIGH" })
expect(compact:find("VC:ON", 1, true), "compact prompt should include compact conflict token")
expect(compact:find("VSB:ON", 1, true), "compact prompt should include compact snapback token")
expect(compact:find("VDR:WIDE", 1, true), "compact prompt should include compact drift alarm token")
Portal.confirmTransition()
clearPortalTile()

-- Calm aligned prompt with no conflict/snapback should not keep drift token latched.
Portal.check(5, 5, buildMap("91"))
local stable = Portal.getTransitionPrompt(260, { threatTier = "LOW" })
expect(not stable:find("VIBE DRIFT:WIDE", 1, true), "drift alarm should clear when neither conflict nor snapback is present")
Portal.cancelTransition()

Portal._setRouteTagOverride("91", nil)
Portal._setRouteTagOverride("92", nil)
Portal.resetCooldown()

print("[PASS] portal route-vibe drift alarm regression validated")
