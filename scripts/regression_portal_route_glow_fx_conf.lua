-- Regression: compact route-glow FX confidence token experiment.
-- Run: DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_ARC=1 DOTPIO_EXPERIMENT_ROUTE_GLOW=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF=1 DOTPIO_EXPERIMENT_PULSE_HEAT_CUE=1 lua scripts/regression_portal_route_glow_fx_conf.lua

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
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF=1")
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
local lowPrompt = Portal.getTransitionPrompt(80, { threatTier = "LOW", vibeTrail = "CALM" })
expect(type(lowPrompt) == "string", "compact low-pressure prompt should exist")
expect(lowPrompt:find("ROUTE GLOW FX:SOFT", 1, true), "low-pressure compact prompt should include ROUTE GLOW FX:SOFT")
expect(lowPrompt:find("RGFXC:L", 1, true), "low-pressure compact prompt should include RGFXC:L")
Portal.cancelTransition()

openPortal("07")
local midPrompt = Portal.getTransitionPrompt(80, { threatTier = "MED", vibeTrail = "ASH" })
expect(type(midPrompt) == "string", "compact mid-pressure prompt should exist")
expect(midPrompt:find("ROUTE GLOW FX:SHARP", 1, true), "mid-pressure compact prompt should include ROUTE GLOW FX:SHARP")
expect(midPrompt:find("RGFXC:M", 1, true), "mid-pressure compact prompt should include RGFXC:M")
Portal.cancelTransition()

openPortal("07")
local highPrompt = Portal.getTransitionPrompt(80, { threatTier = "HIGH", vibeTrail = "ASH" })
expect(type(highPrompt) == "string", "compact high-pressure prompt should exist")
expect(highPrompt:find("ROUTE GLOW FX:SURGE", 1, true), "high-pressure compact prompt should include ROUTE GLOW FX:SURGE")
expect(highPrompt:find("RGFXC:H", 1, true), "high-pressure compact prompt should include RGFXC:H")
Portal.cancelTransition()

print("[PASS] portal compact route glow FX confidence regression validated")
