-- Regression: run summary snapshot/open-close behavior
-- Run: lua scripts/regression_run_summary.lua

package.path = "./?.lua;./?/init.lua;" .. package.path

local RunMissions = require("src.run_missions")
local RunSummary = require("src.run_summary")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

RunMissions.reset()
RunMissions.addProgress("kills", 3)
RunMissions.addProgress("pickup", 1)

local missionState = RunMissions.getState()
local unlockFlags = { advanced_build_categories = false }
local applied = { srl = 4, coins = 3, gems = 1 }

RunSummary.open(missionState, unlockFlags, applied)
local state = RunSummary.getState()

expect(state.active == true, "run summary should open")
expect(state.data ~= nil, "run summary should contain snapshot data")
expect(state.data.missionsDone == 1, "missionsDone should match snapshot")
expect(state.data.missionsTotal == 3, "missionsTotal should match objective count")
expect(state.data.missionPackId == "pack_1", "mission pack id should be captured in summary snapshot")
expect(state.data.momentumStreak == 1, "momentum streak should be captured in summary snapshot")
expect(state.data.advancedUnlocked == false, "unlock state should be copied into snapshot")
expect(#(state.data.objectives or {}) == 3, "summary should include objective rows")
expect(state.data.carry.srl == 4 and state.data.carry.coins == 3 and state.data.carry.gems == 1, "carryover values should match applied reward")

-- Ensure snapshot data is stable even if mission state changes afterwards.
RunMissions.addProgress("pickup", 1)
local changedMissionState = RunMissions.getState()
expect(changedMissionState.doneCount == 2, "control check: mission state should now advance")
expect(state.data.missionsDone == 1, "summary snapshot should remain immutable after open")

RunSummary.close()
expect(RunSummary.isOpen() == false, "run summary should close")

print("[PASS] run summary regression validated")
