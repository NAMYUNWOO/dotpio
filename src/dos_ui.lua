local DosUI = {}

-- 16-color ANSI palette
DosUI.colors = {
    [0]  = {0/255, 0/255, 0/255},       -- Black
    [1]  = {170/255, 0/255, 0/255},      -- Red
    [2]  = {0/255, 170/255, 0/255},      -- Green
    [3]  = {170/255, 85/255, 0/255},     -- Brown
    [4]  = {0/255, 0/255, 170/255},      -- Blue
    [5]  = {170/255, 0/255, 170/255},    -- Magenta
    [6]  = {0/255, 170/255, 170/255},    -- Cyan
    [7]  = {170/255, 170/255, 170/255},  -- Light Gray
    [8]  = {85/255, 85/255, 85/255},     -- Dark Gray
    [9]  = {255/255, 85/255, 85/255},    -- Light Red
    [10] = {85/255, 255/255, 85/255},    -- Light Green
    [11] = {255/255, 255/255, 85/255},   -- Light Yellow
    [12] = {85/255, 85/255, 255/255},    -- Light Blue
    [13] = {255/255, 85/255, 255/255},   -- Light Magenta
    [14] = {85/255, 255/255, 255/255},   -- Light Cyan
    [15] = {255/255, 255/255, 255/255},  -- White
}

-- Single-line box drawing (like MDIR)
DosUI.BOX = {
    TL = "\xe2\x94\x8c",  -- ┌ U+250C
    TR = "\xe2\x94\x90",  -- ┐ U+2510
    BL = "\xe2\x94\x94",  -- └ U+2514
    BR = "\xe2\x94\x98",  -- ┘ U+2518
    H  = "\xe2\x94\x80",  -- ─ U+2500
    V  = "\xe2\x94\x82",  -- │ U+2502
    LT = "\xe2\x94\x9c",  -- ├ U+251C
    RT = "\xe2\x94\xa4",  -- ┤ U+2524
    TT = "\xe2\x94\xac",  -- ┬ U+252C
    BT = "\xe2\x94\xb4",  -- ┴ U+2534
    CR = "\xe2\x94\xbc",  -- ┼ U+253C
}

DosUI.COLS = 80
DosUI.ROWS = 40

local font = nil
local charW = 0
local charH = 0
local offsetX = 0
local offsetY = 0

function DosUI.init()
    font = love.graphics.newFont("assets/dos_font.ttf", 16)
    font:setFilter("nearest", "nearest")
    charW = font:getWidth("A")
    charH = font:getHeight()
    local screenW = love.graphics.getWidth()
    local screenH = love.graphics.getHeight()
    offsetX = math.floor((screenW - DosUI.COLS * charW) / 2)
    offsetY = math.floor((screenH - DosUI.ROWS * charH) / 2)
end

function DosUI.getFont()
    return font
end

function DosUI.getCellSize()
    return charW, charH
end

function DosUI.getOffset()
    return offsetX, offsetY
end

function DosUI.setColor(colorIdx)
    local c = DosUI.colors[colorIdx] or DosUI.colors[7]
    love.graphics.setColor(c[1], c[2], c[3], 1)
end

-- Draw a single character at grid position (handles multi-byte UTF-8)
function DosUI.putChar(col, row, char, fg, bg)
    local px = offsetX + col * charW
    local py = offsetY + row * charH
    if bg and bg >= 0 then
        DosUI.setColor(bg)
        love.graphics.rectangle("fill", px, py, charW, charH)
    end
    if fg then
        DosUI.setColor(fg)
    end
    love.graphics.setFont(font)
    love.graphics.print(char, px, py)
end

-- Draw ASCII-only string at grid position
function DosUI.putString(col, row, str, fg, bg, maxLen)
    if maxLen and #str > maxLen then
        str = str:sub(1, maxLen)
    end
    local px = offsetX + col * charW
    local py = offsetY + row * charH
    local w = #str * charW
    if bg and bg >= 0 then
        DosUI.setColor(bg)
        love.graphics.rectangle("fill", px, py, w, charH)
    end
    if fg then
        DosUI.setColor(fg)
    end
    love.graphics.setFont(font)
    love.graphics.print(str, px, py)
