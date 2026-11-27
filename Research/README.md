# Technical research and decisions

Research baseline: 2026-11-27. Links are upstream sources, not vendored code.

| Resource | Decision |
|---|---|
| [Ludeon Waylith announcement](https://ludeon.com/blog/2026/10/announcing-the-waylith-engine-and-update-1-7/) | Target 1.7 only. |
| [1.7 migration guide](https://rimworldwiki.com/wiki/Modding_Tutorials/RimWorld_1.7_Mod_Updates) | .NET 10; Harmony 3 for patches if needed; audit Unity compatibility stubs and use native API when justified. |
| [RimRef](https://github.com/krafs/RimRef) and [1.7.5014-unstable](https://www.nuget.org/packages/Krafs.Rimworld.Ref/1.7.5014-unstable) | Use exact reference package for reproducible development; provisional pin, not a claim of compatibility with user's build. |
| [RimRefLocal](https://github.com/krafs/RimRefLocal) | Option for local exact-build debugging. |
| [HAR metadata](https://github.com/erdelf/AlienRaces/blob/master/About/About.xml) and [load folders](https://github.com/erdelf/AlienRaces/blob/master/loadFolders.xml) | 1.7 support is declared upstream. Candidate for custom orcs; no dependency or copied code yet. Test with no DLC. |
| [Mod structure](https://rimworldwiki.com/wiki/Modding_Tutorials/Mod_folder_structure) and [About.xml](https://rimworldwiki.com/wiki/Modding_Tutorials/About.xml) | Standard directory and metadata conventions. |
| [Textures](https://rimworldwiki.com/wiki/Modding_Tutorials/Textures) | Directional textures and namespaced asset paths. |
| [RIMAPI](https://github.com/IlyaChichkov/RIMAPI), [Pickle](https://github.com/RimWorks/Rimworld-Pickle), [Quickstarts](https://github.com/RimWorks/Rimworld-Quickstarts) | Candidate runtime testing tools; 1.7 compatibility, licenses and security not yet audited. |

## API map
ThingDef/BodyDef/PawnKindDef/FactionDef for content and anatomy; HediffDef for conditions; JobDriver/ThinkTree/LordJob for behavior; IncidentWorker for events; ThoughtDef for mood; PawnRenderNode for rendering; Scribe for persistence. Confirm actual signatures and def schema in the pinned build before use.

## Dependency gate
Record upstream release/commit, package ID, license, transitive requirements, compatibility test result, source URLs and attribution. Do not bundle proprietary game binaries. No paid DLC requirements; optional DLC integration must be guarded and tested with DLC absent. No dependency is accepted on metadata alone.

## Open decisions
Orc species and factions: HAR versus native implementation; art pilot; approved culture and scope. No gameplay implementation yet. Runtime test host and exact installed build remain unknown.
