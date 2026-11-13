# Codex → Claude 핸드오프 4

현재 교환 파일입니다. 이전 제작 기록은 HANDOFF_FROM_CODEX_3.md에 보존합니다. 현재 상태는 이 파일을 우선합니다.

## 현재 상태

- **코어 소스 해제**. Codex는 코어와 공유 그리기 코드를 수정하지 않습니다.
- Claude의 95ba46f0 / d98c4226 반영 완료. 기본 DLL SHA256 a6d80b29119f7c18447725acc4e0e5c8fb88cdda07d8cef6ccb106e936b64fe0. cachedOBJ API도 포함합니다. EXE 번들은 아직 이전 DLL이므로 재묶기 필요.
- Codex는 그림 제작·정확 계약 연결·대상 굽기 담당, 독립 색/키/실제 재생 검증은 Claude 담당. 기계적 입력 검사만 Codex가 수행합니다.
- 아래 첫 69개 계약(중복2개 공유 = 고유67종) 설치·굽기 완료. 샌드록16종도 추가 설치·굽기 완료. 이번 고유83종, 굽기 오류0. 넓은 전수 굽기는 아닙니다. 라이브러리·저장소 쓰기는 root 한 명만 수행합니다.
- next_shape_art: 샌드록 실제 팔레트 자세 재제작. next_key_art: 데스사이즈 다음 무장 자세. effect_live_palette: 20498 다음 효과 그룹. 모두 라이브 파일과 코어는 수정하지 않습니다.
- 컴퓨터 종료 금지, 사용자 테스트 창 유지, ROM/세이브/사용자 설정/로그 푸시 제외.

## 이번 제작 묶음 (연결·굽기 완료, Claude 독립 검증 대기)

|묶음|수|제작 위치|Claude 확인 대상|
|---|---:|---|---|
|겟타 무장 shaft|2|test_current/parts/getter_remaining_effects/next_effect_source/pole_forms|getter_cutin +56/57/59/90/110/126/207/234. 절단 이음매·잔상·도끼 축. effect 태그 없음|
|21948 효과 새 계약|17|test_current/parts/effect_21948|unit413 weapon1610 frame360+112~128 및 frame600+31/63~94. 기존 exact14개 보존; 새17개만 연결. 흰 중심/민트 가장자리 접합|
|코다르 분신 cached14|14|test_current/parts/borrowed_shape_rework/codarl_clones90_cached_pose|unit280 mechanical_cutin_168+90. 26 OAM/14 unique. 이전17 입력의 phantom3개 폐기·미설치. 칼과 양쪽 분신 연결|
|데스사이즈 일반7086|20|test_current/parts/deathscythe_normal_pose|duo_map_attack.state+120. v1 폐기, continuous 후보 사용. 뿔 금색/눈 초록/회색 장갑·날개/팔/몸통 이음매|
|20498 회색 곡선|2|test_current/parts/effect_20498_gray|unit413 weapon1610 frame600+31 OAM3/4. 연속 상하 두 조각. 전체20498 완성이라는 의미 아님|
|데스사이즈 접힌날개 자세|14|test_current/parts/deathscythe_next_pose|duo_cutin.state+180. 15 OAM 중 기존7086 1개 재사용,14개 연결. 얼굴을 가리는 날개는 원본 문맥. 작은 연결부·색·키 잔여 확인|

각 폴더 install_report.json에 실제 binding 및 IoU 경고를 기록합니다. --defer-shape-review는 통과 판정이 아니라 독립 검증 대기 표시입니다. 굽기 후 아래 결과를 갱신합니다.

## 이번 반영 결과

- 첫67종: bake_parts 오류0, 6.0초. 샌드록16종: 오류0, 5.4초. 이는 제작 굽기 시간이며 게임 FPS 측정이 아닙니다.
- 21948의 회색2종은20498과 실제RGB/크기/인덱스가 같은 계약이라 binding91986/91987을 공유합니다. 최종그림은 연속곡선20498 atlas로 연결됐습니다. 서로 다른 기체 팔레트를 재색칠해 대체한 것이 아닙니다.
- 샌드록16:90624/23931/90626/90638/90622/90611/23523/90640/90602/90608/90605/90629/23914/90612/90596/23925. 기존RGB 정확일치 항목의 그림교체입니다.
- 정확한 전체번호·atlas해시는 `docs/PRODUCTION_ART_BATCH_CURRENT.json`. 각 `graphics/rework_*/pose_contract.json`, `installation_report.json`, `ART_REVIEW_NOTES.md`도 저장해 Git에서 원본계약과 제작검토점을 추적할 수 있게 했습니다.
- `shape_review_required` 경고: 겟타pole slot8,21948 slot8/3/4,20498 slot3/4. 나머지 입력겹침기준은.70 이상이지만 시각적완료 판정은 아닙니다. 키색·색번호·실제재생 수치는 Claude 미측정입니다.
- native_materials/material_slots 캐시는 이번 라이브러리에 맞춰 재생성합니다. EXE 재묶기는 Claude 그림/재생검증 완료 뒤로 남겨둡니다. 실행 중인 사용자창은 건드리지 않았습니다.
