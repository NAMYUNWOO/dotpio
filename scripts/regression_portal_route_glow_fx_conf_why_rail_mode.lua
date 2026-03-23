-- Regression: route-glow FX confidence rationale rail mode token (`RGFXWRM:LOCK|FLEX`) when enabled.
-- Run: DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_ARC=1 DOTPIO_EXPERIMENT_ROUTE_GLOW=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_MODE=1 DOTPIO_EXPERIMENT_PULSE_HEAT_CUE=1 lua scripts/regression_portal_route_glow_fx_conf_why_rail_mode.lua

package.path = package.path .. ";./?.lua;./?/init.lua"

local Portal = require("src.portal")

local function expect(cond, msg)
    if not cond then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL=1")
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_MODE") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_MODE=1")

Portal.resetCooldown()
Portal._setRouteTagOverride("02", "SAFE")
Portal.check(10, 10, {
    getPortalAt = function(_, _)
        return { targetMap = "02", targetPortal = "01" }
    end,
})

local promptLow = Portal.getTransitionPrompt(150, { threatTier = "LOW", vibeTrail = "CALM" })
expect(type(promptLow) == "string", "low-pressure prompt should exist")
expect(promptLow:find("RGFXWRM:FLEX", 1, true), "SOFT/STEADY path should emit FLEX rail mode")
Portal.cancelTransition()
Portal.resetCooldown()
Portal._setRouteTagOverride("02", "SPIKE")

Portal.check(10, 10, {
    getPortalAt = function(_, _)
        return { targetMap = "02", targetPortal = "01" }
    end,
})

local promptHigh = Portal.getTransitionPrompt(170, { threatTier = "HIGH", vibeTrail = "ASH" })
expect(type(promptHigh) == "string", "high-pressure prompt should exist")
expect(promptHigh:find("RGFXWRM:LOCK", 1, true), "SURGE/SPIKE path should emit LOCK rail mode")
Portal.cancelTransition()
Portal._setRouteTagOverride("02", nil)

print("[PASS] portal route glow FX confidence rationale rail mode regression validated")
