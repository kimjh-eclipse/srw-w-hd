# 토라스 머리/등 접합선 교정 후보4개

사용자제보결함에대해root가보호prefix후보제작을명시승인한범위입니다. 기존중앙그림/metadata는수정하지않고별도후보만만들었습니다. 변경제안은4985/4988/4996/4997 네개이며나머지4984~4997중10개는기존spec/atlas/그림그대로입니다.

실제기체 unit8 トーラス/토라스,IMG1219/PLT1220입니다. 기존atlas명space_pirate_body는옛임의명칭입니다. 실제cached14개원본raw/full16와ROM일치근거는이전taurus_seam_review와이번actual_idle_contract14.json에있습니다.

## 새그림과같은master

네부품을실제OAM자세56×48 master(화면원점96,54)에한벌로그려머리4997↔4996/등4985↔4988의master y16 내부수평선과투명한줄을없앴습니다. 기존부품PNG를개별로봉합하지않고새로생성한master의연속면을각사각형에공유했습니다. 별도generated_master.png는내장imagegen실제생성원천입니다. 원본native는형태/색/원천계약참조만했으며원본RGB/alpha/mask를출력에전사하지않았습니다. 생성RGBA crop/resize로전체bbox를실제자세bbox에등록했고출력alpha문턱삭제/형태학삭제는없습니다. own_geometry_registration.json에4개bbox좌표만쓴registration근거가있습니다.

목표네파츠전체가새master그림이며그안의면음영/기계세부는새로근사했습니다. 다른10개부품은기존그림이며후보계약에포함하지않았습니다. 처음좁은접합strip만바꾸는시안은하이라이트불연속이남아폐기했고rejected_local_strip_*에인정근거만보존했습니다. 최종은own_master_56x48_4x.png입니다.

master_box:
- 4985 [0,8,32,8] → source_IMG1219[176,8,32,8] → candidate_atlas[32,0,32,8]
- 4988 [8,16,32,32] → source[0,0,32,32] → atlas[0,32,32,32]
- 4996 [40,16,16,32] → source[32,0,16,32] → atlas[0,96,16,32]
- 4997 [40,0,16,16] → source[80,0,16,16] → atlas[32,96,16,16]

native_atlas128×128 / candidate_atlas512×512정확4배RGBA입니다. 후보에서다른10개영역은투명이며설치대상이아닙니다. currentprior specSHA/네파일SHA는ready_candidate.json에있고네원본사각의raw/indexhash/hash/full16/관측frame·state/source_box/atlas_box는final_flat_contract4.json에있습니다. source_normal_preservation_proof.json은기존10개spec/중앙PNG미변경및native원본대조근거입니다.

## 그림대조와남은위험

master_current_candidate_gray.png와pose_current_candidate_gray.png를수동확인했습니다. 후자는같은actual OAM위치에현재PNG와새4파츠+기존10파츠를직접합성한그림입니다. 두불필요수평선은새그림에서사라졌습니다. 이는실제PartsRenderer.prepare/게임재생/공식QA결과가아닙니다.

현재모델면음영의농도,머리끝/등판세부비율과기계패널선은새생성물근사라시각차이가남습니다. 전체source자세bbox로등록했으나모든외곽점이원본과동일하다고주장하지않습니다. 후보는정확4배이므로종전1254pxatlas의9.8배원천과직접확대대조시선명도차이가있습니다. 사용자가제보한정확frame은없어서기존fixture의같은14부품자세를분석했습니다. 사용자방향미리보기는좌우반전분석자료이고actual flip=false계약은유지합니다. 중앙설치/굽기/공식QA는Claude담당입니다.
