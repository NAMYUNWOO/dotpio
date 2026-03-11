local DosUI = require("src.dos_ui")
local Items = require("src.items")
local Inventory = require("src.inventory")
local Config = require("src.config")
local AiDescribe = require("src.ai_describe")

local InventoryUI = {}

local state = "closed"  -- closed, browsing, dialog, action_menu, equip_select
local player = nil
local entities = nil
local cursor = 1
local scrollOffset = 0
local contents = {}
local sortMode = "name"
local sortModes = {"name", "type", "size"}
local sortIndex = 1
local statusMsg = ""
local statusTimer = 0

-- Panel focus
local focusPanel = "files"  -- "files" or "equip"
local equipCursor = 1       -- 1~8 for equip panel

-- Dialog state
local dialogType = nil   -- "mkdir", "delete", "drop", "help", "move"
local dialogInput = ""
local dialogTarget = nil
local moveDirs = {}
local moveCursor = 1

-- Action menu state
local actionMenuCursor = 1
local actionMenuItems = {}
local actionMenuTarget = nil

-- Equip select state
local equipValidSlots = {}
local equipSelectCursor = 1
local equipSelectTarget = nil

-- Equip slot definitions
local EQUIP_SLOTS = {
    {name = "Head",   label = "Head  "},
    {name = "Body",   label = "Body  "},
    {name = "RHand",  label = "RHand "},
    {name = "LHand",  label = "LHand "},
    {name = "Feet",   label = "Feet  "},
    {name = "Glove",  label = "Glove "},
    {name = "Acc.1",  label = "Acc.1 "},
    {name = "Acc.2",  label = "Acc.2 "},
}

-- Layout constants (3-panel: Equip | Files | Info)
local PANEL_COL = 1
local PANEL_W = 98
local TITLE_ROW = 2
local BOX_TOP = 3
local BOX_H = 35
local BOX_BOT = BOX_TOP + BOX_H - 1

local EQUIP_INNER_COL = 2
local EQUIP_INNER_W = 20
local DIVIDER1_COL = 22
local LIST_INNER_COL = 23
local LIST_INNER_W = 50
local DIVIDER2_COL = 73
local INFO_INNER_COL = 74
local INFO_INNER_W = 24

local CONTENT_TOP = BOX_TOP + 1
local CONTENT_BOT = BOX_BOT - 1
local VISIBLE_ROWS = CONTENT_BOT - CONTENT_TOP + 1

local STATUS_ROW = BOX_BOT + 1
local HELP_ROW = STATUS_ROW + 1

