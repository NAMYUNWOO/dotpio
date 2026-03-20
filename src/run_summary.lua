local RunSummary = {}

local state = {
    active = false,
    data = nil,
}

local function cloneObjectives(objectives)
    local out = {}
    for _, objective in ipairs(objectives or {}) do
        out[#out + 1] = {
            id = objective.id,
            label = objective.label,
            progress = objective.progress or 0,
            target = objective.target or 0,
            done = objective.done == true,
        }
    end
    return out
end

function RunSummary.open(missionState, unlockFlags, appliedCarry, overclockDwellBuckets)
    local missionsDone = (missionState and missionState.doneCount) or 0
    local missionsTotal = (missionState and missionState.total) or 0
    local objectives = cloneObjectives((missionState and missionState.objectives) or {})
    local advancedUnlocked = unlockFlags and unlockFlags.advanced_build_categories == true

    state.data = {
        missionsDone = missionsDone,
        missionsTotal = missionsTotal,
        completed = missionsTotal > 0 and missionsDone == missionsTotal,
        missionPackId = (missionState and missionState.lastPackId) or "unknown",
        missionPackTag = (missionState and missionState.lastPackTag) or "UNKNOWN",
        missionPackLabel = (missionState and missionState.lastPackLabel) or "unknown pacing",
        momentumStreak = (missionState and missionState.completionStreak) or 0,
        varietyBonusCount = (missionState and missionState.varietyBonusCount) or 0,
        objectives = objectives,
        advancedUnlocked = advancedUnlocked,
        carry = {
            srl = (appliedCarry and appliedCarry.srl) or 0,
            coins = (appliedCarry and appliedCarry.coins) or 0,
            gems = (appliedCarry and appliedCarry.gems) or 0,
        },
        overclockDwell = {
            low = math.max(0, math.floor((overclockDwellBuckets and overclockDwellBuckets.LOW) or 0)),
            mid = math.max(0, math.floor((overclockDwellBuckets and overclockDwellBuckets.MID) or 0)),
            high = math.max(0, math.floor((overclockDwellBuckets and overclockDwellBuckets.HIGH) or 0)),
        },
    }
    state.active = true
end

function RunSummary.close()
    state.active = false
end

function RunSummary.isOpen()
    return state.active
end

function RunSummary.getState()
    return {
        active = state.active,
        data = state.data,
    }
end

return RunSummary
