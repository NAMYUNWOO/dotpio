-- Regression: compact portal route afterglow cue experiment flag.
-- Run: DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_ARC=1 DOTPIO_EXPERIMENT_ROUTE_GLOW=1 lua scripts/regression_portal_route_glow.lua

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
expect(os.getenv("DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_ARC") ~= nil, "set DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_ARC=1")
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_GLOW=1")

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

local function clearPortalTile()
    Portal.check(0, 0, {
        portals = {},
        getPortalAt = function(_, _)
            return nil
        end,
    })
end

Portal.resetCooldown()
Portal._setRouteTagOverride("91", "SAFE")

Portal.check(1, 1, buildMap("91"))
local calmCompact = Portal.getTransitionPrompt(80, { threatTier = "LOW", vibeTrail = "CALM" })
expect(calmCompact:find("VTA:R", 1, true), "compact prompt should include CALM arc token")
expect(calmCompact:find("ROUTE GLOW:SOFT", 1, true), "compact prompt should include SOFT route glow for RECOVER arc")
Portal.cancelTransition()
clearPortalTile()

Portal.check(2, 2, buildMap("91"))
local ashCompact = Portal.getTransitionPrompt(80, { threatTier = "LOW", vibeTrail = "ASH" })
expect(ashCompact:find("VTA:S", 1, true), "compact prompt should include ASH arc token")
expect(ashCompact:find("ROUTE GLOW:SHARP", 1, true), "compact prompt should include SHARP route glow for SCAR arc")
Portal.cancelTransition()
clearPortalTile()

Portal._setRouteTagOverride("91", nil)
Portal.resetCooldown()

print("[PASS] portal compact route glow regression validated")
