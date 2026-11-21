/* SRW W HD — Android HD parts composition (phase 1: robot/OBJ sprites and BG tiles).
 *
 * Follows docs/ANDROID_HD_PORT_SPEC.md (PC path: hd_core.py, hd_parts.py compose, native_composition.c).
 *   start:  register_parts(hashes) -> register_effect_parts(ids) -> set_ready_parts(none) -> set_hd_enabled(1)
 *   frame:  textures decoded so far become "ready"; bindings not ready stay native in the core (bit31),
 *           and their textures are requested, so nothing ever disappears while a texture loads.
 *   draw:   native screen (xBRZ or plain) into a 1024x768 target per DS screen (SCALE = 4 = texture scale),
 *           then every HD part back to front with the exact DS visibility mask (layer/priority/owner),
 *           window, BG-alpha foreground re-blend, MASTER_BRIGHT, flips and affine.
 * Pack: android_pack/parts.pack (scripts/build/build_android_pack.py), parts_hashes.bin, effect_ids.bin,
 *       pushed to <external files>/hd/.  WebP decoded with AImageDecoder (API 30+, loaded with dlopen).
 */
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <math.h>
#include <fcntl.h>
#include <unistd.h>
#include <dlfcn.h>
#include <pthread.h>
#include <GLES2/gl2.h>
#include <android/log.h>
#include "hd.h"

#define LOG(...) __android_log_print(ANDROID_LOG_INFO, "srwwhd", __VA_ARGS__)
#define S 4                                   /* HD pixels per native pixel */
#define HW (256 * S)
#define HH (192 * S)
#define BUDGET (400u << 20)                   /* GPU bytes for part textures */

/* ---- core API ---- */
static void (*c_register_parts)(const unsigned *, unsigned), (*c_register_effect)(const unsigned *, unsigned),
            (*c_set_ready)(const unsigned *, unsigned), (*c_set_enabled)(unsigned),
            (*c_copy_parts)(void *, void *), (*c_copy_rendered_obj)(void *), (*c_copy_bg_parts)(void *),
            (*c_copy_layer_ids)(void *), (*c_copy_sub_parts)(void *, void *, void *, void *, void *, void *);
static int (*c_bg_info)(unsigned, unsigned *), (*c_copy_foreground)(void *), (*c_copy_window)(void *);

/* ---- pack ---- */
#pragma pack(push, 1)
typedef struct { uint32_t binding, hash, source; uint16_t w, h; uint64_t off; uint32_t len; } Entry;
#pragma pack(pop)
typedef struct { int fd; uint64_t off; uint32_t len; int state; GLuint tex; int w, h; unsigned bytes; unsigned last; uint8_t *px; } Source;
enum { NONE, ASKED, DECODED, ON_GPU };

static int fd = -1, active, enabled;
static Entry *ents; static unsigned nent;
static int *ent_of;  static unsigned nbind;      /* binding -> entry index or -1 */
static int *src_of;                               /* entry index -> source index */
static Source *srcs; static unsigned nsrc;
static unsigned *ready; static int ready_dirty;
static unsigned frame_no, gpu_bytes;

/* decode thread queues */
static pthread_mutex_t qlock = PTHREAD_MUTEX_INITIALIZER; static pthread_cond_t qcond = PTHREAD_COND_INITIALIZER;
#define QN 8192
static int askq[QN]; static unsigned ask_h, ask_t;
static int doneq[QN]; static unsigned done_h, done_t;

typedef struct AImageDecoder AImageDecoder; typedef struct AImageDecoderHeaderInfo AImageDecoderHeaderInfo;
static int (*d_create)(const void *, size_t, AImageDecoder **); static void (*d_delete)(AImageDecoder *);
static int (*d_format)(AImageDecoder *, int32_t); static int (*d_unpremul)(AImageDecoder *, bool);
static const AImageDecoderHeaderInfo *(*d_info)(const AImageDecoder *);
static int32_t (*d_w)(const AImageDecoderHeaderInfo *), (*d_h)(const AImageDecoderHeaderInfo *);
static size_t (*d_stride)(AImageDecoder *); static int (*d_decode)(AImageDecoder *, void *, size_t, size_t);

