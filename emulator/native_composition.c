/* Standalone exact DS OBJ/BG visibility masks; no emulator core modifications. */
#include <stdint.h>
#ifdef _WIN32
#define API __declspec(dllexport)
#else
#define API
#endif
API int part_visibility(const uint8_t *layers,const uint8_t *owners,const uint8_t *bgpriorities,const uint16_t *objpriorities,
 int stride,int left,int top,int width,int height,int priority,int kind,int item,uint32_t control,uint8_t *output){
    int count=0;int bit=kind?8+item:12;int alpha_bg=((control&0xc0)==0x40)&&bit>=0&&bit<32&&((control>>bit)&1);
    for(int y=0;y<height;y++)for(int x=0;x<width;x++){
        int offset=(top+y)*stride+left+x;int layer=layers[offset],owner=owners[offset];int visible=layer==5;
        if(layer<4){int bg=bgpriorities[layer];visible=visible||bg>priority||(bg==priority&&(!kind||layer>item));
            if(alpha_bg&&((control>>layer)&1))visible=1;
        }else if(layer==4){int obj=objpriorities[owner];visible=obj>priority||(obj==priority&&owner>=item&&!kind);}
        output[y*width+x]=visible?255:0;count+=visible;
    }
    return count==0?0:(count==width*height?2:1);
}
