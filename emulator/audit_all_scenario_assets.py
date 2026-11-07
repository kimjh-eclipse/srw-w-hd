"""File readiness audit for the complete 247-resource scenario scene bank.

Registration and real game verification are separate runtime responsibilities.
"""
import hashlib
import json
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / 'graphics/scenario_backgrounds'
OUT = ROOT / 'test_current/scenario_backgrounds'
BLANKS = {5099: (255, 255, 255), 5276: (0, 0, 0)}


def write(path, data):
    temporary = path.with_suffix('.tmp.json')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf8')
    temporary.replace(path)


def main():
    catalog = json.loads((F / 'catalog.json').read_text(encoding='utf8'))
    checks, missing = [], []
    rows = catalog['resources']
    assert len(rows) == 247
    for row in rows:
        resource = row['map_resource']
        nativepath = ROOT / 'graphics' / row['native']
        imagepath = ROOT / 'graphics' / row['image']
        with Image.open(nativepath) as im:
            native = im.convert('RGB')
        ready = imagepath.is_file()
        row.update(id=resource, resource=row['image_resource'], generated=ready,
                   category='scenario_background' if resource >= 5102 else 'story_cg_or_map',
                   status='generated' if ready else 'native_only')
        result = dict(resource=resource, category=row['category'], native_size=list(native.size),
                      native_sha256=hashlib.sha256(nativepath.read_bytes()).hexdigest(),
                      image_exists=ready, registered=bool(row.get('registered')),
                      game_verified=bool(row.get('game_verified')))
        if ready:
            with Image.open(imagepath) as im:
                art = im.convert('RGB')
            assert art.width >= native.width * 2 and art.height >= native.height * 2, (resource, art.size)
            delta = np.abs(np.asarray(native, dtype='int16') - np.asarray(art.resize(native.size, Image.Resampling.LANCZOS), dtype='int16'))
            changed = int(np.any(delta > 3, axis=2).sum())
            if resource in BLANKS:
                assert np.all(np.asarray(native) == BLANKS[resource]), resource
                assert np.all(np.asarray(art) == BLANKS[resource]), resource
            else:
                assert changed > 0, (resource, 'unchanged native')
            result.update(hd_size=list(art.size), sha256=hashlib.sha256(imagepath.read_bytes()).hexdigest(),
                          bytes=imagepath.stat().st_size, decoded=True, changed_native_pixels=changed,
                          blank_preserved=resource in BLANKS)
            row.update(hd_size=result['hd_size'], hd_sha256=result['sha256'])
        else:
            missing.append(resource)
        checks.append(result)

    cgfile = F / 'cg_batches.json'
    batches = json.loads(cgfile.read_text(encoding='utf8'))
    supportfile = F / 'cg_support_generation.json'
    support = json.loads(supportfile.read_text(encoding='utf8')) if supportfile.exists() else {}
    supportbyname = {b['name']: b for b in support.get('batches', [])}
    for batch in batches['batches']:
        if all((F / f'scenario_{i}_hd.png').is_file() for i in batch['resources']):
            if batch['name'] in supportbyname:
                batch.update(supportbyname[batch['name']])
            batch['status'] = 'generated'
    write(cgfile, batches)
    lineage = {}
    for metafile in ['generation_prompts.json', 'batches.json', 'quad_batches.json', 'cg_batches.json']:
        meta = json.loads((F / metafile).read_text(encoding='utf8'))
        for batch in meta.get('batches', []):
            atlas = F / batch.get('selected', batch.get('atlas', 'missing'))
            if batch.get('status', 'generated') != 'generated' or not atlas.is_file():
                continue
            info = dict(batch=batch['name'], manifest=metafile, atlas=atlas.name,
                        atlas_sha256=hashlib.sha256(atlas.read_bytes()).hexdigest(),
                        generation_source=batch.get('source_path'), tool=meta.get('tool', 'built-in image_gen'))
            for resource in batch['resources']:
                lineage[str(resource)] = info
    lineage['5522'] = dict(manifest='special_generation.json', method='AI generated scrolling effect, resized for runtime')
    for entry in json.loads((F / 'cg_reuse.json').read_text(encoding='utf8'))['resources']:
        lineage[str(entry['resource'])] = dict(manifest='cg_reuse.json', **entry)
    localized_maps = {4790: '오세아니아 지역', 4791: '유럽 지역', 4792: '극동 지역',
                      4793: '북미 지역', 4794: '간토 지역', 4797: '지구권 지역',
                      4800: '태양~목성 지역', 4803: '태양계 지역', 4806: '은하계 지역'}
    write(F / 'asset_lineage.json', dict(scope=247, resources=lineage,
          localized_map_labels=localized_maps,
          other_localization_manifests=['cg_batches.json (cg_11 jacket)', 'cg_support_generation.json (cg_20 TV and school introduction)']))
    catalog.update(generated=sum(r['generated'] for r in rows), scenario_backgrounds=141,
                   scenario_backgrounds_generated=sum(r['generated'] for r in rows if r['map_resource'] >= 5102),
                   story_cg_or_maps=106,
                   story_cg_or_maps_generated=sum(r['generated'] for r in rows if r['map_resource'] < 5102))
    write(F / 'catalog.json', catalog)
    write(F / 'library.json', dict(backgrounds=rows))
    rom = ROOT / 'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds'
    romsha = hashlib.sha256(rom.read_bytes()).hexdigest()
    assert romsha == '0a5a22bd6bb25ebe640767e6b422b91358636e9ae1300e61d7e8ac3c5d8cd478'
    report = dict(scope='All 247 scenario scene bank native resources 4780-5523: 141 backgrounds and 106 story CG or maps',
                  native_resources=247, generated_files=247-len(missing), missing=missing,
                  decoded_files=sum(c.get('decoded', False) for c in checks),
                  total_hd_bytes=sum(c.get('bytes', 0) for c in checks),
                  categories={kind: dict(total=sum(r['category'] == kind for r in rows), generated=sum(r['category'] == kind and r['generated'] for r in rows)) for kind in ['scenario_background', 'story_cg_or_map']},
                  sizes=dict(Counter('x'.join(map(str, c['hd_size'])) for c in checks if 'hd_size' in c)),
                  blank_backgrounds_preserved=list(BLANKS), reused_existing_hd=[4797],
                  canonical_rom_sha256=romsha, canonical_rom_unchanged=True,
                  registered=sum(c['registered'] for c in checks), game_verified=sum(c['game_verified'] for c in checks),
                  verification_scope='Decoded file / dimensions / changed art / hashes / preserved blank scenes. Runtime registration and actual game coverage must be verified separately by root.',
                  tool='built-in image_gen', checks=checks)
    write(F / 'coverage_all.json', report)
    cg = [r for r in rows if r['map_resource'] < 5102]
    OUT.mkdir(parents=True, exist_ok=True)
    for page in range((len(cg)+23)//24):
        sheet = Image.new('RGB', (1024, 624), '#222')
        draw = ImageDraw.Draw(sheet)
        for n, row in enumerate(cg[page*24:(page+1)*24]):
            x, y = n % 6 * 170, n // 6 * 156
            with Image.open(ROOT / 'graphics' / row['image' if row['generated'] else 'native']) as im:
                art = im.convert('RGB').resize((168, 126))
            sheet.paste(art, (x, y))
            draw.text((x, y+128), f"{row['map_resource']} {'HD' if row['generated'] else 'MISSING'}", fill='white' if row['generated'] else 'red')
        sheet.save(OUT / f'cg_hd_contact_{page}.png')
    print(json.dumps({k: v for k, v in report.items() if k != 'checks'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
