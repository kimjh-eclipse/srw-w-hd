# 21427 공유 부모 master 교정 인계

Claude의 실제 영역 판정을 따라 종전 기술보존 결론을 철회했습니다. 93795/93803/93804/93809의 흐린 타원은 공유 부모 master에서 함께 다시 그렸습니다. 여섯 실제 성분 A~F의 source 자리·폭을 유지했고 C/E는 같은 자체 생성 RGBA를 공유합니다.

- 변경 계약 9개: 93794, 93795, 93796, 93799, 93802, 93803, 93804, 93806, 93809.
- live 시작 spec SHA는 live_spec_start.json, 인계 파일 SHA 네 종류는 ready_candidate.json에 있습니다.
- 실제 full16/원본 index raw/관측 frame·state는 final_flat_contract.json과 actual_original_contract22.json에 보존했습니다. source_box와 atlas_box를 분리했습니다. source master [0,0,32,64] → candidate master [0,240,32,64].
- native 256×400, candidate 정확4배 1024×1600. 기존 own RGBA에서 네 자식 사각 범위만 새 own RGBA로 다시 그렸고 나머지 모든 픽셀을 보존했습니다. 다른 팔레트 영역·미변경 바인딩 10개는 그대로입니다.
- 생성 원천의 crop/resize만 사용했습니다. 원본 RGB/alpha/mask 전사, 출력 alpha 문턱삭제·형태학 삭제를 하지 않았습니다. generated alpha와 raw alpha0 RGB도 그대로 유지합니다.
- manual_comparison_gray.png: 위 원본, 가운데 이전 타원, 아래 새 그림. 회색 합성으로 alpha0 RGB와 실제 표시를 구분했습니다.
- 위험: 실제 사용 회색은57/90이며 새 생성물에는 미세한 농도 변화가 있습니다. 모서리를 부드럽게 새로 그렸으나 매우 작은 1~3픽셀 성분이므로 새 HD 세부의 이득은 제한적입니다. 1픽셀 D는 별도 대형 신규 그림으로 세지 않습니다. 원본의 셀 내부 색 경계는 생성물 근사입니다.
- 그림·원천·좌표 계약만 작성했습니다. 중앙 연결/굽기/공식 QA는 수행하지 않았으며 Claude에게 넘깁니다.
