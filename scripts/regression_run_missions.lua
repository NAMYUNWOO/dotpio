-- Regression: run mission prototype objective flow
-- Run: lua scripts/regression_run_missions.lua

local RunMissions = require("src.run_missions")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

RunMissions.reset()
local s = RunMissions.getState()
expect(s.active, "missions should be active after reset")
expect(s.total == 3, "default objective count should be 3")
expect(s.doneCount == 0, "missions should start incomplete")

RunMissions.addProgress("kills", 2)
RunMissions.addProgress("pickup", 1)
RunMissions.addProgress("build", 1)

s = RunMissions.getState()
expect(s.doneCount == 1, "build objective should be complete after one build")

RunMissions.addProgress("kills", 1)
RunMissions.addProgress("pickup", 3)

s = RunMissions.getState()
expect(s.doneCount == 3, "all objectives should complete after reaching targets")
expect(s.completed == true, "mission state should mark run complete")

local killsObj = s.objectives[1]
local pickupObj = s.objectives[2]
expect(killsObj.progress == killsObj.target, "kills progress should clamp to target")
expect(pickupObj.progress == pickupObj.target, "pickup progress should clamp to target")

print("[PASS] run mission prototype regression validated")
