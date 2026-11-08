/* MPL-2.0: adapted from reference_bgm/src/hook.S. */
    .syntax unified
    .arm
    .section .text.hook, "ax", %progbits
    .global bgm_hook
    .type bgm_hook, %function
    .extern voice_glyph_probe
bgm_hook:
    stmdb sp!, {r0-r3, r12, lr}
    bl voice_glyph_probe
    ldmia sp!, {r0-r3, r12, lr}
    @ Replay the main-loop update prologue; preserve its literal load value.
    stmdb sp!, {r3-r5, lr}
    ldr r0, =0x020B7200
    ldr pc, =0x0200EE58
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
