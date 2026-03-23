-- Regression: compact portal route-glow pulse-overdrive token experiment.
-- Run: DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_ARC=1 DOTPIO_EXPERIMENT_ROUTE_GLOW=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX=1 DOTPIO_EXPERIMENT_PULSE_HEAT_CUE=1 lua scripts/regression_portal_route_glow_fx.lua

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
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_GLOW_FX=1")
expect(os.getenv("DOTPIO_EXPERIMENT_PULSE_HEAT_CUE") ~= nil, "set DOTPIO_EXPERIMENT_PULSE_HEAT_CUE=1")

local function openPortal(targetMap)
    Portal.resetCooldown()
    Portal.check(10, 10, {
        getPortalAt = function(_, _)
            return { targetMap = targetMap, targetPortal = "01" }
        end,
    })
end

openPortal("02")
local calmPrompt = Portal.getTransitionPrompt(80, { threatTier = "LOW", vibeTrail = "CALM" })
expect(type(calmPrompt) == "string", "compact low-pressure prompt should exist")
expect(calmPrompt:find("ROUTE GLOW:SOFT", 1, true), "low-pressure compact prompt should include ROUTE GLOW:SOFT")
expect(calmPrompt:find("ROUTE GLOW FX:SOFT", 1, true), "low-pressure compact prompt should include ROUTE GLOW FX:SOFT")
Portal.cancelTransition()

openPortal("07")
local warmPrompt = Portal.getTransitionPrompt(80, { threatTier = "MED", vibeTrail = "ASH" })
expect(type(warmPrompt) == "string", "compact mid-pressure prompt should exist")
expect(warmPrompt:find("ROUTE GLOW:SHARP", 1, true), "mid-pressure compact prompt should include ROUTE GLOW:SHARP")
expect(warmPrompt:find("ROUTE GLOW FX:SHARP", 1, true), "mid-pressure compact prompt should include ROUTE GLOW FX:SHARP")
Portal.cancelTransition()

openPortal("07")
local hotPrompt = Portal.getTransitionPrompt(80, { threatTier = "HIGH", vibeTrail = "ASH" })
expect(type(hotPrompt) == "string", "compact high-pressure prompt should exist")
expect(hotPrompt:find("PULSE HEAT:HOT", 1, true), "high-pressure compact prompt should include PULSE HEAT:HOT")
expect(hotPrompt:find("ROUTE GLOW:SHARP", 1, true), "high-pressure compact prompt should include ROUTE GLOW:SHARP")
expect(hotPrompt:find("ROUTE GLOW FX:SURGE", 1, true), "high-pressure compact prompt should include ROUTE GLOW FX:SURGE")
Portal.cancelTransition()

print("[PASS] portal compact route glow FX regression validated")
