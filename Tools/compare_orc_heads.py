"""Make a private, approximate pixel-aligned overlay comparison from an owned Waylith install.

Requires .NET 10, Pillow, and a tar executable supporting the game's Assets.zip.
The output contains game art: never commit or distribute it.
"""
import argparse
import io
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--game", type=Path, required=True)
    p.add_argument("--dotnet", default="dotnet")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    game = args.game.resolve()
    if args.output.resolve().is_relative_to(ROOT):
        p.error("Output must be outside the repository: it contains game art")
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        project = ROOT / "Tools/WaylithJoin/WaylithJoin.csproj"
        subprocess.run([args.dotnet, "build", str(project), "-c", "Release", f"-p:RimWorldDir={game}", "-o", str(tmp / "build")], check=True)
        sheet = Image.new("RGBA", (4 * 128, 2 * 150), (44, 44, 44, 255))
        draw = ImageDraw.Draw(sheet)
        for row, sex in enumerate(("Male", "Female")):
            for col, direction in enumerate(("south", "east", "north", "west")):
                source_dir = "east" if direction == "west" else direction
                member = f"Resources/Textures/Things/Pawn/Humanlike/Heads/{sex}/{sex}_Average_Normal_{source_dir}.png.dds.split"
                split = tmp / "input.split"
                split.write_bytes(subprocess.check_output(["tar", "-xOf", str(game / "Assets.zip"), member]))
                dds = tmp / "head.dds"
                subprocess.run([args.dotnet, str(tmp / "build/WaylithJoin.dll"), str(split), str(dds)], check=True)
                head = Image.open(dds).convert("RGBA")
                if direction == "west": head = head.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                tusks = Image.open(ROOT / f"Mods/OrcishHordes/Textures/Euclidi/Orcs/Tusks_{direction}.png").convert("RGBA")
                if head.size != tusks.size: raise ValueError(f"Size mismatch: {member}")
                head.alpha_composite(tusks)
                sheet.alpha_composite(head, (col * 128, row * 150 + 20))
                draw.text((col * 128 + 4, row * 150 + 4), f"{sex} {direction}", fill="white")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        sheet.convert("RGB").save(args.output)
        print(f"Private comparison written to {args.output}; do not redistribute.")

if __name__ == "__main__": main()