static void *decoder(void *arg) {
    for (;;) {
        pthread_mutex_lock(&qlock);
        while (ask_h == ask_t) pthread_cond_wait(&qcond, &qlock);
        int s = askq[ask_t]; ask_t = (ask_t + 1) % QN;
        pthread_mutex_unlock(&qlock);
        Source *r = &srcs[s]; uint8_t *buf = malloc(r->len), *px = NULL; int w = 0, h = 0;
        if (buf && pread(r->fd, buf, r->len, r->off) == (ssize_t)r->len) {
            AImageDecoder *d = NULL;
            if (d_create(buf, r->len, &d) == 0) {
                d_format(d, 1 /* RGBA_8888 */); d_unpremul(d, true);
                const AImageDecoderHeaderInfo *in = d_info(d); w = d_w(in); h = d_h(in);
                size_t st = d_stride(d);
                px = malloc(st * h);
                if (px && d_decode(d, px, st, st * h) != 0) { free(px); px = NULL; }
                if (px && st != (size_t)w * 4) for (int y = 1; y < h; y++) memmove(px + y * w * 4, px + y * st, w * 4);
                d_delete(d);
            }
        }
        free(buf);
        pthread_mutex_lock(&qlock);
        r->px = px; r->w = w; r->h = h; r->state = DECODED;   /* px NULL = failed, never retried */
        doneq[done_h] = s; done_h = (done_h + 1) % QN;
        pthread_mutex_unlock(&qlock);
    }
    return arg;
}

static int scene_init(void *core, const char *dir);
static void portraits_init(const char *dir);
static void rumble_init(void *core);
static void text_init(const char *dir);
static void indexed_init(void *core, const char *dir);
static const struct Recolour *recolour_of(unsigned binding);
static void glyph_gl_init(void);
static void portraits_scan(int k, const uint32_t *scr);
static void *readall(const char *path, size_t *n) {
    FILE *f = fopen(path, "rb"); if (!f) return NULL;
    fseek(f, 0, SEEK_END); long z = ftell(f); fseek(f, 0, SEEK_SET);
    void *b = malloc(z ? z : 1); if (b && fread(b, 1, z, f) != (size_t)z) { free(b); b = NULL; }
    fclose(f); *n = z; return b;
}

#define CSYM(p, n) if (!(*(void **)&p = dlsym(core, n))) { LOG("hd: core lacks %s", n); return 0; }

