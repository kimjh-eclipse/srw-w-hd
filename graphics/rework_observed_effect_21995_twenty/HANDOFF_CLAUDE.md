# IMG21995 실제 두 팔레트 효과 후보

- 상태: 새 그림 제작 및 생산 입력 확인 완료. 라이브/DB/코어 변경, 독립 QA, 실제 HD 재생은 하지 않았습니다.
- 파일: candidate.png (448×256), native_combined.png (112×64), new_candidate_contract.json (20계약, 고유 raw 형태 10개, 실제 팔레트 2벌).
- SHA256: 1b4ef1477a4b458c39ebec13751987c68c71ca070f0bebc04ff9c44dab4fbb23
- 실제 출처: unit130/weapon543, test_current/parts/true_missing_19818/unit130_weapon543_source.state, 팔레트별 최초 frame349/470. index bytes, 실제 전체 팔레트, OAM 계약은 source_contract.json에 보존.
- 같은 팔레트의 모든 하위 파츠는 한 벌의 새 생성 그림에서 동일 좌표로 분할합니다. 겹치는 원본 영역은 같은 생성 픽셀을 공유합니다. 원본 RGB/alpha 복사 및 다른 효과 재색칠은 하지 않았습니다.
- 생산 prepare 결과: 20개 모두 maxA255, 빈 그림 없음. 일부 작은 분리 흔적 1~2개 정리됨(상세 production_report.json). native fill/cut ink 사용 없음.
- Claude 확인 필요: 얇은 꺾인 선/작은 원형 효과 크기와 굵기, 생성된 광채 경계, 직선 절단면 사이 이음새 및 실제 전면 효과 순서. 제작 확인은 시각 품질 판정이나 재생 통과가 아닙니다.
