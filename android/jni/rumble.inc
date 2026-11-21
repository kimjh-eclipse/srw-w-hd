/* Included at the end of hd.c: battle rumble, a port of the PC player
 * (emulator/battle_rumble.py, beam_rumble.py, background_rumble.py). Native data only, independent of HD.
 * After every emulated frame: battle active (RAM 0x0a6f38 == 128 and 0x1e7a10 == 0) ->
 *   impact flash (an OBJ palette bank in use brightens), background explosion / white flash,
 *   energy orb, beam stream. The event (low, high, duration ms) is handed to Java for the pad. */
static void *(*c_mem)(unsigned);
static unsigned (*c_effect_debug)(void *, void *, void *, void *);
static int (*c_vram)(unsigned, void *, unsigned);
static uint8_t *ram;

static uint16_t r_oam[128][4], r_pal[16][16], r_bgpal[16][16], r_regs[64];
static int r_age, r_tick, r_last_hit, r_last_beam, r_last_energy, r_was_active, r_engine;
static float r_prev_light[16]; static int r_have_prev;
static int r_beam_visible, r_orb_changed, r_bg_visible; static uint32_t r_last_orb_token, r_orb_token; static int r_orb_active, r_have_orb_token;
/* background observer */
static uint32_t bgo_stamp[4][4]; static int bgo_count[4], bgo_have[4], bgo_flash_have, bgo_flash[2];
/* pending event for Java */
static float ev_low, ev_high; static int ev_duration = -1, ev_beam;

static void rumble_reset(void) {
    r_have_prev = 0; r_age = 0; r_tick = 0; r_last_hit = -100; r_last_beam = -100; r_was_active = 0; r_last_energy = -100;
    r_have_orb_token = 0; r_orb_changed = 0; r_bg_visible = 0; r_beam_visible = 0;
    memset(bgo_have, 0, sizeof bgo_have); bgo_flash_have = 0;
}

static void rumble_init(void *core) {
    *(void **)&c_mem = dlsym(core, "retro_get_memory_data");
    *(void **)&c_effect_debug = dlsym(core, "retro_srw_copy_effect_debug");
    *(void **)&c_vram = dlsym(core, "retro_srw_copy_vram");
    for (uint32_t i = 0; i < 256; i++) { uint32_t c = i; for (int j = 0; j < 8; j++) c = (c >> 1) ^ ((c & 1) ? 0xedb88320u : 0); crctab[i] = c; }
    rumble_reset();
    LOG("hd: battle rumble %s", c_mem && c_effect_debug && c_vram ? "ready" : "unavailable");
}

static void emit(float low, float high, int duration, int beam) {
    ev_low = low; ev_high = high; ev_duration = duration; ev_beam = beam;
}

/* BeamObserver.energy_table for one 16-colour bank (or 256 for 8bpp) */
static void energy_table(const uint16_t *p, int n, uint8_t *out) {
    for (int i = 0; i < n; i++) {
        int r = p[i] & 31, g = (p[i] >> 5) & 31, b = (p[i] >> 10) & 31;
        out[i] = (g >= 24 && g >= r + 5 && g + 5 >= b) || (g >= 25 && b >= 25 && r <= 19) || (b >= 27 && r <= 18 && g >= 15)
              || (r >= 28 && g >= 27 && b <= 19) || (r >= 27 && b >= 27 && g <= 18) || (r >= 28 && g <= 22 && b <= 18) || (r >= 28 && g >= 28 && b >= 28);
    }
}

typedef struct { int xmin, xmax, ymin, ymax, count; } Box;
static void box_of(const uint8_t *mask, int w, int h, Box *bx) {
    bx->xmin = w; bx->xmax = -1; bx->ymin = h; bx->ymax = -1; bx->count = 0;
    for (int y = 0; y < h; y++) for (int x = 0; x < w; x++) if (mask[y * w + x]) {
        bx->count++; if (x < bx->xmin) bx->xmin = x; if (x > bx->xmax) bx->xmax = x; if (y < bx->ymin) bx->ymin = y; if (y > bx->ymax) bx->ymax = y;
    }
}
static int sat(uint16_t c) { int r = c & 31, g = (c >> 5) & 31, b = (c >> 10) & 31, mx = r > g ? (r > b ? r : b) : (g > b ? g : b), mn = r < g ? (r < b ? r : b) : (g < b ? g : b); return mx - mn; }

