-- Regression: mission variety-bonus preview hint in mission state
-- Run: lua scripts/regression_mission_variety_preview.lua

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

local s0 = RunMissions.getState()
expect(s0.nextVarietyLane == nil, "before first completion there should be no variety preview lane")
expect((s0.varietyBonusPreview or 0) == 0, "before first completion preview bonus should be 0")

local r1 = RunMissions.addProgress("alpha", 1)
expect(r1 and r1.rewardSrl == 1, "first completion should still reward normally")

local s1 = RunMissions.getState()
expect(s1.nextVarietyLane == "craft", "preview should point to remaining alternate lane objective")
expect((s1.varietyBonusPreview or 0) == 1, "alternate lane should preview +1 variety bonus")

RunMissions.addProgress("gamma", 1)
local s2 = RunMissions.getState()
expect(s2.nextVarietyLane == "combat", "after switching lanes preview should flip to remaining opposite lane objective")
expect((s2.varietyBonusPreview or 0) == 1, "opposite lane availability should keep +1 preview")

RunMissions.addProgress("beta", 1)
local s3 = RunMissions.getState()
expect(s3.nextVarietyLane == nil, "all objectives complete should clear preview")
expect((s3.varietyBonusPreview or 0) == 0, "completed mission set should clear preview bonus")

print("[PASS] mission variety preview regression validated")
