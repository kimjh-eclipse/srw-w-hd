# SRW W ADPCM STRM 커스텀 BGM 패처

[한국어](README.md) | [English](README.en.md)

Nintendo DS용 **슈퍼로봇대전 W 한국어판 2.0.3**에 사용자 소유 음원을
ADPCM STRM 커스텀 BGM으로 삽입하는 비공식 오픈소스 도구입니다.

이 저장소에는 ROM, 게임에서 추출한 데이터, 음악, FFmpeg, devkitARM,
Nintendo SDK가 포함되지 않습니다. 사용자는 합법적으로 취득한 지원 ROM과
사용 권한이 있는 음원을 직접 준비해야 합니다.

## 주요 기능

- MP3, WAV, FLAC 등 FFmpeg 입력을 22,050 Hz Nintendo DS IMA-ADPCM STRM으로 변환
- 트랙별 모노/스테레오 선택과 최대 ROM 용량 사전 검증
- 최대 70개 BGM ID를 무결성 정보와 함께 `.bgm.pak` v3로 패키징
- ARM9 스트리밍 엔진 컴파일 및 검증된 훅·코드 케이브 적용
- 패치 ROM, 배포용 BPS, 재현 정보가 담긴 빌드 매니페스트 생성
- BGM 정지·전환 시 이중 버퍼 언더런 페이지를 무음 처리

## GitHub Release 사용

[Releases](../../releases/latest)에서 다음 파일을 같은 폴더에 받습니다.

```text
SRW_W_BGM_Pack_Maker.exe
SRW_W_BGM_ROM_Patcher.exe
SHA256SUMS.txt
```

Release EXE에는 실행에 필요한 Python과 Tcl/Tk 런타임이 포함되어 있으므로
Python을 별도로 설치할 필요가 없습니다. EXE는 PyArmor로 난독화하지 않았으며,
이 저장소의 공개 소스를 PyInstaller로 패키징한 Windows x64 단일 실행 파일입니다.

현재 EXE는 코드 서명되지 않았으므로 Windows SmartScreen 경고가 나타날 수
있습니다. 실행 전에 Release에 첨부된 `SHA256SUMS.txt`와 파일 해시를 확인하십시오.

```powershell
Get-FileHash -Algorithm SHA256 .\SRW_W_BGM_Pack_Maker.exe
Get-FileHash -Algorithm SHA256 .\SRW_W_BGM_ROM_Patcher.exe
```

## 사용자 요구 사항

