local DosUI = require("src.dos_ui")
local Items = require("src.items")
local Inventory = require("src.inventory")

local LootboxUI = {}

local state = "closed"  -- closed, browsing, dialog
local lootbox = nil
local player = nil
local cursor = 1
local scrollOffset = 0
local statusMsg = ""
local statusTimer = 0

-- Layout (80x40 grid, 2-column)
local PANEL_COL = 1
local PANEL_W = 98
local TITLE_ROW = 0
local BOX_TOP = 1
local BOX_H = 37       -- rows 1..37
local BOX_BOT = BOX_TOP + BOX_H - 1

local LEFT_W = 48       -- inner width of left (container) column
local DIVIDER_COL = PANEL_COL + LEFT_W + 1
local RIGHT_W = PANEL_W - LEFT_W - 3  -- inner width of right (inventory) column

local CONTENT_TOP = BOX_TOP + 1
local CONTENT_BOT = BOX_BOT - 1
local VISIBLE_ROWS = CONTENT_BOT - CONTENT_TOP + 1

local STATUS_ROW = 38
local HELP_ROW = 39

function LootboxUI.isOpen()
    return state ~= "closed"
end

function LootboxUI.open(lb, p)
    lootbox = lb
    player = p
    state = "browsing"
    cursor = 1
    scrollOffset = 0
    statusMsg = ""
    statusTimer = 0
end

function LootboxUI.close()
    state = "closed"
    lootbox = nil
end

function LootboxUI.update(dt)
    if statusTimer > 0 then
        statusTimer = statusTimer - dt
        if statusTimer <= 0 then statusMsg = "" end
    end
end

------------------------------------------------------------
-- DRAWING
------------------------------------------------------------

