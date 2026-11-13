# IMG21284 기본26 + 별도 밝기변형2

- candidate.png832×256/native208×64, new_candidate_contract.json26계약(실제 기본팔레트1벌/raw26).
- SHA256 f55912ae1390272de6c5b68d8d9cf4de6b6f480a7ddf195ed7f9452fa2e8a09e
- 실제 source test_current/combat/named_attacks/unit_390/mechanical_cutin_153.state, frame190이후. 원본기체가 아닌 흰 전격/속도선+pink탄두/회청투사체/노랑불꼬리 영역입니다. source_contract.json의 actualcached바이트/팔레트/OAM 근거 보존.
- 같은 source 전체를 한 장 새 그림으로 생성하여 source좌표 동일영역 공유. 새그림조각간 겹침 불일치 없음. 원본RGBA stamp/다른FX재색칠없음.
- 나머지 group1/2는 source112,0 16×16 회색ring의 frame200/210 밝기변형 각1입니다. fade_two_contract.json으로 따로 보존. 두 개를 신규형태나 제작완료로 세지 않았고 실제런타임밝기처리/추가팔레트연결은Claude검증큐입니다.
- prepare26 모두maxA255/빈crop0.19crop에서분리흔적1~4제거. fill/cutink0. 실제HD재생/독립QA/라이브DB변경미실행.
- Claude확인: 흰전격/속도선이광평면이어야하는데 생성음영이금속같이볼록해보일수있음. 원본회청영역보존과과장된하이라이트구분,세부발사체너비·ring공백·작은불꽃생존·sourcecutplane이음새확인필요.
