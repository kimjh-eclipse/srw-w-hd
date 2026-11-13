# 형태·빌린 그림 재검토 결과

## 작업 범위
공유 런타임, 라이브 kazuma_parts_library.json, 구운 DB, 메인 HANDOFF_FROM_CODEX.md는 변경하지 않았습니다. 새 그림은 **미설치 후보**입니다.

## 확인한 실제 자세
- 기체: 그레이트 마징가. 사용 fixture는 합체공격 상대가 아닌 **unit297 diagnostic_preview weapon1213 frame300.state +3프레임**입니다. 폴더 이름의 기체와 화면에 동시에 그려지는 기체가 다를 수 있으므로 이름만으로 추정하지 않았습니다.
- path: test_current/combat/named_attacks/unit_297/diagnostic_preview/weapon_1213_capture/frame_300.state
- 화면 x164~226/y56~120, 앞쪽 주먹을 내밀고 양다리를 벌린 자세.
- 실제 OAM0~16의 **17개 전체**를 캡처. 2654+14882의15개 외에 실제 주먹2개(기존14571/14225)도 같은 자세에 속해 반드시 포함했습니다.
- native VRAM + OAM 디코딩으로 실제 index/RGB hash·팔레트·원본RGBA를 저장했습니다. 단순히 기존 아틀라스의 잘못된 참조그림을 사용하지 않았습니다.
- 기존 shape/unpainted 경고 binding7340/7352/7353/82825/7343이 이 자세에 실제 등장합니다.

## 산출물
- great_complete_contract.json: 17개 실제 tile, actual_palette_rgb/BGR555, index_pixels, hash/index_hash, 이전 spec, row/OAM, 후보 atlas_box(네이티브좌표). existing_actual_rgb_binding 및 이전 spec의 palette 일치 여부도 포함.
- part_0_native.png ~ part_16_native.png: 실제 실행중 원본 타일.
- great_complete_pose_native.png / great_pose_comparison.png: 원본조립/후보조립.
- great_candidate_atlas.png: 4배, 네이티브200x160의5x4셀(셀40x40) 아틀라스. 17개 전체. great_native_atlas.png가 대응 원본.
- great_parts_generated.png: built-in imagegen 원출력. 출처 exec-2fe57aed-0b5e-4904-abcf-9403cc2885cc.png. 생성 지시:5x4사각형 위치·각도·원본색 그대로, 동일그레이트마징가17파츠, 절단면외곽선 금지, 투명배경. 실제 팔레트의 파랑장갑/부츠, 라벤더은색, 빨강V/날개, 노랑만 사용. 다른기체 그림 재색칠 아님.

## 검사 (라이브 설치 전, 읽기 전용)
- great_candidate_report.json: 17개 alpha IoU .75~.9673. 기존7340 .4→.8,7352 .556→.75,7353 .566→.8875,82825 .5→.8103,7343 .692→.7647. 원본 알파를 찍어 씌우지 않고 생성그림의 자체 알파를 사용했습니다.
- great_candidate_colour_key_check.json: production PartsRenderer.material_map을 __new__로 메모리에서 호출(디스크캐시/DB 접근 없음), 실제 캡처 index_pixels·팔레트 사용. 17개 misplaced_share=0, known catalog 변형 wrong_colour_share=0, slots_never_native=[], green/magenta잔여0.
- **실제 재생 검증 아님.** 실제재생은 원본 캡처 때만 했고, 후보를 연결한 게임은 아직 실행하지 않았습니다. 굽기/alpha cache/register_part도 통과했다고 말할 수 없습니다.
- 시각검토: 원본과 후보 조립을 나란히 봄. 모든17파츠 위치/부츠·장갑의 파랑, 팔·몸통라벤더, 붉은V·날개는 유지. AI가 일부 관절면/광택을 단순화했으므로 최종 실제재생과 다른 자세 호환성 확인이 필요합니다.

## 설치 시 주의
- source binding을 무작정 덮지 말고 actual RGB hash로 연결하십시오. 기존17중6개는 등록spec의hash와 실제hash가 다르며, 이는 indexed재색칠로 현재 화면에 들어온 경우입니다. 실제값은 contract에 있습니다.
- 동일자세17개를 하나의 atlas로 동시에 연결하세요. exact RGB전용(indexed_safe=False) 권장. 원본5263 prefix는 변경금지.
- 기존actual RGB해시가 있는 항목(existing_actual_rgb_binding)은 중복append하면 선행것이이깁니다. 그 항목의그림만 새atlas로바꾸고, 나머지actual해시만추가하는 설치기가 필요합니다.
- 인덱스가 같은 다른팔레트 기체에 이 새그림을 무조건공유하지 마세요.
- 최종설치 후 resource범위만 굽고, 색번호/키색검사 및 위 실제state 재생, UI/컷인 가림까지 확인해야 합니다.
