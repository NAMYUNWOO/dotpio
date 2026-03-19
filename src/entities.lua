local Config = require("src.config")
local Map = require("src.map")
local EnemyAI = require("src.enemy_ai")
local Items = require("src.items")

local Entities = {}

Entities.enemies = {}
Entities.items = {}
Entities.lootboxes = {}

function Entities.reset()
    Entities.enemies = {}
    Entities.items = {}
    Entities.lootboxes = {}
end

local LOOT_REWARD_PROFILES = {
    [1] = {
        { category = "potion", weight = 22 },
        { category = "food", weight = 20 },
        { category = "scroll", weight = 16 },
        { category = "coin", weight = 14 },
        { category = "torch", weight = 8 },
        { category = "key", weight = 8 },
        { category = "misc", weight = 6 },
        { category = "bone", weight = 4 },
        { category = "skull", weight = 2 },
    },
    [2] = {
        { category = "potion", weight = 16 },
        { category = "food", weight = 12 },
        { category = "scroll", weight = 14 },
        { category = "coin", weight = 10 },
        { category = "weapon", weight = 9 },
        { category = "armor", weight = 8 },
        { category = "shield", weight = 6 },
        { category = "boots", weight = 5 },
        { category = "gloves", weight = 5 },
        { category = "wand", weight = 5 },
        { category = "bow", weight = 5 },
        { category = "gem", weight = 5 },
    },
    [3] = {
        { category = "weapon", weight = 14 },
        { category = "armor", weight = 12 },
        { category = "shield", weight = 8 },
        { category = "wand", weight = 8 },
        { category = "bow", weight = 8 },
        { category = "ring", weight = 7 },
        { category = "necklace", weight = 7 },
        { category = "gem", weight = 7 },
        { category = "book", weight = 6 },
        { category = "crown", weight = 4 },
        { category = "scroll", weight = 8 },
        { category = "potion", weight = 6 },
        { category = "coin", weight = 5 },
    },
}

local function mapTier(mapName)
    local mapNumber = tonumber(mapName or "1") or 1
    if mapNumber <= 2 then return 1 end
    if mapNumber <= 4 then return 2 end
    return 3
end

