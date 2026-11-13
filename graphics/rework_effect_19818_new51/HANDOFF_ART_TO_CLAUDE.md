# IMG19818 새 그림 제작 인계

- 후보 `candidate_atlas.png`, 원본 `native_atlas.png`, 원본 확대 `native_reference.png`, 생성 원출력 `generated.png`.
- 연결 입력 `install_contract.json`: 51종. 실제 cachedOBJ 관측 51종, 원본 IMG/PLT와 실제 팔레트 16값이 완전 일치하는 미관측 0종.
- 각 계약에 원본 indices 압축 바이트, RGB/index hash, source/atlas 좌표와 실제 팔레트 증거 포함. 미관측은 slot/binding/fixture/frame=None, 관측으로 표시하지 않음. 활성 exactRGB/indexed 연결 없는 항목만 제작.
- 캔버스 1024×640, 원본 256×160의 정확4배. 한 벌 생성 후 원래 위치에서 분할하므로 겹침은 동일한 그림. native RGB/alpha 스탬프 없음.
- 모든 계약 crop maxA≥16 기계 확인: True. 공식 audit·재생·독립 시각 판정 하지 않음.
- Claude 확인: 관측 계약 `fixture/frame`와 `observations`의 전체 프레임 참조. 색 단계/미세 파편·선폭/접합·알파는 검증 대기. 생성기가 원본 주변보다 넓은 밝기나 질감을 추가했을 가능성이 있어 원본 쌍으로 확인 필요.
- 라이브/DB/코어 변경 없음, root 설치·굽기 담당.

- 중요: ROM 기본PLT와 실제 분홍variant가 달라 full16 source확정확장은 하지 않았습니다. actual cachedOBJ로source바이트동일한51종만 포함. 생성기는 오른쪽큰광원경계를 사각형에 가깝게 정리했을 가능성 및 회색파편주변색 위험이 있어 Claude 원본쌍 확인 필요. QA전무.
