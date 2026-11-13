# ground195 쐐기2 동일ID 교체 후보

상태: 미검증 그림 후보. 공식 verify_new_art/실제HD 재생 검사는 Claude 담당. 신규미연결 수에 추가하지 않는다. 라이브/코어/DB 수정없음.

- 설치입력 installation_map.json/candidate_atlas.png/native_atlas.png/contract.json/replacement_targets.json.
- 후보 SHA256 c5d82e5e1d82ec143cdbed907a74c917648d47bf828df9a1e233de51d75e6f6d.
- 교체ID는 보고서와같은1-based #92336(hash3388030118)/#92343(hash1127919949), metadata index92335/92342. source8×16/indices SHA b56c750a48b09e66d08186ad23d9f0f482307817db79ecf35225982be1aceaab 동일. 원본contract/fullactual팔레트와현재old_spec의hash/바이트/크기/팔레트 기계대조통과.
- 원본의넓은상단회색면과하단주황면을채운고형쐐기로새로그렸다. 예전의가는V/분리된검은선으로유지하지않았다. 두변형은색번호12가각각붉은색/파란색이라각실제색면으로별도제작했다. RGB/alpha 원본스탬프·기존그림재색칠없음.
- 생성 exec-3f81d32c-45dd-43cb-b650-c8ea865a63cf.png. 앞선계단도트/후광그림은거절자료로보존하고사용하지않음. current2의다른17그림은건드리지않았다.
- 생성alpha를0으로자르는문턱이나Min/Max팽창·침식없음. 정렬앵커160은물체의위치/스케일선택에만사용하며원래전체RGBA셀을변환한다. alpha<160도남긴다. OAM원래사각밖만일반캔버스scissor. 자세한crop/앵커/resize근거 alpha_and_alignment_provenance.json.
- 기존 dynamic_palette=False, resource/source좌표, RGB/indexed설정은old_spec그대로보존. 동일ID그림교체이며새바인딩ID를추가할이유없음.
- 원본unit151/152 mechanical_cutin_168.state +195, screen(192,92)/(192,94), 원본다른기체파츠의존보존. replacement_preview.png는원본/기존/새후보의제작참고이며공식판정아님.

Claude 위험: 매끈한직선대각선으로바꾸면서원본회색·검정비중/작은색번호12의노출면/주황쐐기의폭이바뀌었을수있다. lowerorange가단순대각선으로해석된부분, 양옆절단면연결, 생성AA/낮은alpha주변을실제판정해야한다. 검사를통과하거나완전히해결되었다고주장하지않는다.
