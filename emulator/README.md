# 플레이어 실행 코드

이 폴더에는 게임 실행에 필요한 모듈과 수정한 DeSmuME 코어를 둡니다.

- `hd_emulator.py`, `portable_entry.py`: 개발 실행과 배포 실행 진입점
- `hd_core.py`, `player_worker.py`: 에뮬레이션 코어와 게임 실행 프로세스
- `hd_renderer.py`, `frame_*`, `gpu_*`: HD 화면 합성·전송
- `hd_parts*`, `tile_*`, `hd_*backgrounds.py`: 그림 연결과 합성
- `player_controls.py`, `player_shortcuts.py`, `pad_process.py`: 입력과 패드
- `stage_cache.py`, `parts_disk_cache.py`: 이미지 캐시
- `native_*.c`, `native_*.dll`: 네이티브 보조 모듈
- `desmume/`: 수정한 상위 프로젝트 소스와 라이선스

추출·등록·검사·진단 도구는 상위 `scripts/`로 이동했습니다. 실행 방법은 [개발 도구](../scripts/README.md), 전체 경로는 [소스 구조](../docs/SOURCE_LAYOUT.md)에 있습니다. 기존 실행 CMD와 개인 설정·세이브 경로는 유지합니다.
