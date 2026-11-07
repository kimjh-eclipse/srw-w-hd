/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/. */

OUTPUT_FORMAT("elf32-littlearm")
OUTPUT_ARCH(arm)
ENTRY(bgm_hook)

PushCommand_impl      = 0x0202EA78;
SND_StartTimer        = 0x0202ECE4;
SND_StopTimer         = 0x0202EC74;
SND_FlushCommand      = 0x0202F1DC;
/*
 * CARDi_ReadRom proper.  0x02035BC0 is CARDi_TryReadCardDma and treats r0
 * as a CARDRomStat pointer; calling it with the DMA number crashes at the
 * first stream fill.
 */
FS_InitFile           = 0x02031BC4;
FS_OpenFileDirect     = 0x02031940;
FS_ReadFile           = 0x020316F0;
FS_SeekFile           = 0x02031684;
FS_CloseFile          = 0x0203182C;
DC_FlushRange         = 0x0202D090;
OS_ReceiveMessage     = 0x0202CDEC;
OS_CreateThread       = 0x0202C788;
OS_WakeupThread       = 0x0202C574;
OS_WakeupThreadDirect = 0x0202C540;
/*
 * 0x0200F11C only converts 20.12 fixed point to an integer and sends
 * SND_COMMAND_MASTER_VOLUME.  The retail BGM replacement path actually
 * stops the currently assigned sequence with slot 0 through 0x0200F2E8.
 */
Game_SetMasterVolumeFx = 0x0200F11C;
Game_UpdateBgmState    = 0x0200F25C;
Game_SelectBgmState    = 0x0200F238;

SECTIONS
{
    . = 0x02001040;
    __payload_start = .;
    .text : {
        KEEP(*(.text.hook))
        *(.text*)
        *(.rodata*)
    }
    .data : {
        *(.data*)
    }
    . = ALIGN(32);
    __payload_file_end = .;
    .bss (NOLOAD) : {
        __bss_start = .;
        *(.bss*)
        *(COMMON)
        __bss_end = .;
    }
    __payload_end = .;
    ASSERT(__payload_end <= 0x02003000, "ARM9 code cave overflow")
}
