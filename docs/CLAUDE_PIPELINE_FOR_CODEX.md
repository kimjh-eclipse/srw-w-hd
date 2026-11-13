# 코덱스에게: Claude가 바꾼 방식과 함께 일하는 법

작성: Claude, 2026-11-12. 이 문서는 지금 코드가 어떻게 동작하는지와, 그림 작업을 어떤 순서로 넘기면 되는지를 설명한다. 경위와 측정 수치는 `docs/CLAUDE_REVIEW_RESULT.md`, 그림 작업 목록은 `docs/IMAGE_REWORK_FOR_CODEX.md`에 있다.

굽기는 끝났다(89,199개, 오류 0). 로딩과 화질 측정 결과는 `CLAUDE_REVIEW_RESULT.md` 7절에 있다. 굽기 도구는 팔레트 변환표(`graphics/palette_luts.npz`)도 함께 만든다. 재생 검사는 원본 표시를 `loading`(준비 안 됨)과 `held`(10% 규칙으로 유지)로 나눠 보고한다. `held_frames`가 있는 장면은 그림을 채워야 줄어든다.

## 1. 역할

| 일 | 담당 |
|---|---|
| 새 HD 그림 제작 (기체 파츠, 컷인, BG, 효과) | 코덱스 |
| 빈 파츠 찾기, 원본 소스 추적 | Claude |
| 그림을 라이브러리에 연결·등록 | 코덱스가 해도 되고 Claude에게 넘겨도 된다 |
| 굽기, 재생 검사, 판정 | Claude (코덱스도 같은 명령으로 확인할 수 있다) |
| 실제 게임 화면 확인 | 사용자 |

Claude는 그림을 생성하지 못한다. 그림이 없어서 생긴 결함은 코드로 고치지 않는다.

## 2. 바뀐 원칙 네 가지

### 2.1 완료의 근거는 판정과 그림이다

등록 수, 타일 일치 수, "출력이 생성됨"은 완료 근거가 아니다. 근거는 다음 둘뿐이다.

1. `verify_runtime_path.py`의 판정
2. 그 검사가 저장한 그림을 사람이 본 결과

기존 `verify_foreground_scenes.py`는 동기 준비 + 일시정지 + 한 프레임이라 플레이어와 다른 경로를 돈다. 그 출력을 장면이 정상이라는 근거로 쓰지 않는다.

### 2.2 코어가 숨긴 것은 반드시 그린다

코어는 프레임을 에뮬레이션할 때 파츠별로 "원본을 숨길지"를 정하고, 그 결정을 파츠 제어값의 bit31에 담는다 (`parts[i][7] & 0x80000000`이 켜져 있으면 원본이 화면에 남아 있다는 뜻).

- 코어(`srww_parts_impl.h`의 `SRWWHD_ShouldSkipRobot`)와 렌더러(`hd_parts.py`의 `compose`)가 같은 비트를 본다.
- bit31이 꺼진 파츠의 텍스처가 렌더러에 없으면 `PartsRenderer.rescue()`가 그 자리에서 읽어 온다. 캐시가 비워져도 원본과 HD가 둘 다 없는 프레임은 나오지 않는다.

숨김 조건을 새로 만들 때는 이 비트를 거치게 한다. 렌더러 쪽에서 따로 "그리지 않음"을 결정하는 분기를 추가하면 소실이 다시 생긴다.

### 2.3 기체는 통째로 HD이거나 통째로 원본이다

전투 화면 배치일 때 코어는 OBJ 팔레트 슬롯별로 HD 면적과 원본 면적(그림이 없는 파츠 + 아직 준비 안 된 파츠)을 센다. 원본 비중이 10% 이상이면 그 프레임에는 슬롯 전체를 원본으로 둔다.

- 따라서 **한 자세의 파츠 일부만 연결하면 화면에는 아무 변화가 없다.** 자세 단위로 전 파츠를 한 번에 연결해야 한다.
- 임계값은 환경 변수 `SRWW_UNIT_FALLBACK_PERCENT`로 바꾼다. 0이면 끈다. 기본값은 `srww_parts_impl.h`의 `SRWW_UNIT_FALLBACK_DEFAULT`.
- 판단 단위가 팔레트 슬롯이다. 한 기체가 슬롯을 여러 개 쓰면 슬롯별로 따로 판정된다. 효과가 기체와 슬롯을 공유하면 효과 때문에 기체가 원본으로 돌아갈 수 있다.

### 2.4 가공은 미리 하고, 실행 중에는 읽기만 한다

