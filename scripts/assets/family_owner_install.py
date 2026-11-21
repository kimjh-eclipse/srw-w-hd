"""Any unit family: reinstall every part its units share from ONE unit's drawings.

Generalises strike_owner_install.py (11/19, user-approved for the Strike family). Units of a
family share body sprites (same RGB hash, one HD texture); each unit's install overwrote or
kept another unit's cut, so neighbouring parts came from different drawings (seams, stair
edges). Steps, under the install lock:
  1. shared hashes = used by 2+ family units (and by at most 6 units overall, so common effect
     sprites are left alone); their active bindings are disabled (backup made by the caller);
  2. each shared part gets one owner: the first unit in ORDER whose drawings show >= half of it
     (ORDER default: the unit covering the most shared parts first, so a whole body comes from
     one set of drawings), else the best-covered unit;
  3. the owner's cut is installed; hidden pixels take the sprite's native colours (xBRZ), as in
     strike_owner_install.native_fill.

  py -3.11 -X utf8 scripts/assets/family_owner_install.py --family 54,55,56,57 --tag duel [--order 54,55] [--dry]
"""
import argparse,collections,json,shutil,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets.strike_owner_install import native_fill

BASE=ROOT/'test_current/parts/pose_packets';LIB=ROOT/'graphics/kazuma_parts_library.json'
PY=[sys.executable,'-X','utf8']


def run(*a):
    r=subprocess.run(PY+[str(x) for x in a],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
    if r.returncode:raise RuntimeError(f"{a[0]} failed: {(r.stderr or r.stdout).strip().splitlines()[-3:]}")
    return r.stdout


def main():
    p=argparse.ArgumentParser();p.add_argument('--family',required=True);p.add_argument('--tag',required=True);p.add_argument('--order',default='');p.add_argument('--dry',action='store_true')
    a=p.parse_args();family=[int(x) for x in a.family.split(',')]
    units_of=collections.defaultdict(set)
    for c in BASE.glob('unit_*/robot_set/pose_*/contract.json'):
        u=int(c.parts[-4][5:])
        try:rows=json.loads(c.read_text(encoding='utf-8'))
        except Exception:continue
        if isinstance(rows,list):
            for r in rows:units_of[r['hash']].add(u)
    fam=set(family)
    shared={h for h,us in units_of.items() if len(us&fam)>=2 and len(us)<=6 and us<=fam}
    cover={}
    for u in family:
        rs=BASE/f'unit_{u}/robot_set';cov=rs/'split_fit/coverage.json'
        if not ((rs/'INSTALLED').exists() and cov.exists()):continue
        for r in json.loads(cov.read_text(encoding='utf-8')):
            if r['hash'] in shared and (rs/'split_fit/parts'/f"{r['hash']}.png").exists():cover.setdefault(r['hash'],{})[u]=r['coverage']
    if a.order:order=[int(x) for x in a.order.split(',')]
    else:order=sorted(family,key=lambda u:(-sum(1 for c in cover.values() if c.get(u,0)>=.5),u))
    owners={}
    for h,c in cover.items():
        good=[u for u in order if c.get(u,0)>=.5];u=good[0] if good else max(c,key=lambda u:(c[u],-u))
        owners.setdefault(u,[]).append(h)
    print('family',family,'shared',len(shared),'with drawing',len(cover),'order',order,'owners',{u:len(v) for u,v in sorted(owners.items())})
    out=BASE/f'_family_owner/{a.tag}';out.mkdir(parents=True,exist_ok=True)
    (out/'OWNERS.json').write_text(json.dumps(dict(family=family,order=order,owners={str(h):u for u,hs in owners.items() for h in hs},shared=sorted(shared)),indent=1),encoding='utf-8')
    if a.dry:return
    lib=json.loads(LIB.read_text(encoding='utf-8'));off=[]
    for i,b in enumerate(lib['bindings'],1):
        if b.get('hash') in shared and not b.get('disabled'):
            b['disabled']=True;b['disabled_reason']=f'family {a.tag} shared part: reinstalled from one owner unit (family_owner_install)';off.append(i)
    LIB.write_text(json.dumps(lib,ensure_ascii=False,indent=2),encoding='utf-8');print('disabled',len(off))
    q=ROOT/'docs/PENDING_ART_INSTALL_QUEUE.json';sources=[]
    for u,hs in sorted(owners.items()):
        src=BASE/f'unit_{u}/robot_set';dst=out/f'unit_{u}/robot_set'
        if dst.exists():shutil.rmtree(dst)
        rows={}
        for c in src.glob('pose_*/contract.json'):
            (dst/c.parent.name).mkdir(parents=True,exist_ok=True);shutil.copy2(c,dst/c.parent.name/'contract.json')
            for r in json.loads(c.read_text(encoding='utf-8')):rows.setdefault(r['hash'],r)
        parts=dst/'split_owner/parts';parts.mkdir(parents=True)
        for h in hs:native_fill(src/'split_fit/parts'/f'{h}.png',parts/f'{h}.png',rows[h])
        print(u,run('scripts/assets/package_robot_set.py',dst,'--split','split_owner').strip().splitlines()[-1],flush=True)
        queue=json.loads(q.read_text(encoding='utf-8'))
        for f in sorted((dst/'install').glob('*/queue_entry.json')):
            e=json.loads(f.read_text(encoding='utf-8'));sources.append(e['source'])
            queue['ready_candidates']=[c for c in queue['ready_candidates'] if c.get('source')!=e['source']]+[e]
        q.write_text(json.dumps(queue,ensure_ascii=False,indent=1),encoding='utf-8')
    if sources:
        run('scripts/assets/install_pending_art.py','--only',*sources)
        res=run('scripts/assets/install_pending_art.py','--apply','--only',*sources)
        print('\n'.join(l[:200] for l in res.splitlines() if l.startswith(('new parts','installed','NOT INSTALLED','FAILED'))))


if __name__=='__main__':main()
