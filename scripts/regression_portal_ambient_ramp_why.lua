-- Regression: portal ambient-ramp rationale tokens (`AMBIENT RAMP WHY:*` + `ARW:*`) behind experiment flags.

package.path = package.path .. ";./?.lua;./?/init.lua"

local Portal = require("src.portal")

local function expect(cond, msg)
    if not cond then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

expect(os.getenv("DOTPIO_EXPERIMENT_PORTAL_AMBIENT_RAMP") ~= nil, "set DOTPIO_EXPERIMENT_PORTAL_AMBIENT_RAMP=1")
expect(os.getenv("DOTPIO_EXPERIMENT_PORTAL_AMBIENT_RAMP_CONF") ~= nil, "set DOTPIO_EXPERIMENT_PORTAL_AMBIENT_RAMP_CONF=1")
expect(os.getenv("DOTPIO_EXPERIMENT_PORTAL_AMBIENT_RAMP_WHY") ~= nil, "set DOTPIO_EXPERIMENT_PORTAL_AMBIENT_RAMP_WHY=1")
expect(os.getenv("DOTPIO_EXPERIMENT_PORTAL_AMBIENT_RAMP_COMPACT") ~= nil, "set DOTPIO_EXPERIMENT_PORTAL_AMBIENT_RAMP_COMPACT=1")
expect(os.getenv("DOTPIO_EXPERIMENT_PORTAL_AMBIENT_RAMP_CONF_COMPACT") ~= nil, "set DOTPIO_EXPERIMENT_PORTAL_AMBIENT_RAMP_CONF_COMPACT=1")
expect(os.getenv("DOTPIO_EXPERIMENT_PORTAL_AMBIENT_RAMP_WHY_COMPACT") ~= nil, "set DOTPIO_EXPERIMENT_PORTAL_AMBIENT_RAMP_WHY_COMPACT=1")

local function promptFor(routeTag, threatTier, budget)
    Portal.resetCooldown()
    Portal._setRouteTagOverride("02", routeTag)
    Portal.check(10, 10, {
        getPortalAt = function()
            return { targetMap = "02", targetPortal = "01" }
        end,
    })
    local prompt = Portal.getTransitionPrompt(budget, {
        threatTier = threatTier,
    })
    expect(type(prompt) == "string", "prompt should exist")
    Portal.cancelTransition()
    return prompt
end

local calm = promptFor("SAFE", "LOW", 500)
expect(calm:find("AMBIENT RAMP WHY:SAFE LOCK", 1, true), "SAFE+LOW should emit AMBIENT RAMP WHY:SAFE LOCK")

local risk = promptFor("RISK", "MID", 500)
expect(risk:find("AMBIENT RAMP WHY:PRESSURE HOLD", 1, true), "RISK+MID should emit AMBIENT RAMP WHY:PRESSURE HOLD")

local spikeCompact = promptFor("SPIKE", "HIGH", 96)
expect(spikeCompact:find("ARC:L", 1, true), "compact prompt should retain ARC:L")
expect(spikeCompact:find("ARW:SP", 1, true), "SPIKE+HIGH compact prompt should emit ARW:SP")

Portal._setRouteTagOverride("02", nil)
print("[PASS] portal ambient-ramp rationale token regression validated")
