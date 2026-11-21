# Claude 검토 요청: SRW W HD 작업 실패 원인과 현재 상태

작성일: 2026-11-11 (한국 시간)

이 문서는 사용자가 다른 에이전트에게 현재 작업을 검토시키기 위해 요청한 인계 문서다. **완료 보고서가 아니다.** 작성자의 추정도 포함되어 있으므로 코드·원본 프레임·HD 출력으로 독립 검증해 주기 바란다.

## 1. 사용자 요구와 지금의 결과

목표는 슈퍼로봇대전 W의 기체·무장·컷인·초상화·지도·배경·효과를 HD로 연결하고, 원래 애니메이션과 레이어 순서·팔레트·투명도를 보존하며, 실제 게임에서 확인하는 것이다. 추가로 배포 가능한 실행 파일, 빠른 로딩, 성능 개선, 진동, GitHub 반영을 요구했다.

현재 결과는 그 목표에 크게 못 미친다. 사용자가 직접 테스트하면서 원본과 HD가 섞인 기체, 누락된 공격 자세·효과, 이상한 보조창 그림, 파츠 깨짐, 기체 소실 등을 계속 발견하고 있다. **전 기체·전 무장·전 컷인 HD 완료 또는 실제 게임 전수 검증 완료라고 말할 수 없다.**

사용자는 테스트 창을 직접 조작 중이다. 임의로 창을 닫거나 키를 보내지 말 것. 컴퓨터 종료 요청은 나중에 철회되었다. **완료해도 컴퓨터를 끄지 않는다.** ROM과 세이브는 공개 저장소에 올리지 않는다.

## 2. 내가 잘못한 점 — 검토의 핵심

1. **생성·등록·매칭·실제 표시를 혼동했다.** 이미지 파일을 만들었거나 바인딩 검사에서 통과한 것을 실제 전투에서 정상 HD로 나온 것처럼 취급한 판단이 있었다. 공격 시작·진행·종료, 변형·팔레트·보조 화면까지 확인해야 한다.
2. **검증 범위보다 큰 완료 표현을 사용했다.** 소수 저장 상태의 ID 인식, 합성 성공, 실행 파일 스모크 테스트는 전체 게임의 시각적 정상 동작 증거가 아니다. 기존 보고서의 “검증” 표현도 그대로 신뢰하지 말아야 한다.
3. **사용자에게 실행된 코드와 수정된 코드가 일치하는지 충분히 통제하지 못했다.** Python 부모 GUI, 에뮬레이션 작업 프로세스, 텍스처 작업 프로세스, 여러 DLL, 배포 폴더가 공존한다. 파일 수정만으로 이미 실행된 프로그램이 갱신되지는 않는다.
4. **공통 합성 원인을 고치기 전에 개별 예외와 자산 연결을 누적했다.** 뒤에 그려야 하는 배경을 기체 위에 그리는 문제, 대사창 위로 HD가 올라오는 문제, 팔레트·마스크 문제가 반복됐다.
5. **자동 검사가 시각적 결함을 검출하지 못한다.** 최신 42장 검사도 배열 크기·자료형·출력 성공을 확인할 뿐, 기체 소실·손 깨짐·원본 잔류를 실패로 판정하지 않는다. “Verified 42” 출력은 42장이 정상이라는 뜻이 아니다.
6. **동적 합성과 로딩 의존을 남긴 채 커버리지 수치를 제시했다.** 기본 자세 그림이 있어도 모든 공격 파츠에 쓸 수 있는 것은 아니다. 부분 매칭·지연 합성·잘못된 재색칠로 실제 그림이 달라진다.
7. **산출물과 변경이 과도하게 쌓였다.** 미커밋 코드와 에셋, 오래된 보고서, 실험 DLL, 테스트 출력이 많고 배포물이 최신 소스보다 뒤처져 있다. 재현 가능한 하나의 검증 경로가 필요하다.

