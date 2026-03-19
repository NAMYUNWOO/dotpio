local RunMissions = {}

local OBJECTIVE_VARIANTS = {
    kills_3 = { id = "kills_3", event = "kills", label = "Neutralize enemies", target = 3, lane = "combat" },
    kills_5 = { id = "kills_5", event = "kills", label = "Purge elite wave", target = 5, lane = "combat" },
    pickup_2 = { id = "pickup_2", event = "pickup", label = "Recover dropped loot", target = 2, lane = "scavenge" },
    pickup_4 = { id = "pickup_4", event = "pickup", label = "Sweep salvage caches", target = 4, lane = "scavenge" },
    build_1 = { id = "build_1", event = "build", label = "Complete AI build", target = 1, lane = "craft" },
    build_2 = { id = "build_2", event = "build", label = "Chain two AI builds", target = 2, lane = "craft" },
    search_2 = { id = "search_2", event = "search", label = "Search nearby crates", target = 2, lane = "scavenge" },
    inventory_3 = { id = "inventory_3", event = "inventory", label = "Plan loadout checks", target = 3, lane = "craft" },
}

local DEFAULT_OBJECTIVE_PACKS = {
    {
        id = "pack_1",
        flavorTag = "BASELINE",
        flavorLabel = "steady pressure",
        objectives = { "kills_3", "pickup_2", "build_1" },
    },
    {
        id = "pack_2",
        flavorTag = "HUNT",
        flavorLabel = "aggressive clear",
        objectives = { "kills_5", "pickup_4", "build_1" },
    },
    {
        id = "pack_3",
        flavorTag = "FORGE",
        flavorLabel = "craft surge",
        objectives = { "kills_3", "search_2", "build_2" },
    },
    {
        id = "pack_4",
        flavorTag = "PIVOT",
        flavorLabel = "lane switching",
        objectives = { "kills_5", "pickup_2", "inventory_3" },
    },
}

local state = {
    active = false,
    objectives = {},
    doneCount = 0,
    total = 0,
    cycleIndex = 0,
    lastPackId = nil,
    lastPackTag = nil,
    lastPackLabel = nil,
    completionStreak = 0,
    lastCompletedLane = nil,
}

local MOMENTUM_REWARD_BY_STREAK = {
    1, -- 1st objective in streak
    1, -- 2nd objective in streak
    2, -- 3rd+ objective in streak (cap)
}

local function clampProgress(value, target)
    return math.max(0, math.min(target or 0, tonumber(value) or 0))
end

local function recalcDoneCount()
    local done = 0
    for _, objective in ipairs(state.objectives) do
        objective.done = objective.progress >= objective.target
        if objective.done then
            done = done + 1
        end
    end
    state.doneCount = done
end

local function cloneObjectiveTemplate(template)
    return {
        id = template.id,
        event = template.event or template.id,
        lane = template.lane,
        label = template.label,
        target = math.max(1, tonumber(template.target) or 1),
        progress = 0,
        done = false,
    }
end

