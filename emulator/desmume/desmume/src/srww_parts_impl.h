// Project-local GPL-2.0-or-later content-addressed HD OBJ renderer bridge.
#include <unordered_map>
#include <vector>
int32_t SRWWRobot_Info[8]={0};
uint8_t SRWWRobot_OAM[1024]={0};
uint8_t SRWWNativeOwner[256*192]={0};
uint8_t SRWWSubOwner[256*192]={0};
uint8_t SRWWSubOAM[1024]={0};
uint32_t SRWWSubParts[128*8]={0};
uint16_t SRWWSubPalettes[128*16]={0};
uint32_t SRWWParts[128*8]={0};
uint16_t SRWWPartPalettes[128*16]={0};
uint32_t SRWWBGParts[4*800*8]={0};
uint8_t SRWWBGMask[4][256*192]={0};
uint32_t SRWWUnknownParts[128*8]={0};
uint8_t SRWWUnknownPixels[128*4096]={0};
uint16_t SRWWUnknownPalettes[128*16]={0};
uint32_t SRWWSubUnknownParts[128*8]={0};
uint8_t SRWWSubUnknownPixels[128*4096]={0};
uint16_t SRWWSubUnknownPalettes[128*16]={0};
static uint32_t SRWWCrcTable[256];
#include "srww_texture_cache.h"
static std::unordered_map<uint32_t,uint32_t> SRWWPartBindings;
static std::unordered_map<uint32_t,uint32_t> SRWWIndexedBindings;
static std::unordered_map<uint64_t,uint32_t> SRWWDynamicBindings;
static bool SRWWAsyncParts=false;
static uint8_t SRWWReadyParts[200000]={0};
void SRWWSetReadyParts(const uint32_t *ids,unsigned count) {
    SRWWAsyncParts=true;memset(SRWWReadyParts,0,sizeof(SRWWReadyParts));
    for(unsigned i=0;i<count;i++)if(ids[i]<200000)SRWWReadyParts[ids[i]]=1;
}
void SRWWAddDynamicPart(uint32_t hash,uint32_t material,uint32_t binding) {
    if(binding && binding<200000)SRWWDynamicBindings[((uint64_t)hash<<32)|material]=binding;
}
void SRWWRegisterIndexedParts(const uint32_t *hashes,const uint32_t *bindings,unsigned count) {
    SRWWIndexedBindings.clear();
    for(unsigned i=0;i<count;i++)if(!SRWWIndexedBindings.count(hashes[i]))SRWWIndexedBindings[hashes[i]]=bindings[i];
}
uint32_t SRWWTargetEngine() { return GPU->GetEngineMain()->GetTargetDisplayByID()==NDSDisplayID_Main?0:1; }
void SRWWRegisterParts(const uint32_t *hashes,unsigned count) {
    SRWWAsyncParts=false;SRWWResetTextureCache();
    SRWWDynamicBindings.clear();
    SRWWPartBindings.clear();
    for(unsigned i=0;i<256;i++) {uint32_t c=i;for(unsigned j=0;j<8;j++)c=(c>>1)^((c&1)?0xedb88320u:0);SRWWCrcTable[i]=c;}
    for(unsigned i=0;i<count;i++)if(hashes[i])SRWWPartBindings[hashes[i]]=i+1;
}
bool SRWWHD_ShouldSkipRobot(uint32_t engine,uint32_t sprite,const void *oam) {
    const bool secondary=engine!=SRWWTargetEngine();
    uint32_t *parts=secondary?SRWWSubParts:SRWWParts;
    uint16_t *palettes=secondary?SRWWSubPalettes:SRWWPartPalettes;
    static uint32_t checked[2]={~0u,~0u};
    if(checked[engine]!=SRWWHD_Frame) {
        checked[engine]=SRWWHD_Frame;memset(parts,0,128*8*sizeof(uint32_t));
        if(!secondary)memset(SRWWRobot_Info,0,sizeof(SRWWRobot_Info));
        memcpy(secondary?SRWWSubOAM:SRWWRobot_OAM,oam,1024);
        if(!SRWWHD_Enabled)return false;
        const u16 *raw=(const u16*)oam;
        const uint8_t *regs=MMU.ARM9_REG+(engine?0x1000:0);
        const uint32_t disp=LE_TO_LOCAL_32(*(u32*)regs);
        const bool oneD=(disp&16)!=0;
        const unsigned boundary=oneD?5+((disp>>20)&3):5;
        static const int widths[3][4]={{8,16,32,64},{16,32,32,64},{8,8,16,32}};
        static const int heights[3][4]={{8,16,32,64},{8,8,16,32},{16,32,32,64}};
        for(unsigned i=0;i<128;i++) {
            const unsigned a=LE_TO_LOCAL_16(raw[i*4]),b=LE_TO_LOCAL_16(raw[i*4+1]),c=LE_TO_LOCAL_16(raw[i*4+2]);
            if((!(a&256)&&(a&512)) || (a>>14)==3 || ((a>>10)&3)>=2)continue;
            const unsigned shape=a>>14,size=b>>14,w=widths[shape][size],h=heights[shape][size];
            int screenX=b&511,screenY=a&255;
            if(screenX>=256)screenX-=512;
            if(screenY>=192)screenY-=256;
            const unsigned extent=((a&256)&&(a&512))?2:1;
            if(screenX>=256 || screenY>=192 || screenX+(int)(w*extent)<=0 || screenY+(int)(h*extent)<=0)continue;
            const bool eight=(a&8192)!=0;
            if(eight && (disp&0x80000000u))continue; // extended OBJ palettes stay native
            const unsigned base=(engine?0x06600000u:0x06400000u)+((c&1023)<<boundary),tileBytes=eight?64:32;
            const unsigned stride=oneD?(w/8)*tileBytes:1024;
            const u16 *palette=(const u16*)(MMU.ARM9_VMEM+(engine?1536:512)+(eight?0:(c>>12)*32));
            const auto &texture=SRWWCachedOBJ(engine,i,base,stride,w,h,eight,palette);
            const uint32_t hash=texture.hash,indexHash=texture.indexHash,material=texture.material,usedMask=texture.usedMask,opaque=texture.opaque;
            const uint8_t *nativeIndices=texture.indices;
            const auto found=SRWWPartBindings.find(hash);
            uint32_t binding=found==SRWWPartBindings.end()?0:found->second;
            if(!binding && !eight) {
                const auto indexed=SRWWIndexedBindings.find(indexHash);
                if(indexed!=SRWWIndexedBindings.end())binding=indexed->second;
            }
            if(!binding && !eight) {
                const auto dynamic=SRWWDynamicBindings.find(((uint64_t)indexHash<<32)|material);
                if(dynamic!=SRWWDynamicBindings.end())binding=dynamic->second;
            }
            if(!binding) {
                unsigned colors=0;for(uint32_t mask=usedMask;mask;mask&=mask-1)colors++;
                if(!eight && w*h>=64 && opaque>=24 && colors>=3 && screenY<(secondary?192:120)) {
                    uint32_t *unknown=(secondary?SRWWSubUnknownParts:SRWWUnknownParts)+i*8;
                    unknown[0]=indexHash;unknown[1]=w;unknown[2]=h;unknown[3]=a;unknown[4]=b;unknown[5]=c;unknown[6]=hash;unknown[7]=material;
                    memcpy((secondary?SRWWSubUnknownPixels:SRWWUnknownPixels)+i*4096,nativeIndices,w*h);
                    for(unsigned k=0;k<16;k++)(secondary?SRWWSubUnknownPalettes:SRWWUnknownPalettes)[i*16+k]=LE_TO_LOCAL_16(palette[k]);
                }
                continue;
            }
            uint32_t *part=parts+i*8;
            part[0]=binding;part[1]=a;part[2]=b;part[3]=c;part[4]=hash;
            for(unsigned k=0;k<16;k++)palettes[i*16+k]=LE_TO_LOCAL_16(palette[k]);
            part[5]=LE_TO_LOCAL_16(*(u16*)(regs+0x6c));
            part[6]=LE_TO_LOCAL_16(*(u16*)(regs+0x52));
            part[7]=LE_TO_LOCAL_16(*(u16*)(regs+0x50))|((SRWWAsyncParts && !SRWWReadyParts[binding])?0x80000000u:0);
            if(!secondary)SRWWRobot_Info[0]++;
        }
    }
    // Keep a native fallback underneath asynchronously prepared HD textures.
    // The frontend can display a new animation immediately while its art warms.
    const unsigned binding=parts[sprite*8];
    return binding && (!SRWWAsyncParts || SRWWReadyParts[binding]);
}

