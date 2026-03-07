local DosUI = require("src.dos_ui")
local Items = require("src.items")
local Inventory = require("src.inventory")
local Config = require("src.config")
local AiDescribe = require("src.ai_describe")

local InventoryUI = {}

local state = "closed"  -- closed, browsing, dialog
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

-- Dialog state
local dialogType = nil   -- "mkdir", "delete", "drop", "help", "move"
local dialogInput = ""
local dialogTarget = nil -- for move dialog
local moveDirs = {}
local moveCursor = 1

-- Layout constants (MDIR style: title row separate from box)
-- Row 0:  F-key bar
-- Row 1:  Path bar (C:\BACKPACK\...)
-- Row 2:  Title row "Files" / "Info"
-- Row 3:  ┌──────────────────────┬────────────┐  box top
-- Row 4..36: │ content             │ info       │  box content
-- Row 37: └──────────────────────┴────────────┘  box bottom
-- Row 38: Status bar
-- Row 39: Help bar

local PANEL_COL = 1       -- left edge of entire panel area
local PANEL_W = 78        -- full width
local TITLE_ROW = 2       -- title labels row
local BOX_TOP = 3         -- box top border row
local BOX_H = 35          -- box height (rows 3..37)
local BOX_BOT = BOX_TOP + BOX_H - 1  -- row 37

local LIST_INNER_COL = PANEL_COL + 1  -- first content col inside box
local LIST_INNER_W = 53               -- width of file list area inside box
local DIVIDER_COL = PANEL_COL + LIST_INNER_W + 1  -- │ divider column
local INFO_INNER_COL = DIVIDER_COL + 1  -- first col of info area
local INFO_INNER_W = PANEL_W - LIST_INNER_W - 3  -- info area width

local CONTENT_TOP = BOX_TOP + 1       -- first content row
local CONTENT_BOT = BOX_BOT - 1       -- last content row
local VISIBLE_ROWS = CONTENT_BOT - CONTENT_TOP + 1

