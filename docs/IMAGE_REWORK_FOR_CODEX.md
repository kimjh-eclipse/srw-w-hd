# 코덱스 작업 요청: 이미지 재작업 목록

작성: Claude, 2026-11-11. 근거는 `scripts/verify/verify_runtime_path.py`의 실행 경로 재생 결과다(저장 상태 161개, 각 150프레임, 코어 = 기체 단위 원본 유지 10%).
이 문서는 그림 작업만 다룬다. 합성·코어 쪽 변경은 `docs/CLAUDE_REVIEW_RESULT.md`에 있다.

## 작업 규칙

1. 한 기체의 한 자세는 전 파츠를 한 번에 연결한다. 코어가 팔레트 슬롯 단위로 원본 면적이 10% 이상이면 그 기체를 통째로 원본으로 둔다. 일부 파츠만 연결하면 화면에는 아무것도 바뀌지 않는다.
2. 연결 후 `verify_runtime_path.py --units <id> --per-unit 99`를 돌려 그 장면이 `REVIEW`가 되는지 확인하고, 저장된 `*_last_*.png`를 직접 본다. `INCOMPLETE`가 남으면 완료가 아니다.
3. 기존 자산을 다른 기체에 재사용하거나 재색칠해서 채우지 않는다. 틀린 그림이 연결되면 이 검사로는 잡히지 않는다.
4. 등록 수·타일 일치 수를 완료 근거로 쓰지 않는다. 판정과 그림만 근거다.

## A. 원본으로 확인된 BG 그림 (OBJ 목록에 나오지 않음)

| 대상 | 소스 | 근거 |
|---|---|---|
| FDS 겟타 확대 몸통 (unit 297, weapon 1213, frame 1320) | BG2 = IMG 23382, 220타일, 원점 (0,128) | `test_current/combat/getter_chest_source_audit.log` |
| 같은 장면 에너지 효과 | BG1 = IMG 23393(14타일), IMG 23397(4타일) | 같은 로그 |
| 발호크 빔 효과 (unit 413, weapon 1613, frame 600) | BG1 = IMG 25822, 28타일, 원점 (0,32) | `test_current/combat/jade_effect_source_audit.log` |
| 가이 녹색 기체, 양 주먹 확대 장면 | 미조사. 확대 BG 이미지로 추정되므로 IMG/SCR/PLT부터 대조 | 사용자 제보 |
| 발호크 맥시멈 슈트 마지막 폭발(파란 폭발) | 미조사 | 사용자 제보 |

## B. 연결된 그림이 없는 OBJ 파츠

전체 650종. 상세는 `test_current/combat/runtime_path/regression/gaps.json`(화면 점유가 큰 순), 그림은 같은 폴더 `gaps.png`(앞 640종, 한 줄 16개, 순위 순, 원본 크기).
런타임 타일 조립이 실패한 파츠는 293종이다. 조립 실패분은 새 그림 없이는 HD가 되지 않는다.

기체별 요약 (장면의 HD 면적 비율이 낮은 순). 비율은 로딩이 끝난 뒤 화면의 HD 대 원본 OBJ 면적이다.

