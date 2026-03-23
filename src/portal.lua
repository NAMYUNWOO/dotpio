local Portal = {}
local cooldown = false
local pendingTransition = nil
local routeTagCache = {}
local routeTagOverrides = {}
local routeVibeSyncStreak = 0
local pendingVibeSyncDodgeCharges = 0
local routeVibeRecoveryArmed = false
local routeVibeRecoveryStreak = 0
local routeVibeConflictAge = 999
local routeVibeSnapbackAge = 999

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

local function resolveAltStepCue(pressureScore, altRouteTag, altDelta)
    if not altRouteTag then
        return nil
    end
    if altRouteTag == "SAFE" or (altDelta and altDelta <= -2) then
        return "SAFE"
    end
    if altRouteTag == "RISK" then
        if pressureScore >= 5 then
            return "BAIT"
        end
        return "PUSH"
    end
    return "PUSH"
end

local function resolveAltStepConfidence(pressureScore, altStepCue, altDelta)
    if not altStepCue then
        return nil
    end
    if altStepCue == "SAFE" then
        if altDelta and altDelta <= -2 then
            return "HIGH"
        end
        return pressureScore >= 5 and "MID" or "HIGH"
    end
    if altStepCue == "BAIT" then
        return pressureScore >= 5 and "MID" or "LOW"
    end
    return "LOW"
end

local function resolveAltStepWhy(pressureScore, altStepCue, altStepConfidence, altDelta)
    if not altStepCue then
        return nil
    end

    if altStepCue == "SAFE" then
        if altDelta and altDelta <= -2 then
            return "RISK-DROP"
        end
        if altStepConfidence == "HIGH" then
            return "STABILIZE"
        end
        return "SOFTEN"
    end

    if altStepCue == "BAIT" then
        if pressureScore >= 5 then
            return "PRESSURE"
        end
        return "LURE"
    end

    if altStepConfidence == "LOW" then
        return "CONF-LOW"
    end
    return "MOMENTUM"
end

local function resolveAltStepWhyConfidence(altStepWhy, altStepConfidence)
    if not altStepWhy then
        return nil
    end
    if altStepWhy == "RISK-DROP" or altStepWhy == "STABILIZE" then
        return "HIGH"
    end
    if altStepWhy == "PRESSURE" or altStepWhy == "SOFTEN" then
        return "MID"
    end
    if altStepConfidence == "HIGH" then
        return "MID"
    end
    return "LOW"
end

local function resolveAltStepWhyGlyph(altStepWhy)
    if not altStepWhy then
        return nil
    end
    local glyphByWhy = {
        ["RISK-DROP"] = "v",
        ["STABILIZE"] = "=",
        ["SOFTEN"] = "~",
        ["PRESSURE"] = "!",
        ["LURE"] = "?",
        ["CONF-LOW"] = "-",
        ["MOMENTUM"] = "+",
    }
    return glyphByWhy[altStepWhy] or "."
end

local function isAltPlanExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ALT_PLAN_NUDGE")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isAltStepMicroCueExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ALT_STEP_CUE")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isAltStepConfidenceExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ALT_STEP_CONF")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isAltStepWhyExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ALT_STEP_WHY")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isAltStepWhyConfidenceExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ALT_STEP_WHY_CONF")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isAltStepWhyGlyphExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ALT_WHY_GLYPH")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isAltStepWhyGlyphModeExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ALT_WHY_GLYPH_MODE")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isAltStepWhyGlyphCompactAliasExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ALT_WHY_GLYPH_COMPACT")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isAltStepWhyGlyphModeCompactAliasExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ALT_WHY_GLYPH_MODE_COMPACT")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isAltStepWhyGlyphModeConfidenceCompactAliasExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ALT_WHY_GLYPH_MODE_CONF_COMPACT")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isRoutePulseLinkCompactPromptExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ROUTE_PULSE_LINK_PROMPT")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isRoutePulseModeCompactPromptExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ROUTE_PULSE_MODE_PROMPT")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isRoutePulseFitCompactPromptExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ROUTE_PULSE_FIT_PROMPT")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isRoutePulseFlareCompactPromptExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ROUTE_PULSE_FLARE_PROMPT")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isPulseHeatCompactPromptExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_PULSE_HEAT_CUE")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isPulseHeatFxCompactPromptExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_PULSE_HEAT_FX")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function resolveCompactPulseTokenPriorityMode()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ROUTE_PULSE_TOKEN_PRIORITY")
    if not raw then
        return nil
    end
    local normalized = string.upper(tostring(raw))
    if normalized == "FIT-FIRST" or normalized == "MODE-FIRST" then
        return normalized
    end
    return nil
end

local function resolvePortalFxCue(pressureScore)
    if pressureScore >= 5 then
        return "SURGE", "S"
    elseif pressureScore >= 3 then
        return "FLICKER", "F"
    end
    return "CALM", "C"
end

local function resolveCompactRoutePulseLink(pressureScore, altRouteTag)
    if pressureScore >= 4 or altRouteTag ~= nil then
        return "H"
    end
    return "S"
end

local function resolveRoutePulseMode(pressureScore, altRouteTag)
    if pressureScore >= 5 then
        return "SURGE"
    end
    if pressureScore >= 4 or altRouteTag ~= nil then
        return "SUSTAIN"
    end
    return "IDLE"
