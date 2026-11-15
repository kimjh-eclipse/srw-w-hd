# 21071 청록색 효과 3개 제작 후보 인계

## 범위와 상태

- 기존 문제 5개 중 92596/92597/92599만 같은 ID 교체용 새 후보입니다. 신규 누락 증가가 아닙니다.
- 92601/92604는 정상 부모 92602 안의 원본 부분영역이고, actual 16색과 기존 생성 RGBA까지 이미 동일합니다. 다시 잘라 등록해도 문제가 해결되지 않으므로 설치 목록에서 제외하고 기술 보존·미해결로 남깁니다. 증거: normal_parent_child_current_RGBA_comparison.json.
- 정상 21개 spec 불변을 preserved_normal21_latest.json에 기록했습니다. 라이브 그림/DB/코어 변경은 하지 않았습니다.

## 입력과 제작

- 원본: test_current/parts/true_missing_21071/install_contract.json의 실제 cached OBJ. 교체 3개 모두 unit325/weapon1320 source.state +305 관측입니다. ROM 보충은 0개입니다. 원래 OAM/epoch/속성은 contract.json source_contract 및 source_packet_original에 보존했습니다.
- 실제 팔레트는 청록/하늘색이며 ROM IMG21071의 PLT21070 분홍색 변형과 전체 16색이 다릅니다. ROM 팔레트로 재색칠하지 않았습니다.
- 원본 분리 성분 10개를 각각 새 고해상도 재료 10개로 생성하고, 원래 사각 내부 위치에 기하 조립했습니다. 원본 RGB/alpha를 찍거나 native mask로 깎지 않았습니다. 전체 크기는 native 4배입니다.
- 높은 해상도의 자체 생성 RGBA를 원본 중심선 앵커(최대 7개)·폭의 스칼라에 맞춰 기하 변형했습니다. 알파 gain/문턱 제거는 없습니다. 단색 한 점/한 열은 자체 생성 재료의 안쪽 면을 확대 사용했습니다.

## 설치 파일

- installation_map.json: 교체 3개만 포함. source_cell은 원래 contract의 0/1/2, atlas_box와 proposed spec 좌표를 유지합니다.
- candidate_atlas.png: 최종본, SHA256 `c47550bd4aee9b20c9025c155f61b7a63b136c89f3f05db10c29bbd628d6658e`.
- native_atlas.png, contract.json, geometry_contract_replacement3.json, mechanical_input_identity.json.
- generated_components_raw.png는 원본 생성 출력 보존. 생성 출처 exec-e5f8bd77-f154-49ec-971c-233ce5eeed14.png.
- geometry_v2_provenance.json에 자체 RGBA 입력/출력 SHA, 중심선/폭, 실제 원본 성분 사용 관계 기록.
- candidate_atlas_before_geometry.png와 installation_map_before_geometry_repair.json은 실패/중간 기준이며 설치 금지.

## 생산 사전 검사와 한계

- 후보 및 NullCache prepare 후 같은 root_geometry_preflight 규칙: 3개 모두 flags 없음. IoU는 92596=.750 / 92597=1.000 / 92599=.927, 미칠·외부영역=0입니다.
- 최종 prepare 뒤 원본 10개 성분 bbox 모두 paint alpha16 이상이 남습니다. per_component_prepare_final.json. DB 쓰기 없음.
- replacement_comparison.png는 원본/옛 그림/새 후보 순서의 제작 비교입니다. 실제 재생/공식 QA 완료 증거가 아닙니다.
- 92596 원본은 3texel뿐이므로 .750도 새 후보의 한 native texel 차이에 해당합니다. 작은 하늘색 성분은 매끈한 효과보다는 작은 덩어리로 보일 수 있습니다. 92599의 짧은 가지·방향과 팔레트의 밝은 색 배치는 Claude가 실제 재생에서 확인해야 합니다.
- 생성 출력의 낮은 알파 RGB 잔여를 단순 키 색으로 제거하지 않았습니다. 안티앨리어스의 파랑/청록이 실제 배경에서 거슬리는지는 Claude 확인 항목입니다.
- 정상 부모와 이미 같은 92601/92604는 그대로이므로 원래 결함 판정의 기술 원인은 미해결입니다.

## Claude 재현

- state: test_current/parts/true_missing_21071/unit325_weapon1320_source.state
- 원래 관측 offset: +305 (추가 정상 부모/자식 +301도 별도 확인 가능).
- 원래 fixture/player와 전체 관측 OAM은 contract.json/원본 install_contract.json 참조. 공식 재생 검사는 Claude 담당입니다.
