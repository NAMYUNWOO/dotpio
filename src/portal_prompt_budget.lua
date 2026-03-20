local PortalPromptBudget = {}

local VALID_ROUTE_TAGS = {
    SAFE = true,
    RISK = true,
    SPIKE = true,
}

local function normalizeRouteTag(tag)
    local value = string.upper(tostring(tag or ""))
    if VALID_ROUTE_TAGS[value] then
        return value
    end
    return "UNKNOWN"
end

local function resolveCoach(routeTag)
    if routeTag == "SAFE" then
        return "LOW PRESSURE"
    elseif routeTag == "RISK" then
        return "BALANCED RISK"
    elseif routeTag == "SPIKE" then
        return "HIGH PRESSURE"
    end
    return "NO DATA"
end

local function resolvePressure(routeTag)
    if routeTag == "SAFE" then
        return 1
    elseif routeTag == "RISK" then
        return 2
    elseif routeTag == "SPIKE" then
        return 3
    end
    return 2
end

local function buildPrompt(routeTag)
    local normalized = normalizeRouteTag(routeTag)
    local coach = resolveCoach(normalized)
    local pressure = resolvePressure(normalized)
    return string.format("PORTAL READY -> ENTER:JUMP  N:CANCEL  NEXT ROUTE:%s  COACH:%s  PRESSURE:%d", normalized, coach, pressure)
end

local function parseMapId(path)
    local id = tostring(path):match("map_(%d+)%.lua$")
    return id
end

local function collectEntries(pattern)
    local files = {}
    local pipe = io.popen(string.format("ls %s 2>/dev/null", pattern))
    if pipe then
        for line in pipe:lines() do
            if line ~= "" then
                table.insert(files, line)
            end
        end
        pipe:close()
    end
    table.sort(files)

    local entries = {}
    local routeByMap = {}
    for _, path in ipairs(files) do
        local ok, mapData = pcall(dofile, path)
        if ok and type(mapData) == "table" then
            local mapId = parseMapId(path)
            if mapId then
                local metadata = mapData.metadata
                local hazard = metadata and metadata.overclockHazard
                local routeTag = type(hazard) == "table" and normalizeRouteTag(hazard.routeTag) or "UNKNOWN"
                routeByMap[mapId] = routeTag

                for _, portal in ipairs(mapData.portals or {}) do
                    table.insert(entries, {
                        sourceMap = mapId,
                        targetMap = tostring(portal.targetMap or ""),
                    })
                end
            end
        end
    end

    for _, entry in ipairs(entries) do
        entry.targetRouteTag = routeByMap[entry.targetMap] or "UNKNOWN"
    end

    return entries
end

function PortalPromptBudget.analyze(entries, maxChars)
    local limit = tonumber(maxChars) or 76
    if limit < 1 then
        limit = 1
    end

    local warnings = {}
    local samples = {}
    local maxObserved = 0

    for _, entry in ipairs(entries or {}) do
        local routeTag = normalizeRouteTag(entry.targetRouteTag)
        local prompt = buildPrompt(routeTag)
        local length = #prompt
        if length > maxObserved then
            maxObserved = length
        end

        local sample = {
            sourceMap = entry.sourceMap or "",
            targetMap = entry.targetMap or "",
            routeTag = routeTag,
            coach = resolveCoach(routeTag),
            pressure = resolvePressure(routeTag),
            length = length,
            prompt = prompt,
        }
        table.insert(samples, sample)

        if length > limit then
            table.insert(warnings, {
                sourceMap = sample.sourceMap,
                targetMap = sample.targetMap,
                routeTag = routeTag,
                length = length,
                overBy = length - limit,
                prompt = prompt,
            })
        end
    end

    return {
        status = (#warnings > 0) and "WARN" or "OK",
        budgetChars = limit,
        checkedCount = #samples,
        warningCount = #warnings,
        maxObservedChars = maxObserved,
        warnings = warnings,
        samples = samples,
    }
end

function PortalPromptBudget.scanMapFiles(pattern, maxChars)
    local entries = collectEntries(pattern or "maps/map_*.lua")
    return PortalPromptBudget.analyze(entries, maxChars)
end

return PortalPromptBudget
