-- Regression: combo momentum HUD banner formatting + urgency color mapping
-- Run: lua scripts/regression_combat_combo_momentum_banner.lua

local HUD = require("src.hud")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

local none = HUD.formatComboMomentumBanner({ comboCount = 1, comboTimer = 2.2, heat = "WARM" })
expect(none == nil, "banner should stay hidden for comboCount < 2")

local warm = HUD.formatComboMomentumBanner({ comboCount = 2, comboTimer = 2.4, heat = "WARM" })
expect(warm == "CHAIN x2  WARM  2.4s [STABLE]", "warm stable banner mismatch: " .. tostring(warm))

local hotHold = HUD.formatComboMomentumBanner({ comboCount = 3, comboTimer = 1.4, heat = "HOT" })
expect(hotHold == "CHAIN x3  HOT  1.4s [HOLD]", "hot hold banner mismatch: " .. tostring(hotHold))

local hotNow = HUD.formatComboMomentumBanner({ comboCount = 4, comboTimer = 0.7, heat = "HOT" })
expect(hotNow == "CHAIN x4  HOT  0.7s [NOW]", "hot now banner mismatch: " .. tostring(hotNow))

local ruins = HUD.formatComboMomentumBanner({ comboCount = 3, comboTimer = 1.6, heat = "HOT" }, "RUINS")
expect(ruins == "CHAIN x3  HOT  1.6s [BRACE]", "ruins tier banner mismatch: " .. tostring(ruins))

local forge = HUD.formatComboMomentumBanner({ comboCount = 4, comboTimer = 0.6, heat = "HOT" }, "FORGE")
expect(forge == "CHAIN x4  HOT  0.6s [STRIKE]", "forge tier banner mismatch: " .. tostring(forge))

local abyss = HUD.formatComboMomentumBanner({ comboCount = 2, comboTimer = 2.0, heat = "WARM" }, "ABYSS")
expect(abyss == "CHAIN x2  WARM  2.0s [CALM]", "abyss tier banner mismatch: " .. tostring(abyss))

expect(HUD.resolveComboMomentumMapTier({ mapTier = "forge" }) == "FORGE", "map tier normalize should uppercase valid tier")
expect(HUD.resolveComboMomentumMapTier({ mapTier = "unknown" }) == "DEFAULT", "unknown tier should fallback to DEFAULT")

local r, g, b, a = HUD.getComboMomentumBannerColor({ comboCount = 4, comboTimer = 0.6, heat = "HOT" })
expect(r == 1.0 and g == 0.42 and b == 0.34 and a == 0.96, "hot-now color mismatch")

local wr, wg, wb, wa = HUD.getComboMomentumBannerColor({ comboCount = 2, comboTimer = 2.2, heat = "WARM" })
expect(wr == 0.98 and wg == 0.9 and wb == 0.46 and wa == 0.92, "warm stable color mismatch")

print("[PASS] combat combo momentum banner regression validated")
