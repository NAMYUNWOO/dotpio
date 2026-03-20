-- HUD berserker threat-strip counter regression
-- Run: lua scripts/regression_hud_berserker_counters.lua

local HUD = require("src.hud")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

local enemies = {
    { alive = true, behavior = "raider" },
    { alive = true, behavior = "berserker", desperationActive = true, desperationLungePrimed = true, desperationRecoveryPending = true },
    { alive = true, behavior = "berserker", desperationActive = true, desperationLungePrimed = false, desperationRecoveryPending = true },
    { alive = true, behavior = "berserker", desperationActive = false, desperationLungePrimed = true, desperationRecoveryPending = true },
    { alive = false, behavior = "berserker", desperationActive = true, desperationLungePrimed = true, desperationRecoveryPending = true },
}

local counters = HUD.collectCombatThreatCounters(enemies)
expect(counters.alive == 4, "alive counter should include only alive enemies")
expect(counters.desperateBerserkers == 2, "desperate berserker counter should include only active desperation enemies")
expect(counters.primedBerserkerLunges == 1, "lunge tell counter should include only primed desperate berserkers")
expect(counters.recoveringBerserkers == 2, "recovering counter should include only desperate berserkers with pending recovery")
expect(counters.berserkerThreatScore == 6, "threat score should weight desperate(1) + lunge(2) + recovery(1) contributions")
expect(HUD.getBerserkerThreatTier(counters.berserkerThreatScore) == "HIGH", "threat tier should be HIGH at score >= 6")
expect(HUD.getBerserkerThreatTier(3) == "MED", "threat tier should be MED at score >= 3")
expect(HUD.getBerserkerThreatTier(2) == "LOW", "threat tier should be LOW below medium threshold")
expect(HUD.getBerserkerThreatTier(nil) == "LOW", "threat tier should default to LOW for missing score")
expect(HUD.getBerserkerThreatLegend() == "THREAT = BERSERK + 2*LUNGE + RECOVER", "threat legend copy should stay stable")
expect(HUD.getBerserkerThreatDelta(6, 2) == 4, "threat delta should increase when current score is higher")
expect(HUD.getBerserkerThreatDelta(2, 6) == -4, "threat delta should decrease when current score is lower")
expect(HUD.getBerserkerThreatDelta(nil, nil) == 0, "threat delta should default to zero for missing scores")
expect(HUD.formatBerserkerThreatDelta(6, 2) == "THREAT Δ:+4", "threat delta copy should include explicit plus sign for increases")
expect(HUD.formatBerserkerThreatDelta(2, 6) == "THREAT Δ:-4", "threat delta copy should include minus sign for decreases")
expect(HUD.formatBerserkerThreatDelta(3, 3) == "THREAT Δ:0", "threat delta copy should show zero for no change")
expect(HUD.formatBerserkerThreatBreakdown(counters) == "THREAT = 2 + 2*1 + 2 = 6", "threat breakdown should expose weighted formula")
expect(HUD.formatBerserkerThreatBreakdown(nil) == "THREAT = 0 + 2*0 + 0 = 0", "threat breakdown should be safe on nil")

local lowR, lowG, lowB, lowA = HUD.getBerserkerThreatColor(2)
expect(lowR == 0.5 and lowG == 1 and lowB == 0.62 and lowA == 1, "LOW tier color should be green")
local medR, medG, medB, medA = HUD.getBerserkerThreatColor(3)
expect(medR == 1 and medG == 0.66 and medB == 0.25 and medA == 1, "MED tier color should be amber")
local highR, highG, highB, highA = HUD.getBerserkerThreatColor(6)
expect(highR == 1 and highG == 0.3 and highB == 0.2 and highA == 1, "HIGH tier color should be red")

local empty = HUD.collectCombatThreatCounters(nil)
expect(empty.alive == 0 and empty.desperateBerserkers == 0 and empty.primedBerserkerLunges == 0 and empty.recoveringBerserkers == 0 and empty.berserkerThreatScore == 0,
    "nil enemy list should return zeroed counters")

print("[PASS] hud berserker threat counters regression validated")
