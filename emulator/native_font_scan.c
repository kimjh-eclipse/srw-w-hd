/* Exact bitmap font scan accelerator. Compile independently of the emulator core. */
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#ifdef _WIN32
#define API __declspec(dllexport)
#else
#define API
#endif
typedef struct {uint64_t hash;uint16_t rows[16];int count,next;} Pattern;
typedef struct {int height,width,count;uint64_t weights[16];int heads[65536];Pattern *patterns;} Table;
API void *font_table_create(const uint8_t *packed,int count,int height,int width,int stride){
    if(height<1||height>16||width<1||width>16||count<0||stride*8<height*width)return NULL;
    Table *t=(Table*)calloc(1,sizeof(Table));if(!t)return NULL;
    t->height=height;t->width=width;t->count=count;t->weights[height-1]=1;
    for(int y=height-2;y>=0;y--)t->weights[y]=t->weights[y+1]*65599ULL;
    for(int i=0;i<65536;i++)t->heads[i]=-1;
    t->patterns=(Pattern*)calloc(count?count:1,sizeof(Pattern));if(!t->patterns){free(t);return NULL;}
    /* Descending insertion keeps candidate indices ascending within a bucket. */
    for(int i=count-1;i>=0;i--){Pattern *p=&t->patterns[i];const uint8_t *src=packed+(size_t)i*stride;
        for(int y=0;y<height;y++){uint16_t value=0;
            for(int x=0;x<width;x++){int bit=y*width+x;int ink=(src[bit>>3]>>(7-(bit&7)))&1;value=(uint16_t)((value<<1)|ink);p->count+=ink;}
            p->rows[y]=value;p->hash+=(uint64_t)value*t->weights[y];
        }
        int bucket=(int)(p->hash&65535);p->next=t->heads[bucket];t->heads[bucket]=i;
    }return t;
}
API void font_table_free(void *handle){Table *t=(Table*)handle;if(t){free(t->patterns);free(t);}}
API int font_scan(void *handle,const uint8_t *mask,int height,int width,int minimum,int maximum,int *output,int capacity){
    const Table *t=(Table*)handle;if(!t||!mask||!output||height<t->height||width<t->width)return 0;
    int cols=width-t->width+1,lines=height-t->height+1,count=0;
    uint16_t *rows=(uint16_t*)malloc((size_t)height*cols*sizeof(uint16_t));if(!rows)return -2;
    uint32_t keep=t->width==16?65535:((1U<<t->width)-1);
    for(int y=0;y<height;y++){uint32_t value=0;const uint8_t *src=mask+(size_t)y*width;
        for(int x=0;x<width;x++){value=((value<<1)|(src[x]!=0))&keep;if(x>=t->width-1)rows[(size_t)y*cols+x-t->width+1]=(uint16_t)value;}
    }
    uint64_t *hashes=(uint64_t*)calloc(cols,sizeof(uint64_t));if(!hashes){free(rows);return -2;}
    for(int k=0;k<t->height;k++)for(int x=0;x<cols;x++)hashes[x]+=(uint64_t)rows[(size_t)k*cols+x]*t->weights[k];
    for(int y=0;y<lines;y++)for(int x=0;x<cols;x++){
        uint64_t hash=hashes[x];
        for(int i=t->heads[hash&65535];i!=-1;i=t->patterns[i].next){const Pattern *p=&t->patterns[i];
            if(p->hash!=hash||p->count<minimum||p->count>maximum)continue;
            int exact=1;for(int k=0;k<t->height;k++)if(rows[(size_t)(y+k)*cols+x]!=p->rows[k]){exact=0;break;}
            if(!exact)continue;if(count>=capacity){free(hashes);free(rows);return -1;}
            output[count*3]=x;output[count*3+1]=y;output[count*3+2]=i;count++;
        }
        /* Exact unsigned rolling hash: each following row is constant work,
           rather than rebuilding every 8/12/16-row window at every pixel. */
        if(y+1<lines)hashes[x]=(hash-(uint64_t)rows[(size_t)y*cols+x]*t->weights[0])*65599ULL+rows[(size_t)(y+t->height)*cols+x];
    }free(hashes);free(rows);return count;
}
