# 소드·저스티스·데스사이즈·알트론 제작 인계

공식 QA는 Claude, 라이브 연결/굽기/커밋은 root 담당입니다. 아래는 모두 미검증 제작 후보입니다.

| 패킷 | 설치 대상 | 완전 미연결 | indexed 재제작 | 비고 |
|---|---:|---:|---:|---|
| sword_strike_two_poses_packed8 | 8 | 4 | 4 | 이전 +350 4종 포함, 새 +500 4종 추가 |
| justice_fatum_two_poses_packed12 | 12 | 1 | 11 | 이전 +400 10종 포함, 새 +550 2종 추가 |
| deathscythe_scissors400_missing | 4 | 4 | 0 | 실제 손/무장 연결편3 + 암부 실루엣판1 |
| altron_dragon320_missing | 15 | 6 | 9 | 실제16 OAM 중 기존1 유지 |
| altron_dragon_head450_missing | 1 | 0 | 1 | 동일한 두 OAM에서 한 그림 공유 |

대상 총40종 중 이전 후보14종을 재포장했으므로 이번에 추가로 만든 그림은26종입니다. 40종 전부가 신규 그림이나 신규 누락이라고 세지 마십시오. 패킷마다 installation_map/원본계약/기계적검사/원본·생성출처/위험 메모를 보존했습니다.

소드8·저스티스12는 원래 각 후보의 HD/native RGBA를 완전히 보존해서 포장했습니다. 저스티스 기존2쌍, 알트론320 1쌍의 source 부분교차는 생성HD만 같은 source 좌표로 공유했습니다.

샌드록 sandrock_heated270_missing 6종은 원본 계약만 확정됐고 두 차례 생성에 과장된 연결편/후광이 남아 설치 보류입니다. PRODUCTION_HELD.md를 참고하십시오. installation_map이 없고 완료수에 넣지 않습니다.

추가 source 조사에서 소드14/w46+390와 데스사이즈1/w7+660은 전부 actual exact이므로 중복 그림을 만들지 않았습니다. 샌드록3/w16은 실제 native 메뉴에서 사용할 수 없어 강제로 호출하지 않았습니다.

게임/코어/DB/라이브 에셋·메인 핸드오프 문서는 수정하지 않았습니다. 실제HD 재생이나 공식 색/형태 audit는 하지 않았으며 후보존재/원본bytes·actualpalette·크기/중복·교차 공유만 기계적으로 확인했습니다.
