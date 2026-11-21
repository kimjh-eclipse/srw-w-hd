# 2026-11-21 재작화 인계

최신 요청은 HANDOFF_TO_CODEX_10.md의 196 시범 및 심한 151기체 재작화다. 이전 HANDOFF_FROM_CODEX_55.md와 컷인 원장은 보존한다.

- 우선 196의 pose_00·04·09·05를 같은 판에서 그린다. 네 자세의 원본4x 위치·크기를 유지한 판과 실제4xBRZ를 준비했다. RAW는 변경 없이 전달하며, Claude가 원본 파츠 칸과 대조해 시범 확인 후 나머지를 진행한다.
- 번호 정정: 실제 ATLAS·contract 기준 pose_00·04·09의 공통 앞머리는 #14, pose_05는 #5다. REQUEST.md의 모든 머리 #5 예시는 현 자료와 다르다. 원본 자료는 수정하지 않았다. 증거는 `_codex_20261121/unit_196_pilot/PART_ID_CHECK.json`.
- 공유 파츠의 모양·크기·색·명암·뒤집힘·가림, 특히 #14의 3회 사용을 확인할 것. #5를 첫 세 자세에 강제로 사용하지 않는다. pose_05의 #21 가림도 보존한다.
- 기존 candidate·candidate_fit·설치 파일은 수정하지 않는다. 새 시범 판은 `test_current/parts/redraw_requests/_codex_20261121/unit_196_pilot/`에 별도 전달한다. 비율·해상도 점검은 구조 합격이 아니며, 전체 그림과 실제 파츠 재조립을 Claude가 확인한다.
- 151기체 자료 검사는 별도 원장에 기록한다. 시범 확인 전에 151기체 전체를 무작정 생성하지 않는다.

## 진행

196 시범: 원본 판·실제4xBRZ·개별 머리·조립 가이드로 새4자세 RAW 전달. 파츠 재조립 검증 대기. 컷인23514도 웃는 원본 표정으로 새RAW 전달.

## 2026-11-21T09:59:00.157079+09:00 151기체 자료 검사 (읽기 전용)

- _codex_20261121/REDRAW_INVENTORY_20261121_095326.json:151/151기체,2934자세,기체별파트번호합계12651,요청폴더3539파일. 원본/조립guide/ATLAS/contract/source 누락0,atlas hash+size와posecontract 불일치0. 각원본SHA/치수/우선순위 기록.
- _codex_20261121/SAME_HASH_USED_PALETTE_READONLY_20261121.json:15기체의동일hash·다른전체팔레트벡터를실제index_pixels+original_palette_rgb로재구성해비교. 사용된불투명RGBA충돌0,해석오류0. 사용하지않은팔레트차이로재색칠하지말것.
- 196시범4자세확인후2930자세남음. 기체별최대9자세묶음은전체389판. 이집계는이번151기체범위만이며그림합격/설치완료아님. 23/95/386요청폴더는이151개에없고기존정책보류는손대지않음.
- 상세설명: _codex_20261121/REDRAW_INVENTORY_NOTES_20261121_095326.md. 이미지생성/원본픽셀수정/candidate/ROM/라이브러리변경없음.

## 196 시범4자세 RAW 전달

- 저장: test_current/parts/redraw_requests/_codex_20261121/unit_196_pilot/RAW_imagegen.png
- SHA256 ea4bebad791d694f4f5457f17b8814361f257baf2bd45271b1878c4c16b7560a. 실제1464×1074, 원본판1200×880. 생성RAW 리사이즈·크롭·재색칠·알파수정 없음. 기존 candidate·설치파일 덮어쓰기 없음.
- 좌상00/우상04/좌하09/우하05. 원본4x캔버스 각각540×340,508×364,452×344,396×376, 요청판 원점(30,50)/(646,38)/(74,488)/(702,472). layout_snapshot.json의 좌표를 실제RAW 크기에 맞춰 Claude가 정합한다. 비율gatePASS는 구조·픽셀정합 승인 아님.
- Claude 검증: 공유#14 머리의3회 재사용 형태·크기·명암, #5 별도변형과05의#21가림, 공유22종 파츠의 원본 칸 대응, 클로·팔·다리·뒤장갑의 위치와크기, 주황/황색 눈과cyan센서·darkjaw 보존, 실루엣밖4px이내와alpha0·외곽잔여.
- 엄격한 동일파츠 재조립 합격은 미확인. 시범 확인결과를 파츠번호·자세·칸으로 회신받기 전 151기체 나머지2930자세 대량생성은 진행하지 않는다. 새로 그렸으며 다른 그림을 재색칠하지 않았다.
- 최종프롬프트·5개참조SHA·원본계약SHA는 generation_request_visual.json/DELIVERY.json. 첫8참조 요청은 도구5개 제한으로 생성전 거절되어, source-only 파츠칸 안내판으로 정리 후 성공했다.


## 2026-11-21T10:04:31.631784+09:00 23514 웃는 표정 새작화 전달

- 최신 TO_CODEX10의 23514 재작화 요청을 처리했다. 이전 HD 연결 제외 사유였던 원본 웃는 입을 기준으로, 내장 imagegen에서 새로 그렸다.
- 경로: test_current/parts/redraw_requests/_codex_20261121/cutin_23514/RAW_imagegen.png. SHA256 34015bd56eb489bbedc7cffc7979d9b48c021000411f80b385e8358320edaade. 출력1774x887, 요청1024x512와비율동일, 실제전체A255. RAW는복사만했으며크기변경/재색칠/알파수정/합성없음.
- 원본512x512 중 native[0,0,256,128] 얼굴그림만 독립 전달. dialogueHUD y256..320 제외, 복원4x원점[0,0]. 이 원본사각형자체전부A255여서 투명요청false가정확함. 원본의 알파0영역을 채운것이아님.
- generation_request_visual.json에최종프롬프트/원본·실제4xBRZ·웃는입원본확대의SHA/layout/INDEX계약 저장. DELIVERY_20261121.json 및 READONLY_SMILE_VALIDATION.json 추가. 원본/입력/RAW SHA모두검증.
- 검토관찰: 올라간입꼬리와벌어진붉은입술, 한줄의흰윗니면, 분홍아랫입술, 빨간눈동자 유지. 무표정·찡그림·크게외치는입이아님.
- Claude검증: 원본웃는입의정확한폭·곡률·위치와치아띠, 눈/눈썹/볼비율, 원본회색투구·노란테두리·보라칼라색, 상하원본클립과native4x정합, 실제전투컷인연결/맵지문/표정. 비율PASS와시각관찰은원본칸정합/설치승인이아님. candidate/ROM/라이브러리는수정하지않았다.

