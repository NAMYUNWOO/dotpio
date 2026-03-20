-- Regression: overclock dwell-bucket telemetry artifact schema + bucket math.
-- Run: lua scripts/regression_overclock_dwell_buckets.lua

package.path = "./?.lua;./?/init.lua;" .. package.path

local OverclockHazard = require("src.overclock_hazard")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

local function readFile(path)
    local f = assert(io.open(path, "r"))
    local data = f:read("*a")
    f:close()
    return data
end

OverclockHazard.resetRunTelemetry()
OverclockHazard.onMapLoaded("07", {
    overclockHazard = {
        rect = { x = 10, y = 10, w = 4, h = 4 },
        pulseDuration = 20,
        cooldownDuration = 20,
    }
})

-- Enter zone and stay for 13s total:
-- LOW 0~5s => 5s
-- MID 5~12s => 7s
-- HIGH 12~13s => 1s
OverclockHazard.update(0.1, 11, 11)
OverclockHazard.update(4.9, 11, 11)
OverclockHazard.update(7.0, 11, 11)
OverclockHazard.update(1.0, 11, 11)
OverclockHazard.update(0.0, 2, 2)

local buckets = OverclockHazard.getRunDwellBuckets()
expect(buckets.LOW == 5, "LOW bucket should be 5 seconds")
expect(buckets.MID == 7, "MID bucket should be 7 seconds")
expect(buckets.HIGH == 1, "HIGH bucket should be 1 second")

local base = "logs/playtests/regression_overclock_dwell_buckets"
local out, err = OverclockHazard.writeRunDwellArtifact(base)
expect(out ~= nil, "artifact writer should return metadata: " .. tostring(err))

local jsonText = readFile(base .. ".json")
local mdText = readFile(base .. ".md")

expect(jsonText:find('"dwellBuckets"'), "json should include dwellBuckets object")
expect(jsonText:find('"LOW": 5'), "json should include LOW bucket value")
expect(jsonText:find('"MID": 7'), "json should include MID bucket value")
expect(jsonText:find('"HIGH": 1'), "json should include HIGH bucket value")
expect(jsonText:find('"totalExposureSeconds": 13'), "json should include total exposure seconds")

expect(mdText:find("# Overclock Exposure Dwell Buckets"), "markdown should include header")
expect(mdText:find("- LOW: 5"), "markdown should include LOW row")
expect(mdText:find("- MID: 7"), "markdown should include MID row")
expect(mdText:find("- HIGH: 1"), "markdown should include HIGH row")
expect(mdText:find("- Total exposure seconds: 13"), "markdown should include total row")

print("[PASS] overclock dwell-bucket telemetry regression validated")
