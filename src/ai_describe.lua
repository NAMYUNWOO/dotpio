-- AI Item Description Generator
-- Uses love.thread to asynchronously call llama-server (Qwen 3.5-9B)

local json = require("libs.json")
local Items = require("src.items")

local AiDescribe = {}

local cache = {}        -- itemId → result table
local pending = {}      -- itemId → true (request in flight)
local thread = nil
local inputChannel = nil
local outputChannel = nil
local serverStartedByUs = false

local SERVER_PORT = 8001
-- local SERVER_CMD = './bin/llama-server -m models/Qwen3.5-9B-UD-Q4_K_XL.gguf --alias "qwen3.5-9b" --ctx-size 8192 --port ' .. SERVER_PORT .. ' -ngl 99 > /dev/null 2>&1 &'
local SERVER_CMD = './bin/llama-server -m /Users/yunwoonam/Desktop/qwen/models/Qwen3.5-4B-GGUF/Qwen3.5-4B-Q4_K_M.gguf --alias "qwen3.5-4b" --ctx-size 8192 --port ' .. SERVER_PORT .. ' -ngl 99 > /dev/null 2>&1 &'

local function checkServerHealth()
    local handle = io.popen("curl -s -o /dev/null -w '%{http_code}' --max-time 2 http://127.0.0.1:" .. SERVER_PORT .. "/health 2>/dev/null")
    if not handle then return false end
    local result = handle:read("*a")
    handle:close()
    return result == "200"
end

local function startServer()
    -- Check if binary exists
    local f = io.open("./bin/llama-server", "r")
    if not f then
        print("[AiDescribe] ERROR: ./bin/llama-server not found")
        return false
    end
    f:close()

    -- Check if model exists
    f = io.open("./models/Qwen3.5-9B-UD-Q4_K_XL.gguf", "r")
    if not f then
        print("[AiDescribe] ERROR: model file not found")
        return false
    end
    f:close()

    print("[AiDescribe] Starting llama-server on port " .. SERVER_PORT .. "...")
    os.execute(SERVER_CMD)

    -- Wait for server to be ready (max ~30 seconds)
    for i = 1, 60 do
        love.timer.sleep(0.5)
        if checkServerHealth() then
            print("[AiDescribe] Server ready after ~" .. (i * 0.5) .. "s")
            return true
        end
    end

    print("[AiDescribe] ERROR: Server failed to start within 30 seconds")
    return false
end

function AiDescribe.init()
    cache = {}
    pending = {}

    -- Auto-start llama-server if not running
    if checkServerHealth() then
        print("[AiDescribe] Server already running on port " .. SERVER_PORT)
        serverStartedByUs = false
    else
        if startServer() then
            serverStartedByUs = true
        else
            print("[AiDescribe] WARNING: AI server unavailable. Quitting.")
            love.event.quit()
            return
        end
    end

    inputChannel = love.thread.getChannel("ai_input")
    outputChannel = love.thread.getChannel("ai_output")

    -- Clear any stale channel data
    while inputChannel:pop() do end
    while outputChannel:pop() do end

    thread = love.thread.newThread("src/ai_worker.lua")
    thread:start()
end

local CATEGORY_STAT_HINTS = {
    weapon  = "Primary: atk (2-4). Secondary: agi or fire/ice/poison if magical.",
    armor   = "Primary: def (2-4). May add earth or ice resistance.",
    helmet  = "Primary: def (1-3). May add int if magical crown/circlet.",
    boots   = "Primary: agi (1-3). May add wind or earth.",
    gloves  = "Primary: atk (1-2) or agi (1-2). May add elemental.",
    shield  = "Primary: def (2-4). May add elemental resistance.",
    robe    = "Primary: int (2-3). May add fire/ice/elec.",
    bow     = "Primary: atk (2-3), agi (1-2).",
    wand    = "Primary: int (2-4). Usually has 1 strong elemental.",
    ring    = "Flexible: 1-2 small bonuses in any stat.",
    necklace= "Flexible: 1-2 small bonuses, often int or elemental.",
    crown   = "Primary: int (1-2), def (1-2). May add elemental.",
    belt    = "Primary: def (1) or agi (1). Minor bonuses.",
}

