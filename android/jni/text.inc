/* Included at the end of hd.c: Korean bitmap glyph recognition and HD lettering
 * (port of emulator/hd_fonts.py FontRenderer: _recognize, _heal_native, compose).
 * Recognition on the native screen; the recognised glyphs are erased from the native picture by
 * row interpolation (same as _heal_native) before it is scaled, then drawn again with a scalable
 * font (Java Glyphs: the device's Korean system font; the PC uses Malgun Gothic, which may not be
 * shipped). Unknown, clipped or partly revealed glyphs stay native. */
#include <jni.h>

typedef struct { int n, kb; uint8_t *keys; uint32_t (*cp)[4]; } Table;
static Table T_full, T_narrow, T_compact, T_hud, T_label, T_fore;
static int text_ready;

static int read_table(FILE *in, Table *t) {
    uint32_t n, kb;
    if (fread(&n, 4, 1, in) != 1 || fread(&kb, 4, 1, in) != 1) return 0;
    t->n = n; t->kb = kb; t->keys = malloc(n * kb + 1); t->cp = malloc(sizeof(uint32_t[4]) * (n + 1));
    for (uint32_t i = 0; i < n; i++) if (fread(t->keys + i * kb, 1, kb, in) != kb || fread(t->cp[i], 4, 4, in) != 4) return 0;
    return 1;
}

static void text_init(const char *dir) {
    char p[1200]; snprintf(p, sizeof p, "%s/text.pack", dir);
    FILE *in = fopen(p, "rb"); char head[8];
    if (!in) { LOG("hd: no text pack"); return; }
    if (fread(head, 1, 8, in) == 8 && !memcmp(head, "SRWHDTX1", 8) && read_table(in, &T_full) && read_table(in, &T_narrow)
        && read_table(in, &T_compact) && read_table(in, &T_hud) && read_table(in, &T_label) && read_table(in, &T_fore)) text_ready = 1;
    fclose(in);
    LOG("hd: text tables %s (%d glyphs)", text_ready ? "ready" : "bad", T_full.n);
}

static int find_key(const Table *t, const uint8_t *key) {          /* sorted keys: first equal */
    int lo = 0, hi = t->n;
    while (lo < hi) { int mid = (lo + hi) / 2; if (memcmp(t->keys + mid * t->kb, key, t->kb) < 0) lo = mid + 1; else hi = mid; }
    return lo < t->n && !memcmp(t->keys + lo * t->kb, key, t->kb) ? lo : -1;
}

/* ---- candidates ---- */
typedef struct { int x, y, w, h; uint32_t cp[4]; uint8_t ink[256]; } Cand;
#define MAXC 3000
static Cand cands[MAXC], tmp[MAXC]; static int ncand;

