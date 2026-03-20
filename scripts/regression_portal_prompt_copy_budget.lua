-- Regression: portal prompt copy budget checker should warn on over-budget route preview lines.
-- Run: lua scripts/regression_portal_prompt_copy_budget.lua

package.path = "./?.lua;./?/init.lua;" .. package.path

local Budget = require("src.portal_prompt_budget")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

local sampleEntries = {
    { sourceMap = "01", targetMap = "02", targetRouteTag = "SAFE" },
    { sourceMap = "02", targetMap = "07", targetRouteTag = "SPIKE" },
    { sourceMap = "03", targetMap = "99", targetRouteTag = nil },
}

local okReport = Budget.analyze(sampleEntries, 80)
expect(okReport.status == "OK", "status should be OK when prompts stay within budget")
expect(okReport.warningCount == 0, "warning count should be zero for generous budget")
expect(okReport.maxObservedChars > 0, "max observed chars should be populated")

local warnReport = Budget.analyze(sampleEntries, 60)
expect(warnReport.status == "WARN", "status should become WARN when budget is too small")
expect(warnReport.warningCount == #sampleEntries, "all prompts should exceed tiny budget")
expect(warnReport.warnings[1].overBy > 0, "warning should report positive overBy")

local unknownSample = nil
for _, sample in ipairs(okReport.samples) do
    if sample.routeTag == "UNKNOWN" then
        unknownSample = sample
        break
    end
end
expect(unknownSample ~= nil, "unknown route tag sample should be preserved")
expect(unknownSample.coach == "NO DATA", "unknown route tag should map to NO DATA coach")

print("[PASS] portal prompt copy budget regression validated")