local function buildPrompt(itemId)
    local def = Items.get(itemId)
    if not def then return nil end

    local cat = def.category or "unknown"
    local tileLine = string.format("Tile: 16x16 pixel art, row %d, col %d of tileset",
        def.tileRow or 0, def.tileCol or 0)

    local isEquip = Items.isEquippable(itemId)

    if isEquip then
        local hint = CATEGORY_STAT_HINTS[cat] or "Assign 1-2 small stat bonuses as appropriate."
        return string.format(
[[You are a loremaster for a dark fantasy roguelike dungeon crawler.
The world is filled with cursed dungeons, ancient relics, and elemental forces.

Item: "%s" (%s)
%s

Generate a JSON object with these fields:
- "lore": 1-2 sentence backstory (max 80 chars)
- "traits": array of 2-3 physical traits (max 30 chars each)
- "effect": gameplay feel description (max 60 chars, NO numbers)
- "rarity": "Common" | "Uncommon" | "Rare" | "Legendary"
- "stats_atk": integer -2 to +5 (0 if unaffected)
- "stats_def": integer -2 to +5 (0 if unaffected)
- "stats_agi": integer -2 to +5 (0 if unaffected)
- "stats_int": integer -2 to +5 (0 if unaffected)
- "stats_fire": integer -2 to +5 (0 if unaffected)
- "stats_water": integer -2 to +5 (0 if unaffected)
- "stats_grass": integer -2 to +5 (0 if unaffected)
- "stats_elec": integer -2 to +5 (0 if unaffected)
- "stats_ice": integer -2 to +5 (0 if unaffected)
- "stats_poison": integer -2 to +5 (0 if unaffected)
- "stats_earth": integer -2 to +5 (0 if unaffected)
- "stats_wind": integer -2 to +5 (0 if unaffected)

Stat hint for %s: %s

Respond ONLY with a single-line compact JSON (no newlines, no indentation, no markdown). /no_think]],
            def.desc or def.name, cat, tileLine, cat, hint
        )
    else
        return string.format(
[[You are a loremaster for a dark fantasy roguelike dungeon crawler.
The world is filled with cursed dungeons, ancient relics, and elemental forces.

Item: "%s" (%s)
%s

Generate a JSON object with these fields:
- "lore": 1-2 sentence backstory (max 80 chars)
- "traits": array of 2-3 physical traits (max 30 chars each)
- "effect": gameplay feel description (max 60 chars, NO numbers)
- "rarity": "Common" | "Uncommon" | "Rare" | "Legendary"

Respond ONLY with a single-line compact JSON (no newlines, no indentation, no markdown). /no_think]],
            def.desc or def.name, cat, tileLine
        )
    end
end

function AiDescribe.request(itemId)
    -- Already cached or pending
    if cache[itemId] or pending[itemId] then return end

    local prompt = buildPrompt(itemId)
    if not prompt then return end

    pending[itemId] = true
    local request = json.encode({
        itemId = itemId,
        prompt = prompt,
    })
    inputChannel:push(request)
end

function AiDescribe.getResult(itemId)
    if cache[itemId] then
        return cache[itemId]
    end
    if pending[itemId] then
        return "loading"
    end
    return nil
end

function AiDescribe.update()
    -- Check for thread errors
    if thread and not thread:isRunning() then
        local err = thread:getError()
        if err then
            print("[AiDescribe] Worker error: " .. err)
            -- Restart thread
            thread = love.thread.newThread("src/ai_worker.lua")
            thread:start()
            -- Mark all pending as failed with fallback
            for itemId, _ in pairs(pending) do
                cache[itemId] = {
                    lore = "A mysterious item found in the dungeon.",
                    traits = {"Worn from use", "Slightly warm"},
                    effect = "Unknown effect",
                    rarity = "Common",
                    fallback = true,
                }
                pending[itemId] = nil
            end
        end
    end

    -- Poll output channel for results
    while true do
        local raw = outputChannel:pop()
        if not raw then break end

        local ok, data = pcall(json.decode, raw)
        if ok and data and data.itemId then
            cache[data.itemId] = data.result
            pending[data.itemId] = nil
        end
    end
end

function AiDescribe.shutdown()
    if inputChannel then
        inputChannel:push("quit")
    end

    -- Kill server only if we started it
    if serverStartedByUs then
        print("[AiDescribe] Stopping llama-server (started by game)...")
        os.execute("pkill -f 'llama-server.*--port " .. SERVER_PORT .. "'")
        serverStartedByUs = false
    end
end

return AiDescribe
