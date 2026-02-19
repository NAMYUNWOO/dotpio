local Config = require("src.config")

local Map = {}

Map.width = 0
Map.height = 0
Map.Ground = nil
Map.GroundDeco = nil
Map.Collision = nil
Map.Overlay = nil
Map.dimTiles = {}
Map.occludeTiles = {}

function Map.load()
    local data = dofile("map_data.lua")
    Map.width = data.width
    Map.height = data.height
    Map.Ground = data.Ground
    Map.GroundDeco = data.GroundDeco
    Map.Collision = data.Collision
    Map.Overlay = data.Overlay
    Map.dimTiles = data.dimTiles or {}
    Map.occludeTiles = data.occludeTiles or {}
end

function Map.isOverlayOpaque(gx, gy)
    if not Map.inBounds(gx, gy) then return false end
    local raw = Map.Overlay[gy][gx]
    if raw == 0 then return false end
    local gid = Config.stripFlipBits(raw)
    return Map.occludeTiles[gid] == true
end

function Map.inBounds(gx, gy)
    return gx >= 1 and gy >= 1 and gx <= Map.width and gy <= Map.height
end

function Map.isBlocked(gx, gy)
    if not Map.inBounds(gx, gy) then return true end
    return Map.Collision[gy][gx] ~= 0
end

function Map.isOpaque(gx, gy)
    if not Map.inBounds(gx, gy) then return true end
    local layers = {Map.Ground, Map.GroundDeco, Map.Collision, Map.Overlay}
    for _, layer in ipairs(layers) do
        local raw = layer[gy][gx]
        if raw ~= 0 then
            local gid = Config.stripFlipBits(raw)
            if Map.dimTiles[gid] then return true end
        end
    end
    return false
end

function Map.isWalkable(gx, gy)
    return Map.inBounds(gx, gy) and not Map.isBlocked(gx, gy)
end

return Map
