# Build with the pinned requirements and the project-local GPU packages.
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules,copy_metadata

root=Path(SPECPATH).parent
native=root/'emulator/desmume/desmume/src/frontend/libretro/desmume_libretro.dll'
binaries=[(str(native),'desmume/desmume/src/frontend/libretro')]+[(str(root/'emulator'/name),'.') for name in ('native_composition.dll','native_font_pixels.dll','native_font_scan.dll')]
datas=[(str(root/'emulator'/name),'.') for name in ('hd_parts_registration.py','tile_compositor.py','tile_group_paint.py')]
hidden=['portable_selftest','moderngl','_moderngl','glcontext','glcontext.wgl','pygame._sdl2.video','pygame._sdl2.controller','PIL.WebPImagePlugin','PIL._webp']
hidden+=collect_submodules('glcontext')
for package in ('numpy','Pillow','pygame','pyinstaller'):
    datas+=copy_metadata(package)
a=Analysis([str(root/'emulator/portable_entry.py')],pathex=[str(root/'emulator'),str(root/'tools/gpu_py')],binaries=binaries,datas=datas,hiddenimports=hidden,excludes=['matplotlib','pandas','torch','onnxruntime','scipy','IPython','pytest'])
pyz=PYZ(a.pure)
exe=EXE(pyz,a.scripts,[],exclude_binaries=True,name='SRW_W_HD',console=False,debug=False,strip=False,upx=False,contents_directory='_internal')
coll=COLLECT(exe,a.binaries,a.datas,strip=False,upx=False,name='SRW_W_HD')
