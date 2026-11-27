# Issue 1 execution plan

1. REQ-01 — audit pinned `SDK/Directory.Build.props`, Core XML and HAR source; record build and provenance in `AssetLab/Orc-vanilla-overlay.md`.
2. REQ-02 — implement `Tools/WaylithJoin` and `Tools/compare_orc_heads.py`; inspect a local, private native-resolution composite. Never ship game art.
3. REQ-03 — retain inherited vanilla variants in `Mods/OrcishHordes/Defs/Races/Orc.xml` and test original directional overlays; retain provisional transform when source alone cannot establish visual alignment.
4. REQ-04 — run `python -m unittest discover -s Tools/tests`, .NET 10 `dotnet build Mods/DevelopmentProbe/Source/DevelopmentProbe.csproj -c Release`, `python Tools/pipeline.py check`, `python Tools/pipeline.py package`, and inspect ZIP contents; check GitHub Actions after push.
5. REQ-05 — submit a PR with evidence and explicit remaining runtime and visual gaps. No gameplay scope changes.
