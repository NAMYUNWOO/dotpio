#!/usr/bin/env python3
"""Parse layered TMX files and generate Lua map data for multiple maps."""
import xml.etree.ElementTree as ET
import os
import math

# Parse tsx for tile properties (dim, occlude_ov) — shared across all maps
tsx_path = 'Tilemap/tileset_colored.tsx'
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

# Ensure output directory exists
os.makedirs('maps', exist_ok=True)

map_ids = ['01', '02', '03', '04']

for map_id in map_ids:
    tmx_path = f'Tilemap/layerd_fantasy_{map_id}.tmx'
    tree = ET.parse(tmx_path)
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

    # Parse portal objectgroup
    portals = []
    for objgroup in root.findall('objectgroup'):
        if objgroup.get('name') != 'portal':
            continue
        for obj in objgroup.findall('object'):
            props_el = obj.find('properties')
            if props_el is None:
                continue
            portal_name = None
            target_map = None
            target_portal = None
            for prop in props_el.findall('property'):
                pname = prop.get('name')
                pval = prop.get('value')
                if pname == 'portalName':
                    portal_name = pval
                elif pname == 'targetMap':
                    target_map = pval
                elif pname == 'targetPortalName':
                    target_portal = pval
            if portal_name and target_map and target_portal:
                px = float(obj.get('x'))
                py = float(obj.get('y'))
                pw = float(obj.get('width', '16'))
                ph = float(obj.get('height', '16'))
                # Compute all grid cells covered by the portal rectangle
                gx1 = max(1, math.floor(px / 16) + 1)
                gy1 = max(1, math.floor(py / 16) + 1)
                gx2 = min(width, math.floor((px + pw - 0.01) / 16) + 1)
                gy2 = min(height, math.floor((py + ph - 0.01) / 16) + 1)
                # First cell is the "anchor" used for spawn position
                anchor_x, anchor_y = gx1, gy1
                for cy in range(gy1, gy2 + 1):
                    for cx in range(gx1, gx2 + 1):
                        portals.append({
                            'name': portal_name,
                            'x': anchor_x,
                            'y': anchor_y,
                            'tileX': cx,
                            'tileY': cy,
                            'targetMap': target_map,
                            'targetPortal': target_portal,
                        })

    # Extract lootbox layer separately (not included in normal layer rendering)
    lootbox_grid = layers.pop('lootbox', None)

    # Output Lua
    out_path = f'maps/map_{map_id}.lua'
    with open(out_path, 'w') as f:
        f.write(f'-- Auto-generated from layerd_fantasy_{map_id}.tmx\nreturn {{\n')
        f.write(f'  width = {width},\n  height = {height},\n')
        for name, grid in layers.items():
            f.write(f'  {name} = {{\n')
            for row in grid:
                f.write('    {' + ', '.join(str(v) for v in row) + '},\n')
            f.write('  },\n')

        # lootbox layer
        if lootbox_grid:
            f.write('  lootbox = {\n')
            for row in lootbox_grid:
                f.write('    {' + ', '.join(str(v) for v in row) + '},\n')
            f.write('  },\n')

        # dim/occlude tiles (shared)
        f.write('  dimTiles = { ')
        f.write(', '.join(f'[{g}]=true' for g in sorted(dim_gids)))
        f.write(' },\n')
        f.write('  occludeTiles = { ')
        f.write(', '.join(f'[{g}]=true' for g in sorted(occlude_gids)))
        f.write(' },\n')

        # Portals: tileX/tileY = hit detection, x/y = spawn anchor
        f.write('  portals = {\n')
        for p in portals:
            f.write(f'    {{ name="{p["name"]}", x={p["x"]}, y={p["y"]}, tileX={p["tileX"]}, tileY={p["tileY"]}, targetMap="{p["targetMap"]}", targetPortal="{p["targetPortal"]}" }},\n')
        f.write('  },\n')

        f.write('}\n')

    # Stats
    print(f'\n=== Map {map_id} ({out_path}) ===')
    print(f'Map: {width}x{height}, {len(layers)} layers')
    for name, grid in layers.items():
        nonzero = sum(1 for row in grid for v in row if v != 0)
        print(f'  {name}: {nonzero} non-empty tiles')
    if lootbox_grid:
        lootbox_count = sum(1 for row in lootbox_grid for v in row if v != 0)
        print(f'  lootbox: {lootbox_count} positions')
    print(f'  portals: {len(portals)}')
    for p in portals:
        print(f'    {p["name"]}: ({p["x"]},{p["y"]}) -> map {p["targetMap"]} portal {p["targetPortal"]}')

print(f'\ndimTiles: {len(dim_gids)} GIDs')
print(f'occludeTiles: {len(occlude_gids)} GIDs')
