-- Regression: compact portal prompt should include pulse-link cue when experiment flag is enabled.
-- Run: DOTPIO_EXPERIMENT_ROUTE_PULSE_LINK_PROMPT=1 lua scripts/regression_portal_prompt_pulse_link.lua

package.path = "./?.lua;./?/init.lua;" .. package.path

local Portal = require("src.portal")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_PULSE_LINK_PROMPT") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_PULSE_LINK_PROMPT=1")

Portal.resetCooldown()
Portal.check(10, 10, {
    getPortalAt = function(_, _)
        return { targetMap = "07", targetPortal = "06" }
    end,
})

local compactHighPressure = Portal.getTransitionPrompt(72, { threatTier = "HIGH" })
expect(type(compactHighPressure) == "string", "compact high-pressure prompt should exist")
expect(compactHighPressure:find("PULSE LINK:H", 1, true), "compact high-pressure prompt should include sharp pulse-link cue")

Portal.cancelTransition()
Portal.resetCooldown()
Portal.check(10, 10, {
    getPortalAt = function(_, _)
        return { targetMap = "02", targetPortal = "01" }
    end,
})

local compactLowPressure = Portal.getTransitionPrompt(72, { threatTier = "LOW" })
expect(type(compactLowPressure) == "string", "compact low-pressure prompt should exist")
expect(compactLowPressure:find("PULSE LINK:S", 1, true), "compact low-pressure prompt should include soft pulse-link cue")

Portal.cancelTransition()

print("[PASS] portal compact pulse-link prompt regression validated")
