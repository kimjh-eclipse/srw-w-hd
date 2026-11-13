# M9 저격 자세6종·아바레스트 산탄포 연결편1종 후보

상태: 미검증 후보·연결 준비 완료. Claude가 실제재생/시각검증담당. 라이브/DB/코어변경없음.

## 실제 원본
- source_mechanical_261_1065/source_pose.state: M9 unit261 무장1065 대물저격총, 원본진단메뉴 frame320에저장, 로드후1회run 계약. 본체13OAM 중새6종6OAM.
- source_mechanical_263_1086/source_pose.state: 아바레스트 unit263 무장1086 산탄포복서, 메뉴frame410에저장, 로드후1회run 계약. 본체14OAM 중새1종1OAM.

두상태모두기존 duo_weapons 진단fixture의아군만RAM으로설정, 기력/비용/지형완화한격리원본추출이며 ROM/사용자세이브변경없음. 실제캠페인합법성검증은아니다. capture_meta는각source폴더보존.

계약은 실제 cached OBJ+rendered OAM. 전체27OAM중새7종/7OAM이고기존20OAM 의존관계는whole_pose_dependencies.json보존. 새7종최신exact/indexed연결모두없음(source_identity_and_connection.json). raw index bytes는 모두ROM13662에동일영역확인(rom_indices_identity.json), 첫일치증거이며소유리소스유일성전수조사는아니다. 실제usedpalette와ROM후보일치여부도source_identity_and_connection.json참조. core_path/SHA256·실제RGB·원본indexSHA와좌표는각source_contract에확정.

## 설치
installation_map.json + candidate_atlas.png768×864/native_atlas.png192×216로정확4배. 기계적원본RGB/alpha/indexSHA·크기정합은mechanical_contract_checks.json. 후보빈/alpha_max<16=0은candidate_presence.json. 품질QA결과아님. SHA `01615ebe3139aa6bd43ae418462a36611a59b44b10a50b8ff8ea3f8aee3b3897`.

parts_generated.png는imagegen exec-bc21e95b생성원본. 원본셀및기체bbox문맥을참조해7종각각새로제작. 다른기체재색칠/원본RGB알파스탬프없고 생성알파bbox정렬만사용. prepare_candidate.py재현.

## 주요미검증위험
셀4는실제M9머리전체지원이다. 둥근회색헬멧/옆의노랑작은패널/아래왼쪽초록좁은부분이원본과같은지, 기계마스크를임의얼굴로만든것은아닌지Claude확인필요. 셀2노랑2직사각형을초록센서로바꾸지않았는지 확인. 셀3구멍/셀6연결끝의내부절단선/cap도확인. unit*_production_assembly.png는기존파트를원본으로둔제작자료로실제HD재생증거가아니다.

Claude재생:
```powershell
python scripts/verify/verify_runtime_path.py --state test_current/parts/borrowed_shape_rework/source_mechanical_261_1065/source_pose.state --frames 120 --save-frames 0 15 30 60 --track-atlas m9_sniper_boxer_missing --name m9_sniper
python scripts/verify/verify_runtime_path.py --state test_current/parts/borrowed_shape_rework/source_mechanical_263_1086/source_pose.state --frames 120 --save-frames 0 15 30 60 --track-atlas m9_sniper_boxer_missing --name arbalest_boxer
```

현재확보한자세의누락만그렸으며전무장완성주장없음.
