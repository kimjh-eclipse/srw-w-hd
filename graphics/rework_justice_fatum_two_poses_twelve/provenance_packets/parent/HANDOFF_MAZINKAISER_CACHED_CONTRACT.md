# 마징카이저 두 자세 — cachedOBJ 계약 정합 정정 보고

상태: **원본 입력 기계적 정합 확인만 완료**. 그림 품질·alpha 지원·레이어·실제HD 재생 판정은 Claude가 담당한다. 라이브/DB/그림은 변경하지 않았다.

## 추출 경로의 문제와 실제 결과

기존 두 capture는 `retro_srw_copy_obj_debug`의 프레임 말 MMU OAM/VRAM을 읽었다. 이 방법은 게임이 다음 프레임 자료를 업로드한 장면에서 실제 렌더와 달라질 수 있다. 코다르 +90에서 이 문제가 실제로 발생했으므로 마징카이저도 같은 방법을 믿지 않고 다시 제작 추출했다.

이번 자료는 `retro_srw_copy_cached_obj`의 원본 index/팔레트/hash와 `core.obj`의 실제 rendered OAM을 짝지었다. state는 `test_current/combat/named_attacks/unit_297/diagnostic_preview/weapon_1213_capture/frame_300.state`다. 공식 재생 검증 도구는 실행하지 않았다.

| 자세 | 실제 OAM / 고유RGB | 기존 계약과 차이 | 교체 대상 |
|---|---:|---|---|
| +179 |22 /20|없음|없음|
| +3 |20 /18|없음|없음|

## 행별로 확인한 값

두 자세 총42 OAM 모두 cached hash=core.parts actual hash, 캐시 크기=rendered OAM 크기다. 기존 계약과 RGB hash·index hash·압축 해제 index bytes·실제 BGR555 palette·가로세로·화면좌표·OAM attrs가 모두 같다. 원본 crop의 alpha와 불투명한 RGB도 완전히 같다(보이는 픽셀 최대 RGB 차이0). 완전 투명 픽셀의 숨은 RGB는 옛 decode가0, 새캐시가 palette0 색을 저장해 다를 수 있으나 alpha0이므로 제작 원본의 보이는 색 차이가 아니다.

따라서 phantom0 / 새 actual RGB0 / 교체 대상0이다. 기존에 생성하고 root가 반영한 그림은 유지한다. 원본 추출 방법의 위험이 이 두 fixture offset에서 실제 오류로 나타난 것은 아니었다.

## 파일

- `mazinkaiser179_cached_contract/cached_contract.json`:20종·22OAM의 캐시 정정 계약과 현재live binding.
- `mazinkaiser179_cached_contract/identity_comparison.json`:행별 원본/기존 계약 대조 및 native crop 색/alpha 결과.
- `mazinkaiser3_cached_contract/cached_contract.json`:18종·20OAM의 캐시 정정 계약과 현재live binding.
- `mazinkaiser3_cached_contract/identity_comparison.json`:행별 원본/기존 계약 대조.
- 각 폴더 `all_oam.json`, `cached_snapshot.npz`, `oam_N_native.png`, `actual_frame_native.png`는 원본 제작 추출 자료다.
- `CACHED_CONTRACT_CORRECTION_MAZINKAISER.json` 및 `.csv`:교체·phantom·실제정확대상 요약.

기존 후보 atlas SHA256은 +179 `0e423a8b10e46b598e219ffeefcbb85a4729848ed9c1e90701504deed56d628b`, +3 `79f3bb56eeb2268d39de23633c293ea2062435789a6c4ba78c5bf0b8e58108aa`이며 변경하지 않았다.

## Claude 큐에 유지할 것

+179 slot51의 alpha 지원 경고 .564748은 **그림의 남은 미검증 문제**다. 이번 원본 계약 일치로 해결했다고 주장하지 않는다. 초기 자세18종도 머리/날개/절단면·다른 자세 사용처 검증은 여전히 남아 있다. 실제HD 시각·레이어·vanish/held 검증 결과를 이 기계적 보고로 대신하지 않는다.

코다르 +90은 따로 `codarl_clones90_cached_pose/HANDOFF_CODARL_CLONES90_CACHED_REVIEW.md`의26OAM/14종 정정 입력을 사용한다. 이전17종은 설치 금지로 표시했다.