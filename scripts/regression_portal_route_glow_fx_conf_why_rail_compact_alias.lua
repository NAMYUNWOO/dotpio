-- Regression: compact alias token for route-glow FX confidence rationale rail (`RGFXWR`) when enabled.
-- Run: DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_ARC=1 DOTPIO_EXPERIMENT_ROUTE_GLOW=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_COMPACT=1 DOTPIO_EXPERIMENT_PULSE_HEAT_CUE=1 lua scripts/regression_portal_route_glow_fx_conf_why_rail_compact_alias.lua

package.path = package.path .. ";./?.lua;./?/init.lua"

local Portal = require("src.portal")

local function expect(cond, msg)
    if not cond then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL=1")
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_COMPACT") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_COMPACT=1")

Portal.resetCooldown()
Portal.check(10, 10, {
    getPortalAt = function(_, _)
        return { targetMap = "02", targetPortal = "01" }
    end,
})

local prompt = Portal.getTransitionPrompt(120, { threatTier = "LOW", vibeTrail = "CALM" })
expect(type(prompt) == "string", "compact prompt should exist")
expect(prompt:find("RGFXWR:STEADY", 1, true), "compact prompt should include RGFXWR rail token")
expect(not prompt:find("ROUTE GLOW FX CONF WHY RAIL:", 1, true), "compact prompt should not include long rail label when alias flag is enabled")
Portal.cancelTransition()

print("[PASS] portal compact route glow FX confidence rationale rail alias regression validated")
