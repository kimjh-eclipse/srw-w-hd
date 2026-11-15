# EI13 묶음 #94884 실제 검정 지지면·하부 색 영역 교정 후보

같은 ID1개 교체 후보입니다. 신규 미연결 증가0, 정상26개 유지. 공식QA/HD재생/라이브/코어/DB 쓰기 없음.

## 원본과 실제 오류

- 최신 fixed current machine lost이며 live ei13_observed_mechanical_twentyseven이 같은 것을 확인했습니다. 원래 ei13_complete_observed_native1382/packed/install_contract.json의 actual cached source행에서16×16/155texel/index/full16/RGB CRC를 현재 spec과 재검산했습니다.
- source native_weapon_source_341_1382/unit341_weapon1382_source.state +170/OAM1/screen116,76. 원래 초기 그룹 ei13_initial_native1382/341_170 cell1, continuous component1 단독입니다. 정상 부모 동일raw 포함0. 다른 부품과의 기존 공유5쌍을 바꾸지 않습니다.
- actual_mechanical_pose_341_170/whole_native_context.png는4배 화면이므로 원래좌표를4배로 강조한 actual_bbox_context.png에서 위치를 확인했습니다. 실제 관측에서 이 source의75texel만 앞쪽 정상 부품에 가리지 않고 보였으며 전체155texel가 모두 보였다고 주장하지 않습니다.
- 현재 actual texture_key로 SQLite를 mode=ro SELECT만 해 구운 RGBA를 읽었습니다. raw 그림부터 실제 검정 상부를 붉은 삼각 장갑으로 자동 해석했고 baked에도 같습니다.
- 원본155texel 중90개는 RGB16의 **불투명 검정 지지면**입니다. 그 외 짙은 보라11/붉은31/분홍계23. 기존 그림을 같은 검정 재질 위치와 대조하면 충분한 불투명 어두운 면이 있던 곳은1/90뿐입니다. 단순 AA나 일반 음영 차이가 아니라 실제 색 영역 재해석 오류입니다.
- 따라서 정상 colour115 묶음을 일괄 변경하지 않고 이 machine lost 실제 오류1개만 고칩니다.

## 새 그림

- generated_raw.png는 imagegen 출력 exec-f48f22dc-764f-43a9-a5cd-5b9141c59aa2.png 보존. 원본 검정 상부를 빈 배경/완성된 얼굴·눈·헬멧/붉은 표면으로 바꾸지 않도록 명시했습니다.
- 원래 낮고 넓은 무광 검정 지지영역을 칠하고, 하부의 얕은 붉은/분홍 조각에만 색을 넣었습니다. 눈·관절·센서·홈 같은 장식을 추가하지 않았습니다.
- source 검정은 실제 원본 재질이며 인접 파츠 절단 경계에 새 외곽선을 그은 것이 아닙니다. 상부에 가상의 장갑 하이라이트/캡을 발명하지 않았습니다.
- 자체 생성 전체 RGBA를 bbox 기하 정렬만 했고 원본 RGB/alpha 전사·native mask로 깎기·문턱삭제·침식/팽창·재색칠은 하지 않았습니다. alignment_provenance.json.

## 설치와 생산 확인

- installation_map.json: #94884만 같은 ID 교체. contract.json actual fullsource/old spec/lookupflags/원래source속성 유지.
- candidate_atlas.png SHA `066d173a59ebaa82b2ec4c759ea7e2c6d6ed7f354e66a442ba02ab44db350b05`, native_atlas.png 함께 사용.4배64×64.
- candidate/NullCache prepare 사전기하 flags0, IoU .955/미칠 .013/외부0. 이전 .690/.219/.027보다 개선됐으나 실제 화질 합격 판단은 아닙니다.
- 검정 material 위치 생산 sanity check에서 기존1/90→후보79/90으로 늘었습니다(black_plane_material_presence.json). 이 측정은 원본 mask로 출력을 찍는 작업이 아니고 검정 실제재질을 지켰는지 보는 입력/후보 대조입니다. 공식 audit 대체가 아닙니다.
- replacement_comparison.png에 실제 native/current baked/new candidate를 저장하고 넓은 검정 상부 복원·얕은 하부형상을 직접 제작 대조했습니다. 정상26 spec 불변은 preserved_normal26_latest.json.

## Claude 확인 위험

- 검정90texel 중11개는 하부 AA/색 경계에서 여전히 다릅니다. 실제 head/인접 장갑이 가리는 순서에서 새 검정이 원래처럼 뒤에 남는지 확인해야 합니다.
- 하부 분홍 하이라이트가 원본의 작은 색면보다 연속된 물결무늬처럼 보일 수 있습니다. 새 홈/생물학적 주름을 표현하려는 것이 아니지만 실제 작은 조각의 기계 표면과 맞는지 판정 필요합니다.
- 검정 지지면 상단의 매끈한 곡선과 원래 계단 실루엣 사이에 AA 차이가 남습니다.
- 기존 실제 관측75texel/전체155를 구분하며 이 그림1개로 EI13 모든 기체/기술/다른 자세 완료라고 하지 않습니다.
