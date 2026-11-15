# 22338 공유 부모9성분 교정

종전 기술보존 결론을 Claude의 실제 소실 판정에 따라 철회했습니다. 세 자식 범위의9성분을 새 연속 곡선/연속 색면으로 다시 그렸고 부모92453 및 같은 영역을 읽는 자식 모두 동일 own_master.png를 공유합니다.

변경6개: 92453/92462/92463/92468/92469/92470. 추가92463/92469도 같은 master 약한 영역과 겹쳐 계약에 포함했습니다. 다른6 live 바인딩과 범위 밖 기존 자체RGBA는 그대로입니다. source/atlas master[128,32,32,32], 원본168×96/후보672×384 정확4배입니다.

실제full16/BGR555·index raw·관측frame/state는 final_flat_contract.json/actual_original_contract.json에 보존했습니다. 원본성분좌표는 components_source.json, 생성물crop/resize·배치는 author_config.json/shared_master_contract.json에 있습니다. 작은세로성분2개는 동일ownRGBA를 공유했습니다. 원본 RGB/alpha/mask를 출력에 전사하지 않았고 출력alpha문턱삭제/형태학 삭제도 하지 않았습니다. raw PNG alpha0RGB와 실제표시는 회색 manual_comparison_gray.png로 구분했습니다.

시작specSHA와 네파일SHA는 ready_candidate.json에 있습니다. 위험: 1~3픽셀 성분은 HD세부이득이 제한적이며 생성물의 작은노치/내부밝은면은 원본을 연속면으로 근사합니다. 가장큰3×5성분에 새곡률이 있고 원본 끝면적은 시각적으로 확인해야 합니다. 중앙쓰기/연결/굽기/공식QA는 수행하지 않았습니다.