## 2026-11-21T10:07:29.616370+09:00 196 시범 RAW 원본 정합 읽기검사

- _codex_20261121/unit_196_pilot/READONLY_PILOT_SOURCEFIT.json: source1200x880 대비 RAW1464x1074를 픽셀 중심좌표의 배열 샘플링으로만 비교. 생성이미지 resize/crop/mask/재색칠/출력raster 저장 없음. RAW SHA 전후 동일. 각자세를 따로 이동/축소해 불일치를 숨기지 않음.
- pose00/04/09/05 순서: 원본지지영역 대비 IoU 0.6925/0.6760/0.6247/0.6651, 실제A>200 그림면적 원본의1.291/1.356/1.271/1.332배. 원본4px확장영역 밖 실제그림 비율17.08/18.80/20.86/21.37%. 원본4px수축내부 미대응2.44/1.37/7.17/2.38%.
- 같은순서 bbox확장[L,T,R,B], 단위원본4x픽셀: [27,24,24,0], [46,21,17,2], [37,30,18,-8], [37,33,7,4]. 특히 왼쪽클로/몸통과상단이커지고밀렸으므로 단순4px테두리 차이가 아님. 원본칸위치와크기수정 필요.
- 공통#14가최종원본에서도같이보이는4784샘플만비교. RAW세자세의같은로컬좌표에서 RGB채널평균절대차이76.5/86.8/52.0, 쌍별RGB거리64초과46.6~76.0%. 세자세모두해당머리영역은불투명하지만 원본cyan세부의고정위치가RAW에서는회색등으로나와정합되지않음. cyan색이전체그림에서없다는뜻이아니라원본디테일위치가맞지않는다는뜻.
- 이지표는명암·안티앨리어싱위상·원본가림판별근사도포함한진단이며부분공유합격판정아님. 화풍은별도로검토가능하나151기체확대전원본파트칸/머리크기와위치/공유명암을교정하고실제파츠재조립검증 필요.

## 196 시범 고해상도 개별 전체자세4RAW 추가

- PILOT_SINGLE_POSES_DELIVERY.json: single_pose00/04/09/05에각자완전조립된새RAW저장. 파츠분해그림을생성한것이아니며각자세원본칸/자기색/실제4xBRZ/머리원본으로전체를새작화. 동일sourcehead14는00·04·09,05는5.
- 기존한판RAW두버전은크기·위치·공용파츠정합부족이확인되어geometryHOLD. 현재개별고해상도4개를우선검토,원본당좌표는각layout에기록.
- 00새RAW4dcc72dc...fb4ae,1581×995. 정규화읽기검사 IoU0.93356,원본4px밖0.033%,core누락0,원본bbox[36,40,480,284] vsRAW정규화[36,39,485,283]. 실제공유파츠동일/4px엄격승인아님.
- 04 SHA976f0f66...391c,1481×1062;09 SHA7ebd3cc0...e293,1437×1095;05 SHA235036dc...55fd,1287×1222.05의노란선계단은추가imagegen국소매끈화중.
- 모든RAW원본보존,리사이즈·합성·크롭·재색칠·알파수정없음. Claude가native4x로정합/조각추출/공유파트1원본재사용/가림/재조립검증후시범확인요청. 같은파트를자세마다다른정체성으로교체하지말것. 나머지2930자세는시범확인전생성안함.

## 2026-11-21T10:21:35.095152+09:00 196 독립 전체자세4장 읽기정합 검사

- _codex_20261121/unit_196_pilot/READONLY_SINGLE_PILOT_SOURCEFIT.json: 독립single_pose00/04/09/05의각원본native4x와대응RAW를좌표배열샘플링만으로비교. 원본마스크에만4px확장·수축사용, 개별머리이동/확대축소로오차보정안함. 생성이미지변경/변환raster저장없음, RAW4개SHA전후동일. 기존single00 READONLY_SOURCEFIT.json은보존.
- 00/04/09/05 순 IoU=0.933556/0.789993/0.803089/0.854906, outside4비율=0.0334%/1.8909%/3.2156%/1.5800%, 원본내부누락=0%/4.4535%/2.8354%/0.7860%. 그림면적비=1.0274/0.9872/1.0079/1.0313. 첫4자세판보다전체크기·위치가크게개선됨.
- 같은순서bbox확장[L,T,R,B],원본4x픽셀: [0,1,5,-1]/[0,6,-3,-11]/[10,3,-8,-8]/[2,10,3,-5]. 아직04/09내부파트위치·두께정합과05상단/줄마감확인필요.
- 공유#14의공통원본가시4784샘플 비교: 새HD끼리 RGB채널평균절대차이66.9/83.9/74.4(00-04/00-09/04-09). 원본고정cyan위치32샘플의cyan색유지비율00=71.9%,04=0%,09=0%; 원본yellow96샘플의yellow유지00=81.25%,04=18.75%,09=0%. 색이그림전체에서사라졌다는뜻이아니라04/09의세부위치가고정원본칸과맞지않는다는경고. AA·명암·샘플위상도포함한진단이지자동합격판정아님.
- Claude: 원본공유#14칸의세부위치/같은번호일관성과실제파츠재조립확인후151확대판단. 네개의pretty실루엣만으로공유파트문제해결이라판정하지말것. pose05노란줄계단은부모가별도targetededit진행중이며이검사는원래single05RAW만대상.


## 11/21 20:30 최신 확대 지시 반영 및 수정본 즉시 전달
- TO10 최신 확대승인 확인: 이전 pilot gate는 해제. 196 남은자세 후 HEAVY_151 순서로 전체자세를 개별wholepose로 계속생성.
- 04 공유머리#14·앞집게 수정 RAW: `_codex_20261121/unit_196_pilot/single_pose04/shared_parts_retry/RAW_imagegen.png`, SHA 9ce798ddbef6d3ec4ca05cdb11861f1b57bb6bd8ddcf06f84036e690e5c88699, 1482x1062. 원본508x364 및 기존 layout 기준. canonical00 머리위치에서 y-32로 요청했으나 생성이 동일픽셀 재사용을 보장하지 않으므로 실제공유머리/집게 잘라 재조립 필수. 수정수령이지 접합합격 아님.
- 05 노란줄무늬 smoothing RAW: `single_pose05/stripe_smooth/RAW_imagegen.png`, SHA16a217d4366699e92c70537ef5d1bca3f2c263af64a1e90050855dad21897458,1287x1222. 가는노란곡선 계단현상 개선, 원본geometry·05고유머리#5/21가림 검증. 원RAW 모두보존.
- 원4pose판/geometry_retry는 형상HOLD이고 현재납품은 single_pose별. 00·09·05는 Claude가 조립상통한다고보고,04 위수정본 재검증요청. 이전read-only공유디테일불일치지표는 미해결확인항목으로유지.
- 01·02는 subagent,03·06·07·08·10·11 root준비. 23299및새컷인별도agent병행.


