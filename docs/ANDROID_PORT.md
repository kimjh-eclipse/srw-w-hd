# 안드로이드 포팅

안드로이드 앱은 사용자가 선택한 ROM과 기존 `graphics/` 팩을 읽는다. 카탈로그의 상대 경로, 바인딩 ID, 해시, PNG·WebP의 형식과 투명도를 그대로 사용한다. 앱 패키지는 에뮬레이터와 렌더링 코드를 담는다. 세이브, 설정, 생성 캐시는 앱의 쓰기 가능한 저장소에 둔다.

## ARM64 네이티브 빌드

Windows에서 Android NDK r27d의 압축을 풀고 프로젝트 루트에서 실행한다.

```powershell
.\scripts\build\build_android_arm64.ps1 -NdkPath 'C:\Android\android-ndk-r27d'
```

기본 대상은 ARM64 및 API 24다. 출력은 `build/android-arm64-api24/lib/arm64-v8a/`에 저장된다. 네이티브 라이브러리에는 수정 DeSmuME, xBRZ, 합성, 글꼴 픽셀 처리와 글꼴 검색이 포함된다. 빌드 스크립트는 ARM64 ELF 헤더와 기존 Python 클라이언트가 호출하는 HD 함수의 내보내기를 확인한다.

2026-11-20에 NDK r27d로 다섯 라이브러리를 빌드했다. 코어 함수 34개와 xBRZ 함수 2개, 모든 라이브러리의 16 KB ELF 세그먼트 정렬을 확인했다. 앱 패키징과 실기기 검증은 앱 통합 단계에서 진행한다.

## 앱 통합 범위

1. Android 호스트에서 Libretro 콜백을 연결하고 ROM을 부팅한다. 두 화면, 아래 화면의 좌표 변환과 터치, 오디오, 게임패드, 일시정지, 세이브를 이어 붙인다.
2. 시스템 파일 선택기로 ROM을, 폴더 선택기로 기존 리소스 팩을 연다. 제공자가 반환하는 URI에서 읽고, 일반 파일 경로가 필요한 디코더와 SQLite에는 앱 전용 저장소의 로컬 사본을 사용한다. 먼저 카탈로그와 실제 리소스의 상대 경로와 경로 대소문자를 대조한다.
3. `hd_core.py`의 리소스 등록과 프레임별 데이터 읽기, `hd_renderer.py`의 레이어 합성 순서를 옮긴다. 로봇 파츠, 컷인, 배경, 글꼴과 HUD, xBRZ의 결과를 윈도우와 비교한다. 화면은 Android의 EGL/OpenGL ES를 기준으로 구현한다.
4. ARM64 실기기에서 프레임 시간과 메모리 사용, 오디오 끊김, 절전 복귀, 저장·불러오기를 검증한다. 이 포크의 Android ARM64 설정은 인터프리터를 사용하므로 윈도우 x64에서 측정한 성능을 기준으로 삼지 않는다. 저장 상태의 플랫폼 간 호환성은 별도로 확인한다.

## HD 팩 로딩

PC 구현은 `emulator/parts_catalog.py`에서 파츠 카탈로그의 중복 팔레트를 한 번만 저장한다. 코어와 렌더러, 텍스처 작업 프로세스가 같은 로컬 캐시를 사용한다. 카탈로그의 SHA-256이 바뀌거나 캐시가 손상되면 원본에서 재생성한다. 캐시를 쓸 수 없는 환경에서도 원본을 열 수 있다.

Android 호스트를 구현할 때도 가져온 팩의 인덱스를 앱 전용 저장소에서 재사용한다. 실기기에서는 최초 가져오기, 같은 팩으로 재실행, 첫 전투 진입을 각각 측정하고 동일 세이브의 HD 화면과 파츠 등록 결과를 PC와 대조한다.

[Android NDK 빌드](https://developer.android.com/ndk/guides/ndk-build) · [Android 파일 및 폴더 선택](https://developer.android.com/training/data-storage/shared/documents-files)
