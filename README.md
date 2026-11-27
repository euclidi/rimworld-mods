# Euclidi RimWorld Mods

Development workspace for independent RimWorld 1.7 (Waylith) mods. Base game only; no paid DLC required. The exact installed game build is not yet known.

- [Research](Research/README.md): technical sources and decisions.
- [SDK](SDK/Directory.Build.props): pinned compilation defaults.
- [Mods](Mods/README.md): installable projects.
- [AssetLab](AssetLab/README.md): art and licensing standards.
- [TestLab](TestLab/README.md): runtime testing protocol.
- [Tools](Tools/pipeline.py): static validator and packager.

## Local development

Requires Python 3.11+ and .NET 10 SDK for compiled mods.

    python -m unittest discover -s Tools/tests
    dotnet build Mods/DevelopmentProbe/Source/DevelopmentProbe.csproj -c Release
    python Tools/pipeline.py check
    python Tools/pipeline.py package

Output: dist/*.zip. Extract the mod directory into RimWorld/Mods. DevelopmentProbe is a diagnostic mod only; not a gameplay release.

Do not commit game binaries, third-party assets without permission, or untested compatibility claims. Keep each mod independently installable unless an audited dependency is necessary. Scope and technology approval precede gameplay implementation; complete agreed scope before playtesting and iterative improvement.
