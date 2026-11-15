# 생성 지시/출처

imagegen 스킬 기본 내장 도구. 모든 원출력은 이 폴더에 복사했다. referenced native는 실제 색/위치/폭/성분 참조이며 출력 마스크로 사용하지 않았다.

1. 청색4/회색5 전체: 십자광, 얇은 연결 원호, 원본 위치의 분리 원호10/9/10, 세로선3/2/3 성분. 진짜 투명 배경, 선 폭과 실제 색 보존, 추가 불씨/금속 테두리/블록 경계 금지. 최초 금속블록 해석2장은 거절 보존. 교정2장 generated_cyan_raw.png(exec-c703e72e-a06c-492f-82d1-fea6a053f750) / generated_gray_raw.png(exec-b1b83669-c96a-4b25-ad14-df924166b7ea).
2. 분리 원호별 실제 성분10/19: 각 원본 성분 색/형상을 하나의 독립 셀로 새로 그린다. 단순한 optical material, 윤곽/장식/금속 홈/추가 조각 금지. generated_components_cyan_raw.png(exec-b0b0ace2-a458-43fb-9b51-ac82456d738f), generated_components_gray_raw.png(exec-f7179839-b281-45ab-8bcc-4a8289c54d03).
3. 원본 대각 접촉4성분: 참조 없는 자체 새 생성. 단일 연결 짧은 대각선 2×2 시트, 각 실제 청색/회색 조합, 분리된 두 사각이 되지 않게. generated_diagonal_four_raw.png(exec-ebb71690-7779-420e-82f1-9f242013fa65).
4. 실제청색 세로3재료: 3×1 시트. 실제 #5aace6/#62c5de/#94deee 띠 순서와 길이24/4/2를 보존하며 흰 핵/금속테두리 금지. generated_components_cyan_vertical_raw.png(exec-cd4fff97-3777-4cd6-a871-7af6f35f6d90).

수정은 생성 자체와 기하 정렬만이며 원본 RGB/alpha 찍기·후보 재색칠·알파 지우기는 하지 않았다. 구체적인 셀/스케일/위치는 generation_alignment_provenance.json에 보존했다.
