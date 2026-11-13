# IMG19584 실제 회색 2 변형 / 신규32개 제작

## 설치 인수
candidate_19584_gray_pair.png:704×512 RGBA, native176×128의4배. 위64native행은밝은흰/회색팔레트,아래64행은어두운회색팔레트. **new_candidate_19584_contract.json32개만설치.** candidate_19584_contract.json33개는문맥. atlas observed_effect_19584_gray_pair / exactRGB/static/effectTrue/resourceNone.
기존91679/hash2616632808 1개는keep_existing_19584_contract.json유지. existing_19584_overlap_proof.json의w/h+rawindexbytes+사용currentpaletteRGB1/1동일이다. 새32개는수집당시모두core.binding_id0/unbound였으므로기존indexedHD를재제작한것으로세지않는다.

## 제작 입력/실제 팔레트
capture_21819_19584.py가공통capture_rendered_obj_contracts로unit226/227/261~265 mechanical168 각180frame제작원본을수집. 21819관측28개,19584관측33개. boundOAM은cachedhash==partsactualhash와attrs일치필수. 현재VRAM/obj_debug픽셀사용없음. IMG사각형indexhash후rawindex배열일치까지대조했다. 실제리소스주소추적은아니므로resourceNone.
각candidate계약에source_x/source_y,w/h,index_pixels,hash/indexhash,actualpalette_15bit/RGB,OAM변형/attrs/좌표/engine,state/frame기록. mechanical_19584_production_checks.json에는각source/current팔레트(동일실제수집값),원본RGBhash재계산,배열SHA/크기기록. 원본PLT추정이나다른효과그림색바꾸기로채운것이아니다.

밝은변형slot1~6:white255/gray230/205/180/148/123. 어두운변형slot1~6:gray180/139/106/65/32/black0. slot6의검정은그림색이며index0투명과다르다. 실제각팔레트를독립imagegen신규생성했다.

## 새 그림
generated_19584_0/1.png는built-inimagegen원출력. 원본의큰빛원호/충격원,직사각형연속fill,얇은수평streak,작은먼지형상을전체연속시트로먼저그려같은좌표의overlapcrop으로분할. 별도파츠별검은절단선요구없음. 생성자체낮은alpha주변찌꺼기만정리하고4배축소. nativealpha/RGBstamp/다른이미지재색칠없음. 밝은큰흰핵도생성출력에살아있어서다른팔레트alpha나코드fill로복원하지않았다.

## 알려진 차이 / Claude 검증 필요
원본작은먼지덩어리가생성본에서는잎/렌즈형으로더매끄럽게해석되었다. 큰원호의곡률과밝기band위치도원본과미세하게다르다. 어두운검정테두리의실제opaque지원영역이정확한지미검증. 일부직선crop끝에생성한가는명암선/외곽선이있어다른crop과만나는곳에이음새가생길위험이있다. 원본마스크를찍어원래도트와강제일치시키지않았으며,실제연결화면에서Claude가판정해야한다.
문맥전체33개를모두새아틀라스로교체하지말고신규32개만사용. 21819의검정/라벤더4단계28계약은관측파일에보존했으나이번그림완료에포함하지않았다.

## 실제 장면 큐
- test_current/combat/named_attacks/unit_261/mechanical_cutin_168.state: +96, +98, +100, +104, +106, +109, +111, +114, +116, +119, +124, +127, +131

각행OAM/좌표/변형은JSON참조. Claude는32개실제HD등장/기존1보존,큰원호밝기와알파,검정opaqueedge,연속fill/crop절단선,작은먼지와streak,레이어/UI/준비후held·소실확인.

공식audit/독립QA/후보HD재생검사없음. root등록·굽기후Claude검증대기. liveart/library/DB/core/EXE/설정변경없음.
