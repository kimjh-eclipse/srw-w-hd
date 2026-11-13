# IMG19808 제작 후보 인계

- install_contract.json 12종: 실제 cachedOBJ 관측 10, 같은 IMG/PLT 실제 팔레트 16값 확정 미관측 2. 후보 candidate_atlas.png/native_atlas.png/generated.png/provenance.json.
- 실제 원본 indices/hash/팔레트 및 source/atlas_box 그대로 계약. 모든 활성 RGB/indexed 미연결 확인. 관측은 fixture/frame/observations, 미관측은 None으로 구분.
- 원본의 정확4배 1024×128. 한 벌 새 그림의 생성된 위아래 여백만 전체 bbox로 기하정렬. source RGB/alpha 복사·마스크 없음. 개별 파츠별 임의변형 없음.
- crop maxA≥16 전부: True. 공식 audit·재생·독립 시각 QA 하지 않음.
- 알려진 위험: 원본보다 윤곽이 두껍거나 굽음·전기광선이 부풀었을 수 있음. 전체 높이 정렬만 했으므로 내부 파츠 위치/원본 얇은 선/색 배치와 절단면은 Claude 확인 대기.
- root 설치굽기 담당, 라이브/DB/코어 변경 없음.