end

local function resolveCompactRoutePulseMode(pressureScore, altRouteTag, compactPulseLink)
    if pressureScore >= 5 then
        return "X"
    end
    if compactPulseLink == "H" or pressureScore >= 4 or altRouteTag ~= nil then
        return "S"
    end
    return "I"
end

local function resolveCompactRoutePulseFit(pressureScore, altRouteTag, compactPulseMode, compactPulseLink)
    local mode = compactPulseMode
    if mode == nil then
        mode = resolveCompactRoutePulseMode(pressureScore, altRouteTag, compactPulseLink)
    end
    if mode == "I" then
        return "Y"
    elseif mode == "X" then
        return "R"
    elseif mode == "S" then
        if altRouteTag ~= nil and pressureScore >= 4 then
            return "B"
        end
        return "W"
    end
    return "W"
end

local function resolveCompactPulseFlare(compactPulseMode, compactPulseFit)
    if compactPulseMode ~= "X" then
        return nil
    end
    if compactPulseFit == "B" or compactPulseFit == "R" then
        return "+"
    end
    return nil
end

local function resolveCompactPulseHeat(pressureScore, compactPulseMode)
    if compactPulseMode == "X" or pressureScore >= 5 then
        return "HOT"
    end
    if compactPulseMode == "S" or pressureScore >= 3 then
        return "WARM"
    end
    return "COOL"
end

local function resolveCompactPulseHeatFx(compactPulseHeat)
    if compactPulseHeat == "HOT" then
        return "BLAZE"
    elseif compactPulseHeat == "WARM" then
        return "SPARK"
    elseif compactPulseHeat == "COOL" then
        return "CALM"
    end
    return nil
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

local function isRouteVibeRecoveryExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ROUTE_VIBE_RECOVERY_HINT")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isRouteVibeResilienceExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ROUTE_VIBE_RESILIENCE")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isRouteVibeDriftAlarmExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ROUTE_VIBE_DRIFT_ALARM")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end


local function isRouteVibeDriftGlyphExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ROUTE_VIBE_DRIFT_GLYPH")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function resolveRouteVibeDriftGlyph(routeVibeConflict, vibeSnapback)
    if not isRouteVibeDriftGlyphExperimentEnabled() then
        return nil
    end
    local shortestWindow = 1
    local shortWindow = 2

    if routeVibeConflict and vibeSnapback then
        return "!!!", "!!!"
    end
    if routeVibeConflict and routeVibeSnapbackAge <= shortestWindow then
        return "!!!", "!!!"
    end
    if vibeSnapback and routeVibeConflictAge <= shortestWindow then
        return "!!!", "!!!"
    end
    if routeVibeConflict and routeVibeSnapbackAge <= shortWindow then
        return "!!", "!!"
    end
    if vibeSnapback and routeVibeConflictAge <= shortWindow then
        return "!!", "!!"
    end
    if routeVibeConflict or vibeSnapback then
        return "!", "!"
    end
    return nil
end
local function shouldEmitRouteVibeDriftAlarm(routeVibeConflict, vibeSnapback)
    if not isRouteVibeDriftAlarmExperimentEnabled() then
        return false
    end
    local shortWindow = 2
    if routeVibeConflict and vibeSnapback then
        return true
    end
    if routeVibeConflict and routeVibeSnapbackAge <= shortWindow then
        return true
    end
    if vibeSnapback and routeVibeConflictAge <= shortWindow then
        return true
    end
    return false
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


local function isPortalVibeTrailExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function normalizeVibeTrail(vibeTrail)
    local value = string.upper(tostring(vibeTrail or ""))
    if value == "CALM" or value == "ASH" then
        return value
    end
    return nil
end

local function resolveCompactVibeTrail(vibeTrail)
    if vibeTrail == "CALM" then
        return "C"
    elseif vibeTrail == "ASH" then
        return "A"
    end
    return nil
end

local function isPortalVibeTrailConfidenceExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_CONF")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isPortalVibeTrailConfidenceRailExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_CONF_RAIL")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isPortalVibeTrailWhyExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function resolveVibeTrailWhy(vibeTrail)
    if vibeTrail == "CALM" then
        return "RECOVER"
    elseif vibeTrail == "ASH" then
        return "SCAR"
    end
    return nil
end

local function isPortalVibeTrailWhyConfidenceExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY_CONF")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function resolveVibeTrailWhyConfidence(vibeTrail, vibeTrailWhy)
    if not vibeTrailWhy then
        return nil
    end
    if vibeTrail == "ASH" then
        return "HIGH"
    elseif vibeTrail == "CALM" then
        return "MID"
    end
    return "LOW"
end

local function resolveCompactVibeTrailWhyConfidence(vibeTrailWhyConfidence)
    if vibeTrailWhyConfidence == "HIGH" then
        return "H"
    elseif vibeTrailWhyConfidence == "MID" then
        return "M"
    elseif vibeTrailWhyConfidence == "LOW" then
        return "L"
    end
    return nil
end

