# 생성 알파 보존

각 팔레트 자신의 generated_*.png RGB와 alpha를 사용. preserve_generated. alpha threshold/이진화/모폴로지 없음. 원본 RGB/alpha stamp나 타 팔레트 재색칠 없음. 원 생성 파일과 후보 모두 보존.

기존 prepare 내부 분리성분 제거가 발생한 crop은 production_report.json에 명시. 이는 자체 생성 그림 후처리와 별도이며, 가는 선/약한 glow 손실은 Claude 실제 재생 판단 대기.

## 최종 제작 범위와 알려진 한계
실제 정상 기본팔레트10계약만 제작. 추가 특수 팔레트1계약(hash2730118576)은 actual 원본에서 초록 사각이 생기는 collapse를 보여 HANDOFF_PALETTE_HOLD.md로 분리했다. 그1은 신규그림/완료수 제외이며 native_1.png/source_contract_with_palette_hold.json에 source/base페어 보존. 초록을 임의로 제거하지 않음. 생성 기본은 원본의 화염/연기보다 두껍고 평면적인 면분할/검은틈 변화, 흰 타격면 내부 질감/외부 미세 glow가 있어 Claude 판단 필요.
전체 alpha preserve_generated. native bbox는 위치/크기 참조에만 사용. 라이브/DB/runtime 변경 및 독립 QA/실제 재생 없음.
