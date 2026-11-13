# 최종 생성 알파 보존

최종은 두 실제 팔레트 각각 자기 imagegen RGB+자기 alpha. pale exec-bb10f249 / turquoise exec-93ef118b. preserve_generated, threshold/이진화/모폴로지 없음. 원본 RGB/alpha stamp 없음.

청록 exec-7c605b7e 자체 불투명 신규 그림에서 navy 배경만 imagegen으로 제거한 결과가 최종 generated_1.png. 중앙 solid 유지. 코드 색 키로 알파를 다시 만들지 않음.

shared-alpha/RGB-extension 중간 시도는 거부되어 최종 미사용. rejected_shared_alpha_candidate.png/alpha_material_restoration.json은 실패 경위 기록만. 최종 candidate SHA는 production_report.json 참조.

Claude 실제 QA 미완료. 별도 생성 두 palette의 미세 형상/밝기 차이, 기존 prepare 성분 제거로 가는 광 손실 위험을 확인해야 함.
