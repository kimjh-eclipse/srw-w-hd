"""Build a battle-only Kazuma voice prototype; never edit the source ROM."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
import hashlib, json, shutil, subprocess, sys, struct, wave

ROOT = PROJECT_ROOT
REF = ROOT / 'reference_bgm'
ENGINE = ROOT / 'research/legacy/battle_voice_engine'
CURRENT = ROOT / 'release_battle_v02'
SOURCE = ROOT / 'baseline/SRWW_Korean_1.0.8.nds'
SAMPLE = ROOT.parent / 'work_ogs/runtime/qwen_axel_samples/axel_japanese_reference.wav'
EXPECTED = '0a5a22bd6bb25ebe640767e6b422b91358636e9ae1300e61d7e8ac3c5d8cd478'

def main():
    source = SOURCE.read_bytes()
    assert hashlib.sha256(source).hexdigest() == EXPECTED, 'Unrecognized source ROM'
    ENGINE.mkdir(exist_ok=True)
    for name in ('src',):
        shutil.copytree(REF / name, ENGINE / name, dirs_exist_ok=True)
    for name in ('build.py', 'strm_codec.py', 'LICENSE', 'AUTHORS.md', 'THIRD_PARTY_NOTICES.md'):
        shutil.copy2(REF / name, ENGINE / name)
    src = ENGINE / 'src/stream_patch.c'
    text = src.read_text(encoding='utf-8')
    # The voice uses mono channel 6 while the game's BGM sequence stays active.
    text = text.replace('snd_lock_channel(STREAM_CHANNEL_MASK);', 'snd_lock_channel(STREAM_LEFT_MASK);')
    stop_marker = '    stream_stop_channels(channel_mask);\n    active_channel_mask = 0u;'
    assert stop_marker in text
    text = text.replace(stop_marker, '''    stream_stop_channels(channel_mask);
    /* Return the mono voice channel to the game's sequence allocator. */
    if (channel_mask) {
        PushCommand_impl(27u, channel_mask, 0u, 0u, 0u);
        SND_FlushCommand(SND_COMMAND_BLOCK | SND_COMMAND_IMMEDIATE);
    }
    active_channel_mask = 0u;''')
    old = '''    if (stream_block >= ENTRY_BLOCK_COUNT(entry)) {
        stream_block = 0u;
        FS_SeekFile(stream_file, 0, 0);
    }'''
    assert old in text
    text = text.replace(old, '')
    marker = '    for (channel = 0u; channel < ENTRY_CHANNELS(entry); ++channel) {'
    assert text.count(marker) == 1
    text = text.replace(marker, '''    /* One-shot probe: clear consumed pages at EOF, never seek to the start. */
    if (stream_block >= ENTRY_BLOCK_COUNT(entry)) {
        for (channel = 0u; channel < ENTRY_CHANNELS(entry); ++channel) {
            clear_channel_page(channel, page);
            DC_FlushRange(audio_buffer[channel][page], PAGE_SIZE);
        }
        stream_block++;
        return;
    }
''' + marker)
    marker = '''                fill_page(entry, value - 1u);
                refill_busy = 0;'''
    assert marker in text
    text = text.replace(marker, marker + '''
                /* Both queued pages have played; release the file and stop. */
                if (stream_block >= ENTRY_BLOCK_COUNT(entry) + 2u) {
                    stream_stop_audio();
                    stream_close_files();
                }''')
    text += '\n' + (ROOT/'research/legacy/battle_voice_trigger.c.inc').read_text(encoding='utf-8')
    src.write_text(text, encoding='utf-8')
    original_hook = (ENGINE/'src/hook.S').read_text(encoding='utf-8')
    tail = original_hook[original_hook.index('    .global seq_stop_hook'):]
    hook = '''/* MPL-2.0: adapted from reference_bgm/src/hook.S. */
    .syntax unified
    .arm
    .section .text.hook, "ax", %progbits
    .global bgm_hook
    .type bgm_hook, %function
    .extern voice_glyph_probe
bgm_hook:
    stmdb sp!, {r0-r3, r12, lr}
    bl voice_glyph_probe
    ldmia sp!, {r0-r3, r12, lr}
    @ Replay the main-loop update prologue; preserve its literal load value.
    stmdb sp!, {r3-r5, lr}
    ldr r0, =ORIGINAL_UPDATE_LITERAL
    ldr pc, =0x0200EE58
    .ltorg
    .size bgm_hook, .-bgm_hook
'''
    arm9_file_offset=struct.unpack_from('<I',source,0x20)[0]
    literal=struct.unpack_from('<I',source,arm9_file_offset+0xef14)[0]
    hook=hook.replace('ORIGINAL_UPDATE_LITERAL',f'0x{literal:08X}')
    (ENGINE/'src/hook.S').write_text(hook+tail,encoding='utf-8')
    sys.path.insert(0, str(ENGINE))
    import build, strm_codec
    build.EXPECTED_SHA256 = EXPECTED
    build.SOURCE_ROM = SOURCE
    build.HOOK_ADDRESS = 0x0200EE50
    build.EXPECTED_HOOK_BYTES = bytes.fromhex('38402de9b8009fe5')
    # Keep one stable user-facing ROM; publish it atomically after validation.
    CURRENT.mkdir(exist_ok=True)
    build.OUT_DIR = CURRENT
    build.OUTPUT_ROM_NAME = '.build_rom.tmp'
    build.OUTPUT_BPS_NAME = '.build_patch.tmp'
    compiler = next((ROOT / 'tools').glob('xpack-*/bin/arm-none-eabi-gcc.exe'))
    build.CC = compiler
    build.OBJCOPY = compiler.with_name('arm-none-eabi-objcopy.exe')
    build.NM = compiler.with_name('arm-none-eabi-nm.exe')
    build.STRM_DIR = ENGINE/'hero_streams'
    build.STRM_DIR.mkdir(exist_ok=True)
    audio = ROOT / 'research/legacy/audio'
    audio.mkdir(exist_ok=True)
    shutil.copy2(SAMPLE, audio / 'axel_original.wav')
    ffmpeg = ROOT.parent / '.video-tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
    wav = audio / 'axel_ds_22050.wav'
    subprocess.run([str(ffmpeg), '-y', '-v', 'error', '-i', str(SAMPLE),
                    '-af', 'highpass=f=20,lowpass=f=9500,volume=0.7',
                    '-ar', '22050', '-ac', '1', '-c:a', 'pcm_s16le', str(wav)], check=True)
    with wave.open(str(wav), 'rb') as f:
        pcm = f.readframes(f.getnframes())
    # Pad the last partial codec block; do not truncate the end of the voice.
    unit = strm_codec.BLOCK_SAMPLES * 2
    pcm += b'\0' * ((-len(pcm)) % unit)
    encoded, metadata = strm_codec.make_strm(pcm, 1)
    (build.STRM_DIR / '0.strm').write_bytes(encoded)
    try:
        build.main()
        final_rom = CURRENT/'SRWW_K_Kazuma_BattleVoice_v02.nds'
        (CURRENT/build.OUTPUT_ROM_NAME).replace(final_rom)
        manifest_path = CURRENT/'build_manifest.json'
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        manifest['target']['path'] = str(final_rom)
        manifest.pop('patch', None)
        manifest['patch_validation'] = 'BPS round-trip passed; temporary patch removed'
        manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    finally:
        for name in (build.OUTPUT_ROM_NAME, build.OUTPUT_BPS_NAME):
            (CURRENT/name).unlink(missing_ok=True)
    symbols = {name: build.symbol_address(build.WORK_DIR/'payload.elf',name)
               for name in ['voice_seen','voice_match_count','voice_glyph_calls','voice_last_pointer','voice_battle_count','voice_ignored_map_frames','voice_ignored_speaker_frames','voice_last_quote_hash','stream_underruns','stream_block','playing']}
    (CURRENT/'research/legacy/voice_probe_symbols.json').write_text(json.dumps(symbols,indent=2),encoding='utf-8')
    report = dict(source_sha256=EXPECTED, sample_source=str(SAMPLE),
                  sample_sha256=hashlib.sha256(SAMPLE.read_bytes()).hexdigest(),
                  upstream_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REF,text=True).strip(),
                  trigger='each new Kazuma battle-animation caption; no sentence restriction', loop=False,
                  once_per_quote=True, original_bgm_preserved=True,
                  battle_dialogue_mapping=True, scenario_dialogue_mapping=False, audio=metadata)
    (CURRENT / 'research/legacy/probe_manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED

if __name__ == '__main__':
    main()
