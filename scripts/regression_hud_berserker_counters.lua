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

local empty = HUD.collectCombatThreatCounters(nil)
expect(empty.alive == 0 and empty.desperateBerserkers == 0 and empty.primedBerserkerLunges == 0 and empty.recoveringBerserkers == 0 and empty.berserkerThreatScore == 0,
    "nil enemy list should return zeroed counters")

print("[PASS] hud berserker threat counters regression validated")
