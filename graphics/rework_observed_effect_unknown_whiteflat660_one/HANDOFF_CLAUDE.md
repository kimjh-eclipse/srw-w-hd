# unit48+660 불투명 흰 면 1 (IMG소유 미확정)

- actual source `test_current/parts/native_weapon_source_48_214/unit48_actual_unknown.json`, source.state+660, engine0/OAM32/screen83,88/priority2/mode0. raw32×32 전부 index1, actualRGB[255,255,255],사각전체불투명.
- actual RGB hash1064685919/indexhash3091307759. 최신live exact=[],indexed=[]. 연결이있으면보존/중복등록금지.
- resource=None/owner_confirmed=false/source_candidate_matches=[]。IMG20348 raw에는같은32×32흰원본영역이없어20348로귀속시키지않음. cached출처/전체palette/OAM/bytes는계약에보존.
- 자체 신규 imagegen으로흰색불투명색면생성(generated_white_opaque.png). 원생성은RGB253~255 미세변동,alpha255였음. 균일 white plane필요라 **자체생성의RGBA255연속구역** crop[1253, 132, 1254, 178] (1×46)만 추출하여128×128로resize. crop이원출력오른쪽끝에있다는점도기록; 원본RGBA/원본alpha를복사하거나코드로255칠하지않음. 다른효과/다른색재사용없음. 단색평면이라별도실루엣디테일이없음.
- candidate.png SHA `8d349688908058ccc7166eafeb5053d149c88648057947b7ece38d15165ebe6c`,128×128 /native32×32. candidate/prepare 전체 RGBA[255,255,255,255], minA255,opaque비율100%,reference_fill0/성분제거0/인공절단선0.
- 이확인은생산입력/존재/색면opacity계수이며실제HD재생검증아님. Claude는원state+660에서이흰면의역할·크기·앞뒤순서·시야클리핑확인. 소유IMG불명인기계조각에이처리를확대적용하지않음.
- live/library/DB/core/QA/실재생없음.
