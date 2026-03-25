-- Regression: compact floating damage-number lifecycle trend FX pulse token (`DMGNUM LIFE TREND FX PULSE:COAST|RUSH|BURST`)
-- Run: DOTPIO_EXPERIMENT_DMGNUM_LIFE_CONF_DEBUG=1 DOTPIO_EXPERIMENT_DMGNUM_LIFE_CONF_DELTA_DEBUG=1 DOTPIO_EXPERIMENT_DMGNUM_LIFE_TREND_DEBUG=1 DOTPIO_EXPERIMENT_DMGNUM_LIFE_TREND_FX_PULSE_DEBUG=1 lua scripts/regression_combat_damage_number_life_trend_fx_pulse_token.lua

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

local function expectTrendFxPulse(expected)
    local token = HUD.resolveDamageNumberLifeTrendFxPulseToken()
    expect(token == ("DMGNUM LIFE TREND FX PULSE:" .. expected), string.format("expected %s, got %s", expected, tostring(token)))
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

-- Baseline trend HOLD + zero delta maps to COAST.
expectTrendFxPulse("COAST")

-- Fresh hit keeps confidence band steady => delta 0 => COAST.
enemy = { hp = 999, alive = true }
Combat.meleeAttack(player, enemyAt)
expectTrendFxPulse("COAST")

-- Mid fade confidence drops HIGH->MID => |Δ|=1 => RUSH.
Combat.update(0.30)
expectTrendFxPulse("RUSH")

-- Late fade confidence drops MID->LOW => |Δ|=1 => RUSH.
Combat.update(0.20)
expectTrendFxPulse("RUSH")

-- Expire confidence jumps LOW->HIGH => |Δ|=2 => BURST.
Combat.update(0.11)
expectTrendFxPulse("BURST")

print("[PASS] combat damage-number lifecycle trend FX pulse token regression validated")
