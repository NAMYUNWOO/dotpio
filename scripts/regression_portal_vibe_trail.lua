-- Regression: portal cooloff vibe trail token experiment flags.
-- Run: DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_CONF=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY_CONF=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_CONF_RAIL=1 lua scripts/regression_portal_vibe_trail.lua

package.path = package.path .. ";./?.lua;./?/init.lua"

local Portal = require("src.portal")

local function expect(cond, msg)
    if not cond then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

expect(os.getenv("DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL") ~= nil, "set DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL=1")
expect(os.getenv("DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_CONF") ~= nil, "set DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_CONF=1")
expect(os.getenv("DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY") ~= nil, "set DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY=1")
expect(os.getenv("DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY_CONF") ~= nil, "set DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY_CONF=1")
expect(os.getenv("DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_CONF_RAIL") ~= nil, "set DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_CONF_RAIL=1")

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
local calmPrompt = Portal.getTransitionPrompt(240, { threatTier = "LOW", vibeTrail = "CALM" })
expect(calmPrompt:find("VIBE TRAIL:CALM", 1, true), "detailed prompt should include CALM vibe trail token")
expect(calmPrompt:find("VIBE TRAIL CONF:MID", 1, true), "detailed prompt should include CALM confidence token")
expect(calmPrompt:find("VIBE TRAIL WHY:RECOVER", 1, true), "detailed prompt should include CALM rationale token")
expect(calmPrompt:find("VIBE TRAIL CONF RAIL:STEADY", 1, true), "detailed prompt should include CALM confidence rail token")
expect(calmPrompt:find("VIBE TRAIL WHY CONF:MID", 1, true), "detailed prompt should include CALM rationale confidence token")

local calmCompact = Portal.getTransitionPrompt(80, { threatTier = "LOW", vibeTrail = "CALM" })
expect(calmCompact:find("VTR:C", 1, true), "compact prompt should include VTR:C token")
expect(calmCompact:find("VTC:M", 1, true), "compact prompt should include VTC:M token")
expect(calmCompact:find("VTCR:S", 1, true), "compact prompt should include VTCR:S token")
expect(calmCompact:find("VIBE TRAIL WHY:RECOVER", 1, true), "compact prompt should include CALM rationale token")
expect(calmCompact:find("VTWC:M", 1, true), "compact prompt should include CALM rationale confidence token")
Portal.cancelTransition()
clearPortalTile()

Portal.check(2, 2, buildMap("91"))
local ashPrompt = Portal.getTransitionPrompt(240, { threatTier = "LOW", vibeTrail = "ASH" })
expect(ashPrompt:find("VIBE TRAIL:ASH", 1, true), "detailed prompt should include ASH vibe trail token")
expect(ashPrompt:find("VIBE TRAIL CONF:HIGH", 1, true), "detailed prompt should include ASH confidence token")
expect(ashPrompt:find("VIBE TRAIL WHY:SCAR", 1, true), "detailed prompt should include ASH rationale token")
expect(ashPrompt:find("VIBE TRAIL CONF RAIL:SPIKE", 1, true), "detailed prompt should include ASH confidence rail token")
expect(ashPrompt:find("VIBE TRAIL WHY CONF:HIGH", 1, true), "detailed prompt should include ASH rationale confidence token")

local ashCompact = Portal.getTransitionPrompt(80, { threatTier = "LOW", vibeTrail = "ASH" })
expect(ashCompact:find("VTR:A", 1, true), "compact prompt should include VTR:A token")
expect(ashCompact:find("VTC:H", 1, true), "compact prompt should include VTC:H token")
expect(ashCompact:find("VTCR:X", 1, true), "compact prompt should include VTCR:X token")
expect(ashCompact:find("VIBE TRAIL WHY:SCAR", 1, true), "compact prompt should include ASH rationale token")
expect(ashCompact:find("VTWC:H", 1, true), "compact prompt should include ASH rationale confidence token")
Portal.cancelTransition()
clearPortalTile()

Portal.check(3, 3, buildMap("91"))
local badPrompt = Portal.getTransitionPrompt(240, { threatTier = "LOW", vibeTrail = "NOISE" })
expect(not badPrompt:find("VIBE TRAIL:", 1, true), "invalid vibeTrail context should be ignored")
expect(not badPrompt:find("VTC:", 1, true), "invalid vibeTrail context should not emit compact confidence token")
expect(not badPrompt:find("VIBE TRAIL WHY:", 1, true), "invalid vibeTrail context should not emit rationale token")
expect(not badPrompt:find("VIBE TRAIL CONF RAIL:", 1, true), "invalid vibeTrail context should not emit confidence rail token")
expect(not badPrompt:find("VTWC:", 1, true), "invalid vibeTrail context should not emit rationale confidence token")
expect(not badPrompt:find("VTCR:", 1, true), "invalid vibeTrail context should not emit compact confidence rail token")
Portal.cancelTransition()
clearPortalTile()

Portal._setRouteTagOverride("91", nil)
Portal.resetCooldown()

print("[PASS] portal vibe trail regression validated")
