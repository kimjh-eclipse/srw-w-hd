# Common battle composition checkpoint

The foreground bridge carries RGB555 source color, EVA/EVB, destination flags,
and the actual native destination layer for each pixel. The same calculation
is applied to OBJ parts, parts assembled on BG planes, primary cut-ins and
registered cut-ins. Native priority ties and intervening opaque layers remain
authoritative. This fixes color being lost when HD art is inserted beneath a
translucent foreground BG; reducing the HD art's alpha alone was insufficient.

GPU composition performs the color operation in the shader. The CPU path uses
the same arithmetic and retains painted alpha. No additional large painted
texture is generated per sprite per frame on the GPU path.

Resource-backed cut-ins now validate up to 512 SCR cells instead of relying on
a 16-cell prefix, which can be blank. There are 179 guarded entries; entries 2
and 3 have no verified source SCR and retain their existing recognition.
Fully opaque native 256x256 pictures repeat only when the live hardware plane
is also 256x256, preserving native scrolling without uncovered edge strips.

## Installed artwork and configuration fixes

- Valhawk's attack close-up is a distinct IMG 24394 / SCR 24395 / PLT 24393,
  registered as cut-in 182. It is separate from the previously registered
  mechanical close-ups. Painted alpha IoU is 0.91496. The retained plasma
  attack state recognizes 182 and displays the new art at its native offset.
- Five protagonist configuration selections have exact background bindings,
  including the separate large pilot, aircraft and Valstork pictures.
- The Full Metal Panic favorite-menu unit uses the reviewed intermediate
  style, aligned to the existing menu's part bounds.
- Ttk combobox popdowns no longer pass through Python widget conversion.
  Native mouse polling checks popup grabs and the window under the pointer,
  preventing list selections from becoming game touch/focus events.

## Verification and remaining scope

`verify_foreground_blend.py` checks coefficient arithmetic, priority ties,
intervening opaque layers, painted alpha and GPU/CPU parity.
`verify_foreground_scenes.py` replays 42 retained attack states from 14 named
units plus Getter/GoLion cut-ins. These are diagnostic fixture regressions;
they do not establish that every campaign attack has been visually verified.
`verify_popup_focus.py` checks Tcl-only focus/grab and pointer isolation.

Energy effects still have missing repainted assets. In particular, the retained
Jade firing state has exact tile matches to IMG 25822 that are not currently a
registered HD effect. The unclassified cut-in bank contains malformed/palette-
dependent decodes; its unmatched row count must not be reported as a count of
missing robots. Generic composition corrections do not turn these native
effect pictures into completed HD redraws. The outstanding work recorded in
REMAINING_HD_WORK.md, including HUD glyph cleanup and sustained display speed,
remains open.

The user's active test process is left running. Its already loaded code/core
is not silently replaced; the newly built portable program contains this
checkpoint for the next explicit restart.
