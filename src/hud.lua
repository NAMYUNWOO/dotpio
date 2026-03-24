local Combat = require("src.combat")

local HUD = {
    _lastThreatScore = 0,
    _auxThreatHint = nil,
    _auxThreatHintColor = nil,
    _routeCallout = nil,
    _routeCalloutColor = nil,
}

function HUD.setAuxThreatHint(text, color)
    HUD._auxThreatHint = text
    if type(color) == "table" and #color >= 3 then
        HUD._auxThreatHintColor = { color[1], color[2], color[3], color[4] or 1 }
    else
        HUD._auxThreatHintColor = nil
    end
end

function HUD.setRouteCallout(text, color)
    if text == nil then
        HUD._routeCallout = nil
        HUD._routeCalloutColor = nil
        return
    end
    local value = tostring(text)
    if value == "" then
        HUD._routeCallout = nil
        HUD._routeCalloutColor = nil
        return
    end
    HUD._routeCallout = value
    if type(color) == "table" and #color >= 3 then
        HUD._routeCalloutColor = { color[1], color[2], color[3], color[4] or 1 }
    else
        HUD._routeCalloutColor = nil
    end
end

function HUD.getBerserkerThreatTier(score)
    local value = tonumber(score) or 0
    if value >= 6 then
        return "HIGH"
    end
    if value >= 3 then
        return "MED"
    end
    return "LOW"
end

function HUD.getBerserkerThreatColor(score)
    local tier = HUD.getBerserkerThreatTier(score)
    if tier == "HIGH" then
        return 1, 0.3, 0.2, 1
    end
    if tier == "MED" then
        return 1, 0.66, 0.25, 1
    end
    return 0.5, 1, 0.62, 1
end

function HUD.getBerserkerThreatLegend()
    return "THREAT = BERSERK + 2*LUNGE + RECOVER"
end

function HUD.getBerserkerThreatDelta(currentScore, previousScore)
    local current = tonumber(currentScore) or 0
    local previous = tonumber(previousScore) or 0
    return current - previous
end

function HUD.formatBerserkerThreatDelta(currentScore, previousScore)
    local delta = HUD.getBerserkerThreatDelta(currentScore, previousScore)
    local signed = delta > 0 and ("+" .. delta) or tostring(delta)
    return string.format("THREAT Δ:%s", signed)
end

function HUD.formatBerserkerThreatBreakdown(counters)
    counters = counters or {}
    local berserkers = tonumber(counters.desperateBerserkers) or 0
    local lunges = tonumber(counters.primedBerserkerLunges) or 0
    local recoveries = tonumber(counters.recoveringBerserkers) or 0
    local score = tonumber(counters.berserkerThreatScore) or (berserkers + (lunges * 2) + recoveries)
    return string.format("THREAT = %d + 2*%d + %d = %d", berserkers, lunges, recoveries, score)
end

function HUD.updateBerserkerThreatRiseStreak(currentScore, previousScore, previousStreak)
    local delta = HUD.getBerserkerThreatDelta(currentScore, previousScore)
    local streak = math.max(0, math.floor(tonumber(previousStreak) or 0))
    if delta > 0 then
        streak = streak + 1
    else
        streak = 0
    end
    return streak, delta
end

function HUD.shouldTriggerBerserkerFxPulse(currentScore, previousScore, previousStreak)
    local streak, delta = HUD.updateBerserkerThreatRiseStreak(currentScore, previousScore, previousStreak)
    local triggered = delta > 0 and streak >= 2
    return triggered, streak, delta
end

function HUD.shouldTriggerBerserkerFxFade(previousScore, threatDelta, previousRiseStreak)
    local prevScore = math.max(0, math.floor(tonumber(previousScore) or 0))
    local delta = tonumber(threatDelta) or 0
    local riseStreak = math.max(0, math.floor(tonumber(previousRiseStreak) or 0))
    return riseStreak >= 2 and prevScore > 0 and delta <= 0
end

function HUD.getBerserkerFxFadeTier(previousScore, threatDelta)
    local prevScore = math.max(0, math.floor(tonumber(previousScore) or 0))
    local delta = tonumber(threatDelta) or 0
    if prevScore >= 6 or delta <= -2 then
        return "HARD"
    end
    return "SOFT"