int hd_init(void *core, const char *dir) {
    CSYM(c_register_parts, "retro_srw_register_parts") CSYM(c_register_effect, "retro_srw_register_effect_parts")
    CSYM(c_set_ready, "retro_srw_set_ready_parts") CSYM(c_set_enabled, "retro_srw_set_hd_enabled")
    CSYM(c_copy_parts, "retro_srw_copy_parts") CSYM(c_copy_rendered_obj, "retro_srw_copy_rendered_obj")
    CSYM(c_copy_bg_parts, "retro_srw_copy_bg_parts") CSYM(c_copy_layer_ids, "retro_srw_copy_layer_ids")
    CSYM(c_copy_sub_parts, "retro_srw_copy_sub_parts") CSYM(c_bg_info, "retro_srw_get_bg_info")
    CSYM(c_copy_foreground, "retro_srw_copy_foreground") CSYM(c_copy_window, "retro_srw_copy_window")
    rumble_init(core);                        /* works without the HD packs */
    void *jg = dlopen("libjnigraphics.so", RTLD_NOW);
    if (!jg) { LOG("hd: no libjnigraphics"); return 0; }
#define DSYM(p, n) if (!(*(void **)&p = dlsym(jg, n))) { LOG("hd: no %s (Android 11+ needed)", n); return 0; }
    DSYM(d_create, "AImageDecoder_createFromBuffer") DSYM(d_delete, "AImageDecoder_delete")
    DSYM(d_format, "AImageDecoder_setAndroidBitmapFormat") DSYM(d_unpremul, "AImageDecoder_setUnpremultipliedRequired")
    DSYM(d_info, "AImageDecoder_getHeaderInfo") DSYM(d_w, "AImageDecoderHeaderInfo_getWidth")
    DSYM(d_h, "AImageDecoderHeaderInfo_getHeight") DSYM(d_stride, "AImageDecoder_getMinimumStride")
    DSYM(d_decode, "AImageDecoder_decodeImage")
    char p[1200];
    snprintf(p, sizeof p, "%s/parts.pack", dir);
    fd = open(p, O_RDONLY); if (fd < 0) { LOG("hd: no pack %s", p); return 0; }
    char head[12]; if (pread(fd, head, 12, 0) != 12 || memcmp(head, "SRWHDPK1", 8)) { LOG("hd: bad pack"); return 0; }
    memcpy(&nent, head + 8, 4);
    ents = malloc(sizeof(Entry) * nent);
    if (pread(fd, ents, sizeof(Entry) * nent, 12) != (ssize_t)(sizeof(Entry) * nent)) { LOG("hd: short pack"); return 0; }
    unsigned nmain = nent; int fd2 = -1;
    snprintf(p, sizeof p, "%s/parts_indexed.pack", dir);
    fd2 = open(p, O_RDONLY);
    if (fd2 >= 0 && pread(fd2, head, 12, 0) == 12 && !memcmp(head, "SRWHDPK1", 8)) {
        unsigned n2; memcpy(&n2, head + 8, 4);
        ents = realloc(ents, sizeof(Entry) * (nent + n2));
        if (pread(fd2, ents + nent, sizeof(Entry) * n2, 12) == (ssize_t)(sizeof(Entry) * n2)) nent += n2;
    }
    size_t hn = 0; unsigned *hashes;
    snprintf(p, sizeof p, "%s/parts_hashes.bin", dir);
    if (!(hashes = readall(p, &hn))) { LOG("hd: no hashes"); return 0; }
    nbind = hn / 4;
    ent_of = malloc(sizeof(int) * (nbind + 1)); for (unsigned i = 0; i <= nbind; i++) ent_of[i] = -1;
    int *map = malloc(sizeof(int) * (nbind + 1)); for (unsigned i = 0; i <= nbind; i++) map[i] = -1;
    src_of = malloc(sizeof(int) * nent); srcs = calloc(nent + 4096, sizeof(Source)); ready = malloc(sizeof(unsigned) * nent);
    for (unsigned i = 0; i < nent; i++) {
        Entry *e = &ents[i];
        if (e->binding <= nbind) ent_of[e->binding] = i;
        if (e->source > nbind) e->source = e->binding;
        if (map[e->source] < 0) { map[e->source] = nsrc; srcs[nsrc].fd = i < nmain ? fd : fd2; srcs[nsrc].off = e->off; srcs[nsrc].len = e->len; nsrc++; }
        src_of[i] = map[e->source];
    }
    free(map);
    c_register_parts(hashes, nbind); free(hashes);
    snprintf(p, sizeof p, "%s/effect_ids.bin", dir);
    size_t en = 0; unsigned *eff = readall(p, &en);
    if (eff) { c_register_effect(eff, en / 4); free(eff); }
    indexed_init(core, dir);                  /* 1.3: HUD digits and effects in another palette (recoloured) */
    scene_init(core, dir);
    portraits_init(dir);
    text_init(dir);                    /* cut-ins (1.4, 1.5) after parts (1.1, 1.2) */
    c_set_ready(ready, 0);                    /* async mode: nothing hidden until its texture is on the GPU */
    pthread_t t[2]; for (int i = 0; i < 2; i++) pthread_create(&t[i], NULL, decoder, NULL);   /* two decoders: animated cut-ins arrive quickly */
    active = 1; hd_set_enabled(1);
    LOG("hd: %u bindings, %u textures, effect %zu", nent, nsrc, en / 4);
    return 1;
}

void hd_set_enabled(int on) { enabled = on; if (active) c_set_enabled(on ? 1 : 0); }
int hd_active(void) { return active && enabled; }

static void ask(int s) {
    if (srcs[s].state != NONE) return;
    pthread_mutex_lock(&qlock);
    if ((ask_h + 1) % QN != ask_t) { srcs[s].state = ASKED; askq[ask_h] = s; ask_h = (ask_h + 1) % QN; pthread_cond_signal(&qcond); }
    pthread_mutex_unlock(&qlock);
}

