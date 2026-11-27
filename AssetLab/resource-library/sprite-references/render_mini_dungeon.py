"""Render transparent, fixed-framing Mini Dungeon sprite references in Blender."""

import argparse
import hashlib
import json
import sys
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

import bpy
from mathutils import Vector


DIRECTIONS = {"south": (0, -1), "east": (-1, 0), "north": (0, 1)}
MODELS = {
    "character-human": {"idle": 1, "walk": 8, "sprint": 8},
    "character-orc": {"idle": 1, "walk": 8, "sprint": 8},
    "shield-round": {"static": 1},
    "weapon-spear": {"static": 1},
    "weapon-sword": {"static": 1},
}


def evaluated_points():
    graph = bpy.context.evaluated_depsgraph_get()
    return [
        evaluated.matrix_world @ vertex.co
        for obj in bpy.context.scene.objects
        if obj.type == "MESH"
        for evaluated in (obj.evaluated_get(graph),)
        for vertex in evaluated.data.vertices
    ]


def start_scene(source):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(source))
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.display.shading.light = "STUDIO"
    scene.display.shading.color_type = "TEXTURE"
    scene.display.shading.show_shadows = False
    scene.display.shading.show_cavity = True
    scene.display.shading.cavity_type = "WORLD"
    scene.render.film_transparent = True
    scene.render.resolution_x = scene.render.resolution_y = 160
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.view_settings.view_transform = "Standard"
    camera = bpy.data.objects.new("Orthographic camera", bpy.data.cameras.new("Orthographic camera"))
    scene.collection.objects.link(camera)
    camera.data.type = "ORTHO"
    scene.camera = camera
    return scene, camera


def render_model(source, clips, output):
    scene, camera = start_scene(source)
    armature = next((obj for obj in scene.objects if obj.type == "ARMATURE"), None)
    actions = {}
    if armature:
        animation = armature.animation_data_create()
        for track in animation.nla_tracks:
            actions[track.name] = track.strips[0].action
            track.mute = True
        animation.action = actions["idle"]
        scene.frame_set(int(animation.action.frame_range[0]))
    points = evaluated_points()
    lower = Vector(tuple(min(point[i] for point in points) for i in range(3)))
    upper = Vector(tuple(max(point[i] for point in points) for i in range(3)))
    target = (lower + upper) / 2
    if armature:
        # Keep the same target and scale for both characters and every clip.
        target.x = target.y = 0.0
        target.z = 0.44
        camera.data.ortho_scale = 1.08
    else:
        camera.data.ortho_scale = (upper - lower).length * 1.22

    frames, timing = [], {}
    for clip, count in clips.items():
        if armature:
            animation.action = actions[clip]
            start, end = animation.action.frame_range
        else:
            start = end = 1
        rate = scene.render.fps / scene.render.fps_base
        timing[clip] = {
            "source_duration_seconds": round((end - start) / rate, 6),
            "samples_per_direction": count,
        }
        for direction, (x, y) in DIRECTIONS.items():
            camera.location = target + Vector((x * 5, y * 5, 3.5))
            camera.rotation_euler = (target - camera.location).to_track_quat("-Z", "Y").to_euler()
            for index in range(count):
                sample = start + (end - start) * index / count
                scene.frame_set(int(sample), subframe=sample % 1)
                relative = f"{source.stem}/{clip}/{direction}_{index:02d}.png"
                destination = output / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                scene.render.filepath = str(destination)
                bpy.ops.render.render(write_still=True)
                frames.append({"file": relative, "source_frame": round(sample, 4)})
    return frames, timing


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    options = parser.parse_args(sys.argv[sys.argv.index("--") + 1 :])
    options.output = options.output.resolve()
    folder = Path(__file__).resolve().parent
    source_folder = folder.parent / "foundations-3d" / "kenney-mini-dungeon"
    options.output.mkdir(parents=True, exist_ok=True)
    frame_folder = options.output / "frames"
    manifest = {"blender": bpy.app.version_string, "size_px": [160, 160], "models": {}}
    with ZipFile(options.output / "mini-dungeon-directional.zip", "w") as archive:
        for model, clips in MODELS.items():
            source = source_folder / f"{model}.glb"
            frames, timing = render_model(source, clips, frame_folder)
            manifest["models"][model] = {
                "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "timing": timing,
                "frames": frames,
            }
            for frame in frames:
                name = frame["file"]
                archive.writestr(ZipInfo(name), (frame_folder / name).read_bytes(), ZIP_DEFLATED)
    (options.output / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