static int is_alnum1(uint32_t c) {
    return (c >= '0' && c <= '9') || (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') || (c >= 0xAC00 && c <= 0xD7A3) || (c >= 0x3131 && c <= 0x318E)
        || (c >= 0x4E00 && c <= 0x9FFF) || (c >= 0xFF10 && c <= 0xFF19) || (c >= 0xFF21 && c <= 0xFF3A) || (c >= 0xFF41 && c <= 0xFF5A)
        || (c >= 0x3041 && c <= 0x30FA) || c == 0x30FC || (c >= 0x0391 && c <= 0x03C9) || (c >= 0x0410 && c <= 0x044F)
        || (c >= 0x2160 && c <= 0x217F) || (c >= 0x2460 && c <= 0x249B) || c == 0x00AA || c == 0x00BA;
}
static int is_alnum(const uint32_t *cp) { if (!cp[0]) return 0; for (int i = 0; i < 4 && cp[i]; i++) if (!is_alnum1(cp[i])) return 0; return 1; }
static int is_kanji(const uint32_t *cp) { return !cp[1] && cp[0] >= 0x4E00 && cp[0] <= 0x9FFF; }

/* sliding-window scan of a mask over rows [y0, y1): FontRenderer._scan */
static int scan(const uint8_t *mask, int y0, int y1, int h, int w, const Table *t, int mn, int mx, Cand *out, int room) {
    static int integral[193][257];
    int n = 0, rows = y1 - y0;
    if (rows < h) return 0;
    for (int x = 0; x <= 256; x++) integral[0][x] = 0;
    for (int y = 0; y < rows; y++) { int run = 0; integral[y + 1][0] = 0; for (int x = 0; x < 256; x++) { run += mask[(y0 + y) * 256 + x] != 0; integral[y + 1][x + 1] = integral[y][x + 1] + run; } }
    uint8_t key[32];
    for (int y = 0; y + h <= rows; y++) for (int x = 0; x + w <= 256; x++) {
        int c = integral[y + h][x + w] - integral[y][x + w] - integral[y + h][x] + integral[y][x];
        if (c < mn || c > mx) continue;
        memset(key, 0, sizeof key); int bit = 0;
        for (int j = 0; j < h; j++) for (int i = 0; i < w; i++, bit++) if (mask[(y0 + y + j) * 256 + x + i]) key[bit >> 3] |= 0x80 >> (bit & 7);
        int k = find_key(t, key); if (k < 0) continue;
        if (n >= room) return n;
        Cand *o = &out[n++]; o->x = x; o->y = y0 + y; o->w = w; o->h = h; memcpy(o->cp, t->cp[k], sizeof o->cp);
        for (int j = 0; j < h; j++) for (int i = 0; i < w; i++) o->ink[j * w + i] = mask[(y0 + y + j) * 256 + x + i] != 0;
    }
    return n;
}

static int battle_scan;
static int scan_active(const uint8_t *mask, int h, int w, const Table *t, int mn, int mx, Cand *out, int room) {
    if (!battle_scan) return scan(mask, 0, 192, h, w, t, mn, mx, out, room);
    int n = scan(mask, 0, 16, h, w, t, mn, mx, out, room);
    return n + scan(mask, 120, 192, h, w, t, mn, mx, out + n, room - n);
}

/* ---- per-screen recognition result ---- */
typedef struct { int x, y, w, h, button; uint32_t cp[4]; uint8_t rgb[3]; } Glyph;
typedef struct { int left, top, right, bottom, sl, sr; } Repair;
typedef struct {
    uint32_t stamp; int n; Glyph g[1024];
    uint8_t mask[192 * 256];                     /* pixels to heal (dilated ink + hud erasers + selected buttons) */
    int nrep; Repair rep[64];
} TextScreen;
static TextScreen ts[2];
/* glyphs held while their own ink pixels are unchanged (hd_fonts.py held_glyphs) */
typedef struct { int x, y, w, h, button; uint32_t cp[4]; uint8_t ink[256]; uint32_t col[256]; } Held;
static Held held[2][1024], fresh[1024]; static int nheld[2];

static JNIEnv *jenv; static jclass glyph_class; static jmethodID m_has, m_render;
void hd_set_jni(JNIEnv *e) {
    jenv = e;
    if (!glyph_class && e) {
        jclass c = (*e)->FindClass(e, "kr/srww/hd/Glyphs");
        if (c) { glyph_class = (*e)->NewGlobalRef(e, c); m_has = (*e)->GetStaticMethodID(e, c, "has", "(Ljava/lang/String;)Z"); m_render = (*e)->GetStaticMethodID(e, c, "render", "(Ljava/lang/String;III)[B"); }
        else (*e)->ExceptionClear(e);
    }
}
static jstring jstr(const uint32_t *cp) {
    jchar u[8]; int n = 0;
    for (int i = 0; i < 4 && cp[i]; i++) { uint32_t c = cp[i]; if (c >= 0x10000) { c -= 0x10000; u[n++] = 0xD800 + (c >> 10); u[n++] = 0xDC00 + (c & 1023); } else u[n++] = c; }
    return (*jenv)->NewString(jenv, u, n);
}
static uint32_t dkey[4096]; static uint8_t dval[4096]; static int dn;
static int drawable(const uint32_t *cp) {
    uint32_t k = cp[0] * 2654435761u ^ cp[1] * 40503u ^ cp[2];
    for (int i = 0; i < dn; i++) if (dkey[i] == k) return dval[i];
    if (!jenv || !glyph_class) return 0;
    jstring s = jstr(cp); int v = (*jenv)->CallStaticBooleanMethod(jenv, glyph_class, m_has, s); (*jenv)->DeleteLocalRef(jenv, s);
    if (dn < 4096) { dkey[dn] = k; dval[dn] = v; dn++; }
    return v;
}

static int same_mask(const uint8_t *a, const uint8_t *b) { return !memcmp(a, b, 192 * 256); }
static int any_mask(const uint8_t *a) { for (int i = 0; i < 192 * 256; i++) if (a[i]) return 1; return 0; }

static int selected_span(const uint8_t *green, int left, int right, int y, int *sa, int *sb) {
    int l = left - 4 < 0 ? 0 : left - 4, r = right + 4 > 256 ? 256 : right + 4, A[16], B[16], ns = 0;
    for (int yy = (y - 2 < 0 ? 0 : y - 2); yy < (y + 14 > 192 ? 192 : y + 14); yy++) {
        const uint8_t *row = green + yy * 256; int a = 0, b = 256;
        for (int x = l - 1; x >= 0; x--) if (!row[x]) { a = x + 1; break; }
        for (int x = r; x < 256; x++) if (!row[x]) { b = x; break; }
        int cnt = 0; for (int x = a; x < b; x++) cnt += row[x];
        if (b - a >= 24 && cnt >= 8 && ns < 16) { A[ns] = a; B[ns] = b; ns++; }
    }
    if (ns < 3) return 0;
    /* numpy median, cast to int32 */
    for (int i = 0; i < ns; i++) for (int j = i + 1; j < ns; j++) { if (A[j] < A[i]) { int t = A[i]; A[i] = A[j]; A[j] = t; } if (B[j] < B[i]) { int t = B[i]; B[i] = B[j]; B[j] = t; } }
    *sa = ns & 1 ? A[ns / 2] : (int)((A[ns / 2 - 1] + A[ns / 2]) / 2.0); *sb = ns & 1 ? B[ns / 2] : (int)((B[ns / 2 - 1] + B[ns / 2]) / 2.0);
    return 1;
}
static int selected_run(const uint8_t *green, int left, int right, int y) {
    if (y + 12 > 192) return 0;
    int l = left - 2 < 0 ? 0 : left - 2, r = right + 2 > 256 ? 256 : right + 2;
    for (int yy = y + 8; yy < (y + 16 > 192 ? 192 : y + 16); yy++) {
        int c = 0; for (int x = l; x < r; x++) c += green[yy * 256 + x];
        if (r > l && c >= .8 * (r - l)) return 1;
    }
    int a, b; return selected_span(green, left, right, y, &a, &b);
}

static uint8_t M_bright[192 * 256], M_white[192 * 256], M_green[192 * 256], M_strong[192 * 256], M_hudink[32 * 256], M_hudgold[32 * 256];
static uint8_t M_fg[3][192 * 256], M_dim[16][192 * 256], M_extra[3][192 * 256], M_scan[192 * 256], M_occ[192 * 256], M_cyan[192 * 256];

/* FontRenderer._recognize for one screen (rgba 256x192) */
static void recognize(int k, const uint32_t *scr, int battle) {
    TextScreen *T = &ts[k];
    battle_scan = battle;
    static uint8_t R5[192 * 256], G5[192 * 256], B5[192 * 256];
    for (int i = 0; i < 192 * 256; i++) {
        uint32_t c = scr[i]; int r = c & 255, g = (c >> 8) & 255, b = (c >> 16) & 255;
        int lo = r < g ? (r < b ? r : b) : (g < b ? g : b), hi = r > g ? (r > b ? r : b) : (g > b ? g : b), neutral = hi - lo < 8;
        M_bright[i] = lo >= 80 && neutral; M_white[i] = lo >= 232 && neutral; M_green[i] = r < 48 && g >= 48 && b < 48;
        if (i < 32 * 256) { M_hudink[i] = (g >= 232 && b >= 232 && r >= 80) || (r >= 128 && g < 64 && b < 64) || (r >= 128 && g >= 128 && b < 64)
            /* warning HP digits: the three cyan shades turned red or yellow (native_font_pixels.c) */
            || (r >= 200 && g >= 64 && abs(g - b) <= 8 && r - g >= 24) || (r >= 200 && abs(r - g) <= 8 && r - b >= 24); M_hudgold[i] = r >= 180 && g >= 64 && b < 64; }
        R5[i] = r >> 3; G5[i] = g >> 3; B5[i] = b >> 3;
        M_cyan[i] = g >= 180 && b >= 180;
        int y = i / 256, x = i % 256;
        M_scan[i] = !battle || ((y < 16 || y >= 120) && !(y >= 136 && y < 184 && x < 56));
    }
    if (battle) for (int i = 0; i < 192 * 256; i++) { M_bright[i] &= M_scan[i]; M_white[i] &= M_scan[i]; }
    int levels[32] = {0};
    for (int i = 0; i < 192 * 256; i++) {
        int n5 = R5[i] == G5[i] && G5[i] == B5[i];
        M_fg[0][i] = n5 && R5[i] == 31; M_fg[1][i] = n5 && R5[i] == 20; M_fg[2][i] = R5[i] == 31 && G5[i] == 0 && B5[i] == 0;
        if (n5) levels[R5[i]]++;
        M_strong[i] = R5[i] < 6 && G5[i] >= 24 && B5[i] < 6;
        M_extra[1][i] = R5[i] >= 10 && G5[i] < 2 && B5[i] < 2; M_extra[2][i] = R5[i] >= 10 && G5[i] >= 10 && B5[i] < 2;
    }
    int ndim = 0, dimlevel[16];
    for (int lv = 16; lv <= 30; lv++) if (lv != 20 && levels[lv] >= 24) dimlevel[ndim++] = lv;
    for (int d = 0; d < ndim; d++) for (int i = 0; i < 192 * 256; i++) M_dim[d][i] = R5[i] == G5[i] && G5[i] == B5[i] && R5[i] == dimlevel[d];
    if (battle) {
        for (int f = 0; f < 3; f++) for (int i = 0; i < 192 * 256; i++) M_fg[f][i] &= M_scan[i];
        for (int d = 0; d < ndim; d++) for (int i = 0; i < 192 * 256; i++) M_dim[d][i] &= M_scan[i];
    }
    const uint8_t *masks[8]; int nm = 0;
    for (int f = 0; f < 3; f++) {
        if (!any_mask(M_fg[f])) continue;
        int dup = 0; for (int m = 0; m < nm; m++) dup |= same_mask(masks[m], M_fg[f]);
        if (!dup) masks[nm++] = M_fg[f];
    }
    /* full and narrow */
    static Cand full[MAXC], narrow[MAXC], compact[MAXC]; int nf = 0, nn = 0, nc = 0;
    for (int m = 0; m < nm; m++) {
        nf += scan_active(masks[m], 12, 12, &T_full, 5, 100, full + nf, MAXC - nf);
        nn += scan_active(masks[m], 12, 8, &T_narrow, 1, 80, narrow + nn, MAXC - nn);
    }
    int hudany = any_mask(M_hudink) , goldany = 0; for (int i = 0; i < 32 * 256; i++) goldany |= M_hudgold[i];
    (void)hudany;
    int primary = 0; for (int i = 0; i < nf; i++) primary |= is_alnum(full[i].cp); for (int i = 0; i < nn; i++) primary |= is_alnum(narrow[i].cp);
    { int ink = 0; for (int i = 0; i < 32 * 256; i++) ink |= M_hudink[i]; primary |= ink && goldany; }
    if (!primary) {
        const uint8_t *extra2[2] = {M_bright, M_white};
        for (int e = 0; e < 2; e++) {
            if (!any_mask(extra2[e])) continue;
            int dup = 0; for (int m = 0; m < nm; m++) dup |= same_mask(masks[m], extra2[e]);
            if (dup) continue;
            masks[nm++] = extra2[e];
            nf += scan_active(extra2[e], 12, 12, &T_full, 5, 100, full + nf, MAXC - nf);
            nn += scan_active(extra2[e], 12, 8, &T_narrow, 1, 80, narrow + nn, MAXC - nn);
        }
    }
    /* HUD labels HP / EN and the digits beside them */
    static uint8_t gold192[192 * 256]; memset(gold192, 0, sizeof gold192); memcpy(gold192, M_hudgold, 32 * 256);
    static Cand labels[64]; int nl = scan(gold192, 0, 32, 16, 16, &T_label, 5, 200, labels, 64);
    ncand = 0;
    typedef struct { int x, y, w, h; uint8_t e[256]; } Eraser;
    static Eraser er[256]; int ner = 0;
    Cand *hp = NULL, *en = NULL;
    for (int i = 0; i < nl; i++) { if (labels[i].cp[0] == 'H' && labels[i].cp[1] == 'P' && !hp) hp = &labels[i]; if (labels[i].cp[0] == 'E' && labels[i].cp[1] == 'N' && !en) en = &labels[i]; }
    if (hp && en && en->x - hp->x == 128 && hp->y == en->y) {
        int y = hp->y, xs[32], nx = 0;
        for (int x = hp->x + 16; x < hp->x + 120; x += 8) xs[nx++] = x;
        for (int x = en->x + 16; x < (en->x + 80 < 249 ? en->x + 80 : 249); x += 8) xs[nx++] = x;
        int taken[32] = {0};
        for (int p = 0; p < T_hud.n; p++) {
            const uint8_t *ink = T_hud.keys + p * 32, *opq = ink + 16;
            for (int c = 0; c < nx; c++) {
                if (taken[c] || y + 16 > 32 || xs[c] + 8 > 256) continue;
                int ok = 1;
                for (int j = 0; j < 16 && ok; j++) for (int i = 0; i < 8; i++) {
                    int bit = j * 8 + i; if (!((opq[bit >> 3] >> (7 - (bit & 7))) & 1)) continue;
                    if (M_hudink[(y + j) * 256 + xs[c] + i] != ((ink[bit >> 3] >> (7 - (bit & 7))) & 1)) { ok = 0; break; }
                }
                if (!ok || ncand >= MAXC) continue;
                taken[c] = 1;
                Cand *o = &cands[ncand++]; o->x = xs[c]; o->y = y; o->w = 8; o->h = 16; memcpy(o->cp, T_hud.cp[p], sizeof o->cp);
                for (int bit = 0; bit < 128; bit++) o->ink[bit] = (ink[bit >> 3] >> (7 - (bit & 7))) & 1;
                Eraser *E = &er[ner++]; E->x = xs[c]; E->y = y; E->w = 8; E->h = 16; for (int bit = 0; bit < 128; bit++) E->e[bit] = (opq[bit >> 3] >> (7 - (bit & 7))) & 1;
            }
        }
        for (int i = 0; i < nl && ncand < MAXC; i++) {
            cands[ncand++] = labels[i];
            Eraser *E = &er[ner++]; E->x = labels[i].x; E->y = labels[i].y; E->w = 16; E->h = 16;
            for (int j = 0; j < 16; j++) for (int x = 0; x < 16; x++) {
                int v = 0; for (int dy = -2; dy <= 2 && !v; dy++) for (int dx = -2; dx <= 2 && !v; dx++) { int yy = j + dy, xx = x + dx; if (yy >= 0 && yy < 16 && xx >= 0 && xx < 16) v = labels[i].ink[yy * 16 + xx]; }
                E->e[j * 16 + x] = v;
            }
        }
    }
    /* full + narrow beside text */
    static uint8_t text_row[192]; memset(text_row, 0, sizeof text_row);
    for (int i = 0; i < nf; i++) text_row[full[i].y] = 1;
    for (int i = 0; i < nf && ncand < MAXC; i++) cands[ncand++] = full[i];
    static uint8_t posn[192 * 256];
    memset(posn, 0, sizeof posn); for (int i = 0; i < nn; i++) posn[narrow[i].y * 256 + narrow[i].x] = 1;
    for (int i = 0; i < nn && ncand < MAXC; i++) {
        int x = narrow[i].x, y = narrow[i].y, ok = text_row[y];
        for (int dx = -16; dx <= 16 && !ok; dx += 8) if (dx && x + dx >= 0 && x + dx < 256) ok = posn[y * 256 + x + dx];
        if (ok) cands[ncand++] = narrow[i];
    }
    /* compact HUD figures */
    const uint8_t *cm[12]; int ncm = 0;
    for (int m = 0; m < nm; m++) cm[ncm++] = masks[m];
    cm[ncm++] = M_bright; cm[ncm++] = M_extra[1]; cm[ncm++] = M_extra[2];
    for (int m = 0; m < ncm; m++) if (any_mask(cm[m])) nc += scan_active(cm[m], 8, 8, &T_compact, 5, 60, compact + nc, MAXC - nc);
    memset(posn, 0, sizeof posn); for (int i = 0; i < nc; i++) posn[compact[i].y * 256 + compact[i].x] = 1;
    int top_compact = 0;
    for (int i = 0; i < nc && ncand < MAXC; i++) {
        int x = compact[i].x, y = compact[i].y, ok = text_row[y];
        for (int dx = -16; dx <= 16 && !ok; dx += 8) if (dx && x + dx >= 0 && x + dx < 256) ok = posn[y * 256 + x + dx];
        if (ok) cands[ncand++] = compact[i];
        top_compact += y < 24;
    }
    /* forecast percentages (inserted first) */
    if (!battle && top_compact >= 8 && T_fore.n) {
        static Cand fc[64]; int nfc = 0;
        int spans[2][2] = {{0, 72}, {184, 256}};
        for (int s = 0; s < 2; s++) for (int p = 0; p < T_fore.n; p++) {
            const uint8_t *ink = T_fore.keys + p * 64, *opq = ink + 32;
            for (int yy = 0; yy + 16 <= 24; yy++) for (int xx = 0; spans[s][0] + xx + 16 <= spans[s][1]; xx++) {
                int x = spans[s][0] + xx, y = 76 + yy, ok = 1;
                for (int bit = 0; bit < 256 && ok; bit++) {
                    if (!((opq[bit >> 3] >> (7 - (bit & 7))) & 1)) continue;
                    if (M_cyan[(y + bit / 16) * 256 + x + bit % 16] != ((ink[bit >> 3] >> (7 - (bit & 7))) & 1)) ok = 0;
                }
                if (!ok || nfc >= 64 || ner >= 256) continue;
                Cand *o = &fc[nfc++]; o->x = x; o->y = y; o->w = 16; o->h = 16; memcpy(o->cp, T_fore.cp[p], sizeof o->cp);
                for (int bit = 0; bit < 256; bit++) o->ink[bit] = (ink[bit >> 3] >> (7 - (bit & 7))) & 1;
                Eraser *E = &er[ner++]; E->x = x; E->y = y; E->w = 16; E->h = 16; for (int bit = 0; bit < 256; bit++) E->e[bit] = (opq[bit >> 3] >> (7 - (bit & 7))) & 1;
            }
        }
        /* candidates.insert(0, ...) one by one: the last found ends first */
        if (nfc && ncand + nfc <= MAXC) {
            memmove(cands + nfc, cands, sizeof(Cand) * ncand);
            for (int i = 0; i < nfc; i++) cands[i] = fc[nfc - 1 - i];
            ncand += nfc;
        }
    }
    /* dimmed gray text */
    for (int d = 0; d < ndim; d++) {
        int dup = 0; for (int m = 0; m < nm; m++) dup |= same_mask(masks[m], M_dim[d]);
        if (dup) continue;
        static Cand df[MAXC], dnar[MAXC];
        int ndf = scan_active(M_dim[d], 12, 12, &T_full, 5, 100, df, MAXC);
        int ndn = scan_active(M_dim[d], 12, 8, &T_narrow, 1, 80, dnar, MAXC);
        static uint8_t drow[192]; memset(drow, 0, sizeof drow); for (int i = 0; i < ndf; i++) drow[df[i].y] = 1;
        memset(posn, 0, sizeof posn); for (int i = 0; i < ndn; i++) posn[dnar[i].y * 256 + dnar[i].x] = 1;
        for (int i = 0; i < ndf && ncand < MAXC; i++) cands[ncand++] = df[i];
        for (int i = 0; i < ndn && ncand < MAXC; i++) {
            int x = dnar[i].x, y = dnar[i].y, ok = drow[y];
            for (int dx = -16; dx <= 16 && !ok; dx += 8) if (dx && x + dx >= 0 && x + dx < 256) ok = posn[y * 256 + x + dx];
            if (ok) cands[ncand++] = dnar[i];
        }
    }
    /* drawable, 、 -> , , kanji and dash anchors */
    int nt = 0;
    for (int i = 0; i < ncand; i++) {
        if (cands[i].cp[0] == 0x3001 && !cands[i].cp[1]) cands[i].cp[0] = ',';
        if (drawable(cands[i].cp)) tmp[nt++] = cands[i];
    }
    static uint8_t anchor[192 * 256];
    memset(anchor, 0, sizeof anchor);
    for (int i = 0; i < nt; i++) if (is_alnum(tmp[i].cp) && !is_kanji(tmp[i].cp)) anchor[tmp[i].y * 256 + tmp[i].x] = 1;
    static const int kd[6] = {-12, -8, 8, 12, -16, 16};
    ncand = 0;
    for (int i = 0; i < nt; i++) {
        int ok = !is_kanji(tmp[i].cp);
        for (int d = 0; d < 6 && !ok; d++) { int xx = tmp[i].x + kd[d]; if (xx >= 0 && xx < 256) ok = anchor[tmp[i].y * 256 + xx]; }
        if (ok) cands[ncand++] = tmp[i];
    }
    memset(anchor, 0, sizeof anchor);
    for (int i = 0; i < ncand; i++) if (is_alnum(cands[i].cp)) anchor[cands[i].y * 256 + cands[i].x] = 1;
    nt = 0;
    for (int i = 0; i < ncand; i++) {
        uint32_t c = cands[i].cp[0]; int dash = !cands[i].cp[1] && (c == '_' || c == 0x2015 || c == 0x2501 || c == 0x2500 || c == 0x2014 || c == 0x2502 || c == 0x2503 /* hd_fonts.LINE_MARKS */
            || c == '-' || c == 0xFF0D || c == 0x2010 || c == 0x2212 || c == '`' || c == 0xFF40 || c == 0xFFE3 || c == 0x203E || c == 0x00AF || c == '~' || c == 0xFF5E), ok = !dash;
        for (int d = 0; d < 6 && !ok; d++) { int xx = cands[i].x + kd[d]; if (xx >= 0 && xx < 256) ok = anchor[cands[i].y * 256 + xx]; }
        if (ok) tmp[nt++] = cands[i];
    }
    /* accept in order, no overlap */
    memset(M_occ, 0, sizeof M_occ);
    static uint8_t ink[192 * 256]; memset(ink, 0, sizeof ink);
    T->n = 0;
    for (int i = 0; i < nt && T->n < 1024; i++) {
        Cand *c = &tmp[i]; int busy = 0;
        for (int j = 0; j < c->h && !busy; j++) for (int x = 0; x < c->w; x++) if (c->y + j < 192 && c->x + x < 256 && M_occ[(c->y + j) * 256 + c->x + x]) { busy = 1; break; }
        if (busy) continue;
        int rs = 0, gs = 0, bs = 0, cnt = 0; static int rv[256], gv[256], bv[256];
        for (int j = 0; j < c->h; j++) for (int x = 0; x < c->w; x++) {
            int p = (c->y + j) * 256 + c->x + x; if (c->y + j >= 192 || c->x + x >= 256) continue;
            M_occ[p] = 1;
            if (c->ink[j * c->w + x]) { ink[p] = 1; uint32_t q = scr[p]; rv[cnt] = q & 255; gv[cnt] = (q >> 8) & 255; bv[cnt] = (q >> 16) & 255; cnt++; }
        }
        (void)rs; (void)gs; (void)bs;
        Glyph *g = &T->g[T->n++]; g->x = c->x; g->y = c->y; g->w = c->w; g->h = c->h; g->button = 0; memcpy(g->cp, c->cp, sizeof g->cp);
        /* np.median per channel, then int() */
        int *ch[3] = {rv, gv, bv};
        for (int q = 0; q < 3; q++) {
            int *a = ch[q];
            for (int s = 1; s < cnt; s++) { int v = a[s], t = s; while (t > 0 && a[t - 1] > v) { a[t] = a[t - 1]; t--; } a[t] = v; }
            g->rgb[q] = cnt ? (cnt & 1 ? a[cnt / 2] : (int)((a[cnt / 2 - 1] + a[cnt / 2]) / 2.0)) : 255;
        }
        Held *f = &fresh[T->n - 1]; f->x = c->x; f->y = c->y; f->w = c->w; f->h = c->h; memcpy(f->cp, c->cp, sizeof f->cp); memcpy(f->ink, c->ink, sizeof f->ink);
        for (int j = 0; j < c->h; j++) for (int x = 0; x < c->w; x++) f->col[j * c->w + x] = c->y + j < 192 && c->x + x < 256 ? scr[(c->y + j) * 256 + c->x + x] : 0;
    }
    int nfresh = T->n;
    /* held glyphs: same place, unchanged ink pixels (animated button beds alter the gray masks) */
    static Held keep[1024]; int nkeep = 0;
    for (int h = 0; h < nheld[k] && T->n < 1024; h++) {
        Held *o = &held[k][h]; int ok = 1;
        for (int j = 0; j < o->h && ok; j++) for (int x = 0; x < o->w; x++) {
            int p = (o->y + j) * 256 + o->x + x;
            if (o->y + j >= 192 || o->x + x >= 256) continue;
            if (M_occ[p] || (o->ink[j * o->w + x] && scr[p] != o->col[j * o->w + x])) { ok = 0; break; }
        }
        if (!ok) continue;
        int rv[3] = {0, 0, 0};
        for (int j = 0; j < o->h; j++) for (int x = 0; x < o->w; x++) { int p = (o->y + j) * 256 + o->x + x; if (o->y + j < 192 && o->x + x < 256) { M_occ[p] = 1; if (o->ink[j * o->w + x]) ink[p] = 1; } }
        (void)rv;
        Glyph *g = &T->g[T->n++]; g->x = o->x; g->y = o->y; g->w = o->w; g->h = o->h; g->button = 0; memcpy(g->cp, o->cp, sizeof g->cp);
        /* colour: median of the held ink colours (unchanged by definition) */
        int vals[3][256], cnt = 0;
        for (int i = 0; i < o->w * o->h; i++) if (o->ink[i]) { vals[0][cnt] = o->col[i] & 255; vals[1][cnt] = (o->col[i] >> 8) & 255; vals[2][cnt] = (o->col[i] >> 16) & 255; cnt++; }
        for (int q = 0; q < 3; q++) { int *a = vals[q]; for (int s2 = 1; s2 < cnt; s2++) { int v = a[s2], t = s2; while (t > 0 && a[t - 1] > v) { a[t] = a[t - 1]; t--; } a[t] = v; }
            g->rgb[q] = cnt ? (cnt & 1 ? a[cnt / 2] : (int)((a[cnt / 2 - 1] + a[cnt / 2]) / 2.0)) : 255; }
        keep[nkeep++] = *o;
    }
    memcpy(held[k], keep, sizeof(Held) * nkeep);
    memcpy(held[k] + nkeep, fresh, sizeof(Held) * (nfresh < 1024 - nkeep ? nfresh : 1024 - nkeep));
    nheld[k] = nkeep + (nfresh < 1024 - nkeep ? nfresh : 1024 - nkeep);
    /* the glyph and only its own dark rim (3x3 neighbours with max channel <= 48), as hd_fonts.py:
     * a 5x5 box also erased the animated button gloss beside the letters and smeared it behind them */
    uint8_t *M = T->mask; memcpy(M, ink, sizeof ink);
    if (T->n) {
        for (int y = 0; y < 192; y++) for (int x = 0; x < 256; x++) {
            int p = y * 256 + x; if (ink[p]) continue;
            uint32_t c = scr[p]; int mx = c & 255; if (((c >> 8) & 255) > mx) mx = (c >> 8) & 255; if (((c >> 16) & 255) > mx) mx = (c >> 16) & 255;
            if (mx > 48) continue;
            int v = 0;
            for (int dy = -1; dy <= 1 && !v; dy++) for (int dx = -1; dx <= 1 && !v; dx++) { int yy = y + dy, xx = x + dx; if (yy >= 0 && yy < 192 && xx >= 0 && xx < 256) v = ink[yy * 256 + xx]; }
            M[p] = v;
        }
    }
    for (int e = 0; e < ner; e++) for (int j = 0; j < er[e].h; j++) for (int x = 0; x < er[e].w; x++)
        if (er[e].e[j * er[e].w + x] && er[e].y + j < 192 && er[e].x + x < 256) M[(er[e].y + j) * 256 + er[e].x + x] = 1;
    /* menu runs on 12-high lines; a selected (green) button is repaired as a whole */
    T->nrep = 0;
    static int lx[192][64], lw[192][64], ln[192], lsel[192][64];
    memset(ln, 0, sizeof ln);
    for (int i = 0; i < T->n; i++) if (T->g[i].h == 12 && ln[T->g[i].y] < 64) { int y = T->g[i].y; lx[y][ln[y]] = T->g[i].x; lw[y][ln[y]] = T->g[i].w; lsel[y][ln[y]] = 0; ln[y]++; }
    for (int y = 0; y < 192; y++) {
        int n = ln[y]; if (!n) continue;
        for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) if (lx[y][b] < lx[y][a]) { int t = lx[y][a]; lx[y][a] = lx[y][b]; lx[y][b] = t; t = lw[y][a]; lw[y][a] = lw[y][b]; lw[y][b] = t; }
        int runs[64][3], nr = 0;      /* left, right, first index */
        for (int a = 0; a < n; a++) {
            if (nr && lx[y][a] <= runs[nr - 1][1] + 8) { if (lx[y][a] + lw[y][a] > runs[nr - 1][1]) runs[nr - 1][1] = lx[y][a] + lw[y][a]; }
            else { runs[nr][0] = lx[y][a]; runs[nr][1] = lx[y][a] + lw[y][a]; runs[nr][2] = a; nr++; }
        }
        for (int r = 0; r < nr; r++) {
            int end = r + 1 < nr ? runs[r + 1][2] : n;
            if (!selected_run(M_green, runs[r][0], runs[r][1], y)) continue;
            for (int yy = (y - 2 < 0 ? 0 : y - 2); yy < (y + 14 > 192 ? 192 : y + 14); yy++)
                for (int x = (runs[r][0] - 2 < 0 ? 0 : runs[r][0] - 2); x < (runs[r][1] + 2 > 256 ? 256 : runs[r][1] + 2); x++) M[yy * 256 + x] = 1;
            for (int a = runs[r][2]; a < end; a++) lsel[y][a] = 1;
        }
        /* selected button span */
        int any = 0; for (int a = 0; a < n; a++) any |= lsel[y][a];
        if (!any) continue;
        int spans[80][2], ns = 0;
        for (int r = 0; r < nr; r++) {
            int end = r + 1 < nr ? runs[r + 1][2] : n, has = 0; for (int a = runs[r][2]; a < end; a++) has |= lsel[y][a];
            int sa, sb; if (has && ns < 80 && selected_span(M_green, runs[r][0], runs[r][1], y, &sa, &sb)) { spans[ns][0] = sa; spans[ns][1] = sb; ns++; }
        }
        for (int yy = y + 8; yy < (y + 16 > 192 ? 192 : y + 16); yy++) {
            int x = 0;
            while (x < 256) {
                if (!M_strong[yy * 256 + x]) { x++; continue; }
                int l = x; while (x < 256 && M_strong[yy * 256 + x]) x++;
                if (x - l < 12) continue;
                int hit = 0; for (int a = 0; a < n; a++) if (lsel[y][a]) { float cx = lx[y][a] + lw[y][a] / 2.f; if (l <= cx && cx < x) hit = 1; }
                if (hit && ns < 80) { spans[ns][0] = l; spans[ns][1] = x; ns++; }
            }
        }
        if (!ns) continue;
        int best = 0; for (int s = 1; s < ns; s++) if (spans[s][1] - spans[s][0] > spans[best][1] - spans[best][0]) best = s;
        int bl = spans[best][0], br = spans[best][1], mnx = 999, mxx = -1;
        for (int a = 0; a < n; a++) { float cx = lx[y][a] + lw[y][a] / 2.f; if (bl <= cx && cx < br) { lsel[y][a] = 1; if (lx[y][a] < mnx) mnx = lx[y][a]; if (lx[y][a] + lw[y][a] > mxx) mxx = lx[y][a] + lw[y][a]; } }
        if (mxx < 0) continue;
        int left = mnx - 2 < 0 ? 0 : mnx - 2, right = mxx + 2 > 256 ? 256 : mxx + 2, top = y - 2 < 0 ? 0 : y - 2, bottom = y + 14 > 192 ? 192 : y + 14;
        for (int yy = top; yy < bottom; yy++) for (int x = left; x < right; x++) M[yy * 256 + x] = 1;
        if (T->nrep < 64) { Repair *rp = &T->rep[T->nrep++]; rp->left = left; rp->top = top; rp->right = right; rp->bottom = bottom; rp->sl = bl; rp->sr = br; }
    }
    /* button flag for glyphs on selected runs */
    for (int i = 0; i < T->n; i++) if (T->g[i].h == 12) { int y = T->g[i].y; for (int a = 0; a < ln[y]; a++) if (lx[y][a] == T->g[i].x && lsel[y][a]) T->g[i].button = 1; }
}

