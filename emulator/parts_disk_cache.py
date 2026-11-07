"""Lossless prepared-texture cache; the emulation loop never waits for it."""
import hashlib,json,sqlite3,zlib
from PIL import Image

class PartsDiskCache:
    def __init__(self,path):self.path=path;self.connection=None
    def db(self):
        if self.connection is None:
            self.connection=sqlite3.connect(self.path,timeout=2)
            self.connection.execute('PRAGMA journal_mode=WAL')
            self.connection.execute('PRAGMA synchronous=NORMAL')
            self.connection.execute('CREATE TABLE IF NOT EXISTS parts (key TEXT PRIMARY KEY,w INTEGER,h INTEGER,pixels BLOB,stats TEXT)')
        return self.connection
    def get(self,key):
        row=self.db().execute('SELECT w,h,pixels,stats FROM parts WHERE key=?',(key,)).fetchone()
        if row:return Image.frombytes('RGBA',(row[0],row[1]),zlib.decompress(row[2])),json.loads(row[3])
    def put(self,key,image,stats):
        with self.db():self.connection.execute('INSERT OR REPLACE INTO parts VALUES (?,?,?,?,?)',(key,image.width,image.height,zlib.compress(image.tobytes(),1),json.dumps(stats)))
    def close(self):
        if self.connection:self.connection.close();self.connection=None
