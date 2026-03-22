local Portal = {}
local cooldown = false
local pendingTransition = nil
local routeTagCache = {}
local routeTagOverrides = {}
local routeVibeSyncStreak = 0
local pendingVibeSyncDodgeCharges = 0

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

local function resolveRouteVibe(routeTag)
    if routeTag == "SAFE" then
        return "CALM", "C"
    elseif routeTag == "RISK" then
        return "EDGE", "E"
    elseif routeTag == "SPIKE" then
        return "DOOM", "D"
    end
    return "UNKNOWN", "U"
end

local function isRouteVignetteExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ROUTE_VIGNETTE_ASCII")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isRouteVibeConflictExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ROUTE_VIBE_CONFLICT")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function routeTagToExpectedThreatTier(routeTag)
    if routeTag == "SAFE" then
        return "LOW"
    elseif routeTag == "RISK" then
        return "MED"
    elseif routeTag == "SPIKE" then
        return "HIGH"
    end
    return "MED"
end

local function threatTierToRank(threatTier)
    local normalized = normalizeThreatTier(threatTier)
    if normalized == "LOW" then
        return 1
    elseif normalized == "MED" then
        return 2
    end
    return 3
end

local function hasRouteVibeConflict(routeTag, threatTier)
    local expectedTier = routeTagToExpectedThreatTier(routeTag)
    local expectedRank = threatTierToRank(expectedTier)
    local currentRank = threatTierToRank(threatTier)
    return math.abs(expectedRank - currentRank) >= 2
end

local function isRouteVibeConflictReasonExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ROUTE_VIBE_CONFLICT_REASON")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isRouteVibeCoachOverrideExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ROUTE_VIBE_COACH_OVERRIDE")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isRouteVibeSyncExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ROUTE_VIBE_SYNC_HINT")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isRouteVibeSyncDodgeExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ROUTE_VIBE_SYNC_DODGE")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isRouteVibeSnapbackExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ROUTE_VIBE_SNAPBACK")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isRouteVibeThreatAligned(routeTag, threatTier)
    return routeTagToExpectedThreatTier(routeTag) == normalizeThreatTier(threatTier)
end

local function resolveRouteVibeConflictReason(routeTag, threatTier)
    local routeVibe = "UNKNOWN"
    local compactRouteVibe = "U"
    if routeTag == "SAFE" then
        routeVibe = "CALM"
        compactRouteVibe = "C"
    elseif routeTag == "RISK" then
        routeVibe = "EDGE"
        compactRouteVibe = "E"
    elseif routeTag == "SPIKE" then
        routeVibe = "DOOM"
        compactRouteVibe = "D"
    end
    local normalizedThreat = normalizeThreatTier(threatTier)
    local compactThreat = string.sub(normalizedThreat, 1, 1)
    return string.format("%svs%s", routeVibe, normalizedThreat), string.format("%s/%s", compactRouteVibe, compactThreat)
end

local function resolveRouteVignetteGlyph(routeTag)
    if routeTag == "SAFE" then
        return "[]"
    elseif routeTag == "RISK" then
        return "/!\\"
    elseif routeTag == "SPIKE" then
        return "^^^"
    end
    return "???"
end

local function buildTransitionPrompt(routeTag, coach, pressureScore, altRouteTag, altDelta, altPlanNudge, routeVignette, routeVibeConflict, routeVibeConflictReason, coachOverride, vibeSyncHint, vibeSyncChain, vibeSnapback)
    local fxCue = resolvePortalFxCue(pressureScore)
    local routeVibe = resolveRouteVibe(routeTag)
    local prompt = string.format("PORTAL READY -> ENTER:JUMP  N:CANCEL  NEXT ROUTE:%s  COACH:%s  PRESSURE:%d  FX:%s  ROUTE VIBE:%s", routeTag, coach, pressureScore, fxCue, routeVibe)
    if altRouteTag then
        prompt = string.format("%s  ALT ROUTE:%s", prompt, altRouteTag)
        if altDelta then
            prompt = string.format("%s  ALT DELTA:%+d", prompt, altDelta)
        end
        if altPlanNudge then
            prompt = string.format("%s  ALT PLAN:LOWER RISK", prompt)
        end
    end
    if routeVignette then
        prompt = string.format("%s  ROUTE VIGNETTE:%s", prompt, routeVignette)
    end
    if routeVibeConflict then
        prompt = string.format("%s  VIBE CONFLICT:ON", prompt)
        if routeVibeConflictReason then
            prompt = string.format("%s  VIBE WHY:%s", prompt, routeVibeConflictReason)
        end
        if coachOverride then
            prompt = string.format("%s  COACH OVERRIDE:DE-ESCALATE", prompt)
        end
    end
    if vibeSyncChain then
        prompt = string.format("%s  VIBE CHAIN:%d/3", prompt, vibeSyncChain)
    end
    if vibeSyncHint then
        prompt = string.format("%s  VIBE SYNC:+1", prompt)
    end
    if vibeSnapback then
        prompt = string.format("%s  VIBE SNAPBACK:ON", prompt)
    end
    return prompt
end

