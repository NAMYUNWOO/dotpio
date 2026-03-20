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
        routeTag = "SPIKE",
        discountPct = 0.4,
        pulseDuration = 5,
        cooldownDuration = 12,
        aggroMoveMul = 0.6,
        aggroDetectBonus = 2,
    }
})

local readyHint = OverclockHazard.getHudHint()
expect(type(readyHint) == "string" and readyHint:find("OVERCLOCK READY"), "ready hint should be visible before entering hazard zone")
expect(OverclockHazard.getRouteTag() == "SPIKE", "route tag should be exposed from map metadata")
expect(OverclockHazard.getRouteCallout() == "ROUTE:SPIKE", "route callout should format compact HUD token")
local routeColor = OverclockHazard.getRouteCalloutColor()
expect(type(routeColor) == "table" and #routeColor >= 3, "route callout color should be exposed")
expect(math.abs(routeColor[1] - 1) < 0.001 and math.abs(routeColor[2] - 0.34) < 0.001 and math.abs(routeColor[3] - 0.25) < 0.001, "SPIKE route tag should map to red callout color")
expect(readyHint:find("NEXT BOUNTY:0/%d+"), "ready hint should include next-pulse bounty budget token")
expect(readyHint:find("NEXT PULSE:%d+s"), "ready hint should include next-pulse ETA token")
expect(readyHint:find("RECHARGE:100%%"), "ready hint should show fully charged recharge progress")
expect(readyHint:find("ZONE:OUT"), "ready hint should show outside-zone presence token before entering hazard")
expect(readyHint:find("RISK:[A-Z]+%(%d+%)"), "ready hint should include risk tier + score")
expect(readyHint:find("RISK Δ:0"), "ready hint should include neutral risk-delta token before pulse")
expect(readyHint:find("RISK SRC:D%d+%+DET%d+%+MOVE%d+"), "ready hint should include compact risk-factor breakdown token")

local highRiskColor = OverclockHazard.getHudHintColor()
expect(type(highRiskColor) == "table" and #highRiskColor >= 3, "risk tier color should be exposed for HUD rendering")
expect(math.abs(highRiskColor[1] - 1) < 0.001 and math.abs(highRiskColor[2] - 0.34) < 0.001 and math.abs(highRiskColor[3] - 0.25) < 0.001, "baseline high-risk tier should map to red HUD color")

local idleCost = OverclockHazard.applyBuildCost(5)
expect(idleCost == 5, "no pulse: build cost should remain unchanged")

local events = OverclockHazard.update(0.1, 11, 11)
expect(events.activated == true, "entering hazard zone should activate pulse")

local discounted = OverclockHazard.applyBuildCost(5)
expect(discounted == 3, "pulse should discount build cost (5 -> 3)")

local hotHintBeforeKills = OverclockHazard.getHudHint()
expect(type(hotHintBeforeKills) == "string" and hotHintBeforeKills:find("BOUNTY:0/3"), "hot hint should show zeroed bounty progress at pulse start")
expect(hotHintBeforeKills:find("PULSE:100%%"), "hot hint should show full pulse progress at activation")

local killBonusFirst = OverclockHazard.consumeKillBonus(2)
expect(killBonusFirst == 2, "hot-zone kills should award overclock bonus SRL per kill")

local killBonusCapped = OverclockHazard.consumeKillBonus(3)
expect(killBonusCapped == 1, "per-pulse overclock kill bonus should respect configured cap")
expect(OverclockHazard.getRunRewardSrl() == 3, "run reward SRL should accumulate granted overclock bounty")

local hotHint = OverclockHazard.getHudHint()
local hotRiskColor = OverclockHazard.getHudHintColor()
expect(math.abs(hotRiskColor[1] - 1) < 0.001 and math.abs(hotRiskColor[2] - 0.34) < 0.001 and math.abs(hotRiskColor[3] - 0.25) < 0.001, "positive risk delta should map to red HUD color")
expect(type(hotHint) == "string" and hotHint:find("OVERCLOCK HOT") and hotHint:find("%d+s"), "hot hint should include active pulse countdown seconds")
expect(hotHint:find("ZONE:IN"), "hot hint should show inside-zone presence token")
expect(hotHint:find("EXPOSED:%d+s"), "hot hint should include in-zone exposure-duration token")
expect(hotHint:find("COMMIT:LOW"), "hot hint should include LOW commitment tier at short exposure")
expect(hotHint:find("AGGRO DET:%+%d+"), "hot hint should include aggro detect bonus legend")
expect(hotHint:find("MOVE:%+%d+%%"), "hot hint should include aggro move-speed pressure legend")
expect(hotHint:find("BOUNTY:%d+/%d+"), "hot hint should include bounty progress token")
expect(hotHint:find("BOUNTY:3/3"), "bounty progress token should reflect per-pulse cap consumption")
expect(hotHint:find("PULSE:%d+%%"), "hot hint should include pulse progress token")
expect(hotHint:find("RISK:[A-Z]+%(%d+%)"), "hot hint should include hazard risk tier + score")
expect(hotHint:find("RISK Δ:%+%d+"), "hot hint should include positive risk-delta token during active pulse")
expect(hotHint:find("RISK SRC:D%d+%+DET%d+%+MOVE%d+"), "hot hint should include compact risk-factor breakdown token")

local pressure = OverclockHazard.getPressureProfile()
expect(pressure.active == true, "pressure profile should be active during pulse")
expect(pressure.detectBonus == 2, "pressure detect bonus should match hazard config")
expect(math.abs((pressure.moveMul or 1) - 0.6) < 0.001, "pressure move multiplier should match hazard config")

local coolEvent = OverclockHazard.update(6.0, 11, 11)
expect(coolEvent.expired == true, "pulse should expire after timer elapses")

local cooldownHint = OverclockHazard.getHudHint()
expect(type(cooldownHint) == "string" and cooldownHint:find("OVERCLOCK CD") and cooldownHint:find("%d+s"), "cooldown hint should include cooldown seconds")
expect(cooldownHint:find("ZONE:IN"), "cooldown hint should show inside-zone presence token while player remains in hazard")
expect(cooldownHint:find("EXPOSED:%d+s"), "cooldown hint should keep exposure-duration token while player remains in hazard")
expect(cooldownHint:find("COMMIT:MID"), "cooldown hint should promote commitment tier to MID after sustained exposure")
expect(cooldownHint:find("NEXT BOUNTY:0/%d+"), "cooldown hint should include next-pulse bounty budget token")
expect(cooldownHint:find("NEXT PULSE:%d+s"), "cooldown hint should include next-pulse ETA token")
expect(cooldownHint:find("RECHARGE:%d+%%"), "cooldown hint should include recharge progress token")
expect(cooldownHint:find("RISK:[A-Z]+%(%d+%)"), "cooldown hint should keep risk tier + score visible")
expect(cooldownHint:find("RISK Δ:0"), "cooldown hint should show neutral risk-delta outside imminent window")
expect(cooldownHint:find("RISK SRC:D%d+%+DET%d+%+MOVE%d+"), "cooldown hint should keep risk-factor breakdown token visible")
expect(not cooldownHint:find("IMMINENT:"), "cooldown hint should not show imminent warning too early")

OverclockHazard.update(3.2, 11, 11)
local imminentHint = OverclockHazard.getHudHint()
expect(type(imminentHint) == "string" and imminentHint:find("IMMINENT:%d+s"), "cooldown hint should show imminent pulse warning when inside zone near ready")
expect(imminentHint:find("ZONE:IN"), "imminent cooldown hint should keep inside-zone presence token")
expect(imminentHint:find("EXPOSED:%d+s"), "imminent cooldown hint should keep exposure-duration token while in zone")
expect(imminentHint:find("COMMIT:MID"), "imminent cooldown hint should keep MID commitment tier below high threshold")
expect(imminentHint:find("NEXT BOUNTY:0/%d+"), "imminent cooldown hint should keep next-pulse bounty budget token")
expect(imminentHint:find("NEXT PULSE:%d+s"), "imminent cooldown hint should keep next-pulse ETA token")
expect(imminentHint:find("RECHARGE:%d+%%"), "imminent cooldown hint should keep recharge progress token")
expect(imminentHint:find("RISK Δ:%+%d+"), "imminent cooldown hint should surface elevated risk-delta token while standing in zone")

OverclockHazard.update(2.5, 11, 11)
local highCommitHint = OverclockHazard.getHudHint()
expect(type(highCommitHint) == "string" and highCommitHint:find("OVERCLOCK CD"), "long-exposure commitment tier check should occur in cooldown hint")
expect(highCommitHint:find("COMMIT:HIGH"), "in-zone hint should escalate commitment tier to HIGH at long exposure")

OverclockHazard.update(0.0, 2, 2)
local outsideHint = OverclockHazard.getHudHint()
local outsideRiskColor = OverclockHazard.getHudHintColor()
expect(type(outsideHint) == "string" and not outsideHint:find("IMMINENT:"), "imminent warning should hide when player leaves hazard zone")
expect(outsideHint:find("ZONE:OUT"), "cooldown hint should switch to outside-zone presence token when player leaves hazard")
expect(not outsideHint:find("EXPOSED:"), "outside-zone cooldown hint should clear exposure-duration token")
expect(not outsideHint:find("COMMIT:"), "outside-zone cooldown hint should clear commitment-tier token")
expect(outsideHint:find("RISK Δ:%-1"), "outside-zone cooldown hint should show de-escalation risk-delta token")
expect(math.abs(outsideRiskColor[1] - 0.56) < 0.001 and math.abs(outsideRiskColor[2] - 1) < 0.001 and math.abs(outsideRiskColor[3] - 0.66) < 0.001, "negative risk delta should map to green HUD color")
expect(OverclockHazard.consumeKillBonus(2) == 0, "kill bonus should not trigger while outside hazard zone")

local postCost = OverclockHazard.applyBuildCost(5)
expect(postCost == 5, "after expiry: build cost should return to base")

OverclockHazard.onMapLoaded("07", {
    overclockHazard = {
        rect = { x = 10, y = 10, w = 4, h = 4 },
        discountPct = 0.4,
        pulseDuration = 4,
        cooldownDuration = 10,
        reliefWindowDuration = 3,
    }
})
OverclockHazard.update(0.1, 11, 11)
OverclockHazard.update(2.0, 2, 2)
OverclockHazard.update(2.1, 2, 2)
local reliefHint = OverclockHazard.getHudHint()
expect(type(reliefHint) == "string" and reliefHint:find("OVERCLOCK CD"), "relief scenario should remain in cooldown state")
expect(reliefHint:find("ZONE:OUT"), "relief scenario should keep outside-zone token")
expect(reliefHint:find("WINDOW:%d+s"), "outside cooldown hint should show temporary relief window token after pulse-end disengage")
OverclockHazard.update(3.5, 2, 2)
local reliefExpiredHint = OverclockHazard.getHudHint()
expect(type(reliefExpiredHint) == "string" and reliefExpiredHint:find("OVERCLOCK CD"), "relief expiry check should still be in cooldown")
expect(not reliefExpiredHint:find("WINDOW:"), "relief window token should expire after configured duration")

OverclockHazard.onMapLoaded("07", {
    overclockHazard = {
        rect = { x = 10, y = 10, w = 4, h = 4 },
        discountPct = 0.3,
        pulseDuration = 2,
        cooldownDuration = 6,
    }
})
local retreatCycleOneEnter = OverclockHazard.update(0.1, 11, 11)
expect(retreatCycleOneEnter.activated == true, "retreat streak cycle #1 should activate pulse")
OverclockHazard.update(0.2, 2, 2)
local retreatCycleOneExpire = OverclockHazard.update(2.1, 2, 2)
expect(retreatCycleOneExpire.expired == true, "retreat streak cycle #1 should expire while outside zone")
expect((retreatCycleOneExpire.retreatStreakBonusDodgeCharges or 0) == 0, "single safe disengage should not grant retreat streak dodge bonus")

local retreatCycleTwoEnter = OverclockHazard.update(6.1, 11, 11)
expect(retreatCycleTwoEnter.activated == true, "retreat streak cycle #2 should reactivate pulse after cooldown")
OverclockHazard.update(0.2, 2, 2)
local retreatCycleTwoExpire = OverclockHazard.update(2.1, 2, 2)
expect(retreatCycleTwoExpire.expired == true, "retreat streak cycle #2 should expire while outside zone")
expect((retreatCycleTwoExpire.retreatStreakBonusDodgeCharges or 0) == 1, "two consecutive safe disengages should grant retreat streak dodge bonus")

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
expect(OverclockHazard.getRouteTag() == nil, "route tag should be nil when metadata omits route tag")
expect(OverclockHazard.getRouteCallout() == nil, "route callout should be hidden when route tag missing")

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

OverclockHazard.resetRunTelemetry()
expect(OverclockHazard.getRunRewardSrl() == 0, "run reward SRL should reset with run telemetry reset")

print("[PASS] overclock hazard regression validated")
