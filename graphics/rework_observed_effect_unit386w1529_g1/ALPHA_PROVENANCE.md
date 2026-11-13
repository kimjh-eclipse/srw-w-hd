# Unit386/w1529 실제 점멸·민트6 중group1

- 실제cached8계약에서고유raw6만새그림. 흰점멸4(sourcecontact2/3/4/5,frame505/520/525/530),민트선·쐐기2(contact8/9,frame575). 580의동일raw2는팔레트phase로별도보류. source unit386_1529_input/selected_actual_fx_contracts.json. 실제RGBhash 재계산/used색/원본index/16palette/OAM/좌표/변환/fixture보존.
- ROM missingreport IMG 바이트연결원본은확정못해resourceNone/ownerfalse. x/y는가상40/72셀좌표로ROM좌표아님. actual cached원본으로역할분리:기계/기체몸체는제외. 이group1 2계약. 같은원본의다른팔레트를기존그림재색칠로채우지않고실제palette별새그림.
- builtinimagegen자체RGBA,4배생성등록. 자체alpha32bbox위치/크기만nativebbox기준이고nativeRGB/alpha전사없음. 다른그림alpha공유/단색native색코드채움없음. 흰단색사각·원형절단면4도누락하지않음.
- candidate SHA5ce8c532c2ffbc45bd8cd186560348e17bbc1b8f021a1634034d1ccdbcb2341a/size[576, 288]. prepare전부maxA>=16/support>.1/nearblank0;latestdup0. g0원본밝은14,016샘플alpha<16=0%,중앙alpha254중앙값. g1밝은1,760샘플alpha<16=6.8%로형상끝/틈차이남음;중앙253이고큰핵구멍으로보이진않지만실재생판정대기.
- 알려진위험:g0외곽의원래단계형선은여전히각진절단면을유지하고내부명암이미세추가됐음. g1민트쐐기/가로선연결성분은원본보다날카롭고층별미세틈차이. sourcefragment실제물리조립은검증안했으며frame505~580에서원본/HD크롭과밝기·색·레이어는Claude대기. native_candidate_comparison.png.
- root만라이브/굽기. 독립QA/실제HD재생/공유코드/DB/물리입력변경없음.
