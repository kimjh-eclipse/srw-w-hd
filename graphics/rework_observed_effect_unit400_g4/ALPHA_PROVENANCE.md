# Unit400/w1577 실제 FX 기본형 제작 group4

- 실제 입력 `test_current/parts/native_weapon_source_400_1577/unbound_now.json`의 rendered_obj_cache 원본 raw/전체실제palette/RGBhash/OAM/좌표/변환/state/frame을 보존했다. 대표 state `test_current\parts\native_weapon_source_400_1577\unit400_weapon1577_source.state` +665. source input 채집의 actual cache 계약이며 MMU source 추정 사용 없음.
- 1개 실제 RGB 계약. resource=None/owner_confirmed=false. 원본 IMG 소유를 입증하지 못했고 단색 다중IMG alias도 특정하지 않는다. source_x/y는 실제 IMG가 아니라 이 후보를 위한 가상64셀 배치 좌표다(source_grid_scope 참조). 원래 IMG 좌표로 해석 금지.
- 후보 `test_current\parts\retained_fx_round2\art_unit400_g4/candidate.png`, [256, 256]/native [64, 64], SHA `7ce62fdea9e3bfc01bfce28e485efd74b2035854732350989a1417dbc82eb820`. 모든 actual RGBhash 재계산일치, 최신exact/indexed 중복 0. live 설치 직전 다시대조.
- 자기 생성 그림1장. 각 가상cell의 생성alpha bbox를 위치/크기 계산에만 사용하고 실제 RGBA alpha는 보존. 다른효과/타팔레트 재색칠 없음. native mask/RGB stamp/코드색채움 없음. 독립셀은 source IMG 연속관계를 모르는 서로 다른 actual 객체이며 원래 연속그림이라고 단정하지 않음.
- prepare 1개 모두 maxA>=16/support>=.1. 단색 group4/5는 전체 crop alpha 최소255/불투명100%. 단색 재료는 자신의 새 opaque 생성본 내 균일 불투명 영역 RGBA를 crop/resize했으며 선택위치/색은 production_report.json에 보존. minA 확인은 시각품질 QA가 아님.
- 알려진 한계: flat 자기 생성 mint 재료는 실제 [230,255,230]에서 최대4/255내 차이 가능. 선택한 ownRGBA는 production_report.registration에 공개. 원본RGBA로 코드 채우지 않음. 약한 미세alpha와 prepare 분리성분 제거는 production_report.json에 명시, 실제가림/좌표/시각판정 Claude 대기.
- 전체 원본42계약은 고유raw14. 기본14를 이6그룹으로 제작했고, 다른28fade 변형은 `unit400_1577_input/fade28_source_base_pairs.json`에 실제source/base 그림·hash·state/frame페어를 남겼다. 28은 신규그림/완료수 제외. 단순 색재사용으로 채우지 않았음.
- 라이브/library/DB/core/EXE 변경 및 독립audit/실제HD 재생 없음.
