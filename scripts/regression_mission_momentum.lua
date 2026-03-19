-- Regression: mission momentum reward payout by objective completion streak
-- Run: lua scripts/regression_mission_momentum.lua

local RunMissions = require("src.run_missions")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

RunMissions.reset({
    { id = "alpha", event = "alpha", label = "alpha", lane = "combat", target = 1 },
    { id = "beta", event = "beta", label = "beta", lane = "combat", target = 1 },
    { id = "gamma", event = "gamma", label = "gamma", lane = "craft", target = 1 },
})

local r1 = RunMissions.addProgress("alpha", 1)
expect(r1 and r1.rewardSrl == 1, "streak 1 should reward +1 SRL")
expect((r1.laneSwitchBonusSrl or 0) == 0, "first completion should not grant lane-switch bonus")
expect(r1.completionStreak == 1, "streak 1 completionStreak mismatch")

local r2 = RunMissions.addProgress("beta", 1)
expect(r2 and r2.rewardSrl == 1, "same-lane streak 2 should reward +1 SRL")
expect((r2.laneSwitchBonusSrl or 0) == 0, "same-lane completion should not grant lane-switch bonus")
expect(r2.completionStreak == 2, "streak 2 completionStreak mismatch")

local r3 = RunMissions.addProgress("gamma", 1)
expect(r3 and (r3.baseRewardSrl or 0) == 2, "streak 3 base reward should be +2 SRL")
expect((r3.laneSwitchBonusSrl or 0) == 1, "lane switch should grant +1 SRL variety bonus")
expect(r3.rewardSrl == 3, "streak 3 with lane switch should reward +3 SRL total")
expect(r3.completionStreak == 3, "streak 3 completionStreak mismatch")

local s3 = RunMissions.getState()
expect((s3.varietyBonusCount or 0) == 1, "lane-switch completion should increment variety bonus counter")

local none = RunMissions.addProgress("alpha", 1)
expect(none == nil, "already completed objective should not pay extra momentum reward")

RunMissions.reset({
    { id = "solo", event = "solo", label = "solo", target = 1 },
})
local s = RunMissions.getState()
expect(s.completionStreak == 0, "reset should clear completion streak")
expect((s.varietyBonusCount or 0) == 0, "reset should clear variety bonus counter")

print("[PASS] mission momentum payout regression validated")
