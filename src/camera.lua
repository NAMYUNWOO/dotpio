local Config = require("src.config")
local Map = require("src.map")

local Camera = {x = 0, y = 0}

function Camera.update(playerX, playerY)
    local sw, sh = love.graphics.getWidth(), love.graphics.getHeight()
    Camera.x = playerX * Config.TILE*Config.SCALE - sw/2
    Camera.y = playerY * Config.TILE*Config.SCALE - sh/2
    Camera.x = math.max(0, math.min(Camera.x, Map.width*Config.TILE*Config.SCALE - sw))
    Camera.y = math.max(0, math.min(Camera.y, Map.height*Config.TILE*Config.SCALE - sh))
end

function Camera.apply()
    love.graphics.push()
    love.graphics.scale(Config.SCALE, Config.SCALE)
    love.graphics.translate(-Camera.x/Config.SCALE, -Camera.y/Config.SCALE)
end

function Camera.screenToWorld(mx, my)
    local wx = (mx + Camera.x) / (Config.TILE*Config.SCALE) + 0.5
    local wy = (my + Camera.y) / (Config.TILE*Config.SCALE) + 0.5
    return wx, wy
end

return Camera
