# 12405 바위 공유 master 교정

실제 소실 영역을 부모93132 master에서 새로 그렸습니다. 목표 자식93129/93138 외에 같은 실제source/fullpal 하위그림93134/93136도 동일master crop을 공유하도록 후보에 포함했습니다. 변경5개, 나머지5개의 다른source 그림은 그대로입니다.

master source[192,32,32,32] → atlas[96,0,32,32]. 두 약한 source범위 안14성분의 bbox자리/폭을 유지하며 자체생성원천의 crop/resize로 새 연속곡선/면음영을 그렸습니다. 같은색/모양 1px점은 같은ownRGBA를 재사용했습니다. master의 범위밖 기존왼쪽큰돌과 바깥1px점은 그대로입니다. 자식의 종전 별도그림은 부모의 같은 자체master crop으로 일관화했습니다(여기에는 미변경 기존부모 영역도 포함됩니다).

native160×96, candidate 정확4배640×384. 실제full16/BGR555·rawindex·관측frame/state·source_box/atlas_box는 최종flat계약에 보존했습니다. 시작specSHA/4파일SHA는 ready_candidate.json에 있습니다. 공유source와별도candidate좌표 및alias crop은 author_config.json/shared_master_contract.json에 명시했습니다. manual_comparison_gray.png는 원본/이전/새그림입니다.

원본RGB/alpha/mask를 출력에 전사하지 않았습니다. 생성alpha를 유지하고 출력alpha문턱삭제/형태학삭제를 하지 않았습니다. 작은1px성분은 실제성분수 유지이며 HD이득은 제한적입니다. 위험: 새 면음영의 중간농도와 밝은윗면 비율은 생성근사이고, 일부거의사각돌의 부피감이 종전보다 넓어 보일 수 있습니다. 다른source/팔레트대여는 하지 않았습니다. 중앙연결/굽기/공식QA 미수행입니다.
