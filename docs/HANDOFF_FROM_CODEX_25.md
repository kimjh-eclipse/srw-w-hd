# Codex → Claude 25 — 새 화풍 재작화 전달 현황

파일 집계 시점: **2026-11-15 20:08:16 KST**.

**표준 경로 새 후보 18판 + 별도 대체 배치 후보 1판 = 대상19판의 새작화 자료 19판 전달을 확인했습니다.** 이 숫자는 실제 파일 존재 집계이며 사용자 승인·Claude 검수 합격·정합/형태 통과·설치/실재생 완료 수가 아닙니다.

이전 사용자 반려와 분담은 [24번 인계](HANDOFF_FROM_CODEX_24.md), 상세 화풍 원칙은 [ROBOT_ART_STYLE_DEATHSCYTHE.md](ROBOT_ART_STYLE_DEATHSCYTHE.md)를 확인해 주십시오.

## 집계 방법

- 대상은 unit5 / 100 / 102 / 103 / 104 / 105 / 106의 공식 SHEETS 총19판입니다. unit101의 공유 근거는 별도이며 신규 생성 수에 넣지 않습니다.
- 각 공식 장의 candidate_sheet.png를 표준 후보로 셌습니다. 이전 스타일/얼굴 반려 보존본은 제외했습니다.
- unit104 sheet03은 표준 후보가 없습니다. 공식 비율에 맞지 않은 넓은 RAW는 제외하고, 별도2×2 대체 후보를 정확히1판으로 따로 셌습니다.
- unit102 sheet02의 현재 후보 원출력은 generated_sheet_cleanup_raw.png입니다. 편집 전 generated_sheet.png와 과거 보류 RAW도 보존돼 있으며 현재 후보의 RAW와 구분합니다.
- 원출력과 후보의 실제 크기·SHA256·HANDOFF 경로만 읽었습니다. 그림의 정합·형태·실루엣·화풍 품질을 검증하지 않았고 이미지 생성·수정·설치·중앙 런타임 변경도 하지 않았습니다. 후보가 전체 캔버스 크기 변경본인 경우에도 원출력 자체를 별도로 표기했습니다.

## 표준 경로 현황

