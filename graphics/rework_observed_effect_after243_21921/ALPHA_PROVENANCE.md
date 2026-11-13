# 생성 알파 보존

각 팔레트 자신의 generated_*.png RGB와 alpha를 사용. preserve_generated. alpha threshold/이진화/모폴로지 없음. 원본 RGB/alpha stamp나 타 팔레트 재색칠 없음. 원 생성 파일과 후보 모두 보존.

기존 prepare 내부 분리성분 제거가 발생한 crop은 production_report.json에 명시. 이는 자체 생성 그림 후처리와 별도이며, 가는 선/약한 glow 손실은 Claude 실제 재생 판단 대기.

## 최종 제작 범위와 알려진 한계
전체생성은 극소 세로선(slot2)과 분리 점선곡선(slot4)이 좌표가 어긋나 prepare에서 거의 사라졌다. repair2_generated.png와 repair4_generated.png를 같은 효과로 별도 새 생성 후 자기 alpha>=32 bbox를 위치 산정에만 사용, native bbox 크기/위치에 own RGBA를 등록했다(small_repairs_registration.json). alpha를 이진화/원본mask전사하지 않았고 최종sheet 한 영역으로 모든 교차 crop이 공유한다. 점선 개수/간격과 원본보다 두꺼운 cyan/glow/사각chip 형상 변화, 기타palette 회색 선의 자체 gray outline/haze는 Claude 실재생 대기. 15계약/8고유raw/2실팔레트.
전체 alpha preserve_generated. native bbox는 위치/크기 참조에만 사용. 라이브/DB/runtime 변경 및 독립 QA/실제 재생 없음.
