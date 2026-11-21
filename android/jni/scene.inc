/* Included at the end of hd.c: cut-ins and battle backgrounds (scene.pack), and the per-screen draw.
 * PC references: hd_renderer.py render_top, cutin_assets.py, painted_edges.cutin_visibility,
 * hd_battle_backgrounds.py, background_color_filter.py. */
typedef struct { int id, flags, bx, by, w, h, rl, rt, rr, rb, src; } Cut;
typedef struct { int mask, w, h, src; } BGArt;
static Cut cuts[512]; static int ncut, cut_of[4096];
static BGArt bgart[512]; static int nbg; static uint16_t *refs; static uint8_t *pcol;   /* pcol: nbg x 4096 bytes, bit per RGB555 */
static void (*c_hd_state)(unsigned *), (*c_hd_layers)(unsigned *), (*c_reg_cutins)(const unsigned *, unsigned),
            (*c_reg_maps)(const unsigned *, unsigned), (*c_reg_windows)(const unsigned *, unsigned);
static unsigned hdst[12], hdl[4][12], bginfo[4][9];
static uint16_t native555[192 * 256];
static int cyan;
/* diagnostics: counted per screen frame, logged once a second */

static int scene_init(void *core, const char *dir) {
    for (int i = 0; i < 4096; i++) cut_of[i] = -1;
    *(void **)&c_hd_state = dlsym(core, "retro_srw_get_hd_state"); *(void **)&c_hd_layers = dlsym(core, "retro_srw_get_hd_layers");
    *(void **)&c_reg_cutins = dlsym(core, "retro_srw_register_cutins"); *(void **)&c_reg_maps = dlsym(core, "retro_srw_register_cutin_maps");
    *(void **)&c_reg_windows = dlsym(core, "retro_srw_register_cutin_map_windows");
    if (!c_hd_state || !c_hd_layers || !c_reg_cutins || !c_reg_maps || !c_reg_windows) { LOG("hd: core lacks cut-in API"); c_hd_state = NULL; return 0; }
    char p[1200]; snprintf(p, sizeof p, "%s/scene.pack", dir);
    int f = open(p, O_RDONLY); if (f < 0) { LOG("hd: no scene pack"); c_hd_state = NULL; return 0; }
    FILE *in = fdopen(dup(f), "rb"); char head[8]; unsigned n;
    if (!in || fread(head, 1, 8, in) != 8 || memcmp(head, "SRWHDSC1", 8)) { LOG("hd: bad scene pack"); if (in) fclose(in); c_hd_state = NULL; return 0; }
#pragma pack(push, 1)
    struct { uint32_t id, flags; int32_t bx, by; uint32_t w, h; int32_t r[4]; uint64_t off; uint32_t len; } cr;
    struct { uint32_t mask; uint16_t w, h; uint64_t off; uint32_t len; } br;
#pragma pack(pop)
    fread(&n, 4, 1, in);
    for (unsigned i = 0; i < n; i++) {
        fread(&cr, sizeof cr, 1, in);
        if (ncut >= 512 || cr.id >= 4096) continue;
        Cut *c = &cuts[ncut]; c->id = cr.id; c->flags = cr.flags; c->bx = cr.bx; c->by = cr.by; c->w = cr.w; c->h = cr.h;
        c->rl = cr.r[0]; c->rt = cr.r[1]; c->rr = cr.r[2]; c->rb = cr.r[3];
        c->src = nsrc; srcs[nsrc].fd = f; srcs[nsrc].off = cr.off; srcs[nsrc].len = cr.len; nsrc++;
        cut_of[cr.id] = ncut++;
    }
    unsigned *rows;
    fread(&n, 4, 1, in); rows = malloc(n * 20 + 4); fread(rows, 20, n, in); c_reg_cutins(rows, n); free(rows);
    fread(&n, 4, 1, in); rows = malloc(n * 8 + 4); fread(rows, 8, n, in); c_reg_maps(rows, n); free(rows);
    fread(&n, 4, 1, in); rows = malloc(n * 12 + 4); fread(rows, 12, n, in); c_reg_windows(rows, n); free(rows);
    fread(&n, 4, 1, in);
    for (unsigned i = 0; i < n; i++) {
        fread(&br, sizeof br, 1, in);
        if (nbg >= 512) continue;
        BGArt *b = &bgart[nbg++]; b->mask = br.mask; b->w = br.w; b->h = br.h; b->src = -1;
        if (br.len) { b->src = nsrc; srcs[nsrc].fd = f; srcs[nsrc].off = br.off; srcs[nsrc].len = br.len; nsrc++; }
    }
    refs = malloc((size_t)nbg * 65536 * 2); pcol = calloc((size_t)nbg, 4096);
    if (fread(refs, 2, (size_t)nbg * 65536, in) != (size_t)nbg * 65536) { LOG("hd: short references"); nbg = 0; }
    fclose(in);
    /* possible colours: every valid reference colour within one RGB555 step (background_color_filter.py) */
    static uint8_t seen[32768];
    for (int b = 0; b < nbg; b++) {
        memset(seen, 0, sizeof seen);
        const uint16_t *r = refs + (size_t)b * 65536; uint8_t *pc = pcol + (size_t)b * 4096;
        for (int i = 0; i < 65536; i++) if (r[i] & 32768) seen[r[i] & 32767] = 1;
        for (int c = 0; c < 32768; c++) if (seen[c]) {
            int cr_ = c & 31, cg = (c >> 5) & 31, cb = (c >> 10) & 31;
            for (int dr = -1; dr <= 1; dr++) for (int dg = -1; dg <= 1; dg++) for (int db = -1; db <= 1; db++) {
                int rr = cr_ + dr, gg = cg + dg, bb = cb + db;
                if (rr < 0 || rr > 31 || gg < 0 || gg > 31 || bb < 0 || bb > 31) continue;
                int v = rr | gg << 5 | bb << 10; pc[v >> 3] |= 1 << (v & 7);
            }
        }
    }
    if (cut_of[1] >= 0) ask(cuts[cut_of[1]].src);          /* id 1: the core hides its whole BG */
    LOG("hd: %d cut-ins, %d battle backgrounds", ncut, nbg);
    return 1;
}

