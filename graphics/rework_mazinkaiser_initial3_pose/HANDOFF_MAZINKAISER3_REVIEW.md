# 마징카이저 초기 +3 자세 제작 인계

현재 상태: **미검증 그림 후보 / 연결 준비 가능**. 라이브 등록·굽기는 root가 직렬 처리하고, 공식 검사·시각 판정·실제 재생은 Claude가 담당한다. 이번 최종 그림에 대한 공식 audit와 재생 검증은 실행하지 않았다.

## 선정과 실제 계약

원본 state는 `test_current/combat/named_attacks/unit_297/diagnostic_preview/weapon_1213_capture/frame_300.state`, offset +3이다. Core를 4회 진행해 제작용 OAM/VRAM/팔레트를 추출했다. 재생 검증을 수행한 것이 아니다.

- 마징카이저는 실제 palette slot 0, OAM 37~56의 20개다. 그레이트와 겟타를 제외했다.
- 고유 actual RGB 해시는 18개다. 방금 설치된 running179의 20개와 교집합은 0이다.
- 12개 고유 그림은 이미 exact RGB 연결이 있었다. 6개 고유 그림은 8개 OAM에서 다른 source hash의 indexed proxy를 사용했다. 분량을 단순히 '전부 누락'이라고 기록하지 않는다.
- 이 자세를 한 벌로 그렸으므로 exact 12개의 그림도 새 후보로 교체하게 된다. 같은 actual RGB를 쓰는 다른 공격에 영향을 줄 수 있다.
- 셀16 OAM53/55, 셀17 OAM54/56은 원본 index bytes·팔레트·atlas box가 같아 한 그림을 공유한다. 실제 OAM 좌표와 반전은 contract에 남겼다.

계약은 `contract.json`(20 OAM), `contract_unique18.json`(18종), `classification.json`, `duplicate_check.json`, `actual_buffers.npz`다. `all_oam.json`과 `all_oam_contact.png`에는 타 기체까지 포함한 추출 자료가 있다.

## 원본과 제작 그림

- `native_atlas.png`: 320×288, native 원본.
- `grid_reference.png` / `grid_context_gray.png`: 동일 배치 원본 확대와 셀 번호.
- `native_pose.png` / `native_pose_detail.png`: 원본 OAM 우선순위·역순 조립.
- `whole_oam_context.png`: 실제 조립 위 각 파츠 bbox 표시. 역할명은 이 문맥 확인 전 추측하지 않는다.
- `candidate_atlas.png`: 1280×1152, 4배 최종 미검증 후보.
- `candidate_pose.png` / `candidate_detail.png` / `pose_comparison.png`: 동일 OAM 좌표로 제작 과정에서 조립한 전달 자료. 시각 판정 완료 증거가 아니다.
- `parts_generated.png`: 18종을 5×4 셀에 만든 원 생성본. 마지막 2셀은 빈 셀이다.
- `head_joint_generated.png`: 실제 인접 셀1/2/3을 연속 그림으로 제작. actual origin(35,47), 크기48×40, 각 OAM 직사각형으로 역분할했다.
- `wing_joint_generated.png`: 실제 셀15/16/17의 연속 날개를 제작. origin(67,45), 크기40×64. 같은 해시를 쓰는 반대쪽 날개는 처음 OAM 위치를 기준으로 만든 동일 그림을 공유한다.

머리 셀1/2/3과 날개15/16/17의 각 사각형은 서로 면적이 겹치지 않는다. 뒤 파츠가 숨긴 원본 영역을 앞 그림 색으로 덮는 경우를 피하도록 이 범위만 공동 그림으로 나눴다. 생성 그림의 alpha만 정리·크기 맞춤했으며 native RGB나 alpha를 복사해 후보에 찍지 않았다. 실제 팔레트의 보라/연분홍 장갑, 붉은 테두리, 황토색 날개 내부, 노란 눈·장식을 생성 지시했다. 의도대로 되었는지는 Claude가 원본과 대조한다.

## root 설치 입력

`installation_map.json`은 기존 running179와 같은 형식이다.

- atlas_id: `mazinkaiser_initial3_pose`
- image: `graphics/rework_mazinkaiser_initial3_pose/pose_hd.png`
- reference: `graphics/rework_mazinkaiser_initial3_pose/pose_native.png`
- native_size: `[320,288]`
- actual RGB 전용 18 entries, indexed_safe=false. 기존 indexed fallback을 다른 팔레트용으로 보존해야 한다.
- 후보 SHA256: `79f3bb56eeb2268d39de23633c293ea2062435789a6c4ba78c5bf0b8e58108aa`

`mechanical_final.json`은 개수·크기·index bytes 길이·사각형 범위·파일 SHA256만 확인했다. 모든18개 후보 사각형에 alpha가 있다는 기계적 확인이며 형태/색/레이어가 옳다는 검사가 아니다. `provenance.json`에 생성 출처와 처리법을 기록했다. 라이브/DB/공유 실행 코드를 수정하지 않았다.

## Claude 검증 큐

root 연결·재굽기 이후 다음 장면을 확인한다. +3은 컷인이 기체를 가릴 수 있으므로 OAM 계약 자체와 이어지는 자세/다른 사용처도 대조한다. +179는 다른 팔레트의 running179 자세이며 이번18종과 혼합 집계하지 않는다.

```powershell
& 'C:\Program Files\Python311\python.exe' -X utf8 scripts/verify/verify_runtime_path.py --state test_current/combat/named_attacks/unit_297/diagnostic_preview/weapon_1213_capture/frame_300.state --frames 300 --pure-native --save-frames 3 20 40 179 --track-atlas mazinkaiser_initial3_pose --name mazinkaiser3_claude
```

현재 미확인 사항:

1. 연속 머리1/2/3의 눈·센서·색 영역, 턱 그릴과 주변 파츠의 접합.
2. 연속 날개15/16/17의 실제 외곽 지원 영역과 파츠별 절단 경계.
3. 나머지 개별 생성 파츠가 가진 내부 절단면 선/색 차이, 모든 OAM에서의 연결.
4. 기존 exact12종을 바꾸면서 다른 자세가 손상되는지.
5. 대사창 가림과 컷인·효과 레이어는 이번 제작으로 해결됐다고 주장하지 않는다.
6. 별도 running179 후보의 slot51(새 binding91913) 지원 alpha IoU .564748 경고는 root가 기록한 **남은 그림 수정 사항**이다. 이번 초기 자세는 다른 actual RGB로 그 경고를 자동 해결하지 않는다. 이전179의16~19 분할에서 earlier-generated alpha 제한이 걸렸던 점을 조사할 수 있으나, 이번 파일을 그179 해시에 무작정 연결하면 안 된다.

공식 audit 수치나 실제 재생 결과를 이 문서에 대신 채우지 않는다. Claude 결과가 나오면 필요한 그림 수정 범위를 전달받는다.