위 항목은 작업 방식에 대한 자기 평가다. 모든 결함의 기술적 원인이 확정되었다는 의미는 아니다.

## 3. 작업 위치와 보호 사항

- 저장소: `D:/패치유틸.xdeltaUI/work_srw_w_voice`
- 원격: `https://github.com/kimjh-eclipse/srw-w-hd`, 브랜치 `main`
- 확인한 마지막 커밋: `d4bf96e7` — `Remove unsupported neighboring atlas strokes from attack parts`
- 실행: 프로젝트 `run.py`; 별도 테스트 UI는 `scripts/diagnostics/preview_unit_attacks.py`
- Python: `C:/Program Files/Python311/python.exe`
- 규칙: 루트 `AGENTS.md`를 먼저 읽을 것.
- 유일한 시험 ROM: `release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds`
- ROM SHA256: `0a5a22bd6bb25ebe640767e6b422b91358636e9ae1300e61d7e8ac3c5d8cd478`
- `inputs/`, `baseline/`, 사용자 세이브, 다른 음원 작업, 프로젝트 외 파일을 보존한다.
- 기존 바인딩 앞 5263개 및 `graphics/kazuma_parts_atlas_facefix.png`는 보호 대상으로 기존 검사 도구가 확인한다.
- `emulator/desmume`는 별도 Git 상태도 확인해야 한다. 상위 저장소 배포에는 `emulator/hd_core.patch` 내보내기가 필요하다.

`git status --short`에는 수천 개의 미추적 테스트 파일이 있으므로 처음에는 `--untracked-files=no`, 변경 통계, 대상 디렉터리별 목록을 사용하라. 무차별 `git add .` 금지. ROM·세이브·재생 상태는 공개 푸시 대상이 아니다.

## 4. 최신 사용자 제보 — 정상 확인되지 않음

| 장면 | 실제 문제 | 검토 방향 (아직 가설 포함) |
|---|---|---|
| 가이 / 녹색 기체, 양 주먹을 내민 확대 장면 | 기체와 주변 효과가 원본 픽셀로 보임 | 별도 확대 BG 이미지인지 확인하고 소스 IMG/SCR/PLT부터 대조 |
| 그레이트 마징가 / 썬더 브레이크 | 보조창 작은 기체 그림이 이상함 | 주 화면과 다른 바인딩·팔레트·축소 경로 조사 |
| 같은 공격의 본체 | 몸 일부는 HD지만 손·발 등 일부 파츠 깨짐 | 정확한 사각형·팔레트·원본 좌표와 HD 소스 비교 |
| FMP 여러 기체 | HD 지연, 팔·다리·칼 원본 잔류, 전투 도중 기체 소실 | 작업 큐와 합성 순서 및 소스 누락을 분리 |
| 겟타 3 / 벤케이 | 몸통 상당 부분이 원본 | 기본 자세 외 공격 파츠 누락 확인 |
| FDS / 료마의 겟타 확대 | HD 주먹과 원본 몸통·에너지 효과 혼재 | IMG 23382가 몸통 유력 소스, 아래 증거 참조 |
| 발호크 맥시멈 슈트·빔·마지막 폭발 | 효과 원본, 기체와 효과 순서 이상 | BG/OBJ 우선순위와 새 효과 에셋 연결 각각 필요 |
| 아스테바리스 공격 | 기본 컷인 HD여도 실제 공격 자세가 원본 | 자세별 파츠와 동적 합성 검사 |
| 블레이드 합체 공격 | 무기·팔 일부 이상 | 다른 소스의 잘못된 재사용 여부 확인 |
| HD 전반 | 대사창 프레임·이름칸 위에 HD가 올라옴 | 공통 대사 UI 보호 필요. 마지막 42장에서도 예외가 남음 |

최근 첨부 파일은 `C:/Users/OXP2/AppData/Local/Temp/`에 있다:

- `codex-clipboard-0f2dd701-6e30-4ce2-90f4-12aa96ee6d80.png`: 가이 장면.
- `codex-clipboard-e242ae59-6db1-4c28-b1a8-0bdfe5afeedd.png`: 그레이트 마징가 보조창.
- `codex-clipboard-42b88245-f59f-47dd-a484-6e24fd3249de.png`: 썬더 브레이크 파츠 깨짐.
- `codex-clipboard-0df691c0-1020-4848-a74e-9879ac367425.png`: FMP 기체 소실.
- `codex-clipboard-a660b91c-9c92-4912-806e-7cb5274a7efa.png`: 겟타 확대 몸통 원본.
- `codex-clipboard-2306be3b-2034-4e84-b1ad-0c916ca02413.png`: 파란 폭발 효과 원본.

과거 제보의 글꼴 깜빡임·검은 사각 배경·붉은색/노란색 HP 숫자·외곽선·팔레트 오류·60프레임·진동 전수 적용도 전체 해결됐다고 인증할 수 없다.

## 5. 주요 코드와 최근 미커밋 변경

### 공통 합성

- `emulator/hd_renderer.py`: 주/보조 화면 조립, 컷인, 대사창 복원.
- `emulator/hd_parts.py`: 파츠 선택·팔레트 변경·비동기 준비·그리기 순서.
- `emulator/gpu_surface.py`: GPU 그리기와 foreground 셰이더.
- `emulator/foreground_blend.py`: 신규. native BG 반투명 합성의 CPU/GPU 공통 계산.
- `emulator/frame_compositor.py`, `hd_core.py`: 프레임 자료 전달 및 네이티브 브리지.
- `emulator/desmume/desmume/src/GPU.cpp`, `srww_hd.h`, `srww_parts_impl.h`, `frontend/libretro/libretro.cpp`: 네이티브 변경.

신규 foreground 브리지는 RGB555, EVA/EVB, 대상 플래그, 실제 native 대상 레이어를 전달한다. 네이티브 API `retro_srw_foreground_format()` 값 3을 요구한다. 수학 테스트 통과와 실제 모든 효과의 정상 표시는 별개다.

바로 직전 변경: 컷인/BG 콜백과 HD OBJ를 `PartsRenderer.compose(..., background_planes=...)`의 동일 우선순위 큐에서 그리도록 했다. 이전에는 모든 OBJ 다음 모든 컷인을 그려, 불투명 구름 BG인 컷인 168이 기체를 덮을 수 있었다. **수정 후에도 다른 소실 원인이 남는지 조사 필요.** 동일 BG에 일반 BG 파츠와 컷인이 중복되는 경우, native ownership 마스크와 native 그리기 생략이 충돌하는 경우도 검토하라.

대사창 수정은 전투에서 native y=128..191 영역을 `clean_native()` 후 다시 덮고 HD 글자·초상화를 그리는 방식이다. `hd[10]`, `is_battle`, cyan 감지 조건을 사용한다. 이것은 **조건부 휴리스틱**이며 모든 UI 배치/컷인에 맞는다는 증거가 없다. 최신 contact sheet 마지막 겟타/고라이온 장면에는 여전히 컷인과 대사 영역의 문제가 보인다.

### 로딩

`hd_parts.py`에서 64×64 파츠 사전 준비 허용, 8개씩 그룹 사전 준비 완료 판정 수정, 알려진 파츠가 대기 중일 때 미지 파츠 추측 작업 보류, 미지 작업 동시 대기를 12→2로 줄였다. **체감 지연과 프레임 개선 수치는 아직 측정하지 않았다.** StageCache는 약 1 GiB LRU를 사용한다. 캐시가 존재한다는 것과 공격 시작 전에 필요한 자산이 준비됐다는 것은 다르다.

### 테스트 UI

`preview_unit_attacks.py`, `hd_emulator.py`, `gpu_display.py`에 combobox popdown/focus/클릭 통과 방지 수정이 있다. 이전에는 `KeyError('popdown')`, 다른 기체 클릭이 같은 기체로 돌아가는 오류가 있었다. 독립 popup 검사와 두 기체 선택은 확인했지만, 현재 사용자 환경을 다시 확인해야 한다.