local function isPortalVibeTrailWhyConfidenceWhyExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY_CONF_WHY")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function resolveVibeTrailWhyConfidenceWhy(vibeTrailWhy, vibeTrailWhyConfidence)
    if vibeTrailWhy == nil or vibeTrailWhyConfidence == nil then
        return nil
    end
    if vibeTrailWhy == "SCAR" and vibeTrailWhyConfidence == "HIGH" then
        return "LOCKED"
    end
    if vibeTrailWhy == "RECOVER" and vibeTrailWhyConfidence == "MID" then
        return "TREND"
    end
    if vibeTrailWhyConfidence == "LOW" then
        return "THIN"
    end
    return "MIXED"
end

local function isPortalVibeTrailWhyConfidenceWhyConfidenceExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY_CONF_WHY_CONF")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function resolveVibeTrailWhyConfidenceWhyConfidence(vibeTrailWhyConfidenceWhy)
    if vibeTrailWhyConfidenceWhy == "LOCKED" then
        return "HIGH"
    elseif vibeTrailWhyConfidenceWhy == "TREND" then
        return "MID"
    elseif vibeTrailWhyConfidenceWhy ~= nil then
        return "LOW"
    end
    return nil
end

local function resolveCompactVibeTrailWhyConfidenceWhyConfidence(vibeTrailWhyConfidenceWhyConfidence)
    if vibeTrailWhyConfidenceWhyConfidence == "HIGH" then
        return "H"
    elseif vibeTrailWhyConfidenceWhyConfidence == "MID" then
        return "M"
    elseif vibeTrailWhyConfidenceWhyConfidence == "LOW" then
        return "L"
    end
    return nil
end

local function isPortalVibeTrailWhyConfidenceWhyRailExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY_CONF_WHY_RAIL")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function resolveVibeTrailWhyConfidenceWhyRail(vibeTrailWhyConfidenceWhy)
    if vibeTrailWhyConfidenceWhy == "LOCKED" then
        return "SPIKE"
    elseif vibeTrailWhyConfidenceWhy ~= nil then
        return "STEADY"
    end
    return nil
end

local function resolveCompactVibeTrailWhyConfidenceWhyRail(vibeTrailWhyConfidenceWhyRail)
    if vibeTrailWhyConfidenceWhyRail == "SPIKE" then
        return "X"
    elseif vibeTrailWhyConfidenceWhyRail == "STEADY" then
        return "S"
    end
    return nil
end

local function isPortalVibeTrailWhyCompactAliasExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_WHY_COMPACT_ALIAS")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function resolveVibeTrailWhyTokenLabel(compact)
    if compact and isPortalVibeTrailWhyCompactAliasExperimentEnabled() then
        return "VTW"
    end
    return "VIBE TRAIL WHY"
end

local function isPortalVibeTrailArcExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_PORTAL_VIBE_TRAIL_ARC")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isRouteGlowCompactPromptExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isRouteGlowConfidenceCompactPromptExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_CONF")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isRouteGlowFxCompactPromptExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isRouteGlowFxConfidenceCompactPromptExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_CONF")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isRouteGlowFxCompactAliasExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_FX_COMPACT")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function isRouteGlowConfidenceCompactAliasExperimentEnabled()
    local raw = os.getenv("DOTPIO_EXPERIMENT_ROUTE_GLOW_CONF_COMPACT")
    if not raw then
        return false
    end
    local value = string.lower(tostring(raw))
    return value == "1" or value == "true" or value == "on" or value == "yes"
end

local function resolveVibeTrailArc(vibeTrailWhy)
    if vibeTrailWhy == "RECOVER" then
        return "RECOVER"
    elseif vibeTrailWhy == "SCAR" then
        return "SCAR"
    elseif vibeTrailWhy ~= nil then
        return "MIXED"
    end
    return nil
end

local function resolveCompactVibeTrailArc(vibeTrailArc)
    if vibeTrailArc == "RECOVER" then
        return "R"
    elseif vibeTrailArc == "SCAR" then
        return "S"
    elseif vibeTrailArc == "MIXED" then
        return "M"
    end
    return nil
end

local function resolveCompactRouteGlow(vibeTrailArc)
    if vibeTrailArc == "RECOVER" then
        return "SOFT"
    elseif vibeTrailArc == "SCAR" or vibeTrailArc == "MIXED" then
        return "SHARP"
    end
    return nil
end

local function resolveRouteGlowConfidence(vibeTrailArc)
    if vibeTrailArc == "SCAR" then
        return "HIGH"
    elseif vibeTrailArc == "RECOVER" then
        return "MID"
    elseif vibeTrailArc == "MIXED" then
        return "LOW"
    end
    return nil
end

local function resolveCompactRouteGlowFx(compactRouteGlow, compactPulseHeat)
    if compactRouteGlow == nil then
        return nil
    end
    if compactPulseHeat == "HOT" then
        return "SURGE"
    end
    if compactRouteGlow == "SOFT" then
        return "SOFT"
    end
    return "SHARP"
end

local function resolveRouteGlowFxConfidence(compactRouteGlowFx)
    if compactRouteGlowFx == "SURGE" then
        return "HIGH"
    elseif compactRouteGlowFx == "SHARP" then
        return "MID"
    elseif compactRouteGlowFx == "SOFT" then
        return "LOW"
    end
    return nil
end

