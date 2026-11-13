# 합체1560 마징카이저 작은전신 3파트 재제작 후보

미검증 후보. 공식QA/실제재생은Claude. 라이브/DB/코어 변경없음.

frame_1560.state 로드+1 실제cachedOBJ/renderedOAM 팔레트1 OAM19~21, 기존legacy3 재제작이며신규누락3로집계금지. 계약/실제palette/indexSHA/기존ID installation_map.json·source_identity_and_connection.json. ROM14886첫bytes일치. 이전Great/Mazinkaiser새atlas동일actualRGB와중복없음.

원본한기체의3사각형은48×40연속원본에완전히비겹침으로배치됨(joint_partition_provenance.json). 서로다른기체가있는전체화면master나가려진다른파트내용을사용하지않았다. 원본palette동일·반전없음. 한새전신을생성하고원래세사각형으로역투영. 원본alpha찍기없음.

imagegen exec-692c242f 새그림이오른쪽윙상단에서원본사각형지원밖36/15201불투명pixels를만들어, 생성도구 exec-9be86cea로오른쪽윙상단만안쪽으로접은parts_generated.png로교정. 최종지원밖10/15210(0.066%),4배texel기준native1pixel미만의상단경계잔여는projection_support_report.json. 이잔여를원본alpha마스크로지우지않았으며Claude가경계판정할것. 주요손/팔/다리/윙은원래세사각형안에있고생성그림을잘라새파트로구성했다.

candidate_atlas.png864×288/native216×72 정확4배. SHAc10e8f21cb722e1dd10fbb79d19a814c7d4bbcaff81958a591e218cc97e89aa9. 원본indexSHA/색/alpha/크기 mechanical_contract_checks.json,빈후보0 candidate_presence.json. 이검사는품질통과아님. candidate_pose_production.png는세파트재조립제작자료이며HD게임재생증거아님.

눈은원본노랑으로,머리의청록사각패널은눈으로늘리지않고실제위치유지하도록그렸다. 전체원본actual보라갑옷/빨강윙·V/노랑표지기준. 작은원본에서모델이손가락·관절세부를늘리거나색면·비율을바꿨을가능성은Claude가판정해야함. 3사각형경계에새검정캡은추가하지않았다.

Claude:
```powershell
python scripts/verify/verify_runtime_path.py --state test_current/combat/mazinger_combination/frame_1560.state --frames 120 --save-frames 0 15 30 60 --track-atlas mazinkaiser_combo1560_pose --name mazinkaiser_combo1560
```