end

function HUD.getRunSummaryOverclockGlossary()
    return "GLOSSARY: DWELL=EXPOSURE sec(L/M/H)  EFF=SRL/EXPOSED sec  PROFILE=COMMIT TIER"
end

function HUD.collectCombatThreatCounters(enemies)
    local counters = {
        alive = 0,
        desperateBerserkers = 0,
        primedBerserkerLunges = 0,
        recoveringBerserkers = 0,
        berserkerThreatScore = 0,
    }

    for _, e in ipairs(enemies or {}) do
        if e.alive then
            counters.alive = counters.alive + 1
            if e.behavior == "berserker" and e.desperationActive then
                counters.desperateBerserkers = counters.desperateBerserkers + 1
                counters.berserkerThreatScore = counters.berserkerThreatScore + 1
                if e.desperationLungePrimed then
                    counters.primedBerserkerLunges = counters.primedBerserkerLunges + 1
                    counters.berserkerThreatScore = counters.berserkerThreatScore + 2
                end
                if e.desperationRecoveryPending then
                    counters.recoveringBerserkers = counters.recoveringBerserkers + 1
                    counters.berserkerThreatScore = counters.berserkerThreatScore + 1
                end
            end
        end
    end

    return counters
end

local function drawMissionPanel(missionState, unlockFlags, startY)
    if not missionState or not missionState.active then
        return
    end

    local panelY = startY or 84

    love.graphics.setColor(0, 0, 0, 0.72)
    love.graphics.rectangle("fill", 8, panelY, 380, 108)

    local headerColor = missionState.completed and {0.4, 1, 0.6, 1} or {0.95, 0.9, 0.6, 1}
    love.graphics.setColor(headerColor)
    love.graphics.print(string.format("RUN MISSIONS %d/%d", missionState.doneCount or 0, missionState.total or 0), 16, panelY + 6)

    local metaPack = string.upper(tostring(missionState.lastPackId or "unknown"))
    local metaTag = string.upper(tostring(missionState.lastPackTag or "unknown"))
    local metaStreak = tonumber(missionState.completionStreak) or 0
    local metaVarietyCount = tonumber(missionState.varietyBonusCount) or 0
    local metaNextVarietyLane = missionState.nextVarietyLane and string.upper(tostring(missionState.nextVarietyLane)) or nil
    local metaVarietyBonus = tonumber(missionState.varietyBonusPreview) or 0
    love.graphics.setColor(0.7, 0.88, 1, 1)
    local metaLine = string.format("PACK:%s  TAG:%s  STREAK:%d  VAR:%d", metaPack, metaTag, metaStreak, metaVarietyCount)
    if metaNextVarietyLane and metaVarietyBonus > 0 then
        metaLine = string.format("%s  NEXT:%s +%d", metaLine, metaNextVarietyLane, metaVarietyBonus)
    end
    love.graphics.print(metaLine, 16, panelY + 22)

    local row = panelY + 40
    for _, objective in ipairs(missionState.objectives or {}) do
        local done = objective.done
        local marker = done and "[x]" or "[ ]"
        local fg = done and {0.5, 1, 0.6, 1} or {0.8, 0.8, 0.8, 1}
        love.graphics.setColor(fg)
        love.graphics.print(string.format("%s %s (%d/%d)", marker, objective.label or "?", objective.progress or 0, objective.target or 0), 16, row)
        row = row + 16
    end

    local advancedUnlocked = unlockFlags and unlockFlags.advanced_build_categories
    love.graphics.setColor(advancedUnlocked and 0.45 or 0.6, advancedUnlocked and 1 or 0.6, advancedUnlocked and 0.7 or 0.6, 1)
    love.graphics.print(string.format("UNLOCK: ADVANCED SCHEMATICS [%s]", advancedUnlocked and "ON" or "OFF"), 16, row)
end

