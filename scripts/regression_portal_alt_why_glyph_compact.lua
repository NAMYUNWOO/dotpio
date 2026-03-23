-- Regression: compact ALT WHY glyph alias token experiment.
-- Run: DOTPIO_EXPERIMENT_ALT_STEP_CUE=1 DOTPIO_EXPERIMENT_ALT_STEP_CONF=1 DOTPIO_EXPERIMENT_ALT_STEP_WHY=1 DOTPIO_EXPERIMENT_ALT_STEP_WHY_CONF=1 DOTPIO_EXPERIMENT_ALT_WHY_GLYPH=1 DOTPIO_EXPERIMENT_ALT_WHY_GLYPH_MODE=1 DOTPIO_EXPERIMENT_ALT_WHY_GLYPH_COMPACT=1 lua scripts/regression_portal_alt_why_glyph_compact.lua

package.path = "./?.lua;./?/init.lua;" .. package.path

local Portal = require("src.portal")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

local function enabled(name)
    local value = string.lower(tostring(os.getenv(name) or ""))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

expect(enabled("DOTPIO_EXPERIMENT_ALT_STEP_CUE"), "set DOTPIO_EXPERIMENT_ALT_STEP_CUE=1")
expect(enabled("DOTPIO_EXPERIMENT_ALT_STEP_CONF"), "set DOTPIO_EXPERIMENT_ALT_STEP_CONF=1")
expect(enabled("DOTPIO_EXPERIMENT_ALT_STEP_WHY"), "set DOTPIO_EXPERIMENT_ALT_STEP_WHY=1")
expect(enabled("DOTPIO_EXPERIMENT_ALT_STEP_WHY_CONF"), "set DOTPIO_EXPERIMENT_ALT_STEP_WHY_CONF=1")
expect(enabled("DOTPIO_EXPERIMENT_ALT_WHY_GLYPH"), "set DOTPIO_EXPERIMENT_ALT_WHY_GLYPH=1")
expect(enabled("DOTPIO_EXPERIMENT_ALT_WHY_GLYPH_MODE"), "set DOTPIO_EXPERIMENT_ALT_WHY_GLYPH_MODE=1")
expect(enabled("DOTPIO_EXPERIMENT_ALT_WHY_GLYPH_COMPACT"), "set DOTPIO_EXPERIMENT_ALT_WHY_GLYPH_COMPACT=1")

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
expect(detailed:find("ALT WHY GLYPH:!", 1, true), "detailed prompt should keep full ALT WHY GLYPH token")
expect(detailed:find("ALT WHY GLYPH MODE:SPIKE", 1, true), "detailed prompt should include ALT WHY GLYPH MODE token")

local compact = Portal.getTransitionPrompt(180, { threatTier = "HIGH" })
expect(compact:find("AWG:!", 1, true), "compact prompt should use AWG alias token")
expect(not compact:find("ALT WHY GLYPH:", 1, true), "compact prompt should not duplicate full ALT WHY GLYPH token when alias experiment enabled")
expect(compact:find("ALT WHY GLYPH MODE:SPIKE", 1, true), "compact prompt should include ALT WHY GLYPH MODE token")

Portal.cancelTransition()
print("[PASS] portal compact ALT WHY glyph alias regression validated")
