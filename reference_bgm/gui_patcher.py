# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import struct
import subprocess
import tempfile
import traceback
import wave
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterable

import bgm_pack
import build
import strm_codec


ROOT = Path(os.environ.get("SRWW_ASSET_ROOT", Path(__file__).resolve().parent))
DEFAULT_ROM = ROOT / "input.nds"
DEFAULT_OUTPUT = ROOT / "out" / "custom"
DEFAULT_PACK = ROOT / "out" / "custom.bgm.pak"
CATALOG_PATH = ROOT / "bgm_catalog.json"
SAMPLE_RATE = 22_050
AUDIO_FILTER = (
    "highpass=f=20,lowpass=f=9500,volume=0.70,"
    "alimiter=limit=0.95:attack=5:release=50:level=0:latency=1"
)
SOURCE_ROM_SIZE = 65_414_568
NDS_MAX_SIZE = 512 * 1024 * 1024
ROM_ALIGNMENT = 0x200
# Reserve the worst-case per-track alignment/header overhead for all 70 slots.
# At 22.05 kHz mono IMA-ADPCM this is roughly 11.5 hours of source audio.
MAX_TOTAL_AUDIO_SECONDS = (
    NDS_MAX_SIZE
    - ((SOURCE_ROM_SIZE + ROM_ALIGNMENT - 1) // ROM_ALIGNMENT * ROM_ALIGNMENT)
    - build.BGM_COUNT * (ROM_ALIGNMENT - 1 + strm_codec.HEADER_SIZE)
    - (ROM_ALIGNMENT - 1)
) * strm_codec.BLOCK_SAMPLES // (SAMPLE_RATE * strm_codec.BLOCK_SIZE)
Log = Callable[[str], None]


@dataclass(frozen=True)
class Track:
    bgm_id: int
    source: Path
    channels: int = 1


def load_bgm_catalog(path: Path | None = None) -> list[dict[str, object]]:
    source = path or CATALOG_PATH
    rows = json.loads(source.read_text(encoding="utf-8"))
    if len(rows) != build.BGM_COUNT:
        raise RuntimeError(f"BGM 카탈로그는 {build.BGM_COUNT}곡이어야 합니다.")
    if [row.get("id") for row in rows] != list(range(build.BGM_COUNT)):
        raise RuntimeError("BGM 카탈로그 ID가 00부터 연속적이지 않습니다.")
    return rows


def natural_sort_paths(paths: Iterable[str | Path]) -> list[Path]:
    """Return a stable human/numeric filename order independent of the file dialog."""
    def key(path: Path) -> tuple[tuple[tuple[int, object], ...], str]:
        parts: list[tuple[int, object]] = []
        for part in re.split(r"(\d+)", path.name.casefold()):
            parts.append((0, int(part)) if part.isdigit() else (1, part))
        return tuple(parts), str(path.resolve()).casefold()

    return sorted((Path(path) for path in paths), key=key)


def pack_sidecar_path(package: Path) -> Path:
    package = Path(package).resolve()
    return package.with_name(package.name + ".manifest.json")


def recent_pack_record_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    return base / "SRW_W_BGM_Patcher" / "recent_pack.json"


def remember_recent_pack(package: Path, manifest: dict[str, object]) -> None:
    record_path = recent_pack_record_path()
    record_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = record_path.with_suffix(".tmp")
    data = {
        "path": str(Path(package).resolve()),
        "size": int(manifest["size"]),
        "sha256": str(manifest["sha256"]),
        "track_count": int(manifest["track_count"]),
        "updated_utc": datetime.now(timezone.utc).isoformat(),
    }
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, record_path)


def load_recent_pack() -> Path | None:
    record_path = recent_pack_record_path()
    try:
        data = json.loads(record_path.read_text(encoding="utf-8"))
        package = Path(data["path"]).resolve()
        if package.is_file() and package.stat().st_size == int(data["size"]):
            return package
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError):
        pass
    return None


