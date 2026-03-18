local RunMissions = {}

local DEFAULT_OBJECTIVES = {
    { id = "kills", label = "Neutralize enemies", target = 3 },
    { id = "pickup", label = "Recover dropped loot", target = 2 },
    { id = "build", label = "Complete AI build", target = 1 },
}

local state = {
    active = false,
    objectives = {},
    doneCount = 0,
    total = 0,
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

local function cloneObjectives(source)
    local list = {}
    for _, objective in ipairs(source or DEFAULT_OBJECTIVES) do
        list[#list + 1] = {
            id = objective.id,
            label = objective.label,
            target = math.max(1, tonumber(objective.target) or 1),
            progress = 0,
            done = false,
        }
    end
    return list
end

function RunMissions.reset(objectives)
    state.objectives = cloneObjectives(objectives)
    state.total = #state.objectives
    state.active = state.total > 0
    state.doneCount = 0
    recalcDoneCount()
end

function RunMissions.addProgress(objectiveId, amount)
    if not state.active then return false end
    local delta = tonumber(amount) or 0
    if delta <= 0 then return false end

    for _, objective in ipairs(state.objectives) do
        if objective.id == objectiveId then
            local beforeDone = objective.done
            objective.progress = clampProgress(objective.progress + delta, objective.target)
            recalcDoneCount()
            return objective.done and not beforeDone
        end
    end

    return false
end

function RunMissions.getState()
    return {
        active = state.active,
        doneCount = state.doneCount,
        total = state.total,
        completed = (state.total > 0 and state.doneCount == state.total) or false,
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

return RunMissions
