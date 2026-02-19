local Config = require("src.config")
local Map = require("src.map")
local EnemyAI = require("src.enemy_ai")

local Entities = {}

Entities.enemies = {}
Entities.items = {}

function Entities.reset()
    Entities.enemies = {}
    Entities.items = {}
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
    for i = 1, Config.ITEM_COUNT do
        if idx > #pool then break end
        local p = pool[idx]; idx = idx + 1
        Entities.items[#Entities.items+1] = {
            x=p[1], y=p[2], collected=false,
            gid=Config.MP_ITEM_GID,
            mpRestore=love.math.random(5, 10),
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
