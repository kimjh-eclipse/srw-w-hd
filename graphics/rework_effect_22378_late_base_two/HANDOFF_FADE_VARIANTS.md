# 22378 추가: 기본 형태2개 / fade 팔레트67개 계약

## 분량을 구분할 것
- 실제관측총83 RGB계약:기존16 + 추가67.
- 추가67의고유raw인덱스형태는2개뿐(indexhash3232673513,3279530199). 67개독립그림을만들거나1개그림을재색칠해67개완료로세지않았다.
- 기본그림2개만새제작: candidate_base_two.png256×128, new_candidate_contract.json2개. 가장밝은실제사용팔레트의hash4082394179(source128,0,32,32),1296546371(source160,0,32,32).
- 등록은atlas observed_effect_22378_base_two/exactRGB/static/effectTrue/resourceNone. 나머지65RGB계약도자동해결됐다고표시하면안된다.

## 실제 계약
공통cachedOBJ+renderedOAMhelper로unit413 weapon1610/1613/1614의frame1320/1560보유state각180frame제작원본수집. source22378모든8grid크기사각형과indexhash+rawbytes일치대조. 실제주소추적아니므로resourceNone.
observed_contract.json83개, new_22378.json67개에현재palette_15bit/RGB,index_pixels,hash/indexhash,sourcecoords,engine/attrs/변환/OAM/좌표/state/frame기록. bound16개는cachedhash==core.parts와attrs일치확인. 추가67개는row0/unbound였고캐시계약으로확인.
기존16개는existing_overlap_proof.json의w/h+rawindex+사용색16/16동일이며변경없다.

## fade를별도인계하는이유
67개는frame1560 +75~99의실제팔레트가매프레임점차바뀌는두형태다. 첫번째indexshape는25개,두번째는42색계약이관측되었다. unusedslot전체가아니라각shape사용슬롯8~13의실제색이달라RGBhash가바뀐다. 기존16개와같은그림이라는뜻은아니다. 기본두형태는기존16에없어새로제작했다.
Claude는두형태의실제반복팔레트변화/전역fade밝기적용과새기본그림의관계가올바른지검증할것. 코드/셰이더로어떻게연결할지는이child가수정하지않았다. palette/frame별계약은보존했으며임의대표1개색으로나머지를덮지않았다.

## 새 그림
reference_base_two.png의실제색을imagegen built-in으로새로제작한generated_base_two.png. 옅은회색/흰색연기리본두형태. 원출력의낮은alpha주변찌꺼기를생성alpha만정리후4배축소. nativealpha/RGB강제찍기없음. 다른effect그림재사용/재색칠없음. native_candidate_comparison.png.

원본보다흐르는곡선과층진음영이늘어났고작은음각이변했다. 생성원출력주변흰fringe가정리되었으나미세색점/흰영역과gap형태/기존그림과접합은미검증. alpha를원본마스크로강제일치시켜통과시키지않았다.

## Claude 확인
state:test_current/combat/named_attacks/unit_413/native_reference/diagnostic_preview/weapon_1610_capture/frame_1560.state
기본2개첫관측+75,67fade는+75~99. 각행OAM/위치/현재사용색/변환은JSON. 기존16문맥은frame1320에서관측.
기본2개HD등장과그림색/alpha/형태,fade연속성·소실·가림/UI를Claude가검증. 67RGB모두새그림완료라고보고하지말것.

공식audit/독립QA/후보HD재생없음. live/core/library/DB/EXE/설정수정없음.
