-- Regression: portal prompts should include pulse-mode cue when experiment flag is enabled.
-- Run: DOTPIO_EXPERIMENT_ROUTE_PULSE_MODE_PROMPT=1 lua scripts/regression_portal_prompt_pulse_mode.lua

package.path = "./?.lua;./?/init.lua;" .. package.path

local Portal = require("src.portal")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_PULSE_MODE_PROMPT") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_PULSE_MODE_PROMPT=1")

Portal.resetCooldown()
Portal.check(10, 10, {
    getPortalAt = function(_, _)
        return { targetMap = "07", targetPortal = "06" }
    end,
})

local detailedSurgeMode = Portal.getTransitionPrompt(512, { threatTier = "HIGH" })
expect(type(detailedSurgeMode) == "string", "detailed surge prompt should exist")
expect(detailedSurgeMode:find("ROUTE PULSE MODE:SURGE", 1, true), "detailed surge prompt should include surge pulse-mode cue")

local compactSurgeMode = Portal.getTransitionPrompt(72, { threatTier = "HIGH" })
expect(type(compactSurgeMode) == "string", "compact surge prompt should exist")
expect(compactSurgeMode:find("PULSE MODE:X", 1, true), "compact surge prompt should include surge pulse-mode cue")

Portal.cancelTransition()
Portal.resetCooldown()
Portal.check(10, 10, {
    getPortalAt = function(_, _)
        return { targetMap = "07", targetPortal = "06" }
    end,
})

local detailedSustainMode = Portal.getTransitionPrompt(512, { threatTier = "MED" })
expect(type(detailedSustainMode) == "string", "detailed sustain prompt should exist")
expect(detailedSustainMode:find("ROUTE PULSE MODE:SUSTAIN", 1, true), "detailed sustain prompt should include sustain pulse-mode cue")

local compactSustainMode = Portal.getTransitionPrompt(72, { threatTier = "MED" })
expect(type(compactSustainMode) == "string", "compact sustain prompt should exist")
expect(compactSustainMode:find("PULSE MODE:S", 1, true), "compact sustain prompt should include sustain pulse-mode cue")

Portal.cancelTransition()
Portal.resetCooldown()
Portal.check(10, 10, {
    getPortalAt = function(_, _)
        return { targetMap = "02", targetPortal = "01" }
    end,
})

local detailedIdleMode = Portal.getTransitionPrompt(512, { threatTier = "LOW" })
expect(type(detailedIdleMode) == "string", "detailed idle prompt should exist")
expect(detailedIdleMode:find("ROUTE PULSE MODE:IDLE", 1, true), "detailed idle prompt should include idle pulse-mode cue")

local compactIdleMode = Portal.getTransitionPrompt(72, { threatTier = "LOW" })
expect(type(compactIdleMode) == "string", "compact idle prompt should exist")
expect(compactIdleMode:find("PULSE MODE:I", 1, true), "compact idle prompt should include idle pulse-mode cue")

Portal.cancelTransition()

print("[PASS] portal detailed+compact pulse-mode prompt regression validated")
