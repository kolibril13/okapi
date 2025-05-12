import bpy
from bpy.props import IntProperty, PointerProperty, BoolProperty


# ─── PANEL ────────────────────────────────────────────────────────────────────
class GEO_PT_GeoNodesToShapeKey(bpy.types.Panel):
    bl_label = "GN to SKey"
    bl_idname = "GEO_PT_geonodes_to_shapekey"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "GeoNodes"

    def draw(self, context):
        layout = self.layout
        props = context.scene.geonodes_to_shapekey_props

        layout.prop(props, "selected_object")
        layout.prop(props, "total_frames")

        layout.operator("object.geonodes_prep", text="Prep Copies")
        layout.separator()
        layout.operator("object.merge_to_shapekeys", text="Merge to ShapeKeys")
        layout.prop(props, "use_relative")
        layout.separator()
        layout.operator("object.rename_and_delete", text="Rename and Delete")


# ─── PREP OPERATOR ────────────────────────────────────────────────────────────
class GEO_OT_GeoNodesPrep(bpy.types.Operator):
    bl_idname = "object.geonodes_prep"
    bl_label = "Prepare GeoNodes Copies"
    bl_description = "Duplicate object at key frames, apply GeoNodes, and offset in Y"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.geonodes_to_shapekey_props
        base_obj = props.selected_object
        total = props.total_frames
        scene = context.scene

        if not base_obj:
            self.report({"ERROR"}, "No object selected.")
            return {"CANCELLED"}

        geo_mod = next((m for m in base_obj.modifiers if m.type == "NODES"), None)
        if not geo_mod:
            self.report({"ERROR"}, "Selected object has no Geometry Nodes modifier.")
            return {"CANCELLED"}

        if context.mode != "OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")

        original_active = context.view_layer.objects.active

        for i in range(total):
            frame = i * 10
            scene.frame_set(frame)

            bpy.ops.object.select_all(action="DESELECT")
            base_obj.select_set(True)
            context.view_layer.objects.active = base_obj

            bpy.ops.object.duplicate()
            copy = context.view_layer.objects.active
            copy.name = f"copy{i+1}"
            copy.location.y += 2 * (i + 1)

            try:
                bpy.ops.object.modifier_apply(modifier=geo_mod.name)
            except RuntimeError as e:
                self.report(
                    {"WARNING"}, f"Could not apply modifier on {copy.name}: {e}"
                )

        # Restore selection
        bpy.ops.object.select_all(action="DESELECT")
        if original_active:
            original_active.select_set(True)
            context.view_layer.objects.active = original_active

        self.report({"INFO"}, f"Prepared {total} copies, each offset in Y.")
        return {"FINISHED"}


