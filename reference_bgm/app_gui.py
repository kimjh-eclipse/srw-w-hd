# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

import os
import queue
import shutil
import threading
import traceback
from pathlib import Path
from typing import Callable

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText

import gui_patcher


ROOT = Path(os.environ.get("SRWW_ASSET_ROOT", Path(__file__).resolve().parent))
AUDIO_TYPES = [
    ("오디오 파일", "*.mp3 *.wav *.flac *.ogg *.m4a *.aac *.wma *.opus *.aiff *.aif"),
    ("모든 파일", "*.*"),
]


class StageGui:
    def __init__(self, mode: str, self_test: bool = False) -> None:
        if mode not in {"pack", "patch"}:
            raise ValueError(f"지원하지 않는 GUI 모드입니다: {mode}")
        self.mode = mode
        self.self_test = self_test
        self.root = tk.Tk()
        if mode == "pack":
            self.root.title("슈퍼로봇대전 W BGM.PAK 제작기")
            self.root.geometry("940x760")
            self.root.minsize(860, 680)
        else:
            self.root.title("슈퍼로봇대전 W BGM ROM 패처")
            self.root.geometry("820x440")
            self.root.minsize(760, 400)
        if self_test:
            self.root.withdraw()

        base_output = Path(os.environ.get("SRWW_DEFAULT_OUTPUT", ROOT / "out"))
        recent_pack = None if self_test else gui_patcher.load_recent_pack()
        initial_pack = recent_pack or (base_output / "custom.bgm.pak")
        default_rom = os.environ.get("SRWW_DEFAULT_ROM", "")
        ffmpeg = os.environ.get("SRWW_FFMPEG") or shutil.which("ffmpeg") or ""
        devkit = os.environ.get("DEVKITARM", "")
        if not devkit and Path(r"C:\devkitPro\devkitARM").is_dir():
            devkit = r"C:\devkitPro\devkitARM"

        self.ffmpeg_var = tk.StringVar(value=ffmpeg)
        self.pack_out_var = tk.StringVar(value=str(base_output / "custom.bgm.pak"))
        self.rom_var = tk.StringVar(value=default_rom)
        self.pack_in_var = tk.StringVar(value=str(initial_pack))
        self.initial_pack_path = str(initial_pack)
        self.pack_path_user_selected = False
        self.pack_summary_var = tk.StringVar(value="BGM.PAK을 선택하면 포함 ID를 검사합니다.")
        self.rom_out_var = tk.StringVar(value=str(base_output / "rom"))
        self.devkit_var = tk.StringVar(value=devkit)
        self.current_var = tk.StringVar(value="현재 BGM ID: 00")
        self.duration_var = tk.StringVar()
        self.channel_mode_var = tk.StringVar(value="모노 (1채널)")
        self.status_var = tk.StringVar(
            value=(
                "음원을 선택해 BGM.PAK을 만듭니다."
                if mode == "pack" else "BGM.PAK과 원본 ROM을 합쳐 패치를 만듭니다."
            )
        )
        self.tracks: dict[int, Path] = {}
        self.track_durations: dict[int, float] = {}
        self.track_channels: dict[int, int] = {}
        self.events: queue.Queue[tuple[str, object]] = queue.Queue()
        self.active_controls: list[tk.Widget] = []
        self.working = False

        outer = ttk.Frame(self.root, padding=12)
        outer.pack(fill="both", expand=True)
        outer.rowconfigure(0, weight=1)
        outer.columnconfigure(0, weight=1)

        self.content = ttk.Frame(outer, padding=12)
        self.content.grid(row=0, column=0, sticky="nsew")
        if mode == "pack":
            self.pack_tab = self.content
            self._build_pack_tab()
        else:
            self.rom_tab = self.content
            self._build_rom_tab()
            self._refresh_pack_summary()

        ttk.Label(outer, text="작업 로그").grid(row=1, column=0, sticky="w", pady=(10, 3))
        self.log_box = ScrolledText(outer, height=7, state="disabled", font=("Consolas", 9))
        self.log_box.grid(row=2, column=0, sticky="nsew")
        outer.rowconfigure(2, weight=0)

        bottom = ttk.Frame(outer)
        bottom.grid(row=3, column=0, sticky="ew", pady=(8, 0))
        bottom.columnconfigure(0, weight=1)
        ttk.Label(bottom, textvariable=self.status_var).grid(row=0, column=0, sticky="w")
        self.progress = ttk.Progressbar(bottom, mode="indeterminate", length=190)
        self.progress.grid(row=0, column=1, padx=(10, 0))

        self.root.protocol("WM_DELETE_WINDOW", self._close)
        self.root.after(100, self._poll_events)

    def _path_row(
        self,
        parent: ttk.Frame,
        row: int,
        label: str,
        variable: tk.StringVar,
        command: Callable[[], None],
    ) -> None:
        ttk.Label(parent, text=label, width=16).grid(row=row, column=0, sticky="w", pady=3)
        ttk.Entry(parent, textvariable=variable).grid(row=row, column=1, sticky="ew", pady=3)
        ttk.Button(parent, text="찾기...", command=command).grid(row=row, column=2, padx=(6, 0), pady=3)
        parent.columnconfigure(1, weight=1)

    def _build_pack_tab(self) -> None:
        tab = self.pack_tab
        tab.rowconfigure(6, weight=1)
        self._path_row(tab, 0, "FFmpeg 실행 파일", self.ffmpeg_var, self._browse_ffmpeg)
        self._path_row(tab, 1, "출력 BGM.PAK", self.pack_out_var, self._browse_pack_output)
        ttk.Label(
            tab,
            text="여러 파일은 파일명 숫자를 인식해 자연 정렬한 뒤 ID 순서로 배치합니다.",
            foreground="#555555",
        ).grid(row=2, column=0, columnspan=3, sticky="w", pady=(5, 3))
        duration_box = ttk.LabelFrame(tab, text="선택한 음원 재생시간", padding=8)
        duration_box.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(5, 7))
        duration_box.columnconfigure(0, weight=1)
        self.duration_progress = ttk.Progressbar(
            duration_box,
            mode="determinate",
            maximum=gui_patcher.MAX_TOTAL_AUDIO_SECONDS,
        )
        self.duration_progress.grid(row=0, column=0, sticky="ew")
        ttk.Label(duration_box, textvariable=self.duration_var).grid(
            row=1, column=0, sticky="w", pady=(5, 0)
        )
        ttk.Label(tab, textvariable=self.current_var, font=("Malgun Gothic", 10, "bold")).grid(
            row=4, column=0, columnspan=3, sticky="w", pady=(4, 5)
        )
        toolbar = ttk.Frame(tab)
        toolbar.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(0, 6))
        self.add_button = ttk.Button(toolbar, text="선택 ID부터 음원 지정", command=self._add_tracks)
        self.add_button.pack(side="left")
        self.remove_button = ttk.Button(toolbar, text="지정 음원 해제", command=self._remove_tracks)
        self.remove_button.pack(side="left", padx=6)
        ttk.Label(toolbar, text="변환:").pack(side="left", padx=(12, 4))
        self.channel_mode_box = ttk.Combobox(
            toolbar,
            textvariable=self.channel_mode_var,
            values=("모노 (1채널)", "스테레오 (2채널)"),
            state="readonly",
            width=15,
        )
        self.channel_mode_box.pack(side="left")
        self.apply_mode_button = ttk.Button(
            toolbar, text="선택 곡에 적용", command=self._apply_channel_mode
        )
        self.apply_mode_button.pack(side="left", padx=6)
        self.make_pack_button = ttk.Button(toolbar, text="BGM.PAK 만들기", command=self._start_make_pack)
        self.make_pack_button.pack(side="right")

        columns = ("id", "title", "mode", "duration", "file", "path")
        self.tree = ttk.Treeview(tab, columns=columns, show="headings", selectmode="extended")
        headings = ("BGM ID", "게임 BGM 곡명", "변환 방식", "시간", "교체 음원", "음원 경로")
        widths = (60, 225, 90, 70, 155, 285)
        for column, heading, width in zip(columns, headings, widths):
            self.tree.heading(column, text=heading)
            self.tree.column(column, width=width, anchor="center" if column == "id" else "w")
        self.tree.grid(row=6, column=0, columnspan=3, sticky="nsew")
        scroll = ttk.Scrollbar(tab, orient="vertical", command=self.tree.yview)
        scroll.grid(row=6, column=3, sticky="ns")
        self.tree.configure(yscrollcommand=scroll.set)
        for row in gui_patcher.load_bgm_catalog():
            bgm_id = int(row["id"])
            self.tree.insert(
                "", "end", iid=str(bgm_id),
                values=(f"{bgm_id:02d}", row["title"], "", "", "", ""),
            )
        self.tree.selection_set("0")
        self.tree.bind("<<TreeviewSelect>>", self._selection_changed)

    def _build_rom_tab(self) -> None:
        tab = self.rom_tab
        self._path_row(tab, 0, "원본 NDS ROM", self.rom_var, self._browse_rom)
        self._path_row(tab, 1, "입력 BGM.PAK", self.pack_in_var, self._browse_pack_input)
        ttk.Label(tab, textvariable=self.pack_summary_var, foreground="#315d8a").grid(
            row=2, column=0, columnspan=3, sticky="w", pady=(2, 7)
        )
        self._path_row(tab, 3, "출력 폴더", self.rom_out_var, self._browse_output_dir)
        self._path_row(tab, 4, "devkitARM 폴더", self.devkit_var, self._browse_devkit)

        ttk.Label(
            tab,
            text="devkitARM은 EXE에 포함되지 않습니다. 공식 배포처에서 별도로 설치하세요.",
            foreground="#555555",
        ).grid(row=5, column=0, columnspan=3, sticky="w", pady=(12, 4))
        buttons = ttk.Frame(tab)
        buttons.grid(row=6, column=0, columnspan=3, sticky="ew", pady=(8, 0))
        ttk.Button(buttons, text="배포/라이선스 안내", command=self._show_notices).pack(side="left")
        ttk.Button(buttons, text="PAK 배치 내용 보기", command=self._show_pack_details).pack(side="left", padx=6)
        self.apply_button = ttk.Button(buttons, text="ROM 패치 만들기", command=self._start_apply_pack)
        self.apply_button.pack(side="right")

    def _browse_ffmpeg(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("FFmpeg", "ffmpeg.exe"), ("실행 파일", "*.exe")])
        if path:
            self.ffmpeg_var.set(path)

    def _browse_pack_output(self) -> None:
        path = filedialog.asksaveasfilename(
            defaultextension=".bgm.pak",
            filetypes=[("SRW W BGM package", "*.bgm.pak"), ("모든 파일", "*.*")],
            initialfile=Path(self.pack_out_var.get()).name,
        )
        if path:
            self.pack_out_var.set(path)

    def _browse_rom(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Nintendo DS ROM", "*.nds"), ("모든 파일", "*.*")])
        if path:
            self.rom_var.set(path)

    def _browse_pack_input(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("SRW W BGM package", "*.bgm.pak"), ("모든 파일", "*.*")])
        if path:
            self.pack_path_user_selected = True
            self.pack_in_var.set(path)
            self._refresh_pack_summary(show_error=True)

    def _browse_output_dir(self) -> None:
        path = filedialog.askdirectory(initialdir=self.rom_out_var.get() or str(ROOT))
        if path:
            self.rom_out_var.set(path)

    def _browse_devkit(self) -> None:
        path = filedialog.askdirectory(initialdir=self.devkit_var.get() or str(ROOT))
        if path:
            self.devkit_var.set(path)

    def _refresh_pack_summary(self, show_error: bool = False) -> None:
        package = Path(self.pack_in_var.get())
        if not package.is_file():
            self.pack_summary_var.set("BGM.PAK 파일을 선택하세요.")
            return
        try:
            self.pack_summary_var.set(gui_patcher.describe_pack(package))
        except Exception as exc:
            self.pack_summary_var.set(f"사용할 수 없는 BGM.PAK: {exc}")
            if show_error:
                messagebox.showerror("BGM.PAK 검사 실패", str(exc), parent=self.root)

    def _show_pack_details(self) -> None:
        package = Path(self.pack_in_var.get())
        try:
            text = gui_patcher.pack_detail_text(package)
        except Exception as exc:
            messagebox.showerror("BGM.PAK 검사 실패", str(exc), parent=self.root)
            return
        window = tk.Toplevel(self.root)
        window.title("BGM.PAK ID 배치 내용")
        window.geometry("860x620")
        box = ScrolledText(window, wrap="none", font=("Consolas", 9))
        box.pack(fill="both", expand=True, padx=10, pady=10)
        box.insert("1.0", text)
        box.configure(state="disabled")

    def _add_tracks(self) -> None:
        try:
            ffmpeg = gui_patcher.find_ffmpeg(self.ffmpeg_var.get())
        except Exception as exc:
            messagebox.showerror("FFmpeg 확인", str(exc), parent=self.root)
            return
        raw_paths = filedialog.askopenfilenames(title="BGM으로 넣을 음원 선택", filetypes=AUDIO_TYPES)
        if not raw_paths:
            return
        selected = [int(item) for item in self.tree.selection()]
        start = min(selected) if selected else 0
        paths = gui_patcher.natural_sort_paths(raw_paths)
        channels = self._selected_channel_count()
        mode_text = self._channel_mode_text(channels)
        available = 70 - start
        if len(paths) > available:
            messagebox.showwarning(
                "BGM ID 범위 초과",
                f"ID {start:02d}부터는 {available}곡만 넣을 수 있습니다.\n"
                "범위를 넘는 파일은 배치하지 않습니다.",
                parent=self.root,
            )
            paths = paths[:available]
        preview_lines = [
            f"{start + offset:02d}  [{mode_text}]  <-  {path.name}"
            for offset, path in enumerate(paths)
        ]
        preview = "\n".join(preview_lines)
        if len(preview) > 5000:
            preview = preview[:5000] + "\n..."
        if not messagebox.askokcancel(
            "BGM ID 배치 확인",
            "파일명 자연 정렬 결과를 다음과 같이 배치합니다.\n\n" + preview,
            parent=self.root,
        ):
            return

        self.root.configure(cursor="wait")
        self.root.update_idletasks()
        try:
            # Probe everything first. A single bad file must not leave a half-applied ID range.
            pending: list[tuple[int, Path, float]] = []
            for offset, path in enumerate(paths):
                duration = gui_patcher.probe_audio_duration(path, ffmpeg)
                pending.append((start + offset, path, duration))
            for bgm_id, path, duration in pending:
                self.tracks[bgm_id] = path
                self.track_durations[bgm_id] = duration
                self.track_channels[bgm_id] = channels
                current = list(self.tree.item(str(bgm_id), "values"))
                current[2:] = [mode_text, self._format_duration(duration), path.name, str(path)]
                self.tree.item(str(bgm_id), values=current)
        except Exception as exc:
            messagebox.showerror("음원 시간 확인 실패", str(exc), parent=self.root)
        finally:
            self.root.configure(cursor="")
            self._update_duration_summary()
        next_id = min(69, start + len(paths))
        self.tree.selection_set(str(next_id))
        self.tree.see(str(next_id))

    def _remove_tracks(self) -> None:
        for item in self.tree.selection():
            bgm_id = int(item)
            self.tracks.pop(bgm_id, None)
            self.track_durations.pop(bgm_id, None)
            self.track_channels.pop(bgm_id, None)
            current = list(self.tree.item(item, "values"))
            current[2:] = ["", "", "", ""]
            self.tree.item(item, values=current)
        self._update_duration_summary()

    def _selected_channel_count(self) -> int:
        return 2 if self.channel_mode_var.get().startswith("스테레오") else 1

    @staticmethod
    def _channel_mode_text(channels: int) -> str:
        return "스테레오" if channels == 2 else "모노"

    def _apply_channel_mode(self) -> None:
        channels = self._selected_channel_count()
        mode_text = self._channel_mode_text(channels)
        changed = 0
        for item in self.tree.selection():
            bgm_id = int(item)
            if bgm_id not in self.tracks:
                continue
            self.track_channels[bgm_id] = channels
            current = list(self.tree.item(item, "values"))
            current[2] = mode_text
            self.tree.item(item, values=current)
            changed += 1
        if not changed:
            messagebox.showinfo(
                "변환 방식",
                "먼저 음원이 지정된 BGM ID를 선택하세요.",
                parent=self.root,
            )
        self._update_duration_summary()

    @staticmethod
    def _format_duration(seconds: float) -> str:
        total = max(0, int(round(seconds)))
        hours, remainder = divmod(total, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}" if hours else f"{minutes:02d}:{seconds:02d}"

    def _update_duration_summary(self) -> None:
        if self.mode != "pack" or not hasattr(self, "duration_progress"):
            return
        actual_total = sum(self.track_durations.values())
        total = sum(
            duration * self.track_channels.get(bgm_id, 1)
            for bgm_id, duration in self.track_durations.items()
        )
        maximum = gui_patcher.MAX_TOTAL_AUDIO_SECONDS
        self.duration_progress.configure(value=min(total, maximum))
        remaining = max(0.0, maximum - total)
        over = total > maximum
        self.duration_var.set(
            f"실제 곡 길이 합계 {self._format_duration(actual_total)}  |  "
            f"용량 환산 {self._format_duration(total)} / 최대 {self._format_duration(maximum)}"
            + (
                f"  |  초과 {self._format_duration(total - maximum)}"
                if over else f"  |  남음 {self._format_duration(remaining)}"
            )
        )
        if hasattr(self, "make_pack_button") and not self.working:
            valid = bool(self.tracks) and len(self.track_durations) == len(self.tracks) and not over
            self.make_pack_button.configure(state="normal" if valid else "disabled")

    def _selection_changed(self, _event: object = None) -> None:
        selection = self.tree.selection()
        if selection:
            values = self.tree.item(selection[0], "values")
            self.current_var.set(f"현재 BGM ID: {values[0]}  |  {values[1]}")

    def _append_log(self, text: str) -> None:
        self.log_box.configure(state="normal")
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _set_working(self, working: bool, controls: list[tk.Widget] | None = None) -> None:
        self.working = working
        if controls is not None:
            self.active_controls = controls
        for control in self.active_controls:
            control.configure(state="disabled" if working else "normal")
        if not working and hasattr(self, "channel_mode_box"):
            self.channel_mode_box.configure(state="readonly")
        if working:
            self.progress.start(12)
        else:
            self.progress.stop()
            self._update_duration_summary()

    def _start_worker(self, operation: str, function: Callable[[], dict[str, object]], controls: list[tk.Widget]) -> None:
        if self.working:
            return
        self._append_log("=" * 60)
        self._set_working(True, controls)

        def worker() -> None:
            try:
                manifest = function()
                self.events.put(("done", (operation, manifest)))
            except Exception as exc:
                self.events.put(("error", (str(exc), traceback.format_exc())))

        threading.Thread(target=worker, daemon=True).start()

    def _start_make_pack(self) -> None:
        weighted_total = sum(
            duration * self.track_channels.get(bgm_id, 1)
            for bgm_id, duration in self.track_durations.items()
        )
        if weighted_total > gui_patcher.MAX_TOTAL_AUDIO_SECONDS:
            messagebox.showwarning(
                "최대 재생시간 초과",
                "채널 수를 반영한 용량 환산 시간이 최대 "
                f"{self._format_duration(gui_patcher.MAX_TOTAL_AUDIO_SECONDS)}를 넘었습니다.\n"
                "스테레오는 같은 길이의 모노보다 2배 용량을 사용합니다.",
                parent=self.root,
            )
            return
        try:
            tracks = gui_patcher.validate_tracks(
                gui_patcher.Track(bgm_id, path, self.track_channels.get(bgm_id, 1))
                for bgm_id, path in self.tracks.items()
            )
            ffmpeg = gui_patcher.find_ffmpeg(self.ffmpeg_var.get())
            output = Path(self.pack_out_var.get())
        except Exception as exc:
            messagebox.showerror("입력 확인", str(exc), parent=self.root)
            return
        self.status_var.set("음원 변환 및 BGM.PAK 부호화 중...")
        self._start_worker(
            "make_pack",
            lambda: gui_patcher.create_bgm_pack(tracks, output, ffmpeg, lambda line: self.events.put(("log", line))),
            [
                self.make_pack_button, self.add_button, self.remove_button,
                self.channel_mode_box, self.apply_mode_button,
            ],
        )

    def _start_apply_pack(self) -> None:
        rom = Path(self.rom_var.get())
        package = Path(self.pack_in_var.get())
        if not self.pack_path_user_selected and str(package) == self.initial_pack_path:
            recent_pack = gui_patcher.load_recent_pack()
            if recent_pack is not None:
                package = recent_pack
                self.pack_in_var.set(str(package))
                self.initial_pack_path = str(package)
        output = Path(self.rom_out_var.get())
        devkit = Path(self.devkit_var.get())
        if not rom.is_file():
            messagebox.showwarning("입력 확인", "원본 NDS ROM을 선택하세요.", parent=self.root)
            return
        if not package.is_file():
            messagebox.showwarning("입력 확인", "BGM.PAK 파일을 선택하세요.", parent=self.root)
            return
        try:
            self.pack_summary_var.set(gui_patcher.describe_pack(package))
            gui_patcher.find_devkitarm(devkit)
        except Exception as exc:
            messagebox.showerror("입력 확인", str(exc), parent=self.root)
            return
        self.status_var.set("BGM.PAK 검증 및 ROM 패치 생성 중...")
        self._start_worker(
            "apply_pack",
            lambda: gui_patcher.apply_bgm_pack(rom, package, output, devkit, lambda line: self.events.put(("log", line))),
            [self.apply_button],
        )

    def _poll_events(self) -> None:
        try:
            while True:
                kind, value = self.events.get_nowait()
                if kind == "log":
                    self._append_log(str(value))
                elif kind == "error":
                    message, detail = value
                    self._set_working(False)
                    self._append_log(detail)
                    self.status_var.set("실패 — 작업 로그를 확인하세요.")
                    messagebox.showerror("작업 실패", message, parent=self.root)
                elif kind == "done":
                    operation, manifest = value
                    self._set_working(False)
                    if operation == "make_pack":
                        package_path = str(manifest["package"]["path"])
                        self.pack_in_var.set(package_path)
                        self.status_var.set("BGM.PAK 생성 완료")
                        messagebox.showinfo("1단계 완료", f"BGM.PAK을 만들었습니다.\n\n{package_path}", parent=self.root)
                    else:
                        target = str(manifest["build"]["target"]["path"])
                        self.status_var.set("ROM과 BPS 패치 생성 완료")
                        messagebox.showinfo("2단계 완료", f"패치 ROM을 만들었습니다.\n\n{target}", parent=self.root)
        except queue.Empty:
            pass
        if self.root.winfo_exists():
            self.root.after(100, self._poll_events)

    def _show_notices(self) -> None:
        path = ROOT / "THIRD_PARTY_NOTICES.md"
        text = path.read_text(encoding="utf-8") if path.is_file() else "라이선스 고지 파일을 찾지 못했습니다."
        window = tk.Toplevel(self.root)
        window.title("배포 및 제3자 라이선스 안내")
        window.geometry("720x520")
        box = ScrolledText(window, wrap="word")
        box.pack(fill="both", expand=True, padx=10, pady=10)
        box.insert("1.0", text)
        box.configure(state="disabled")

    def _close(self) -> None:
        if self.working and not messagebox.askyesno("작업 중", "진행 중인 작업을 중단하고 종료할까요?", parent=self.root):
            return
        self.root.destroy()

    def run(self) -> int:
        self._update_duration_summary()
        if self.self_test:
            if self.mode == "pack":
                assert len(self.tree.get_children()) == 70
                assert self.tree.item("69", "values")[1] == "Unk_15"
                assert gui_patcher.MAX_TOTAL_AUDIO_SECONDS == 41885
                assert str(self.make_pack_button["state"]) == "disabled"
                self.tracks[0] = Path("self-test.wav")
                self.track_channels[0] = 1
                self.track_durations[0] = gui_patcher.MAX_TOTAL_AUDIO_SECONDS + 1
                self._update_duration_summary()
                assert str(self.make_pack_button["state"]) == "disabled"
                self.track_durations[0] = gui_patcher.MAX_TOTAL_AUDIO_SECONDS
                self._update_duration_summary()
                assert str(self.make_pack_button["state"]) == "normal"
                self.track_channels[0] = 2
                self._update_duration_summary()
                assert str(self.make_pack_button["state"]) == "disabled"
            else:
                assert self.apply_button.winfo_exists()
                assert not hasattr(self, "capacity_canvas")
            self.root.update_idletasks()
            self.root.destroy()
            return 0
        self.root.mainloop()
        return 0


def main(mode: str = "pack", self_test: bool = False) -> int:
    return StageGui(mode=mode, self_test=self_test).run()


if __name__ == "__main__":
    selected_mode = "patch" if "--patch" in os.sys.argv else "pack"
    raise SystemExit(main(selected_mode, "--self-test" in os.sys.argv))
