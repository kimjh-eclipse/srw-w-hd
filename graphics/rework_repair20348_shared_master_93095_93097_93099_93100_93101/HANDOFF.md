# 20348_new10 공유 부모 입자 교정

종전 기술보존 결론을 Claude의 실제 그림 영역 판정에 따라 철회했습니다. 93095 부모의 우상단8개 입자를 채워진 실제 폭으로 새로 그렸습니다. 93097/93099/93100과 추가 겹침93101은 같은 master RGBA를 공유합니다.

변경5개: 93095/93097/93099/93100/93101. source master [224,32,32,32]와 candidate master [0,32,32,32]를 구분했습니다. full16/raw index/관측 frame·state는 계약에 보존했습니다. 다른 팔레트5개와 부모의 나머지 기존 자체 그림은 그대로입니다. source native32×64, candidate 정확4배128×256.

작업 시작 지문과 4파일SHA는 live_spec_start.json / ready_candidate.json에 있습니다. manual_comparison_gray.png는 원본/이전/새그림 순서입니다. 생성원천 crop/resize만 사용했습니다. 단색1px 성분은 같은 생성물의 불투명 내부 material을 잘라 사용했으며 원본 RGB/alpha 전사와 출력 alpha문턱 삭제는 하지 않았습니다. 입자 개수/자리/폭을 유지했습니다.

남은 위험: 생성색에 미세 농도차가 있고 작은 1~2픽셀 입자라 HD세부 이득은 제한적입니다. 원본 블록형 폭을 복구하는 교정이며 독립 신규8장으로 세지 않습니다. 중앙 연결/굽기/공식검증은 수행하지 않았습니다.

## 연속 HD 면 재교정

최종 선택은 ready_repaint.json / candidate_repaint.png / contract_repaint.json / generated_repaint.png입니다. 이전 ready_candidate.json의 원래 그림 SHA는 복원하여 보류 상태로 보존했습니다. 내부 격자색면을 제거하고 자체 새 생성물의 연속 톤과 매끈한 모서리로 다시 그렸습니다. 원본 성분 자리/폭 및 동일 master 관계는 유지했습니다. 작은1px점은 성분 보존이며 HD 이득으로 별도 계수하지 않습니다.