local function drawRunSummary(runSummary)
    if not runSummary or not runSummary.active or not runSummary.data then
        return
    end

    local data = runSummary.data
    local w = love.graphics.getWidth()
    local h = love.graphics.getHeight()

    love.graphics.setColor(0, 0, 0, 0.86)
    love.graphics.rectangle("fill", 88, 118, w - 176, h - 236, 6, 6)

    love.graphics.setColor(0.95, 0.95, 0.7, 1)
    love.graphics.printf("RUN SUMMARY", 0, 136, w, "center")

    love.graphics.setColor(0.8, 0.9, 1, 1)
    love.graphics.printf(string.format("MISSIONS: %d/%d", data.missionsDone or 0, data.missionsTotal or 0), 112, 168, w - 224, "left")
    love.graphics.setColor(0.7, 0.88, 1, 1)
    love.graphics.printf(string.format("PACK: %s   TAG: %s   STREAK: %d   VAR: %d", string.upper(tostring(data.missionPackId or "unknown")), string.upper(tostring(data.missionPackTag or "unknown")), data.momentumStreak or 0, data.varietyBonusCount or 0), 112, 188, w - 224, "left")

    love.graphics.setColor(0.62, 0.78, 0.95, 1)
    love.graphics.printf(string.format("PACE: %s", string.upper(tostring(data.missionPackLabel or "unknown pacing"))), 112, 206, w - 224, "left")


    local row = 232
    for _, objective in ipairs(data.objectives or {}) do
        local marker = objective.done and "[x]" or "[ ]"
        local fg = objective.done and {0.45, 1, 0.65, 1} or {0.8, 0.8, 0.8, 1}
        love.graphics.setColor(fg)
        love.graphics.printf(string.format("%s %s (%d/%d)", marker, objective.label or "?", objective.progress or 0, objective.target or 0), 112, row, w - 224, "left")
        row = row + 20
    end

    row = row + 8
    love.graphics.setColor(0.7, 0.9, 1, 1)
    love.graphics.printf(string.format("UNLOCK: ADVANCED SCHEMATICS [%s]", data.advancedUnlocked and "ON" or "OFF"), 112, row, w - 224, "left")

    row = row + 28
    local carry = data.carry or { srl = 0, coins = 0, gems = 0 }
    love.graphics.setColor(0.9, 0.85, 0.65, 1)
    love.graphics.printf("FAIL-FORWARD CARRYOVER APPLIED", 112, row, w - 224, "left")
    row = row + 20
    love.graphics.setColor(0.88, 0.88, 0.88, 1)
    love.graphics.printf(string.format("+%d BUILDER.SRL   +%d COIN   +%d GEM", carry.srl or 0, carry.coins or 0, carry.gems or 0), 112, row, w - 224, "left")

    row = row + 20
    local dwell = data.overclockDwell or { low = 0, mid = 0, high = 0 }
    love.graphics.setColor(0.76, 0.9, 1, 1)
    love.graphics.printf(string.format("OVERCLOCK DWELL L/M/H: %ds / %ds / %ds", dwell.low or 0, dwell.mid or 0, dwell.high or 0), 112, row, w - 224, "left")

    row = row + 20
    local exposureTotal = math.max(0, (dwell.low or 0) + (dwell.mid or 0) + (dwell.high or 0))
    local overclockRewardSrl = math.max(0, data.overclockRewardSrl or 0)
    local efficiencyToken = "n/a"
    if exposureTotal > 0 then
        efficiencyToken = string.format("%.2f", overclockRewardSrl / exposureTotal)
    end
    love.graphics.setColor(0.68, 0.95, 0.78, 1)
    love.graphics.printf(string.format("OVERCLOCK EFF: %d SRL / %ds = %s SRL/EXPOSED sec", overclockRewardSrl, exposureTotal, efficiencyToken), 112, row, w - 224, "left")

    row = row + 20
    love.graphics.setColor(0.92, 0.86, 0.64, 1)
    love.graphics.printf(string.format("OVERCLOCK PROFILE: %s", string.upper(tostring(data.overclockProfile or "BALANCED"))), 112, row, w - 224, "left")

    row = row + 20
    love.graphics.setColor(0.7, 0.92, 0.78, 1)
    love.graphics.printf(string.format("OVERCLOCK COACH: %s", string.upper(tostring(data.overclockCoachTip or "HOLD MID-ZONE TEMPO"))), 112, row, w - 224, "left")

    row = row + 20
    love.graphics.setColor(0.72, 0.82, 0.9, 1)
    love.graphics.printf(HUD.getRunSummaryOverclockGlossary(), 112, row, w - 224, "left")

    love.graphics.setColor(0.65, 0.65, 0.65, 1)
    love.graphics.printf("Press R / Enter / Esc to close", 0, h - 148, w, "center")
