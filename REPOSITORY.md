# Repository snapshot

Source layout: player modules remain in `emulator/`; asset tools, checks,
diagnostics and native-build helpers live under `scripts/`. Earlier voice
experiments and historical outputs are preserved in `research/legacy/`.
See `docs/SOURCE_LAYOUT.md` and `docs/source_moves.json` for the layout and path map.

This repository preserves the SRW W HD development work: the modified DeSmuME
sources and frontend, generated HD artwork and asset mappings, preparation tools,
and verification records. Large files use Git LFS; install Git LFS before cloning.

Game ROMs, player saves, save states, main-memory snapshots, credentials, Python
environments and downloaded compiler toolchains are excluded. Supply your own
compatible Korean 1.0.8 ROM locally at
`release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds`.

See `README.md` and `emulator/BUILD.txt` for the existing implementation and build
information. This is an in-progress development snapshot. Full campaign coverage
and a consistent 60 fps have not been verified. SDL controller updates no longer
dispatch the Tk window message pump; a real running window was moved successfully
after this fix. Long-session crash coverage remains incomplete. Voice insertion was
abandoned at the user's request; earlier research is retained as history.

DeSmuME retains its upstream GPL license and notices in `emulator/desmume/`.
Original game characters and material remain the property of their respective
rights holders; repository publication does not grant rights to those materials.

The first PNG optimization pass uses oxipng without resizing, palette reduction or alpha changes.
The optimizer verifies decoded mode, dimensions and all pixel bytes before atomic
replacement and leaves the approved face atlas untouched. The measured report is
`test_current/image_optimization/report.json`.

The subsequent display-size pass caps both game screens at 768–960 pixels wide.
Registered portraits, cut-ins, icons, menu art and oversized background/part
atlases were reduced using their native dimensions and logical display scale.
Packed world maps and atlases span multiple screens; their total width can exceed
960 while keeping the same per-pixel display budget. Original native signature
images and the approved initial part sources are preserved. See
`test_current/image_optimization/resized_art.json` for the 1,009 changed assets.
Menu textures are prebaked for the seven supported widths (84 textures total),
and all 548 portrait cache entries were rebuilt at the new maximum scale.

The subsequent frame-rate pass removes per-frame task/future turnaround waits,
adds conservative background color rejection, native font color masks, and stops
invalidating the Tk canvas during SDL presentation. A 40-second foreground battle
replay at width 768 averaged 59.032 displayed fps, with one-second lows near 49.
This is not a locked-60 or full-campaign result. Streaming capture, resolution
changes, input acknowledgement, pause/save/load, HD toggling and shutdown passed.
