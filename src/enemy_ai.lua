local Config = require("src.config")
local Map = require("src.map")

-- Jumper A* pathfinding
local Grid = require("libs.jumper.jumper.grid")
local Pathfinder = require("libs.jumper.jumper.pathfinder")

local EnemyAI = {}

local grid, finder

-- Build walkability grid for Jumper (0 = walkable, 1 = blocked)
function EnemyAI.buildGrid()
    local map = {}
    for y = 1, Map.height do
        map[y] = {}
        for x = 1, Map.width do
            map[y][x] = Map.isWalkable(x, y) and 0 or 1
        end
    end
    grid = Grid(map)
    finder = Pathfinder(grid, 'ASTAR', 0)
    finder:setMode('ORTHOGONAL')
end

-- Line-of-sight check using Map.isOpaque (same as FOV)
local function hasLOS(x1, y1, x2, y2)
    local dx, dy = x2 - x1, y2 - y1
    local steps = math.max(math.abs(dx), math.abs(dy))
    if steps == 0 then return true end
    local xi, yi = dx / steps, dy / steps
    local cx, cy = x1, y1
    for _ = 1, steps - 1 do
        cx, cy = cx + xi, cy + yi
        if Map.isOpaque(math.floor(cx + 0.5), math.floor(cy + 0.5)) then
            return false
        end
    end
    return true
end

local function dist(x1, y1, x2, y2)
    local dx, dy = x2 - x1, y2 - y1
    return math.sqrt(dx * dx + dy * dy)
end

local function isAdjacent(x1, y1, x2, y2)
    return math.abs(x1 - x2) <= 1 and math.abs(y1 - y2) <= 1
        and not (x1 == x2 and y1 == y2)
end

-- Get next step from A* path toward target
local function getNextStep(fromX, fromY, toX, toY, enemies, selfIdx)
    if not finder then return nil, nil end
    local path = finder:getPath(fromX, fromY, toX, toY)
    if not path then return nil, nil end
    -- path:iter() yields nodes; skip first (current position)
    local first = true
    for node, _ in path:iter() do
        if first then
            first = false
        else
            local nx, ny = node:getX(), node:getY()
            -- Check no other alive enemy occupies target
            local occupied = false
            for i, e in ipairs(enemies) do
                if i ~= selfIdx and e.alive and e.x == nx and e.y == ny then
                    occupied = true
                    break
                end
            end
            if not occupied then
                return nx, ny
            end
            return nil, nil  -- blocked by another enemy
        end
    end
    return nil, nil
end

-- Pick a random walkable tile near spawn for patrol
local function pickPatrolTarget(e)
    local range = 4
    for _ = 1, 20 do
        local tx = e.spawnX + love.math.random(-range, range)
        local ty = e.spawnY + love.math.random(-range, range)
        if Map.isWalkable(tx, ty) then
            return tx, ty
        end
    end
    return e.spawnX, e.spawnY
end

function EnemyAI.init(e, idx)
    e.state = "idle"
    e.moveTimer = love.math.random() * Config.ENEMY_MOVE_CD
    e.atkTimer = 0
    e.spawnX = e.x
    e.spawnY = e.y
    e.patrolX = nil
    e.patrolY = nil
    e.idleTimer = love.math.random() * 1.5
end

function EnemyAI.update(e, idx, dt, player, enemies)
    if not e.alive then return end

    e.moveTimer = math.max(0, e.moveTimer - dt)
    e.atkTimer = math.max(0, e.atkTimer - dt)

    local d = dist(e.x, e.y, player.x, player.y)
    local los = d <= Config.ENEMY_CHASE and hasLOS(e.x, e.y, player.x, player.y)
    local canSee = d <= Config.ENEMY_DETECT and los

    -- State transitions
    if e.state == "idle" then
        e.idleTimer = e.idleTimer - dt
        if canSee then
            e.state = "chase"
        elseif e.idleTimer <= 0 then
            e.state = "patrol"
            e.patrolX, e.patrolY = pickPatrolTarget(e)
        end

    elseif e.state == "patrol" then
        if canSee then
            e.state = "chase"
        elseif e.x == e.patrolX and e.y == e.patrolY then
            e.state = "idle"
            e.idleTimer = 1.0 + love.math.random() * 1.5
        end

    elseif e.state == "chase" then
        if e.hp <= Config.ENEMY_FLEE_HP then
            e.state = "flee"
        elseif isAdjacent(e.x, e.y, player.x, player.y) then
            e.state = "attack"
        elseif d > Config.ENEMY_CHASE or not los then
            e.state = "idle"
            e.idleTimer = 0.5
        end

    elseif e.state == "attack" then
        if e.hp <= Config.ENEMY_FLEE_HP then
            e.state = "flee"
        elseif not isAdjacent(e.x, e.y, player.x, player.y) then
            e.state = "chase"
        end

    elseif e.state == "flee" then
        if d > Config.ENEMY_CHASE then
            e.state = "idle"
            e.idleTimer = 1.0
        end
    end

    -- Actions per state
    if e.state == "patrol" and e.moveTimer <= 0 and e.patrolX then
        local nx, ny = getNextStep(e.x, e.y, e.patrolX, e.patrolY, enemies, idx)
        if nx then
            e.x, e.y = nx, ny
            e.moveTimer = Config.ENEMY_MOVE_CD
        else
            -- Can't reach patrol target, go idle
            e.state = "idle"
            e.idleTimer = 1.0
        end

    elseif e.state == "chase" and e.moveTimer <= 0 then
        local nx, ny = getNextStep(e.x, e.y, player.x, player.y, enemies, idx)
        if nx then
            e.x, e.y = nx, ny
            e.moveTimer = Config.ENEMY_MOVE_CD
        end

    elseif e.state == "attack" and e.atkTimer <= 0 then
        -- Deal damage to player
        player.hp = player.hp - Config.ENEMY_ATK_DMG
        e.atkTimer = Config.ENEMY_ATK_CD
        return "hit_player"

    elseif e.state == "flee" and e.moveTimer <= 0 then
        -- Move away from player
        local fleeX = e.x + (e.x - player.x)
        local fleeY = e.y + (e.y - player.y)
        -- Clamp to map bounds
        fleeX = math.max(1, math.min(Map.width, fleeX))
        fleeY = math.max(1, math.min(Map.height, fleeY))
        local nx, ny = getNextStep(e.x, e.y, fleeX, fleeY, enemies, idx)
        if nx then
            e.x, e.y = nx, ny
            e.moveTimer = Config.ENEMY_MOVE_CD
        else
            -- Try random adjacent walkable cell
            local dirs = {{1,0},{-1,0},{0,1},{0,-1}}
            for _, dir in ipairs(dirs) do
                local tx, ty = e.x + dir[1], e.y + dir[2]
                if Map.isWalkable(tx, ty) then
                    local occupied = false
                    for i, other in ipairs(enemies) do
                        if i ~= idx and other.alive and other.x == tx and other.y == ty then
                            occupied = true; break
                        end
                    end
                    if not occupied and not (tx == player.x and ty == player.y) then
                        e.x, e.y = tx, ty
                        e.moveTimer = Config.ENEMY_MOVE_CD
                        break
                    end
                end
            end
        end
    end
end

return EnemyAI
