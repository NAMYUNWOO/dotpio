-- Top-down Roguelike with Fan-shaped FOV System
-- Layered map: Ground → GroundDeco → Collision → Player → Overlay

local mapData = dofile("map_data.lua")

------------------------------------------------------------
-- CONSTANTS
------------------------------------------------------------
local TILE     = 16
local SCALE    = 3
local TS_COLS  = 32
local TS_SIZE  = 543
local FOV_HALF = math.pi / 4
local FOV_RANGE = 10
local MOVE_CD  = 0.12
local MAGIC_COST   = 2    -- MP per cast
local MAGIC_DMG    = 2    -- damage per hit
local MAGIC_FLY    = 0.15 -- travel time to target (seconds)
local ENEMY_COUNT  = 8
local ITEM_COUNT   = 6
local MP_ITEM_GID  = 817  -- mana potion tile (Tiled ID 816 + 1)

local DIR8 = {
    {1,0},{1,1},{0,1},{-1,1},{-1,0},{-1,-1},{0,-1},{1,-1},
}

-- Tiled flip flags
local FLIP_H = 0x80000000
local FLIP_V = 0x40000000
local FLIP_D = 0x20000000

------------------------------------------------------------
-- GID DECODING (Tiled flip flags → Love2D transform)
------------------------------------------------------------
local function decodeGid(raw)
    if raw == 0 then return 0, 0, 1, 1 end
    local fh, fv, fd = false, false, false
    if raw >= FLIP_H then raw = raw - FLIP_H; fh = true end
    if raw >= FLIP_V then raw = raw - FLIP_V; fv = true end
    if raw >= FLIP_D then raw = raw - FLIP_D; fd = true end
    local r, sx, sy = 0, 1, 1
    if fd then
        if fh and fv then r = math.pi/2; sx = -1
        elseif fh then r = math.pi/2
        elseif fv then r = -math.pi/2
        else r = math.pi/2; sy = -1
        end
    else
        if fh then sx = -1 end
        if fv then sy = -1 end
    end
    return raw, r, sx, sy
end

------------------------------------------------------------
-- GAME STATE
------------------------------------------------------------
local tileset, quads
local camera = {x = 0, y = 0}
local player = {
    x = 0, y = 0, aimAngle = 0,
    moveTimer = 0,
    hp = 10, maxHp = 10,
    mp = 20, maxMp = 20,
    attackTimer = 0, attackDir = nil,
}
local enemies = {}
local items = {}
local projectiles = {}
local fovSet = {}
local damageFlash = {}

------------------------------------------------------------
-- TILE HELPERS (layer-based)
------------------------------------------------------------
local function inBounds(gx, gy)
    return gx >= 1 and gy >= 1 and gx <= mapData.width and gy <= mapData.height
end

local function isBlocked(gx, gy)
    if not inBounds(gx, gy) then return true end
    return mapData.Collision[gy][gx] ~= 0
end

local function isOpaque(gx, gy)
    if not inBounds(gx, gy) then return true end
    return mapData.Collision[gy][gx] ~= 0
end

local function isWalkable(gx, gy)
    return inBounds(gx, gy) and not isBlocked(gx, gy)
end

local function enemyAt(gx, gy)
    for i, e in ipairs(enemies) do
        if e.alive and e.x == gx and e.y == gy then return i, e end
    end
    return nil
end

------------------------------------------------------------
-- FOV SYSTEM
------------------------------------------------------------
local function normalizeAngle(a)
    while a > math.pi do a = a - 2*math.pi end
    while a < -math.pi do a = a + 2*math.pi end
    return a
end

local function hasLOS(x1, y1, x2, y2)
    local dx, dy = x2-x1, y2-y1
    local steps = math.max(math.abs(dx), math.abs(dy))
    if steps == 0 then return true end
    local xi, yi = dx/steps, dy/steps
    local cx, cy = x1+0.0, y1+0.0
    for _ = 1, steps-1 do
        cx, cy = cx+xi, cy+yi
        if isOpaque(math.floor(cx+0.5), math.floor(cy+0.5)) then return false end
    end
    return true
