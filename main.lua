-- Top-down Roguelike with Fan-shaped FOV System
-- Layered map: Ground -> GroundDeco -> Collision -> Player -> Overlay

local Config      = require("src.config")
local Map         = require("src.map")
local Tileset     = require("src.tileset")
local FOV         = require("src.fov")
local Player      = require("src.player")
local Combat      = require("src.combat")
local Entities    = require("src.entities")
local Camera      = require("src.camera")
local HUD         = require("src.hud")
local Portal      = require("src.portal")
local InventoryUI = require("src.inventory_ui")
local AiDescribe  = require("src.ai_describe")

local gameOver = false

local function loadMap(mapName, portalName)
    Map.load(mapName)
    Combat.reset()
    if portalName then
        local portal = Map.getPortalByName(portalName)
        if portal then
            Player.x, Player.y = portal.x, portal.y
        end
        Entities.spawn(Player, true)
        Portal.setCooldown()
    else
        Entities.spawn(Player)
        Portal.resetCooldown()
    end
    Player.visualX, Player.visualY = Player.x, Player.y
    FOV.calculate(Player.x, Player.y, Player.aimAngle)
    gameOver = false
end

Portal.onLoad = loadMap

------------------------------------------------------------
-- LOVE CALLBACKS
------------------------------------------------------------
function love.load()
    love.graphics.setDefaultFilter("nearest", "nearest")
    Tileset.load()
    InventoryUI.init()
    AiDescribe.init()
    Player.init(0, 0)
    loadMap("01", nil)
end

function love.update(dt)
    AiDescribe.update()
    if InventoryUI.isOpen() then
        InventoryUI.update(dt)
        return
    end
    if gameOver then return end

    Player.update(dt, Camera, Entities.items)
    FOV.calculate(Player.x, Player.y, Player.aimAngle)
    Combat.update(dt, Entities.enemyAt)
    Entities.update(dt, Player, Combat.addDamageFlash)
    Camera.update(Player.visualX, Player.visualY)

    if Player.hp <= 0 then
        Player.hp = 0
        gameOver = true
    end

    Portal.check(Player.x, Player.y, Map)
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
    love.graphics.arc("fill", (Player.visualX-1)*TILE+TILE/2, (Player.visualY-1)*TILE+TILE/2,
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

    -- Inventory overlay (drawn last, on top of everything)
    if InventoryUI.isOpen() then
        InventoryUI.draw()
    end
end

function love.keypressed(key)
    if InventoryUI.isOpen() then
        InventoryUI.keypressed(key)
        return
    end
    if key == "tab" or key == "i" then
        InventoryUI.open(Player, Entities)
        return
    end
    if key == "r" then
        Player.inventory = nil
        Player.init(0, 0)
        loadMap("01", nil)
        return
    end
    if gameOver then return end
    if key == "space" then
        Combat.meleeAttack(Player, Entities.enemyAt)
    elseif key == "escape" then
        love.event.quit()
    end
end

function love.textinput(text)
    if InventoryUI.isOpen() then
        InventoryUI.textinput(text)
    end
end

function love.quit()
    AiDescribe.shutdown()
end

function love.mousepressed(x, y, button)
    if InventoryUI.isOpen() then return end
    if gameOver then return end
    if button == 1 then
        local tx = (x + Camera.x) / (Config.TILE*Config.SCALE) + 0.5
        local ty = (y + Camera.y) / (Config.TILE*Config.SCALE) + 0.5
        Combat.castMagic(Player, tx, ty)
    end
end
