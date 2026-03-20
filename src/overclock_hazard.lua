local Map = require("src.map")

local OverclockHazard = {}

local state = {
    mapName = nil,
    zone = nil,
    pulseActive = false,
    pulseTimer = 0,
    cooldownTimer = 0,
    enteredZone = false,
    killBonusGrantedThisPulse = 0,
}

local function resolveZone(metadata)
    local hazard = metadata and metadata.overclockHazard
    if type(hazard) ~= "table" then return nil end
    local rect = hazard.rect
    if type(rect) ~= "table" then return nil end
    if not rect.x or not rect.y or not rect.w or not rect.h then return nil end

    return {
        name = hazard.name or "OVERCLOCK",
        x = rect.x,
        y = rect.y,
        w = rect.w,
        h = rect.h,
        discountPct = math.max(0, math.min(0.75, tonumber(hazard.discountPct) or 0.35)),
        pulseDuration = math.max(1, tonumber(hazard.pulseDuration) or 7),
        cooldownDuration = math.max(3, tonumber(hazard.cooldownDuration) or 16),
        aggroMoveMul = math.max(0.4, tonumber(hazard.aggroMoveMul) or 0.7),
        aggroDetectBonus = math.max(0, math.floor(tonumber(hazard.aggroDetectBonus) or 2)),
        killBonusPerKill = math.max(0, math.floor(tonumber(hazard.killBonusPerKill) or 1)),
        killBonusPulseCap = math.max(0, math.floor(tonumber(hazard.killBonusPulseCap) or 3)),
    }
end

local function inRect(px, py, rect)
    return rect and px >= rect.x and px < (rect.x + rect.w) and py >= rect.y and py < (rect.y + rect.h)
end

local function getRiskComponents(zone)
    if not zone then
        return { discount = 0, detect = 0, move = 0 }
    end

    return {
        discount = math.floor((zone.discountPct or 0) * 10 + 0.5),
        detect = math.max(0, tonumber(zone.aggroDetectBonus) or 0),
        move = math.max(0, math.floor((1 - (tonumber(zone.aggroMoveMul) or 1)) * 10 + 0.5)),
    }
end

local function getRiskScore(zone)
    local parts = getRiskComponents(zone)
    return parts.discount + parts.detect + parts.move
end

local function getRiskTier(zone)
    local score = getRiskScore(zone)
    if score >= 10 then
        return "HIGH", score
    end
    if score >= 6 then
        return "MED", score
    end
    return "LOW", score
end

local function getRiskTierColor(tier)
    if tier == "HIGH" then
        return { 1, 0.34, 0.25, 1 }
    end
    if tier == "MED" then
        return { 1, 0.7, 0.3, 1 }
    end
    return { 0.56, 1, 0.66, 1 }
end

local function getAggroPressureLegend(zone)
    if not zone then
        return "AGGRO DET:+0 MOVE:+0%"
    end

    local detectBonus = math.max(0, math.floor(tonumber(zone.aggroDetectBonus) or 0))
    local moveBoostPct = math.max(0, math.floor(((1 / math.max(0.01, tonumber(zone.aggroMoveMul) or 1)) - 1) * 100 + 0.5))
    return string.format("AGGRO DET:+%d MOVE:+%d%%", detectBonus, moveBoostPct)
end

local function getBountyProgressToken()
    local cap = math.max(0, math.floor((state.zone and state.zone.killBonusPulseCap) or 0))
    local granted = math.max(0, math.floor(state.killBonusGrantedThisPulse or 0))
    return string.format("BOUNTY:%d/%d", math.min(granted, cap), cap)
end

local function getNextBountyBudgetToken()
    local cap = math.max(0, math.floor((state.zone and state.zone.killBonusPulseCap) or 0))
    return string.format("NEXT BOUNTY:0/%d", cap)
end

local function getNextPulseEtaToken()
    if state.pulseActive then
        return string.format("NEXT PULSE:%ds", math.max(0, math.ceil(state.pulseTimer or 0)))
    end
    local seconds = 0
    if (state.cooldownTimer or 0) > 0 then
        seconds = math.max(0, math.ceil(state.cooldownTimer))
    end
    return string.format("NEXT PULSE:%ds", seconds)
end

local function getPulseProgressToken()
    local duration = math.max(1, tonumber(state.zone and state.zone.pulseDuration) or 1)
    local ratio = math.max(0, math.min(1, (tonumber(state.pulseTimer) or 0) / duration))
    return string.format("PULSE:%d%%", math.floor(ratio * 100 + 0.5))
end

local function getRechargeProgressToken()
    local duration = math.max(1, tonumber(state.zone and state.zone.cooldownDuration) or 1)
    local remaining = math.max(0, tonumber(state.cooldownTimer) or 0)
    local ratio = 1 - math.max(0, math.min(1, remaining / duration))
    return string.format("RECHARGE:%d%%", math.floor(ratio * 100 + 0.5))
end

local function getRiskBreakdownToken(zone)
    local parts = getRiskComponents(zone)
    return string.format("RISK SRC:D%d+DET%d+MOVE%d", parts.discount, parts.detect, parts.move)
end

local function getRiskDeltaValue()
    if state.pulseActive then
        return 2
    end
    if (state.cooldownTimer or 0) > 0 and state.enteredZone and (state.cooldownTimer or 0) <= 3 then
        return 1
    end
    return 0
end

local function getRiskDeltaToken()
    local delta = getRiskDeltaValue()
    if delta > 0 then
        return string.format("RISK Δ:+%d", delta)
    end
    if delta < 0 then
        return string.format("RISK Δ:%d", delta)
    end
    return "RISK Δ:0"
