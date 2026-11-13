# 실제 unit110 / weapon467 메뉴350 기계 6종 후보

상태 `CACHED_OBJ_ARTWORK_CANDIDATE_UNVERIFIED`. 제작 후보와 actual 원본 계약만 준비했다. 라이브·공유 코드·코어·DB 변경 없음. 공식 검사·실제 HD 재생은 Claude 대기.

- 설치 입력: installation_map.json, candidate_atlas.png, native_atlas.png, contract.json.
- 후보 SHA256: `59c31145bc7761d17e37372769874595edd81846feaf0d089025f70a0973afea`.
- 실제 fixture: `source_mechanical_fixed_110_467_350/source_pose.state` +0. 실제 메뉴350 cached OBJ/OAM/팔레트/코어SHA 보존.
- 원래 미연결 셀1/2/5/9/10의5종은 최종0..4이다. 추가 최종셀5는 원래0의 indexed proxy25333으로, 셀0과 실제 source 8×16 일부를 공유하여 같은 생성 그림으로 함께 교체한다. 신규 누락5 + proxy 공유경계 교체1이며 신규누락6으로 세지 않는다.
- 대상4종 IMG9750, 2종 IMG9749의 원본 인덱스 바이트 일치. 전체16색 PLT1648/20312 bank0 동일. 단일소유 팔레트는 단정하지 않는다.
- 셀5 source(128,0)32×32와 셀0 source(152,16)32×16의 공유8×16 원본 인덱스와 전체16색을 검산했다(source_partial_overlap_proof.json). 실제 지원영역은 두 분리된 섬이며 하나로 잇지 않았다. 56×32 원본 master에서 두 생성 조각의 상대 위치와 빈틈을 보존해 원래 사각형으로 분할했다. same_generated_master 및 분할재조립 RGBA 완전일치/사각지원밖누락0은 continuous_generated_split_proof.json에 기록했다.
- 다른 사각형은 source가 닿았다는 이유만으로 하나의 연결 물체로 그리지 않았다. actual 반전/좌표/OAM priority/기존 의존은 whole_pose_dependencies에 보존한다.
- 생성원본 parts_generated_raw.png 보존, 생성 자체 alpha<64만 정리, 고알파RGBA 불변. native RGB/alpha 복사·스탬프 없음.
- candidate_pose_production.png는 제작 참고이고 실제 HD 게임 검사 결과가 아니다.

Claude 위험: 금색 기계 조각의 모델 손가락 해석·작은 관절/금색면 개수, 셀5/0 분리섬의 상대위치와 source공유 영역, 장갑판의 빨강띠/아래 절단면, 어두운 연결줄 사이의 빈틈, 새 그림과 기존 검정/금색 몸체의 경계/명암을 확인해야 한다. 일부 선과 금색 면이 실제 원본보다 둥글거나 선명해졌을 수 있다. 전체 기체/무장 완료로 세지 않는다.
