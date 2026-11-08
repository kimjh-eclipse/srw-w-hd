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
