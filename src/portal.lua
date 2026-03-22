local Portal = {}
local cooldown = false
local pendingTransition = nil
local routeTagCache = {}
local routeTagOverrides = {}

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
    if routeTagOverrides[key] ~= nil then
        return routeTagOverrides[key] or nil
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

local function collectReachableTargetMaps(Map)
    local reachable = {}
    if type(Map) ~= "table" or type(Map.portals) ~= "table" then
        return reachable
    end
    for _, candidate in ipairs(Map.portals) do
        local targetMap = tostring(candidate and candidate.targetMap or "")
        if targetMap ~= "" then
            reachable[targetMap] = true
        end
    end
    return reachable
end

local function setPendingTransition(portal, Map)
    if not portal then
        pendingTransition = nil
        return
    end
    pendingTransition = {
        sourceMap = tostring(Map and Map.currentMap or ""),
        targetMap = portal.targetMap,
        targetPortal = portal.targetPortal,
        routeTag = resolveMapRouteTag(portal.targetMap),
        reachableTargetMaps = collectReachableTargetMaps(Map),
    }
end

function Portal.check(playerX, playerY, Map)
    local p = Map.getPortalAt(playerX, playerY)
    if p and not cooldown then
        cooldown = true
        setPendingTransition(p, Map)
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

local function resolveAdaptiveAltRoute(routeTag, pressureScore, threatTier, reachableTargetMaps)
    if pressureScore < 4 then
        return nil
    end

    local best = nil
    local currentPressure = resolvePressureScore(routeTag, threatTier)

    if type(reachableTargetMaps) == "table" then
        for targetMap, enabled in pairs(reachableTargetMaps) do
            if enabled then
                local candidateRouteTag = resolveMapRouteTag(targetMap)
                if candidateRouteTag and candidateRouteTag ~= routeTag then
                    local candidatePressure = resolvePressureScore(candidateRouteTag, threatTier)
                    if candidatePressure < currentPressure then
                        if not best or candidatePressure < best.pressure then
                            best = {
                                routeTag = candidateRouteTag,
                                pressure = candidatePressure,
                            }
                        end
                    end
                end
            end
        end
    end

    if best then
        return best.routeTag
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

local function isAltPlanExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ALT_PLAN_NUDGE")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function resolvePortalFxCue(pressureScore)
    if pressureScore >= 5 then
        return "SURGE", "S"
    elseif pressureScore >= 3 then
        return "FLICKER", "F"
    end
    return "CALM", "C"
end

local function buildTransitionPrompt(routeTag, coach, pressureScore, altRouteTag, altDelta, altPlanNudge)
    local fxCue = resolvePortalFxCue(pressureScore)
    local prompt = string.format("PORTAL READY -> ENTER:JUMP  N:CANCEL  NEXT ROUTE:%s  COACH:%s  PRESSURE:%d  FX:%s", routeTag, coach, pressureScore, fxCue)
    if altRouteTag then
        prompt = string.format("%s  ALT ROUTE:%s", prompt, altRouteTag)
        if altDelta then
            prompt = string.format("%s  ALT DELTA:%+d", prompt, altDelta)
        end
        if altPlanNudge then
            prompt = string.format("%s  ALT PLAN:LOWER RISK", prompt)
        end
    end
    return prompt
end

local function buildCompactTransitionPrompt(routeTag, pressureScore, altRouteTag, altDelta, altPlanNudge)
    local _, compactFxCue = resolvePortalFxCue(pressureScore)
    local prompt = string.format("PORTAL READY -> ENTER:JUMP  N:CANCEL  NEXT:%s  COACH:%s  P:%d  FX:%s", routeTag, resolveCompactCoach(routeTag), pressureScore, compactFxCue)
    if altRouteTag then
        prompt = string.format("%s  ALT:%s", prompt, altRouteTag)
        if altDelta then
            prompt = string.format("%s  ADEL:%+d", prompt, altDelta)
        end
        if altPlanNudge then
            prompt = string.format("%s  AP:LOW", prompt)
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
    local altRouteTag = resolveAdaptiveAltRoute(routeTag, pressureScore, threatTier, pendingTransition.reachableTargetMaps)
    local altDelta = resolveAdaptiveAltPressureDelta(routeTag, altRouteTag, threatTier)
    local altPlanNudge = isAltPlanExperimentEnabled() and altRouteTag ~= nil
    local prompt = buildTransitionPrompt(routeTag, coach, pressureScore, altRouteTag, altDelta, altPlanNudge)
    local budget = tonumber(maxChars) or 76
    if budget > 0 and #prompt > budget then
        return buildCompactTransitionPrompt(routeTag, pressureScore, altRouteTag, altDelta, altPlanNudge)
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

function Portal._setRouteTagOverride(mapName, routeTag)
    local key = tostring(mapName or "")
    if key == "" then
        return
    end
    if routeTag == nil then
        routeTagOverrides[key] = nil
        return
    end
    routeTagOverrides[key] = normalizeRouteTag(routeTag) or false
end

return Portal
