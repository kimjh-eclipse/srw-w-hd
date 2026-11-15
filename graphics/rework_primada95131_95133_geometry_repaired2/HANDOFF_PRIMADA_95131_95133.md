# 프리마다 밝은 기계 자세 2개 형태 교정 후보

같은 ID #95131/#95133만 교체할 미검증 후보입니다. 신규 누락 추가 0. 라이브/DB/코어/공식 QA/실제 HD 재생 없음.

## 원인과 입력

- 최신 codex_art_recheck_current/classified.json의 machine lost이며 현재 live atlas observed_fixture347_bright_pose160_eight가 그대로인 것을 확인했습니다. colour103 일괄 수정은 하지 않았습니다.
- 원래 패킷 test_current/parts/primada_bright_pose160_native1398/packed/install_contract.json의 실제 cached 두 행을 읽었습니다. actual index bytes/전체16팔레트/RGB CRC를 live spec과 검산했습니다.
- 원본 전체 문맥: actual_mechanical_pose_347_160/whole_native_context.png. 분홍색 원통·바퀴형 기계의 일부입니다. 원본 IMG와 실제 소유 기체 번호는 미확정이며 카탈로그 EI-29로 단정하지 않습니다.
- 같은 actual +160 source, frame/epoch/OAM/screen(121,66)/(101,70)/flip없음 등 contract.json 보존. source.state는 native_weapon_source_347_1398/unit347_weapon1398_source.state, offset160.
- current actual texture_key로 parts_baked.sqlite를 **mode=ro** SELECT만 해 구운 RGBA를 읽었습니다. 두 원래 그림은 넓은 판과 내부면을 가는 기둥처럼 축소했습니다. baked에도 같은 모양이어서 굽기 중 소실이 아닙니다.
- 현재 #95131: IoU .097/미칠 .878/밖 .347, #95133 .241/.746/.016. 검정 재질을 포함한 실제 큰 면적 소실입니다.
- 원래 패킷 raw 포함관계0. 정상 부모 동일 child를 새 교정이라고 셈하지 않았습니다. 같은 atlas 다른6개 불변 스냅샷은 preserved_normal6.json/최신 비교 preserved_normal6_latest.json.

## 제작

- 첫 참조는 실제 native 두 조각, 두번째는 전체 기계 문맥만 제공했습니다. 전체 기체나 캐릭터 얼굴을 새로 그리지 않았습니다.
- 넓은 분홍 패널, 짙은 자주/검정 불투명 내부, 작은 회색 U/V 삽입면을 새로 생성했습니다. #95131 오른쪽 직선은 인접부품과 만나는 내부 절단면이므로 새 검은 캡을 만들지 않도록 요청했습니다. #95133을 사람 얼굴/눈/보석/빈 고리로 자동완성하지 않도록 요청했습니다.
- 생성 원본 exec-48d465e4-f28d-4975-bbb4-ac5d46cd4807.png는 generated_two_halo_rejected.png로 보존. 외부 분홍 흔적이 보여 도구로 후광 제거를 추가 요청했습니다.
- 최종 exec-dff2ff96-ec05-49dc-979b-d52077b848c4.png를 generated_two_raw.png로 보존. 배경 RGB에는 분홍 값이 남지만 검사 좌표의 alpha0이며, 그 색만 보고 불투명 키 잔여라 단정하지 않았습니다. 원본 RGB/alpha 전사·알파 문턱 삭제·침식/팽창·재색칠은 하지 않았습니다.
- 자체 생성 전체 RGBA를 실제 원본 bbox로 기하 확대·정렬만 했습니다. native 지지영역을 마스크로 덮어찍지 않았습니다. initial_alignment_provenance.json.

## 설치 후보

- installation_map.json: 2개 같은 ID, 기존 flags/fullpalette/index/resource/source속성 보존. 새 atlas 좌표 x0/x64, 그 외 정상 그림 불변.
- candidate_atlas.png SHA256 `f0ef0e12733df3876f4769a93b3ccc62c9f56cc604d972da008a7913a0b6fcf9`. native_atlas.png/contract.json 함께 사용.
- candidate 및 NullCache prepare 후 사전기하 두 개 모두 flags 없음, IoU .993/.993, 미칠0/외부0. 준비 후에도 실제 넓은 판이 남습니다.
- replacement_comparison.png 원본/현재 baked/새 후보 순서로 수동 제작 대조했습니다. 넓은 지지영역이 회복됐지만 이것을 실제 플레이 완료 판정이라고 하지 않습니다.

## Claude 확인 위험

- 새 그림의 직선적인 하드서피스 명암이 주변 기존 그림보다 평평할 수 있습니다. 작은 회색 삽입면과 분홍 하이라이트의 위치·넓이는 실제 조립에서 확인 필요합니다.
- 오른쪽 내부 절단면이 인접 기존 큰 바퀴/몸통과 매끈히 이어지는지, 검정이 실제 불투명 내부인 부분을 정확히 유지했는지 확인해야 합니다.
- 밝은 팔레트 +160만 교정했으며 원래 +155 어두운 변형 7종까지 해결했다고 주장하지 않습니다.
- 원래 fullcutin/pilot는 범위 밖입니다. 기존 source_owner=None과 원본 IMG 미확정은 유지됩니다.
- 미연결 대상도 새 2개 증가가 아니라 기존 #95131/#95133의 같은 ID 그림 교체입니다.
