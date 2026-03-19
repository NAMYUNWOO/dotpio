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
    { "kills_3", "pickup_2", "build_1" },
    { "kills_5", "pickup_4", "build_1" },
    { "kills_3", "search_2", "build_2" },
    { "kills_5", "pickup_2", "inventory_3" },
}

local state = {
    active = false,
    objectives = {},
    doneCount = 0,
    total = 0,
    cycleIndex = 0,
    lastPackId = nil,
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
        return packOrObjectives, "custom"
    end

    local packs = DEFAULT_OBJECTIVE_PACKS
    if #packs == 0 then
        return { OBJECTIVE_VARIANTS.kills_3, OBJECTIVE_VARIANTS.pickup_2, OBJECTIVE_VARIANTS.build_1 }, "fallback"
    end

    state.cycleIndex = state.cycleIndex + 1
    local idx = ((state.cycleIndex - 1) % #packs) + 1
    return packs[idx], string.format("pack_%d", idx)
end

function RunMissions.reset(objectives)
    local source, packId = resolvePack(objectives)
    state.objectives = cloneObjectives(source)
    state.total = #state.objectives
    state.active = state.total > 0
    state.doneCount = 0
    state.lastPackId = packId
    recalcDoneCount()
end

function RunMissions.addProgress(eventId, amount)
    if not state.active then return false end
    local delta = tonumber(amount) or 0
    if delta <= 0 then return false end

    local completedNew = false
    local matched = false
    for _, objective in ipairs(state.objectives) do
        if objective.event == eventId or objective.id == eventId then
            matched = true
            local beforeDone = objective.done
            objective.progress = clampProgress(objective.progress + delta, objective.target)
            objective.done = objective.progress >= objective.target
            if objective.done and not beforeDone then
                completedNew = true
            end
        end
    end

    if matched then
        recalcDoneCount()
    end

    return completedNew
end

function RunMissions.getState()
    return {
        active = state.active,
        doneCount = state.doneCount,
        total = state.total,
        completed = (state.total > 0 and state.doneCount == state.total) or false,
        lastPackId = state.lastPackId,
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
