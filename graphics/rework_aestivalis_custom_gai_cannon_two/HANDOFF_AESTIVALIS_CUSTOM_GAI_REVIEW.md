# 아스테바리스 커스텀 가이 포격 신규 2종

미검증 후보·연결 준비. 공식 QA/실제 재생은 Claude 담당. 라이브/DB/코어 변경 없음.

unit194 무장807 격리 진단메뉴 frame180에서 저장된 source_mechanical_194_807/source_pose.state 로드 후 1회 run 실제 cachedOBJ + renderedOAM. 팔레트0 기체16OAM 중 신규2종2OAM, 나머지14기존 의존. whole_pose_dependencies.json은 전체좌표/가림/역순 조립용. source_identity_and_connection.json에서 최신 exact/indexed 0. 실제사용palette와 ROM palette 후보도 함께 기록. ROM11414 첫 원본 byte 일치 (0,64), (32,32); 단독소유 유일성은 미확정.

설치 installation_map.json + candidate_atlas.png 768×288 / native_atlas.png 192×72 정확4배. 원본indexSHA/크기/RGB/alpha 정합은 mechanical_contract_checks.json, 빈 후보/alpha_max16미만0은 candidate_presence.json. 실제 그림 품질이나 게임 검증 통과 뜻 아님. SHA 4fe69bd7c3d523cf9ece9f292691f2435bb75ad82f6ddb792ca9c0940c606151.

parts_generated.png는 imagegen exec-03861e9a 출력. native 셀·기체전체bbox문맥으로 새그림 제작, 다른 기체/팔레트 재색칠과 원본RGB/alpha복사 없음. 생성자체 알파bbox를 실제가시bbox에 정렬. 청록 하이라이트와 회색 연결부, 파란 판금의 지지영역·접합 외곽선은 미검증. 생성에서 회색 연결편을 조금 세분화하고 둥근 볼트를 추가했을 위험이 있어 Claude가 원본 조립과 비교 판정해야 함. 일부 주변 연무는 투명 재요청 후에도 프리뷰에 보였으므로 alpha 경계 잔여 검토 필요.

Claude:
```powershell
python scripts/verify/verify_runtime_path.py --state test_current/parts/borrowed_shape_rework/source_mechanical_194_807/source_pose.state --frames 120 --save-frames 0 15 30 60 --track-atlas aestivalis_custom_gai_cannon_missing --name aestivalis_custom_gai_cannon
```

190/789 신규 차집합0. 196/814 미연결2개는 기계/흰방사선효과 역할 불명확하여 본 묶음에 포함하지 않았다. 전무장완료 주장 없음.