def write_pack_sidecar(package_manifest: dict[str, object]) -> Path:
    package = Path(str(package_manifest["path"])).resolve()
    sidecar = pack_sidecar_path(package)
    temporary = sidecar.with_suffix(sidecar.suffix + ".tmp")
    document = {
        "format": "SRW W BGM package manifest v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "package": package_manifest,
    }
    temporary.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    os.replace(temporary, sidecar)
    return sidecar


def load_pack_sidecar(package: Path) -> dict[str, object] | None:
    package = Path(package).resolve()
    sidecar = pack_sidecar_path(package)
    try:
        document = json.loads(sidecar.read_text(encoding="utf-8"))
        manifest = document["package"]
        if (
            document.get("format") == "SRW W BGM package manifest v1"
            and int(manifest["size"]) == package.stat().st_size
            and int(manifest["track_count"]) == len(manifest["tracks"])
        ):
            return document
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError):
        pass
    return None


def describe_pack(package: Path) -> str:
    index = bgm_pack.inspect_pack(package)
    ids = [int(row["bgm_id"]) for row in index["tracks"]]
    ranges = ", ".join(f"{bgm_id:02d}" for bgm_id in ids)
    if len(ranges) > 72:
        ranges = ranges[:69] + "..."
    modified = datetime.fromtimestamp(Path(package).stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    return (
        f"검증됨: {index['track_count']}곡 | ID {ranges} | "
        f"{int(index['size']) / (1024 * 1024):.2f} MiB | 수정 {modified}"
    )


def pack_detail_text(package: Path) -> str:
    package = Path(package).resolve()
    index = bgm_pack.inspect_pack(package)
    sidecar = load_pack_sidecar(package)
    source_by_id: dict[int, dict[str, object]] = {}
    if sidecar is not None:
        source_by_id = {
            int(row["bgm_id"]): row for row in sidecar["package"]["tracks"]
        }
    lines = [
        f"파일: {package}",
        f"크기: {int(index['size']):,} bytes",
        f"포함 곡: {index['track_count']}곡",
        "",
        "BGM ID  게임 BGM 곡명  <-  지정 음원",
    ]
    catalog = load_bgm_catalog()
    for row in index["tracks"]:
        bgm_id = int(row["bgm_id"])
        source = source_by_id.get(bgm_id, {})
        source_name = str(source.get("source_file", "(파일명 정보 없음)"))
        channel_mode = str(source.get("channel_mode", "unknown"))
        lines.append(
            f"{bgm_id:02d}  [{channel_mode}]  {catalog[bgm_id]['title']}  <-  {source_name}"
        )
    if sidecar is None:
        lines.extend(["", "참고: 함께 생성된 manifest.json이 없어 원본 파일명은 표시할 수 없습니다."])
    return "\n".join(lines)


def find_ffmpeg(explicit: str | Path | None = None) -> Path:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit).expanduser())
    if os.environ.get("FFMPEG"):
        candidates.append(Path(os.environ["FFMPEG"]).expanduser())
    path_match = shutil.which("ffmpeg")
    if path_match:
        candidates.append(Path(path_match))
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    raise FileNotFoundError("FFmpeg를 찾지 못했습니다. GUI에서 ffmpeg.exe 위치를 지정하세요.")


def find_devkitarm(explicit: str | Path | None = None) -> Path:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit).expanduser())
    if os.environ.get("DEVKITARM"):
        candidates.append(Path(os.environ["DEVKITARM"]).expanduser())
    candidates.append(Path(r"C:\devkitPro\devkitARM"))
    for candidate in candidates:
        gcc = candidate / "bin" / "arm-none-eabi-gcc.exe"
        objcopy = candidate / "bin" / "arm-none-eabi-objcopy.exe"
        nm = candidate / "bin" / "arm-none-eabi-nm.exe"
        if gcc.is_file() and objcopy.is_file() and nm.is_file():
            return candidate.resolve()
    raise FileNotFoundError("devkitARM을 찾지 못했습니다. GUI에서 devkitARM 폴더를 지정하세요.")


