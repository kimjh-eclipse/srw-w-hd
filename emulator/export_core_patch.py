"""Export tracked edits and new native bridge headers as one reproducible patch."""
from pathlib import Path
import subprocess,difflib
HERE=Path(__file__).resolve().parent;repo=HERE/'desmume'
patch=subprocess.check_output(['git','diff','--no-ext-diff','--binary'],cwd=repo).decode('utf-8')
for name in subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=repo).decode().splitlines():
    if not name.startswith('desmume/src/') or not name.endswith('.h'):continue
    contents=(repo/name).read_text().splitlines(keepends=True)
    patch+=f'diff --git a/{name} b/{name}\nnew file mode 100644\n'
    patch+=''.join(difflib.unified_diff([],contents,fromfile='/dev/null',tofile='b/'+name))
(HERE/'hd_core.patch').write_text(patch,encoding='utf-8',newline='\n')
print('Exported native source patch')
