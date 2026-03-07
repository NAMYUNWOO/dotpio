local Config = require("src.config")
local Map = require("src.map")
local Inventory = require("src.inventory")

local Player = {
    x = 0, y = 0, aimAngle = 0,
    visualX = 0, visualY = 0,
    moveTimer = 0,
    hp = 10, maxHp = 10,
    mp = 20, maxMp = 20,
    attackTimer = 0, attackDir = nil,
    inventory = nil,
}

function Player.init(x, y)
    Player.x = x
    Player.y = y
    Player.visualX = x
    Player.visualY = y
    Player.aimAngle = 0
    Player.moveTimer = 0
    Player.hp = 10
    Player.maxHp = 10
    Player.mp = 20
    Player.maxMp = 20
    Player.attackTimer = 0
    Player.attackDir = nil
    if not Player.inventory then
        Player.inventory = Inventory.new()
    end
end

function Player.update(dt, camera, items)
    Player.moveTimer = math.max(0, Player.moveTimer - dt)
    Player.attackTimer = math.max(0, Player.attackTimer - dt)
    if Player.attackTimer <= 0 then Player.attackDir = nil end

    -- WASD
    if Player.moveTimer <= 0 then
        local dx, dy = 0, 0
        if love.keyboard.isDown("w","up")    then dy = dy-1 end
        if love.keyboard.isDown("s","down")  then dy = dy+1 end
        if love.keyboard.isDown("a","left")  then dx = dx-1 end
        if love.keyboard.isDown("d","right") then dx = dx+1 end
        if dx ~= 0 or dy ~= 0 then
            local nx, ny = Player.x+dx, Player.y+dy
            local moved = false
            if Map.isWalkable(nx, ny) then
                Player.x, Player.y = nx, ny; moved = true
            elseif dx ~= 0 and dy ~= 0 then
                if Map.isWalkable(Player.x+dx, Player.y) then
                    Player.x = Player.x+dx; moved = true
                elseif Map.isWalkable(Player.x, Player.y+dy) then
                    Player.y = Player.y+dy; moved = true
                end
            end
            if moved then
                Player.moveTimer = Config.MOVE_CD
                for _, it in ipairs(items) do
                    if not it.collected and it.x == Player.x and it.y == Player.y then
                        local itemId = it.itemId
                        local ok = Inventory.addItem(Player.inventory, itemId, 1)
                        if ok then
                            it.collected = true
                        end
                    end
                end
            end
        end
    end

    -- Visual lerp
    local t = math.min(1, Config.LERP_SPEED * dt)
    Player.visualX = Player.visualX + (Player.x - Player.visualX) * t
    Player.visualY = Player.visualY + (Player.y - Player.visualY) * t

    -- Mouse aim (based on visual position)
    local mx, my = love.mouse.getPosition()
    local wx = (mx + camera.x) / (Config.TILE*Config.SCALE) + 0.5
    local wy = (my + camera.y) / (Config.TILE*Config.SCALE) + 0.5
    Player.aimAngle = math.atan2(wy - Player.visualY, wx - Player.visualX)
end

function Player.draw()
    local TILE = Config.TILE
    local vx, vy = Player.visualX, Player.visualY
    local underOverlay = Map.isOverlayOpaque(Player.x, Player.y)
    local alpha = underOverlay and 0.45 or 1

    -- Player body
    love.graphics.setColor(0, 1, 0.4, alpha)
    love.graphics.rectangle("fill", (vx-1)*TILE+2, (vy-1)*TILE+2, TILE-4, TILE-4)
    -- Direction dot
    local dir = Config.angleTo8Dir(Player.aimAngle)
    love.graphics.setColor(1, 1, 1, alpha)
    love.graphics.circle("fill", (vx-1)*TILE+TILE/2+dir[1]*5, (vy-1)*TILE+TILE/2+dir[2]*5, 2)

    -- Highlight outline when under overlay
    if underOverlay then
        local pulse = 0.6 + 0.4 * math.sin(love.timer.getTime() * 4)
        love.graphics.setColor(1, 1, 1, pulse * 0.7)
        love.graphics.setLineWidth(2)
        love.graphics.rectangle("line", (vx-1)*TILE+1, (vy-1)*TILE+1, TILE-2, TILE-2)
        love.graphics.setLineWidth(1)
    end

    -- Melee flash (stays on logical grid)
    if Player.attackDir then
        local ax = (Player.x+Player.attackDir[1]-1)*TILE
        local ay = (Player.y+Player.attackDir[2]-1)*TILE
        love.graphics.setColor(1,1,1, (Player.attackTimer/0.2)*0.6)
        love.graphics.rectangle("line", ax, ay, TILE, TILE)
        love.graphics.line(ax,ay, ax+TILE,ay+TILE)
        love.graphics.line(ax+TILE,ay, ax,ay+TILE)
    end
end

return Player
