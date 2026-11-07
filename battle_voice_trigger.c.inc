/* Battle-only prototype for the verified Korean 1.0.8 revision.
 * The scenario-script pointer, battle display allocation and caption screen
 * flags distinguish animation captions from map/story dialogue. */
__attribute__((used)) volatile u32 voice_glyph_calls;
__attribute__((used)) volatile u32 voice_match_count;
__attribute__((used)) volatile u32 voice_last_pointer;
__attribute__((used)) volatile u32 voice_battle_count;
__attribute__((used)) volatile u32 voice_ignored_map_frames;
__attribute__((used)) volatile u32 voice_ignored_speaker_frames;
__attribute__((used)) volatile u32 voice_seen;
static u32 voice_was_battle;
__attribute__((used)) volatile u32 voice_last_quote_hash;

__attribute__((used)) void voice_glyph_probe(const void *context)
{
    static const u8 kazuma_name[] = {0x92,0xa9,0x91,0x8e,0x8c,0xb4,0x00};
    const volatile u8 *name = (const volatile u8 *)0x021f7238u;
    const volatile u8 *caption = (const volatile u8 *)0x021f7338u;
    u32 battle_allocation = *(volatile u32 *)0x020a6f38u;
    u32 scenario_node = *(volatile u32 *)0x021e7a10u;
    u32 screen_flags = *(volatile u32 *)0x021f729cu;
    u32 i, line, hash;
    (void)context;
    voice_glyph_calls++;
    if (battle_allocation != 0x80u || scenario_node != 0u) {
        voice_ignored_map_frames++;
        if (playing) stream_stop();
        voice_seen = 0u;
        voice_was_battle = 0u;
        voice_last_quote_hash = 0u;
        return;
    }
    if (!voice_was_battle) {
        voice_was_battle = 1u;
        voice_battle_count++;
    }
    /* The previous map caption remains in RAM during the loading fade.
     * Wait for the actual main-screen animation caption rather than that copy. */
    if ((screen_flags & 0x8000u) != 0u) return;
    if (caption[0] != 0x81u || caption[1] != 0x75u) return;
    for (i=0u; i<sizeof(kazuma_name); ++i) {
        if (name[i] != kazuma_name[i]) {
            voice_ignored_speaker_frames++;
            if (playing) stream_stop();
            voice_last_quote_hash = 0u;
            return;
        }
    }
    /* Identify the full displayed quote, not one hardcoded sentence.
     * Text rows are zero-terminated and 0x100 bytes apart. */
    hash = 2166136261u;
    for (line=0u; line<3u; ++line) {
        for (i=0u; i<0x100u; ++i) {
            u32 value = caption[line*0x100u+i];
            if (!value) break;
            hash = (hash ^ value) * 16777619u;
        }
        hash = (hash ^ 0xffu) * 16777619u;
    }
    if (hash == voice_last_quote_hash) return;
    voice_last_quote_hash = hash;
    voice_seen = 1u;
    voice_match_count++;
    voice_last_pointer = (u32)caption;
    stream_init();
    /* Finish releasing an old sample before claiming the channel again. */
    stream_stop();
    /* stream_init runs once, but each later battle needs the channel lock. */
    snd_lock_channel(STREAM_LEFT_MASK);
    stream_play(&STREAM_ENTRIES[0]);
}
