-- Regression: compact portal prompt uses budget-aware unknown-route coach fallback.
-- Run: lua scripts/regression_portal_unknown_compact_coach.lua

package.path = "./?.lua;./?/init.lua;" .. package.path

local Portal = require("src.portal")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

Portal.resetCooldown()
Portal.check(10, 10, {
    getPortalAt = function(_, _)
        return { targetMap = "01", targetPortal = "02" }
    end,
})

expect(Portal.hasPendingTransition(), "portal should enter pending transition state")

local compactWithHeadroom = Portal.getTransitionPrompt(86, { threatTier = "LOW" })
expect(type(compactWithHeadroom) == "string", "compact prompt should render with medium budget")
expect(compactWithHeadroom:find("NEXT:UNKNOWN", 1, true), "compact prompt should keep UNKNOWN route tag")
expect(compactWithHeadroom:find("COACH:NO DATA", 1, true), "compact prompt should prefer NO DATA unknown coach when budget allows")

local tightCompact = Portal.getTransitionPrompt(82, { threatTier = "LOW" })
expect(type(tightCompact) == "string", "compact prompt should render with tight budget")
expect(tightCompact:find("COACH:UNK", 1, true), "compact prompt should fall back to UNK unknown coach when NO DATA exceeds budget")

Portal.cancelTransition()

print("[PASS] portal compact unknown coach budget fallback regression validated")
