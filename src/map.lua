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
Map.portals = {}
Map.lootbox = nil
Map.currentMap = nil

function Map.load(mapName)
    mapName = mapName or "01"
    Map.currentMap = mapName
    local data = dofile("maps/map_" .. mapName .. ".lua")
    Map.width = data.width
    Map.height = data.height
    Map.Ground = data.Ground
    Map.GroundDeco = data.GroundDeco
    Map.Collision = data.Collision
    Map.Overlay = data.Overlay
    Map.dimTiles = data.dimTiles or {}
    Map.occludeTiles = data.occludeTiles or {}
    Map.portals = data.portals or {}
    Map.lootbox = data.lootbox
end

function Map.getLootboxPositions()
    local positions = {}
    if not Map.lootbox then return positions end
    for y = 1, Map.height do
        for x = 1, Map.width do
            if Map.lootbox[y][x] ~= 0 then
                table.insert(positions, {x, y})
            end
        end
    end
    return positions
end

function Map.getPortalAt(gx, gy)
    for _, p in ipairs(Map.portals) do
        if p.tileX == gx and p.tileY == gy then
            return p
        end
    end
    return nil
end

function Map.getPortalByName(name)
    for _, p in ipairs(Map.portals) do
        if p.name == name then
            return p
        end
    end
    return nil
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

Map.extraBlockers = nil  -- optional callback(gx,gy) → true if blocked

function Map.isWalkable(gx, gy)
    if not Map.inBounds(gx, gy) or Map.isBlocked(gx, gy) then return false end
    if Map.extraBlockers and Map.extraBlockers(gx, gy) then return false end
    return true
end

return Map
