"""Reduce registered HD art to the 960-wide DS display budget, preserving native references."""
import hashlib,json,os,tempfile
from pathlib import Path
from PIL import Image
from render_resolution import MAX_WIDTH,MAX_HEIGHT

ROOT=Path(__file__).resolve().parent.parent
GRAPHICS=ROOT/'graphics'

def main():
    plan={};categories={};protected={'kazuma_parts_atlas_facefix.png'}
    def add(name,size,kind):
        name=str(name).replace('\\','/')
        if name in protected:return
        size=tuple(map(int,size))
        previous=plan.get(name,(0,0));plan[name]=(max(size[0],previous[0]),max(size[1],previous[1]));categories[name]=kind
    meta=json.loads((GRAPHICS/'kazuma_parts_library.json').read_text())
    flags=('auto_unit','auto_animation','auto_animation_reuse','auto_late_attack','auto_full_attack','auto_shared_attack','observed_generated','observed_reuse','disabled')
    for binding in meta['bindings']:
        if not any(binding.get(k) for k in flags):
            spec=meta.get('atlases',{}).get(binding.get('atlas_id'))
            if spec:protected.add(spec['image'])
    for spec in meta.get('atlases',{}).values():
        w,h=spec['native_size'];add(spec['image'],(w*4,h*4),'part_atlas')
    portraits=json.loads((GRAPHICS/'portraits/library.json').read_text())['portraits']
    for item in portraits:
        w,h=item['rectangle'][2:];add(item['path'],(round(w*MAX_WIDTH/256),round(h*MAX_HEIGHT/192)),'portrait')
    for catalog,key,prefix in [('scenario_backgrounds/library.json','backgrounds',''),('backgrounds/library.json','backgrounds',''),('battle_backgrounds/catalog.json','backgrounds','')]:
        path=GRAPHICS/catalog
        if not path.exists():continue
        data=json.loads(path.read_text())
        rows=data.get(key,data.get('items',data.get('resources',[])))
        for item in rows:
            if not item.get('image'):continue
            size=item.get('native_size')
            if size is None and item.get('native'):
                with Image.open(GRAPHICS/item['native']) as original:size=original.size
            if size:add(item['image'],(round(size[0]*MAX_WIDTH/256),round(size[1]*MAX_HEIGHT/192)),'background')
    for item in json.loads((GRAPHICS/'cutins_library.json').read_text())['cutins']:
        add(item['image'],(MAX_WIDTH,MAX_HEIGHT),'cutin')
    add('kazuma_cutin_hd.png',(MAX_WIDTH,MAX_HEIGHT),'cutin')
    # Icons are one 16x16 native tile, not a complete screen.
    for row in json.loads((GRAPHICS/'map_icons/library.json').read_text())['records']:
        if row.get('prepared'):add('map_icons/'+row['prepared'],(60,60),'map_icon')
    # Full maps can span several screens; budget by native world dimensions.
    for item in json.loads((GRAPHICS/'map_tiles/library.json').read_text())['maps']:
        if item.get('image'):add('map_tiles/'+item['image'],(round(item['width']*MAX_WIDTH/256),round(item['height']*MAX_HEIGHT/192)),'map')
    menu_path=GRAPHICS/'menu_units/scene_runtime.json';menu=json.loads(menu_path.read_text())
    basis=menu.get('source_width',1440)
    for name in menu['images'].values():
        with Image.open(GRAPHICS/'menu_units'/name) as image:
            add('menu_units/'+name,(round(image.width*MAX_WIDTH/basis),round(image.height*MAX_WIDTH/basis)),'menu')
    report=[]
    for name,size in sorted(plan.items()):
        path=GRAPHICS/name
        if not path.exists():continue
        before=path.stat().st_size
        with Image.open(path) as opened:
            if opened.width<=size[0] or opened.height<=size[1]:continue
            old_size=opened.size;original=opened.convert('RGBA' if 'A' in opened.getbands() else 'RGB')
            smaller=original.resize(size,Image.Resampling.LANCZOS)
        fd,temp=tempfile.mkstemp(suffix='.tmp.png',dir=path.parent);os.close(fd)
        try:
            smaller.save(temp,compress_level=9)
            with Image.open(temp) as check:
                assert check.size==size and check.tobytes()==smaller.tobytes()
            os.replace(temp,path)
        finally:
            if os.path.exists(temp):os.unlink(temp)
        report.append(dict(path=name,category=categories[name],old_size=old_size,new_size=size,before=before,after=path.stat().st_size))
    menu['source_width']=MAX_WIDTH;menu['display_scale']=MAX_WIDTH/256;menu_path.write_text(json.dumps(menu,indent=2))
    out=ROOT/'test_current/image_optimization/resized_art.json'
    previous={r['path']:r for r in json.loads(out.read_text())['entries']} if out.exists() else {}
    for row in report:
        if row['path'] in previous:
            row.update(before=previous[row['path']]['before'],old_size=previous[row['path']]['old_size'])
        previous[row['path']]=row
    report=list(previous.values())
    result=dict(reference_width=MAX_WIDTH,resized=len(report),saved_bytes=sum(r['before']-r['after'] for r in report),protected_approved_sources=sorted(protected),entries=report)
    out.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ['entries','protected_approved_sources']}))

if __name__=='__main__':main()
