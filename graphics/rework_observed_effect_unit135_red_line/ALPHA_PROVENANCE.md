# Unit135/w563 가는빨간연출선1

- 제작source: borrowed_shape_rework/unit135_laserline_source_for_fx/ROOT_FX_SOURCE_HANDOFF.md와contract.json. 실제source_mechanical_fixed_135_563_350/source_pose.state+0/OAM15. hash2979222028/index3720258710,32x8,opaque43. IMG10443(64,16)바이트일치,실제팔레트소유를추정하지않고resourceNone/ownerfalse 유지. virtual40grid/native40x40에실부품32x8을배치.
- 실제raw/index/전체16palette/RGBhash/원state/OAM/변환은new_candidate_contract.json. builtinimagegen 자체새RGBA로 생성. 위치·확대만nativebbox에등록;원본RGB/alpha전사·색강제채움·다른그림alpha공유없음. 떨어진 검정흔적도삭제하지않음.
- candidateSHA 8b4dfa99c0c746539af8eb416bcca2a9b63ccae73bd0aff7c2bab5a6ff95f7f3;4배160x160. actualRGBhash재계산일치,preparemaxA>=16/support>.1,최신exact/indexed중복0. 이는제작존재만,실재생QA아님.
- 원본은좌측어두운가로선+빨강짧은부분+오렌지점과오른쪽별도검정선인데생성본은왼쪽이약간날카로운번개처럼매끈해졌고오렌지영역이늘었을수있음. 원본43texel매우얇은선이므로실제확대시두께/색영역/연결성분을Claude가원state+0에서비교해야함. native_candidate_comparison.png준비.
- 라이브/library/DB/core/EXE/공유코드와물리입력변경없음.
