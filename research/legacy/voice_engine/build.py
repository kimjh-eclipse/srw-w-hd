# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

import hashlib
import json
import os
import struct
import subprocess
import sys
import zlib
from pathlib import Path

import strm_codec


ROOT = Path(__file__).resolve().parent
SOURCE_ROM = ROOT / "input.nds"
STRM_DIR = ROOT / "streams"
SRC_DIR = ROOT / "src"
WORK_DIR = ROOT / "work"
OUT_DIR = ROOT / "out"
OUTPUT_ROM_NAME = "0870 - Super Robot Taisen W (k) [STRM BGM].nds"
OUTPUT_BPS_NAME = "SRW_W_STRM_BGM.bps"
BGM_COUNT = 70

EXPECTED_SHA256 = "9cbeacfe4fdbeacd6b0ea070b2f2a583c04018f49a47f1e636d02614988c1287"
ARM9_RAM = 0x02000000
CAVE_START = 0x02001040
CAVE_END = 0x02003000
HOOK_ADDRESS = 0x02013110
EXPECTED_HOOK_BYTES = bytes.fromhex("10402de90040a0e1")
STOP_HOOK_ADDRESS = 0x0200F2E8
EXPECTED_STOP_HOOK_BYTES = bytes.fromhex("10402de940109fe5")
VOLUME_HOOK_ADDRESS = 0x0200F33C
EXPECTED_VOLUME_HOOK_BYTES = bytes.fromhex("08402de93c209fe5")
# The retail-compatible sound alarm refills alternating pages. 768 bytes keeps
# a two-channel double buffer and all 70 stream entries inside the verified cave.
PAGE_SIZE = 768
CC = Path(r"C:\devkitPro\devkitARM\bin\arm-none-eabi-gcc.exe")
OBJCOPY = Path(r"C:\devkitPro\devkitARM\bin\arm-none-eabi-objcopy.exe")
NM = Path(r"C:\devkitPro\devkitARM\bin\arm-none-eabi-nm.exe")


def align(value: int, alignment: int) -> int:
    return (value + alignment - 1) & ~(alignment - 1)