local function buildCategoryPools()
    local pools = {}
    for _, itemId in ipairs(Items.allItemIds) do
        local def = Items.get(itemId)
        if def and not def.isSystem then
            pools[def.category] = pools[def.category] or {}
            pools[def.category][#pools[def.category] + 1] = itemId
        end
    end
    return pools
end

local function pickWeightedCategory(profile)
    local totalWeight = 0
    for _, entry in ipairs(profile) do
        totalWeight = totalWeight + (entry.weight or 0)
    end
    if totalWeight <= 0 then return nil end

    local roll = love.math.random() * totalWeight
    local acc = 0
    for _, entry in ipairs(profile) do
        acc = acc + (entry.weight or 0)
        if roll <= acc then
            return entry.category
        end
    end
    return profile[#profile] and profile[#profile].category or nil
end

local function pickLootItemIdForTier(tier, categoryPools)
    local profile = LOOT_REWARD_PROFILES[tier] or LOOT_REWARD_PROFILES[1]
    local category = pickWeightedCategory(profile)
    local pool = category and categoryPools[category] or nil
    if pool and #pool > 0 then
        return pool[love.math.random(1, #pool)]
    end

    -- Fallback: any non-system item.
    local fallback = {}
    for _, catPool in pairs(categoryPools) do
        for i = 1, #catPool do
            fallback[#fallback + 1] = catPool[i]
        end
    end
    if #fallback == 0 then return nil end
    return fallback[love.math.random(1, #fallback)]
end

function Entities.spawn(player, skipPlayerPlace)
    Entities.enemies = {}
    Entities.items = {}

    local interior, fallback = {}, {}
    for y = 2, Map.height-1 do
        for x = 2, Map.width-1 do
            if Map.isWalkable(x,y) then
                if Map.isWalkable(x-1,y) and Map.isWalkable(x+1,y) and Map.isWalkable(x,y-1) and Map.isWalkable(x,y+1) then
                    interior[#interior+1] = {x,y}
                else
                    fallback[#fallback+1] = {x,y}
                end
            end
        end
    end
    local pool = #interior > 0 and interior or fallback
    if #pool == 0 then return end

    for i = #pool, 2, -1 do
        local j = love.math.random(1, i)
        pool[i], pool[j] = pool[j], pool[i]
    end

    local idx
    if skipPlayerPlace then
        idx = 1
    else
        player.x, player.y = pool[1][1], pool[1][2]
        idx = 2
    end

    local enemyVariants = {
        { name = "raider", chance = 0.27, hp = 3, gidPool = {45, 23, 25, 26} },
        { name = "skirmisher", chance = 0.18, hp = 2, gidPool = {27, 28, 31} },
        { name = "bruiser", chance = 0.17, hp = 5, gidPool = {57, 58} },
        { name = "sentinel", chance = 0.10, hp = 4, gidPool = {32, 45} },
        { name = "warcaller", chance = 0.11, hp = 4, gidPool = {43, 44, 46} },
        { name = "hunter", chance = 0.09, hp = 3, gidPool = {29, 30, 33} },
        { name = "berserker", chance = 0.08, hp = 4, gidPool = {57, 58, 29} },
    }

    local encounterProfile = (Map.metadata and Map.metadata.encounterProfile) or {}
    local variantBias = encounterProfile.variantBias or {}
    local totalChance = 0
    for _, variant in ipairs(enemyVariants) do
        variant.adjustedChance = variant.chance * (variantBias[variant.name] or 1)
        totalChance = totalChance + variant.adjustedChance
    end

    if totalChance <= 0 then
        totalChance = 1
        for _, variant in ipairs(enemyVariants) do
            variant.adjustedChance = 1 / #enemyVariants
        end
    end

    local function pickVariant()
        local roll = love.math.random() * totalChance
        local acc = 0
        for _, variant in ipairs(enemyVariants) do
            acc = acc + variant.adjustedChance
            if roll <= acc then return variant end
        end
        return enemyVariants[1]
    end

    local enemyCount = Config.ENEMY_COUNT
    local countMultiplier = tonumber(encounterProfile.enemyCountMultiplier)
    if countMultiplier and countMultiplier > 0 then
        enemyCount = math.max(1, math.floor(enemyCount * countMultiplier + 0.5))
    end

    for i = 1, enemyCount do
        if idx > #pool then break end
        local p = pool[idx]; idx = idx + 1
        local variant = pickVariant()
        local hp = variant.hp
        local gidPool = variant.gidPool
        local e = {
            x=p[1], y=p[2], hp=hp, maxHp=hp, alive=true,
            behavior = variant.name,
            gid=gidPool[love.math.random(1, #gidPool)],
        }
        Entities.enemies[#Entities.enemies+1] = e
    end
    -- Spawn lootbox containers at map lootbox positions
    Entities.lootboxes = {}
    local lootPositions = Map.getLootboxPositions()
    local tier = mapTier(Map.currentMap)
    local categoryPools = buildCategoryPools()
    for _, pos in ipairs(lootPositions) do
        local itemCount = love.math.random(Config.LOOTBOX_MIN_ITEMS, Config.LOOTBOX_MAX_ITEMS)
        local boxItems = {}
        for i = 1, itemCount do
            local itemId = pickLootItemIdForTier(tier, categoryPools)
            if itemId then
                boxItems[#boxItems + 1] = itemId
            end
        end
        Entities.lootboxes[#Entities.lootboxes+1] = {
            x = pos[1], y = pos[2],
            looted = false,
            locked = love.math.random() < Config.LOOTBOX_LOCKED_CHANCE,
            items = boxItems,
            gid = Config.LOOTBOX_GID,
        }
    end

    -- Build pathfinding grid and init AI for each enemy
    EnemyAI.buildGrid()
    for i, e in ipairs(Entities.enemies) do
        EnemyAI.init(e, i)
    end
end

function Entities.update(dt, player, damageFlashFn)
    local events = { hits = 0, berserkerLungeTelegraphs = 0 }
    for i, e in ipairs(Entities.enemies) do
        local result = EnemyAI.update(e, i, dt, player, Entities.enemies)
        if result == "hit_player" then
            events.hits = events.hits + 1
            if damageFlashFn then
                damageFlashFn(player.x, player.y)
            end
        elseif result == "berserker_lunge_telegraph" then
            events.berserkerLungeTelegraphs = events.berserkerLungeTelegraphs + 1
        end
    end
    return events
end

function Entities.enemyAt(gx, gy)
    for i, e in ipairs(Entities.enemies) do
        if e.alive and e.x == gx and e.y == gy then return i, e end
    end
    return nil
end

function Entities.itemAt(gx, gy)
    for i, it in ipairs(Entities.items) do
        if not it.collected and it.x == gx and it.y == gy then
            return i, it
        end
    end
    return nil
end

function Entities.removeItem(index)
    if index and index >= 1 and index <= #Entities.items then
        table.remove(Entities.items, index)
    end
end

function Entities.drawEnemies(fov, tileset)
    local TILE = Config.TILE
    local img = tileset.getImage()
    for _, e in ipairs(Entities.enemies) do
        if e.alive and fov.isVisible(e.x, e.y) then
            local vx, vy = e.visualX or e.x, e.visualY or e.y
            local alpha = Map.isOverlayOpaque(e.x, e.y) and 0.45 or 1
            love.graphics.setColor(1,1,1,alpha)
            love.graphics.draw(img, tileset.getQuad(e.gid), (vx-1)*TILE, (vy-1)*TILE)
            local bx, by = (vx-1)*TILE, (vy-1)*TILE - 3
            love.graphics.setColor(0.3,0,0,alpha)
            love.graphics.rectangle("fill", bx, by, TILE, 2)
            love.graphics.setColor(1,0,0,alpha)
            love.graphics.rectangle("fill", bx, by, TILE*(e.hp/e.maxHp), 2)
        end
    end
end

function Entities.lootboxAt(gx, gy)
    for i, lb in ipairs(Entities.lootboxes) do
        if lb.x == gx and lb.y == gy then
            return i, lb
        end
    end
    return nil
end

function Entities.drawLootboxes(fov, tileset)
    local TILE = Config.TILE
    local img = tileset.getImage()
    for _, lb in ipairs(Entities.lootboxes) do
        if fov.isVisible(lb.x, lb.y) then
            local alpha = Map.isOverlayOpaque(lb.x, lb.y) and 0.45 or 1
            love.graphics.setColor(1,1,1,alpha)
            love.graphics.draw(img, tileset.getQuad(lb.gid), (lb.x-1)*TILE, (lb.y-1)*TILE)
            -- Tint: locked=orange, unlocked=green, empty=gray
            if #lb.items == 0 then
                love.graphics.setColor(0.5, 0.5, 0.5, 0.3 * alpha)
            elseif lb.locked then
                love.graphics.setColor(1, 0.5, 0, (0.25 + 0.1*math.sin(love.timer.getTime()*3)) * alpha)
            else
                love.graphics.setColor(0, 1, 0.3, (0.2 + 0.1*math.sin(love.timer.getTime()*3)) * alpha)
            end
            love.graphics.rectangle("fill", (lb.x-1)*TILE, (lb.y-1)*TILE, TILE, TILE)
        end
    end
end

function Entities.getEnemyBehaviorVariants()
    return { "raider", "skirmisher", "bruiser", "sentinel", "warcaller", "hunter", "berserker" }
end

function Entities.debugSampleLootboxItems(mapName, samples)
    local tier = mapTier(mapName)
    local categoryPools = buildCategoryPools()
    local out = {}
    local n = samples or 100
    for i = 1, n do
        local itemId = pickLootItemIdForTier(tier, categoryPools)
        if itemId then out[#out + 1] = itemId end
    end
    return out, tier
end

function Entities.drawItems(fov, tileset)
    local TILE = Config.TILE
    local img = tileset.getImage()
    for _, it in ipairs(Entities.items) do
        if not it.collected and fov.isVisible(it.x, it.y) then
            local alpha = Map.isOverlayOpaque(it.x, it.y) and 0.45 or 1
            love.graphics.setColor(1,1,1,alpha)
            love.graphics.draw(img, tileset.getQuad(it.gid), (it.x-1)*TILE, (it.y-1)*TILE)
            love.graphics.setColor(1,1,0, (0.3 + 0.15*math.sin(love.timer.getTime()*4)) * alpha)
            love.graphics.rectangle("fill", (it.x-1)*TILE, (it.y-1)*TILE, TILE, TILE)
        end
    end
end

return Entities