| 기체 | 판 / 항목 수 | 공통 기본 자세 | 새 표준 후보 | 현재 후보 원출력 크기 | 후보 크기 | 해당 판 인계 |
|---|---|---|---|---|---|---|
| 5 | sheet_01 / 9 | pose_09 | [있음](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_5/robot_set/SHEETS/sheet_01/candidate_sheet.png) | [1358×1159](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_5/robot_set/SHEETS/sheet_01/generated_sheet.png) | 1358×1159 | [HANDOFF](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_5/robot_set/SHEETS/sheet_01/HANDOFF.md) |
| 5 | sheet_02 / 9 | pose_09 | [있음](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_5/robot_set/SHEETS/sheet_02/candidate_sheet.png) | [1388×1133](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_5/robot_set/SHEETS/sheet_02/generated_sheet.png) | 1388×1133 | [HANDOFF](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_5/robot_set/SHEETS/sheet_02/HANDOFF.md) |
| 5 | sheet_03 / 8 | pose_09 | [있음](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_5/robot_set/SHEETS/sheet_03/candidate_sheet.png) | [1351×1164](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_5/robot_set/SHEETS/sheet_03/generated_sheet.png) | 1351×1164 | [HANDOFF](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_5/robot_set/SHEETS/sheet_03/HANDOFF.md) |
| 100 | sheet_01 / 9 | pose_03 | [있음](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_100/robot_set/SHEETS/sheet_01/candidate_sheet.png) | [1261×1247](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_100/robot_set/SHEETS/sheet_01/generated_sheet.png) | 1261×1247 | [HANDOFF](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_100/robot_set/SHEETS/sheet_01/HANDOFF.md) |
| 102 | sheet_01 / 9 | pose_03 | [있음](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_102/robot_set/SHEETS/sheet_01/candidate_sheet.png) | [1297×1212](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_102/robot_set/SHEETS/sheet_01/generated_sheet.png) | 1297×1212 | [HANDOFF](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_102/robot_set/SHEETS/sheet_01/HANDOFF.md) |
| 102 | sheet_02 / 7 | pose_03 | [있음](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_102/robot_set/SHEETS/sheet_02/candidate_sheet.png) | [1328×1184](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_102/robot_set/SHEETS/sheet_02/generated_sheet_cleanup_raw.png) | 1328×1184 | [HANDOFF](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_102/robot_set/SHEETS/sheet_02/HANDOFF.md) |
| 103 | sheet_01 / 9 | pose_11 | [있음](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_103/robot_set/SHEETS/sheet_01/candidate_sheet.png) | [1285×1224](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_103/robot_set/SHEETS/sheet_01/generated_sheet.png) | 1285×1224 | [HANDOFF](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_103/robot_set/SHEETS/sheet_01/HANDOFF.md) |
| 103 | sheet_02 / 6 | pose_11 | [있음](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_103/robot_set/SHEETS/sheet_02/candidate_sheet.png) | [1532×1026](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_103/robot_set/SHEETS/sheet_02/generated_sheet.png) | 1532×1026 | [HANDOFF](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_103/robot_set/SHEETS/sheet_02/HANDOFF.md) |
| 104 | sheet_01 / 9 | pose_06 | [있음](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_104/robot_set/SHEETS/sheet_01/candidate_sheet.png) | [1435×1096](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_104/robot_set/SHEETS/sheet_01/generated_sheet.png) | 1435×1096 | [HANDOFF](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_104/robot_set/SHEETS/sheet_01/HANDOFF.md) |
| 104 | sheet_02 / 9 | pose_06 | [있음](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_104/robot_set/SHEETS/sheet_02/candidate_sheet.png) | [1383×1137](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_104/robot_set/SHEETS/sheet_02/generated_sheet.png) | 1383×1137 | [HANDOFF](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_104/robot_set/SHEETS/sheet_02/HANDOFF.md) |
| 104 | sheet_03 / 3 | pose_06 | 없음 · 아래 대체 후보 | [2172×724 · 비율 보류](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_104/robot_set/SHEETS/sheet_03/generated_sheet_wide_style_v2.png) | — | [HANDOFF](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_104/robot_set/SHEETS/sheet_03/HANDOFF.md) |
| 105 | sheet_01 / 9 | pose_10 | [있음](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_105/robot_set/SHEETS/sheet_01/candidate_sheet.png) | [1593×987](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_105/robot_set/SHEETS/sheet_01/generated_sheet.png) | 2280×1412 | [HANDOFF](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_105/robot_set/SHEETS/sheet_01/HANDOFF.md) |
| 105 | sheet_02 / 9 | pose_10 | [있음](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_105/robot_set/SHEETS/sheet_02/candidate_sheet.png) | [1373×1146](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_105/robot_set/SHEETS/sheet_02/generated_sheet.png) | 1868×1560 | [HANDOFF](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_105/robot_set/SHEETS/sheet_02/HANDOFF.md) |
| 105 | sheet_03 / 9 | pose_10 | [있음](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_105/robot_set/SHEETS/sheet_03/candidate_sheet.png) | [1608×978](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_105/robot_set/SHEETS/sheet_03/generated_sheet.png) | 2184×1328 | [HANDOFF](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_105/robot_set/SHEETS/sheet_03/HANDOFF.md) |
| 105 | sheet_04 / 4 | pose_10 | [있음](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_105/robot_set/SHEETS/sheet_04/candidate_sheet.png) | [1771×888](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_105/robot_set/SHEETS/sheet_04/generated_sheet.png) | 1684×844 | [HANDOFF](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_105/robot_set/SHEETS/sheet_04/HANDOFF.md) |
| 106 | sheet_01 / 9 | pose_24 | [있음](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_106/robot_set/SHEETS/sheet_01/candidate_sheet.png) | [1372×1146](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_106/robot_set/SHEETS/sheet_01/generated_sheet.png) | 1600×1336 | [HANDOFF](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_106/robot_set/SHEETS/sheet_01/HANDOFF.md) |
| 106 | sheet_02 / 9 | pose_24 | [있음](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_106/robot_set/SHEETS/sheet_02/candidate_sheet.png) | [1330×1182](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_106/robot_set/SHEETS/sheet_02/generated_sheet.png) | 1476×1312 | [HANDOFF](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_106/robot_set/SHEETS/sheet_02/HANDOFF.md) |
| 106 | sheet_03 / 9 | pose_24 | [있음](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_106/robot_set/SHEETS/sheet_03/candidate_sheet.png) | [1376×1143](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_106/robot_set/SHEETS/sheet_03/generated_sheet.png) | 1580×1312 | [HANDOFF](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_106/robot_set/SHEETS/sheet_03/HANDOFF.md) |
| 106 | sheet_04 / 2 | pose_24 | [있음](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_106/robot_set/SHEETS/sheet_04/candidate_sheet.png) | [1979×795](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_106/robot_set/SHEETS/sheet_04/generated_sheet.png) | 1056×424 | [HANDOFF](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_106/robot_set/SHEETS/sheet_04/HANDOFF.md) |

