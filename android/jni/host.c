/* SRW W HD — Android host (first version: original screens, no HD composition).
 * Loads the patched DeSmuME libretro core (libretro.so, built by scripts/build/build_android_arm64.ps1),
 * runs one frame per GL draw, draws the two DS screens and the on-screen buttons with GLES2,
 * hands audio to Java (AudioTrack) through a ring buffer, and takes buttons/touch from Java.
 */
#include <jni.h>
#include <dlfcn.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>
#include <time.h>
#include <GLES2/gl2.h>
#include <android/log.h>
#include "libretro.h"
#include "hd.h"

#define LOG(...) __android_log_print(ANDROID_LOG_INFO, "srwwhd", __VA_ARGS__)

/* core entry points */
static void *core;
static void (*p_init)(void), (*p_deinit)(void), (*p_run)(void), (*p_reset)(void);
static bool (*p_load_game)(const struct retro_game_info *);
static void (*p_unload_game)(void);
static void (*p_set_env)(retro_environment_t), (*p_set_video)(retro_video_refresh_t), (*p_set_audio)(retro_audio_sample_t),
            (*p_set_batch)(retro_audio_sample_batch_t), (*p_set_poll)(retro_input_poll_t), (*p_set_state)(retro_input_state_t);
static size_t (*p_ser_size)(void);
static bool (*p_serialize)(void *, size_t), (*p_unserialize)(const void *, size_t);
static void (*p_av_info)(struct retro_system_av_info *);

static char dir[1024];
static int pixel_format = RETRO_PIXEL_FORMAT_0RGB1555;
static unsigned fb_w = 256, fb_h = 384;
static uint32_t frame[256 * 768];          /* RGBA, room for layouts up to 256x768 */
static uint32_t argb[256 * 384];         /* xBRZ input (0xAARRGGBB) */
static uint32_t hd_argb[1024 * 1536], hd_rgba[1024 * 1536];
static void (*xbrz4)(const uint32_t *, uint32_t *, int, int);
static volatile int buttons = 0;           /* bit = RETRO_DEVICE_ID_JOYPAD_* */
static volatile int touching = 0, touch_x = 0, touch_y = 0;
static int loaded = 0;

/* audio ring buffer (stereo int16) */
#define RING (44100 * 2 / 2)
static int16_t ring[RING];
static volatile unsigned rhead, rtail;
static pthread_mutex_t rlock = PTHREAD_MUTEX_INITIALIZER;

static void push_audio(const int16_t *s, size_t frames) {
    pthread_mutex_lock(&rlock);
    for (size_t i = 0; i < frames * 2; i++) {
        unsigned n = (rhead + 1) % RING;
        if (n == rtail) break;                 /* full: drop */
        ring[rhead] = s[i]; rhead = n;
    }
    pthread_mutex_unlock(&rlock);
}

struct var { const char *key, *value; };
static struct var vars[] = {
    {"desmume_cpu_mode", "interpreter"},
    {"desmume_screens_layout", "top/bottom"},
    {"desmume_opengl_mode", "disabled"},
    {"desmume_frameskip", "0"},
    {"desmume_pointer_type", "touch"},
    {NULL, NULL}};

#include <stdarg.h>
static void core_log(enum retro_log_level level, const char *fmt, ...) {
    va_list ap; va_start(ap, fmt); __android_log_vprint(ANDROID_LOG_INFO, "srwwcore", fmt, ap); va_end(ap);
}

