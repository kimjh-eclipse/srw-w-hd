"""Audit actual HD files separately from registration and game verification."""
import hashlib,json
from pathlib import Path
from collections import Counter
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent.parent;F=ROOT/'graphics/scenario_backgrounds';OUT=ROOT/'test_current/scenario_backgrounds'

def write(path,data):
    temporary=path.with_suffix('.tmp.json');temporary.write_text(json.dumps(data,indent=2));temporary.replace(path)

def main():
    catalog=json.loads((F/'catalog.json').read_text());rows=catalog['resources'];checks=[];missing=[]
    for row in rows:
        nativepath=ROOT/'graphics'/row['native'];imagepath=ROOT/'graphics'/row['image'];ready=imagepath.is_file()
        row.update(id=row['map_resource'],resource=row['image_resource'],generated=ready,category='scenario_background' if row['map_resource']>=5102 else 'story_cg_or_map')
        row['status']='generated' if ready else 'native_only'
        if row['category']!='scenario_background':continue
        with Image.open(nativepath) as opened:native=opened.convert('RGB');native.load()
        result=dict(resource=row['map_resource'],native_size=list(native.size),image_exists=ready,registered=bool(row.get('registered')),game_verified=bool(row.get('game_verified')))
        if ready:
            with Image.open(imagepath) as opened:art=opened.convert('RGB');art.load()
            assert art.width>=native.width*2 and art.height>=native.height*2,(imagepath,art.size)
            delta=np.abs(np.asarray(native,dtype='int16')-np.asarray(art.resize(native.size,Image.Resampling.LANCZOS),dtype='int16'))
            result.update(hd_size=list(art.size),sha256=hashlib.sha256(imagepath.read_bytes()).hexdigest(),changed_native_pixels=int(np.any(delta>3,axis=2).sum()),decoded=True,blank_preserved=row['map_resource']==5276)
            assert result['changed_native_pixels']>0 or row['map_resource']==5276,(imagepath,'native art unchanged')
            row['hd_size']=result['hd_size'];row['hd_sha256']=result['sha256']
        else:missing.append(row['map_resource'])
        checks.append(result)
    scope=[r for r in rows if r['category']=='scenario_background'];catalog.update(generated=sum(r['generated'] for r in rows),scenario_backgrounds=len(scope),scenario_backgrounds_generated=sum(r['generated'] for r in scope))
    write(F/'catalog.json',catalog);write(F/'library.json',dict(backgrounds=rows))
    batchfile=F/'quad_batches.json';meta=json.loads(batchfile.read_text());supportfile=F/'icon_agent_generation.json';support=json.loads(supportfile.read_text())['batches'] if supportfile.exists() else [];byname={b['name']:b for b in support}
    for batch in meta['batches']:
        if all((F/f'scenario_{i}_hd.png').exists() for i in batch['resources']):
            batch['status']='generated'
            if batch['name'] in byname:batch.update(byname[batch['name']])
    write(batchfile,meta)
    report=dict(scope='All 141 native background resources in scenario PLT/IMG/SCR bank 5100-5522',native_resources=len(scope),generated_files=len(scope)-len(missing),missing=missing,all_files_decode=not missing,blank_backgrounds_preserved=[5276] if (F/'scenario_5276_hd.png').exists() else [],registered=sum(c['registered'] for c in checks),game_verified=sum(c['game_verified'] for c in checks),sizes=dict(Counter('x'.join(map(str,c.get('hd_size',[]))) for c in checks)),checks=checks,excluded_story_cg_or_maps=106,tool='built-in image_gen',registration_and_game_verification_owner='root runtime integration; asset readiness does not establish in-game coverage')
    write(F/'coverage.json',report)
    for page in range((len(scope)+23)//24):
        sheet=Image.new('RGB',(1024,624),'#222');draw=ImageDraw.Draw(sheet)
        for n,row in enumerate(scope[page*24:(page+1)*24]):
            x=n%6*170;y=n//6*156;path=ROOT/'graphics'/(row['image'] if row['generated'] else row['native']);art=Image.open(path).convert('RGB').resize((168,126));sheet.paste(art,(x,y));draw.text((x,y+128),f"{row['map_resource']} {'HD' if row['generated'] else 'MISSING'}",fill='white' if row['generated'] else 'red')
        sheet.save(OUT/f'hd_contact_{page}.png')
    print(json.dumps({k:v for k,v in report.items() if k!='checks'}))

if __name__=='__main__':main()