공통 위치: C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_<번호>/robot_set/SHEETS/sheet_NN/. HANDOFF 링크는 실제 파일 존재 확인이며, 검수 판정이 아닙니다.

## unit104 sheet03 — 별도 대체 배치 후보1판

- [대체 후보](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_104/robot_set/SHEETS/sheet_03/candidate_sheet_alt_2x2.png): **1354×1162**.
- [대체 원출력 RAW](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_104/robot_set/SHEETS/sheet_03/generated_sheet_alt_2x2.png): **1354×1162**. 후보와 RAW의 바이트 SHA 일치: 일치.
- [대체 원본 입력](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_104/robot_set/SHEETS/sheet_03/native_sheet_alt_2x2.png): **904×776**. 적용할 좌표는 [layout_alt_2x2.json](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_104/robot_set/SHEETS/sheet_03/layout_alt_2x2.json)입니다.
- [해당 HANDOFF](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_104/robot_set/SHEETS/sheet_03/HANDOFF.md)에 원본3자세와 기본 pose06, 대체 배치 인계 이유가 기록돼 있습니다.

공식 입력1404×436과 공식 layout.json은 보존됐습니다. 공식 배치용 넓은 출력2172×724는 비율 불일치로 generated_sheet_wide_style_v2.png에만 남겼으며 표준 후보에 넣지 않았습니다.

**대체 그림에 공식 layout.json을 그대로 적용하면 안 됩니다.** Claude가 별도2×2 배치와 layout_alt_2x2.json을 채택한 뒤 정합·분할해야 합니다. 대체 후보 존재는 배치 채택·정합·설치 통과를 뜻하지 않습니다.

## unit102 sheet02 — 배경제거 편집 전달과 담당자 정정

[최신 HANDOFF](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_102/robot_set/SHEETS/sheet_02/HANDOFF.md)와 [편집 프롬프트/메타데이터](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_102/robot_set/SHEETS/sheet_02/cleanup_prompt.json)에 따르면 담당자가 마지막 보류 RAW 한 장을 참조해 내장 도구 배경제거 편집을1회 수행했습니다. 현재 [후보](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_102/robot_set/SHEETS/sheet_02/candidate_sheet.png)와 [편집 RAW](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_102/robot_set/SHEETS/sheet_02/generated_sheet_cleanup_raw.png)는 1328×1184이며, 바이트 SHA는 일치합니다. 코드로 알파/RGB를 고치거나 원본 마스크·재색칠·분할을 적용하지 않았다는 담당 기록이 있습니다.

**담당자 정정:** 도구 미리보기에서 보였던 회갈색은 실제 alpha0 투명 영역에 남은 RGB였다는 보고입니다. 실제 알파를 적용한 흰/검정 배경 검토 렌더링에서는7기체와 넓은 후광이 없는 상태를 확인했다고 HANDOFF를 정정했습니다. 미리보기의 투명 영역 RGB만으로 불투명 배경 실패라고 단정했던 이전 기록과 구분해 주십시오. REVIEW_ONLY_cleanup_on_white.png / REVIEW_ONLY_cleanup_on_black.png는 검토용 렌더링이며 후보가 아닙니다.

이 문서 작성자는 해당 그림의 형태·정합·알파 화면을 새로 검증하지 않았습니다. 작은 선/채색·형상 소실, 두 손/팔 중복 해석 의심, 원본 정합은 여전히 미검수라는 담당 기록을 유지합니다. **그 밖의 과거 보류 RAW 상태는 이번에 재판정하지 않았습니다.**

## 첫 판과 얼굴 수정의 파일 식별

- unit5 sheet01의 현재 새 후보는 가운데 pose03 얼굴을 수정한 **1f4e616a**입니다. 이전4bbc30bf는 generated_sheet_face_rejected_v2.png로 보존됐습니다. 파일 SHA 식별: 1f4e616a=일치, 4bbc30bf=일치.
- unit104 sheet01의 현재 새 후보는 **e68d01dc**입니다. 파일 SHA 식별: e68d01dc=일치.
- 이는 생성 파일과 프로젝트 파일의 식별 확인입니다. 얼굴 수정 적합성·다른8자세 영향·화풍 승인이나 설치 판정이 아닙니다.

## unit101 공유 근거 — 신규 생성 수에 미포함

