# 아스테바리스 육전형 후반 공격 미연결 19종 후보

현재 상태: **미검증 후보·연결 준비 완료**. 그림 제작과 원본 계약 기계적 정합만 수행했다. 실제 재생·색 영역·형태 판정은 Claude 담당이며 라이브·DB·코어를 수정하지 않았다.

## 선정 범위와 원본 계약

unit151~155의 test_current/combat/named_attacks/unit_각번호/mechanical_cutin_168.state +195에서 실제 cached OBJ + rendered OAM으로 추출. 래퍼는 state 로드 뒤196회 core.run하며 video_epoch=196. source 계약 각 항목에 core_path와 실제 DLL SHA256 보존. 상태마다 타이밍이 다르므로 같은 공격의 같은 애니메이션 자세라는 추측으로 섞지 않았다. 각 시점의 실제 본체 palette0을 별도로 계약했다.

미연결19종/19OAM: 151은6종,152는7종,153/154/155는각2종. 모두 binding0이며 최신 라이브 exact/indexed 연결도0(source_identity_and_connection.json). 불투명0인 빈 OAM2개씩은 제외했다. 앞선 육전 +90 12종과 다르다. 각 본체 전체 OAM 수는 {151: 12, 152: 12, 153: 14, 154: 14, 155: 14}, 총66OAM이며 나머지47OAM은 기존 연결 의존관계로 보존. 156 +195에는 미연결 palette0이 없어 이번 제작범위에서 제외했다.

- contract.json:19고유 캐시 계약, 실제 index bytes·팔레트·OAM·화면좌표·컨텍스트.
- whole_pose_dependencies.json:원본 전체66OAM 및 기존 binding 기록.
- rom_indices_identity.json:19종 모두 ROM 이미지 실제 원본 bytes와 완전 일치. 먼저 찾은 동일 bytes 영역 기록이며 다른 이미지에도 동일 모양이 있을 수 있다. image10778/10767/10779/10700/10749 등으로 구성.
- source_identity_and_connection.json:사용 팔레트 색 번호별 ROM 팔레트 후보와 현재 연결 유무. 일부 기체 색변형은 animation_audit가 열거한 팔레트 후보에서 찾지 못했다. 기준색은 렌더 순간의 확정된 cached palette이며, 모든 ROM 팔레트 일치를 주장하지 않는다.

## 루트 설치 입력

installation_map.json의19 entries와 candidate_atlas.png / native_atlas.png. actual RGB 전용, indexed_safe=false. 후보1024×960/원본256×240로 정확4배. 각 entry에 ROM source 좌표, 캐시SHA와 원본 bytes 증거를 붙였다. metadata shape 검사는 Claude가 담당한다.

후보 SHA256: `2c1a17ae45ebf25a1b9537c274efb7cad4cf745adf144c844433e82db14a6174`

원본 참조: native_atlas_reference_gray.png, native_cells_context.png, whole_native_bbox_context.png, unit151~155_native_context.png. 빨간 사각형은 실제 미연결 OAM 전체 지원영역이며 생성물에 들어가지 않는다.

## 그림 제작 출처

imagegen 스킬 사용. exec-6e9a5b6e 생성 PNG를 parts_generated.png로 보존. 원본 셀과 전체 기체 문맥을 참조해19개 각각 새로 그렸고, 다른 기체 그림 재색칠은 하지 않았다. 원본 RGB/alpha는 후보에 찍지 않았다. 생성 alpha bbox만 원본 보이는 bbox 위치에 맞춰 분리·축소했다. prepare_candidate.py 재현 가능.

원본 및 후보는 각4열5행, 마지막19번 셀은 빈칸. 실제 셀14/16/18의 분리된 두 작은 부품은 분리 지원영역이 유지되도록 프롬프트에 명시했다. 셀3/10은 얇은 연결편이어서 형태가 과하게 커지거나 색을 잘못 완성했을 위험을 Claude가 확인해야 한다. 생성물이 관절/몸체의 가려진 실제 지원영역을 임의로 재구성했는지와 내부 절단면 선도 확인 필요.

unit151~155_production_assembly.png는 새19종+기존 연결 파츠의 **원본** 조립을 보여주는 제작자료다. 완성된 HD 재생/시각 QA 증거가 아니다. 기존 파츠 품질이 맞는지까지 보장하지 않는다.

## Claude 재생 인계

```powershell
python scripts/verify/verify_runtime_path.py --state test_current/combat/named_attacks/unit_151/mechanical_cutin_168.state --frames 280 --save-frames 180 195 210 240 --track-atlas aestivalis_ground195_missing --name aestivalis_ground195_151
```

152~155도 해당 state로 각각 실행. 캐시 원본의 팔레트0 실색(151붉은 분홍/152파랑/153분홍/154주황/155청록)을 기준으로 비교한다. 렌더 레이어, 기체 통째 교체 여부, 모든 지원영역 표시·누락·접합은 검증대기 상태다.
