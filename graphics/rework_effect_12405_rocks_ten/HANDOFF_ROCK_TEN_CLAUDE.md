# 기존 키색 지적 IMG12405 암석 파편 실제색 재제작10

라이브/DB변경, 독립감사/재생은 하지 않았습니다.

- source선정: green_key_review/report.json의 기존 binding46275/46247/46249/46273/46252/46274/46260/46282/46250/46276. 현재 production manifest와 겹치지 않고 보호5263 밖.
- 원래등록palette와 실제색이 다르므로 기존hash를 새그림에 억지로 유지하지 않습니다. new_candidate_contract.json의 실제hash10을 기준으로 parent가 연결하며, replace_bindings는 기존 source선정 근거입니다. 다른팔레트 기존 경로까지 완전히 고쳤다는 뜻이 아닙니다.
- 원본확정: unit226 weapon915_source.state frame637/643/649/661 실제 rendered_obj_cache. 원본IMG12405 해당source좌표 rawindex와 actual byte동일을 확인. 실제palette1벌.
- candidate_rocks_ten.png 640×384/native160×96 4배, SHA374c498bec6c89a088fad3261f151e88167bdec377686dd4ee0f5a3498d21b1e.
- 새 회녹색암석 전체 모양·명암을 그렸고 초록지우기/원본alpha나RGBstamp/다른효과 재색칠을 하지 않았습니다. 자체alpha220+형태정리만 적용.
- production_report.json prepare10/10 maxA255,지원면적비1.044~1.249. 2crop에서 작은 분리성분1/2개 제거. nativefill0/cutink0.
- Claude 확인: 작은입자 배치, 반복되는 원본영역끼리 새로 그린 조각의 세부차이, 원본보다 약간 둥글고 큰 모서리, 원출력 얇은 녹색프린지가 실제 후보/재색칠에 남는지. production presence는 품질판정이 아닙니다.
- 원본10은 실제한프레임 동시조립이 아니라 같은효과의 연속 crop들입니다. 첫5263와 공유런타임 미변경.
