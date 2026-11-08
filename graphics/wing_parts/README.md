# Wing 계열 누락 수정과 확인 범위

## 적용

- IMG → PLT → PAT 순서의 묶음 39개를 추가 조사했다. 원래 추출기의 PLT → IMG → PAT 순서와 함께 읽도록 수정했고, 가변 길이 PAT 좌표·확장 항목도 해석한다.
- 데스사이즈(1164)·샌드록(1180) 기본 파츠의 크기/좌표 변형 1,328개를 등록했다. 기존 공격 파츠 70개는 같은 원본 인덱스를 대조해 연결했다.
- `graphics/img_first`의 8개 그림으로 추가 누락을 보충했다. 공유 연결로 처리하지 못했던 유효 PAT 파츠 389개를 추가했다. 조사한 39개 묶음의 미등록 유효 파츠는 0개다. 그림자·동일 파츠는 기존 공유 연결을 사용한다.
- 샌드록 확대 파츠(7278)는 실제 전투 팔레트로 다시 그려 기존 연결 96개를 교정했다. 정상 HD 그림 전체에 원본 재질 격자를 덧씌우지 않는다. 공격 중 색 변환과 부적합한 색 테두리 보정은 유지한다.
- 실제 BG 타일과 아카이브 전체를 대조해 듀오 외침(22808), 웃음(24987), 카토르 컷인(24993)을 찾아 ID 6·8·7로 연결했다. 부분 눈 컷인 ID 4·5도 별도 원본과 연결한다.
- 컷인의 전후 관계·가림을 유지하면서 외곽 한 픽셀 구간에서 HD 알파 가장자리를 보존한다. 그림은 프로젝트 안에 저장하며 최대 변은 960픽셀이다.

새 그림은 내장 `image_gen.imagegen`으로 제작했다. 프롬프트는 `generation_prompts.json`, 원본 비교 이미지는 `*_reference.png`, 실제 소비 이미지는 `*_registered.png`와 `*_hd.png`다. 보충 그림의 생성 원본 식별자는 `../img_first/generated_sources.json`에 기록했다. 기본 파츠와 부분 눈 컷인은 앞선 작업에서 생성한 그림을 사용한다. AI가 재해석한 작은 형태 차이는 남을 수 있다.

## 실제 게임 재생

1화 아군 합류 이후 실제 게임 상태에서 무장·타깃 선택과 전투를 재생했다.

| 기체 | 무장 | 재생 결과 |
|---|---|---|
| 샌드록 | 발칸 | 시작부터 종료까지 1,167프레임 |
| 샌드록 | 크로스 크래셔 | 2,003프레임, 카토르 HD 컷인 ID 7 |
| 샌드록 | 히트 쇼텔 | 1,934프레임, ID 7 및 확대 기체 파츠 |
| 데스사이즈 | 발칸 | 1,061프레임 |
| 데스사이즈 | 빔 사이즈 | 1,846프레임, 듀오 HD 컷인 ID 8·6 |
| 데스사이즈 | 빔 사이즈 MAP | 1,168프레임, 듀오 HD 컷인 ID 8 |

MAP 병기는 기력 120 조건이 있다. 검증용 상태에만 듀오의 기력 필드(`0x1eb284`)를 111→120으로 바꿨다. ROM·사용자 저장 파일은 바꾸지 않았다. `prepare_duo_map_fixture.py`와 `duo_map_fixture.json`에 이 예외를 명시했다.

최신 데스크톱 게임 창에서도 듀오 외침·웃음과 카토르 컷인의 HD 표시를 직접 확인했다. 기본/확대 기체·전투 이펙트·양쪽 화면은 저장 전투와 CPU/GPU 비교로 검사했다. 12개 장면의 양쪽 화면에서 CPU/GPU 최대 채널 차이는 2 이하였다(허용값 3). OBJ/BG 우선순위·알파 조합 139,264건과 기존 본타군·에이드 색상/알파 검사도 통과했다.

검사 자료:

- `test_current/combat/sandrock_weapon_verification.json`, `duo_weapon_verification.json`, `duo_map_verification.json` 및 해당 `*_replay.png`, `*_cutin_hd.png`
- `test_current/rom_catalog/img_first_audit.json`
- `test_current/combat/wing_installation_verification.json`, `edge_palette_verification.json`, `cutin_composition_audit.json`
- `test_current/performance/gpu_surface_verification.json`

## 제한과 보존

위 6개 무장 재생과 39개 묶음의 연결 검사를 완료했다. 전 캠페인의 모든 연출을 재생하거나 모든 프레임에서 원본 대체가 끝났다는 보장은 아니다. 다른 형식·미관측 변형과 비동기 준비 중 원본 표시가 남을 수 있다. 이번 결과로 새 60fps 보장을 주장하지 않는다.

ROM SHA-256, 승인된 얼굴 그림, 초기 5,263개 연결을 보존했다. ROM·세이브·메모리 상태·개인 설정·오류 로그·실행 중 등록 캐시는 공개 커밋에서 제외한다.

재설치 순서: `install_wing_parts.py`, `install_wing_cutins.py`, `install_wing_full_cutins.py`, `install_wing_closeup.py`, `install_img_first_supplement.py`, `build_native_material_cache.py`, `build_material_slot_cache.py`, `build_tile_library.py`. 타일 DB를 교체할 때는 게임을 종료한다. 전투 재생 검사는 공개하지 않는 로컬 저장 상태가 필요하다.