static void scene_capture(const uint32_t *rgba) {
    if (!c_hd_state) return;
    c_hd_state(hdst); c_hd_layers(&hdl[0][0]);
    for (int l = 0; l < 4; l++) c_bg_info(l, bginfo[l]);
    int cy = 0;
    for (int i = 0; i < 192 * 256; i++) {
        uint32_t c = rgba[i]; int r = c & 255, g = (c >> 8) & 255, b = (c >> 16) & 255;
        native555[i] = (r >> 3) | (g >> 3) << 5 | (b >> 3) << 10;
        if (i >= 124 * 256 && i < 132 * 256 && r < 64 && g > 96 && b > 96) cy++;
    }
    cyan = cy >= 80;
}

/* ---- battle background identification (hd_battle_backgrounds.py identify/_identify_full) ---- */
static int bg_active[4] = {-1, -1, -1, -1}, bg_dx[4], bg_dy[4], bg_failed[4] = {-99, -99, -99, -99}, tick;
typedef struct { int layer, x, y, w, h, item; } BGMatch;

static int try_candidates(const int *cand, int nc, int layer, int x, int y, int w, int h, const int *sy, const int *sx, const uint16_t *act, int ns, BGMatch *m) {
    int minimum = (int)ceil(ceil(ns * .75) * .90), keep[512], nk = 0;
    for (int c = 0; c < nc; c++) {
        const uint8_t *pc = pcol + (size_t)cand[c] * 4096; int hits = 0;
        for (int i = 0; i < ns; i++) hits += (pc[act[i] >> 3] >> (act[i] & 7)) & 1;
        if (hits >= minimum) keep[nk++] = cand[c];
    }
    if (!nk) return 0;
    static const int offs[9][2] = {{0, 0}, {1, -1}, {-1, 1}, {1, 0}, {-1, 0}, {0, 1}, {0, -1}, {1, 1}, {-1, -1}};
    int order[10][2], no = 0; order[no][0] = bg_dx[layer]; order[no][1] = bg_dy[layer]; no++;
    for (int o = 0; o < 9; o++) if (offs[o][0] != bg_dx[layer] || offs[o][1] != bg_dy[layer]) { order[no][0] = offs[o][0]; order[no][1] = offs[o][1]; no++; }
    for (int o = 0; o < no; o++) {
        int dx = order[o][0], dy = order[o][1], best = -1; float bs = -1;
        for (int c = 0; c < nk; c++) {
            const uint16_t *R = refs + (size_t)keep[c] * 65536; int counts = 0, exact = 0, near = 0;
            for (int i = 0; i < ns; i++) {
                int rx = ((sx[i] + x + dx) % w + w) % w, ry = ((sy[i] + y + dy) % h + h) % h;
                if (rx >= 256 || ry >= 256) continue;
                uint16_t e = R[ry * 256 + rx]; if (!(e & 32768)) continue;
                counts++; e &= 32767; uint16_t a = act[i];
                exact += e == a;
                near += abs((e & 31) - (a & 31)) <= 1 && abs(((e >> 5) & 31) - ((a >> 5) & 31)) <= 1 && abs(((e >> 10) & 31) - ((a >> 10) & 31)) <= 1;
            }
            if (counts >= ns * .75 && near >= counts * .90 && exact >= counts * .60) {
                float sc = (exact + near) / (float)(counts ? counts : 1);
                if (sc > bs) { bs = sc; best = keep[c]; }
            }
        }
        if (best >= 0) {
            bg_active[layer] = best; bg_dx[layer] = dx; bg_dy[layer] = dy;
            m->layer = layer; m->x = x + dx; m->y = y + dy; m->w = w; m->h = h; m->item = best; return 1;
        }
    }
    return 0;
}

