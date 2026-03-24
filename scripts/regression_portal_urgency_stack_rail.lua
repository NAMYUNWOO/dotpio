-- Regression: compact urgency-stack rail token (`URG STACK RAIL:STEADY|SPIKE`) behind experiment flag.

package.path = package.path .. ";./?.lua;./?/init.lua"

local Portal = require("src.portal")

local function expect(cond, msg)
    if not cond then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

expect(os.getenv("DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL") ~= nil, "set DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL=1")
expect(os.getenv("DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY") ~= nil, "set DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY=1")
expect(os.getenv("DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_ARC") ~= nil, "set DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_ARC=1")
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_GLOW=1")
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_CONF") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_GLOW_CONF=1")
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_GLOW_FX=1")
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF=1")
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY=1")
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL=1")
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_MODE") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_MODE=1")
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY=1")
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY=1")
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF=1")
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF_URGENCY") ~= nil, "set ..._URGENCY=1")
expect(os.getenv("DOTPIO_EXPERIMENT_URGENCY_STACK_TIER") ~= nil, "set DOTPIO_EXPERIMENT_URGENCY_STACK_TIER=1")
expect(os.getenv("DOTPIO_EXPERIMENT_URGENCY_STACK_RAIL") ~= nil, "set DOTPIO_EXPERIMENT_URGENCY_STACK_RAIL=1")

local function promptFor(routeTag, threatTier, vibe, budget)
    Portal.resetCooldown()
    Portal._setRouteTagOverride("02", routeTag)
    Portal.check(10, 10, {
        getPortalAt = function()
            return { targetMap = "02", targetPortal = "01" }
        end,
    })
    local prompt = Portal.getTransitionPrompt(budget, {
        threatTier = threatTier,
        vibeTrail = vibe,
    })
    expect(type(prompt) == "string", "prompt should exist")
    Portal.cancelTransition()
    return prompt
end

local tight = promptFor("SAFE", "MID", "CALM", 120)
expect(tight:find("URG STACK:TIGHT", 1, true), "tight budget should emit URG STACK:TIGHT")
expect(tight:find("URG STACK RAIL:SPIKE", 1, true), "tight budget should emit URG STACK RAIL:SPIKE")

local steady = promptFor("SAFE", "MID", "CALM", 175)
expect(steady:find("URG STACK:LOOSE", 1, true), "loose budget should emit URG STACK:LOOSE")
expect(steady:find("URG STACK RAIL:STEADY", 1, true), "loose budget + non-high urgency should emit URG STACK RAIL:STEADY")

Portal._setRouteTagOverride("02", nil)
print("[PASS] portal urgency-stack rail regression validated")
