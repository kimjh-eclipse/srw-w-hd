"""Produce a ROM-free Windows portable folder, notices, source and manifest."""
from pathlib import Path
import subprocess,sys,shutil,json,hashlib,zipfile,sqlite3
ROOT=Path(__file__).resolve().parent.parent
TARGET=ROOT/'dist/SRW_W_HD'

def main():
    if sys.platform!='win32':raise SystemExit('Build this Windows distribution on Windows.')
    subprocess.run([sys.executable,str(ROOT/'emulator/build_text_patterns.py')],cwd=ROOT,check=True)
    subprocess.run([sys.executable,'-m','PyInstaller','--noconfirm','--clean','--distpath',str(ROOT/'dist'),'--workpath',str(ROOT/'build/portable'),str(ROOT/'distribution/SRW_W_HD.spec')],cwd=ROOT,check=True)
    assets=[]
    for source in (ROOT/'graphics').rglob('*'):
        if not source.is_file() or source.name.startswith('parts_registered.sqlite') or source.suffix in ('.lock','.html') or source.name.endswith(('-wal','-shm')):continue
        if source.suffix.lower() not in ('.png','.json','.npz','.npy','.sqlite','.md','.txt','.otf'):continue
        dest=TARGET/source.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest);assets.append(source.relative_to(ROOT).as_posix())
    (TARGET/'roms').mkdir(exist_ok=True)
    (TARGET/'portable.txt').write_text('Settings, saves and generated cache are stored in data/.\n',encoding='utf-8')
    (TARGET/'사용방법.txt').write_text('슈퍼로봇대전 W HD\n\n1. 압축을 모두 풉니다.\n2. SRW_W_HD.exe를 실행합니다. Python 설치는 필요 없습니다.\n3. 파일 → 롬 열기에서 본인의 한글 1.0.8 롬을 선택합니다.\n\n롬과 세이브는 포함되어 있지 않습니다.\n설정과 세이브는 data 폴더에 저장됩니다. 업데이트할 때 data 폴더를 보존하세요.\nHD 그림을 사용하므로 graphics 폴더도 실행 파일과 함께 보관하세요.\n게임패드와 키 설정은 설정 메뉴에서 변경할 수 있습니다.\n\n소스와 라이선스: source 및 licenses 폴더\n소스 저장소: https://github.com/kimjh-eclipse/srw-w-hd\n',encoding='utf-8')
    licenses=TARGET/'licenses';licenses.mkdir(exist_ok=True)
    for source in (Path(sys.base_prefix)/'LICENSE.txt',ROOT/'REPOSITORY.md'):
        if source.exists():shutil.copy2(source,licenses/source.name)
    # Include matching sources from the working tree, not an older commit.
    source_dir=TARGET/'source';source_dir.mkdir(exist_ok=True)
    tracked=subprocess.check_output(['git','ls-files','-z','emulator','distribution','REPOSITORY.md','README.md'],cwd=ROOT).decode().split('\0')
    candidates=set(x for x in tracked if x)
    candidates.update(p.relative_to(ROOT).as_posix() for p in (ROOT/'distribution').glob('*') if p.is_file())
    candidates.update(p.relative_to(ROOT).as_posix() for p in (ROOT/'emulator').glob('portable*.py'))
    candidates.add('emulator/runtime_paths.py');candidates.add('emulator/build_text_patterns.py')
    with zipfile.ZipFile(source_dir/'source.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
        for name in sorted(candidates):
            source=ROOT/name
            if source.is_file() and source.suffix.lower() not in ('.dll','.exe','.state','.nds','.bin','.log','.npz','.npy','.json','.png','.wav','.pcm') and source.name!='player_settings.json':archive.write(source,name)
    core_license=ROOT/'emulator/desmume/desmume/COPYING'
    if core_license.exists():shutil.copy2(core_license,licenses/'DeSmuME-GPL.txt')
    manifest=[]
    forbidden={'.nds','.gba','.iso','.rom','.state','.sav','.dsv','.srm','.key','.pem'}
    for file in sorted(TARGET.rglob('*')):
        if not file.is_file() or 'data' in file.relative_to(TARGET).parts:continue
        assert file.suffix.lower() not in forbidden,file
        manifest.append(dict(path=file.relative_to(TARGET).as_posix(),bytes=file.stat().st_size,sha256=hashlib.sha256(file.read_bytes()).hexdigest()))
    (TARGET/'distribution_manifest.json').write_text(json.dumps(dict(format=1,python_install_required=False,roms_included=False,saves_included=False,files=manifest),indent=2),encoding='utf-8')
    print(json.dumps(dict(executable=str(TARGET/'SRW_W_HD.exe'),files=len(manifest),bytes=sum(x['bytes'] for x in manifest)),ensure_ascii=False),flush=True)

if __name__=='__main__':main()