/* classify, classify_orb, classify_white_orb on decoded indices (w x h) */
static void classify_all(const uint8_t *ind, int w, int h, const uint16_t *pal, int npal, int *beam, int *orb, int *white_orb) {
    static uint8_t lut[256], mask[64 * 64 * 4], wm[64 * 64 * 4];
    energy_table(pal, npal, lut); lut[0] = 0;
    int n = w * h, opaque = 0;
    for (int i = 0; i < n; i++) { mask[i] = lut[ind[i]]; opaque += ind[i] != 0; }
    Box b; box_of(mask, w, h, &b);
    *beam = 0; *orb = 0; *white_orb = 0;
    int width = b.count ? b.xmax - b.xmin + 1 : 0, height = b.count ? b.ymax - b.ymin + 1 : 0;
    /* classify */
    if (b.count >= 24 && width >= 10) {
        int green = 0, nsat = 0, rowmax = 0;
        for (int y = 0; y < h; y++) { int rc = 0; for (int x = 0; x < w; x++) rc += mask[y * w + x]; if (rc > rowmax) rowmax = rc; }
        for (int i = 0; i < n; i++) if (mask[i]) {
            uint16_t c = pal[ind[i]]; int r = c & 31, g = (c >> 5) & 31, bb = (c >> 10) & 31;
            green += g >= 25 && r <= 18 && bb <= 25; nsat += sat(c) >= 8;
        }
        int stream = width >= (18 > height * 2.5 ? 18 : height * 2.5) && rowmax >= 12;
        if (nsat < 24) stream = width >= (24 > height * 4 ? 24 : height * 4) && b.count >= opaque * .8;
        *beam = stream || (green >= (24 > opaque * .55 ? 24 : opaque * .55) && width >= 10 && width <= 24 && height >= 4 && height <= 24);
    }
    /* classify_white_orb */
    {
        for (int i = 0; i < n; i++) { uint16_t c = pal[ind[i]]; wm[i] = ind[i] && (c & 31) >= 28 && ((c >> 5) & 31) >= 28 && ((c >> 10) & 31) >= 28; }
        Box wb; box_of(wm, w, h, &wb);
        if (wb.count >= 120) {
            int ww = wb.xmax - wb.xmin + 1, wh = wb.ymax - wb.ymin + 1; float fill = wb.count / (float)(ww * wh), ratio = ww / (float)wh;
            *white_orb = (ww < wh ? ww : wh) >= 16 && ratio >= .7f && ratio <= 1.4f && fill >= .5f && fill <= .88f && wb.count >= opaque * .85;
        }
    }
    /* classify_orb */
    if (b.count >= 80 && (width < height ? width : height) >= 12 && (width > height ? width : height) <= (width < height ? width : height) * 2.5) {
        int colored = 0;
        for (int i = 0; i < n; i++) if (mask[i] && sat(pal[ind[i]]) >= 7) colored++;
        *orb = b.count >= width * height * .3 && (colored >= 32 || *white_orb);
    }
}

/* BeamObserver.active */
static uint32_t bcache_key[96]; static uint8_t bcache_val[96]; static int bcache_n, bcache_next;
static int beams_active(void) {
    r_orb_active = 0;
    static const int WS[3][4] = {{8, 16, 32, 64}, {16, 32, 32, 64}, {8, 8, 16, 32}}, HS[3][4] = {{8, 16, 32, 64}, {8, 8, 16, 32}, {16, 32, 32, 64}};
    uint32_t disp = r_regs[0] | (uint32_t)r_regs[1] << 16; int one_d = (disp & 16) != 0, boundary = one_d ? 5 + ((disp >> 20) & 3) : 5;
    uint8_t banks[16] = {0}, lut[16]; int anybank = 0;
    for (int k = 0; k < 16; k++) { energy_table(r_pal[k], 16, lut); lut[0] = 0; for (int i = 1; i < 16; i++) banks[k] |= lut[i]; anybank |= banks[k]; }
    static uint8_t raw[8192], ind[64 * 64];
    for (int idx = 0; idx < 128; idx++) {
        int a = r_oam[idx][0], b = r_oam[idx][1], c = r_oam[idx][2], shape = a >> 14, size = b >> 14;
        if (shape == 3 || ((a >> 10) & 3) >= 2 || (!(a & 256) && (a & 512))) continue;
        int x = b & 511, y = a & 255; if (x >= 256) x -= 512; if (y >= 192) y -= 256;
        int w = WS[shape][size], h = HS[shape][size];
        if (x >= 256 || y >= 120 || x + w * 2 <= 0 || y + h * 2 <= 0) continue;
        int eight = (a & 8192) != 0;
        if (eight && (disp & 0x80000000u)) continue;
        if (!(eight ? anybank : banks[c >> 12])) continue;
        const uint16_t *colors = eight ? &r_pal[0][0] : r_pal[c >> 12]; int npal = eight ? 256 : 16;
        int tile_bytes = eight ? 64 : 32, stride = one_d ? w / 8 * tile_bytes : 1024, length = (h / 8 - 1) * stride + w / 8 * tile_bytes;
        unsigned base = (r_engine ? 0x06600000u : 0x06400000u) + ((unsigned)(c & 1023) << boundary);
        if (length > (int)sizeof raw || !c_vram(base, raw, length)) continue;
        uint32_t key = crc32b(crc32b(w * 131 + h * 7 + eight, raw, length), (const uint8_t *)colors, npal * 2);
        int found = -1;
        for (int i = 0; i < bcache_n; i++) if (bcache_key[i] == key) { found = bcache_val[i]; break; }
        if (found < 0) {
            for (int ty = 0; ty < h / 8; ty++) for (int tx = 0; tx < w / 8; tx++) for (int py = 0; py < 8; py++) for (int px = 0; px < 8; px++) {
                const uint8_t *t = raw + ty * stride + tx * tile_bytes; int v;
                if (eight) v = t[py * 8 + px]; else { uint8_t pb = t[py * 4 + px / 2]; v = px & 1 ? pb >> 4 : pb & 15; }
                ind[(ty * 8 + py) * w + tx * 8 + px] = v;
            }
            int beam, orb, white; classify_all(ind, w, h, colors, npal, &beam, &orb, &white);
            found = beam | orb << 1 | white << 2;
            bcache_key[bcache_next] = key; bcache_val[bcache_next] = found; bcache_next = (bcache_next + 1) % 96; if (bcache_n < 96) bcache_n++;
        }
        if ((((a >> 10) & 3) == 1 && (found & 2)) || (found & 4)) { r_orb_active = 1; r_orb_token = key * 31u + idx; }
        if (found & 1) return 1;
    }
    return 0;
}

