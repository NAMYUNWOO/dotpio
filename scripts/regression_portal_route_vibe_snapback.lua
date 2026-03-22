-- Regression: route-vibe snapback warning experiment flag.
-- Run: DOTPIO_EXPERIMENT_ROUTE_VIBE_SYNC_HINT=1 DOTPIO_EXPERIMENT_ROUTE_VIBE_SNAPBACK=1 lua scripts/regression_portal_route_vibe_snapback.lua

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
local thresholdPrompt = Portal.getTransitionPrompt(240, { threatTier = "LOW" })
expect(thresholdPrompt:find("VIBE CHAIN:3/3", 1, true), "threshold transition should show sync chain 3/3")
expect(thresholdPrompt:find("VIBE SYNC:%+1"), "threshold transition should show sync reward hint")
Portal.confirmTransition()
clearPortalTile()

-- Immediate post-sync misalignment should emit snapback warning.
Portal.check(4, 4, buildMap("91"))
local snapbackPrompt = Portal.getTransitionPrompt(240, { threatTier = "HIGH" })
expect(snapbackPrompt:find("VIBE CHAIN:0/3", 1, true), "misaligned post-sync transition should show chain reset")
expect(snapbackPrompt:find("VIBE SNAPBACK:ON", 1, true), "misaligned post-sync transition should show snapback warning")
local compactSnapback = Portal.getTransitionPrompt(70, { threatTier = "HIGH" })
expect(compactSnapback:find("VSC:0/3", 1, true), "compact misaligned transition should show compact chain reset")
expect(compactSnapback:find("VSB:ON", 1, true), "compact misaligned transition should show compact snapback warning")
Portal.confirmTransition()
clearPortalTile()

-- Subsequent misalignment should no longer emit immediate snapback.
Portal.check(5, 5, buildMap("91"))
local steadyMisaligned = Portal.getTransitionPrompt(240, { threatTier = "HIGH" })
expect(not steadyMisaligned:find("VIBE SNAPBACK:ON", 1, true), "non-immediate misalignment should not keep snapback warning armed")
Portal.cancelTransition()

Portal._setRouteTagOverride("91", nil)
Portal._setRouteTagOverride("92", nil)
Portal.resetCooldown()

print("[PASS] portal route-vibe snapback regression validated")
