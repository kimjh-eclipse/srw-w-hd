"""Install art candidates handed over in docs/PENDING_ART_INSTALL_QUEUE.json.

One writer connects art: this tool. The drawer lists finished candidates in the
queue (source folder, contract, drawing, native, generated, bindings, file
SHA-256 and the SHA-256 of each binding's current spec); nothing else writes
the part library, the baked store or the production manifest.

Without --apply it only checks: every listed file must still have its
recorded hash and every binding its recorded spec (so a candidate drawn
against an older library is refused, not installed over newer art), and it
draws native | candidate for each part on grey into
test_current/parts/pending_install/precheck.png for a visual check.

With --apply it installs the checked candidates through the same per-atlas
installer and target bake the producer used (test_current/parts/
root_pending_repair_factory.py), records them in the production manifest,
measures them with verify_new_art.py and appends them to
docs/ART_INSTALL_DONE.json, which later runs use to skip them.
"""
import argparse,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
import numpy as np
from PIL import Image,ImageDraw

QUEUE=ROOT/'docs/PENDING_ART_INSTALL_QUEUE.json';DONE=ROOT/'docs/ART_INSTALL_DONE.json';LIBRARY=ROOT/'graphics/kazuma_parts_library.json'
OUT=ROOT/'test_current/parts/pending_install'
sha=lambda data:hashlib.sha256(data).hexdigest()


def spec_hash(spec):
    return {sha(json.dumps(spec,sort_keys=True,ensure_ascii=False).encode()),sha(json.dumps(spec,sort_keys=True).encode())}


def atlas_name(candidate):
    stem=re.sub(r'[^a-z0-9]+','_',Path(candidate['source']).name.lower()).strip('_')
    stem=re.sub(r'^(claude_|root_|borrowed_shape_rework_)','',stem)
    return f"{stem}_{'_'.join(map(str,sorted(candidate['bindings'])))[:40]}"


def rows_of(folder,candidate):
    rows=json.loads((folder/candidate['contract']).read_text(encoding='utf-8'))
    for row in rows:
        box=row.get('atlas_box')
        binding=row.get('replace_binding',row.get('replacement_of_existing_binding',row.get('binding_id')))
        yield binding,box


def check(queue,done,library,rejected=()):
    installed={(d['source'],d['drawing_sha256']) for d in done};seen={(d['source'],d['drawing_sha256']):d['reason'] for d in rejected}
    ready=[];refused=[]
    for c in queue.get('ready_candidates',[]):
        folder=ROOT/c['source'];problems=[];key=(c['source'],c.get('file_sha256',{}).get('drawing'))
        if key in installed:continue
        if key in seen:print('REJECTED EARLIER (same drawing)',c['source'],seen[key]);continue
        for role,want in c.get('file_sha256',{}).items():
            f=folder/c.get(role,'')
            if not f.is_file():problems.append(f'{role} file missing')
            elif sha(f.read_bytes())!=want:problems.append(f'{role} changed since handover')
        for role in ('contract','drawing','native','generated'):
            if role not in c.get('file_sha256',{}):problems.append(f'no recorded hash for {role}')
        for b in c['bindings']:
            want=c.get('prior_binding_spec_sha256',{}).get(str(b))
            if want is None:problems.append(f'no recorded spec for {b}')
            elif want not in spec_hash(library['bindings'][b-1]):problems.append(f'binding {b} changed since the candidate was drawn')
        (refused if problems else ready).append((c,problems))
    return ready,refused


def matte_residue(c):
    """Parts whose drawing keeps alpha over most of the area that is empty (and
    not next to ink) in the native image: a faint box would be drawn there."""
    folder=ROOT/Path(c['source'].replace('\\','/'));native=np.asarray(Image.open(folder/c['native']).convert('RGBA'));art=np.asarray(Image.open(folder/c['drawing']).convert('RGBA'))
    scale=art.shape[1]//native.shape[1];bad=[]
    for binding,(x,y,w,h) in rows_of(folder,c):
        ink=np.pad(native[y:y+h,x:x+w,3]>0,1);near=ink[1:-1,1:-1]|ink[:-2,1:-1]|ink[2:,1:-1]|ink[1:-1,:-2]|ink[1:-1,2:]
        far=~np.kron(near,np.ones((scale,scale),bool));a=art[y*scale:(y+h)*scale,x*scale:(x+w)*scale,3]
        if far.any() and (a[far]>8).mean()>.3:bad.append(binding if binding is not None else (x,y))
    return bad


