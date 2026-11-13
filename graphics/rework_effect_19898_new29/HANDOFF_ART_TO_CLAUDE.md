# IMG19898 새 그림 제작 인계

- 후보 `candidate_atlas.png`, 원본 `native_atlas.png`, 원본 확대 `native_reference.png`, 생성 원출력 `generated.png`.
- 연결 입력 `install_contract.json`: 29종. 실제 cachedOBJ 관측 29종, 원본 IMG/PLT와 실제 팔레트 16값이 완전 일치하는 미관측 0종.
- 각 계약에 원본 indices 압축 바이트, RGB/index hash, source/atlas 좌표와 실제 팔레트 증거 포함. 미관측은 slot/binding/fixture/frame=None, 관측으로 표시하지 않음. 활성 exactRGB/indexed 연결 없는 항목만 제작.
- 캔버스 1024×1536, 원본 256×384의 정확4배. 한 벌 생성 후 원래 위치에서 분할하므로 겹침은 동일한 그림. native RGB/alpha 스탬프 없음.
- 모든 계약 crop maxA≥16 기계 확인: True. 공식 audit·재생·독립 시각 판정 하지 않음.
- Claude 확인: 관측 계약 `fixture/frame`와 `observations`의 전체 프레임 참조. 색 단계/미세 파편·선폭/접합·알파는 검증 대기. 생성기가 원본 주변보다 넓은 밝기나 질감을 추가했을 가능성이 있어 원본 쌍으로 확인 필요.
- 라이브/DB/코어 변경 없음, root 설치·굽기 담당.

- actual4단계는ROM색과다르므로미관측추가안함. unit314_weapon1279_source.state actual29전용. source_palette_bank는실제색단계배치인덱스,ROM동일주장아님. full16_exact=False 증거참조.
- 그림위험: 생성기가흰색core를원본보다유동적으로그렸고주변bloom이넓을수있음. 네단계구멍/원래solid피복과알파는Claude검증대기.
