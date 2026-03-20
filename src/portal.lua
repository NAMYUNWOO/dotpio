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

local function resolveCompactCoach(routeTag)
    if routeTag == "SAFE" then
        return "LOW"
    elseif routeTag == "RISK" then
        return "MID"
    elseif routeTag == "SPIKE" then
        return "HIGH"
    end
    return "UNK"
end

local function normalizeThreatTier(threatTier)
    local value = string.upper(tostring(threatTier or ""))
    if value == "LOW" or value == "MED" or value == "HIGH" then
        return value
    end
    return "LOW"
end

local function resolveRoutePressureBase(routeTag)
    if routeTag == "SAFE" then
        return 1
    elseif routeTag == "RISK" then
        return 2
    elseif routeTag == "SPIKE" then
        return 3
    end
    return 2
end

local function resolveThreatPressureOffset(threatTier)
    if threatTier == "MED" then
        return 1
    elseif threatTier == "HIGH" then
        return 2
    end
    return 0
end

local function resolvePressureScore(routeTag, threatTier)
    local score = resolveRoutePressureBase(routeTag) + resolveThreatPressureOffset(normalizeThreatTier(threatTier))
    if score < 1 then
        return 1
    elseif score > 5 then
        return 5
    end
    return score
end

local function resolveAdaptiveAltRoute(routeTag, pressureScore)
    if pressureScore < 4 then
        return nil
    end
    if routeTag == "SPIKE" then
        return "RISK"
    elseif routeTag == "RISK" then
        return "SAFE"
    end
    return nil
end

local function resolveAdaptiveAltPressureDelta(routeTag, altRouteTag, threatTier)
    if not altRouteTag then
        return nil
    end
    local currentPressure = resolvePressureScore(routeTag, threatTier)
    local altPressure = resolvePressureScore(altRouteTag, threatTier)
    local delta = altPressure - currentPressure
    if delta >= 0 then
        return nil
    end
    return delta
end

local function buildTransitionPrompt(routeTag, coach, pressureScore, altRouteTag, altDelta)
    local prompt = string.format("PORTAL READY -> ENTER:JUMP  N:CANCEL  NEXT ROUTE:%s  COACH:%s  PRESSURE:%d", routeTag, coach, pressureScore)
    if altRouteTag then
        prompt = string.format("%s  ALT ROUTE:%s", prompt, altRouteTag)
        if altDelta then
            prompt = string.format("%s  ALT DELTA:%+d", prompt, altDelta)
        end
    end
    return prompt
end

local function buildCompactTransitionPrompt(routeTag, pressureScore, altRouteTag, altDelta)
    local prompt = string.format("PORTAL READY -> ENTER:JUMP  N:CANCEL  NEXT:%s  COACH:%s  P:%d", routeTag, resolveCompactCoach(routeTag), pressureScore)
    if altRouteTag then
        prompt = string.format("%s  ALT:%s", prompt, altRouteTag)
        if altDelta then
            prompt = string.format("%s  ADEL:%+d", prompt, altDelta)
        end
    end
    return prompt
end

function Portal.getTransitionPrompt(maxChars, context)
    if not pendingTransition then
        return nil
    end
    local routeTag = pendingTransition.routeTag or "UNKNOWN"
    local coach = resolveRouteCoach(routeTag)
    local threatTier = context and context.threatTier or nil
    local pressureScore = resolvePressureScore(routeTag, threatTier)
    local altRouteTag = resolveAdaptiveAltRoute(routeTag, pressureScore)
    local altDelta = resolveAdaptiveAltPressureDelta(routeTag, altRouteTag, threatTier)
    local prompt = buildTransitionPrompt(routeTag, coach, pressureScore, altRouteTag, altDelta)
    local budget = tonumber(maxChars) or 76
    if budget > 0 and #prompt > budget then
        return buildCompactTransitionPrompt(routeTag, pressureScore, altRouteTag, altDelta)
    end
    return prompt
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