end

local function isDamageGlyphLiveDebugExperimentEnabled()
    local v = os.getenv("DOTPIO_EXPERIMENT_DMG_GLYPH_LIVE_DEBUG")
    if not v then return false end
    v = string.lower(v)
    return v == "1" or v == "true" or v == "yes" or v == "on"
end

local function isDamageGlyphFxLiveDebugExperimentEnabled()
    local v = os.getenv("DOTPIO_EXPERIMENT_DMG_GLYPH_FX_LIVE_DEBUG")
    if not v then return false end
    v = string.lower(v)
    return v == "1" or v == "true" or v == "yes" or v == "on"
end

function HUD.resolveDamageGlyphLiveToken()
    if not isDamageGlyphLiveDebugExperimentEnabled() then
        return nil
    end
    local numbers = Combat.debugGetDamageNumbers and Combat.debugGetDamageNumbers() or {}
    local latest = numbers[#numbers]
    if not latest then
        return "DMG GLYPH LIVE:BASIC"
    end
    local band = tostring(latest.glyphBand or "BASIC")
    if band ~= "BASIC" and band ~= "SPIKE" and band ~= "OVERDRIVE" then
        band = "BASIC"
    end
    return string.format("DMG GLYPH LIVE:%s", band)
end

function HUD.resolveDamageGlyphFxLiveToken()
    if not isDamageGlyphFxLiveDebugExperimentEnabled() then
        return nil
    end

    local numbers = Combat.debugGetDamageNumbers and Combat.debugGetDamageNumbers() or {}
    local latest = numbers[#numbers]
    if not latest then
        return "DMG GLYPH FX LIVE:CALM"
    end

    local band = tostring(latest.glyphBand or "BASIC")
    local fx = "CALM"
    if band == "SPIKE" then
        fx = "SPARK"
    elseif band == "OVERDRIVE" then
        fx = "BLAZE"
    end
    return string.format("DMG GLYPH FX LIVE:%s", fx)
end

function HUD.draw(player, enemies, gameOver, missionState, unlockFlags, runSummary, onboardingHint)
    love.graphics.setColor(0,0,0,0.7)
    love.graphics.rectangle("fill", 8, 8, 240, 92)
    love.graphics.setColor(1,1,1,1)
    love.graphics.print("HP:", 16, 14)
    love.graphics.setColor(0.3,0,0,1)
    love.graphics.rectangle("fill", 44, 14, 100, 14)
    love.graphics.setColor(0,0.8,0.3,1)
    love.graphics.rectangle("fill", 44, 14, 100*(player.hp/player.maxHp), 14)
    love.graphics.setColor(1,1,1,1)
    love.graphics.print("MP:", 16, 34)
    love.graphics.setColor(0.1,0.1,0.3,1)
    love.graphics.rectangle("fill", 44, 34, 100, 14)
    love.graphics.setColor(0.3,0.3,1,1)
    love.graphics.rectangle("fill", 44, 34, 100*(player.mp/player.maxMp), 14)
    love.graphics.setColor(0.75, 0.95, 1, 1)
    love.graphics.print(string.format("Dodge: %d", player.getDodgeChargeCount and player.getDodgeChargeCount() or 0), 16, 54)
    local counters = HUD.collectCombatThreatCounters(enemies)
    love.graphics.setColor(1,0.5,0.5,1)
    love.graphics.print("Enemies: "..counters.alive, 160, 14)
    if HUD._routeCallout then
        if HUD._routeCalloutColor then
            love.graphics.setColor(HUD._routeCalloutColor)
        else
            love.graphics.setColor(0.82, 0.9, 1, 1)
        end
        love.graphics.print(HUD._routeCallout, 160, 30)
    end
    if HUD._auxThreatHint then
        if HUD._auxThreatHintColor then
            love.graphics.setColor(HUD._auxThreatHintColor)
        else
            love.graphics.setColor(0.95, 0.82, 0.48, 1)
        end
        love.graphics.print(HUD._auxThreatHint, 16, 58)
    end
    if counters.desperateBerserkers > 0 then
        local threatTopY = HUD._routeCallout and 46 or 30
        love.graphics.setColor(1, 0.35, 0.2, 1)
        love.graphics.print(string.format("Berserk: %d", counters.desperateBerserkers), 160, threatTopY)
        local threatTier = HUD.getBerserkerThreatTier(counters.berserkerThreatScore)
        love.graphics.setColor(HUD.getBerserkerThreatColor(counters.berserkerThreatScore))
        love.graphics.print(string.format("Threat: %d (%s)", counters.berserkerThreatScore, threatTier), 160, threatTopY + 16)

        local threatDelta = HUD.getBerserkerThreatDelta(counters.berserkerThreatScore, HUD._lastThreatScore)
        if threatDelta > 0 then
            love.graphics.setColor(1, 0.48, 0.36, 1)
        elseif threatDelta < 0 then
            love.graphics.setColor(0.58, 1, 0.68, 1)
        else
            love.graphics.setColor(0.78, 0.78, 0.78, 1)
        end
        love.graphics.print(HUD.formatBerserkerThreatDelta(counters.berserkerThreatScore, HUD._lastThreatScore), 160, threatTopY + 32)

        local rowY = threatTopY + 48
        if counters.primedBerserkerLunges > 0 then
            love.graphics.setColor(1, 0.6, 0.25, 1)
            love.graphics.print(string.format("Lunge Tell: %d", counters.primedBerserkerLunges), 160, rowY)
            rowY = rowY + 16
        end

        if counters.recoveringBerserkers > 0 then
            love.graphics.setColor(1, 0.78, 0.38, 1)
            love.graphics.print(string.format("Recovering: %d", counters.recoveringBerserkers), 160, rowY)
            rowY = rowY + 16
        end

        love.graphics.setColor(0.78, 0.88, 1, 1)
        love.graphics.print(HUD.formatBerserkerThreatBreakdown(counters), 160, rowY)
    end
    HUD._lastThreatScore = counters.berserkerThreatScore
    love.graphics.setColor(0.6,0.6,0.6,1)
    love.graphics.print("WASD:Move  Click:Magic  Space:Melee  E:Search  G:Pickup  R:Restart", 16, 74)

    if onboardingHint then
        love.graphics.setColor(0, 0, 0, 0.74)
        love.graphics.rectangle("fill", 8, 84, 460, 28)
        love.graphics.setColor(0.95, 0.95, 0.7, 1)
        love.graphics.print("ONBOARDING", 16, 90)
        love.graphics.setColor(0.82, 0.9, 1, 1)
        love.graphics.print(onboardingHint, 112, 90)
    end

    love.graphics.setColor(0.5,0.5,0.5,0.8)
    love.graphics.print(string.format("Pos: %d,%d", player.x, player.y), 16, 690)

    local damageGlyphLiveToken = HUD.resolveDamageGlyphLiveToken()
    if damageGlyphLiveToken then
        love.graphics.setColor(0.86, 0.8, 1.0, 0.92)
        love.graphics.print(damageGlyphLiveToken, 160, 690)
    end

    local damageGlyphFxLiveToken = HUD.resolveDamageGlyphFxLiveToken()
    if damageGlyphFxLiveToken then
        love.graphics.setColor(1.0, 0.82, 0.64, 0.92)
        love.graphics.print(damageGlyphFxLiveToken, 420, 690)
    end

    drawMissionPanel(missionState, unlockFlags, onboardingHint and 118 or 84)

    if gameOver then
        love.graphics.setColor(0,0,0,0.6)
        love.graphics.rectangle("fill", 0, 280, love.graphics.getWidth(), 80)
        love.graphics.setColor(1,0.2,0.2,1)
        love.graphics.printf("GAME OVER", 0, 290, love.graphics.getWidth(), "center")
        love.graphics.setColor(0.8,0.8,0.8,1)
        love.graphics.printf("Press R to restart", 0, 320, love.graphics.getWidth(), "center")
    elseif counters.alive == 0 and #enemies > 0 then
        love.graphics.setColor(0,1,0.5,1)
        love.graphics.printf("ALL ENEMIES DEFEATED! Press R to restart", 0, 200, love.graphics.getWidth(), "center")
    end

    drawRunSummary(runSummary)
end

return HUD
