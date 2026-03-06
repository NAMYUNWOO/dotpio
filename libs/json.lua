-- Minimal JSON encoder/decoder for Lua
-- Handles basic types: string, number, boolean, nil, table (array/object)

local json = {}

-- Encode --

local encodeValue

local function encodeString(s)
    s = s:gsub('\\', '\\\\')
    s = s:gsub('"', '\\"')
    s = s:gsub('\n', '\\n')
    s = s:gsub('\r', '\\r')
    s = s:gsub('\t', '\\t')
    return '"' .. s .. '"'
end

local function isArray(t)
    local i = 0
    for _ in pairs(t) do
        i = i + 1
        if t[i] == nil then return false end
    end
    return true
end

local function encodeArray(arr)
    local parts = {}
    for i = 1, #arr do
        parts[i] = encodeValue(arr[i])
    end
    return "[" .. table.concat(parts, ",") .. "]"
end

local function encodeObject(obj)
    local parts = {}
    for k, v in pairs(obj) do
        if type(k) == "string" then
            parts[#parts + 1] = encodeString(k) .. ":" .. encodeValue(v)
        end
    end
    return "{" .. table.concat(parts, ",") .. "}"
end

encodeValue = function(v)
    local t = type(v)
    if v == nil then return "null"
    elseif t == "boolean" then return v and "true" or "false"
    elseif t == "number" then
        if v ~= v then return "null" end -- NaN
        if v == math.huge or v == -math.huge then return "null" end
        return tostring(v)
    elseif t == "string" then return encodeString(v)
    elseif t == "table" then
        if isArray(v) then return encodeArray(v)
        else return encodeObject(v) end
    else
        return "null"
    end
end

function json.encode(v)
    return encodeValue(v)
end

-- Decode --

local function skipWhitespace(s, i)
    while i <= #s do
        local c = s:byte(i)
        if c == 32 or c == 9 or c == 10 or c == 13 then
            i = i + 1
        else
            break
        end
    end
    return i
end

local decodeValue

local function decodeString(s, i)
    -- i points to opening "
    i = i + 1
    local parts = {}
    while i <= #s do
        local c = s:sub(i, i)
        if c == '"' then
            return table.concat(parts), i + 1
        elseif c == '\\' then
            i = i + 1
            local esc = s:sub(i, i)
            if esc == '"' then parts[#parts+1] = '"'
            elseif esc == '\\' then parts[#parts+1] = '\\'
            elseif esc == '/' then parts[#parts+1] = '/'
            elseif esc == 'n' then parts[#parts+1] = '\n'
            elseif esc == 'r' then parts[#parts+1] = '\r'
            elseif esc == 't' then parts[#parts+1] = '\t'
            elseif esc == 'u' then
                local hex = s:sub(i+1, i+4)
                local code = tonumber(hex, 16)
                if code and code < 128 then
                    parts[#parts+1] = string.char(code)
                else
                    parts[#parts+1] = "?"
                end
                i = i + 4
            else
                parts[#parts+1] = esc
            end
            i = i + 1
        else
            parts[#parts+1] = c
            i = i + 1
        end
    end
    error("Unterminated string")
end

local function decodeNumber(s, i)
    local j = i
    if s:sub(j, j) == '-' then j = j + 1 end
    while j <= #s and s:sub(j, j):match("[0-9]") do j = j + 1 end
    if j <= #s and s:sub(j, j) == '.' then
        j = j + 1
        while j <= #s and s:sub(j, j):match("[0-9]") do j = j + 1 end
    end
    if j <= #s and s:sub(j, j):match("[eE]") then
        j = j + 1
        if j <= #s and s:sub(j, j):match("[%+%-]") then j = j + 1 end
        while j <= #s and s:sub(j, j):match("[0-9]") do j = j + 1 end
    end
    local num = tonumber(s:sub(i, j - 1))
    if not num then error("Invalid number at " .. i) end
    return num, j
end

local function decodeArray(s, i)
    i = i + 1 -- skip [
    local arr = {}
    i = skipWhitespace(s, i)
    if s:sub(i, i) == ']' then return arr, i + 1 end
    while true do
        local val
        val, i = decodeValue(s, i)
        arr[#arr + 1] = val
        i = skipWhitespace(s, i)
        local c = s:sub(i, i)
        if c == ']' then return arr, i + 1
        elseif c == ',' then i = skipWhitespace(s, i + 1)
        else error("Expected ',' or ']' at " .. i) end
    end
end

local function decodeObject(s, i)
    i = i + 1 -- skip {
    local obj = {}
    i = skipWhitespace(s, i)
    if s:sub(i, i) == '}' then return obj, i + 1 end
    while true do
        i = skipWhitespace(s, i)
        if s:sub(i, i) ~= '"' then error("Expected string key at " .. i) end
        local key
        key, i = decodeString(s, i)
        i = skipWhitespace(s, i)
        if s:sub(i, i) ~= ':' then error("Expected ':' at " .. i) end
        i = skipWhitespace(s, i + 1)
        local val
        val, i = decodeValue(s, i)
        obj[key] = val
        i = skipWhitespace(s, i)
        local c = s:sub(i, i)
        if c == '}' then return obj, i + 1
        elseif c == ',' then i = skipWhitespace(s, i + 1)
        else error("Expected ',' or '}' at " .. i) end
    end
end

decodeValue = function(s, i)
    i = skipWhitespace(s, i)
    local c = s:sub(i, i)
    if c == '"' then return decodeString(s, i)
    elseif c == '{' then return decodeObject(s, i)
    elseif c == '[' then return decodeArray(s, i)
    elseif c == 't' then
        if s:sub(i, i+3) == "true" then return true, i+4 end
        error("Invalid value at " .. i)
    elseif c == 'f' then
        if s:sub(i, i+4) == "false" then return false, i+5 end
        error("Invalid value at " .. i)
    elseif c == 'n' then
        if s:sub(i, i+3) == "null" then return nil, i+4 end
        error("Invalid value at " .. i)
    elseif c == '-' or c:match("[0-9]") then
        return decodeNumber(s, i)
    else
        error("Unexpected character '" .. c .. "' at " .. i)
    end
end

function json.decode(s)
    local val, _ = decodeValue(s, 1)
    return val
end

return json
