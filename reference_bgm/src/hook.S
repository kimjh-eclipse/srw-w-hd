    /* This Source Code Form is subject to the terms of the Mozilla Public
     * License, v. 2.0. If a copy of the MPL was not distributed with this
     * file, You can obtain one at https://mozilla.org/MPL/2.0/. */

    .syntax unified
    .arm
    .section .text.hook, "ax", %progbits
    .global bgm_hook
    .type bgm_hook, %function

    .extern stream_probe
    .extern stream_after_original
    .extern stream_stop_from_game
    .extern stream_set_volume_from_game

bgm_hook:
    stmdb   sp!, {r0-r3, r12, lr}
    bl      stream_probe
    cmp     r0, #1
    ldmia   sp!, {r0-r3, r12, lr}
    beq     1f

    @ Re-run the two ARM instructions replaced at 0x02013110.
    stmdb   sp!, {r4, lr}
    mov     r4, r0
    ldr     pc, =0x02013118

1:
    @
    @ Do not enter the retail function body for a replacement.  Its final
    @ call starts an asynchronous SSEQ card load; cancelling that load and
    @ issuing CARDi_ReadRom later deadlocks melonDS.  The C replacement calls
    @ only the verified non-loader state helpers, then starts raw PCM.
    stmdb   sp!, {r0-r3, r12, lr}
    bl      stream_after_original
    ldmia   sp!, {r0-r3, r12, lr}
    mov     r0, #0
    bx      lr

    .ltorg
    .size bgm_hook, .-bgm_hook

    .global seq_stop_hook
    .type seq_stop_hook, %function
seq_stop_hook:
    stmdb   sp!, {r0-r3, r12, lr}
    cmp     r0, #0
    bleq    stream_stop_from_game
    ldmia   sp!, {r0-r3, r12, lr}
    b       seq_stop_original
    .size seq_stop_hook, .-seq_stop_hook

    .global seq_stop_original
    .type seq_stop_original, %function
seq_stop_original:
    @ Re-run the two instructions replaced at 0x0200F2E8, then continue.
    stmdb   sp!, {r4, lr}
    ldr     r1, =0x020B7200
    ldr     pc, =0x0200F2F0
    .ltorg
    .size seq_stop_original, .-seq_stop_original

    .global seq_volume_hook
    .type seq_volume_hook, %function
seq_volume_hook:
    stmdb   sp!, {r0-r3, r12, lr}
    cmp     r0, #0
    bleq    stream_set_volume_from_game
    ldmia   sp!, {r0-r3, r12, lr}
    b       seq_volume_original
    .size seq_volume_hook, .-seq_volume_hook

    .global seq_volume_original
    .type seq_volume_original, %function
seq_volume_original:
    @ Re-run the two instructions replaced at 0x0200F33C, then continue.
    stmdb   sp!, {r3, lr}
    ldr     r2, =0x020B7200
    ldr     pc, =0x0200F344
    .ltorg
    .size seq_volume_original, .-seq_volume_original
