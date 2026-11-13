# Built-in image_gen 프롬프트

1. Six-part sprite sheet: exact positions/angles/extents/negative space and narrow disconnected original fragment silhouettes; gray to true transparency; smooth cel-shaded original colors, no new hands/fists/boots/bulky armor, no cut-edge caps, no glow/fringe/halo/text. Top/bottom-left are thin purple-white brackets, middle two mauve/blue-white chips, top-right thin purple sliver, bottom-right disconnected dark/red dashes. Geometry before detail.
2. Background-extraction edit only: remove black backdrop and every diffuse halo to actual alpha zero; preserve six hard painted fragments, exact geometry/positions/colors/scale and normal edge antialiasing; no embellishment/thickening/completion, no floor, no added cut-edge outlines.

도구: built-in image_gen, transparent_background=true. 결과는동일폴더generated_v3_halo_rejected.png/generated_v4_background_extract.png. 첫파일명halo_rejected는육안RGB오해시작성된이름이며실제alpha판정은HANDOFF_ROOT_RETRY.md정정우선.