/* FontRenderer._heal_native over one screen: rgba and argb (xBRZ input) of the same 256x192 screen */
static void heal(int k, uint32_t *rgba, uint32_t *argb) {
    TextScreen *T = &ts[k]; const uint8_t *M = T->mask;
    if (!T->n && !T->nrep) { int any = 0; for (int i = 0; i < 192 * 256 && !any; i++) any = M[i]; if (!any) return; }
    static uint32_t src[192 * 256]; memcpy(src, rgba, sizeof src);
    for (int y = 0; y < 192; y++) {
        const uint8_t *row = M + y * 256; int first = -1, last = -1;
        for (int x = 0; x < 256; x++) if (!row[x]) { if (first < 0) first = x; last = x; }
        if (first < 0) continue;
        int left = -1;
        for (int x = 0; x < 256; x++) {
            if (!row[x]) { left = x; continue; }
            int l = left < 0 ? first : left, r = x; while (r < 256 && row[r]) r++; if (r >= 256) r = last;
            uint32_t ca = src[y * 256 + l], cb = src[y * 256 + r];
            int a[3] = {ca & 255, (ca >> 8) & 255, (ca >> 16) & 255}, b[3] = {cb & 255, (cb >> 8) & 255, (cb >> 16) & 255};
            /* HEAL_SKIP_INK: a bright neutral neighbour is ink, take the other side */
            int amx = a[0] > a[1] ? (a[0] > a[2] ? a[0] : a[2]) : (a[1] > a[2] ? a[1] : a[2]), amn = a[0] < a[1] ? (a[0] < a[2] ? a[0] : a[2]) : (a[1] < a[2] ? a[1] : a[2]);
            int bmx = b[0] > b[1] ? (b[0] > b[2] ? b[0] : b[2]) : (b[1] > b[2] ? b[1] : b[2]), bmn = b[0] < b[1] ? (b[0] < b[2] ? b[0] : b[2]) : (b[1] < b[2] ? b[1] : b[2]);
            int inka = amx - amn < 24 && amn >= 150, inkb = bmx - bmn < 24 && bmn >= 150, apart = 0;
            for (int q = 0; q < 3; q++) if (abs(a[q] - b[q]) > 64) apart = 1;
            if (apart && inka && !inkb) memcpy(a, b, sizeof a); else if (apart && inkb && !inka) memcpy(b, a, sizeof b);
            double w = r != l ? (double)(x - l) / (r - l) : 0;
            int o[3]; for (int q = 0; q < 3; q++) o[q] = (int)(a[q] + (b[q] - a[q]) * w);
            rgba[y * 256 + x] = 0xff000000u | o[2] << 16 | o[1] << 8 | o[0];
        }
    }
    for (int i = 0; i < T->nrep; i++) {
        Repair *rp = &T->rep[i];
        for (int yy = rp->top; yy < rp->bottom; yy++) {
            int rv[256], gv[256], bv[256], cnt = 0;
            for (int x = rp->sl; x < rp->sr; x++) {
                uint32_t c = src[yy * 256 + x]; int r = c & 255, g = (c >> 8) & 255, b = (c >> 16) & 255;
                if (g > r + 16 && g > b + 16) { rv[cnt] = r; gv[cnt] = g; bv[cnt] = b; cnt++; }
            }
            if (cnt < 4) continue;
            int *ch[3] = {rv, gv, bv}, col[3];
            for (int q = 0; q < 3; q++) { int *a = ch[q]; for (int s = 1; s < cnt; s++) { int v = a[s], t = s; while (t > 0 && a[t - 1] > v) { a[t] = a[t - 1]; t--; } a[t] = v; }
                col[q] = cnt & 1 ? a[cnt / 2] : (int)((a[cnt / 2 - 1] + a[cnt / 2]) / 2.0); }
            for (int x = rp->left; x < rp->right; x++) if (M[yy * 256 + x]) rgba[yy * 256 + x] = 0xff000000u | col[2] << 16 | col[1] << 8 | col[0];
        }
    }
    if (argb) for (int i = 0; i < 192 * 256; i++) if (M[i]) { uint32_t c = rgba[i]; argb[i] = 0xff000000u | (c & 255) << 16 | (c & 0xff00) | ((c >> 16) & 255); }
}

