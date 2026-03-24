-- Regression: portal ambient-ramp hint token (`AMBIENT RAMP:CALM|TENSE`) behind experiment flag.

package.path = package.path .. ";./?.lua;./?/init.lua"

local Portal = require("src.portal")

local function expect(cond, msg)
    if not cond then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

expect(os.getenv("DOTPIO_EXPERIMENT_PORTAL_AMBIENT_RAMP") ~= nil, "set DOTPIO_EXPERIMENT_PORTAL_AMBIENT_RAMP=1")

local function promptFor(routeTag, threatTier)
    Portal.resetCooldown()
    Portal._setRouteTagOverride("02", routeTag)
    Portal.check(10, 10, {
        getPortalAt = function()
            return { targetMap = "02", targetPortal = "01" }
        end,
    })
    local prompt = Portal.getTransitionPrompt(500, {
        threatTier = threatTier,
    })
    expect(type(prompt) == "string", "prompt should exist")
    Portal.cancelTransition()
    return prompt
end

local calm = promptFor("SAFE", "LOW")
expect(calm:find("AMBIENT RAMP:CALM", 1, true), "SAFE+LOW should emit AMBIENT RAMP:CALM")

local tense = promptFor("RISK", "MID")
expect(tense:find("AMBIENT RAMP:TENSE", 1, true), "RISK+MID should emit AMBIENT RAMP:TENSE")

Portal._setRouteTagOverride("02", nil)
print("[PASS] portal ambient-ramp token regression validated")
