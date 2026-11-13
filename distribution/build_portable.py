"""Produce a ROM-free Windows portable folder, notices, source and manifest."""
from pathlib import Path
import subprocess,sys,shutil,json,hashlib,zipfile,sqlite3,argparse
from source_bundle import write_source_bundle
ROOT=Path(__file__).resolve().parent.parent
TARGET=ROOT/'dist/SRW_W_HD'

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--assets-only',action='store_true');parser.add_argument('--program-only',action='store_true');args=parser.parse_args()
    if sys.platform!='win32':raise SystemExit('Build this Windows distribution on Windows.')
    subprocess.run([sys.executable,str(ROOT/'scripts/assets/build_text_patterns.py')],cwd=ROOT,check=True)
    manifest_path=TARGET/'distribution_manifest.json'
    previous_manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else None
    if not args.assets_only:
        frozen_dist=ROOT/'build/frozen_update' if args.program_only else ROOT/'dist'
        subprocess.run([sys.executable,'-m','PyInstaller','--noconfirm','--clean','--distpath',str(frozen_dist),'--workpath',str(ROOT/'build/portable'),str(ROOT/'distribution/SRW_W_HD.spec')],cwd=ROOT,check=True)
        if args.program_only:shutil.copytree(frozen_dist/'SRW_W_HD',TARGET,dirs_exist_ok=True)
        # Same bundled interpreter and dependencies, with an explicit test entry.
        shutil.copy2(TARGET/'SRW_W_HD.exe',TARGET/'SRW_W_Test.exe')
    if not args.program_only:subprocess.run([sys.executable,str(ROOT/'distribution/prepare_images.py')],cwd=ROOT,check=True)
    optimization=json.loads((ROOT/'test_current/image_optimization/package_images.json').read_text())
    optimized={r['path']:r for r in optimization['entries'] if r.get('encoded')}
    assets=[];unchanged_assets=set();copied_assets=0
    for source in ([] if args.program_only else (ROOT/'graphics').rglob('*')):
        if not source.is_file() or source.name.startswith('parts_registered.sqlite') or source.suffix in ('.lock','.html') or source.name.endswith(('-wal','-shm')):continue
        if source.suffix.lower() not in ('.png','.json','.npz','.npy','.sqlite','.md','.txt','.otf'):continue
        relative=source.relative_to(ROOT);row=optimized.get(source.relative_to(ROOT/'graphics').as_posix())
        if row:source=ROOT/row['encoded'];relative=Path('graphics')/row['output']
        dest=TARGET/relative;dest.parent.mkdir(parents=True,exist_ok=True)
        source_stat=source.stat();target_stat=dest.stat() if dest.exists() else None
        if target_stat and (target_stat.st_size,target_stat.st_mtime_ns)==(source_stat.st_size,source_stat.st_mtime_ns):
            unchanged_assets.add(relative.as_posix())
        else:shutil.copy2(source,dest);copied_assets+=1
        assets.append(relative.as_posix())
    print(json.dumps(dict(copied_assets=copied_assets,unchanged_assets=len(unchanged_assets))),flush=True)
    (TARGET/'image_optimization.json').write_text(json.dumps({k:v for k,v in optimization.items() if k!='entries'},indent=2),encoding='utf-8')
    # Retain the already-prepared portraits: only their packaged file stamps
    # changed, not the portrait identities or source design.
    sys.path.insert(0,str(ROOT/'emulator'))
    import hd_portraits
    portrait_db=TARGET/'graphics/portraits/prepared.sqlite'
    if portrait_db.exists() and not args.program_only:
        unchanged_assets.discard('graphics/portraits/prepared.sqlite')
        with sqlite3.connect(portrait_db) as db:
            for item in json.loads((ROOT/'graphics/portraits/library.json').read_text())['portraits']:
                stamp=[f'portrait-registration-3-{hd_portraits.MAX_WIDTH}']
                for key in ('path','portrait_mask'):
                    if item.get(key):
                        path=TARGET/'graphics'/item[key]
                        if not path.exists():path=path.with_suffix('.webp')
                        stat=path.stat();stamp.extend((str(stat.st_mtime_ns),str(stat.st_size)))
                db.execute('UPDATE art SET stamp=? WHERE path=? AND stamp=?',(':'.join(stamp),item['path'],hd_portraits._asset_stamp(item)))
    (TARGET/'roms').mkdir(exist_ok=True)
    (TARGET/'portable.txt').write_text('Settings, saves and generated cache are stored in data/.\n',encoding='utf-8')
    (TARGET/'사용방법.txt').write_text('슈퍼로봇대전 W HD\n\n1. 압축을 모두 풉니다.\n2. SRW_W_HD.exe를 실행합니다. Python 설치는 필요 없습니다.\n3. 파일 → 롬 열기에서 본인의 한글 1.0.8 롬을 선택합니다.\n\n롬과 세이브는 포함되어 있지 않습니다.\n설정과 세이브는 data 폴더에 저장됩니다. 업데이트할 때 data 폴더를 보존하세요.\nHD 그림을 사용하므로 graphics 폴더도 실행 파일과 함께 보관하세요.\n게임패드와 키 설정은 설정 메뉴에서 변경할 수 있습니다.\n\n소스와 라이선스: source 및 licenses 폴더\n소스 저장소: https://github.com/kimjh-eclipse/srw-w-hd\n',encoding='utf-8')
    licenses=TARGET/'licenses';licenses.mkdir(exist_ok=True)
    for source in (Path(sys.base_prefix)/'LICENSE.txt',ROOT/'REPOSITORY.md'):
        if source.exists():shutil.copy2(source,licenses/source.name)
    # Include matching sources from the working tree, not an older commit.
    source_dir=TARGET/'source';source_dir.mkdir(exist_ok=True)
    write_source_bundle(source_dir/'source.zip')
    core_license=ROOT/'emulator/desmume/desmume/COPYING'
    if core_license.exists():shutil.copy2(core_license,licenses/'DeSmuME-GPL.txt')
    manifest=[]
    previous_assets={r['path']:r for r in previous_manifest['files'] if r['path'].startswith('graphics/')} if previous_manifest else {}
    forbidden={'.nds','.gba','.iso','.rom','.state','.sav','.dsv','.srm','.key','.pem'}
    for file in sorted(TARGET.rglob('*')):
        if not file.is_file() or 'data' in file.relative_to(TARGET).parts or file.name=='distribution_manifest.json':continue
        assert file.suffix.lower() not in forbidden,file
        name=file.relative_to(TARGET).as_posix()
        reusable=name in previous_assets and (args.program_only or name in unchanged_assets) and previous_assets[name]['bytes']==file.stat().st_size
        manifest.append(previous_assets[name] if reusable else dict(path=name,bytes=file.stat().st_size,sha256=hashlib.sha256(file.read_bytes()).hexdigest()))
    (TARGET/'distribution_manifest.json').write_text(json.dumps(dict(format=1,python_install_required=False,roms_included=False,saves_included=False,files=manifest),indent=2),encoding='utf-8')
    print(json.dumps(dict(executable=str(TARGET/'SRW_W_HD.exe'),files=len(manifest),bytes=sum(x['bytes'] for x in manifest)),ensure_ascii=False),flush=True)

if __name__=='__main__':main()