## 2026-11-21T20:31:10.941906+09:00 23317 원본팔레트 충돌 — 실제원본확인요청

- 최신 TO_CODEX10는23317도회색·초록보석이라하지만 실제batch G055/23317_canvas.png와23317_screen.png는모두금색·노란얼굴/투구와초록보석, 주황장갑이다. 23315/23316도전체canvas RGBA가23317과동일해회색원본이아니다.
- 증거: test_current/parts/redraw_requests/_codex_20261121/cutin_23317/SOURCE_PALETTE_CONFLICT.json. 23317 원본PNG SHA52a6a7ff3b31db804e5aedc8462bac3f190fc9a7a0c84840ec765e97dd740f6f,전체RGBA SHA23a698399624dd44562e362069bb1f9318ddd487825eccbc9a315db5caf3cdca. 가장많은금색RGBA(238,230,0,255)3962픽셀.
- Claude: 정확한해당장면을확인하고 회색이의도라면그장면의실제회색팔레트원본을다시제공할것. 금색native나기존HD를임의회색재색칠하지않았다. 23317imagegen미호출,원본/기존그림/설치변경없음.
- 23299는실제회색원본과문서가일치하여원본+actual4xBRZ+회색머리원본확대3참조로독립새작화진행.

- 20:33 196 pose03 wholepose RAW 즉시전달: single_pose03/RAW_imagegen.png, SHA7324680e0e888da1085409a9f01b84018598eab828d75a701689b4a08c07c4be,1058x1487; logical296x416. 머리·교차상단블레이드·양발 접합/공유part칸 검증 요청. native/real4xBRZ/partbox/style refs와 prompt/layout 저장. 생성RAW 무변환.


## 2026-11-21T20:32:34.110276+09:00 23299 회색머리·초록보석 새작화 전달

- test_current/parts/redraw_requests/_codex_20261121/cutin_23299/RAW_imagegen.png. 내장imagegen독립새작화, 기존금색HD재색칠아님. SHA256 ddc90a5b59fab1c87b566305d91a951c6ce05c1a1fe7f4452f6e94e9969cfa9d, 출력1672x941/요청1024x576,비율gatePASS, actualalpha0..255. 생성RAW변경없음.
- 원본native256x256의모든실제paint를포함하는bbox[0,0,256,144]만source-only crop했다. 4x원점[0,0], full1024x1024canvas로복원필요. nativey144아래는모두원래alpha0이며누락paint없음.
- 시각관찰: 회색투구/은회색각진얼굴mask, 이마초록보석·원본분홍eye slit 유지. 원본에합법적으로있는오른쪽노랑vent/왼쪽파랑·빨강어깨/아래얇은노랑cheststrip도유지. 머리를금색으로그리지않음.
- generation_request_visual.json에최종프롬프트/원본SHA/real4xBRZ/머리원본확대/INDEX계약/layout저장. DELIVERY_20261121.json과원본기준읽기전용alpha진단추가. 원본·참조·RAW SHA검증.
- Claude: 정확원본머리·gem·눈·턱plate각도/크기/위치, vent검은slot개수와clip, 실제원본팔레트/알파0및opaque검은면, fullcanvas복원과게임컷인연결확인. 비율gate와시각관찰은정합·설치승인아님. candidate/ROM/라이브러리변경없음.

## 2026-11-21T20:34:48.897284+09:00 196 pose01/02 전체 새작화2RAW 전달

- _codex_20261121/unit_196_pilot/AGENT_01_02_DELIVERY.json:각자기원본native4x+실제4xBRZ+원본파트칸+자기head파트원본+single00HD화풍(디자인복사금지)을보고내장imagegen으로각각전체자세새작화. 01=1324x1188 SHA f63612d0...08317d,02=1280x1229 SHA9261cffc...d7b9b9. 각폴더request/DELIVERY에최종prompt/promptSHA/원본·참조·layoutSHA/RAW경로기록. 기존파일/candidate/ROM/라이브러리변경없음.
- 01은head5의쪼그린앞3/4자세,02는head7대부분가려진뒷모습과위로올린클로:눈/앞얼굴새로추가하지않음. 각원본칸위치와팔레트,공유번호·뒤집힘/가림을Claude재조립확인할것.
- 읽기전용정규화샘플진단:01 IoU0.88818/outside4 0.1157%/내부누락1.4505%,02 IoU0.80721/outside4 2.4768%/내부누락5.5021%. 아래쪽bbox가원본보다01은10px,02는13px짧아발/등핀·클로끝과원본파트칸정합주의. 비율gatePASS는구조합격아님. RAW각SHA전후동일,생성그림크롭/리사이즈/재색칠/알파수정없음.