void SRWWBeginPartsFrame() {
    memset(SRWWSubParts,0,sizeof(SRWWSubParts));
    memset(SRWWUnknownParts,0,sizeof(SRWWUnknownParts));
    memset(SRWWSubUnknownParts,0,sizeof(SRWWSubUnknownParts));
    memset(SRWWParts,0,sizeof(SRWWParts));memset(SRWWBGParts,0,sizeof(SRWWBGParts));memset(SRWWBGMask,0,sizeof(SRWWBGMask));
}

void SRWWPrepareBG(uint32_t engine,uint32_t layer,uint32_t map,uint32_t tiles,uint32_t scrollX,uint32_t scrollY,uint32_t w,uint32_t h,uint32_t eight,uint32_t priority) {
    if(engine!=SRWWTargetEngine() || layer>3 || !SRWWHD_Enabled || SRWWPartBindings.empty())return;
    static uint32_t checked[4]={~0u,~0u,~0u,~0u};
    if(checked[layer]==SRWWHD_Frame)return;checked[layer]=SRWWHD_Frame;
    unsigned count=0;
    for(int sy=-(int)(scrollY&7);sy<192;sy+=8)for(int sx=-(int)(scrollX&7);sx<256;sx+=8) {
        if(layer==0 && sy>=120)continue; // dialogue/font/portraits have their own high-resolution path
        const unsigned tx=((sx+scrollX)&(w-1))/8,ty=((sy+scrollY)&(h-1))/8;
        const unsigned block=(ty/32)*(w/256)+tx/32,entryIndex=block*1024+(ty&31)*32+(tx&31);
        const unsigned entry=LE_TO_LOCAL_16(*(u16*)MMU_gpu_map(map+entryIndex*2));
        const unsigned tile=entry&1023;
        const u16 *pal=(const u16*)(MMU.ARM9_VMEM+(engine?1024:0)+(eight?0:(entry>>12)*32));
        const uint8_t *data=(const uint8_t*)MMU_gpu_map(tiles+tile*(eight?64:32));
        const uint32_t hash=SRWWCachedBG(engine,layer,tile,eight!=0,data,pal);
        const auto found=SRWWPartBindings.find(hash);
        if(found==SRWWPartBindings.end())continue;
        if(count>=800)continue;
        uint32_t *p=SRWWBGParts+(layer*800+count++)*8;
        p[0]=found->second;p[1]=entry&0xc00;p[2]=sx;p[3]=sy;p[4]=layer;p[5]=priority;
        const uint8_t *regs=MMU.ARM9_REG+(engine?0x1000:0);
        p[6]=LE_TO_LOCAL_16(*(u16*)(regs+0x6c));p[7]=LE_TO_LOCAL_16(*(u16*)(regs+0x50))|((SRWWAsyncParts && !SRWWReadyParts[found->second])?0x80000000u:0);
        if(!SRWWAsyncParts || SRWWReadyParts[found->second])
            for(int y=std::max(sy,0);y<std::min(sy+8,192);y++)for(int x=std::max(sx,0);x<std::min(sx+8,256);x++)SRWWBGMask[layer][y*256+x]=1;
    }
}
