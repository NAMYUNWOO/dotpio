local Config = require("src.config")
local Map = require("src.map")
local Stats = require("src.stats")

local Combat = {}

local projectiles = {}
local damageFlash = {}
local damageNumbers = {}
local killCount = 0

local DMGNUM_DURATION = 0.6
local DMGNUM_RISE = 12  -- pixels to float upward
local DMGNUM_STACK_CAP = 8  -- DMGNUM STACK CAP: max concurrent floating numbers

local function isDamageGlyphBurstExperimentEnabled()
    local v = os.getenv("DOTPIO_EXPERIMENT_DAMAGE_GLYPH_BURST")
    if not v then return false end
    v = string.lower(v)
    return v == "1" or v == "true" or v == "yes" or v == "on"
end

local function damageGlyphBandFromAmount(amount, lethal)
    local dmg = tonumber(amount) or 0
    if lethal and dmg >= 4 then
        return "OVERDRIVE"
    end
    if dmg >= 8 then
        return "OVERDRIVE"
    elseif dmg >= 4 then
        return "SPIKE"
    end
    return "BASIC"
end

local function damageGlyphVisualFromBand(band)
    if band == "OVERDRIVE" then return "✹" end
    if band == "SPIKE" then return "✦" end
    return "·"
end

local function pushDamageNumber(entry)
    damageNumbers[#damageNumbers + 1] = entry
    while #damageNumbers > DMGNUM_STACK_CAP do
        table.remove(damageNumbers, 1)
    end
end

function Combat.reset()
    projectiles = {}
    damageFlash = {}
    damageNumbers = {}
    killCount = 0
end

function Combat.meleeAttack(player, enemyAtFn)
    local dir = Config.angleTo8Dir(player.aimAngle)
    local tx, ty = player.x+dir[1], player.y+dir[2]
    player.attackTimer = 0.2
    player.attackDir = {dir[1], dir[2]}
    local _, e = enemyAtFn(tx, ty)
    if e then
        local dmg = Stats.meleeDamage(2, player.effectiveStats)
        local finalDmg = math.max(1, math.floor(dmg + 0.5))
        e.hp = e.hp - finalDmg
        e.alerted = true
        local lethal = e.hp <= 0 and e.alive
        local glyphBand = damageGlyphBandFromAmount(finalDmg, lethal)
        damageFlash[#damageFlash+1] = {x=tx, y=ty, timer=0.3}
        pushDamageNumber({x=tx, y=ty, amount=finalDmg, timer=DMGNUM_DURATION, magic=false, lethal=lethal, glyphBand=glyphBand})
        if lethal then
            e.alive = false
            e.deathTimer = 0.4
            killCount = killCount + 1
        end
    end
end

function Combat.castMagic(player, targetTileX, targetTileY)
    Combat._playerRef = player
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
                    local dmg = Stats.magicDamage(Config.MAGIC_DMG, Combat._playerRef and Combat._playerRef.effectiveStats or {int = 3})
                    local finalDmg = math.max(1, math.floor(dmg + 0.5))
                    e.hp = e.hp - finalDmg
                    e.alerted = true
                    local lethal = e.hp <= 0 and e.alive
                    local glyphBand = damageGlyphBandFromAmount(finalDmg, lethal)
                    pushDamageNumber({x=p.targetX, y=p.targetY, amount=finalDmg, timer=DMGNUM_DURATION, magic=true, lethal=lethal, glyphBand=glyphBand})
                    if lethal then
                        e.alive = false
                        e.deathTimer = 0.4
                        killCount = killCount + 1
                    end
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
    for i = #damageNumbers, 1, -1 do
        damageNumbers[i].timer = damageNumbers[i].timer - dt
        if damageNumbers[i].timer <= 0 then table.remove(damageNumbers, i) end
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

    for _, n in ipairs(damageNumbers) do
        if not Map.isOverlayOpaque(n.x, n.y) then
            local progress = 1 - math.max(0, math.min(1, n.timer / DMGNUM_DURATION))
            local alpha = 1 - progress
            local px = (n.x - 1) * TILE + TILE * 0.5
            local py = (n.y - 1) * TILE + TILE * 0.28 - (progress * DMGNUM_RISE)
            local label = tostring(n.amount)
            if n.magic then
                love.graphics.setColor(0.72, 0.58, 1.0, alpha)
            else
                love.graphics.setColor(1.0, 0.86, 0.38, alpha)
            end
            if n.lethal then
                label = label .. "!"
                love.graphics.setColor(1.0, 0.35, 0.35, alpha)
            end
            if isDamageGlyphBurstExperimentEnabled() then
                local glyphBand = n.glyphBand or damageGlyphBandFromAmount(n.amount, n.lethal == true)
                local glyph = damageGlyphVisualFromBand(glyphBand)
                label = string.format("%s %s", label, glyph)
            end
            love.graphics.printf(label, px - TILE * 0.5, py, TILE, "center")
        end
    end
end

function Combat.consumeKillCount()
    local n = killCount
    killCount = 0
    return n
end

function Combat.debugGetDamageNumbers()
    local out = {}
    for i = 1, #damageNumbers do
        local n = damageNumbers[i]
        out[#out + 1] = {
            x = n.x,
            y = n.y,
            amount = n.amount,
            timer = n.timer,
            magic = n.magic == true,
            lethal = n.lethal == true,
            glyphBand = n.glyphBand,
        }
    end
    return out
end

function Combat.debugGetDamageNumberStackCap()
    return DMGNUM_STACK_CAP
end

return Combat
