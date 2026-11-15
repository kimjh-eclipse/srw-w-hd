# 22591 공유 부모 입자8개 교정 인계

Claude의 실제 그림 판정에 따라 종전 기술보존 결론을 철회했습니다. 부모92645의 오른쪽 source/atlas [16,0,8,16] 영역에서 잘리거나 얇아진 입자를 새 ownRGBA로 다시 그렸습니다. 92648/92649는 같은 own_master_16x16.png의 실제 영역을 공유합니다.

- 변경3개: 92645/92648/92649. 다른7개와 부모 본체의 왼쪽 자체RGBA는 픽셀 그대로 보존했습니다.
- 실제 입자자리8곳: (17,2),(21,3),(16,6)2×1,(20,7)2×1,(18,8),(16,9),(16,11),(18,11). source(16,9)는 부모 본체와 이어지는 조각이며 잘라 독립 신규 그림으로 세지 않습니다.
- 각진 내부 사각색면 전사를 피하고 생성원천에서 부드러운 모서리와 연속 톤을 새로 그렸습니다. 1픽셀 점은 실제 성분/자리/폭 보존이며 HD 세부 이득은 제한적입니다. 작은 점들을 독립 신규8장으로 세지 않습니다.
- native64×32, candidate 정확4배256×128. 실제 full16/BGR555·index raw·관측 state/frame은 final_flat_contract.json과 actual_original_contract10.json에 보존했습니다. source_box/atlas_box를 명시했습니다.
- generated_components.png를 crop/resize한 자체RGBA만 사용했습니다. source RGB/alpha/mask 전사, 출력 alpha문턱삭제·형태학 삭제를 하지 않았습니다. generated alpha를 유지했습니다. manual_comparison_gray.png는 원본/이전/새그림이며 회색 합성으로 실제표시와 alpha0RGB를 구분했습니다.
- 작업 시작 spec SHA와 네 파일 SHA는 live_spec_start.json/ready_candidate.json에 있습니다.
- 위험: 생성물이 실제 황색/황토색 사이를 연속 톤으로 근사하며 미세 농도차가 남습니다. 대부분 1픽셀 점이라 체감 HD이득은 제한적이고 폭 복원 성격이 큽니다. 중앙 연결/굽기/공식QA를 수행하지 않았으며 Claude에게 인계합니다.
