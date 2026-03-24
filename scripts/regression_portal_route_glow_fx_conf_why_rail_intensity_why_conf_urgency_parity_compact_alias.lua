-- Regression: compact alias for urgency parity token (`RGFXWRIUP:<LOW|MID|HIGH>`) behind compact alias flag.

package.path = package.path .. ";./?.lua;./?/init.lua"

local Portal = require("src.portal")

local function expect(cond, msg)
    if not cond then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF_URGENCY") ~= nil, "set ..._URGENCY=1")
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF_URGENCY_PARITY") ~= nil, "set ..._URGENCY_PARITY=1")
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF_URGENCY_PARITY_COMPACT") ~= nil, "set ..._URGENCY_PARITY_COMPACT=1")

local function promptFor(routeTag, pressure, vibe)
    Portal.resetCooldown()
    Portal._setRouteTagOverride("02", routeTag)
    Portal.check(10, 10, {
        getPortalAt = function()
            return { targetMap = "02", targetPortal = "01" }
        end,
    })
    local prompt = Portal.getTransitionPrompt(pressure, { threatTier = pressure >= 170 and "HIGH" or "MID", vibeTrail = vibe })
    expect(type(prompt) == "string", "prompt should exist")
    Portal.cancelTransition()
    return prompt
end

local safe = promptFor("SAFE", 150, "CALM")
expect(safe:find("RGFXWRIUP:LOW", 1, true), "SAFE path should emit compact urgency parity alias")
expect(not safe:find("ROUTE GLOW FX CONF WHY RAIL INTENSITY WHY CONF URGENCY:", 1, true), "detailed urgency parity label should be suppressed when compact alias flag is on")

local risk = promptFor("RISK", 160, "ASH")
expect(risk:find("RGFXWRIUP:MID", 1, true), "RISK path should emit MID compact urgency parity alias")

local spike = promptFor("SPIKE", 175, "ASH")
expect(spike:find("RGFXWRIUP:HIGH", 1, true), "SPIKE path should emit HIGH compact urgency parity alias")

Portal._setRouteTagOverride("02", nil)
print("[PASS] portal route glow urgency parity compact alias regression validated")
