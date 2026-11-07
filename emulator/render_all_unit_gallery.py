"""Assemble ROM-native poses with the same per-part painter as the player.

This checks static PAT assembly. Gameplay is verified separately; this does not
claim to exercise every attack in the game.
"""
from pathlib import Path
import json,sys,math,time
import numpy as np
from PIL import Image,ImageDraw
from hd_parts import PartsRenderer,SCALE,ROOT

OUT=ROOT/'graphics/all_units';catalog=json.loads((OUT/'catalog.json').read_text())
installed=json.loads((OUT/'installed.json').read_text());coverage={p['resource']:p['bindings'] for p in installed['coverage']}
if installed['missing_images'] and '--partial' not in sys.argv:raise RuntimeError('Some HD sheets are still pending')
renderer=PartsRenderer();lookup={b['hash']:i for i,b in enumerate(renderer.bindings,1) if b.get('rgb_enabled',True)}
started=time.time();cards=[];report=[]
for package in catalog['packages']:
    resource=package['resource']
    if resource>=3500 or resource not in coverage:continue
    filename=f'unit_{resource}_hd_pose.png';target=OUT/filename
    if not target.exists() or '--refresh' in sys.argv:
        image=Image.new('RGBA',(1440,1080));pose=next(p for p in package['poses'] if p)
        native_parts={(p['x'],p['y'],p['w'],p['h']):p for p in package['parts']}
        count=0
        palette=np.asarray(package['palette_rgb'],dtype='uint32');five=(palette*31+127)//255
        colors=(five[:,0]|(five[:,1]<<5)|(five[:,2]<<10)).astype('uint16')
        for part in reversed(pose):
            source=native_parts.get((part['u'],part['v'],part['w'],part['h']))
            if not source:continue
            assert source['hash'] in lookup,(resource,source)
            binding=lookup[source['hash']];spec=renderer.bindings[binding-1]
            assert (spec['w'],spec['h'])==(part['w'],part['h'])
            # In-game mirroring/affine motion comes from actual OAM. This
            # reference pose follows the same canonical source orientation.
            row=np.array([binding,0,0,0,source['hash'],0,0,0],dtype='uint32')
            art=renderer.sprite(row,bytes(1024),colors)
            image.alpha_composite(art,(round((128+part['x'])*SCALE),round((100+part['y'])*SCALE)));count+=1
        assert count and image.getbbox(),(resource,'empty assembly')
        image.save(target)
        report.append(dict(resource=resource,parts=count))
    cards.append(dict(number=len(cards)+1,native=f'unit_{resource}_pose.png',hd=filename))
    if len(cards)%24==0:(OUT/'gallery_progress.json').write_text(json.dumps(dict(assembled=len(cards),seconds=round(time.time()-started,1))))
html='''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>슈퍼로봇대전 W HD 기체 미리보기</title>
<style>*{box-sizing:border-box}body{margin:0;background:#10151f;color:#eef3fa;font:16px "Malgun Gothic",sans-serif}header{position:sticky;top:0;background:#10151ff2;padding:20px 5vw;border-bottom:1px solid #334156;z-index:1}h1{font-size:23px;margin:0 0 10px}p{margin:8px 0;color:#b6c5d9}button{border:1px solid #526582;background:#1d2c44;color:white;border-radius:8px;padding:10px 20px;cursor:pointer}button.active{background:#246bd4}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:12px;padding:24px 5vw}.card{padding:10px;background:#192333;border:1px solid #334156;border-radius:12px;text-align:center;cursor:pointer}.card img{width:100%;aspect-ratio:4/3;object-fit:contain}dialog{background:#10151f;color:white;border:1px solid #526582;border-radius:12px;width:min(94vw,1200px);padding:18px}dialog::backdrop{background:#000b}dialog img{width:100%;max-height:75vh;object-fit:contain}.bar{display:flex;gap:12px;align-items:center;flex-wrap:wrap}</style>
<header><h1>슈퍼로봇대전 W · HD 기체 미리보기</h1><div class="bar"><button id="hd" class="active">HD 보기</button><button id="native">원본 보기</button><span id="count"></span></div><p>기체를 누르면 크게 볼 수 있습니다. 변형·무장 형태와 같은 그림을 쓰는 형태도 포함합니다.</p></header><main class="grid" id="grid"></main><dialog id="dialog"><button id="close">닫기</button><img id="large" alt="선택한 기체"></dialog>
<script>const cards=__CARDS__;let hd=true,chosen=null;const grid=document.getElementById('grid'),dialog=document.getElementById('dialog');document.getElementById('count').textContent=cards.length+'개 형태';for(const c of cards){const e=document.createElement('div');e.className='card';const im=document.createElement('img');im.loading='lazy';im.src=c.hd;im.alt='기체 '+c.number;e.append(im);const label=document.createElement('div');label.textContent='기체 '+c.number;e.append(label);e.onclick=()=>{chosen=c;document.getElementById('large').src=hd?c.hd:c.native;dialog.showModal()};grid.append(e)}function mode(value){hd=value;document.getElementById('hd').classList.toggle('active',hd);document.getElementById('native').classList.toggle('active',!hd);[...grid.querySelectorAll('img')].forEach((im,i)=>im.src=hd?cards[i].hd:cards[i].native);if(chosen)document.getElementById('large').src=hd?chosen.hd:chosen.native}document.getElementById('hd').onclick=()=>mode(true);document.getElementById('native').onclick=()=>mode(false);document.getElementById('close').onclick=()=>dialog.close();</script></html>'''
(OUT/'index.html').write_text(html.replace('__CARDS__',json.dumps(cards)),encoding='utf-8')
result=dict(kind='static ROM PAT assembly; not full-game gameplay coverage',forms=len(cards),newly_rendered=len(report),prepared_parts=len(renderer.prepared),loaded_lazy_atlases=len(renderer.lazy_atlases),seconds=round(time.time()-started,1))
assert len(renderer.lazy_atlases)<=4 and len(renderer.prepared)<=512
(OUT/'gallery_report.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