## 2026-11-21T20:36:37.053676+09:00 196전체12자세 RAW전달 색인(설치확인아님)
- `C:\Emul\Workshop\SRW_W_HD\test_current\parts\redraw_requests\_codex_20261121\unit_196_pilot\UNIT_196_WHOLEPOSE_DELIVERY.json`에 최신preferred RAW/크기/layout/request/SHA 저장. 실제RAW 12장, 각자세wholepose 한장씩, 투명alpha유지.
- pose_00: `single_pose00\RAW_imagegen.png`, SHA 4dcc72dc46b901f24fa480f2d9e180eb5c1ebda047a5b5e32f9316d11f9fb4ae, 크기[1581, 995] → native4x[540, 340] layout.
- pose_01: `single_pose01\RAW_imagegen.png`, SHA f63612d06363b63b11d4a8534943f54464476685bd8e00c8c2485c5e7d08317d, 크기[1324, 1188] → native4x[348, 312] layout.
- pose_02: `single_pose02\RAW_imagegen.png`, SHA 9261cffc3003c0d54ae1f56c1c4e80f3636e39f76915d1f7d33b6184fed7b9b9, 크기[1280, 1229] → native4x[396, 380] layout.
- pose_03: `single_pose03\RAW_imagegen.png`, SHA 7324680e0e888da1085409a9f01b84018598eab828d75a701689b4a08c07c4be, 크기[1058, 1487] → native4x[296, 416] layout.
- pose_04: `single_pose04\shared_parts_retry\RAW_imagegen.png`, SHA 9ce798ddbef6d3ec4ca05cdb11861f1b57bb6bd8ddcf06f84036e690e5c88699, 크기[1482, 1062] → native4x[508, 364] layout.
- pose_05: `single_pose05\stripe_smooth\RAW_imagegen.png`, SHA 16a217d4366699e92c70537ef5d1bca3f2c263af64a1e90050855dad21897458, 크기[1287, 1222] → native4x[396, 376] layout.
- pose_06: `single_pose06\RAW_imagegen.png`, SHA 676166217c3d38b7b739ed33617a7faf8dcfbb30a9665d2b61d4f3662f7650d7, 크기[1193, 1319] → native4x[340, 376] layout.
- pose_07: `single_pose07\RAW_imagegen.png`, SHA 1df3f02528a7200e04b0c9e6e91aaea7c1c2d35314547e5d5a9b02fadf32c531, 크기[1093, 1438] → native4x[292, 384] layout.
- pose_08: `single_pose08\RAW_imagegen.png`, SHA 2b43533f5a8ec404035597668f191cadbd3e485ee9be30fd0deeaf3cfcf65571, 크기[1474, 1067] → native4x[420, 304] layout.
- pose_09: `single_pose09\RAW_imagegen.png`, SHA 7ebd3cc07c679281fec543a51bda00fd8a4b6afb169518d8eca904367a85e293, 크기[1437, 1095] → native4x[452, 344] layout.
- pose_10: `single_pose10\RAW_imagegen.png`, SHA 849a375f37d784b121e5dbb00ebf54888a7b89b43325545134ae5a6ec8250b94, 크기[1458, 1079] → native4x[400, 296] layout.
- pose_11: `single_pose11\RAW_imagegen.png`, SHA 41a411d213a56517201c4e5b0a63b630e5301d52f3f847579817afd87bdb86ca, 크기[1370, 1148] → native4x[420, 352] layout.
- Claude 검증: 원본파츠칸 내부상세(눈/센서/노란띠), 공통part 원본flip, head14(00/04/09) 동일성,05head5/21가림,02뒷모습에앞얼굴생성안됨,03·11교차블레이드접합,팔/다리/집게끝 실루엣·알파. 04수정본도 동일픽셀재사용 보장안되므로 잘라조립후확인. 형식gate는 기하/파츠검증합격을뜻하지않음.
- 다음: HEAVY_151 순서120부터 기준wholepose시작(agent). 나머지기체목록은 계속갱신.

- 314 기준pose00 새RAW: `_codex_20261121/unit_314/single_pose00/RAW_imagegen.png`, SHA65726f139e62866bed28805abc1551c2d03bbc2406cac10c5e8a2bd4a2d452d7,1426x1103→logical440x340. 기존cool silver갈기를 원본warmkhaki/tangrey로 새로작화; green얼굴·magenta갈기·yellow눈·greenserpent 원본위치/공유part및얼굴세부 대조검증요청. 스타일양호하나nativefixedpartshape완전일치보장안됨.


### 2026-11-21 unit120 canonical pose00 새 wholepose 전달
- RAW: 	est_current/parts/redraw_requests/_codex_20261121/unit_120_redraw/single_pose00/RAW_imagegen.png, 1188×1324, SHA256 8342d277d282f5f72fa0353fdc63cd3476c026a7ff027121cc71b8b14de8b22a. 원본/native4x+real4xBRZ+source-only boxes+head10, 부드러운 선과 쨍한 원래 주황/검은 모노아이/초록 crest로 재작화. 기존 candidate와 ROM 미변경, 생성 RAW 변형 없음.
- 읽기전용 좌표 샘플 진단: IoU 0.92822, outside4 0.00012, missingInner 0.00344. 실제 파츠칸/동일ID/머리/포즈 조립 검수는 Claude 대기(설치 승인 아님).
- 최신 확대 승인 적용. 나머지120은 이 새00의 기체 정체성/화풍을 참고하고 각각 자기 원본 위치/크기/색을 우선함.


## 2026-11-21T20:41:13.610927+09:00 311 지옥왕고든 기준pose00 즉시전달
- 최신 RAW: `test_current/parts/redraw_requests/_codex_20261121/unit_311/single_pose00/smooth_redraw/RAW_imagegen.png`,SHA e754f6c51703683b66c95fbe483f97a1396da8101c7632a0932f6436a728d92a,1235x1274,logical388x400. builtin imagegen. Smooth HD 재작화 확보; 최초 single_pose00/RAW는 enlargedpixelstyle로 STYLE_HOLD, 기준으로쓰지않음. 원RAW보존.
- native/real4xBRZ/파츠칸/원atlas/style참고와 최종prompt/hash/layout/DELIVERY 저장. 생성후픽셀무변환.
- Claude 검증: 네팔의손/손목/소매칸 위치, #1머리뿔·눈·붉은수염띠,흰수염·턱조각,망토/구두 외곽과투명빈칸,공유part잘라재조립. 요청원본에는 기계흰수염이실재하므로 임의인간얼굴아님. 형식gatePASS는조립합격아님.
- unit311 전체17자세 원본과실제4xBRZ/partbox/layout 준비. 다음01부터새smooth00기준으로계속.

- 314 pose00/01/02 RAW 및기체DELIVERY.json 즉시저장: 원본partbox,actual4xBRZ,canonical00기준. 01/02 새그림도warmkhaki갈기. 긴왼쪽촉수pose02는원본위치·두께·길이/연결부 검증. 파일별SHA/prompt/layout은unit_314/DELIVERY.json과각single_poseNN/DELIVERY.json. 설치검증아님.

- 311 pose01 뒷면 RAW 즉시전달: single_pose01/RAW_imagegen.png, SHA c9b23591fa6b5738e5f06dc6f84a25f979c3033105a1d58326fd0889992b16e3,1240x1268→logical364x372. 원본뒷모습/흰푸른뒤털/붉은망토, 앞눈얼굴추가없음. 손·소매·뒤털파츠칸 정확도/alpha와팔가림 검증요청. 생성후RAW무변환.


## 2026-11-21T20:43:45.902379+09:00 23076·24640 새작화/검증 및 컷인 색인

