/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/. */

typedef unsigned char u8;
typedef signed char s8;
typedef signed short s16;
typedef unsigned int u32;
typedef int s32;

#define PAGE_SIZE 768u
#define BUFFER_SIZE (PAGE_SIZE * 2u)
#define BLOCK_SAMPLES 384u
#define ADPCM_BLOCK_SIZE 196u
#define STREAM_TIMER 759u
#define STREAM_ALARM_PERIOD 9108u
#define STREAM_MAX_VOLUME 110u
#define STREAM_LEFT_CHANNEL 6u
#define STREAM_RIGHT_CHANNEL 7u
#define STREAM_LEFT_MASK (1u << STREAM_LEFT_CHANNEL)
#define STREAM_RIGHT_MASK (1u << STREAM_RIGHT_CHANNEL)
#define STREAM_CHANNEL_MASK (STREAM_LEFT_MASK | STREAM_RIGHT_MASK)
#define STREAM_ALARM 7u
#define STREAM_ALARM_MASK (1u << STREAM_ALARM)
#define OS_MESSAGE_BLOCK 1
#define SND_COMMAND_BLOCK 1u
#define SND_COMMAND_IMMEDIATE 2u
#define STREAM_MESSAGE_PAGE0 1u
#define STREAM_MESSAGE_PAGE1 2u
#define STREAM_MESSAGE_START 3u
#define STREAM_THREAD_PRIORITY 12u

#ifndef STREAM_DIAG_STAGE
#define STREAM_DIAG_STAGE 6
#endif

typedef struct {
    u32 bgm_id;
    u32 data_rom_offset;
    u32 block_count_flags;
} StreamEntry;

#define ENTRY_BLOCK_COUNT(entry) ((entry)->block_count_flags & 0x7fffffffu)
#define ENTRY_CHANNELS(entry) (((entry)->block_count_flags >> 31) + 1u)

#include "generated_config.h"

typedef struct {
    void *send_head;
    void *send_tail;
    void *receive_head;
    void *receive_tail;
    void **messages;
    s32 capacity;
    s32 first;
    s32 used;
} StreamMessageQueue;

typedef struct {
    void (*handler)(void *);
    void *argument;
    volatile u8 id;
    u8 padding[3];
} SoundAlarmHandler;

extern void PushCommand_impl(u32 command, u32 arg1, u32 arg2, u32 arg3, u32 arg4);
extern void SND_StartTimer(u32 channel_mask, u32 capture_mask, u32 alarm_mask, u32 flags);
extern void SND_StopTimer(u32 channel_mask, u32 capture_mask, u32 alarm_mask, u32 flags);
extern s32 SND_FlushCommand(u32 flags);
extern void FS_InitFile(void *file);
extern s32 FS_OpenFileDirect(void *file, void *archive, u32 image_top,
                             u32 image_bottom, u32 file_index);
extern s32 FS_ReadFile(void *file, void *destination, s32 size);
extern s32 FS_SeekFile(void *file, s32 offset, s32 origin);
extern s32 FS_CloseFile(void *file);
extern void DC_FlushRange(const void *address, u32 size);
extern s32 OS_ReceiveMessage(void *queue, void **message, s32 flags);
extern void OS_CreateThread(void *thread, void (*function)(void *), void *arg,
                            void *stack_bottom, u32 stack_size, u32 priority);
extern void OS_WakeupThread(void *queue);
extern void OS_WakeupThreadDirect(void *thread);
extern void Game_SetMasterVolumeFx(u32 volume_fx);
extern void seq_stop_original(u32 slot);
extern void Game_UpdateBgmState(void);
extern void Game_SelectBgmState(u32 bgm_id);

/* Channel-major layout keeps both double buffers contiguous for sound DMA. */
static u8 audio_buffer[2][2][PAGE_SIZE] __attribute__((aligned(32)));
static u8 stream_thread_object[0xc0] __attribute__((aligned(8)));
static u8 stream_thread_stack[1024] __attribute__((aligned(8)));
static StreamMessageQueue message_queue __attribute__((aligned(8)));
static void *message_slots[2];
/* Retail SDK FSFile is 0x4c bytes in this ARM9 build. */
static u8 stream_file[0x4c] __attribute__((aligned(4)));
static u8 adpcm_block[ADPCM_BLOCK_SIZE] __attribute__((aligned(4)));

