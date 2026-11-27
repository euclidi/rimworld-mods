# Directional sprite references

[mini-dungeon-directional.zip](mini-dungeon-directional.zip) contains 111 transparent 160×160 PNGs. Human and orc share fixed framing, with one idle frame and eight samples per walk and sprint cycle in south, east and north views. Three prop studies cover the shield, spear and sword in the same views. The east character faces right on screen. Mirror it only if the equipment can also be mirrored.

[manifest.json](manifest.json) records source frame, clip duration and model hashes. Rebuild against the checked-in GLBs with Blender 4.2:

    blender --background --factory-startup --python-exit-code 1 --python render_mini_dungeon.py -- --output ./build-sprites

The [original Mini Dungeon license](../foundations-3d/kenney-mini-dungeon/LICENSE-CC0.txt) applies to the source art. [Texture study archives](texture-study/sources.json) add three 16 px packs with dungeon, town and farm silhouettes for comparison. These references live in AssetLab. Match RimWorld pawn alignment, tint masks, apparel and rendering conventions before adapting any derivatives for a mod.
