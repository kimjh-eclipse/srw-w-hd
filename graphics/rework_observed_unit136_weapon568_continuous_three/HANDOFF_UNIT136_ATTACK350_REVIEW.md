# 실제 unit136 / weapon568 메뉴350 전신3조각 후보

상태 `CACHED_OBJ_ARTWORK_CANDIDATE_UNVERIFIED`. 실제 HD 재생/공식 검사 Claude대기. 라이브/공유 코드/코어/DB 변경없음.

- 설치 입력 installation_map.json/candidate_atlas.png/native_atlas.png/contract.json.
- 후보 SHA256 `5f6db5a49cbf868fc0855244af5c7eb15644ed12aa3f3d4456a45306f8114393`.
- fixture source_mechanical_fixed_136_568_350/source_pose.state +0. 메뉴350 actual cached OBJ/OAM/팔레트/코어SHA 보존.
- 빨강/검정 기체한자세를 실제화면에서 위64×32/아래64×32/왼쪽8×16의3조각으로표시하며 전부 actual exact0/indexed0. 원본IMG10519의세raw사각형바이트와일치한다. 전체16색 PLT1793 bank0일치.
- 실제화면 사각형은(104,59)64×32/(104,91)64×32/(96,91)8×16. 원본IMG의세사각형은가로로저장되어있지만 그대로가로로붙여그리지않고 실제화면의72×64 공통native조립을먼저만들었다(actual_full_pose_continuity.json).
- 한몸의새생성그림을그린뒤 원래OAM사각형으로나눠 머리/몸통/팔의중앙절단면을같은생성픽셀로이어지게했다. 전체재조립RGBA동일/사각지원밖누락0. 가장작은왼쪽지지조각도같은그림의해당영역을갖는다.
- actual 원본의붉은장갑/검정면/주황·노랑안테나와작은하늘색눈/카메라를참조했고카탈로그이름만보고기존다른그림을재사용/재색칠하지않았다. 생성원본/자체alpha<64정리근거보존·고알파RGBA불변. native RGB/alpha/mask 복사·스탬프없음.
- candidate_pose_production은실제좌표로신규3조각을조립한제작참고이고실제HD게임검사가아니다.

Claude위험: 큰왼쪽붉은무장/장갑덩어리·오른손/다리의형태를모델이임의로완성했는지,원본의세부기계구조와색면위치/눈·카메라·뿔색/명암을확인해야한다. 새그림이원본보다반사광과분홍하이라이트가강할수있고왼쪽아래에발/장갑구조를가정했을수있다. 가로32px분할선/작은지지대의연결과실제레이어순서는Claude재생확인대상이다. 한관측한자세3조각의후보이며전체기체/무장완료로세지않는다.