/* host: after the shown frame was produced, before it is uploaded */
void hd_text_frame(uint32_t *rgba, uint32_t *argb) {
    if (!hd_active() || !text_ready) return;
    { /* debug: first time red HUD digits show in the top HUD rows, record 30 frames to files/frames_red.raw */
        static int done, left2; static FILE *rf;
        if (!done && !left2) { int red = 0; for (int i = 0; i < 32 * 256; i++) { uint32_t c = rgba[i]; if ((c & 255) >= 128 && ((c >> 8) & 255) < 64 && ((c >> 16) & 255) < 64) red++; }
            if (red >= 40) { rf = fopen("/sdcard/Android/data/kr.srww.hd/files/frames_red.raw", "wb"); left2 = 30; done = 1; LOG("red HUD seen (%d px), recording", red); } }
        if (left2 > 0 && rf) { fwrite(rgba, 4, 256 * 384, rf); if (--left2 == 0) { fclose(rf); rf = NULL; LOG("red frames recorded"); } }
    }
    { /* debug: while files/dumpframes exists, append 90 raw frames (both screens) to files/frames.raw */
        static int left = -1; static FILE *df;
        if (left < 0 && access("/sdcard/Android/data/kr.srww.hd/files/dumpframes", F_OK) == 0) { left = 90; for (int i = 0; i < 128; i++) if (parts[i][0]) { const struct Recolour *rc = recolour_of(parts[i][0]); int e = parts[i][0] <= nbind ? ent_of[parts[i][0]] : -1;
            LOG("part %d bind %u xy %u,%u bit31 %u hash %08x indexed %d tex %d", i, parts[i][0], parts[i][2] & 511, parts[i][1] & 255, parts[i][7] >> 31, parts[i][4], rc != NULL, e >= 0 ? srcs[src_of[e]].state : -1); } df = fopen("/sdcard/Android/data/kr.srww.hd/files/frames.raw", "wb"); unlink("/sdcard/Android/data/kr.srww.hd/files/dumpframes"); }
        if (left > 0 && df) { fwrite(rgba, 4, 256 * 384, df); if (--left == 0) { fclose(df); df = NULL; LOG("frames dumped"); left = -1; } }
    }
    for (int k = 0; k < 2; k++) {
        uint32_t *scr = rgba + k * 256 * 192;
        int battle = k == 0 && (hdst[0] || (bginfo[3][2] == 0x06018000 && bginfo[2][2] == 0x06010000));
        uint32_t stamp = crc32b(battle, (const uint8_t *)scr, 256 * 192 * 4);
        if (stamp != ts[k].stamp) {
            ts[k].stamp = stamp; recognize(k, scr, battle);
            { static int lastn[2] = {-1, -1}; static int logleft; if (access("/sdcard/Android/data/kr.srww.hd/files/logtext", F_OK) == 0) { logleft = 300; unlink("/sdcard/Android/data/kr.srww.hd/files/logtext"); }
              if (logleft > 0) { logleft--; uint32_t h = 0; for (int i = 0; i < ts[k].n; i++) h = h * 31 + ts[k].g[i].x * 7 + ts[k].g[i].y * 131 + ts[k].g[i].cp[0];
                if (ts[k].n != lastn[k] || 1) LOG("tx %d n %d held %d sig %08x", k, ts[k].n, nheld[k], h); lastn[k] = ts[k].n; } }
        }
        heal(k, scr, argb ? argb + k * 256 * 192 : NULL);
    }
}

