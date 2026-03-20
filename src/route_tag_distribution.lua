local RouteTagDistribution = {}

local VALID_TAGS = {
    SAFE = true,
    RISK = true,
    SPIKE = true,
}

local function normalizeTag(tag)
    local value = string.upper(tostring(tag or ""))
    if VALID_TAGS[value] then
        return value
    end
    return nil
end

function RouteTagDistribution.analyzeMapTables(entries)
    local counts = { SAFE = 0, RISK = 0, SPIKE = 0 }
    local hazardMaps = {}
    local invalidTags = {}

    for _, entry in ipairs(entries or {}) do
        local mapName = tostring(entry.mapName or "")
        local mapData = entry.mapData
        if type(mapData) == "table" then
            local metadata = mapData.metadata
            local hazard = metadata and metadata.overclockHazard
            if type(hazard) == "table" then
                local rawTag = hazard.routeTag
                local tag = normalizeTag(rawTag)
                if tag then
                    counts[tag] = counts[tag] + 1
                    table.insert(hazardMaps, { mapName = mapName, routeTag = tag })
                else
                    table.insert(invalidTags, { mapName = mapName, routeTag = tostring(rawTag or "") })
                end
            end
        end
    end

    table.sort(hazardMaps, function(a, b)
        return a.mapName < b.mapName
    end)

    local uniqueTags = 0
    for _, tag in ipairs({ "SAFE", "RISK", "SPIKE" }) do
        if counts[tag] > 0 then
            uniqueTags = uniqueTags + 1
        end
    end

    local status = "OK"
    local warnings = {}
    if #hazardMaps == 0 then
        status = "WARN"
        table.insert(warnings, "No hazard-enabled maps expose a valid routeTag.")
    elseif uniqueTags == 1 then
        status = "WARN"
        table.insert(warnings, "All hazard-enabled maps converge on a single routeTag profile.")
    end
    if #invalidTags > 0 then
        status = "WARN"
        table.insert(warnings, "One or more hazard-enabled maps contain invalid routeTag values.")
    end

    return {
        status = status,
        hazardMapCount = #hazardMaps,
        uniqueRouteTagCount = uniqueTags,
        counts = counts,
        hazardMaps = hazardMaps,
        invalidTags = invalidTags,
        warnings = warnings,
    }
end

function RouteTagDistribution.scanMapFiles(globPattern)
    local pattern = globPattern or "maps/map_*.lua"
    local command = string.format("ls %s 2>/dev/null", pattern)
    local handle = io.popen(command)
    local entries = {}
    if handle then
        for path in handle:lines() do
            local mapName = path:match("map_(%d+)%.lua$") or path
            local ok, mapData = pcall(dofile, path)
            if ok then
                table.insert(entries, { mapName = mapName, mapData = mapData })
            else
                table.insert(entries, { mapName = mapName, mapData = nil })
            end
        end
        handle:close()
    end
    return RouteTagDistribution.analyzeMapTables(entries)
end

return RouteTagDistribution
