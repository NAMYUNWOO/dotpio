local HUD = {}

local function drawMissionPanel(missionState, unlockFlags)
    if not missionState or not missionState.active then
        return
    end

    love.graphics.setColor(0, 0, 0, 0.72)
    love.graphics.rectangle("fill", 8, 84, 320, 92)

    local headerColor = missionState.completed and {0.4, 1, 0.6, 1} or {0.95, 0.9, 0.6, 1}
    love.graphics.setColor(headerColor)
    love.graphics.print(string.format("RUN MISSIONS %d/%d", missionState.doneCount or 0, missionState.total or 0), 16, 90)

    local row = 108
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

function HUD.draw(player, enemies, gameOver, missionState, unlockFlags)
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
    for _, e in ipairs(enemies) do if e.alive then alive = alive+1 end end
    love.graphics.setColor(1,0.5,0.5,1)
    love.graphics.print("Enemies: "..alive, 160, 14)
    love.graphics.setColor(0.6,0.6,0.6,1)
    love.graphics.print("WASD:Move  Click:Magic  Space:Melee  E:Search  G:Pickup  R:Restart", 16, 54)
    love.graphics.setColor(0.5,0.5,0.5,0.8)
    love.graphics.print(string.format("Pos: %d,%d", player.x, player.y), 16, 690)

    drawMissionPanel(missionState, unlockFlags)

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
end

return HUD
