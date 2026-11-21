"""Remove baked textures no current library binding uses, then compact the file (11/21).

Every reinstall/re-cut added new textures under new keys; old ones stayed. Kept: the key of every
binding in the library (enabled or disabled, so a re-enabled part needs no re-bake) for both cut
policies. Everything else in the textures table goes. Then VACUUM. Run when nothing else uses the
store (no installer, no player, no bake).

  py -3.11 -X utf8 scripts/assets/prune_baked_store.py [--dry]
"""
import argparse,sqlite3,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
sys.path.insert(0,str(ROOT/'emulator'))


def main():
    a=argparse.ArgumentParser();a.add_argument('--dry',action='store_true');a=a.parse_args()
    from hd_parts import PartsRenderer
    r=PartsRenderer(async_prepare=False);keep=set()
    for i,spec in enumerate(r.bindings,1):
        if spec.get('source_binding') or spec.get('runtime_texture') or spec.get('disabled'):continue   # turned-off parts go too (user 11/21); a re-enabled part is re-baked
        for cp in (True,False):
            try:keep.add(r.texture_key(i,spec['w'],spec['h'],cut_policy=cp))
            except Exception:pass
    path=ROOT/'graphics/parts_baked.sqlite';db=sqlite3.connect(path)
    present=[k for (k,) in db.execute('SELECT key FROM textures')]
    drop=[k for k in present if k not in keep]
    print('stored',len(present),'kept',len(present)-len(drop),'drop',len(drop),'keys wanted',len(keep))
    if a.dry:return
    db.executemany('DELETE FROM textures WHERE key=?',[(k,) for k in drop]);db.commit()
    before=path.stat().st_size;db.execute('VACUUM');db.close()
    print('size',round(before/1e9,2),'GB ->',round(path.stat().st_size/1e9,2),'GB')


if __name__=='__main__':main()
