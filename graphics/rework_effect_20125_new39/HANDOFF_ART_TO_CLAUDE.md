# IMG20125 새 그림 제작 인계

- 후보 `candidate_atlas.png`, 원본 `native_atlas.png`, 원본 확대 `native_reference.png`, 생성 원출력 `generated.png`.
- 연결 입력 `install_contract.json`: 41종. 실제 cachedOBJ 관측 41종, 원본 IMG/PLT와 실제 팔레트 16값이 완전 일치하는 미관측 0종.
- 각 계약에 원본 indices 압축 바이트, RGB/index hash, source/atlas 좌표와 실제 팔레트 증거 포함. 미관측은 slot/binding/fixture/frame=None, 관측으로 표시하지 않음. 활성 exactRGB/indexed 연결 없는 항목만 제작.
- 캔버스 1024×1152, 원본 256×288의 정확4배. 한 벌 생성 후 원래 위치에서 분할하므로 겹침은 동일한 그림. native RGB/alpha 스탬프 없음.
- 모든 계약 crop maxA≥16 기계 확인: True. 공식 audit·재생·독립 시각 판정 하지 않음.
- Claude 확인: 관측 계약 `fixture/frame`와 `observations`의 전체 프레임 참조. 색 단계/미세 파편·선폭/접합·알파는 검증 대기. 생성기가 원본 주변보다 넓은 밝기나 질감을 추가했을 가능성이 있어 원본 쌍으로 확인 필요.
- 라이브/DB/코어 변경 없음, root 설치·굽기 담당.

- 중요: ROM PLT20124의청색과actual색이달라미관측확장안함. 실제cachedOBJ 3색단계41원본바이트계약만포함. source_palette_bank0/1/2는이3actual단계레이아웃인덱스이며ROM색동일주장아님. source_palette_confirmation/full16_exact=False와actual_proof를참조. 41계약은39actualhash+색변형source오버랩복수source좌표가있을수있으니고유hash로집계하세요.
- 초안주의: 작은파편이형태보다장식적인블록으로그려졌을수있고매끄러운HD가아닌픽셀형질감이남을가능성. Claude판정전완료아님.
