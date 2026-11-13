# 합체기1920 마징카이저17종 자세 재제작 후보

미검증 후보·연결 준비. 공식 QA와 실제재생 판정은 Claude. 코어/라이브/DB 변경 없음.

원본 test_current/combat/mazinger_combination/frame_1920.state 로드+1의 실제 cachedOBJ/renderedOAM. mazinger_combo1920_cached_source/rendered_contract_all.json에 actualpalette/indexSHA/core_path/DLLSHA/OAM좌표 보존. 오래된obj npz/종료시점MMU VRAM/추정palette를 쓰지 않았다. 팔레트1의 OAM1 및16~31 총17OAM을 한 자세로 선정했다. 다른기체의공유손/이펙트를 섞지 않았다.

17종 모두 기존legacy 연결이 있는 재제작이며 새미연결17로 세면 안 된다. 원본 hash+w/h까지같은 최신6개재작업atlas manifest를 대조해 중복보존대상을 선정했으며 이17에서는동일actualRGB 최신재작업이없었다. 단rawindex같은다른palette의최근그림은동일색으로추정해재사용하지않았다. 기존exact/indexed목록 source_identity_and_connection.json, 기존ID교체준비 installation_map.json. ROM14887/2645 원본bytes첫일치 rom_indices_identity.json. 소유IMG유일성미확정.

머리OAM20 32×32(x69,y57), OAM19 16×32(x101,y57)는 같은actualpalette/반전없음/겹침0으로맞닿는다. 48×32 연속원본을한번그린후x32분할. joint_head_provenance.json,joined_head_native_clean.png,joined_head_hd.png. 원본알파를그림에찍지않았고 다른파트가숨긴내용을이웃파트색으로채우지않았다. 각원본사각형을보존해생성그림에서만잘랐다.

imagegen exec-38570288의16그림(머리2파트를1그림)으로새제작. painting_reference16.png/whole_native_tight.png/actual연속머리를참조했다. 가슴빨강V·노랑연결끝은얼굴아님을명시해 몸통으로그렸고 작은원본절단편도전체장식으로확대하지말도록했다. 눈의큰흰하이라이트는제작단계에서actual노랑[246,246,8]과달라 exec-0290d524로노랑교정. 작은청록사각부위는원본패널로보존하고새눈을추가하지않았다. head_generated_eye_fixed.png, 다른15RGBA동일 eye_fix_preserved_other15.json.

최종 candidate_atlas.png1152×1440/native_atlas.png288×360 정확4배. SHA4f6c597c76aa4dc1429138cf9cf076f1a821d0babc162c9b4fe2e697aa6ab412. 원본indexSHA/크기/색/alpha정합 mechanical_contract_checks.json. 빈후보/alpha_max16미만0 candidate_presence.json. 어떠한기계검사도공식품질통과뜻아님.

candidate_whole_pose_production.png/candidate_tight_production.png는원래좌표와priority/OAM역순으로새17을한벌조립한제작자료이며게임HD재생증거아님.

Claude판정항목: 연속48×32머리·마스크그릴아래경계의연결/눈·뿔실제색, 작은가슴·윙접합조각지지영역, 양팔·주먹·무릎파트 역할·관절연속성, 큰박쥐윙의열린빈틈·가느다란빨강조각. 생성에서주먹손가락이나무릎돌기를늘렸을위험/윙주변반투명빨강스필이있을수있으므로비교판정필요. 알려진큰불연속을수치로통과시켰다는주장없음.

Claude:
```powershell
python scripts/verify/verify_runtime_path.py --state test_current/combat/mazinger_combination/frame_1920.state --frames 120 --save-frames 0 15 30 60 --track-atlas mazinkaiser_combo1920_pose --name mazinkaiser_combo1920
```
