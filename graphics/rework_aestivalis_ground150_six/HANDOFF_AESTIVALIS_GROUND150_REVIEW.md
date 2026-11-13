# 육전 아스테바리스 +150 연결편 6색 후보

상태: 미검증 후보·연결 준비 완료. Claude가 시각/재생을 담당한다. 라이브/DB/코어 변경 없음.

unit151~156 mechanical_cutin_168.state +150(151회 run)의 본체 palette0 각각1종, 6OAM/6고유 RGB를 새로 그렸다. 전체 본체78OAM 의존관계는 whole_pose_dependencies.json에 보존. 불투명0인 OAM은 제작에서 제외. 최신 exact/indexed 연결 모두0(source_identity_and_connection.json). 앞선 +90/+195과 다른 조각이다.

원본 index bytes 6종 모두 같고 ROM image10778 (56,0,32,16)와 완전 일치. 색은 기체별 실제 캐시 팔레트에 근거해 각각 새로 그렸다. ROM 팔레트 후보가 없는 색변형도 있으므로 실제 캐시 palette가 최종 기준이다. 계약에 core_path/SHA256 기록.

설치: installation_map.json + candidate_atlas.png(768×384) + native_atlas.png(192×96). 정확4배. 원본 문맥은 native_atlas_reference_gray.png와 whole_native_bbox_context.png. 원본 SHA/크기/실색 픽셀 동일성은 mechanical_contract_checks.json, 모든 후보 alpha max>=16 확인은 candidate_presence.json. 이 수치는 형태/색영역 QA가 아니다.

후보SHA256 `37c535c11b93d781bbf80677576bfa88cb5bd5ba6201a1aeccd9afeac7b1df4c`. 생성 출처 parts_generated.png / exec-82ee8e92 이미지. 원본 RGB/알파를 후보에 복사하지 않았고 생성 알파 자체의 bbox 정렬만 수행. prepare_candidate.py 재현.

원본은 둥근 도색 장갑+짧은 접합편이다. 새 그림 왼쪽 은색 연결부가 손가락처럼 과하게 해석됐는지, 둥근 장갑이 과하게 입체적인지, 접합면 검은 cap이 생겼는지 Claude 확인 필요. 기존 부분은 원본으로 둔 unit*_production_assembly.png는 제작문맥 자료이며 실제 HD 재생 증거 아님.

Claude 명령 예시:
```powershell
python scripts/verify/verify_runtime_path.py --state test_current/combat/named_attacks/unit_151/mechanical_cutin_168.state --frames 210 --save-frames 135 150 165 180 --track-atlas aestivalis_ground150_missing --name aestivalis_ground150_151
```
152~156도 같은 방식으로 실제 조립/눈금/기체 전부 교체 및 팔레트 색영역 확인 필요.
