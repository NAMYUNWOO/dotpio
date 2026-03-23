-- Regression: compact portal prompt should honor pulse token priority mode under strict budget.
-- Run:
--   DOTPIO_EXPERIMENT_ROUTE_PULSE_MODE_PROMPT=1 \
--   DOTPIO_EXPERIMENT_ROUTE_PULSE_FIT_PROMPT=1 \
--   DOTPIO_EXPERIMENT_ROUTE_PULSE_TOKEN_PRIORITY=FIT-FIRST \
--   lua scripts/regression_portal_prompt_pulse_token_priority.lua

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

local priority = string.upper(tostring(os.getenv("DOTPIO_EXPERIMENT_ROUTE_PULSE_TOKEN_PRIORITY") or ""))
expect(priority == "FIT-FIRST" or priority == "MODE-FIRST", "set DOTPIO_EXPERIMENT_ROUTE_PULSE_TOKEN_PRIORITY=FIT-FIRST|MODE-FIRST")

Portal.resetCooldown()
Portal.check(10, 10, {
    getPortalAt = function(_, _)
        return { targetMap = "07", targetPortal = "06" }
    end,
})

local compactPrompt = Portal.getTransitionPrompt(100, { threatTier = "HIGH" })
expect(type(compactPrompt) == "string", "compact prompt should exist")

if priority == "FIT-FIRST" then
    expect(compactPrompt:find("PRI:F", 1, true), "FIT-FIRST should include compact priority cue")
    expect(compactPrompt:find("PULSE FIT:R", 1, true), "FIT-FIRST should keep PULSE FIT token under budget")
    expect(not compactPrompt:find("PULSE MODE:X", 1, true), "FIT-FIRST should drop later PULSE MODE token under strict budget")
else
    expect(compactPrompt:find("PRI:M", 1, true), "MODE-FIRST should include compact priority cue")
    expect(compactPrompt:find("PULSE MODE:X", 1, true), "MODE-FIRST should keep PULSE MODE token under budget")
    expect(not compactPrompt:find("PULSE FIT:R", 1, true), "MODE-FIRST should drop later PULSE FIT token under strict budget")
end

Portal.cancelTransition()

print("[PASS] portal compact pulse token-priority regression validated")
