-- Regression: sync-threshold dodge handoff behind route-vibe sync dodge experiment flag.
-- Run: DOTPIO_EXPERIMENT_ROUTE_VIBE_SYNC_HINT=1 DOTPIO_EXPERIMENT_ROUTE_VIBE_SYNC_DODGE=1 lua scripts/regression_portal_route_vibe_sync_dodge.lua

package.path = package.path .. ";./?.lua;./?/init.lua"

local Portal = require("src.portal")

local function expect(cond, msg)
    if not cond then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_VIBE_SYNC_HINT") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_VIBE_SYNC_HINT=1")
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_VIBE_SYNC_DODGE") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_VIBE_SYNC_DODGE=1")

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

-- Build to chain 2/3; no dodge grant expected.
Portal.check(1, 1, buildMap("91"))
Portal.getTransitionPrompt(240, { threatTier = "LOW" })
Portal.confirmTransition()
clearPortalTile()
Portal.check(2, 2, buildMap("92"))
Portal.getTransitionPrompt(240, { threatTier = "MED" })
Portal.confirmTransition()
clearPortalTile()
expect(Portal.consumeVibeSyncDodgeCharges() == 0, "no sync dodge charge should be queued before threshold")

-- Third aligned transition triggers VIBE SYNC:+1 and should queue one dodge charge.
Portal.check(3, 3, buildMap("91"))
local thresholdPrompt = Portal.getTransitionPrompt(240, { threatTier = "LOW" })
expect(thresholdPrompt:find("VIBE SYNC:%+1"), "threshold transition should include VIBE SYNC:+1 hint")
Portal.confirmTransition()
clearPortalTile()
expect(Portal.consumeVibeSyncDodgeCharges() == 1, "threshold sync should queue exactly one dodge charge")
expect(Portal.consumeVibeSyncDodgeCharges() == 0, "consume should clear queued sync dodge charges")

-- Misalignment resets chain and should not queue a charge.
Portal.check(4, 4, buildMap("91"))
Portal.getTransitionPrompt(240, { threatTier = "HIGH" })
Portal.confirmTransition()
clearPortalTile()
expect(Portal.consumeVibeSyncDodgeCharges() == 0, "misaligned transition should not queue sync dodge charge")

Portal._setRouteTagOverride("91", nil)
Portal._setRouteTagOverride("92", nil)
Portal.resetCooldown()

print("[PASS] portal route-vibe sync dodge regression validated")
