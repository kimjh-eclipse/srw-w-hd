# 자체 RGBA 출처

imagegen3panel각cell의자체생성RGBA만사용. 원본alpha/RGB전사·다른팔레트alpha공유·threshold/morph삭제없음. A>=16은자체그림bbox위치측정용이며출력alpha자르기아님. flat3material은자체생성내부opaque RGBAcrop(253~254그대로)을사용해1texel입자도보존. 위치는49개원본component bboxgeometry만사용했습니다.