local function resolveCompactRouteGlowFxConfidence(routeGlowFxConfidence)
    if routeGlowFxConfidence == "HIGH" then
        return "H"
    elseif routeGlowFxConfidence == "MID" then
        return "M"
    elseif routeGlowFxConfidence == "LOW" then
        return "L"
    end
    return nil
end

local function resolveVibeTrailConfidence(vibeTrail)
    if vibeTrail == "ASH" then
        return "HIGH"
    elseif vibeTrail == "CALM" then
        return "MID"
    end
    return nil
end

local function resolveCompactVibeTrailConfidence(vibeTrailConfidence)
    if vibeTrailConfidence == "HIGH" then
        return "H"
    elseif vibeTrailConfidence == "MID" then
        return "M"
    elseif vibeTrailConfidence == "LOW" then
        return "L"
    end
    return nil
end


local function resolveVibeTrailConfidenceRail(vibeTrailConfidence)
    if vibeTrailConfidence == "HIGH" then
        return "SPIKE"
    elseif vibeTrailConfidence == "MID" or vibeTrailConfidence == "LOW" then
        return "STEADY"
    end
    return nil
end

local function resolveCompactVibeTrailConfidenceRail(vibeTrailConfidenceRail)
    if vibeTrailConfidenceRail == "SPIKE" then
        return "X"
    elseif vibeTrailConfidenceRail == "STEADY" then
        return "S"
    end
    return nil
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

local function buildTransitionPrompt(routeTag, coach, pressureScore, altRouteTag, altDelta, altPlanNudge, altStepCue, altStepConfidence, altStepWhy, altStepWhyConfidence, altStepWhyGlyph, altStepWhyGlyphMode, routeVignette, routeVibeConflict, routeVibeConflictReason, coachOverride, vibeSyncHint, vibeSyncChain, vibeSnapback, vibeRecovery, vibeResilience, vibeDriftWide, vibeDriftGlyph, routePulseMode, vibeTrail, vibeTrailConfidence, vibeTrailConfidenceRail, vibeTrailWhy, vibeTrailArc, vibeTrailWhyConfidence, vibeTrailWhyConfidenceWhy, vibeTrailWhyConfidenceWhyConfidence, vibeTrailWhyConfidenceWhyRail)
    local fxCue = resolvePortalFxCue(pressureScore)
    local routeVibe = resolveRouteVibe(routeTag)
    local prompt = string.format("PORTAL READY -> ENTER:JUMP  N:CANCEL  NEXT ROUTE:%s  COACH:%s  PRESSURE:%d  FX:%s  ROUTE VIBE:%s", routeTag, coach, pressureScore, fxCue, routeVibe)
    if routePulseMode then
        prompt = string.format("%s  ROUTE PULSE MODE:%s", prompt, routePulseMode)
    end
    if vibeTrail then
        prompt = string.format("%s  VIBE TRAIL:%s", prompt, vibeTrail)
        if vibeTrailConfidence then
            prompt = string.format("%s  VIBE TRAIL CONF:%s", prompt, vibeTrailConfidence)
            if vibeTrailConfidenceRail then
                prompt = string.format("%s  VIBE TRAIL CONF RAIL:%s", prompt, vibeTrailConfidenceRail)
            end
        end
        if vibeTrailWhy then
            prompt = string.format("%s  %s:%s", prompt, resolveVibeTrailWhyTokenLabel(false), vibeTrailWhy)
            if vibeTrailArc then
                prompt = string.format("%s  VIBE TRAIL ARC:%s", prompt, vibeTrailArc)
            end
            if vibeTrailWhyConfidence then
                prompt = string.format("%s  VIBE TRAIL WHY CONF:%s", prompt, vibeTrailWhyConfidence)
                if vibeTrailWhyConfidenceWhy then
                    prompt = string.format("%s  VIBE TRAIL WHY CONF WHY:%s", prompt, vibeTrailWhyConfidenceWhy)
                    if vibeTrailWhyConfidenceWhyConfidence then
                        prompt = string.format("%s  VIBE TRAIL WHY CONF WHY CONF:%s", prompt, vibeTrailWhyConfidenceWhyConfidence)
                    end
                    if vibeTrailWhyConfidenceWhyRail then
                        prompt = string.format("%s  VIBE TRAIL WHY CONF WHY RAIL:%s", prompt, vibeTrailWhyConfidenceWhyRail)
                    end
                end
            end
        end
    end
    if altRouteTag then
        prompt = string.format("%s  ALT ROUTE:%s", prompt, altRouteTag)
        if altDelta then
            prompt = string.format("%s  ALT DELTA:%+d", prompt, altDelta)
        end
        if altPlanNudge then
            prompt = string.format("%s  ALT PLAN:LOWER RISK", prompt)
        end
        if altStepCue then
            prompt = string.format("%s  ALT STEP:%s", prompt, altStepCue)
            if altStepConfidence then
                prompt = string.format("%s  ALT STEP CONF:%s", prompt, altStepConfidence)
            end
            if altStepWhy then
                prompt = string.format("%s  ALT STEP WHY:%s", prompt, altStepWhy)
                if altStepWhyConfidence then
                    prompt = string.format("%s  ALT STEP WHY CONF:%s", prompt, altStepWhyConfidence)
                end
                if altStepWhyGlyph then
                    prompt = string.format("%s  ALT WHY GLYPH:%s", prompt, altStepWhyGlyph)
                end
                if altStepWhyGlyphMode then
                    prompt = string.format("%s  ALT WHY GLYPH MODE:%s", prompt, altStepWhyGlyphMode)
                end
            end
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
    if vibeRecovery then
        prompt = string.format("%s  VIBE RECOVER:READY", prompt)
        if vibeResilience then
            prompt = string.format("%s  VIBE RESILIENCE:%d", prompt, vibeResilience)
        end
    end
    if vibeDriftWide then
        prompt = string.format("%s  VIBE DRIFT:WIDE", prompt)
        if vibeDriftGlyph then
            prompt = string.format("%s  DRIFT GLYPH:%s", prompt, vibeDriftGlyph)
        end
    end
    return prompt
