# 슈퍼로봇대전 W — 카즈마 음성 샘플 시험

사용자가 제공한 일본판에 한글패치 1.0.8을 적용한 롬을 기준으로 작업합니다.
음성은 기존 OGs 작업에서 추출한 액셀의 일본어 원음 한 개입니다. 대사의 내용에
맞춘 더빙이 아니라 게임 내부 음성 재생을 확인하기 위한 샘플입니다.

## 기준 파일

- 원본 압축파일: `C:/Users/OXP2/Downloads/Super Robot Taisen W (Japan) (1).zip`
- 한글패치: `C:/Users/OXP2/Downloads/SRW W 1.0.8.zip`의 `1.0.8.xdelta`
- 일본판 SHA-256: `f76c700b7b44cdf01d8161ab541732dc1a1758bfec74447e1f36545b3d2e14cc`
- 한글판 SHA-256: `0a5a22bd6bb25ebe640767e6b422b91358636e9ae1300e61d7e8ac3c5d8cd478`
- 한글판 기준 파일: `baseline/SRWW_Korean_1.0.8.nds`

한글패치는 xdelta로 정상 적용됐으며, 결과는 작업 폴더에 기존에 있던 W 롬과
해시가 일치합니다. 입력 압축파일과 기존 롬은 수정하지 않았습니다.

## 시험판 동작

- BGM을 음성 파일로 교체하지 않습니다.
- 일반 대사 처리 중 카즈마의 화자 코드가 처음 나타나면 액셀 샘플을 한 번 재생합니다.
- 한 번 재생한 뒤 반복하지 않습니다. 재생이 끝나면 사용한 음성 채널을 반환합니다.
- 여러 대사를 더빙하거나 무기별 음성을 연결하는 기능은 아직 포함하지 않습니다.
- 중간 저장 상태의 코드 교체 시험과 처음 실행부터 하는 시험은 구분해서 기록합니다.
- 이 시험판은 처음 실행한 뒤 새 게임 또는 게임 자체의 로드를 사용하는 것을 전제로 합니다.
  다른 버전의 에뮬레이터 중간 저장 상태는 지원 대상으로 보지 않습니다.

## 개발 자료

- `build_voice_probe.py`: 원본 확인, 음원 변환, 음성 엔진 빌드, 롬/BPS 생성
- `run_core_probe.py`: DeSmuME libretro를 이용한 화면·음성·메모리 기록
- `verify_voice_result.py`: 재생 횟수·종료·오디오 샘플 상관 검증
- `baseline/manifest.json`: 한글패치 적용 결과와 해시
- `probe_manifest.json`: 샘플 출처와 재생 조건
- `voice_engine/out/build_manifest.json`: 시험판 생성 결과

`inspect_dialogue.py`와 `analysis/`는 탐색 중인 자료입니다. 아직 해석하지 못한
제어 코드와 사전 압축 코드가 있으므로 전체 대사 추출 결과로 사용하지 않습니다.

## 참고 및 라이선스

음원 변환과 스트리밍은 공개 프로젝트
[bwah-leaf/SRWw_customBGM_MODE](https://github.com/bwah-leaf/SRWw_customBGM_MODE)를
참고해 수정했습니다. 원본 저장소와 라이선스는 `reference_bgm/`에 보존했습니다.
수정한 엔진 소스와 고지는 `voice_engine/src/`, `voice_engine/LICENSE`,
`voice_engine/AUTHORS.md`, `voice_engine/THIRD_PARTY_NOTICES.md`에 있습니다.
해당 엔진 소스는 MPL-2.0 조건을 따릅니다.

대사 자료의 탐색에는
[NDS-SRW-K](https://github.com/snake759494/NDS-SRW-K)의 공개 포맷 설명도 참고했습니다.

Nintendo DS 실기와 RG351 환경에서의 검증은 별도로 필요합니다.

## 최종 확인 결과

`kazuma_cold_final/`에서 처음 실행 → 새 게임 → 도입부 → 카즈마 대사까지
진행했습니다. 재생 신호는 1회, 음성은 182개 오디오 블록을 모두 재생한 뒤
종료됐고 버퍼 끊김 기록은 0회였습니다. 실제 출력 녹음에서도 원음 샘플을
확인했습니다. 결과는 `verification_result.json`에 기록했습니다.

`kazuma_clean_check/voice_plus_060.png`에서 카즈마의 이름과 대상 대사창을
확인했습니다. 배포용 로컬 결과물은 `release/`에 모았습니다.
