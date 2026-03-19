local maps = { "03", "04", "05", "06", "07" }

local seenSilhouette = {}
local seenLane = {}
local report = {}

for _, mapId in ipairs(maps) do
    local data = dofile("maps/map_" .. mapId .. ".lua")
    local meta = data.metadata or {}
    assert(type(meta.silhouette) == "string" and meta.silhouette ~= "", "map_" .. mapId .. " missing metadata.silhouette")
    assert(type(meta.laneStructure) == "string" and meta.laneStructure ~= "", "map_" .. mapId .. " missing metadata.laneStructure")
    assert(type(meta.encounterRhythm) == "string" and meta.encounterRhythm ~= "", "map_" .. mapId .. " missing metadata.encounterRhythm")

    assert(not seenSilhouette[meta.silhouette], "duplicate silhouette tag: " .. meta.silhouette)
    assert(not seenLane[meta.laneStructure], "duplicate laneStructure tag: " .. meta.laneStructure)
    seenSilhouette[meta.silhouette] = true
    seenLane[meta.laneStructure] = true

    local encounter = meta.encounterProfile or {}
    local mul = tonumber(encounter.enemyCountMultiplier)
    assert(mul and mul > 0, "map_" .. mapId .. " invalid encounterProfile.enemyCountMultiplier")
    local bias = encounter.variantBias or {}
    local biasCount = 0
    for _, v in pairs(bias) do
        if tonumber(v) then biasCount = biasCount + 1 end
    end
    assert(biasCount >= 2, "map_" .. mapId .. " needs >=2 variant bias entries")

    report[#report + 1] = string.format("map_%s silhouette=%s lanes=%s enemyMul=%.2f biasKeys=%d", mapId, meta.silhouette, meta.laneStructure, mul, biasCount)
end

print("[regression_map_profile_distinctness] PASS")
for _, line in ipairs(report) do
    print(" - " .. line)
end