static bool env(unsigned cmd, void *data) {
    switch (cmd) {
    case RETRO_ENVIRONMENT_GET_SYSTEM_DIRECTORY:
    case RETRO_ENVIRONMENT_GET_SAVE_DIRECTORY:
    case RETRO_ENVIRONMENT_GET_CORE_ASSETS_DIRECTORY:
        *(const char **)data = dir; return true;
    case RETRO_ENVIRONMENT_SET_PIXEL_FORMAT:
        pixel_format = *(const int *)data; return true;
    case RETRO_ENVIRONMENT_GET_VARIABLE: {
        struct retro_variable *v = data;
        for (int i = 0; vars[i].key; i++)
            if (!strcmp(vars[i].key, v->key)) { v->value = vars[i].value; return true; }
        v->value = NULL; return false;
    }
    case RETRO_ENVIRONMENT_GET_VARIABLE_UPDATE:
        *(bool *)data = false; return true;
    case RETRO_ENVIRONMENT_GET_LOG_INTERFACE:
        ((struct retro_log_callback *)data)->log = core_log; return true;
    case RETRO_ENVIRONMENT_GET_INPUT_BITMASKS:
        return false;
    case RETRO_ENVIRONMENT_GET_CAN_DUPE:
        *(bool *)data = true; return true;
    case RETRO_ENVIRONMENT_SET_VARIABLES:
    case RETRO_ENVIRONMENT_SET_INPUT_DESCRIPTORS:
    case RETRO_ENVIRONMENT_SET_SUPPORT_NO_GAME:
        return true;
    default:
        return false;
    }
}

static void video(const void *data, unsigned w, unsigned h, size_t pitch) {
    if (!data || data == RETRO_HW_FRAME_BUFFER_VALID) return;
    if (w > 256 || h > 768) return;
    fb_w = w; fb_h = h;
    for (unsigned y = 0; y < h; y++) {
        const uint8_t *row = (const uint8_t *)data + y * pitch;
        uint32_t *out = frame + y * w;
        for (unsigned x = 0; x < w; x++) {
            uint8_t r, g, b;
            if (pixel_format == RETRO_PIXEL_FORMAT_XRGB8888) {
                uint32_t p = ((const uint32_t *)row)[x]; r = p >> 16; g = p >> 8; b = p;
            } else if (pixel_format == RETRO_PIXEL_FORMAT_RGB565) {
                uint16_t p = ((const uint16_t *)row)[x];
                r = ((p >> 11) & 31) * 255 / 31; g = ((p >> 5) & 63) * 255 / 63; b = (p & 31) * 255 / 31;
            } else {
                uint16_t p = ((const uint16_t *)row)[x];
                r = ((p >> 10) & 31) * 255 / 31; g = ((p >> 5) & 31) * 255 / 31; b = (p & 31) * 255 / 31;
            }
            out[x] = 0xff000000u | (b << 16) | (g << 8) | r;
            if (h == 384 && w == 256) argb[y * 256 + x] = 0xff000000u | (r << 16) | (g << 8) | b;
        }
    }
}
static void sample(int16_t l, int16_t r) { int16_t s[2] = {l, r}; push_audio(s, 1); }
static size_t batch(const int16_t *s, size_t frames) { push_audio(s, frames); return frames; }
static void poll(void) {}
static int16_t state(unsigned port, unsigned device, unsigned index, unsigned id) {
    if (port) return 0;
    if (device == RETRO_DEVICE_JOYPAD) return (buttons >> id) & 1;
    if (device == RETRO_DEVICE_POINTER) {
        if (id == RETRO_DEVICE_ID_POINTER_X) return touch_x;
        if (id == RETRO_DEVICE_ID_POINTER_Y) return touch_y;
        if (id == RETRO_DEVICE_ID_POINTER_PRESSED) return touching;
    }
    return 0;
}

#define SYM(p, n) if (!(*(void **)&p = dlsym(core, n))) { LOG("missing %s", n); return JNI_FALSE; }

