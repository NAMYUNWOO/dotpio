-- Route-tag distribution checker across hazard-enabled maps.
-- Run: lua scripts/check_route_tag_distribution.lua

package.path = "./?.lua;./?/init.lua;" .. package.path

local RouteTagDistribution = require("src.route_tag_distribution")

local function ensureDir(path)
    os.execute(string.format("mkdir -p %q", path))
end

local function writeFile(path, content)
    local file = assert(io.open(path, "w"))
    file:write(content)
    file:close()
end

local function encodeJsonString(value)
    local s = tostring(value or "")
    s = s:gsub("\\", "\\\\"):gsub('"', '\\"'):gsub("\n", "\\n")
    return '"' .. s .. '"'
end

local function toJson(report)
    local lines = {
        "{",
        string.format('  "status": %s,', encodeJsonString(report.status)),
        string.format('  "hazardMapCount": %d,', report.hazardMapCount),
        string.format('  "uniqueRouteTagCount": %d,', report.uniqueRouteTagCount),
        string.format('  "counts": {"SAFE": %d, "RISK": %d, "SPIKE": %d},', report.counts.SAFE, report.counts.RISK, report.counts.SPIKE),
        '  "hazardMaps": [',
    }

    for i, entry in ipairs(report.hazardMaps) do
        local comma = (i < #report.hazardMaps) and "," or ""
        table.insert(lines, string.format('    {"mapName": %s, "routeTag": %s}%s', encodeJsonString(entry.mapName), encodeJsonString(entry.routeTag), comma))
    end

    table.insert(lines, "  ],")
    table.insert(lines, '  "invalidTags": [')
    for i, entry in ipairs(report.invalidTags) do
        local comma = (i < #report.invalidTags) and "," or ""
        table.insert(lines, string.format('    {"mapName": %s, "routeTag": %s}%s', encodeJsonString(entry.mapName), encodeJsonString(entry.routeTag), comma))
    end

    table.insert(lines, "  ],")
    table.insert(lines, '  "warnings": [')
    for i, warning in ipairs(report.warnings) do
        local comma = (i < #report.warnings) and "," or ""
        table.insert(lines, string.format("    %s%s", encodeJsonString(warning), comma))
    end

    table.insert(lines, "  ]")
    table.insert(lines, "}")
    return table.concat(lines, "\n")
end

local function toMarkdown(report)
    local lines = {
        "# Route Tag Distribution Audit",
        "",
        string.format("- Status: **%s**", report.status),
        string.format("- Hazard-enabled maps with valid route tags: **%d**", report.hazardMapCount),
        string.format("- Unique route profiles: **%d**", report.uniqueRouteTagCount),
        string.format("- Counts: SAFE=%d, RISK=%d, SPIKE=%d", report.counts.SAFE, report.counts.RISK, report.counts.SPIKE),
        "",
        "## Hazard maps",
    }

    if #report.hazardMaps == 0 then
        table.insert(lines, "- (none)")
    else
        for _, entry in ipairs(report.hazardMaps) do
            table.insert(lines, string.format("- map_%s -> %s", entry.mapName, entry.routeTag))
        end
    end

    if #report.invalidTags > 0 then
        table.insert(lines, "")
        table.insert(lines, "## Invalid route tags")
        for _, entry in ipairs(report.invalidTags) do
            table.insert(lines, string.format("- map_%s -> `%s`", entry.mapName, entry.routeTag))
        end
    end

    if #report.warnings > 0 then
        table.insert(lines, "")
        table.insert(lines, "## Warnings")
        for _, warning in ipairs(report.warnings) do
            table.insert(lines, "- " .. warning)
        end
    end

    table.insert(lines, "")
    table.insert(lines, string.format("Generated at: %s", os.date("%Y-%m-%d %H:%M:%S")))
    return table.concat(lines, "\n")
end

local report = RouteTagDistribution.scanMapFiles("maps/map_*.lua")

ensureDir("logs/playtests")
writeFile("logs/playtests/route_tag_distribution.json", toJson(report))
writeFile("logs/playtests/route_tag_distribution.md", toMarkdown(report))

local summary = string.format(
    "[ROUTE TAG AUDIT] status=%s hazardMaps=%d unique=%d SAFE=%d RISK=%d SPIKE=%d",
    report.status,
    report.hazardMapCount,
    report.uniqueRouteTagCount,
    report.counts.SAFE,
    report.counts.RISK,
    report.counts.SPIKE
)
print(summary)
if #report.warnings > 0 then
    for _, warning in ipairs(report.warnings) do
        print("[WARN] " .. warning)
    end
end
