-- Regression: compact route-glow FX confidence rationale rail token experiment.
-- Run: DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_ARC=1 DOTPIO_EXPERIMENT_ROUTE_GLOW=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL=1 DOTPIO_EXPERIMENT_PULSE_HEAT_CUE=1 lua scripts/regression_portal_route_glow_fx_conf_why_rail.lua

package.path = package.path .. ";./?.lua;./?/init.lua"

local Portal = require("src.portal")

local function expect(cond, msg)
    if not cond then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY=1")
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL=1")

local function openPortal(targetMap)
    Portal.resetCooldown()
    Portal.check(10, 10, {
        getPortalAt = function(_, _)
            return { targetMap = targetMap, targetPortal = "01" }
        end,
    })
end

openPortal("02")
local lowPrompt = Portal.getTransitionPrompt(120, { threatTier = "LOW", vibeTrail = "CALM" })
expect(type(lowPrompt) == "string", "compact low-pressure prompt should exist")
expect(lowPrompt:find("ROUTE GLOW FX CONF WHY:STABLE", 1, true), "low-pressure prompt should include STABLE rationale")
expect(lowPrompt:find("ROUTE GLOW FX CONF WHY RAIL:STEADY", 1, true), "low-pressure prompt should include STEADY rail token")
Portal.cancelTransition()

openPortal("07")
local midPrompt = Portal.getTransitionPrompt(120, { threatTier = "MED", vibeTrail = "ASH" })
expect(type(midPrompt) == "string", "compact mid-pressure prompt should exist")
expect(midPrompt:find("ROUTE GLOW FX CONF WHY:PRESSURE", 1, true), "mid-pressure prompt should include PRESSURE rationale")
expect(midPrompt:find("ROUTE GLOW FX CONF WHY RAIL:SPIKE", 1, true), "mid-pressure prompt should include SPIKE rail token")
Portal.cancelTransition()

openPortal("07")
local highPrompt = Portal.getTransitionPrompt(120, { threatTier = "HIGH", vibeTrail = "ASH" })
expect(type(highPrompt) == "string", "compact high-pressure prompt should exist")
expect(highPrompt:find("ROUTE GLOW FX CONF WHY:OVERDRIVE", 1, true), "high-pressure prompt should include OVERDRIVE rationale")
expect(highPrompt:find("ROUTE GLOW FX CONF WHY RAIL:SPIKE", 1, true), "high-pressure prompt should include SPIKE rail token")
Portal.cancelTransition()

print("[PASS] portal compact route glow FX confidence rationale rail regression validated")