/* before retro_run: upload decoded textures, evict old ones, tell the core which parts are ready */
void hd_before_run(void) {
    if (!active) return;
    frame_no++;
    unsigned up = 0;
    for (;;) {
        pthread_mutex_lock(&qlock);
        if (done_h == done_t || up > (24u << 20)) { pthread_mutex_unlock(&qlock); break; }
        int s = doneq[done_t]; done_t = (done_t + 1) % QN;
        pthread_mutex_unlock(&qlock);
        Source *r = &srcs[s];
        if (!r->px) continue;                     /* failed decode: stays native */
        glGenTextures(1, &r->tex); glBindTexture(GL_TEXTURE_2D, r->tex);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR); glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE); glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
        glPixelStorei(GL_UNPACK_ALIGNMENT, 4);
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, r->w, r->h, 0, GL_RGBA, GL_UNSIGNED_BYTE, r->px);
        free(r->px); r->px = NULL;
        r->bytes = r->w * r->h * 4; gpu_bytes += r->bytes; up += r->bytes;
        r->state = ON_GPU; r->last = frame_no; ready_dirty = 1;
    }
    if (gpu_bytes > BUDGET) {                      /* drop textures unused for 4 s, oldest first */
        for (int pass = 0; pass < 2 && gpu_bytes > BUDGET * 9 / 10; pass++)
            for (unsigned s = 0; s < nsrc && gpu_bytes > BUDGET * 9 / 10; s++) {
                Source *r = &srcs[s];
                if (r->state != ON_GPU || frame_no - r->last < (pass ? 240u : 1800u)) continue;
                glDeleteTextures(1, &r->tex); r->tex = 0; gpu_bytes -= r->bytes; r->state = NONE; ready_dirty = 1;
            }
    }
    if (ready_dirty) {
        unsigned n = 0;
        for (unsigned i = 0; i < nent; i++) if (srcs[src_of[i]].state == ON_GPU) ready[n++] = ents[i].binding;
        c_set_ready(ready, n); ready_dirty = 0;
    }
}

/* ---- per-frame data (after the run that produced the shown frame) ---- */
static uint32_t parts[128][8], sparts[128][8], bgparts[3200][8];
static uint8_t owners[192 * 256], sowners[192 * 256], ids[192 * 256], sids[192 * 256], oam[1024], soam[1024], win[192 * 256];
static uint16_t spal[128][16], tpal[128][16];
static void (*c_copy_part_palettes)(void *);
static uint8_t bgprio[6], sbgprio[6];
static uint64_t fgrec[192 * 256];
static int fg_on, win_on;
static void scene_capture(const uint32_t *rgba);

void hd_after_run(const uint32_t *rgba) {
    if (!hd_active()) return;
    scene_capture(rgba);
    portraits_scan(0, rgba); portraits_scan(1, rgba + 256 * 192);
    c_copy_parts(parts, owners); c_copy_rendered_obj(oam);
    if (c_copy_part_palettes) c_copy_part_palettes(tpal); c_copy_bg_parts(bgparts); c_copy_layer_ids(ids);
    uint8_t pr[4] = {4, 4, 4, 4};
    c_copy_sub_parts(sparts, sowners, soam, spal, sids, pr);
    for (int l = 0; l < 4; l++) { unsigned o[9] = {0}; c_bg_info(l, o); bgprio[l] = o[8]; sbgprio[l] = pr[l]; }
    bgprio[4] = bgprio[5] = sbgprio[4] = sbgprio[5] = 4;
    fg_on = c_copy_foreground(fgrec);
    win_on = c_copy_window(win);
    if (win_on) { int all = 1; for (int i = 0; i < 192 * 256; i++) if ((win[i] & 31) != 31) { all = 0; break; } if (all) win_on = 0; }
}

/* ---- GL ---- */
static GLint u_rmode, u_rn, u_ka, u_kb, u_rs, u_rd;
static GLuint prog, masktex, fgtex; static GLint a_p, a_t, a_m, u_art, u_mask, u_fg, u_use, u_alpha, u_bright;
#define MW 1024
#define MH 1024
static uint8_t maskbuf[MW * MH]; static int shelf_x, shelf_y, shelf_h;
static uint8_t fgplane[192 * 256 * 4];

static GLuint sh(GLenum t, const char *s) {
    GLuint o = glCreateShader(t); glShaderSource(o, 1, &s, 0); glCompileShader(o);
    GLint ok; glGetShaderiv(o, GL_COMPILE_STATUS, &ok);
    if (!ok) { char b[1024]; glGetShaderInfoLog(o, sizeof b, 0, b); LOG("hd shader: %s", b); }
    return o;
}

