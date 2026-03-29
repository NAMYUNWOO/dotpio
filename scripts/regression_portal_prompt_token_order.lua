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
expect(type(report.writerPreview) == "table", "writer preview payload should be present")
expect(report.writerPreview.token == "CBGCFXWSBPFXPD MICROLINE", "writer preview token should match CBGCFXWSBPFXPD MICROLINE")
expect(report.writerPreview.legendVersion == "v1", "writer preview legend version should be v1")
expect(type(report.writerPreview.legendHash) == "string" and #report.writerPreview.legendHash == 12, "writer preview legend hash should be 12-char digest")
expect(type(report.writerPreview.decode) == "table", "writer preview decode table should be present")
expect(type(report.writerPreview.decode.S) == "string" and report.writerPreview.decode.S ~= "", "writer preview decode for S should be populated")
expect(type(report.writerPreview.decode.U) == "string" and report.writerPreview.decode.U ~= "", "writer preview decode for U should be populated")
expect(type(report.writerPreview.aliasPreviewRows) == "table" and #report.writerPreview.aliasPreviewRows == 2, "writer preview alias rows should include S/U examples")

local tightReport = Linter.analyze(20)
expect(tightReport.status == "WARN", "tiny budget should force warnings")
expect(tightReport.warningCount > 0, "tiny budget should generate over-budget warnings")

print("[PASS] portal prompt token-order regression validated")
