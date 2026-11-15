#92544 three-component redraw

Use ready_candidate.json. This is a NEW built-in imagegen source, not root's earlier two-streak thin/wide/pixel-step drafts. No central files, queue, DB, runtime, game window or quarantine state were changed.

## Exact source structure

source_review.json[-1].captured_source is the actual rendered_obj_cache observation: unit214 mechanical_cutin_168.state+97,epoch98,engine0,OAM1,palette6,source16x32,flipX=false/flipY=true. Original raw/RGB/index/full16 palette match current registered92544 exactly (recomputed). Current captured key is2508490014/index3466631593. The drawing stays canonical UNFLIPPED; runtime flipY is retained in contract.

Original64 opaque texels have THREE8-connected components:
-Upper short4-texel yellow/gold segment, bbox[1,1,2,4].
-Main44-texel yellow/gold/white broken-highlight streak, bbox[3,6,11,26].
-Lower16-texel yellow/gold/orange stroke, bbox[1,21,7,10].

Source rowy5 is completely empty and disconnects upper short component from main. Main and lower bounding rectangles overlap, so the reference sheet was rendered from separately identified original components rather than naïvely cropping both components into the main cell. This source extraction is REFERENCE ONLY. No such mask was ever applied to generated output.

## New generated material and packing

three_component_reference.png is the exact3-cell reference used by built-in imagegen. generated_components.png is the unmodified actual generated3-cell own-alpha sheet. The prompt demanded three separate smooth2D strokes, native1–2texel thickness modulation, original gold/yellow/white/orange placements, no pixel stairs/cubes, no extra star/halo/blob. The selected output is soft/smooth and not the rejected pixel-step look.

Each whole generated stroke rectangle was LANCZOS resized into its OWN original bbox and translated into a16x32 source canvas at4x. own_component_packing.json records all three source boxes and selected generated rectangles. own_component_0/1/2.png are those own RGBA materials after geometric resampling, before composition. Generated alpha is retained; no native RGB/alpha transfer, pixel stencil, output threshold clearing, morphology, recoloring or edge repair is used.

## Producer checks

native_candidate_gray_pair.png was inspected on gray. It has three visible separated strokes, smooth contours, retained thickness modulation and native color families. The entire sourcey5 gap (output rows20–23) is ALPHA ZERO. Whole source envelope matches the native4x bbox. Per-component exact measured envelopes are in metrics.json: upper/lower match their geometric bbox; main's natural antialias starts1 output pixel below the native box, and its visible end is2 output pixels inside the box (one-quarter/half native-pixel differences, explicitly not a claim pixel-identical endpoints).

Native area64 → candidate native-equivalent area64.0625 at alpha>16,65.125 at>8,61.875 at>32,53.4375 at>128; alpha-weighted area53.1373. Main and lower visible areas are43.5 and15.9375 versus native44 and16. Diagnostic alpha-IoU.7498. Thus the old severe21/32 thin result and84 wide result are not reused.

At alpha>8/16/32/128 there are exactly3 components. ALL nonzero alpha retains17 components because14 subvisible generated/resampling islands remain; no low alpha is deleted to manufacture a3-count pass. Their size/max-alpha/bbox are openly recorded in metrics.json. Root/Claude must decide acceptance of this retained subvisible detail. Full-alpha preservation and visible3-component correctness are separate statements.

ready_candidate.json includes prior current bindingSpecSHA plus contract/drawing/native/generated4roleSHA. Registered source22342[32,0,16,32] is retained as current source metadata; no extra source-owner claim is invented. Source has no registered same-palette overlap from source_review's scope.

Ready for ROOT VISUAL REVIEW; producer_visual_check=true, connected=false,baked=false,independent_visual_QA=false,root_reported_quarantined=true. Do not lift quarantine automatically. Root/Claude own review/connection/bake/gameplay checks.

Final built-in prompt: exactly3 source cells; short4texel yellow/gold segment; main44texel11x26 diagonal with original1–2texel thickness and broken white patches; lower16texel7x10 gold/orange diagonal; smooth2D contours and original isolated source shapes, no cube/pixel-stair appearance, extra components or broad glow; true transparent own alpha. Exact full prompt is in this chat's tool invocation.
