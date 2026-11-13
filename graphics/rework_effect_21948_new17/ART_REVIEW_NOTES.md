# 21948 효과 그림 인수 / 신규17개 (관측문맥31개)

## 설치용과 문맥용 구분

**설치용은 new_candidate_contract.json의17개만이다.**

- candidate_21948_31.png:768×640 RGBA,4배아틀라스.한파일에모든그림문맥31개있음.
- new_candidate_contract.json:정확17개신규RGB계약(3 mint+12 white/mint+2 charcoal gray).
- candidate_contract.json:관측31개전체문맥.이걸전부새로추가하면기존14개를중복/덮어쓰기하므로사용하지말것.
- keep_existing_contract.json / existing_rgb_overlap.json:이미활성RGB와일치하는14개.13개observed_energy_mint,1개extra의4477.이번에이들의라이브바인딩/그림을바꾸지말것.
- native_21948_31.png / native_candidate_comparison.png:실제원본색과새그림문맥.

기존21798/22163작업과중복하지않았고, 아래의 배열·사용색 대조까지 끝내 신규 17개로 분리했다.

## 실제 렌더 계약

default cachedOBJ읽기API를사용했다.렌더된OAM활성/화면범위/캐시의w/h와rendered OAM형태크기일치조건후원본index/palette/RGBhash/indexhash/priority/screen좌표를기록했다. PLT추정/현재MMU미래VRAM읽기없음.

source21948의모든8단위사각형을기계적으로만들어actualcached원본배열과일치하는것을찾았다. indexhash만맞춘게아니라rawindex배열도완전동일하다.1~2색파트도미리거르지않았으나21948관측31개에는그런flatfill이없었다.20498은별도59개/4palette와flat3개가관측되어후순위로capture원본에보존했다.

실제ROM주소를추적하지않았으므로'resource21948에서실제로읽었다'고확정하지않는다.특히13개mint공유파편은다른IMG와동일배열/색을공유한다.등록은resource=None/exactRGB/static으로제한하여잘못된추정팔레트재색칠을피한다.

계약수집원본은observed_contract.json.기계적제작확인은mechanical_production_checks.json에있다.공식audit/독립QA/후보HD재생은수행하지않았다.

## 아틀라스와 새 그림

native192×160 / artwork768×640:
- y0..64:mint독립생성full192×64시트
- y64..128:white/mint독립생성full192×64시트
- (0,128)32×32:charcoal gray fullshard.두32×16바인딩은여기를상하분할.
- (32,128)32×16:gray palette3참조문맥.이미4477로연결되어신규등록없음.

imagegenbuilt-in으로각실제팔레트를별도그렸다.다른팔레트그림을재색칠해채우지않았다.원본alpha찍기/nativeRGBcodefill없음.

큰plume/beam은연속시트를먼저그리고분할하여내부cut선윤곽을추가하지않았다.파편은별도top-white/mint/bottom-mint/jade참조로신규생성했다.원본component의위치/bbox계약에맞는생성자체조각을색/위치/종횡비로선택해자체alpha그대로등록했다.그림의RGB를코드로바꾸지않았다. particle_registration.json에선택기록.

gray첫출력이도트계단을그대로확대해rejected_gray_pixel_stairs.png로보존하고,새곡선그림generated_gray_two.png를다시생성했다.최종gray에이재제작본을사용했다.

원출력:generated_palette0/1.png,generated_gray_two.png,generated_particles_two.png.최종prepare_candidate.py는생성알파만최소정리/리사이즈하며최종작은크기에서Min/Max를추가해가는조각을없애지않는다.

## 알려진 문제 / Claude검증큐

검증완료아님.생성된불꽃꼬리/작은빈홈이원본보다부드럽고뾰족점의개수/위치가달라진부분이있다. gray큰hook은원본보다유기적인곡선/추가뾰족점이있어형태대조필요.파편은원본위치/bbox에맞췄지만모든흰영역이미세하게완전동일하다고보장하지않는다.초록이이효과정상색이므로키색오탐과실제과채도잔여를구분해야한다.

Claude state/frame:
1. test_current/combat/named_attacks/unit_413/native_reference/diagnostic_preview/weapon_1610_capture/frame_360.state
   +112(mint파편),+114~128(white파편/부분변화)
2. test_current/combat/named_attacks/unit_413/native_reference/diagnostic_preview/weapon_1610_capture/frame_600.state
   +31(gray2신규/gray기존4477문맥),+63(큰흰plume),+69(부분crop),+72(mint큰꼬리),+74~75(가는조각),+86/+94(파편)

위offset은원본계약첫등장위치이며후보실재생합격증거가아니다.설치후Claude가신규17각HD등장/기존14보존/준비후hold/소실/색영역/공식검사/UI앞뒤를봐야한다.

