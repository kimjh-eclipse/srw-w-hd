# Deathscythe expanded source repair candidate

Use expanded_candidate_packet.json. Earlier limited_candidate_packet.json/61-ID output is superseded. Producer source and visual checks PASS; independent Claude visual QA, connection, bake and actual runtime replay are still PENDING.

## Final scope and result

342 active bindings are covered:
-310 full-palette AND raw-index-exact children/parents from IMG1164 [0,0,128,32].
-30 full-palette AND raw-index-exact children/parents from IMG7086 [0,0,128,64].
-Front lower-right component23041 IMG7112 [72,112,32,32] and opposite foot22426 IMG7106 [128,16,32,16]. Crossing sibling coordinates for these two DO NOT have simultaneous full-palette/raw-index proof, so they remain separate rather than being merged by names or coordinates.

This includes primary front abdomen89484 IMG1164[40,0,32,32], normal abdomen37474 IMG7086[32,0,32,32], normal feet37475 IMG7086[64,0,32,32] and37487 IMG7086[96,16,32,16], all exact matching contained children and the matching broad parents that previously remained uncorrected. IMG7086 cells5/6 are scythe shaft/energy and were not guessed to be legs.

The two IMG7086 left/right64x64 masters were expanded into ONE128x64 source master because the curved shoulder/arm island [58,37..80,62] crosses x64. All cuts across that surface now sample the exact same generated RGBA. Native source component bounding-box inspection confirmed the nearby diagonal panel [38,36..56,53] is a separate island with a two-pixel gap, so geometric rectangle packing does not split a shared painted surface. Its detached tiny six-pixel native island near[53,48..56,51] was explicitly regenerated with the main panel and preserved.

## Drawing provenance

Built-in imagegen was used for all new raster art. Inputs were original raw-index/full-palette decoded source layouts plus existing HD style references. No assembled full robot was masked into a texture. Full source-layout generations retained separated canonical head/torso/arm/foot/joint/polygon islands. The normal torso/feet use better prior OWN generated same-source materials, packed as complete source islands into that one final128x64 master. Original generated materials, selected region coordinates and SHA-256 values are in parent_masters/selected_own_materials.json and generation_manifest.json.

Both eyes in the IMG1164 head were restored to GREEN through targeted imagegen edits. Source-layout attempts that introduced red eyes or simplified away the normal waist were rejected. No code recoloring was performed.

Only own-generated RGBA rectangle crops, LANCZOS scale and translation were used for final packing. There is NO native alpha/RGB transfer, source stencil, threshold deletion, color remap, morphology or seam-blending operation. Initial BICUBIC affine downsampling caused avoidable aliasing; final registration uses properly antialiased LANCZOS geometric resizing. Diagnostic alpha thresholds used for measuring IoU do not alter any output pixels.

## Validation and review

expanded_producer_checks.json records342 verified original RGB/index/full-palette/native-alpha contracts and8580 shared-source RGBA overlap checks, all byte-exact. All342 prior binding spec SHAs still matched at handoff. Primary diagnostic IoUs:23041 .906;22426 .721;89484 .846;37474 .924;37475 .830;37487 .796. Broader parent IoUs .780–.876. These are shape diagnostics, not independent art QA.

Producer inspected parent_masters/source1164_master_compare.png, parent_masters/source7086_full_master_compare.png and both WHOLE-POSE comparisons: expanded_closed_wholepose_compare.png and expanded_normal_wholepose_compare.png. Source OAM matrix/offset/output dimensions/position/priority from archived actual contracts were reused. These composites are source-backed producer reassemblies, NOT fresh HD runtime playback. The archived closed fixture is duo_map_forecast.state frame0; normal fixture duo_map_attack.state frame120. No fresh OAM capture for the user's open-front screenshot was invented.

Front component23041's exact source/placement are proven, but its colloquial anatomy (leg vs arm/shield-like assembly) is not asserted; the redraw preserves its real slender protrusion and panel geometry without inventing a giant fist. Root/Claude must inspect candidate anatomy against the native and user screenshots.

Producer visual flag is true and ready_for_install=true because the confirmed parent groups and primary source shapes now have a complete candidate. Independent_visual_QA=false, connected=false, baked=false. Root owns queue/shared handoff; Claude owns independent art inspection, installation, bake and live QA. The scope is the two stated source master extents plus two separately proven front components, not the entire game's graphic library.

No central library, DB, runtime, queue, manifest, shared handoff or root wing packet/reference was modified. build_expanded.py and reassemble_expanded.py reproduce local artifacts only.


## Producer preview palette limitation and wing exclusion

The normal native panel shows a green energy blade, while both current and candidate producer panels show dark purple stored atlas paint. This difference is PREEXISTING and OUTSIDE the body targets: the producer compositor directly places stored atlas RGBA and does not emulate runtime dynamic-palette remapping. It does not establish the actual runtime blade color. No weapon/energy color fix or wholepose color-correctness claim is made here. Weapon/energy IDs37538/37516/37525/37518/37519 are excluded.

Normal wing37485 and alternate wing37482 are excluded from all342 targets. Accepted closed wing IDs89573/89419/89721/89913/89946/89504/89910/89943 are also excluded. Thus producer candidate panes retain the current root/Claude accepted wing artwork as read from the library; this agent did not overwrite those wing packets/assets/bindings. expanded_pose_color_scope.json records these assertions.

All342 native/candidate child crops were additionally viewed on11 contact sheets. expanded_children_contact_index.json lists every ID per sheet. These are producer checks; they do not change independent_visual_QA=false.
