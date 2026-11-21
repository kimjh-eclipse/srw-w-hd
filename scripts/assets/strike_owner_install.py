"""Strike family: reinstall each shared part from ONE unit's drawings.

Units 11-22 / Rouge 39-45 share body sprites (same RGB hash, one HD texture). Each
variant's install overwrote the others' cut of the same part, so neighbouring parts
came from different drawings and did not line up (user review 2026-11-19).
disable_strike_shared.py turned those parts off; this puts them back with one owner per
part: the family unit whose drawings show that part most completely (split_fit
coverage, ties -> lower unit id). The parts are cut from Codex's whole-robot drawings
exactly as before (split_fit/parts/<hash>.png of the owner); only the choice of source
changes. Nothing is recoloured.

  py -3.11 -X utf8 scripts/assets/strike_owner_install.py [--dry]
Run under the install lock.
"""
import argparse,json,shutil,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT

BASE=ROOT/'test_current/parts/pose_packets'
FAMILY=[11,12,13,14,15,16,17,18,19,20,21,22,39,40,41,42,43,44,45]
ORDER=[11,12,19,20,22,21,40,42,43,16,17,18,13,41,14,15,39,44,45]
PY=[sys.executable,'-X','utf8']


def native_fill(src,dst,row):
    """Pixels no drawing shows (hidden behind another sprite in every battle pose) take the
    sprite's own native colours, upscaled 4x by xBRZ, instead of package_robot_set's grow_fill.
    Grown colour invented a blue slab over Strike's face on the status screen / icon, where the
    chest sprite's top (the face) is in front (user report 2026-11-19). Not a recolour: the
    native pixels of this very sprite. Parts drawn for less than half stay as cut (dropped)."""
    import base64,zlib
    import numpy as np
    from PIL import Image
    sys.path.insert(0,str(ROOT/'emulator'))
    from native_obj_filter import _xbrz4
    art=np.asarray(Image.open(src).convert('RGBA')).copy()
    idx=np.frombuffer(zlib.decompress(base64.b64decode(row['index_pixels'])),dtype='uint8').reshape(row['h'],row['w'])
    want=np.kron(idx>0,np.ones((4,4),bool));drawn=(art[...,3]>127)&want
    cov_src=Path(src).parent.parent/'cov'/Path(src).name
    if cov_src.exists():   # soft-edge split: copy the coverage; covered pixels keep the drawing's alpha
        cov=np.asarray(Image.open(cov_src))>0;drawn=cov&want
        (Path(dst).parent.parent/'cov').mkdir(exist_ok=True);shutil.copy2(cov_src,Path(dst).parent.parent/'cov'/Path(src).name)
    if drawn.sum()<.5*want.sum() or drawn.sum()==want.sum():Image.fromarray(art).save(dst);return
    pal=np.array(row['original_palette_rgb'],dtype='uint32')
    argb=np.where(idx>0,(255<<24)|(pal[idx,0]<<16)|(pal[idx,1]<<8)|pal[idx,2],0).astype(np.uint32)
    up=np.asarray(_xbrz4(argb),dtype=np.uint32).reshape(row['h']*4,row['w']*4)
    fill=want&~drawn
    art[fill,0]=(up[fill]>>16)&255;art[fill,1]=(up[fill]>>8)&255;art[fill,2]=up[fill]&255;art[fill,3]=255
    Image.fromarray(art).save(dst)


def run(*a):
    r=subprocess.run(PY+[str(x) for x in a],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
    if r.returncode:raise RuntimeError(f"{a[0]} failed: {(r.stderr or r.stdout).strip().splitlines()[-3:]}")
    return r.stdout


def main():
    p=argparse.ArgumentParser();p.add_argument('--dry',action='store_true');a=p.parse_args()
    shared=set(json.loads((BASE/'STRIKE_SHARED_DISABLED.json').read_text())['hashes'])
    # Neighbouring parts must come from the same drawings, so owners are taken in a fixed
    # order (base Strike body first, then each pack's unit), not per part by coverage.
    # A unit owns a part when its drawings show at least half of it (package_robot_set
    # drops less); otherwise the best-covered unit takes it.
    best={};cover={}
    for u in FAMILY:
        rs=BASE/f'unit_{u}/robot_set';cov=rs/'split_fit/coverage.json'
        if not ((rs/'INSTALLED').exists() and cov.exists()):continue
        for r in json.loads(cov.read_text(encoding='utf-8')):
            if r['hash'] in shared and (rs/'split_fit/parts'/f"{r['hash']}.png").exists():cover.setdefault(r['hash'],{})[u]=r['coverage']
    for h,c in cover.items():
        good=[u for u in ORDER if c.get(u,0)>=.5]
        u=good[0] if good else max(c,key=lambda u:(c[u],-u))
        best[h]=(c[u],u)
    owners={}
    for h,(k,u) in best.items():owners.setdefault(u,[]).append(h)
    print('shared',len(shared),'with an owner',len(best),'no drawing',len(shared-set(best)))
    print({u:len(v) for u,v in sorted(owners.items())})
    out=BASE/'_strike_owner';(out).mkdir(exist_ok=True)
    (out/'OWNERS.json').write_text(json.dumps({str(h):u for h,(k,u) in best.items()},indent=1),encoding='utf-8')
    if a.dry:return
    q=ROOT/'docs/PENDING_ART_INSTALL_QUEUE.json';sources=[]
    for u,hs in sorted(owners.items()):
        src=BASE/f'unit_{u}/robot_set';dst=out/f'unit_{u}/robot_set'
        if dst.exists():shutil.rmtree(dst)
        for c in src.glob('pose_*/contract.json'):
            (dst/c.parent.name).mkdir(parents=True,exist_ok=True);shutil.copy2(c,dst/c.parent.name/'contract.json')
        parts=dst/'split_owner/parts';parts.mkdir(parents=True)
        rows={}
        for c in src.glob('pose_*/contract.json'):
            for r in json.loads(c.read_text(encoding='utf-8')):rows.setdefault(r['hash'],r)
        for h in hs:native_fill(src/'split_fit/parts'/f'{h}.png',parts/f'{h}.png',rows[h])
        print(u,run('scripts/assets/package_robot_set.py',dst,'--split','split_owner').strip().splitlines()[-1],flush=True)
        queue=json.loads(q.read_text(encoding='utf-8'))
        for f in sorted((dst/'install').glob('*/queue_entry.json')):
            e=json.loads(f.read_text(encoding='utf-8'));sources.append(e['source'])
            queue['ready_candidates']=[c for c in queue['ready_candidates'] if c.get('source')!=e['source']]+[e]
        q.write_text(json.dumps(queue,ensure_ascii=False,indent=1),encoding='utf-8')
    print(run('scripts/assets/install_pending_art.py','--only',*sources)[-1500:])
    res=run('scripts/assets/install_pending_art.py','--apply','--only',*sources)
    print('\n'.join(l for l in res.splitlines() if l.startswith(('new parts','installed','NOT INSTALLED','FAILED'))))


if __name__=='__main__':main()
