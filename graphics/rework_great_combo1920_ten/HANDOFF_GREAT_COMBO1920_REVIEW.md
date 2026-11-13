# 합체기 1920 그레이트 마징가 10종 재제작 후보

미검증 후보·연결 준비. Claude가 공식 QA와 실제 재생 판정 담당. 코어/라이브/DB 변경 없음.

원본은 test_current/combat/mazinger_combination/frame_1920.state 로드 후 1회 run의 실제 cached OBJ + rendered OAM. source 폴더 mazinger_combo1920_cached_source에 추출 계약, 실제 palette, original index pixels/indicesSHA, core_path/실제 DLL SHA를 보존했다. 예전 obj_1920.npz나 MMU 종료시점 VRAM을 쓰지 않았다. banks_contact.png는 원본은행 시트이며 HD결과가 아니고 이번 계약 선정 근거로 대체하지 않았다.

실제 팔레트2의 그레이트는 OAM2~15 총14개. 이 중 최신 Great 새그림4개(OAM8~11, bindings82808/7351/7345/7350)는 actualRGB·raw index bytes·사용palette가 같음을 확인해 원본 rawpaint 그대로 의존 보존. same_character_dependency_proof.json, preserved_recent_art.json. 나머지10은 모두 기존 legacy 연결이 있으므로 '새 미연결10'이 아니라 기존 그림 재제작10이다. 당시 exact/indexed 연결목록과 palette 근거는 source_identity_and_connection.json. installation_map.json에 기존 exact RGB binding을 명시하여 root가 직렬 교체할 수 있다. ROM14882/14887에 원본bytes첫일치, 소유유일성은 별도미확정.

머리는 OAM7 32×32(x136,y60)와 OAM6 8×32(x168,y60), 반전 없음·동일 실제palette·겹침0. 이웃한40×32 원본으로 한 번 새로 그리고 생성 그림을 x32에서 나눴다. joint_head_provenance.json, joined_head_native_clean.png, joined_head_hd.png. 원본 alpha를 생성결과에 찍지 않았으며 각 파츠를 별도 완성 머리로 그리지 않았다. 생성지원영역 bbox를 연속 원본의 가시bbox에 정렬 후 원래두사각형으로 분리했다.

imagegen exec-8e123a5f 새그림 parts_generated.png. painting_reference9.png(머리2조각을한그림으로묶어총9셀), 실제 whole_native_tight.png와 같은기체의 기존좋은 Great179 candidate_pose를 스타일참고로 사용. 원본 눈은 노랑, 뿔·갑옷·날개 실제색 유지가 제작지시였다. 어떤 숫자검사를 품질통과로 주장하지 않는다.

설치 installation_map.json + candidate_atlas.png1152×864 / native_atlas.png288×216 정확4배. SHA 77ea9021adbe4029c7beebdd868d73b36b22a59828d312295766871fabc88e2f. nativeindexSHA/크기/RGB/alpha계약 정합 mechanical_contract_checks.json. 빈후보/최대alpha16미만0 candidate_presence.json.

candidate_whole_pose_production.png / candidate_tight_production.png는 새10과 기존좋은4의 rawpaint를 원래 OAM 좌표·priority/OAM역순으로 조립한 제작자료. 기존그림을 r.part로다시등록해 이중정렬하지 않았고 rawpaint source좌표대로 잘라 사용. 실제 게임 HD 재생 증거가 아니다.

Claude 판정 대상: 연속머리40×32의 눈한줄·뿔끝·32경계, 마스크그릴 OAM5와 머리 하단이 맞는지, 파란 주먹/옆팔 접합·작은부품 절단면, 몸통 오른쪽의 작은 빨강/노랑 연결끝·윙 접합이 원본지지영역과 맞는지. 생성의 과한 외곽 반투명색/그릴 구멍수·원형관절부피 등도 미검증. 이 한자세의 다른원본기체를 그레이트로 섞지 않았다.

Claude 실제재생:
```powershell
python scripts/verify/verify_runtime_path.py --state test_current/combat/mazinger_combination/frame_1920.state --frames 120 --save-frames 0 15 30 60 --track-atlas great_combo1920_pose --name great_combo1920
```

이 fixture의 세 기체는 마징카이저·그레이트·진겟타1(2613 공유)이며 마징가Z가 실제 관측됐다고 명명하지 않았다. 마징가Z는 별도 정상메뉴 source가 필요하다.

제작 후 눈색 교정: 처음 생성한 눈의 큰 흰 하이라이트를 실제 원본 [246,246,8] 노랑에 맞춰 imagegen exec-572b71c4로 교정(head_generated_eye_fixed.png). 연속머리2조각만 바꾸고 다른8 RGBA동일(eye_fix_preserved_other8.json). 이 색 교정은 제작 교정이며 공식재생QA 통과 뜻 아님.
