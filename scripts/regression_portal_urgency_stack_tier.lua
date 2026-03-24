-- Regression: compact urgency-stack pruning tier token (`URG STACK:TIGHT|MID|LOOSE`) behind experiment flag.

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

local tight = promptFor("SPIKE", "HIGH", "ASH", 120)
expect(tight:find("URG STACK:TIGHT", 1, true), "small compact budget should emit URG STACK:TIGHT")

local mid = promptFor("RISK", "MID", "ASH", 160)
expect(mid:find("URG STACK:MID", 1, true), "mid compact budget should emit URG STACK:MID")

local loose = promptFor("SAFE", "MID", "CALM", 175)
expect(loose:find("URG STACK:LOOSE", 1, true), "larger compact budget should emit URG STACK:LOOSE")

Portal._setRouteTagOverride("02", nil)
print("[PASS] portal urgency-stack pruning tier regression validated")
