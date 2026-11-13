# 샌드록 무장 확대 자세9종 제작 인계

상태: **미검증 그림 후보 / 연결 준비 가능**. root 설치·굽기, Claude 공식QA/독립시각/실제재생 담당. 후보의 공식audit·HD재생 검증은 실행하지 않았다.

## 실제 제작 입력과 기존 그림 차집합

- state `test_current/combat/sandrock_closeup_cutin_full.state`, offset0(Core.run1회 뒤 추출).
- `scripts/assets/capture_rendered_obj_contract.py` + cachedOBJ + core.obj rendered OAM 사용. MMU 프레임 말 OAM/VRAM을 읽지 않았다.
- 실제 기본DLL core_path와 SHA는 각 `rendered_contract_all.json`/`contract.json` 및 `capture_meta.json`에 기록했다. SHA256 `a6d80b29119f7c18447725acc4e0e5c8fb88cdda07d8cef6ccb106e936b64fe0`.
- 실제 관측9 OAM/9 RGB, 일반몸체16종과 actualRGB 교집합0. 그림 재사용 의존도0이며 모두 새로 생성했다.
- 최신 라이브 메타를 다시 읽어 집계: 기존 `wing_closeup` exact8개 품질교체 + 실제 unbound1개(셀6/hash274003082) 신규 연결. 일반몸체16개를9개에 재활용하지 않았다.
- 원본에 좌우 대칭처럼 보이는 파츠도 각각 실제RGB가 다르므로9개를 별도로 유지한다.

## 제한과 원본 문맥

원본 화면은 백색 플래시가 기체를 가린다. cached 파츠9개가 존재한다는 입력 근거이지 이 프레임에 기체가 화면에 보였다는 증거는 아니다. 원본 OBJ 조립 자체에도 떨어진 영역/빈 간격이 있다. 이것을 누락된 몸통이라고 추측해 임의로 그리거나 메우지 않았다. BG나 다른 레이어 몸체를 이9종으로 모두 해소했다고 주장하지 않는다.

일부 파츠 y가 음수여서 화면 밖으로 나간 영역도 있다. atlas에는 원본 사각형 전체를 보존했다. `native_extended_pose.png`/`candidate_extended_pose.png`는 캔버스에 y+128을 더해 화면 밖 파츠까지 보이게 한 제작 문맥 자료일 뿐, 실제 OAM 좌표는 바꾸지 않았다.

## 파일

- `rendered_contract_all.json`, `rendered_arrays.npz`, `capture_meta.json`:공통helper 실제 원본.
- `contract.json`, `contract_unique9.json`:9종 actualhash/index/palette/coords + 기존 binding.
- `reuse_dependencies.json`:일반16/외부그림 재사용0, 최신exact8/new1 표.
- `native_atlas.png`:192×216, `candidate_atlas.png`:768×864(4배). 3×3 셀로 빈 공간을 줄였다.
- `grid_context_gray.png`/`whole_oam_context.png`:원본crop/실제bbox문맥.
- `native_extended_pose.png`와 `candidate_extended_detail.png`:실제 사각형/OAM priority 역순의 제작 조립 자료. 최종시각검증 결과가 아니다.
- `parts_generated.png`:9종 새 생성원본.
- `lower4_small6_generated.png`:4/6 추가 새 생성원본. 원본의 허리 위 두 흰색/노란 직사각형을 포구로 자동완성하지 않도록 수정했고, 작은6조각을 원본 불규칙 색면으로 그리도록 지시했다. 성공 여부는 Claude판정.
- `provenance.json`, `mechanical_final.json`:출처·가공법·기계적개수/크기/hash/원본색일치 확인.

원본의 골드/밝은노랑 뿔과 붉은 패널, 초록 눈/센서, 보라 그림자·밝은 장갑·원래 날 곡률을 참조했다. 원본색·alpha를 그림에 찍거나 다른 그림을 재색칠하지 않았다. 생성alpha 정리와 원본bbox 정렬만 사용했다. 각 파츠 경계의 선·곡선 연결·색 배치는 아직 미검증이다.

## root 설치 입력

`installation_map.json`9 entries. atlas_id `sandrock_weapon_closeup_cached_pose`, image `graphics/rework_sandrock_weapon_closeup_cached_pose/pose_hd.png`, reference `graphics/rework_sandrock_weapon_closeup_cached_pose/pose_native.png`, native_size `[192,216]`.

candidate SHA256 `139fec8af7ea68b899f2039d7dec695e43d284c68e508dc2f52c1de5096548bb`.

기존exact8개를 교체하므로 다른 사용처에도 영향이 있다. fallback/이전그림을 임의삭제하지 않는다. 라이브/DB/공유코드는 수정하지 않았다. 후보각사각형에 alpha가 있고 원본 nativecrop의 alpha/보이는RGB가 실제cached index/palette와 같음을 기계적으로 확인했으며, 후보 색/형태 QA를 통과했다는 말은 아니다.

## Claude 큐

root 설치·굽기 뒤 예시:

```powershell
& 'C:\Program Files\Python311\python.exe' -X utf8 scripts/verify/verify_runtime_path.py --state test_current/combat/sandrock_closeup_cutin_full.state --frames 90 --pure-native --save-frames 0 3 8 15 30 60 --track-atlas sandrock_weapon_closeup_cached_pose --name sandrock_weapon_closeup_cached_claude
```

검토할 위험은 백색/X베기 효과와의 가림·전후 프레임, 부분화면밖 파츠지원, 원본에 있던 빈 간격/다른레이어기체 유무, V-fin색·눈·곡선날·작은6조각 형상, 기존8개 다른사용처, 대사창 침범이다. 원본+후보 조립은 입력 확인 자료이며 실제 정상 판정은 Claude가 맡는다.
