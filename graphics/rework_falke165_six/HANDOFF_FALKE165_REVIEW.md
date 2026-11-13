# 팔케 +165 실제 미연결 6종 후보

상태: 미검증 후보·연결 준비 완료. Claude가 재생/시각검증 담당. 라이브/DB/코어 변경 없음.

unit276 diagnostic_preview/mechanical_cutin_168.state +165 (166회 run) 실제 cached OBJ + rendered OAM 본체 palette0을 계약했다.16OAM 중 미연결7OAM/6고유 RGB, 동일1861179502 두 OAM의 raw bytes/실제 사용 palette 동일하여 한 그림을 공유. 나머지 기존9OAM 의존 보존(whole_pose_dependencies.json). 최신 exact/indexed 연결 모두없음(source_identity_and_connection.json).

installation_map.json 설치 입력. candidate_atlas.png768×384/native_atlas.png192×96, 정확4배. 계약 core_path/SHA 보존. rom_indices_identity.json:6종 모두 image14225/14249 실제 ROM bytes와 완전 일치. 참조 원본RGB/알파/index SHA는 mechanical_contract_checks.json, 후보 전부 alpha_max>=16은 candidate_presence.json. 품질 판정이 아닌 기계적 계약 확인이다.

후보SHA `2d0fad63d6f37e268af2f2b709282cad1f40ac61c8ba9913e38aa24a9ec829ef`. parts_generated.png는 imagegen exec-b65210a6 생성원본 보존. 각 원본 fragment와 whole_native_bbox_context.png의 실제 기체 문맥을 참조해 새로 그렸다. 원본 RGB/알파를 후보에 복사하지 않았고 생성지원 bbox 정렬만 수행했다.

이 자세는 기체 일부가 화면 위(y<0)에 있다. 원본과 후보는 각 파츠의 전체사각형을 보존했다. 원본이 화면에 잘렸다고 alpha를 잘라내지 않았다. 기존9OAM을 원본으로 조합한 unit276_production_assembly.png는 제작문맥 자료이며 최종 HD 재생 증거가 아니다.

셀2/3 작은 삼각 연결편을 생성기가 독립 장갑판처럼 그렸을 수 있고, 셀0/4의 가려진 연결 지원영역이 새 선으로 막혔는지 확인 필요. 셀5의 작은 주황/붉은 점과 회청색/흰색 실색영역은 Claude판정 대기.

Claude 재생 명령:
```powershell
python scripts/verify/verify_runtime_path.py --state test_current/combat/named_attacks/unit_276/diagnostic_preview/mechanical_cutin_168.state --frames 230 --save-frames 150 165 180 210 --track-atlas falke165_missing --name falke165
```

전체 기체 HD 완성 주장 없음. 다음 +285는 별도 다른 자세이며 이후 후보 제작 예정.