void hd_gl_init(void) {
    prog = glCreateProgram();
    glAttachShader(prog, sh(GL_VERTEX_SHADER,
        "attribute vec2 p;attribute vec2 t;attribute vec2 m;varying vec2 vt;varying vec2 vm;"
        "void main(){vt=t;vm=m;gl_Position=vec4(p,0.,1.);}"));
    glAttachShader(prog, sh(GL_FRAGMENT_SHADER,
        "precision highp float;varying vec2 vt;varying vec2 vm;uniform sampler2D art;uniform sampler2D mask;uniform sampler2D fg;"
        "uniform float use;uniform float alpha;uniform vec2 bright;uniform float rmode;uniform float rn;uniform vec3 ka;uniform vec3 kb;uniform vec3 rs[15];uniform vec3 rd[15];"
        "void main(){if(vt.x<0.||vt.y<0.||vt.x>1.||vt.y>1.)discard;"
        "vec4 c=texture2D(art,vt);float a=c.a*alpha;float k=1.;"
        "if(use>.5){k=texture2D(mask,vm).a;a*=k>.25?1.:0.;}"
        "if(a<=0.)discard;vec3 rgb=c.rgb;"
        "if(rmode>1.5){vec3 p=rgb*255.;float ws=0.;vec3 sh=vec3(0.);for(int i=0;i<15;i++){if(float(i)<rn){vec3 d=p-rs[i];float w=1./(dot(d,d)+576.);ws+=w;sh+=w*(rd[i]-rs[i]);}}"
        "rgb=clamp((p+sh/max(ws,1e-9))/255.,0.,1.);}else if(rmode>.5)rgb=clamp(rgb*ka+kb/255.,0.,1.);"
        "if(bright.x>1.5)rgb*=1.-bright.y;else if(bright.x>.5)rgb+=(1.-rgb)*bright.y;"
        "if(k>.25&&k<.75){vec4 e=texture2D(fg,vec2(gl_FragCoord.x/1024.,1.-gl_FragCoord.y/768.));rgb=clamp(rgb*(e.a*255./16.)+e.rgb,0.,1.);}"
        "gl_FragColor=vec4(rgb,a);}"));
    glLinkProgram(prog);
    a_p = glGetAttribLocation(prog, "p"); a_t = glGetAttribLocation(prog, "t"); a_m = glGetAttribLocation(prog, "m");
    u_art = glGetUniformLocation(prog, "art"); u_mask = glGetUniformLocation(prog, "mask"); u_fg = glGetUniformLocation(prog, "fg");
    u_rmode = glGetUniformLocation(prog, "rmode"); u_rn = glGetUniformLocation(prog, "rn"); u_ka = glGetUniformLocation(prog, "ka");
    u_kb = glGetUniformLocation(prog, "kb"); u_rs = glGetUniformLocation(prog, "rs"); u_rd = glGetUniformLocation(prog, "rd");
    u_use = glGetUniformLocation(prog, "use"); u_alpha = glGetUniformLocation(prog, "alpha"); u_bright = glGetUniformLocation(prog, "bright");
    GLuint t[2]; glGenTextures(2, t); masktex = t[0]; fgtex = t[1];
    for (int i = 0; i < 2; i++) {
        glBindTexture(GL_TEXTURE_2D, t[i]);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST); glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE); glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
    }
    glBindTexture(GL_TEXTURE_2D, masktex); glPixelStorei(GL_UNPACK_ALIGNMENT, 1);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_ALPHA, MW, MH, 0, GL_ALPHA, GL_UNSIGNED_BYTE, NULL);
    glBindTexture(GL_TEXTURE_2D, fgtex);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 256, 192, 0, GL_RGBA, GL_UNSIGNED_BYTE, NULL);
    /* textures from an older GL context are gone: forget them */
    for (unsigned s = 0; s < nsrc; s++) if (srcs[s].state == ON_GPU) { srcs[s].state = NONE; srcs[s].tex = 0; ready_dirty = 1; }
    gpu_bytes = 0;
    glyph_gl_init();
}

/* ---- tasks ---- */
typedef struct {
    int key, src;                 /* key = sort order (priority, kind, item) */
    float x0, y0, x1, y1;         /* native screen rect of the drawn quad */
    float u0, v0, dux, duy, dvx, dvy;   /* art uv at (x0,y0) and per native pixel */
    int left, top, w, h, mx, my, state, fgany;
    float alpha, bmode, bamt;
    uint32_t ctl;
    int type, cut, prio, item, pilot;      /* type 1 = cut-in plane, 2 = battle background */
    int rmode, rn; float ka[3], kb[3], rs[15][3], rd[15][3];   /* recolour: 0 none, 1 affine, 2 smooth */
} Task;
static Task tasks[128 + 3200 + 64];

