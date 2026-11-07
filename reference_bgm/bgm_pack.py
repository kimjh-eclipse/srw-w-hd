# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

import hashlib
import os
import struct
import tempfile
import zlib
from pathlib import Path
from typing import Callable, Iterable

import strm_codec


PACK_MAGIC = b"SRWBGP3\0"
PACK_VERSION = 3
PACK_FLAGS = 0x0003  # zlib-compressed and XOR-stream encoded
PACK_HEADER = struct.Struct("<8sHH16sI")
ENTRY_HEADER = struct.Struct("<4sHHQQ32s")
ENTRY_MAGIC = b"TRAK"
CHUNK_SIZE = 1024 * 1024
PACK_KEY = bytes.fromhex(
    "97a84f21d91e7a6b4cfe0dc9276d835f"
    "8c463a0b5ef274a3b8e92d1061f533ca"
)
Log = Callable[[str], None]


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(CHUNK_SIZE):
            digest.update(chunk)
    return digest.hexdigest()


def _entry_seed(salt: bytes, bgm_id: int) -> bytes:
    return hashlib.sha256(PACK_KEY + salt + struct.pack("<H", bgm_id)).digest()


def _xor_stream(data: bytes, seed: bytes, offset: int) -> bytes:
    output = bytearray(len(data))
    position = 0
    while position < len(data):
        absolute = offset + position
        counter, skip = divmod(absolute, 32)
        block = hashlib.sha256(seed + struct.pack("<Q", counter)).digest()
        count = min(len(data) - position, 32 - skip)
        for index in range(count):
            output[position + index] = data[position + index] ^ block[skip + index]
        position += count
    return bytes(output)


def _compress_to_temp(source: Path) -> tuple[Path, int, bytes]:
    digest = hashlib.sha256()
    raw_size = 0
    handle = tempfile.NamedTemporaryFile(prefix="srww_pack_", suffix=".z", delete=False)
    compressed_path = Path(handle.name)
    compressor = zlib.compressobj(level=9)
    try:
        with source.open("rb") as input_stream, handle:
            while chunk := input_stream.read(CHUNK_SIZE):
                digest.update(chunk)
                raw_size += len(chunk)
                encoded = compressor.compress(chunk)
                if encoded:
                    handle.write(encoded)
            handle.write(compressor.flush())
        return compressed_path, raw_size, digest.digest()
    except Exception:
        compressed_path.unlink(missing_ok=True)
        raise


def write_pack(
    tracks: Iterable[tuple[int, Path]],
    destination: Path,
    log: Log = print,
) -> dict[str, object]:
    rows = sorted((int(bgm_id), Path(path)) for bgm_id, path in tracks)
    if not rows:
        raise ValueError("BGM.PAK에 넣을 음원이 없습니다.")
    if len({bgm_id for bgm_id, _ in rows}) != len(rows):
        raise ValueError("BGM.PAK의 BGM ID가 중복되었습니다.")
    for bgm_id, path in rows:
        if not 0 <= bgm_id < 70:
            raise ValueError(f"BGM ID 범위는 0~69입니다: {bgm_id}")
        if not path.is_file():
            raise FileNotFoundError(path)
        try:
            strm_codec.parse_strm(path)
        except ValueError as exc:
            raise ValueError(f"BGM {bgm_id:02d} is not a supported ADPCM STRM: {exc}") from exc

    destination = Path(destination).resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + ".tmp")
    salt = os.urandom(16)
    report: list[dict[str, object]] = []
    try:
        with temporary.open("wb") as output:
            output.write(PACK_HEADER.pack(PACK_MAGIC, PACK_VERSION, PACK_FLAGS, salt, len(rows)))
            for index, (bgm_id, path) in enumerate(rows, 1):
                log(f"[{index}/{len(rows)}] BGM {bgm_id:02d} 패키지 부호화 중")
                compressed_path, raw_size, digest = _compress_to_temp(path)
                try:
                    stored_size = compressed_path.stat().st_size
                    output.write(ENTRY_HEADER.pack(
                        ENTRY_MAGIC, bgm_id, 0, raw_size, stored_size, digest
                    ))
                    seed = _entry_seed(salt, bgm_id)
                    offset = 0
                    with compressed_path.open("rb") as compressed:
                        while chunk := compressed.read(CHUNK_SIZE):
                            output.write(_xor_stream(chunk, seed, offset))
                            offset += len(chunk)
                finally:
                    compressed_path.unlink(missing_ok=True)
                report.append({
                    "bgm_id": bgm_id,
                    "strm_bytes": raw_size,
                    "sha256": digest.hex(),
                })
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)

    return {
        "format": "SRW W BGM.PAK v3 (ADPCM STRM)",
        "path": str(destination),
        "size": destination.stat().st_size,
        "sha256": file_sha256(destination),
        "track_count": len(report),
        "tracks": report,
    }


