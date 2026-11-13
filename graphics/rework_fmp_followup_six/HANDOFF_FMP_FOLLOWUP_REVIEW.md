# FMP 셰도우 격투·기본 M9 손 신규6종

미검증 후보·연결 준비. Claude 공식 QA/실재생 담당. 라이브/코어/DB 변경 없음.

실제 cached OBJ + rendered OAM 기반. 격리 진단메뉴 source_pose.state 로드 후1회run 계약. 비용/기력/지형완화·ROM/사용자저장불변·캠페인합법성미검증은 각capture_meta.json.
- unit270 무장1113, 메뉴frame190, `C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_270_1113\source_pose.state`
- unit271 무장1115, 메뉴frame190, `C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_271_1115\source_pose.state`
- unit260 무장1058, 메뉴frame270, `C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_260_1058\source_pose.state`

전체 41 OAM 중 새6종 7 OAM, 나머지34 기존 의존 whole_pose_dependencies.json. 앞선 enemy_weapons8종 actualRGB는 제외. 최신 exact/indexed0 확인 source_identity_and_connection.json. ROM14037/13662 원본bytes일치, 실제사용palette와ROM후보(없는변형포함)도기록. 소유IMG유일성미확정.

installation_map.json + candidate_atlas.png1024×576/native256×144 정확4배. 원본indexSHA·크기·색·alpha정합 mechanical_contract_checks.json. 빈 후보/alpha_max16미만0 candidate_presence.json. SHA f67c173fe7e95dddf38297c653fe4a3b6eadc200974f6319542a382737c08ae0.

imagegen exec-0172e606 새그림 parts_generated.png. 원본셀/whole기계문맥으로직접새제작. 원본RGB/alpha복사나 다른기체재색칠재사용 없음. 생성자체bbox정렬만. 원본작은파트에 비해cell0이원통형으로과해석됐을 위험, cell1/3의 절단면caps와cell2/4 긴단의형상, cell5두분리섬·손가락수가특히Claude검토대상. 품질통과 주장 없음.

pose*_production_assembly.png는기존원본조각과의제작조립자료이며HD게임증거아님.

Claude:
```powershell
python scripts/verify/verify_runtime_path.py --state "C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_270_1113\source_pose.state" --frames 120 --save-frames 0 15 30 60 --track-atlas fmp_followup_source_missing --name fmp_followup_0
python scripts/verify/verify_runtime_path.py --state "C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_271_1115\source_pose.state" --frames 120 --save-frames 0 15 30 60 --track-atlas fmp_followup_source_missing --name fmp_followup_1
python scripts/verify/verify_runtime_path.py --state "C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_260_1058\source_pose.state" --frames 120 --save-frames 0 15 30 60 --track-atlas fmp_followup_source_missing --name fmp_followup_2
```

unit260 source에서 미연결로 관측된16개 중이묶음기계는팔레트0한종만포함. 다른효과를기계신규로세지않았음. 전무장완료주장없음.