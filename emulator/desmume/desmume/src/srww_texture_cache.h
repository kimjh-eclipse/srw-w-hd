// GPL-2.0-or-later. Content-validated cache; VRAM and palettes are compared
// every frame, so animation uploads, recolors, bank remaps and state reloads
// invalidate naturally. Never key a texture by its address alone.
struct SRWWTextureIdentity {
    bool valid=false,eight=false;
    unsigned w=0,h=0;
    uint8_t raw[4096],indices[4096];
    uint16_t palette[256];
    uint32_t hash=0,indexHash=0,material=0,usedMask=0,opaque=0;
};
struct SRWWBGTextureIdentity {
    bool valid=false,eight=false;
    uint8_t raw[64];uint16_t palette[256];uint32_t hash=0;
};
static SRWWTextureIdentity SRWWObjTextures[2][128];
static SRWWBGTextureIdentity SRWWBGTextures[2][4][1024];
uint32_t SRWWTextureCacheStats[6]={0};
// Read-only diagnostic snapshot. Counts are elements, not bytes; no cache
// lookup or refresh occurs here. Callers must use this frame's rendered OAM.
unsigned SRWWCopyCachedOBJ(unsigned engine,unsigned sprite,unsigned *row,unsigned rowCount,
                         void *indices,unsigned indexCount,void *palette,unsigned paletteCount) {
    if(engine>=2 || sprite>=128)return 0;
    const auto &cache=SRWWObjTextures[engine][sprite];
    if(!cache.valid || !cache.w || !cache.h || cache.w>64 || cache.h>64)return 0;
    const unsigned pixels=cache.w*cache.h,palettes=cache.eight?256:16;
    if((row && rowCount<8) || (indices && indexCount<pixels) || (palette && paletteCount<palettes))return 0;
    if(row) {
        row[0]=cache.w;row[1]=cache.h;row[2]=cache.hash;row[3]=cache.indexHash;
        row[4]=cache.material;row[5]=cache.usedMask;row[6]=cache.opaque;row[7]=cache.eight?1:0;
    }
    if(indices)memcpy(indices,cache.indices,pixels);
    if(palette)memcpy(palette,cache.palette,palettes*sizeof(uint16_t));
    return 1;
}
static void SRWWResetTextureCache() {
    for(unsigned e=0;e<2;e++) {
        for(unsigned i=0;i<128;i++)SRWWObjTextures[e][i].valid=false;
        for(unsigned l=0;l<4;l++)for(unsigned i=0;i<1024;i++)SRWWBGTextures[e][l][i].valid=false;
    }
    memset(SRWWTextureCacheStats,0,sizeof(SRWWTextureCacheStats));
}
static SRWWTextureIdentity &SRWWCachedOBJ(unsigned engine,unsigned sprite,unsigned base,unsigned stride,unsigned w,unsigned h,bool eight,const u16 *palette) {
    auto &cache=SRWWObjTextures[engine][sprite];const unsigned tileBytes=eight?64:32,paletteBytes=eight?512:32,tilesWide=w/8;
    uint8_t packed[4096];unsigned bytes=0;
    for(unsigned ty=0;ty<h/8;ty++)for(unsigned tx=0;tx<tilesWide;tx++) {
        memcpy(packed+bytes,MMU_gpu_map(base+ty*stride+tx*tileBytes),tileBytes);bytes+=tileBytes;
    }
    SRWWTextureCacheStats[0]++;
    if(cache.valid && cache.w==w && cache.h==h && cache.eight==eight && !memcmp(cache.raw,packed,bytes) && !memcmp(cache.palette,palette,paletteBytes)) {
        SRWWTextureCacheStats[1]++;return cache;
    }
    SRWWTextureCacheStats[2]++;cache.valid=true;cache.w=w;cache.h=h;cache.eight=eight;
    memcpy(cache.raw,packed,bytes);memcpy(cache.palette,palette,paletteBytes);
    uint32_t crc=~0u,indexCrc=~0u,material=2166136261u,usedMask=0,opaque=0;
    for(unsigned y=0;y<h;y++)for(unsigned x=0;x<w;x++) {
        const unsigned at=((y/8)*tilesWide+x/8)*tileBytes+(y&7)*(eight?8:4)+(eight?(x&7):((x&7)/2));
        const unsigned index=eight?packed[at]:((packed[at]>>((x&1)*4))&15);
        cache.indices[y*w+x]=(uint8_t)index;
        if(!eight) {
            material=(material^index)*16777619u;if(index){usedMask|=1u<<index;opaque++;}
            indexCrc=SRWWCrcTable[(indexCrc^index)&255]^(indexCrc>>8);
            indexCrc=SRWWCrcTable[(indexCrc^(index?128:0))&255]^(indexCrc>>8);
        }
        const unsigned color=index?(LE_TO_LOCAL_16(palette[index])|0x8000):0;
        crc=SRWWCrcTable[(crc^(color&255))&255]^(crc>>8);crc=SRWWCrcTable[(crc^(color>>8))&255]^(crc>>8);
    }
    cache.hash=(~crc)^(w<<16)^h;cache.indexHash=(~indexCrc)^(w<<16)^h;cache.material=material;cache.usedMask=usedMask;cache.opaque=opaque;
    return cache;
}
static uint32_t SRWWCachedBG(unsigned engine,unsigned layer,unsigned tile,bool eight,const uint8_t *data,const u16 *palette) {
    auto &cache=SRWWBGTextures[engine][layer][tile];const unsigned bytes=eight?64:32,paletteBytes=eight?512:32;SRWWTextureCacheStats[3]++;
    if(cache.valid && cache.eight==eight && !memcmp(cache.raw,data,bytes) && !memcmp(cache.palette,palette,paletteBytes)) {
        SRWWTextureCacheStats[4]++;return cache.hash;
    }
    SRWWTextureCacheStats[5]++;cache.valid=true;cache.eight=eight;memcpy(cache.raw,data,bytes);memcpy(cache.palette,palette,paletteBytes);
    uint32_t crc=~0u;
    for(unsigned i=0;i<64;i++) {
        const unsigned index=eight?data[i]:((data[i/2]>>((i&1)*4))&15),color=index?(LE_TO_LOCAL_16(palette[index])|0x8000):0;
        crc=SRWWCrcTable[(crc^(color&255))&255]^(crc>>8);crc=SRWWCrcTable[(crc^(color>>8))&255]^(crc>>8);
    }
    return cache.hash=(~crc)^(8<<16)^8;
}