def inspect_pack(source: Path) -> dict[str, object]:
    """Read and validate the package index without decoding the audio bodies."""
    source = Path(source).resolve()
    if not source.is_file():
        raise FileNotFoundError(f"BGM.PAK 파일이 없습니다: {source}")

    file_size = source.stat().st_size
    tracks: list[dict[str, object]] = []
    seen: set[int] = set()
    with source.open("rb") as stream:
        header = stream.read(PACK_HEADER.size)
        if len(header) != PACK_HEADER.size:
            raise ValueError("BGM.PAK 헤더가 잘렸습니다.")
        magic, version, flags, _salt, count = PACK_HEADER.unpack(header)
        if magic != PACK_MAGIC or version != PACK_VERSION or flags != PACK_FLAGS:
            raise ValueError("지원하지 않거나 손상된 BGM.PAK입니다.")
        if not 1 <= count <= 70:
            raise ValueError(f"BGM.PAK 트랙 수가 올바르지 않습니다: {count}")

        for _ in range(count):
            raw_header = stream.read(ENTRY_HEADER.size)
            if len(raw_header) != ENTRY_HEADER.size:
                raise ValueError("BGM.PAK 트랙 헤더가 잘렸습니다.")
            tag, bgm_id, reserved, raw_size, stored_size, digest = ENTRY_HEADER.unpack(raw_header)
            if tag != ENTRY_MAGIC or reserved != 0 or bgm_id >= 70 or bgm_id in seen:
                raise ValueError("BGM.PAK 트랙 테이블이 올바르지 않습니다.")
            if stored_size > file_size - stream.tell():
                raise ValueError(f"BGM {bgm_id:02d} 데이터가 잘렸습니다.")
            seen.add(bgm_id)
            tracks.append({
                "bgm_id": bgm_id,
                "strm_bytes": raw_size,
                "stored_bytes": stored_size,
                "sha256": digest.hex(),
            })
            stream.seek(stored_size, 1)

        if stream.tell() != file_size:
            raise ValueError("BGM.PAK 끝에 알 수 없는 데이터가 있습니다.")

    return {
        "format": "SRW W BGM.PAK v3 (ADPCM STRM)",
        "path": str(source),
        "size": file_size,
        "track_count": len(tracks),
        "tracks": tracks,
    }


def extract_pack(
    source: Path,
    destination: Path,
    log: Log = print,
) -> dict[str, object]:
    source = Path(source).resolve()
    destination = Path(destination).resolve()
    if not source.is_file():
        raise FileNotFoundError(f"BGM.PAK 파일이 없습니다: {source}")
    destination.mkdir(parents=True, exist_ok=True)
    report: list[dict[str, object]] = []
    seen: set[int] = set()

    with source.open("rb") as stream:
        header = stream.read(PACK_HEADER.size)
        if len(header) != PACK_HEADER.size:
            raise ValueError("BGM.PAK 헤더가 잘렸습니다.")
        magic, version, flags, salt, count = PACK_HEADER.unpack(header)
        if magic != PACK_MAGIC or version != PACK_VERSION or flags != PACK_FLAGS:
            raise ValueError("지원하지 않거나 손상된 BGM.PAK입니다.")
        if not 1 <= count <= 70:
            raise ValueError(f"BGM.PAK 트랙 수가 올바르지 않습니다: {count}")

        for index in range(1, count + 1):
            raw_header = stream.read(ENTRY_HEADER.size)
            if len(raw_header) != ENTRY_HEADER.size:
                raise ValueError("BGM.PAK 트랙 헤더가 잘렸습니다.")
            tag, bgm_id, reserved, raw_size, stored_size, expected_digest = ENTRY_HEADER.unpack(raw_header)
            if tag != ENTRY_MAGIC or reserved != 0 or bgm_id >= 70 or bgm_id in seen:
                raise ValueError("BGM.PAK 트랙 테이블이 올바르지 않습니다.")
            seen.add(bgm_id)
            log(f"[{index}/{count}] BGM {bgm_id:02d} 패키지 검증 중")
            destination_path = destination / f"{bgm_id:04d}.strm"
            temporary_path = destination_path.with_suffix(".strm.tmp")
            seed = _entry_seed(salt, bgm_id)
            remaining = stored_size
            encoded_offset = 0
            digest = hashlib.sha256()
            actual_size = 0
            decompressor = zlib.decompressobj()
            try:
                with temporary_path.open("wb") as output:
                    while remaining:
                        chunk = stream.read(min(CHUNK_SIZE, remaining))
                        if not chunk:
                            raise ValueError("BGM.PAK 트랙 데이터가 잘렸습니다.")
                        remaining -= len(chunk)
                        decoded = _xor_stream(chunk, seed, encoded_offset)
                        encoded_offset += len(chunk)
                        raw = decompressor.decompress(decoded)
                        if raw:
                            output.write(raw)
                            digest.update(raw)
                            actual_size += len(raw)
                    tail = decompressor.flush()
                    if tail:
                        output.write(tail)
                        digest.update(tail)
                        actual_size += len(tail)
                if not decompressor.eof or actual_size != raw_size or digest.digest() != expected_digest:
                    raise ValueError(f"BGM {bgm_id:02d} 무결성 검증에 실패했습니다.")
                strm_codec.parse_strm(temporary_path)
                os.replace(temporary_path, destination_path)
            finally:
                temporary_path.unlink(missing_ok=True)
            report.append({
                "bgm_id": bgm_id,
                "strm_bytes": actual_size,
                "sha256": expected_digest.hex(),
            })

        if stream.read(1):
            raise ValueError("BGM.PAK 끝에 알 수 없는 데이터가 있습니다.")

    return {
        "format": "SRW W BGM.PAK v3 (ADPCM STRM)",
        "path": str(source),
        "size": source.stat().st_size,
        "sha256": file_sha256(source),
        "track_count": len(report),
        "tracks": report,
    }
