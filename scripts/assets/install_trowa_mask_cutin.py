"""Connect Codex's one-piece Trowa half-mask cut-in (trowa_mask_cutin_user_report/candidate_full.png).

The picture is in screen space at 4x (1024x768, both BG scrolls are 0):
  BG2 IMG22818 (whole face)  -> cut-in id 15: image replaced, live map window used
  BG1 IMG22817 (hair)        -> new cut-in, layer 1, base-relative tile probe measured live
  OBJ OAM0-4 (mask and hand, IMG7152) -> new sprite parts: a one-pose set built from the
      captured sprites (rendered_obj225.json), split by front-most sprite and installed
      through the normal installer.
The renderer shows each BG picture only where that BG is visible natively, so the
same full picture serves both BG layers.

  py -3.11 -X utf8 scripts/assets/install_trowa_mask_cutin.py
"""
import json,shutil,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from PIL import Image
from scripts.assets.build_object_packets import compose_canvas

SRC=ROOT/'test_current/parts/trowa_mask_cutin_user_report'
PY=[sys.executable,'-X','utf8']


def bg_picture(size_native,path):
    """Screen-space 4x drawing -> BG plane picture at the library's 3.75x scale (960 per 256)."""
    art=Image.open(SRC/'candidate_full.png').convert('RGBA')
    scale=960/256;w,h=size_native
    plane=Image.new('RGBA',(round(w*scale),round(h*scale)))
    plane.alpha_composite(art.resize((round(256*scale),round(192*scale)),Image.Resampling.LANCZOS),(0,0))
    plane.save(path);return path


def main():
    lib_path=ROOT/'graphics/cutins_library.json';lib=json.loads(lib_path.read_text(encoding='utf-8'))
    shutil.copy2(lib_path,ROOT/'test_current/parts/pending_install/cutins_library.before_trowa_mask.json')
    dst=ROOT/'graphics/pilot_cutins/trowa_mask';dst.mkdir(parents=True,exist_ok=True)
    face=bg_picture((256,256),dst/'trowa_mask_bg2_22818_hd.png');hair=bg_picture((512,512),dst/'trowa_mask_bg1_22817_hd.png')
    rel=lambda p:str(p.relative_to(ROOT/'graphics')).replace('\\','/')
    for c in lib['cutins']:
        if c['id']==15:
            c['image']=c['paint_image']=rel(face)
            c['map_window_signature']=c.pop('map_window_live_measured',c['map_window_signature']);c.pop('held_reason',None)
            c['note']='Trowa half-mask cut-in face (BG2); Codex one-piece drawing 11/15, map window measured live'
    lib['cutins']=[c for c in lib['cutins'] if c.get('name')!='trowa_mask_hair_22817']
    lib['cutins'].append(dict(id=max(c['id'] for c in lib['cutins'])+1,name='trowa_mask_hair_22817',resource=22817,layer=1,layers=[1],native_size=[512,512],
        image=rel(hair),paint_image=rel(hair),signatures=[1058631903],presentation_role='pilot_foreground',
        note='Trowa half-mask cut-in hair (BG1); base-relative probe measured at unit_2 weapon 12 frame 225'))
    lib_path.write_text(json.dumps(lib,ensure_ascii=False,indent=1),encoding='utf-8')
    print('cut-ins: id 15 face replaced, hair added as id',lib['cutins'][-1]['id'])
    # OBJ mask and hand as a one-pose set
    rows=json.loads((SRC/'rendered_obj225.json').read_text(encoding='utf-8'))
    rs=ROOT/'test_current/parts/pose_packets/trowa_mask_cutin/robot_set';pose=rs/'pose_00'
    if rs.exists():shutil.rmtree(rs)
    pose.mkdir(parents=True)
    # Sprites may hang off the screen edge: work on a canvas that holds them all.
    ox=max(0,-min(r['screen_x'] for r in rows));oy=max(0,-min(r['screen_y'] for r in rows))
    W=max(256+ox,max(r['screen_x']+r['w'] for r in rows)+ox);H=max(192+oy,max(r['screen_y']+r['h'] for r in rows)+oy)
    rows=[dict(r,screen_x=r['screen_x']+ox,screen_y=r['screen_y']+oy) for r in rows]
    canvas,_=compose_canvas(rows,W,H)
    Image.fromarray(canvas).save(pose/'native.png');Image.fromarray(canvas).resize((W*4,H*4),Image.Resampling.NEAREST).save(pose/'native_4x.png')
    (pose/'contract.json').write_text(json.dumps(rows,ensure_ascii=False),encoding='utf-8');(pose/'frames.json').write_text(json.dumps(dict(frames=[225])),encoding='utf-8')
    drawing=Image.new('RGBA',(W*4,H*4));drawing.alpha_composite(Image.open(SRC/'candidate_full.png').convert('RGBA'),(ox*4,oy*4))
    drawing.save(pose/'candidate_fit.png')   # Codex placed it in screen space; only shifted by the canvas margin
    (rs/'DRAWINGS_STATUS.json').write_text(json.dumps({'pose_00':dict(state='accepted',note='Claude: Codex drawing placed in screen space')}),encoding='utf-8')
    for cmd in (['scripts/assets/split_object_drawings.py',str(rs),'--drawing','candidate_fit.png','--out',str(rs/'split_fit')],['scripts/assets/package_robot_set.py',str(rs)]):
        r=subprocess.run(PY+cmd,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace');print(r.stdout.strip()[-300:],r.stderr.strip()[-300:])


if __name__=='__main__':main()