static int mask_alloc(int w, int h, int *x, int *y) {
    if (shelf_x + w > MW) { shelf_y += shelf_h; shelf_x = 0; shelf_h = 0; }
    if (shelf_y + h > MH || w > MW) return 0;
    *x = shelf_x; *y = shelf_y; shelf_x += w; if (h > shelf_h) shelf_h = h; return 1;
}

/* DS visibility of one part over its native region (vis.c), plus window and foreground eligibility.
 * mask: 0 hidden, 255 visible, 128 visible and re-blended with the BG-alpha foreground. */
static int visibility(int top_screen, Task *k, int priority, int kind, int item, uint32_t control, uint8_t *out, int stride) {
    const uint8_t *L = top_screen ? ids : sids, *O = top_screen ? owners : sowners, *bp = top_screen ? bgprio : sbgprio;
    const uint8_t *om = top_screen ? oam : soam;
    int bit = kind ? 8 + item : 12;
    int alpha_bg = (control & 0xc0) == 0x40 && ((control >> bit) & 1);
    int target = kind ? item : 4, count = 0, total = k->w * k->h;
    k->fgany = 0;
    for (int y = 0; y < k->h; y++) for (int x = 0; x < k->w; x++) {
        int p = (k->top + y) * 256 + k->left + x, layer = L[p], vis = layer == 5;
        if (layer < 4) {
            int b = bp[layer];
            vis = vis || b > priority || (b == priority && (!kind || layer > item));
            if (alpha_bg && ((control >> layer) & 1)) vis = 1;
        } else if (layer == 4) {
            int o = O[p], ob = (om[o * 8 + 5] >> 2) & 3;
            vis = ob > priority || (ob == priority && o >= item && !kind);
        }
        int v = vis ? 255 : 0;
        if (top_screen && fg_on) {
            uint64_t r = fgrec[p]; int fl = (r >> 15) & 7;
            if (fl) {
                fl -= 1;
                int eva = (r >> 18) & 31, evb = (r >> 23) & 31, targets = (r >> 32) & 31, dest = (r >> 37) & 7;
                int fprio = bp[fl], dprio = dest < 6 ? bp[dest] : 4;
                int energy = target == 4 && eva > 0 && evb == 16 && fprio == priority;
                int front = fprio < priority || (fprio == priority && fl < target && target < 4) || energy;
                int behind = dest < 4 && (dprio > priority || (dprio == priority && (target == 4 || dest > target)));
                int adjacent = dest == target || dest == 5 || behind;
                int el = (layer == fl || (energy && layer == 4)) && ((targets >> target) & 1) && front && adjacent;
                if (layer == 4 && !vis) el = 0;
                if (el) { v = 128; k->fgany = 1; }
            }
        }
        if (top_screen && win_on && !((win[p] >> (kind ? item : 4)) & 1)) v = 0;
        if (out) out[y * stride + x] = v;
        count += v != 0;
    }
    return count == 0 ? 0 : count == total ? 2 : 1;
}

/* fill quad geometry; returns 0 when off screen */
static int place(Task *k, float x, float y, float fw, float fh) {
    k->x0 = x; k->y0 = y; k->x1 = x + fw; k->y1 = y + fh;
    float cx0 = fmaxf(k->x0, 0), cy0 = fmaxf(k->y0, 0), cx1 = fminf(k->x1, 256), cy1 = fminf(k->y1, 192);
    if (cx0 >= cx1 || cy0 >= cy1) return 0;
    k->u0 += k->dux * (cx0 - x) + k->duy * (cy0 - y); k->v0 += k->dvx * (cx0 - x) + k->dvy * (cy0 - y);
    k->x0 = cx0; k->y0 = cy0; k->x1 = cx1; k->y1 = cy1;
    k->left = (int)floorf(cx0); k->top = (int)floorf(cy0);
    k->w = (int)ceilf(cx1) - k->left; k->h = (int)ceilf(cy1) - k->top;
    return 1;
}

static void bright(Task *k, uint32_t v) {
    int mode = (v >> 14) & 3; k->bmode = mode == 1 || mode == 2 ? mode : 0; k->bamt = (v & 31) > 16 ? 1.f : (v & 31) / 16.f;
}

static int cmp(const void *a, const void *b) { return ((const Task *)b)->key - ((const Task *)a)->key; }

