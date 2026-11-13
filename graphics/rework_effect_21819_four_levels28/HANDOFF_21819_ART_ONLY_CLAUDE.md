# IMG21819 4 실제 밝기 단계 / 신규28계약 그림

## 수량과 설치
candidate_21819_four_levels.png:768×512 RGBA(native192×128,4배). **new_candidate_21819_contract.json28개만설치.** atlas observed_effect_21819_four_levels / exactRGB/static/effectTrue/resourceNone.
수량구분:실제팔레트4단계,고유index형태12개,그림계약28개. 28개의완전히다른기체/형태를그린것으로부풀리지않는다. 기존exact연결0개,수집시모두binding_id0/unbound로기존indexed기체재교체아님.

native y0..32행에는검정초기2개만x0..8/x8..16,y0에배치. 이2개는8×8실제source88,8 및88,0의작은검정원/큰검정원이다. 흰배경을검정으로codefill한것이아니라imagegen이그린자체RGB/alpha를사용. 검정이므로검은preview에선안보인다. black_generated_on_gray.png에서생성alpha지원영역을볼수있다.
y32..64:밝은white/graylavender11개, y64..96:중간8개,y96..128:어두운7개. 각native밝기참조를한문맥에서따로그린3행그림이며이전그림코드재색칠아님.

## 제작 입력과source/current팔레트
capture_21819_19584.py공통capture_rendered_obj_contracts가unit226/227 mechanical168에서실제28개를수집. bound는actualcachedhash==core.parts및attrs일치,unbound캐시계약. 원본source21819사각형과indexhash+rawindexbytes일치. 현재MMU/obj_debug픽셀사용없음. 실제ROM리소스주소추적아니므로resourceNone.
계약마다source_x/source_y,현재actualpalette_15bit/RGB,index_pixels/indexhash/hash,OAMattrs/변형/좌표/engine/state/firstframe기록. mechanical_21819_production_checks.json에각source/current실제palette(동일수집값),RGBhash재계산,인덱스SHA기록.

검정초기2개의실제사용슬롯은RGB0이다. 밝은단계는white255,graylavender222/189/156/123;중간은222/189/156/123/90;어두운단계는189/156/123/90/57이주색이다. 서로다른단계의색값을한canonical팔레트로임의덮지않았다.

## 새 그림
reference_21819_three.png실제3행참조→imagegen built-in. 첫출력은금속테두리/불필요한halfdisc/dash추가여서rejected_21819_metallic.png로보존/미사용. 두번째generated_21819_three.png를채택해원형선·arc·작은원·strip을flat2D로다시생성했다.
검정2개는reference_21819_black_two.png(회색보기배경)로별도imagegen→generated_21819_black_two.png. 그생성알파를그대로4배크기로축소사용하고회색보기배경은생성출력에없음.
생성자체낮은alpha주변찌꺼기만정리/축소. nativealpha/RGBstamp,기존이미지재색칠,원본pixel코드채움없음.

## 미검증 그림 차이
큰원과ring은원본보다균일/매끈한stroke다. 가장오른쪽arc들은생성본에서직선처럼펴진구간과연결점이있어원본곡률·좌표/반경이맞는지Claude대조필수. thinring에가는이중테두리나각crop끝의윤곽선이남을수있다. 3행밝기단계별flatgray/lavender색영역이실제와정확한지공식판정안함. 실제레이어위치/블렌딩은확인하지않았다. 새그림을기계적크기로등록한것을실재생합격으로보고하지않는다.

## Claude 장면 큐
- test_current/combat/named_attacks/unit_226/mechanical_cutin_168.state: +77, +79, +81, +83, +85, +87, +89, +91, +93, +143, +145, +147, +149

정확OAM/좌표/변형은JSON참조. 검정2초기단계누락/비가시alpha오류,ring/큰arc반경과곡률,stripcrop끝,실제4단계팔레트밝기,효과/UI/가림/준비후held·소실을검증할것.
공식audit/독립QA/후보HD재생없음. root설치·굽기후Claude확인대기. liveart/library/DB/core/EXE/설정변경없음.

## 빈 그림 4개 교정 (최신 후보)

root의설치전알파하드검사로half-disc1개가완전투명,source64,24의점선3색이최대alpha5인사실을발견했다. 제가실제반원을금속화생성본의추가발명으로잘못해석해삭제금지프롬프트를쓴것이half-disc누락원인이었다. 점선도원래존재하는strip인데단순한수평bar하나로축약하면서빠졌다. 이전생성완료보고는이4개의픽셀존재를보장하지못했다.

최신candidate_21819_four_levels.png는repair_21819_four.py교정후파일이다. 원본마스크/원본RGB를찍어채우지않았다.
- half-disc1989650155:새반원출력은중앙흰구멍이생겨rejected_repair_half_disc_hole.png로미사용. 이**같은효과첫자체생성출력**rejected_21819_metallic.png의원래있던반원crop을회수하여자체pixels/alpha를원본bbox에맞춰등록했다. source전체금속모델을다시활성화한것이아니라그반원하나만회수했다.
- dash912208730/3173909472/2963383029:generated_repair_three_dash.png를새로생성. 각행7개자체생성segment를실제7개segment의bbox에맞춰자체RGBA그대로등록했다. 색코드채움·원본alphastamp없음.

repair_four_mechanical_checks.json:28개모든계약crop최대alpha>=16(각교정4개는255),바뀐계약정확4개,나머지24개및검정초기2개RGBAbyte SHA동일. 겹침crop영향도28개를기계적으로대조했다. 시각품질합격/후보HD재생검증은아니다.
최신SHA는mechanical_21819_production_checks.json및repair_four_mechanical_checks.json. 원생성반영script prepare_21819_candidate.py만다시실행하면교정전으로돌아가므로현재최종파일을설치하거나그후repair_21819_four.py를실행해야한다. 후보계약/좌표/actual팔레트는변경없다.

남은그림한계는그대로Claude확인:반원얇은metal성border잔여,각점선shade와source3색배치의차이/균일성,ring/오른쪽arc형태,기존crop과이음새. root28전체설치보류후재인수용이며라이브/core/DB/QA는여전히변경하지않았다.
