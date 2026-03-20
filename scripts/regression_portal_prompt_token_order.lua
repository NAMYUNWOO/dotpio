-- Regression: portal transition prompt token-order linter + budget parser baseline.
-- Run: lua scripts/regression_portal_prompt_token_order.lua

package.path = package.path .. ";./?.lua;./src/?.lua"

local Linter = require("src.portal_prompt_linter")

local function expect(condition, message)
    if not condition then
        error("[FAIL] " .. tostring(message), 2)
    end
end

local report = Linter.analyze(76)
expect(report.status == "OK", "token-order lint should pass at default budget")
expect(report.warningCount == 0, "warning count should be zero at default budget")
expect(report.checkedCount == 20, "should sample all routeTag/pressure combinations")

local tightReport = Linter.analyze(20)
expect(tightReport.status == "WARN", "tiny budget should force warnings")
expect(tightReport.warningCount > 0, "tiny budget should generate over-budget warnings")

print("[PASS] portal prompt token-order regression validated")
