# HD verification status

The ROM defines 493 unit records and 1,804 weapon records, including enemy, transformation and statistics variants. These counts are not unique mechanical designs.

- Named primary-part audit: no unmapped primary rectangles; 474 forecast definitions have been exercised through native game rendering. Attack poses are outside this forecast check.
- Added 219 primary-part links (103 exact reused fragments and 116 painted fragments). Original approved bindings and the ROM remain unchanged.
- Added 117 pilot/background cut-in resources; registration and alpha validation pass for all 117. All artwork is loaded lazily.
- Native replay confirmed cut-in IDs 6, 7, 75, 90 and 107 in the corresponding Duo, Quatre, Bonta, Getter-fixture and GoLion scenes. Getter fixture naming is historical; replay evidence names the observed pilot.
- Latest scene replay also covers actual Vulcan and Eid firing, and Sandrock/Deathscythe forecast scenes. This is limited replay coverage, not every weapon.
- Numeric checks cover normal, red and yellow forecast/battle digits. Portrait matching and frame-protection regression pass.
- Full weapon-by-weapon campaign verification, remaining mechanical BG close-ups, and unresolved palette/contour cases are still pending. Do not describe this build as fully verified.

Source code was reorganized into emulator/, scripts/, research/legacy/ and docs/. docs/source_moves.json lists the moves; scripts/verify/verify_repository_layout.py validates paths, imports, source bundle contents, protected ROM and approved artwork. ROMs and saves are excluded from Git and distribution.

## Expanded energy feedback

Feedback runs in the emulator; the ROM is read-only. Native OBJ/VRAM palettes and BG texture maps are sampled, independently of HD artwork and audio. The current build still restricts feedback to the exact supported ROM hash; audio/BGM variants need separate compatibility validation.

The detector now covers changing translucent round OBJ energy, dense changing BG energy, and native brightening flashes. Static textures, camera scrolling alone, unused palette colors and opaque armor are negative cases. Rumble stops outside battle and on pause.

Plasma Excurtion (weapon 1612) was replayed in an isolated native state with diagnostic firing requirements relaxed; animation identity was unchanged. HD off/on event timelines match: 43 BG-energy/flash pulses and 5 beam pulses. This confirms detection during that animation, not canonical campaign availability or subjective physical motor strength. Eid and Bonta timelines also match across HD modes. The latest per-scene detector timings are recorded in test_current/combat/energy_rumble_verification.json.

The new named-attack harness routed the first weapons of Wing Zero, Deathscythe, Heavyarms, Sandrock and Altron through native battle menus successfully. It substitutes the unit in an isolated state and selects canonical pilot IDs decoded from the ROM. Uninitialized pilot statistics are synthesized from the fixture and explicitly flagged; this does not certify campaign legality. Full weapon coverage remains incomplete. Native weapon menu order is now read from RAM, because it can differ from ROM record order or omit unavailable combination attacks. Every replay separately checks the weapon actually used.

## Mechanical BG artwork

45 additional reviewed mechanical close-up/weapon/BG resources are painted and registered in graphics/mechanical_cutins. All 45 pass the unchanged alpha-overlap threshold of 0.82; two cells use documented atlas-coordinate registration without imposing the original pixel mask. Registration is not actual gameplay verification. Corrupt/unclassified decodes remain outside this completed artwork scope.

## Separate mini-unit image bank (2026-11-10)

The unit graphics record has a second IMG pointer at offset +4. This bank was missing from the painted tile catalog, even when the primary animation parts were connected. All 322 distinct named secondary IMG resources are now registered. 296 reuse the corresponding assembled painted pose after silhouette validation; 26 use distinct reviewed paintings. The offline overlap threshold remains 0.82. Registration only translates/resamples the painted contour and never stamps the native pixel alpha onto it.

`scripts/verify/verify_secondary_unit_catalog.py` verifies all 322 resources through the production exact-tile compositor. Every resource assembles successfully and retains its offline registered contour. Artwork is at most 960 pixels on the longest axis. This verifies texel/binding coverage, not every campaign appearance on both displays. Native saved-state checks also exercise actual secondary OAM rendering in status, forecast and map screens.

## Shared Mazinger-family weapon frames

IMG 20713..20749 contains the shared flying fist, spinning wrist, smoke and launch fragments. All 37 records are accounted for: 36 nonempty frames assemble from exact painted texels and one record is intentionally empty. Some frames reuse exact matching painted tiles from another frame rather than accepting an inaccurate generated picture. The live punch material palette is recorded separately from the archive's template palette. Production recoloring still follows each native palette change.

`scripts/verify/verify_shared_weapon_frames.py` checks the complete sequence. Mazinger Z's available attacks are also replayed through native menus; unavailable attacks are retained as unverified cases. Generated canvases and palette provenance are in `graphics/shared_weapon_frames/`.

## Native attack audit limits

The crash-isolated audit attempted 1,804 weapon records across 473 unit records. After longer replays, 1,499 correctly selected attacks completed. Another 229 weapons were absent from the fixture's native menu, 73 did not enter the tracked battle state, and three unit-423 (スキエンティア) cases did not complete even after 9,000 simulated frames. Combination/story/formation legality has not been certified. These failures must not be presented as HD-verified attacks. MAP attacks need a separate on-map replay check; lack of entry into a normal battle is not proof of a missing animation.

The audit also captures native effect textures that are still outside the painted tile library. This includes energy, smoke and other effects; it is not a count of missing robots. Full campaign weapon/cut-in/contour verification remains incomplete. The user has revoked the earlier shutdown request: keep the computer on even after completion.

Completed asynchronous textures now enter the stage cache even when no unknown OBJ remains in the next frame. Previously this early return could leave a finished request permanently marked as pending after scene changes. `verify_texture_completion.py` covers successful and unpainted completions without a visible source OBJ. The nine-scene warmed replay passes after this fix.
