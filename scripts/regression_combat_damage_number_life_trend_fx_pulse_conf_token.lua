-- Regression: compact floating damage-number lifecycle trend FX pulse confidence token (`DMGNUM LIFE TREND FX PULSE CONF:LOW|MID|HIGH`)
-- Run: DOTPIO_EXPERIMENT_DMGNUM_LIFE_CONF_DEBUG=1 DOTPIO_EXPERIMENT_DMGNUM_LIFE_CONF_DELTA_DEBUG=1 DOTPIO_EXPERIMENT_DMGNUM_LIFE_TREND_DEBUG=1 DOTPIO_EXPERIMENT_DMGNUM_LIFE_TREND_FX_PULSE_DEBUG=1 DOTPIO_EXPERIMENT_DMGNUM_LIFE_TREND_FX_PULSE_CONF_DEBUG=1 lua scripts/regression_combat_damage_number_life_trend_fx_pulse_conf_token.lua

local Combat = require("src.combat")
local HUD = require("src.hud")
local Map = require("src.map")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

Map.load("01")
Combat.reset()

local function expectPulseConf(expected)
    local token = HUD.resolveDamageNumberLifeTrendFxPulseConfidenceToken()
    expect(token == ("DMGNUM LIFE TREND FX PULSE CONF:" .. expected), string.format("expected %s, got %s", expected, tostring(token)))
end

local enemy = { hp = 999, alive = true }
local function enemyAt(tx, ty)
    if tx == 2 and ty == 1 and enemy.alive then
        return 1, enemy
    end
    return nil, nil
end

local player = {
    x = 1,
    y = 1,
    aimAngle = 0,
    effectiveStats = { atk = 6, int = 6 },
    attackTimer = 0,
    attackDir = {0, 0},
}

-- Baseline pulse COAST -> LOW confidence.
expectPulseConf("LOW")

-- Fresh hit keeps confidence delta 0 -> COAST -> LOW.
enemy = { hp = 999, alive = true }
Combat.meleeAttack(player, enemyAt)
expectPulseConf("LOW")

-- Mid fade delta magnitude 1 -> RUSH -> MID.
Combat.update(0.30)
expectPulseConf("MID")

-- Late fade still magnitude 1 -> RUSH -> MID.
Combat.update(0.20)
expectPulseConf("MID")

-- Expire jumps by magnitude 2 -> BURST -> HIGH.
Combat.update(0.11)
expectPulseConf("HIGH")

print("[PASS] combat damage-number lifecycle trend FX pulse confidence token regression validated")