JNIEXPORT jboolean JNICALL Java_kr_srww_hd_Native_init(JNIEnv *e, jclass c, jstring jrom, jstring jdir, jstring jhd) {
    if (loaded) return JNI_TRUE;
    LOG("init start");
    const char *rom = (*e)->GetStringUTFChars(e, jrom, 0), *d = (*e)->GetStringUTFChars(e, jdir, 0);
    snprintf(dir, sizeof dir, "%s", d);
    /* palette groups stay HD even when a piece of the group has no HD art (user decision 11/21):
     * the core otherwise turns the whole face/unit native on such frames, which blinks. */
    setenv("SRWW_UNIT_FALLBACK_PERCENT", "0", 1);
    core = dlopen("libretro.so", RTLD_NOW);
    if (!core) { LOG("dlopen: %s", dlerror()); return JNI_FALSE; }
    SYM(p_init, "retro_init") SYM(p_deinit, "retro_deinit") SYM(p_run, "retro_run") SYM(p_reset, "retro_reset")
    SYM(p_load_game, "retro_load_game") SYM(p_unload_game, "retro_unload_game")
    SYM(p_set_env, "retro_set_environment") SYM(p_set_video, "retro_set_video_refresh") SYM(p_set_audio, "retro_set_audio_sample")
    SYM(p_set_batch, "retro_set_audio_sample_batch") SYM(p_set_poll, "retro_set_input_poll") SYM(p_set_state, "retro_set_input_state")
    SYM(p_ser_size, "retro_serialize_size") SYM(p_serialize, "retro_serialize") SYM(p_unserialize, "retro_unserialize")
    SYM(p_av_info, "retro_get_system_av_info")
    p_set_env(env); p_set_video(video); p_set_audio(sample); p_set_batch(batch); p_set_poll(poll); p_set_state(state);
    LOG("callbacks set, retro_init");
    p_init();
    LOG("retro_init done, load_game");
    struct retro_game_info g = {rom, NULL, 0, NULL};
    loaded = p_load_game(&g);
    LOG("load %s -> %d", rom, loaded);
    if (loaded) { const char *h = (*e)->GetStringUTFChars(e, jhd, 0); hd_init(core, h); (*e)->ReleaseStringUTFChars(e, jhd, h); }
    (*e)->ReleaseStringUTFChars(e, jrom, rom); (*e)->ReleaseStringUTFChars(e, jdir, d);
    return loaded ? JNI_TRUE : JNI_FALSE;
}

JNIEXPORT void JNICALL Java_kr_srww_hd_Native_input(JNIEnv *e, jclass c, jint b, jint t, jint x, jint y) {
    buttons = b; touching = t; touch_x = x; touch_y = y;
}

JNIEXPORT jint JNICALL Java_kr_srww_hd_Native_audio(JNIEnv *e, jclass c, jshortArray out) {
    jsize n = (*e)->GetArrayLength(e, out);
    jshort *o = (*e)->GetShortArrayElements(e, out, 0);
    int k = 0;
    pthread_mutex_lock(&rlock);
    while (k < n && rtail != rhead) { o[k++] = ring[rtail]; rtail = (rtail + 1) % RING; }
    pthread_mutex_unlock(&rlock);
    (*e)->ReleaseShortArrayElements(e, out, o, 0);
    return k;
}

static int file_write(const char *path, const void *p, size_t n) {
    FILE *f = fopen(path, "wb"); if (!f) return 0;
    size_t w = fwrite(p, 1, n, f); fclose(f); return w == n;
}

JNIEXPORT jboolean JNICALL Java_kr_srww_hd_Native_saveState(JNIEnv *e, jclass c, jstring jpath) {
    if (!loaded) return JNI_FALSE;
    const char *path = (*e)->GetStringUTFChars(e, jpath, 0);
    size_t n = p_ser_size(); void *buf = malloc(n); int ok = 0;
    if (buf && p_serialize(buf, n)) ok = file_write(path, buf, n);
    free(buf); (*e)->ReleaseStringUTFChars(e, jpath, path);
    return ok ? JNI_TRUE : JNI_FALSE;
}

JNIEXPORT jboolean JNICALL Java_kr_srww_hd_Native_loadState(JNIEnv *e, jclass c, jstring jpath) {
    if (!loaded) return JNI_FALSE;
    const char *path = (*e)->GetStringUTFChars(e, jpath, 0);
    FILE *f = fopen(path, "rb"); int ok = 0;
    if (f) {
        fseek(f, 0, SEEK_END); long n = ftell(f); fseek(f, 0, SEEK_SET);
        void *buf = malloc(n);
        if (buf && fread(buf, 1, n, f) == (size_t)n) ok = p_unserialize(buf, n);
        free(buf); fclose(f);
    }
    (*e)->ReleaseStringUTFChars(e, jpath, path);
    return ok ? JNI_TRUE : JNI_FALSE;
}

