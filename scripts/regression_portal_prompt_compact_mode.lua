-- Regression: portal transition prompt should fall back to compact copy when budget is constrained.
-- Run: lua scripts/regression_portal_prompt_compact_mode.lua

package.path = "./?.lua;./?/init.lua;" .. package.path

local Portal = require("src.portal")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

Portal.resetCooldown()
Portal.check(10, 10, {
    getPortalAt = function(_, _)
        return { targetMap = "07", targetPortal = "06" }
    end,
})

local fullPrompt = Portal.getTransitionPrompt(160, { threatTier = "HIGH" })
expect(type(fullPrompt) == "string" and fullPrompt:find("NEXT ROUTE:SPIKE"), "full prompt should retain detailed NEXT ROUTE token")
expect(fullPrompt:find("COACH:HIGH PRESSURE"), "full prompt should retain full coach phrase")
expect(fullPrompt:find("PRESSURE:5"), "full prompt should include pressure token")

local compactPrompt = Portal.getTransitionPrompt(60, { threatTier = "HIGH" })
expect(type(compactPrompt) == "string" and compactPrompt:find("NEXT:SPIKE"), "compact prompt should use shortened NEXT token")
expect(compactPrompt:find("COACH:HIGH"), "compact prompt should use shortened coach token")
expect(compactPrompt:find("P:5"), "compact prompt should include abbreviated pressure token")
expect(not compactPrompt:find("NEXT ROUTE:"), "compact prompt should remove verbose NEXT ROUTE label")
expect(#compactPrompt < #fullPrompt, "compact prompt should be shorter than full prompt")

Portal.cancelTransition()

print("[PASS] portal prompt compact-mode regression validated")
