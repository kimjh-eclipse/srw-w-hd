# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

import struct
from pathlib import Path


SAMPLE_RATE = 22_050
BLOCK_SAMPLES = 384
BLOCK_SIZE = 4 + BLOCK_SAMPLES // 2
HEADER_SIZE = 0x68
WAVE_TYPE_ADPCM = 2

_STEP_TABLE = (
    7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 19, 21, 23, 25, 28, 31,
    34, 37, 41, 45, 50, 55, 60, 66, 73, 80, 88, 97, 107, 118, 130,
    143, 157, 173, 190, 209, 230, 253, 279, 307, 337, 371, 408, 449,
    494, 544, 598, 658, 724, 796, 876, 963, 1060, 1166, 1282, 1411,
    1552, 1707, 1878, 2066, 2272, 2499, 2749, 3024, 3327, 3660, 4026,
    4428, 4871, 5358, 5894, 6484, 7132, 7845, 8630, 9493, 10442,
    11487, 12635, 13899, 15289, 16818, 18500, 20350, 22385, 24623,
    27086, 29794, 32767,
)
_INDEX_TABLE = (-1, -1, -1, -1, 2, 4, 6, 8)


def _clamp_sample(value: int) -> int:
    return max(-32768, min(32767, value))


def _initial_index(samples: list[int]) -> int:
    if len(samples) < 2:
        return 0
    target = abs(samples[1] - samples[0]) * 4 // 3
    for index, step in enumerate(_STEP_TABLE):
        if step >= target:
            return index
    return 88


def encode_adpcm_block(samples: list[int], predictor: int | None = None,
                       step_index: int | None = None) -> tuple[bytes, int, int]:
    if not samples or len(samples) & 1:
        raise ValueError("ADPCM block requires a non-empty even sample count")
    predictor = _clamp_sample(samples[0] if predictor is None else predictor)
    step_index = _initial_index(samples) if step_index is None else max(0, min(88, step_index))
    output = bytearray(struct.pack("<hBB", predictor, step_index, 0))
    packed = 0
    for sample_index, sample in enumerate(samples):
        step = _STEP_TABLE[step_index]
        difference = int(sample) - predictor
        nibble = 8 if difference < 0 else 0
        magnitude = -difference if difference < 0 else difference
        delta = step >> 3
        if magnitude >= step:
            nibble |= 4
            magnitude -= step
            delta += step
        if magnitude >= step >> 1:
            nibble |= 2
            magnitude -= step >> 1
            delta += step >> 1
        if magnitude >= step >> 2:
            nibble |= 1
            delta += step >> 2
        predictor = _clamp_sample(predictor - delta if nibble & 8 else predictor + delta)
        step_index = max(0, min(88, step_index + _INDEX_TABLE[nibble & 7]))
        if sample_index & 1:
            output.append(packed | (nibble << 4))
        else:
            packed = nibble
    return bytes(output), predictor, step_index


def decode_adpcm_block(block: bytes, sample_count: int) -> list[int]:
    if sample_count < 0 or len(block) != 4 + (sample_count + 1) // 2:
        raise ValueError("ADPCM block size does not match its sample count")
    predictor, step_index, reserved = struct.unpack_from("<hBB", block)
    if step_index > 88 or reserved != 0:
        raise ValueError("Invalid Nintendo DS IMA-ADPCM block state")
    output: list[int] = []
    for byte in block[4:]:
        for nibble in (byte & 0x0F, byte >> 4):
            if len(output) == sample_count:
                break
            step = _STEP_TABLE[step_index]
            delta = step >> 3
            if nibble & 1:
                delta += step >> 2
            if nibble & 2:
                delta += step >> 1
            if nibble & 4:
                delta += step
            predictor = _clamp_sample(predictor - delta if nibble & 8 else predictor + delta)
            step_index = max(0, min(88, step_index + _INDEX_TABLE[nibble & 7]))
            output.append(predictor)
    return output


