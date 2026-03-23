-- Top-down Roguelike with Fan-shaped FOV System
-- Layered map: Ground -> GroundDeco -> Collision -> Player -> Overlay

local Config      = require("src.config")
local Map         = require("src.map")
local Tileset     = require("src.tileset")
local FOV         = require("src.fov")
local Player      = require("src.player")
local Combat      = require("src.combat")
local Entities    = require("src.entities")
local Camera      = require("src.camera")
local HUD         = require("src.hud")
local Portal      = require("src.portal")
local Items       = require("src.items")
local Inventory   = require("src.inventory")
local InventoryUI = require("src.inventory_ui")
local LootboxUI   = require("src.lootbox_ui")
local AiDescribe  = require("src.ai_describe")
local RunMissions = require("src.run_missions")
local Unlocks     = require("src.unlocks")
local FailForward = require("src.fail_forward")
local RunSummary  = require("src.run_summary")
local OnboardingHints = require("src.onboarding_hints")
local OverclockHazard = require("src.overclock_hazard")

local gameOver = false
local autoShotDone = false
local autoShotTimer = 0
local autoShotPath = os.getenv("AUTO_SCREENSHOT")
local autoStartMap = os.getenv("AUTO_START_MAP")
local autoStartPortal = os.getenv("AUTO_START_PORTAL")
local autoOpenInventory = os.getenv("AUTO_OPEN_INVENTORY") == "1"

local lootboxInteract = {
    active = false, lootbox = nil, timer = 0, duration = 0,
}
local hoveredLootbox = nil
local lastPlayerX, lastPlayerY = 0, 0
local missionUnlockAnnounced = false
local threatScoreLastTick = 0
local threatRiseWindow = 0
local berserkerThreatRiseStreak = 0

local function resetRunState()
    RunMissions.reset()
    OnboardingHints.reset()
    OverclockHazard.resetRunTelemetry()
    missionUnlockAnnounced = false
    threatScoreLastTick = 0
    threatRiseWindow = 0
    berserkerThreatRiseStreak = 0
end

local function applyMissionProgress(eventId, amount)
    local risingThreat = threatRiseWindow > 0
    local threatCounters = HUD.collectCombatThreatCounters(Entities.enemies)
    local threatTier = HUD.getBerserkerThreatTier(threatCounters.berserkerThreatScore or 0)
    local completion = RunMissions.addProgress(eventId, amount, { risingThreat = risingThreat, threatTier = threatTier })
    if not completion then
        return
    end

    local rewardSrl = completion.rewardSrl or 0
    local laneBonus = completion.laneSwitchBonusSrl or 0
    local pressureBreakerCharge = completion.pressureBreakerDodgeCharge or 0
    local laneBonusSuffix = ""
    if laneBonus > 0 then
        if completion.threatLinkedVarietyScalerApplied then
            laneBonusSuffix = string.format(" [VARIETY +%d HIGH-THREAT SCALER]", laneBonus)
        else
            laneBonusSuffix = string.format(" [VARIETY +%d]", laneBonus)
        end
    end
    local pressureBreakerSuffix = ""
    if pressureBreakerCharge > 0 then
        local totalCharges = Player.grantDodgeCharge(pressureBreakerCharge, 6)
        pressureBreakerSuffix = string.format(" [PRESSURE BREAKER +%d DODGE (%ds) | READY:%d]", pressureBreakerCharge, 6, totalCharges)
    end

    if rewardSrl <= 0 then
        if pressureBreakerCharge > 0 then
            InventoryUI.setStatus(string.format("MISSION MOMENTUM x%d%s", completion.completionStreak or 1, pressureBreakerSuffix))
        end
        return
    end

    local ok = Inventory.addItem(Player.inventory, "builder_scroll", rewardSrl)
    if ok then
        InventoryUI.setStatus(string.format("MISSION MOMENTUM x%d: +%d BUILDER.SRL%s%s", completion.completionStreak or 1, rewardSrl, laneBonusSuffix, pressureBreakerSuffix))
        return
    end

    InventoryUI.setStatus(string.format("MISSION MOMENTUM x%d: +%d BUILDER.SRL%s%s DROPPED (BAG FULL)", completion.completionStreak or 1, rewardSrl, laneBonusSuffix, pressureBreakerSuffix))