/* BackgroundEnergyObserver.sample */
static int background_sample(void) {
    int cnt = r_regs[0x50 / 2], fade = ((cnt >> 6) & 3) == 2 ? ((r_regs[0x54 / 2] & 31) > 16 ? 16 : r_regs[0x54 / 2] & 31) : 0;
    int master = r_regs[0x6c / 2], white = (master >> 14) == 1 ? ((master & 31) > 16 ? 16 : master & 31) : 0;
    int event = bgo_flash_have && (fade - bgo_flash[0] >= 3 || white - bgo_flash[1] >= 3);
    bgo_flash[0] = fade; bgo_flash[1] = white; bgo_flash_have = 1;
    static uint8_t maps[8192], tiles[65536];
    static uint16_t indices[30][64]; static uint8_t mk[30][64];
    for (int layer = 1; layer < 4; layer++) {
        unsigned *in = bginfo[layer];
        if (!in[7] || (in[5] != 256 && in[5] != 512) || (in[6] != 256 && in[6] != 512)) continue;
        int eight = (in[0] & 128) != 0, tile_bytes = eight ? 65536 : 32768, map_bytes = in[5] * in[6] / 32;
        if (!c_vram(in[1], maps, map_bytes) || !c_vram(in[2], tiles, tile_bytes)) continue;
        uint32_t s0 = crc32b(0, maps, map_bytes), s1 = crc32b(0, tiles, tile_bytes), s2 = crc32b(0, (const uint8_t *)r_bgpal, 512);
        if (bgo_have[layer] && bgo_stamp[layer][0] == s0 && bgo_stamp[layer][1] == s1 && bgo_stamp[layer][2] == s2) continue;
        const uint16_t *pal = &r_bgpal[0][0]; uint8_t lut[256]; energy_table(pal, 256, lut); lut[0] = 0;
        uint8_t used[256] = {0}; int count = 0;
        for (int j = 0; j < 30; j++) for (int i = 0; i < 64; i++) {
            int gx = (2 + i * 4 + in[3]) % in[5], gy = (2 + j * 4 + in[4]) % in[6];
            int address = ((gy / 256) * (in[5] / 256) + gx / 256) * 1024 + (gy % 256 / 8) * 32 + gx % 256 / 8;
            uint16_t e = maps[address * 2] | maps[address * 2 + 1] << 8;
            int px = gx % 8, py = gy % 8; if (e & 1024) px = 7 - px; if (e & 2048) py = 7 - py;
            int tile = e & 1023, pixel = py * 8 + px, v;
            if (eight) v = tiles[(tile * 64 + pixel) % 65536];
            else { uint8_t pk = tiles[(tile * 32 + pixel / 2) % 32768]; int local = pixel & 1 ? pk >> 4 : pk & 15; v = local ? local + (e >> 12) * 16 : 0; }
            indices[j][i] = v; mk[j][i] = lut[v & 255]; count += mk[j][i]; used[v & 255] = 1;
        }
        int dense = 0;
        if (count >= 64) {
            for (int j = 0; j + 6 <= 30 && !dense; j++) for (int i = 0; i + 6 <= 64 && !dense; i++) {
                int sum = 0; for (int dy = 0; dy < 6; dy++) for (int dx = 0; dx < 6; dx++) sum += mk[j + dy][i + dx];
                if (sum >= 26) dense = 1;
            }
        }
        uint16_t usedcol[256]; int nu = 0; for (int v = 1; v < 256; v++) if (used[v]) usedcol[nu++] = pal[v];
        uint32_t s3 = crc32b(0, (const uint8_t *)usedcol, nu * 2);
        int had = bgo_have[layer], pcount = bgo_count[layer]; uint32_t p3 = bgo_stamp[layer][3];
        bgo_stamp[layer][0] = s0; bgo_stamp[layer][1] = s1; bgo_stamp[layer][2] = s2; bgo_stamp[layer][3] = s3; bgo_count[layer] = count; bgo_have[layer] = 1;
        if (!had) continue;
        int grew = count >= pcount * 1.15 + 12, recolored = s3 != p3 && count >= pcount * .8;
        if (dense && (grew || recolored)) event = 1;
    }
    return event;
}