static int identify_bgs(BGMatch *out) {
    int n = 0; tick++;
    if (!nbg) return 0;
    static int where[192 * 256], cand[512];
    for (int layer = 3; layer >= 2; layer--) {
        unsigned *in = bginfo[layer]; int cnt = in[0], x = in[3], y = in[4], w = in[5], h = in[6], vis = in[7], cb = (cnt >> 2) & 15;
        if (!vis || (w != 256 && w != 512) || (h != 256 && h != 512) || cb != (layer == 3 ? 6 : 4)) continue;
        int nw = 0;
        for (int p = 0; p < 192 * 256; p++) if (ids[p] == layer) where[nw++] = p;
        if (nw < 64) continue;
        int step = nw / 96 > 1 ? nw / 96 : 1, sy[128], sx[128], ns = 0; uint16_t act[128];
        for (int i = 0; i < nw && ns < 128; i += step) { sy[ns] = where[i] / 256; sx[ns] = where[i] % 256; act[ns] = native555[where[i]]; ns++; }
        int distinct = 0; uint16_t d[3];
        for (int i = 0; i < ns && distinct < 3; i++) { int k = 0; while (k < distinct && d[k] != act[i]) k++; if (k == distinct) d[distinct++] = act[i]; }
        if (distinct < 3) continue;
        BGMatch m; int nc = 0, ok = 0;
        if (bg_active[layer] >= 0 && bgart[bg_active[layer]].src >= 0) { cand[0] = bg_active[layer]; ok = try_candidates(cand, 1, layer, x, y, w, h, sy, sx, act, ns, &m); }
        if (!ok) {
            if (tick - bg_failed[layer] < 4) continue;
            for (int b = 0; b < nbg; b++) if ((bgart[b].mask >> layer & 1) && bgart[b].src >= 0) cand[nc++] = b;
            ok = try_candidates(cand, nc, layer, x, y, w, h, sy, sx, act, ns, &m);
            if (!ok) { bg_failed[layer] = tick; bg_active[layer] = -1; continue; }
        }
        out[n++] = m;
    }
    return n;
}

