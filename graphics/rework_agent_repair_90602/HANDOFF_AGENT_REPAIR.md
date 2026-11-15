# Sandrock source and head repair candidate

CORRECTION: `candidate_packet.json` is the only current packet. It uses `head_candidate_preserved_alpha_4x.png`, resampled directly from untouched `head_generated.png` with no alpha thresholds, morphology, native alpha transfer or recoloring; only zero-alpha RGB cleanup. `preserved_alpha_proof.json` records this. The previous `head_candidate_4x.png`, `head_generated_alpha_clean.png`, `head_candidate_packet.json` and `head_alpha_cleanup.json` are WITHDRAWN diagnostic drafts and must not be installed. They are preserved separately, as recorded in `WITHDRAWN_THRESHOLD_DRAFT.json`. The later user-constraint clarification invalidates the threshold operation described below.

The source of truth is `docs/HANDOFF_TO_CODEX_6.md`, which supersedes the closed 5 file. Claude verified pure-HD-off head colors at state-relative +2/+30/+60/+90: red crest, dark purple panels, yellow horns, purple body are intentional. This resolves the earlier warning against accepting the palette solely from a filename containing native.

## Actual new art

`head_candidate_preserved_alpha_4x.png` is a new smooth head-tile candidate from built-in imagegen, native32x32 ->128x128. `head_generated.png` preserves the full original generated RGBA. The current drawing is spatially resized directly from that untouched generation, with zero-alpha RGB cleanup only. No existing source art was overwritten. `PROMPT.md` records the exact generation instructions and the observed limitation that the generator also simplified lower-face rendering. This is a whole head-tile candidate requiring body-context inspection, not an approved surgical crest-only patch.

The three columns of `head_before_after_reference.png` are native / current HD / generated candidate. The stepped upper red crest is now smoothly outlined. This visual comparison does not establish runtime registration or dynamic palette correctness.

`candidate_packet.json` contains four final role hashes, relative filenames, bindings[90602], the prior map and nested=true. `head_install_contract.json` contains one installer row with replace_binding90602, atlas_box[0,0,32,32] and the full source contract. Current binding: library zero-based index90601, core one-based id90602. It is currently `sandrock_cached_pose` x208 y88 w32 h32. Its prior spec SHA is `32e3c29f98f4ce5b73253a384ec3c122e3e1034c2d718948e9361023b32fc408`.

Source state: `test_current/parts/borrowed_shape_rework/source_mechanical_3_15/source_pose.state`, relative frame0, epoch557, engine0 OAM9. Actual RGB hash1614348685, index hash2140177243, unpacked raw1024 bytes SHA `6f756d296c67559a836a74104a89a1be1e8b0e2bc174fa90a57170db88aeb349`. Raw and all16 RGB/15-bit palette entries are preserved in `head_source_contract.json` / `head_raw_indices.bin`. The same index appears in other bindings with different palettes; do not replace every indexed match with this exact RGB tile.

## Shield source localized, palette not yet accepted

The screenshot's oval shield and lower split jaws geometrically match IMG7242 body x192 y0 32x32, adjoining lower-jaw source x224 y0 32x32, represented in `full_attack_044` at x460 y6 and x492 y6. The intermediate crop x208 y0 also exists. Library indices38080/38082/38083 are structural candidates, not a list of confirmed runtime defense dependencies. They carry a red/gray template palette which must not be accepted as the actual defense palette. Recoloring them with the confirmed head palette produces incorrect green/red areas, so those exploratory `shield_probe_*` images are explicitly rejected diagnostic probes.

`shield_structural_source_reference.png` uses the original template palette and labels the three crop rectangles. `shield_source_hypothesis.json` preserves raw index hashes, full specs and their prior hashes. Claude still needs the defense state/frame, actual cached full16 palette, OAM attrs/orientation/screen positions and MMU/ROM comparison. Do not install this hypothesis or treat screenshot purple as approved paint.

## Remaining reported work

The attack screenshots show different head poses, uncovered chest/legs, swords and rear body. The two held states3_14/3_15 at relative0 are scarf/default poses, not those exact attack/defense frames. `current_default_pose_dependencies.json` snapshots every bank0 dependency with full raw/index/palette and current binding hashes for both default poses. It does not claim they cover the reported attack/rear/shield frames.

No sword/chest/legs/rear/shield repaint is claimed complete. Exact state/frame contracts for those screenshot poses remain necessary before an honest whole-pose redraw. Existing flash-derived weapon cache is not silently promoted to a trustworthy native contract. Root should carry these open items into the shared handoff. Claude owns connecting, baking and runtime QA; this agent changed no runtime, core, central library, DB, install manifest, queue or shared handoff.
