-- Portal transition prompt token-order + budget parser checker.
-- Run: lua scripts/check_portal_prompt_token_order.lua [maxChars]

package.path = package.path .. ";./?.lua;./src/?.lua"

local Linter = require("src.portal_prompt_linter")

local function writeFile(path, content)
    local handle, err = io.open(path, "w")
    if not handle then
        error("failed to write file `" .. tostring(path) .. "`: " .. tostring(err))
    end
    handle:write(content)
    handle:close()
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
        '  "warnings": [',
    }

    for i, warning in ipairs(report.warnings or {}) do
        local comma = (i < #(report.warnings or {})) and "," or ""
        table.insert(lines, "    {")
        table.insert(lines, string.format('      "routeTag": %s,', jsonString(warning.routeTag)))
        table.insert(lines, string.format('      "pressure": %d,', warning.pressure))
        table.insert(lines, string.format('      "mode": %s,', jsonString(warning.mode)))
        table.insert(lines, string.format('      "length": %d,', warning.length))
        table.insert(lines, string.format('      "overBy": %d,', warning.overBy or 0))
        table.insert(lines, string.format('      "prompt": %s,', jsonString(warning.prompt)))
        table.insert(lines, '      "lintWarnings": [')
        for j, text in ipairs(warning.lintWarnings or {}) do
            local lintComma = (j < #(warning.lintWarnings or {})) and "," or ""
            table.insert(lines, string.format('        %s%s', jsonString(text), lintComma))
        end
        table.insert(lines, "      ]")
        table.insert(lines, "    }" .. comma)
    end

    table.insert(lines, "  ]")
    local writerPreview = report.writerPreview or {}
    local aliasRows = writerPreview.aliasPreviewRows or {}
    table.insert(lines, ',  "writerPreview": {')
    table.insert(lines, string.format('    "token": %s,', jsonString(writerPreview.token or "")))
    table.insert(lines, string.format('    "legendVersion": %s,', jsonString(writerPreview.legendVersion or "")))
    table.insert(lines, string.format('    "legendHash": %s,', jsonString(writerPreview.legendHash or "")))
    table.insert(lines, '    "decode": {')
    table.insert(lines, string.format('      "S": %s,', jsonString((writerPreview.decode or {}).S or "")))
    table.insert(lines, string.format('      "U": %s', jsonString((writerPreview.decode or {}).U or "")))
    table.insert(lines, "    },")
    table.insert(lines, '    "aliasPreviewRows": [')
    for i, row in ipairs(aliasRows) do
        local comma = (i < #aliasRows) and "," or ""
        table.insert(lines, string.format('      %s%s', jsonString(row), comma))
    end
    table.insert(lines, "    ]")
    table.insert(lines, "  }")
    table.insert(lines, "}")
    return table.concat(lines, "\n")
end

local function toMarkdown(report)
    local lines = {
        "# Portal Prompt Token-Order Lint",
        "",
        string.format("- Status: **%s**", report.status),
        string.format("- Budget: **%d chars**", report.budgetChars),
        string.format("- Checked prompts: **%d**", report.checkedCount),
        string.format("- Warnings: **%d**", report.warningCount),
        "",
        "Expected order: `ACTION -> ROUTE -> COACH -> PRESSURE`",
        "",
    }

    if report.warningCount > 0 then
        table.insert(lines, "## Warnings")
        for _, warning in ipairs(report.warnings) do
            table.insert(lines, string.format("- [%s/P%d/%s] len=%d (+%d)", warning.routeTag, warning.pressure, warning.mode, warning.length, warning.overBy or 0))
            table.insert(lines, string.format("  - `%s`", warning.prompt))
            for _, lintWarning in ipairs(warning.lintWarnings or {}) do
                table.insert(lines, string.format("  - lint: %s", lintWarning))
            end
        end
    else
        table.insert(lines, "- All sampled prompts satisfy token order and budget selection checks.")
    end

    local writerPreview = report.writerPreview or {}
    local decode = writerPreview.decode or {}
    table.insert(lines, "")
    table.insert(lines, "## Writer Preview — CBGCFXWSBPFXPD MICROLINE")
    table.insert(lines, string.format("- Token: `%s`", writerPreview.token or "CBGCFXWSBPFXPD MICROLINE"))
    table.insert(lines, string.format("- Legend: `v=%s hash=%s`", writerPreview.legendVersion or "?", writerPreview.legendHash or "?"))
    table.insert(lines, string.format("- `S` decode: %s", decode.S or "(missing)"))
    table.insert(lines, string.format("- `U` decode: %s", decode.U or "(missing)"))
    for _, row in ipairs(writerPreview.aliasPreviewRows or {}) do
        table.insert(lines, string.format("- Preview: `%s`", row))
    end

    return table.concat(lines, "\n")
end

local budgetChars = tonumber(arg and arg[1]) or 76
local report = Linter.analyze(budgetChars)

writeFile("logs/playtests/portal_prompt_token_order.json", toJson(report))
writeFile("logs/playtests/portal_prompt_token_order.md", toMarkdown(report))

print(string.format("[PORTAL PROMPT LINT] status=%s checked=%d budget=%d warnings=%d", report.status, report.checkedCount, report.budgetChars, report.warningCount))
for _, warning in ipairs(report.warnings or {}) do
    print(string.format("[WARN] %s P%d %s len=%d (+%d)", warning.routeTag, warning.pressure, warning.mode, warning.length, warning.overBy or 0))
end
