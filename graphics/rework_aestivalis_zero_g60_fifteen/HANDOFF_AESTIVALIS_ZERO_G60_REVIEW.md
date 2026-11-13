# 0G 아스테바리스 손·팔 실제미연결15종 후보

상태: 미검증 후보·연결 준비 완료. Claude 시각/재생검증 대기. 라이브·DB·코어변경없음.

unit139~144/mechanical_cutin_168.state +60(61회run) 실제cachedOBJ+renderedOAM 본체palette0 기준. 본체 전체78OAM 중 새15고유RGB가 21회 OAM에나타남. 남은파츠는기존binding 의존 whole_pose_dependencies.json보존. RGB해시·원본indexbytes·실제사용palette·크기같은조각만공유했다. 색이원래다른팔을재색칠재사용하지않고각색별새로그렸다.

새15종최신exact/indexed연결없음(source_identity_and_connection.json). 두주요손/팔형태는ROM10751(24,0)/(0,16)의실제bytes완전일치. 작은10픽셀연결편은10695/10697에같은bytes가있지만실제소유IMG유일성미확정이므로resource=None/source_candidate_matches에첫일치예시만저장(비전수목록). 실제캐시 exact계약은확정. 실제사용palette와ROM후보일치여부는source_identity_and_connection.json. core_path/SHA·실제팔레트·indexSHA·OAM좌표는contract.json에보존.

설치installation_map.json + candidate_atlas.png1024×1152/native_atlas.png256×288로정확4배. 64×72셀4열4행중마지막15번은빈칸. 원본RGB/alpha/indexSHA·크기기계확인은mechanical_contract_checks.json, 후보빈/nearalpha max16미만0은candidate_presence.json. 품질QA결과아님. 후보SHA `bc1048e18e1c9c8f0802cb3b7ab34607748e4b9718e313f67ba7df9fb920e287`.

parts_generated.png는imagegen exec-bea0eee7생성원본. 원본셀과기체bbox문맥을참조해새로제작. 원본RGB/알파스탬프없고 생성알파bbox정렬만수행. prepare_candidate.py재현.

주의: cell0/3/8/11/14는매우작은지원조각이므로임의두께·cap·색변화를Claude가확인해야함. 손/팔셀은회색세로마디개수/배치·안쪽빈영역/절단면검은선·둥근도색관절의과한광택이없는지판정대기다. 색별둥근관절의밝은부분이원본같은색영역을유지하는지또한검증필요. unit*_production_assembly.png는기존파트원본과새그림을조합한제작문맥으로실제HD재생증거아님.

Claude재생예시:
```powershell
python scripts/verify/verify_runtime_path.py --state test_current/combat/named_attacks/unit_139/mechanical_cutin_168.state --frames 180 --save-frames 45 60 90 120 --track-atlas aestivalis_zero_g60_missing --name zero_g139
```
140~144도동일시점기준각각재생. 139기체는큰손/팔새그림이이미연결되어작은연결편만이번에추가됐다. 모든기체/전무장완성주장없음.
