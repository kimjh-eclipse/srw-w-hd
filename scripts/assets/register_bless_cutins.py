"""Register the 20 Bless pilot cut-in frames (IMG25328..25347) in graphics/cutins_library.json.

Specs come from test_current/parts/bless_cutin_user_report/proposed_cutin_spec*.json;
for 25328/25330/25332 the *_corrected spec is used. Images are copied to
graphics/pilot_cutins/bless/. A spec whose drawing hash differs from its
packet's recorded SHA is refused. Existing entries with the same resource are replaced.
"""
import hashlib,json,shutil,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT

SRC=ROOT/'test_current/parts/bless_cutin_user_report';DST=ROOT/'graphics/pilot_cutins/bless'


def main():
    lib_path=ROOT/'graphics/cutins_library.json';lib=json.loads(lib_path.read_text(encoding='utf-8'));cutins=lib['cutins']
    DST.mkdir(parents=True,exist_ok=True);added=[]
    next_id=max(c['id'] for c in cutins)+1
    for img in range(25328,25348):
        corrected=img in (25328,25330,25332)
        spec_file=SRC/(f'proposed_cutin_spec_{img}_corrected.json' if corrected else ('proposed_cutin_spec.json' if img==25340 else f'proposed_cutin_spec_{img}.json'))
        packet_file=SRC/(f'candidate_packet_{img}_corrected.json' if corrected else ('candidate_packet.json' if img==25340 else f'candidate_packet_{img}.json'))
        spec=json.loads(spec_file.read_text(encoding='utf-8'));packet=json.loads(packet_file.read_text(encoding='utf-8'))
        drawing=SRC/packet['drawing'];assert spec['resource']==img,(img,spec['resource'])
        assert hashlib.sha256(drawing.read_bytes()).hexdigest()==packet['file_sha256']['drawing'],('drawing changed since handover',img)
        target=DST/f'bless_{img}_hd.png';shutil.copy2(drawing,target)
        entry=dict(id=next((c['id'] for c in cutins if c.get('resource')==img),None) or next_id,name=f'pilot_bless_{img}',layer=spec['layer'],layers=spec['layers'],native_size=spec['native_size'],
            image=str(target.relative_to(ROOT/'graphics')).replace('\\','/'),paint_image=str(target.relative_to(ROOT/'graphics')).replace('\\','/'),signatures=spec['signatures'],resource=img,
            source_map=spec.get('source_map'),source_palette=spec.get('source_palette'),signature_mode=spec.get('signature_mode','image_origin'),presentation_role=spec.get('presentation_role','pilot_foreground'))
        for k in ('map_signature','map_window_signature','map_window_entries'):
            if k in spec:entry[k]=spec[k]
        if entry['id']==next_id:next_id+=1
        cutins[:]=[c for c in cutins if c.get('resource')!=img];cutins.append(entry);added.append((img,entry['id'],entry['signature_mode'],entry['signatures']))
    shutil.copy2(lib_path,ROOT/'test_current/parts/pending_install/cutins_library.before_bless.json')
    lib_path.write_text(json.dumps(lib,ensure_ascii=False,indent=1),encoding='utf-8')
    for a in added:print(a)
    sigs=[(c['signatures'][0],c.get('signature_mode')) for c in cutins]
    dup=[s for s in set(sigs) if sigs.count(s)>1];print('registered',len(added),'duplicate signature+mode pairs',dup)


if __name__=='__main__':main()