end

local function loadMap(mapName, portalName)
    Map.load(mapName)
    Combat.reset()
    if portalName then
        local portal = Map.getPortalByName(portalName)
        if portal then
            Player.x, Player.y = portal.x, portal.y
        end
        Entities.spawn(Player, true)
        Portal.setCooldown()
    else
        Entities.spawn(Player)
        Portal.resetCooldown()
    end
    Player.visualX, Player.visualY = Player.x, Player.y
    FOV.calculate(Player.x, Player.y, Player.aimAngle)
    gameOver = false
    lootboxInteract = {active = false, lootbox = nil, timer = 0, duration = 0}
    hoveredLootbox = nil
    lastPlayerX, lastPlayerY = Player.x, Player.y
    OverclockHazard.onMapLoaded(Map.currentMap, Map.metadata)

    Map.extraBlockers = function(gx, gy)
        for _, lb in ipairs(Entities.lootboxes) do
            if lb.x == gx and lb.y == gy then return true end
        end
        return false
    end
end

Portal.onLoad = loadMap

------------------------------------------------------------
-- LOVE CALLBACKS
------------------------------------------------------------
function love.load()
    love.graphics.setDefaultFilter("nearest", "nearest")
    Tileset.load()
    Items.loadFromJson()
    InventoryUI.init()
    AiDescribe.init()
    InventoryUI.setBuildCompletedHandler(function()
        OnboardingHints.mark("build")
        applyMissionProgress("build", 1)
    end)
    resetRunState()
    Player.init(0, 0)
    Player.recalcStats()
    loadMap(autoStartMap or "01", autoStartPortal)
    if autoOpenInventory then
        InventoryUI.open(Player, Entities)
    end
end

