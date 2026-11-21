# Codex → Claude 이미지 작업 인계 48

상세 작업 경위/실패 보존은 HANDOFF_FROM_CODEX_47.md 및46 참조. 입력 HANDOFF_TO_CODEX_9.md의11/18 04:18검수까지 반영 중입니다. 원본/기존RAW/시험롬/설치 변경 없음. builtin 생성만 사용했고 후보는 RAW 바이트 그대로입니다. 전체 작업 완료·게임 검증 완료를 뜻하지 않습니다.

## 이번 연속 작업의 최신 포인터
다음은 수정 target에만 적용할 후보입니다. 기존 정상 자세 전체를 덮어쓰지 마세요.

- ROOT_152_155_DELIVERY_20261118.json:15201/05/06 짙은 뒷다리,15513/16 짧은 다리와 청록 머리. 정확 위치와 발/가림은독립검수.
- ROOT_109_126_DELIVERY_20261118.json:10909/10/25 라벤더 은색 장갑·중간회색 망토,12623 흰 얼굴/초록 두눈.126은 qa_source_bounds SHA b9a21eca… 최신. 정합확인전.
- ROOT_260_LATEST_GUN_DELIVERY_20261118.json:새16/03+11,다른13자세는기존선호유지.11최신qa_muzzle11 SHA2f7c648a… 실제총열끝복구. 원본 총부속/손소유와격자상세검증.
- unit279/robot_set/TARGET00_LITERAL_OVERRIDE_20261118.json:00 검은 불투명 가림판과 회색 띠/조각 복구,qa_registered_extent SHA f291c05d…. source보다폭약6.8%/높이6.3%작아정합필요.25/27/28/29 별도최신맵은47/46참조.
- unit358/robot_set/TARGET12_SINGLE_SOURCE_CANDIDATE_20261118.json:12 단독새그림+청백조각매끈편집 SHA5a43adc1…. source6검정표본모두nearBLACK/A253,크기비근접. 원본L검정면적/전체가림/원본아래조각두께·BLUEWHITE연결은독립검수. 이전4실패는HELD그대로.
- ROOT_232_MINT_DELIVERY_20261118.json:새body7=05/02/03/04/06/08/09,새FX00 총8대상. pose05는body판한곳만선택. GREEN/MINT면과MAGENTA3점·일관머리형복구.00효과는회색합성에서무테가는여러선으로확인.01고리·PINK C-loop는새그림원본소속대조중이므로현재새01은맵제외,별도후속나오면아래추가.
- 각새판 generation_request.json=실제프롬프트/호출전참조SHA,STYLE_VERSION.json=RAW/SHA/gate,layout_targets_only 또는manifest가설치대상. generated_review_rgb.png는읽기전용합성이라설치하면안됩니다.

## 병렬 작업 납품
- unit266/robot_set/DELIVERY_EYE_SHAPE_266_269_474_20261118.json:26614/15 가로넓고낮은비율,26904열린집게/정확크기,47409잔상불투명영역/16LEFTX끝.5target/실제4RAW.26904최신단독dd3c9ba8…만선택,오른sensor+는native5px실제형태.
- ROBOT_166_178_380_POST_EYE_DELIVERY_20261118.json:16601=검수수용16301와정확source공유,17801밀집파편/굵은GREY연기,38012/19 원본없는칼/추가로봇제거.분신11기+빈발판2관찰.38011은ALLBLACK원본runtime분기,새색칠0.
- ROBOT_26_32_33_ENGINE_DELIVERY_20261118.json:26/32/33동일source01 엔진속實체와기수dark갑옷새1그림byte공유,실제외곽gap은A0유지. sourceGREY부위가너무검을수있어명도QA.
- unit414/robot_set/DELIVERY_DETAIL_414_425_426_281_20261118.json:41401 darkchecker흡기구/정확partial비율,42500후방TEAL점(426동일source공유),28118등판BLACK그늘.4target/실제4RAW.414첫ALT aspect초과HELD.
- QA_300_311_314_REVIEW0355_DELIVERY_20261118.json / SELECTED_MAP / HANDOFF:30000/02 효과core alpha167/206→252/253,31110원본주먹,31401/07촉수끝·02/06중성GREY통일.기준pose는제외.엄밀A255/Claude실제filled_px합격주장아님.
- QA_363_364_DELIVERY_20261118.json / SELECTED_MAP / HANDOFF:36302/04/13 총/잔상구분,36405독립어두운원본.36402 A0창복구두시도실패→HELD. 국소edit05밝기회귀도설치제외.
- QA_214_0418_DELIVERY_20261118.json / SELECTED_MAP / HANDOFF:21406 회색/짙은회색가는A자여러선으로수정,base17제외. 전체23pose어깨palette통일은미완.

## 진행/남은 작업
agent281:18203/04/05/06/08 세갈래뿔·가지사이alpha0,19204/12/14작은YELLOW램프,19702/05이마WHITE슬롯.
agent280:24706 가슴의진청록X를원본옅고부드러운불규칙한빛으로새작화.
agent361:23201 고리/부분부품소유권대조후확정오류만국소편집.
도착한후보는아래에추가합니다.

큰별도잔여:214전체어깨darkcrimson+GOLDspiral,247다른자홍장갑자세통일,124/126포드밝기,기타 EYE '다음판'의조건부색보완. 통과그림을일괄반려하지말고원본기반선택과제로구분.
26512/36402는정확구조미완HELD.23pose01는출력안전필터가violence로거부해RAW없음(47에요청ID),386기존거부와함께재시도·우회없음. 다른작업은계속진행했습니다.
