local Config = require("src.config")
local Map = require("src.map")

local Combat = {}

local projectiles = {}
local damageFlash = {}

function Combat.reset()
    projectiles = {}
    damageFlash = {}
end

function Combat.meleeAttack(player, enemyAtFn)
    local dir = Config.angleTo8Dir(player.aimAngle)
    local tx, ty = player.x+dir[1], player.y+dir[2]
    player.attackTimer = 0.2
    player.attackDir = {dir[1], dir[2]}
    local _, e = enemyAtFn(tx, ty)
    if e then
        e.hp = e.hp - 2
        e.alerted = true
        damageFlash[#damageFlash+1] = {x=tx, y=ty, timer=0.3}
        if e.hp <= 0 then e.alive = false end
    end
end

function Combat.castMagic(player, targetTileX, targetTileY)
    if player.mp < Config.MAGIC_COST then return end
    local tx = math.floor(targetTileX + 0.5)
    local ty = math.floor(targetTileY + 0.5)
    if not Map.inBounds(tx, ty) then return end
    player.mp = player.mp - Config.MAGIC_COST
    projectiles[#projectiles+1] = {
        startX = player.x, startY = player.y,
        targetX = tx, targetY = ty,
        timer = 0, duration = Config.MAGIC_FLY,
        alive = true,
    }
end

function Combat.update(dt, enemyAtFn)
    for _, p in ipairs(projectiles) do
        if p.alive then
            p.timer = p.timer + dt
            if p.timer >= p.duration then
                p.alive = false
                damageFlash[#damageFlash+1] = {x=p.targetX, y=p.targetY, timer=0.3}
                local _, e = enemyAtFn(p.targetX, p.targetY)
                if e then
                    e.hp = e.hp - Config.MAGIC_DMG
                    e.alerted = true
                    if e.hp <= 0 then e.alive = false end
                end
            end
        end
    end
    for i = #projectiles, 1, -1 do
        if not projectiles[i].alive then table.remove(projectiles, i) end
    end
    for i = #damageFlash, 1, -1 do
        damageFlash[i].timer = damageFlash[i].timer - dt
        if damageFlash[i].timer <= 0 then table.remove(damageFlash, i) end
    end
end

function Combat.drawProjectiles()
    local TILE = Config.TILE
    for _, p in ipairs(projectiles) do
        if p.alive then
            local t = p.timer / p.duration
            local cx = p.startX + (p.targetX - p.startX) * t
            local cy = p.startY + (p.targetY - p.startY) * t
            local gx = math.floor(cx + 0.5)
            local gy = math.floor(cy + 0.5)
            if not Map.isOverlayOpaque(gx, gy) then
                local px = (cx - 1) * TILE + TILE/2
                local py = (cy - 1) * TILE + TILE/2
                love.graphics.setColor(0.4, 0.2, 1, 0.4)
                love.graphics.circle("fill", px, py, 5)
                love.graphics.setColor(0.7, 0.4, 1, 1)
                love.graphics.circle("fill", px, py, 3)
            end
        end
    end
end

function Combat.addDamageFlash(x, y)
    damageFlash[#damageFlash+1] = {x=x, y=y, timer=0.3}
end

function Combat.drawEffects()
    local TILE = Config.TILE
    for _, d in ipairs(damageFlash) do
        if not Map.isOverlayOpaque(d.x, d.y) then
            love.graphics.setColor(1,0,0, (d.timer/0.3)*0.5)
            love.graphics.rectangle("fill", (d.x-1)*TILE, (d.y-1)*TILE, TILE, TILE)
        end
    end
end

return Combat
