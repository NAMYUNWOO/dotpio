-- Regression: compact portal prompt should include pulse-heat cue when experiment flag is enabled.
-- Run: DOTPIO_EXPERIMENT_PULSE_HEAT_CUE=1 lua scripts/regression_portal_pulse_heat.lua

package.path = "./?.lua;./?/init.lua;" .. package.path

local Portal = require("src.portal")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

expect(os.getenv("DOTPIO_EXPERIMENT_PULSE_HEAT_CUE") ~= nil, "set DOTPIO_EXPERIMENT_PULSE_HEAT_CUE=1")

local function openPortal(targetMap)
    Portal.resetCooldown()
    Portal.check(10, 10, {
        getPortalAt = function(_, _)
            return { targetMap = targetMap, targetPortal = "01" }
        end,
    })
end

openPortal("02")
local coolPrompt = Portal.getTransitionPrompt(72, { threatTier = "LOW" })
expect(type(coolPrompt) == "string", "compact low-pressure prompt should exist")
expect(coolPrompt:find("PULSE HEAT:COOL", 1, true), "low-pressure compact prompt should include PULSE HEAT:COOL")
Portal.cancelTransition()

openPortal("07")
local warmPrompt = Portal.getTransitionPrompt(72, { threatTier = "MED" })
expect(type(warmPrompt) == "string", "compact mid-pressure prompt should exist")
expect(warmPrompt:find("PULSE HEAT:WARM", 1, true), "mid-pressure compact prompt should include PULSE HEAT:WARM")
Portal.cancelTransition()

openPortal("07")
local hotPrompt = Portal.getTransitionPrompt(72, { threatTier = "HIGH" })
expect(type(hotPrompt) == "string", "compact high-pressure prompt should exist")
expect(hotPrompt:find("PULSE HEAT:HOT", 1, true), "high-pressure compact prompt should include PULSE HEAT:HOT")
Portal.cancelTransition()

print("[PASS] portal compact pulse-heat cue regression validated")