-- Word-wrap text into lines of at most `w` characters
local function wordWrap(text, w)
    local lines = {}
    for _, paragraph in ipairs(type(text) == "string" and {text} or text) do
        local remaining = paragraph
        while #remaining > 0 do
            if #remaining <= w then
                lines[#lines+1] = remaining
                break
            end
            local cut = w
            local space = remaining:sub(1, w):find("%s[^%s]*$")
            if space and space > 1 then
                cut = space - 1
            end
            lines[#lines+1] = remaining:sub(1, cut)
            local next_pos = cut + 1
            if remaining:byte(next_pos) == 32 then next_pos = next_pos + 1 end
            remaining = remaining:sub(next_pos)
        end
    end
    return lines
end

function InventoryUI.init()
    DosUI.init()
end

function InventoryUI.isOpen()
    return state ~= "closed"
end

function InventoryUI.open(p, ents)
    player = p
    entities = ents
    state = "browsing"
    focusPanel = "files"
    cursor = 1
    scrollOffset = 0
    statusMsg = ""
    statusTimer = 0
    InventoryUI.refreshContents()
end

function InventoryUI.close()
    state = "closed"
    dialogType = nil
end

function InventoryUI.refreshContents()
    if not player or not player.inventory then
        contents = {}
        return
    end
    contents = Inventory.getContents(player.inventory.currentDir)
    if player.inventory.currentDir.parent then
        table.insert(contents, 1, {type = "up", name = "..", parent = player.inventory.currentDir.parent})
    end
    if cursor > #contents then cursor = math.max(1, #contents) end
    if cursor < 1 then cursor = 1 end
end

function InventoryUI.update(dt)
    if statusTimer > 0 then
        statusTimer = statusTimer - dt
        if statusTimer <= 0 then
            statusMsg = ""
        end
    end
end

function InventoryUI.setStatus(msg)
    statusMsg = msg
    statusTimer = 3
end

------------------------------------------------------------
-- DRAWING
------------------------------------------------------------

function InventoryUI.draw()
    love.graphics.setColor(0, 0, 0, 0.95)
    love.graphics.rectangle("fill", 0, 0, love.graphics.getWidth(), love.graphics.getHeight())

    local cw, ch = DosUI.getCellSize()
    local uiScale = love.graphics.getHeight() / (DosUI.ROWS * ch)
    local uiW = DosUI.COLS * cw * uiScale
    local ox, oy = DosUI.getOffset()
    love.graphics.push()
    love.graphics.translate((love.graphics.getWidth() - uiW) / 2 - ox * uiScale, -oy * uiScale)
    love.graphics.scale(uiScale, uiScale)

    InventoryUI.drawFunctionBar()

    local path = Inventory.getPath(player.inventory.currentDir)
    DosUI.fillRect(0, 1, 100, 1, " ", nil, 0)
    DosUI.putString(1, 1, path, 15, 0, 78)

    -- Title row (row 2)
    DosUI.fillRect(PANEL_COL, TITLE_ROW, PANEL_W, 1, " ", nil, 0)
    local equipLabel = " Equip "
    local equipTx = PANEL_COL + math.floor((EQUIP_INNER_W + 2 - #equipLabel) / 2)
    DosUI.putString(equipTx, TITLE_ROW, equipLabel, focusPanel == "equip" and 15 or 14, 0)
    local filesLabel = " Files "
    local filesTx = DIVIDER1_COL + math.floor((LIST_INNER_W + 1 - #filesLabel) / 2)
    DosUI.putString(filesTx, TITLE_ROW, filesLabel, focusPanel == "files" and 15 or 14, 0)
    local infoLabel = " Info "
    local infoTx = DIVIDER2_COL + math.floor((INFO_INNER_W + 1 - #infoLabel) / 2)
    DosUI.putString(infoTx, TITLE_ROW, infoLabel, 14, 0)

    -- Box
    DosUI.drawBox(PANEL_COL, BOX_TOP, PANEL_W, BOX_H, 14, 0)

    -- Divider 1 (between equip and files)
    DosUI.drawVLine(DIVIDER1_COL, CONTENT_TOP, VISIBLE_ROWS, 14, -1)
    DosUI.putTT(DIVIDER1_COL, BOX_TOP, 14)
    DosUI.putBT(DIVIDER1_COL, BOX_BOT, 14)

    -- Divider 2 (between files and info)
    DosUI.drawVLine(DIVIDER2_COL, CONTENT_TOP, VISIBLE_ROWS, 14, -1)
    DosUI.putTT(DIVIDER2_COL, BOX_TOP, 14)
    DosUI.putBT(DIVIDER2_COL, BOX_BOT, 14)

    InventoryUI.drawEquipPanel()
    InventoryUI.drawFileList()
    InventoryUI.drawInfoPanel()
    InventoryUI.drawStatusBar()
    InventoryUI.drawHelpBar()

    if state == "dialog" then
        InventoryUI.drawDialog()
    elseif state == "action_menu" then
        InventoryUI.drawActionMenu()
    end

    love.graphics.pop()
end

function InventoryUI.drawFunctionBar()
    DosUI.fillRect(0, 0, 100, 1, " ", nil, 8)
    local buttons = {
        {key = "F1", label = "Help"},
        {key = "Ent", label = "Action"},
        {key = "F3", label = "Drop"},
        {key = "F5", label = "Sort"},
        {key = "F6", label = "Move"},
        {key = "F7", label = "MkDir"},
        {key = "F8", label = "Del"},
        {key = "L/R", label = "Panel"},
        {key = "F10", label = "Close"},
    }
    local col = 0
    for _, btn in ipairs(buttons) do
        DosUI.putString(col, 0, btn.key, 15, 8)
        col = col + #btn.key
        DosUI.putString(col, 0, btn.label, 0, 6)
        col = col + #btn.label + 1
    end
end

function InventoryUI.drawEquipPanel()
    -- Clear equip area
    DosUI.fillRect(EQUIP_INNER_COL, CONTENT_TOP, EQUIP_INNER_W, VISIBLE_ROWS, " ", nil, 0)

    local inv = player.inventory
    for i = 1, 8 do
        local row = CONTENT_TOP + (i - 1) * 4
        if row > CONTENT_BOT - 1 then break end

        local slot = EQUIP_SLOTS[i]
        local equipped = Inventory.getEquipped(inv, i)
        local isSelected = false
        local isValidTarget = false

        if state == "equip_select" then
            -- In equip select mode, highlight valid slots
            for _, vs in ipairs(equipValidSlots) do
                if vs == i then isValidTarget = true end
            end
            isSelected = (equipSelectCursor == i)
        elseif focusPanel == "equip" and state == "browsing" then
            isSelected = (equipCursor == i)
        end

        local bg = 0
        if isSelected then bg = 4 end

        -- Slot label
        DosUI.fillRect(EQUIP_INNER_COL, row, EQUIP_INNER_W, 1, " ", nil, bg)
        local labelColor = 8
        if state == "equip_select" then
            labelColor = isValidTarget and 14 or 8
        elseif focusPanel == "equip" then
            labelColor = 14
        end
        DosUI.putString(EQUIP_INNER_COL, row, slot.label, labelColor, bg)

        -- Item name or [Empty]
        DosUI.fillRect(EQUIP_INNER_COL, row + 1, EQUIP_INNER_W, 1, " ", nil, bg)
        if equipped then
            local def = Items.get(equipped.itemId)
            local fg = def and def.color or 7
            local name = equipped.name
            if #name > EQUIP_INNER_W - 1 then name = name:sub(1, EQUIP_INNER_W - 1) end
            DosUI.putString(EQUIP_INNER_COL + 1, row + 1, name, fg, bg)
        else
            local emptyColor = 8
            if state == "equip_select" and not isValidTarget then
                emptyColor = 8
            end
            DosUI.putString(EQUIP_INNER_COL + 1, row + 1, "[Empty]", emptyColor, bg)
        end

        -- Separator line (skip after last slot)
        if i < 8 and row + 2 <= CONTENT_BOT then
            DosUI.fillRect(EQUIP_INNER_COL, row + 2, EQUIP_INNER_W, 1, " ", nil, 0)
            local sep = string.rep("-", EQUIP_INNER_W)
            DosUI.putString(EQUIP_INNER_COL, row + 2, sep, 8, 0)
        end
        -- Extra blank line
        if i < 8 and row + 3 <= CONTENT_BOT then
            DosUI.fillRect(EQUIP_INNER_COL, row + 3, EQUIP_INNER_W, 1, " ", nil, 0)
        end
    end
end

function InventoryUI.drawFileList()
    for i = 1, VISIBLE_ROWS do
        local idx = i + scrollOffset
        local row = CONTENT_TOP + i - 1
        if idx <= #contents then
            local item = contents[idx]
            local isSelected = (focusPanel == "files" and idx == cursor)
            local bg = isSelected and 4 or 0
            local fg = 7

            -- Highlight equip target in action_menu/equip_select
            if state == "equip_select" and equipSelectTarget and item == equipSelectTarget then
                bg = 5  -- magenta
            end

            DosUI.fillRect(LIST_INNER_COL, row, LIST_INNER_W, 1, " ", nil, bg)

            if item.type == "up" then
                fg = 15
                DosUI.putString(LIST_INNER_COL + 1, row, "..", fg, bg)
                DosUI.putString(LIST_INNER_COL + 20, row, "[Parent]", 8, bg)
            elseif item.type == "dir" then
                fg = 15
                DosUI.putString(LIST_INNER_COL + 1, row, item.name, fg, bg)
                DosUI.putString(LIST_INNER_COL + 20, row, "[SubDir]", 11, bg)
            elseif item.type == "file" then
                local def = Items.get(item.itemId)
                fg = def and def.color or 7
                DosUI.putString(LIST_INNER_COL + 1, row, item.name, fg, bg, 18)
                if item.count > 1 then
                    DosUI.putString(LIST_INNER_COL + 21, row, "x" .. item.count, 7, bg)
                end
                local sz = def and (def.size * item.count) or 0
                local szStr = tostring(sz)
                DosUI.putString(LIST_INNER_COL + LIST_INNER_W - 2 - #szStr, row, szStr, 8, bg)
            end
        end
    end
end

function InventoryUI.drawInfoPanel()
    local infoRow = CONTENT_TOP + 1
    DosUI.fillRect(INFO_INNER_COL, CONTENT_TOP, INFO_INNER_W, VISIBLE_ROWS, " ", nil, 0)

    -- Determine which item to show info for
    local item = nil
    if focusPanel == "equip" and state == "browsing" then
        local equipped = Inventory.getEquipped(player.inventory, equipCursor)
        if equipped then
            item = equipped
        end
    elseif cursor >= 1 and cursor <= #contents then
        item = contents[cursor]
    end
    if not item then return end

    if item.type == "up" then
        DosUI.putString(INFO_INNER_COL + 1, infoRow, "Parent directory", 7, 0)
    elseif item.type == "dir" then
        DosUI.putString(INFO_INNER_COL + 1, infoRow, item.name .. "/", 15, 0)
        DosUI.putString(INFO_INNER_COL + 1, infoRow + 2, "Type: Directory", 7, 0)
        local count = 0
        for _ in ipairs(item.children) do count = count + 1 end
        DosUI.putString(INFO_INNER_COL + 1, infoRow + 3, "Items: " .. count, 7, 0)
    elseif item.type == "file" then
        local def = Items.get(item.itemId)
        if def then
            -- Item tile sprite
            local tileset = require("src.tileset")
            local img = tileset.getImage()
            if img then
                local quad = tileset.getQuad(def.gid)
                local ox2, oy2 = DosUI.getOffset()
                local cw2, ch2 = DosUI.getCellSize()
                local px = ox2 + (INFO_INNER_COL + 7) * cw2
                local py = oy2 + infoRow * ch2
                love.graphics.setColor(1, 1, 1, 1)
                love.graphics.draw(img, quad, px, py, 0, 2, 2)
            end

            local maxW = INFO_INNER_W - 2
            DosUI.putString(INFO_INNER_COL + 1, infoRow + 3, item.name, def.color, 0, maxW)
            DosUI.putString(INFO_INNER_COL + 1, infoRow + 5, "Category:", 8, 0)
            DosUI.putString(INFO_INNER_COL + 1, infoRow + 6, " " .. (def.category or "?"), Items.categoryColor(def.category), 0)

            AiDescribe.request(item.itemId)
            local aiResult = AiDescribe.getResult(item.itemId)

            local rarityStr = "Common"
            local rarityColor = 7
            if type(aiResult) == "table" and aiResult.rarity then
                rarityStr = aiResult.rarity
            end
            if rarityStr == "Legendary" then rarityColor = 13
            elseif rarityStr == "Rare" then rarityColor = 12
            elseif rarityStr == "Uncommon" then rarityColor = 10
            else rarityColor = 7 end
            DosUI.putString(INFO_INNER_COL + 1, infoRow + 7, "Rarity: " .. rarityStr, rarityColor, 0)

            DosUI.putString(INFO_INNER_COL + 1, infoRow + 8, "Size: " .. def.size, 7, 0)
            DosUI.putString(INFO_INNER_COL + 1, infoRow + 9, "Count: " .. item.count, 7, 0)

            local sep = string.rep("-", maxW)
            DosUI.putString(INFO_INNER_COL + 1, infoRow + 10, sep, 8, 0)

            local r = infoRow + 11

            if aiResult == "loading" then
                local dots = string.rep(".", math.floor(love.timer.getTime() * 3) % 4)
                DosUI.putString(INFO_INNER_COL + 1, r, "Analyzing" .. dots, 11, 0)
            elseif type(aiResult) == "table" then
                if aiResult.lore then
                    local loreLines = wordWrap('"' .. aiResult.lore .. '"', maxW)
                    for _, line in ipairs(loreLines) do
                        if r >= CONTENT_BOT - 6 then break end
                        DosUI.putString(INFO_INNER_COL + 1, r, line, 14, 0)
                        r = r + 1
                    end
                end
                if aiResult.traits and type(aiResult.traits) == "table" then
                    r = r + 1
                    for _, trait in ipairs(aiResult.traits) do
                        if r >= CONTENT_BOT - 2 then break end
                        local traitLines = wordWrap("* " .. tostring(trait), maxW)
                        for _, line in ipairs(traitLines) do
                            if r >= CONTENT_BOT - 2 then break end
                            DosUI.putString(INFO_INNER_COL + 1, r, line, 10, 0)
                            r = r + 1
                        end
                    end
                end
                if aiResult.effect then
                    r = r + 1
                    if r < CONTENT_BOT then
                        DosUI.putString(INFO_INNER_COL + 1, r, "Effect:", 8, 0)
                        r = r + 1
                        local effLines = wordWrap("  " .. aiResult.effect, maxW)
                        for _, line in ipairs(effLines) do
                            if r >= CONTENT_BOT then break end
                            DosUI.putString(INFO_INNER_COL + 1, r, line, 11, 0)
                            r = r + 1
                        end
                    end
                end
            else
                if def.desc then
                    DosUI.putString(INFO_INNER_COL + 1, r, def.desc, 7, 0, maxW)
                end
            end
        end
    end
end

function InventoryUI.drawStatusBar()
    DosUI.fillRect(0, STATUS_ROW, 100, 1, " ", nil, 0)
    local fileCount, dirCount = 0, 0
    for _, c in ipairs(contents) do
        if c.type == "file" then fileCount = fileCount + 1
        elseif c.type == "dir" then dirCount = dirCount + 1 end
    end
    local totalSize = Inventory.getTotalSize(player.inventory)
    local info = string.format("%d Files  %d Dir    %d/%d Bytes    Sort:%s",
        fileCount, dirCount, totalSize, Inventory.capacity, sortMode:upper())
    DosUI.putString(1, STATUS_ROW, info, 7, 0)

    if #statusMsg > 0 then
        DosUI.putString(55, STATUS_ROW, statusMsg, 11, 0, 24)
    end
end

function InventoryUI.drawHelpBar()
    DosUI.fillRect(0, HELP_ROW, 100, 1, " ", nil, 0)
    if state == "equip_select" then
        DosUI.putString(1, HELP_ROW,
            "Up/Dn:Slot Enter:Equip Esc:Cancel", 8, 0)
    elseif focusPanel == "equip" then
        DosUI.putString(1, HELP_ROW,
            "Up/Dn:Slot Enter:Unequip L/R:Panel Esc:Close", 8, 0)
    else
        DosUI.putString(1, HELP_ROW,
            "Arrows:Nav Enter:Action L/R:Panel F5:Sort Esc:Close", 8, 0)
    end
end

------------------------------------------------------------
-- ACTION MENU
------------------------------------------------------------

function InventoryUI.buildActionMenu(item)
    local def = Items.get(item.itemId)
    local menu = {}
    -- USE
    local hasUse = def and def.onUse
    menu[#menu+1] = {label = "USE", enabled = hasUse, action = "use"}
    -- EQUIP
    local canEquip = Items.isEquippable(item.itemId)
    menu[#menu+1] = {label = "EQUIP", enabled = canEquip, action = "equip"}
    -- RECYCLE (always disabled)
    menu[#menu+1] = {label = "RECYCLE", enabled = false, action = "recycle"}
    -- DELETE (drop)
    menu[#menu+1] = {label = "DELETE", enabled = true, action = "delete"}
    return menu
end

function InventoryUI.drawActionMenu()
    local w = 20
    local h = #actionMenuItems + 4
    local col = math.floor((100 - w) / 2)
    local row = math.floor((40 - h) / 2)
    DosUI.drawBox(col, row, w, h, 15, 4)

    -- Item name header
    local itemName = actionMenuTarget and actionMenuTarget.name or "?"
    DosUI.putString(col + 2, row + 1, itemName, 15, 4, w - 4)

    -- Separator
    local sepStr = string.rep("\xe2\x94\x80", w - 2)
    DosUI.putString(col + 1, row + 2, sepStr, 15, 4, w - 2)

    for i, mi in ipairs(actionMenuItems) do
        local isSelected = (i == actionMenuCursor)
        local bg = isSelected and 12 or 4
        local fg = mi.enabled and 15 or 8
        DosUI.fillRect(col + 1, row + 2 + i, w - 2, 1, " ", nil, bg)
        local prefix = isSelected and "> " or "  "
        DosUI.putString(col + 2, row + 2 + i, prefix .. mi.label, fg, bg)
    end
end

------------------------------------------------------------
-- DIALOGS
------------------------------------------------------------

function InventoryUI.drawDialog()
    if dialogType == "mkdir" then
        InventoryUI.drawMkdirDialog()
    elseif dialogType == "delete" then
        InventoryUI.drawConfirmDialog("Delete " .. (dialogTarget and dialogTarget.name or "?") .. "? [Y/N]")
    elseif dialogType == "drop" then
        local item = contents[cursor]
        local label = item and item.name or "?"
        local cnt = item and item.count or 1
        InventoryUI.drawConfirmDialog("Drop " .. label .. " x" .. cnt .. "? [Y/N]")
    elseif dialogType == "help" then
        InventoryUI.drawHelpDialog()
    elseif dialogType == "move" then
        InventoryUI.drawMoveDialog()
    end
end

function InventoryUI.drawMkdirDialog()
    local w, h = 40, 6
    local col = math.floor((100 - w) / 2)
    local row = math.floor((40 - h) / 2)
    DosUI.drawBox(col, row, w, h, 15, 4)
    DosUI.putString(col + 2, row + 1, "New Folder", 15, 4)
    DosUI.putString(col + 2, row + 2, "Name (max 8 chars):", 7, 4)
    DosUI.fillRect(col + 2, row + 3, w - 4, 1, " ", nil, 0)
    DosUI.putString(col + 2, row + 3, dialogInput .. "_", 15, 0)
    DosUI.putString(col + 2, row + 4, "Enter=OK  Esc=Cancel", 8, 4)
end

function InventoryUI.drawConfirmDialog(msg)
    local w = math.max(#msg + 6, 30)
    local h = 4
    local col = math.floor((100 - w) / 2)
    local row = math.floor((40 - h) / 2)
    DosUI.drawBox(col, row, w, h, 15, 4)
    DosUI.putString(col + 2, row + 1, "Confirm", 15, 4)
    DosUI.putString(col + 2, row + 2, msg, 15, 4)
end

function InventoryUI.drawHelpDialog()
    local w, h = 50, 22
    local col = math.floor((100 - w) / 2)
    local row = math.floor((40 - h) / 2)
    DosUI.drawBox(col, row, w, h, 15, 4)
    DosUI.putString(col + 2, row + 1, "Help - Key Bindings", 15, 4)
    local lines = {
        "",
        "Up/Down     Navigate list / slots",
        "Left/Right  Switch panel (Equip/Files)",
        "Enter       Action menu (file) / Unequip",
        "Backspace   Go to parent folder",
        "Home/End    Jump to first/last",
        "PgUp/PgDn   Page up/down",
        "",
        "F1          This help screen",
        "F3          Drop item to map",
        "F5          Cycle sort mode",
        "F6          Move item to folder",
        "F7          Create new folder",
        "F8          Delete empty folder",
        "F10 / Esc   Close inventory",
        "Tab / I     Toggle inventory",
        "",
        "In Action Menu: USE/EQUIP/DELETE",
        "",
        "Press any key to close...",
    }
    for i, line in ipairs(lines) do
        if row + 1 + i < row + h - 1 then
            DosUI.putString(col + 2, row + 1 + i, line, 15, 4, w - 4)
        end
    end
end

function InventoryUI.drawMoveDialog()
    local w, h = 40, math.min(#moveDirs + 5, 25)
    local col = math.floor((100 - w) / 2)
    local row = math.floor((40 - h) / 2)
    DosUI.drawBox(col, row, w, h, 15, 4)
    DosUI.putString(col + 2, row + 1, "Move to folder", 15, 4)
    for i, entry in ipairs(moveDirs) do
        if i + 1 < h - 2 then
            local isSelected = (i == moveCursor)
            local bg = isSelected and 12 or 4
            local indent = string.rep("  ", entry.depth)
            local label = indent .. entry.dir.name .. "/"
            DosUI.fillRect(col + 1, row + 1 + i, w - 2, 1, " ", nil, bg)
            DosUI.putString(col + 2, row + 1 + i, label, 15, bg, w - 4)
        end
    end
    DosUI.putString(col + 2, row + h - 2, "Enter=Move  Esc=Cancel", 8, 4)
end

------------------------------------------------------------
-- INPUT
------------------------------------------------------------

function InventoryUI.keypressed(key)
    if state == "dialog" then
        InventoryUI.dialogKeypressed(key)
        return
    end

    if state == "action_menu" then
        InventoryUI.actionMenuKeypressed(key)
        return
    end

    if state == "equip_select" then
        InventoryUI.equipSelectKeypressed(key)
        return
    end

    -- Browsing state
    if focusPanel == "equip" then
        InventoryUI.equipPanelKeypressed(key)
    else
        InventoryUI.filesPanelKeypressed(key)
    end
end

function InventoryUI.filesPanelKeypressed(key)
    if key == "up" then
        cursor = cursor - 1
        if cursor < 1 then cursor = math.max(1, #contents) end
        InventoryUI.ensureVisible()
    elseif key == "down" then
        cursor = cursor + 1
        if cursor > #contents then cursor = 1 end
        InventoryUI.ensureVisible()
    elseif key == "home" then
        cursor = 1
        scrollOffset = 0
    elseif key == "end" then
        cursor = #contents
        InventoryUI.ensureVisible()
    elseif key == "pageup" then
        cursor = math.max(1, cursor - VISIBLE_ROWS)
        InventoryUI.ensureVisible()
    elseif key == "pagedown" then
        cursor = math.min(#contents, cursor + VISIBLE_ROWS)
        InventoryUI.ensureVisible()
    elseif key == "return" then
        InventoryUI.activateItem()
    elseif key == "backspace" then
        InventoryUI.goUp()
    elseif key == "left" or key == "right" then
        focusPanel = "equip"
        equipCursor = 1
    elseif key == "escape" or key == "f10" then
        InventoryUI.close()
    elseif key == "tab" or key == "i" then
        InventoryUI.close()
    elseif key == "f1" then
        state = "dialog"
        dialogType = "help"
    elseif key == "f3" then
        InventoryUI.promptDrop()
    elseif key == "f5" then
        InventoryUI.cycleSort()
    elseif key == "f6" then
        InventoryUI.promptMove()
    elseif key == "f7" then
        state = "dialog"
        dialogType = "mkdir"
        dialogInput = ""
    elseif key == "f8" then
        InventoryUI.promptDelete()
    end
end

function InventoryUI.equipPanelKeypressed(key)
    if key == "up" then
        equipCursor = equipCursor - 1
        if equipCursor < 1 then equipCursor = 8 end
    elseif key == "down" then
        equipCursor = equipCursor + 1
        if equipCursor > 8 then equipCursor = 1 end
    elseif key == "left" or key == "right" then
        focusPanel = "files"
    elseif key == "return" then
        -- Unequip from selected slot
        local equipped = Inventory.getEquipped(player.inventory, equipCursor)
        if equipped then
            local ok, err = Inventory.unequip(player.inventory, equipCursor)
            if ok then
                InventoryUI.setStatus("Unequipped " .. equipped.name)
            else
                InventoryUI.setStatus(err or "Error")
            end
            InventoryUI.refreshContents()
        end
    elseif key == "escape" or key == "f10" then
        InventoryUI.close()
    elseif key == "tab" or key == "i" then
        InventoryUI.close()
    elseif key == "f1" then
        state = "dialog"
        dialogType = "help"
    end
end

function InventoryUI.actionMenuKeypressed(key)
    if key == "up" then
        -- Move cursor up, skipping disabled items
        local start = actionMenuCursor
        repeat
            actionMenuCursor = actionMenuCursor - 1
            if actionMenuCursor < 1 then actionMenuCursor = #actionMenuItems end
        until actionMenuItems[actionMenuCursor].enabled or actionMenuCursor == start
    elseif key == "down" then
        local start = actionMenuCursor
        repeat
            actionMenuCursor = actionMenuCursor + 1
            if actionMenuCursor > #actionMenuItems then actionMenuCursor = 1 end
        until actionMenuItems[actionMenuCursor].enabled or actionMenuCursor == start
    elseif key == "return" then
        local mi = actionMenuItems[actionMenuCursor]
        if mi and mi.enabled then
            if mi.action == "use" then
                state = "browsing"
                InventoryUI.useSelected()
            elseif mi.action == "equip" then
                -- Enter equip select mode
                equipValidSlots = Items.getValidSlots(actionMenuTarget.itemId)
                equipSelectTarget = actionMenuTarget
                if #equipValidSlots > 0 then
                    equipSelectCursor = equipValidSlots[1]
                    state = "equip_select"
                else
                    state = "browsing"
                    InventoryUI.setStatus("Cannot equip")
                end
            elseif mi.action == "delete" then
                state = "dialog"
                dialogType = "drop"
            end
        end
    elseif key == "escape" then
        state = "browsing"
    end
end

function InventoryUI.equipSelectKeypressed(key)
    if key == "up" then
        -- Find prev valid slot
        local idx = 0
        for i, vs in ipairs(equipValidSlots) do
            if vs == equipSelectCursor then idx = i; break end
        end
        idx = idx - 1
        if idx < 1 then idx = #equipValidSlots end
        equipSelectCursor = equipValidSlots[idx]
    elseif key == "down" then
        local idx = 0
        for i, vs in ipairs(equipValidSlots) do
            if vs == equipSelectCursor then idx = i; break end
        end
        idx = idx + 1
        if idx > #equipValidSlots then idx = 1 end
        equipSelectCursor = equipValidSlots[idx]
    elseif key == "return" then
        -- Equip the item to selected slot
        local ok = Inventory.equip(player.inventory, equipSelectTarget, equipSelectCursor)
        if ok then
            InventoryUI.setStatus("Equipped to " .. EQUIP_SLOTS[equipSelectCursor].name)
        else
            InventoryUI.setStatus("Cannot equip")
        end
        state = "browsing"
        focusPanel = "files"
        InventoryUI.refreshContents()
    elseif key == "escape" then
        state = "browsing"
        focusPanel = "files"
    end
end

function InventoryUI.dialogKeypressed(key)
    if dialogType == "help" then
        state = "browsing"
        dialogType = nil
        return
    end

    if dialogType == "mkdir" then
        if key == "return" then
            if #dialogInput > 0 then
                local ok, err = Inventory.createFolder(player.inventory, dialogInput)
                if ok then
                    InventoryUI.setStatus("Folder created")
                else
                    InventoryUI.setStatus(err or "Error")
                end
                InventoryUI.refreshContents()
            end
            state = "browsing"
            dialogType = nil
        elseif key == "escape" then
            state = "browsing"
            dialogType = nil
        elseif key == "backspace" then
            dialogInput = dialogInput:sub(1, -2)
        end
        return
    end

    if dialogType == "delete" then
        if key == "y" then
            if dialogTarget then
                local ok, err = Inventory.deleteFolder(player.inventory, dialogTarget)
                if ok then
                    InventoryUI.setStatus("Folder deleted")
                else
                    InventoryUI.setStatus(err or "Error")
                end
                InventoryUI.refreshContents()
            end
            state = "browsing"
            dialogType = nil
        elseif key == "n" or key == "escape" then
            state = "browsing"
            dialogType = nil
        end
        return
    end

    if dialogType == "drop" then
        if key == "y" then
            InventoryUI.doDrop()
            state = "browsing"
            dialogType = nil
        elseif key == "n" or key == "escape" then
            state = "browsing"
            dialogType = nil
        end
        return
    end

    if dialogType == "move" then
        if key == "up" then
            moveCursor = moveCursor - 1
            if moveCursor < 1 then moveCursor = #moveDirs end
        elseif key == "down" then
            moveCursor = moveCursor + 1
            if moveCursor > #moveDirs then moveCursor = 1 end
        elseif key == "return" then
            InventoryUI.doMove()
            state = "browsing"
            dialogType = nil
        elseif key == "escape" then
            state = "browsing"
            dialogType = nil
        end
        return
    end
end

function InventoryUI.textinput(text)
    if state == "dialog" and dialogType == "mkdir" then
        if text:match("^[A-Za-z0-9_]$") and #dialogInput < 8 then
            dialogInput = dialogInput .. text:upper()
        end
    end
end

------------------------------------------------------------
-- ACTIONS
------------------------------------------------------------

function InventoryUI.ensureVisible()
    if cursor <= scrollOffset then
        scrollOffset = cursor - 1
    elseif cursor > scrollOffset + VISIBLE_ROWS then
        scrollOffset = cursor - VISIBLE_ROWS
    end
    if scrollOffset < 0 then scrollOffset = 0 end
end

function InventoryUI.activateItem()
    if cursor < 1 or cursor > #contents then return end
    local item = contents[cursor]
    if item.type == "up" then
        InventoryUI.goUp()
    elseif item.type == "dir" then
        player.inventory.currentDir = item
        cursor = 1
        scrollOffset = 0
        InventoryUI.refreshContents()
    elseif item.type == "file" then
        -- Open action menu
        actionMenuTarget = item
        actionMenuItems = InventoryUI.buildActionMenu(item)
        actionMenuCursor = 1
        -- Skip to first enabled item
        for i, mi in ipairs(actionMenuItems) do
            if mi.enabled then
                actionMenuCursor = i
                break
            end
        end
        state = "action_menu"
    end
end

function InventoryUI.goUp()
    local cur = player.inventory.currentDir
    if cur.parent then
        player.inventory.currentDir = cur.parent
        cursor = 1
        scrollOffset = 0
        InventoryUI.refreshContents()
    end
end

function InventoryUI.useSelected()
    if cursor < 1 or cursor > #contents then return end
    local item = contents[cursor]
    if item.type ~= "file" then return end
    local ok, msg = Inventory.useItem(player.inventory, item, player)
    if ok then
        InventoryUI.setStatus(msg or "Item used")
    else
        InventoryUI.setStatus(msg or "Cannot use")
    end
    InventoryUI.refreshContents()
end

function InventoryUI.promptDrop()
    if cursor < 1 or cursor > #contents then return end
    local item = contents[cursor]
    if item.type ~= "file" then return end
    state = "dialog"
    dialogType = "drop"
end

function InventoryUI.doDrop()
    if cursor < 1 or cursor > #contents then return end
    local item = contents[cursor]
    if item.type ~= "file" then return end

    local def = Items.get(item.itemId)
    if def and entities then
        entities.items[#entities.items + 1] = {
            x = player.x, y = player.y,
            collected = false,
            gid = def.gid,
            itemId = item.itemId,
        }
    end
    Inventory.removeItem(player.inventory, item, item.count)
    InventoryUI.setStatus("Dropped " .. item.name)
    InventoryUI.refreshContents()
end

function InventoryUI.cycleSort()
    sortIndex = sortIndex % #sortModes + 1
    sortMode = sortModes[sortIndex]
    Inventory.sortContents(player.inventory.currentDir, sortMode)
    InventoryUI.refreshContents()
    InventoryUI.setStatus("Sort: " .. sortMode:upper())
end

function InventoryUI.promptDelete()
    if cursor < 1 or cursor > #contents then return end
    local item = contents[cursor]
    if item.type ~= "dir" then
        InventoryUI.setStatus("Not a folder")
        return
    end
    state = "dialog"
    dialogType = "delete"
    dialogTarget = item
end

function InventoryUI.promptMove()
    if cursor < 1 or cursor > #contents then return end
    local item = contents[cursor]
    if item.type ~= "file" then
        InventoryUI.setStatus("Select a file")
        return
    end
    moveDirs = Inventory.getAllDirs(player.inventory.root)
    moveCursor = 1
    state = "dialog"
    dialogType = "move"
    dialogTarget = item
end

function InventoryUI.doMove()
    if not dialogTarget or moveCursor < 1 or moveCursor > #moveDirs then return end
    local target = moveDirs[moveCursor].dir
    local ok, err = Inventory.moveItem(player.inventory, dialogTarget, target)
    if ok then
        InventoryUI.setStatus("Moved to " .. target.name)
    else
        InventoryUI.setStatus(err or "Error")
    end
    InventoryUI.refreshContents()
end

return InventoryUI
