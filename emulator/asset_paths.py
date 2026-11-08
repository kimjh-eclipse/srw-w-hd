"""Resolve packaged WebP art while keeping catalog identities and native PNGs."""
from pathlib import Path
import os,sys

class AssetPath(type(Path())):
    def __truediv__(self,key):
        path=super().__truediv__(key)
        if path.suffix.lower()=='.png' and (getattr(sys,'frozen',False) or os.environ.get('SRWW_OPTIMIZED_ASSETS')=='1'):
            alternate=path.with_suffix('.webp')
            if not path.exists() and alternate.exists():return alternate
        return path

def asset_root(path):return AssetPath(path)