/* cut-in visibility (painted_edges.cutin_visibility + foreground eligibility + window) over the task region */
static int cutin_visibility(Task *k, uint8_t *out, int stride) {
    int layer = k->item, priority = k->prio, count = 0; k->fgany = 0;
    for (int y = 0; y < k->h; y++) for (int x = 0; x < k->w; x++) {
        int p = (k->top + y) * 256 + k->left + x, L = ids[p], blocked = 0;
        if (L < 4) blocked = bgprio[L] < priority || (bgprio[L] == priority && L < layer);
        else if (L == 4 && !k->pilot) blocked = ((oam[owners[p] * 8 + 5] >> 2) & 3) <= priority;
        int v = blocked ? 0 : 255;
        if (fg_on) {
            uint64_t r = fgrec[p]; int fl = (r >> 15) & 7;
            if (fl) {
                fl -= 1;
                int targets = (r >> 32) & 31, dest = (r >> 37) & 7;
                int fprio = bgprio[fl], dprio = dest < 6 ? bgprio[dest] : 4, target = layer;
                int front = fprio < priority || (fprio == priority && fl < target);
                int behind = dest < 4 && (dprio > priority || (dprio == priority && dest > target));
                if (L == fl && ((targets >> target) & 1) && front && (dest == target || dest == 5 || behind)) { v = 128; k->fgany = 1; }
            }
        }
        if (win_on && !((win[p] >> layer) & 1)) v = 0;
        if (out) out[y * stride + x] = v;
        count += v != 0;
    }
    return count == 0 ? 0 : count == k->w * k->h ? 2 : 1;
}

static void prefetch_family(int ci) {
    static int last = -1; int fam = cuts[ci].flags >> 8;
    if (!fam || fam == last) return;
    last = fam;
    for (int j = ci; j < ncut; j++) if (cuts[j].flags >> 8 == fam) ask(cuts[j].src);   /* following frames first */
    for (int j = 0; j < ci; j++) if (cuts[j].flags >> 8 == fam) ask(cuts[j].src);
}

static int cutin_task(const unsigned *row, int x, int y, Task *k) {
    int ci = row[0] < 4096 ? cut_of[row[0]] : -1; if (ci < 0) return 0;
    Cut *c = &cuts[ci];
    ask(c->src); prefetch_family(ci);
    if (srcs[c->src].state != ON_GPU) { ask(c->src); return 0; }
    memset(k, 0, sizeof *k);
    k->type = 1; k->cut = ci; k->src = c->src; k->item = row[5] & 3; k->prio = row[6] & 3; k->pilot = c->flags & 1;
    k->key = (k->prio << 20) | (1 << 16) | (k->item << 4);
    float nx = -x + c->bx / (float)S, ny = -y + c->by / (float)S, fw = srcs[c->src].w / (float)S, fh = srcs[c->src].h / (float)S;
    k->dux = 1 / fw; k->dvy = 1 / fh;
    if (!place(k, nx, ny, fw, fh)) return 0;
    k->alpha = 1;
    srcs[c->src].last = frame_no;
    return 1;
}

