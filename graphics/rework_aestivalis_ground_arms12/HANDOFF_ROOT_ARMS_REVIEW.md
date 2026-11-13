# 아스테바리스 육전151~156 실제미연결 손·팔12종

- 각unit151~156 mechanical_cutin_168.state +90(91회run). cached OBJ + rendered OAM 계약.6색각2종,전부제작전binding0/exact·indexed없음. 전체기체완료라는의미아님. 기존연결파트는whole_pose_dependencies.json.
- 원본index bytes는ROM IMG10778의(24,0,32,16)/(0,16,32,16)와12/12완전동일. 원본색은렌더시점실제팔레트. ROM PLT리소스번호가6개모두확정됐다는주장은하지않음(151/156만사용색후보발견).
- built-in image_gen으로12색별그림을한3×4시트에새로생성. pink/deepblue/crimson/orange/teal/periwinkle 각두손자세. 다른기체그림의재색칠없음.
- generated own-alpha major component로각셀crop을찾아원본bbox위치/크기에만맞춤. generated alpha보존,원본RGB/alpha stamp/도트덧칠없음. production_fitting.json 좌표기록. runtime768×768(4배).
- Claude확인:각unit+90와공격전후. 손가락/마디수·형태자동완성/손목둥근core크기,나머지기체HD와선굵기·손목절단면cap/경계,회전·affine/격자/대사창가림,아주낮은alpha색프린지. 팔레트pink와crimson/deepblue와periwinkle구분. 입력IoU기준통과는품질완료가아님. 독립QA·후보HD재생은수행하지않음.
