# IMG20348 실제 두 팔레트 효과 신규 그림 10계약

제작 완료, 라이브 설치·굽기·독립 QA·HD 재생은 하지 않았습니다.

- 후보: candidate_20348_two_palettes.png (128×256, 원본 좌표계32×64, 4배)
- 연결: new_candidate_contract.json 10개, 실제 팔레트2벌.
- SHA256: 5a5a46065e39dcf1492376a2d8ef50b5faec29726da630fcd3a49a98c0d2af1f
- 원본IMG20348 (224,32)32×32 실제 cached OBJ 인덱스와 대조. 노랑/분홍 각각 독립 생성. 원본 픽셀/알파 스탬프, 다른 효과 재색칠 없음.
- 실제 입력: unit8_weapon29_source.state frame195/543, unit39_weapon162_source.state frame675~691. fresh capture는 상위 observed_contract.json, 원본출처는 contract_0/1.json.
- 제작 검사: production_report.json. prepare 10개 모두 maxA255, 지원면적비0.994~1.167. 3개에서 분리 성분1~2개 제거됨. native fill/절단면 잉크 모두0. 캐시쓰기 없음.
- 알려진 위험: 원본 작은 네모 입자가 생성본에서는 조금 유기적인 모양입니다. 전역 bbox 정렬이므로 개별 입자 위치·잘린 연결면은 Claude 확인 필요. 제거된 작은 성분도 확인 대상.
- 처음 픽셀블록으로 생성된 두 그림은 폐기하고 smooth 생성 두 벌을 사용. generated_0/1.png가 실제 사용 원출력.
- 전체 팔레트 변화 처리나 실제 이펙트 순서·가림은 검증하지 않았습니다.
