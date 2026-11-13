"""Fit one continuous painting to a captured OAM contract without moving parts.

Writes a candidate atlas and a reconstruction; never changes live bindings or
the baked store. Review these before installing. The captured transform must
belong to the same animation frame as the native silhouette.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--drawing', type=Path, required=True)
    parser.add_argument('--contract', type=Path, required=True)
    parser.add_argument('--native-pose', type=Path, required=True)
    parser.add_argument('--atlas', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    contract = json.loads(args.contract.read_text(encoding='utf-8'))
    origin = np.asarray(contract.get('canvas_origin', [0, 0]), dtype=float)
    native = Image.open(args.native_pose).convert('RGBA')
    drawing = Image.open(args.drawing).convert('RGBA')
    # The original fitter moved the WHOLE painting down whenever any wing
    # crossed the centre OBJ's top edge. That compressed the pose vertically.
    # Geometry belongs to the captured scene, not to an individual OBJ window.
    bbox = native.getbbox()
    desired = Image.new('RGBA', native.size)
    # Generated transparent canvases can contain near-zero alpha over their
    # whole extent. Such padding must not determine the artwork's proportions.
    paint_bbox = drawing.getchannel('A').point(lambda a: 255 if a > 64 else 0).getbbox()
    if paint_bbox is None:
        raise ValueError('Painting has no visible pixels')
    piece = drawing.crop(paint_bbox).resize(
        (bbox[2] - bbox[0], bbox[3] - bbox[1]), Image.Resampling.LANCZOS)
    desired.alpha_composite(piece, bbox[:2])
    atlas = Image.open(args.atlas).convert('RGBA')
    scale = 4
    reconstructed = Image.new('RGBA', native.size)
    for part in contract['parts']:
        matrix = np.asarray(part['matrix'], dtype=float)
        inverse = np.linalg.inv(matrix)
        shift = np.array([part['x'], part['y']]) - origin - inverse @ part['offset']
        coeff = (inverse[0, 0], inverse[0, 1], shift[0] * scale,
                 inverse[1, 0], inverse[1, 1], shift[1] * scale)
        cropped = desired.transform((part['w'] * scale, part['h'] * scale),
                                    Image.Transform.AFFINE, coeff,
                                    Image.Resampling.BICUBIC)
        atlas.paste(cropped, (part['source_x'] * scale, 0))
        # Reconstruct using the original OAM transform, including doubled OBJ.
        coeff = (matrix[0, 0], matrix[0, 1], part['offset'][0] * scale,
                 matrix[1, 0], matrix[1, 1], part['offset'][1] * scale)
        posed = cropped.transform((part['w'] * 2 * scale, part['h'] * 2 * scale),
                                  Image.Transform.AFFINE, coeff,
                                  Image.Resampling.BICUBIC)
        reconstructed.alpha_composite(posed, (round((part['x']-origin[0])*scale), round((part['y']-origin[1])*scale)))
    wanted = np.asarray(desired)
    actual = np.asarray(reconstructed)
    opaque = wanted[:, :, 3] > 224
    lost = opaque & (actual[:, :, 3] < 128)
    difference = np.abs(wanted[:, :, :3].astype('int16') - actual[:, :, :3])
    report = dict(scope='Offline OAM geometry only; not gameplay verification',
                  bindings=[p['binding'] for p in contract['parts']],
                  screen_bbox=bbox, painting_bbox=paint_bbox,
                  canvas_origin=origin.tolist(),
                  reconstructed_bbox=reconstructed.getbbox(),
                  opaque_pixels=int(opaque.sum()), lost_opaque_pixels=int(lost.sum()),
                  mean_rgb_error=float(difference[opaque].mean()),
                  live_atlas_modified=False, gameplay_verified=False)
    desired.save(args.output / 'desired.png')
    reconstructed.save(args.output / 'reconstructed.png')
    atlas.save(args.output / 'candidate_atlas.png')
    (args.output / 'report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
