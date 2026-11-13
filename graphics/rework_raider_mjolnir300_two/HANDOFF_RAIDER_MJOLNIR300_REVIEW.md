# 레이더 묘르닐 준비 자세 기계2종 — 미검증 후보

- 실제 unit81/weapon345 메뉴300. `source_mechanical_fixed_81_345_300/source_pose.state` +0. 팔레트0 기체12 OAM 중 새 실제RGB2, 기존exact10 의존 보존.
- 미연결1(세로연결부 cell1) / indexed 다른색 재제작1(cell0 메타65676). 두그림 raw IMG9066(0,32)32×32, IMG9068(32,0)16×32 일치. 실cached palette 보존, ROM PLT는 셀1 어두운 사용색만같은3개동률이므로 하나로 단정하지 않음.
- actual cell1 flip_x=True, cell0False; affine없음. raw그림원래방향제작 후 actualOAM반전으로조립. 다른리소스 source교차없음.
- 전체 기체 문맥의 비스듬한 장갑/연결부와 들린팔 세로부재만 제작. 얼굴/손가락 새로완성하지 않음. 생성 raw 보존, 자체 alpha64미만만RGBA0/고알파불변, 원본RGB/alpha스탬프없음.
- SHA256 e2f910cb29c6099097e5c7bf9ce396bd388d901a0d6c872a5d58f40aa9a864af
- installation_map/candidate_atlas/native_atlas와raw팔레트·크기·후보존재 기계적 확인 포함. production조립은공식QA/실제HD재생아님.
- Claude 위험: 비스듬한 장갑이 기존어깨와만나는절단면, cell1중간/아래연결 폭과반전, 생성명암이원본보다밝은지. 시각/실재생미검증.
- 같은공격+500은 palette0기체가사라지고 palette2철구(기존연결),palette10미연결효과와palette13상대기체가나온장면. 그것을레이더기체누락으로세거나palette0계약을강제로만들지않았음.
- 라이브/DB/코어변경없음,모니터off/headless.