end

local function calculateFOV()
    fovSet = {}
    local px, py = player.x, player.y
    for dy = -FOV_RANGE, FOV_RANGE do
        for dx = -FOV_RANGE, FOV_RANGE do
            local tx, ty = px+dx, py+dy
            if inBounds(tx, ty) then
                local dist = math.sqrt(dx*dx + dy*dy)
                if dist <= FOV_RANGE then
                    if dist <= 1.5 then
                        fovSet[tx..","..ty] = true
                    else
                        local diff = normalizeAngle(math.atan2(dy,dx) - player.aimAngle)
                        if math.abs(diff) <= FOV_HALF and hasLOS(px,py,tx,ty) then
                            fovSet[tx..","..ty] = true
                        end
                    end
                end
            end
        end
    end
end

local function isInFOV(gx, gy)
    return fovSet[gx..","..gy] == true
end

------------------------------------------------------------
-- DIRECTION
------------------------------------------------------------
local function angleTo8Dir(angle)
    return DIR8[math.floor((angle + math.pi/8) / (math.pi/4)) % 8 + 1]
end

------------------------------------------------------------
-- SPAWNING
------------------------------------------------------------
local function spawnEntities()
    -- Find walkable interior tiles
    local interior, fallback = {}, {}
    for y = 2, mapData.height-1 do
        for x = 2, mapData.width-1 do
            if isWalkable(x,y) then
                if isWalkable(x-1,y) and isWalkable(x+1,y) and isWalkable(x,y-1) and isWalkable(x,y+1) then
                    interior[#interior+1] = {x,y}
                else
                    fallback[#fallback+1] = {x,y}
                end
            end
        end
    end
    local pool = #interior > 0 and interior or fallback
    if #pool == 0 then return end

    -- Shuffle
    for i = #pool, 2, -1 do
        local j = love.math.random(1, i)
        pool[i], pool[j] = pool[j], pool[i]
    end

    player.x, player.y = pool[1][1], pool[1][2]

    local enemyGids = {45, 23, 25, 26, 27, 28, 31, 32, 57, 58}

    local idx = 2
    for i = 1, ENEMY_COUNT do
        if idx > #pool then break end
        local p = pool[idx]; idx = idx + 1
        enemies[#enemies+1] = {
            x=p[1], y=p[2], hp=3, maxHp=3, alive=true,
            gid=enemyGids[love.math.random(1, #enemyGids)],
        }
    end
    for i = 1, ITEM_COUNT do
        if idx > #pool then break end
        local p = pool[idx]; idx = idx + 1
        items[#items+1] = {
            x=p[1], y=p[2], collected=false,
            gid=MP_ITEM_GID,
            mpRestore=love.math.random(5, 10),
        }
    end
end

------------------------------------------------------------
-- COMBAT
------------------------------------------------------------
local function meleeAttack()
    local dir = angleTo8Dir(player.aimAngle)
    local tx, ty = player.x+dir[1], player.y+dir[2]
    player.attackTimer = 0.2
    player.attackDir = {dir[1], dir[2]}
    local _, e = enemyAt(tx, ty)
    if e then
        e.hp = e.hp - 2
        damageFlash[#damageFlash+1] = {x=tx, y=ty, timer=0.3}
        if e.hp <= 0 then e.alive = false end
    end
end

local function castMagic(targetTileX, targetTileY)
    if player.mp < MAGIC_COST then return end
    local tx = math.floor(targetTileX + 0.5)
    local ty = math.floor(targetTileY + 0.5)
    if not inBounds(tx, ty) then return end
    player.mp = player.mp - MAGIC_COST

    -- Projectile flies from player to target then explodes
    local dx, dy = tx - player.x, ty - player.y
    projectiles[#projectiles+1] = {
        startX = player.x, startY = player.y,
        targetX = tx, targetY = ty,
        timer = 0, duration = MAGIC_FLY,
        alive = true,
    }
end

------------------------------------------------------------
-- LOVE CALLBACKS
------------------------------------------------------------
function love.load()
    love.graphics.setDefaultFilter("nearest", "nearest")
    tileset = love.graphics.newImage("kenny1bit/Tilemap/tileset_legacy_transparent.png")
    quads = {}
    for gid = 1, 1024 do
        local row = math.floor((gid-1) / TS_COLS)
        local col = (gid-1) % TS_COLS
        quads[gid] = love.graphics.newQuad(col*17, row*17, TILE, TILE, TS_SIZE, TS_SIZE)
    end
    spawnEntities()
    calculateFOV()
end

function love.update(dt)
    player.moveTimer = math.max(0, player.moveTimer - dt)
    player.attackTimer = math.max(0, player.attackTimer - dt)
    if player.attackTimer <= 0 then player.attackDir = nil end

    -- WASD
    if player.moveTimer <= 0 then
        local dx, dy = 0, 0
        if love.keyboard.isDown("w","up")    then dy = dy-1 end
        if love.keyboard.isDown("s","down")  then dy = dy+1 end
        if love.keyboard.isDown("a","left")  then dx = dx-1 end
        if love.keyboard.isDown("d","right") then dx = dx+1 end
        if dx ~= 0 or dy ~= 0 then
            local nx, ny = player.x+dx, player.y+dy
            local moved = false
            if isWalkable(nx, ny) then
                player.x, player.y = nx, ny; moved = true
            elseif dx ~= 0 and dy ~= 0 then
                if isWalkable(player.x+dx, player.y) then
                    player.x = player.x+dx; moved = true
                elseif isWalkable(player.x, player.y+dy) then
                    player.y = player.y+dy; moved = true
                end
            end
            if moved then
                player.moveTimer = MOVE_CD
                for _, it in ipairs(items) do
                    if not it.collected and it.x == player.x and it.y == player.y then
                        it.collected = true
                        player.mp = math.min(player.maxMp, player.mp + it.mpRestore)
                    end
                end
            end
        end
    end

    -- Mouse aim
    local mx, my = love.mouse.getPosition()
    local wx = (mx + camera.x) / (TILE*SCALE) + 0.5
    local wy = (my + camera.y) / (TILE*SCALE) + 0.5
    player.aimAngle = math.atan2(wy - player.y, wx - player.x)
    calculateFOV()

    -- Magic projectiles (fly to target then hit)
    for _, p in ipairs(projectiles) do
        if p.alive then
            p.timer = p.timer + dt
            if p.timer >= p.duration then
                -- Arrived at target: deal damage
                p.alive = false
                damageFlash[#damageFlash+1] = {x=p.targetX, y=p.targetY, timer=0.3}
                local _, e = enemyAt(p.targetX, p.targetY)
                if e then
                    e.hp = e.hp - MAGIC_DMG
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

    -- Camera
    local sw, sh = love.graphics.getWidth(), love.graphics.getHeight()
    camera.x = player.x * TILE*SCALE - sw/2
    camera.y = player.y * TILE*SCALE - sh/2
    camera.x = math.max(0, math.min(camera.x, mapData.width*TILE*SCALE - sw))
    camera.y = math.max(0, math.min(camera.y, mapData.height*TILE*SCALE - sh))
end

function love.keypressed(key)
    if key == "space" then meleeAttack()
    elseif key == "escape" then love.event.quit()
    elseif key == "r" then
        enemies, items, projectiles, damageFlash = {}, {}, {}, {}
        player.hp, player.mp, player.moveTimer = 10, 20, 0
        spawnEntities(); calculateFOV()
    end
end

function love.mousepressed(x, y, button)
    if button == 1 then
        local tx = (x + camera.x) / (TILE*SCALE) + 0.5
        local ty = (y + camera.y) / (TILE*SCALE) + 0.5
        castMagic(tx, ty)
    end
end

------------------------------------------------------------
-- DRAWING
------------------------------------------------------------
local function drawTileRaw(rawGid, px, py)
    local gid, r, sx, sy = decodeGid(rawGid)
    if gid == 0 or not quads[gid] then return end
    love.graphics.draw(tileset, quads[gid], px + TILE/2, py + TILE/2, r, sx, sy, TILE/2, TILE/2)
end

local function drawLayer(layerData, dimOutsideFOV)
    for y = 1, mapData.height do
        for x = 1, mapData.width do
            local raw = layerData[y][x]
            if raw ~= 0 then
                if dimOutsideFOV and not isInFOV(x, y) then
                    love.graphics.setColor(0.15, 0.15, 0.25, 1)
                else
                    love.graphics.setColor(1, 1, 1, 1)
                end
                drawTileRaw(raw, (x-1)*TILE, (y-1)*TILE)
            end
        end
    end
end

function love.draw()
    love.graphics.push()
    love.graphics.scale(SCALE, SCALE)
    love.graphics.translate(-camera.x/SCALE, -camera.y/SCALE)

    -- 1. Ground (always rendered)
    drawLayer(mapData.Ground, true)
    -- 2. Ground decorations
    drawLayer(mapData.GroundDeco, true)
    -- 3. Collision (walls - visible)
    drawLayer(mapData.Collision, true)

    -- 4. Items (FOV only)
    for _, it in ipairs(items) do
        if not it.collected and isInFOV(it.x, it.y) then
            love.graphics.setColor(1,1,1,1)
            love.graphics.draw(tileset, quads[it.gid], (it.x-1)*TILE, (it.y-1)*TILE)
            love.graphics.setColor(1,1,0, 0.3 + 0.15*math.sin(love.timer.getTime()*4))
            love.graphics.rectangle("fill", (it.x-1)*TILE, (it.y-1)*TILE, TILE, TILE)
        end
    end

    -- 5. Enemies (FOV only)
    for _, e in ipairs(enemies) do
        if e.alive and isInFOV(e.x, e.y) then
            love.graphics.setColor(1,1,1,1)
            love.graphics.draw(tileset, quads[e.gid], (e.x-1)*TILE, (e.y-1)*TILE)
            local bx, by = (e.x-1)*TILE, (e.y-1)*TILE - 3
            love.graphics.setColor(0.3,0,0,1)
            love.graphics.rectangle("fill", bx, by, TILE, 2)
            love.graphics.setColor(1,0,0,1)
            love.graphics.rectangle("fill", bx, by, TILE*(e.hp/e.maxHp), 2)
        end
    end

    -- 6. Damage flash
    for _, d in ipairs(damageFlash) do
        love.graphics.setColor(1,0,0, (d.timer/0.3)*0.5)
        love.graphics.rectangle("fill", (d.x-1)*TILE, (d.y-1)*TILE, TILE, TILE)
    end

    -- 7. Player
    love.graphics.setColor(0, 1, 0.4, 1)
    love.graphics.rectangle("fill", (player.x-1)*TILE+2, (player.y-1)*TILE+2, TILE-4, TILE-4)
    local dir = angleTo8Dir(player.aimAngle)
    love.graphics.setColor(1,1,1,1)
    love.graphics.circle("fill", (player.x-1)*TILE+TILE/2+dir[1]*5, (player.y-1)*TILE+TILE/2+dir[2]*5, 2)

    -- Melee flash
    if player.attackDir then
        local ax = (player.x+player.attackDir[1]-1)*TILE
        local ay = (player.y+player.attackDir[2]-1)*TILE
        love.graphics.setColor(1,1,1, (player.attackTimer/0.2)*0.6)
        love.graphics.rectangle("line", ax, ay, TILE, TILE)
        love.graphics.line(ax,ay, ax+TILE,ay+TILE)
        love.graphics.line(ax+TILE,ay, ax,ay+TILE)
    end

    -- 8. Magic projectiles (lerp from player to target)
    for _, p in ipairs(projectiles) do
        if p.alive then
            local t = p.timer / p.duration
            local cx = p.startX + (p.targetX - p.startX) * t
            local cy = p.startY + (p.targetY - p.startY) * t
            local px = (cx - 1) * TILE + TILE/2
            local py = (cy - 1) * TILE + TILE/2
            -- Glow
            love.graphics.setColor(0.4, 0.2, 1, 0.4)
            love.graphics.circle("fill", px, py, 5)
            -- Core
            love.graphics.setColor(0.7, 0.4, 1, 1)
            love.graphics.circle("fill", px, py, 3)
        end
    end

    -- 9. Overlay (above player)
    drawLayer(mapData.Overlay, true)

    -- FOV cone border
    love.graphics.setColor(0.3,0.5,1, 0.12)
    love.graphics.arc("fill", (player.x-1)*TILE+TILE/2, (player.y-1)*TILE+TILE/2,
        FOV_RANGE*TILE, player.aimAngle-FOV_HALF, player.aimAngle+FOV_HALF)

    -- Aim crosshair
    local mx, my = love.mouse.getPosition()
    local agx = math.floor((mx+camera.x)/(TILE*SCALE)) + 1
    local agy = math.floor((my+camera.y)/(TILE*SCALE)) + 1
    if inBounds(agx, agy) then
        love.graphics.setColor(1,0.3,0.3, 0.5+0.2*math.sin(love.timer.getTime()*6))
        love.graphics.rectangle("line", (agx-1)*TILE, (agy-1)*TILE, TILE, TILE)
        local cx = (agx-1)*TILE+TILE/2
        local cy = (agy-1)*TILE+TILE/2
        love.graphics.line(cx-4,cy, cx+4,cy)
        love.graphics.line(cx,cy-4, cx,cy+4)
    end

    love.graphics.pop()

    -- HUD
    love.graphics.setColor(0,0,0,0.7)
    love.graphics.rectangle("fill", 8, 8, 220, 70)
    love.graphics.setColor(1,1,1,1)
    love.graphics.print("HP:", 16, 14)
    love.graphics.setColor(0.3,0,0,1)
    love.graphics.rectangle("fill", 44, 14, 100, 14)
    love.graphics.setColor(0,0.8,0.3,1)
    love.graphics.rectangle("fill", 44, 14, 100*(player.hp/player.maxHp), 14)
    -- MP bar
    love.graphics.setColor(1,1,1,1)
    love.graphics.print("MP:", 16, 34)
    love.graphics.setColor(0.1,0.1,0.3,1)
    love.graphics.rectangle("fill", 44, 34, 100, 14)
    love.graphics.setColor(0.3,0.3,1,1)
    love.graphics.rectangle("fill", 44, 34, 100*(player.mp/player.maxMp), 14)
    local alive = 0
    for _, e in ipairs(enemies) do if e.alive then alive = alive+1 end end
    love.graphics.setColor(1,0.5,0.5,1)
    love.graphics.print("Enemies: "..alive, 160, 14)
    love.graphics.setColor(0.6,0.6,0.6,1)
    love.graphics.print("WASD:Move  Click:Magic  Space:Melee  R:Restart", 16, 54)
    love.graphics.setColor(0.5,0.5,0.5,0.8)
    love.graphics.print(string.format("Pos: %d,%d", player.x, player.y), 16, 690)
    if alive == 0 and #enemies > 0 then
        love.graphics.setColor(0,1,0.5,1)
        love.graphics.printf("ALL ENEMIES DEFEATED! Press R to restart", 0, 200, love.graphics.getWidth(), "center")
    end
end
