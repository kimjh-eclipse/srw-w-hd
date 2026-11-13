# 17168 패널형 오브젝트4종 제작 인계

- unit348 / weapon1400. source_pose.state load 뒤 run1회(offset0)의 캐시 계약. isolated RAM preview, ROM/저장파일 변경없음. 기본코어 a6d80b29.
- ROM IMG17168 원본색번호를 직접 대조: OAM0=(48,48,32,32),1=(0,48,64,32),2=(48,0,32,64),3=(0,0,64,64). 네 crop 전부 원본indices exact. 가로·세로16px 겹침이 있는 하나의80×80원본 영역.
- 이80×80전체를 하나의새그림으로그린뒤동일좌표에서읽도록함. 독립그림4장으로겹침/선굵기차이를만들지않음. nativeRGB/alpha stamp, 다른그림재색칠없음. 생성alpha그대로4배320×320로축소.
- 생성도구built-in image_gen, source_union_reference.png를참조. panel_generated.png가생성원본. 고해상도자홍색/분홍-흰전면,짙은측면·수평전기무늬를원본시점으로지시. 프롬프트는generation_provenance.json.
- 각cached원본binding0이고제작전exact/indexed미연결. 패널형오브젝트이나기체본체/효과의의미분류는미확정이므로effect_part태그는넣지않고actual palette고정. Claude가순수원본과역할/가림·core보호룰을봐야함.
- Claude검증: source_pose.state+0 및전후동작. 두꺼운실제검은경계/파츠절단선오인,겹침16px접합,배경키색잔여,원본대비너무정돈된무늬/단색gradient·하단밝기,affine변형·대사창가림. framebuffer_hd_enabled는순수원본증거가아님. 독립QA/후보HD재생미실행.
