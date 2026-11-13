# valarm_mechanical_native1640 실제원본 기계 새그림 인계

11계약/고유RGB11. packed/ 원본/후보/계약은 원source기하/fixture/OAM/원atlas_box를보존한무손실배치. 각RGBAcrop전후SHA256동일. 원source폴더보존. actualRGB/indexed0,NullCacheprepare모두nonempty. 원본 포함 1쌍: +520 작은 조각은 +540 큰 조각의 좌상단, 같은 생성 영역 공유,반복OAM/동일frame자료는same_source_aliases.json(15건).

첫 생성 한 벌의 자체 알파를 그대로 사용했습니다. 원본RGB/alpha찍기·다른기체리컬러없음. 원본상true기계context만제작,이묶음으로전체기체/무장완료라하지않음. 공식QA·실제HD재생은Claude대기. 단면외곽선·원본실루엣/센서색·작은조각과잉완성·whole그림해부학/기존부품연결이중점위험. 라이브/DB/core변경없음.


실행 주체는 unit420이나 부품 소유자를 ROM 리소스로 독립 확정하지 않았으므로 모든 source_owner=None / source_owner_confirmed=false입니다. 실제 원본 조각을 그린 것이며 소유자를 유추해 몸체를 완성하지 않았습니다. 11계약은 포함 영역 1쌍을 공유하므로 독립 생성 영역은 10개입니다. 생산 입력용 작은 조각의 밝기·관절 폭·절단면은 Claude 실제 재생 확인 대기입니다.


명칭 근거 정정: 카탈로그 weapon1640은 F호크 스트라이크로 표시하지만, 실제 +430 대사는 아플리칸트의 「플라즈마 노바 드라이버… 풀 차지!」입니다. 따라서 카탈로그 기술명을 실제 장면 기술명으로 확정하지 않습니다. 이 묶음의 확정 식별자는 fixture unit420/w1640와 계약의 원본 바이트/실제 팔레트입니다. 부품 IMG 소유자는 None / source_owner_confirmed=false입니다.


## 카탈로그와 실제 장면 불일치 근거

- 요청/카탈로그: unit420 발아룸 / weapon1640 F호크 스트라이크.
- 실제 원본 캡처: `test_current/parts/actual_mechanical_pose_420_430/whole_native_context.png`
- 캡처 상태: `test_current/parts/native_weapon_source_420_1640/unit420_weapon1640_source.state`, 상대 프레임 +430.
- 실제 화자: 아플리칸트. 실제 대사: 「플라즈마 노바 드라이버… 풀 차지!」
- 원본 +600도 동일 기체/화자를 유지하며 주황색 발·검정/파랑 몸체의 기계입니다. 그림 조각은 해당 캐시의 실제 indices/팔레트 그대로이며 명칭 불일치로 RGB 계약을 바꾸지 않았습니다.

전투 원본 채집 도구 `test_current/parts/capture_source_420_1640.py`는 `duo_weapons.state`에서 RAM unit/pilot 레코드를 바꾸고 실제 메뉴 배열(0x1e8408)을 읽어 `1640 in menu`를 확인한 뒤 선택 위치를 옮깁니다. 그러나 메뉴의 실제 화면 무기명이나 재생에 들어간 내부 애니메이션 ID를 독립 대조하지는 않았습니다. 카탈로그 자체 매핑 차이인지, native 메뉴 선택/전투 도구의 unit·weapon/animation 주소 해석 차이인지는 아직 확정하지 않았습니다. 이 도구의 선택과 실제 재생 기술 ID 연결을 Claude/코드 담당이 검토해야 합니다. 본 작업은 fixture420/w1640 관측 기계 조각 11개로만 인계하며 기술 완료로 세지 않습니다.
