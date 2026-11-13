# 본타군 공격 후반 실제 미연결 2종 후보

상태: 미검증 후보·연결 준비 완료. Claude 재생·시각검증 대기. 라이브·DB·코어 변경 없음.

test_current/combat/bonta_attack.state +315/+360(각316/361회 run) 실제 cached OBJ+rendered OAM 본체 palette0에서 확보. 전체12OAM 의존보존, 새미연결2종2OAM만 제작. 실제 기체 문맥으로 확인한 올리브색 장비/몸체조각과 작은주황연결편이며, 총이라고 부르지 않는다. 원본에서 총이 표시되는 다른부분은 이미 연결되어 있고 그림품질은 별도문제다.

두새RGB 모두 최신 exact/indexed 연결없음(source_identity_and_connection.json), ROM image13893 (128,32,32,32)/(136,0,8,16) bytes완전일치(rom_indices_identity.json). 실제사용 palette와 ROM후보도일치. 계약 core_path/SHA256 보존. 원본RGB/알파/index SHA·크기는 mechanical_contract_checks.json, 후보alpha_max>=16은 candidate_presence.json. 시각품질판정아님.

installation_map.json + candidate_atlas.png768×192/native_atlas.png192×48로정확4배. parts_generated.png는 imagegen exec-ccca196a 생성원본. 원본RGB/알파찍기없고 생성지원bbox정렬만. 후보SHA `3b086d04969b9f8acdb4b60dd7453fbc17343798d475c03d0532ab3e7b196b7b`.

위험: 큰부품윗절단면에 새검은cap이생겼는지, 올리브실색과주황끝위치, 작은14픽셀지원영역이과하게굵어졌는지는Claude확인필요. whole_native_bbox_context.png 원본문맥과 native_atlas_reference_gray.png 제공. frame*_production_assembly.png는 기존파트를원본으로둔제작문맥이며 실제HD재생증거아님.

Claude재생:
```powershell
python scripts/verify/verify_runtime_path.py --state test_current/combat/bonta_attack.state --frames 390 --save-frames 300 315 345 360 --track-atlas bonta_late_missing --name bonta_late
```

같은공격다른시점과다른무장에대한전부완성주장은하지않는다.
