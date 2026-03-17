-- AI Item Description + Crafting manager (DeepSeek API via ai_worker thread)

local json = require("libs.json")
local Items = require("src.items")

local AiDescribe = {}

local cache = {}
local pending = {}
local thread = nil
local inputChannel = nil
local outputChannel = nil

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

local function ensureThread()
    if thread and thread:isRunning() then return true end

    inputChannel = love.thread.getChannel("ai_input")
    outputChannel = love.thread.getChannel("ai_output")
    while inputChannel:pop() do end
    while outputChannel:pop() do end

    thread = love.thread.newThread("src/ai_worker.lua")
    thread:start()
    return true
end

function AiDescribe.init()
    cache = {}
    pending = {}
    ensureThread()
end

local function buildPrompt(itemId)
    local def = Items.get(itemId)
    if not def then return nil end

    local cat = def.category or "unknown"
    local tileLine = string.format("Tile: 16x16 pixel art, row %d, col %d of tileset", def.tileRow or 0, def.tileCol or 0)
    local isEquip = Items.isEquippable(itemId)

    if isEquip then
        local hint = CATEGORY_STAT_HINTS[cat] or "Assign 1-2 small stat bonuses as appropriate."
        return string.format(
[[You are a loremaster for a dark fantasy roguelike dungeon crawler.
Item: "%s" (%s)
%s
Generate JSON with keys: lore, traits[], effect, rarity, stats_atk, stats_def, stats_agi, stats_int, stats_fire, stats_water, stats_grass, stats_elec, stats_ice, stats_poison, stats_earth, stats_wind.
Ranges: each stat integer -2..+5.
Stat hint for %s: %s
Return ONLY compact one-line JSON.]],
            def.desc or def.name, cat, tileLine, cat, hint
        )
    else
        return string.format(
[[You are a loremaster for a dark fantasy roguelike dungeon crawler.
Item: "%s" (%s)
%s
Generate JSON with keys: lore, traits[], effect, rarity.
Return ONLY compact one-line JSON.]],
            def.desc or def.name, cat, tileLine
        )
    end
end

function AiDescribe.request(itemId)
    if cache[itemId] or pending[itemId] then return end
    if not ensureThread() then return end

    local prompt = buildPrompt(itemId)
    if not prompt then return end

    pending[itemId] = true
    inputChannel:push(json.encode({ mode = "describe", itemId = itemId, prompt = prompt }))
end

function AiDescribe.getResult(itemId)
    if cache[itemId] then return cache[itemId] end
    if pending[itemId] then return "loading" end
    return nil
end

local function generateRequestId(prefix)
    return string.format("%s_%d_%04d", prefix, os.time(), love.math.random(1000, 9999))
end

local function awaitSyncResponse(requestId, timeoutSec)
    local timeout = timeoutSec or 6
    local start = love.timer.getTime()

    while love.timer.getTime() - start < timeout do
        local raw = outputChannel:pop()
        if raw then
            local ok, data = pcall(json.decode, raw)
            if ok and data then
                if data.requestId and data.requestId == requestId then
                    return data.result
                elseif data.itemId then
                    cache[data.itemId] = data.result
                    pending[data.itemId] = nil
                end
            end
        else
            love.timer.sleep(0.03)
        end
    end

    return { fallback = true, error = "sync_timeout" }
end

local SPECIAL_ECONOMY_ITEM_IDS = {
    builder_scroll = true,
}

