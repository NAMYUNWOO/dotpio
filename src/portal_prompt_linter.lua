local PortalPromptLinter = {}

local ROUTE_TAGS = { "SAFE", "RISK", "SPIKE", "UNKNOWN" }
local COACH_BY_ROUTE = {
    SAFE = "LOW PRESSURE",
    RISK = "BALANCED RISK",
    SPIKE = "HIGH PRESSURE",
    UNKNOWN = "NO DATA",
}
local COMPACT_COACH_BY_ROUTE = {
    SAFE = "LOW",
    RISK = "MID",
    SPIKE = "HIGH",
    UNKNOWN = "UNK",
}

local function normalizeRouteTag(routeTag)
    local value = string.upper(tostring(routeTag or ""))
    for _, valid in ipairs(ROUTE_TAGS) do
        if value == valid then
            return value
        end
    end
    return "UNKNOWN"
end

local function buildDetailedPrompt(routeTag, pressure)
    local tag = normalizeRouteTag(routeTag)
    return string.format("PORTAL READY -> ENTER:JUMP  N:CANCEL  NEXT ROUTE:%s  COACH:%s  PRESSURE:%d", tag, COACH_BY_ROUTE[tag], pressure)
end

local function buildCompactPrompt(routeTag, pressure)
    local tag = normalizeRouteTag(routeTag)
    return string.format("PORTAL READY -> ENTER:JUMP  N:CANCEL  NEXT:%s  COACH:%s  P:%d", tag, COMPACT_COACH_BY_ROUTE[tag], pressure)
end

local function resolveTokenOrder(prompt)
    local actionPos = prompt:find("ENTER:JUMP", 1, true)
    local routePos = prompt:find("NEXT ROUTE:", 1, true) or prompt:find("NEXT:", 1, true)
    local coachPos = prompt:find("COACH:", 1, true)
    local pressurePos = prompt:find("PRESSURE:", 1, true) or prompt:find("P:", 1, true)

    return {
        ACTION = actionPos,
        ROUTE = routePos,
        COACH = coachPos,
        PRESSURE = pressurePos,
    }
end

local function lintPrompt(prompt)
    local positions = resolveTokenOrder(prompt)
    local warnings = {}

    for _, token in ipairs({ "ACTION", "ROUTE", "COACH", "PRESSURE" }) do
        if not positions[token] then
            table.insert(warnings, string.format("missing token `%s`", token))
        end
    end

    if positions.ACTION and positions.ROUTE and positions.ACTION > positions.ROUTE then
        table.insert(warnings, "token order violation: ACTION appears after ROUTE")
    end
    if positions.ROUTE and positions.COACH and positions.ROUTE > positions.COACH then
        table.insert(warnings, "token order violation: ROUTE appears after COACH")
    end
    if positions.COACH and positions.PRESSURE and positions.COACH > positions.PRESSURE then
        table.insert(warnings, "token order violation: COACH appears after PRESSURE")
    end

    return {
        ok = #warnings == 0,
        positions = positions,
        warnings = warnings,
    }
end

function PortalPromptLinter.analyze(maxChars)
    local budget = tonumber(maxChars) or 76
    if budget < 1 then
        budget = 1
    end

    local samples = {}
    local warnings = {}

    for _, routeTag in ipairs(ROUTE_TAGS) do
        for pressure = 1, 5 do
            local detailed = buildDetailedPrompt(routeTag, pressure)
            local compact = buildCompactPrompt(routeTag, pressure)
            local selectedMode = (#detailed > budget) and "compact" or "detailed"
            local selectedPrompt = (selectedMode == "compact") and compact or detailed

            local lint = lintPrompt(selectedPrompt)
            local overBy = #selectedPrompt - budget
            local budgetViolation = overBy > 0
            if not lint.ok or budgetViolation then
                table.insert(warnings, {
                    routeTag = routeTag,
                    pressure = pressure,
                    mode = selectedMode,
                    prompt = selectedPrompt,
                    length = #selectedPrompt,
                    overBy = budgetViolation and overBy or 0,
                    lintWarnings = lint.warnings,
                })
            end

            table.insert(samples, {
                routeTag = routeTag,
                pressure = pressure,
                mode = selectedMode,
                length = #selectedPrompt,
                detailedLength = #detailed,
                compactLength = #compact,
                budgetOk = not budgetViolation,
                lintOk = lint.ok,
                positions = lint.positions,
                prompt = selectedPrompt,
            })
        end
    end

    return {
        status = (#warnings == 0) and "OK" or "WARN",
        budgetChars = budget,
        checkedCount = #samples,
        warningCount = #warnings,
        warnings = warnings,
        samples = samples,
    }
end

return PortalPromptLinter
