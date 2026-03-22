-- Regression: route-vibe resilience streak token experiment flag.
-- Run: DOTPIO_EXPERIMENT_ROUTE_VIBE_SYNC_HINT=1 DOTPIO_EXPERIMENT_ROUTE_VIBE_SNAPBACK=1 DOTPIO_EXPERIMENT_ROUTE_VIBE_RECOVERY_HINT=1 DOTPIO_EXPERIMENT_ROUTE_VIBE_RESILIENCE=1 lua scripts/regression_portal_route_vibe_resilience.lua

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
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_VIBE_RESILIENCE") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_VIBE_RESILIENCE=1")

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

local function buildSyncThreshold()
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
end

local function triggerSnapback()
    Portal.check(4, 4, buildMap("91"))
    local snapbackPrompt = Portal.getTransitionPrompt(240, { threatTier = "HIGH" })
    expect(snapbackPrompt:find("VIBE SNAPBACK:ON", 1, true), "snapback setup should emit warning token")
    Portal.confirmTransition()
    clearPortalTile()
end

local function recoverAndExpect(streak)
    Portal.check(5, 5, buildMap("91"))
    local recoveryPrompt = Portal.getTransitionPrompt(260, { threatTier = "LOW" })
    expect(recoveryPrompt:find("VIBE RECOVER:READY", 1, true), "recovery transition should emit recovery cue")
    expect(recoveryPrompt:find("VIBE RESILIENCE:" .. tostring(streak), 1, true), "recovery transition should emit resilience streak token")
    local compactRecovery = Portal.getTransitionPrompt(72, { threatTier = "LOW" })
    expect(compactRecovery:find("VR:OK", 1, true), "compact recovery should emit recovery cue token")
    expect(compactRecovery:find("VRES:" .. tostring(streak), 1, true), "compact recovery should emit compact resilience token")
    Portal.confirmTransition()
    clearPortalTile()
end

Portal.resetCooldown()
Portal._setRouteTagOverride("91", "SAFE")
Portal._setRouteTagOverride("92", "RISK")

buildSyncThreshold()
triggerSnapback()
recoverAndExpect(1)

-- Rebuild threshold + second snapback/recovery chain should increment streak.
buildSyncThreshold()
triggerSnapback()
recoverAndExpect(2)

Portal._setRouteTagOverride("91", nil)
Portal._setRouteTagOverride("92", nil)
Portal.resetCooldown()

print("[PASS] portal route-vibe resilience regression validated")
