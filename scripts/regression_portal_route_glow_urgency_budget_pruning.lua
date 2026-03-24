-- Regression: deterministic budget-headroom pruning keeps core urgency token while dropping urgency parity/FX stack when compact prompt budget is saturated.
-- Run: DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_ARC=1 DOTPIO_EXPERIMENT_ROUTE_GLOW=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_COMPACT=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_COMPACT=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_COMPACT=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_MODE=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF_COMPACT=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF_URGENCY=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF_URGENCY_PARITY=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF_URGENCY_PARITY_COMPACT=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF_URGENCY_FX=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF_WHY_RAIL_INTENSITY_WHY_CONF_URGENCY_COACH=1 lua scripts/regression_portal_route_glow_urgency_budget_pruning.lua

package.path = package.path .. ";./?.lua;./?/init.lua"

local Portal = require("src.portal")

local function expect(cond, msg)
    if not cond then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

local function promptFor(maxChars)
    Portal.resetCooldown()
    Portal._setRouteTagOverride("02", "SPIKE")
    Portal.check(10, 10, {
        getPortalAt = function(_, _)
            return { targetMap = "02", targetPortal = "01" }
        end,
    })
    local prompt = Portal.getTransitionPrompt(maxChars, { threatTier = "HIGH", vibeTrail = "ASH" })
    expect(type(prompt) == "string", "prompt should exist")
    Portal.cancelTransition()
    return prompt
end

local tight = promptFor(150)
expect(tight:find("RGFXWRIU:", 1, true), "tight budget should keep core urgency token")
expect(not tight:find("RGFXWRIUP:", 1, true), "tight budget should prune urgency parity compact token first")
expect(not tight:find("RGFXWRIU COACH:", 1, true), "tight budget should prune urgency coach token")
expect(not tight:find("RGFXWRIUFX:", 1, true), "tight budget should prune urgency FX token")

local looser = promptFor(170)
expect(looser:find("RGFXWRIU:", 1, true), "looser budget should still keep core urgency token")
expect(not looser:find("RGFXWRIUP:", 1, true), "looser budget still prunes urgency parity when headroom is exhausted")
expect(not looser:find("RGFXWRIUFX:", 1, true), "looser budget still prunes urgency FX when headroom is exhausted")

Portal._setRouteTagOverride("02", nil)
print("[PASS] portal route glow urgency budget pruning regression validated")