function LootboxUI.draw()
    -- Full screen dark background
    love.graphics.setColor(0, 0, 0, 0.95)
    love.graphics.rectangle("fill", 0, 0, love.graphics.getWidth(), love.graphics.getHeight())

    -- Scale UI to fill screen height
    local cw, ch = DosUI.getCellSize()
    local uiScale = love.graphics.getHeight() / (DosUI.ROWS * ch)
    local uiW = DosUI.COLS * cw * uiScale
    local ox, oy = DosUI.getOffset()
    love.graphics.push()
    love.graphics.translate((love.graphics.getWidth() - uiW) / 2 - ox * uiScale, -oy * uiScale)
    love.graphics.scale(uiScale, uiScale)

    -- Title row
    DosUI.fillRect(0, TITLE_ROW, 100, 1, " ", nil, 0)
    local title = "<<< CONTAINER >>>"
    local tx = math.floor((100 - #title) / 2)
    DosUI.putString(tx, TITLE_ROW, title, 15, 0)

    -- Main box
    DosUI.drawBox(PANEL_COL, BOX_TOP, PANEL_W, BOX_H, 14, 0)

    -- Vertical divider
    DosUI.drawVLine(DIVIDER_COL, CONTENT_TOP, VISIBLE_ROWS, 14, -1)
    DosUI.putTT(DIVIDER_COL, BOX_TOP, 14)
    DosUI.putBT(DIVIDER_COL, BOX_BOT, 14)

    -- Column headers (inside box, first content row)
    DosUI.fillRect(PANEL_COL + 1, CONTENT_TOP, LEFT_W, 1, " ", nil, 0)
    DosUI.putString(PANEL_COL + 2, CONTENT_TOP, "CONTAINER", 15, 0)
    DosUI.fillRect(DIVIDER_COL + 1, CONTENT_TOP, RIGHT_W, 1, " ", nil, 0)
    DosUI.putString(DIVIDER_COL + 2, CONTENT_TOP, "INVENTORY", 15, 0)

    -- Header separator lines
    local sepRow = CONTENT_TOP + 1
    DosUI.putChar(PANEL_COL, sepRow, DosUI.BOX.LT, 14, -1)        -- ├
    for c = 1, LEFT_W do
        DosUI.putChar(PANEL_COL + c, sepRow, DosUI.BOX.H, 14, -1) -- ─
    end
    DosUI.putChar(DIVIDER_COL, sepRow, DosUI.BOX.CR, 14, -1)      -- ┼
    for c = 1, RIGHT_W do
        DosUI.putChar(DIVIDER_COL + c, sepRow, DosUI.BOX.H, 14, -1)
    end
    DosUI.putChar(PANEL_COL + PANEL_W - 1, sepRow, DosUI.BOX.RT, 14, -1) -- ┤

    -- Draw container items (left column)
    LootboxUI.drawContainerList()

    -- Draw inventory summary (right column)
    LootboxUI.drawInventorySummary()

    -- Status bar
    DosUI.fillRect(0, STATUS_ROW, 100, 1, " ", nil, 0)
    if #statusMsg > 0 then
        DosUI.putString(1, STATUS_ROW, statusMsg, 11, 0, 78)
    else
        local count = lootbox and #lootbox.items or 0
        DosUI.putString(1, STATUS_ROW, count .. " items in container", 7, 0)
    end

    -- Help bar
    DosUI.fillRect(0, HELP_ROW, 100, 1, " ", nil, 0)
    DosUI.putString(1, HELP_ROW, "Up/Down:Select  Enter:Take  Q/Esc:Close", 8, 0)

    -- Dialog overlay
    if state == "dialog" then
        LootboxUI.drawTakeDialog()
    end

    love.graphics.pop()
end

function LootboxUI.drawContainerList()
    if not lootbox then return end
    local startRow = CONTENT_TOP + 2  -- skip header + separator
    local maxRows = CONTENT_BOT - startRow
    for i = 1, maxRows do
        local idx = i + scrollOffset
        local row = startRow + i - 1
        DosUI.fillRect(PANEL_COL + 1, row, LEFT_W, 1, " ", nil, 0)
        if idx <= #lootbox.items then
            local itemId = lootbox.items[idx]
            local def = Items.get(itemId)
            local isSelected = (idx == cursor)
            local bg = isSelected and 4 or 0
            local fg = def and def.color or 7
            DosUI.fillRect(PANEL_COL + 1, row, LEFT_W, 1, " ", nil, bg)
            local name = def and (def.name .. "." .. def.ext) or "UNKNOWN"
            DosUI.putString(PANEL_COL + 2, row, name, fg, bg, LEFT_W - 2)
            if def then
                local cat = def.category or "?"
                DosUI.putString(PANEL_COL + LEFT_W - #cat - 1, row, cat, 8, bg)
            end
        end
    end
end

function LootboxUI.drawInventorySummary()
    if not player or not player.inventory then return end
    local startRow = CONTENT_TOP + 2  -- skip header + separator
    local col = DIVIDER_COL + 1

    -- Show current inventory contents (flat list of all items)
    local allItems = {}
    local function walk(dir)
        for _, child in ipairs(dir.children) do
            if child.type == "file" then
                allItems[#allItems + 1] = child
            elseif child.type == "dir" then
                walk(child)
            end
        end
    end
    walk(player.inventory.root)

    local totalSize = Inventory.getTotalSize(player.inventory)
    DosUI.fillRect(col, startRow, RIGHT_W, 1, " ", nil, 0)
    local capStr = string.format("Capacity: %d/%d", totalSize, Inventory.capacity)
    DosUI.putString(col + 1, startRow, capStr, 7, 0)

    local maxRows = CONTENT_BOT - startRow - 1
    for i = 1, maxRows do
        local row = startRow + 1 + i - 1
        DosUI.fillRect(col, row, RIGHT_W, 1, " ", nil, 0)
        if i <= #allItems then
            local item = allItems[i]
            local def = Items.get(item.itemId)
            local fg = def and def.color or 7
            local label = item.name
            if item.count > 1 then
                label = label .. " x" .. item.count
            end
            DosUI.putString(col + 1, row, label, fg, 0, RIGHT_W - 2)
        end
    end
end

function LootboxUI.drawTakeDialog()
    if not lootbox or cursor < 1 or cursor > #lootbox.items then return end
    local itemId = lootbox.items[cursor]
    local def = Items.get(itemId)
    local name = def and (def.name .. "." .. def.ext) or "UNKNOWN"
    local msg = "Take " .. name .. "? [Enter/N]"
    local w = math.max(#msg + 6, 30)
    local h = 4
    local col = math.floor((100 - w) / 2)
    local row = math.floor((40 - h) / 2)
    DosUI.drawBox(col, row, w, h, 15, 4)
    DosUI.putString(col + 2, row + 1, "Confirm", 15, 4)
    DosUI.putString(col + 2, row + 2, msg, 15, 4)
end

------------------------------------------------------------
-- INPUT
------------------------------------------------------------

function LootboxUI.keypressed(key)
    if state == "dialog" then
        if key == "return" then
            LootboxUI.doTake()
            state = "browsing"
        elseif key == "n" or key == "escape" then
            state = "browsing"
        end
        return
    end

    -- Browsing
    if key == "up" then
        if lootbox and #lootbox.items > 0 then
            cursor = cursor - 1
            if cursor < 1 then cursor = #lootbox.items end
            LootboxUI.ensureVisible()
        end
    elseif key == "down" then
        if lootbox and #lootbox.items > 0 then
            cursor = cursor + 1
            if cursor > #lootbox.items then cursor = 1 end
            LootboxUI.ensureVisible()
        end
    elseif key == "return" then
        if lootbox and cursor >= 1 and cursor <= #lootbox.items then
            state = "dialog"
        end
    elseif key == "q" or key == "escape" then
        LootboxUI.close()
    end
end

function LootboxUI.ensureVisible()
    local maxRows = CONTENT_BOT - CONTENT_TOP - 2  -- minus header + separator
    if cursor <= scrollOffset then
        scrollOffset = cursor - 1
    elseif cursor > scrollOffset + maxRows then
        scrollOffset = cursor - maxRows
    end
    if scrollOffset < 0 then scrollOffset = 0 end
end

------------------------------------------------------------
-- ACTIONS
------------------------------------------------------------

function LootboxUI.doTake()
    if not lootbox or not player then return end
    if cursor < 1 or cursor > #lootbox.items then return end

    local itemId = lootbox.items[cursor]
    local ok, err = Inventory.addItem(player.inventory, itemId, 1)
    if ok then
        table.remove(lootbox.items, cursor)
        local def = Items.get(itemId)
        local name = def and (def.name .. "." .. def.ext) or "UNKNOWN"
        statusMsg = "Took " .. name
        statusTimer = 2
        if cursor > #lootbox.items then
            cursor = math.max(1, #lootbox.items)
        end
    else
        statusMsg = err or "Inventory full!"
        statusTimer = 2
    end
end

return LootboxUI