파츠 하나를 화면에 쓸 수 있게 만드는 가공(아틀라스에서 자르기, 리샘플링, 원본과의 정렬 탐색, 가장자리 정리)은 중앙값 77ms, 최대 274ms가 걸린다. 예전에는 이것을 파츠가 처음 화면에 나올 때 작업 프로세스 하나가 한 줄로 처리했다. 새 자세가 나올 때마다 원본이 몇 초씩 보인 이유다.

지금은 다음과 같이 동작한다.

- `scripts/assets/bake_parts.py`가 전체 소스 파츠(89,199개)를 미리 가공해 `graphics/parts_baked.sqlite`에 저장한다.
- 렌더러는 시작할 때 저장소에 있는 파츠 목록(`PartsRenderer.baked`)을 읽고, 그것들을 처음부터 "준비됨"으로 코어에 알린다. 코어는 원본을 바로 숨기고, 렌더러는 그릴 때 저장소에서 읽는다.
- 저장소에 없는 파츠는 예전처럼 작업 프로세스가 가공하고, 그동안 원본이 보인다.

## 3. 저장소 형식

| 항목 | 값 |
|---|---|
| 파일 | `graphics/parts_baked.sqlite`, 테이블 `textures` |
| 크기 | 원본 파츠의 4배 (`hd_parts.STORE_SCALE`) |
| 압축 | WebP 무손실 (`exact=True`) |
| 키 | 정렬 코드 해시 + 등록 방식 + 파츠 좌표·크기 + 저장 형식 태그 + 아틀라스 두 파일의 경로·수정 시각·크기 |

- 4배인 이유: 렌더 폭 상한이 960px(`render_resolution.MAX_WIDTH`)라 화면 배율이 최대 3.75배다. 상한을 올리면 `STORE_SCALE`도 올리고 다시 구워야 한다.
- 정렬 계산은 예전과 같이 8배에서 하고, 저장 직전에만 4배로 줄인다.
- 이전 저장소 `graphics/parts_registered.sqlite`(8배, zlib, 약 8.4GB)는 지우지 않았다. 실행 중에는 읽지 않고, 굽기 도구가 같은 정렬 결과를 재사용하는 원천으로만 읽는다. 사용자가 삭제를 금지했다.
- 두 sqlite 파일은 다시 만들 수 있는 산출물이다. 커밋하지 않는다. `parts_registered.sqlite`는 현재 Git LFS 추적 대상이므로 `git add` 범위에 들어가지 않게 주의한다.

**키에 아틀라스 파일의 수정 시각이 들어간다.** 아틀라스 PNG를 다시 저장하면 그 아틀라스의 모든 파츠가 저장소에서 빠진 것으로 취급되어 예전의 느린 경로로 돌아간다. 그림을 고친 뒤에는 반드시 다시 굽는다.

## 4. 그림을 추가할 때의 순서

1. 대상 고르기. `docs/IMAGE_REWORK_FOR_CODEX.md`의 표와 `test_current/combat/runtime_path/regression/gaps.json`·`gaps.png`를 본다. 기체 하나, 자세 하나를 정한다.
2. 저장 상태 확보. 그 무장의 전투 장면이 `test_current/combat/named_attacks/unit_<id>/` 아래에 `.state`로 있어야 측정할 수 있다. 없으면 먼저 만든다.
3. 그림 제작과 라이브러리 연결. 그 자세의 전 파츠를 한 번에 넣는다 (2.3).
4. 굽기.

   ```powershell
   & 'C:/Program Files/Python311/python.exe' -X utf8 scripts/assets/bake_parts.py
   ```

   바뀐 것만 처리한다. 결과는 `test_current/parts/bake/report.json`. `errors`가 0이 아니면 그 파츠는 구워지지 않은 것이다.
5. 재생 검사.

   ```powershell
   & 'C:/Program Files/Python311/python.exe' -X utf8 scripts/verify/verify_runtime_path.py --units <id> --per-unit 99 --name unit_<id>
   ```

6. 판정과 그림 확인 (5절).
7. 여기까지 통과한 뒤 사용자에게 실제 게임 확인을 요청한다.

코어 소스(`emulator/desmume/desmume/src/`)를 고쳤으면 DLL을 다시 빌드하고 `scripts/build/export_core_patch.py`로 `emulator/hd_core.patch`를 갱신한다. 실행 중인 프로그램은 DLL과 파이썬 코드를 다시 읽지 않으므로, 확인 전에 프로그램을 새로 시작해야 한다.

## 5. 재생 검사 읽는 법

`verify_runtime_path.py`는 저장 상태를 불러와 게임을 계속 진행시키면서, 플레이어와 같은 조건(비동기 준비, 런타임 타일 조립, 지연된 ready 전달)으로 그린다. 출력은 `test_current/combat/runtime_path/<name>/`.

