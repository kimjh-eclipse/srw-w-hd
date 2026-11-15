# 22342 대각선 효과5 후보 인계

상태: **기존 같은 ID5개 교체용 미검증 후보**. 정상28 유지. 후보와 NullCache prepare 출력 모두 같은 사전 기하 도구 경고0이다. 실제 HD 재생·전체 색/화질 판정은 Claude 대기다. 숫자 통과로 완료라고 주장하지 않는다.

## 설치 입력

- 최종 installation_map.json / candidate_atlas.png / native_atlas.png / contract.json.
- 기존92543/92545/92546/92547/92548 교체, SHA256 ae646c036cc4fe8dd79344a830d73ac441acedf1656db076d0b43fbfdbdeaec0.
- candidate_atlas_geometry_v2.png도 최종과 파일바이트 동일한 복사본이다. installation_map_geometry_v2.json은 같은 후보의 명시 경로 맵이다.
- before_geometry 파일은 너무 가는 실패 초안이므로 설치하지 않는다. source_box와 후보 atlas_box는 구분해 저장했다.

## 실제 관측2 / ROM 보충3

true_missing_22342/install_contract.json의 원래 계약을 source_packet_original로 보존한다.92543은 unit254/mechanical_cutin_168.state +101,92545는 +97 실제 cached OBJ다. source raw/actual full16색/OAM/attr/flip/video_epoch는 각 source_contract에 남아 있다.

92546/92547/92548은 **원래부터 actual_observed=False인 ROM 보충**이다. slot/frame은None, source_type은 ROM_expansion_unobserved로 유지했다. 원래 IMG22342 raw index exact/실제 full16색 팔레트 근거를 보존하며 관측됐다고 바꾸지 않았다. 실제 표시 검증은 아직 남아 있다.

모든5개 BGR555 CRC/indexbytes/wh/full16팔레트는 mechanical_input_identity.json에서 기존 바인딩과 같았다. 후보 IMG와 실제 업로드 소유는 구분하며 owner=None 유지. 정상/문제 사이 같은 이미지/전체 팔레트의 source사각 교차는 없었다(source_intersections.json). 별도 hash별 ID는 actual_hash_alias_lookup.json.

## 그림·폭·곡률 교정

원래 문제는 가는18개 대각 성분/분리점이 굵은 빔/구부러진 리본처럼 바뀐 것이었다. 실제18성분은15종의 서로 다른 원본 조각이다. components_unique_contract.json에서 원본 component indexbytes/크기/full 실제 팔레트가 완전히 같을 때만 동일 자체 생성 RGBA를 여러 원래 위치에 공유한다.

imagegen 내장 도구로 generated_components_raw.png의15개 광선/단순재료를 새로 그렸다. components_reference_smooth.png는 원본 위치·색을 읽기 위한 확대 참조일 뿐 후보로 복사하지 않았다. 모델이 잘못 남긴 번호는 모든 재료 바깥의 상단12% 사각 header만 지리적으로 crop했다. alpha값으로 지운 것이 아니며 원출력은 보존했다.

처음 bbox맞춤 후보는 너무 가늘고 곡선 위치도 어긋나5개 모두 같은 사전 기하 도구에서 걸렸다. 이를 설치 후보로 넘기지 않고, **자체 고해상도 생성 RGBA만** 제한된 실제 중심 앵커(성분당 최대7개)의 monotone PCHIP와 법선폭으로 기하 변형했다. 폭은 원본 면적/중심 곡선 길이의 단일 스칼라로 추정했다. 이 과정은 원본 RGB/alpha/마스크를 출력에 찍거나 출력alpha를 증폭/임계처리하는 방식이 아니다. 매우 단순한 한 행짜리 불투명 재료는 자체 생성 재료의 안쪽 사각을 crop/확대하여 장식을 발명하지 않았다.

geometry_v2_provenance.json은 원출력SHA/실제 중심 앵커/폭 스칼라/좌표/같은 원본 성분 공유를 남긴다. 원래 성분 위치에 조립했으며 normal28 전체 spec SHA는 보존 전후 동일하다.

## 생산 진단과 Claude 위험

- NullCache prepare 뒤 원본18개 성분 각각 bbox에 paint가 남는다(per_component_prepare_geometry_v2.json). DB/라이브를 바꾸지 않았다.
- root의 preflight_candidate_geometry.py를 최종4배 PNG와 prepare 조립에 각각 사용했다. alpha128→4×4 집계, IoU<.60/미칠>.20/원거리밖>.15 기준을 그대로 유지했고 양쪽 모두 경고0이다(candidate_geometry_preflight.json / prepared_geometry_preflight.json).
- 이 검사는 기하만 본다. 생성이 넣은 미세한 잔가지·가장자리 반사/선, 원래 노랑·흰 패치의 정확한 색과 자리, 단순 재료의 평면감은 실제 화질 판정이 남아 있다.
- 기하변형이 자체 생성색 패치를 따라 늘리므로 white patch의 위치가 원본과 달라지거나 작은 조각 경계가 너무 정돈돼 보일 위험이 있다. 재색칠로 검사 통과시키지 않았다.
- 실제 관측 두 프레임 외3개의 ROM 보충은 실제 표시 프레임을 찾아 확인해야 한다. 준비됐다/수치통과와 실제 표시 완료는 구분한다.

라이브/DB/공유코드/코어/EXE/모니터/물리입력 변경, 공식 audit·독립 HD 재생은 하지 않았다.
