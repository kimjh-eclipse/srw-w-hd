# M9·아바레스트 커터 자세 실제미연결4종 후보

상태: 미검증 후보·연결 준비 완료. Claude가 실제재생/시각검증 담당. 라이브·DB·코어변경없음.

source_mechanical_262_1075/source_pose.state(M9/커터1075,메뉴frame240)와 source_mechanical_263_1087/source_pose.state(아바레스트/커터1087,메뉴frame270)의로드후1회run 실제캐시OBJ+renderedOAM 계약이다. 격리RAM진단메뉴원본이며 비용/기력/지형완화·ROM/사용자저장불변·캠페인합법성미검증은각capture_meta.json참조.

본체31OAM 중새4종4OAM, 기존27OAM 의존whole_pose_dependencies.json. 앞서M9/Falke후보와동일한actualRGB를선정에서제외했다. 새4종최신exact/indexed없음(source_identity_and_connection.json). ROM13696/13785에실제원본bytes완전일치(rom_indices_identity.json), 소유리소스유일성은별도미확정. 실제사용palette와ROM후보일치여부는source_identity_and_connection.json. core_path/SHA256·원본RGB·indexSHA·OAM좌표는contract.json.

설치installation_map.json + candidate_atlas.png512×576/native_atlas.png128×144로정확4배. 원본RGB/alpha/indexSHA/크기는mechanical_contract_checks.json, 빈/alpha_max16미만0은candidate_presence.json. QA판정아님. SHA `412d7ef4b503b82903ed356841655b84119e443466760307cf49e4b2fbaa45af`.

parts_generated.png는imagegen exec-b8a6ae14생성원본. 원본셀과두기체bbox문맥참조새그림이며 원본RGB/알파찍기나색변형재사용없음. 생성알파bbox정렬만수행. cell0은기계의부분패널로완전한머리로자동완성하지말도록했다. 원본의작은노랑위치·두회색띠·절단면/지원영역은Claude미검증. cell1접합안쪽검은면/cell2넓은암부/cell3분리끝이원본을따르는지도판정필요. unit*_production_assembly.png는기존원본과의제작조립자료이며최종HD재생증거아님.

Claude재생:
```powershell
python scripts/verify/verify_runtime_path.py --state test_current/parts/borrowed_shape_rework/source_mechanical_262_1075/source_pose.state --frames 120 --save-frames 0 15 30 60 --track-atlas fmp_cutter_missing --name m9_cutter
python scripts/verify/verify_runtime_path.py --state test_current/parts/borrowed_shape_rework/source_mechanical_263_1087/source_pose.state --frames 120 --save-frames 0 15 30 60 --track-atlas fmp_cutter_missing --name arbalest_cutter
```

265/1097에서먼저나온11미연결은흰방사형이펙트이므로이기계4종에넣지않았다. 팔케1125의수평흰3줄1종도기계역할불확실하여제외. 전무장완성주장없음.
