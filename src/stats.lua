local Stats = {}

Stats.PHYS_KEYS = {"atk", "def", "agi", "int"}
Stats.PHYS_LABELS = {"ATK", "DEF", "AGI", "INT"}

Stats.ELEM_KEYS = {"fire", "water", "grass", "elec", "ice", "poison", "earth", "wind"}
Stats.ELEM_LABELS = {"Fire", "Water", "Grass", "Elec", "Ice", "Poison", "Earth", "Wind"}

Stats.ALL_KEYS = {}
for _, k in ipairs(Stats.PHYS_KEYS) do Stats.ALL_KEYS[#Stats.ALL_KEYS + 1] = k end
for _, k in ipairs(Stats.ELEM_KEYS) do Stats.ALL_KEYS[#Stats.ALL_KEYS + 1] = k end

function Stats.zero()
    local s = {}
    for _, k in ipairs(Stats.ALL_KEYS) do s[k] = 0 end
    return s
end

function Stats.defaultBase()
    return {
        atk = 3, def = 3, agi = 3, int = 3,
        fire = 1, water = 1, grass = 1, elec = 1,
        ice = 1, poison = 1, earth = 1, wind = 1,
    }
end

function Stats.computeEffective(baseStats, equippedItemStats)
    local eff = {}
    for _, k in ipairs(Stats.ALL_KEYS) do
        eff[k] = baseStats[k] or 0
    end
    for _, itemStats in ipairs(equippedItemStats) do
        for _, k in ipairs(Stats.ALL_KEYS) do
            eff[k] = eff[k] + (itemStats[k] or 0)
        end
    end
    for _, k in ipairs(Stats.ALL_KEYS) do
        eff[k] = math.max(1, math.min(10, eff[k]))
    end
    return eff
end

function Stats.meleeDamage(baseDmg, effectiveStats)
    return baseDmg * (0.5 + (effectiveStats.atk or 3) * 0.15)
end

function Stats.magicDamage(baseDmg, effectiveStats)
    return baseDmg * (0.5 + (effectiveStats.int or 3) * 0.15)
end

function Stats.damageReduction(rawDmg, effectiveStats)
    return rawDmg * (1.0 - (effectiveStats.def or 3) * 0.07)
end

function Stats.moveCooldown(baseCD, effectiveStats)
    return baseCD * (1.1 - (effectiveStats.agi or 3) * 0.04)
end

return Stats
