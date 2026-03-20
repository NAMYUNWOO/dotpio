local RouteTagDensityLedger = {}

local VALID_TAGS = { SAFE = true, RISK = true, SPIKE = true }

local function normalizeTag(value)
    local tag = string.upper(tostring(value or ""))
    if VALID_TAGS[tag] then
        return tag
    end
    return nil
end

local function sortedKeys(map)
    local keys = {}
    for key in pairs(map or {}) do
        table.insert(keys, key)
    end
    table.sort(keys)
    return keys
end

local function parseMapId(path)
    return path:match("map_(%d+)%.lua$")
end

function RouteTagDensityLedger.buildGraph(entries)
    local graph = {}
    local routeTags = {}

    for _, entry in ipairs(entries or {}) do
        local mapId = tostring(entry.mapId or "")
        if mapId ~= "" then
            graph[mapId] = graph[mapId] or { edges = {} }
            local mapData = entry.mapData
            if type(mapData) == "table" then
                local metadata = mapData.metadata
                local hazard = metadata and metadata.overclockHazard
                local tag = type(hazard) == "table" and normalizeTag(hazard.routeTag) or nil
                routeTags[mapId] = tag

                for _, portal in ipairs(mapData.portals or {}) do
                    local targetMap = tostring(portal.targetMap or "")
                    if targetMap ~= "" then
                        graph[mapId].edges[targetMap] = true
                    end
                end
            end
        end
    end

    for mapId, node in pairs(graph) do
        local edges = sortedKeys(node.edges)
        graph[mapId].edges = edges
    end

    return graph, routeTags
end

local function bfsFromMap(startMapId, graph, routeTags)
    local queue = { { mapId = startMapId, depth = 0 } }
    local front = 1
    local visited = { [startMapId] = true }
    local byDepth = {}
    local maxDepth = 0

    while front <= #queue do
        local current = queue[front]
        front = front + 1

        local depth = current.depth
        maxDepth = math.max(maxDepth, depth)

        if depth > 0 then
            local bucket = byDepth[depth]
            if not bucket then
                bucket = {
                    depth = depth,
                    totalReachable = 0,
                    tagCounts = { SAFE = 0, RISK = 0, SPIKE = 0 },
                    maps = {},
                }
                byDepth[depth] = bucket
            end

            local mapId = current.mapId
            local tag = routeTags[mapId]
            bucket.totalReachable = bucket.totalReachable + 1
            if tag then
                bucket.tagCounts[tag] = bucket.tagCounts[tag] + 1
            end
            table.insert(bucket.maps, { mapId = mapId, routeTag = tag or "NONE" })
        end

        local edges = (graph[current.mapId] and graph[current.mapId].edges) or {}
        for _, nextMapId in ipairs(edges) do
            if not visited[nextMapId] and graph[nextMapId] then
                visited[nextMapId] = true
                table.insert(queue, { mapId = nextMapId, depth = depth + 1 })
            end
        end
    end

    local depthRows = {}
    for depth = 1, maxDepth do
        local row = byDepth[depth]
        if row then
            table.sort(row.maps, function(a, b)
                return a.mapId < b.mapId
            end)
            table.insert(depthRows, row)
        end
    end

    return {
        startMap = startMapId,
        maxDepth = maxDepth,
        reachableCount = #queue - 1,
        depthRows = depthRows,
    }
end

function RouteTagDensityLedger.analyzeEntries(entries)
    local graph, routeTags = RouteTagDensityLedger.buildGraph(entries)
    local startMaps = sortedKeys(graph)
    local ledgers = {}

    for _, startMapId in ipairs(startMaps) do
        table.insert(ledgers, bfsFromMap(startMapId, graph, routeTags))
    end

    return {
        generatedAt = os.date("%Y-%m-%d %H:%M:%S"),
        mapCount = #startMaps,
        ledgers = ledgers,
    }
end

function RouteTagDensityLedger.scanMapFiles(globPattern)
    local pattern = globPattern or "maps/map_*.lua"
    local command = string.format("ls %s 2>/dev/null", pattern)
    local handle = io.popen(command)
    local entries = {}

    if handle then
        for path in handle:lines() do
            local mapId = parseMapId(path)
            if mapId then
                local ok, mapData = pcall(dofile, path)
                if ok and type(mapData) == "table" then
                    table.insert(entries, { mapId = mapId, mapData = mapData })
                end
            end
        end
        handle:close()
    end

    table.sort(entries, function(a, b)
        return a.mapId < b.mapId
    end)

    return RouteTagDensityLedger.analyzeEntries(entries)
end

return RouteTagDensityLedger
