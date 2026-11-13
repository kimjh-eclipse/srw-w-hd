# 생성 알파 보존

각 팔레트 자신의 generated_*.png RGB와 alpha를 사용. preserve_generated. alpha threshold/이진화/모폴로지 없음. 원본 RGB/alpha stamp나 타 팔레트 재색칠 없음. 원 생성 파일과 후보 모두 보존.

기존 prepare 내부 분리성분 제거가 발생한 crop은 production_report.json에 명시. 이는 자체 생성 그림 후처리와 별도이며, 가는 선/약한 glow 손실은 Claude 실제 재생 판단 대기.

최신판은 각 실제palette 자기 imagegen RGBA. opacity복원도 imagegen 자체그림에서 수행하며 다른palette alpha공유/원본alpha stamp/코드채움 없음. 원생성 파일은generated_*.png, 실패판은rejected_*로보존. 등록bbox는alpha>=8 위치계산만, alpha값유지.
