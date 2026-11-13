# 생성 알파 보존

각 팔레트 자신의 generated_*.png RGB와 alpha를 사용. preserve_generated. alpha threshold/이진화/모폴로지 없음. 원본 RGB/alpha stamp나 타 팔레트 재색칠 없음. 원 생성 파일과 후보 모두 보존.

기존 prepare 내부 분리성분 제거가 발생한 crop은 production_report.json에 명시. 이는 자체 생성 그림 후처리와 별도이며, 가는 선/약한 glow 손실은 Claude 실제 재생 판단 대기.

위치 등록은 생성 alpha>=8 bbox로 크기/위치만 계산하며, alpha 자체를 threshold하지 않고 전체 자체 RGBA affine으로 변형한다. 원본mask는 사용하지 않는다. 미약한 떨어진 alpha1 흔적 때문에 본체가 과도하게 축소되는 것을 피하기 위한 자체 위치 보정이다.
