local Items = {}

Items.defs = {
    mp_potion = {
        name = "MP_POT",  ext = "POT", gid = 817,
        category = "potion", color = 14, size = 1,
        stackable = true, maxStack = 10,
        desc = "Restores 5-10 MP",
        tileDesc = "Blue potion bottle icon",
        onUse = function(player)
            local restore = love.math.random(5, 10)
            player.mp = math.min(player.maxMp, player.mp + restore)
            return true, "Restored " .. restore .. " MP"
        end,
    },
    hp_potion = {
        name = "HP_POT",  ext = "POT", gid = 818,
        category = "potion", color = 14, size = 1,
        stackable = true, maxStack = 10,
        desc = "Restores 5-10 HP",
        tileDesc = "Glass potion bottle icon",
        onUse = function(player)
            local restore = love.math.random(5, 10)
            player.hp = math.min(player.maxHp, player.hp + restore)
            return true, "Restored " .. restore .. " HP"
        end,
    },
    sword_rusty = {
        name = "RUSTYSWD", ext = "SWD", gid = 819,
        category = "weapon", color = 9, size = 3,
        stackable = false,
        desc = "A rusty sword. +2 ATK",
        tileDesc = "Brown potion bottle icon",
    },
    scroll_fire = {
        name = "FIRSCROL", ext = "SCR", gid = 820,
        category = "scroll", color = 11, size = 1,
        stackable = true, maxStack = 5,
        desc = "Casts fire spell",
        tileDesc = "Pixel art exclamation mark icon",
    },
    key_brass = {
        name = "BRASSKEY", ext = "KEY", gid = 821,
        category = "key", color = 13, size = 1,
        stackable = true, maxStack = 3,
        desc = "Opens locked doors",
        tileDesc = "Exclamation mark icon for alerts",
    },
    shield_wood = {
        name = "WOODSHLD", ext = "SHD", gid = 822,
        category = "armor", color = 10, size = 3,
        stackable = false,
        desc = "Wooden shield. +1 DEF",
        tileDesc = "Pixel art question mark icon",
    },
}

local categoryColors = {
    potion = 14,
    weapon = 9,
    scroll = 11,
    key    = 13,
    armor  = 10,
}

function Items.get(itemId)
    return Items.defs[itemId]
end

function Items.dosName(itemId, idx)
    local def = Items.defs[itemId]
    if not def then return "UNKNOWN.???" end
    local name = def.name
    if idx and idx > 0 then
        local suffix = "~" .. tostring(idx)
        local maxBase = 8 - #suffix
        if #name > maxBase then
            name = name:sub(1, maxBase)
        end
        name = name .. suffix
    end
    return name .. "." .. def.ext
end

function Items.categoryColor(cat)
    return categoryColors[cat] or 7
end

-- Map from GID to itemId for pickup
Items.gidToItemId = {}
for id, def in pairs(Items.defs) do
    Items.gidToItemId[def.gid] = id
end

-- Spawn pool: weighted list of item IDs for random spawning
Items.spawnPool = {
    "mp_potion", "mp_potion", "mp_potion",
    "hp_potion", "hp_potion",
    "scroll_fire",
    "key_brass",
    "sword_rusty",
    "shield_wood",
}

return Items
