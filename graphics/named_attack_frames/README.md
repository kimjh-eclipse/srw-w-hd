# Observed attack fragments

These IMG resources were found by matching exact native 8×8 tiles captured
during named-unit weapon replays. They are separate from the main unit images.
The extraction reads the baseline ROM without changing it. Palettes come from
the recorded native battle textures, rather than a neighboring PLT assumption.

`plan.json` records source IDs and palette evidence. `registration.json` lists
accepted and rejected drawings. Rejected drawings are retained for review but
are not registered. Each registered PNG is at most 960 pixels on its long side;
transparent pixels have zero RGB. The generated outlines are preserved.

Registration uses silhouette overlap. For native images only 16–32 pixels high,
an additional symmetric one-native-pixel check tolerates antialiasing differences
without imposing the original staircase mask on the drawing. These checks are
reported individually. Two gun atlases, 8264 and 8265, have byte-identical alpha
masks; their different native color indices are retained.

`coverage.json` checks production tile assembly for the accepted full resources
and the previously unmatched captured hardware rectangles. `gameplay.json`
records native weapon-menu replays, including a second pass with the stage cache
already populated. Neither report certifies every campaign pose.

Artwork was generated with the built-in image generation tool. The prompts
requested faithful anime mechanical texture fragments with original positions,
colors and silhouettes, transparent background, no assembly into whole units,
and no additional fragments or scenery. Four four-row sheets were followed by
individual redraws for failed registrations. Original generated files remain
unchanged; the `frame_*_hd.png` files are bounded registered derivatives.
