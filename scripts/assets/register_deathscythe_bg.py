"""Register the Deathscythe yellow lightning (two alternating frames) and rock ring BG effects as cut-ins.

Signatures were read from the live source state (source_mechanical_fixed_1_7_400,
frames 1200/1205): both lightning frames share the image-origin probe of BG1
and are told apart by the 512-entry map window, as the core supports.
"""
import json,shutil,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT

SRC=ROOT/'test_current/parts/deathscythe_user_report';DST=ROOT/'graphics/mechanical_cutins/deathscythe'
ENTRIES=[('yellow_lightning_bg',27956,1,3360086054,2495998395),('yellow_lightning_bg_phase2',27957,1,3360086054,444596593),('rock_ring_bg',24640,2,2322043876,752023458)]


def main():
    path=ROOT/'graphics/cutins_library.json';lib=json.loads(path.read_text(encoding='utf-8'));cutins=lib['cutins'];DST.mkdir(parents=True,exist_ok=True)
    shutil.copy2(path,ROOT/'test_current/parts/pending_install/cutins_library.before_deathscythe_bg.json')
    next_id=max(c['id'] for c in cutins)+1
    for folder,img,layer,probe,window in ENTRIES:
        target=DST/f'{folder}_{img}_hd.png';shutil.copy2(SRC/folder/'candidate_960.png',target)
        rel=str(target.relative_to(ROOT/'graphics')).replace('\\','/')
        cutins[:]=[c for c in cutins if c.get('resource')!=img]
        cutins.append(dict(id=next_id,name=f'deathscythe_{folder}',layer=layer,layers=[layer],native_size=[256,128],image=rel,paint_image=rel,signatures=[probe],resource=img,
            signature_mode='image_origin',map_window_signature=window,map_window_entries=512,presentation_role='battle_effect_bg'))
        print(folder,'id',next_id);next_id+=1
    path.write_text(json.dumps(lib,ensure_ascii=False,indent=1),encoding='utf-8')


if __name__=='__main__':main()
