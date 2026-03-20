-- Portal transition prompt copy budget checker.
-- Run: lua scripts/check_portal_prompt_copy_budget.lua [maxChars]

package.path = "./?.lua;./?/init.lua;" .. package.path

local Budget = require("src.portal_prompt_budget")

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
        string.format('  "status": %s,', jsonString(report.status)),
        string.format('  "budgetChars": %d,', report.budgetChars),
        string.format('  "checkedCount": %d,', report.checkedCount),
        string.format('  "warningCount": %d,', report.warningCount),
        string.format('  "maxObservedChars": %d,', report.maxObservedChars),
        '  "warnings": [',
    }

    for i, warning in ipairs(report.warnings or {}) do
        local comma = (i < #(report.warnings or {})) and "," or ""
        table.insert(lines, string.format('    {"sourceMap": %s, "targetMap": %s, "routeTag": %s, "length": %d, "overBy": %d, "prompt": %s}%s',
            jsonString(warning.sourceMap),
            jsonString(warning.targetMap),
            jsonString(warning.routeTag),
            warning.length,
            warning.overBy,
            jsonString(warning.prompt),
            comma
        ))
    end

    table.insert(lines, "  ]")
    table.insert(lines, "}")
    return table.concat(lines, "\n")
end

local function toMarkdown(report)
    local lines = {
        "# Portal Prompt Copy Budget Audit",
        "",
        string.format("- Status: **%s**", report.status),
        string.format("- Budget: **%d chars**", report.budgetChars),
        string.format("- Checked prompts: **%d**", report.checkedCount),
        string.format("- Max observed length: **%d chars**", report.maxObservedChars),
        string.format("- Warnings: **%d**", report.warningCount),
        "",
    }

    if report.warningCount > 0 then
        table.insert(lines, "## Over-budget prompts")
        for _, warning in ipairs(report.warnings) do
            table.insert(lines, string.format("- map_%s -> map_%s [%s] length=%d (+%d)", warning.sourceMap, warning.targetMap, warning.routeTag, warning.length, warning.overBy))
            table.insert(lines, string.format("  - `%s`", warning.prompt))
        end
    else
        table.insert(lines, "- No portal route preview prompt exceeds budget.")
    end

    table.insert(lines, "")
    table.insert(lines, string.format("Generated at: %s", os.date("%Y-%m-%d %H:%M:%S")))
    return table.concat(lines, "\n")
end

local budgetChars = tonumber(arg and arg[1]) or 76
local report = Budget.scanMapFiles("maps/map_*.lua", budgetChars)

ensureDir("logs/playtests")
writeFile("logs/playtests/portal_prompt_copy_budget.json", toJson(report))
writeFile("logs/playtests/portal_prompt_copy_budget.md", toMarkdown(report))

print(string.format("[PORTAL PROMPT BUDGET] status=%s checked=%d budget=%d max=%d warnings=%d", report.status, report.checkedCount, report.budgetChars, report.maxObservedChars, report.warningCount))
for _, warning in ipairs(report.warnings) do
    print(string.format("[WARN] map_%s->map_%s %s len=%d (+%d)", warning.sourceMap, warning.targetMap, warning.routeTag, warning.length, warning.overBy))
end