function love.update(dt)
    AiDescribe.update()
    Player.recalcStats()
    OnboardingHints.update(dt)

    if autoShotPath and not autoShotDone then
        autoShotTimer = autoShotTimer + dt
        if autoShotTimer > 0.5 then
            local shotPath = autoShotPath
            love.graphics.captureScreenshot(function(imgData)
                imgData:encode("png", shotPath)
                print("[AUTO_SCREENSHOT] saved: " .. shotPath)
                love.event.quit()
            end)
            autoShotDone = true
        end
    end
    if InventoryUI.isOpen() then
        InventoryUI.update(dt)
        return
    end
    if LootboxUI.isOpen() then
        LootboxUI.update(dt)
        return
    end
    if RunSummary.isOpen() then
        return
    end
    if gameOver then return end

    local overclockEvents = OverclockHazard.update(dt, Player.x, Player.y)
    local overclockPressure = OverclockHazard.getPressureProfile()
    Entities.setThreatPressure(overclockPressure)
    HUD.setAuxThreatHint(OverclockHazard.getHudHint(), OverclockHazard.getHudHintColor())
    HUD.setRouteCallout(OverclockHazard.getRouteCallout(), OverclockHazard.getRouteCalloutColor())
    if overclockEvents.activated then
        InventoryUI.setStatus("OVERCLOCK ONLINE: BUILD COST DISCOUNT ACTIVE, ENEMIES AGGRO BOOSTED")
    elseif overclockEvents.expired then
        InventoryUI.setStatus("OVERCLOCK COOLED: SRL DISCOUNT OFF")
    end
    local retreatBonusCharges = math.max(0, math.floor(tonumber(overclockEvents.retreatStreakBonusDodgeCharges) or 0))
    if retreatBonusCharges > 0 then
        local totalCharges = Player.grantDodgeCharge(retreatBonusCharges, 6)
        InventoryUI.setStatus(string.format("OVERCLOCK RETREAT STREAK: +%d DODGE (%ds) | READY:%d", retreatBonusCharges, 6, totalCharges))
    end

    threatRiseWindow = math.max(0, threatRiseWindow - dt)

    Player.update(dt, Camera)
    FOV.calculate(Player.x, Player.y, Player.aimAngle)
    Combat.update(dt, Entities.enemyAt)
    local kills = Combat.consumeKillCount()
    if kills > 0 then
        applyMissionProgress("kills", kills)
        local overclockKillBonus = OverclockHazard.consumeKillBonus(kills)
        if overclockKillBonus > 0 then
            if Inventory.addItem(Player.inventory, "builder_scroll", overclockKillBonus) then
                InventoryUI.setStatus(string.format("OVERCLOCK BOUNTY: +%d BUILDER.SRL (HOT ZONE KILL)", overclockKillBonus))
            else
                InventoryUI.setStatus(string.format("OVERCLOCK BOUNTY: +%d BUILDER.SRL DROPPED (BAG FULL)", overclockKillBonus))
            end
        end
    end

    local missionState = RunMissions.getState()
    if missionState.completed and not missionUnlockAnnounced then
        if Unlocks.unlock("advanced_build_categories") then
            InventoryUI.setStatus("UNLOCKED: ADVANCED SCHEMATICS (RING/WAND/GEM)")
        else
            InventoryUI.setStatus("MISSIONS CLEARED: ADVANCED SCHEMATICS READY")
        end
        missionUnlockAnnounced = true
    end

    local enemyEvents = Entities.update(dt, Player, Combat.addDamageFlash) or {}

    local threatCounters = HUD.collectCombatThreatCounters(Entities.enemies)
    local threatScore = threatCounters.berserkerThreatScore or 0
    local previousThreatScore = threatScoreLastTick
    local previousRiseStreak = berserkerThreatRiseStreak
    local berserkFxPulseTriggered, nextRiseStreak, threatDelta = HUD.shouldTriggerBerserkerFxPulse(threatScore, previousThreatScore, previousRiseStreak)
    local berserkFxFadeTriggered = HUD.shouldTriggerBerserkerFxFade(previousThreatScore, threatDelta, previousRiseStreak)
    berserkerThreatRiseStreak = nextRiseStreak
    if threatScore > previousThreatScore then
        threatRiseWindow = math.max(threatRiseWindow, 0.9)
    end
    threatScoreLastTick = threatScore

    local visibleEnrageCount = 0
    for _, enemy in ipairs(Entities.enemies) do
        if enemy.justEnteredDesperation then
            if FOV.isVisible(enemy.x, enemy.y) then
                visibleEnrageCount = visibleEnrageCount + 1
            end
            enemy.justEnteredDesperation = false
        end
    end
    if visibleEnrageCount > 0 then
        OnboardingHints.mark("threat")
        local threatHint = "THREAT=B+2L+R"
        if visibleEnrageCount == 1 then
            InventoryUI.setStatus(string.format("BERSERKER ENRAGED: LOW-HP SPIKE INCOMING [%s]", threatHint))
        else
            InventoryUI.setStatus(string.format("BERSERKERS ENRAGED x%d: LOW-HP SPIKES INCOMING [%s]", visibleEnrageCount, threatHint))
        end
    end

    if (enemyEvents.berserkerLungeTelegraphs or 0) > 0 then
        OnboardingHints.mark("threat")
        local telegraphCount = enemyEvents.berserkerLungeTelegraphs
        if telegraphCount == 1 then
            InventoryUI.setStatus("BERSERKER LUNGE TELL: IMPACT NEXT TURN")
        else
            InventoryUI.setStatus(string.format("BERSERKER LUNGE TELLS x%d: IMPACT NEXT TURN", telegraphCount))
        end
    elseif (enemyEvents.berserkerLungeRecoveries or 0) > 0 then
        local recoveryCount = enemyEvents.berserkerLungeRecoveries
        if recoveryCount == 1 then
            InventoryUI.setStatus("BERSERKER RECOVERING: BRIEF BREATHER")
        else
            InventoryUI.setStatus(string.format("BERSERKERS RECOVERING x%d: BRIEF BREATHER", recoveryCount))
        end
    elseif (enemyEvents.dodges or 0) > 0 then
        local dodgeCount = enemyEvents.dodges
        if dodgeCount == 1 then
            InventoryUI.setStatus("PRESSURE BREAKER: DODGE CHARGE TRIGGERED")
        else
            InventoryUI.setStatus(string.format("PRESSURE BREAKER: DODGE CHARGES TRIGGERED x%d", dodgeCount))
        end
    elseif berserkFxPulseTriggered then
        OnboardingHints.mark("threat")
        local pulseDelta = threatDelta > 0 and ("+" .. threatDelta) or tostring(threatDelta)
        InventoryUI.setStatus(string.format("BERSERK FX:PULSE  [THREAT Δ:%s]", pulseDelta))
    elseif berserkFxFadeTriggered then
        local fadeDelta = threatDelta > 0 and ("+" .. threatDelta) or tostring(threatDelta)
        local fadeTier = HUD.getBerserkerFxFadeTier(previousThreatScore, threatDelta)
        InventoryUI.setStatus(string.format("BERSERK FX:FADE(%s)  [THREAT Δ:%s]", fadeTier, fadeDelta))
    end

    Camera.update(Player.visualX, Player.visualY)

    if Player.hp <= 0 then
        Player.hp = 0
        gameOver = true
    end

    Portal.check(Player.x, Player.y, Map)

    -- Detect player movement → reset lootbox interact
    if Player.x ~= lastPlayerX or Player.y ~= lastPlayerY then
        lootboxInteract.active = false
        lootboxInteract.timer = 0
        lastPlayerX, lastPlayerY = Player.x, Player.y
    end

    -- Proximity + FOV lootbox detection (Chebyshev distance ≤ 1)
    hoveredLootbox = nil
    local bestDist = math.huge
    for _, lb in ipairs(Entities.lootboxes) do
        local dx = math.abs(lb.x - Player.x)
        local dy = math.abs(lb.y - Player.y)
        local rdx, rdy = lb.x - Player.x, lb.y - Player.y
        local ang = math.abs(math.atan2(rdy, rdx) - Player.aimAngle)
        if ang > math.pi then ang = 2*math.pi - ang end
        if dx <= 1 and dy <= 1 and ang <= Config.FOV_HALF then
            local dist = math.max(dx, dy)
            if dist < bestDist then
                bestDist = dist
                hoveredLootbox = lb
            end
        end
    end

    -- E key hold for progress bar
    if love.keyboard.isDown("e") and hoveredLootbox then
        if not lootboxInteract.active or lootboxInteract.lootbox ~= hoveredLootbox then
            lootboxInteract.active = true
            lootboxInteract.lootbox = hoveredLootbox
            lootboxInteract.timer = 0
            lootboxInteract.duration = hoveredLootbox.locked
                and Config.LOOTBOX_BREACH_TIME or Config.LOOTBOX_SEARCH_TIME
        end
        lootboxInteract.timer = lootboxInteract.timer + dt
        if lootboxInteract.timer >= lootboxInteract.duration then
            LootboxUI.open(hoveredLootbox, Player)
            OnboardingHints.mark("searched")
            applyMissionProgress("search", 1)
            lootboxInteract.active = false
            lootboxInteract.timer = 0
            hoveredLootbox = nil
        end
    else
        lootboxInteract.active = false
        lootboxInteract.timer = 0
    end
