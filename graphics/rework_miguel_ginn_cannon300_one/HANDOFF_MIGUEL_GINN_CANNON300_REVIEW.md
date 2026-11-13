# 미겔전용 진 실제64×64 자세1종 — 미검증 후보,녹색선1보류

- 실제 menu unit132/weapon552 +300. `source_mechanical_fixed_132_552_300/source_pose.state` +0. palette0 64×64 actual RGB1739415205 exact0/indexed0 미연결1을새그림제작. IMG10162(192,32) 원본전체4096index bytes 일치/PLT1737 bank0사용색일치. catalog120/132가같은미겔전용진range1737..1748을공유함을확인,팔레트기본색일치이며fade색아님.
- 중요관측범위: OAM0 screen(10,-50)으로이프레임에는아래14행만화면에걸친다. 계약/원본64×64전체는rendered cachedOBJ에존재하므로그림전체지원은보존했으나,기체전체가화면에보이는실제HD재생검증은없다. 현재부분관측을전체장면완료라고세지않음.
- 단일주황기체의붉은단안/황토·노랑면/회청·회백연결/실제녹색무장부재를그대로참조. 녹색을키색으로지우지않음. source상단·오른쪽잘린부재도원래캔버스범위유지,전체날개임의완성안함.
- 같은palette0 녹색선8×16 RGB1800241813/27texel은화면(128,12)로기체와분리. 같은IMG10162(248,0)/PLT1737일치이나역할불명. 인접native offset10에는그선/기체0모두사라지고palette10 affine효과만있고,+30에는OBJ없음. 확인한것은원본입력변화뿐,기계/빔으로임의분류하지않음. held_green_line_contract.json및adjacent10/30에보존,설치지도제외/미완료유지.
- 자체alpha<64만RGBA0/고알파불변,원본RGB/alpha스탬프없음. 크기4배/nativeCRC·palette·후보존재기계적확인. 공식QA/HD실재생안함.
- 최종SHA256 e668ea8ee39b9543d62f1d15a234ea364ad27d5823d8c4d656ca56969e4f7950
- installation_map/candidate_atlas/native_atlas가설치입력. 전체2개원본은contract_all2_source/native_atlas_all2_source및proof_all2로보존.
- Claude위험: 단안·몸통/발원근,주황·녹색의실제색영역과새그림밝은광택,원래잘린상단/오른쪽부재경계,다음완전노출장면에서의기하. 이관측은일부클리핑된장면이므로전체기체정상출력확인불가.
- 라이브/DB/코어수정없음,headless/모니터off유지.
