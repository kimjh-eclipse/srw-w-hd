# 컷인 페이드·단색 플래시 공통 원인 검토

## 결론

읽기 전용 검토다. 공유 런타임·DLL·라이브러리·DB를 수정하지 않았다. 서로 다른 두 누락을 확인했다.

1. **겟타와 고라이온 캐릭터 컷인의 자기 페이드 계수가 HD 그림에 적용되지 않는다.** 기존 foreground_blend는 앞 BG 색이 뒤 HD 그림에 섞이는 경우만 처리한다. 컷인 자신의 첫대상 BG 계수는 계산하지 않는다.
2. **unit333의 주황/하늘 단색 플래시는 관측값상 MASTER_BRIGHT/BLDY가 아니라 윈도우의 레이어 허용 비트를 무시하는 문제다.** 게임이 상단에서 기체·BG1/2/3을 끄지만, HD 합성기는 그 빈 backdrop 위치를 가림 없는 영역으로 해석해 그림을 다시 올린다.

전체 그림을 밝게/어둡게 하는 임시 보정이나 컷인 그림 자체의 알파를 수정하면 원래 다른 프레임이 깨진다. 프레임별 실제 하드웨어 상태를 합성에 적용해야 한다.

## 실제 비교 근거

### 겟타

- 상태: `test_current/combat/getter_cutin.state`, offset30.
- 진짜 원본/HD 쌍: `test_current/combat/runtime_path/getter_head_v4_final/getter_cutin_pure_pair_30.png`.
- 순수 원본에서 료마 컷인은 배경이 비칠 만큼 흐려졌지만 HD 컷인은 불투명이다. 직접 시각 확인.
- 컷인90, BG1, priority1, cutin_layers row7(master)=0, row9~11=0. 별도 cutin alpha 필드는 없다.
- 프레임 종료 레지스터 BLDCNT=0x3c42: 첫대상 BG1, 모드 alpha, 두번째대상 BG2/BG3/OBJ/backdrop. BLDALPHA EVA8/EVB8, BLDY0, MASTER0.
- 같은 렌더 프레임에서 수집한 실제 foreground 래스터 계수는 (EVA9,EVB7)와 (4,16)이다. **프레임 종료 레지스터 값과 래스터 값이 다르므로 끝의8/8만 복사하면 정확한 수정이 아니다.**

### 고라이온

- 상태: `test_current/combat/golion_cutin.state`, offset0.
- 별도 실제 재생: `test_current/combat/runtime_path/golion_fade_readonly/golion_cutin_pure_pair_0.png`.
- 원본 코가네 컷인은 거의 사라질 정도로 희미하지만 HD는 진한 빨강·피부색의 불투명 컷인이다. 직접 시각 확인.
- 컷인107, BG1, priority1. BLDCNT0x3c42, 종료EVA1/EVB15, 래스터실제(2,14)·(1,16), BLDY0/MASTER0. 겟타와 같은 자기 첫대상 alpha 경로다.
- offset10에는 컷인 메타데이터 자체가 사라진다. 이후 정상 소실이 앞선 불투명 페이드 오류를 없애 주지는 않는다.

### 합체 컷인 대조군

- unit297 / weapon1213 / frame_300.state, offset0~90.
- 컷인171/172/173, BG1/2에 순차 등장. 종료EVA16/EVB0, 실제foreground도16/0. 순수 원본과 HD가 모두 불투명인 것이 정상이다.
- 따라서 모든 컷인을 고정50%로 투명하게 만드는 수정은 틀리다.

### unit333 단색 플래시

- 상태: `test_current/combat/named_attacks/unit_333/diagnostic_preview/mechanical_cutin_168.state`.
- 직접 확인: `test_current/combat/runtime_path/effect19645_final/mechanical_cutin_168_pure_pair_28.png`, `_32.png`.
- +28 순수 원본 상단 주황, +32 하늘색 단색. HD는 구름·기체·충격광을 계속 그린다. 아래 대사창은 원본에 남아야 하며 플래시에서 보호된다.
- 모든 탐색 프레임 BLDY0, MASTER_BRIGHT0. 이 사례를 전역 밝기 조절이라고 단정하면 안 된다.
- DISPCNT=0x10017f00. WIN0H=0x0080, WIN1H=0x8000, WIN0V/WIN1V=0x0080: 상단0~128행을 좌/우 두 윈도우가 덮는다.
- 보통 WININ=0x3f3f(전부 허용). +28/+30에는 **0x2121**: 두 윈도우 안에서 BG0와 색효과만 허용, **BG1/2/3/OBJ 금지**. 하단 밖 WINOUT=0x23 유지.
- +28 backdrop BGR555=351은 R31/G10/B0(주황), +30은32448(하늘 계열). HD 원본 입력의 상단32768픽셀 중31946개가 layer ID5(backdrop),822개가BG0(크리티컬 글자)인 것도 배경·기체를 숨기는 동작과 일치한다.
- +32 종료WININ은이미0x3f3f로 복구됐지만, 같은 표시 프레임의 순수 원본은 하늘 플래시다. 코어가 프레임을 그린 시점과 마지막CPU 레지스터 상태가 달라질 수 있다. **래스터 시점 윈도우 허용 마스크를 내보내야 한다.**
- BG2 메카컷인168과 BG3 배경의 맵CRC·팔레트 뱅크는 플래시 전후 그대로다. 그림/타일 해시만 보고 존재를 판단하면 윈도우로 감춘 그림이 여전히 유효하다고 나온다.

