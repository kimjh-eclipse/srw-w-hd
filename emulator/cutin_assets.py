"""Load the active pilot/mechanical cut-in, retaining it for the stage."""
import json
from PIL import Image
from stage_cache import StageCache
from painted_edges import clean_alpha

class CutinAssets:
    def __init__(self,root,primary,width):
        self.root=root;self.primary=primary;self.width=width;self.cache=StageCache();self.specs={}
        path=root/'graphics/cutins_library.json'
        if path.exists():self.specs={int(row['id']):row for row in json.loads(path.read_text())['cutins']}

    def set_width(self,width):self.width=int(width)

    def __contains__(self,key):return key==1 or key in self.specs

    def get(self,key,default=None):
        if key not in self:return default
        return self[key]

    def region(self,key):
        """Cache the painted extent so transparent canvas never gets uploaded."""
        cachekey=('region',int(key),self.width)
        if cachekey not in self.cache:
            image=self[key];box=image.getbbox() or (0,0,1,1)
            self.cache[cachekey]=(image.crop(box),box)
        return self.cache[cachekey]

    def __getitem__(self,key):
        cachekey=(int(key),self.width)
        if cachekey in self.cache:return self.cache[cachekey]
        if key==1:
            art=self.primary.resize((self.width,self.width*3//4),Image.Resampling.LANCZOS)
        else:
            row=self.specs[key];w,h=row.get('native_size',[256,192])
            with Image.open(self.root/'graphics'/row.get('paint_image',row['image'])) as source:
                art=source.convert('RGBA').resize((self.width,round(self.width*h/w)),Image.Resampling.LANCZOS)
            if row.get('paint_image'):art=clean_alpha(art)
        self.cache[cachekey]=art
        return art
