local EconomyTelemetry = {}

local function ensureDir(path)
    os.execute(string.format("mkdir -p %q", path))
end

local function utcNowIso()
    return os.date("!%Y-%m-%dT%H:%M:%SZ")
end

function EconomyTelemetry.append(eventType, fields, opts)
    local ok, json = pcall(require, "libs.json")
    if not ok or type(json) ~= "table" or type(json.encode) ~= "function" then
        return false, "json unavailable"
    end

    if type(eventType) ~= "string" or eventType == "" then
        return false, "invalid event type"
    end

    fields = fields or {}
    local payload = {
        event = eventType,
        ts = utcNowIso(),
    }
    for k, v in pairs(fields) do payload[k] = v end

    local line = json.encode(payload)
    if not line then return false, "encode failed" end

    local logDir = (opts and opts.logDir) or "logs"
    local logPath = (opts and opts.logPath) or (logDir .. "/economy_telemetry.ndjson")
    ensureDir(logDir)

    local f = io.open(logPath, "a")
    if not f then return false, "open failed" end
    f:write(line, "\n")
    f:close()
    return true
end

return EconomyTelemetry
