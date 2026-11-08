"""Export tracked edits and new native bridge headers as one reproducible patch."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
import subprocess,difflib
HERE=(PROJECT_ROOT/'emulator');repo=HERE/'desmume'
patch=subprocess.check_output(['git','diff','--no-ext-diff','--binary'],cwd=repo).decode('utf-8')
for name in subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=repo).decode().splitlines():
    if not name.startswith('desmume/src/') or not name.endswith('.h'):continue
    contents=(repo/name).read_text().splitlines(keepends=True)
    patch+=f'diff --git a/{name} b/{name}\nnew file mode 100644\n'
    patch+=''.join(difflib.unified_diff([],contents,fromfile='/dev/null',tofile='b/'+name))
(HERE/'hd_core.patch').write_text(patch,encoding='utf-8',newline='\n')
print('Exported native source patch')
