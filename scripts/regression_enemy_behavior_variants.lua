-- Enemy behavior variant regression
-- Run: lua scripts/regression_enemy_behavior_variants.lua

if not love then love = {} end
if not love.math then love.math = {} end
if not love.math.random then
    function love.math.random(a, b)
        if not a then return 0.5 end
        if not b then return 1 end
        return a
    end
end

local EnemyAI = require("src.enemy_ai")
local Entities = require("src.entities")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

local variantRoster = Entities.getEnemyBehaviorVariants()
expect(#variantRoster >= 7, "expected at least 7 spawn variants including berserker experiment")

local byName = {}
for _, name in ipairs(variantRoster) do byName[name] = true end
expect(
    byName.skirmisher and byName.bruiser and byName.sentinel and byName.warcaller and byName.hunter and byName.berserker,
    "missing required behavior variants"
)

local probe = {
    raider = { x = 1, y = 1, behavior = "raider", hp = 3, alive = true },
    skirmisher = { x = 1, y = 1, behavior = "skirmisher", hp = 3, alive = true },
    bruiser = { x = 1, y = 1, behavior = "bruiser", hp = 3, alive = true },
    sentinel = { x = 1, y = 1, behavior = "sentinel", hp = 3, alive = true },
    warcaller = { x = 2, y = 1, behavior = "warcaller", hp = 4, alive = true, state = "idle", alerted = false },
    hunter = { x = 3, y = 1, behavior = "hunter", hp = 3, alive = true, state = "idle", alerted = false },
    berserker = { x = 4, y = 1, behavior = "berserker", hp = 4, alive = true, state = "idle", alerted = false },
    ally = { x = 2, y = 2, behavior = "raider", hp = 3, alive = true, state = "idle", alerted = false },
}

for _, enemy in pairs(probe) do EnemyAI.init(enemy, 1) end

expect(probe.skirmisher.moveCd < probe.raider.moveCd, "skirmisher should move faster than raider")
expect(probe.bruiser.atkDmg > probe.raider.atkDmg, "bruiser should hit harder than raider")
expect(probe.sentinel.leashRadius ~= nil, "sentinel should have leash radius")
expect(probe.skirmisher.retreatAfterHit == true, "skirmisher should retreat after hit")

local berserkerBaseMove = probe.berserker.moveCd
local berserkerBaseAtkCd = probe.berserker.atkCd
local berserkerBaseAtk = probe.berserker.atkDmg
local _, desperationOff = EnemyAI.debugSyncSynergy(probe.berserker, { probe.berserker })
expect(desperationOff == false and probe.berserker.desperationActive == false, "berserker should not be desperate at full HP")
expect(probe.berserker.justEnteredDesperation == false, "berserker should not emit desperation entry signal at full HP")
probe.berserker.hp = 2
local _, desperationOn = EnemyAI.debugSyncSynergy(probe.berserker, { probe.berserker })
expect(desperationOn == true and probe.berserker.desperationActive == true, "berserker should trigger desperation at low HP")
expect(probe.berserker.justEnteredDesperation == true, "berserker should emit entry signal when desperation first activates")
expect(probe.berserker.moveCd < berserkerBaseMove, "berserker desperation should increase move speed")
expect(probe.berserker.atkCd < berserkerBaseAtkCd, "berserker desperation should increase attack cadence")
expect(probe.berserker.atkDmg > berserkerBaseAtk, "berserker desperation should increase attack damage")

EnemyAI.debugSyncSynergy(probe.berserker, { probe.berserker })
expect(probe.berserker.justEnteredDesperation == false, "berserker entry signal should only fire on transition")

local telegraphFirst = EnemyAI.debugConsumeDesperationAttackWindow(probe.berserker)
expect(telegraphFirst == true and probe.berserker.desperationLungePrimed == true, "berserker desperate attack should telegraph before first lunge")
local telegraphSecond = EnemyAI.debugConsumeDesperationAttackWindow(probe.berserker)
expect(telegraphSecond == false and probe.berserker.desperationLungePrimed == false, "berserker lunge should resolve after telegraph window")

probe.berserker.desperationRecoveryPending = true
local recoveryFirst = EnemyAI.debugConsumeDesperationRecoveryWindow(probe.berserker)
expect(recoveryFirst == true and probe.berserker.desperationRecoveryPending == false, "berserker should consume one-turn post-lunge recovery window")
local recoverySecond = EnemyAI.debugConsumeDesperationRecoveryWindow(probe.berserker)
expect(recoverySecond == false, "berserker should only recover for a single turn")

probe.berserker.hp = 3
EnemyAI.debugSyncSynergy(probe.berserker, { probe.berserker })
expect(
    probe.berserker.desperationActive == false
        and probe.berserker.desperationLungePrimed == false
        and probe.berserker.desperationRecoveryPending == false,
    "lunge telegraph/recovery windows should reset when berserker leaves desperation"
)

local hunterSolo = { x = 8, y = 8, behavior = "hunter", hp = 3, alive = true }
EnemyAI.init(hunterSolo, 1)
local soloMoveCd = hunterSolo.moveCd
local soloAtk = hunterSolo.atkDmg
EnemyAI.debugSyncSynergy(hunterSolo, { hunterSolo })
expect(hunterSolo.moveCd == soloMoveCd and hunterSolo.atkDmg == soloAtk, "hunter should not be buffed without warcaller")

EnemyAI.debugSyncSynergy(probe.hunter, { probe.hunter, probe.warcaller })
expect(probe.hunter.synergyEmpowered == true, "hunter should be empowered near warcaller")
expect(probe.hunter.moveCd < soloMoveCd, "hunter empowered moveCd should be reduced")
expect(probe.hunter.atkDmg > soloAtk, "hunter empowered attack should increase")

local alertedCount = EnemyAI.debugAlertNearbyAllies(probe.warcaller, { probe.warcaller, probe.ally, probe.hunter })
expect(alertedCount >= 1, "warcaller should alert nearby allies")
expect(probe.ally.alerted == true, "warcaller should set ally alerted flag")
expect(probe.ally.state == "chase", "warcaller alert should force idle ally into chase")

print("[PASS] enemy behavior variants + synergy regression validated")