/* ---- glyph atlas and drawing ---- */
#define GA 2048
static GLuint gtex, gprog; static GLint g_p, g_t, g_tex, g_col;
typedef struct { uint32_t key; int x, y, w, h; } GSlot;
static GSlot gs[4096]; static int ngs, gsx, gsy, gsh;

static void glyph_gl_init(void) {
    gprog = glCreateProgram();
    glAttachShader(gprog, sh(GL_VERTEX_SHADER, "attribute vec2 p;attribute vec2 t;varying vec2 v;void main(){v=t;gl_Position=vec4(p,0.,1.);}"));
    glAttachShader(gprog, sh(GL_FRAGMENT_SHADER,
        "precision mediump float;varying vec2 v;uniform sampler2D s;uniform vec3 c;"
        "void main(){vec4 q=texture2D(s,v);float f=q.r,a=q.a;if(a<=0.)discard;"
        "vec3 o=vec3(8.,16.,20.)/255.;gl_FragColor=vec4((c*f+o*max(a-f,0.))/a,a);}"));
    glLinkProgram(gprog);
    g_p = glGetAttribLocation(gprog, "p"); g_t = glGetAttribLocation(gprog, "t"); g_tex = glGetUniformLocation(gprog, "s"); g_col = glGetUniformLocation(gprog, "c");
    glGenTextures(1, &gtex); glBindTexture(GL_TEXTURE_2D, gtex);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR); glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE); glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_LUMINANCE_ALPHA, GA, GA, 0, GL_LUMINANCE_ALPHA, GL_UNSIGNED_BYTE, NULL);
    ngs = gsx = gsy = gsh = 0;
}

