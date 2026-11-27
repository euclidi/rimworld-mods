# HAR race diagnostic

Status: source only; not tested in game.

1. Record exact RimWorld 1.7 build, OS, HAR version and all enabled mods. Install HAR from its upstream distribution; check upstream prerequisites for the installed release. Disable all paid DLC.
2. Enable Core, required HAR prerequisites, HAR, then Euclidi HAR Race Probe. Start a new disposable colony with development mode enabled.
3. Inspect startup log for missing classes, unresolved references, XML inheritance errors, missing graphics, or patch errors.
4. Use Spawn Pawn to select race probe colonist (Euclidi_HARRaceProbeColonist). Spawn at least 12 pawns. Verify custom race identity and the green skin palette on heads and bodies. Check all directions and portraits.
5. Test apparel, beds, food, work, combat, injuries, vanilla surgery, recruitment, caravan travel, death/corpse, save and reload. Compare with normal humans; no stat changes are intended.
6. Record screenshots and log excerpts. A failed color channel is a graphics compatibility issue, not proof the race itself failed. Test with the palette temporarily removed only on a local diagnostic copy.
7. Discard the test save before removing the mod. Do not mix with a production save.

Pass condition: no relevant game errors and all intended tests pass. This is not a playable orc release. No custom artwork, factions or gameplay are included.