- Windows 10/11
- [FFmpeg](https://ffmpeg.org/download.html): 음원 변환 시 필요
- [devkitARM](https://devkitpro.org/wiki/Getting_Started): ARM9 패치 빌드 시 필요
- 지원 원본 ROM SHA-256:
  `9cbeacfe4fdbeacd6b0ea070b2f2a583c04018f49a47f1e636d02614988c1287`

FFmpeg와 devkitARM은 EXE에 포함되지 않습니다. libnds와 Nintendo SDK는 필요하지
않습니다.

## 빠른 시작

1. Release에서 받은 파일의 SHA-256을 확인합니다.
2. `SRW_W_BGM_Pack_Maker.exe`를 실행합니다.
3. `ffmpeg.exe`와 음원을 지정하고 BGM ID별 모노/스테레오 설정 후 `.bgm.pak`을 만듭니다.
4. `SRW_W_BGM_ROM_Patcher.exe`를 실행합니다.
5. 지원 원본 ROM, 생성한 `.bgm.pak`, devkitARM 폴더와 출력 폴더를 지정합니다.
6. 출력 ROM과 `build_manifest.json`을 에뮬레이터에서 검증합니다.

`SRW_W_BGM_Pack_Maker.exe`와 `SRW_W_BGM_ROM_Patcher.exe`는 서로 독립적입니다.
음원 제작자는 `.bgm.pak`만 전달할 수 있고, 사용자는 ROM 패처로 자신의 원본
ROM에 직접 적용할 수 있습니다.

## 소스에서 실행

소스 실행과 개발에는 Python 3.10 이상이 필요합니다. Python 애플리케이션 자체는
표준 라이브러리만 사용합니다.

```powershell
SRW_W_BGM_Pack_Maker.bat
SRW_W_BGM_ROM_Patcher.bat
```

또는 `python app_gui.py --pack`, `python app_gui.py --patch`로 직접 실행합니다.

CLI 예시:

```powershell
python gui_patcher.py --make-pack --ffmpeg C:\tools\ffmpeg.exe `
  --track "0=C:\music\opening.flac" --pack-out out\custom.bgm.pak

python gui_patcher.py --apply-pack --rom C:\roms\input.nds `
  --pack out\custom.bgm.pak --devkitarm C:\devkitPro\devkitARM `
  --output-dir out\rom
```

## 오디오 규격과 용량

```text
Sample rate : 22,050 Hz
Channels    : Mono 또는 Stereo (트랙별 선택)
Codec       : Nintendo DS IMA-ADPCM (4-bit)
Container   : STRM (HEAD/DATA 블록 스트림)
```

변환에는 20 Hz 하이패스, 9.5 kHz 로우패스, 70% 프리게인과 피크
리미터가 적용됩니다. 재생 채널 음량은 110/127로 제한됩니다. 검증된 원본에서
사용할 수 있는 보수적인 모노 환산 한도는 약 `11:38:05`이며, 스테레오 1초는
모노 2초와 같은 공간을 사용합니다.

## 개발 및 테스트

```powershell
python -m unittest discover -s tests -v
python -m compileall -q .
```

### Windows EXE 빌드

`build_release.bat`을 실행하면 프로젝트 전용 `.venv`에 고정 버전
PyInstaller를 설치하고 다음 파일을 `dist/`에 만듭니다.

```text
SRW_W_BGM_Pack_Maker.exe
SRW_W_BGM_ROM_Patcher.exe
SHA256SUMS.txt
```

EXE는 난독화하지 않습니다. 카탈로그, ARM9 빌드 소스, MPL 라이선스, 저작자와
제3자 고지를 그대로 묶습니다. ROM, 음원, FFmpeg, devkitARM과 Nintendo SDK는
포함하지 않습니다. GitHub Release에는 두 EXE와 `SHA256SUMS.txt`, 해당 태그의
GitHub 자동 생성 소스 압축 파일을 함께 제공하십시오.

ARM9 페이로드는 ROM 패치 단계에서 devkitARM의 `arm-none-eabi-gcc`,
`objcopy`, `nm`을 사용해 빌드됩니다. 빌더는 입력 ROM 해시, 원본 훅 바이트,
코드 케이브의 빈 영역, 페이로드 크기와 BPS 라운드트립을 확인하고 하나라도
일치하지 않으면 중단합니다.

## 저장소 구조

| 경로 | 내용 |
|---|---|
| `app_gui.py` | 두 GUI의 진입점 |
| `gui_patcher.py` | 음원 변환·패키지 적용 워크플로와 CLI |
| `bgm_pack.py` | BGM.PAK v3 읽기·쓰기·검증 |
| `strm_codec.py` | IMA-ADPCM STRM 인코더·파서 |
| `build.py` | ARM9 빌드, ROM 삽입, BPS 생성·검증 |
| `src/` | ARM9 훅, 스트리밍 엔진, 링커 스크립트 |
| `tests/` | 패키지·매핑·포맷 회귀 테스트 |

## 알려진 제한

- 일부 에뮬레이터 설정에서 STRM 간 전환 시 매우 짧은 정지감이 들릴 수 있습니다.
- 에뮬레이터의 오디오 동기화, 프레임 스킵과 백엔드 설정에 따라 결과가 달라집니다.
- 현재 코드는 위 SHA-256의 한 리비전만 지원하며 다른 ROM에는 적용하지 않습니다.
- Nintendo DS 실기 검증은 완료되지 않았습니다.

문제를 제보할 때 ROM이나 저작권 음원을 첨부하지 말고, 에뮬레이터와 버전,
BGM ID, 장면, 재현 절차, `build_manifest.json`의 비민감 정보만 제공하십시오.

## 라이선스

프로젝트의 소스 코드 형식은 [Mozilla Public License 2.0](LICENSE)에 따라
배포됩니다. MPL-2.0은 파일 단위 카피레프트 라이선스입니다. 수정한 MPL 파일을
실행 가능한 형태로 배포할 경우 해당 수정 파일의 소스도 MPL-2.0 조건으로
제공해야 합니다. 별개의 파일과 더 큰 결합 저작물에는 다른 라이선스를 적용할
수 있습니다.

제3자 프로그램과 게임 관련 권리는 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)를
참조하십시오. 기여 방법은 [CONTRIBUTING.md](CONTRIBUTING.md)를 따릅니다.

## 비공식 프로젝트 고지

이 프로젝트는 Nintendo, Bandai Namco Entertainment 또는 Banpresto와 제휴하거나
보증받지 않았습니다. 제품명과 상표는 호환 대상을 설명하기 위해서만 사용합니다.
