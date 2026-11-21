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
  if(i<header){
   hud_ink[i]=(g>=232 && b>=232 && r>=80) ||
              (r>=128 && g<64 && b<64) || (r>=128 && g>=128 && b<64) ||
              /* warning digits: the cyan face/bevel shades turned red (205,72,74 / 230,157,156 /
                 255,230,230) or yellow (r==g); all three shades are ink like the cyan ones */
              (r>=200 && g>=64 && g-b<=8 && b-g<=8 && r-g>=24) || (r>=200 && r-g<=8 && g-r<=8 && r-b>=24);
   hud_gold[i]=(r>=180 && g>=64 && b<64);
  }
 }
}
