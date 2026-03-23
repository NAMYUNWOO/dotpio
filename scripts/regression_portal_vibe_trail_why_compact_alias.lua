-- Regression: compact alias token for portal vibe trail rationale.
-- Run: DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY_COMPACT_ALIAS=1 lua scripts/regression_portal_vibe_trail_why_compact_alias.lua

package.path = package.path .. ";./?.lua;./?/init.lua"

local Portal = require("src.portal")

local function expect(cond, msg)
    if not cond then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

expect(os.getenv("DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL") ~= nil, "set DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL=1")
expect(os.getenv("DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY") ~= nil, "set DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY=1")
expect(os.getenv("DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY_COMPACT_ALIAS") ~= nil, "set DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY_COMPACT_ALIAS=1")

local function buildMap(targetMap)
    return {
        portals = {
            { targetMap = targetMap, targetPortal = "A" },
        },
        getPortalAt = function(_, _)
            return { targetMap = targetMap, targetPortal = "A" }
        end,
    }
end

Portal.resetCooldown()
Portal._setRouteTagOverride("91", "SAFE")
Portal.check(1, 1, buildMap("91"))

local detailed = Portal.getTransitionPrompt(240, { threatTier = "LOW", vibeTrail = "CALM" })
expect(detailed:find("VIBE TRAIL WHY:RECOVER", 1, true), "detailed prompt should keep full rationale label")

local compact = Portal.getTransitionPrompt(80, { threatTier = "LOW", vibeTrail = "CALM" })
expect(compact:find("VTW:RECOVER", 1, true), "compact prompt should include VTW alias token")
expect(not compact:find("VIBE TRAIL WHY:", 1, true), "compact prompt should not duplicate full VIBE TRAIL WHY label when alias enabled")

Portal.cancelTransition()
Portal._setRouteTagOverride("91", nil)
Portal.resetCooldown()

print("[PASS] portal vibe trail why compact alias regression validated")