def probe_audio_duration(source: Path, ffmpeg: str | Path | None = None) -> float:
    """Return source duration in seconds without decoding the whole track."""
    source = Path(source).resolve()
    ffmpeg_path = find_ffmpeg(ffmpeg)
    ffprobe_name = "ffprobe.exe" if os.name == "nt" else "ffprobe"
    ffprobe = ffmpeg_path.with_name(ffprobe_name)
    if not ffprobe.is_file():
        match = shutil.which("ffprobe")
        ffprobe = Path(match) if match else ffprobe
    flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    if ffprobe.is_file():
        result = subprocess.run(
            [
                str(ffprobe), "-v", "error", "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1", str(source),
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=flags,
        )
        try:
            duration = float(result.stdout.strip())
            if result.returncode == 0 and duration > 0:
                return duration
        except ValueError:
            pass

    result = subprocess.run(
        [str(ffmpeg_path), "-hide_banner", "-i", str(source)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        creationflags=flags,
    )
    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", result.stdout)
    if not match:
        raise RuntimeError(f"음원 재생시간을 확인하지 못했습니다: {source.name}")
    hours, minutes, seconds = match.groups()
    duration = int(hours) * 3600 + int(minutes) * 60 + float(seconds)
    if duration <= 0:
        raise RuntimeError(f"음원 재생시간이 올바르지 않습니다: {source.name}")
    return duration


def estimated_patched_rom_size(strm_sizes: Iterable[int]) -> int:
    pack_base = (SOURCE_ROM_SIZE + ROM_ALIGNMENT - 1) // ROM_ALIGNMENT * ROM_ALIGNMENT
    local_size = 0
    for size in strm_sizes:
        local_size = (local_size + ROM_ALIGNMENT - 1) // ROM_ALIGNMENT * ROM_ALIGNMENT
        local_size += int(size)
    result = pack_base + local_size
    return (result + ROM_ALIGNMENT - 1) // ROM_ALIGNMENT * ROM_ALIGNMENT


def validate_tracks(tracks: Iterable[Track]) -> list[Track]:
    result = list(tracks)
    if not result:
        raise ValueError("추가된 음원이 없습니다.")
    seen: set[int] = set()
    for track in result:
        if not 0 <= track.bgm_id < build.BGM_COUNT:
            raise ValueError(f"BGM ID 범위는 0~{build.BGM_COUNT - 1}입니다: {track.bgm_id}")
        if track.bgm_id in seen:
            raise ValueError(f"BGM ID가 중복되었습니다: {track.bgm_id}")
        if not track.source.is_file():
            raise FileNotFoundError(f"음원 파일이 없습니다: {track.source}")
        if track.channels not in (1, 2):
            raise ValueError(f"채널 수는 모노(1) 또는 스테레오(2)여야 합니다: {track.channels}")
        seen.add(track.bgm_id)
    return sorted(result, key=lambda item: item.bgm_id)


def _run_ffmpeg(command: list[str]) -> None:
    flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    result = subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        creationflags=flags,
    )
    if result.returncode:
        tail = "\n".join(result.stdout.splitlines()[-20:])
        raise RuntimeError(f"FFmpeg 변환 실패:\n{tail}")


def convert_audio_to_strm(
    source: Path,
    destination: Path,
    ffmpeg: Path,
    channels: int = 1,
) -> dict[str, int]:
    if channels not in (1, 2):
        raise ValueError(f"채널 수는 1 또는 2여야 합니다: {channels}")
    source = source.resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="srww_audio_") as temp_name:
        wav_path = Path(temp_name) / "decoded.wav"
        _run_ffmpeg([
            str(ffmpeg), "-hide_banner", "-loglevel", "error", "-y",
            "-i", str(source), "-vn", "-map_metadata", "-1",
            "-ac", str(channels), "-ar", str(SAMPLE_RATE),
            "-af", AUDIO_FILTER,
            "-c:a", "pcm_s16le", "-f", "wav", str(wav_path),
        ])
        with wave.open(str(wav_path), "rb") as reader:
            if reader.getnchannels() != channels or reader.getsampwidth() != 2:
                raise RuntimeError(f"FFmpeg 출력이 {channels}채널 PCM16 형식이 아닙니다.")
            frame_count = reader.getnframes()
            pcm = reader.readframes(frame_count)
            sample_rate = reader.getframerate()
    data, info = strm_codec.make_strm(pcm, channels, sample_rate)
    destination.write_bytes(data)
    return info


