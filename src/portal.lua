local Portal = {}
local cooldown = false
local pendingTransition = nil
local routeTagCache = {}

-- 맵 전환 콜백: onLoad(targetMap, targetPortal)
Portal.onLoad = nil

local function normalizeRouteTag(tag)
    local value = string.upper(tostring(tag or ""))
    if value == "SAFE" or value == "RISK" or value == "SPIKE" then
        return value
    end
    return nil
end

local function resolveMapRouteTag(mapName)
    local key = tostring(mapName or "")
    if key == "" then
        return nil
    end
    if routeTagCache[key] ~= nil then
        return routeTagCache[key] or nil
    end

    local ok, mapData = pcall(dofile, "maps/map_" .. key .. ".lua")
    local tag = nil
    if ok and type(mapData) == "table" then
        local metadata = mapData.metadata
        local hazard = metadata and metadata.overclockHazard
        if type(hazard) == "table" then
            tag = normalizeRouteTag(hazard.routeTag)
        end
    end

    routeTagCache[key] = tag or false
    return tag
end

local function setPendingTransition(portal)
    if not portal then
        pendingTransition = nil
        return
    end
    pendingTransition = {
        targetMap = portal.targetMap,
        targetPortal = portal.targetPortal,
        routeTag = resolveMapRouteTag(portal.targetMap),
    }
end

function Portal.check(playerX, playerY, Map)
    local p = Map.getPortalAt(playerX, playerY)
    if p and not cooldown then
        cooldown = true
        setPendingTransition(p)
    elseif not p then
        cooldown = false
        pendingTransition = nil
    end
end

function Portal.hasPendingTransition()
    return pendingTransition ~= nil
end

function Portal.getPendingTransition()
    return pendingTransition
end

local function resolveRouteCoach(routeTag)
    if routeTag == "SAFE" then
        return "LOW PRESSURE"
    elseif routeTag == "RISK" then
        return "BALANCED RISK"
    elseif routeTag == "SPIKE" then
        return "HIGH PRESSURE"
    end
    return "NO DATA"
end

function Portal.getTransitionPrompt()
    if not pendingTransition then
        return nil
    end
    local routeTag = pendingTransition.routeTag or "UNKNOWN"
    local coach = resolveRouteCoach(routeTag)
    return string.format("PORTAL READY -> ENTER:JUMP  N:CANCEL  NEXT ROUTE:%s  COACH:%s", routeTag, coach)
end

function Portal.confirmTransition()
    if not pendingTransition then
        return false
    end

    local transition = pendingTransition
    pendingTransition = nil
    if Portal.onLoad then
        Portal.onLoad(transition.targetMap, transition.targetPortal)
    end
    return true
end

function Portal.cancelTransition()
    if not pendingTransition then
        return false
    end
    pendingTransition = nil
    return true
end

function Portal.resetCooldown()
    cooldown = false
    pendingTransition = nil
end

function Portal.setCooldown()
    cooldown = true
end

return Portal
