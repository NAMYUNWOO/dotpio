-- Regression: economy telemetry payload includes input/output/SRL envelope
-- Run: lua scripts/regression_economy_telemetry.lua

package.path = "./?.lua;./?/init.lua;" .. package.path

local json = require("libs.json")
local EconomyTelemetry = require("src.economy_telemetry")

local function fail(msg)
    io.stderr:write("[FAIL] " .. msg .. "\n")
    os.exit(1)
end

local function expect(cond, msg)
    if not cond then fail(msg) end
end

local tmpDir = "logs/_regression"
os.execute(string.format("mkdir -p %q", tmpDir))
local logPath = tmpDir .. "/economy_telemetry_test.ndjson"
os.remove(logPath)

local ok1, err1 = EconomyTelemetry.append("disassemble", {
    status = "ok",
    itemId = "rusty_sword",
    inputCount = 1,
    srlBefore = 10,
    srlSpent = 2,
    srlAfter = 8,
    outputCount = 2,
    outputs = {
        { itemId = "iron_scrap", count = 2 },
        { itemId = "dust", count = 1 },
    },
}, { logDir = tmpDir, logPath = logPath })
expect(ok1, "failed to append disassemble telemetry: " .. tostring(err1))

local ok2, err2 = EconomyTelemetry.append("build", {
    status = "ok",
    folder = "WEAPONS",
    componentCount = 3,
    requiredComponents = 3,
    components = {"iron_scrap", "dust", "builder_core"},
    srlBefore = 8,
    srlSpent = 3,
    srlAfter = 5,
    outputItemId = "iron_blade",
    outputAdded = 1,
}, { logDir = tmpDir, logPath = logPath })
expect(ok2, "failed to append build telemetry: " .. tostring(err2))

local f = io.open(logPath, "r")
if not f then fail("telemetry log file not created") end
local lines = {}
for line in f:lines() do
    if line ~= "" then lines[#lines + 1] = line end
end
f:close()

expect(#lines == 2, string.format("expected 2 telemetry lines, got %d", #lines))

local row1 = json.decode(lines[1])
local row2 = json.decode(lines[2])

expect(row1.event == "disassemble", "row1 event should be disassemble")
expect(row1.itemId == "rusty_sword", "row1 itemId missing")
expect(row1.inputCount == 1, "row1 inputCount missing")
expect(row1.outputCount == 2, "row1 outputCount missing")
expect(type(row1.outputs) == "table" and #row1.outputs == 2, "row1 outputs missing")
expect(row1.srlBefore == 10 and row1.srlSpent == 2 and row1.srlAfter == 8, "row1 SRL envelope missing")
expect(type(row1.ts) == "string" and #row1.ts >= 20, "row1 timestamp missing")

expect(row2.event == "build", "row2 event should be build")
expect(row2.folder == "WEAPONS", "row2 folder missing")
expect(row2.componentCount == 3 and row2.requiredComponents == 3, "row2 component metadata missing")
expect(type(row2.components) == "table" and #row2.components == 3, "row2 components missing")
expect(row2.outputItemId == "iron_blade" and row2.outputAdded == 1, "row2 output metadata missing")
expect(row2.srlBefore == 8 and row2.srlSpent == 3 and row2.srlAfter == 5, "row2 SRL envelope missing")
expect(type(row2.ts) == "string" and #row2.ts >= 20, "row2 timestamp missing")

os.remove(logPath)
print("[PASS] economy telemetry regression validated")
