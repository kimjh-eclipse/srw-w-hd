# 실제 unit117 / weapon492 메뉴380 미연결 4종 후보

상태 `CACHED_OBJ_ARTWORK_CANDIDATE_UNVERIFIED`. 공식 검사·실제 HD 재생은 Claude 대기. 라이브/코어/DB 변경 없음.

- 설치 입력: `installation_map.json`, `candidate_atlas.png`, `native_atlas.png`, `contract.json`.
- 후보 SHA256: `0a098d278dd8fef11c92f6ebb8ef2eeb35c3e8b48091ec51616cf378aee3868b`.
- fixture: `source_mechanical_fixed_117_492_350/source_pose.state` +0. 요청350 뒤 실제 메뉴380에서 캡처했다. actual cached OBJ/팔레트/OAM/코어SHA 보존.
- 네 조각 모두 실제 exact0/indexed0이며, 원래5번째 actual 셀4의 indexed proxy43406은 이번 그림에서 제외하고 의존 보존했다. 전체 기체·무장 완료로 세지 않는다.
- 셀0은32×8 얇은 회백/회청색 굽은 날/장갑면, 셀1은16×16의 작은 회백색 잘린 조각, 셀2는32×32 파란 머리/회백 테두리/비대칭 뿔, 셀3은32×16 파란색 하단 기계 조각이다. 원본 IMG10053 3종/10066 1종과 바이트 일치. 대상 원본 사각형끼리 교집합 없다.
- 팔레트 소유는 사용색 후보와 전체16색 대조를 구분해 `full_palette_phase_proof.json`에 기록했다. 실제 작은 빨강 슬릿 눈과 아래 주황 면을 원본 위치로 참조했고 일반 양눈이나 금색V뿔을 넣지 않았다.
- 생성 원본 보존, 자체 alpha<64만 정리·고알파RGBA 불변. 원본 RGB/알파 복사/스탬프 없음. 각 원본 캔버스 크기와 실제 반전/OAM/priority 보존.
- `candidate_pose_production.png`는 제작 참고이지 HD 실제 게임검사가 아니다.

Claude 위험: 파란 머리의 원본보다 둥근 헬멧 곡면·빨간 슬릿 위치·주황 면 크기, 얇은 조각0의 위끝/하단, 셀1의 빈 구멍과 잘린 끝, 셀3 기존 몸체 접합과 검정 빈틈, AA 가장자리의 밝은 픽셀을 실제 재생에서 확인해야 한다. 기존 파란색 indexed 하체는 그대로라 새 그림과의 스타일/명암 차이도 미확정이다.
