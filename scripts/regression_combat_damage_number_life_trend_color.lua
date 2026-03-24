-- Regression: optional trend-accent color mapping for `DMGNUM LIFE TREND` token
-- Run: DOTPIO_EXPERIMENT_DMGNUM_LIFE_TREND_COLOR_DEBUG=1 lua scripts/regression_combat_damage_number_life_trend_color.lua

local HUD = require("src.hud")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

local function approx(a, b)
    return math.abs(a - b) < 1e-6
end

local function expectColor(actual, expected, label)
    expect(#actual == 4, string.format("%s expected RGBA length 4, got %d", label, #actual))
    for i = 1, 4 do
        expect(approx(actual[i], expected[i]), string.format("%s channel %d expected %.4f got %.4f", label, i, expected[i], actual[i]))
    end
end

local function srgbToLinear(c)
    if c <= 0.04045 then
        return c / 12.92
    end
    return ((c + 0.055) / 1.055) ^ 2.4
end

local function relativeLuminance(r, g, b)
    return (0.2126 * srgbToLinear(r)) + (0.7152 * srgbToLinear(g)) + (0.0722 * srgbToLinear(b))
end

local function contrastAgainstBlack(r, g, b)
    local l1 = relativeLuminance(r, g, b)
    local l2 = 0
    return (math.max(l1, l2) + 0.05) / (math.min(l1, l2) + 0.05)
end

local function colorFor(token)
    return { HUD.resolveDamageNumberLifeTrendColor(token) }
end

-- With color experiment enabled, each trend maps to deterministic accent color.
local up = colorFor("DMGNUM LIFE TREND:UP")
local hold = colorFor("DMGNUM LIFE TREND:HOLD")
local down = colorFor("DMGNUM LIFE TREND:DOWN")

expectColor(up, {0.46, 0.96, 0.52, 0.92}, "UP")
expectColor(hold, {1.0, 0.83, 0.32, 0.92}, "HOLD")
expectColor(down, {1.0, 0.46, 0.46, 0.92}, "DOWN")

-- DOS contrast budget: keep all accents comfortably legible against black HUD backdrop.
expect(contrastAgainstBlack(up[1], up[2], up[3]) >= 4.5, "UP accent contrast below 4.5:1")
expect(contrastAgainstBlack(hold[1], hold[2], hold[3]) >= 4.5, "HOLD accent contrast below 4.5:1")
expect(contrastAgainstBlack(down[1], down[2], down[3]) >= 4.5, "DOWN accent contrast below 4.5:1")

print("[PASS] combat damage-number trend color mapping + DOS contrast budget regression validated")
