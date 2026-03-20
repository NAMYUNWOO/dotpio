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

local function resolveOverclockProfile(low, mid, high)
    low = math.max(0, math.floor(tonumber(low) or 0))
    mid = math.max(0, math.floor(tonumber(mid) or 0))
    high = math.max(0, math.floor(tonumber(high) or 0))
    local total = low + mid + high
    if total <= 0 then
        return "CAUTIOUS"
    end

    local highPct = (high / total) * 100
    local lowPct = (low / total) * 100
    if high >= mid and high >= low and highPct >= 45 then
        return "ALL-IN"
    end
    if lowPct >= 55 then
        return "CAUTIOUS"
    end
    return "BALANCED"
end

local function resolveOverclockCoachTip(profile, totalExposureSec, rewardSrl)
    local exposure = math.max(0, math.floor(tonumber(totalExposureSec) or 0))
    local reward = math.max(0, math.floor(tonumber(rewardSrl) or 0))
    local efficiency = exposure > 0 and (reward / exposure) or 0

    if exposure <= 0 then
        return "SEED HOT-ZONE REPS"
    end

    if profile == "ALL-IN" then
        if efficiency < 0.40 then
            return "DISENGAGE AFTER CAP"
        end
        return "PRESS HOT STREAKS"
    end

    if profile == "CAUTIOUS" then
        if efficiency >= 0.45 then
            return "EXTEND HOT WINDOWS"
        end
        return "TEST MID-RISK RE-ENTRY"
    end

    if efficiency >= 0.50 then
        return "LOCK BALANCED ROUTE"
    end
    if efficiency < 0.30 then
        return "CHASE CLEANER PICKS"
    end
    return "HOLD MID-ZONE TEMPO"
end

function RunSummary.open(missionState, unlockFlags, appliedCarry, overclockDwellBuckets, overclockRewardSrl)
    local missionsDone = (missionState and missionState.doneCount) or 0
    local missionsTotal = (missionState and missionState.total) or 0
    local objectives = cloneObjectives((missionState and missionState.objectives) or {})
    local advancedUnlocked = unlockFlags and unlockFlags.advanced_build_categories == true

    local dwellLow = math.max(0, math.floor((overclockDwellBuckets and overclockDwellBuckets.LOW) or 0))
    local dwellMid = math.max(0, math.floor((overclockDwellBuckets and overclockDwellBuckets.MID) or 0))
    local dwellHigh = math.max(0, math.floor((overclockDwellBuckets and overclockDwellBuckets.HIGH) or 0))
    local rewardSrl = math.max(0, math.floor(tonumber(overclockRewardSrl) or 0))
    local profile = resolveOverclockProfile(dwellLow, dwellMid, dwellHigh)
    local exposureTotal = dwellLow + dwellMid + dwellHigh

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
            low = dwellLow,
            mid = dwellMid,
            high = dwellHigh,
        },
        overclockRewardSrl = rewardSrl,
        overclockProfile = profile,
        overclockCoachTip = resolveOverclockCoachTip(profile, exposureTotal, rewardSrl),
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
