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
        model = "qwen3.5-9b",
        messages = {
            { role = "user", content = prompt }
        },
        temperature = 0.7,
        max_tokens = 300,
    })

    local cmd = "curl -s -m 10 http://127.0.0.1:8001/v1/chat/completions "
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
        -- Strip <think>...</think> blocks (Qwen thinking mode)
        content = content:gsub("<think>.-</think>", "")
        content = content:match("^%s*(.-)%s*$") or content
        -- Try to extract JSON from the content
        local jsonStr = content:match("{.-}") or content
        local ok2, parsed = pcall(json.decode, jsonStr)
        if ok2 and type(parsed) == "table" then
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