local function buildCompactTransitionPrompt(routeTag, pressureScore, altRouteTag, altDelta, altPlanNudge, routeVignette, routeVibeConflict, routeVibeConflictReasonCompact, coachOverride, vibeSyncHint, vibeSyncChain, vibeSnapback)
    local _, compactFxCue = resolvePortalFxCue(pressureScore)
    local _, compactRouteVibe = resolveRouteVibe(routeTag)
    local prompt = string.format("PORTAL READY -> ENTER:JUMP  N:CANCEL  NEXT:%s  COACH:%s  P:%d  FX:%s  VIBE:%s", routeTag, resolveCompactCoach(routeTag), pressureScore, compactFxCue, compactRouteVibe)
    if altRouteTag then
        prompt = string.format("%s  ALT:%s", prompt, altRouteTag)
        if altDelta then
            prompt = string.format("%s  ADEL:%+d", prompt, altDelta)
        end
        if altPlanNudge then
            prompt = string.format("%s  AP:LOW", prompt)
        end
    end
    if routeVignette then
        prompt = string.format("%s  RV:%s", prompt, routeVignette)
    end
    if routeVibeConflict then
        prompt = string.format("%s  VC:ON", prompt)
        if routeVibeConflictReasonCompact then
            prompt = string.format("%s  VCWHY:%s", prompt, routeVibeConflictReasonCompact)
        end
        if coachOverride then
            prompt = string.format("%s  COVR:DEESC", prompt)
        end
    end
    if vibeSyncChain then
        prompt = string.format("%s  VSC:%d/3", prompt, vibeSyncChain)
    end
    if vibeSyncHint then
        prompt = string.format("%s  VS:+1", prompt)
    end
    if vibeSnapback then
        prompt = string.format("%s  VSB:ON", prompt)
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
    local routeVignette = nil
    if isRouteVignetteExperimentEnabled() then
        routeVignette = resolveRouteVignetteGlyph(routeTag)
    end
    local routeVibeConflict = false
    local routeVibeConflictReason = nil
    local routeVibeConflictReasonCompact = nil
    if isRouteVibeConflictExperimentEnabled() then
        routeVibeConflict = hasRouteVibeConflict(routeTag, threatTier)
        if routeVibeConflict and isRouteVibeConflictReasonExperimentEnabled() then
            routeVibeConflictReason, routeVibeConflictReasonCompact = resolveRouteVibeConflictReason(routeTag, threatTier)
        end
    end
    if routeVibeConflict and not altRouteTag then
        altRouteTag = resolveAdaptiveAltRoute(routeTag, 4, threatTier, pendingTransition.reachableTargetMaps)
        altDelta = resolveAdaptiveAltPressureDelta(routeTag, altRouteTag, threatTier)
        altPlanNudge = isAltPlanExperimentEnabled() and altRouteTag ~= nil
    end
    local routeVibeAligned = isRouteVibeThreatAligned(routeTag, threatTier)
    pendingTransition.routeVibeAligned = routeVibeAligned
    local syncEnabled = isRouteVibeSyncExperimentEnabled()
    local projectedVibeSyncStreak = routeVibeAligned and (routeVibeSyncStreak + 1) or 0
    if projectedVibeSyncStreak > 3 then
        projectedVibeSyncStreak = 3
    end
    local vibeSyncChain = syncEnabled and projectedVibeSyncStreak or nil
    local vibeSyncHint = syncEnabled and routeVibeAligned and (routeVibeSyncStreak + 1) >= 3
    local vibeSnapback = isRouteVibeSnapbackExperimentEnabled() and syncEnabled and routeVibeAligned == false and routeVibeSyncStreak >= 3
    local coachOverride = isRouteVibeCoachOverrideExperimentEnabled() and routeVibeConflict and altRouteTag ~= nil
    local prompt = buildTransitionPrompt(routeTag, coach, pressureScore, altRouteTag, altDelta, altPlanNudge, routeVignette, routeVibeConflict, routeVibeConflictReason, coachOverride, vibeSyncHint, vibeSyncChain, vibeSnapback)
    local budget = tonumber(maxChars) or 76
    if budget > 0 and #prompt > budget then
        return buildCompactTransitionPrompt(routeTag, pressureScore, altRouteTag, altDelta, altPlanNudge, routeVignette, routeVibeConflict, routeVibeConflictReasonCompact, coachOverride, vibeSyncHint, vibeSyncChain, vibeSnapback)
    end
    return prompt
end

function Portal.confirmTransition()
    if not pendingTransition then
        return false
    end

    local transition = pendingTransition
    local aligned = transition.routeVibeAligned
    local syncEnabled = isRouteVibeSyncExperimentEnabled()
    local syncHintTriggered = syncEnabled and aligned == true and (routeVibeSyncStreak + 1) >= 3
    pendingTransition = nil
    if aligned == true then
        routeVibeSyncStreak = routeVibeSyncStreak + 1
    elseif aligned == false then
        routeVibeSyncStreak = 0
    end
    if syncHintTriggered and isRouteVibeSyncDodgeExperimentEnabled() then
        pendingVibeSyncDodgeCharges = pendingVibeSyncDodgeCharges + 1
    end
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

function Portal.consumeVibeSyncDodgeCharges()
    local charges = math.max(0, math.floor(tonumber(pendingVibeSyncDodgeCharges) or 0))
    pendingVibeSyncDodgeCharges = 0
    return charges
end

function Portal.resetCooldown()
    cooldown = false
    pendingTransition = nil
    routeVibeSyncStreak = 0
    pendingVibeSyncDodgeCharges = 0
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
