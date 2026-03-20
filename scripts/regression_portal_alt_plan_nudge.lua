-- Regression: portal ALT PLAN nudge experiment flag.
-- Run: DOTPIO_EXPERIMENT_ALT_PLAN_NUDGE=1 lua scripts/regression_portal_alt_plan_nudge.lua

package.path = "./?.lua;./?/init.lua;" .. package.path

local Portal = require("src.portal")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

local enabled = os.getenv("DOTPIO_EXPERIMENT_ALT_PLAN_NUDGE")
expect(enabled == "1" or enabled == "true" or enabled == "on" or enabled == "yes", "set DOTPIO_EXPERIMENT_ALT_PLAN_NUDGE=1 when running this regression")

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

local detailed = Portal.getTransitionPrompt(200, { threatTier = "HIGH" })
expect(detailed:find("ALT ROUTE:RISK", 1, true), "detailed prompt should include adaptive ALT route")
expect(detailed:find("ALT PLAN:LOWER RISK", 1, true), "detailed prompt should include ALT PLAN nudge token when experiment enabled")

local compact = Portal.getTransitionPrompt(86, { threatTier = "HIGH" })
expect(compact:find("ALT:RISK", 1, true), "compact prompt should include adaptive ALT route")
expect(compact:find("AP:LOW", 1, true), "compact prompt should include compact ALT PLAN nudge token")

Portal.cancelTransition()
print("[PASS] portal ALT PLAN nudge experiment regression validated")
