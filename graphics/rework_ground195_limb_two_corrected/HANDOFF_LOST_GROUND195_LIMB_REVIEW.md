# Ground195 큰 두 조각 같은 ID 교체 후보

미검증 후보. 신규 완료 수 없음. 공식 검사·실제 재생은 Claude가 수행한다.

- ID 92345 / metadata92344 / RGB4237753839 / 32×32. unit152 mechanical_cutin_168.state +195 OAM13 (149,67), flip 없음. IMG10779 (0,24).
- ID 92347 / metadata92346 / RGB3925135182 / 16×32. unit153 mechanical_cutin_168.state +195 OAM14 (170,83), flipX. IMG10749 (96,0).
- 후보 candidate_atlas.png SHA256: 87fa2b6f8af34535e1cd63547241b1d5b1fc678eccd6158af1217a2ea3a0eaa7.
- contract.json / replacement_targets.json / installation_map.json / native_atlas.png.

## 고친 그림 구조

92345의 원본은 넓고 불투명한 하부 지지면이 있는데 기존 그림은 작은 빈 V로 바뀌었다. 새 그림은 넓게 채워진 하부 면과 파란 삽입 면을 유지했다. 92347은 실제로 떨어진 상부 세로 조각과 하부 장갑이며, 새 생성에서 두 분리 영역을 유지했다. 왼쪽 절단면에 인위적 끝막음을 만들지 않고 원래 OAM 너비 안에 배치했다.

두 대상의 기존 dynamic_palette=False를 그대로 보존했다. 원본 index bytes/16색/해시/크기는 이전 연결과 기계적으로 일치한다. 라이브 전체에서 같은 resource+전체 actual palette에 겹치는 source 사각형은 발견하지 못했다(source_overlap_lookup.json). 전체 의존관계는 whole_pose_dependencies.json에 원래대로 유지했다.

## Claude 검토 위험

새 그림에도 원본보다 정교한 둥근 상단 관절과 표면 홈이 들어갔다. 원본 팔레트 내의 회색 비율, 파란 면의 크기, 하부 지지면 폭/각도, 두 분리 조각 사이 간격 및 flipX 조립을 실제 원본과 판정해야 한다. 제작용 replacement_preview.png는 공식 검증 결과가 아니다. 이번 대상 외 healthy 조각이나 앞서 쐐기2는 수정하지 않았다.

## 제작 근거

내장 imagegen 결과를 4배 OAM 캔버스로 정렬한 후보다. native RGB/alpha를 후보에 찍지 않았고 alpha 문턱·침식·팽창을 사용하지 않았다. reference_native2.png는 계약 index+실제 palette로 재구성한 참조이며 생성용으로만 사용했다. 생성 원본 parts_generated_raw.png와 generation_provenance.json 보존. 공유 라이브·DB·코어·공식 검사 변경 없음.