static GSlot *glyph_slot(const Glyph *g) {
    int w = g->w * S, h = g->h * S, mode = (g->h == 8 || g->h == 16 ? 1 : 0) | (g->button ? 2 : 0);
    uint32_t key = (g->cp[0] * 2654435761u) ^ (g->cp[1] * 40503u) ^ (g->cp[2] * 97u) ^ (w << 20) ^ (h << 10) ^ mode;
    for (int i = 0; i < ngs; i++) if (gs[i].key == key) return &gs[i];
    if (!jenv || !glyph_class) return NULL;
    if (gsx + w > GA) { gsy += gsh; gsx = 0; gsh = 0; }
    if (gsy + h > GA || ngs >= 4096) { ngs = gsx = gsy = gsh = 0; }      /* full: start over */
    jstring s = jstr(g->cp);
    jbyteArray arr = (*jenv)->CallStaticObjectMethod(jenv, glyph_class, m_render, s, w, h, mode);
    (*jenv)->DeleteLocalRef(jenv, s);
    if (!arr) { (*jenv)->ExceptionClear(jenv); return NULL; }
    jbyte *px = (*jenv)->GetByteArrayElements(jenv, arr, 0);
    glBindTexture(GL_TEXTURE_2D, gtex); glPixelStorei(GL_UNPACK_ALIGNMENT, 1);
    glTexSubImage2D(GL_TEXTURE_2D, 0, gsx, gsy, w, h, GL_LUMINANCE_ALPHA, GL_UNSIGNED_BYTE, px);
    (*jenv)->ReleaseByteArrayElements(jenv, arr, px, JNI_ABORT); (*jenv)->DeleteLocalRef(jenv, arr);
    GSlot *o = &gs[ngs++]; o->key = key; o->x = gsx; o->y = gsy; o->w = w; o->h = h;
    gsx += w; if (h > gsh) gsh = h;
    return o;
}