local STATUS_ROW = BOX_BOT + 1  -- row 38
local HELP_ROW = STATUS_ROW + 1 -- row 39

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
    -- Add ".." entry if not at root
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
    -- Full screen dark background (before scale so it covers everything)
    love.graphics.setColor(0, 0, 0, 0.95)
    love.graphics.rectangle("fill", 0, 0, love.graphics.getWidth(), love.graphics.getHeight())

    -- Scale UI to fill screen height, center horizontally
    local cw, ch = DosUI.getCellSize()
    local uiScale = love.graphics.getHeight() / (DosUI.ROWS * ch)
    local uiW = DosUI.COLS * cw * uiScale
    local ox, oy = DosUI.getOffset()
    love.graphics.push()
    love.graphics.translate((love.graphics.getWidth() - uiW) / 2 - ox * uiScale, -oy * uiScale)
    love.graphics.scale(uiScale, uiScale)

    -- Function key bar (row 0)
    InventoryUI.drawFunctionBar()

    -- Path bar (row 1)
    local path = Inventory.getPath(player.inventory.currentDir)
    DosUI.fillRect(0, 1, 80, 1, " ", nil, 0)
    DosUI.putString(1, 1, path, 15, 0, 78)

    -- Title row (row 2) - separate from box, like MDIR
    DosUI.fillRect(PANEL_COL, TITLE_ROW, PANEL_W, 1, " ", nil, 0)
    -- "Files" label centered over file list area
    local filesLabel = " Files "
    local filesTx = PANEL_COL + math.floor((LIST_INNER_W + 2 - #filesLabel) / 2)
    DosUI.putString(filesTx, TITLE_ROW, filesLabel, 14, 0)
    -- "Info" label centered over info area
    local infoLabel = " Info "
    local infoTx = DIVIDER_COL + math.floor((INFO_INNER_W + 1 - #infoLabel) / 2)
    DosUI.putString(infoTx, TITLE_ROW, infoLabel, 14, 0)

    -- Box (single border around everything)
    DosUI.drawBox(PANEL_COL, BOX_TOP, PANEL_W, BOX_H, 14, 0)

    -- Vertical divider between file list and info
    DosUI.drawVLine(DIVIDER_COL, CONTENT_TOP, VISIBLE_ROWS, 14, -1)
    -- T-junctions where divider meets top/bottom border
    DosUI.putTT(DIVIDER_COL, BOX_TOP, 14)
    DosUI.putBT(DIVIDER_COL, BOX_BOT, 14)

    -- Draw file list content
    InventoryUI.drawFileList()

    -- Draw info panel content
    InventoryUI.drawInfoPanel()

    -- Status bar
    InventoryUI.drawStatusBar()

    -- Help bar
    InventoryUI.drawHelpBar()

    -- Dialog overlay
    if state == "dialog" then
        InventoryUI.drawDialog()
    end

    love.graphics.pop()
end

function InventoryUI.drawFunctionBar()
    DosUI.fillRect(0, 0, 80, 1, " ", nil, 8)
    local buttons = {
        {key = "F1", label = "Help"},
        {key = "F2", label = "Use"},
        {key = "F3", label = "Drop"},
        {key = "F5", label = "Sort"},
        {key = "F6", label = "Move"},
        {key = "F7", label = "MkDir"},
        {key = "F8", label = "Del"},
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

function InventoryUI.drawFileList()
    for i = 1, VISIBLE_ROWS do
        local idx = i + scrollOffset
        local row = CONTENT_TOP + i - 1
        if idx <= #contents then
            local item = contents[idx]
            local isSelected = (idx == cursor)
            local bg = isSelected and 4 or 0
            local fg = 7

            -- Clear row (file list area only)
            DosUI.fillRect(LIST_INNER_COL, row, LIST_INNER_W, 1, " ", nil, bg)

            if item.type == "up" then
                fg = 15
                DosUI.putString(LIST_INNER_COL + 1, row, "..", fg, bg)
                DosUI.putString(LIST_INNER_COL + 28, row, "[Parent]", 8, bg)
            elseif item.type == "dir" then
                fg = 15
                DosUI.putString(LIST_INNER_COL + 1, row, item.name, fg, bg)
                DosUI.putString(LIST_INNER_COL + 28, row, "[SubDir]", 11, bg)
            elseif item.type == "file" then
                local def = Items.get(item.itemId)
                fg = def and def.color or 7
                DosUI.putString(LIST_INNER_COL + 1, row, item.name, fg, bg, 20)
                if item.count > 1 then
                    DosUI.putString(LIST_INNER_COL + 23, row, "x" .. item.count, 7, bg)
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
    -- Clear info area
    DosUI.fillRect(INFO_INNER_COL, CONTENT_TOP, INFO_INNER_W, VISIBLE_ROWS, " ", nil, 0)

    if cursor < 1 or cursor > #contents then return end
    local item = contents[cursor]

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
                local ox, oy = DosUI.getOffset()
                local cw, ch = DosUI.getCellSize()
                local px = ox + (INFO_INNER_COL + 7) * cw
                local py = oy + infoRow * ch
                love.graphics.setColor(1, 1, 1, 1)
                love.graphics.draw(img, quad, px, py, 0, 2, 2)
            end

            local maxW = INFO_INNER_W - 2
            DosUI.putString(INFO_INNER_COL + 1, infoRow + 3, item.name, def.color, 0, maxW)
            DosUI.putString(INFO_INNER_COL + 1, infoRow + 5, "Category:", 8, 0)
            DosUI.putString(INFO_INNER_COL + 1, infoRow + 6, " " .. (def.category or "?"), Items.categoryColor(def.category), 0)

            -- Request AI description
            AiDescribe.request(item.itemId)
            local aiResult = AiDescribe.getResult(item.itemId)

            -- Rarity line (from AI or default)
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

            -- Separator
            local sep = string.rep("-", maxW)
            DosUI.putString(INFO_INNER_COL + 1, infoRow + 10, sep, 8, 0)

            local r = infoRow + 11

            if aiResult == "loading" then
                -- Blinking "Analyzing..." animation
                local dots = string.rep(".", math.floor(love.timer.getTime() * 3) % 4)
                DosUI.putString(INFO_INNER_COL + 1, r, "Analyzing" .. dots, 11, 0)
            elseif type(aiResult) == "table" then
                -- AI Lore
                if aiResult.lore then
                    local lore = '"' .. aiResult.lore .. '"'
                    while #lore > 0 and r < CONTENT_BOT - 6 do
                        local line = lore:sub(1, maxW)
                        lore = lore:sub(maxW + 1)
                        DosUI.putString(INFO_INNER_COL + 1, r, line, 14, 0)
                        r = r + 1
                    end
                end

                -- AI Traits
                if aiResult.traits and type(aiResult.traits) == "table" then
                    r = r + 1
                    for _, trait in ipairs(aiResult.traits) do
                        if r >= CONTENT_BOT - 2 then break end
                        DosUI.putString(INFO_INNER_COL + 1, r, "* " .. tostring(trait), 10, 0, maxW)
                        r = r + 1
                    end
                end

                -- AI Effect
                if aiResult.effect then
                    r = r + 1
                    if r < CONTENT_BOT then
                        DosUI.putString(INFO_INNER_COL + 1, r, "Effect:", 8, 0)
                        r = r + 1
                        local eff = " " .. aiResult.effect
                        while #eff > 0 and r < CONTENT_BOT do
                            local line = eff:sub(1, maxW)
                            eff = eff:sub(maxW + 1)
                            DosUI.putString(INFO_INNER_COL + 1, r, line, 11, 0)
                            r = r + 1
                        end
                    end
                end
            else
                -- No AI result yet, show basic description
                if def.desc then
                    DosUI.putString(INFO_INNER_COL + 1, r, def.desc, 7, 0, maxW)
                end
            end
        end
    end
end

function InventoryUI.drawStatusBar()
    DosUI.fillRect(0, STATUS_ROW, 80, 1, " ", nil, 0)
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
    DosUI.fillRect(0, HELP_ROW, 80, 1, " ", nil, 0)
    DosUI.putString(1, HELP_ROW,
        "Arrows:Navigate Enter:Open F2:Use F3:Drop F7:MkDir Esc:Close", 8, 0)
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
    local col = math.floor((80 - w) / 2)
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
    local col = math.floor((80 - w) / 2)
    local row = math.floor((40 - h) / 2)
    DosUI.drawBox(col, row, w, h, 15, 4)
    DosUI.putString(col + 2, row + 1, "Confirm", 15, 4)
    DosUI.putString(col + 2, row + 2, msg, 15, 4)
end

function InventoryUI.drawHelpDialog()
    local w, h = 50, 20
    local col = math.floor((80 - w) / 2)
    local row = math.floor((40 - h) / 2)
    DosUI.drawBox(col, row, w, h, 15, 4)
    DosUI.putString(col + 2, row + 1, "Help - Key Bindings", 15, 4)
    local lines = {
        "",
        "Up/Down     Navigate file list",
        "Enter       Open folder / Use item",
        "Backspace   Go to parent folder",
        "Home/End    Jump to first/last",
        "PgUp/PgDn   Page up/down",
        "",
        "F1          This help screen",
        "F2          Use selected item",
        "F3          Drop item to map",
        "F5          Cycle sort mode",
        "F6          Move item to folder",
        "F7          Create new folder",
        "F8          Delete empty folder",
        "F10 / Esc   Close inventory",
        "Tab / I     Toggle inventory",
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
    local col = math.floor((80 - w) / 2)
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

    -- Browsing state
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
    elseif key == "escape" or key == "f10" then
        InventoryUI.close()
    elseif key == "tab" or key == "i" then
        InventoryUI.close()
    elseif key == "f1" then
        state = "dialog"
        dialogType = "help"
    elseif key == "f2" then
        InventoryUI.useSelected()
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
        InventoryUI.useSelected()
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
