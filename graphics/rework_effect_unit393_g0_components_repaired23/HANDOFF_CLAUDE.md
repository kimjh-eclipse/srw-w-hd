# unit393_g0 문제23개 교정 후보 — Claude 검토 대기

## 현재 상태
최신 classified 총477개판본에서도이묶음문제23개는그대로있었습니다. observed_effect_unit393_g0 최신26개중23개만자체새RGBA로교정했습니다. 정상3(94939/94951/94952)은기존픽셀·바인딩·키보존대상입니다. 정상부모완전포함관계는없었습니다.

원본23개를28개연결성분으로나누어작은독립파란점도따로새그림으로만들고원본bbox자리로등록했습니다. 28motif/3생성panel입니다. 줄기와가지수·꺾임·국소굵기를유지하되경계AA를추가했습니다. 원본component분해는source시트배치근거이지실제로같은프레임에모두동시등장한다는주장이아닙니다.

## 입력·좌표·메모리 준비
normalized_installer_contract23.json에실제rendered cached원본전체가있습니다. 23개모두rawbytes/w/h/indexhash/전체16색BGR555/RGBhash대조일치. sourcebox는actual원본좌표,atlasbox/spec는기존candidate좌표이며서로혼동하지않습니다. normalized installer자체좌표로NullCache prepare23개를실행했고direct기존candidate좌표준비결과와RGBA가모두같았습니다. maxA255/원본fill0,빈텍스처없음입니다.

## 알파/그림출처
자체imagegen RGBA3panel에서만출력그림을가져왔습니다. 원본alpha/RGB전사/다른팔레트alpha공유/threshold/morph삭제없음. A>=16은생성bbox위치측정용. 별도파란단색material1개는동일생성셀의내부RGBAcrop(생성alpha253~254그대로)을원본1texel성분에배치했습니다.255강제칠하기없음입니다.

## 남은 위험
원본격자alpha128 IoU .827~1.0/면적비.991~1.183입니다. 94927의얇은전격은원본보다약18%넓고,일부전격끝의AA나원본계단차이가있습니다. 큰흰원형새그림으로대체한것이아니며원본꺾임을유지했습니다. RGB음영미세차이는colour_production_comparison23.json에서볼수있습니다. 공식검사/HD실재생정상판정은하지않았으며사용자창/모니터조작도없습니다.

## 인계
ready_replacement23.json / normalized_installer_contract23.json / candidate_atlas.png / native_atlas.png / native_prepared_pairs23.png.
새atlas effect_unit393_g0_components_repaired23로같은23ID만교체하고정상3기존atlas/키를변경하지마십시오. root설치·굽기,Claude공식검증대기입니다. 공유runtime/live/DB/EXE/Git변경없음입니다.
