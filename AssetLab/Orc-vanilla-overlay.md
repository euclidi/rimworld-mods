# Orc visual pilot: reference and verification record

The preserved overlays are original art; no game textures are distributed. Local game: RimWorld Waylith 1.7.5021 rev1365; local `Waylith.dll` SHA-256 `c412b83a658dd46bf32ccb894f4e83e9d3c00bfd2aab91f91853faafada6fc00`. The compiled diagnostic uses `Krafs.Rimworld.Ref` **1.7.5014-unstable**, nupkg SHA-256 `7709fd10e646c82f269ec8d016b879f5ff1772d4473d7f263421e688af6ab76e`; this is not an exact reference match to the installed game.

HAR source audited: https://github.com/erdelf/AlienRaces/tree/b715c63ea7179bd2f9b9cedcdb39233c2bb36ef0, commit `b715c63ea7179bd2f9b9cedcdb39233c2bb36ef0` (2026-10-15). No installed HAR was found, so this is a source audit, not proof that a particular released binary matches or loads in 1.7.5021. Upstream metadata identifies `erdelf.HumanoidAlienRaces`, lists 1.7, and has no mandatory dependency; the mod metadata declares HAR and load-after.

Core XML confirms `Human`, `BasePlayerPawnKind`, and the average head def names. HAR's 1.7 Human patch supplies five adult body types and twelve vanilla head types. The previous explicit `headTypes` override limited the pilot to two; removing it preserves the inherited choices. `ColorChannelGenerator` accepts `first`/`second`; the base channel initializes white. `BodyAddon` supports `alignWithHead`, `defaultOffset`, `drawSize`, `colorChannel`, and the named BodyPart/Apparel conditions; those conditions check the jaw and FullHead apparel. The render node parents to Head and its transform adds directional offsets, changes north layering, and defaults `scaleWithPawnDrawsize` to false with a 1.5 multiplier. An equal-pixel composite does not establish that those runtime transforms coincide with the head mesh. West flipping and helmet, jaw and portrait behavior must be checked in game.

## Local reference comparison

Install Pillow, .NET 10 SDK and a `tar` supporting Assets.zip. Example (PowerShell):

```powershell
python -m pip install Pillow
python Tools/compare_orc_heads.py --game 'D:\Program Files (x86)\Steam\steamapps\common\RimWorld' --dotnet 'C:\Users\jvriv\AppData\Local\RimMed\dotnet\dotnet.exe' --output "$env:TEMP\orc-comparison.png"
```

The tool invokes the installed game's `Waylith.dll` to join its split DDS streams and makes a **private** 128-pixel-per-cell composite outside the repository. Do not upload or redistribute it. The inspected average male/female south, east, north and mirrored west images place the original south tusks at the jaw edges, the east/west tusk near the face, and north is transparent. The result is an image-space comparison only: no tint, hair, apparel, render-tree scaling, actual game resolution or placement is simulated. Other inherited head shapes have not been individually registered; do not infer verified alignment. The south and side overlays were revised into slimmer, softly shaded tusks after inspecting the composite; runtime scale and alignment still require verification.

## Requirement map and outstanding work

- REQ-01: Source/package audit above; exact installed HAR binary match and runtime compatibility remain open.
- REQ-02: Local official images decoded and private composite generated using `Tools/compare_orc_heads.py`; output is excluded from this repository.
- REQ-03: `Defs/Races/Orc.xml` restores inherited heads, bodies, and hair and retains the original green channel and original tusks. Alignment for all head types and actual runtime remains unverified.
- REQ-04: `Tools/pipeline.py`, its unit tests, `DevelopmentProbe.csproj`, and ZIP checks are the offline pipeline; see PR for observed results and CI. Core + HAR runtime tests remain pending.
- REQ-05: This remains a visual pilot, not faction or gameplay implementation. Use `TestLab/Orc-visual.md` for a disposable-colony test.

