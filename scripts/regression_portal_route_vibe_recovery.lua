-- Regression: route-vibe post-snapback recovery cue experiment flag.
-- Run: DOTPIO_EXPERIMENT_ROUTE_VIBE_SYNC_HINT=1 DOTPIO_EXPERIMENT_ROUTE_VIBE_SNAPBACK=1 DOTPIO_EXPERIMENT_ROUTE_VIBE_RECOVERY_HINT=1 lua scripts/regression_portal_route_vibe_recovery.lua

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
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_VIBE_RECOVERY_HINT") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_VIBE_RECOVERY_HINT=1")

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

-- Build vibe-sync streak to threshold.
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

-- Trigger snapback by immediate misalignment after sync threshold.
Portal.check(4, 4, buildMap("91"))
local snapbackPrompt = Portal.getTransitionPrompt(240, { threatTier = "HIGH" })
expect(snapbackPrompt:find("VIBE SNAPBACK:ON", 1, true), "snapback setup transition should show snapback token")
Portal.confirmTransition()
clearPortalTile()

-- First aligned transition after snapback should show one-shot recovery cue.
Portal.check(5, 5, buildMap("91"))
local recoveryPrompt = Portal.getTransitionPrompt(240, { threatTier = "LOW" })
expect(recoveryPrompt:find("VIBE RECOVER:READY", 1, true), "first aligned transition after snapback should show recovery cue")
local compactRecovery = Portal.getTransitionPrompt(70, { threatTier = "LOW" })
expect(compactRecovery:find("VR:OK", 1, true), "compact prompt should show recovery cue token")
Portal.confirmTransition()
clearPortalTile()

-- Recovery cue should clear after confirmation and not repeat every aligned transition.
Portal.check(6, 6, buildMap("92"))
local steadyAligned = Portal.getTransitionPrompt(240, { threatTier = "MED" })
expect(not steadyAligned:find("VIBE RECOVER:READY", 1, true), "recovery cue should be one-shot and clear after recovery confirm")
Portal.cancelTransition()

Portal._setRouteTagOverride("91", nil)
Portal._setRouteTagOverride("92", nil)
Portal.resetCooldown()

print("[PASS] portal route-vibe recovery regression validated")
