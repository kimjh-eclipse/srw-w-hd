# 소스 구조

실행 코드, 개발 도구, 이전 실험 기록을 분리했습니다. 이 정리는 폴더와 경로 변경이며, HD 적용 범위나 미완료 기능을 완료 처리하는 변경은 아닙니다.

```text
run.py                   게임 실행 진입점
emulator/                플레이어·화면 합성·입력·캐시 실행 코드
  desmume/               수정한 DeSmuME 원본 소스와 라이선스
  native_*.c             성능이 필요한 네이티브 보조 코드
scripts/
  assets/                추출·제작 준비·등록·이미지 최적화
  verify/                기능·화면·성능 검증
  diagnostics/           캡처·추적·프로파일링·분석
  build/                 네이티브 보조 DLL 빌드·코어 패치 내보내기
  run.py                 개발 도구 실행과 목록 확인
  tool_index.json        도구 이름 → 실제 소스 경로
distribution/            Windows 실행 파일·배포 ZIP 제작
graphics/                HD 그림·연결 정보·생성 출처
docs/                    구조 설명·이전 경로 대조표
research/legacy/         중단한 음성 연구·이전 검사 자료
test_current/            현재 검사 결과와 재현용 로컬 상태
tools/                   로컬 컴파일러·외부 도구
build/                   임시 빌드·변환 이미지
dist/                    배포 실행 파일·ZIP
inputs/                  보존하는 원본 입력 자료
baseline/                보존하는 기준 한글 ROM
release_battle_v02/      계속 사용하는 시험 ROM 한 개
```

`reference_bgm/`와 `release/`의 기존 자료는 별도 출처와 용도를 가진 로컬 자료이므로 그대로 보존했습니다. 프로젝트 바깥의 사용자 파일도 이동하지 않았습니다.

## 실행

저장소 루트에서 `python run.py`를 실행합니다. 기존 `emulator/HD_게임실행.cmd`도 계속 사용할 수 있습니다. 실행 코드의 위치, 개인 설정과 세이브 경로는 유지합니다.

## 개발 도구

```powershell
python scripts/run.py --list
python scripts/run.py verify_stage_cache
python scripts/verify/verify_controller_chords.py
python scripts/build/build_native_font_pixels.py
python distribution/build_portable.py --program-only
```

개별 도구는 다른 작업 폴더에서도 절대 경로로 실행할 수 있습니다. 프로젝트 위치와 실행 모듈 검색 경로는 `scripts/_bootstrap.py`에서 공통으로 설정합니다. 여러 도구를 호출하는 작업은 `tool_path()`로 경로를 찾습니다.

기존 경로 전체 대조표는 `docs/source_moves.json`입니다. 도구 호출 경로와 파이썬 모듈 참조, Git LFS의 파일 경로를 함께 갱신했습니다. 과거 커밋을 읽는 `git show 커밋:경로`는 당시 경로를 유지합니다.

## 작업 상태와 보존 범위

- 이전 음성 실험 자료는 삭제하지 않고 `research/legacy/`로 묶었습니다.
- ROM·세이브·승인된 얼굴 그림과 초기 연결 정보는 이 정리에서 변경하지 않습니다.
- 흰색·빨간색·노란색 숫자 처리와 기체별 이름/무장/컷인 연결에 대한 진행 중 수정은 보존합니다. 이번 구조 정리의 검사 통과를 해당 기능의 전체 완료로 해석하면 안 됩니다.
- 배포용 소스 묶음에는 새 `scripts/`와 `docs/`를 포함합니다. ROM과 개인 저장 데이터는 포함하지 않습니다.

새 개발 도구를 추가하면 목적에 맞는 하위 폴더에 넣고 `scripts/tool_index.json`에 등록합니다. 기능별 검사 결과는 기존 규칙대로 `test_current/`의 고정 경로에 기록합니다.
