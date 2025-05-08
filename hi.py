import bpy

# 1. grab your source
src = bpy.data.objects["Cube"]

# 2. duplicate it (keep original safe)
bpy.ops.object.select_all(action='DESELECT')
src.select_set(True)
bpy.context.view_layer.objects.active = src
bpy.ops.object.duplicate()
dup = bpy.context.view_layer.objects.active
dup.name = "BakedShapeKeyObject"

# 3. make sure there’s a Basis key
if not dup.data.shape_keys:
    dup.shape_key_add(name="Basis", from_mix=False)

# 4. frames you want to bake
frames = [1, 25, 50, 75, 100]

for f in frames:
    bpy.context.scene.frame_set(f)

    # bake ALL modifiers into a new relative Shape Key
    sk = dup.shape_key_add(name=f"Frame_{f}", from_mix=True)

    # keyframe ALL shape‐keys: set the new one to 1, the rest to 0
    for block in dup.data.shape_keys.key_blocks:
        block.value = 1.0 if block.name == sk.name else 0.0
        block.keyframe_insert(data_path="value", frame=f)

# 5. remove the GeoNodes modifier so only shape‐keys remain
if mod := dup.modifiers.get("GeometryNodes"):
    dup.modifiers.remove(mod)

print(" Done! Baked frames into shape keys on", dup.name)
