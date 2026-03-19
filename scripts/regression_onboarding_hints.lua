local OnboardingHints = require("src.onboarding_hints")

local function assertTrue(cond, msg)
    if not cond then
        error(msg or "assertTrue failed")
    end
end

local function assertEq(a, b, msg)
    if a ~= b then
        error((msg or "assertEq failed") .. string.format(" (got=%s expected=%s)", tostring(a), tostring(b)))
    end
end

OnboardingHints.reset()
assertTrue(OnboardingHints.isActive(), "onboarding should start active")
assertTrue((OnboardingHints.getHint() or ""):match("MOVE:"), "first hint should teach movement")

OnboardingHints.mark("moved")
assertTrue((OnboardingHints.getHint() or ""):match("SEARCH:"), "second hint should teach search")

OnboardingHints.mark("searched")
assertTrue((OnboardingHints.getHint() or ""):match("PICKUP:"), "third hint should teach pickup")

OnboardingHints.mark("pickup")
assertTrue((OnboardingHints.getHint() or ""):match("INVENTORY:"), "fourth hint should teach inventory")

OnboardingHints.mark("inventory")
assertTrue((OnboardingHints.getHint() or ""):match("BUILD:"), "fifth hint should teach build")

OnboardingHints.mark("build")
local loopHint = OnboardingHints.getHint() or ""
assertTrue(loopHint:match("LOOP:") or loopHint:match("TIP:"), "post-onboarding hint should rotate loop tips")

OnboardingHints.update(300)
assertEq(OnboardingHints.isActive(), false, "onboarding window should expire at 5 minutes")
assertEq(OnboardingHints.getHint(), nil, "no hint should remain after onboarding expiry")

print("regression_onboarding_hints: PASS")
