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

    local enemyGids = {45, 23, 25, 26, 27, 28, 31, 32, 57, 58}
    for i = 1, Config.ENEMY_COUNT do
        if idx > #pool then break end
        local p = pool[idx]; idx = idx + 1
        local e = {
            x=p[1], y=p[2], hp=3, maxHp=3, alive=true,
            gid=enemyGids[love.math.random(1, #enemyGids)],
        }
        Entities.enemies[#Entities.enemies+1] = e
    end
    -- Spawn lootbox containers at map lootbox positions
    Entities.lootboxes = {}
    local lootPositions = Map.getLootboxPositions()
    for _, pos in ipairs(lootPositions) do
        local itemCount = love.math.random(Config.LOOTBOX_MIN_ITEMS, Config.LOOTBOX_MAX_ITEMS)
        local boxItems = {}
        for i = 1, itemCount do
            boxItems[i] = Items.allItemIds[love.math.random(#Items.allItemIds)]
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
    for i, e in ipairs(Entities.enemies) do
        local result = EnemyAI.update(e, i, dt, player, Entities.enemies)
        if result == "hit_player" and damageFlashFn then
            damageFlashFn(player.x, player.y)
        end
    end
end

function Entities.enemyAt(gx, gy)
    for i, e in ipairs(Entities.enemies) do
        if e.alive and e.x == gx and e.y == gy then return i, e end
    end
    return nil
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
        if not lb.looted and lb.x == gx and lb.y == gy then
            return i, lb
        end
    end
    return nil
end

function Entities.drawLootboxes(fov, tileset)
    local TILE = Config.TILE
    local img = tileset.getImage()
    for _, lb in ipairs(Entities.lootboxes) do
        if not lb.looted and fov.isVisible(lb.x, lb.y) then
            local alpha = Map.isOverlayOpaque(lb.x, lb.y) and 0.45 or 1
            love.graphics.setColor(1,1,1,alpha)
            love.graphics.draw(img, tileset.getQuad(lb.gid), (lb.x-1)*TILE, (lb.y-1)*TILE)
            -- Tint: locked=orange, unlocked=green
            if lb.locked then
                love.graphics.setColor(1, 0.5, 0, (0.25 + 0.1*math.sin(love.timer.getTime()*3)) * alpha)
            else
                love.graphics.setColor(0, 1, 0.3, (0.2 + 0.1*math.sin(love.timer.getTime()*3)) * alpha)
            end
            love.graphics.rectangle("fill", (lb.x-1)*TILE, (lb.y-1)*TILE, TILE, TILE)
        end
    end
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
