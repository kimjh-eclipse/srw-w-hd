# 생성 알파 보존

각 팔레트 자신의 generated_*.png RGB와 alpha를 사용. preserve_generated. alpha threshold/이진화/모폴로지 없음. 원본 RGB/alpha stamp나 타 팔레트 재색칠 없음. 원 생성 파일과 후보 모두 보존.

기존 prepare 내부 분리성분 제거가 발생한 crop은 production_report.json에 명시. 이는 자체 생성 그림 후처리와 별도이며, 가는 선/약한 glow 손실은 Claude 실제 재생 판단 대기.

등록 위치 보정: 생성 alpha1에 멀리 떨어진 미약 흔적이 있어 본체가 과도하게 축소되는 것을 막으려고, 생성 alpha>=8 bbox를 좌표 등록의 크기/위치에만 사용했다. alpha 값은 전혀 threshold하지 않고 전체 자체 RGBA를 affine으로 이동/크기 변경했다. 원본 bbox는 위치/크기 참조이며 원본 mask를 후보에 찍지 않았다. production_report.registration에 실제 좌표가 기록돼 있다.
