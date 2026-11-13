# 진 무반동포 암부 4종 재제작 후보 인계

상태: `CACHED_OBJ_ARTWORK_CANDIDATE_UNVERIFIED`. 이전 도트 확대 초안은 거절본으로 보존했고 새 생성 그림으로 4종을 다시 준비했다. 라이브 연결·굽기·실제 HD 재생 검증은 하지 않았다.

- 대상: unit60 / weapon276의 원본 메뉴 220 및 400 시점. 각 `source_contract.state`에서 +0으로 재현한다.
- 설치 입력: `installation_map.json`, `contract.json`, `candidate_atlas.png`, `native_atlas.png`.
- 후보 SHA256: `472b157e8bbaecaed88bc6317a903db95b395b857778228a5e48eaa3efbd4bb3`.
- 4종 모두 실제 cached OBJ의 정확 RGB 및 indexed 연결이 없었던 대상이다. actual RGB 해시: 2676906374, 827191567, 2660667410, 2054346999.
- 원본 인덱스 바이트: IMG8726 3종, IMG8695 1종과 일치. `rom_indices_identity.json`에 좌표·바이트 SHA 보존. 기체 소유를 첫 이미지 검색 결과만으로 단정하지 않는다.
- 페이드 아님: `full_palette_phase_proof.json`의 전체 16색이 ROM PLT1414 bank0와 4종 모두 일치한다. 원래 기본 팔레트로 어둡게 그려진 뒷면·가림 영역이다. 사용색만 비교한 여러 후보와 전체 팔레트 일치를 구분했다.
- `parts_generated_raw.png`가 새 생성 원본. 생성 자체 alpha <64만 RGBA0으로 정리했고 그 이상 RGBA는 불변이다. 원본 알파/색 복사나 마스크 덮어쓰기 없음. 검정 불투명 영역도 생성 그림에 남아 있다.
- 두 상태의 의존관계를 섞어 한 장면처럼 합성하지 않았다. `native_pose_production_0/1.png`와 `candidate_pose_production_0/1.png`는 상태별 제작 조립 참고다. 실제 HD 재생 결과가 아니다.
- 의존: 각 상태 `whole_pose_dependencies.json`의 기존 몸체·무장 그림은 변경하지 않는다. cell0은 두 상태에서 같은 실제 RGB로 공유한다.

Claude 확인 사항: 암부의 굴곡·몸체 연결면이 원래 그림보다 둥글어졌는지, 잘린 내부 경계에 검정 테두리가 새로 생겼는지, 셀2 곡선 간격과 셀3 검은 불투명 영역, 두 자세의 기존 파츠와 색/이음새를 확인해야 한다. 작은 팔레트 색 수 때문에 추정 역할명을 생성에 넣지 않았으며 전체 기술 완료로 세지 않는다.
