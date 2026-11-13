# 소드 계열 실제 메뉴 원본 후보 42_230

현재: 그림 제작 및 설치 입력 준비, Claude 검토 대기.

- candidate_atlas.png / native_atlas.png / install_contract.json 8개 / provenance.json. 원본 정확4배, 각 부품 자체 생성 투명도 사용. 원본RGB/alpha stamp·wholepose이웃crop 없음.
- 정상 native 메뉴 fixture `test_current\parts\native_weapon_source_42_176\unit42_weapon176_source.state` +230, OAM [3, 4, 5, 10, 12, 13, 14, 15]. 전체 원본문맥 test_current/parts/actual_mechanical_pose_42_230/whole_native_context.png.
- 기존 부품 preserved_existing_pose.json대로 보존. 라이브/DB/코어 미변경. actual palette 사용, source_owner IMG 미확정 None.
- 실제 prepare_texture 메모리 nonempty만 확인. 공식 audit/독립 HD replay 없음. 검증 완료 표시하지 않음.
- 알려진 위험: 원본과 생성된 부분 헤드/칼날 연결부·색상·절단면 형태 정확성은 Claude가 판정. 모델이 부품 장식/외곽선 발명했을 수 있음.
- 이 자세에 남은 미분류 작은 source 1개는 remaining_unclassified_source.json 참조. 19/42는 OAM8 16x8 중 불투명5픽셀인 조각으로 소유역할 불명확해 임의 모양 추가하지 않음. 이 둘을 자세 전체 HD 완료로 세지 말 것.

## 설치 통계 정정
18계약 가운데19/42 OAM13/14/15 공통 무기 세조각은 원본bytes·크기·실사용색이 완전히 동일하여 19 그림 연결을42에서도 보존. 총15고유 RGB 바인딩이며 다른 기체 재색칠 아님. cross_unit_exact_aliases.json 참조.
