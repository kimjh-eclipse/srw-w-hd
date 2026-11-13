# 아스테바리스 중기동·월면12기체 실제미연결11종 후보

상태: 미검증 후보·연결 준비 완료. Claude 실제재생/시각검증담당. 라이브·DB·코어변경없음.

## 실제관측범위
source_mechanical_157_681~162_701 각중기동기체의첫무장(4씩증가) 및source_mechanical_163_704~168_724 각월면기체의첫무장(4씩증가). 각source_pose.state 로드후1회run 계약. 실제메뉴원본저장frame은중기동250,월면230(168은240)이며각capture_meta참조. 격리RAM진단메뉴에서비용/기력/지형완화한원본이며ROM/사용자저장변경없고 캠페인합법성QA아니다.

전체12기체 본체palette0 174OAM 의존관계 whole_pose_dependencies.json 보존. 새11고유 RGB가 30회OAM에나타난다. 같은기체계열이라도색이달라actualRGB가다르면각각새로제작. rawbytes·실제사용palette·크기까지같으면중복공유하며12기체라고24그림을중복생성하지않았다. 새11종최신exact/indexed연결없음(source_identity_and_connection.json).

actualcached팔레트·core_path/SHA256·원본indexSHA·attrs/좌표는contract.json. ROM11019/11046에서11종원본bytes완전일치(rom_indices_identity.json), 실제소유리소스유일성은별도미확정. 사용palette와ROM후보일치여부도source_identity_and_connection.json.

## 설치입력
installation_map.json + candidate_atlas.png1024×864/native_atlas.png256×216, 정확4배. 셀64×72/4열3행중마지막11번빈칸. mechanical_contract_checks.json은원본RGB/alpha/indexSHA/크기정합이며candidate_presence.json은빈/alpha_max16미만0. 품질QA아님. SHA `8a0ad3f365190021c3c8a4d199405113d1c32da5b1addbd05eaa6750946cc835`.

## 그림제작
parts_generated_halo_rejected.png(exec-a3b28d05)에는생성회색헤일로가남아채택하지않았다. imagegen알파정리편집으로parts_generated.png(exec-8eebe3f2)새후보를준비했다. 원본참조는native_atlas_reference_gray.png / primary_two_native_bbox_context.png / whole_native_bbox_context.png. 원본RGB/알파스탬프및다른기체재색칠없고 생성지원bbox정렬만수행. prepare_candidate.py재현.

cell0~8은원본의얇은부분기계구조이며무기/얼굴이라고명명하지않았다. 원본의탁한보라갈색구조와옅은민트/연보라하이라이트를따르도록생성. cell9세마디작은회색연결부,10짙은남색/적갈색긴패널. 옅은민트는실제원본팔레트색이며크로마키로일괄지우면안된다. 생성기가절단면을완성된장갑외곽선/cap으로해석했는지,안쪽빈영역이닫혔는지,미세한기체별밝은색변화와색영역이맞는지는Claude확인필요. unit*_production_assembly.png는기존파트원본으로둔제작문맥이며최종HD재생증거아님.

## Claude재생
```powershell
python scripts/verify/verify_runtime_path.py --state test_current/parts/borrowed_shape_rework/source_mechanical_157_681/source_pose.state --frames 90 --save-frames 0 15 30 60 --track-atlas aestivalis_heavy_lunar_missing --name aestivalis_heavy157
python scripts/verify/verify_runtime_path.py --state test_current/parts/borrowed_shape_rework/source_mechanical_163_704/source_pose.state --frames 90 --save-frames 0 15 30 60 --track-atlas aestivalis_heavy_lunar_missing --name aestivalis_lunar163
```

나머지10기체도각source로확인필요. 전체무장완성주장없음.
