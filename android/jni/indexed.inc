/* Included at the end of hd.c: palette-indexed HUD/effect parts (core 1.3) and their recolouring,
 * a port of hd_parts.PartsRenderer.sprite for bindings with dynamic_palette when the sprite's live
 * palette differs from its art (row[4] != spec.hash). Robots are never recoloured (not registered).
 *   affine rule: per channel target = a*source + b over the used slots, least squares; when the worst
 *     error is <= 34 (8-bit) the whole HD picture takes that rule (fades, flashes, red/green HUD).
 *   otherwise each HD pixel moves by the slots' source->target change, weighted 1/(d^2 + 24^2) by its
 *     colour distance to each used source slot (RECOLOUR_SMOOTH; the material anchor is not available
 *     on Android, so the weights are by colour only). */
struct Recolour { uint32_t binding, rgbhash; uint16_t used; uint8_t src[16][3], orig[16][3], has_orig; };
static struct Recolour *recol; static int nrecol;
static int *recol_of; static unsigned recol_cap;

static void indexed_init(void *core, const char *dir) {
    void (*reg)(const unsigned *, const unsigned *, unsigned) = NULL;
    *(void **)&reg = dlsym(core, "retro_srw_register_indexed_parts");
    *(void **)&c_copy_part_palettes = dlsym(core, "retro_srw_copy_part_palettes");
    char p[1200]; snprintf(p, sizeof p, "%s/indexed.pack", dir);
    FILE *in = fopen(p, "rb"); char head[8]; unsigned n = 0;
    if (!in || !reg || fread(head, 1, 8, in) != 8 || memcmp(head, "SRWHDIX1", 8) || fread(&n, 4, 1, in) != 1) { LOG("hd: no indexed pack"); if (in) fclose(in); return; }
    recol = calloc(n + 1, sizeof *recol);
    unsigned *keys = malloc(4 * (n + 1)), *ids = malloc(4 * (n + 1));
#pragma pack(push, 1)
    struct { uint32_t key, binding, rgb; uint16_t used, pad; uint8_t src[48], orig[48], has, pad2[3]; } e;
#pragma pack(pop)
    for (unsigned i = 0; i < n; i++) {
        if (fread(&e, sizeof e, 1, in) != 1) break;
        keys[nrecol] = e.key; ids[nrecol] = e.binding;
        struct Recolour *r = &recol[nrecol++]; r->binding = e.binding; r->rgbhash = e.rgb; r->used = e.used;
        memcpy(r->src, e.src, 48); memcpy(r->orig, e.orig, 48); r->has_orig = e.has;
    }
    fclose(in);
    reg(keys, ids, nrecol); free(keys); free(ids);
    recol_cap = 0; for (int i = 0; i < nrecol; i++) if (recol[i].binding > recol_cap) recol_cap = recol[i].binding;
    recol_of = malloc(sizeof(int) * (recol_cap + 1)); for (unsigned i = 0; i <= recol_cap; i++) recol_of[i] = -1;
    for (int i = 0; i < nrecol; i++) recol_of[recol[i].binding] = i;
    LOG("hd: %d indexed HUD/effect parts", nrecol);
}

static const struct Recolour *recolour_of(unsigned binding) {
    return recol_of && binding <= recol_cap && recol_of[binding] >= 0 ? &recol[recol_of[binding]] : NULL;
}

static void recolour_task(Task *k, unsigned binding, uint32_t rgbhash, const uint16_t *pal) {
    k->rmode = 0;
    const struct Recolour *r = recolour_of(binding);
    if (!r || rgbhash == r->rgbhash) return;
    float dst[16][3], src[16][3];
    for (int i = 0; i < 16; i++) {
        uint16_t c = pal[i];
        dst[i][0] = (c & 31) * 255 / 31; dst[i][1] = ((c >> 5) & 31) * 255 / 31; dst[i][2] = ((c >> 10) & 31) * 255 / 31;
        for (int q = 0; q < 3; q++) src[i][q] = r->src[i][q];
    }
    if (r->has_orig) {
        int same1 = 1, same0 = 1;
        for (int i = 0; i < 16; i++) for (int q = 0; q < 3; q++) { int eq = (int)dst[i][q] == r->orig[i][q]; if (i) same1 &= eq; same0 &= eq; }
        if (same1 || same0) return;          /* the art's own palette */
    }
    int used[15], nu = 0;
    for (int i = 1; i < 16; i++) if (r->used >> i & 1) used[nu++] = i;
    if (!nu) for (int i = 1; i < 16; i++) used[nu++] = i;
    /* affine rule per channel (least squares), worst error */
    float worst = 0, a[3], b[3];
    for (int q = 0; q < 3; q++) {
        float mn = 1e9, mx = -1e9, sx = 0, sy = 0, sxx = 0, sxy = 0;
        for (int u = 0; u < nu; u++) { float x = src[used[u]][q], y = dst[used[u]][q]; if (x < mn) mn = x; if (x > mx) mx = x; sx += x; sy += y; sxx += x * x; sxy += x * y; }
        if (mx - mn < 1) { a[q] = 0; b[q] = sy / nu; }
        else { float d = nu * sxx - sx * sx; a[q] = (nu * sxy - sx * sy) / d; b[q] = (sy - a[q] * sx) / nu; }
        for (int u = 0; u < nu; u++) { float e = fabsf(a[q] * src[used[u]][q] + b[q] - dst[used[u]][q]); if (e > worst) worst = e; }
    }
    if (worst <= 34) { k->rmode = 1; for (int q = 0; q < 3; q++) { k->ka[q] = a[q]; k->kb[q] = b[q]; } return; }
    k->rmode = 2; k->rn = nu;
    for (int u = 0; u < 15; u++) for (int q = 0; q < 3; q++) { k->rs[u][q] = u < nu ? src[used[u]][q] : 0; k->rd[u][q] = u < nu ? dst[used[u]][q] : 0; }
}