static void quad(Task *k) {
    float xs[2] = {k->x0, k->x1}, ys[2] = {k->y0, k->y1}, pv[8], tv[8], mv[8];
    int order[4][2] = {{0, 1}, {1, 1}, {0, 0}, {1, 0}};      /* strip: bottom-left, bottom-right, top-left, top-right */
    for (int q = 0; q < 4; q++) {
        float nx = xs[order[q][0]], ny = ys[order[q][1]], dx = nx - k->x0, dy = ny - k->y0;
        pv[q * 2] = nx / 128.f - 1; pv[q * 2 + 1] = 1 - ny / 96.f;
        tv[q * 2] = k->u0 + k->dux * dx + k->duy * dy; tv[q * 2 + 1] = k->v0 + k->dvx * dx + k->dvy * dy;
        mv[q * 2] = (k->mx + nx - k->left) / MW; mv[q * 2 + 1] = (k->my + ny - k->top) / MH;
    }
    glBindTexture(GL_TEXTURE_2D, srcs[k->src].tex);
    glUniform1f(u_use, k->state == 3 ? 0.f : 1.f); glUniform1f(u_alpha, k->alpha); glUniform2f(u_bright, k->bmode, k->bamt);
    glUniform1f(u_rmode, k->rmode);
    if (k->rmode == 1) { glUniform3fv(u_ka, 1, k->ka); glUniform3fv(u_kb, 1, k->kb); }
    if (k->rmode == 2) { glUniform1f(u_rn, k->rn); glUniform3fv(u_rs, 15, &k->rs[0][0]); glUniform3fv(u_rd, 15, &k->rd[0][0]); }
    glVertexAttribPointer(a_p, 2, GL_FLOAT, 0, 0, pv); glVertexAttribPointer(a_t, 2, GL_FLOAT, 0, 0, tv);
    glVertexAttribPointer(a_m, 2, GL_FLOAT, 0, 0, mv);
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);
}

static Task bgt[16], pilots[64];
static Task *all[128 + 3200 + 64 + 64 + 16];
static uint8_t keep_ids[192 * 256];

/* draw the HD pictures of one screen into the bound 1024x768 target (render_top / render_bottom).
 * Sort key: priority<<20 | kind<<16 | item<<4 | sub (sub 1 = BG tile, before the cut-in of the same layer). */
