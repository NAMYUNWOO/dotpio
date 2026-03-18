-- Regression: unlock flag framework for advanced build options
-- Run: lua scripts/regression_unlock_flags.lua

local Unlocks = require("src.unlocks")
local RunMissions = require("src.run_missions")
local AiDescribe = require("src.ai_describe")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

local function hasValue(list, wanted)
    for _, v in ipairs(list or {}) do
        if v == wanted then return true end
    end
    return false
end

Unlocks.resetAll()
AiDescribe.debugResetBuildCategoryHistory()

local baseTargets = AiDescribe.debugGetBuildTargetCategories()
expect(not hasValue(baseTargets, "ring"), "ring should be locked before unlock")
expect(not hasValue(baseTargets, "wand"), "wand should be locked before unlock")
expect(not hasValue(baseTargets, "gem"), "gem should be locked before unlock")

RunMissions.reset()
RunMissions.addProgress("kills", 3)
RunMissions.addProgress("pickup", 2)
RunMissions.addProgress("build", 1)

local mission = RunMissions.getState()
expect(mission.completed == true, "mission should be complete after hitting all objectives")

local didUnlock = Unlocks.unlock("advanced_build_categories")
expect(didUnlock == true, "unlock should flip on first completion")
expect(Unlocks.isUnlocked("advanced_build_categories"), "advanced build categories flag should be true")
expect(Unlocks.unlock("advanced_build_categories") == false, "unlock should be idempotent")

local advancedTargets = AiDescribe.debugGetBuildTargetCategories()
expect(hasValue(advancedTargets, "ring"), "ring should unlock after mission completion")
expect(hasValue(advancedTargets, "wand"), "wand should unlock after mission completion")
expect(hasValue(advancedTargets, "gem"), "gem should unlock after mission completion")

print("[PASS] unlock flag framework regression validated")
