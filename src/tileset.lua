local Config = require("src.config")
local Map = require("src.map")

local Tileset = {}

local tileset, quads

local function decodeGid(raw)
    if raw == 0 then return 0, 0, 1, 1 end
    local fh, fv, fd = false, false, false
    if raw >= Config.FLIP_H then raw = raw - Config.FLIP_H; fh = true end
    if raw >= Config.FLIP_V then raw = raw - Config.FLIP_V; fv = true end
    if raw >= Config.FLIP_D then raw = raw - Config.FLIP_D; fd = true end
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

function Tileset.load()
    tileset = love.graphics.newImage("Tilemap/tileset_legacy_transparent.png")
    quads = {}
    for gid = 1, 1024 do
        local row = math.floor((gid-1) / Config.TS_COLS)
        local col = (gid-1) % Config.TS_COLS
        quads[gid] = love.graphics.newQuad(col*17, row*17, Config.TILE, Config.TILE, Config.TS_SIZE, Config.TS_SIZE)
    end
end

function Tileset.drawTile(rawGid, px, py)
    local gid, r, sx, sy = decodeGid(rawGid)
    if gid == 0 or not quads[gid] then return end
    love.graphics.draw(tileset, quads[gid], px + Config.TILE/2, py + Config.TILE/2, r, sx, sy, Config.TILE/2, Config.TILE/2)
end

function Tileset.drawLayer(layerData, fov, dimOutside)
    for y = 1, Map.height do
        for x = 1, Map.width do
            local raw = layerData[y][x]
            if raw ~= 0 then
                if dimOutside and not fov.isVisible(x, y) then
                    love.graphics.setColor(Config.DIM_R, Config.DIM_G, Config.DIM_B, 1)
                else
                    love.graphics.setColor(1, 1, 1, 1)
                end
                Tileset.drawTile(raw, (x-1)*Config.TILE, (y-1)*Config.TILE)
            end
        end
    end
end

function Tileset.getImage()
    return tileset
end

function Tileset.getQuad(gid)
    return quads[gid]
end

return Tileset