[unit101 SOURCE_IDENTITY.json](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_101/robot_set/SHEETS/SOURCE_IDENTITY.json)에 unit100과 unit101 전체9자세의 PNG SHA·RGBA·크기·순서 동일 근거가 있습니다. 공유 대상은 [unit100 이번 새 후보](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_100/robot_set/SHEETS/sheet_01/candidate_sheet.png)입니다. 다른 팔레트 그림을 재색칠하거나 unit101을 별도 생성한 것으로 세지 않습니다. 공유 근거와 새 그림 검수·바인딩·설치 상태는 구분합니다.

## 유지할 참조와 후속 검수

[사용자가 언급한 데스사이즈 실물](C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_1/robot_set/pose_00/generated.png)을 매 호출의 직접 화풍 참조로 쓰고, 후속 판에는 같은 기체의 **이번 새 첫 판**도 참조합니다. 사용자가 언급한 실물 참조이며 이번 새 후보의 사용자 최종 승인을 뜻하지 않습니다. 한 판 최대9자세·첫 칸 공통 base_pose, 원본 실제색/위치/크기/겹침/실루엣과 검정/흰 실루엣·효과·부분 조각·구멍을 유지하며 도구 RAW와 실제 프롬프트를 보존합니다. 상세 원칙은 [화풍 지침](ROBOT_ART_STYLE_DEATHSCYTHE.md)을 따릅니다.

얼굴/바이저·마스크·턱, 손발·몸통·어깨·무장과 접합, 원본색, 효과 개수/길이/틈, 배치/실루엣/알파 경계, 장 사이 기본 자세/설계·화풍 일관성은 Claude가 확인할 항목입니다. unit5 가운데 얼굴 수정 영향과 unit102 편집 후 작은 선·형상 유지, unit104 대체 배치 선택도 해당 HANDOFF를 기준으로 확인해 주십시오.

## 파일 식별 SHA256 전체

다음 경로는 위 공통 SHEETS 위치의 기체/판을 줄여 표기했습니다. SHA는 그림 품질 판정에 사용하지 않았습니다.

~~~text
unit5/sheet_01/candidate_sheet.png
  SHA256 546813c4b7c0605d2048b5f83f19e253cea32ea1f2b1b23057b195515841fb74
unit5/sheet_01/generated_sheet.png
  SHA256 546813c4b7c0605d2048b5f83f19e253cea32ea1f2b1b23057b195515841fb74
unit5/sheet_02/candidate_sheet.png
  SHA256 85cf2e6c387b8f65f45e877bc00cdc63b710e3fb699a20b6c3bc1dbbacb3ffd3
unit5/sheet_02/generated_sheet.png
  SHA256 85cf2e6c387b8f65f45e877bc00cdc63b710e3fb699a20b6c3bc1dbbacb3ffd3
unit5/sheet_03/candidate_sheet.png
  SHA256 493a01383bf2b8a2a6655ba746d6f81115b7c8a97a1bcb851a18e0feb2ecc5aa
unit5/sheet_03/generated_sheet.png
  SHA256 493a01383bf2b8a2a6655ba746d6f81115b7c8a97a1bcb851a18e0feb2ecc5aa
unit100/sheet_01/candidate_sheet.png
  SHA256 b6decbe372d617991e4a911aa03f88bd680249a97e68180659010a943cff6f1f
unit100/sheet_01/generated_sheet.png
  SHA256 b6decbe372d617991e4a911aa03f88bd680249a97e68180659010a943cff6f1f
unit102/sheet_01/candidate_sheet.png
  SHA256 06f864ec585f26111bd53e3044c2e87648fc4c6bd2fee5398fc57233e3c7588a
unit102/sheet_01/generated_sheet.png
  SHA256 06f864ec585f26111bd53e3044c2e87648fc4c6bd2fee5398fc57233e3c7588a
unit102/sheet_02/candidate_sheet.png
  SHA256 54099ce6193187852f9c79ddc9d1b430868451ab87e822e37ebb356ab5eaa079
unit102/sheet_02/generated_sheet_cleanup_raw.png
  SHA256 54099ce6193187852f9c79ddc9d1b430868451ab87e822e37ebb356ab5eaa079
unit103/sheet_01/candidate_sheet.png
  SHA256 de331eb40fe4084b376abd1fe596e42c0bd1e5800d199f6deed63a13e5a137f2
unit103/sheet_01/generated_sheet.png
  SHA256 de331eb40fe4084b376abd1fe596e42c0bd1e5800d199f6deed63a13e5a137f2
