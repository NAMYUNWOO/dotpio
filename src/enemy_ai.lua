local Config = require("src.config")
local Map = require("src.map")
local Stats = require("src.stats")

-- Jumper A* pathfinding
local Grid = require("libs.jumper.jumper.grid")
local Pathfinder = require("libs.jumper.jumper.pathfinder")

local EnemyAI = {}

local grid, finder

local BEHAVIOR_DEFAULTS = {
    moveCdMul = 1.0,
    atkCdMul = 1.0,
    atkDmgBonus = 0,
    detectBonus = 0,
    chaseBonus = 0,
    fleeHp = Config.ENEMY_FLEE_HP,
    leashRadius = nil,
    retreatAfterHit = false,
    alertAlliesRange = nil,
    synergyFromBehavior = nil,
    synergyRange = 0,
    synergyMoveCdMul = 1.0,
    synergyAtkDmgBonus = 0,
}

local BEHAVIOR_PROFILES = {
    raider = {},
    skirmisher = {
        moveCdMul = 0.75,
        detectBonus = 1,
        chaseBonus = 1,
        retreatAfterHit = true,
    },
    bruiser = {
        moveCdMul = 1.2,
        atkCdMul = 1.15,
        atkDmgBonus = 1,
        detectBonus = -1,
        chaseBonus = -1,
        fleeHp = 0,
    },
    sentinel = {
        moveCdMul = 0.9,
        detectBonus = 2,
        chaseBonus = -2,
        leashRadius = 5,
        fleeHp = 0,
    },
    warcaller = {
        moveCdMul = 0.95,
        atkCdMul = 0.9,
        detectBonus = 1,
        chaseBonus = 0,
        alertAlliesRange = 4,
    },
    hunter = {
        moveCdMul = 1.0,
        atkCdMul = 1.0,
        atkDmgBonus = 0,
        detectBonus = 1,
        chaseBonus = 1,
        synergyFromBehavior = "warcaller",
        synergyRange = 4,
        synergyMoveCdMul = 0.75,
        synergyAtkDmgBonus = 1,
    },
}

local function behaviorFor(e)
    local profile = BEHAVIOR_PROFILES[e.behavior or "raider"] or {}
    return setmetatable(profile, { __index = BEHAVIOR_DEFAULTS })
end

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

local function hasNearbyBehavior(e, enemies, behaviorName, range)
    if not behaviorName or (range or 0) <= 0 then return false end
    for _, other in ipairs(enemies or {}) do
        if other ~= e and other.alive and other.behavior == behaviorName then
            if dist(e.x, e.y, other.x, other.y) <= range then
                return true
            end
        end
    end
    return false
end

local function alertNearbyAllies(e, enemies, range)
    if not range or range <= 0 then return 0 end
    local alerted = 0
    for _, other in ipairs(enemies or {}) do
        if other ~= e and other.alive then
            if dist(e.x, e.y, other.x, other.y) <= range then
                if not other.alerted then alerted = alerted + 1 end
                other.alerted = true
                if other.state == "idle" or other.state == "patrol" then
                    other.state = "chase"
                end
            end
        end
    end
    return alerted
end

local function syncSynergy(e, enemies)
    local behavior = behaviorFor(e)
    local empowered = hasNearbyBehavior(e, enemies, behavior.synergyFromBehavior, behavior.synergyRange)
    e.synergyEmpowered = empowered
    e.moveCd = e.baseMoveCd * (empowered and behavior.synergyMoveCdMul or 1)
    e.atkDmg = e.baseAtkDmg + (empowered and behavior.synergyAtkDmgBonus or 0)
    return empowered
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
    e.behavior = e.behavior or "raider"
    local behavior = behaviorFor(e)
    e.state = "idle"
    e.baseMoveCd = Config.ENEMY_MOVE_CD * behavior.moveCdMul
    e.moveCd = e.baseMoveCd
    e.atkCd = Config.ENEMY_ATK_CD * behavior.atkCdMul
    e.fleeHp = behavior.fleeHp
    e.detectRange = math.max(2, Config.ENEMY_DETECT + behavior.detectBonus)
    e.chaseRange = math.max(e.detectRange, Config.ENEMY_CHASE + behavior.chaseBonus)
    e.leashRadius = behavior.leashRadius
    e.baseAtkDmg = Config.ENEMY_ATK_DMG + behavior.atkDmgBonus
    e.atkDmg = e.baseAtkDmg
    e.retreatAfterHit = behavior.retreatAfterHit
    e.moveTimer = love.math.random() * e.moveCd
    e.atkTimer = 0
    e.spawnX = e.x
    e.spawnY = e.y
    e.visualX = e.x
    e.visualY = e.y
    e.patrolX = nil
    e.patrolY = nil
    e.idleTimer = love.math.random() * 1.5
    e.alerted = false