end

function love.draw()
    Camera.apply()

    -- Layers
    Tileset.drawLayer(Map.Ground, FOV, true)
    Tileset.drawLayer(Map.GroundDeco, FOV, true)
    Tileset.drawLayer(Map.Collision, FOV, true)

    -- Lootboxes, Items & Enemies
    Entities.drawLootboxes(FOV, Tileset)
    Entities.drawItems(FOV, Tileset)
    Entities.drawEnemies(FOV, Tileset)

    -- Effects & Player
    Combat.drawEffects()
    Player.draw()
    Combat.drawProjectiles()

    -- Overlay
    Tileset.drawLayer(Map.Overlay, FOV, true)

    -- FOV cone border
    local TILE = Config.TILE
    love.graphics.setColor(0.3,0.5,1, 0.12)
    love.graphics.arc("fill", (Player.visualX-1)*TILE+TILE/2, (Player.visualY-1)*TILE+TILE/2,
        Config.FOV_RANGE*TILE, Player.aimAngle-Config.FOV_HALF, Player.aimAngle+Config.FOV_HALF)

    -- Aim crosshair
    local mx, my = love.mouse.getPosition()
    local agx = math.floor((mx+Camera.x)/(TILE*Config.SCALE)) + 1
    local agy = math.floor((my+Camera.y)/(TILE*Config.SCALE)) + 1
    if Map.inBounds(agx, agy) then
        love.graphics.setColor(1,0.3,0.3, 0.5+0.2*math.sin(love.timer.getTime()*6))
        love.graphics.rectangle("line", (agx-1)*TILE, (agy-1)*TILE, TILE, TILE)
        local cx = (agx-1)*TILE+TILE/2
        local cy = (agy-1)*TILE+TILE/2
        love.graphics.line(cx-4,cy, cx+4,cy)
        love.graphics.line(cx,cy-4, cx,cy+4)
    end

    love.graphics.pop()

    -- HUD
    HUD.draw(Player, Entities.enemies, gameOver, RunMissions.getState(), Unlocks.getAllFlags(), RunSummary.getState(), OnboardingHints.getHint())
    drawPortalTransitionPrompt()

    -- Lootbox hover tooltip (with integrated progress fill)
    if hoveredLootbox and not LootboxUI.isOpen() then
        local TILE = Config.TILE
        local label = hoveredLootbox.locked and "[E] Breach & Search" or "[E] Search"
        local isLocked = hoveredLootbox.locked
        local tw = #label * 8 + 8
        local th = 20
        local sx = (hoveredLootbox.x - 1) * TILE * Config.SCALE - Camera.x
        local sy = (hoveredLootbox.y - 1) * TILE * Config.SCALE - Camera.y
        local tx, ty = sx + (TILE * Config.SCALE - tw) / 2, sy - th - 4

        -- Dark background
        love.graphics.setColor(0, 0, 0, 0.8)
        love.graphics.rectangle("fill", tx, ty, tw, th, 3, 3)

        -- Progress fill (left to right)
        if lootboxInteract.active and lootboxInteract.duration > 0 then
            local progress = math.min(lootboxInteract.timer / lootboxInteract.duration, 1)
            if isLocked then
                love.graphics.setColor(1, 0.5, 0, 0.6)
            else
                love.graphics.setColor(0.3, 1, 0.5, 0.6)
            end
            love.graphics.rectangle("fill", tx, ty, tw * progress, th, 3, 3)
        end

        -- Label text
        local fg = isLocked and {1, 0.5, 0} or {0.3, 1, 0.5}
        love.graphics.setColor(fg[1], fg[2], fg[3], 1)
        love.graphics.print(label, tx + 4, ty + 4)
    end

    -- Inventory overlay (drawn last, on top of everything)
    if InventoryUI.isOpen() then
        InventoryUI.draw()
    end

    -- Lootbox UI overlay
    if LootboxUI.isOpen() then
        LootboxUI.draw()
    end
