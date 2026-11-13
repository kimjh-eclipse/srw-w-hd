# 생성 알파 보존

각 팔레트 자신의 generated_*.png RGB와 alpha를 사용. preserve_generated. alpha threshold/이진화/모폴로지 없음. 원본 RGB/alpha stamp나 타 팔레트 재색칠 없음. 원 생성 파일과 후보 모두 보존.

기존 prepare 내부 분리성분 제거가 발생한 crop은 production_report.json에 명시. 이는 자체 생성 그림 후처리와 별도이며, 가는 선/약한 glow 손실은 Claude 실제 재생 판단 대기.

## 최종 제작 범위와 알려진 한계
초기 생성본은 도트의 큰 계단이 그대로여서 부드러운 새 광선으로 imagegen 교정했다. 최종 generated_0/1은 각 실팔레트 자신의 RGB/alpha이고 다른팔레트 alpha를 빌리지 않았다. 두팔레트 crop형태가 약간 다르고 작은 파편의 폭/주변 저알파 haze 및 큰 광선 끝이 원본과 다를 수 있어 Claude 확인 대기. 6계약/5고유raw/2실팔레트. 기존 prepare 작은 독립광 성분 제거3건 기록.
전체 alpha preserve_generated. native bbox는 위치/크기 참조에만 사용. 라이브/DB/runtime 변경 및 독립 QA/실제 재생 없음.