## 코드 근거와 최소 수정 위치

### 컷인 자기 alpha

- `GPU.cpp` 179~183: SRWWHD_Layers에는 id/scroll/size/layer/priority/master/base만 저장. master 이외의 자기 BLDCNT/EVA/EVB/BLDY는 없다.
- `GPU.cpp` 4292~4299: SRWWForeground는 실제 래스터에서 첫대상 BG의 색/EVA/EVB/두번째대상/목적지 레이어를 기록한다.
- `foreground_blend.py` 30~42의 `_fast`,65~81의 `eligibility`: `front_priority < priority` 또는 더 앞 BG 번호만 허용한다. **같은 BG 자신의 페이드는 통과하지 않는다.** 이것은 앞 이펙트를 올리는 용도에는 맞다.
- `hd_renderer.py` 174~209 `draw_cutin`: 위 eligibility로 앞이펙트만 적용하고, 그림 고유 알파로 `top.draw(... alpha=True)` 또는 paste 한다. DS 자기 첫대상 색효과 계수는 적용하지 않는다.
- `gpu_surface.py` 셰이더39~41: 기존 foreground는 `HD*EVB + 앞native색*EVA` 경로다. 자기 컷인은 반대로 **그림*EVA + 뒤 대상*EVB**여야 한다.

제안: 자기 source-effect 데이터를 별도 경로로 기록/전달하고 `draw_cutin` 및 GPU 셰이더에 반영한다. 실제 래스터상 layer==cutin.layer이고 첫대상인 경우를 사용하되 원래 윈도우의 색효과 허용비트와 두번째대상 자격도 적용한다. 그림의 매끄러운 고유알파는 보존한다. EVA+EVB가16이 아닌 가산식도 있으므로 단순 alpha=EVA/16은 완전한 식이 아니다. 뒤 대상의 HD/원본 면을 확보해 원래 DS 식으로 합성한다. 이미 혼합된 원본 컷인 위에 다시 혼합하면 이중 잔상이 생기므로 기존 컷인 원본을 제거/복원하는 경로도 함께 확인해야 한다.

### 윈도우 플래시

- `painted_edges.py` 42~53 `cutin_visibility`: 레이어 우선순위/OBJ 가림만 검사. backdrop ID5는 차단하지 않는다. **윈도우가 그 레이어를 금지했는지** 알 수 없다.
- `hd_parts.py` 650 compose와 각 배경 합성 경로에도 실제 윈도우 허용 마스크가 전달되지 않는다. 컷인만 고치면 구름·기체가 플래시를 계속 덮는다.
- 코어에는 `GPU.h`의 `_didPassWindowTestNative[5][256]`, `_enableColorEffectNative[5][256]`가 이미 있다. 한 행용 상태이므로 그릴 때192행 마스크에 기록하는 export가 최소 공통 확장이다. 레이어별 허용 비트와 색효과 허용 비트를 기록해 BG0~3/OBJ 모든 HD draw에 적용한다.
- 레이어 ID는 실제 최종색을 차지한 레이어만 나타내며, 투명 픽셀과 윈도우 금지를 구별하지 못한다. `layer_ids==5`를 일괄 차단하면 원래 실루엣 밖 매끄러운 HD 외곽선을 자르므로 금지.
- 임시로 단색 화면을 인식해 덮는 휴리스틱 대신 하드웨어 윈도우 상태를 사용한다. 아래 대사창은 원래 윈도우 밖이므로 유지해야 한다.

### BLDY와 MASTER는 별도 미검증 범위

이번 네 상태에서는 모두0이었다. Python 런타임에 BLDCNT/BLDY/MASTER_BRIGHT 처리 코드는 검색되지 않았고 cutin row7 master도 draw에서 읽지 않는다. 따라서 비제로 장면에서는 별도 누락 가능성이 있지만 **이번 플래시 원인으로 측정된 것은 아니다.** 실제 비제로 상태를 확보한 뒤 source별 밝기증감과 최종 MASTER 후처리를 래스터 행별로 분리 검증해야 한다.

## 산출물과 재현

- `raster_probe.json`: 네 상태 각91프레임 중0/10/20/28/30/32/40/60/90의 원시 레지스터,cutin rows,실제foreground계수,윈도우,맵CRC·팔레트뱅크·색/레이어통계.
- `probe.py`, `probe.log`: Core 읽기 전용 수집. `retro_srw_copy_effect_debug`를 사용하며 코어를 바꾸지 않았다.
- `golion_replay.log`: 30프레임 실제재생 명령 결과. 다른 두 주요 비교는 머리v4/효과19645 검사에서 만들어진 순수원본 쌍을 재사용했다.
- 수정 후 최소 회귀: getter30/32, golion0~5의 투명도; trio0~150의불투명함; unit333+28/+32상단단색과하단UI; 창 경계 밖 HD 외곽선; BG효과/OBJ 앞뒤순서. 실제 래스터 계수와 최종레지스터가 다름을 반드시 고려한다.
