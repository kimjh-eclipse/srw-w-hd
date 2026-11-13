# IMG20498 흰색·민트 실제 효과 그룹 / 제작 인계

## 설치용
**new_candidate_contract.json의 신규 7개만 설치할 것.** candidate_white_39.png는 native256×128의4배1024×512 RGBA. 전체candidate_contract.json39개는 관측 문맥이며 기존32개 덮어쓰기용이 아니다.

처음 조사 시 신규13개였으나 root의21948 설치가 같은 RGB/배열/색의6개를 먼저 연결하여 지금은 신규7개다. 정확 신규hash:172217739,2794022688,4202769659,3463381043,1514132322,3177956239,4099899612. atlas observed_effect_20498_white_39 / resource=None / static / effect_part=True.

## 제작 입력 / 새 공통 helper 사용
`test_current/parts/capture_20498_white.py`가 `scripts/assets/capture_rendered_obj_contract.py`의 capture_rendered_obj_contracts를 사용했다. unit413 weapon1610 frame360 및600 두 상태에서 각180프레임의 **제작 원본 계약만 수집**했다. bound일 때 cachedhash==core.parts actualhash 및 attrs동일을 요구했다. unbound는 캐시 원본을 사용했다. 현재MMU VRAM/obj_debug 픽셀은 사용하지 않았다.39개 전부 다시 관측됐다. source20498 후보 crop과 rawindexbytes까지 일치했으나 실제ROM주소추적이 아니므로 resource=None으로 한다.

이 그룹은 20498의 가장 큰 실제 팔레트 그룹39개 전부다. charcoal2개/21948신규17개는 건드리지 않았다. 20498의 나머지 jade 팔레트10개와 별도gray8개는 이번 그림범위가 아니다. 원수집에는1~2색 flatfill도 포함했으며 흰/민트그룹39개를 임의로색수로제외하지 않았다.

## 기존32개 계약 중복 근거
existing_overlap_proof.json에 w/h + raw index + 사용비투명슬롯RGB를 기록했다.32/32 정확계약일치.
30개는 저장index_pixels와original_palette_rgb 직접대조.4719/4720은 source_binding4476/4463의extra 원본참조를 기존source_palette_rgb의 고유사용색으로역복원해 실제index배열과완전일치, 별도alias palette_rgb도실제팔레트사용슬롯과일치했다. 이2개는 저장raw배열이아니라참조원본역복원이라는차이가있다. CRC단독으로중복판정하지않았다. 기존그림품질합격이라는뜻은아니며32개그대로유지한다.

## 새 그림과 원출력
imagegen built-in 사용. 전체효과를연속시트로그린뒤 overlapping사각형을공유좌표로자른다. 잘린면검은윤곽선을추가하지않는다.
- generated_flat.png: 흰핵/파스텔민트연속plume/대각선ray 새그림.
- rejected_glow_beads.png: 첫시도는작은파편을구슬처럼그려미사용.
- generated_particles.png: upperright96×32 파편영역별도새그림. 원본각component의위치/bbox를사용해생성자체component중색/상대위치/종횡비로고른것을배치했다. nativealpha찍기/nativeRGB복사/코드재색칠은없다. particle_registration.json에선택기록.
- 생성alpha의저농도잔여만최소정리하고4배로축소했다. native의불투명마스크를생성알파로덮지않았다.

프롬프트는원본배치·흰핵불투명·옅은민트/제이드경계·작은파편의독립간격·내부절단면윤곽금지를요구했다. 결과가원본과완전히같다는판정은하지않았다.

## 알려진 차이 / Claude 검증 큐
큰불꽃은원본보다삼각꼬리곡률과민트띠모양이달라졌다. tiny칩새그림에일부기하학적명암/둥근모서리가있고원본파편보다선명할수있다. 생성경계정리후에도미세한청록테두리/흰핵면적/가는필라멘트손실여부는미검증이다. 기존32개를유지하므로신규7개와같은연속효과의사각형이교대할때스타일/굵기/알파접합차이가날수있다. 전체39개후보는그비교문맥이다.

fixture1: test_current/combat/named_attacks/unit_413/native_reference/diagnostic_preview/weapon_1610_capture/frame_360.state
최초관측+100~128. 신규대표+102(작은빛),+104(넓은흰plume일부),+106(좌측큰불꽃),+110(32×32변형),+118이후파편/부분cropping. 정확개별firstframe은observed_contract.json 참조.
fixture2: 같은weapon_1610_capture/frame_600.state. +31 다른gray그룹, +63~94 흰/민트연속효과문맥. **후보HD재생검증은수행하지않았다.**

Claude는신규7개HD등장/기존32보존/흰핵색영역/작은파편/내부절단면/가림/UI순서와준비후소실을판정할것. 제작용원본계약수집과hash/크기확인은공식QA/재생합격증거가아니다.

## 변경 경계
live그림/library/DB/core/EXE/player설정변경없음. root만신규7개설치·exact굽기,Claude가공식audit/후보실재생담당.
