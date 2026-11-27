"""Static checks and install-layout ZIPs. Does not validate RimWorld runtime semantics."""
from pathlib import Path
import argparse
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIRS = {"About", "Assemblies", "Defs", "Patches", "Textures", "Sounds", "Languages", "Materials", "Shaders", "Common", "1.7"}
RUNTIME_FILES = {"LoadFolders.xml", "loadFolders.xml"}
DLC = {"royalty", "ideology", "biotech", "anomaly", "odyssey"}

def mods(root):
    return sorted(p for p in (root / "Mods").iterdir() if p.is_dir() and (p / "About" / "About.xml").is_file())

def check(root=ROOT, require_assemblies=True):
    errors, ids = [], set()
    found = mods(root)
    if not found:
        errors.append("No mods found")
    for mod in found:
        parsed = {}
        for path in mod.rglob("*.xml"):
            if any(part in {"Source", "obj", "bin"} for part in path.relative_to(mod).parts):
                continue
            try:
                parsed[path] = ET.parse(path).getroot()
            except ET.ParseError as exc:
                errors.append(f"{path}: {exc}")
        meta = parsed.get(mod / "About" / "About.xml")
        if meta is not None:
            if meta.tag != "ModMetaData":
                errors.append(f"{mod.name}: invalid metadata root")
            for field in ("name", "author", "packageId", "description"):
                if not (meta.findtext(field) or "").strip():
                    errors.append(f"{mod.name}: missing {field}")
            pid = (meta.findtext("packageId") or "").strip().lower()
            if not re.fullmatch(r"euclidi\.[a-z0-9_.-]+", pid) or pid in ids:
                errors.append(f"{mod.name}: invalid or duplicate package ID {pid}")
            ids.add(pid)
            if [(x.text or "").strip() for x in meta.findall("supportedVersions/li")] != ["1.7"]:
                errors.append(f"{mod.name}: expected 1.7 only")
            for dependency in meta.findall(".//modDependencies/li/packageId") + meta.findall(".//modDependenciesByVersion//packageId"):
                value = (dependency.text or "").strip().lower()
                if value.startswith("ludeon.rimworld.") and value.rsplit(".", 1)[-1] in DLC:
                    errors.append(f"{mod.name}: mandatory paid DLC {value}")
        seen = set()
        for path, doc in parsed.items():
            if doc.tag != "Defs":
                continue
            for node in doc:
                name = node.findtext("defName")
                if name:
                    key = (node.tag, name.strip())
                    if key in seen:
                        errors.append(f"{mod.name}: repeated literal Def {key}")
                    seen.add(key)
        if require_assemblies and list((mod / "Source").rglob("*.csproj")) and not list((mod / "Assemblies").glob("*.dll")):
            errors.append(f"{mod.name}: compile before packaging")
        for path in mod.rglob("*"):
            if path.is_symlink():
                errors.append(f"{path}: symlinks not permitted")
    return errors

def package(root=ROOT):
    errors = check(root)
    if errors:
        raise ValueError("\n".join(errors))
    out = root / "dist"
    out.mkdir(exist_ok=True)
    for mod in mods(root):
        target = out / f"{mod.name}-1.7.zip"
        with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(mod.rglob("*")):
                rel = path.relative_to(mod)
                if not path.is_file() or path.is_symlink():
                    continue
                if rel.parts[0] not in RUNTIME_DIRS and str(rel) not in RUNTIME_FILES:
                    continue
                if path.suffix.lower() in {".pdb", ".cs", ".csproj"}:
                    continue
                if path.name in {"Assembly-CSharp.dll", "Waylith.dll", "0Harmony.dll"} or path.name.startswith(("UnityEngine", "System.")):
                    raise ValueError(f"Unexpected runtime dependency: {path}")
                archive.write(path, (Path(mod.name) / rel).as_posix())
        print(target)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["check", "package"])
    parser.add_argument("--source-only", action="store_true", help="Allow uncompiled projects for check only")
    args = parser.parse_args()
    if args.command == "package":
        try:
            package()
        except ValueError as exc:
            print(exc, file=sys.stderr)
            return 1
        return 0
    errors = check(require_assemblies=not args.source_only)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Static checks passed (runtime not tested).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
