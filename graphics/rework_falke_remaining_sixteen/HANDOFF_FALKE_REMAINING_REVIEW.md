# 팔케 여러 공격 단계의 실제 미연결 16종 후보

상태: 미검증 후보·연결 준비 완료. Claude가 시각 및 재생검증 담당. 라이브/DB/코어 변경 없음.

## 원본 범위
unit276 diagnostic_preview/mechanical_cutin_168.state의 관측 offset [0, 60, 180, 255, 270, 300, 345]. 해당시점 cached OBJ + rendered OAM의 본체 palette0만 포함. 실제 지원영역과 팔레트는 각 source_contract에 보존하며 다른 시점 OAM/VRAM 혼용 없음. 추출기 capture_rendered_art.py는 offset+1회 run. 각 계약에 core_path/SHA256 보존.

원본 전체104OAM을 whole_pose_dependencies.json에 기록. 새16고유 RGB는 26회 실제 관측OAM에 나타났다. 앞선 falke165/285의15회OAM은 raw bytes·실제사용 palette·크기동일 검산하고 prior_candidate_dependencies.json에 의존 기록. 그 외 기존 연결도 원본 계약 그대로 보존. 같은기체 실제같은파츠만 공유하며 다른기체 그림 재색칠은 하지 않았다.

새16종 최신 exact/indexed 연결없음(source_identity_and_connection.json). ROM index bytes16종 전부 image14225/14249/14250 등 실제원본과 완전일치(rom_indices_identity.json). 사용 palette 색은 모든16종에 ROM 일치후보도 확인했다. 원본RGB/알파/index SHA/크기 기계정합은 mechanical_contract_checks.json, 후보빈/alpha_max<16인것0은 candidate_presence.json. 이는 색영역/형태 QA결과가 아니다.

## 설치 입력
installation_map.json + candidate_atlas.png1024×1152 / native_atlas.png256×288, 정확4배.16셀4열4행. cell5 등64높이 원본을 보존하기 위해 native셀64×72로 저장, 셀사이 절단으로 긴원본을 잘라내지 않았다. 후보SHA `c119dc9297ac0d40a6fc323f13f0337199412b8e9c11e83976d46152ef701d59`.

원본참조 native_atlas_reference_gray.png / native_cells_context.png / whole_native_bbox_context.png / unit276_frame각offset_native_context.png.

## 제작 및 알려진 위험
parts_generated.png는 imagegen exec-57d27b86 생성원본. 원본셀과 각기체 bbox문맥을 보고 새로 그렸다. 원본RGB/알파 복사없음. 생성지원bbox 정렬/분리만 수행했다. prepare_candidate.py 및 assemble_falke_remaining.py로 재현.

cell5는 긴 부분칼날이며 완전한검이 아니다. cell7은10픽셀에불과한 작은조각이다. cell13은 얇은 칼날끝,14는부분가드/칼날,15는전체곡선칼날이다. 생성기의 새 검은절단면 선, 지원영역/금속빛 과장·날끝형상·작은빨강/노랑점위치가 맞는지는 Claude판정 대기다.

frame*_production_assembly_extended.png는 기존파츠를 원본으로 두고 새그림을조합한 제작문맥이다. 음수 y파츠 보존을 위해 출력에만 y+64를 더했다. 계약의화면좌표는변경하지 않았다. 최종HD재생 증거아님.

## Claude 재생
```powershell
python scripts/verify/verify_runtime_path.py --state test_current/combat/named_attacks/unit_276/diagnostic_preview/mechanical_cutin_168.state --frames 375 --save-frames 0 60 180 255 270 300 345 --track-atlas falke_remaining_missing --name falke_remaining
```
전체기체/전체공격HD완성 주장은 하지 않는다. source선정은 15프레임 간격이므로 사이 짧은자세의 누락 가능성은 남는다.
