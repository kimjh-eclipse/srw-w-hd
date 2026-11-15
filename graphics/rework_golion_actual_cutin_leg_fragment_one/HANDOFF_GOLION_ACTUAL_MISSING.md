# 고라이온 컷인 미연결4개 실제 역할과 기계1개 새 후보

## 결론

미연결4개 중 **세 개는 순수 검정 지면 그림자**, 하나만 실제 회청색 다리/골반 접합 조각입니다. 세 그림자를 기계 다리 3개로 오인해서 그리지 않았습니다. 실제 기계 조각 1개에 새 그림과 신규 설치 계약을 준비했습니다. 아직 실제 HD 재생/공식 QA/라이브 연결/굽기는 하지 않았습니다.

## 실제 원본 추출

- Claude 표본: test_current/combat/runtime_path/claude_sample_393/report.json, state test_current/combat/golion_cutin.state, 180프레임 보고서 HD 면적 .877 / vanished0 / unbound max4.
- 생산용 별도 headless Core로 같은 state의 +0/30/60/84/120/154를 actual rendered OAM과 cached OBJ API에서 추출했습니다. 소스 입력만 얻었고 HDRenderer나 공식 QA는 실행하지 않았습니다. 모든 frame/epoch/속성/실제16팔레트/index/RGBhash는 all_rendered_obj_contracts.json/unknown_source_contracts.json에 있습니다. core_path/실제 SHA는 capture_identity.json.
- cached API는 enabledTrue에서만 채워져 생산 core를 enabledTrue로 추출했습니다. 이때 whole_native_*.png에는 기존 core suppression이 포함될 수 있으므로 **순수 원본 비교 증거가 아닙니다.** 전체 문맥은 Claude가 저장한 golion_cutin_native_reference/native_120.png를 사용했습니다.
- oam6_pure_native_context.png는 그 순수 원본에서 실제 사각을 강조한 자료입니다. 초기에 잘못된 세로배율로 강조했던 파일은 최종 올바른 비율로 정정했습니다.

## 실제 미연결 분류

| raw cell | OAM | actual RGBhash | 원본사각 | 실제 역할 | 신규그림 |
|---|---|---|---|---|---|
|0|16|1658932538|16×16|순수 검정 그림자 가운데|없음|
|1|17|2007164626|32×16|같은 검정 그림자 오른쪽|없음|
|2|18|1164961886|32×16|같은 검정 그림자 왼쪽|없음|
|3|6|2861633776|32×8|다리/골반 위 회청색 접합 조각|새 후보1|

- 그림자3은 full16 동일/palette bank15/사용 index1 RGB(0,0,0)뿐입니다. screen x120/135/89,y112, 전체사각89..167×112..128의 연속 그림자입니다. 실제 원본 계약은 shadow_role_three.json에 따로 기록했습니다.
- 그림자3 **사각 면적**256+512+512=1280은 보고서 timeline +0~78 unbound_area1280과 일치합니다. +84의1536은 기계32×8=256이 추가된 값과 같습니다. HD88%라는 면적수치를 다리 장갑 여러 개의 소실로 해석하면 안 됩니다.
- 기계1은 +84/+120/+154에서 관측됐고 actual exactRGB/안전indexed 모두0입니다. 같은 fullpalette 기존 큰 원본에 완전포함도0(native_parent_containment.json). 기존 큰 파츠 그림을 빌려 재색칠하지 않았습니다.
- 그림자3은 새 기체 그림 증가/완료로 세지 않습니다. 원본 검정 그림자를 유지할지 별도 준비 규칙으로 처리할지는 runtime/Claude 검토로 남겼습니다.

## 새 기계 그림과 설치

- 새 raw exec-f0a93758-59b5-46d7-8e6a-5b681bc0cec4.png를 generated_leg_raw.png로 보존. native fragment와 실제 전체 기계 문맥을 참조했고 완성 기체/다리/발로 자동완성하지 않도록 요청했습니다.
- 넓고 얕은 회청색/은색 두 면과 검정 불투명 연결구조를 원래 높이·오프셋대로 새로 그렸습니다. 도트 확대/사슬 마디·임의 나사/밝은 색 발명은 피했습니다. 원본 RGB/alpha 전사·문턱 삭제·native mask 출력 없음. 생성 자체 RGBA의 bbox 기하 정렬만 했습니다. alignment_provenance.json.
- 설치용 installation_map.json **신규 exactRGB binding 필요** 1개. hash2861633776/index/fullactual팔레트는 source cached와 같습니다. source_owner/resource=None을 유지하며 원본 IMG를 추정하지 않았습니다. install_contract.json/leg_contract.json/native_atlas.png 함께 사용.
- candidate_atlas.png SHA256 `faa843316fa60ae08a6f9308b33093fb53bd10846678096c3b4a82a5a210f70f`. 실제4배128×32, native32×8.
- 정상 기체16개 의존관계와 현재 spec 불변은 existing_normal_pose_dependencies.json/기계적 최신 비교 existing_normal_dependencies_latest.json에 보존했습니다.
- candidate와 NullCache prepare 사전기하 flags0, IoU .846/미칠 .027/외부0. 같은 source 원본 crop과 새 그림/prepare를 leg_replacement_comparison.png에 나란히 저장했습니다. 그림 준비 검사이며 Claude 공식 판정 아님.

## Claude 확인할 것

- source state golion_cutin.state +84/+120/+154에서 실제 기계의 작은 회청색 접합이 주변 정상 허리/다리 그림과 이어지는지, 은색 상단의 명암과 검정 접합 부분이 과도하게 돌출되지 않는지 확인해야 합니다.
- 실팔레트 색 분포는 유지하려 했지만 새 하이라이트가 원본보다 밝거나 평평할 수 있습니다.
- 원본 전체32×8에 캔버스 바깥 새 그림은 없으며 임의로 주변 기계 영역을 메우지 않았습니다.
- 이번1개 설치 후에도 그림자3은 미연결로 남습니다. 장면 모든 HD 완료/최종88→100%를 주장하지 않습니다.
