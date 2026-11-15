# 합체 1560 팁 두 그림 / 같은 ID 세 연결 교체 후보

미검증 후보. 신규 완료 수 없음. 공식 검사·실제 재생은 Claude가 수행한다.

- 설치 입력은 installation_map_with_duplicate3.json. 두 개의 새 그림을 세 기존 ID에 공유한다. 기본 installation_map.json은 중복을 추가하기 전의 두 그림 자료다.
- #68906 RGB3904433334 32×8: 실제 OAM의 날개·머리 가장 위 분리 팁. 동일 actual 원본인 #93318에도 같은 후보 셀0을 사용한다. 두 ID의 raw indices/wh/full palette/hash 동일 근거는 same_actual_duplicate_dependency.json.
- #93351 RGB1708426716 16×8: 뿔의 꼭대기5texel과 별도 보라1texel 조각. 실제 source owner=None 유지. 메타 source_x/y만으로 IMG 소유를 단정하지 않는다.
- candidate_atlas.png SHA256: 389c44b89143b9477ff25b7534becb5f1bf9ba3da523b80a66eedc0900f80a5a.
- 실제 장면: test_current/combat/mazinger_combination/frame_1560.state +0. 원본 계약 contract.json에 OAM/attr/actual palette/화면 좌표 보존.

## 제작 내용

원본의 분리 팁 개수와 작은 채움면을 유지하고 실제 색(분홍/흰색/보라/황토)을 따라 새로 그렸다. 그림이 없는 빈부분을 연결하지 않았고 알파 문턱으로 작은 조각을 지우지 않았다. 전체 기체 이미지는 문맥 참조로만 썼고 상부 팁 조각만 제작했다. 생성 원본 parts_generated_raw.png 보존. 내장 imagegen 결과 exec-957235e2-51ef-41ca-a57d-ab2eae94a11d.png.

## 보존과 위험

#68895 주먹은 모서리 면적 차이 외 뚜렷한 그림 소실을 확인하지 못해 그대로 보존했다. 색 경고나 lost 수치만으로 바꾸지 않았다. 이번 두 팁도 원본 1texel 작은 성분을 매끈하게 만들면서 면적·형태가 달라질 위험이 있다. 아래 정상 몸체와 맞닿는 가로 경계의 선/색 연결은 Claude의 실제 조립 판정이 필요하다. 같은 actual 두 ID를 서로 다른 후보로 설치하지 말아야 한다. 두 ID 중 실제 활성 연결의 정리는 root가 담당한다.

기존 dynamic_palette=True 보존. native RGBA/alpha stamp, 형태 마스크, 알파 문턱, 팽창/침식 없음. replacement_preview.png는 제작용 대조이며 공식 QA가 아니다. 라이브/코어/DB 변경 없음.

## RGB/indexed 분기 보존

93318은 rgb_enabled=False / indexed_safe=True / dynamic_palette=True인 indexed fallback이다. 68906은 RGB 활성 / indexed 비활성이다. 같은 raw/전체 팔레트여도 lookup 역할은 다르다. installation_map_with_duplicate3의93318 proposed_binding은 기존93318 spec에서 위치/atlas만 바꿨으므로 이 False/True 플래그를 보존한다. root의 같은 ID 교체 도구에서도 각 기존 lookup 역할을 그대로 유지해야 하며 임의 RGB 활성화하지 않는다.
