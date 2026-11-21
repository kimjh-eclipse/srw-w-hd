# 보조화면 HP 라벨·체력바 원본 인계

## 범위와 현재 상태

사용자 제보 `C:/Users/OXP2/AppData/Local/Temp/codex-clipboard-620696ae-cdd2-4d3e-bc2b-a6b7dce9528e.png`와 같은 전투 보조화면 HUD 원천을 준비했습니다. 그림 생성·HD 연결·굽기·런타임 코드 수정·공식 HD 재생 검증은 하지 않았습니다. 사용자 게임창과 물리 입력도 건드리지 않았습니다.

제보 화면은 적 `우주해적` HP239 / 아군 카즈마 HP5000입니다. 이번에 보유한 독립 원본은 적 `에이드` HP1308→0 / 카즈마5000으로, 적과 수치가 다릅니다. 이름 판과 노란 HP 두 개, EN 없는 단일 체력줄 및 초록/빨강 바의 구조는 동일합니다. 제보와 정확히 같은 프레임을 확보했다고 주장하지 않습니다.

## 순수 원본 두 시점

`stable_fixture_contract.json`에 실제 DLL 경로/SHA와 원점 state를 기록했습니다. 원점은 기존413/무장1610 frame360에서 +90인 `test_current/ui/valhawk_reported_pose/actual_frame90.state`입니다. 독립 Core를 `enabled=False`로 실행해 `core.native`만 저장했습니다.

- `native_offset0/`: 원점 로드 후1회 run. 적 HP1308(노랑), 아군5000. 왼쪽 바는 초록 일부+빨강 나머지.
- `native_offset1080/`: 같은 원점에서1081회 run. 적 HP0(빨강), 아군5000. 왼쪽 바는 빨강, 오른쪽 초록은 유지.

각 폴더에 `source.state`, `both_screens.png`, `physical_lower_native.png`, 8개 BG층 PNG/NPZ, 레지스터, lower OAM 원본, HUD 타일계약이 있습니다. 최종 비교는 `two_moment_native_hud_comparison.png`입니다. 스크립트는 `test_current/parts/borrowed_shape_rework/capture_subscreen_hp_native_private.py`이며 중앙 코드가 아닙니다.

중간 `native_offset1060`은 채움/수치 변경 중이라 GPU가 표시한 native 숫자872와 run 뒤 MMU에서 읽은 BG 숫자828이 달랐습니다. 이를 정확한 동일프레임 계약으로 사용하지 않았습니다. 이 위험을 숨기지 않고 `stable_fixture_contract.json`에 기록했고 최종 자료는0/1080의 안정 시점만 사용합니다.

## 레이어와 위치

이 장면의 물리 아래 화면은 엔진1입니다. OBJ가 아닌 **엔진1 BG0**에 노란 HP 글자, 수치, 초록/빨강 바가 있습니다. **BG1**에는 빨강/파랑 이름 판과 청록 수치 판 프레임이 있습니다. BG0는4bpp, BG0CNT=0x0004, map VRAM=0x06200000, char VRAM=0x06204000입니다. 두 BG의 스크롤은0입니다. BG0/BG1만 임의로 합친 HD 결과가 아니라, 원래 BG3→2→1→0을 원본 타일로 조립해 비교했습니다. 두 시점의 HUD5120픽셀 모두 DS5비트 색으로 환산하면 native와 일치했고, 8비트 복원 방식에 따른 최대 채널 차이는2입니다(`BG_only_HUD_pixel_evidence.json`). 이 자료는 HUD 원천 분류 근거이며 HD 품질 판정이 아닙니다.

| 역할 | 물리 아래 화면 원본 좌표 x,y,w,h |
| --- | --- |
| 왼쪽 이름 판 | 48,80,80,16 |
| 오른쪽 이름 판 | 128,80,80,16 |
| 왼쪽 노랑 HP 실제 불투명 bbox | 53,98,14,6 |
| 오른쪽 노랑 HP 실제 불투명 bbox | 133,98,14,6 |
| 왼쪽 수치 가변 칸 | 88,96,32,8 |
| 오른쪽 수치 가변 칸 | 168,96,32,8 |
| 왼쪽 바 실제 bbox | 53,104,70,5 |
| 오른쪽 바 실제 bbox | 133,104,70,5 |

`hud_source_regions.json`, `glyph_and_bar_geometry.json`에 원본 좌표와 실제 y106의 색 구간을 보존했습니다. 적 HP1308 시점 y106에서 x55..71은초록17픽셀, x72..121은빨강50픽셀입니다. HP0 때 x55..121은빨강67픽셀로 바뀝니다. 아군 바의 x135..201 초록67픽셀은 두 시점 동일합니다. 끝단 테두리도 별도 색입니다.

## 실제 ROM 원천

`HP_label_and_bar_source_contract.json`에 타일별 원본 바이트/SHA·원래 화면 위치·ROM 후보 좌표를 모았습니다.

- **IMG4651**, 4bpp256×24. 원본 HP 라벨 타일52/53, 뒤쪽 조각54, 바 타일1/9/65/66/69/70 등의32바이트가 ROM의 타일 경계와 정확히 일치합니다. 복제된 같은 타일이 있을 때는 후보를 둘 다 보존했습니다.
- HP 라벨은 IMG4651의 [160,8,24,8] 원본 타일 영역(52..54)에 해당합니다. 실제 화면 불투명 글자는 앞의14×6이며 타일 캔버스24×8 전체를 글자폭으로 착각하면 안 됩니다.
- **PLT4650**, 총48색. 라벨/바는bank0을 사용합니다. 실제16색은 ROM bank0과 index0만 198→0으로 달라졌고, index1..15는 일치합니다. 원본의0번은 투명 인덱스이므로 실제 runtime 전체팔레트도 계약에 보존했습니다. 숫자 노랑/빨강 bank1/2는 ROM 전체16색과 일치합니다.
- **SCR 단일 소유는 미확정**입니다. HUD BG0 map은 숫자와 부분 채움에 맞춰 갱신되고, 현재 메모리 타일맵은 각 시점 NPZ/계약으로 보존했습니다. 인접 리소스 번호만 보고 SCR 소유를 추정하지 않았습니다.

`rom_tile_and_palette_candidates.json`은 후보 원천 상세, `ROM_IMG4651_indices.npy`/`ROM_PLT4650_raw.bin`은 읽은 ROM 원천, `IMG4651_actual_bank0_4x.png`는 실제 runtime bank0로 보이는 원본 참고입니다. 이 그림은 HD 후보가 아닙니다.

## 연결 시 지켜야 할 것

HP 라벨/바 틀/끝단 소재와 숫자·채움은 분리해야 합니다. HP1308/0/5000 같은 수치를 정적 이미지에 구우면 안 됩니다. 숫자 색은 노랑→빨강으로 바뀌고, bar는 BG0 map의 부분 채움 타일9→1 및 끝단65→69처럼 갱신됩니다(`two_moment_tile_changes.json`). 전체 바를 한 그림으로 덮어 현재 채움 비율을 고정하지 않아야 합니다.

원본은 **EN이 없는 HP-only 보조화면**입니다. 그러므로 HD 글자 경로가 HP+EN 동일줄만 인식한다면 이 화면을 빠뜨릴 수 있다는 root의 코드 조사와 일치하는 별도 원천 근거가 됩니다. 다만 이 패킷에서는 그 코드를 실행해 HD 수정 유효성을 검증하지 않았습니다. Claude가 HP-only 라벨/숫자/바 및 물리 아래 화면 경로를 연결하고 판정할 자료입니다.
