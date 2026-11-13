# 실제 unit102 / weapon427 +350 미연결 기계 조각 5종

상태 `CACHED_OBJ_ARTWORK_CANDIDATE_UNVERIFIED`. 라이브/DB/공유 코드 변경 없음. 실제 HD 재생 및 공식 검사는 Claude 대기.

- 설치 입력: `installation_map.json`, `candidate_atlas.png`, `native_atlas.png`, `contract.json`.
- 후보 SHA256: `b8dcac092c142735595477091549c6db931f1e7ae1aa56cdee48821da3f7e2e7`.
- 실제 fixture: `source_mechanical_fixed_102_427_350/source_pose.state` +0. 메뉴350의 cached OBJ/팔레트/OAM/코어SHA 계약 보존.
- 기존 exact가 없는14종 중9종은 indexed 연결이 있어 제외했다. 이번 실제 미연결5는 원래 셀3/7/10/11/12이며 최종 셀0..4로 재번호했다. `*_all14_source.json`과 시트에 전체 추출 보존.
- 5종 전부 actual exact0/indexed0이다. 원본4종은 IMG9506, 1종은 IMG9532의 기록된 실제 인덱스 사각형과 일치한다. 연결되는 본체 전체19/21의 완성이나 기술 전체 완료로 세지 않는다.
- 전체16색은 PLT1621/1638/9639 bank0와 모두 동일하다. 하나를 단일 팔레트 소유로 단정하지 않는다. 실제 청색/남보라/회백색/주황·빨강·노랑 면을 그대로 참조했다.
- 대상 원본 사각형끼리 교집합 없음. 같은 source의 인접 사각형이라는 이유로 서로 다른 화면 위치의 조각을 한 물체로 그리지 않았다. 전체 pose의 기존 indexed/exact 의존과 실제 OAM/priority 좌표를 보존한다.
- 역할은 실제 native 기계 문맥만으로 정했다. 작은 다각형 패널을 얼굴/눈/완성된 손으로 자동완성하지 않도록 생성했다. 주황·노랑 면은 광원·불꽃으로 만들지 않았다.
- 원본과 생성 원본 모두 보존, 생성 alpha<64만 정리하며 고알파RGBA 불변. 원본 RGB/알파 복사/스탬프 없음.
- `candidate_pose_production.png`는 제작 참고이고 실제 HD 게임 결과가 아니다.

Claude 위험: 주황 사각면의 개수·위치와 명암, 셀1 기계 연결부의 해석, 셀3 넓은 비스듬한 회백색 면의 연결, 셀4 작은 절단 조각의 AA/명암, 기존 청백색 indexed 몸체와의 이음새를 확인해야 한다. 현재 작은 후광/AA와 파츠 사이의 그림 스타일 차이는 실제 재생 전 미확정이다.
