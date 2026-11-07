# Repository snapshot

This repository preserves the SRW W HD development work: the modified DeSmuME
sources and frontend, generated HD artwork and asset mappings, preparation tools,
and verification records. Large files use Git LFS; install Git LFS before cloning.

Game ROMs, player saves, save states, main-memory snapshots, credentials, Python
environments and downloaded compiler toolchains are excluded. Supply your own
compatible Korean 1.0.8 ROM locally at
`release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds`.

See `README.md` and `emulator/BUILD.txt` for the existing implementation and build
information. This is an in-progress development snapshot. Full campaign coverage
and a consistent 60 fps have not been verified; the latest reported SDL/Tk window
movement and crash issues are still under investigation. Voice insertion was
abandoned at the user's request; earlier research is retained as history.

DeSmuME retains its upstream GPL license and notices in `emulator/desmume/`.
Original game characters and material remain the property of their respective
rights holders; repository publication does not grant rights to those materials.

PNG optimization uses oxipng without resizing, palette reduction or alpha changes.
The optimizer verifies decoded mode, dimensions and all pixel bytes before atomic
replacement and leaves the approved face atlas untouched. The measured report is
`test_current/image_optimization/report.json`.