def make_strm(interleaved_pcm16: bytes, channels: int,
              sample_rate: int = SAMPLE_RATE) -> tuple[bytes, dict[str, int]]:
    if channels not in (1, 2):
        raise ValueError("STRM channels must be mono or stereo")
    if sample_rate <= 0 or sample_rate > 32728:
        raise ValueError(f"Unsupported STRM sample rate: {sample_rate}")
    frame_size = channels * 2
    usable_frames = len(interleaved_pcm16) // frame_size
    usable_frames -= usable_frames % BLOCK_SAMPLES
    if usable_frames < BLOCK_SAMPLES * 2:
        raise ValueError("Audio must contain at least two ADPCM blocks")
    values = struct.unpack_from(f"<{usable_frames * channels}h", interleaved_pcm16)
    channel_samples = [list(values[channel::channels]) for channel in range(channels)]
    block_count = usable_frames // BLOCK_SAMPLES
    wave_data = bytearray()
    states: list[tuple[int | None, int | None]] = [(None, None)] * channels
    for block_index in range(block_count):
        begin = block_index * BLOCK_SAMPLES
        end = begin + BLOCK_SAMPLES
        for channel in range(channels):
            predictor, step_index = states[channel]
            encoded, predictor, step_index = encode_adpcm_block(
                channel_samples[channel][begin:end], predictor, step_index
            )
            wave_data.extend(encoded)
            states[channel] = predictor, step_index

    file_size = HEADER_SIZE + len(wave_data)
    timer = 16_756_991 // sample_rate // 32
    output = bytearray(struct.pack("<4sHHIHH", b"STRM", 0xFEFF, 0x0100,
                                   file_size, 0x10, 2))
    output.extend(struct.pack("<4sI", b"HEAD", 0x50))
    output.extend(struct.pack(
        "<4B2H8I8I", WAVE_TYPE_ADPCM, 1, channels, 0, sample_rate, timer,
        0, usable_frames, HEADER_SIZE, block_count, BLOCK_SIZE, BLOCK_SAMPLES,
        BLOCK_SIZE, BLOCK_SAMPLES, *([0] * 8),
    ))
    output.extend(struct.pack("<4sI", b"DATA", 8 + len(wave_data)))
    output.extend(wave_data)
    return bytes(output), {
        "sample_rate": sample_rate,
        "samples": usable_frames,
        "channels": channels,
        "block_count": block_count,
        "block_size": BLOCK_SIZE,
        "encoded_bytes": len(wave_data),
    }


def parse_strm(source: bytes | bytearray | Path) -> dict[str, int | bytes]:
    data = Path(source).read_bytes() if isinstance(source, Path) else bytes(source)
    if len(data) < HEADER_SIZE:
        raise ValueError("STRM header is truncated")
    magic, bom, version, file_size, header_size, section_count = struct.unpack_from(
        "<4sHHIHH", data, 0
    )
    if (magic, bom, version, header_size, section_count) != (b"STRM", 0xFEFF, 0x0100, 0x10, 2):
        raise ValueError("Unsupported or invalid Nintendo DS STRM header")
    if file_size != len(data):
        raise ValueError("STRM declared size does not match the file")
    head_magic, head_size = struct.unpack_from("<4sI", data, 0x10)
    if head_magic != b"HEAD" or head_size != 0x50:
        raise ValueError("STRM HEAD section is invalid")
    fields = struct.unpack_from("<4B2H8I8I", data, 0x18)
    (wave_type, looped, channels, unknown, sample_rate, time, loop_start,
     sample_count, data_offset, block_count, block_size, samples_per_block,
     last_block_size, last_block_samples, *reserved) = fields
    if wave_type != WAVE_TYPE_ADPCM:
        raise ValueError("Only ADPCM STRM files are supported")
    if looped != 1 or channels not in (1, 2) or unknown != 0 or any(reserved):
        raise ValueError("Unsupported STRM channel, loop, or reserved fields")
    if sample_rate <= 0 or sample_rate > 32728 or time != 16_756_991 // sample_rate // 32:
        raise ValueError("Invalid STRM sample rate or timer")
    if loop_start != 0 or data_offset != HEADER_SIZE or block_count < 2:
        raise ValueError("Only whole-track, multi-block STRM loops are supported")
    if (block_size, samples_per_block, last_block_size, last_block_samples) != (
        BLOCK_SIZE, BLOCK_SAMPLES, BLOCK_SIZE, BLOCK_SAMPLES
    ):
        raise ValueError("STRM block layout is incompatible with this player")
    if sample_count != block_count * BLOCK_SAMPLES:
        raise ValueError("STRM sample count does not match its blocks")
    data_magic, data_size = struct.unpack_from("<4sI", data, 0x60)
    encoded_size = block_count * channels * BLOCK_SIZE
    if data_magic != b"DATA" or data_size != 8 + encoded_size or len(data) != HEADER_SIZE + encoded_size:
        raise ValueError("STRM DATA section size is invalid")
    for offset in range(HEADER_SIZE, len(data), BLOCK_SIZE):
        if data[offset + 2] > 88 or data[offset + 3] != 0:
            raise ValueError("STRM contains an invalid ADPCM block state")
    return {
        "data": data,
        "sample_rate": sample_rate,
        "samples": sample_count,
        "channels": channels,
        "block_count": block_count,
        "block_size": block_size,
        "data_offset": data_offset,
        "encoded_size": encoded_size,
    }
