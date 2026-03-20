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
        aggroMoveMul = 0.6,
        aggroDetectBonus = 2,
    }
})

local readyHint = OverclockHazard.getHudHint()
expect(type(readyHint) == "string" and readyHint:find("OVERCLOCK READY"), "ready hint should be visible before entering hazard zone")
expect(readyHint:find("NEXT BOUNTY:0/%d+"), "ready hint should include next-pulse bounty budget token")
expect(readyHint:find("RISK:[A-Z]+%(%d+%)"), "ready hint should include risk tier + score")
expect(readyHint:find("RISK SRC:D%d+%+DET%d+%+MOVE%d+"), "ready hint should include compact risk-factor breakdown token")

local highRiskColor = OverclockHazard.getHudHintColor()
expect(type(highRiskColor) == "table" and #highRiskColor >= 3, "risk tier color should be exposed for HUD rendering")
expect(math.abs(highRiskColor[1] - 1) < 0.001 and math.abs(highRiskColor[2] - 0.34) < 0.001 and math.abs(highRiskColor[3] - 0.25) < 0.001, "high-risk tier should map to red HUD color")

local idleCost = OverclockHazard.applyBuildCost(5)
expect(idleCost == 5, "no pulse: build cost should remain unchanged")

local events = OverclockHazard.update(0.1, 11, 11)
expect(events.activated == true, "entering hazard zone should activate pulse")

local discounted = OverclockHazard.applyBuildCost(5)
expect(discounted == 3, "pulse should discount build cost (5 -> 3)")

local hotHintBeforeKills = OverclockHazard.getHudHint()
expect(type(hotHintBeforeKills) == "string" and hotHintBeforeKills:find("BOUNTY:0/3"), "hot hint should show zeroed bounty progress at pulse start")

local killBonusFirst = OverclockHazard.consumeKillBonus(2)
expect(killBonusFirst == 2, "hot-zone kills should award overclock bonus SRL per kill")

local killBonusCapped = OverclockHazard.consumeKillBonus(3)
expect(killBonusCapped == 1, "per-pulse overclock kill bonus should respect configured cap")

local hotHint = OverclockHazard.getHudHint()
expect(type(hotHint) == "string" and hotHint:find("OVERCLOCK HOT") and hotHint:find("%d+s"), "hot hint should include active pulse countdown seconds")
expect(hotHint:find("AGGRO DET:%+%d+"), "hot hint should include aggro detect bonus legend")
expect(hotHint:find("MOVE:%+%d+%%"), "hot hint should include aggro move-speed pressure legend")
expect(hotHint:find("BOUNTY:%d+/%d+"), "hot hint should include bounty progress token")
expect(hotHint:find("BOUNTY:3/3"), "bounty progress token should reflect per-pulse cap consumption")
expect(hotHint:find("RISK:[A-Z]+%(%d+%)"), "hot hint should include hazard risk tier + score")
expect(hotHint:find("RISK SRC:D%d+%+DET%d+%+MOVE%d+"), "hot hint should include compact risk-factor breakdown token")

local pressure = OverclockHazard.getPressureProfile()
expect(pressure.active == true, "pressure profile should be active during pulse")
expect(pressure.detectBonus == 2, "pressure detect bonus should match hazard config")
expect(math.abs((pressure.moveMul or 1) - 0.6) < 0.001, "pressure move multiplier should match hazard config")

local coolEvent = OverclockHazard.update(6.0, 11, 11)
expect(coolEvent.expired == true, "pulse should expire after timer elapses")

local cooldownHint = OverclockHazard.getHudHint()
expect(type(cooldownHint) == "string" and cooldownHint:find("OVERCLOCK CD") and cooldownHint:find("%d+s"), "cooldown hint should include cooldown seconds")
expect(cooldownHint:find("NEXT BOUNTY:0/%d+"), "cooldown hint should include next-pulse bounty budget token")
expect(cooldownHint:find("RISK:[A-Z]+%(%d+%)"), "cooldown hint should keep risk tier + score visible")
expect(cooldownHint:find("RISK SRC:D%d+%+DET%d+%+MOVE%d+"), "cooldown hint should keep risk-factor breakdown token visible")
expect(not cooldownHint:find("IMMINENT:"), "cooldown hint should not show imminent warning too early")

OverclockHazard.update(3.2, 11, 11)
local imminentHint = OverclockHazard.getHudHint()
expect(type(imminentHint) == "string" and imminentHint:find("IMMINENT:%d+s"), "cooldown hint should show imminent pulse warning when inside zone near ready")
expect(imminentHint:find("NEXT BOUNTY:0/%d+"), "imminent cooldown hint should keep next-pulse bounty budget token")

OverclockHazard.update(0.0, 2, 2)
local outsideHint = OverclockHazard.getHudHint()
expect(type(outsideHint) == "string" and not outsideHint:find("IMMINENT:"), "imminent warning should hide when player leaves hazard zone")
expect(OverclockHazard.consumeKillBonus(2) == 0, "kill bonus should not trigger while outside hazard zone")

local postCost = OverclockHazard.applyBuildCost(5)
expect(postCost == 5, "after expiry: build cost should return to base")

OverclockHazard.onMapLoaded("07", {
    overclockHazard = {
        rect = { x = 10, y = 10, w = 4, h = 4 },
        discountPct = 0.2,
        aggroMoveMul = 0.9,
        aggroDetectBonus = 1,
    }
})
local lowRiskColor = OverclockHazard.getHudHintColor()
expect(math.abs(lowRiskColor[1] - 0.56) < 0.001 and math.abs(lowRiskColor[2] - 1) < 0.001 and math.abs(lowRiskColor[3] - 0.66) < 0.001, "low-risk tier should map to green HUD color")

OverclockHazard.onMapLoaded("07", {
    overclockHazard = {
        rect = { x = 10, y = 10, w = 4, h = 4 },
        discountPct = 0.35,
        aggroMoveMul = 0.8,
        aggroDetectBonus = 1,
    }
})
local medRiskColor = OverclockHazard.getHudHintColor()
expect(math.abs(medRiskColor[1] - 1) < 0.001 and math.abs(medRiskColor[2] - 0.7) < 0.001 and math.abs(medRiskColor[3] - 0.3) < 0.001, "medium-risk tier should map to amber HUD color")

print("[PASS] overclock hazard regression validated")
