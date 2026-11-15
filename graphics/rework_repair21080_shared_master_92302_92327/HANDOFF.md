# 21080 공유 부모 상단12성분 교정

실제소실 자식92302와 공유부모92327의 상단32×8영역을 새연속곡선·연속색면으로 교정했습니다. 변경2개이며 다른동일atlas47개와 부모하부는 그대로입니다. 실제12성분의 자리/폭을 유지했고 동일1px남색2점은 같은ownRGBA를 공유합니다. 작은1px점은 생성물 불투명내부 재질crop이며 독립HD세부이득은제한적입니다.

중요한 관측구분:92302는 실제관측계약, 부모92327의전체32×32형상은 actual index/fullpal 원천확정이나 전체형상재생미관측입니다. 기존 unobserved_completion 계약의 actual_observed=false와 actual_index_observed=true를 그대로 유지했습니다. 추정frame/state를 새로 넣지 않았습니다. merged_actual_source_contract51.json과 final_flat_contract.json을 참조하세요.

source master[128,32,32,32] → candidate[128,128,32,32]. native256×192 / candidate1024×768 정확4배. actualfull16/BGR555/rawindex/source_box/atlas_box 및 시작specSHA/4파일SHA를 포함했습니다. 같은own_master.png를 부모와자식이 공유합니다. 원본RGB/alpha/mask전사·출력alpha문턱삭제·형태학삭제없이 생성RGBA crop/resize만사용했습니다. 회색 manual_comparison_gray.png에서 원본/이전/새그림을 보았습니다.

위험: tiny1~2픽셀 성분이라 HD세부이득이 작고 생성물 내부농도는 실제팔레트의 연속근사입니다. 부모전체형상 재생미관측은 남습니다. 중앙쓰기/연결/굽기/공식QA를 수행하지 않았습니다.
