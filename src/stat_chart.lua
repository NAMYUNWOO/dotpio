local StatChart = {}

-- Catmull-Rom spline interpolation
local function catmullRom(t, p0, p1, p2, p3)
    local t2, t3 = t * t, t * t * t
    return 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)
end

-- Generate smooth curve points for a polygon with N vertices
local function generateCurvePoints(cx, cy, radius, values, n, segments)
    segments = segments or 8
    local points = {}
    -- Compute vertex positions
    local vx, vy = {}, {}
    for i = 1, n do
        local angle = -math.pi / 2 + (i - 1) * (2 * math.pi / n)
        local r = (values[i] / 10) * radius
        vx[i] = cx + math.cos(angle) * r
        vy[i] = cy + math.sin(angle) * r
    end
    -- Generate curve through vertices using Catmull-Rom
    for i = 1, n do
        local i0 = ((i - 2) % n) + 1
        local i1 = i
        local i2 = (i % n) + 1
        local i3 = ((i + 1) % n) + 1
        for s = 0, segments - 1 do
            local t = s / segments
            local px = catmullRom(t, vx[i0], vx[i1], vx[i2], vx[i3])
            local py = catmullRom(t, vy[i0], vy[i1], vy[i2], vy[i3])
            points[#points + 1] = {px, py}
        end
    end
    return points
end

-- Draw background grid (axes + outline)
local function drawGrid(cx, cy, radius, n)
    love.graphics.setLineWidth(1)
    -- Max outline
    love.graphics.setColor(1, 1, 1, 0.08)
    local outVerts = {}
    for i = 1, n do
        local angle = -math.pi / 2 + (i - 1) * (2 * math.pi / n)
        outVerts[#outVerts + 1] = cx + math.cos(angle) * radius
        outVerts[#outVerts + 1] = cy + math.sin(angle) * radius
    end
    love.graphics.polygon("line", outVerts)
    -- Axis lines
    love.graphics.setColor(1, 1, 1, 0.06)
    for i = 1, n do
        local angle = -math.pi / 2 + (i - 1) * (2 * math.pi / n)
        love.graphics.line(cx, cy, cx + math.cos(angle) * radius, cy + math.sin(angle) * radius)
    end
    -- Mid ring
    love.graphics.setColor(1, 1, 1, 0.04)
    local midVerts = {}
    for i = 1, n do
        local angle = -math.pi / 2 + (i - 1) * (2 * math.pi / n)
        midVerts[#midVerts + 1] = cx + math.cos(angle) * radius * 0.5
        midVerts[#midVerts + 1] = cy + math.sin(angle) * radius * 0.5
    end
    love.graphics.polygon("line", midVerts)
end

-- Draw a radar chart with gradient fill and curved edges
local function drawChart(cx, cy, radius, stats, keys, color, alpha)
    local n = #keys
    local values = {}
    for i, k in ipairs(keys) do
        values[i] = math.max(1, math.min(10, stats[k] or 1))
    end

    -- Background grid
    drawGrid(cx, cy, radius, n)

    -- Generate curve points
    local curvePoints = generateCurvePoints(cx, cy, radius, values, n, 8)

    -- Build mesh with gradient: center opaque → edge transparent
    local meshVerts = {}
    -- Center vertex
    meshVerts[1] = {cx, cy, 0, 0, color[1], color[2], color[3], alpha}
    for i, p in ipairs(curvePoints) do
        meshVerts[i + 1] = {p[1], p[2], 0, 0, color[1], color[2], color[3], alpha * 0.15}
    end

    -- Build triangle fan indices
    local indices = {}
    local numPts = #curvePoints
    for i = 1, numPts do
        indices[#indices + 1] = 1         -- center
        indices[#indices + 1] = i + 1     -- current point
        indices[#indices + 1] = (i % numPts) + 2  -- next point (wrap)
    end

    local mesh = love.graphics.newMesh(meshVerts, "triangles")
    mesh:setVertexMap(indices)
    love.graphics.setColor(1, 1, 1, 1)
    love.graphics.draw(mesh)

    -- Curve outline
    local outlineVerts = {}
    for _, p in ipairs(curvePoints) do
        outlineVerts[#outlineVerts + 1] = p[1]
        outlineVerts[#outlineVerts + 1] = p[2]
    end
    if #outlineVerts >= 6 then
        love.graphics.setColor(color[1], color[2], color[3], alpha * 0.7)
        love.graphics.setLineWidth(1.5)
        love.graphics.polygon("line", outlineVerts)
        love.graphics.setLineWidth(1)
    end

    -- Axis labels
    love.graphics.setColor(1, 1, 1, 0.5)
    local font = love.graphics.getFont()
    local labels
    if n == 4 then
        labels = {"ATK", "DEF", "AGI", "INT"}
    else
        labels = {"Fi", "Wa", "Gr", "El", "Ic", "Po", "Ea", "Wi"}
    end
    for i = 1, n do
        local angle = -math.pi / 2 + (i - 1) * (2 * math.pi / n)
        local lx = cx + math.cos(angle) * (radius + 8)
        local ly = cy + math.sin(angle) * (radius + 8)
        local lbl = labels[i]
        local tw = font:getWidth(lbl)
        love.graphics.print(lbl, lx - tw / 2, ly - font:getHeight() / 2)
    end
end

function StatChart.drawQuad(cx, cy, radius, stats, keys, color, alpha)
    drawChart(cx, cy, radius, stats, keys, color or {0.3, 0.8, 1.0}, alpha or 0.6)
end

function StatChart.drawOcta(cx, cy, radius, stats, keys, color, alpha)
    drawChart(cx, cy, radius, stats, keys, color or {1.0, 0.5, 0.3}, alpha or 0.5)
end

return StatChart
