-- Regression: compact portal prompt should include pulse-fit cue when experiment flag is enabled.
-- Run: DOTPIO_EXPERIMENT_ROUTE_PULSE_FIT_PROMPT=1 lua scripts/regression_portal_prompt_pulse_fit.lua

package.path = "./?.lua;./?/init.lua;" .. package.path

local Portal = require("src.portal")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_PULSE_FIT_PROMPT") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_PULSE_FIT_PROMPT=1")

Portal.resetCooldown()
Portal.check(10, 10, {
    getPortalAt = function(_, _)
        return { targetMap = "02", targetPortal = "01" }
    end,
})

local compactIdleFit = Portal.getTransitionPrompt(72, { threatTier = "LOW" })
expect(type(compactIdleFit) == "string", "compact idle-fit prompt should exist")
expect(compactIdleFit:find("PULSE FIT:Y", 1, true), "compact idle-fit prompt should include Y cue")
Portal.cancelTransition()

Portal.resetCooldown()
Portal.check(10, 10, {
    getPortalAt = function(_, _)
        return { targetMap = "07", targetPortal = "06" }
    end,
})

local compactBreakFit = Portal.getTransitionPrompt(72, { threatTier = "MED" })
expect(type(compactBreakFit) == "string", "compact break-fit prompt should exist")
expect(compactBreakFit:find("PULSE FIT:B", 1, true), "compact medium-pressure prompt should include B cue when alt route exists")
Portal.cancelTransition()

Portal.resetCooldown()
Portal.check(10, 10, {
    getPortalAt = function(_, _)
        return { targetMap = "07", targetPortal = "06" }
    end,
})

local compactResetFit = Portal.getTransitionPrompt(72, { threatTier = "HIGH" })
expect(type(compactResetFit) == "string", "compact reset-fit prompt should exist")
expect(compactResetFit:find("PULSE FIT:R", 1, true), "compact high-pressure prompt should include R cue")
Portal.cancelTransition()

print("[PASS] portal compact pulse-fit prompt regression validated")
