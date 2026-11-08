"""Map the two original copyright-image signatures to scalable Korean text."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json,hashlib
import numpy as np
from PIL import Image
from hd_core import ROOT

def main():
    source=np.asarray(Image.open(ROOT/'test_current/boot/frame_00540.png').convert('RGB'))
    lines=[[
        '© 가토 쇼지·시키 도지 / 미스릴',
        '© 가토 쇼지·시키 도지 / 진다이 고교 학생회',
        '© 가토 쇼지·시키 도지 / Full Metal Panic! Film Partners',
        '© 선라이즈',
        '© 지벡 / 나데시코 제작위원회',
        '© 지벡 / 1998 NADESICO 제작위원회',
        '© 소츠 에이전시·선라이즈',
        '© 소츠 에이전시·선라이즈·마이니치 방송'],[
        '© 소츠 에이전시·타츠노코 프로',
        '© 타츠노코 프로·소츠 에이전시',
        '© DARTS',
        '© 다이나믹 기획',
        '© 도에이',
        '© 2001 나가이 고 / 다이나믹 기획·광자력 연구소',
        '© 2003 나가이 고 / 다이나믹 기획·광자력 연구소',
        '© BANPRESTO 2007']]
    screens=[]
    for index in range(2):
        frame=source[index*192:(index+1)*192];ink=np.all(frame>210,axis=2)
        screens.append(dict(index='copyright_'+str(index),ink_sha256=hashlib.sha256(np.packbits(ink).tobytes()).hexdigest(),lines=lines[index],source_sha256=hashlib.sha256(frame.tobytes()).hexdigest()))
    path=ROOT/'graphics/localized_screens/copyright_library.json';path.write_text(json.dumps(dict(screens=screens),ensure_ascii=False,indent=2),encoding='utf-8');print('Registered two Korean copyright screens')

if __name__=='__main__':main()
