-- Regression: overclock hazard pulse applies build-cost discount + aggro pressure profile.
-- Run: lua scripts/regression_overclock_hazard.lua

package.path = "./?.lua;./?/init.lua;" .. package.path

local OverclockHazard = require("src.overclock_hazard")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

OverclockHazard.onMapLoaded("07", {
    overclockHazard = {
        rect = { x = 10, y = 10, w = 4, h = 4 },
        discountPct = 0.4,
        pulseDuration = 5,
        cooldownDuration = 12,
        aggroMoveMul = 0.7,
        aggroDetectBonus = 2,
    }
})

local readyHint = OverclockHazard.getHudHint()
expect(type(readyHint) == "string" and readyHint:find("OVERCLOCK READY"), "ready hint should be visible before entering hazard zone")
expect(readyHint:find("RISK:[A-Z]+%(%d+%)"), "ready hint should include risk tier + score")

local idleCost = OverclockHazard.applyBuildCost(5)
expect(idleCost == 5, "no pulse: build cost should remain unchanged")

local events = OverclockHazard.update(0.1, 11, 11)
expect(events.activated == true, "entering hazard zone should activate pulse")

local discounted = OverclockHazard.applyBuildCost(5)
expect(discounted == 3, "pulse should discount build cost (5 -> 3)")

local hotHint = OverclockHazard.getHudHint()
expect(type(hotHint) == "string" and hotHint:find("OVERCLOCK HOT") and hotHint:find("%d+s"), "hot hint should include active pulse countdown seconds")
expect(hotHint:find("AGGRO DET:%+%d+"), "hot hint should include aggro detect bonus legend")
expect(hotHint:find("MOVE:%+%d+%%"), "hot hint should include aggro move-speed pressure legend")
expect(hotHint:find("RISK:[A-Z]+%(%d+%)"), "hot hint should include hazard risk tier + score")

local pressure = OverclockHazard.getPressureProfile()
expect(pressure.active == true, "pressure profile should be active during pulse")
expect(pressure.detectBonus == 2, "pressure detect bonus should match hazard config")
expect(math.abs((pressure.moveMul or 1) - 0.7) < 0.001, "pressure move multiplier should match hazard config")

local coolEvent = OverclockHazard.update(6.0, 11, 11)
expect(coolEvent.expired == true, "pulse should expire after timer elapses")

local cooldownHint = OverclockHazard.getHudHint()
expect(type(cooldownHint) == "string" and cooldownHint:find("OVERCLOCK CD") and cooldownHint:find("%d+s"), "cooldown hint should include cooldown seconds")
expect(cooldownHint:find("RISK:[A-Z]+%(%d+%)"), "cooldown hint should keep risk tier + score visible")
expect(not cooldownHint:find("IMMINENT:"), "cooldown hint should not show imminent warning too early")

OverclockHazard.update(3.2, 11, 11)
local imminentHint = OverclockHazard.getHudHint()
expect(type(imminentHint) == "string" and imminentHint:find("IMMINENT:%d+s"), "cooldown hint should show imminent pulse warning when inside zone near ready")

OverclockHazard.update(0.0, 2, 2)
local outsideHint = OverclockHazard.getHudHint()
expect(type(outsideHint) == "string" and not outsideHint:find("IMMINENT:"), "imminent warning should hide when player leaves hazard zone")

local postCost = OverclockHazard.applyBuildCost(5)
expect(postCost == 5, "after expiry: build cost should return to base")

print("[PASS] overclock hazard regression validated")
