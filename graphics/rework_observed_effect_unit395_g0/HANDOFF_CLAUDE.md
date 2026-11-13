# Unit395/w1565 FX group0: 노랑/주황 타격 파편3

- 실제원본 `test_current/parts/native_weapon_source_395_1565/unbound_now.json`의 source_contact indices40/41/42와52/53/54/56/57/58/59만선정. 칼/기계/greenoutline몸체와역할불명부품은제외. 실제10계약=raw10종, 실제palette2개, 단순색변형0. 10전체를phase중복으로부풀리지않음.
- 3계약, 대표 `test_current\parts\native_weapon_source_395_1565\unit395_weapon1565_source.state` +560. rendered_obj_cache actualraw/indexhash/RGBhash/전체16색palette/OAM/좌표/변환/원state를보존했고actualRGBhash재계산일치. sourceIMG소유는missingreport로확정못해 resource=None/owner_confirmed=false. x/y 및source_x/y는 가상셀원본 배치로실제ROM IMG좌표가아님.
- actual팔레트별자체새그림, 원래색유지. 다른기체/다른palette재색칠또는alpha공유없음. source bbox는위치/확대만, 자체생성cell 전체RGBA를affine등록해그림. alpha를threshold로지우거나nativeRGB/alpha mask를붙이지않음.
- candidate.png [384, 128]/native [96, 32], SHA `162c601aab3999c117db7841911970a9bf90594762be47d17b09702a3000451f`, latestexact/indexed중복0. root인수직전재대조. prepare3전부maxA>=16/support>=.1,nearblank0. 원본/후보 gray합성쌍 native_candidate_comparison.png. 제작존재/해시확인이지독립QA/실제HD판정아님.
- 알려진위험: 처음 generated_0에는 주변 검은alpha matte가 보여 rejected_black_matte_generated.png 보존하고 같은그림의배경제거tool로교정. 최종gray합성에서 검은 사각이 없어졌음. 작은 파편수/폭/색배치와 실제OAM의 위치/회전/반전은Claude실재생대기. source/sourcegrid/원생성/실패본/최종을보존. 생성은builtin imagegen.
- 라이브/library/DB/core/EXE와공유코드변경,독립audit/실제HD검증,물리입력/플레이어창조작없음.
