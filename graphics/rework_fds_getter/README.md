# FDS Getter body redraw — pending review

Source: IMG 23382, SCR 23411, PLT 23380 from the Korean baseline ROM.
The original assembled BG body is 256×128. Retained scene: unit_297 /
weapon_1213_capture / frame_1320 (the unit identifier belongs to the initiating
Kaiser record, not the Getter shown during the combined attack).

`body_23382_palette_23380_native.png` is an extracted reference, not HD art.
`body_23382_reference.png` is a nearest-neighbor reference enlargement.
PLT 23381 is retained as a palette alternative for investigation.

`body_23382_rejected_eyes.png` is rejected: the small red head was incorrectly
given rounded red goggle shapes. Do not register or bake it. A subsequent
experiment incorrectly interpreted the large silver chest as a face; that
experiment is also rejected. The actual head is the small red helmet above
the central chest, between the shoulder shells.

No existing atlas, production binding, cut-in library or baked database was
changed by this asset preparation. Registration and full-scene playback are
still pending. The energy plane (IMG 23393 / 23397) and separate OBJ fists
must be checked independently; completing this BG drawing alone does not
complete the entire attack.
