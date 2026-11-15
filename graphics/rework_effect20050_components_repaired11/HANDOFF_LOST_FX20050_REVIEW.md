# FX20050 문제13 중 후보11 / 보류2 인계

상태: **미검증 후보11, 미완료 보류2**. 신규 누락/완료 수 증가 없음. 공식 검사와 실제 재생 판정은 Claude 담당이며 이번 작업에서 돌리지 않았다.

## 설치 파일

- installation_map.json은 기존 ID11개 교체만 포함한다. candidate_atlas.png / native_atlas.png와 함께 사용한다.
- 후보 SHA256: 2c09e35127c01767007f648f05060a8beee9e72d2d46cc564280c3295080908f.
- 후보:94711/94712/94713/94714/94715/94716/94718/94719/94720/94724/94725.
- 보류:94721/94722는 설치 맵에서 제외했다. HELD_FRAME350_NOT_FOR_INSTALL.json에 실제 원본/실패 생성/성분 진단을 보존한다.
- 정상94710/94717/94723은 수정하지 않았다. preserved_normal_three.json 및 latest 파일의 전체spec SHA가 모두 불변이다.

## 원본·팔레트·별칭

13개 모두 보존된 실제 cached OBJ/core.obj 관측이다. 대표 source는 native_weapon_source_248_1015/unit248_weapon1015_source.state +330~360이며 각 state/frame/video_epoch/OAM/attrs/flip/actual palette는 contract.json에 보존했다. ROM 패턴을 미관측 확장한 것이 아니다.

13개 실제 BGR555 CRC를 index bytes와 full16색으로 다시 계산해 기존 ID와 같음을 확인했다(mechanical_input_identity.json). 원래 actual cached 각crop이 IMG20050 bytes와 같았던 근거도 original_cached_to_ROM_source_proof.json에 보존했다. 실제 업로드 소유는 단정하지 않고 owner=None을 유지한다. actual hash의 다른 바인딩과 같은 resource/fullpalette의 다른 source 사각 교차는 각각 actual_hash_alias_lookup.json/source_overlap_lookup.json에서 없었다. 따라서 정상3의 큰 그림에 포함되는 child를 별도 새 그림으로 덮은 경우는 발견하지 못했다.

**source_x/y는 원본IMG좌표, atlas_box와 proposed_binding x/y는 새 후보의192×128 배치다. 두 좌표 공간을 혼동하지 않는다.** 모든 기존 lookup/rgb/indexed/dynamic/effect 플래그는 보존했다.

## 같은 실제 화면에서 연속한 부품

- +330의94713/94714/94711은 실제(57,29)/(89,30)/(121,32) 배치,96×11 master다.
- +345의94719/94720은 실제(138,32)/(170,42) 배치,64×26 master다.
- +350의94721/94722는 실제(146,41)/(178,44) 배치,64×19 master이나 이번 후보에서 보류다.

actual_screen_groups.json과 각 *_native.png에 원본 실제 배치와 오프셋을 보존했다. 단순 raw시트 가로인접을 연속물체로 해석하지 않았다. 연결된 main은 생성 한 그림을 그대로 유지한 뒤 실제OAM사각형으로 나눴다.

## 생성과 성분 정렬

generated_0/1/2_raw.png, generated_retry_raw.png, generated_frame350_single_raw.png는 내장 imagegen 원본이며 SHA는 generated_files.json에 있다. 원본 RGB/alpha를 후보에 덮어찍지 않았다. 생성 알파를 문턱/침식/팽창으로 삭제하지 않았다.

분리 성분은 원본과 생성의 성분 수·x순서·색/문맥이 명확히 대응할 때만 자체 생성 RGBA의 수직 지리 분할영역을 각 원본 성분 bbox 위치/크기로 정렬했다. 원본 bbox는 위치·크기에만 썼다. alpha160은 생성 성분 anchor를 **측정**하는 기준일 뿐 출력 알파가 아니다. 각 분할영역은 생성 원본의 모든 RGBA를 보존하며 원본 마스크를 전사하지 않는다. 긴 연결 main을 잘라 여러 점으로 바꾸지 않았다. generation_alignment_provenance.json에 영역/배율/이동을 모두 기록했다.

## 생산 진단과 한계

최종 계약의 candidate 좌표를 NullCache prepare로 준비한 후,11개/원본36성분 각각의 bbox에서 paint를 확인했다(per_component_prepare_presence.json).36개 모두 maxalpha255/alpha16이상paint 존재,unattached 성분 제거0이다. DB쓰기는 없었다. 이는 tiny가 완전히 사라지지 않았다는 **생산 존재 근거**이며 형태·색·정체·실제재생이 맞다는 공식 QA가 아니다.

새 그림의 둥근 작은 광점/표면 명암이 원본의 납작한 cyan조각과 다를 수 있다.94724/94725는 원본의 연결성과 실제색을 보존하려고 상대적으로 평평한 표현으로 생성되어 다른 광점의 화풍과 다를 위험이 있다. 긴 trail의 절단 경계/굵기/원본 대비 밝기는 Claude가 실제 장면에서 판정해야 한다.

+350은 원본 실제 master8성분이다.7+2 OAM 성분 수를 단순 더한9라는 초반 설명을 수정했다(native_group_component_layouts.json). 모델이 여러 번7/11개의 고알파 성분으로 붙이거나 나누었다. 이를 강제로 알파 삭제하거나 연결해 수치를 맞추지 않고 원본 두 ID를 보류했다. 실패 그림은 재활용/완료 처리하지 않는다.

공유 라이브/DB/코어/공식 QA/물리 입력 변경 없음. root가 같은 ID 연결·굽기를 하고 Claude가 독립 검증한다.
