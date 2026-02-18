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

# Output Lua
with open('map_data.lua', 'w') as f:
    f.write(f'-- Auto-generated from layerd_fantasy.tmx\nreturn {{\n')
    f.write(f'  width = {width},\n  height = {height},\n')
    for name, grid in layers.items():
        f.write(f'  {name} = {{\n')
        for row in grid:
            f.write('    {' + ', '.join(str(v) for v in row) + '},\n')
        f.write('  },\n')
    f.write('}\n')

# Stats
for name, grid in layers.items():
    nonzero = sum(1 for row in grid for v in row if v != 0)
    print(f'  {name}: {nonzero} non-empty tiles')
print(f'Map: {width}x{height}, {len(layers)} layers')
