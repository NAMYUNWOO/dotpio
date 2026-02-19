local Config = require("src.config")
local Map = require("src.map")

local FOV = {}

local fovSet = {}

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
        if Map.isOpaque(math.floor(cx+0.5), math.floor(cy+0.5)) then return false end
    end
    return true
end

function FOV.calculate(px, py, aimAngle)
    fovSet = {}
    for dy = -Config.FOV_RANGE, Config.FOV_RANGE do
        for dx = -Config.FOV_RANGE, Config.FOV_RANGE do
            local tx, ty = px+dx, py+dy
            if Map.inBounds(tx, ty) then
                local dist = math.sqrt(dx*dx + dy*dy)
                if dist <= Config.FOV_RANGE then
                    if dist <= 1.5 then
                        fovSet[tx..","..ty] = true
                    else
                        local diff = normalizeAngle(math.atan2(dy,dx) - aimAngle)
                        if math.abs(diff) <= Config.FOV_HALF and hasLOS(px,py,tx,ty) then
                            fovSet[tx..","..ty] = true
                        end
                    end
                end
            end
        end
    end
end

function FOV.isVisible(gx, gy)
    return fovSet[gx..","..gy] == true
end

return FOV