## 6. 재현 자료와 검사 결과를 읽는 법

### 최신 실제 저장 상태 재생 검사

실행한 명령:

```powershell
& 'C:/Program Files/Python311/python.exe' -X utf8 scripts/verify/verify_foreground_scenes.py
```

- 출력: `test_current/combat/foreground/regression/report.json`, `contact.png`, 장면별 PNG.
- 직전 실행은 42개 저장 상태 재생과 출력 생성을 마쳤다. 14개 named unit 및 겟타/고라이온 저장 상태 포함.
- **검사가 확인하는 것:** 예외 없이 출력, 768×576 RGB 배열, 인식 ID/합성 시간 기록.
- **확인하지 못하는 것:** 올바른 파츠, 완전 HD, 기체 소실, 정확한 효과 순서, 실시간 프레임 유지.
- contact sheet를 직접 보니 여전히 원본 잔류와 일부 의심스러운 장면이 있다. 이 검사를 “42장 정상 확인”으로 보고하면 안 된다.
- `paused=True`라 실행 중과 다른 native fallback을 허용한다. **paused=False / 실제 연속 재생 및 cold cache 경로도 반드시 확인해야 한다.**

기타 검사:

- `scripts/verify/verify_foreground_blend.py`: 계수·우선순위·가림·CPU/GPU 수학 일치.
- `scripts/verify/verify_popup_focus.py`: Tcl focus/grab/포인터 격리.
- `scripts/verify/verify_repository_layout.py`: 이동 경로·보호 해시·구조 확인. 현재 최신 변경 기준 재실행 필요.
- `verify_compact_cutin_windows.py`, `verify_cutin_region_composition.py`: 제한된 인식/합성 검사. 전투 정상 인증 아님.

### 정확한 소스가 확인된 누락 후보

FDS 겟타 몸통:

- 폴더: `test_current/combat/named_attacks/unit_297/diagnostic_preview/weapon_1213_capture`
- 프레임: 1320. `native_1320.png`, `bg_1320_*.npz`, `frame_1320.state`.
- `source_audit.json`: BG2에서 **IMG 23382의 서로 다른 타일 220개** 정확 일치, 원점 (0,128). 현재 알려진 cut-in 등록 없음.
- BG1은 IMG 23393 14타일, IMG 23397 4타일. 효과 후보.
- 로그: `test_current/combat/getter_chest_source_audit.log`.
- 아직 새 HD 몸통을 만들어 연결하지 않았다.

발호크 빔 효과:

- unit 413 / weapon 1613 / frame 600.
- BG1에서 **IMG 25822 28타일** 정확 일치, 원점 (0,32), 현재 HD 효과 등록 없음.
- 로그: `test_current/combat/jade_effect_source_audit.log`.
- foreground 합성 계산을 고쳐도 이 원본 효과 자체가 새 HD로 바뀌지는 않는다.

관측 사각형 집계:

- `test_current/parts/observed_attack_gaps/current_assembly.json`.
- 이전 집계 3902개 중 동적 합성 성공 414개, 실패 3488개.
- 이는 **기체 수나 미완료 무장 수가 아니다.** 효과와 중복 사각형 등이 섞여 있다.
- 성공 414개도 시각 검증을 거쳐 사전 등록하면 로딩 개선 여지가 있으나 아직 구현하지 않았다.

이름 목록: `test_current/parts/named_unit_catalog.json` (493 unit records / 1804 weapon records). 변형·적·지원·능력치 차이가 포함되어 있어 서로 다른 로봇/공격 개수처럼 세지 말 것.

## 7. 실행물과 배포물 불일치 주의

