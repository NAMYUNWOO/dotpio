-- Regression: portal ALT STEP WHY rationale micro-cue experiment flag.
-- Run: DOTPIO_EXPERIMENT_ALT_STEP_CUE=1 DOTPIO_EXPERIMENT_ALT_STEP_CONF=1 DOTPIO_EXPERIMENT_ALT_STEP_WHY=1 lua scripts/regression_portal_alt_step_why.lua

package.path = "./?.lua;./?/init.lua;" .. package.path

local Portal = require("src.portal")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

local cueEnabled = os.getenv("DOTPIO_EXPERIMENT_ALT_STEP_CUE")
local confEnabled = os.getenv("DOTPIO_EXPERIMENT_ALT_STEP_CONF")
local whyEnabled = os.getenv("DOTPIO_EXPERIMENT_ALT_STEP_WHY")
expect(cueEnabled == "1" or cueEnabled == "true" or cueEnabled == "on" or cueEnabled == "yes", "set DOTPIO_EXPERIMENT_ALT_STEP_CUE=1 when running this regression")
expect(confEnabled == "1" or confEnabled == "true" or confEnabled == "on" or confEnabled == "yes", "set DOTPIO_EXPERIMENT_ALT_STEP_CONF=1 when running this regression")
expect(whyEnabled == "1" or whyEnabled == "true" or whyEnabled == "on" or whyEnabled == "yes", "set DOTPIO_EXPERIMENT_ALT_STEP_WHY=1 when running this regression")

Portal.resetCooldown()
Portal.check(12, 12, {
    currentMap = "06",
    portals = {
        { targetMap = "07", targetPortal = "06" },
        { targetMap = "05", targetPortal = "06" },
    },
    getPortalAt = function(_, _)
        return { targetMap = "07", targetPortal = "06" }
    end,
})

local detailed = Portal.getTransitionPrompt(280, { threatTier = "HIGH" })
expect(detailed:find("ALT STEP:BAIT", 1, true), "detailed prompt should include ALT STEP token")
expect(detailed:find("ALT STEP CONF:MID", 1, true), "detailed prompt should include ALT STEP CONF token")
expect(detailed:find("ALT STEP WHY:PRESSURE", 1, true), "detailed prompt should include ALT STEP WHY rationale token")

local compact = Portal.getTransitionPrompt(140, { threatTier = "HIGH" })
expect(compact:find("ALT STEP:BAIT", 1, true), "compact prompt should include ALT STEP token")
expect(compact:find("ALT STEP CONF:MID", 1, true), "compact prompt should include ALT STEP CONF token")
expect(compact:find("ALT STEP WHY:PRESSURE", 1, true), "compact prompt should include ALT STEP WHY rationale token")

Portal.cancelTransition()
print("[PASS] portal ALT STEP WHY rationale micro-cue regression validated")
