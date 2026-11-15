# 내장 생성 프롬프트 사양

전부투명배경을요청하고실제검정/#313131/#525252/#737373만사용하도록지정했습니다. 참조중간회색#808080은배경/구멍이므로투명,검정은불투명재질이라는점을강조했습니다. 원래큰덩어리/가지/구멍/채움폭/비율을유지하며픽셀미세계단과디더링은새연속lobed cloud경계로다시그릴것을요청했습니다. 가는hollow ring/wire로줄이지않고외부glow/haze/밝은테두리/흰연기/화염/색변색/추가조각/문자를금지했습니다.

- component0:넓은검정덩어리와회색infill이불규칙원형으로배치된큰연기. 큰구멍과가지위치유지,가느다란고리로바꾸지않음.
- component2:아래오른쪽notch가있는짧고굵은hook형검정/회색조각. hook방향/채움폭/회색위치유지.
- component3:긴위쪽줄기에서오른쪽두꺼운덩어리와아랫곡선으로이어지는검정조각,왼쪽큰open notch유지.
- component6:위왼쪽/아래왼쪽넓은덩어리및회색infill,오른쪽중간큰구멍주변가지의원래모양/채움폭유지.
- component8:왼쪽위curl에서큰중앙회색덩어리,오른쪽굵은black hook과아래가지로이어지는모양유지.
- component9:위왼쪽비뚤어진줄기/중앙회색패치/아래왼쪽hook/아래오른쪽가지의연결과두께유지.
- small sheet:고정4열2행의8개작은검정형상과회색패치,각cell위치와notch방향/채움폭/분리유지. 새매끈모서리,첫셀은순수불투명검정재질square. grid/text/프레임/추가조각금지.

## 94102 추가 생성 프롬프트

component8/9: 원래실루엣의가지/구멍/위치/채움폭을유지하며realistic hand-painted black smoke로새로해석.각채움을연속curl/billow/낮은명암striations로만들고geometricroundedrectangles/flatblackicons/pixelblocks/uniformtube/blurredpixelupscale금지.원래graypatch에만#313131/#525252/#737373,검정이불투명본체.외부haze/새wisp/가지/brightwhite rim/색/불/점/문자금지.
small2x2:원래4개작은형상의방향/폭/notch/cell위치유지.내부말린연기결과연속작은billow경계,검정위주/첫cell원래회색부분에만작은gray.각cell하나의연결성분.도트업스케일/geometryicon/thincurl/외부haze/glow/추가조각/문자/grid금지.
