# 아스테바리스 커스텀 가이 플레어 다리 신규 2종

미검증 후보. 공식 QA/실제재생 판정은 Claude 담당. 라이브/DB/코어 변경 없음.

unit194 무장808 격리 진단메뉴 frame170 source_mechanical_194_808/source_pose.state 로드+1 실제cachedOBJ/renderedOAM. 팔레트0 기체19OAM 중 본후보 신규2, 앞선 cannon의 공유3874693915 1개, 아직 별도 제작 필요한 노랑 작은 단2종과 나머지14기존 의존. 전체 whole_pose_dependencies.json. 앞선다른그림 재색칠/원본RGB와alpha찍기 없음.

원본ROM11414 (0,32)/(200,0) 실제bytes일치, actualpalette·exact/indexed연결0은 source_identity_and_connection.json. 원본 계약크기/indexSHA/색/alpha정합 mechanical_contract_checks.json. 후보4배768×288/native192×72, 빈그림0·alpha최대16미만0 candidate_presence.json. SHA 5c2a71d9df35086b83bf9cd029c5655a0aac40ffd9f8714d6152f64eed9ddd32.

parts_generated.png imagegen exec-74fb9f2b 새그림. 앞선2회는 고무판 같은 평평한블록/굵은경계로 실패하여 채택하지 않았음. 최종은 실제전체기체위치문맥을재참조해기계판금으로생성. 생성자체알파bbox정렬만 적용. 원본 매우어두운 actualpalette 대비 하이라이트가 밝아졌을 위험, 세로장갑 홈이 원본검은면과 대응하는지, 연결절단면/지원알파에 연무가 남았는지 Claude 판정필요. 품질통과 주장 없음.

unit194_production_assembly.png는 기존파츠 원본과 조립한 제작자료이며 게임HD재생증거 아님.

Claude:
```powershell
python scripts/verify/verify_runtime_path.py --state test_current/parts/borrowed_shape_rework/source_mechanical_194_808/source_pose.state --frames 120 --save-frames 0 15 30 60 --track-atlas aestivalis_custom_gai_legs_missing --name aestivalis_custom_gai_legs
```

노랑 작은단1792706204/3201486845는 부모에게 별도원본그룹 제안했고 본다리2계약에는없음. 전자세완료 주장 없음.
