-- Regression: route-tag distribution checker warning logic.
-- Run: lua scripts/regression_route_tag_distribution.lua

package.path = "./?.lua;./?/init.lua;" .. package.path

local RouteTagDistribution = require("src.route_tag_distribution")

local function expect(ok, msg)
    if not ok then
        io.stderr:write("[FAIL] " .. msg .. "\n")
        os.exit(1)
    end
end

local converged = RouteTagDistribution.analyzeMapTables({
    {
        mapName = "07",
        mapData = { metadata = { overclockHazard = { routeTag = "SPIKE" } } },
    },
    {
        mapName = "08",
        mapData = { metadata = { overclockHazard = { routeTag = "SPIKE" } } },
    },
})

expect(converged.status == "WARN", "converged hazard maps should warn")
expect(converged.hazardMapCount == 2, "hazard map count should match valid route-tag maps")
expect(converged.uniqueRouteTagCount == 1, "converged test should report single profile")
expect(converged.counts.SPIKE == 2 and converged.counts.SAFE == 0 and converged.counts.RISK == 0, "converged counts should be correct")

local mixed = RouteTagDistribution.analyzeMapTables({
    {
        mapName = "05",
        mapData = { metadata = { overclockHazard = { routeTag = "SAFE" } } },
    },
    {
        mapName = "06",
        mapData = { metadata = { overclockHazard = { routeTag = "RISK" } } },
    },
    {
        mapName = "07",
        mapData = { metadata = { overclockHazard = { routeTag = "SPIKE" } } },
    },
})

expect(mixed.status == "OK", "mixed profile hazard maps should be healthy")
expect(mixed.uniqueRouteTagCount == 3, "mixed profile should report all tags")
expect(mixed.counts.SAFE == 1 and mixed.counts.RISK == 1 and mixed.counts.SPIKE == 1, "mixed profile counts should be balanced")

local invalidTag = RouteTagDistribution.analyzeMapTables({
    {
        mapName = "09",
        mapData = { metadata = { overclockHazard = { routeTag = "CHAOS" } } },
    },
})
expect(invalidTag.status == "WARN", "invalid route tag should warn")
expect(#invalidTag.invalidTags == 1, "invalid route tag should be captured")

print("[PASS] route-tag distribution regression validated")