int hd_draw(int top_screen) {
    if (!hd_active()) return 0;
    int nb = 0, np = 0, n = 0, restored = 0, restore_layer = -1, band = 0;
    if (top_screen && c_hd_state) {
        unsigned planes[4][12]; int nplanes = 0;
        if (hdst[0]) { memcpy(planes[0], hdst, sizeof hdst); nplanes = 1; }
        int nl = 0; unsigned lr[4][12];
        for (int l = 0; l < 4; l++) if (hdl[l][0] && hdl[l][0] < 4096 && cut_of[hdl[l][0]] >= 0) memcpy(lr[nl++], hdl[l], sizeof lr[0]);
        if (nl) {                                    /* back to front: (priority, layer) descending */
            for (int a = 0; a < nl; a++) for (int b = a + 1; b < nl; b++) {
                unsigned ka = lr[a][6] * 8 + lr[a][5], kb = lr[b][6] * 8 + lr[b][5];
                if (kb > ka) { unsigned t[12]; memcpy(t, lr[a], sizeof t); memcpy(lr[a], lr[b], sizeof t); memcpy(lr[b], t, sizeof t); }
            }
            memcpy(planes, lr, sizeof lr[0] * nl); nplanes = nl;
        }
        int battle = hdst[0] || (bginfo[3][2] == 0x06018000 && bginfo[2][2] == 0x06010000);
        band = battle && cyan;
        BGMatch bm[2]; int nm = identify_bgs(bm);
        if (hdst[0] > 1 && nplanes) {
            /* restoration: native cut-in pixels become the backdrop layer behind (renderer.py 165-188) */
            int minp = 9; for (int i = 0; i < nplanes; i++) if ((int)planes[i][6] < minp) minp = planes[i][6];
            int behind[4], nbh = 0; for (int l = 0; l < 4; l++) if (bgprio[l] > minp) behind[nbh++] = l;
            if (nbh) {
                int best = -1, bk = -1;
                for (int pass = 0; pass < 2 && best < 0; pass++)
                    for (int i = 0; i < nbh; i++) {
                        int l = behind[i], known = 0;
                        for (int m = 0; m < nm; m++) known |= bm[m].layer == l;
                        if (pass == 0 && !known) continue;
                        int key = bgprio[l] * 8 + l; if (key > bk) { bk = key; best = l; }
                    }
                restore_layer = best;
                memcpy(keep_ids, ids, sizeof ids);
                for (int i = 0; i < nplanes; i++) {
                    if (planes[i][0] <= 1) continue;
                    int lay = planes[i][5], ci = planes[i][0] < 4096 ? cut_of[planes[i][0]] : -1;
                    int x = planes[i][1], y = planes[i][2]; if (x >= 256) x -= 512; if (y >= 256) y -= 512;
                    int rect = ci >= 0 && (cuts[ci].flags & 4);
                    for (int p = 0; p < 192 * 256; p++) {
                        if (keep_ids[p] != lay) continue;
                        if (rect) {
                            int xx = p % 256, yy = p / 256; Cut *c = &cuts[ci];
                            if (xx < c->rl - x || xx >= c->rr - x || yy < c->rt - y || yy >= c->rb - y) continue;
                        }
                        ids[p] = restore_layer; restored = 1;
                    }
                }
                if (!restored) restore_layer = -1;
            }
        }
        for (int m = 0; m < nm; m++) {                /* battle backgrounds, 2x2 wrap at the hardware period */
            BGArt *a = &bgart[bm[m].item];
            if (srcs[a->src].state != ON_GPU) { ask(a->src); continue; }
            srcs[a->src].last = frame_no;
            int w = bm[m].w, h = bm[m].h, px = ((bm[m].x % w) + w) % w, py = ((bm[m].y % h) + h) % h;
            for (int ox = 0; ox < 2; ox++) for (int oy = 0; oy < 2; oy++) {
                if (nb >= 16) continue;
                Task *k = &bgt[nb]; memset(k, 0, sizeof *k);
                k->type = 2; k->src = a->src; k->item = bm[m].layer; k->alpha = 1; k->dux = 1.f / a->w; k->dvy = 1.f / a->h;
                if (place(k, ox ? w - px : -px, oy ? h - py : -py, a->w, a->h)) nb++;
            }
        }
        for (int i = 0; i < nplanes; i++) {           /* cut-ins: pilots go above everything, others join the parts order */
            int ci = planes[i][0] < 4096 ? cut_of[planes[i][0]] : -1; if (ci < 0) continue;
            int lay = planes[i][5] & 3, rep = (cuts[ci].flags & 2) && bginfo[lay][5] == 256 && bginfo[lay][6] == 256;
            int xs[2], ys[2], cnt = rep ? 2 : 1;
            if (rep) { xs[0] = planes[i][1] % 256; xs[1] = xs[0] - 256; ys[0] = planes[i][2] % 256; ys[1] = ys[0] - 256; }
            else { xs[0] = planes[i][1]; ys[0] = planes[i][2]; if (xs[0] >= 256) xs[0] -= 512; if (ys[0] >= 256) ys[0] -= 512; }
            for (int a = 0; a < cnt; a++) for (int b = 0; b < cnt; b++) {
                int pilot = cuts[ci].flags & 1;
                Task *k = pilot ? (np < 64 ? &pilots[np] : NULL) : &tasks[n];
                if (!k || !cutin_task(planes[i], xs[a], ys[b], k)) continue;
                if (pilot) np++; else n++;
            }
        }
    }
    uint32_t (*P)[8] = top_screen ? parts : sparts;
    for (int i = 0; i < 128; i++) if (P[i][0] && obj_task(top_screen, i, P[i], &tasks[n])) {
        Task *k = &tasks[n++]; k->key = ((k->key >> 16) << 20) | ((k->key & 0xfff) << 4);
    }
    if (top_screen)
        for (int l = 0; l < 4; l++)
            for (int r = l * 800; r < l * 800 + 800 && bgparts[r][0]; r++) if (bg_task(bgparts[r], &tasks[n])) {
                Task *k = &tasks[n++]; k->key = ((k->key >> 16) << 20) | (1 << 16) | ((k->key & 0xfff) << 4) | 1;
            }
    if (n) qsort(tasks, n, sizeof(Task), cmp);
    shelf_x = shelf_y = shelf_h = 0;
    int any_fg = 0, na = 0;
    for (int i = 0; i < nb; i++) all[na++] = &bgt[i];
    for (int i = 0; i < n; i++) all[na++] = &tasks[i];
    for (int i = 0; i < np; i++) all[na++] = &pilots[i];
    for (int t = 0; t < na; t++) {
        Task *k = all[t];
        if (k->type == 2) {                           /* layer pixels (+ restoration) & window, art alpha */
            if (!mask_alloc(k->w, k->h, &k->mx, &k->my)) { k->state = 0; continue; }
            int cnt = 0;
            for (int y = 0; y < k->h; y++) for (int x = 0; x < k->w; x++) {
                int p = (k->top + y) * 256 + k->left + x;
                int v = (restored ? keep_ids[p] : ids[p]) == k->item || (restored && k->item == restore_layer && ids[p] == restore_layer);
                if (win_on && !((win[p] >> k->item) & 1)) v = 0;
                maskbuf[(k->my + y) * MW + k->mx + x] = v ? 255 : 0; cnt += v;
            }
            k->state = cnt ? 1 : 0; continue;
        }
        if (k->type == 1) {
            k->state = cutin_visibility(k, NULL, 0);
            if (!k->state) continue;
            if (!fg_on && k->state == 2) { k->state = 3; continue; }
            if (!mask_alloc(k->w, k->h, &k->mx, &k->my)) { k->state = 3; continue; }
            k->state = cutin_visibility(k, maskbuf + k->my * MW + k->mx, MW);
            if (k->fgany) any_fg = 1; else if (k->state == 2) k->state = 3;
            continue;
        }
        int kind = k->mx >> 16 & 1, priority = k->mx >> 8 & 3, item = k->mx & 255;
        int semi = k->alpha < 1;
        if (k->state == 2 && !semi && !(top_screen && fg_on)) { k->state = 3; continue; }   /* no mask needed */
        if (!mask_alloc(k->w, k->h, &k->mx, &k->my)) { k->state = 3; continue; }
        k->state = visibility(top_screen, k, priority, kind, item, k->ctl, maskbuf + k->my * MW + k->mx, MW);
        if (k->fgany) any_fg = 1;
        if (k->state == 2 && !k->fgany && !semi) k->state = 3;
    }
    if (restored) memcpy(ids, keep_ids, sizeof ids);
    if (!na) return band;
    glUseProgram(prog);
    glActiveTexture(GL_TEXTURE1); glBindTexture(GL_TEXTURE_2D, masktex);
    if (shelf_y + shelf_h > 0) { glPixelStorei(GL_UNPACK_ALIGNMENT, 1); glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, MW, shelf_y + shelf_h, GL_ALPHA, GL_UNSIGNED_BYTE, maskbuf); }
    glActiveTexture(GL_TEXTURE2); glBindTexture(GL_TEXTURE_2D, fgtex);
    if (any_fg) {
        for (int p = 0; p < 192 * 256; p++) {
            uint64_t r = fgrec[p]; uint8_t *o = fgplane + p * 4;
            if ((r >> 15) & 7) {
                int c = r & 0x7fff, eva = (r >> 18) & 31, evb = (r >> 23) & 31;
                o[0] = (((c & 31) * 255 + 15) / 31 * eva) / 16; o[1] = ((((c >> 5) & 31) * 255 + 15) / 31 * eva) / 16;
                o[2] = ((((c >> 10) & 31) * 255 + 15) / 31 * eva) / 16; o[3] = evb;
            } else { o[0] = o[1] = o[2] = 0; o[3] = 16; }
        }
        glPixelStorei(GL_UNPACK_ALIGNMENT, 4);
        glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, 256, 192, GL_RGBA, GL_UNSIGNED_BYTE, fgplane);
    }
    glUniform1i(u_art, 0); glUniform1i(u_mask, 1); glUniform1i(u_fg, 2);
    glActiveTexture(GL_TEXTURE0);
    glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glEnableVertexAttribArray(a_p); glEnableVertexAttribArray(a_t); glEnableVertexAttribArray(a_m);
    for (int t = 0; t < na; t++) if (all[t]->state) quad(all[t]);
    glDisableVertexAttribArray(a_m);
    glDisable(GL_BLEND);
    return band;
}
