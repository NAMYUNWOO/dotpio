-- Regression: vibe-consistency reward hint experiment flag.
-- Run: DOTPIO_EXPERIMENT_ROUTE_VIBE_SYNC_HINT=1 lua scripts/regression_portal_route_vibe_sync_hint.lua

package.path = package.path .. ";./?.lua;./?/init.lua"

local Portal = require("src.portal")

local function expect(cond, msg)
    if not cond then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

expect(os.getenv("DOTPIO_EXPERIMENT_ROUTE_VIBE_SYNC_HINT") ~= nil, "set DOTPIO_EXPERIMENT_ROUTE_VIBE_SYNC_HINT=1")

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
Portal._setRouteTagOverride("92", "RISK")

-- Transition 1: aligned (SAFE + LOW) -> no hint yet, chain 1/3.
Portal.check(1, 1, buildMap("91"))
local p1 = Portal.getTransitionPrompt(240, { threatTier = "LOW" })
expect(p1:find("VIBE CHAIN:1/3", 1, true), "first aligned transition should show chain 1/3")
expect(not p1:find("VIBE SYNC:%+1"), "first aligned transition should not show sync hint")
Portal.confirmTransition()
clearPortalTile()

-- Transition 2: aligned (RISK + MED) -> no hint yet, chain 2/3.
Portal.check(2, 2, buildMap("92"))
local p2 = Portal.getTransitionPrompt(240, { threatTier = "MED" })
expect(p2:find("VIBE CHAIN:2/3", 1, true), "second aligned transition should show chain 2/3")
expect(not p2:find("VIBE SYNC:%+1"), "second aligned transition should not show sync hint")
Portal.confirmTransition()
clearPortalTile()

-- Transition 3: aligned (SAFE + LOW) -> hint should appear.
Portal.check(3, 3, buildMap("91"))
local p3 = Portal.getTransitionPrompt(240, { threatTier = "LOW" })
expect(p3:find("VIBE CHAIN:3/3", 1, true), "third aligned transition should show chain 3/3")
expect(p3:find("VIBE SYNC:%+1"), "third aligned transition should show sync hint")
local compact = Portal.getTransitionPrompt(70, { threatTier = "LOW" })
expect(compact:find("VSC:3/3", 1, true), "compact prompt should include compact chain token")
expect(compact:find("VS:%+1"), "compact prompt should include compact sync hint token")
Portal.confirmTransition()
clearPortalTile()

-- Transition 4: misaligned resets streak (SAFE + HIGH) -> chain 0/3 and no hint.
Portal.check(4, 4, buildMap("91"))
local misaligned = Portal.getTransitionPrompt(240, { threatTier = "HIGH" })
expect(misaligned:find("VIBE CHAIN:0/3", 1, true), "misaligned transition should show chain reset 0/3")
expect(not misaligned:find("VIBE SYNC:%+1"), "misaligned transition should not show sync hint")
Portal.confirmTransition()
clearPortalTile()

-- Next aligned should start from streak=1 (still no hint).
Portal.check(5, 5, buildMap("91"))
local restart = Portal.getTransitionPrompt(240, { threatTier = "LOW" })
expect(restart:find("VIBE CHAIN:1/3", 1, true), "streak should restart at chain 1/3 after misalignment")
expect(not restart:find("VIBE SYNC:%+1"), "streak should reset after misalignment")
Portal.cancelTransition()

Portal._setRouteTagOverride("91", nil)
Portal._setRouteTagOverride("92", nil)
Portal.resetCooldown()

print("[PASS] portal route-vibe sync hint regression validated")