unit103/sheet_02/candidate_sheet.png
  SHA256 d8d0bb2df12722bb32874f731163f8ca26554741ff2acbecbcd28fbd9975124e
unit103/sheet_02/generated_sheet.png
  SHA256 d8d0bb2df12722bb32874f731163f8ca26554741ff2acbecbcd28fbd9975124e
unit104/sheet_01/candidate_sheet.png
  SHA256 2d2f9beaa6a03639518916ee33a4eb84af81e24538d9589a29111e0ddf5acb17
unit104/sheet_01/generated_sheet.png
  SHA256 2d2f9beaa6a03639518916ee33a4eb84af81e24538d9589a29111e0ddf5acb17
unit104/sheet_02/candidate_sheet.png
  SHA256 4ce9324bc6890cdf8046b07e32dfb81f71cde37d52fe1d9b70b30ff9fd8f2af8
unit104/sheet_02/generated_sheet.png
  SHA256 4ce9324bc6890cdf8046b07e32dfb81f71cde37d52fe1d9b70b30ff9fd8f2af8
unit104/sheet_03/generated_sheet_wide_style_v2.png
  SHA256 04ae30985ffa5a6f1c5fb6dd6581cf1d7691c4cc219f722074a649f416f75259
unit105/sheet_01/candidate_sheet.png
  SHA256 166fe5db41be4ef8c23e9832a5e723684dcae45aac602e803095f858bf35b00c
unit105/sheet_01/generated_sheet.png
  SHA256 281820960a94cd73dcaf534de719925fe6d6b2668426a209cdfcfd77b02e250d
unit105/sheet_02/candidate_sheet.png
  SHA256 dceac33378272b98b0cad365205122745d5c33fb96d2555717170ca20378a023
unit105/sheet_02/generated_sheet.png
  SHA256 681b698cf8392823c36a46e4f02d6b2c7ebadc8014023acc0554c99a35026efc
unit105/sheet_03/candidate_sheet.png
  SHA256 6a60c2562a2e77026951933d0c1da647590392217d27c95f916b7d92c2b3f549
unit105/sheet_03/generated_sheet.png
  SHA256 acc9d7f23398b0112a5088e50d66afd326ac76ac41f3256a6ec426b51ed66449
unit105/sheet_04/candidate_sheet.png
  SHA256 573317feab43849a7439bb94c47b58500b597d27a47556cc96dc3494eda5d2a7
unit105/sheet_04/generated_sheet.png
  SHA256 22defbe229f571c1fbb045e295bebbf223bf9586231025bfa31bcbf1d72d9ca3
unit106/sheet_01/candidate_sheet.png
  SHA256 24367ac2ca41fae26020c026535f3e5f868b28a2371693a6a85f97a44e29a24e
unit106/sheet_01/generated_sheet.png
  SHA256 35d553d4d976a3c6d506b774eee50faf71d2130ec2a2e033bdbb37a1118aa254
unit106/sheet_02/candidate_sheet.png
  SHA256 7c4938e4096ddd9d5408c9387ce430304c60aafa0ea889f3353d9e2d012a8bca
unit106/sheet_02/generated_sheet.png
  SHA256 1a8ef9edd546d78573c10d825d77da4ed9fe050816ff9cc80cb9cec0a68ca342
unit106/sheet_03/candidate_sheet.png
  SHA256 7a51947ea002aea96d4924d547652a51382ca14963ff89b095d89a0f7af78b51
unit106/sheet_03/generated_sheet.png
  SHA256 eb265201c38b85fcdbc7eacc28315cd28c7cdbe6c208b78dc9e1cb47ab71c85c
unit106/sheet_04/candidate_sheet.png
  SHA256 c22b130c885183e195ba0a1fd454d9c059adb3f47c4b94420828cbf05efbd56b
unit106/sheet_04/generated_sheet.png
  SHA256 533fd677e6c75ed47ad4d64cfb795c162380ae105100ac692fe4fd9a1f53ed70
unit104/sheet_03/candidate_sheet_alt_2x2.png
  SHA256 c0a9294368f91f93f22d13affd4d291eb2c027f422317c3217ac61339f298848
unit104/sheet_03/generated_sheet_alt_2x2.png
  SHA256 c0a9294368f91f93f22d13affd4d291eb2c027f422317c3217ac61339f298848
~~~

원본 자료·반려 보존본·도구 RAW를 유지합니다. **19판 자료 전달과 검수 합격·게임 설치/실재생 완료를 구분해 기록합니다.**
