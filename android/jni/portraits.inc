/* Included at the end of hd.c: pilot portraits (emulator/hd_portraits.py, portraits.pack).
 * Lookup per screen: positions 136, 0, 24, 8..144 step 8; key = crc32 of rgb5 bytes of rows y+2..y+45,
 * columns 5..47; candidate accepted when the portrait_mask reference matches exactly. The HD face is
 * pasted with its own alpha above everything else on that screen. */
typedef struct { uint32_t key; int x, w, h, src; uint8_t *ref; } Face;
static Face *faces; static int nface;
static uint32_t crctab[256];
static int face_match[2][8], face_y[2][8], nmatch[2];
static uint32_t face_stamp[2] = {1, 1};

static uint32_t crc32b(uint32_t crc, const uint8_t *p, size_t n) {
    crc = ~crc;
    while (n--) crc = crctab[(crc ^ *p++) & 255] ^ (crc >> 8);
    return ~crc;
}

static void portraits_init(const char *dir) {
    for (uint32_t i = 0; i < 256; i++) { uint32_t c = i; for (int j = 0; j < 8; j++) c = (c >> 1) ^ ((c & 1) ? 0xedb88320u : 0); crctab[i] = c; }
    char p[1200]; snprintf(p, sizeof p, "%s/portraits.pack", dir);
    int f = open(p, O_RDONLY); if (f < 0) { LOG("hd: no portrait pack"); return; }
    FILE *in = fdopen(dup(f), "rb"); char head[8]; unsigned n = 0;
    if (!in || fread(head, 1, 8, in) != 8 || memcmp(head, "SRWHDPT1", 8) || fread(&n, 4, 1, in) != 1) { LOG("hd: bad portrait pack"); if (in) fclose(in); return; }
    faces = calloc(n, sizeof(Face));
#pragma pack(push, 1)
    struct { uint32_t key; int32_t x, w, h; uint64_t off; uint32_t len, has; } e;
#pragma pack(pop)
    for (unsigned i = 0; i < n; i++) {
        if (fread(&e, sizeof e, 1, in) != 1) break;
        Face *fc = &faces[nface];
        fc->key = e.key; fc->x = e.x; fc->w = e.w; fc->h = e.h;
        if (e.has) { fc->ref = malloc(56 * 48 * 4); if (fread(fc->ref, 1, 56 * 48 * 4, in) != 56 * 48 * 4) break; }
        fc->src = nsrc; srcs[nsrc].fd = f; srcs[nsrc].off = e.off; srcs[nsrc].len = e.len; nsrc++;
        nface++;
    }
    fclose(in);
    LOG("hd: %d portraits", nface);
}

static int face_reference_ok(const Face *fc, const uint32_t *scr, int x, int y) {
    if (!fc->ref) return 1;
    const uint8_t *mask = fc->ref, *rgb = fc->ref + 56 * 48;
    for (int j = 0; j < 48; j++) for (int i = 0; i < 56; i++) {
        if (!mask[j * 56 + i]) continue;
        uint32_t c = scr[(y + j) * 256 + x + i]; const uint8_t *e = rgb + (j * 56 + i) * 3;
        if ((int)((c & 255) >> 3) != e[0] || (int)(((c >> 8) & 255) >> 3) != e[1] || (int)(((c >> 16) & 255) >> 3) != e[2]) return 0;
    }
    return 1;
}

/* scr: RGBA 256x192 of one screen */
static void portraits_scan(int k, const uint32_t *scr) {
    if (!nface) return;
    /* the whole searched strip: unchanged = same answer */
    uint32_t stamp = 0; static uint8_t strip[192 * 56 * 3];
    for (int y = 0; y < 192; y++) for (int x = 0; x < 56; x++) {
        uint32_t c = scr[y * 256 + x]; uint8_t *o = strip + (y * 56 + x) * 3; o[0] = c; o[1] = c >> 8; o[2] = c >> 16;
    }
    stamp = crc32b(0, strip, sizeof strip);
    if (stamp == face_stamp[k]) return;
    face_stamp[k] = stamp; nmatch[k] = 0;
    static const int ys0[3] = {136, 0, 24};
    int ys[24], ny = 0;
    for (int i = 0; i < 3; i++) ys[ny++] = ys0[i];
    for (int y = 8; y <= 144; y += 8) if (y != 24 && y != 136) ys[ny++] = y;
    static uint8_t cell[44 * 43 * 3];
    for (int t = 0; t < ny && nmatch[k] < 8; t++) {
        int y = ys[t], busy = 0;
        for (int m = 0; m < nmatch[k]; m++) if (y < face_y[k][m] + 48 && face_y[k][m] < y + 48) busy = 1;
        if (busy || y + 48 > 192) continue;
        for (int j = 0; j < 44; j++) for (int i = 0; i < 43; i++) {
            uint32_t c = scr[(y + 2 + j) * 256 + 5 + i]; uint8_t *o = cell + (j * 43 + i) * 3;
            o[0] = (c & 255) >> 3; o[1] = ((c >> 8) & 255) >> 3; o[2] = ((c >> 16) & 255) >> 3;
        }
        uint32_t key = crc32b(0, cell, sizeof cell);
        for (int fi = 0; fi < nface; fi++) {
            if (faces[fi].key != key || !face_reference_ok(&faces[fi], scr, faces[fi].x, y)) continue;
            face_match[k][nmatch[k]] = fi; face_y[k][nmatch[k]] = y; nmatch[k]++;
            break;
        }
    }
}

/* above everything on that screen (renderer.py: portraits after the dialogue band) */
void hd_draw_overlay(int top_screen) {
    if (!hd_active()) return;
    int k = top_screen ? 0 : 1, any = 0;
    for (int m = 0; m < nmatch[k]; m++) {
        Face *fc = &faces[face_match[k][m]];
        if (srcs[fc->src].state != ON_GPU) { ask(fc->src); continue; }
        srcs[fc->src].last = frame_no;
        if (!any) {
            glUseProgram(prog); glUniform1i(u_art, 0); glActiveTexture(GL_TEXTURE0);
            glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
            glEnableVertexAttribArray(a_p); glEnableVertexAttribArray(a_t); glEnableVertexAttribArray(a_m);
            any = 1;
        }
        Task t; memset(&t, 0, sizeof t);
        t.src = fc->src; t.alpha = 1; t.state = 3; t.dux = 1.f / fc->w; t.dvy = 1.f / fc->h;
        if (!place(&t, fc->x, face_y[k][m], fc->w, fc->h)) continue;
        quad(&t);
    }
    if (any) { glDisableVertexAttribArray(a_m); glDisable(GL_BLEND); }
}
