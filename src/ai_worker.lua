-- AI Worker Thread for llama-server communication
-- Runs in love.thread, communicates via channels

local inputChannel = love.thread.getChannel("ai_input")
local outputChannel = love.thread.getChannel("ai_output")

local function escapeShellArg(s)
    return "'" .. s:gsub("'", "'\\''") .. "'"
end

local function callLlamaServer(prompt)
    local json = require("libs.json")

    local requestBody = json.encode({
        -- model = "qwen3.5-9b",
        model = "qwen3.5-4b",
        messages = {
            { role = "user", content = prompt }
        },
        temperature = 0.7,
        max_tokens = 500,
    })

    local cmd = "curl -s -m 30 http://127.0.0.1:8001/v1/chat/completions "
        .. "-H 'Content-Type: application/json' "
        .. "-d " .. escapeShellArg(requestBody)

    local handle = io.popen(cmd, "r")
    if not handle then
        return nil, "Failed to execute curl"
    end

    local result = handle:read("*a")
    handle:close()

    if not result or #result == 0 then
        return nil, "Empty response from server"
    end

    local ok, response = pcall(json.decode, result)
    if not ok then
        return nil, "JSON parse error: " .. tostring(response)
    end

    if response.choices and response.choices[1] and response.choices[1].message then
        local content = response.choices[1].message.content or ""
        -- Strip <think>...</think> blocks (Qwen thinking mode, may span multiple lines)
        while content:find("<think>") do
            local s = content:find("<think>")
            local _, e = content:find("</think>", s)
            if e then
                content = content:sub(1, s - 1) .. content:sub(e + 1)
            else
                -- Unclosed <think> tag, remove from <think> onwards
                content = content:sub(1, s - 1)
                break
            end
        end
        content = content:match("^%s*(.-)%s*$") or content
        -- Extract top-level JSON object (handles nested braces)
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
        print("[AiWorker] Raw AI response: " .. content:sub(1, 500))
        print("[AiWorker] Extracted JSON: " .. jsonStr:sub(1, 500))
        local ok2, parsed = pcall(json.decode, jsonStr)
        if ok2 and type(parsed) == "table" then
            -- Reassemble flat stats keys (stats_atk, stats_def, ...) into stats table
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
        else
            return nil, "Failed to parse AI JSON: " .. jsonStr:sub(1, 100)
        end
    end

    return nil, "Unexpected response structure"
end

local function makeFallback(itemId)
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
        local result, err = callLlamaServer(data.prompt)
        if not result then
            print("[AiWorker] ERROR for " .. tostring(data.itemId) .. ": " .. tostring(err))
            result = makeFallback(data.itemId)
            result.error = err
        end
        local json = require("libs.json")
        outputChannel:push(json.encode({
            itemId = data.itemId,
            result = result,
        }))
    end
end