def normalized_pack_path(path: Path) -> Path:
    path = Path(path).resolve()
    if not path.name.lower().endswith(".bgm.pak"):
        path = path.with_name(path.name + ".bgm.pak")
    return path


def create_bgm_pack(
    tracks: Iterable[Track],
    output_pack: Path,
    ffmpeg: str | Path | None = None,
    log: Log = print,
) -> dict[str, object]:
    track_list = validate_tracks(tracks)
    catalog = load_bgm_catalog()
    ffmpeg_path = find_ffmpeg(ffmpeg)
    output_pack = normalized_pack_path(output_pack)
    stream_info: dict[int, dict[str, int]] = {}
    with tempfile.TemporaryDirectory(prefix="srww_strm_") as temp_name:
        strm_dir = Path(temp_name)
        strm_tracks: list[tuple[int, Path]] = []
        for index, track in enumerate(track_list, 1):
            log(f"[{index}/{len(track_list)}] BGM {track.bgm_id:02d}: {track.source.name} 변환 중")
            destination = strm_dir / f"{track.bgm_id:04d}.strm"
            info = convert_audio_to_strm(
                track.source, destination, ffmpeg_path, track.channels
            )
            stream_info[track.bgm_id] = info
            seconds = info["samples"] / info["sample_rate"]
            mode = "mono" if track.channels == 1 else "stereo"
            log(f"    {info['sample_rate']} Hz / {mode} IMA-ADPCM STRM / {seconds:.2f}초")
            strm_tracks.append((track.bgm_id, destination))
        estimated_size = estimated_patched_rom_size(path.stat().st_size for _, path in strm_tracks)
        if estimated_size > NDS_MAX_SIZE:
            raise ValueError(
                "선택한 음원의 합계가 NDS 최대 용량을 초과합니다. "
                "음원 길이를 줄인 뒤 다시 시도하세요."
            )
        manifest = bgm_pack.write_pack(strm_tracks, output_pack, log)
    source_by_id = {track.bgm_id: track for track in track_list}
    for row in manifest["tracks"]:
        bgm_id = int(row["bgm_id"])
        track = source_by_id[bgm_id]
        row["title"] = str(catalog[bgm_id]["title"])
        row["source_file"] = track.source.resolve().name
        row["channels"] = track.channels
        row["channel_mode"] = "mono" if track.channels == 1 else "stereo"
        row["samples"] = stream_info[bgm_id]["samples"]
        row["block_count"] = stream_info[bgm_id]["block_count"]
        row["duration_seconds"] = stream_info[bgm_id]["samples"] / SAMPLE_RATE
    log(f"BGM.PAK 생성 완료: {output_pack}")
    try:
        sidecar = write_pack_sidecar(manifest)
        manifest["manifest_path"] = str(sidecar)
        log(f"ID/파일명 매핑 기록: {sidecar}")
    except OSError as exc:
        log(f"주의: 보조 매핑 문서를 저장하지 못했습니다: {exc}")
    try:
        remember_recent_pack(output_pack, manifest)
    except OSError as exc:
        log(f"주의: 최근 PAK 자동 연결 정보를 저장하지 못했습니다: {exc}")
    return {"operation": "make_pack", "package": manifest}


