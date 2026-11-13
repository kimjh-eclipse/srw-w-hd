# IMG21934 흰 중심7 — 자동 배경 추출 문제

원본 group0 왼쪽64x64 영역의 실제7계약은단색흰빛으로속이차야합니다. 새OPAQUE그림(generated_opaque_gray/navy.png)은그조건을충족하지만 imagegen배경추출이흰내부를배경처럼지워구멍을만듭니다. 실패추출본회색/남색모두동일. 예:2172x724 원본opaque의(500,450)RGB=(254,254,254),추출RGBA=(0,0,0,0). 같은그림자체RGB/alpha만쓰려고여러회시도했고다른palettealpha나원본mask/색을복사하지않았습니다.

생성그림의나머지황백6와별도pink7은연결/굽기대상이나이7은미연결·완료수제외. source원본/실제pal/raw/좌표/전체sheet근거와프롬프트보존. 원본색번호팔레트를새그림색으로덮어수치만통과시키지않습니다.

Claude에게 기술 검토 요청: own opaque generated RGB를 유지하며 배경색만 분리할 재현 가능한 에셋 준비 방법 또는 이미지 도구의 알파 손실 경로 검토. 이것은 실제HD재생QA완료나runtime수정지시가아닙니다. source계약은held_contract_seven.json. 실패alpha를그대로연결하면안됩니다. native원본alpha를후보에찍는방법은사용하지마세요.