static const StreamEntry *current_stream;
static const StreamEntry *requested_stream;
static u32 stream_block;
static s32 initialized;
static volatile s32 playing;
static u32 stream_file_open;
static u32 active_channel_mask;
static volatile u32 next_refill_page;
static volatile s32 refill_busy;
static volatile u32 silence_page_mask;
__attribute__((used)) volatile u32 stream_underruns;

static const s16 adpcm_step_table[89] = {
    7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 19, 21, 23, 25, 28, 31,
    34, 37, 41, 45, 50, 55, 60, 66, 73, 80, 88, 97, 107, 118, 130,
    143, 157, 173, 190, 209, 230, 253, 279, 307, 337, 371, 408, 449,
    494, 544, 598, 658, 724, 796, 876, 963, 1060, 1166, 1282, 1411,
    1552, 1707, 1878, 2066, 2272, 2499, 2749, 3024, 3327, 3660, 4026,
    4428, 4871, 5358, 5894, 6484, 7132, 7845, 8630, 9493, 10442,
    11487, 12635, 13899, 15289, 16818, 18500, 20350, 22385, 24623,
    27086, 29794, 32767
};
static const s8 adpcm_index_table[8] = {-1, -1, -1, -1, 2, 4, 6, 8};

/* SNDi alarm handler table entry 7 in this exact retail ARM9 build. */
static volatile SoundAlarmHandler *const alarm_handler =
    (volatile SoundAlarmHandler *)0x0220d314u;

static void stream_stop(void);
static void stream_stop_audio(void);
static void stream_stop_channels(u32 channel_mask);
static void clear_channel_page(u32 channel, u32 page);

static void snd_lock_channel(u32 channel_mask)
{
    PushCommand_impl(26u, channel_mask, 0u, 0u, 0u);
}

static void snd_setup_pcm(u32 channel, const void *data, u32 data_words,
                          u32 timer, u32 pan)
{
    u32 arg1 = channel | (timer << 16);
    u32 arg3 = data_words | (STREAM_MAX_VOLUME << 24);
    u32 arg4 = (1u << 26) | (1u << 24) | (pan << 16);
    PushCommand_impl(14u, arg1, (u32)data, arg3, arg4);
}

static void snd_set_channel_volume(u32 channel_mask, u32 volume)
{
    /* SND_COMMAND_CHANNEL_VOLUME, SND_CHANNEL_DATASHIFT_NONE. */
    PushCommand_impl(20u, channel_mask, volume, 0u, 0u);
}

static void stream_alarm_callback(void *argument)
{
    u32 page;
    u32 stale_page;
    s32 slot;
    (void)argument;
    if (!playing) {
        return;
    }

    page = next_refill_page;
    next_refill_page ^= 1u;
    if (refill_busy || message_queue.used >= message_queue.capacity) {
        /* The previous refill page is now being replayed by sound DMA. */
        stale_page = page ^ 1u;
        silence_page_mask |= 1u << stale_page;
        clear_channel_page(0u, stale_page);
        DC_FlushRange(audio_buffer[0][stale_page], PAGE_SIZE);
        clear_channel_page(1u, stale_page);
        DC_FlushRange(audio_buffer[1][stale_page], PAGE_SIZE);
        stream_underruns++;
    }
    if (message_queue.used >= message_queue.capacity) {
        return;
    }
    slot = message_queue.first + message_queue.used;
    if (slot >= message_queue.capacity) {
        slot -= message_queue.capacity;
    }
    message_queue.messages[slot] = (void *)(page + 1u);
    message_queue.used++;
    OS_WakeupThread(&message_queue.receive_head);
}

static void snd_setup_stream_alarm(u32 tick, u32 period)
{
    u8 id;
    alarm_handler->handler = stream_alarm_callback;
    alarm_handler->argument = 0;
    id = (u8)(alarm_handler->id + 1u);
    alarm_handler->id = id;
    PushCommand_impl(18u, STREAM_ALARM, tick, period, id);
}

