# 합체1560 그레이트 작은전신 3파트 재제작 후보

미검증 후보·연결 준비. 공식QA/실제재생은Claude. 라이브/DB/코어 변경없음.

frame_1560.state 로드+1 실제cachedOBJ/renderedOAM 팔레트2 OAM16~18. 기존legacy3 재제작이며 신규누락3로세지않음. 기존exact/indexed와actualpalette source_identity_and_connection.json,기존ID installation_map.json,원본bytes ROM14886 첫일치. 극소파트는단독소유IMG유일성이미확정이므로 resource=None/첫일치후보로분리기록. 실제캐시index/RGB는확정.

한작은그레이트전신이40×40에서3비겹침사각형으로분할됨. (16,0,16,8),(0,24,8,8),(8,8,32,32); 동일palette·반전없음,겹침0 joint_partition_provenance.json. 다른기체와섞인master를자르지않고해당기체만의연속원본으로새그림제작. 원본alpha/RGB찍기없음.

첫imagegen exec-6c71c6e3 그림은왼손/왼발이원래OAM지원범위밖으로나와210불투명HDpixel(2.10%)이잘려보류했다. exec-8518c91a로왼팔을내리고,잘못된반대발을옮긴실패결과는채택하지않고,exec-1bf5ac61로정확한화면왼쪽부츠를참조하여안쪽으로옮긴 parts_generated.png를선택했다. 마지막남은19HD경계pixel은생성그림자체를수평1native texel좁혀오른쪽정렬했다(generated_alignment.json). 원본그림을색/alpha마스크로찍거나돌출영역을지워수치를맞추지않았다. 원래OAM계약좌표·w/h는불변. 최종alpha>=160의지원영역밖은0,alpha16/1기준세부는projection_support_report.json. 이기하조건이그림품질통과뜻은아니다.

candidate_atlas.png864×288/native216×72 정확4배. SHA f839d1d6a4dddfb3ba3deca084bf5c9b1c59cbeeae3a6cc82f51da1cdc44d647. 원본indexSHA/색/alpha/크기 mechanical_contract_checks.json,빈후보0 candidate_presence.json. candidate_pose_production.png는새3파트제작재조립이며게임HD재생증거아님.

실제원본의작은얼굴중앙청색띠·노랑작은표지와양뿔색·손발색을참조하여그렸다. 생성에서오른눈이두노랑조각으로나뉘었던것은기하교정때하나로이어두눈한줄이되게했다. 원본의작은팔끝보다생성주먹세부가늘었을위험,발위치·얼굴작은색영역/뿔과새원본사각형경계의연속성은Claude가판정할것. 기계수치로시각완료주장하지않음.

Claude:
```powershell
python scripts/verify/verify_runtime_path.py --state test_current/combat/mazinger_combination/frame_1560.state --frames 120 --save-frames 0 15 30 60 --track-atlas great_combo1560_pose --name great_combo1560
```