static void recolour_task(Task *k, unsigned binding, uint32_t rgbhash, const uint16_t *pal);
static int obj_task(int top_screen, int i, const uint32_t *row, Task *k) {
    int e = row[0] <= nbind ? ent_of[row[0]] : -1; if (e < 0) return 0;
    int s = src_of[e];
    if (row[7] & 0x80000000u) { ask(s); return 0; }       /* core keeps it native this frame */
    if (srcs[s].state != ON_GPU) { ask(s); return 0; }
    uint32_t a = row[1], b = row[2], c = row[3];
    int w = ents[e].w, h = ents[e].h, x = b & 511, y = a & 255;
    if (x >= 256) x -= 512; if (y >= 192) y -= 256;
    int priority = (c >> 10) & 3;
    memset(k, 0, sizeof *k); k->src = s; k->key = (priority << 16) | (0 << 12) | i;
    float fw = w, fh = h;
    if (a & 256) {                                   /* affine: OAM matrix (b>>9)&31 */
        const uint8_t *om = top_screen ? oam : soam; int m = (b >> 9) & 31;
        float pm[4];
        for (int q = 0; q < 4; q++) { int o = (m * 4 + q) * 8 + 6; pm[q] = (int16_t)(om[o] | om[o + 1] << 8) / 256.f; }
        if (a & 512) { fw = 2 * w; fh = 2 * h; }
        /* input art pixel (native units) = M * (X,Y) + (w/2 - fw/2*pa - fh/2*pb, h/2 - fw/2*pc - fh/2*pd) */
        float ox = w / 2.f - fw / 2 * pm[0] - fh / 2 * pm[1], oy = h / 2.f - fw / 2 * pm[2] - fh / 2 * pm[3];
        k->u0 = ox / w; k->v0 = oy / h; k->dux = pm[0] / w; k->duy = pm[1] / w; k->dvx = pm[2] / h; k->dvy = pm[3] / h;
    } else {
        int hf = b & 4096, vf = b & 8192;
        k->u0 = hf ? 1 : 0; k->dux = hf ? -1.f / w : 1.f / w; k->v0 = vf ? 1 : 0; k->dvy = vf ? -1.f / h : 1.f / h;
    }
    if (!place(k, x, y, fw, fh)) return 0;
    bright(k, row[5]);
    k->alpha = 1;
    recolour_task(k, row[0], row[4], top_screen ? tpal[i] : spal[i]);
    if (((a >> 10) & 3) == 1) { int eva = row[6] & 31; k->alpha = (eva > 16 ? 16 : eva) / 16.f; }   /* semi-transparent OBJ */
    k->state = visibility(top_screen, k, priority, 0, i, row[7], NULL, 0);
    if (!k->state) return 0;
    k->mx = (priority << 8) | i; k->ctl = row[7];        /* remember for the mask pass */
    srcs[s].last = frame_no;
    return 1;
}

static int bg_task(const uint32_t *row, Task *k) {
    int e = row[0] <= nbind ? ent_of[row[0]] : -1; if (e < 0) return 0;
    int s = src_of[e];
    if (row[7] & 0x80000000u) { ask(s); return 0; }
    if (srcs[s].state != ON_GPU) { ask(s); return 0; }
    int x = (int32_t)row[2], y = (int32_t)row[3], layer = row[4] & 3, priority = row[5] & 3;
    int w = ents[e].w, h = ents[e].h;
    memset(k, 0, sizeof *k); k->src = s; k->key = (priority << 16) | (1 << 12) | layer;
    int hf = row[1] & 0x400, vf = row[1] & 0x800;
    k->u0 = hf ? 1 : 0; k->dux = hf ? -1.f / w : 1.f / w; k->v0 = vf ? 1 : 0; k->dvy = vf ? -1.f / h : 1.f / h;
    if (!place(k, x, y, w, h)) return 0;
    bright(k, row[6]); k->alpha = 1;
    k->state = visibility(1, k, priority, 1, layer, row[7], NULL, 0);
    if (!k->state) return 0;
    k->mx = (priority << 8) | layer | 0x10000; k->ctl = row[7];
    srcs[s].last = frame_no;
    return 1;
}

#include "scene.inc"
#include "portraits.inc"
#include "rumble.inc"
#include "text.inc"
#include "indexed.inc"
void hd_rumble_frame(void) { rumble_frame(); }