/* ---------- xBRZ 4x (top and bottom screen in parallel) ---------- */
struct half { int k; };
static void *xbrz_half(void *arg) {
    int k = ((struct half *)arg)->k;           /* 0 = top 256x192, 1 = bottom */
    xbrz4(argb + k * 256 * 192, hd_argb + k * 1024 * 768, 256, 192);
    uint32_t *src = hd_argb + k * 1024 * 768, *dst = hd_rgba + k * 1024 * 768;
    for (int i = 0; i < 1024 * 768; i++) { uint32_t p = src[i]; dst[i] = 0xff000000u | ((p & 0xff) << 16) | (p & 0xff00) | ((p >> 16) & 0xff); }
    return NULL;
}
static int xbrz_ready(void) {
    static int tried;
    if (!tried) { tried = 1; void *h = dlopen("libxbrz_compare.so", RTLD_NOW); if (h) *(void **)&xbrz4 = dlsym(h, "srww_xbrz4_argb"); LOG("xbrz %s", xbrz4 ? "ready" : "missing"); }
    return xbrz4 != NULL;
}

/* ---------- GLES2 drawing ---------- */
static GLuint prog, solid, tex, fbo[2], fbtex[2];
static GLint a_pos, a_uv, u_tex, s_pos, s_col;
static int vw, vh;

static GLuint shader(GLenum t, const char *src) {
    GLuint s = glCreateShader(t); glShaderSource(s, 1, &src, 0); glCompileShader(s); return s;
}
static GLuint program(const char *vs, const char *fs) {
    GLuint p = glCreateProgram();
    glAttachShader(p, shader(GL_VERTEX_SHADER, vs)); glAttachShader(p, shader(GL_FRAGMENT_SHADER, fs));
    glLinkProgram(p); return p;
}

static void quad_px(float x, float y, float w, float h, float *out) { /* pixel rect -> clip coords, 4 verts strip */
    float l = x / vw * 2 - 1, r = (x + w) / vw * 2 - 1, t = 1 - y / vh * 2, b = 1 - (y + h) / vh * 2;
    float q[8] = {l, b, r, b, l, t, r, t}; memcpy(out, q, sizeof q);
}

JNIEXPORT void JNICALL Java_kr_srww_hd_Native_surface(JNIEnv *e, jclass c, jint w, jint h) {
    vw = w; vh = h;
    prog = program("attribute vec2 p;attribute vec2 t;varying vec2 v;void main(){v=t;gl_Position=vec4(p,0.,1.);}",
                   "precision mediump float;varying vec2 v;uniform sampler2D s;void main(){gl_FragColor=texture2D(s,v);}");
    a_pos = glGetAttribLocation(prog, "p"); a_uv = glGetAttribLocation(prog, "t"); u_tex = glGetUniformLocation(prog, "s");
    solid = program("attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}",
                    "precision mediump float;uniform vec4 c;void main(){gl_FragColor=c;}");
    s_pos = glGetAttribLocation(solid, "p"); s_col = glGetUniformLocation(solid, "c");
    glGenTextures(1, &tex); glBindTexture(GL_TEXTURE_2D, tex);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST); glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE); glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
    glViewport(0, 0, w, h);
    hd_gl_init();
    glGenTextures(2, fbtex); glGenFramebuffers(2, fbo);
    for (int k = 0; k < 2; k++) {
        glBindTexture(GL_TEXTURE_2D, fbtex[k]);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE); glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 1024, 768, 0, GL_RGBA, GL_UNSIGNED_BYTE, NULL);
        glBindFramebuffer(GL_FRAMEBUFFER, fbo[k]);
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, fbtex[k], 0);
    }
    glBindFramebuffer(GL_FRAMEBUFFER, 0);
}

