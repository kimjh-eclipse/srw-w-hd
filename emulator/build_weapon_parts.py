"""Prepare and install observed rifle fragments, keeping previous binding IDs."""
from pathlib import Path
import json,sys
from PIL import Image

ROOT=Path(__file__).resolve().parent.parent
MANIFEST=ROOT/'graphics/kazuma_weapon_parts_manifest.json'

def main():
    if '--prepare' in sys.argv:
        records=json.loads((ROOT/'test_current/parts/missing_parts.json').read_text())
        keys=[4259027044,1821243665,2621939059]
        parts=[next(r for r in records if r['hash']==key) for key in keys]
        atlas=Image.new('RGBA',(96,64))
        for i,part in enumerate(parts):
            x,y=i%3*32,i//3*32;part.update(atlas_x=x,atlas_y=y)
            atlas.paste(Image.open(ROOT/f"test_current/parts/missing_{part['hash']:08x}.png"),(x,y))
        atlas.resize((1536,1024),Image.Resampling.NEAREST).save(ROOT/'graphics/kazuma_weapon_parts_reference.png')
        MANIFEST.write_text(json.dumps(dict(native_size=[96,64],parts=parts),indent=2))
        return
    manifest=json.loads(MANIFEST.read_text());path=ROOT/'graphics/kazuma_parts_library.json'
    # The final two initial candidates only occur during the black scene wipe,
    # not the rifle animation. Leave their native transition rendering intact.
    excluded={1917363372,2547954115}
    manifest['parts']=[p for p in manifest['parts'] if p['hash'] not in excluded]
    manifest['excluded_transition_hashes']=sorted(excluded)
    MANIFEST.write_text(json.dumps(manifest,indent=2))
    meta=json.loads(path.read_text());known={b['hash'] for b in meta['bindings']}
    stale=[i for i,b in enumerate(meta['bindings']) if b.get('atlas_id')=='weapon' and b['hash'] in excluded]
    if stale:
        assert stale==list(range(stale[0],len(meta['bindings']))),'cannot remove published interior binding IDs'
        del meta['bindings'][stale[0]:]
    assert (ROOT/'graphics/kazuma_weapon_parts_hd.png').exists()
    meta.setdefault('atlases',{})['weapon']=dict(image='kazuma_weapon_parts_hd.png',reference='kazuma_weapon_parts_reference.png',native_size=manifest['native_size'])
    for part in manifest['parts']:
        if part['hash'] in known:continue
        meta['bindings'].append(dict(hash=part['hash'],x=part['atlas_x'],y=part['atlas_y'],w=part['w'],h=part['h'],atlas_id='weapon'))
        known.add(part['hash'])
    path.write_text(json.dumps(meta,indent=2));print(json.dumps(dict(bindings=len(meta['bindings']),weapon_parts=sum(b.get('atlas_id')=='weapon' for b in meta['bindings']))))

if __name__=='__main__':main()
