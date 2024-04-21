import json
from litemapy import Schematic


schem = Schematic.load("21444.litematic")

if not schem.regions:
    raise ValueError("No regions found in the schematic.")

region = list(schem.regions.values())[0]

min_y_in_region = min(y for x, y, z in region.allblockpos() if region.getblock(x, y, z).blockid != "minecraft:air")

user_defined_start = {
    "x": 0,
    "y": 40,
    "z": 0,
}

blocks = []

for x, y, z in region.allblockpos():
    block_state = region.getblock(x, y, z)

    if block_state.blockid == "minecraft:air":
        continue
    relative_position = {
        "x": x - region.x,
        "y": y - min_y_in_region, 
        "z": z - region.z,
    }

    block_id = block_state.blockid
    print(block_state.__dict__)
    block_name = block_id.replace("minecraft:", "")
    properties = block_state._BlockState__properties
    blocks.append({
        "blockName": block_name,
        "facing" : properties['facing'] if 'facing' in properties else None,
        "relativePosition": relative_position,
    })
litematic_json = {
    "startingPosition": user_defined_start,
    "blocks": blocks,
}

litematic_json_str = json.dumps(litematic_json, indent=4)

with open("out.json", "w") as json_file:
    json_file.write(litematic_json_str)

print("JSON data saved to out.json")