JNIEXPORT void JNICALL Java_kr_srww_hd_Native_setHd(JNIEnv *e, jclass c, jboolean on) { hd_set_enabled(on); }
JNIEXPORT jboolean JNICALL Java_kr_srww_hd_Native_hdReady(JNIEnv *e, jclass c) { return hd_active() ? JNI_TRUE : JNI_FALSE; }

static void draw_tex(float x, float y, float w, float h, float u0, float v0, float u1, float v1) {
    float v[8], uv[8] = {u0, v1, u1, v1, u0, v0, u1, v0};
    quad_px(x, y, w, h, v);
    glVertexAttribPointer(a_pos, 2, GL_FLOAT, 0, 0, v); glEnableVertexAttribArray(a_pos);
    glVertexAttribPointer(a_uv, 2, GL_FLOAT, 0, 0, uv); glEnableVertexAttribArray(a_uv);
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);
}


/* top, bottom: x,y,w,h of each DS screen on the surface (bottom w=0 hides it); linear: smooth filter */
JNIEXPORT void JNICALL Java_kr_srww_hd_Native_frame(JNIEnv *e, jclass c, jint run, jfloatArray jtop, jfloatArray jbottom, jint linear) {
    /* run = number of emulated frames to run now (paced by Java to 59.83 fps, more when fast-forwarding) */
    static struct timespec t0; static int counted; static double busy;
    hd_set_jni(e);
    if (loaded && run > 0) hd_before_run();
    for (int i = 0; loaded && i < run; i++) {
        struct timespec a, b; clock_gettime(CLOCK_MONOTONIC, &a); p_run(); clock_gettime(CLOCK_MONOTONIC, &b);
        busy += (b.tv_sec - a.tv_sec) + (b.tv_nsec - a.tv_nsec) / 1e9; counted++;
        hd_rumble_frame();
        if (i == run - 1) { hd_after_run(frame); if (fb_w == 256 && fb_h == 384) hd_text_frame(frame, argb); }
    }
    if (counted >= 300) {
        struct timespec n; clock_gettime(CLOCK_MONOTONIC, &n);
        double el = (n.tv_sec - t0.tv_sec) + (n.tv_nsec - t0.tv_nsec) / 1e9;
        if (t0.tv_sec) LOG("emulated %.1f fps, core %.2f ms/frame", counted / el, busy * 1000 / counted);
        t0 = n; counted = 0; busy = 0;
    }
    glClearColor(0, 0, 0, 1); glClear(GL_COLOR_BUFFER_BIT);
    glUseProgram(prog); glActiveTexture(GL_TEXTURE0); glBindTexture(GL_TEXTURE_2D, tex);
    /* linear: 0 sharp pixels, 1 smooth (bilinear), 2 xBRZ 4x then smooth */
    int use_xbrz = linear == 2 && fb_w == 256 && fb_h == 384 && xbrz_ready();
    GLint f = linear ? GL_LINEAR : GL_NEAREST;
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, f); glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, f);
    glPixelStorei(GL_UNPACK_ALIGNMENT, 4);
    if (use_xbrz) {
        static struct timespec x0; static int xn; static double xs;
        struct timespec a, b; clock_gettime(CLOCK_MONOTONIC, &a);
        if (run > 0 || !xn) {                       /* only when a new frame was emulated */
            pthread_t t[2]; struct half hs[2] = {{0}, {1}};
            for (int k = 0; k < 2; k++) pthread_create(&t[k], NULL, xbrz_half, &hs[k]);
            for (int k = 0; k < 2; k++) pthread_join(t[k], NULL);
        }
        clock_gettime(CLOCK_MONOTONIC, &b); xs += (b.tv_sec - a.tv_sec) + (b.tv_nsec - a.tv_nsec) / 1e9;
        if (++xn % 300 == 0) LOG("xbrz %.2f ms/frame", xs * 1000 / 300), xs = 0;
        (void)x0;
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 1024, 1536, 0, GL_RGBA, GL_UNSIGNED_BYTE, hd_rgba);
    } else
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, fb_w, fb_h, 0, GL_RGBA, GL_UNSIGNED_BYTE, frame);
    glUniform1i(u_tex, 0);
    if (hd_active() && fb_w == 256 && fb_h == 384) {
        /* each DS screen into its own 1024x768 target, HD parts on top, then the targets onto the surface */
        static struct timespec h0; static int hn; static double hs; struct timespec a, b; clock_gettime(CLOCK_MONOTONIC, &a);
        int vw0 = vw, vh0 = vh;
        for (int k = 0; k < 2; k++) {
            glBindFramebuffer(GL_FRAMEBUFFER, fbo[k]); glViewport(0, 0, 1024, 768); vw = 1024; vh = 768;
            glUseProgram(prog); glActiveTexture(GL_TEXTURE0); glBindTexture(GL_TEXTURE_2D, tex);
            draw_tex(0, 0, 1024, 768, 0, k * 0.5f, 1, k * 0.5f + 0.5f);
            if (hd_draw(k == 0)) {           /* battle dialogue band stays the game's own, above every HD picture */
                glUseProgram(prog); glActiveTexture(GL_TEXTURE0); glBindTexture(GL_TEXTURE_2D, tex); glUniform1i(u_tex, 0);
                draw_tex(0, 512, 1024, 256, 0, 128 / 384.f, 1, 192 / 384.f);
            }
            hd_draw_overlay(k == 0);
            hd_draw_text(k == 0);
        }
        glBindFramebuffer(GL_FRAMEBUFFER, 0); vw = vw0; vh = vh0; glViewport(0, 0, vw, vh);
        glUseProgram(prog); glActiveTexture(GL_TEXTURE0); glUniform1i(u_tex, 0);
        jfloatArray rs[2] = {jtop, jbottom};
        for (int k = 0; k < 2; k++) {
            float *r = (*e)->GetFloatArrayElements(e, rs[k], 0);
            glBindTexture(GL_TEXTURE_2D, fbtex[k]);
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, f); glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, f);
            if (r[2] > 0 && r[3] > 0) draw_tex(r[0], r[1], r[2], r[3], 0, 1, 1, 0);   /* FBO rows are bottom-up */
            (*e)->ReleaseFloatArrayElements(e, rs[k], r, JNI_ABORT);
        }
        clock_gettime(CLOCK_MONOTONIC, &b); hs += (b.tv_sec - a.tv_sec) + (b.tv_nsec - a.tv_nsec) / 1e9;
        if (++hn % 300 == 0) LOG("hd compose %.2f ms/frame", hs * 1000 / 300), hs = 0;
        (void)h0;
        return;
    }
    float half = fb_h >= 384 ? 0.5f : 1.0f;   /* frame = top screen over bottom screen */
    jfloatArray arrs[2] = {jtop, jbottom};
    for (int k = 0; k < 2; k++) {
        float *r = (*e)->GetFloatArrayElements(e, arrs[k], 0);
        if (r[2] > 0 && r[3] > 0) {
            float v0 = k == 0 ? 0 : half, v1 = k == 0 ? half : 1;
            float v[8], uv[8] = {0, v1, 1, v1, 0, v0, 1, v0};
            quad_px(r[0], r[1], r[2], r[3], v);
            glVertexAttribPointer(a_pos, 2, GL_FLOAT, 0, 0, v); glEnableVertexAttribArray(a_pos);
            glVertexAttribPointer(a_uv, 2, GL_FLOAT, 0, 0, uv); glEnableVertexAttribArray(a_uv);
            glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);
        }
        (*e)->ReleaseFloatArrayElements(e, arrs[k], r, JNI_ABORT);
    }
}

JNIEXPORT void JNICALL Java_kr_srww_hd_Native_reset(JNIEnv *e, jclass c) { if (loaded) p_reset(); }

JNIEXPORT jint JNICALL Java_kr_srww_hd_Native_rumble(JNIEnv *e, jclass c, jfloatArray jout) {
    float o[3]; int d = hd_take_rumble(o);
    if (d >= 0) (*e)->SetFloatArrayRegion(e, jout, 0, 3, o);
    return d;
}