end

local function getZonePresenceToken()
    if state.enteredZone then
        return "ZONE:IN"
    end
    return "ZONE:OUT"
end

function OverclockHazard.onMapLoaded(mapName, metadata)
    state.mapName = tostring(mapName or "")
    state.zone = resolveZone(metadata)
    state.pulseActive = false
    state.pulseTimer = 0
    state.cooldownTimer = 0
    state.enteredZone = false
    state.killBonusGrantedThisPulse = 0
end

function OverclockHazard.update(dt, playerX, playerY)
    local events = {}
    if not state.zone then return events end

    if state.cooldownTimer > 0 then
        state.cooldownTimer = math.max(0, state.cooldownTimer - dt)
    end

    if state.pulseActive then
        state.pulseTimer = state.pulseTimer - dt
        if state.pulseTimer <= 0 then
            state.pulseActive = false
            state.pulseTimer = 0
            events.expired = true
        end
    end

    local inside = inRect(playerX, playerY, state.zone)
    if inside and not state.enteredZone then
        state.enteredZone = true
        if (not state.pulseActive) and state.cooldownTimer <= 0 then
            state.pulseActive = true
            state.pulseTimer = state.zone.pulseDuration
            state.cooldownTimer = state.zone.cooldownDuration
            state.killBonusGrantedThisPulse = 0
            events.activated = true
        end
    elseif not inside and state.enteredZone then
        state.enteredZone = false
    end

    return events
end

function OverclockHazard.consumeKillBonus(kills)
    local killCount = math.max(0, math.floor(tonumber(kills) or 0))
    if killCount <= 0 or not state.zone or not state.pulseActive or not state.enteredZone then
        return 0
    end

    local perKill = math.max(0, state.zone.killBonusPerKill or 0)
    local pulseCap = math.max(0, state.zone.killBonusPulseCap or 0)
    if perKill <= 0 or pulseCap <= 0 then
        return 0
    end

    local remaining = math.max(0, pulseCap - (state.killBonusGrantedThisPulse or 0))
    if remaining <= 0 then
        return 0
    end

    local proposedReward = killCount * perKill
    local reward = math.min(remaining, proposedReward)
    state.killBonusGrantedThisPulse = (state.killBonusGrantedThisPulse or 0) + reward
    return reward
end

function OverclockHazard.applyBuildCost(baseCost)
    local cost = math.max(1, math.floor(tonumber(baseCost) or 1))
    if not state.zone or not state.pulseActive then
        return cost, 0
    end

    local discount = math.max(1, math.floor(cost * state.zone.discountPct + 0.5))
    local discounted = math.max(1, cost - discount)
    return discounted, (cost - discounted)
end

function OverclockHazard.getPressureProfile()
    if not state.zone or not state.pulseActive then
        return { active = false, moveMul = 1.0, detectBonus = 0 }
    end

    return {
        active = true,
        moveMul = state.zone.aggroMoveMul,
        detectBonus = state.zone.aggroDetectBonus,
        pulseTimer = state.pulseTimer,
        discountPct = state.zone.discountPct,
    }
end

function OverclockHazard.getHudHintColor()
    if not state.zone then return nil end
    local riskTier = getRiskTier(state.zone)
    return getRiskTierColor(riskTier)
end

function OverclockHazard.getHudHint()
    if not state.zone then return nil end
    local riskTier, riskScore = getRiskTier(state.zone)
    local riskBreakdown = getRiskBreakdownToken(state.zone)
    local riskDelta = getRiskDeltaToken()
    local zonePresence = getZonePresenceToken()
    if state.pulseActive then
        local pulseSeconds = math.max(0, math.ceil(state.pulseTimer or 0))
        local aggroLegend = getAggroPressureLegend(state.zone)
        local bountyProgress = getBountyProgressToken()
        local pulseProgress = getPulseProgressToken()
        return string.format("OVERCLOCK HOT %ds: -%d%% SRL / %s / %s / %s %s  RISK:%s(%d) %s %s", pulseSeconds, math.floor(state.zone.discountPct * 100 + 0.5), aggroLegend, bountyProgress, pulseProgress, zonePresence, riskTier, riskScore, riskDelta, riskBreakdown)
    end
    if state.cooldownTimer > 0 then
        local cooldownSeconds = math.max(0, math.ceil(state.cooldownTimer))
        local nextBounty = getNextBountyBudgetToken()
        local nextPulseEta = getNextPulseEtaToken()
        local rechargeProgress = getRechargeProgressToken()
        if state.enteredZone and cooldownSeconds <= 3 then
            return string.format("OVERCLOCK CD %ds (IMMINENT:%ds) %s %s %s %s  RISK:%s(%d) %s %s", cooldownSeconds, cooldownSeconds, nextBounty, nextPulseEta, rechargeProgress, zonePresence, riskTier, riskScore, riskDelta, riskBreakdown)
        end
        return string.format("OVERCLOCK CD %ds %s %s %s %s  RISK:%s(%d) %s %s", cooldownSeconds, nextBounty, nextPulseEta, rechargeProgress, zonePresence, riskTier, riskScore, riskDelta, riskBreakdown)
    end
    return string.format("OVERCLOCK READY %s %s %s %s  RISK:%s(%d) %s %s", getNextBountyBudgetToken(), getNextPulseEtaToken(), getRechargeProgressToken(), zonePresence, riskTier, riskScore, riskDelta, riskBreakdown)
end

function OverclockHazard.debugSetPulse(active, pulseTimer)
    state.pulseActive = active == true
    state.pulseTimer = tonumber(pulseTimer) or 0
end

return OverclockHazard
