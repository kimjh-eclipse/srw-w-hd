# unit250/weapon1026 실제 빔 FX 46 계약 제작 인계

## 입력과 수량
- source state `test_current/parts/native_weapon_source_250_1026/unit250_weapon1026_source.state`, +525~640. 실제 rendered OBJ cache/OAM/전체 palette/priority/flip/화면 위치는 계약 원문에 보존.
- source IMG12281 raw crop과 46개 모두 byte 일치. 실제 두 팔레트의 같은 full IMG index 배열을 사용. 46 계약/고유 raw는 source_integrity.json 참고. 실제 full 팔레트 2개(옅은 민트, 포화 청록), 단색 중앙 fill 2개도 포함.
- flat raw는 다중 IMG에서 byte 일치하므로 source_candidate_matches 전부 보존, owner=false/resource=None. 임의로 IMG 소유를 확정하지 않음.
- 4배 candidate.png 1024×896/native_combined.png 256×224. 각 실제 palette당 한 연속 새 그림, 같은 source 영역의 모든 하위 crop은 정확히 같은 생성 픽셀을 공유함. source_integrity.json에 부분 교차 쌍 기록.

## 최종 알파/색 생성 경위
- 최종 candidate는 각 실제 팔레트마다 **자기 imagegen RGB와 자기 imagegen alpha**만 사용. alpha 공유/다른 색 재색칠/자체 RGB 연장 없음.
- 옅은 민트는 exec-bb10f249 자체 transparent 생성본. 청록은 처음 transparent 생성 3회 중앙에 잘못된 구멍이 있어 제외. 먼저 불투명 navy 배경에 중앙 solid 유지한 청록 그림을 새로 생성(exec-7c605b7e), 그 그림에서 navy만 imagegen으로 제거해 자기 transparent 최종 그림(exec-93ef118b)을 얻음.
- 각각 generated_0.png/generated_1.png 원출력 보존. alpha preserve_generated, threshold/이진화/MinFilter 없음. 원본 RGB/alpha stamp와 코드 단색 채움 없음.
- 중간 시도 shared-alpha+RGB-extension은 root가 기하 불일치 때문에 거부했으며 **최종에서 제외**. rejected_shared_alpha_candidate.png와 alpha_material_restoration.json/원 생성 실패본은 실패 경위 보존용, 설치 대상 아님.
- 최종 후보 시각 확인에서 큰 중앙 plane의 잘못된 투명 구멍은 보이지 않음. 두 palette가 자기 생성 형상을 사용하므로 서로 조금 다른 실루엣/위치가 나타날 가능성은 Claude 실제 전환 장면 확인 필요.

## 생산 존재 확인과 미확인
- prepare46 모두 maxA255/empty0, original RGB hash 계약 일치. source integrity/overlap은 제작 정합만 확인, 실제 재생/독립 audit 없음.
- 알려진 시각 위험: 원본 평면보다 아주 약한 생성 texture/밝기 변동 있음. 청록 일부 미세 contour/밝기가 민트 별도 생성본과 다름. 기존 prepare 분리성분 제거가 일부 crop에서 1~3개 발생해 얇은 광 손실 여부는 Claude 확인 필요.
- Claude 우선 확인: +525/+545 작은 빔 파편, +560/+565 중앙 단색 fill 및 겹침 crop 연결, +605/+640 전체 평면, 두 palette 색 변환 시 형태 일관성과 알파 구멍 없음. source가 원래 잘린 flat plane을 임의로 닫거나 cap을 붙이지 않음.
- 최신 exact/indexed 중복 필터는 latest_live_filter.json. 인수 직전 root가 최신 live와 다시 중복 제외할 것.
- 라이브/library/DB/core/EXE 변경 없음. 실제 게임 HD 정상 판정 대기.
