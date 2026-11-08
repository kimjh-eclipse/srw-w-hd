"""Publish all 70 chapter-title image translations with the redrawn emblem."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=PROJECT_ROOT
TRANSLATIONS=[
(1,'宇宙の海に帆をあげろ','우주의 바다에 돛을 올려라'),
(2,'白き鉄騎士たち','하얀 철기사들'),
(3,'ミッション「ナデシコ破壊指令」','미션 「나데시코 파괴 지령」'),
(4,'砕け散る希望','부서지는 희망'),
(5,'機界・機械・奇々怪々','기계 세계·기계·기기괴괴'),
(6,'GGG危機一髪','GGG 일촉즉발'),
(7,'「出会いと別れ」の赤い星','「만남과 이별」의 붉은 별'),
(8,'沖縄の一番暑い日','오키나와의 가장 뜨거운 날'),
(9,'最悪な災厄の採択','최악의 재앙을 선택하다'),
(9,'戦うボーイズ・アンド・ガールズ','싸우는 소년들과 소녀들'),
(10,'赤と白の悪魔','붉고 하얀 악마'),
(11,'魔神相打つ','마신, 맞서 싸우다'),
(11,'心求めて','마음을 찾아서'),
(12,'放送不可のウォークライ','방송 불가의 워크라이'),
(12,'「艦長」は君だ！「教授」は誰だ！','「함장」은 너다! 「교수」는 누구냐!'),
(13,'「秘密のバイト」は危険な香り','「비밀 아르바이트」의 위험한 향기'),
(13,'友情のファニーアニマルズ','우정의 퍼니 애니멀즈'),
(14,'その生命、誰がために','그 목숨, 누구를 위하여'),
(15,'五色の絆、金色の勇気','오색의 인연, 황금의 용기'),
(16,'閉ざされた二人','닫혀 버린 두 사람'),
(17,'さらば勇者達！東京大決戦！！','잘 있거라 용사들이여! 도쿄 대결전!!'),
(18,'悲劇のワン・ナイト・スタンド','비극의 원 나이트 스탠드'),
(19,'激突！魔神VS地獄王','격돌! 마신 VS 지옥왕'),
(20,'加速する宇宙','가속하는 우주'),
(21,'送られてきた刺客','보내져 온 자객'),
(22,'過去からの帰還者','과거에서 돌아온 자'),
(22,'やってきた「遠い同胞」','찾아온 「먼 동포」'),
(23,'終わらない円舞曲・終幕','끝나지 않는 왈츠·종막'),
(24,'それぞれの「自分らしく」','저마다의 「나답게」'),
(25,'木星決戦！超重力の罠','목성 결전! 초중력의 함정'),
(26,'勇気ある戦い','용기 있는 싸움'),
(27,'そして、終わらない明日へ','그리고, 끝나지 않는 내일로'),
(28,'宇宙に一人だけの','우주에 단 한 사람'),
(29,'赤い魂、青い炎','붉은 혼, 푸른 불꽃'),
(30,'女神の夢、戦神の野望','여신의 꿈, 전신의 야망'),
(31,'姫と道化、女王と勇者','공주와 광대, 여왕과 용사'),
(32,'終わるハイスクールライフ','끝나는 하이스쿨 라이프'),
(32,'決意のパートタイムジョブ','결의의 파트타임 잡'),
(33,'忍び寄る黄金の影','다가오는 황금의 그림자'),
(33,'VIRGIN FLUSH','버진 플러시'),
(34,'よみがえる墓場の名刀','되살아나는 묘지의 명검'),
(34,'揺れる想いと小さな決意','흔들리는 마음과 작은 결의'),
(35,'熱砂に吹く風','뜨거운 모래에 부는 바람'),
(36,'別れのイントゥ・ザ・ブルー','이별의 인투 더 블루'),
(37,'平和の国の雷','평화의 나라에 울리는 우레'),
(37,'暗黒からの侵略者','암흑에서 온 침략자'),
(38,'彼と彼女の問題','그와 그녀의 문제'),
(38,'死闘！魔神VS大将軍','사투! 마신 VS 대장군'),
(39,'鉄騎士再誕','철기사 재탄생'),
(40,'勇者の真実','용사의 진실'),
(41,'想いと力、その向かう先','마음과 힘, 그 너머'),
(42,'暁の閃光','새벽의 섬광'),
(43,'記憶の底から','기억의 밑바닥에서'),
(44,'帰るべきデイ・バイ・デイ','돌아가야 할 데이 바이 데이'),
(44,'運命の子ら','운명의 아이들'),
(45,'生まれ落ちた悪意','태어난 악의'),
(45,'吹き荒れる破壊の嵐','몰아치는 파괴의 폭풍'),
(46,'新しい時代の始まりに','새로운 시대의 시작에'),
(47,'黒衣の復讐鬼の最期','검은 복수귀의 최후'),
(48,'逆襲の大帝王','역습의 대제왕'),
(49,'戦いの海に勇気の帆を','싸움의 바다에 용기의 돛을'),
(50,'静止した時の二人','정지된 시간 속의 두 사람'),
(50,'憎悪と運命の螺旋','증오와 운명의 나선'),
(51,'燃え尽きる生命','불타 없어지는 생명'),
(51,'進んだ道の先','걸어온 길의 끝'),
(52,'歪んだ太陽','일그러진 태양'),
(53,'朝をよぶ者達','아침을 부르는 이들'),
(54,'忘れえぬ思い出を胸に','잊을 수 없는 추억을 가슴에'),
(None,'果て無き未来への出航','끝없는 미래로 떠나는 출항'),
(None,'終わり無き旅路','끝없는 여정'),
]

def main():
    out=ROOT/'graphics/localized_screens';catalog=json.loads((out/'chapter_catalog.json').read_text());assert len(TRANSLATIONS)==len(catalog['titles'])==70
    emblem=Image.open(out/'chapter_emblem_hd.png').convert('RGB').resize((1440,1080),Image.Resampling.LANCZOS)
    for row,(episode,japanese,korean) in zip(catalog['titles'],TRANSLATIONS):
        image=emblem.copy();d=ImageDraw.Draw(image);header=f'제{episode}화' if episode is not None else '최종화'
        for text,y,size in [(header,397,76),(korean,577,74)]:
            font=ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf',size)
            while d.textlength(text,font=font)>1340:
                size-=1;font=ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf',size)
            d.text((720,y),text,font=font,anchor='mm',fill='white',stroke_width=4,stroke_fill='black')
        path=out/f"chapter_{row['index']:02}_ko.png";image.save(path,compress_level=1)
        row.update(episode=episode,japanese=japanese,korean=korean,image=path.name,status='translated_runtime_indexed',image_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    catalog['translated_titles']=70;path=out/'chapter_library.json';temp=path.with_suffix('.tmp.json');temp.write_text(json.dumps(catalog,ensure_ascii=False,indent=2),encoding='utf-8');temp.replace(path)
    (out/'chapter_translations.json').write_text(json.dumps([dict(index=i,episode=e,japanese=j,korean=k) for i,(e,j,k) in enumerate(TRANSLATIONS)],ensure_ascii=False,indent=2),encoding='utf-8')
    print('Published',len(catalog['titles']),'translated chapter screens')

if __name__=='__main__':main()