- 컷인색인: _codex_20261121/CUTIN_REDRAW_DELIVERY_23514_23299_23317_23076_24640.json. 각RAW/프롬프트/SHA/layout/상태링크.23514는최신TO10기준Claude연결완료,23299와24640은새RAW검증대기,23317은원본색충돌,23076은불투명검은면alpha복원검증HOLD.
- 24640: cutin_24640/RAW_imagegen.png SHA3e2063bfe09d7820a61bc7cc042062f1c8c7877f80d1c3bd363b79a4990b23cf,1774x887gatePASS. 실제sourceuppernative[0,0,256,128]의darkgrey/purple불규칙바위opening만새작화. Screenshot로봇/번개/흰파편은다른layer라그리지않음. source25pxerode12333내부표본lowA0%,outside12054 highA0%. 정확opening곡선/원본clipping/회보라팔레트/알파/게임레이어연결은Claude검증. 아래HUD제외partial이며full2048square원점0복원필요.
- 23076: cutin_23076/RAW_imagegen.png SHA4a264e88b63538bf1105463830470e695d0792d956742fb5382eafd7d96478da,1254squaregatePASS. 상반신본체의pink흉부/회색기계/붉고노란큰어깨와원본하반부green16scanlinebands를동일wholelayer로새작화. 원본외부를채운것은아님.
- 중요23076 HOLD: originalopaqueBLACK(0,0,0,255)와nearblack(8,0,0,255)이배경으로제거됨. 전체source25px-erode normalizedpaint lowA6.524%, dense검사누락색중순수opaqueBLACK23932점이대부분. 원본의검은면과alpha0빈영역을구분해야함. 하반부greenbands는native1px-erode9488core모두A>=200이나경계/alpha0틈/정확한16줄주기확인필요.
- READONLY_OPACITY_AND_SCANLINE_DIAGNOSTIC.json 및 SOURCE_ONLY_OPAQUE_BLACK_MATERIAL_MASK_NN4.png, opacity_retry_01/SOURCE_OPACITY_MAP_guidance_only.png에원본알파판정자료. 이들은SOURCE-only분석/가이드이며새그림이나RAW가아님. 추가imagegen호출은하지않고technicalalpha복원을Claude에게넘김. 기존RAW에alpha마스크나색수정을적용하지않음. 원본[0,0,256,256]에서그대로4x복원후본문검은면/stripegap알파와MAP레이어게임확인필수.
- 내장imagegen사용, 모든생성RAW는즉시프로젝트복사/SHA검증. 생성이미지crop/resize/recolor/alpha수정/합성/candidate/ROM/라이브러리변경없음.


### 2026-11-21T20:43:58.710147+09:00 unit120 추가 RAW 전달
- pose01: RAW_imagegen.png, [1289, 1220], SHA256 7ccc2637ac51927b064aeb14718752d931f96ca7d9f39769761a572af0e6dd87; IoU 0.91069, outside4 0.00724, missingInner 0.00154. 위치: test_current/parts/redraw_requests/_codex_20261121/unit_120_redraw/single_pose01/
- pose02: RAW_imagegen.png, [1117, 1409], SHA256 8a3dc9b69483bd06a4ca6dd76dc5bbe0606964290950c49881e802b0bdd35485; IoU 0.84205, outside4 0.01957, missingInner 0.03296. 위치: test_current/parts/redraw_requests/_codex_20261121/unit_120_redraw/single_pose02/
- native/실제4xBRZ/source-only boxes/원본 headpart + 새12000 HD 기준. 생성 RAW 무변형 보존, 기존 candidate/ROM 미변경. Claude 원본 파츠 칸/공유ID/가림/팔레트/조립 검수 대기, 자동 합격 아님.

- 311 pose02·03 RAW 추가전달. C:\Emul\Workshop\SRW_W_HD\test_current\parts\redraw_requests\_codex_20261121\unit_311\DELIVERY.json 최신색인. 02 SHA e0a7819903bd5a5f776838f88d4ccfdb20469352ea1f7ca93e69496e86f7f4a9,1313x1198→408x372;03 SHA dd77a6024ee98134ebc64982664bbb79bdfe3a2e14fc6601e97ba75b73101c7b,1282x1227→372x356. smooth00기준, 원본각자세의입모양/수염/손가림/망토와공유part칸 확인요청. 총4/17자세RAW,설치확인아님.

- 2026-11-21T20:45:46.096750+09:00 병렬수령실황: unit_196_pilot 12자세 RAW, unit_120_redraw 5자세 RAW, unit_314 7자세 RAW, unit_311 5자세 RAW. `LIVE_WHOLEPOSE_RECEIPT_INDEX.json` 파일별SHA/layout기록. 314 00..06까지원본매칭검증필요, 나머지이어작화. 설치/승인수치아님.


### 2026-11-21T20:45:50.484018+09:00 unit120 추가 RAW 전달
- pose03: RAW_imagegen.png, [1154, 1363], SHA256 449e2570ce8933c89cfda0d302e0839ec12c575e6d7f721966b2ef48c1936f71; IoU 0.74539, outside4 0.07429, missingInner 0.10300. 위치: test_current/parts/redraw_requests/_codex_20261121/unit_120_redraw/single_pose03/
- pose04: RAW_imagegen.png, [1262, 1246], SHA256 04e471239744c44059e3133de628f9cb37151297ec2eab29ceef1963320bfc00; IoU 0.88828, outside4 0.02240, missingInner 0.00442. 위치: test_current/parts/redraw_requests/_codex_20261121/unit_120_redraw/single_pose04/
- native/실제4xBRZ/source-only boxes/원본 headpart + 새12000 HD 기준. 생성 RAW 무변형 보존, 기존 candidate/ROM 미변경. Claude 원본 파츠 칸/공유ID/가림/팔레트/조립 검수 대기, 자동 합격 아님.


### 2026-11-21T20:47:42.221017+09:00 unit120 추가 RAW 전달
- pose05: RAW_imagegen.png, [1083, 1453], SHA256 eaeb05af6222d060d3cc3c40f447d14314d98dfecc6eb155a5132d1506b3e176; IoU 0.88399, outside4 0.00237, missingInner 0.01438. 위치: test_current/parts/redraw_requests/_codex_20261121/unit_120_redraw/single_pose05/
- pose06: RAW_imagegen.png, [1149, 1369], SHA256 3c079a1d2c78024680673048d29f731272e972c9d6b5e09600d7a5e1cc5f74cc; IoU 0.79835, outside4 0.01775, missingInner 0.09061. 위치: test_current/parts/redraw_requests/_codex_20261121/unit_120_redraw/single_pose06/
- native/실제4xBRZ/source-only boxes/원본 headpart + 새12000 HD 기준. 생성 RAW 무변형 보존, 기존 candidate/ROM 미변경. Claude 원본 파츠 칸/공유ID/가림/팔레트/조립 검수 대기, 자동 합격 아님.

- 311 pose04·05·06 RAW 추가전달(총7/17). unit_311/DELIVERY.json 최신색인, 각 single_poseNN에 원RAW·prompt·layout·refs/sourceSHA.
  - pose_04 SHA b27effa4ea3b37cd9dcd306b1c348f681cd8ab21f1d80d8832e8c3618c701b43; [1172, 1342]→[356, 408].
  - pose_05 SHA d1c04be98bc1c0d1d2bab555d87c84f0da853b08383439615784fb5f86c0bb28; [1168, 1346]→[316, 364].
  - pose_06 SHA be0309bde55d69177d99ffdf36f5f02958644957c5a4c85ec105632d85f343cf; [1170, 1344]→[324, 372].
