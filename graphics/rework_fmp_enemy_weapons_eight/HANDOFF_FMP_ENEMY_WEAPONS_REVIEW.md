# FMP 적·훈련기 무장 실제 미연결 8종 후보

미검증 후보·연결 준비 완료. Claude가 공식 QA와 실제 재생 판정 담당. 라이브/DB/코어 변경 없음.

다음은 격리 진단메뉴로 저장한 원본 source_pose.state 로드 후 1회 run cachedOBJ + rendered OAM 계약이다. 비용/기력/지형 완화, ROM·사용자 저장 불변, 캠페인 합법성 미검증은 각 capture_meta.json.
- unit 269 / 무장 1110 / 메뉴 frame 160 / `C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_269_1110\source_pose.state`
- unit 269 / 무장 1111 / 메뉴 frame 130 / `C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_269_1111\source_pose.state`
- unit 270 / 무장 1112 / 메뉴 frame 190 / `C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_270_1112\source_pose.state`
- unit 271 / 무장 1114 / 메뉴 frame 190 / `C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_271_1114\source_pose.state`
- unit 275 / 무장 1123 / 메뉴 frame 160 / `C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_275_1123\source_pose.state`
- unit 275 / 무장 1124 / 메뉴 frame 160 / `C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_275_1124\source_pose.state`

기체 팔레트0 전체70 OAM(6관측시점)에 신규8 고유그림·10 OAM, 나머지60기존 의존. 전체좌표/가림/중복은 whole_pose_dependencies.json. 최신 exact/indexed0은 source_identity_and_connection.json. ROM14005/14038/14083/14210의 첫bytes 일치·실제palette 후보 포함. 리소스 단독 소유 유일성은 미확정.

installation_map.json + candidate_atlas.png1024×576/native_atlas.png256×144 정확4배. 원본indexSHA/크기/RGB·alpha계약 mechanical_contract_checks.json. 빈 후보/alpha_max16미만0 candidate_presence.json. SHA fc740044f01119c31ab7e7b23fd150253dbc0ccdaf76576fca554c6e791834eb.

parts_generated.png는 imagegen exec-d591b991 새그림. 실제 8셀과 6관측의 기체전체bbox문맥을 참고했다. 원본RGB/alpha찍기·다른 기체 재색칠 재사용 없음. 샌드색과 빨강 팔부품은 rawindex가 같아도 actualpalette가 달라 두 그림을 별도로 그렸다. 생성의 얇은 부품 외곽은 다소 굵어졌거나 작은 손가락/볼트/지지면을 늘렸을 위험이 있다. 특히 cell0 가느다란 모래색 부분, cell2의 손 모양·회색돌기 수, cell3/6 좁은단의 열린 접합, cell4 세로파트 아래 연결부는 Claude 판정 필요. QA 통과 주장 없음.

pose*_production_assembly.png는 나머지를 원본으로 둔 제작 조립자료이며 최종HD 재생 증거가 아니다. 원본 좌표/priority·OAM 역순을 적용.

Claude 재생 명령:
```powershell
python scripts/verify/verify_runtime_path.py --state "C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_269_1110\source_pose.state" --frames 120 --save-frames 0 15 30 60 --track-atlas fmp_enemy_weapons_missing --name fmp_enemy_weapons_0
python scripts/verify/verify_runtime_path.py --state "C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_269_1111\source_pose.state" --frames 120 --save-frames 0 15 30 60 --track-atlas fmp_enemy_weapons_missing --name fmp_enemy_weapons_1
python scripts/verify/verify_runtime_path.py --state "C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_270_1112\source_pose.state" --frames 120 --save-frames 0 15 30 60 --track-atlas fmp_enemy_weapons_missing --name fmp_enemy_weapons_2
python scripts/verify/verify_runtime_path.py --state "C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_271_1114\source_pose.state" --frames 120 --save-frames 0 15 30 60 --track-atlas fmp_enemy_weapons_missing --name fmp_enemy_weapons_3
python scripts/verify/verify_runtime_path.py --state "C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_275_1123\source_pose.state" --frames 120 --save-frames 0 15 30 60 --track-atlas fmp_enemy_weapons_missing --name fmp_enemy_weapons_4
python scripts/verify/verify_runtime_path.py --state "C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_275_1124\source_pose.state" --frames 120 --save-frames 0 15 30 60 --track-atlas fmp_enemy_weapons_missing --name fmp_enemy_weapons_5
```

본타·전 FMP 모든 기술 완료 주장은 하지 않음. 이 후보8은 관측된 기계 신규만 포함.
