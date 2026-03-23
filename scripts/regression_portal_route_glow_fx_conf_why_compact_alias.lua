-- Regression: compact alias token for route-glow FX confidence rationale (`RGFXW`) when enabled.
-- Run: DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_ARC=1 DOTPIO_EXPERIMENT_ROUTE_GLOW=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_COMPACT=1 DOTPIO_EXPERIMENT_PULSE_HEAT_CUE=1 lua scripts/regression_portal_route_glow_fx_conf_why_compact_alias.lua

package.path = package.path .. ";./?.lua;./?/init.lua"

local Portal = require("src.portal")

local function expect(cond, msg)
    if not cond then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_COMPACT") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_COMPACT=1")

local function openPortal(targetMap)
    Portal.resetCooldown()
    Portal.check(10, 10, {
        getPortalAt = function(_, _)
            return { targetMap = targetMap, targetPortal = "01" }
        end,
    })
end

openPortal("07")
local prompt = Portal.getTransitionPrompt(80, { threatTier = "HIGH", vibeTrail = "ASH" })
expect(type(prompt) == "string", "compact prompt should exist")
expect(prompt:find("RGFXW:O", 1, true), "compact prompt should include RGFXW:O when compact alias flag is enabled")
expect(not prompt:find("ROUTE GLOW FX CONF WHY:", 1, true), "compact prompt should not include long rationale label when alias flag is enabled")
Portal.cancelTransition()

print("[PASS] portal compact route glow FX confidence rationale alias regression validated")