| unit | 이름 | 장면 수 | 최저 HD 비율 | 미연결 파츠 종 | 판정 |
|---|---|---|---|---|---|
| 292 | 진・겟타2 | 1 | 0.0 | 11 | INCOMPLETE |
| 293 | 진・겟타3 | 1 | 0.0 | 54 | INCOMPLETE |
| 256 | 테카맨 데드 | 1 | 0.039 | 10 | INCOMPLETE |
| 232 | 테카맨 대거 | 1 | 0.127 | 5 | INCOMPLETE |
| 299 | 그레이트 마징가 | 3 | 0.306 | 20 | INCOMPLETE/NO_HD_PARTS/REVIEW |
| 147 | 에스테바리스 공중 | 2 | 0.5 | 9 | INCOMPLETE |
| 297 | 마징카이저KS | 9 | 0.54 | 63 | INCOMPLETE/NO_HD_PARTS/REVIEW |
| 413 | 발호크 | 28 | 0.555 | 276 | INCOMPLETE/NO_HD_PARTS/REVIEW |
| 280 | 플랜1059 코다르c | 1 | 0.594 | 27 | INCOMPLETE |
| 148 | 에스테바리스 공중 | 2 | 0.624 | 9 | INCOMPLETE |
| 298 | 그레이트 마징가 | 2 | 0.625 | 13 | INCOMPLETE/REVIEW |
| 149 | 에스테바리스 공중 | 2 | 0.628 | 9 | INCOMPLETE |
| 254 | 이성인 테카맨 | 1 | 0.636 | 32 | INCOMPLETE |
| 390 | 천룡신 | 2 | 0.66 | 12 | INCOMPLETE/REVIEW |
| 214 | 랑그 | 2 | 0.696 | 37 | INCOMPLETE |
| 187 | 블랙 사레나 | 1 | 0.719 | 1 | INCOMPLETE |
| 226 | B테카맨 블레이드 | 4 | 0.732 | 28 | INCOMPLETE/NO_HD_PARTS |
| 386 | 가오파이가 | 1 | 0.739 | 0 | INCOMPLETE |
| 261 | M9 건즈벡 | 2 | 0.754 | 40 | INCOMPLETE |
| 141 | 에스테바리스 0G | 2 | 0.758 | 16 | INCOMPLETE |
| 249 | 테카맨 아키 | 3 | 0.777 | 43 | INCOMPLETE/NO_HD_PARTS |
| 265 | ARX-7 아바레스트 | 1 | 0.78 | 22 | INCOMPLETE |
| 481 | ARX-7 아바레스트 | 1 | 0.78 | 22 | INCOMPLETE |
| 225 | 테카맨 블레이드+P | 2 | 0.783 | 35 | INCOMPLETE |
| 250 | 테카맨 아키+PII | 3 | 0.784 | 56 | INCOMPLETE/NO_HD_PARTS |
| 227 | B테카맨 블레이드+P | 4 | 0.785 | 38 | INCOMPLETE/NO_HD_PARTS |
| 263 | ARX-7 아바레스트 | 1 | 0.785 | 22 | INCOMPLETE |
| 264 | ARX-7 아바레스트 | 1 | 0.785 | 22 | INCOMPLETE |
| 480 | ARX-7 아바레스트 | 1 | 0.785 | 22 | INCOMPLETE |
| 262 | M9 건즈벡 | 2 | 0.791 | 24 | INCOMPLETE/REVIEW |
| 153 | 에스테바리스 육지 | 2 | 0.809 | 15 | INCOMPLETE |
| 323 | 가오가이가 | 1 | 0.811 | 0 | INCOMPLETE |
| 395 | 폴턴 | 1 | 0.812 | 21 | INCOMPLETE |
| 486 | 폴턴 | 1 | 0.812 | 21 | INCOMPLETE |
| 333 | 볼포그 | 1 | 0.816 | 5 | INCOMPLETE |
| 365 | 볼포그 | 1 | 0.816 | 5 | INCOMPLETE |
| 377 | 볼포그 | 1 | 0.816 | 5 | INCOMPLETE |
| 224 | 테카맨 블레이드 | 1 | 0.826 | 25 | INCOMPLETE |
| 243 | 테카맨 이벨 | 2 | 0.836 | 10 | INCOMPLETE/NO_HD_PARTS |
| 417 | 발자카드 | 2 | 0.842 | 4 | INCOMPLETE/REVIEW |
| 42 | 소드 스트라이크 루즈 | 1 | 0.854 | 21 | INCOMPLETE |
| 155 | 에스테바리스 육지 | 2 | 0.857 | 14 | INCOMPLETE |
| 151 | 에스테바리스 육지 | 2 | 0.859 | 4 | INCOMPLETE/REVIEW |
| 19 | 소드 스트라이크 건담 | 1 | 0.865 | 21 | INCOMPLETE |
| 143 | 에스테바리스 0G | 2 | 0.874 | 12 | INCOMPLETE |
| 154 | 에스테바리스 육지 | 2 | 0.881 | 13 | INCOMPLETE |
| 375 | 환룡신 | 2 | 0.889 | 0 | INCOMPLETE/REVIEW |
| 373 | 초룡신 | 1 | 0.894 | 0 | INCOMPLETE |
| 142 | 에스테바리스 0G | 2 | 0.897 | 6 | INCOMPLETE |
| 145 | 에스테바리스 공중 | 2 | 0.902 | 4 | INCOMPLETE/REVIEW |
| 140 | 에스테바리스 0G | 2 | 0.912 | 4 | INCOMPLETE/REVIEW |
| 190 | 에스테바리스 커스텀 | 1 | 0.916 | 4 | INCOMPLETE |
| 48 | 저스티스 건담 | 1 | 0.919 | 11 | INCOMPLETE |
| 479 | 저스티스 건담 | 1 | 0.921 | 8 | INCOMPLETE |
| 152 | 에스테바리스 육지 | 2 | 0.923 | 2 | INCOMPLETE/REVIEW |
| 131 | 소드 카라미티 | 1 | 0.924 | 8 | INCOMPLETE |
| 136 | 소드 카라미티 | 1 | 0.924 | 8 | INCOMPLETE |
| 491 | 소드 카라미티 | 1 | 0.924 | 8 | INCOMPLETE |
| 144 | 에스테바리스 0G | 1 | 0.925 | 0 | INCOMPLETE |
| 156 | 에스테바리스 육지 | 1 | 0.928 | 1 | INCOMPLETE |
| 146 | 에스테바리스 공중 | 2 | 0.936 | 1 | INCOMPLETE/REVIEW |
| 139 | 에스테바리스 0G | 2 | 0.938 | 0 | INCOMPLETE/REVIEW |
| 324 | 스타 가오가이가 | 1 | 0.938 | 0 | INCOMPLETE |
| 150 | 에스테바리스 공중 | 1 | 0.941 | 0 | INCOMPLETE |
| 404 | 고라이온 | 1 | 0.961 | 14 | INCOMPLETE |
| 244 | 테카맨 이벨+γ호 | 2 | 0.971 | 8 | INCOMPLETE/NO_HD_PARTS |
| 245 | 테카맨 조마 | 2 | 0.976 | 6 | INCOMPLETE/NO_HD_PARTS |
| 247 | 테카맨 베스나 | 2 | 0.999 | 2 | NO_HD_PARTS/REVIEW |
| 246 | 테카맨 조마+β호 | 2 | 1.0 | 4 | NO_HD_PARTS/REVIEW |
| 248 | 테카맨 베스나+α호 | 2 | 1.0 | 0 | NO_HD_PARTS/REVIEW |

