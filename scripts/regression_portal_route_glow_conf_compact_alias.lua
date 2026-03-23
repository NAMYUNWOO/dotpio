-- Regression: compact alias token for route glow confidence (`RGC`) when enabled.
-- Run: DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY=1 DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_ARC=1 DOTPIO_EXPERIMENT_ROUTE_GLOW=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_CONF=1 DOTPIO_EXPERIMENT_ROUTE_GLOW_CONF_COMPACT=1 lua scripts/regression_portal_route_glow_conf_compact_alias.lua

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
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_CONF") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_GLOW_CONF=1")
expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_CONF_COMPACT") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_GLOW_CONF_COMPACT=1")

Portal.resetCooldown()
Portal.check(10, 10, {
    getPortalAt = function(_, _)
        return { targetMap = "07", targetPortal = "01" }
    end,
})

local compact = Portal.getTransitionPrompt(80, { threatTier = "LOW", vibeTrail = "CALM" })
expect(type(compact) == "string", "compact prompt should exist")
expect(compact:find("RGC:MID", 1, true), "compact prompt should include RGC:MID when alias flag is enabled")
expect(not compact:find("ROUTE GLOW CONF:", 1, true), "compact prompt should not include long route glow confidence label when alias flag is enabled")

Portal.cancelTransition()
print("[PASS] portal route glow confidence compact alias regression validated")
