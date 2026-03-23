-- Regression: compact ALT STEP WHY confidence alias token experiment.
-- Run: DOTPIO_EXPERIMENT_ALT_STEP_CUE=1 DOTPIO_EXPERIMENT_ALT_STEP_CONF=1 DOTPIO_EXPERIMENT_ALT_STEP_WHY=1 DOTPIO_EXPERIMENT_ALT_STEP_WHY_CONF=1 DOTPIO_EXPERIMENT_ALT_WHY_GLYPH=1 DOTPIO_EXPERIMENT_ALT_WHY_GLYPH_MODE=1 DOTPIO_EXPERIMENT_ALT_WHY_GLYPH_COMPACT=1 DOTPIO_EXPERIMENT_ALT_WHY_GLYPH_MODE_COMPACT=1 DOTPIO_EXPERIMENT_ALT_WHY_GLYPH_MODE_CONF_COMPACT=1 lua scripts/regression_portal_alt_why_glyph_mode_confidence_compact.lua

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
expect(enabled("DOTPIO_EXPERIMENT_ALT_WHY_GLYPH_MODE_COMPACT"), "set DOTPIO_EXPERIMENT_ALT_WHY_GLYPH_MODE_COMPACT=1")
expect(enabled("DOTPIO_EXPERIMENT_ALT_WHY_GLYPH_MODE_CONF_COMPACT"), "set DOTPIO_EXPERIMENT_ALT_WHY_GLYPH_MODE_CONF_COMPACT=1")

Portal.resetCooldown()
Portal.check(14, 14, {
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
expect(detailed:find("ALT STEP WHY CONF:MID", 1, true), "detailed prompt should keep full ALT STEP WHY CONF token")

local compact = Portal.getTransitionPrompt(180, { threatTier = "HIGH" })
expect(compact:find("AWGMC:MID", 1, true), "compact prompt should use AWGMC alias token")
expect(not compact:find("ALT STEP WHY CONF:", 1, true), "compact prompt should not duplicate full ALT STEP WHY CONF token when alias experiment enabled")

Portal.cancelTransition()
print("[PASS] portal compact ALT STEP WHY confidence alias regression validated")
