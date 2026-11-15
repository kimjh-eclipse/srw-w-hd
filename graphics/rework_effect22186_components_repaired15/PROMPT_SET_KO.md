# 생성 지시와 출처

도구: imagegen 스킬의 기본 내장 image_gen. 후보는 완전 새 raster 생성, 기술적 기하 정렬만 적용. 원본 도트 RGB/alpha 전사 없음.

밝은7: reference_group0.png의 3×3 배치에서 마지막2셀은 비운다. 보라 배경/번호는 제거, 진짜 투명 배경. 원본의 굵은 민트/흰 핵, 곡률, 각 끝, 흩어진 불씨 위치를 유지. 가는 바늘/추가 가지/고리/키색 구름은 만들지 않는다. generated_bright_raw.png 출처 exec-0f4aef45-028c-40bb-8c68-34d3353ce655.png.

어두운6: reference_group1.png의 3×2 배치 유지. 실제 #181818~#414141 회색만의 불투명 덩어리/리본/분리 불씨로 그린다. 흰 빛/민트/밝은 광원/추가 외곽선을 만들지 않는다. 모양/두께/끝 위치 보존. generated_dark_raw.png 출처 exec-a35fdfc0-fc90-4fce-8b48-289f6db7e60b.png.

프롬프트의 불씨 개수8은 원본9를 잘못 센 초안 표현이다. 실제 생성9/원본9를 보존했고 임의 삭제하지 않았다. 정렬과 불변 근거는 generation_alignment_provenance.json.
