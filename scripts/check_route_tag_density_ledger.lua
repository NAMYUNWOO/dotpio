-- Route-tag density ledger by reachable portal depth.
-- Run: lua scripts/check_route_tag_density_ledger.lua

package.path = "./?.lua;./?/init.lua;" .. package.path

local Ledger = require("src.route_tag_density_ledger")

local function ensureDir(path)
    os.execute(string.format("mkdir -p %q", path))
end

local function writeFile(path, content)
    local file = assert(io.open(path, "w"))
    file:write(content)
    file:close()
end

local function jsonString(value)
    local s = tostring(value or "")
    s = s:gsub("\\", "\\\\"):gsub('"', '\\"'):gsub("\n", "\\n")
    return '"' .. s .. '"'
end

local function toJson(report)
    local lines = {
        "{",
        string.format('  "generatedAt": %s,', jsonString(report.generatedAt)),
        string.format('  "mapCount": %d,', report.mapCount),
        '  "ledgers": [',
    }

    for i, ledger in ipairs(report.ledgers or {}) do
        local ledgerComma = (i < #report.ledgers) and "," or ""
        table.insert(lines, "    {")
        table.insert(lines, string.format('      "startMap": %s,', jsonString(ledger.startMap)))
        table.insert(lines, string.format('      "maxDepth": %d,', ledger.maxDepth or 0))
        table.insert(lines, string.format('      "reachableCount": %d,', ledger.reachableCount or 0))
        table.insert(lines, '      "depthRows": [')

        for j, row in ipairs(ledger.depthRows or {}) do
            local rowComma = (j < #ledger.depthRows) and "," or ""
            table.insert(lines, "        {")
            table.insert(lines, string.format('          "depth": %d,', row.depth or 0))
            table.insert(lines, string.format('          "totalReachable": %d,', row.totalReachable or 0))
            table.insert(lines, string.format('          "tagCounts": {"SAFE": %d, "RISK": %d, "SPIKE": %d},', row.tagCounts.SAFE or 0, row.tagCounts.RISK or 0, row.tagCounts.SPIKE or 0))
            table.insert(lines, '          "maps": [')
            for k, mapEntry in ipairs(row.maps or {}) do
                local mapComma = (k < #row.maps) and "," or ""
                table.insert(lines, string.format('            {"mapId": %s, "routeTag": %s}%s', jsonString(mapEntry.mapId), jsonString(mapEntry.routeTag), mapComma))
            end
            table.insert(lines, "          ]")
            table.insert(lines, "        }" .. rowComma)
        end

        table.insert(lines, "      ]")
        table.insert(lines, "    }" .. ledgerComma)
    end

    table.insert(lines, "  ]")
    table.insert(lines, "}")
    return table.concat(lines, "\n")
end

local function toMarkdown(report)
    local lines = {
        "# Route Tag Density Ledger",
        "",
        string.format("- Generated at: %s", report.generatedAt),
        string.format("- Maps analyzed: **%d**", report.mapCount or 0),
        "",
    }

    for _, ledger in ipairs(report.ledgers or {}) do
        table.insert(lines, string.format("## Start map_%s", ledger.startMap))
        table.insert(lines, string.format("- Reachable maps: **%d**", ledger.reachableCount or 0))
        table.insert(lines, string.format("- Max depth: **%d**", ledger.maxDepth or 0))

        if #(ledger.depthRows or {}) == 0 then
            table.insert(lines, "- No outbound reachable maps.")
            table.insert(lines, "")
        else
            table.insert(lines, "")
            for _, row in ipairs(ledger.depthRows) do
                table.insert(lines, string.format("- Depth %d -> SAFE:%d RISK:%d SPIKE:%d (reachable:%d)", row.depth, row.tagCounts.SAFE or 0, row.tagCounts.RISK or 0, row.tagCounts.SPIKE or 0, row.totalReachable or 0))
                for _, mapEntry in ipairs(row.maps or {}) do
                    table.insert(lines, string.format("  - map_%s [%s]", mapEntry.mapId, mapEntry.routeTag))
                end
            end
            table.insert(lines, "")
        end
    end

    return table.concat(lines, "\n")
end

local report = Ledger.scanMapFiles("maps/map_*.lua")

ensureDir("logs/playtests")
writeFile("logs/playtests/route_tag_density_ledger.json", toJson(report))
writeFile("logs/playtests/route_tag_density_ledger.md", toMarkdown(report))

print(string.format("[ROUTE TAG DENSITY LEDGER] maps=%d startMaps=%d", report.mapCount or 0, #(report.ledgers or {})))