/* HD lettering over the healed native, into the bound 1024x768 target */
void hd_draw_text(int top_screen) {
    if (!hd_active() || !text_ready || !gprog) return;
    TextScreen *T = &ts[top_screen ? 0 : 1];
    if (!T->n) return;
    glUseProgram(gprog); glActiveTexture(GL_TEXTURE0); glBindTexture(GL_TEXTURE_2D, gtex); glUniform1i(g_tex, 0);
    glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glEnableVertexAttribArray(g_p); glEnableVertexAttribArray(g_t);
    for (int i = 0; i < T->n; i++) {
        Glyph *g = &T->g[i];
        GSlot *s = glyph_slot(g);
        if (!s) continue;
        glBindTexture(GL_TEXTURE_2D, gtex);
        float l = g->x / 128.f - 1, r = (g->x + g->w) / 128.f - 1, t = 1 - g->y / 96.f, b = 1 - (g->y + g->h) / 96.f;
        float u0 = s->x / (float)GA, u1 = (s->x + s->w) / (float)GA, v0 = s->y / (float)GA, v1 = (s->y + s->h) / (float)GA;
        float pv[8] = {l, b, r, b, l, t, r, t}, tv[8] = {u0, v1, u1, v1, u0, v0, u1, v0};
        glUniform3f(g_col, g->rgb[0] / 255.f, g->rgb[1] / 255.f, g->rgb[2] / 255.f);
        glVertexAttribPointer(g_p, 2, GL_FLOAT, 0, 0, pv); glVertexAttribPointer(g_t, 2, GL_FLOAT, 0, 0, tv);
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);
    }
    glDisable(GL_BLEND);
}
