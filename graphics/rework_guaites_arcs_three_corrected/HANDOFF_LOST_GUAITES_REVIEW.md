# Guaites 호3 동일ID 교체 후보

상태: 미검증 그림후보. 신규미연결/완료수추가없음. 공식 verify_new_art/실제HD 재생은Claude담당. 라이브/코어/DB 변경없음.

- 설치입력 installation_map.json/candidate_atlas.png/native_atlas.png/contract.json/replacement_targets.json.
- 후보 SHA256 8fd24d294d29177f2a8c994891dce2d0db11a855491e6cf8ea092a5df9ea6178.
- 보고서의1-based #94608/#94609/#94611만교체대상. metadata94607/94608/94610이고actualRGB2374703497/1684750652/4173263909. 현재old_spec와원본계약index바이트/hash/w/h/전체actual팔레트동일확인.
- #94610(864110818)은classified lost/다른flag에걸리지않았고원본source사각교집합도없어기존그림그대로둠. preserved_binding_94610.json에기록. 같은묶음의#94607/#94612도손대지않음.
- source_mechanical_fixed_74_313_300/source_pose.state +0, 실제호의원본8×16/32×32/16×32각지원과screen(162,65)/(170,65)/(146,65)보존. raw저장위치와화면위치가다르므로연속하나의완성고리로발명하지않고세조각별실제방향을그림.
- 기존가는호에서빠진폭/면을고형녹색띠로새로그렸다. 첫작은J는새생성 exec-b8296c07-6c80-4765-8330-9aadd8defe7e.png, 마지막S호는 exec-9f44c8ac-ca2a-4137-a525-ddcdee9b7311.png. 가운데긴호는root곡률지적후 exec-8dd1090b-602b-4f92-a693-2e3ba33db22f.png로새로교정했다. 자체생성끼리만시트로조립했고다른두호cropRGBA완전불변SHA근거있음.
- 앞선도트확대/후광그림및작은J중앙알파구멍후보는미채택으로보존. 원본RGB/alpha스탬프나알파팽창으로구멍을메우지않고그부분만완전고형면으로재생성함.
- alpha문턱/MinMax팽창·침식없음. 원래전체생성RGBA셀을변환하고낮은alpha도남김. 정렬앵커160은스케일/위치측정용이며alpha수정이아님. 일반OAM캔버스밖scissor만적용. alpha_and_alignment_provenance.json 참조.
- 기존renderflags/resource/source좌표/dynamic_palette설정은old_spec그대로유지. replacement_preview.png는원본/기존/새후보제작참고이며공식QA판정이아님.

Claude 위험: 새호의굵기/곡률/끝단이원본을넘어두꺼워졌거나더평평해졌을수있다. 특히첫J의짧은가로발과수직길이·마지막S호의굽음/넓은초록면비중·밝은녹색범위를봐야한다. 생성alpha는보존했으므로남은반투명/AA경계도확인필요. 자동검사통과또는해결완료주장없음.

## 가운데 긴 호 후속 정정

root가초기후보의과도한C형곡률을지적해그후보는보류/보존했다(candidate_bowed_curve_rejected.png). 실제원본9개열중앙선과대조하니최대2.90nativepx이동이있었다. 원본앵커를측정한진단용곡선가이드로새그림을다시생성했다. 원본RGB/alpha를최종그림에찍지않았다. curve94609_path_geometry_v2.png는생성참조용가이드이지설치그림이아니다.

새그림은일반생산정렬로2HD픽셀(0.5nativepx)상향평행이동했다. 곡선을비선형변형하거나폭을바꾸지않았고alpha팽창/마스크도없다. 9앵커의최대이동은1.00nativepx로남아있으며완전동일성을주장하지않는다(curve94609_centerline_after_rework.json). 처음작은J/마지막S 두후보cropRGBA는이전과완전불변이다. 이수치는root요청에따른제작기하확인이며공식QA대체아님.
