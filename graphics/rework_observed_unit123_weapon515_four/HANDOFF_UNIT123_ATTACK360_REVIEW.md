# 실제 unit123 / weapon515 메뉴360 기계 4종 + 3밴드 재료1 후보

상태 `CACHED_OBJ_ARTWORK_CANDIDATE_UNVERIFIED`. 실제 HD 재생 및 공식 검사는 Claude 대기. 라이브/DB/공유 코드/코어 변경 없음.

- 최종 설치 입력: installation_map.json, candidate_atlas.png, native_atlas.png, contract.json. 총5종 전부 actual exact0/indexed0.
- 최종 후보 SHA256: `c433239a98f6129824d7dcb165b98922a05a54fc5d616e1f360a225be937f1bb`.
- 이전4종 후보(a53275...)의 각 생성 crop RGBA는 완전불변이다. 이번 증가분은 최종셀4의 재료1개뿐이며 앞4를 다시 신규수로 세지 않는다. three_band_material_provenance.json에 불변 crop SHA 증거.
- 실제 fixture: source_mechanical_fixed_123_515_350/source_pose.state +0. 메뉴360 실제 cached OBJ/OAM/팔레트/코어SHA 확보.
- 셀0..3 그림4: IMG10385 3종/10406 1종 원본 인덱스 바이트 일치, 전체16색 PLT1765 bank0. 셀1 머리32×32 source(40,0)와 셀0 오른쪽8×32 source(72,0)는 실제 화면(135,98)/(167,98)에서도 가로연속. 같은 full16/반전없음 증거로 한40×32 생성 master를 분할했다. 재조립RGBA동일/사각지원밖누락0. 빨강뿔/작은노랑면/초록눈·카메라는 원본색 참조. 다리/관절은 각각 원본 절단형태로 제작.
- 생성원본 보존, 생성 자체 alpha<64 정리·고알파RGBA 불변. 원본RGB/알파 복사·스탬프 없음. 제작 조립은 실제 HD 검사 결과가 아니다.

## 최종셀4: 8×8 실제3밴드 재료

작은 시트에서 균일면으로 오독했던 것을 인덱스 검산으로 정정했다. 실제는 위 검정1행/RGB16,16,16, 가운데 회보라3행/RGB106,106,131, 아래 짙은회색4행/RGB74,82,98의 3색 가로띠다. 단색 생성 시도는 assertion에서 중단돼 반영되지 않았다.

root 지시에 따라 이 알려진 그림 구조를 독립 절차 재료로 제작했다. `unit123_generate_three_band_material.py`가 새 불투명32×32 캔버스에 세 고정색 사각 밴드를1:3:4로 그리며, native 픽셀/알파/마스크를 복사하지 않는다. 장식/외곽선/해부학적 이름을 발명하지 않았다. 결과는 three_band_material_generated.png, 근거는 three_band_material_provenance.json. 이 항목은 AI 새 기체 원화가 아니라 독립 3밴드 재료라는 종류를 명시했다.

원본 hash2329246620/OAM7/priority2는 +0/+10/+30에(149,122)→(125,74)→(122,69)로 머리와 함께 이동한다. 머리 OAM4 뒤/다리 OAM8 앞의 머리 하단 안쪽에 놓이는 실제 평면 조각이며, 정확한 해부학적 이름과 가림의도는 미확정이다. held_patch_role_trace.json의 인접 native 추적 참조. 첫 IMG10342 검색 일치를 단일소유로 확정하지 않아 이 재료의 resource는 null/source_candidate_matches로 보존했다.

Claude 위험: 머리 눈/카메라크기·빨강뿔/노랑면·얼굴비대칭, 오른쪽8px 분할이음새, 다리/관절과 기존몸체 경계·명암·AA, 재료의 실제 가림순서/색밴드 표시를 확인해야 한다. 전체기체/무장 완료로 세지 않는다.