end

local function buildCompactTransitionPrompt(routeTag, pressureScore, altRouteTag, altDelta, altPlanNudge, altStepCue, altStepConfidence, altStepWhy, altStepWhyConfidence, altStepWhyGlyph, altStepWhyGlyphMode, routeVignette, routeVibeConflict, routeVibeConflictReasonCompact, coachOverride, vibeSyncHint, vibeSyncChain, vibeSnapback, vibeRecovery, vibeResilience, vibeDriftWide, vibeDriftGlyphCompact, compactPulseLink, compactPulseMode, compactPulseFit, compactPulseFlare, compactPulseHeat, compactPulseHeatFx, compactVibeTrail, compactVibeTrailConfidence, compactVibeTrailConfidenceRail, vibeTrailWhy, compactVibeTrailArc, compactRouteGlow, compactRouteGlowConfidence, compactRouteGlowFx, compactRouteGlowFxConfidence, compactVibeTrailWhyConfidence, vibeTrailWhyConfidenceWhy, compactVibeTrailWhyConfidenceWhyConfidence, compactVibeTrailWhyConfidenceWhyRail, maxChars)
    local _, compactFxCue = resolvePortalFxCue(pressureScore)
    local _, compactRouteVibe = resolveRouteVibe(routeTag)
    local prompt = string.format("PORTAL READY -> ENTER:JUMP  N:CANCEL  NEXT:%s  COACH:%s  P:%d  FX:%s  VIBE:%s", routeTag, resolveCompactCoach(routeTag), pressureScore, compactFxCue, compactRouteVibe)
    local budget = tonumber(maxChars) or 0
    local function appendToken(token, enforceBudget)
        if not token then
            return
        end
        local chunk = "  " .. token
        if enforceBudget and budget > 0 and (#prompt + #chunk) > budget then
            return
        end
        prompt = prompt .. chunk
    end

    if compactPulseLink then
        appendToken(string.format("PULSE LINK:%s", compactPulseLink), false)
    end

    local pulsePriorityMode = resolveCompactPulseTokenPriorityMode()
    local enforcePulseBudget = pulsePriorityMode ~= nil
    local compactPulsePriorityCue = nil
    if pulsePriorityMode == "FIT-FIRST" then
        compactPulsePriorityCue = "F"
    elseif pulsePriorityMode == "MODE-FIRST" then
        compactPulsePriorityCue = "M"
    end
    appendToken(compactPulsePriorityCue and string.format("PRI:%s", compactPulsePriorityCue) or nil, enforcePulseBudget)

    if pulsePriorityMode == "FIT-FIRST" then
        appendToken(compactPulseFit and string.format("PULSE FIT:%s", compactPulseFit) or nil, enforcePulseBudget)
        appendToken(compactPulseMode and string.format("PULSE MODE:%s", compactPulseMode) or nil, enforcePulseBudget)
    else
        appendToken(compactPulseMode and string.format("PULSE MODE:%s", compactPulseMode) or nil, enforcePulseBudget)
        appendToken(compactPulseFit and string.format("PULSE FIT:%s", compactPulseFit) or nil, enforcePulseBudget)
    end

    if compactPulseFlare then
        appendToken(string.format("PULSE FLARE:%s", compactPulseFlare), false)
    end
    if compactPulseHeat then
        appendToken(string.format("PULSE HEAT:%s", compactPulseHeat), false)
    end
    if compactPulseHeatFx then
        appendToken(string.format("PULSE HEAT FX:%s", compactPulseHeatFx), false)
    end
    if compactVibeTrail then
        appendToken(string.format("VTR:%s", compactVibeTrail), false)
        if compactVibeTrailConfidence then
            appendToken(string.format("VTC:%s", compactVibeTrailConfidence), false)
            if compactVibeTrailConfidenceRail then
                appendToken(string.format("VTCR:%s", compactVibeTrailConfidenceRail), false)
            end
        end
        if vibeTrailWhy then
            appendToken(string.format("%s:%s", resolveVibeTrailWhyTokenLabel(true), vibeTrailWhy), false)
            if compactVibeTrailArc then
                appendToken(string.format("VTA:%s", compactVibeTrailArc), false)
                if compactRouteGlow then
                    appendToken(string.format("ROUTE GLOW:%s", compactRouteGlow), false)
                    if compactRouteGlowConfidence then
                        local routeGlowConfidenceTokenLabel = isRouteGlowConfidenceCompactAliasExperimentEnabled() and "RGC" or "ROUTE GLOW CONF"
                        appendToken(string.format("%s:%s", routeGlowConfidenceTokenLabel, compactRouteGlowConfidence), false)
                    end
                    if compactRouteGlowFx then
                        local routeGlowFxTokenLabel = isRouteGlowFxCompactAliasExperimentEnabled() and "RGFX" or "ROUTE GLOW FX"
                        appendToken(string.format("%s:%s", routeGlowFxTokenLabel, compactRouteGlowFx), false)
                        if compactRouteGlowFxConfidence then
                            appendToken(string.format("RGFXC:%s", compactRouteGlowFxConfidence), false)
                        end
                    end
                end
            end
            if compactVibeTrailWhyConfidence then
                appendToken(string.format("VTWC:%s", compactVibeTrailWhyConfidence), false)
                if vibeTrailWhyConfidenceWhy then
                    appendToken(string.format("VTCW:%s", vibeTrailWhyConfidenceWhy), false)
                    if compactVibeTrailWhyConfidenceWhyConfidence then
                        appendToken(string.format("VTCWC:%s", compactVibeTrailWhyConfidenceWhyConfidence), false)
                    end
                    if compactVibeTrailWhyConfidenceWhyRail then
                        appendToken(string.format("VTCWR:%s", compactVibeTrailWhyConfidenceWhyRail), false)
                    end
                end
            end
        end
    end
    if altRouteTag then
        prompt = string.format("%s  ALT:%s", prompt, altRouteTag)
        if altDelta then
            prompt = string.format("%s  ADEL:%+d", prompt, altDelta)
        end
        if altPlanNudge then
            prompt = string.format("%s  AP:LOW", prompt)
        end
        if altStepCue then
            prompt = string.format("%s  ALT STEP:%s", prompt, altStepCue)
            if altStepConfidence then
                prompt = string.format("%s  ALT STEP CONF:%s", prompt, altStepConfidence)
            end
            if altStepWhy then
                prompt = string.format("%s  ALT STEP WHY:%s", prompt, altStepWhy)
                if altStepWhyConfidence then
                    local altStepWhyConfTokenLabel = isAltStepWhyGlyphModeConfidenceCompactAliasExperimentEnabled() and "AWGMC" or "ALT STEP WHY CONF"
                    prompt = string.format("%s  %s:%s", prompt, altStepWhyConfTokenLabel, altStepWhyConfidence)
                end
                if altStepWhyGlyph then
                    local glyphTokenLabel = isAltStepWhyGlyphCompactAliasExperimentEnabled() and "AWG" or "ALT WHY GLYPH"
                    prompt = string.format("%s  %s:%s", prompt, glyphTokenLabel, altStepWhyGlyph)
                end
                if altStepWhyGlyphMode then
                    local glyphModeTokenLabel = isAltStepWhyGlyphModeCompactAliasExperimentEnabled() and "AWGM" or "ALT WHY GLYPH MODE"
                    prompt = string.format("%s  %s:%s", prompt, glyphModeTokenLabel, altStepWhyGlyphMode)
                end
            end
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
    if vibeRecovery then
        prompt = string.format("%s  VR:OK", prompt)
        if vibeResilience then
            prompt = string.format("%s  VRES:%d", prompt, vibeResilience)
        end
    end
    if vibeDriftWide then
        prompt = string.format("%s  VDR:WIDE", prompt)
        if vibeDriftGlyphCompact then
            prompt = string.format("%s  DGL:%s", prompt, vibeDriftGlyphCompact)
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
    local altStepCue = nil
    if isAltStepMicroCueExperimentEnabled() then
        altStepCue = resolveAltStepCue(pressureScore, altRouteTag, altDelta)
    end
    local altStepConfidence = nil
    if isAltStepConfidenceExperimentEnabled() then
        altStepConfidence = resolveAltStepConfidence(pressureScore, altStepCue, altDelta)
    end
    local altStepWhy = nil
    if isAltStepWhyExperimentEnabled() then
        altStepWhy = resolveAltStepWhy(pressureScore, altStepCue, altStepConfidence, altDelta)
    end
    local altStepWhyConfidence = nil
    if isAltStepWhyConfidenceExperimentEnabled() then
        altStepWhyConfidence = resolveAltStepWhyConfidence(altStepWhy, altStepConfidence)
    end
    local altStepWhyGlyph = nil
    if isAltStepWhyGlyphExperimentEnabled() then
        altStepWhyGlyph = resolveAltStepWhyGlyph(altStepWhy)
    end
    local altStepWhyGlyphMode = nil
    if isAltStepWhyGlyphModeExperimentEnabled() and altStepWhyGlyph then
        altStepWhyGlyphMode = altStepWhy == "PRESSURE" and "SPIKE" or "STEADY"
    end
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
        if isAltStepMicroCueExperimentEnabled() then
            altStepCue = resolveAltStepCue(pressureScore, altRouteTag, altDelta)
        end
        if isAltStepConfidenceExperimentEnabled() then
            altStepConfidence = resolveAltStepConfidence(pressureScore, altStepCue, altDelta)
        end
        if isAltStepWhyExperimentEnabled() then
            altStepWhy = resolveAltStepWhy(pressureScore, altStepCue, altStepConfidence, altDelta)
        end
        if isAltStepWhyConfidenceExperimentEnabled() then
            altStepWhyConfidence = resolveAltStepWhyConfidence(altStepWhy, altStepConfidence)
        end
        if isAltStepWhyGlyphExperimentEnabled() then
            altStepWhyGlyph = resolveAltStepWhyGlyph(altStepWhy)
        end
        if isAltStepWhyGlyphModeExperimentEnabled() and altStepWhyGlyph then
            altStepWhyGlyphMode = altStepWhy == "PRESSURE" and "SPIKE" or "STEADY"
        end
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
    local vibeRecovery = isRouteVibeRecoveryExperimentEnabled() and routeVibeRecoveryArmed and routeVibeAligned == true
    pendingTransition.vibeRecovery = vibeRecovery
    local vibeResilience = nil
    if vibeRecovery and isRouteVibeResilienceExperimentEnabled() then
        vibeResilience = routeVibeRecoveryStreak + 1
        pendingTransition.vibeResilience = vibeResilience
    else
        pendingTransition.vibeResilience = nil
    end
    local vibeDriftWide = shouldEmitRouteVibeDriftAlarm(routeVibeConflict, vibeSnapback)
    local vibeDriftGlyph, vibeDriftGlyphCompact = resolveRouteVibeDriftGlyph(routeVibeConflict, vibeSnapback)
    pendingTransition.routeVibeConflict = routeVibeConflict
    pendingTransition.vibeSnapback = vibeSnapback
    local coachOverride = isRouteVibeCoachOverrideExperimentEnabled() and routeVibeConflict and altRouteTag ~= nil
    local routePulseMode = nil
    if isRoutePulseModeCompactPromptExperimentEnabled() then
        routePulseMode = resolveRoutePulseMode(pressureScore, altRouteTag)
    end
    local vibeTrail = nil
    local vibeTrailConfidence = nil
    local vibeTrailConfidenceRail = nil
    local vibeTrailWhy = nil
    local vibeTrailArc = nil
    local vibeTrailWhyConfidence = nil
    local vibeTrailWhyConfidenceWhy = nil
    local vibeTrailWhyConfidenceWhyConfidence = nil
    local vibeTrailWhyConfidenceWhyRail = nil
    if isPortalVibeTrailExperimentEnabled() then
        vibeTrail = normalizeVibeTrail(context and context.vibeTrail or nil)
        if isPortalVibeTrailConfidenceExperimentEnabled() then
            vibeTrailConfidence = resolveVibeTrailConfidence(vibeTrail)
            if isPortalVibeTrailConfidenceRailExperimentEnabled() then
                vibeTrailConfidenceRail = resolveVibeTrailConfidenceRail(vibeTrailConfidence)
            end
        end
        if isPortalVibeTrailWhyExperimentEnabled() then
            vibeTrailWhy = resolveVibeTrailWhy(vibeTrail)
            if isPortalVibeTrailArcExperimentEnabled() then
                vibeTrailArc = resolveVibeTrailArc(vibeTrailWhy)
            end
            if isPortalVibeTrailWhyConfidenceExperimentEnabled() then
                vibeTrailWhyConfidence = resolveVibeTrailWhyConfidence(vibeTrail, vibeTrailWhy)
                if isPortalVibeTrailWhyConfidenceWhyExperimentEnabled() then
                    vibeTrailWhyConfidenceWhy = resolveVibeTrailWhyConfidenceWhy(vibeTrailWhy, vibeTrailWhyConfidence)
                    if isPortalVibeTrailWhyConfidenceWhyConfidenceExperimentEnabled() then
                        vibeTrailWhyConfidenceWhyConfidence = resolveVibeTrailWhyConfidenceWhyConfidence(vibeTrailWhyConfidenceWhy)
                    end
                    if isPortalVibeTrailWhyConfidenceWhyRailExperimentEnabled() then
                        vibeTrailWhyConfidenceWhyRail = resolveVibeTrailWhyConfidenceWhyRail(vibeTrailWhyConfidenceWhy)
                    end
                end
            end
        end
    end
    local prompt = buildTransitionPrompt(routeTag, coach, pressureScore, altRouteTag, altDelta, altPlanNudge, altStepCue, altStepConfidence, altStepWhy, altStepWhyConfidence, altStepWhyGlyph, altStepWhyGlyphMode, routeVignette, routeVibeConflict, routeVibeConflictReason, coachOverride, vibeSyncHint, vibeSyncChain, vibeSnapback, vibeRecovery, vibeResilience, vibeDriftWide, vibeDriftGlyph, routePulseMode, vibeTrail, vibeTrailConfidence, vibeTrailConfidenceRail, vibeTrailWhy, vibeTrailArc, vibeTrailWhyConfidence, vibeTrailWhyConfidenceWhy, vibeTrailWhyConfidenceWhyConfidence, vibeTrailWhyConfidenceWhyRail)
    local budget = tonumber(maxChars) or 76
    if budget > 0 and #prompt > budget then
        local compactPulseLink = nil
        if isRoutePulseLinkCompactPromptExperimentEnabled() then
            compactPulseLink = resolveCompactRoutePulseLink(pressureScore, altRouteTag)
        end
        local compactPulseMode = nil
        if isRoutePulseModeCompactPromptExperimentEnabled() then
            compactPulseMode = resolveCompactRoutePulseMode(pressureScore, altRouteTag, compactPulseLink)
        end
        local compactPulseFit = nil
        if isRoutePulseFitCompactPromptExperimentEnabled() then
            compactPulseFit = resolveCompactRoutePulseFit(pressureScore, altRouteTag, compactPulseMode, compactPulseLink)
        end
        local compactPulseFlare = nil
        if isRoutePulseFlareCompactPromptExperimentEnabled() then
            compactPulseFlare = resolveCompactPulseFlare(compactPulseMode, compactPulseFit)
        end
        local compactPulseHeat = nil
        if isPulseHeatCompactPromptExperimentEnabled() then
            compactPulseHeat = resolveCompactPulseHeat(pressureScore, compactPulseMode)
        end
        local compactPulseHeatFx = nil
        if isPulseHeatFxCompactPromptExperimentEnabled() then
            compactPulseHeatFx = resolveCompactPulseHeatFx(compactPulseHeat)
        end
        local compactVibeTrail = resolveCompactVibeTrail(vibeTrail)
        local compactVibeTrailConfidence = resolveCompactVibeTrailConfidence(vibeTrailConfidence)
        local compactVibeTrailConfidenceRail = resolveCompactVibeTrailConfidenceRail(vibeTrailConfidenceRail)
        local compactVibeTrailArc = resolveCompactVibeTrailArc(vibeTrailArc)
        local compactRouteGlow = nil
        if isRouteGlowCompactPromptExperimentEnabled() then
            compactRouteGlow = resolveCompactRouteGlow(vibeTrailArc)
        end
        local compactRouteGlowConfidence = nil
        if isRouteGlowConfidenceCompactPromptExperimentEnabled() then
            compactRouteGlowConfidence = resolveRouteGlowConfidence(vibeTrailArc)
        end
        local compactRouteGlowFx = nil
        if isRouteGlowFxCompactPromptExperimentEnabled() then
            compactRouteGlowFx = resolveCompactRouteGlowFx(compactRouteGlow, compactPulseHeat)
        end
        local compactRouteGlowFxConfidence = nil
        if isRouteGlowFxConfidenceCompactPromptExperimentEnabled() then
            compactRouteGlowFxConfidence = resolveCompactRouteGlowFxConfidence(resolveRouteGlowFxConfidence(compactRouteGlowFx))
        end
        local compactVibeTrailWhyConfidence = resolveCompactVibeTrailWhyConfidence(vibeTrailWhyConfidence)
        local compactVibeTrailWhyConfidenceWhyConfidence = resolveCompactVibeTrailWhyConfidenceWhyConfidence(vibeTrailWhyConfidenceWhyConfidence)
        local compactVibeTrailWhyConfidenceWhyRail = resolveCompactVibeTrailWhyConfidenceWhyRail(vibeTrailWhyConfidenceWhyRail)
        return buildCompactTransitionPrompt(routeTag, pressureScore, altRouteTag, altDelta, altPlanNudge, altStepCue, altStepConfidence, altStepWhy, altStepWhyConfidence, altStepWhyGlyph, altStepWhyGlyphMode, routeVignette, routeVibeConflict, routeVibeConflictReasonCompact, coachOverride, vibeSyncHint, vibeSyncChain, vibeSnapback, vibeRecovery, vibeResilience, vibeDriftWide, vibeDriftGlyphCompact, compactPulseLink, compactPulseMode, compactPulseFit, compactPulseFlare, compactPulseHeat, compactPulseHeatFx, compactVibeTrail, compactVibeTrailConfidence, compactVibeTrailConfidenceRail, vibeTrailWhy, compactVibeTrailArc, compactRouteGlow, compactRouteGlowConfidence, compactRouteGlowFx, compactRouteGlowFxConfidence, compactVibeTrailWhyConfidence, vibeTrailWhyConfidenceWhy, compactVibeTrailWhyConfidenceWhyConfidence, compactVibeTrailWhyConfidenceWhyRail, budget)
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
    local snapbackTriggered = isRouteVibeSnapbackExperimentEnabled() and syncEnabled and aligned == false and routeVibeSyncStreak >= 3
    local recoveryResolved = transition.vibeRecovery == true and aligned == true
    local conflictTriggered = transition.routeVibeConflict == true
    pendingTransition = nil
    if aligned == true then
        routeVibeSyncStreak = routeVibeSyncStreak + 1
    elseif aligned == false then
        routeVibeSyncStreak = 0
    end
    if syncHintTriggered and isRouteVibeSyncDodgeExperimentEnabled() then
        pendingVibeSyncDodgeCharges = pendingVibeSyncDodgeCharges + 1
    end
    if snapbackTriggered then
        routeVibeRecoveryArmed = true
    elseif recoveryResolved then
        routeVibeRecoveryArmed = false
    end

    if conflictTriggered then
        routeVibeConflictAge = 0
    else
        routeVibeConflictAge = math.min(routeVibeConflictAge + 1, 999)
    end
    if snapbackTriggered then
        routeVibeSnapbackAge = 0
    else
        routeVibeSnapbackAge = math.min(routeVibeSnapbackAge + 1, 999)
    end

    if recoveryResolved then
        routeVibeRecoveryStreak = routeVibeRecoveryStreak + 1
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
    routeVibeRecoveryArmed = false
    routeVibeRecoveryStreak = 0
    routeVibeConflictAge = 999
    routeVibeSnapbackAge = 999
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