local function pickItemByCategory(category, opts)
    opts = opts or {}
    local ids = Items.getIdsByCategory(category)
    if not ids or #ids == 0 then return nil end

    local filtered = {}
    local maxSize = tonumber(opts.maxSize)
    local minSize = tonumber(opts.minSize)
    for _, iid in ipairs(ids) do
        if not SPECIAL_ECONOMY_ITEM_IDS[iid] or opts.includeSpecial then
            local d = Items.get(iid)
            local size = (d and d.size) or 1
            local okMax = (not maxSize) or size <= maxSize
            local okMin = (not minSize) or size >= minSize
            if okMax and okMin then
                filtered[#filtered + 1] = iid
            end
        end
    end

    local pool = (#filtered > 0) and filtered or ids
    if not opts.includeSpecial and #filtered == 0 then
        return nil
    end
    return pool[love.math.random(1, #pool)]
end

function AiDescribe.generateDisassembly(itemId)
    if not ensureThread() then return {} end
    local def = Items.get(itemId)
    if not def then return {} end

    local prompt = string.format(
[[Game context: dark fantasy + DOS-like inventory UI.
Task: Disassemble one item into salvage materials.
Input item category: %s
Input item name: %s
Return strict JSON:
{"outputs":[{"category":"gem|scroll|tool|bone|skull|coin|potion|misc","count":1-2}, ...], "note":"short text"}
Rules: exactly 1-2 output rows, total count 1-3, no rare jackpots, make thematic sense, keep output low-tier for simple inputs, and never output builder scroll equivalents.]],
        def.category or "misc", def.name or "UNKNOWN"
    )

    local req = generateRequestId("dis")
    inputChannel:push(json.encode({ mode = "disassemble", requestId = req, prompt = prompt }))
    local result = awaitSyncResponse(req, 6)

    local outputs = {}
    local itemSize = tonumber(def.size) or 1
    local maxOutSize = math.max(1, itemSize - 1)

    -- Balance pass: disassembly should be a convenience path, not a free size multiplier.
    -- Use both a stack-count cap and a total salvage-size budget.
    -- Tightened to keep medium/high-tier loops SRL-negative unless the player mixes in fresh drops.
    local salvageStackCap = math.max(1, math.min(2, math.ceil(itemSize / 4)))
    local salvageSizeBudget = math.max(1, math.floor(itemSize * 0.50))
    local remainingStacks = salvageStackCap
    local remainingSize = salvageSizeBudget

    if result and type(result.outputs) == "table" then
        for _, row in ipairs(result.outputs) do
            if remainingStacks <= 0 or remainingSize <= 0 or #outputs >= 2 then break end
            local cat = tostring(row.category or "misc")
            local wanted = math.max(1, math.min(2, tonumber(row.count) or 1))

            local outId = pickItemByCategory(cat, { maxSize = math.min(maxOutSize, remainingSize) })
                or pickItemByCategory("misc", { maxSize = math.min(maxOutSize, remainingSize) })

            if outId then
                local outDef = Items.get(outId) or {}
                local outSize = math.max(1, tonumber(outDef.size) or 1)
                local sizeLimited = math.floor(remainingSize / outSize)
                local cnt = math.min(wanted, remainingStacks, math.max(0, sizeLimited))

                if cnt > 0 then
                    table.insert(outputs, { itemId = outId, count = cnt })
                    remainingStacks = remainingStacks - cnt
                    remainingSize = remainingSize - (outSize * cnt)
                end
            end
        end
    end

    if #outputs == 0 then
        local fallbackId = pickItemByCategory("misc", { maxSize = math.min(maxOutSize, remainingSize) })
        if fallbackId then
            outputs = {{ itemId = fallbackId, count = 1 }}
        end
    end

    return outputs, (result and result.note) or "Recovered salvage"
end

function AiDescribe.generateBuild(folderName, componentIds)
    if not ensureThread() then return nil, "AI unavailable" end

    local cats = {}
    local totalSize = 0
    local maxSize = 1
    for _, iid in ipairs(componentIds) do
        local d = Items.get(iid)
        if d then
            cats[#cats + 1] = d.category or "misc"
            local s = tonumber(d.size) or 1
            totalSize = totalSize + s
            if s > maxSize then maxSize = s end
        end
    end

    local componentCount = math.max(1, #componentIds)
    local avgSize = totalSize / componentCount
    local buildCeil = math.max(1, math.min(3, math.ceil(avgSize)))
    local buildFloor = math.max(1, math.min(buildCeil, math.floor(avgSize)))

    local prompt = string.format(
[[Game context: dark fantasy roguelike with DOS build metaphor.
Task: Synthesize ONE new item from folder components.
Folder: %s
Component categories: %s
Power budget: avg component size %.2f (output size must stay in this range)
Return strict JSON: {"target_category":"weapon|armor|ring|wand|scroll|tool|gem|potion|misc", "rarity_hint":"Common|Uncommon|Rare|Legendary", "note":"short text"}
Choose category that matches component synergy and keep result grounded to component quality. Never return build-enabler items.]],
        folderName or "PROJECT", table.concat(cats, ","), avgSize
    )

    local req = generateRequestId("bld")
    inputChannel:push(json.encode({ mode = "build", requestId = req, prompt = prompt }))
    local result = awaitSyncResponse(req, 6)

    local target = (result and result.target_category) or "misc"
    local itemId = pickItemByCategory(target, { minSize = buildFloor, maxSize = buildCeil })
        or pickItemByCategory(target, { maxSize = math.max(maxSize, buildCeil) })
        or pickItemByCategory("misc", { maxSize = math.max(maxSize, buildCeil) })
        or pickItemByCategory("misc")
    return itemId, ((result and result.note) or "Build complete")
end

function AiDescribe.update()
    if not thread then return end
    if not thread:isRunning() then
        local err = thread:getError()
        if err then print("[AiDescribe] Worker error: " .. err) end
        ensureThread()
    end

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
    if inputChannel then inputChannel:push("quit") end
end

return AiDescribe