static s32 stream_open_files(const StreamEntry *entry)
{
    u32 data_size = ENTRY_BLOCK_COUNT(entry) * ENTRY_CHANNELS(entry) * ADPCM_BLOCK_SIZE;
    FS_InitFile(stream_file);
    if (!FS_OpenFileDirect(stream_file, (void *)0x0220d3d4u,
                           entry->data_rom_offset,
                           entry->data_rom_offset + data_size,
                           0xffffffffu)) {
        return 0;
    }
    stream_file_open = 1u;
    return 1;
}

static void stream_close_files(void)
{
    if (stream_file_open) {
        FS_CloseFile(stream_file);
    }
    stream_file_open = 0u;
}

static s32 clamp_sample(s32 value)
{
    if (value < -32768) {
        return -32768;
    }
    return value > 32767 ? 32767 : value;
}

static __attribute__((always_inline)) inline s32 decode_adpcm_nibble(
    s32 predictor, s32 *step_index, u32 nibble)
{
    s32 step = adpcm_step_table[*step_index];
    s32 delta = step >> 3;
    if (nibble & 1u) delta += step >> 2;
    if (nibble & 2u) delta += step >> 1;
    if (nibble & 4u) delta += step;
    predictor = clamp_sample((nibble & 8u) ? predictor - delta : predictor + delta);
    *step_index += adpcm_index_table[nibble & 7u];
    if (*step_index < 0) *step_index = 0;
    else if (*step_index > 88) *step_index = 88;
    return predictor;
}

static s32 decode_adpcm_block(s16 *destination)
{
    s32 predictor = (s16)((u32)adpcm_block[0] | ((u32)adpcm_block[1] << 8));
    s32 step_index = adpcm_block[2];
    u32 byte_index;
    if (step_index > 88 || adpcm_block[3] != 0u) {
        return 0;
    }
    for (byte_index = 0u; byte_index < BLOCK_SAMPLES / 2u; ++byte_index) {
        u32 packed = adpcm_block[4u + byte_index];
        predictor = decode_adpcm_nibble(predictor, &step_index, packed & 15u);
        destination[byte_index * 2u] = (s16)predictor;
        predictor = decode_adpcm_nibble(predictor, &step_index, packed >> 4);
        destination[byte_index * 2u + 1u] = (s16)predictor;
    }
    return 1;
}

static void clear_channel_page(u32 channel, u32 page)
{
    u32 *destination = (u32 *)audio_buffer[channel][page];
    u32 index;
    for (index = 0u; index < PAGE_SIZE / 4u; ++index) {
        destination[index] = 0u;
    }
}

static void fill_page(const StreamEntry *entry, u32 page)
{
    u32 channel;
    if (!entry || ENTRY_BLOCK_COUNT(entry) == 0u) {
        return;
    }
    /* One-shot probe: clear consumed pages at EOF, never seek to the start. */
    if (stream_block >= ENTRY_BLOCK_COUNT(entry)) {
        for (channel = 0u; channel < ENTRY_CHANNELS(entry); ++channel) {
            clear_channel_page(channel, page);
            DC_FlushRange(audio_buffer[channel][page], PAGE_SIZE);
        }
        stream_block++;
        return;
    }
    for (channel = 0u; channel < ENTRY_CHANNELS(entry); ++channel) {
        if (FS_ReadFile(stream_file, adpcm_block, ADPCM_BLOCK_SIZE) != ADPCM_BLOCK_SIZE ||
            !decode_adpcm_block((s16 *)audio_buffer[channel][page])) {
            clear_channel_page(channel, page);
        }
        if (silence_page_mask & (1u << page)) {
            clear_channel_page(channel, page);
        }
        DC_FlushRange(audio_buffer[channel][page], PAGE_SIZE);
    }
    silence_page_mask &= ~(1u << page);
    stream_block++;

}

