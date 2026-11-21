from pathlib import Path
import json,hashlib,shutil
import numpy as np
from PIL import Image,ImageDraw
P=Path('test_current/ui/start_menu_user_repair');OLD=Path('test_current/ui/start_menu_hd_candidate');S=16
# Procedural vector UI from design vertices, not the native raster alpha.
def vector_panel(w,h,points,stops,stroke_points=None,stroke_color=None,stroke_width=1):
 mask=Image.new('L',(w*S,h*S));d=ImageDraw.Draw(mask);d.polygon([(round(x*S),round(y*S)) for x,y in points],fill=255)
 ys=np.arange(h*S,dtype=float)/S;st=np.array([v[0] for v in stops]);cols=np.array([v[1] for v in stops]);rgba=np.zeros((h*S,w*S,4),dtype='uint8')
 for ch in range(3):rgba[:,:,ch]=np.interp(ys,st,cols[:,ch])[:,None].astype('uint8')
 rgba[:,:,3]=np.array(mask);im=Image.fromarray(rgba)
 if stroke_points:
  draw=ImageDraw.Draw(im);draw.line([(round(x*S),round(y*S)) for x,y in stroke_points],fill=tuple(stroke_color)+(255,),width=round(stroke_width*S),joint='curve')
 return im.resize((w*4,h*4),Image.Resampling.LANCZOS)
