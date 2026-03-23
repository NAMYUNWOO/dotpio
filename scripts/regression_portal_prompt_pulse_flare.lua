-- Regression: compact portal prompt should include pulse-flare warning token when flare experiment is enabled.
-- Run:
-- DOTPIO_EXPERIMENT_ROUTE_PULSE_MODE_PROMPT=1 \
-- DOTPIO_EXPERIMENT_ROUTE_PULSE_FIT_PROMPT=1 \
-- DOTPIO_EXPERIMENT_ROUTE_PULSE_FLARE_PROMPT=1 \
-- lua scripts/regression_portal_prompt_pulse_flare.lua

package.path = "./?.lua;./?/init.lua;" .. package.path

local Portal = require("src.portal")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_PULSE_MODE_PROMPT") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_PULSE_MODE_PROMPT=1")
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_PULSE_FIT_PROMPT") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_PULSE_FIT_PROMPT=1")
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_PULSE_FLARE_PROMPT") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_PULSE_FLARE_PROMPT=1")

Portal.resetCooldown()
Portal.check(10, 10, {
    getPortalAt = function(_, _)
        return { targetMap = "07", targetPortal = "06" }
    end,
})

local compactSurge = Portal.getTransitionPrompt(72, { threatTier = "HIGH" })
expect(type(compactSurge) == "string", "compact surge prompt should exist")
expect(compactSurge:find("PULSE MODE:X", 1, true), "compact surge prompt should include pulse-mode X")
expect(compactSurge:find("PULSE FIT:R", 1, true), "compact surge prompt should include pulse-fit R")
expect(compactSurge:find("PULSE FLARE:+", 1, true), "compact surge prompt should include pulse-flare token")
Portal.cancelTransition()

Portal.resetCooldown()
Portal.check(10, 10, {
    getPortalAt = function(_, _)
        return { targetMap = "02", targetPortal = "01" }
    end,
})

local compactIdle = Portal.getTransitionPrompt(72, { threatTier = "LOW" })
expect(type(compactIdle) == "string", "compact idle prompt should exist")
expect(compactIdle:find("PULSE MODE:I", 1, true), "compact idle prompt should include pulse-mode I")
expect(not compactIdle:find("PULSE FLARE:+", 1, true), "compact idle prompt should not include pulse-flare token")
Portal.cancelTransition()

print("[PASS] portal compact pulse-flare prompt regression validated")
