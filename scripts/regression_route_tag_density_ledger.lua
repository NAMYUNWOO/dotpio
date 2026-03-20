-- Regression: route-tag density ledger depth accounting.
-- Run: lua scripts/regression_route_tag_density_ledger.lua

package.path = "./?.lua;./?/init.lua;" .. package.path

local Ledger = require("src.route_tag_density_ledger")

local function expect(ok, message)
    if not ok then
        io.stderr:write("[FAIL] " .. message .. "\n")
        os.exit(1)
    end
end

local report = Ledger.analyzeEntries({
    {
        mapId = "01",
        mapData = {
            metadata = { overclockHazard = { routeTag = "SAFE" } },
            portals = {
                { targetMap = "02" },
                { targetMap = "03" },
            },
        },
    },
    {
        mapId = "02",
        mapData = {
            metadata = { overclockHazard = { routeTag = "RISK" } },
            portals = {
                { targetMap = "04" },
            },
        },
    },
    {
        mapId = "03",
        mapData = {
            metadata = { overclockHazard = { routeTag = "SPIKE" } },
            portals = {
                { targetMap = "04" },
            },
        },
    },
    {
        mapId = "04",
        mapData = {
            metadata = { overclockHazard = { routeTag = "RISK" } },
            portals = {},
        },
    },
})

expect(report.mapCount == 4, "map count should be 4")

local byStart = {}
for _, ledger in ipairs(report.ledgers or {}) do
    byStart[ledger.startMap] = ledger
end

local start01 = byStart["01"]
expect(start01 ~= nil, "ledger for start map 01 must exist")
expect(start01.reachableCount == 3, "map_01 should reach 3 maps")
expect(#start01.depthRows == 2, "map_01 should have two depth rows")

local depth1 = start01.depthRows[1]
expect(depth1.depth == 1, "depth1 row should be depth 1")
expect(depth1.totalReachable == 2, "depth1 should include two maps")
expect(depth1.tagCounts.RISK == 1 and depth1.tagCounts.SPIKE == 1, "depth1 tag counts should be RISK=1/SPIKE=1")

local depth2 = start01.depthRows[2]
expect(depth2.depth == 2, "depth2 row should be depth 2")
expect(depth2.totalReachable == 1, "depth2 should include one map")
expect(depth2.tagCounts.RISK == 1 and depth2.tagCounts.SAFE == 0 and depth2.tagCounts.SPIKE == 0, "depth2 tag counts should only include RISK")

local start04 = byStart["04"]
expect(start04 ~= nil, "ledger for start map 04 must exist")
expect(start04.reachableCount == 0, "leaf map should have zero reachable maps")
expect(#start04.depthRows == 0, "leaf map should have no depth rows")

print("[PASS] route-tag density ledger regression validated")