def precheck_sheet(ready,path):
    cells=[]
    for c,_ in ready:
        folder=ROOT/c['source'];native=Image.open(folder/c['native']).convert('RGBA');art=Image.open(folder/c['drawing']).convert('RGBA')
        scale=art.width//native.width
        for binding,(x,y,w,h) in rows_of(folder,c):
            cells.append((f'#{binding} {folder.name[:24]}',native.crop((x,y,x+w,y+h)),art.crop((x*scale,y*scale,(x+w)*scale,(y+h)*scale))))
    cell=180;per=3
    sheet=Image.new('RGB',(per*cell*2,max(1,(len(cells)+per-1)//per)*(cell+16)),(96,96,104));draw=ImageDraw.Draw(sheet)
    for i,(label,a,b) in enumerate(cells):
        x=(i%per)*cell*2;y=(i//per)*(cell+16);k=min((cell-6)/a.width,(cell-6)/a.height)
        size=(max(1,round(a.width*k)),max(1,round(a.height*k)))
        A=a.resize(size,Image.Resampling.NEAREST);B=b.resize(size,Image.Resampling.LANCZOS)
        sheet.paste(A,(x+3,y+3),A);sheet.paste(B,(x+cell+3,y+3),B);draw.text((x+3,y+cell),label,fill=(255,255,255))
    sheet.save(path)


def main():
    parser=argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--apply',action='store_true',help='connect, bake, record and measure the checked candidates')
    parser.add_argument('--only',nargs='*',default=[],help='limit to these source folders (as written in the queue)')
    parser.add_argument('--skip',nargs='*',default=[],help='leave these source folders out this run')
    parser.add_argument('--reject',nargs=2,action='append',default=[],metavar=('SOURCE','REASON'),help='record a visual rejection; the same drawing is not offered again')
    parser.add_argument('--no-caches',action='store_true',help='skip rebuilding the material caches and tile library after installing')
    parser.add_argument('--allow-original',type=int,nargs='*',default=[],help='original bindings (1..5263) a reviewed candidate may replace (user-reported fixes only)')
    args=parser.parse_args()
    queue=json.loads(QUEUE.read_text(encoding='utf-8'));library=json.loads(LIBRARY.read_text(encoding='utf-8'))
    record=json.loads(DONE.read_text(encoding='utf-8')) if DONE.exists() else {}
    done=record.get('installed',[]);rejected=record.get('rejected',[])
    for source,reason in args.reject:
        c=next(c for c in queue['ready_candidates'] if c['source']==source)
        rejected.append(dict(source=source,bindings=c['bindings'],drawing_sha256=c['file_sha256']['drawing'],reason=reason,date=__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')))
    if args.reject:save(done,rejected)
    ready,refused=check(queue,done,library,rejected)
    if args.only:ready=[r for r in ready if r[0]['source'] in args.only]
    ready=[r for r in ready if r[0]['source'] not in args.skip]
    OUT.mkdir(parents=True,exist_ok=True)
    for c,problems in refused:print('REFUSED',c['source'],c['bindings'],problems)
    for c,_ in ready:
        residue=matte_residue(c)
        print('READY',c['source'],c['bindings'],f'MATTE RESIDUE in {len(residue)} parts {residue[:6]}' if residue else '')
    if not ready:print('nothing to install');return
    shown=OUT/'precheck.json'
    if args.apply:
        # Install only what the last visual check showed: a candidate listed
        # after the sheet was drawn has not been looked at.
        seen={(s,d) for s,d in json.loads(shown.read_text(encoding='utf-8'))} if shown.exists() else set()
        late=[c['source'] for c,_ in ready if (c['source'],c['file_sha256']['drawing']) not in seen]
        for source in late:print('NOT YET CHECKED (skipped this run)',source)
        ready=[r for r in ready if r[0]['source'] not in late]
        if not ready:print('nothing checked to install');return
    else:
        precheck_sheet(ready,OUT/'precheck.png');print('visual check:',OUT/'precheck.png')
        shown.write_text(json.dumps([(c['source'],c['file_sha256']['drawing']) for c,_ in ready]),encoding='utf-8')
        return
    stamp=__import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')
    backup=OUT/f'backup_{stamp}';backup.mkdir()
    for f in (LIBRARY,ROOT/'docs/PRODUCTION_ART_BATCH_CURRENT.json'):shutil.copy2(f,backup/f.name)
    # Each backup holds a 150 MB library copy; the latest three are enough to roll back.
    for old in sorted(OUT.glob('backup_*'))[:-3]:shutil.rmtree(old,ignore_errors=True)
    run=lambda *a:subprocess.run([sys.executable,'-X','utf8',*map(str,a)],cwd=ROOT,check=True)
    ready=split_mixed(ready,stamp)
    fresh=[r for r in ready if not r[0]['bindings']];ready=[r for r in ready if r[0]['bindings']]
    for c,_ in fresh:
        installed=install_new(c,library,stamp,run)
        done.append(installed);save(done,rejected)
        print('new parts',installed['bindings'],'flagged',installed['flagged'])
    if not ready:
        rebuild_caches(run,args)
        print('backup',backup);return
    jobs=[]
    for c,_ in ready:
        name=atlas_name(c);assert not (ROOT/'graphics'/('rework_'+name)).exists(),name
        job=dict(source=c['source'],bindings=c['bindings'],atlas=name,contract=c['contract'],drawing=c['drawing'],native=c['native'],generated=c['generated'],
            effect=any(library['bindings'][b-1].get('effect_part') for b in c['bindings']))
        if c.get('nested'):job['nested']=True
        jobs.append(job)
    config=OUT/f'config_{stamp}.json';results=f'test_current/parts/pending_install/results_{stamp}.json'
    originals=sorted({b for job in jobs for b in job['bindings'] if b<=5263})
    assert set(originals)<=set(args.allow_original),('candidate replaces original bindings not named with --allow-original',originals)
    config.write_text(json.dumps(dict(results=results,jobs=jobs,allow_original=originals),ensure_ascii=False,indent=2),encoding='utf-8')
    run('test_current/parts/root_pending_repair_factory.py',config)
    run('test_current/parts/record_completed_art_batch.py',results)
    ids=[b for job in jobs for b in job['bindings']]
    run('scripts/verify/verify_new_art.py','--bindings',*ids,'--out','test_current/parts/pending_install/check')
    report=json.loads((OUT/'check/report.json').read_text(encoding='utf-8'))
    installed=json.loads((ROOT/results).read_text(encoding='utf-8'))
    for (c,_),row in zip(ready,installed):
        done.append(dict(source=c['source'],bindings=row['bindings'],atlas=row['atlas'],drawing_sha256=c['file_sha256']['drawing'],installed=stamp,
            flagged=[p['binding'] for p in report['parts'] if p['binding'] in row['bindings']]))
    save(done,rejected)
    rebuild_caches(run,args)
    print('installed',len(ids),'flagged',report['flagged'],'backup',backup)


def split_mixed(ready,stamp):
    """A package may hold both replacements (rows with replace_binding) and new
    parts (rows listed in new_source_keys). Install them as two entries over
    the same drawing, each with its own filtered contract."""
    out=[]
    for c,problems in ready:
        if not (c['bindings'] and c.get('new_source_keys')):out.append((c,problems));continue
        folder=ROOT/Path(c['source'].replace('\\','/'));rows=json.loads((folder/c['contract']).read_text(encoding='utf-8'))
        keyof=lambda r:(r.get('source_contract') or r)['hash']
        new_keys={k['hash'] if isinstance(k,dict) else int(k) for k in c['new_source_keys']}
        replace=[r for r in rows if r.get('replace_binding') is not None];fresh=[r for r in rows if r.get('replace_binding') is None]
        assert {keyof(r) for r in fresh}==new_keys,('new rows differ from new_source_keys',c['source'])
        assert sorted(int(r['replace_binding']) for r in replace)==sorted(c['bindings']),('replacement rows differ from bindings',c['source'])
        name=folder.name
        for part,kind in ((replace,'replace'),(fresh,'new')):
            path=OUT/f'split_{stamp}_{name}_{kind}.json';path.write_text(json.dumps(part,ensure_ascii=False),encoding='utf-8')
            entry=dict(c,contract=str(path),bindings=c['bindings'] if kind=='replace' else [])
            if kind=='replace':entry.pop('new_source_keys',None)
            out.append((entry,problems))
        print('split',c['source'],len(replace),'replacements',len(fresh),'new')
    return out


def rebuild_caches(run,args):
    """Caches derived from the part library: material slots for runtime
    recolouring and the 8x8 tile library for parts the game assembles from
    tiles at run time. Without this, newly installed art is missing there."""
    if args.no_caches:print('caches NOT rebuilt (--no-caches)');return
    run('scripts/build/build_native_material_cache.py')
    run('scripts/assets/build_material_slot_cache.py')
    # A running player keeps the tile library open; the new one then waits as
    # parts_tile_library.tmp.sqlite and is swapped in once the player is closed.
    done=subprocess.run([sys.executable,'-X','utf8','scripts/assets/build_tile_library.py'],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
    if done.returncode:
        waiting=(ROOT/'graphics/parts_tile_library.tmp.sqlite').exists()
        print('tile library NOT swapped'+(' (player running; new file waits as parts_tile_library.tmp.sqlite)' if waiting else ''),done.stderr.strip().splitlines()[-1:] if done.stderr else '')


def install_new(c,library,stamp,run):
    """Connect parts that have no binding yet (new_source_keys) as new bindings."""
    folder=ROOT/Path(c['source'].replace('\\','/'));rows=json.loads((folder/c['contract']).read_text(encoding='utf-8'))
    # Nested contracts carry the observed source row inside, the atlas box outside.
    rows=[dict(r['source_contract'],atlas_box=r['atlas_box'],**{k:v for k,v in r.items() if k not in ('source_contract','atlas_box')}) if 'source_contract' in r else r for r in rows]
    for r in rows:
        if 'actual_palette_bgr555' not in r and 'palette_15bit' in r:r['actual_palette_bgr555']=r['palette_15bit']
        if 'actual_palette_rgb' not in r:r['actual_palette_rgb']=[[(v&31)*255//31,((v>>5)&31)*255//31,((v>>10)&31)*255//31] for v in r['actual_palette_bgr555']]
    active={b['hash'] for b in library['bindings'] if b.get('rgb_enabled',True) and not b.get('disabled')}
    taken=[r['hash'] for r in rows if r['hash'] in active]
    assert not taken,('already connected; a new part would duplicate it',taken)
    keys=[k['hash'] if isinstance(k,dict) else int(k) for k in c.get('new_source_keys',[])]
    assert sorted(r['hash'] for r in rows)==sorted(keys),'contract rows differ from new_source_keys'
    for n,r in enumerate(rows):
        assert 'replace_binding' not in r and 'replacement_of_existing_binding' not in r
        r.setdefault('slot',r.get('oam',n))
        # The source position is a record only (lookup is by hash); an
        # unconfirmed candidate position is used when no confirmed one exists.
        box=r.get('source_box') or r.get('source_box_candidate') or [None,None]
        r.setdefault('spec',dict(resource=r.get('resource',r.get('source_owner',r.get('source_image_candidate'))),source_x=r.get('source_x',box[0]),source_y=r.get('source_y',box[1])))
    contract=OUT/f'new_contract_{stamp}_{folder.name}.json';contract.write_text(json.dumps(rows,ensure_ascii=False),encoding='utf-8')
    name=atlas_name(c)+'_new'+str(len(rows));assert not (ROOT/'graphics'/('rework_'+name)).exists(),name
    flags=['--defer-shape-review','--new-only','--apply']
    if all(r.get('render_mode')=='static' for r in rows):flags.append('--static-palette')
    if any(r.get('effect_part') for r in rows):flags.append('--effect')
    report=folder/'install_report.json';before=report.stat().st_mtime if report.exists() else None
    run('scripts/assets/install_great_mazinger_pose.py','--source-dir',folder,'--contract',contract,'--drawing',c['drawing'],'--native',c['native'],'--generated',c['generated'],
        '--atlas-id',name,'--graphics-dir','rework_'+name,*flags)
    assert report.exists() and report.stat().st_mtime!=before,'installer wrote no report'
    ids=[p['binding'] for p in json.loads(report.read_text(encoding='utf-8'))['parts'] if not p.get('skipped_existing')]
    assert len(ids)==len(rows),ids
    shutil.copy2(report,ROOT/'graphics'/('rework_'+name)/'install_report.json')
    run('scripts/assets/bake_parts.py','--workers','4','--bindings',*ids)
    results=OUT/f'results_{stamp}_{folder.name}.json'
    results.write_text(json.dumps([dict(source=c['source'],atlas=name,folder='rework_'+name,bindings=ids)],indent=2),encoding='utf-8')
    run('test_current/parts/record_completed_art_batch.py',results.relative_to(ROOT))
    run('scripts/verify/verify_new_art.py','--bindings',*ids,'--out','test_current/parts/pending_install/check')
    check=json.loads((OUT/'check/report.json').read_text(encoding='utf-8'))
    return dict(source=c['source'],bindings=ids,atlas=name,drawing_sha256=c['file_sha256']['drawing'],installed=stamp,new_parts=True,flagged=[p['binding'] for p in check['parts']])


def save(done,rejected):
    DONE.write_text(json.dumps(dict(note='Candidates from PENDING_ART_INSTALL_QUEUE.json that install_pending_art.py connected and baked, and drawings rejected at the visual check. A listed drawing is not offered again; a new drawing for the same parts is.',
        installed=done,rejected=rejected),ensure_ascii=False,indent=1),encoding='utf-8')


if __name__=='__main__':main()
