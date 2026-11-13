# 22472 밝은 팔레트 연기 고리 3 계약 자체 그림 교정

- 교체 actual hashes:3446316649 (원 계약 배열 index10, source72,0,64,64),1439743527(index12,source72,0,32,32),3402466599(index14,source96,24,32,32). 모든 group0.
- root 임시보류한 동일3ID 복원용. 계약 전체16은 new_candidate_contract.json, candidate_file은 이 후보를 가리킴. 신규 개수 추가가 아니라 기존3교정.
- candidate SHA `81acfb205d38110338b84e4d6ef72ee5c68bae2d571c81476765bd8cce548e59`. 768×512, 기존 atlas와 크기/좌표 같음. 원 atlas source(72,0,56,64)영역만 새로운 자체 생성 ring 그림으로 교체. 오른쪽 puff와 겹치는 source128..136 부분은 원 후보 자체 픽셀 그대로 보존.
- 영향을 받지 않는 나머지13계약 모든 crop RGBA byte동일 assert 통과. 교정3만 changed, partial 교집합은 같은 patch픽셀 공유. source/native/actualpalette 계약은 기존 22472 원본과 동일.
- 원본 고리의 큰 구멍을 filled smoke ball로 그렸던 문제를 원본 구조참조로 다시 imagegen. 첫 교정은 너무 가늘어 후보별도보존(ring_repair), 최종은 같은 자체 그림의 가지폭35% 보강 imagegen (exec-cc13564c). 원본 RGB/alpha stamp/다른palettealpha공유/코드색채움 없음.
- alpha preserve_generated 그대로, ownalpha>=8 bbox로 위치만 등록. 실제 source mask는 위치크기 참조 이외 사용하지 않음.
- 제작 중 hole-presence 참고: 원본 crop72,0,64,64 빈영역2602 nativepx, 교정전 약1379, 최종 약2745(alpha16기준). 원본 실루엣 완전일치 지표가 아니며 단순 filled-hole 문제가 완화됐는지 보는 제작보조. 실제QA/독립audit 아님.
- prepare16 모두 maxA>=16/empty0. 원본보다 strand가 부드럽고 밝은 부분 존재, 세부 굴곡/구멍 모양은 여전히 달라 실제 source +525/+535/+545 OAM/레이어/알파 검증 Claude 대기. g1 고리는 변경하지 않았고 기존 굴곡 차이 Claude 확인 대기.
- live/library/DB/core 미변경. root가 전체atlas16 다시굽고 동일3ID 재활성화 가능. 원 후보/원생성/두교정안은 부모폴더와 ring_repair/에 보존.
