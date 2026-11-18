"""Add the drawing brief to the cut-in request packets made by build_cutin_request_packet.py.

For each packet: reference_screen_4x.png (top 128 rows of the live screen, 4x - the cut-in as
shown, effects included) and reference_clean_4x.png (only the ROM pictures of the cut-in layers,
placed at the matched scroll, back to front - no HUD, no text, no OBJ effects). Writes the
'deliver' block into contract.json. Nothing is installed.

  py -3.11 -X utf8 scripts/assets/finish_cutin_request_packets.py
"""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT

OUT=ROOT/'test_current/parts/cutin_requests'
COMMON=('Draw over the native at the same place and the same size (4x nearest of the native canvas = the drawing canvas). '
        'No recolouring: colours come from the native/live picture. Outside the native silhouette alpha 0; inside fully opaque '
        '(no soft halo, no threshold-cut edge). Do not paint the HUD, the text box or OBJ effects (sparks, glow, lightning). '
        'Claude splits and connects; the library is not touched by the drawer.')
BRIEF={
 'mazinkaiser_fire_blaster':dict(item=3,deliver=[
   dict(file='candidate_23021.png',size=[1024,576],over='native_23021_4x.png',
        what='Mazinkaiser upper-body close-up (BG1 IMG23021). Black armour, red V chest plate with the round gem, silver face and horns, both fists. '
             'Transparent (alpha 0) where native_23021 is transparent. The cyan V glow seen in the game is an OBJ effect drawn on top - keep the RED native chest plate.'),
   dict(file='candidate_24557.png',size=[1024,512],over='native_24557_4x.png',
        what='Green-yellow background (BG2 IMG24557). Fully opaque. It scrolls left continuously under the robot, so the left and right edges must join seamlessly (horizontal tiling).')],
   notes='The two layers move independently (BG2 scrolls 4 px per 8 frames, BG1 is fixed), so they are two drawings, not one picture. Same picture in unit 296 weapon 1200.'),
 'creuset_helmet':dict(item=2,deliver=[
   dict(file='candidate_22864.png',size=[960,576],over='native_22864_4x.png',
        what='Creuset bust (BG1 IMG22864, 30 map columns): white helmet with orange stripe, his white MASK over the eyes, blond hair inside the helmet, purple suit. '
             'The existing HD (graphics/pilot_cutins/cutin_22864_hd.png) shows the face without the mask - wrong, use it only for line style. Transparent outside the native silhouette.'),
   dict(file='candidate_26391.png',size=[1024,1024],over='native_26391_4x.png',
        what='Blue scanline background (BG2 IMG26391) in the shown blue colours. Fully opaque. It scrolls down continuously, so top and bottom edges must join seamlessly (vertical tiling); keep the vertical streak texture and the dark/light blob pattern.')],
   notes='The game uses the same IMG26391 with a red palette elsewhere; this request is the blue one shown here (native_26391.png is decoded with the live palette). '
         'The figure bobs a few pixels vertically; the background scrolls ~10 px per frame.'),
 'taiga_goldion_stage':dict(item=1,deliver=[
   dict(file='candidate_23591.png',size=[1024,1024],over='native_23591_4x.png',
        what='Stage behind Taiga (BG3 IMG23591): two dark green pillars meeting in the centre with the zig-zag crack, brown-red curved walls left and right. Fully opaque, the whole 256x256 canvas '
             '(the camera pans from row 123 up to row 14, so all of it is seen).')],
   notes='Figure (BG2 IMG23588/23589/23590, three hair frames, streamed while the camera pans) is not part of this request: our renderer check shows no HD connected for it either, '
         'but the user reported it as already HD, so Claude confirms first. Live captures are in figure_*_f*/ for reference only.'),
}


def main():
    for name,b in BRIEF.items():
        d=OUT/name;c=json.loads((d/'contract.json').read_text(encoding='utf-8'))
        live=Image.open(d/'live_native.png').convert('RGB')
        live.crop((0,0,256,128)).resize((1024,512),Image.Resampling.NEAREST).save(d/'reference_screen_4x.png')
        clean=np.zeros((128,256,4),dtype='uint8')
        prio={row['bg']:row['priority'] for row in c['layers']}
        for cv in sorted(c['drawing_canvases'],key=lambda v:-prio[v['bg']]):   # back to front
            pic=np.asarray(Image.open(d/cv['native']).convert('RGBA'));info=c['bg_layout'][cv['bg']];W,H=info[5],info[6]
            plane=np.zeros((H,W,4),dtype='uint8');plane[:min(H,pic.shape[0]),:min(W,pic.shape[1])]=pic[:H,:W]
            sx,sy=cv['matched_scroll'];view=np.roll(np.roll(plane,-sy,0),-sx,1)[:128,:256];m=view[:,:,3]>0;clean[m]=view[m]
        Image.fromarray(clean).resize((1024,512),Image.Resampling.NEAREST).save(d/'reference_clean_4x.png')
        c['request']=dict(todo_item=b['item'],deliver=b['deliver'],notes=b['notes'],rules=COMMON,
            references=['reference_screen_4x.png (as shown, top 128 rows)','reference_clean_4x.png (only these layers, ROM pictures at the matched scroll)']+[cv['native_4x'] for cv in c['drawing_canvases']])
        (d/'contract.json').write_text(json.dumps(c,ensure_ascii=False,indent=1),encoding='utf-8');print(name,'ok')


if __name__=='__main__':main()
