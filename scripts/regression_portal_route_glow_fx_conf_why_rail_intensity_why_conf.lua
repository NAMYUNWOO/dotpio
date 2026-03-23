-- Regression: flagged rail-intensity rationale confidence token (`RGFXWRI WHY CONF:LOW|MID|HIGH`) remains deterministic.
-- Run: DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_ARC=1 DOTPIO_EXPERIMENT_ROUTE_GLOW=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_MODE=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF=1 DOTPIO_EXPERIMENT_PULSE_HEAT_CUE=1 lua scripts/regression_portal_route_glow_fx_conf_why_rail_intensity_why_conf.lua

package.path = package.path .. ";./?.lua;./?/init.lua"

local Portal = require("src.portal")

local function expect(cond, msg)
    if not cond then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY=1")
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF=1")

local function promptFor(routeTag, pressure, vibe)
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

local stable = promptFor("SAFE", 150, "CALM")
expect(stable:find("RGFXWRI WHY:STABLE HOLD", 1, true), "SAFE path rationale should be STABLE HOLD")
expect(stable:find("RGFXWRI WHY CONF:LOW", 1, true), "SAFE path confidence should be LOW")

local pressure = promptFor("RISK", 160, "ASH")
expect(pressure:find("RGFXWRI WHY:PRESSURE HOLD", 1, true), "RISK path rationale should be PRESSURE HOLD")
expect(pressure:find("RGFXWRI WHY CONF:MID", 1, true), "RISK path confidence should be MID")

local overdrive = promptFor("SPIKE", 175, "ASH")
expect(overdrive:find("RGFXWRI WHY:LOCK PUSH", 1, true), "SPIKE path rationale should be LOCK PUSH")
expect(overdrive:find("RGFXWRI WHY CONF:HIGH", 1, true), "SPIKE path confidence should be HIGH")

Portal._setRouteTagOverride("02", nil)
print("[PASS] portal route glow FX confidence rationale rail intensity why confidence regression validated")