static void stream_thread_main(void *arg)
{
    void *message;
    u32 value;
    const StreamEntry *entry;
    (void)arg;
    for (;;) {
        OS_ReceiveMessage(&message_queue, &message, OS_MESSAGE_BLOCK);
        value = (u32)message;
        if (value == STREAM_MESSAGE_START && requested_stream) {
            entry = requested_stream;
            stream_close_files();
            if (!stream_open_files(entry)) {
                continue;
            }
            stream_block = 0u;
            fill_page(entry, 0u);
#if STREAM_DIAG_STAGE == 3
            /* Diagnostic: prove the deferred NitroFS read returns. */
            stream_close_files();
            continue;
#else
            fill_page(entry, 1u);
            if (requested_stream != entry) {
                stream_close_files();
                continue;
            }
            current_stream = entry;
            active_channel_mask = STREAM_LEFT_MASK;
            snd_setup_pcm(STREAM_LEFT_CHANNEL, audio_buffer[0], BUFFER_SIZE / 4u,
                          STREAM_TIMER, ENTRY_CHANNELS(entry) == 2u ? 0u : 64u);
            if (ENTRY_CHANNELS(entry) == 2u) {
                snd_setup_pcm(STREAM_RIGHT_CHANNEL, audio_buffer[1], BUFFER_SIZE / 4u,
                              STREAM_TIMER, 127u);
                active_channel_mask |= STREAM_RIGHT_MASK;
            }
            snd_setup_stream_alarm(STREAM_ALARM_PERIOD, STREAM_ALARM_PERIOD);
#if STREAM_DIAG_STAGE == 4
            /* Diagnostic: queue PCM setup, but do not start its timer. */
            stream_close_files();
            continue;
#endif
            playing = 1;
            silence_page_mask = 0u;
            next_refill_page = 0u;
            SND_StartTimer(active_channel_mask, 0u, STREAM_ALARM_MASK, 0u);
#if STREAM_DIAG_STAGE == 5
            /* Diagnostic: start the double buffer without useful refills. */
            stream_close_files();
            continue;
#endif
#endif
        } else if ((value == STREAM_MESSAGE_PAGE0 ||
                    value == STREAM_MESSAGE_PAGE1) && playing) {
            entry = current_stream;
            if (entry) {
                refill_busy = 1;
                fill_page(entry, value - 1u);
                refill_busy = 0;
                /* Both queued pages have played; release the file and stop. */
                if (stream_block >= ENTRY_BLOCK_COUNT(entry) + 2u) {
                    stream_stop_audio();
                    stream_close_files();
                }
            }
        }
    }
}

static void stream_init(void)
{
    if (initialized) {
        return;
    }
    message_queue.send_head = 0;
    message_queue.send_tail = 0;
    message_queue.receive_head = 0;
    message_queue.receive_tail = 0;
    message_queue.messages = message_slots;
    message_queue.capacity = 2;
    message_queue.first = 0;
    message_queue.used = 0;
    OS_CreateThread(stream_thread_object, stream_thread_main, 0,
                    stream_thread_stack + sizeof(stream_thread_stack),
                    sizeof(stream_thread_stack), STREAM_THREAD_PRIORITY);
    OS_WakeupThreadDirect(stream_thread_object);
    snd_lock_channel(STREAM_LEFT_MASK);
    initialized = 1;
}

static void silence_audio_buffer(void)
{
    u32 *word = (u32 *)audio_buffer;
    u32 index;
    for (index = 0u; index < (BUFFER_SIZE * 2u) / 4u; ++index) {
        word[index] = 0u;
    }
    /* ARM7/sound DMA must see the zeroes rather than stale ARM9 cache data. */
    DC_FlushRange(audio_buffer, BUFFER_SIZE * 2u);
}

static void stream_stop_channels(u32 channel_mask)
{
    if (channel_mask) {
        /*
         * Mute and stop before clearing RAM. A refill already running on the
         * worker can otherwise restore the final PCM page after it was
         * cleared, making the tiny loop buzz until ARM7 handles the stop.
         */
        snd_set_channel_volume(channel_mask, 0u);
        SND_StopTimer(channel_mask, 0u, STREAM_ALARM_MASK, 0u);
        /* Wait until ARM7 has applied both commands. */
        SND_FlushCommand(SND_COMMAND_BLOCK | SND_COMMAND_IMMEDIATE);
        silence_audio_buffer();
    }
}

