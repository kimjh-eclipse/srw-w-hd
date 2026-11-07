// Project-local GPL-2.0-or-later HD cut-in bridge.
#ifndef SRWW_HD_H
#define SRWW_HD_H
#include <stdint.h>
extern uint32_t SRWWHD_Enabled;
extern uint32_t SRWWHD_Frame;
extern uint32_t SRWWHD_Info[12];
extern int32_t SRWWRobot_Info[8];
extern uint8_t SRWWRobot_OAM[1024];
extern uint8_t SRWWNativeOwner[256*192];
extern uint32_t SRWWParts[128*8];
extern uint16_t SRWWPartPalettes[128*16];
extern uint32_t SRWWBGParts[4*800*8];
extern uint8_t SRWWBGMask[4][256*192];
extern uint32_t SRWWUnknownParts[128*8];
extern uint8_t SRWWUnknownPixels[128*4096];
extern uint16_t SRWWUnknownPalettes[128*16];
void SRWWAddDynamicPart(uint32_t hash,uint32_t material,uint32_t binding);
void SRWWRegisterParts(const uint32_t *hashes,unsigned count);
void SRWWRegisterIndexedParts(const uint32_t *hashes,const uint32_t *bindings,unsigned count);
void SRWWRegisterCutins(const uint32_t *rows,unsigned count);
void SRWWSetReadyParts(const uint32_t *ids,unsigned count);
void SRWWBeginPartsFrame();
uint32_t SRWWTargetEngine();
void SRWWPrepareBG(uint32_t engine,uint32_t layer,uint32_t map,uint32_t tiles,uint32_t x,uint32_t y,uint32_t w,uint32_t h,uint32_t eight,uint32_t priority);
bool SRWWHD_ShouldSkipRobot(uint32_t engine,uint32_t sprite,const void *oam);
bool SRWWHD_ShouldSkip(uint32_t engine,uint32_t layer,uint32_t map,uint32_t tiles,uint32_t x,uint32_t y,uint32_t priority,uint32_t master);
#endif

extern uint32_t SRWWTextureCacheStats[6];