end

function EnemyAI.update(e, idx, dt, player, enemies)
    if not e.alive then return end

    e.moveTimer = math.max(0, e.moveTimer - dt)
    e.atkTimer = math.max(0, e.atkTimer - dt)

    local d = dist(e.x, e.y, player.x, player.y)
    local los = d <= e.chaseRange and hasLOS(e.x, e.y, player.x, player.y)
    local canSee = d <= e.detectRange and los
    local behavior = behaviorFor(e)

    syncSynergy(e, enemies)
    if canSee and behavior.alertAlliesRange then
        alertNearbyAllies(e, enemies, behavior.alertAlliesRange)
    end

    -- State transitions
    if e.state == "idle" then
        e.idleTimer = e.idleTimer - dt
        if canSee or e.alerted then
            e.state = "chase"
        elseif e.idleTimer <= 0 then
            e.state = "patrol"
            e.patrolX, e.patrolY = pickPatrolTarget(e)
        end

    elseif e.state == "patrol" then
        if canSee or e.alerted then
            e.state = "chase"
        elseif e.x == e.patrolX and e.y == e.patrolY then
            e.state = "idle"
            e.idleTimer = 1.0 + love.math.random() * 1.5
        end

    elseif e.state == "chase" then
        local distFromSpawn = dist(e.x, e.y, e.spawnX, e.spawnY)
        if e.hp <= e.fleeHp then
            e.state = "flee"
            e.alerted = false
        elseif e.leashRadius and distFromSpawn > e.leashRadius then
            e.state = "idle"
            e.idleTimer = 0.5
            e.patrolX, e.patrolY = e.spawnX, e.spawnY
        elseif isAdjacent(e.x, e.y, player.x, player.y) then
            e.state = "attack"
        elseif e.alerted then
            if d > e.detectRange then
                e.alerted = false
                e.state = "idle"
                e.idleTimer = 0.5
            end
        elseif d > e.chaseRange or not los then
            e.state = "idle"
            e.idleTimer = 0.5
        end

    elseif e.state == "attack" then
        if e.hp <= e.fleeHp then
            e.state = "flee"
        elseif not isAdjacent(e.x, e.y, player.x, player.y) then
            e.state = "chase"
        end

    elseif e.state == "flee" then
        if d > e.chaseRange then
            e.state = "idle"
            e.idleTimer = 1.0
        end
    end

    -- Visual lerp
    local t = math.min(1, Config.LERP_SPEED * dt)
    e.visualX = (e.visualX or e.x) + (e.x - (e.visualX or e.x)) * t
    e.visualY = (e.visualY or e.y) + (e.y - (e.visualY or e.y)) * t

    -- Actions per state
    if e.state == "patrol" and e.moveTimer <= 0 and e.patrolX then
        local nx, ny = getNextStep(e.x, e.y, e.patrolX, e.patrolY, enemies, idx)
        if nx then
            e.x, e.y = nx, ny
            e.moveTimer = e.moveCd
        else
            -- Can't reach patrol target, go idle
            e.state = "idle"
            e.idleTimer = 1.0
        end

    elseif e.state == "chase" and e.moveTimer <= 0 then
        local nx, ny = getNextStep(e.x, e.y, player.x, player.y, enemies, idx)
        if nx then
            e.x, e.y = nx, ny
            e.moveTimer = e.moveCd
        end

    elseif e.state == "attack" and e.atkTimer <= 0 then
        -- Deal damage to player
        local dmg = Stats.damageReduction(e.atkDmg, player.effectiveStats)
        player.hp = player.hp - math.max(1, math.floor(dmg + 0.5))
        e.atkTimer = e.atkCd
        if e.retreatAfterHit then
            e.state = "flee"
        end
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
            e.moveTimer = e.moveCd
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
                        e.moveTimer = e.moveCd
                        break
                    end
                end
            end
        end
    end
end

function EnemyAI.getBehaviorProfiles()
    return BEHAVIOR_PROFILES
end

function EnemyAI.debugSyncSynergy(e, enemies)
    return syncSynergy(e, enemies or {})
end

function EnemyAI.debugAlertNearbyAllies(e, enemies)
    local behavior = behaviorFor(e)
    return alertNearbyAllies(e, enemies or {}, behavior.alertAlliesRange)
end

return EnemyAI