- 추가검증:04위로포갠손/소매의가림,05입안/턱수염파츠,06앞으로넘긴망토와가려진다리·손위치/공유칸. 현재위치동일성은미확정이므로 Claude 잘라조립 검증필수.


### 2026-11-21T20:49:37.067376+09:00 unit120 추가 RAW 전달
- pose07: RAW_imagegen.png, [1161, 1355], SHA256 8f2b9dbf4df034b24b47428a9c1cf0cf7218a8672db5ed1c3b5faf860888866e; IoU 0.83771, outside4 0.02091, missingInner 0.03863. 위치: test_current/parts/redraw_requests/_codex_20261121/unit_120_redraw/single_pose07/
- pose08: RAW_imagegen.png, [1202, 1309], SHA256 f63e8b68fafc47d1b5dac506c61de37fc8f2a06068f64531e843183e1c66193a; IoU 0.93344, outside4 0.00702, missingInner 0.00053. 위치: test_current/parts/redraw_requests/_codex_20261121/unit_120_redraw/single_pose08/
- native/실제4xBRZ/source-only boxes/원본 headpart + 새12000 HD 기준. 생성 RAW 무변형 보존, 기존 candidate/ROM 미변경. Claude 원본 파츠 칸/공유ID/가림/팔레트/조립 검수 대기, 자동 합격 아님.


## 2026-11-21 뇌룡328 canonical pose00 RAW 전달
- 위치: `test_current/parts/redraw_requests/_codex_20261121/unit_328_single_pose00/RAW_imagegen.png`
- SHA256: `5d9d45b4258191fc4943478e461289c036ae54e136d10a136f97b3a41c91ddcc`; builtin image_gen, RAW 파일 무변경. 크기1263×1245, 요청332×340와 다름. 아직 승인·candidate·설치 아님.
- source native83×85 / NN4 / 실제 DLL4xBRZ / ASSEMBLY 왼쪽 원본 및 정확 파츠9·1 참조. 원본 금색/주황 팔레트로 자세 전체 새 작화. reference3 오른쪽 구HD는 화풍만 참고.
- 파츠9 머리 hash1553354984 box4x[96,32,128,128], 파츠1 전면 블레이드 hash3230475050 box4x[32,180,256,128], 모두 무반전. 나머지 원본 파츠 박스와 반전은 layout_snapshot.json에 기록.
- Claude 검증: 얼굴·마스크 및 볏 형태, 왼손 크기/관절, 오른쪽 든 팔/손, 블레이드 상단/기울기/오른쪽 격자·하단 및 가림, 원본색·불투명 검정 유지,4px 외곽 허용과 공유파츠 일치. 출력 비율 차이가 있어 정밀 위치 맞춤 승인 전 분할하지 말 것.
- 요청/prompt/source·reference SHA/layout SHA: generation_request_visual.json, layout_snapshot.json. source만 진단했으며 READONLY_SOURCE_FIT_DIAGNOSTIC.json은 기하 적합 승인 아님.
- 다음 자세에서는 canonical 승인 전 공유머리/블레이드를 임의로 다시 해석하지 말 것.


## 2026-11-21T20:50:23.868179+09:00 314 전체11자세 RAW전달완료(재조립QA대기)
- `_codex_20261121/unit_314/DELIVERY.json`: pose00..10 모든원본wholepose/real4xBRZ/sourcepartbox/atlas/canonical00기준으로 새로작화. 원본cool아닌warmkhaki/tangrey갈기유지. 원RAW무변환, 각요청문서에prompt/SHA/layout저장.
- ['pose_00'] SHA65726f139e62866bed28805abc1551c2d03bbc2406cac10c5e8a2bd4a2d452d7 [1426, 1103]→native4x[440, 340]
- ['pose_01'] SHAf2133231f3206af1aeadb6ce91aeb8d1fbb312f51c8168b98ee03aebcd234e3c [1484, 1060]→native4x[476, 340]
- ['pose_02'] SHA15c4db5ccb84f4bf7f973c68cacd798e8e3f28625970b2416b0d38f438e68505 [1806, 871]→native4x[704, 340]
- ['pose_03'] SHA4d5ddd1786ca0b33677157404a7f40b5a7ac126e8bea0ab6b7c224fc4ef686a9 [1208, 1302]→native4x[360, 388]
- ['pose_04'] SHA3181b682800124b7310a71fa9421ceed27509696cd1ec1746055e6a46d8a05a7 [1297, 1212]→native4x[364, 340]
- ['pose_05'] SHA6c9b971153a516ca18b66929ec8c633d0de0f56a3f3fb3f825966daf518cb89e [1505, 1045]→native4x[484, 336]
- ['pose_06'] SHA6877c8319bf672b51e1b30240243757333a7abb4a08a5b7625ead672b4cb871b [1875, 839]→native4x[760, 340]
- ['pose_07'] SHAf105fc834f05b318729ba99a6c7e833691f95f57a2c26cf2be6c920ea4c8bb28 [1247, 1261]→native4x[352, 356]
- ['pose_08'] SHA7b36794eba3f37be8cd929bba4860d90c553e1615676e5ec5b7cf07c818ad2f7 [1506, 1045]→native4x[484, 336]
- ['pose_09'] SHA57fbf76d3dfe6836be8ed52163f127c96c77e7826bf9cc8bb4c75e8cb8204f81 [1374, 1145]→native4x[408, 340]
- ['pose_10'] SHAd3b455dea0e9be96b8eee55587121671030f7a220b2813dd13ac77065328c093 [1241, 1268]→native4x[380, 388]
- Claude검증: 같은얼굴/갈기/뱀머리 번호끼리 조각크기·눈/입/센서 상대위치 동일성, flip, 02/06 긴수평촉수 반복조각접합, 원본과얼굴비율/표정, 불필요한장식생성 및실루엣4px범위, 모든alpha0구멍. 포즈별독립생성이라 동일part의픽셀완전동일성보장안됨. 형식gate는실제게임검증합격아님.
- 다음HEAVY151unit345 root착수,120/311/328 agents병행.

- 311 pose07/08도 즉시저장. 07 SHA9663e90de05a3982170c0adf772124254b8a6d5805e9ee15fe5e2c1295c20d27 (1369x1149→396x332),08 SHAdd65c993c7d659a2e3dc2f9a746bbef30864915d2b9eff4d56b2cb1403b1fccb (1334x1179→408x360). 07 네주먹/08앞으로포갠주먹과뒤털·띠망토, 원본공유파츠칸 검증. 총9/17 RAW. smooth00기준,설치아님.


