-- Regression: compact ambient-ramp alias token (`AR:<C|T>`) behind experiment flag.

package.path = package.path .. ";./?.lua;./?/init.lua"

local Portal = require("src.portal")

local function expect(cond, msg)
    if not cond then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

expect(os.getenv("DOTPIO_EXPERIMENT_PORTAL_AMBIENT_RAMP") ~= nil, "set DOTPIO_EXPERIMENT_PORTAL_AMBIENT_RAMP=1")
expect(os.getenv("DOTPIO_EXPERIMENT_PORTAL_AMBIENT_RAMP_COMPACT") ~= nil, "set DOTPIO_EXPERIMENT_PORTAL_AMBIENT_RAMP_COMPACT=1")

local function promptFor(routeTag, threatTier)
    Portal.resetCooldown()
    Portal._setRouteTagOverride("02", routeTag)
    Portal.check(10, 10, {
        getPortalAt = function()
            return { targetMap = "02", targetPortal = "01" }
        end,
    })
    local prompt = Portal.getTransitionPrompt(76, {
        threatTier = threatTier,
    })
    expect(type(prompt) == "string", "prompt should exist")
    Portal.cancelTransition()
    return prompt
end

local calm = promptFor("SAFE", "LOW")
expect(calm:find("AR:C", 1, true), "SAFE+LOW compact prompt should emit AR:C")

local tense = promptFor("SPIKE", "HIGH")
expect(tense:find("AR:T", 1, true), "SPIKE+HIGH compact prompt should emit AR:T")

Portal._setRouteTagOverride("02", nil)
print("[PASS] portal compact ambient-ramp alias regression validated")