end

local function drawPortalTransitionPrompt()
    local threatCounters = HUD.collectCombatThreatCounters(Entities.enemies)
    local threatTier = HUD.getBerserkerThreatTier(threatCounters.berserkerThreatScore or 0)
    local prompt = Portal.getTransitionPrompt(nil, { threatTier = threatTier })
    if not prompt then
        return
    end

    local w = love.graphics.getWidth()
    local h = love.graphics.getHeight()
    local boxW = math.min(w - 80, math.max(460, (#prompt * 7) + 24))
    local boxH = 56
    local boxX = math.floor((w - boxW) / 2)
    local boxY = h - 118

    love.graphics.setColor(0, 0, 0, 0.86)
    love.graphics.rectangle("fill", boxX, boxY, boxW, boxH, 5, 5)
    love.graphics.setColor(0.95, 0.95, 0.7, 1)
    love.graphics.printf("PORTAL TRANSITION", boxX + 12, boxY + 8, boxW - 24, "left")
    love.graphics.setColor(0.78, 0.9, 1, 1)
    love.graphics.printf(prompt, boxX + 12, boxY + 28, boxW - 24, "left")
end

local function tryPickupItem()
    local itemIndex, item = Entities.itemAt(Player.x, Player.y)
    if not item then
        return
    end

    local ok, err = Inventory.addItem(Player.inventory, item.itemId, 1)
    if not ok then
        InventoryUI.setStatus("PICKUP FAILED: " .. ((err or "error"):upper()))
        return
    end

    item.collected = true
    Entities.removeItem(itemIndex)
    OnboardingHints.mark("pickup")
    applyMissionProgress("pickup", 1)

    local itemName = item.itemId
    local def = Items.get(item.itemId)
    if def and def.name then
        itemName = def.name
    end
    InventoryUI.setStatus("PICKUP OK: " .. itemName:upper())
end

function love.keypressed(key)
    if InventoryUI.isOpen() then
        InventoryUI.keypressed(key)
        return
    end
    if LootboxUI.isOpen() then
        LootboxUI.keypressed(key)
        return
    end
    if RunSummary.isOpen() then
        if key == "r" or key == "return" or key == "escape" then
            RunSummary.close()
        end
        return
    end
    if Portal.hasPendingTransition() then
        if key == "return" or key == "kpenter" or key == "y" or key == "e" then
            local confirmed = Portal.confirmTransition()
            if confirmed then
                local vibeSyncDodgeCharges = Portal.consumeVibeSyncDodgeCharges()
                if vibeSyncDodgeCharges > 0 then
                    local totalCharges = Player.grantDodgeCharge(vibeSyncDodgeCharges, 6)
                    InventoryUI.setStatus(string.format("VIBE SYNC DODGE:+%d (%ds) | READY:%d", vibeSyncDodgeCharges, 6, totalCharges))
                end
            end
        elseif key == "n" or key == "backspace" or key == "escape" then
            Portal.cancelTransition()
        end
        return
    end
    if key == "w" or key == "a" or key == "s" or key == "d" then
        OnboardingHints.mark("moved")
    end
    if key == "tab" or key == "i" then
        OnboardingHints.mark("inventory")
        applyMissionProgress("inventory", 1)
        InventoryUI.open(Player, Entities)
        return
    end
    if key == "r" then
        local missionState = RunMissions.getState()
        local unlockFlags = Unlocks.getAllFlags()
        local carryReward = FailForward.compute(Player.inventory, missionState)
        local overclockDwellBuckets = OverclockHazard.getRunDwellBuckets()
        local overclockRewardSrl = OverclockHazard.getRunRewardSrl()
        OverclockHazard.writeRunDwellArtifact("logs/playtests/overclock_dwell_buckets_latest")
        OverclockHazard.writeRunDwellArtifact("logs/playtests/overclock_dwell_buckets_run_" .. os.date("%Y%m%d_%H%M%S"))

        Player.inventory = nil
        resetRunState()
        Player.init(0, 0)

        local applied = FailForward.apply(Player.inventory, carryReward)
        InventoryUI.setStatus(FailForward.formatStatus(applied))
        RunSummary.open(missionState, unlockFlags, applied, overclockDwellBuckets, overclockRewardSrl)

        loadMap("01", nil)
        return
    end
    if gameOver then return end
    if key == "g" then
        tryPickupItem()
    elseif key == "space" then
        Combat.meleeAttack(Player, Entities.enemyAt)
    elseif key == "escape" then
        love.event.quit()
    end
end

function love.textinput(text)
    if InventoryUI.isOpen() then
        InventoryUI.textinput(text)
    end
end

function love.quit()
    AiDescribe.shutdown()
end

function love.mousepressed(x, y, button)
    if InventoryUI.isOpen() then return end
    if LootboxUI.isOpen() then return end
    if gameOver then return end
    if button == 1 then
        local tx = (x + Camera.x) / (Config.TILE*Config.SCALE) + 0.5
        local ty = (y + Camera.y) / (Config.TILE*Config.SCALE) + 0.5
        Combat.castMagic(Player, tx, ty)
    end
end
