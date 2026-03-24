-- Regression: compact urgency coach token `RGFXWRIU COACH:<STEADY|SPIKE>` emits behind dedicated flag when urgency parity is enabled.
-- Run: DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_ARC=1 DOTPIO_EXPERIMENT_ROUTE_GLOW=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_MODE=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF_URGENCY=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF_URGENCY_PARITY=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF_URGENCY_COACH=1 DOTPIO_EXPERIMENT_PULSE_HEAT_CUE=1 lua scripts/regression_portal_route_glow_fx_conf_why_rail_intensity_why_conf_urgency_coach.lua

package.path = package.path .. ";./?.lua;./?/init.lua"

local Portal = require("src.portal")

local function expect(cond, msg)
    if not cond then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF_URGENCY") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF_URGENCY=1")
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF_URGENCY_PARITY") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF_URGENCY_PARITY=1")
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF_URGENCY_COACH") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF_URGENCY_COACH=1")

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
expect(stable:find("RGFXWRIU:LOW", 1, true), "SAFE path should emit LOW urgency")
expect(stable:find("ROUTE GLOW FX CONF WHY RAIL INTENSITY WHY CONF URGENCY:LOW", 1, true), "SAFE path should emit detailed urgency parity token")
expect(stable:find("RGFXWRIU COACH:STEADY", 1, true), "SAFE path should emit STEADY urgency coach")

local pressure = promptFor("RISK", 160, "ASH")
expect(pressure:find("RGFXWRIU:MID", 1, true), "RISK path should emit MID urgency")
expect(pressure:find("ROUTE GLOW FX CONF WHY RAIL INTENSITY WHY CONF URGENCY:MID", 1, true), "RISK path should emit detailed urgency parity token")
expect(pressure:find("RGFXWRIU COACH:SPIKE", 1, true), "RISK path should emit SPIKE urgency coach")

local overdrive = promptFor("SPIKE", 175, "ASH")
expect(overdrive:find("RGFXWRIU:HIGH", 1, true), "SPIKE path should emit HIGH urgency")
expect(overdrive:find("ROUTE GLOW FX CONF WHY RAIL INTENSITY WHY CONF URGENCY:HIGH", 1, true), "SPIKE path should emit detailed urgency parity token")
expect(overdrive:find("RGFXWRIU COACH:SPIKE", 1, true), "SPIKE path should emit SPIKE urgency coach")

Portal._setRouteTagOverride("02", nil)
print("[PASS] portal route glow urgency coach token regression validated")
