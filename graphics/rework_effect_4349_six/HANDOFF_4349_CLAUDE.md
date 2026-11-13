# IMG4349 전략 지도 폭발·연기 신규 6계약

제작 완료, 라이브 설치·굽기·독립 QA·HD 재생 미수행.

- 후보 candidate_4349_six.png: 384×256/native96×64,4배. new_candidate_contract.json 6개.
- SHA256 e6de876f664718cbcf64c6b519a116f8129f14e80d47d8f83d26fe0863f894f6
- 실제 원본: unit190/mechanical_cutin_136.state+280, body_missing_probe_190_280/rendered_contract_all.json. 전략 지도 위 폭발/연기이며 아스테바리스 기체 그림이 아닙니다.
- 원본4349 각 crop와 actual cached raw index bytes 일치, 실제 동일 팔레트1벌, RGBhash 재계산6/6일치. 현재 라이브에 이미 같은hash 있는 항목은 보존하여 과거8후보 중 신규는6.
- source_contract.json에 원본좌표/인덱스/팔레트/OAM/변환/프레임 보존. resource=None, effect_part=True, dynamic_palette=False.
- own 생성본 generated_six.png의 여섯 영역을 각각 자체alpha로 추출 후 원본bbox에 위치만 정렬. 중간 아래 arc에 옆 폭발 빛이 번진 영역은 생성본 상단160행만 추출해 제외. 원본RGBA/alpha스탬프 없음.
- production_report.json: prepare6/6 maxA255,지원면적비1.007~1.089,분리성분제거0/nativefill0/cutink0. 캐시쓰기 없음.
- Claude 확인대상: 작은 회색연기의 형태 세부,폭발 하단과 기존 파츠 연결면, 생성된 불꽃 곡선이 원본과 다른 정도. generated_six.png는 옅은 네온 번짐이 있지만 실제 후보는 자체alpha220 이상으로 정리했습니다. 신규6만 그림이며 전체4349 전수완료 주장이 아닙니다.
