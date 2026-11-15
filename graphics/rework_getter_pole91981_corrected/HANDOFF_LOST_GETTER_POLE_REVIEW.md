# 겟타 청보라 봉 형태 같은 ID 후보1

미검증 후보. 신규 완료 수 없음. 공식 검사·실제 재생은 Claude 담당이다.

설치 installation_map.json / candidate_atlas.png / native_atlas.png. 후보 SHA256 29ab60aa6856df03ba5a4218076ec09513f15dc913fdf5ba00e252a29e087eac.

- #91981 metadata91980 RGB2684431255 / index3563099472 / 32×16. 실제 getter_cutin.state +90~126에서86회 관측한 source 패킷을 보존했다. palette15는 기존 실제 cached full16색을 그대로 복사했고 RGB 역산하지 않았다.
- 원본 source 후보 IMG14461/14485 [48,128,32,16] 등은 원래 자료 그대로 source_alternatives로 유지했다. 현재 atlas의 source 좌표가 단일 소유를 확정하는 근거는 아니다.
- source_packet_record에 모든 관측 rows/actual palette/bytes를 보존하고, source_contract에 첫 +90 OAM8의 attrs와 원본 좌표를 명시했다. 화면 중복/반전 사용은 원래 관측 그대로다. catalog unit 소유는 미확정(None)이며 임의297로 붙이지 않았다.

원본은 토마호크 연출에서 보이는 굵기가 있는 청보라 대각 봉/축의 잔상 형태다. 기존 그림은 넓은 검정/보라 면이 한 줄로 줄었다. 새 그림은 원래 대각 기울기와 넓은 검정/보라 물질을 유지하며 끝캡/화살촉/빛을 추가하지 않도록 만들었다. 이전 짧은 세로 봉1과 전체 무기 다른 파츠는 수정하지 않는다.

parts_generated_raw.png는 내장 imagegen exec-064db209-cd54-4957-a3cd-a99fa5751018.png. 원본 RGB/alpha stamp 없음. 생성 alpha 문턱/침식/팽창 없음. native bbox는 위치/크기 정렬에만 사용했다. 실제 hash/indices/full16palette는 기존 연결과 일치했고 dynamic_palette=True를 보존했다.

## Claude 위험

원본의 작은 교차하는 하이라이트 점이 새 그림에서 매끈한 면으로 이어질 수 있다. 봉의 검정/보라 굵기, 여러 잔상과 겹칠 때의 의미, 절단 양끝과 인접 무기 연결은 실제 재생으로 판정해야 한다. 제작용 replacement_preview.png는 공식 QA가 아니다. 얇은 선을 두껍게 했다는 사유만으로 완료 주장하지 않는다. 라이브·코어·DB·공식 QA·물리 입력 변경 없음.