selected_points=[(14,0),(50,0),(64,14),(64,18),(50,32),(14,32),(0,18),(0,14)]
selected_stops=[(0,(0,148,148)),(7,(0,148,148)),(11,(0,123,131)),(15,(0,106,106)),(18,(0,90,90)),(22,(0,74,74)),(25,(0,49,49)),(28,(0,32,32)),(32,(0,16,16))]
selected=vector_panel(64,32,selected_points,selected_stops,[(0,14),(14,0.5),(50,0.5),(64,14)],(0,255,255),1)
gray_points=[(40,2),(72,2),(80,10),(80,14),(72,22),(40,22),(32,14),(32,10)]
gray_stops=[(2,(82,82,82)),(6,(82,82,82)),(9,(74,74,74)),(12,(57,57,57)),(15,(41,41,41)),(18,(24,24,24)),(22,(8,8,8))]
gray=vector_panel(80,24,gray_points,gray_stops,[(32,10),(40,2.5),(72,2.5),(80,10)],(139,139,139),1)
old=Image.open(OLD/'candidate_atlas.png').convert('RGBA');candidate=old.copy();candidate.paste(gray.crop((128,0,320,96)),(128,0));candidate.paste(selected,(0,128));candidate.save(P/'generated_master.png');shutil.copy2(P/'generated_master.png',P/'candidate_atlas.png');shutil.copy2(OLD/'native_atlas.png',P/'native_atlas.png');selected.save(P/'selected_panel_4x.png');gray.save(P/'gray_panel_4x.png')
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="64" viewBox="0 0 256 64"><defs><linearGradient id="cyan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#009494"/><stop offset=".22" stop-color="#009494"/><stop offset=".35" stop-color="#007b83"/><stop offset=".47" stop-color="#006a6a"/><stop offset=".56" stop-color="#005a5a"/><stop offset=".69" stop-color="#004a4a"/><stop offset=".78" stop-color="#003131"/><stop offset=".88" stop-color="#002020"/><stop offset="1" stop-color="#001010"/></linearGradient><linearGradient id="gray" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#525252"/><stop offset=".2" stop-color="#525252"/><stop offset=".35" stop-color="#4a4a4a"/><stop offset=".5" stop-color="#393939"/><stop offset=".65" stop-color="#292929"/><stop offset=".8" stop-color="#181818"/><stop offset="1" stop-color="#080808"/></linearGradient></defs><polygon points="40,2 72,2 80,10 80,14 72,22 40,22 32,14 32,10" fill="url(#gray)"/><path d="M32 10 L40 2.5 H72 L80 10" fill="none" stroke="#8b8b8b" stroke-width="1"/><g transform="translate(0 32)"><polygon points="14,0 50,0 64,14 64,18 50,32 14,32 0,18 0,14" fill="url(#cyan)"/><path d="M0 14 L14 .5 H50 L64 14" fill="none" stroke="#00ffff" stroke-width="1"/></g></svg>'''
(P/'panel_geometry.svg').write_text(svg,encoding='utf-8');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();proof=dict(method='Code-native polygon and gradient UI, supersampled vector rasterization; new analytic design vertices. Exact native alpha was not read or stamped by this producer.',selected_native_design_vertices=selected_points,gray_native_design_vertices=gray_points,source_IMG=23,source_PLT=22,source_resource_proof='../start_menu_source/ROM_resource_palette_proof.json',base_preserved_from=str(OLD/'candidate_atlas.png'),base_sha256=sha(OLD/'candidate_atlas.png'),preserved_art='Existing own generated labels and repeating line segments are unchanged outside modified parent regions.',modified_native_parent_regions=[[32,0,48,24],[0,32,64,32]],new_generated_UI_panels=2,new_generated_text=0,new_generated_title_logos=0,renderer_or_blend_modified=False,alpha_threshold_cleanup=False,source_alpha_stamped=False,generated_master_sha256=sha(P/'generated_master.png'));(P/'drawing_provenance.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2),encoding='utf-8')
rows=json.loads((OLD/'contract.json').read_text(encoding='utf-8'));lib=json.loads(Path('graphics/kazuma_parts_library.json').read_text(encoding='utf-8'));hm={b['hash']:(i+1,b) for i,b in enumerate(lib['bindings']) if b.get('rgb_enabled',True) and not b.get('disabled')};selected_rows=[];priors={};unchanged=[]
for r in rows:
 x,y,w,h=r['atlas_box'];before=old.crop((x*4,y*4,(x+w)*4,(y+h)*4));after=candidate.crop((x*4,y*4,(x+w)*4,(y+h)*4));bid,spec=hm[r['hash']]
 if np.array_equal(np.array(before),np.array(after)):unchanged.append(bid);continue
 c=dict(r,replace_binding=bid,binding_array_index=bid-1,binding_id=bid,slot=bid,spec=dict(resource=23,source_x=x,source_y=y),actual_observed=True,render_mode='static',dynamic_palette=False,indexed_safe=False,preserve_existing_lookup_flags=True,review_status='pending_claude',note='Procedural vector panel geometry repair; native45degree sides and topcap restored. Existing own wordart preserved. Sourcealpha not stamped.')
 selected_rows.append(c);priors[str(bid)]=hashlib.sha256(json.dumps(spec,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
(P/'contract.json').write_text(json.dumps(selected_rows,ensure_ascii=False,indent=2),encoding='utf-8');roles=dict(contract='contract.json',drawing='candidate_atlas.png',native='native_atlas.png',generated='generated_master.png');packet=dict(source=str(P).replace('\\','/'),bindings=[r['replace_binding'] for r in selected_rows],**roles,file_sha256={k:sha(P/f) for k,f in roles.items()},prior_binding_spec_sha256=priors,nested=True,note='선택/비선택패널의원본각도·길이복원. 기존문자와반복선보존. 코드native vectorUI2소재/타이틀새그림0. 실재생QA대기.');(P/'candidate_packet.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2),encoding='utf-8');print('changedbindings',packet['bindings'],'unchanged',unchanged)
for selected_index in range(3):
 rs=[r for r in json.loads(Path(f'test_current/ui/start_menu_source/selected_{selected_index}/actual_cached_obj_contracts.json').read_text(encoding='utf-8')) if r['engine']==0];canvas=Image.new('RGBA',(1024,768))
 for r in sorted(rs,key=lambda r:(r['priority'],r['oam']),reverse=True):
  match=next(c for c in rows if c['hash']==r['hash']);x,y,w,h=match['atlas_box'];part=candidate.crop((x*4,y*4,(x+w)*4,(y+h)*4));canvas.alpha_composite(part,(r['screen_x']*4,r['screen_y']*4))
 canvas.save(P/f'producer_selected{selected_index}.png');bed=Image.new('RGBA',canvas.size,(48,52,64,255));bed.alpha_composite(canvas);bed.convert('RGB').save(P/f'producer_selected{selected_index}_gray.png')
print('drawingSHA',sha(P/'candidate_atlas.png'))