/* after each emulated frame (BattleRumble.sample + observe) */
static void rumble_frame(void) {
    if (!c_mem || !c_effect_debug || !c_vram) return;
    if (!ram) { ram = c_mem(2); if (!ram) return; }
    int active = *(uint32_t *)(ram + 0xa6f38) == 128 && *(uint32_t *)(ram + 0x1e7a10) == 0;
    if (!active) { if (r_was_active) emit(0, 0, 0, 0); rumble_reset(); return; }
    r_engine = (int)c_effect_debug(r_oam, r_pal, r_bgpal, r_regs) - 1; if (r_engine < 0) r_engine = 0;
    for (int l = 0; l < 4; l++) c_bg_info(l, bginfo[l]);   /* fresh layout even when HD is off */
    if (r_tick % 2 == 0) {
        r_beam_visible = beams_active();
        r_orb_changed = r_orb_active && (!r_have_orb_token || r_orb_token != r_last_orb_token);
        r_last_orb_token = r_orb_token; r_have_orb_token = r_orb_active;
        r_bg_visible = background_sample();
    }
    r_was_active = 1; r_age++; r_tick++;
    float light[16];
    for (int k = 0; k < 16; k++) { float s = 0; for (int i = 1; i < 16; i++) { uint16_t c = r_pal[k][i]; s += (c & 31) + ((c >> 5) & 31) + ((c >> 10) & 31); } light[k] = s / 45.f; }
    int had = r_have_prev; float prev[16]; memcpy(prev, r_prev_light, sizeof prev); memcpy(r_prev_light, light, sizeof light); r_have_prev = 1;
    if (!had || r_age < 30) return;
    int used[16] = {0};
    for (int i = 0; i < 128; i++) {
        int a = r_oam[i][0], b = r_oam[i][1], c = r_oam[i][2], y = a & 255, x = b & 511;
        if ((a & 0x300) != 0x200 && (a >> 14) != 3 && ((a >> 10) & 3) < 2 && y < 120 && (x < 256 || x > 448)) used[c >> 12] = 1;
    }
    int pulse = 0;
    for (int k = 0; k < 16; k++) if (used[k] && light[k] >= 25 && prev[k] >= 5 && light[k] - prev[k] >= 5) pulse = 1;
    if (pulse && r_tick - r_last_hit >= 5) {
        int repeated = r_tick - r_last_hit <= 24; r_last_hit = r_tick;
        emit(repeated ? .9f : 1.f, 1.f, repeated ? 95 : 155, 0); return;
    }
    if (r_bg_visible && r_tick - r_last_energy >= 8) { r_last_energy = r_tick; r_last_hit = r_tick; emit(1, 1, 180, 0); return; }
    if (r_orb_changed && r_tick - r_last_hit >= 6 && r_tick - r_last_energy >= 6) { r_last_energy = r_tick; emit(.85f, 1, 125, 0); return; }
    if (r_beam_visible && r_tick - r_last_hit >= 8 && r_tick - r_last_beam >= 4) {
        r_last_beam = r_tick; emit((r_tick / 4) % 2 ? .9f : .65f, 1, 110, 1); return;
    }
}

/* Java: out = {low, high, beam}; returns duration ms, 0 = stop, -1 = nothing new */
int hd_take_rumble(float *out) {
    int d = ev_duration; if (d < 0) return -1;
    out[0] = ev_low; out[1] = ev_high; out[2] = ev_beam; ev_duration = -1; return d;
}
