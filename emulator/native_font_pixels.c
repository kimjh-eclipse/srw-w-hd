/* Exact equivalents of the font recognizer's five NumPy color predicates. */
#include <stdint.h>
#ifdef _WIN32
#define API __declspec(dllexport)
#else
#define API
#endif
API void font_pixel_masks(const uint8_t *restrict rgb,int height,int width,
 uint8_t *restrict bright,uint8_t *restrict white,uint8_t *restrict selected,
 uint8_t *restrict hud_ink,uint8_t *restrict hud_gold){
 int count=height*width,header=(height<32?height:32)*width;
 for(int i=0;i<count;i++){
  int r=rgb[3*i],g=rgb[3*i+1],b=rgb[3*i+2];
  int lo=r<g?r:g;lo=lo<b?lo:b;
  int hi=r>g?r:g;hi=hi>b?hi:b;
  bright[i]=(lo>=80 && hi-lo<8);white[i]=(lo>=232 && hi-lo<8);
  selected[i]=(r<48 && g>=48 && b<48);
  if(i<header){hud_ink[i]=(g>=232 && b>=232 && r>=80);hud_gold[i]=(r>=180 && g>=64 && b<64);}
 }
}
