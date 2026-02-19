-- Top-down Roguelike with Fan-shaped FOV System
-- Layered map: Ground -> GroundDeco -> Collision -> Player -> Overlay

local Config   = require("src.config")
local Map      = require("src.map")
local Tileset  = require("src.tileset")
local FOV      = require("src.fov")
local Player   = require("src.player")
local Combat   = require("src.combat")
local Entities = require("src.entities")
local Camera   = require("src.camera")
local HUD      = require("src.hud")

local gameOver = false

------------------------------------------------------------
-- LOVE CALLBACKS
------------------------------------------------------------
function love.load()
    love.graphics.setDefaultFilter("nearest", "nearest")
    Map.load()
    Tileset.load()
    Entities.spawn(Player)
    FOV.calculate(Player.x, Player.y, Player.aimAngle)
    gameOver = false
end

function love.update(dt)
    if gameOver then return end

    Player.update(dt, Camera, Entities.items)
    FOV.calculate(Player.x, Player.y, Player.aimAngle)
    Combat.update(dt, Entities.enemyAt)
    Entities.update(dt, Player, Combat.addDamageFlash)
    Camera.update(Player.x, Player.y)

    if Player.hp <= 0 then
        Player.hp = 0
        gameOver = true
    end
end

function love.draw()
    Camera.apply()

    -- Layers
    Tileset.drawLayer(Map.Ground, FOV, true)
    Tileset.drawLayer(Map.GroundDeco, FOV, true)
    Tileset.drawLayer(Map.Collision, FOV, true)

    -- Items & Enemies
    Entities.drawItems(FOV, Tileset)
    Entities.drawEnemies(FOV, Tileset)

    -- Effects & Player
    Combat.drawEffects()
    Player.draw()
    Combat.drawProjectiles()

    -- Overlay
    Tileset.drawLayer(Map.Overlay, FOV, true)

    -- FOV cone border
    local TILE = Config.TILE
    love.graphics.setColor(0.3,0.5,1, 0.12)
    love.graphics.arc("fill", (Player.x-1)*TILE+TILE/2, (Player.y-1)*TILE+TILE/2,
        Config.FOV_RANGE*TILE, Player.aimAngle-Config.FOV_HALF, Player.aimAngle+Config.FOV_HALF)

    -- Aim crosshair
    local mx, my = love.mouse.getPosition()
    local agx = math.floor((mx+Camera.x)/(TILE*Config.SCALE)) + 1
    local agy = math.floor((my+Camera.y)/(TILE*Config.SCALE)) + 1
    if Map.inBounds(agx, agy) then
        love.graphics.setColor(1,0.3,0.3, 0.5+0.2*math.sin(love.timer.getTime()*6))
        love.graphics.rectangle("line", (agx-1)*TILE, (agy-1)*TILE, TILE, TILE)
        local cx = (agx-1)*TILE+TILE/2
        local cy = (agy-1)*TILE+TILE/2
        love.graphics.line(cx-4,cy, cx+4,cy)
        love.graphics.line(cx,cy-4, cx,cy+4)
    end

    love.graphics.pop()

    -- HUD
    HUD.draw(Player, Entities.enemies, gameOver)
end

function love.keypressed(key)
    if key == "r" then
        Combat.reset()
        Player.init(0, 0)
        Entities.spawn(Player)
        FOV.calculate(Player.x, Player.y, Player.aimAngle)
        gameOver = false
        return
    end
    if gameOver then return end
    if key == "space" then
        Combat.meleeAttack(Player, Entities.enemyAt)
    elseif key == "escape" then
        love.event.quit()
    end
end

function love.mousepressed(x, y, button)
    if gameOver then return end
    if button == 1 then
        local tx = (x + Camera.x) / (Config.TILE*Config.SCALE) + 0.5
        local ty = (y + Camera.y) / (Config.TILE*Config.SCALE) + 0.5
        Combat.castMagic(Player, tx, ty)
    end
end
