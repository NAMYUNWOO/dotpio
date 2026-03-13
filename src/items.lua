local json = require("libs.json")

local Items = {}

Items.defs = {}
Items.gidToItemId = {}
Items.allItemIds = {}

local CATEGORY_DEFAULTS = {
    potion   = { ext="POT", color=14, size=1, stackable=true,  maxStack=10 },
    food     = { ext="FOD", color=14, size=1, stackable=true,  maxStack=10 },
    weapon   = { ext="WPN", color=15, size=3, stackable=false, maxStack=1  },
    armor    = { ext="ARM", color=15, size=3, stackable=false, maxStack=1  },
    helmet   = { ext="HLM", color=15, size=2, stackable=false, maxStack=1  },
    boots    = { ext="BTS", color=15, size=2, stackable=false, maxStack=1  },
    gloves   = { ext="GLV", color=15, size=2, stackable=false, maxStack=1  },
    shield   = { ext="SLD", color=15, size=3, stackable=false, maxStack=1  },
    robe     = { ext="ROB", color=13, size=3, stackable=false, maxStack=1  },
    bow      = { ext="BOW", color=15, size=3, stackable=false, maxStack=1  },
    wand     = { ext="WND", color=13, size=2, stackable=false, maxStack=1  },
    scroll   = { ext="SCR", color=11, size=1, stackable=true,  maxStack=5  },
    book     = { ext="BOK", color=11, size=2, stackable=false, maxStack=1  },
    key      = { ext="KEY", color=14, size=1, stackable=true,  maxStack=5  },
    gem      = { ext="GEM", color=11, size=1, stackable=true,  maxStack=10 },
    ring     = { ext="RNG", color=13, size=1, stackable=false, maxStack=1  },
    necklace = { ext="NKL", color=13, size=1, stackable=false, maxStack=1  },
    crown    = { ext="CRN", color=14, size=2, stackable=false, maxStack=1  },
    coin     = { ext="CON", color=14, size=1, stackable=true,  maxStack=99 },
    bomb     = { ext="BMB", color=12, size=1, stackable=true,  maxStack=5  },
    arrow    = { ext="ARW", color=15, size=1, stackable=true,  maxStack=20 },
    tool     = { ext="TUL", color=7,  size=2, stackable=false, maxStack=1  },
    bag      = { ext="BAG", color=6,  size=2, stackable=false, maxStack=1  },
    belt     = { ext="BLT", color=6,  size=1, stackable=false, maxStack=1  },
    skull    = { ext="SKL", color=8,  size=1, stackable=true,  maxStack=5  },
    bone     = { ext="BNE", color=8,  size=1, stackable=true,  maxStack=5  },
    torch    = { ext="TCH", color=14, size=1, stackable=true,  maxStack=5  },
    box      = { ext="BOX", color=6,  size=3, stackable=false, maxStack=1  },
    misc     = { ext="MIS", color=7,  size=1, stackable=true,  maxStack=5  },
}

local CATEGORY_ON_USE = {
    potion = function(player)
        local amt = love.math.random(5, 10)
        player.mp = math.min(player.mp + amt, player.maxMp)
        return true, "Restored " .. amt .. " MP"
    end,
    food = function(player)
        local amt = love.math.random(3, 8)
        player.hp = math.min(player.hp + amt, player.maxHp)
        return true, "Restored " .. amt .. " HP"
    end,
    scroll = function(player)
        local amt = love.math.random(1, 3)
        player.mp = math.min(player.mp + amt, player.maxMp)
        return true, "Gained " .. amt .. " MP"
    end,
    bomb = function(player)
        return true, "BOOM! Area damage!"
    end,
    gem = function(player)
        return true, "The gem shimmers..."
    end,
    coin = function(player)
        return true, "Added to coin pouch"
    end,
}

local function makeDosName(description)
    local name = description:upper():gsub("%s+", "_"):gsub("[^%w_]", ""):sub(1, 8)
    if name == "" then name = "ITEM" end
    return name
end

function Items.loadFromJson()
    local contents = love.filesystem.read("item_tile_data.json")
    local data = json.decode(contents)
    Items.defs = {}
    Items.gidToItemId = {}
    Items.allItemIds = {}

    for _, entry in ipairs(data.items) do
        local itemId = "item_" .. entry.tiled_id
        local cat = entry.category or "misc"
        local defaults = CATEGORY_DEFAULTS[cat] or CATEGORY_DEFAULTS.misc

        Items.defs[itemId] = {
            name     = makeDosName(entry.description),
            ext      = defaults.ext,
            gid      = entry.gid,
            category = cat,
            color    = defaults.color,
            size     = defaults.size,
            stackable = defaults.stackable,
            maxStack = defaults.maxStack,
            desc     = entry.description,
            tileDesc = cat .. " sprite: " .. entry.description,
            tileRow  = entry.row,
            tileCol  = entry.col,
            onUse    = CATEGORY_ON_USE[cat],
            equip_slot = entry.equip_slot or 0,
        }
        Items.gidToItemId[entry.gid] = itemId
        table.insert(Items.allItemIds, itemId)
    end
end

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
    local defaults = CATEGORY_DEFAULTS[cat]
    if defaults then return defaults.color end
    return 7
end

function Items.getValidSlots(itemId)
    local def = Items.defs[itemId]
    if not def then return {} end
    local es = def.equip_slot
    if es >= 1 and es <= 6 then return {es} end
    if es == 7 then return {7, 8} end
    return {}
end

function Items.isEquippable(itemId)
    return #Items.getValidSlots(itemId) > 0
end

return Items