### 2026-11-21T20:51:26.904174+09:00 unit120 추가 RAW 전달
- pose09: RAW_imagegen.png, [1166, 1349], SHA256 02e64ff33abb355f1296bd93646449f27ace82a506c8d6bea1d280d84e87c2da; IoU 0.85622, outside4 0.00739, missingInner 0.04023. 위치: test_current/parts/redraw_requests/_codex_20261121/unit_120_redraw/single_pose09/
- pose10: RAW_imagegen.png, [1152, 1365], SHA256 3489ba85118524a35dd5a92b4c3aebbcd9c68a82ef1956aeea384d69e361194c; IoU 0.87848, outside4 0.00426, missingInner 0.01676. 위치: test_current/parts/redraw_requests/_codex_20261121/unit_120_redraw/single_pose10/
- native/실제4xBRZ/source-only boxes/원본 headpart + 새12000 HD 기준. 생성 RAW 무변형 보존, 기존 candidate/ROM 미변경. Claude 원본 파츠 칸/공유ID/가림/팔레트/조립 검수 대기, 자동 합격 아님.


### 뇌룡328 pose01 RAW 즉시 전달
- `_codex_20261121/unit_328/single_pose01/RAW_imagegen.png`; SHA256 `5c658e14c54e4c19ee0f5d13fd750119ff61ad242e5f60a6841e68f3ebf96326`;1214×1295,A0..255. 요청364×388, 종횡비 오차0.0738%. RAW 무변경, candidate/설치 없음.
- 원본 NN4와 real4xBRZ, ASSEMBLY 왼쪽 원본, canonical00화풍 참조. gray/lavender 상단 공격효과 포함. Claude는 얼굴 투영/손·팔과 공격효과 개수·위치/어깨·가슴 및 원본 파츠박스 검증. canonical승인 기다리는gate 없이 다음pose진행.

- 345 기준은FX없는pose01 선택(00은사격연기가림). `unit_345/single_pose01/RAW_imagegen.png`, SHA8a61f7327743e6d504d007824d394d6c4b40a6bcd029bd95af4e7e9fd84fa137,1334x1179. sourceNN4/real4xBRZ/partbox/atlas원본으로freshsmoothredraw. canonical01를나머지samepartref에추가; 과장된claw/hullposition/vent비율 및part칸맞춤검증, 설치아님.

- 311 pose09/10 RAW 추가전달(총11/17),DELIVERY.json 갱신. 09 SHAeead268f194143cd9e18fe471a18161f27ad569d5685835472ac5e1c703fdf97,1330x1182→396x352;10 SHAa377e165613ac1154ab06c53581a360df1cca347f4d382c722fa9ae9a214356d,1349x1166→412x356. 좌우쏟은주먹과4팔가림·앞치마/허리·공유head1 눈센서 정위치 확인필요.


### 2026-11-21T20:53:32.978869+09:00 unit120 추가 RAW 전달
- pose11: RAW_imagegen.png, [1337, 1176], SHA256 9faf4574c56e8fff8ff03af413f45164129491aecd26e85c16db333908c2c079; IoU 0.93564, outside4 0.00355, missingInner 0.00064. 위치: test_current/parts/redraw_requests/_codex_20261121/unit_120_redraw/single_pose11/
- pose12: RAW_imagegen.png, [1170, 1344], SHA256 6c801d199a08e2e529388d24e686f0cb43f06c08bbb0b3df0e778b81c095548f; IoU 0.85872, outside4 0.00849, missingInner 0.02633. 위치: test_current/parts/redraw_requests/_codex_20261121/unit_120_redraw/single_pose12/
- native/실제4xBRZ/source-only boxes/원본 headpart + 새12000 HD 기준. 생성 RAW 무변형 보존, 기존 candidate/ROM 미변경. Claude 원본 파츠 칸/공유ID/가림/팔레트/조립 검수 대기, 자동 합격 아님.


### 뇌룡328 pose02 RAW 전달
- `_codex_20261121/unit_328/single_pose02/RAW_imagegen.png`; SHA256 `b46d7c61543aa19fcb273e76b3fd883de8b4e4468e9eacc40d187797ae370d56`; 크기[1188, 1324], 요청[384, 428], 종횡비 오차0.0094%. A[0, 255]. RAW무변경, 미승인·미설치.
- nativeNN4/real4xBRZ/ASSEMBLY왼쪽 원본 authority, canonical00화풍/공유파츠 기준. prompt/SHA/layout/DELIVERY파일 동봉.
- Claude검증: 원본의 좁은 선형 효과가 일부 굵은 파편형으로 바뀜: 효과 개수/두께/끝 위치를 원본과 반드시 비교. 머리9 공유 동일성, 블레이드 측면 격자와 팔/흉부/가림 검증. geometry승인 아님.


### 뇌룡328 pose03 RAW 전달
- `_codex_20261121/unit_328/single_pose03/RAW_imagegen.png`; SHA256 `5dbd68316a183b91482288ba6f764d4e10e7d548145aa7a85e25fbe8cd647e62`; 크기[1459, 1078], 요청[352, 260], 종횡비 오차0.0306%. A[0, 255]. RAW무변경, 미승인·미설치.
- nativeNN4/real4xBRZ/ASSEMBLY왼쪽 원본 authority, canonical00화풍/공유파츠 기준. prompt/SHA/layout/DELIVERY파일 동봉.
- Claude검증: 눈 영역이 원본보다 명암부가 넓어짐: 원본 얼굴11 투영과 작은 눈색/마스크를 대조. 팔·손·부츠와 어깨 높이, 소스 contour/박스 검증.


### 2026-11-21T20:55:43.034657+09:00 unit120 추가 RAW 전달
- pose13: RAW_imagegen.png, [1317, 1194], SHA256 5885a5e5708f11119411fa21320e6d4489f91b3d69deea4aa6c80cee0b078298; IoU 0.84667, outside4 0.01564, missingInner 0.02794. 위치: test_current/parts/redraw_requests/_codex_20261121/unit_120_redraw/single_pose13/
- pose14: RAW_imagegen.png, [1114, 1412], SHA256 724aabc8425481e68c0f598e4df30c6572a2c9b9949fad20215e394738bf8bab; IoU 0.85650, outside4 0.01427, missingInner 0.02455. 위치: test_current/parts/redraw_requests/_codex_20261121/unit_120_redraw/single_pose14/
- native/실제4xBRZ/source-only boxes/원본 headpart + 새12000 HD 기준. 생성 RAW 무변형 보존, 기존 candidate/ROM 미변경. Claude 원본 파츠 칸/공유ID/가림/팔레트/조립 검수 대기, 자동 합격 아님.


