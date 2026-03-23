-- Regression: portal ALT WHY GLYPH compact rationale experiment flag.
-- Run: DOTPIO_EXPERIMENT_ALT_STEP_CUE=1 DOTPIO_EXPERIMENT_ALT_STEP_CONF=1 DOTPIO_EXPERIMENT_ALT_STEP_WHY=1 DOTPIO_EXPERIMENT_ALT_STEP_WHY_CONF=1 DOTPIO_EXPERIMENT_ALT_WHY_GLYPH=1 lua scripts/regression_portal_alt_why_glyph.lua

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
local whyConfEnabled = os.getenv("DOTPIO_EXPERIMENT_ALT_STEP_WHY_CONF")
local glyphEnabled = os.getenv("DOTPIO_EXPERIMENT_ALT_WHY_GLYPH")

expect(cueEnabled == "1" or cueEnabled == "true" or cueEnabled == "on" or cueEnabled == "yes", "set DOTPIO_EXPERIMENT_ALT_STEP_CUE=1 when running this regression")
expect(confEnabled == "1" or confEnabled == "true" or confEnabled == "on" or confEnabled == "yes", "set DOTPIO_EXPERIMENT_ALT_STEP_CONF=1 when running this regression")
expect(whyEnabled == "1" or whyEnabled == "true" or whyEnabled == "on" or whyEnabled == "yes", "set DOTPIO_EXPERIMENT_ALT_STEP_WHY=1 when running this regression")
expect(whyConfEnabled == "1" or whyConfEnabled == "true" or whyConfEnabled == "on" or whyConfEnabled == "yes", "set DOTPIO_EXPERIMENT_ALT_STEP_WHY_CONF=1 when running this regression")
expect(glyphEnabled == "1" or glyphEnabled == "true" or glyphEnabled == "on" or glyphEnabled == "yes", "set DOTPIO_EXPERIMENT_ALT_WHY_GLYPH=1 when running this regression")

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

local detailed = Portal.getTransitionPrompt(320, { threatTier = "HIGH" })
expect(detailed:find("ALT STEP WHY:PRESSURE", 1, true), "detailed prompt should include ALT STEP WHY token")
expect(detailed:find("ALT WHY GLYPH:!", 1, true), "detailed prompt should include ALT WHY GLYPH token")

local compact = Portal.getTransitionPrompt(180, { threatTier = "HIGH" })
expect(compact:find("ALT STEP WHY:PRESSURE", 1, true), "compact prompt should include ALT STEP WHY token")
expect(compact:find("ALT WHY GLYPH:!", 1, true), "compact prompt should include ALT WHY GLYPH token")

Portal.cancelTransition()
print("[PASS] portal ALT WHY GLYPH regression validated")
