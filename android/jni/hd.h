/* HD parts composition (hd.c) */
#ifndef SRWW_HD_H
#define SRWW_HD_H
#include <stdbool.h>
#include <stdint.h>
int hd_init(void *core, const char *dir);   /* after retro_load_game; 0 = no pack / no HD */
void hd_gl_init(void);                        /* on every new GL surface */
void hd_set_enabled(int on);
int hd_active(void);
void hd_before_run(void);                     /* GL thread, before retro_run */
void hd_after_run(const uint32_t *rgba);       /* after the run whose frame is shown (RGBA 256x384) */
int hd_draw(int top_screen);                  /* into the bound 1024x768 target; 1 = redraw native dialogue band 128-191 on top */
void hd_draw_overlay(int top_screen);          /* portraits: above everything on that screen */
void hd_rumble_frame(void);                    /* after every emulated frame */
int hd_take_rumble(float *out);                /* {low, high, beam}; ms, 0 stop, -1 none */
#include <jni.h>
void hd_set_jni(JNIEnv *e);                    /* every frame: env for the Java glyph renderer */
void hd_text_frame(uint32_t *rgba, uint32_t *argb); /* recognise and erase native lettering (both screens) */
void hd_draw_text(int top_screen);              /* HD lettering, last */
#endif
