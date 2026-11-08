"""Keep project-bound generated artwork within the requested 960-pixel ceiling."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json
from PIL import Image
from hd_core import ROOT

def main():
    folder=ROOT/'graphics/wing_parts';records=[]
    for path in folder.glob('*_generated.png'):
        with Image.open(path) as source:
            im=source.convert('RGBA');before=im.size;im.thumbnail((960,960),Image.Resampling.LANCZOS);im.save(path,optimize=True)
        records.append(dict(path=path.relative_to(ROOT).as_posix(),before=before,after=im.size,bytes=path.stat().st_size))
    # The final HD files are the portable inputs to installers. Origin names
    # document generation provenance, without embedding a user's home path.
    path=ROOT/'graphics/img_first/generated_sources.json';origins=json.loads(path.read_text())
    path.write_text(json.dumps({key:value.replace('\\','/').split('/')[-1] for key,value in origins.items()},indent=2))
    (folder/'asset_sizes.json').write_text(json.dumps(records,indent=2))

if __name__=='__main__':main()