def apply_bgm_pack(
    rom: Path,
    package: Path,
    output_dir: Path,
    devkitarm: str | Path | None = None,
    log: Log = print,
) -> dict[str, object]:
    rom = Path(rom).resolve()
    package = Path(package).resolve()
    output_dir = Path(output_dir).resolve()
    if not rom.is_file():
        raise FileNotFoundError(f"원본 ROM이 없습니다: {rom}")
    toolchain = find_devkitarm(devkitarm)
    output_dir.mkdir(parents=True, exist_ok=True)
    build.WORK_DIR.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="srww_unpack_", dir=build.WORK_DIR) as temp_name:
        strm_dir = Path(temp_name)
        package_manifest = bgm_pack.extract_pack(package, strm_dir, log)
        safe_stem = rom.stem
        old_values = (
            build.SOURCE_ROM, build.STRM_DIR, build.OUT_DIR,
            build.OUTPUT_ROM_NAME, build.OUTPUT_BPS_NAME,
            build.CC, build.OBJCOPY, build.NM,
        )
        try:
            build.SOURCE_ROM = rom
            build.STRM_DIR = strm_dir
            build.OUT_DIR = output_dir
            build.OUTPUT_ROM_NAME = f"{safe_stem} [Custom STRM BGM].nds"
            build.OUTPUT_BPS_NAME = f"{safe_stem} [Custom STRM BGM].bps"
            build.CC = toolchain / "bin" / "arm-none-eabi-gcc.exe"
            build.OBJCOPY = toolchain / "bin" / "arm-none-eabi-objcopy.exe"
            build.NM = toolchain / "bin" / "arm-none-eabi-nm.exe"
            log("ARM9 스트리밍 엔진 컴파일 및 ROM 생성 중")
            build.main()
            manifest_path = output_dir / "build_manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["bgm_package"] = {
                "path": str(package),
                "size": package_manifest["size"],
                "sha256": package_manifest["sha256"],
                "track_count": package_manifest["track_count"],
            }
            manifest_path.write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
        finally:
            (
                build.SOURCE_ROM, build.STRM_DIR, build.OUT_DIR,
                build.OUTPUT_ROM_NAME, build.OUTPUT_BPS_NAME,
                build.CC, build.OBJCOPY, build.NM,
            ) = old_values
    log("완료: 원본 ROM과 BGM.PAK은 변경하지 않았습니다.")
    return {"operation": "apply_pack", "package": package_manifest, "build": manifest}


def parse_track(value: str) -> Track:
    try:
        raw_id, raw_path = value.split("=", 1)
        return Track(int(raw_id, 0), Path(raw_path))
    except (ValueError, TypeError) as exc:
        raise argparse.ArgumentTypeError("--track 형식은 BGM_ID=음원경로 입니다.") from exc


def _execute(args: argparse.Namespace, log: Log) -> dict[str, object]:
    if args.make_pack:
        return create_bgm_pack(args.track, args.pack_out, args.ffmpeg, log)
    return apply_bgm_pack(args.rom, args.pack, args.output_dir, args.devkitarm, log)


def main() -> int:
    parser = argparse.ArgumentParser(description="SRW W 2단계 커스텀 BGM 패처")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--make-pack", action="store_true", help="음원으로 BGM.PAK 생성")
    mode.add_argument("--apply-pack", action="store_true", help="BGM.PAK을 NDS ROM에 결합")
    parser.add_argument("--pack", type=Path, default=DEFAULT_PACK)
    parser.add_argument("--pack-out", type=Path, default=DEFAULT_PACK)
    parser.add_argument("--rom", type=Path, default=DEFAULT_ROM)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--ffmpeg", type=Path)
    parser.add_argument("--devkitarm", type=Path)
    parser.add_argument("--track", action="append", type=parse_track, default=[])
    parser.add_argument("--status-file", type=Path)
    args = parser.parse_args()

    if args.status_file:
        logs: list[str] = []
        exit_code = 0
        try:
            manifest = _execute(args, logs.append)
            status: dict[str, object] = {"success": True, "logs": logs, "manifest": manifest}
        except Exception as exc:
            exit_code = 1
            status = {
                "success": False,
                "logs": logs,
                "error": str(exc),
                "traceback": traceback.format_exc(),
            }
        args.status_file.parent.mkdir(parents=True, exist_ok=True)
        args.status_file.write_text(
            json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        return exit_code

    print(json.dumps(_execute(args, print), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
