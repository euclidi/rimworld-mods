# Orcish Hordes — architecture decision record

Date: 2026-11-27. Status: recommended, not runtime-approved.

## Decision
Use Humanoid Alien Races (HAR) as a separately installed dependency if the diagnostic passes on Core-only 1.7. Prefer ordinary game XML and public APIs for systems outside race rendering. Do not fork or vendor HAR at present.

| Option | Benefits | Risks |
|---|---|---|
| HAR | Existing custom graphics, color channels, body addons, backstories, race restrictions and compatibility machinery | External dependency, runtime patch conflicts, 1.7 migration still needs verification |
| Native ThingDef with custom C# | Full control and fewer dependencies | More engine-specific rendering and generation patches; larger regression surface |
| Biotech xenotypes | Official genetic system | Disallowed: paid DLC |

Evidence: upstream [metadata](https://github.com/erdelf/AlienRaces/blob/master/About/About.xml) lists 1.7 and package ID erdelf.HumanoidAlienRaces; [repository](https://github.com/erdelf/AlienRaces) includes a 1.7 directory and MIT license. [Getting Started](https://github.com/erdelf/AlienRaces/wiki/Getting-Started) documents race and pawn kind definitions; [General Settings](https://github.com/erdelf/AlienRaces/wiki/General-Settings) describes skin channels and addons. The wiki examples predate 1.7; the probe is a hypothesis, not a verified implementation. [RimRef migration discussion](https://github.com/krafs/RimRef/discussions/108) confirms that 1.7 references use .NET 10 SDK and game-owned assemblies.

No external code or artwork has been bundled. Record the installed HAR version and source revision before accepting it. Do not imply that the MIT license of HAR grants reuse rights to third-party race mods.

## Proposed gameplay scope (not approved)
A true orc species rather than human xenotypes. Shared anatomy, distinct heads/tusks, body silhouettes, skin variation, adult warriors, civilians and specialists. Potential cultures: tribal raiders, settled strongholds, scrap-industrial clans, cave-dwelling groups. Cultures should have distinct pawn kinds, trade stock, equipment, settlement generation and diplomacy; species alone should not dictate personality or hostility. Captivity, ransom, rescue, injuries, rivalries, and recovery can integrate with vanilla storytelling. Use non-graphic mature storytelling; no sexualized minors or sexual assault mechanics. Confirm scope before implementing gameplay.

## Build map
- Race: HAR ThingDef_AlienRace, PawnKindDef; human anatomy fallback initially for diagnostic only.
- Art: custom directional heads and tusk silhouettes; test apparel overlap and skin tint before full body variants. No bulk generation before approved pilot.
- Faction: FactionDef, PawnGroupMaker, pawn kinds and backstories; verify actual 1.7 fields from local game XML.
- Equipment: ThingDefs, recipes, stock generation; use vanilla materials/technology where appropriate.
- Behavior: vanilla jobs and faction AI first; add narrowly scoped C# only for missing mechanics.
- Persistence: stable namespaced Def IDs; test save/load, death, recruitment, world pawn generation and caravans.
- No DLC symbols in unconditional XML or mandatory metadata.

## Acceptance
Core + HAR + HarRaceProbe: startup without red errors, correct species ID, green tint across directions, usable vanilla apparel, normal injury and surgery, recruitment, caravan and save/load. Then test full project against same installation. If the probe fails, diagnose the exact build and dependency before switching architecture. See TestLab/HAR-probe.md.