local function cloneObjectives(source)
    local list = {}
    for _, objective in ipairs(source or {}) do
        local template = OBJECTIVE_VARIANTS[objective] or objective
        if template and template.id and template.label then
            list[#list + 1] = cloneObjectiveTemplate(template)
        end
    end
    return list
end

local function resolvePack(packOrObjectives)
    if packOrObjectives ~= nil then
        return {
            id = "custom",
            flavorTag = "CUSTOM",
            flavorLabel = "custom mission set",
            objectives = packOrObjectives,
        }
    end

    local packs = DEFAULT_OBJECTIVE_PACKS
    if #packs == 0 then
        return {
            id = "fallback",
            flavorTag = "FALLBACK",
            flavorLabel = "core loop",
            objectives = { OBJECTIVE_VARIANTS.kills_3, OBJECTIVE_VARIANTS.pickup_2, OBJECTIVE_VARIANTS.build_1 },
        }
    end

    state.cycleIndex = state.cycleIndex + 1
    local idx = ((state.cycleIndex - 1) % #packs) + 1
    return packs[idx]
end

function RunMissions.reset(objectives)
    local pack = resolvePack(objectives)
    state.objectives = cloneObjectives(pack.objectives)
    state.total = #state.objectives
    state.active = state.total > 0
    state.doneCount = 0
    state.lastPackId = pack.id or "unknown"
    state.lastPackTag = pack.flavorTag or "UNKNOWN"
    state.lastPackLabel = pack.flavorLabel or "unknown pacing"
    state.completionStreak = 0
    state.lastCompletedLane = nil
    recalcDoneCount()
end

function RunMissions.addProgress(eventId, amount)
    if not state.active then return nil end
    local delta = tonumber(amount) or 0
    if delta <= 0 then return nil end

    local completedAny = false
    local completedNow = {}
    local completedLanes = {}
    local matched = false
    for _, objective in ipairs(state.objectives) do
        if objective.event == eventId or objective.id == eventId then
            matched = true
            local beforeDone = objective.done
            objective.progress = clampProgress(objective.progress + delta, objective.target)
            objective.done = objective.progress >= objective.target
            if objective.done and not beforeDone then
                completedAny = true
                completedNow[#completedNow + 1] = objective.id
                completedLanes[#completedLanes + 1] = objective.lane
            end
        end
    end

    if matched then
        recalcDoneCount()
    end

    if not completedAny then
        return nil
    end

    state.completionStreak = state.completionStreak + #completedNow
    local rewardTier = math.min(state.completionStreak, #MOMENTUM_REWARD_BY_STREAK)
    local rewardSrl = MOMENTUM_REWARD_BY_STREAK[rewardTier] or 0

    local laneSwitchBonusSrl = 0
    local completionLane = completedLanes[1]
    if completionLane and state.lastCompletedLane and completionLane ~= state.lastCompletedLane then
        laneSwitchBonusSrl = 1
    end
    if completionLane then
        state.lastCompletedLane = completionLane
    end

    return {
        completedObjectiveIds = completedNow,
        completionStreak = state.completionStreak,
        rewardSrl = rewardSrl + laneSwitchBonusSrl,
        baseRewardSrl = rewardSrl,
        laneSwitchBonusSrl = laneSwitchBonusSrl,
        completionLane = completionLane,
    }
end

local function getNextVarietyLaneHint()
    if not state.lastCompletedLane then
        return nil
    end

    for _, objective in ipairs(state.objectives) do
        if not objective.done and objective.lane and objective.lane ~= state.lastCompletedLane then
            return objective.lane
        end
    end

    return nil
end

function RunMissions.getState()
    local nextVarietyLane = getNextVarietyLaneHint()
    return {
        active = state.active,
        doneCount = state.doneCount,
        total = state.total,
        completed = (state.total > 0 and state.doneCount == state.total) or false,
        completionStreak = state.completionStreak,
        lastPackId = state.lastPackId,
        lastPackTag = state.lastPackTag,
        lastPackLabel = state.lastPackLabel,
        nextVarietyLane = nextVarietyLane,
        varietyBonusPreview = nextVarietyLane and 1 or 0,
        objectives = state.objectives,
    }
end

function RunMissions.debugSetProgress(objectiveId, value)
    for _, objective in ipairs(state.objectives) do
        if objective.id == objectiveId then
            objective.progress = clampProgress(value, objective.target)
            recalcDoneCount()
            return true
        end
    end
    return false
end

function RunMissions.debugGetVariantCatalog()
    local catalog = {}
    for id, objective in pairs(OBJECTIVE_VARIANTS) do
        catalog[id] = {
            id = objective.id,
            event = objective.event,
            lane = objective.lane,
            label = objective.label,
            target = objective.target,
        }
    end
    return catalog
end

return RunMissions
