    .syntax unified
    .arm
    .text
    .global log_ecd
log_ecd:
    stmdb sp!, {r0-r5, r12, lr}
    ldr r1, =0x02001030
    ldr r2, [r1]
    cmp r2, #448
    bhs done
    ldr r3, =0x02001200
    add r3, r3, r2, lsl #4
    ldmia r0, {r0, r4, r5, r12}
    stmia r3, {r0, r4, r5, r12}
    add r2, r2, #1
    str r2, [r1]
done:
    ldmia sp!, {r0-r5, r12, lr}
    stmdb sp!, {r0-r3}
    ldr pc, =0x0200d41c
    .ltorg