겟타·고라이온 컷인 저장 상태(`getter_cutin`, `golion_cutin`)도 INCOMPLETE다. 고라이온은 날개 파츠가 미연결이라 현재 기체 전체가 원본으로 나온다.

## C. 사람이 그림을 확인해야 하는 기체

측정 가능한 결함은 없었지만 그림이 맞는지는 확인되지 않았다: 99 파워드 레드, 215 조아 총사령관, 276 팔케, 294 마징가Z, 295 마징카이저, 311 지옥왕 고든, 361 가오가이가, 367 가오가이가, 368 스타 가오가이가, 374 격룡신, 376 강룡신, 414 발호크.

## D. 이 목록에 없는 것

- 저장 상태가 없는 무장. 보유한 상태는 161개이고 무장 기록은 1804개다. 나머지는 측정하지 않았다.
- 사용자 제보 중 저장 상태가 없는 장면: 그레이트 마징가 썬더 브레이크의 보조창 그림과 손·발 파츠 깨짐, FMP 기체들, 겟타 3(벤케이) 몸통, 아스테바리스 공격 자세, 블레이드 합체 공격의 무기·팔. 먼저 각 장면의 저장 상태를 `test_current/combat/named_attacks/unit_<id>/` 아래에 만들고 2번 규칙대로 돌린다.
- 연결은 됐지만 틀린 그림. 썬더 브레이크 파츠 깨짐과 블레이드 건은 이쪽일 가능성이 있다. 해당 파츠의 `index_hash`가 `SRWWIndexedBindings`(팔레트를 뺀 인덱스 해시, 먼저 등록된 것이 이김)로 다른 기체 그림에 묶였는지 확인한다.
