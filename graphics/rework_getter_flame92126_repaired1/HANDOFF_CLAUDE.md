# #92126 노란 불꽃 연출 교정 — Claude 대기

기존 machine 분류였으나 실제22062 노란/주황 연출임을 역할 정정했습니다. source는 getter_true_missing_22054_22062의 actual cached 계약, getter_cutin.state +82, source IMG22062(40,0,32,32)입니다. 같은 기존ID92126만 새 atlas getter_flame92126_repaired1로 교체하는 후보입니다.

원본 raw index bytes/full16색 BGR555/RGB hash1419942958은 모두 기존 계약과 일치했습니다. candidate atlas 좌표는 기존[32,0,32,32]이고 source[40,0]과 다릅니다. normalized spec 실제 좌표로 NullCache prepare했고 maxA255, reference_fill0, alpha문턱삭제/원본RGBA전사 없음입니다. 새그림은 자체 생성 RGBA를 원본bbox로 등록했습니다. 기존atlas의 나머지 영역은 그대로입니다.

첫 출력은 현실적인 불꽃 돌기를 과하게 발명하여 rejected_invented_flames.png로 보존/미사용했습니다. 최종은 원본의 굵은 C형 밴드·갈라진 위쪽 돌기를 유지한 평면 그림입니다. 원본격자 IoU .863/면적1.041/미칠한5.45%라 아주 가는 돌기 일부/둥근모서리 AA 차이가 남습니다. 기존 IoU .496에서 개선됐지만 공식검사/실재생 정상판정이 아닙니다. native_candidate_pair.png로 비교하십시오.

ready_replacement1.json/normalized_installer_contract1.json/candidate_atlas.png/native_atlas.png를 root에게 인계합니다. 공유코드·live·DB 변경과 실제재생은 하지 않았습니다.