- production core: `emulator/desmume/desmume/src/frontend/libretro/desmume_libretro.dll`에 format 3 DLL을 복사했다.
- 실험 DLL: `desmume_foreground_verify.dll` (구 ABI), `desmume_foreground_final.dll`, `desmume_foreground_versioned.dll` 등이 남아 있다.
- 사용자 테스트 부모 프로세스가 구 `SRWW_CORE_PATH`를 물려받았었다. `hd_core.py`는 구 ABI override를 감지하면 production format 3으로 우회하도록 수정했다. 새 작업 프로세스에서만 적용된다.
- 마지막 기록된 GUI root PID는 6652지만 **종료/재시작 대상으로 그대로 사용하지 말고 현재 프로세스를 먼저 확인**할 것.
- 테스트 설정: `test_current/gui/unit_review/settings.json`; 플레이어 저장과 분리된 `isolated_saves`.
- `dist/SRW_W_HD` 및 패키지는 최신 소스/ABI/합성/큐 수정 전 빌드가 섞여 있다. **최신 버전이라고 배포하지 말 것.**
- 네이티브 변경 후 `scripts/build/export_core_patch.py` 재실행 필요.
- `distribution/build_portable.py --program-only` 및 필요 시 `--assets-only`, frozen self-test, source bundle, archive 검사를 같은 체크포인트에서 다시 해야 한다.

`docs/COMMON_EFFECT_COMPOSITION.md`, `docs/REMAINING_HD_WORK.md`도 과거 시점의 설명이 섞여 있다. 특히 “현재 배포물에 포함” 또는 “검증 완료” 표현은 빌드 날짜/소스와 대조할 것.

## 8. Claude에게 부탁하는 리뷰와 복구 순서

우선 **수정 없이 독립 리뷰**로 아래를 답해 주기 바란다.

1. HD 렌더 경로가 native 우선순위, window, alpha, 밝기, affine, BG raster 변화를 어떤 지점에서 잃는가? 현재 덮어 그리기 구조 자체가 공통 오류를 반복하는가?
2. native를 숨기는 조건과 HD 자산 준비 성공 조건은 원자적으로 일치하는가? HD 준비 실패/지연에도 native가 지워져 기체가 사라지는가?
3. 주 화면·보조 화면이 정확한 동일 기체/프레임의 소스와 팔레트를 쓰는가? 사각형 크기·hash만 맞고 잘못된 그림이 연결되는가?
4. `paused=True` 검사와 정상 플레이 경로 사이에 어떤 차이가 있는가? 실제로 로딩이 늦거나 무너지는 경로가 검사에서 감춰지는가?
5. 등록 수치·타일 일치·추출 성공을 실제 시각 커버리지로 오인한 보고서를 식별하고, 믿을 수 있는 완료 기준을 제안해 달라.

복구 작업을 맡게 된다면 권장 순서:

1. 사용자 제보 장면 중 소실·파츠 깨짐·UI 침범을 각각 하나씩 고정 재현. native/HD OFF/HD ON 동일 프레임 비교와 연속 재생을 저장.
2. 숨김/그리기 순서/팔레트/좌표/로드 누락 원인을 분리. 잘못 매칭된 자산을 새 그림으로 덮어 감추지 말 것.
3. 공통 수정 뒤 동일 부류의 여러 기체에서 회귀 확인. 성공 장면뿐 아니라 기존 실패 장면을 포함.
4. IMG 23382, 25822 같은 **입증된 누락 자산**을 제작·연결하고 실제 전투에서 확인.
5. cold/warm 로딩 및 실행 중 출력 프레임·입력 지연 측정. core 실행 FPS와 화면 표시 FPS를 분리.
6. 같은 소스 체크포인트로 배포 빌드 후 검증. 변경 파일을 선별 커밋/푸시하고 ROM·세이브 제외 확인.

완료 보고에는 “수정한 것 / 실제 재생으로 확인한 것 / 아직 남은 것”을 분리해 달라. **스크린샷에서 명백한 결함이 남으면 완료가 아니다.**
