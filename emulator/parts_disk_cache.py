"""Lossless prepared-texture store; the emulation loop never waits for it."""
import io,json,sqlite3,zlib
from PIL import Image

class PartsDiskCache:
    """Finished part textures as lossless WebP, addressed by their inputs."""
    def __init__(self,path):
        from runtime_paths import texture_cache
        self.path=texture_cache(path);self.connection=None
    def db(self):
        if self.connection is None:
            self.connection=sqlite3.connect(self.path,timeout=2)
            self.connection.execute('PRAGMA journal_mode=WAL')
            self.connection.execute('PRAGMA synchronous=NORMAL')
            self.connection.execute('CREATE TABLE IF NOT EXISTS textures (key TEXT PRIMARY KEY,w INTEGER,h INTEGER,pixels BLOB,stats TEXT)')
        return self.connection
    @staticmethod
    def encode(image):
        # exact keeps colour under transparent pixels, so decoding returns
        # the stored array bit for bit.
        data=io.BytesIO();image.save(data,format='WEBP',lossless=True,exact=True,method=4);return data.getvalue()
    def get(self,key):
        row=self.db().execute('SELECT pixels,stats FROM textures WHERE key=?',(key,)).fetchone()
        if row:
            image=Image.open(io.BytesIO(row[0])).convert('RGBA');image.load()
            return image,json.loads(row[1])
    def put(self,key,image,stats):
        with self.db():self.connection.execute('INSERT OR REPLACE INTO textures VALUES (?,?,?,?,?)',(key,image.width,image.height,self.encode(image),json.dumps(stats)))
    def keys(self):return {row[0] for row in self.db().execute('SELECT key FROM textures')}
    def close(self):
        if self.connection:self.connection.close();self.connection=None

class LegacyPartsCache:
    """Read-only view of the earlier 8x zlib store, kept as a bake source."""
    def __init__(self,path):self.path=path;self.connection=None
    def get(self,key):
        if self.connection is None:self.connection=sqlite3.connect(f'file:{self.path.as_posix()}?mode=ro',uri=True,timeout=2)
        row=self.connection.execute('SELECT w,h,pixels,stats FROM parts WHERE key=?',(key,)).fetchone()
        if row:return Image.frombytes('RGBA',(row[0],row[1]),zlib.decompress(row[2])),json.loads(row[3])
