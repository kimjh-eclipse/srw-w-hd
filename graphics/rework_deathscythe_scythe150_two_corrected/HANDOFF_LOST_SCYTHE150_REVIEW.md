# 데스사이즈 연속 에너지 날 같은 ID 후보2

미검증 후보. 신규 완료 수 없음. 공식 검사·실제 재생 판정은 Claude 담당이다.

설치 installation_map.json / candidate_atlas.png / native_atlas.png. 후보 SHA256 14750becd6e91d4f783555cbf43aeca4310ac41f75737b7bac2aa0f2f27fb97f.

- #92083 metadata92082 RGB1592824817, #92084 metadata92083 RGB3599948006, 둘32×16.
- 실제 fixture test_current/combat/duo_cutin.state +150, cached OBJ/core.obj 보존 계약. OAM24 (134,99), OAM14 (166,99). source IMG7105 (0,144)32×16 / (32,144)32×16. 동일 full16색·identity matrix·화면상32px 연속 배치다.
- 실제 역할은 기계 장갑이 아니라 초록 에너지 낫 날 FX다. 실제 초록은 키색이 아니므로 지우지 않았다. 기존 lookup/dynamic_palette/render flags를 그대로 보존하고 역할 설명만 별도 기록했다.

## 제작

기존 그림은 원본의 형상과 대체로 비슷하지만 넓은 중간·하단 면이 줄고 일부 spur가 가늘어지는 차이가 있다. 두 조각을 따로 그리지 않고 실제64×16 원본 연속 날을 문맥으로 하나의 넓은 생성 그림을 만들었다. 생성 전체를 단 한번 정렬/리사이즈하여4배256×64캔버스에 놓고, 정확한 x128에서 좌우32×16영역으로 나눠 공유한다. 반쪽별 정렬/폭 조정이 없으므로 중앙 접합의 생성 픽셀은 한 master에서 온다.

parts_generated_raw.png 생성 원본과 continuous_master_provenance.json 보존. 내장 imagegen exec-300cc659-bc66-49dd-b008-c3fadbefd653.png. native RGB/alpha를 후보에 찍지 않았다. 생성 알파를 자르는 문턱·침식·팽창 없음. alpha160은 전체 위치를 재는 anchor에만 사용했고 낮은 알파는 전체 RGBA 변환에 포함했다.

## Claude 위험

새 생성은 원본보다 부드러운 가장자리/명암을 만들었고 미세한 가장자리 speckle과 빛 번짐이 남을 수 있다. 하단 여러 fork 끝점, 상단 spur, 실제 넓은 면의 alpha가 원본처럼 유지되는지 실제 재생과 공식 검사로 판정해야 한다. 같은 master여도 실제 lower resolution 표현과 색비율 차이는 남을 수 있다. replacement_master_preview.png는 제작 대조 그림이며 공식 QA가 아니다.

original contract / current meta의 실제 hash/wh/index bytes/full palette 일치는 mechanical_input_identity.json. 같은 resource/full actual palette의 다른 사각 교차는 source_overlap_lookup.json에서 없음. 전체 기체 기존 의존관계 whole_pose_dependencies.json 보존. 공유 라이브/코어/DB/공식 QA/물리 입력 변경 없음.