## 변경 경계

이child는live그림/library/DB/defaultDLL/EXE/공유소스/플레이어설정을변경하지않았다. root만신규17개등록→exact17재굽기하고Claude검증큐로인계할것.

## 기존 14개 보존 근거: CRC 외의 기계적 대조

`existing_exact_overlap_proof.json` 및 재현 스크립트 `prove_existing_overlap.py`에 기록했다. **14개 전부 크기(w/h), 원본 index byte 배열, 실제 사용한 비투명 슬롯의 RGB가 일치했다.** CRC 단독 매칭으로 중복 판정하지 않았다. 사용하지 않는 팔레트 슬롯과 투명 슬롯 0의 색은 비교 대상에서 제외했다. 바인딩 번호는 1부터 센다.

- 91810, 91815, 91819, 91820, 91822, 91823, 91826, 91827, 91830, 91831, 91832, 91833, 91834: 기존에 저장된 `index_pixels`를 복호화해 새 실제 관측 배열과 바이트 단위로 대조하고, `original_palette_rgb`의 각 사용 슬롯을 대조했다.
- 4477(extra): 기존 바인딩에는 index 배열/팔레트 기록이 없다. 따라서 단순 해시 중복으로 판정하지 않았다. `kazuma_extra_parts_reference.png`를 선언된 native_size 256×160으로 읽고 (0,128,32,16)을 비교했다. 불투명 색 4개가 실제 관측의 슬롯 2,3,4,5와 각각 고유하게 대응하며, 미매핑 픽셀 0개이고 투명 지지영역도 같았다. 이 고유 색 대응으로 복원한 인덱스 배열이 실제 배열과 완전히 같다. 원본 참조에서 인덱스를 복원했다는 한계는 증거 파일에도 명시했다.

이는 등록 중복 여부를 위한 기계적 원본 계약 비교이며, 기존 HD 그림의 품질 합격 판정은 아니다. 신규 그림을 덮어 씌우지 않고 기존 14개를 유지한다.

## Claude 추가 검증 큐: 기존/신규 혼합 접합

31개 전부를 새 그림으로 교체하지 않으므로 **동일한 연속 효과 안에서 기존 mint 그림과 신규 17개 그림이 섞일 수 있다.** 원본 계약이 동일하다는 사실은 HD 색 경계·굵기·알파·잘린 면이 이어진다는 뜻이 아니다.

- 원본 source21948의 파편 구역 (x0..64,y32..64)은 기존 13개 mint 바인딩과 신규 파편이 겹치거나 이웃한 여러 크기의 사각형으로 사용된다. 새 그림은 해당 구역을 연속 생성했지만 기존 13개는 다른 생성 아틀라스를 유지한다. 밝은 흰 핵·민트 경계의 끊김, 중복 도장, 작은 조각의 굵기 차이가 우선 점검 대상이다.
- unit413 weapon_1610_capture/frame_360.state +112 및 +114~128, frame_600.state +63,+69,+72,+74~75,+86,+94에서 기존/신규를 함께 볼 것. 이 offset은 각 계약의 첫 관측 시점이며, **모든 바인딩이 정확히 같은 한 프레임에 공존한다고 재확인한 것은 아니다.** 새 후보 재생을 수행하지 않았으므로 공존 시점·연속 접합은 Claude가 판정해야 한다.
- frame_600.state +31의 신규 charcoal 두 조각과 기존 gray4477도 원본 palette가 서로 다르다. 서로 다른 색 변형을 같은 회색으로 강제 통일하지 말고, 실제 팔레트별 조각 및 동시 표시 위치를 대조할 것.
- 전체 `candidate_contract.json` 31개와 그 비교 그림은 문맥/선택용이다. live 설치는 `new_candidate_contract.json`의 신규 17개만 사용한다. 기존 14개를 새 후보로 바꾸려면 별도의 명시적 검토가 필요하다.

공유 코드·live·library·DB 변경, 공식 audit, 새 HD 재생 검증은 수행하지 않았다.

## 제작 입력의 캐시 경로

이 묶음의 원본 계약은 `retro_srw_copy_cached_obj`의 렌더된 index/palette 및 `core.obj` rendered OAM에서 수집했다. 현재 MMU VRAM 또는 obj_debug의 소스 픽셀을 사용하지 않았다. 이후 공통 함수는 `scripts/assets/capture_rendered_obj_contract.py`를 사용한다. 새 함수는 bound OAM의 cached hash/attributes와 core.parts를 대조하고, unbound row 0은 cache 계약을 사용한다. 이 기존 묶음의 수집 스크립트를 새 helper로 재실행한 것은 아니다.
