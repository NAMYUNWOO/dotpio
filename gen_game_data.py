#!/usr/bin/env python3
"""Parse layered TMX and generate Lua map data."""
import xml.etree.ElementTree as ET

tree = ET.parse('kenny1bit/Tilemap/layerd_fantasy.tmx')
root = tree.getroot()

width = int(root.get('width'))
height = int(root.get('height'))

layers = {}
for layer_el in root.findall('layer'):
    name = layer_el.get('name')
    data = layer_el.find('data').text.strip()
    values = [int(v.strip()) for v in data.split(',') if v.strip()]
    rows = []
    for y in range(height):
        rows.append(values[y * width : (y + 1) * width])
    layers[name] = rows

# Parse tsx for tile properties (dim, occlude_ov)
tsx_path = 'kenny1bit/Tilemap/tileset_colored.tsx'
tsx_tree = ET.parse(tsx_path)
tsx_root = tsx_tree.getroot()

dim_gids = []
occlude_gids = []
for tile_el in tsx_root.findall('tile'):
    tid = int(tile_el.get('id'))
    gid = tid + 1  # tsx tile id is 0-based, game GID is 1-based
    props = tile_el.find('properties')
    if props is None:
        continue
    for prop in props.findall('property'):
        name = prop.get('name')
        value = prop.get('value')
        if name == 'dim' and value == 'true':
            dim_gids.append(gid)
        elif name == 'occlude_ov' and value == 'true':
            occlude_gids.append(gid)

# Output Lua
with open('map_data.lua', 'w') as f:
    f.write(f'-- Auto-generated from layerd_fantasy.tmx\nreturn {{\n')
    f.write(f'  width = {width},\n  height = {height},\n')
    for name, grid in layers.items():
        f.write(f'  {name} = {{\n')
        for row in grid:
            f.write('    {' + ', '.join(str(v) for v in row) + '},\n')
        f.write('  },\n')

    # dim: tiles that block FOV rays (e.g. trees, walls)
    f.write('  dimTiles = { ')
    f.write(', '.join(f'[{g}]=true' for g in sorted(dim_gids)))
    f.write(' },\n')
    f.write('  occludeTiles = { ')
    f.write(', '.join(f'[{g}]=true' for g in sorted(occlude_gids)))
    f.write(' },\n')

    f.write('}\n')

# Stats
for name, grid in layers.items():
    nonzero = sum(1 for row in grid for v in row if v != 0)
    print(f'  {name}: {nonzero} non-empty tiles')
print(f'Map: {width}x{height}, {len(layers)} layers')
print(f'  dimTiles: {len(dim_gids)} GIDs')
print(f'  occludeTiles: {len(occlude_gids)} GIDs')
