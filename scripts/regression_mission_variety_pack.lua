-- Regression: mission variety pack rotation and new objective catalog
-- Run: lua scripts/regression_mission_variety_pack.lua

local RunMissions = require("src.run_missions")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

local catalog = RunMissions.debugGetVariantCatalog()
local catalogCount = 0
for _ in pairs(catalog) do
    catalogCount = catalogCount + 1
end
expect(catalogCount >= 8, "objective catalog should include at least 8 variants")

local seenPackIds = {}
local seenObjectiveIds = {}
for i = 1, 4 do
    RunMissions.reset()
    local state = RunMissions.getState()
    expect(state.total == 3, "each generated pack should contain 3 objectives")
    expect(state.lastPackId ~= nil, "generated pack should expose pack id")
    expect(state.lastPackTag ~= nil and state.lastPackTag ~= "UNKNOWN", "generated pack should expose flavor tag")
    expect(state.lastPackLabel ~= nil and state.lastPackLabel ~= "unknown pacing", "generated pack should expose flavor label")
    seenPackIds[state.lastPackId] = true
    for _, objective in ipairs(state.objectives or {}) do
        seenObjectiveIds[objective.id] = true
    end
end

local packCount = 0
for _ in pairs(seenPackIds) do
    packCount = packCount + 1
end
expect(packCount >= 4, "mission reset should rotate through at least 4 pack ids")

expect(seenObjectiveIds["search_2"], "rotation should include new search objective")
expect(seenObjectiveIds["inventory_3"], "rotation should include new inventory objective")
expect(seenObjectiveIds["build_2"], "rotation should include new advanced build objective")

print("[PASS] mission variety pack regression validated")
