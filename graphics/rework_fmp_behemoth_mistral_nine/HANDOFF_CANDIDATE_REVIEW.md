# 베헤모스·미스트랄 후속9종 분리지지영역교정

미검증 후보·연결 준비. Claude 공식 QA/실재생 담당. 라이브/코어/DB 변경 없음.

실제 cachedOBJ + renderedOAM, 격리 진단메뉴 source_pose.state 로드 후1회run 계약. 비용/기력/지형완화·ROM/사용자저장불변·캠페인합법성미검증은 각capture_meta.json.
- unit272 무장1117, 메뉴frame130, `C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_272_1117\source_pose.state`
- unit277 무장1130, 메뉴frame130, `C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_277_1130\source_pose.state`
- unit277 무장1131, 메뉴frame150, `C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_277_1131\source_pose.state`

전체52 OAM 중새9종10 OAM, 나머지42 기존의존 whole_pose_dependencies.json. 최신exact/indexed 연결은 source_identity_and_connection.json. ROM첫bytes일치는 rom_indices_identity.json. 실제사용palette와ROM후보(없는변형포함)도기록. 소유IMG유일성미확정.

installation_map.json + candidate_atlas.png / native_atlas.png 정확4배. 원본indexSHA·크기·색·alpha정합 mechanical_contract_checks.json. 빈후보/alpha_max16미만0 candidate_presence.json. SHA 8a647fa6c3786f7734fb61d7fe7217f79f464bd56707d09359071dde21554241.

parts_generated.png: 기존7종exec-9104b20c·slot0/6새imagegen exec-46b984ba. 원본셀/whole기계문맥참조 새그림. 원본RGB/alpha찍기·다른기체재색칠없음. 생성자체bbox정렬만. 품질통과주장없음.

알려진 제작위험: 이전slot0은큰돔/아래작은붉은면사이빈틈을합쳐보류. 두슬롯만생성도구로새제작하여큰투명빈틈/레일사이의투명틈을보존한후보로교정. 원본alpha찍기없음. native0은4연결828texel한형상이지만두붉은면사이넓은투명홈존재. 새그림은두섬분리로제작되어정확지원영역/너무밝은색/녹색외곽스필은Claude검토필요. native6은4연결성분98/54/70/23texel이며세로여러줄이이루는4지지영역,생성은세로틈을모두비웠으나정확배치는Claude판정. 이전7종변경없음.

pose*_production_assembly.png는기존원본과제작조립자료이며실제HD재생증거아님.

Claude:
```powershell
python scripts/verify/verify_runtime_path.py --state "C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_272_1117\source_pose.state" --frames 120 --save-frames 0 15 30 60 --track-atlas fmp_behemoth_mistral_followup_missing --name fmp_behemoth_mistral_followup_missing_0
python scripts/verify/verify_runtime_path.py --state "C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_277_1130\source_pose.state" --frames 120 --save-frames 0 15 30 60 --track-atlas fmp_behemoth_mistral_followup_missing --name fmp_behemoth_mistral_followup_missing_1
python scripts/verify/verify_runtime_path.py --state "C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_277_1131\source_pose.state" --frames 120 --save-frames 0 15 30 60 --track-atlas fmp_behemoth_mistral_followup_missing --name fmp_behemoth_mistral_followup_missing_2
```

전무장완료주장없음.