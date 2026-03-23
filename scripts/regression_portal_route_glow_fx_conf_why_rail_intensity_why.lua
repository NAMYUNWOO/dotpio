-- Regression: flagged rail-intensity rationale token (`RGFXWRI WHY:<short>`) stays deterministic with RGFXW/RGFXWRM mappings.
-- Run: DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_ARC=1 DOTPIO_EXPERIMENT_ROUTE_GLOW=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_MODE=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY=1 DOTPIO_EXPERIMENT_PULSE_HEAT_CUE=1 lua scripts/regression_portal_route_glow_fx_conf_why_rail_intensity_why.lua

package.path = package.path .. ";./?.lua;./?/init.lua"

local Portal = require("src.portal")

local function expect(cond, msg)
    if not cond then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY=1")
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY=1")

local function getPrompt(routeTag, pressure, vibe)
    Portal.resetCooldown()
    Portal._setRouteTagOverride("02", routeTag)
    Portal.check(10, 10, {
        getPortalAt = function(_, _)
            return { targetMap = "02", targetPortal = "01" }
        end,
    })

    local prompt = Portal.getTransitionPrompt(pressure, { threatTier = pressure >= 170 and "HIGH" or "MID", vibeTrail = vibe })
    expect(type(prompt) == "string", "prompt should exist")
    Portal.cancelTransition()
    return prompt
end

local promptStable = getPrompt("SAFE", 150, "CALM")
expect(promptStable:find("RGFXWRI:SOFT", 1, true), "SAFE path should emit SOFT intensity")
expect(promptStable:find("RGFXWRI WHY:STABLE HOLD", 1, true), "SAFE path should emit STABLE HOLD rationale")

local promptPressure = getPrompt("RISK", 160, "ASH")
expect(promptPressure:find("RGFXWRI:SOFT", 1, true), "RISK path should emit SOFT intensity")
expect(promptPressure:find("RGFXWRI WHY:PRESSURE HOLD", 1, true), "RISK path should emit PRESSURE HOLD rationale")

local promptOverdrive = getPrompt("SPIKE", 175, "ASH")
expect(promptOverdrive:find("RGFXWRI:HARD", 1, true), "SPIKE path should emit HARD intensity")
expect(promptOverdrive:find("RGFXWRI WHY:LOCK PUSH", 1, true), "SPIKE path should emit LOCK PUSH rationale")

Portal._setRouteTagOverride("02", nil)

print("[PASS] portal route glow FX confidence rationale rail intensity why regression validated")