### 뇌룡328 pose04 RAW 전달
- `_codex_20261121/unit_328/single_pose04/RAW_imagegen.png`; SHA256 `3dda7dee15dea54ddb848e2050d92ae678d4c4949ec17711085269b8fa027a97`; 크기[1397, 1126], 요청[412, 332], 종횡비 오차0.0233%. A[0, 255]. RAW무변경, 미승인·미설치.
- nativeNN4/real4xBRZ/ASSEMBLY왼쪽 원본 authority, canonical00화풍/공유파츠 기준. prompt/SHA/layout/DELIVERY파일 동봉.
- Claude검증: 원본 머리8 얼굴·붉은 입점/노란 눈, 장비13 좌측face 세 사각금속과 상단회색판, 팔40 접합과 오른손52·부츠를 sourceoverlay로 비교. 기체 비율/파츠 크기 최종검증 필요.

- 311 pose11 rearview SHA d88429f82edf65bb26ef12247d3aac723be04e5404e387877ee99cd495596d96,1208x1302→356x384. 앞얼굴없이뒤털/망토 유지. pose12 최신은 single_pose12/hand_smooth/RAW_imagegen.png SHA3acf0f53ec5d4d04af87d8e0b3f9dbc6875772ac1a933323901ba932efe911c5,1195x1316→356x392: 위손등체크무늬를smooth면으로그림. 12 최초RAW는체크무늬STYLE_HOLD 보존. 원본part25의손외곽/가림/알파판단 검증. 총13/17자세RAW,13..16계속.


### 뇌룡328 pose05 RAW 전달
- `_codex_20261121/unit_328/single_pose05/RAW_imagegen.png`; SHA256 `546ea6ca4c7cf3e78eed3647a6a41e6825850922767de479e1b46bad3a723247`; 크기[1128, 1394], 요청[272, 336], 종횡비 오차0.0422%. A[0, 255]. RAW무변경, 미승인·미설치.
- nativeNN4/real4xBRZ/ASSEMBLY왼쪽 원본 authority, canonical00화풍/공유파츠 기준. prompt/SHA/layout/DELIVERY파일 동봉.
- Claude검증: 머리9 공유형상, 들린 손25 flip_x, 수평 교차하는 반대 팔/손가락 및 백팩/부츠를 원본 박스대로 대조. 팔 접합/위치·외곽 최종검증.


### 2026-11-21T20:58:32.886847+09:00 unit120 추가 RAW 전달
- pose15: RAW_imagegen.png, [1188, 1324], SHA256 4042f6c88f33f357433ae8eb3da27297e3bd2c022904c4a011ace86eb6730a9d; IoU 0.82745, outside4 0.00652, missingInner 0.07247. 위치: test_current/parts/redraw_requests/_codex_20261121/unit_120_redraw/single_pose15/
- pose16: RAW_imagegen.png, [1207, 1303], SHA256 ebc68e1717fac197b0e5aa91fbbb75a6c6fb41559e4cb44975cbe2798834c181; IoU 0.84738, outside4 0.00180, missingInner 0.05838. 위치: test_current/parts/redraw_requests/_codex_20261121/unit_120_redraw/single_pose16/
- pose17: RAW_imagegen.png, [1196, 1315], SHA256 cae873cd4acb25d0e7ee6d42310074a7aa52aaf119331b2a62eda14131404842; IoU 0.86764, outside4 0.00805, missingInner 0.03314. 위치: test_current/parts/redraw_requests/_codex_20261121/unit_120_redraw/single_pose17/
- native/실제4xBRZ/source-only boxes/원본 headpart + 새12000 HD 기준. 생성 RAW 무변형 보존, 기존 candidate/ROM 미변경. Claude 원본 파츠 칸/공유ID/가림/팔레트/조립 검수 대기, 자동 합격 아님.


### 뇌룡328 pose06 RAW 전달
- `_codex_20261121/unit_328/single_pose06/RAW_imagegen.png`; SHA256 `78fa9a86c6249fb185436b93e0258f0516f5dabc44d1e6cd9fea20f600f498a6`; 크기[1277, 1231], 요청[336, 324], 종횡비 오차0.0319%. A[0, 255]. RAW무변경, 미승인·미설치.
- nativeNN4/real4xBRZ/ASSEMBLY왼쪽 원본 authority, canonical00화풍/공유파츠 기준. prompt/SHA/layout/DELIVERY파일 동봉.
- Claude검증: 수평효과가 원본 얇은선보다 두껍고 끝이 일부 둥글어짐: #30반복부 원본 좌표/알파를 대조해 효과분할·복원 검증. 로봇 얼굴/양손·부츠 sharedpart 대응 검증. RAW는 최종승인 아님.


### 2026-11-21 20:59 unit120 요청18장 RAW 전달 완료
- 요청 ASSEMBLY_pose_00~17 모두 생성/프로젝트 복사 완료(18 RAW/18 DELIVERY/18 read-only SOURCEFIT). 전달표: test_current/parts/redraw_requests/_codex_20261121/unit_120_redraw/UNIT_DELIVERY_PROGRESS.json. 검증 안내: 같은 폴더 DELIVERY_README.md.
- 위치 오차 우선 확인: 03 IoU .74539/outside4 .07429, 06 IoU .79835/missingInner .09061, 04 crest 위15px, 15/16 하단16px 짧음. 완전 정합/게임 설치 승인으로 처리하지 않음.
- 공유 head10(00/05~10/12~17)의 모양/명암, 01/11 head11 후면 가림, 02 head2,03 head7,04 head6 및14 전경팔 가림을 Claude가 실제 조립으로 검증.
- 기존 candidate/ROM/라이브러리/source 미변경. 생성 RAW 후처리 없음. pose_a00~a03은 REQUEST ASSEMBLY가 없으므로 이번 18장 범위에서 생성하지 않음. 다음 우선순위는 HEAVY_151의314이나 병렬 담당중복 확인 후 진행.


### 뇌룡328 pose07 RAW 전달
- `_codex_20261121/unit_328/single_pose07/RAW_imagegen.png`; SHA256 `960b8f0ad4229ef6ca5a912539d8376c18c286193ea6d94cfee36aec066b746e`; 크기[1416, 1111], 요청[408, 320], 종횡비 오차0.0371%. A[0, 255]. RAW무변경, 미승인·미설치.
- nativeNN4/real4xBRZ/ASSEMBLY왼쪽 원본 authority, canonical00화풍/공유파츠 기준. prompt/SHA/layout/DELIVERY파일 동봉.
- Claude검증: 얼굴 눈이 원본 작은명암보다 평평한직사각형으로 표현됨: 얼굴11 mask/eye shape검증 및 작은장비26의 원본 윤곽/회색inset, 양팔 길이·오른주먹50, 백팩/하체박스 대조.