static void stream_stop_audio(void)
{
    u32 channel_mask = active_channel_mask;
    playing = 0;
    stream_stop_channels(channel_mask);
    /* Return the mono voice channel to the game's sequence allocator. */
    if (channel_mask) {
        PushCommand_impl(27u, channel_mask, 0u, 0u, 0u);
        SND_FlushCommand(SND_COMMAND_BLOCK | SND_COMMAND_IMMEDIATE);
    }
    active_channel_mask = 0u;
    current_stream = 0;
    silence_page_mask = 0u;
}

static void stream_stop(void)
{
    stream_stop_audio();
    requested_stream = 0;
}

/* Called when the retail game stops its BGM sequence player (slot 0). */
__attribute__((used)) void stream_stop_from_game(void)
{
    stream_stop();
}

/* Mirror the retail SSEQ player-0 fade onto the replacement PCM channel. */
__attribute__((used)) void stream_set_volume_from_game(u32 slot, s32 volume_fx)
{
    s32 volume;
    if (slot != 0u || !playing) {
        return;
    }
    volume = volume_fx >> 12;
    if (volume < 0) {
        volume = 0;
    } else if (volume > (s32)STREAM_MAX_VOLUME) {
        volume = (s32)STREAM_MAX_VOLUME;
    }
    snd_set_channel_volume(active_channel_mask, (u32)volume);
}

static void stream_play(const StreamEntry *entry)
{
    stream_stop();
    requested_stream = entry;

    /* Wake the NitroFS worker; subsequent page requests come from alarm 7. */
    message_slots[0] = (void *)STREAM_MESSAGE_START;
    message_queue.first = 0;
    message_queue.used = 1;
    OS_WakeupThread(&message_queue.receive_head);
}

static const StreamEntry *find_stream(u32 bgm_id)
{
    u32 index;
    for (index = 0u; index < STREAM_ENTRY_COUNT; ++index) {
        if (STREAM_ENTRIES[index].bgm_id == bgm_id) {
            return &STREAM_ENTRIES[index];
        }
    }
    return 0;
}

/*
 * Entry-side probe used by the assembly trampoline.  Non-replaced BGM calls
 * continue through the untouched retail function body.  Replaced calls use
 * the state-only path below so the retail asynchronous SSEQ loader is never
 * started for an ID that will be streamed as PCM.
 */
__attribute__((used)) s32 stream_probe(u32 bgm_id)
{
    const StreamEntry *entry = find_stream(bgm_id);
    /* Stop at the same request boundary for both STRM and retail SSEQ. */
    stream_stop();
    return entry != 0;
}

__attribute__((used)) void stream_after_original(u32 bgm_id)
{
    const StreamEntry *entry = find_stream(bgm_id);
    volatile u32 *sound_flags = (volatile u32 *)0x021e7ebcu;
    volatile u8 *current_bgm = (volatile u8 *)0x021e7eddu;
    if (!entry) {
        return;
    }
    /* These are all retail side effects before the final SSEQ-load call. */
    if ((*sound_flags & 0x800u) != 0u) {
        return;
    }
    *current_bgm = (u8)bgm_id;
    Game_SetMasterVolumeFx(0x7f000u);
    Game_UpdateBgmState();
    Game_SelectBgmState(bgm_id);

#if STREAM_DIAG_STAGE == 0
    /* State-only replacement and hook return. */
    return;
#elif STREAM_DIAG_STAGE == 1
    /* Add OS queue/thread and channel lock initialization. */
    stream_init();
    return;
#elif STREAM_DIAG_STAGE == 2
    /* Stop the SSEQ only after the retail function registered its state. */
    stream_init();
    seq_stop_original(0u);
    return;
#elif STREAM_DIAG_STAGE == 3
    /* Add one deferred raw-ROM page read, but no sound commands. */
    stream_init();
    seq_stop_original(0u);
    stream_play(entry);
    return;
#else
    stream_init();
    seq_stop_original(0u);
    stream_play(entry);
    return;
#endif
}

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
