-- AI Worker Thread for DeepSeek API communication
-- Runs in love.thread, communicates via channels

local inputChannel = love.thread.getChannel("ai_input")
local outputChannel = love.thread.getChannel("ai_output")

local function escapeShellArg(s)
    return "'" .. s:gsub("'", "'\\''") .. "'"
end

local function loadApiKey()
    local key = os.getenv("DEEPSEEK_API_KEY")
    if key and #key > 0 then return key end

    local f = io.open(".env.ai", "r")
    if not f then return nil end
    for line in f:lines() do
        local k, v = line:match("^%s*([A-Za-z_][A-Za-z0-9_]*)%s*=%s*(.-)%s*$")
        if k == "DEEPSEEK_API_KEY" and v and #v > 0 then
            v = v:gsub('^"', ""):gsub('"$', "")
            v = v:gsub("^'", ""):gsub("'$", "")
            f:close()
            return v
        end
    end
    f:close()
    return nil
end

local function callDeepSeek(messages, maxTokens, temperature)
    local json = require("libs.json")
    local apiKey = loadApiKey()
    if not apiKey then
        return nil, "DEEPSEEK_API_KEY not set (env or .env.ai)"
    end

    local requestBody = json.encode({
        model = "deepseek-chat",
        messages = messages,
        temperature = temperature or 0.6,
        max_tokens = maxTokens or 500,
    })

    local cmd = "curl -s -m 35 https://api.deepseek.com/v1/chat/completions "
        .. "-H 'Content-Type: application/json' "
        .. "-H " .. escapeShellArg("Authorization: Bearer " .. apiKey) .. " "
        .. "-d " .. escapeShellArg(requestBody)

    local handle = io.popen(cmd, "r")
    if not handle then
        return nil, "Failed to execute curl"
    end

    local result = handle:read("*a")
    handle:close()

    if not result or #result == 0 then
        return nil, "Empty response from DeepSeek"
    end

    local ok, response = pcall(json.decode, result)
    if not ok then
        return nil, "JSON parse error: " .. tostring(response)
    end

    if response.error then
        return nil, tostring(response.error.message or "DeepSeek API error")
    end

    local content = (((response.choices or {})[1] or {}).message or {}).content
    if not content or #content == 0 then
        return nil, "Unexpected response structure"
    end

    while content:find("<think>") do
        local s = content:find("<think>")
        local _, e = content:find("</think>", s)
        if e then
            content = content:sub(1, s - 1) .. content:sub(e + 1)
        else
            content = content:sub(1, s - 1)
            break
        end
    end
    content = content:match("^%s*(.-)%s*$") or content

    local function extractJson(s)
        local start = s:find("{")
        if not start then return s end
        local depth = 0
        for i = start, #s do
            local c = s:sub(i, i)
            if c == "{" then depth = depth + 1
            elseif c == "}" then
                depth = depth - 1
                if depth == 0 then return s:sub(start, i) end
            end
        end
        return s:sub(start)
    end

    local jsonStr = extractJson(content)
    local ok2, parsed = pcall(json.decode, jsonStr)
    if not ok2 or type(parsed) ~= "table" then
        return nil, "Failed to parse AI JSON"
    end

    return parsed
end

local function normalizeStats(parsed)
    local ALL_KEYS = {"atk","def","agi","int","fire","water","grass","elec","ice","poison","earth","wind"}
    if parsed.stats_atk ~= nil then
        local cleanStats = {}
        for _, key in ipairs(ALL_KEYS) do
            local v = tonumber(parsed["stats_" .. key]) or 0
            cleanStats[key] = math.max(-2, math.min(5, math.floor(v)))
            parsed["stats_" .. key] = nil
        end
        parsed.stats = cleanStats
    elseif parsed.stats and type(parsed.stats) == "table" then
        local cleanStats = {}
        for _, key in ipairs(ALL_KEYS) do
            local v = tonumber(parsed.stats[key]) or 0
            cleanStats[key] = math.max(-2, math.min(5, math.floor(v)))
        end
        parsed.stats = cleanStats
    end
    return parsed
end

local function makeFallback()
    return {
        lore = "A mysterious item found in the dungeon.",
        traits = {"Worn from use", "Slightly warm"},
        effect = "Unknown effect",
        rarity = "Common",
        stats = {atk=1, def=0, agi=0, int=0, fire=0, water=0, grass=0, elec=0, ice=0, poison=0, earth=0, wind=0},
        fallback = true,
    }
end

-- Worker loop
while true do
    local request = inputChannel:demand()
    if request == "quit" then break end

    local ok, data = pcall(function()
        local json = require("libs.json")
        return json.decode(request)
    end)

    if ok and data then
        local mode = data.mode or "describe"
        local parsed, err

        if mode == "describe" then
            parsed, err = callDeepSeek({
                { role = "system", content = "You generate compact valid JSON only." },
                { role = "user", content = data.prompt }
            }, 500, 0.7)
            if parsed then parsed = normalizeStats(parsed) end

            if not parsed then
                parsed = makeFallback()
                parsed.error = err
            end

            local json = require("libs.json")
            outputChannel:push(json.encode({ itemId = data.itemId, result = parsed }))

        elseif mode == "disassemble" or mode == "build" then
            parsed, err = callDeepSeek({
                { role = "system", content = "You are a roguelike item system generator. Return strict JSON only." },
                { role = "user", content = data.prompt }
            }, 280, 0.5)
            if not parsed then
                parsed = { fallback = true, error = err }
            end
            local json = require("libs.json")
            outputChannel:push(json.encode({ requestId = data.requestId, mode = mode, result = parsed }))
        end
    end
end
