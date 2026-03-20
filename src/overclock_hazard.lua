local Map = require("src.map")

local OverclockHazard = {}

local state = {
    mapName = nil,
    zone = nil,
    pulseActive = false,
    pulseTimer = 0,
    cooldownTimer = 0,
    enteredZone = false,
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
    }
end

local function inRect(px, py, rect)
    return rect and px >= rect.x and px < (rect.x + rect.w) and py >= rect.y and py < (rect.y + rect.h)
end

function OverclockHazard.onMapLoaded(mapName, metadata)
    state.mapName = tostring(mapName or "")
    state.zone = resolveZone(metadata)
    state.pulseActive = false
    state.pulseTimer = 0
    state.cooldownTimer = 0
    state.enteredZone = false
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
            events.activated = true
        end
    elseif not inside and state.enteredZone then
        state.enteredZone = false
    end

    return events
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

function OverclockHazard.getHudHint()
    if not state.zone then return nil end
    if state.pulseActive then
        return string.format("OVERCLOCK HOT: -%d%% SRL / AGGRO+", math.floor(state.zone.discountPct * 100 + 0.5))
    end
    if state.cooldownTimer > 0 then
        return string.format("OVERCLOCK CD: %.0fs", math.ceil(state.cooldownTimer))
    end
    return "OVERCLOCK READY"
end

function OverclockHazard.debugSetPulse(active, pulseTimer)
    state.pulseActive = active == true
    state.pulseTimer = tonumber(pulseTimer) or 0
end

return OverclockHazard
