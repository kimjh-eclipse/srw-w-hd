# IMG21657 노란색 2 실제 변형 / 신규29개 그림

## 설치용
candidate_yellow_pair.png: native192×128,4배768×512 RGBA. 위64native행은white-core/yellow-edge실제팔레트,아래64행은olive-core/white-edge실제역배열팔레트. imagegen을각각별도로새생성했으며한그림코드재색칠아님.
**new_candidate_contract.json29개만설치.** 전체candidate_contract.json30개는문맥,keep_existing_contract.json1개는유지. atlas observed_effect_21657_yellow_pair / resourceNone / exactRGB/static/effectTrue.
기존바인딩92081(hash3177956239)는원본16×16단색흰사용슬롯1만같아서palette나머지가달라도w/h+indexbytes+실제사용색일치한다. existing_overlap_proof.json에1/1증거. 기존그림은수정하지않는다.

## 실제 원본 계약
capture_21657_22419.py가공통capture_rendered_obj_contracts로unit214mechanical168,unit225mechanical159,unit280mechanical168각180frame을제작원본수집했다. 현재VRAM/obj_debug픽셀안씀. bound는cachedhash==core.partsactualhash및attrs일치필수,unbound는cachedOBJ. source21657/22419의사각형과rawindex배열까지대조했다.
전체관측109:21657에87계약,22419에22계약. 겹치는원본배열/actual색은같은RGB해시를공유하므로두리소스누락을각각독립그림완료로중복세지않는다. 이번제작범위는21657의안정노란2팔레트30계약뿐이다. 원리소스주소추적아니므로resourceNone.
각candidate행은sourcecoords/actualpalette_15bit/RGB/rawindex/indexhash/OAMattrs/변환/좌표/engine/state/frame포함. mechanical_production_checks.json에는각계약의source/currentpalette값(동일실제캐시),원본RGBhash재계산과크기기록. 회색/검정캐릭터성팔레트시계열fade등나머지계약은그대로observed_contract.json에남겼고이번에같은그림재색칠로메우지않음.

## 팔레트 구성
위변형:slot1white[255,255,255],2palelemon[255,255,172],3yellow[255,255,82],4~6oliveyellow[222,222,74]/[189,189,57]/[156,156,49].
아래변형:slot1부터6이역순. 그래서흰핵을olive핵으로그려야하며흰색만유지하면틀린색이된다. reference_yellow_0/1.png및native_yellow_0/1.png가실제source색참조다. 다른효과이미지재색칠안함.

## 새 그림
generated_yellow_0/1.png각별도imagegen출력. fullsheet를연속그림으로그린뒤overlapcrop을같은좌표에서사용. 작은particle를구슬처럼그린첫fullsheet부분은그대로쓰지않고generated_yellow_particles.png별도새생성으로교체했다. native작은component의bbox/상대위치/평균색을등록계약으로만사용해생성자체component를선택/배치. particle_registration.json에기록. 색을코드로칠하지않았고nativealpha/RGBstamp없다.
생성자체alpha의낮은fringe/작은잡음만정리하고4배축소. source176,32의단색fill은전체source참조엔있으나**이번actual노란30개계약에없다**. white생성은그칸을투명으로해석했으나그누락칸을등록하지않는다. 임의nativefill/다른팔레트alpha복원하지않음. 이후그영역을관측하면별도actual팔레트계약으로제작해야한다.

## 알려진 그림 차이 / Claude 확인 큐
불꽃/beam내부명암이원본보다세분화되었고색띠·뾰족점의위치/폭·작은파편모서리가달라졌다. 일부generated외곽에가는노란테두리가남고,특히왼쪽quarter형crop끝에짧은윤곽선이보일수있다. 원래다른조각에이어지는면이면밝기선/이음새가될위험이있어검증필수다. nativealpha로강제일치시키거나검사기준을낮추지않았다. 새그림을만든것이실재생합격증거는아니다.

정확fixture별첫관측offset(계약에서자동집계):
- test_current/combat/named_attacks/unit_225/mechanical_cutin_159.state: +117, +119, +121, +125, +126, +128, +129, +171, +174, +175
위목록은제작계약첫관측으로정확세부OAM/좌표는JSON우선. Claude는29신규HD등장/기존1보존,노란두색배열,작은칩,quarter절단선,겹침crop밝기연속성,가림/UI/준비후held와소실을판정할것.

## 작업 경계
liveart/library/DB/core/EXE/설정변경없음. 공식audit/독립QA/후보HD실재생없음. root등록/굽기후Claude검증대기후보29개이다.