def run(command: list[str]) -> str:
    result = subprocess.run(command, cwd=ROOT, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(
            f"외부 빌드 명령 실패 ({result.returncode}): {command[0]}\n{result.stdout}"
        )
    return result.stdout


def parse_strm(path: Path) -> dict[str, object]:
    try:
        parsed = strm_codec.parse_strm(path)
    except ValueError as exc:
        raise ValueError(f"지원하지 않는 ADPCM STRM입니다: {path}: {exc}") from exc
    if int(parsed["sample_rate"]) != strm_codec.SAMPLE_RATE:
        raise ValueError(
            f"지원하지 않는 ADPCM STRM입니다: {path}: "
            f"sample rate must be {strm_codec.SAMPLE_RATE} Hz"
        )
    return parsed


def collect_streams(pack_base: int) -> tuple[bytes, list[dict[str, int]], list[dict[str, object]]]:
    candidates: list[tuple[int, Path]] = []
    for path in sorted(STRM_DIR.glob("*.strm")):
        try:
            bgm_id = int(path.stem)
        except ValueError:
            continue
        if path.stat().st_size > strm_codec.HEADER_SIZE:
            candidates.append((bgm_id, path))
    if not candidates:
        raise RuntimeError("사용할 ADPCM STRM 파일을 찾지 못했습니다.")

    pack = bytearray()
    by_hash: dict[str, tuple[int, dict[str, object]]] = {}
    entries: list[dict[str, int]] = []
    report: list[dict[str, object]] = []

    for bgm_id, path in candidates:
        parsed = parse_strm(path)
        data = parsed["data"]
        assert isinstance(data, bytes)
        digest = hashlib.sha256(data).hexdigest()
        was_duplicate = digest in by_hash
        if was_duplicate:
            local_offset, canonical = by_hash[digest]
            parsed = canonical
        else:
            local_offset = align(len(pack), 0x200)
            pack.extend(b"\x00" * (local_offset - len(pack)))
            pack.extend(data)
            by_hash[digest] = (local_offset, parsed)

        sample_rate = int(parsed["sample_rate"])
        channels = int(parsed["channels"])
        block_count = int(parsed["block_count"])
        data_offset = pack_base + local_offset + int(parsed["data_offset"])
        entries.append({
            "bgm_id": bgm_id,
            "data_rom_offset": data_offset,
            "block_count_flags": block_count | (0x80000000 if channels == 2 else 0),
        })
        report.append({
            "bgm_id": bgm_id,
            "source": path.name,
            "sample_rate": sample_rate,
            "strm_bytes": len(data),
            "adpcm_bytes": int(parsed["encoded_size"]),
            "samples": int(parsed["samples"]),
            "blocks": block_count,
            "channels": channels,
            "channel_mode": "mono" if channels == 1 else "stereo",
            "rom_offset": f"0x{pack_base + local_offset:08X}",
            "deduplicated": was_duplicate,
        })
    return bytes(pack), entries, report


def write_generated_config(entries: list[dict[str, int]]) -> None:
    lines = [
        "#ifndef GENERATED_CONFIG_H",
        "#define GENERATED_CONFIG_H",
        f"#define STREAM_ENTRY_COUNT {len(entries)}u",
        "static const StreamEntry STREAM_ENTRIES[STREAM_ENTRY_COUNT] = {",
    ]
    for entry in entries:
        lines.append(
            "    {%du, 0x%08Xu, 0x%08Xu}," % (
                entry["bgm_id"], entry["data_rom_offset"], entry["block_count_flags"],
            )
        )
    lines.extend(["};", "#endif", ""])
    (SRC_DIR / "generated_config.h").write_text("\n".join(lines), encoding="utf-8")


def symbol_address(elf: Path, name: str) -> int:
    for line in run([str(NM), "-n", str(elf)]).splitlines():
        fields = line.split()
        if len(fields) >= 3 and fields[2] == name:
            return int(fields[0], 16)
    raise RuntimeError(f"ELF 심볼을 찾지 못했습니다: {name}")


def build_payload(entries: list[dict[str, int]]) -> tuple[bytes, dict[str, int]]:
    write_generated_config(entries)
    c_obj = WORK_DIR / "stream_patch.o"
    hook_obj = WORK_DIR / "hook.o"
    elf = WORK_DIR / "payload.elf"
    binary = WORK_DIR / "payload.bin"
    common = [
        "-marm", "-march=armv5te", "-mlittle-endian", "-Os",
        "-ffreestanding", "-fno-builtin", "-fno-stack-protector",
        "-fdata-sections", "-ffunction-sections", "-Wall", "-Wextra",
        "-I", str(SRC_DIR),
    ]
    diag_stage = os.environ.get("STREAM_DIAG_STAGE")
    if diag_stage is not None:
        common.append(f"-DSTREAM_DIAG_STAGE={int(diag_stage)}")
    run([str(CC), *common, "-std=c11", "-c", str(SRC_DIR / "stream_patch.c"), "-o", str(c_obj)])
    run([str(CC), *common, "-c", str(SRC_DIR / "hook.S"), "-o", str(hook_obj)])
    run([
        str(CC), "-nostdlib", "-Wl,--gc-sections", "-Wl,-Map," + str(WORK_DIR / "payload.map"),
        "-T", str(SRC_DIR / "payload.ld"), str(hook_obj), str(c_obj), "-o", str(elf),
    ])
    run([str(OBJCOPY), "-O", "binary", str(elf), str(binary)])
    payload = binary.read_bytes()
    symbols = {
        "bgm_hook": symbol_address(elf, "bgm_hook"),
        "seq_stop_hook": symbol_address(elf, "seq_stop_hook"),
        "seq_volume_hook": symbol_address(elf, "seq_volume_hook"),
        "payload_start": symbol_address(elf, "__payload_start"),
        "payload_file_end": symbol_address(elf, "__payload_file_end"),
        "payload_end": symbol_address(elf, "__payload_end"),
        "bss_start": symbol_address(elf, "__bss_start"),
        "bss_end": symbol_address(elf, "__bss_end"),
    }
    if symbols["payload_end"] > CAVE_END:
        raise RuntimeError("컴파일된 페이로드가 검증된 코드 케이브를 넘었습니다.")
    expected_file_size = symbols["payload_file_end"] - symbols["payload_start"]
    # objcopy omits trailing alignment-only zeroes. The untouched cave is
    # already zero-filled, so a shorter file image is valid; a longer one is not.
    if len(payload) > expected_file_size:
        raise RuntimeError(f"페이로드 크기 초과: {len(payload)} > {expected_file_size}")
    return payload, symbols


def encode_arm_branch(source: int, destination: int) -> bytes:
    delta = destination - (source + 8)
    if delta & 3:
        raise ValueError("ARM branch destination is not word aligned")
    immediate = delta >> 2
    if not -(1 << 23) <= immediate < (1 << 23):
        raise ValueError("ARM branch target is out of range")
    return struct.pack("<I", 0xEA000000 | (immediate & 0x00FFFFFF))


def bps_number(value: int) -> bytes:
    output = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        if value == 0:
            output.append(byte | 0x80)
            return bytes(output)
        output.append(byte)
        value -= 1


def make_bps(source: bytes, target: bytes) -> bytes:
    patch = bytearray(b"BPS1")
    patch += bps_number(len(source))
    patch += bps_number(len(target))
    patch += bps_number(0)
    position = 0
    while position < len(target):
        same = position < len(source) and target[position] == source[position]
        end = position + 1
        if same:
            while end < len(target) and end < len(source) and target[end] == source[end]:
                end += 1
            patch += bps_number(((end - position - 1) << 2) | 0)
        else:
            while end < len(target):
                if end < len(source) and target[end] == source[end]:
                    lookahead = 0
                    while (end + lookahead < len(target)
                           and end + lookahead < len(source)
                           and target[end + lookahead] == source[end + lookahead]
                           and lookahead < 32):
                        lookahead += 1
                    if lookahead >= 32:
                        break
                end += 1
            patch += bps_number(((end - position - 1) << 2) | 1)
            patch += target[position:end]
        position = end
    patch += struct.pack("<I", zlib.crc32(source) & 0xFFFFFFFF)
    patch += struct.pack("<I", zlib.crc32(target) & 0xFFFFFFFF)
    patch += struct.pack("<I", zlib.crc32(patch) & 0xFFFFFFFF)
    return bytes(patch)


def read_bps_number(data: bytes, position: int) -> tuple[int, int]:
    value = 0
    shift = 1
    while True:
        byte = data[position]
        position += 1
        value += (byte & 0x7F) * shift
        if byte & 0x80:
            return value, position
        shift <<= 7
        value += shift


def apply_bps(source: bytes, patch: bytes) -> bytes:
    if patch[:4] != b"BPS1":
        raise RuntimeError("BPS magic 불일치")
    position = 4
    source_size, position = read_bps_number(patch, position)
    target_size, position = read_bps_number(patch, position)
    metadata_size, position = read_bps_number(patch, position)
    position += metadata_size
    if source_size != len(source):
        raise RuntimeError("BPS source size 불일치")
    output = bytearray()
    action_end = len(patch) - 12
    while position < action_end and len(output) < target_size:
        action, position = read_bps_number(patch, position)
        mode = action & 3
        length = (action >> 2) + 1
        if mode == 0:
            start = len(output)
            output.extend(source[start:start + length])
        elif mode == 1:
            output.extend(patch[position:position + length])
            position += length
        else:
            raise RuntimeError("이 빌더가 생성하지 않는 BPS copy 모드가 발견되었습니다.")
    if len(output) != target_size:
        raise RuntimeError("BPS target size 불일치")
    source_crc, target_crc, patch_crc = struct.unpack_from("<III", patch, len(patch) - 12)
    if source_crc != (zlib.crc32(source) & 0xFFFFFFFF):
        raise RuntimeError("BPS source CRC 불일치")
    if target_crc != (zlib.crc32(output) & 0xFFFFFFFF):
        raise RuntimeError("BPS target CRC 불일치")
    if patch_crc != (zlib.crc32(patch[:-4]) & 0xFFFFFFFF):
        raise RuntimeError("BPS patch CRC 불일치")
    return bytes(output)


def nds_header_crc(rom: bytearray) -> None:
    crc = 0xFFFF
    for byte in rom[:0x15E]:
        crc ^= byte
        for _ in range(8):
            crc = (crc >> 1) ^ (0xA001 if crc & 1 else 0)
    struct.pack_into("<H", rom, 0x15E, crc)


def nds_device_capacity(size: int) -> int:
    """Return the smallest DS capacity code that can contain *size*."""
    for code in range(13):
        if size <= (1 << (17 + code)):
            return code
    raise RuntimeError("출력 ROM이 NDS 최대 용량 512 MiB를 초과합니다.")


def main() -> None:
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    source = SOURCE_ROM.read_bytes()
    source_sha256 = hashlib.sha256(source).hexdigest()
    if source_sha256 != EXPECTED_SHA256:
        raise RuntimeError(f"원본 SHA-256 불일치: {source_sha256}")

    arm9_offset, arm9_size = struct.unpack_from("<II", source, 0x20)[0], struct.unpack_from("<I", source, 0x2C)[0]
    cave_offset = CAVE_START - ARM9_RAM
    cave_end_offset = CAVE_END - ARM9_RAM
    hook_offset = HOOK_ADDRESS - ARM9_RAM
    stop_hook_offset = STOP_HOOK_ADDRESS - ARM9_RAM
    volume_hook_offset = VOLUME_HOOK_ADDRESS - ARM9_RAM
    arm9 = source[arm9_offset:arm9_offset + arm9_size]
    if arm9[hook_offset:hook_offset + len(EXPECTED_HOOK_BYTES)] != EXPECTED_HOOK_BYTES:
        raise RuntimeError("BGM 훅 원본 바이트가 분석값과 다릅니다.")
    if arm9[stop_hook_offset:stop_hook_offset + len(EXPECTED_STOP_HOOK_BYTES)] != EXPECTED_STOP_HOOK_BYTES:
        raise RuntimeError("BGM stop hook original bytes do not match the analyzed ROM.")
    if arm9[volume_hook_offset:volume_hook_offset + len(EXPECTED_VOLUME_HOOK_BYTES)] != EXPECTED_VOLUME_HOOK_BYTES:
        raise RuntimeError("BGM volume hook original bytes do not match the analyzed ROM.")
    if any(arm9[cave_offset:cave_end_offset]):
        raise RuntimeError("검증된 ARM9 코드 케이브가 더 이상 비어 있지 않습니다.")

    pack_base = align(len(source), 0x200)
    pack, entries, audio_report = collect_streams(pack_base)
    payload, symbols = build_payload(entries)
    payload_offset = symbols["payload_start"] - ARM9_RAM
    if payload_offset < cave_offset or payload_offset + len(payload) > cave_end_offset:
        raise RuntimeError("페이로드 파일 영역이 코드 케이브 밖입니다.")

    target = bytearray(source)
    target[arm9_offset + payload_offset:arm9_offset + payload_offset + len(payload)] = payload
    target[arm9_offset + hook_offset:arm9_offset + hook_offset + 4] = encode_arm_branch(
        HOOK_ADDRESS, symbols["bgm_hook"]
    )
    target[arm9_offset + stop_hook_offset:arm9_offset + stop_hook_offset + 4] = encode_arm_branch(
        STOP_HOOK_ADDRESS, symbols["seq_stop_hook"]
    )
    target[arm9_offset + volume_hook_offset:arm9_offset + volume_hook_offset + 4] = encode_arm_branch(
        VOLUME_HOOK_ADDRESS, symbols["seq_volume_hook"]
    )
    target.extend(b"\xFF" * (pack_base - len(target)))
    target.extend(pack)
    target.extend(b"\xFF" * (align(len(target), 0x200) - len(target)))

    target[0x14] = nds_device_capacity(len(target))
    struct.pack_into("<I", target, 0x80, len(target))
    nds_header_crc(target)

    output_rom = OUT_DIR / OUTPUT_ROM_NAME
    output_bps = OUT_DIR / OUTPUT_BPS_NAME
    output_rom.write_bytes(target)
    bps = make_bps(source, bytes(target))
    if apply_bps(source, bps) != bytes(target):
        raise RuntimeError("BPS 적용 라운드트립 검증 실패")
    output_bps.write_bytes(bps)

    manifest = {
        "source": {
            "path": str(SOURCE_ROM),
            "size": len(source),
            "sha256": source_sha256,
            "crc32": f"{zlib.crc32(source) & 0xFFFFFFFF:08X}",
        },
        "target": {
            "path": str(output_rom),
            "size": len(target),
            "sha256": hashlib.sha256(target).hexdigest(),
            "crc32": f"{zlib.crc32(target) & 0xFFFFFFFF:08X}",
        },
        "patch": {
            "path": str(output_bps),
            "size": output_bps.stat().st_size,
            "sha256": hashlib.sha256(output_bps.read_bytes()).hexdigest(),
        },
        "hook": {
            "address": f"0x{HOOK_ADDRESS:08X}",
            "destination": f"0x{symbols['bgm_hook']:08X}",
            "payload_file_bytes": len(payload),
            "payload_memory_bytes": symbols["payload_end"] - symbols["payload_start"],
            "cave": f"0x{CAVE_START:08X}-0x{CAVE_END:08X}",
        },
        "stop_hook": {
            "address": f"0x{STOP_HOOK_ADDRESS:08X}",
            "destination": f"0x{symbols['seq_stop_hook']:08X}",
        },
        "volume_hook": {
            "address": f"0x{VOLUME_HOOK_ADDRESS:08X}",
            "destination": f"0x{symbols['seq_volume_hook']:08X}",
        },
        "audio": audio_report,
    }
    (OUT_DIR / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    rendered = json.dumps(manifest, ensure_ascii=False, indent=2)
    try:
        print(rendered)
    except UnicodeEncodeError:
        sys.stdout.buffer.write(rendered.encode("utf-8") + b"\n")


if __name__ == "__main__":
    main()
