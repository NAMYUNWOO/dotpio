-- Regression: mission pressure-breaker bonus grants dodge charge only on rising threat.
-- Run: lua scripts/regression_mission_pressure_breaker.lua

local RunMissions = require("src.run_missions")
local Player = require("src.player")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

RunMissions.reset({
    { id = "alpha", event = "alpha", label = "Alpha", target = 1, lane = "combat" },
})

local noThreat = RunMissions.addProgress("alpha", 1, { risingThreat = false })
expect(noThreat ~= nil, "objective completion should return reward payload")
expect((noThreat.pressureBreakerDodgeCharge or 0) == 0, "no rising threat should not grant pressure-breaker dodge")

RunMissions.reset({
    { id = "beta", event = "beta", label = "Beta", target = 1, lane = "combat" },
})

local risingThreat = RunMissions.addProgress("beta", 1, { risingThreat = true })
expect((risingThreat.pressureBreakerDodgeCharge or 0) == 1, "rising threat should grant exactly one dodge charge")
expect(risingThreat.risingThreat == true, "completion payload should expose rising-threat context")

Player.dodgeCharges = {}
local afterGrant = Player.grantDodgeCharge(risingThreat.pressureBreakerDodgeCharge, 6)
expect(afterGrant == 1, "player should hold one dodge charge after pressure-breaker grant")
expect(Player.consumeDodgeCharge() == true, "player should consume granted dodge charge")
expect(Player.consumeDodgeCharge() == false, "no second dodge charge should exist")

print("[PASS] mission pressure-breaker regression validated")
