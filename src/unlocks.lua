local Unlocks = {}

local DEFINITIONS = {
    advanced_build_categories = {
        id = "advanced_build_categories",
        label = "Advanced Schematics",
        description = "Unlocks ring/wand/gem synthesis targets for AI builds.",
    },
}

local state = {
    flags = {},
}

local function cloneTable(src)
    local out = {}
    for k, v in pairs(src or {}) do
        out[k] = v
    end
    return out
end

local function ensureKnown(flagId)
    return DEFINITIONS[flagId] ~= nil
end

function Unlocks.resetAll()
    state.flags = {}
    for flagId in pairs(DEFINITIONS) do
        state.flags[flagId] = false
    end
end

function Unlocks.isUnlocked(flagId)
    if not ensureKnown(flagId) then return false end
    return state.flags[flagId] == true
end

function Unlocks.unlock(flagId)
    if not ensureKnown(flagId) then return false end
    if state.flags[flagId] == true then
        return false
    end
    state.flags[flagId] = true
    return true
end

function Unlocks.getDefinition(flagId)
    return DEFINITIONS[flagId]
end

function Unlocks.getAllFlags()
    return cloneTable(state.flags)
end

Unlocks.resetAll()

return Unlocks