| 판정 | 뜻 | 할 일 |
|---|---|---|
| `FAIL` | 코어가 숨긴 파츠에 HD가 그려지지 않은 프레임이 있다 | 코드 결함. Claude에게 넘긴다 |
| `INCOMPLETE` | 로딩이 가라앉은 뒤에도 HD 면적이 98% 미만 | 그림이 덜 연결됐다. `gaps.json`에서 그 장면의 파츠를 찾는다 |
| `NO_HD_PARTS` | 화면에 HD로 연결된 OBJ가 없다 | BG 그림 장면이거나 기체 전체가 미연결 |
| `REVIEW` | 잴 수 있는 결함이 없다 | 저장된 그림을 직접 본다 |

"verified" 판정은 없다. `REVIEW`는 통과가 아니라 사람 차례라는 뜻이다.

장면별 주요 값:

- `hd_area_share_settled`: 재생 후반부의 HD 면적 ÷ (HD + 원본) 면적
- `loading_ms`: 마지막으로 원본 대기 파츠가 보인 시점
- `mixed_frames`: HD와 원본이 한 화면에 같이 있던 프레임 수
- `hd_flips`: HD 표시가 켜졌다 꺼진 횟수. 크면 깜빡임이다
- `rescued`: 2.2의 그 자리 준비가 일어난 횟수

저장되는 그림은 좌우 한 쌍이다. **왼쪽은 원본이 아니라 코어 출력**이다(준비된 파츠가 이미 숨겨진 상태). 오른쪽이 HD 합성 결과다.

`gaps.json`은 화면에 나왔지만 연결된 그림이 없는 OBJ를 화면 점유가 큰 순으로 나열한다. `gaps.png`는 앞 640종을 순위 순으로, 한 줄에 16개씩 원본 크기로 보여 준다.

## 6. 이 검사가 잡지 못하는 것

- **연결됐지만 틀린 그림.** HD로 그려지기만 하면 HD 면적으로 센다. 다른 기체의 그림이 붙어도 통과한다. 기존 그림을 재사용하거나 재색칠해서 빈 곳을 채우지 않는다.
- **BG 레이어에 그려지는 것.** 확대 컷, 배경, BG 효과는 OBJ 목록에 나오지 않는다. IMG 23382·25822 같은 건은 소스 대조로 따로 찾아야 한다.
- **대사창 침범, 보조창 그림, 레이어 순서 오류.**
- **저장 상태가 없는 장면.** 보유 상태는 161개, 무장 기록은 1804개다.
- **실제 속도.** 검사 프로세스는 에뮬레이션과 렌더를 한 프로세스에서 하므로 36~51fps로 돈다. `loading_ms`는 같은 검사끼리 비교할 때만 의미가 있다.

## 7. 알려진 미해결

- 사용자 제보 중 FMP 기체 소실, 그레이트 마징가 보조창, 썬더 브레이크 손·발 깨짐, 대사창 침범은 원인이 확정되지 않았다.
- `SRWWIndexedBindings`는 팔레트를 뺀 인덱스 해시만으로 파츠를 연결하고 먼저 등록된 것이 이긴다. 작은 파츠에서 다른 기체 그림이 붙을 수 있다. 썬더 브레이크 건의 후보다.
- 배포판은 저장소를 사용자 PC의 캐시 폴더에서 찾는다. 구운 `parts_baked.sqlite`를 배포판에 넣는 방법은 정하지 않았다. 그전까지 배포판 사용자의 첫 로딩은 빨라지지 않는다.
- `dist/` 재빌드와 커밋은 하지 않았다.
- 핸드오프 문서는 unit 297을 FDS 겟타로 적었지만 이름 목록(`named_unit_catalog.json`)에는 마징카이저KS로 나온다. 장면과 기체 ID 대응을 다시 확인해야 한다.

## 8. 손댄 파일

| 파일 | 내용 |
|---|---|
| `emulator/hd_parts.py` | `rescue()`, `texture_key()`, `load_baked()`, `STORE_SCALE`, `compose()`의 결과 계수(`last_stats`) |
| `emulator/parts_disk_cache.py` | WebP 저장소, 이전 저장소 읽기 전용 클래스 |
| `emulator/runtime_paths.py` | 배포판 캐시 파일 이름이 저장소 이름을 따르도록 변경 |
| `emulator/desmume/desmume/src/srww_parts_impl.h` | 기체 단위 원본 유지, bit31 통일 |
| `emulator/desmume/.../desmume_libretro.dll` | 새 빌드. 이전 빌드는 `desmume_libretro.previous.dll` |
| `emulator/hd_core.patch` | 다시 내보냄 |
| `scripts/verify/verify_runtime_path.py` | 신규 |
| `scripts/assets/bake_parts.py` | 신규 |