end

function DosUI.fillRect(col, row, w, h, char, fg, bg)
    local px = offsetX + col * charW
    local py = offsetY + row * charH
    if bg and bg >= 0 then
        DosUI.setColor(bg)
        love.graphics.rectangle("fill", px, py, w * charW, h * charH)
    end
    if char and char ~= "" and fg then
        DosUI.setColor(fg)
        love.graphics.setFont(font)
        local line = string.rep(char, w)
        for r = 0, h - 1 do
            love.graphics.print(line, px, py + r * charH)
        end
    end
end

-- Draw single-line box: ┌─┐│└┘
function DosUI.drawBox(col, row, w, h, fg, bg)
    local B = DosUI.BOX
    if bg and bg >= 0 then
        DosUI.fillRect(col, row, w, h, " ", nil, bg)
    end
    love.graphics.setFont(font)
    DosUI.setColor(fg or 7)
    -- Draw char by char to avoid multi-byte string width issues
    -- Top-left corner
    DosUI.putChar(col, row, B.TL, fg, -1)
    -- Top edge
    for c = 1, w - 2 do
        DosUI.putChar(col + c, row, B.H, fg, -1)
    end
    -- Top-right corner
    DosUI.putChar(col + w - 1, row, B.TR, fg, -1)
    -- Bottom-left corner
    DosUI.putChar(col, row + h - 1, B.BL, fg, -1)
    -- Bottom edge
    for c = 1, w - 2 do
        DosUI.putChar(col + c, row + h - 1, B.H, fg, -1)
    end
    -- Bottom-right corner
    DosUI.putChar(col + w - 1, row + h - 1, B.BR, fg, -1)
    -- Sides
    for r = 1, h - 2 do
        DosUI.putChar(col, row + r, B.V, fg, -1)
        DosUI.putChar(col + w - 1, row + r, B.V, fg, -1)
    end
end

-- Panel = box with title on separate header row (MDIR style)
-- Title row sits at `row`, box starts at `row+1`
-- Total height = h (1 title row + h-1 box rows)
function DosUI.drawPanel(col, row, w, h, title, fg, bg)
    -- Title/header row (separate, above box)
    DosUI.fillRect(col, row, w, 1, " ", nil, bg or 0)
    if title and #title > 0 then
        local t = " " .. title .. " "
        local tx = col + math.floor((w - #t) / 2)
        DosUI.putString(tx, row, t, fg or 15, bg or 0)
    end
    -- Box below the title
    if h > 1 then
        DosUI.drawBox(col, row + 1, w, h - 1, fg, bg)
    end
end

-- Horizontal line with T-junctions at ends (for splitting inside a box)
function DosUI.drawHLine(col, row, w, fg, bg)
    local B = DosUI.BOX
    if bg and bg >= 0 then
        local px = offsetX + col * charW
        local py = offsetY + row * charH
        DosUI.setColor(bg)
        love.graphics.rectangle("fill", px, py, w * charW, charH)
    end
    DosUI.putChar(col, row, B.LT, fg, -1)
    for c = 1, w - 2 do
        DosUI.putChar(col + c, row, B.H, fg, -1)
    end
    DosUI.putChar(col + w - 1, row, B.RT, fg, -1)
end

-- Vertical line (for splitting inside a box)
function DosUI.drawVLine(col, row, h, fg, bg)
    for r = 0, h - 1 do
        DosUI.putChar(col, row + r, DosUI.BOX.V, fg, bg)
    end
end

-- T-junction connectors for joining panels
function DosUI.putTT(col, row, fg)  -- ┬
    DosUI.putChar(col, row, DosUI.BOX.TT, fg, -1)
end
function DosUI.putBT(col, row, fg)  -- ┴
    DosUI.putChar(col, row, DosUI.BOX.BT, fg, -1)
end
function DosUI.putCR(col, row, fg)  -- ┼
    DosUI.putChar(col, row, DosUI.BOX.CR, fg, -1)
end

return DosUI
