# 생성 알파 보존

각 팔레트 자신의 generated_*.png RGB와 alpha를 사용. preserve_generated. alpha threshold/이진화/모폴로지 없음. 원본 RGB/alpha stamp나 타 팔레트 재색칠 없음. 원 생성 파일과 후보 모두 보존.

기존 prepare 내부 분리성분 제거가 발생한 crop은 production_report.json에 명시. 이는 자체 생성 그림 후처리와 별도이며, 가는 선/약한 glow 손실은 Claude 실제 재생 판단 대기.

## 최종 제작 범위와 알려진 한계
원본의 우측 큰 흰 L면 slot5(source192,0,64,32)는 전체생성에서 투명하게 빠져 두 차례 교정했다. 최종 whiteplane5_generated.png 자기 RGB/alpha를 해당 crop 위치에 resize해서 복원(whiteplane5_patch.json), 원본 mask/색 채움 없음. 거친 바깥 AA/얇은 암선과 대각 경계/내부코너가 원본과 다를 가능성 Claude 확인 필요. 나머지28 계약 원래 생성영역 보존. 기본 밝은 팔레트19+황색 팔레트10은 고유 raw19종의 두 실색 구성이지 고유 도형29종을 뜻하지 않음.
전체 alpha preserve_generated. native bbox는 위치/크기 참조에만 사용. 라이브/DB/runtime 변경 및 독립 QA/실제 재생 없음.
