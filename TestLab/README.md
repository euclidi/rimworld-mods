# Runtime validation protocol

Static validation is not in-game validation. Record game version/build, OS, enabled mods and DLCs, commit SHA, test case, result and log evidence.

1. Compile with pinned reference package; match it to installed game build before compatibility claims.
2. Extract DevelopmentProbe into Mods. Enable Core and probe only, no DLC. Start game; confirm mod constructor log, no errors.
3. Start a new colony; save, reload, advance simulation and inspect logs.
4. For race mods: test world generation, pawn spawning, all directions, clothing, equipment, injuries, recruitment, caravans, combat, save/reload and removal policy.
5. For framework dependencies: repeat Core + dependency + mod, with DLCs absent. Test performance and conflicts separately.
6. Archive relevant redacted log excerpts and report failures. Release only after static checks, compilation and required runtime tests pass.

Runtime status: NOT RUN. No accessible installed RimWorld runtime has been established.