# ─── MERGE OPERATOR ───────────────────────────────────────────────────────────
class GEO_OT_MergeToShapeKeys(bpy.types.Operator):
    bl_idname = "object.merge_to_shapekeys"
    bl_label = "Merge to ShapeKeys"
    bl_description = (
        "On copy1: add Basis, join copy2…copyN as shape-keys, "
        "disable relative mode, and keyframe eval_time"
    )
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        # Ensure Object mode
        if context.mode != "OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")

        props = context.scene.geonodes_to_shapekey_props
        scene = context.scene
        use_relative = props.use_relative

        # Collect and sort all copyN objects
        copies = [o for o in scene.objects if o.name.startswith("copy")]
        if len(copies) < 2:
            self.report({"ERROR"}, "Need at least copy1 and copy2 present.")
            return {"CANCELLED"}

        def idx(o):
            try:
                return int(o.name.replace("copy", ""))
            except:
                return 0

        copies.sort(key=idx)

        copy1 = copies[0]
        rest = copies[1:]

        # Select copy1 and make active
        bpy.ops.object.select_all(action="DESELECT")
        copy1.select_set(True)
        context.view_layer.objects.active = copy1

        # 1) Add Basis shape key
        bpy.ops.object.shape_key_add(from_mix=False)

        # 2) Join each other copy as its own shape key
        for o in rest:
            o.select_set(True)
            bpy.ops.object.join_shapes()
            o.select_set(False)

        # 3) Configure shape keys based on mode
        sk_block = copy1.data.shape_keys
        if not use_relative:
            sk_block.use_relative = False

            # 4) Animate eval_time from 0 → (num_copies−1)*10 over frames [1…(num_copies−1)*24]
            start_frame = 1
            end_frame = (len(copies) - 1) * 24

            # Ensure we have animation data
            if not sk_block.animation_data:
                sk_block.animation_data_create()

            sk_block.eval_time = 0
            sk_block.keyframe_insert(data_path="eval_time", frame=start_frame)

            sk_block.eval_time = (len(copies) - 1) * 10
            sk_block.keyframe_insert(data_path="eval_time", frame=end_frame)

            # Force linear interpolation on the eval_time fcurve
            action = sk_block.animation_data.action
            for fcu in action.fcurves:
                if fcu.data_path == "eval_time":
                    for kp in fcu.keyframe_points:
                        kp.interpolation = "LINEAR"

            self.report(
                {"INFO"},
                f"Merged {len(rest)} copies into '{copy1.name}', "
                f"eval_time keyed @ {start_frame} → {end_frame}",
            )
        else:
            # For relative mode, keyframe each shape key value
            # Ensure we have animation data
            if not sk_block.animation_data:
                sk_block.animation_data_create()

            # Get all shape keys except the basis
            shape_keys = [
                sk for sk in copy1.data.shape_keys.key_blocks if sk.name != "Basis"
            ]

        step = 10  # half-width of each triangle
        for i, sk in enumerate(shape_keys):
            # for key i:
            start = i * step  #     0, 10, 20, ...
            peak = start + step  #    10, 20, 30, ...
            end = start + 2 * step  #    20, 30, 40, ...

            # insert 0 → 1 → 0 (or 0 → 1 for last shape key)
            sk.value = 0
            sk.keyframe_insert("value", frame=start)

            sk.value = 1
            sk.keyframe_insert("value", frame=peak)

            # Only insert the end keyframe if this is not the last shape key
            if i < len(shape_keys) - 1:
                sk.value = 0
                sk.keyframe_insert("value", frame=end)

            # Force linear interpolation on all shape key value fcurves
            action = sk_block.animation_data.action
            for fcu in action.fcurves:
                if fcu.data_path.startswith("key_blocks[") and fcu.data_path.endswith(
                    "].value"
                ):
                    for kp in fcu.keyframe_points:
                        kp.interpolation = "LINEAR"

            self.report(
                {"INFO"},
                f"Merged {len(rest)} copies into '{copy1.name}' with relative shape keys",
            )
        return {"FINISHED"}


# ─── RENAME & DELETE OPERATOR ─────────────────────────────────────────────────
class GEO_OT_RenameAndDelete(bpy.types.Operator):
    bl_idname = "object.rename_and_delete"
    bl_label = "Rename and Delete"
    bl_description = "Rename 'copy1' to 'shapekey_object' and delete all other copies"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        # Find all copyN objects
        copies = [o for o in scene.objects if o.name.startswith("copy")]

        if not copies:
            self.report({"ERROR"}, "No objects named 'copy1', 'copy2', etc. found.")
            return {"CANCELLED"}

        # Sort so we get copy1 first
        def idx(o):
            try:
                return int(o.name.replace("copy", ""))
            except:
                return 0

        copies.sort(key=idx)

        copy1 = copies[0]
        other_copies = copies[1:]

        # Rename copy1
        old_name = copy1.name
        copy1.name = "shapekey_object"

        # Delete all others
        for obj in other_copies:
            bpy.data.objects.remove(obj, do_unlink=True)

        self.report(
            {"INFO"},
            f"Renamed '{old_name}' → 'shapekey_object', deleted {len(other_copies)} copies.",
        )
        return {"FINISHED"}


# ─── PROPS & REGISTER ─────────────────────────────────────────────────────────
class GEO_Props(bpy.types.PropertyGroup):
    total_frames: IntProperty(
        name="Frames",
        description="Number of timed duplicates to make",
        default=4,
        min=1,
    )
    selected_object: PointerProperty(
        name="Object",
        description="Select the GeoNodes-enabled object",
        type=bpy.types.Object,
    )
    use_relative: BoolProperty(
        name="Relative",
        description="Use relative shape keys instead of absolute",
        default=True,
    )


classes = (
    GEO_Props,
    GEO_OT_GeoNodesPrep,
    GEO_OT_MergeToShapeKeys,
    GEO_OT_RenameAndDelete,
    GEO_PT_GeoNodesToShapeKey,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.geonodes_to_shapekey_props = bpy.props.PointerProperty(
        type=GEO_Props
    )


def unregister():
    del bpy.types.Scene.geonodes_to_shapekey_props
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
