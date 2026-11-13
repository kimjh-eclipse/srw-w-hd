# 진겟타 1·2·3 공격 기계 세부 5종 제작 인계

미검증 후보. 공식 시각/실재생 QA는 Claude 담당이며 실행하지 않았다. 공유 runtime/라이브/DB/코어를 수정하지 않았다.

- 실제 정상 메뉴에서 unit291 weapon1169 +310 / unit292 weapon1174 +300 / unit293 weapon1180 +220에 source state를 저장하고 다음1프레임 cachedOBJ/rendered OAM을 캡처했다. 각 source_mechanical_UID_WID/source_pose.state +0이 같은 입력 상태다.
- 고유5는 각각1/3/1종. 전체3자세48 OAM의 나머지는 기존 연결 의존이다. 전체기체48종을 새로 그렸다는 뜻이 아니다. exact0/indexed0/core0은 source_identity_and_connection.json에 기록했고 실제 사용색과 일치하는 ROM 팔레트 후보도 있다.
- source IMG14526 1종 / IMG14577 3종 / IMG14685 1종 전체 raw index bytes가 일치한다. 첫 ROM witness이며 유일 소유 증명은 아니다. 같은 그룹 내부 source rectangles는 서로 포함하지 않으므로 다른 그림의 부분을 무작정 재사용하지 않았다.
- candidate_atlas.png/native_atlas.png/installation_map.json 설치 입력. 후보 SHA2569f44992252d877069f02673ec79fe744b3651680066b16211c42da8ccdb587ce.4배, 모든 raw index SHA/실제 팔레트 RGB/크기/후보 존재 기계적 확인은 mechanical_contract_checks.json.
- 실제 원본 색을 유지하도록 내장 imagegen으로 제작했다. 첫 작은 회녹색 연결편/겟타2 은보라 연결부 및 붉은 기계 조각/겟타3 노란 원형 장갑의 회보라 홈을 그렸으며 새로운 사람 얼굴이나 임의 눈은 만들지 않았다. 원본 RGB/alpha stamp나 기존 다른기체 재색칠을 사용하지 않았다.
- candidate_pose_sequence_production.png는 새5만 반영하고 기존 의존은 native로 남겨 실제좌표/반전/priority+OAM 역순 제작 조립을 만든 것이다. HD 게임 화면 또는 공식 재생 판정이 아니다.
- Claude 확인: 작은0 연결편의 실제홈과 색영역, 겟타2 세 조각의 팔·드릴/발 접합, 겟타3 원형 장갑/회보라 홈이 원래 기계 형태와 맞는지 및 같은파츠가 다른동작에 쓰일 때 지원영역 보존. 셀0의 새 구멍 내부 보라 디테일과 셀3의 끝 돌출은 원본보다 구체화되어 있어 독립 확인이 필요하다. 기체 얼굴이 정확하다는 완료 주장을 하지 않는다.
- 추가 source 분류: 보스보롯트301 무장1236/1238 초반5는 실제 whole에서 슬래시/궤적 조각이므로 기계 제작에서 제외했다.1240은 네이티브 메뉴에 없어 강제 실행하지 않았다.
