local HUD = {}

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
    love.graphics.setColor(0.7, 0.88, 1, 1)
    love.graphics.print(string.format("PACK:%s  TAG:%s  STREAK:%d", metaPack, metaTag, metaStreak), 16, panelY + 22)

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
    love.graphics.printf(string.format("PACK: %s   TAG: %s   STREAK: %d", string.upper(tostring(data.missionPackId or "unknown")), string.upper(tostring(data.missionPackTag or "unknown")), data.momentumStreak or 0), 112, 188, w - 224, "left")

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

    love.graphics.setColor(0.65, 0.65, 0.65, 1)
    love.graphics.printf("Press R / Enter / Esc to close", 0, h - 148, w, "center")
end

function HUD.draw(player, enemies, gameOver, missionState, unlockFlags, runSummary, onboardingHint)
    love.graphics.setColor(0,0,0,0.7)
    love.graphics.rectangle("fill", 8, 8, 220, 70)
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
    local alive = 0
    local desperateBerserkers = 0
    local primedBerserkerLunges = 0
    for _, e in ipairs(enemies) do
        if e.alive then
            alive = alive + 1
            if e.behavior == "berserker" and e.desperationActive then
                desperateBerserkers = desperateBerserkers + 1
                if e.desperationLungePrimed then
                    primedBerserkerLunges = primedBerserkerLunges + 1
                end
            end
        end
    end
    love.graphics.setColor(1,0.5,0.5,1)
    love.graphics.print("Enemies: "..alive, 160, 14)
    if desperateBerserkers > 0 then
        love.graphics.setColor(1, 0.35, 0.2, 1)
        love.graphics.print(string.format("Berserk: %d", desperateBerserkers), 160, 30)
        if primedBerserkerLunges > 0 then
            love.graphics.setColor(1, 0.6, 0.25, 1)
            love.graphics.print(string.format("Lunge Tell: %d", primedBerserkerLunges), 160, 46)
        end
    end
    love.graphics.setColor(0.6,0.6,0.6,1)
    love.graphics.print("WASD:Move  Click:Magic  Space:Melee  E:Search  G:Pickup  R:Restart", 16, 54)

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

    drawMissionPanel(missionState, unlockFlags, onboardingHint and 118 or 84)

    if gameOver then
        love.graphics.setColor(0,0,0,0.6)
        love.graphics.rectangle("fill", 0, 280, love.graphics.getWidth(), 80)
        love.graphics.setColor(1,0.2,0.2,1)
        love.graphics.printf("GAME OVER", 0, 290, love.graphics.getWidth(), "center")
        love.graphics.setColor(0.8,0.8,0.8,1)
        love.graphics.printf("Press R to restart", 0, 320, love.graphics.getWidth(), "center")
    elseif alive == 0 and #enemies > 0 then
        love.graphics.setColor(0,1,0.5,1)
        love.graphics.printf("ALL ENEMIES DEFEATED! Press R to restart", 0, 200, love.graphics.getWidth(), "center")
    end

    drawRunSummary(runSummary)
end

return HUD
