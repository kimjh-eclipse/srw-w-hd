# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

import os
import struct
import sys
import tempfile
import unittest
import wave
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import bgm_pack  # noqa: E402
import build  # noqa: E402
import gui_patcher  # noqa: E402
import strm_codec  # noqa: E402


def make_strm(path: Path, bgm_id: int) -> bytes:
    samples = [max(-32768, min(32767, -16000 + bgm_id * 400 + i * 8)) for i in range(768)]
    pcm = struct.pack("<768h", *samples)
    data, _info = strm_codec.make_strm(pcm, 1)
    path.write_bytes(data)
    return pcm


def make_stereo_strm(path: Path) -> bytes:
    values = [value for index in range(768) for value in (index * 20, -index * 20)]
    pcm = struct.pack("<1536h", *values)
    data, _info = strm_codec.make_strm(pcm, 2)
    path.write_bytes(data)
    return pcm


class RobustMappingTests(unittest.TestCase):
    def test_natural_filename_order_is_stable(self) -> None:
        paths = gui_patcher.natural_sort_paths([
            "track10.mp3", "track2.mp3", "TRACK01.mp3", "track1b.mp3",
        ])
        self.assertEqual(
            [path.name for path in paths],
            ["TRACK01.mp3", "track1b.mp3", "track2.mp3", "track10.mp3"],
        )

    def test_all_70_ids_survive_randomized_pack_encoding(self) -> None:
        with tempfile.TemporaryDirectory(prefix="srww_mapping_test_") as temp_name:
            root = Path(temp_name)
            source = root / "source"
            first = root / "first"
            second = root / "second"
            source.mkdir()
            tracks: list[tuple[int, Path]] = []
            for bgm_id in range(70):
                path = source / f"{bgm_id:04d}.strm"
                make_strm(path, bgm_id)
                tracks.append((bgm_id, path))

            pack_a = root / "a.bgm.pak"
            pack_b = root / "b.bgm.pak"
            bgm_pack.write_pack(tracks, pack_a, lambda _line: None)
            bgm_pack.write_pack(tracks, pack_b, lambda _line: None)
            self.assertNotEqual(pack_a.read_bytes(), pack_b.read_bytes())

            index_a = bgm_pack.inspect_pack(pack_a)
            index_b = bgm_pack.inspect_pack(pack_b)
            expected_ids = list(range(70))
            self.assertEqual([row["bgm_id"] for row in index_a["tracks"]], expected_ids)
            self.assertEqual([row["bgm_id"] for row in index_b["tracks"]], expected_ids)

            bgm_pack.extract_pack(pack_a, first, lambda _line: None)
            bgm_pack.extract_pack(pack_b, second, lambda _line: None)
            for bgm_id in expected_ids:
                self.assertEqual(
                    (first / f"{bgm_id:04d}.strm").read_bytes(),
                    (second / f"{bgm_id:04d}.strm").read_bytes(),
                )

    def test_sidecar_and_recent_package_record(self) -> None:
        with tempfile.TemporaryDirectory(prefix="srww_recent_test_") as temp_name:
            root = Path(temp_name)
            source = root / "0034.strm"
            make_strm(source, 34)
            package = root / "test.bgm.pak"
            manifest = bgm_pack.write_pack([(34, source)], package, lambda _line: None)
            manifest["tracks"][0]["source_file"] = "34_song.wav"

            with mock.patch.dict(os.environ, {"LOCALAPPDATA": str(root / "local")}):
                gui_patcher.write_pack_sidecar(manifest)
                gui_patcher.remember_recent_pack(package, manifest)
                self.assertEqual(gui_patcher.load_recent_pack(), package.resolve())
                detail = gui_patcher.pack_detail_text(package)
                self.assertIn("34_song.wav", detail)
                self.assertIn("34", detail)

    def test_adpcm_codec_roundtrip_has_bounded_error(self) -> None:
        samples = [int(14000 * ((index % 96) - 48) / 48) for index in range(384)]
        encoded, _predictor, _index = strm_codec.encode_adpcm_block(samples)
        decoded = strm_codec.decode_adpcm_block(encoded, len(samples))
        mean_error = sum(abs(a - b) for a, b in zip(samples, decoded)) / len(samples)
        self.assertEqual(len(encoded), strm_codec.BLOCK_SIZE)
        self.assertLess(mean_error, 1500)

    def test_build_accepts_mono_and_stereo_adpcm_strm(self) -> None:
        with tempfile.TemporaryDirectory(prefix="srww_stereo_test_") as temp_name:
            root = Path(temp_name)
            mono_path = root / "0033.strm"
            stereo_path = root / "0034.strm"
            make_strm(mono_path, 33)
            make_stereo_strm(stereo_path)

            mono = build.parse_strm(mono_path)
            stereo = build.parse_strm(stereo_path)
            self.assertEqual(mono["channels"], 1)
            self.assertEqual(stereo["channels"], 2)
            self.assertEqual(stereo["block_size"], strm_codec.BLOCK_SIZE)
            self.assertEqual(stereo["block_count"], 2)

            old_dir = build.STRM_DIR
            try:
                build.STRM_DIR = root
                _pack, entries, report = build.collect_streams(0x04000000)
            finally:
                build.STRM_DIR = old_dir
            self.assertEqual(entries[0]["block_count_flags"] >> 31, 0)
            self.assertEqual(entries[1]["block_count_flags"] >> 31, 1)
            self.assertEqual(report[1]["channel_mode"], "stereo")

    def test_pcm_nwav_and_old_pack_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="srww_reject_test_") as temp_name:
            root = Path(temp_name)
            nwav = root / "0000.nwav"
            nwav.write_bytes(b"NWAV" + bytes(128))
            with self.assertRaisesRegex(ValueError, "STRM"):
                strm_codec.parse_strm(nwav)
            old_pack = root / "old.bgm.pak"
            old_pack.write_bytes(b"SRWBGP2\0" + bytes(64))
            with self.assertRaisesRegex(ValueError, "지원하지 않거나 손상"):
                bgm_pack.inspect_pack(old_pack)

    def test_corrupt_adpcm_block_state_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="srww_corrupt_test_") as temp_name:
            path = Path(temp_name) / "0000.strm"
            make_strm(path, 0)
            damaged = bytearray(path.read_bytes())
            damaged[strm_codec.HEADER_SIZE + 2] = 89
            path.write_bytes(damaged)
            with self.assertRaisesRegex(ValueError, "block state"):
                strm_codec.parse_strm(path)

    def test_audio_conversion_applies_transition_filters(self) -> None:
        with tempfile.TemporaryDirectory(prefix="srww_filter_test_") as temp_name:
            root = Path(temp_name)
            source = root / "source.raw"
            destination = root / "0000.strm"
            source.write_bytes(b"input")
            captured: list[str] = []

            def fake_ffmpeg(command: list[str]) -> None:
                captured.extend(command)
                with wave.open(command[-1], "wb") as output:
                    output.setnchannels(1)
                    output.setsampwidth(2)
                    output.setframerate(gui_patcher.SAMPLE_RATE)
                    output.writeframes(struct.pack("<768h", *([1000] * 768)))

            with mock.patch.object(gui_patcher, "_run_ffmpeg", side_effect=fake_ffmpeg):
                gui_patcher.convert_audio_to_strm(source, destination, Path("ffmpeg.exe"))

            self.assertIn("-af", captured)
            self.assertIn(gui_patcher.AUDIO_FILTER, captured)
            self.assertIn("latency=1", gui_patcher.AUDIO_FILTER)
            self.assertNotIn("afade", gui_patcher.AUDIO_FILTER)
            self.assertEqual(strm_codec.parse_strm(destination)["channels"], 1)

    def test_runtime_build_rejects_non_22050_strm(self) -> None:
        with tempfile.TemporaryDirectory(prefix="srww_rate_test_") as temp_name:
            path = Path(temp_name) / "0000.strm"
            pcm = struct.pack("<768h", *([0] * 768))
            data, _info = strm_codec.make_strm(pcm, 1, 16000)
            path.write_bytes(data)
            with self.assertRaisesRegex(ValueError, "22050 Hz"):
                build.parse_strm(path)


if __name__ == "__main__":
    unittest.main()
