# 코다르 3변형 실제기계 신규5종

미검증 후보·연결 준비. Claude 공식 QA/실재생 담당. 라이브/코어/DB 변경 없음.

실제 cachedOBJ + renderedOAM, 격리 진단메뉴 source_pose.state 로드 후1회run 계약. 비용/기력/지형완화·ROM/사용자저장불변·캠페인합법성미검증은 각capture_meta.json.
- unit273 무장1119, 메뉴frame140, `C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_273_1119\source_pose.state`
- unit278 무장1132, 메뉴frame400, `C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_278_1132\source_pose.state`
- unit279 무장1134, 메뉴frame220, `C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_279_1134\source_pose.state`

전체50 OAM 중새5종5 OAM, 나머지45 기존의존 whole_pose_dependencies.json. 최신exact/indexed 연결은 source_identity_and_connection.json. ROM첫bytes일치는 rom_indices_identity.json. 실제사용palette와ROM후보(없는변형포함)도기록. 소유IMG유일성미확정.

installation_map.json + candidate_atlas.png / native_atlas.png 정확4배. 원본indexSHA·크기·색·alpha정합 mechanical_contract_checks.json. 빈후보/alpha_max16미만0 candidate_presence.json. SHA c7dc322d6a637c618ba9c96b48d6cc8fb98b6549fff8949bb0043c7ef79fd8eb.

parts_generated.png: imagegen exec-0fd8709d 새그림. 원본셀/whole기계문맥참조 새그림. 원본RGB/alpha찍기·다른기체재색칠없음. 생성자체bbox정렬만. 품질통과주장없음.

알려진 제작위험: 셀0/4길게기계팔조각 상단분기·사각홈형상/셀1·3사선연결끝/cell2작은황토패널실제색영역/내부절단면기계적연속은Claude가판정해야함. 검정극소슬리버3734296757/2089952647은역할불확실하여제외.

pose*_production_assembly.png는기존원본과제작조립자료이며실제HD재생증거아님.

Claude:
```powershell
python scripts/verify/verify_runtime_path.py --state "C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_273_1119\source_pose.state" --frames 120 --save-frames 0 15 30 60 --track-atlas fmp_codarl_body_missing --name fmp_codarl_body_missing_0
python scripts/verify/verify_runtime_path.py --state "C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_278_1132\source_pose.state" --frames 120 --save-frames 0 15 30 60 --track-atlas fmp_codarl_body_missing --name fmp_codarl_body_missing_1
python scripts/verify/verify_runtime_path.py --state "C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_279_1134\source_pose.state" --frames 120 --save-frames 0 15 30 60 --track-atlas fmp_codarl_body_missing --name fmp_codarl_body_missing_2
```

전무장완료주장없음.