# Remaining HD validation

Normal native-menu diagnostics currently complete 1,702 of 1,804 weapon
records. These records include enemies, stat variants, transformations and
support actions; they are not 1,804 distinct offensive animations. The
remaining normal-route cases are 87 omitted menu entries, 12 cases that do not
start a battle, and three unfinished Scientia cases. Diagnostic terrain and
level overrides affect isolated RAM only, never the distributed ROM or saves.

Locked animations are additionally previewed in the game's native battle
engine by injecting a menu entry. Their reports live in each unit's
`diagnostic_preview` directory and are summarized separately. They do not
increase normal menu/campaign coverage. Kaiser Nova and Final Dynamic Special
both completed this route with the requested native weapon IDs.

## Connected in this pass

Thirteen additional full IMG resources: 7152, 8264, 8265, 8287, 8805, 8812,
8826, 8832, 10780, 11079, 15026, 17168 and 18170. Their source tiles were
observed in native weapon replays. Production assembly currently verifies
78 previously unmatched recorded rectangles. Second-pass replays observed
all thirteen source resources. The separate Strike Rouge bazooka rectangle
937738407 (associated with bank 7656) is also registered and observed in its
completed weapon replay; that does not certify the entire 7656 bank.

The 322 secondary unit pictures and 37 shared punch IMG records (36 nonempty)
still pass their production assembly checks. The frozen executable also
passed its Quatre cut-in/controller-worker smoke test. No controller was
physically connected during that smoke test.

## Newly exposed cut-in class

Final Dynamic Special contains compact, tile-rearranged pilot faces that are
not in the existing large BG cut-in registrations. Exact native tile matching
identified IMG 23473 and 23474 in captured BG layers 1 and 2. The surrounding
bank has IMG 23473..23483 and matching SCR 23484..23494, preceded by multiple
PLT entries. These are compact atlases, not directly displayable full faces.

All eleven assembled pictures (six face canvases and five effect canvases)
are now registered. The native bridge exports one first raster window per
BG layer, and the renderer composites those planes in native priority order.
Compact restoration is limited to the 256x128 picture region so dialogue UI
on the same BG layer survives. Phase-specific PLTs are replacements, not one
concatenated palette: live BG captures confirmed 23467 at battle frame 600
and 23468/23470 at frame 720. The initial incorrect palette candidates were
replaced before packaging.

Final Dynamic Special replayed to completion (2,080 battle-loop frames),
observing IDs 171..181. Captured native-engine HD frames at 360, 720 and 1080
show simultaneous faces, corrected masks and the preserved dialogue frame.
Five earlier pilot cut-in states retain their native bridge IDs; the separate
Bonta OBJ-state check only checks bindings and is not a new visual certificate.
The exact source audit remains in the fixed native capture folder.

## Historical missing-texture audit

The audit now includes locked-animation previews. Of 3,902 retained native
rectangle inputs, the current production tile assembler resolves 414; 3,488
still fail that assembly path. A direct indexed-binding cross-check found no
additional direct matches among those failures. These are hardware rectangles
and palette variants, not 3,488 robots. Many are explosions, beams, flashes,
smoke, terrain fragments or mechanical attack inserts. The remaining entries
have 296 first-choice ROM source candidates; shared tiles can make those
candidates ambiguous. This establishes unfinished work, not full HD coverage.
`test_current/parts/observed_attack_gaps/current_assembly.json` preserves the
exact assembler results for subsequent work.

## Effect fragments under review

The remaining observed pieces associated with banks 1775 and 11202 are mostly
muzzle/light streak fragments. Several generated candidates merely reproduced
the native square pixels at a larger size; those are explicitly unapproved
in `graphics/named_attack_frames/observed_plan.json` and are not installed.
Another smooth flare candidate has insufficient silhouette agreement and is
also not installed. No rejected drawing is counted as a finished HD asset.

Full campaign legality and visual verification of every pose remain open.
The computer must remain powered on after work completes.

## Presentation speed remains open

Two 25-second foreground desktop replays at fixed 768-wide HD rendering
measured 59.525/59.838 emulated FPS and 53.551/53.217 displayed FPS. The cached
cut-in-region path removes full-canvas alpha work and passes 36 CPU/GPU alpha
equivalence cases, but these runs do not demonstrate a display-FPS gain.
The short headless target-state worker test also failed its 54-FPS threshold
(42.29 FPS in the quiet rerun). Its older passing report is not evidence for
this build. A sustained 60 displayed FPS certificate is still outstanding.
