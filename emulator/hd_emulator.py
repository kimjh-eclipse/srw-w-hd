"""Windows menu-based player for the modified DeSmuME HD core."""
from pathlib import Path
import argparse,copy,json,multiprocessing as mp,os,time,traceback,struct,math
from datetime import datetime,timezone,timedelta
from multiprocessing import shared_memory
import tkinter as tk
from tkinter import ttk,filedialog,messagebox
from PIL import Image,ImageTk,ImageDraw
from player_controls import BUTTONS,DEFAULT_KEYS,DEFAULT_PAD,DEFAULTS,LAYOUTS,sdl_pad_mapping,read_settings,write_settings,key_buttons,pad_buttons,screen_rectangles,touch_position
from player_worker import worker_main,TOP_BYTES,BOTTOM_BYTES,FRAME_BYTES
from player_rumble import PadRumble
from player_shortcuts import ShortcutMixin
from gpu_display import GPUDisplay,RGBFrame
from player_metrics import PlayerMetrics
from windows_keyboard import WindowsKeyboard
from render_resolution import DEFAULT_WIDTH,MIN_WIDTH,MAX_WIDTH,clamp_width
import sdl_pad_state

HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
CANONICAL=ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds'

class EmulatorWindow(ShortcutMixin):
    def __init__(self,root,args):
        self.root=root;self.args=args;self.config_path=args.config or HERE/'player_settings.json';self.settings=read_settings(self.config_path)
        self.timer_precision=None
        if os.name=='nt':
            import ctypes
            if ctypes.windll.winmm.timeBeginPeriod(1)==0:self.timer_precision=ctypes.windll.winmm
        self.ctx=mp.get_context('spawn');self.process=None;self.pipe=None;self.memory=None;self.lock=None
        self.loaded=False;self.opening=False;self.paused=False;self.current_rom=None;self.demo=False;self.save_dir=None
        self.gpu=None;self.gpu_error=None;self.metrics=PlayerMetrics(getattr(args,'metrics',None));self.received_frame=0;self.last_bottom_revision=None
        self.latest=None;self.photos=[];self.rects=[None,None];self.dirty=True;self.held=set();self.touch=None;self.last_input=None
        self.render_width=DEFAULT_WIDTH;self.resolution_changed_at=0
        self.dialog=None;self.capture=None;self.pad_draft=None;self.devices=[];self.pad=None;self.last_device_refresh=0;self.closed=False;self.session_error=False
        self.rumble=PadRumble()
        self.physical_keyboard=WindowsKeyboard()
        self.init_shortcuts()
        self.pause_var=tk.StringVar(value='일시정지');self.hd_var=tk.BooleanVar(value=self.settings['hd']);self.volume_var=tk.IntVar(value=self.settings['volume'])
        self.auto_quality_var=tk.BooleanVar(value=self.settings['hd_auto_quality'])
        self.layout_var=tk.StringVar(value=self.settings['layout']);self.swap_var=tk.BooleanVar(value=self.settings['swap']);self.slot_var=tk.IntVar(value=self.settings['slot'])
        self.settings['auto_pause']=False
        self.auto_pause_var=tk.BooleanVar(value=False);self.status_var=tk.StringVar(value='롬을 열거나 HD 미리보기를 실행하세요.');self.pad_status=tk.StringVar(value='패드 확인 중')
        root.title('슈퍼로봇대전 W HD');root.geometry(self.settings['geometry']);root.minsize(900,600)
        root.option_add('*Font',('맑은 고딕',9));style=ttk.Style()
        if 'vista' in style.theme_names():style.theme_use('vista')
        self.build_menu();self.build_toolbar();self.build_layout_toolbar()
        self.canvas=tk.Canvas(root,background='#10151f',highlightthickness=0,takefocus=True);self.canvas.pack(fill='both',expand=True)
        self.tk_key_seen={};self.tk_pointer_seen=None
        self.canvas.bind('<KeyPress>',lambda e:self.note_tk_key(e,True),add='+')
        self.canvas.bind('<KeyRelease>',lambda e:self.note_tk_key(e,False),add='+')
        self.canvas.bind('<Configure>',lambda e:self.request_redraw());self.canvas.bind('<ButtonPress-1>',self.mouse_down);self.canvas.bind('<B1-Motion>',self.mouse_drag);self.canvas.bind('<ButtonRelease-1>',self.mouse_up)
        self.fit_job=None;root.bind('<Configure>',self.window_configured,add='+')
        self.canvas.bind('<Double-Button-1>',self.double_click)
        footer=ttk.Frame(root,padding=(10,5));self.footer=footer;footer.pack(fill='x');ttk.Label(footer,textvariable=self.status_var).pack(side='left');ttk.Label(footer,textvariable=self.pad_status).pack(side='right')
        self.popup=tk.Menu(root,tearoff=False);self.popup.add_command(label='계속 / 일시정지',command=self.toggle_pause);self.popup.add_checkbutton(label='HD 그래픽',variable=self.hd_var,command=self.set_hd);self.popup.add_command(label='키 · 패드 설정…',command=self.controls_dialog)
        self.canvas.bind('<Button-3>',lambda e:self.popup.tk_popup(e.x_root,e.y_root))
        root.bind('<KeyPress>',self.key_down);root.bind('<KeyRelease>',self.key_up);root.bind('<FocusOut>',self.focus_lost)
        for sequence,callback in [('<Control-o>',self.open_rom),('<Control-d>',self.start_demo),('<Control-r>',self.restart),('<F1>',self.toggle_hd),('<F11>',self.fullscreen),('<Escape>',self.leave_fullscreen)]:
            root.bind(sequence,lambda e,fn=callback:self.bound_shortcut(e,fn))
        for number,(mode,_) in enumerate(LAYOUTS,1):root.bind(f'<Control-Key-{number}>',lambda e,m=mode:self.shortcut(lambda:self.choose_layout(m)))
        root.protocol('WM_DELETE_WINDOW',self.close)
        def callback_error(kind,value,trace):
            (HERE/'player_ui_error.log').write_text(''.join(traceback.format_exception(kind,value,trace)),encoding='utf-8')
            messagebox.showerror('요청을 처리하지 못했습니다',str(value),parent=root)
        root.report_callback_exception=callback_error
        icon=Image.new('RGBA',(32,32),(0,0,0,0));draw=ImageDraw.Draw(icon);draw.rounded_rectangle((4,2,28,30),radius=4,fill='#2365b9');draw.rectangle((8,6,24,14),fill='#e8f3ff');draw.rectangle((8,18,24,26),fill='#b5e0ff');self.icon=ImageTk.PhotoImage(icon);root.iconphoto(True,self.icon)
        self.init_gamepads();root.after(15,self.poll)
        if not args.no_start:
            if args.demo:root.after(100,lambda:self.start_session(CANONICAL,True,args.state,args.state_frame,args.paused))
            elif args.rom or args.state:root.after(100,lambda:self.start_session(args.rom or CANONICAL,False,args.state,args.state_frame,args.paused))
            elif CANONICAL.exists():root.after(100,lambda:self.start_session(CANONICAL))

    def build_menu(self):
        bar=tk.Menu(self.root);self.menu_bar=bar;self.root.config(menu=bar)
        file=tk.Menu(bar,tearoff=False);self.file_menu=file;bar.add_cascade(label='파일',menu=file)
        file.add_command(label='롬 열기…',accelerator='Ctrl+O',command=self.open_rom);self.recent_menu=tk.Menu(file,tearoff=False);file.add_cascade(label='최근 게임',menu=self.recent_menu);self.refresh_recent()
        file.add_separator();file.add_command(label='중간 저장 파일 불러오기…',command=self.load_state_file);file.add_command(label='중간 저장 파일로 내보내기…',command=self.save_state_file)
        file.add_command(label='스크린샷 저장…',command=self.screenshot);file.add_separator();file.add_command(label='종료',command=self.close)
        game=tk.Menu(bar,tearoff=False);self.game_menu=game;bar.add_cascade(label='게임',menu=game)
        game.add_command(label='계속 / 일시정지',accelerator='Space',command=self.toggle_pause);game.add_command(label='다시 시작',accelerator='Ctrl+R',command=self.restart)
        game.add_command(label='HD 전투 미리보기',accelerator='Ctrl+D',command=self.start_demo);game.add_separator()
        slots=tk.Menu(game,tearoff=False);self.slot_menu=slots;game.add_cascade(label='저장 칸 선택',menu=slots)
        for i in range(1,6):slots.add_radiobutton(label=f'{i}번',value=i,variable=self.slot_var,command=self.set_slot)
        game.add_command(label='선택한 칸에 저장',accelerator='F5',command=self.quick_save);game.add_command(label='선택한 칸 불러오기',accelerator='F8',command=self.quick_load)
        view=tk.Menu(bar,tearoff=False);self.view_menu=view;bar.add_cascade(label='화면',menu=view)
        for number,(value,label) in enumerate(LAYOUTS,1):view.add_radiobutton(label=label,accelerator=f'Ctrl+{number}',value=value,variable=self.layout_var,command=lambda m=value:self.choose_layout(m))
        view.add_radiobutton(label='위 화면만',value='top',variable=self.layout_var,command=lambda:self.choose_layout('top'))
        view.add_checkbutton(label='위 · 아래 화면 위치 바꾸기',variable=self.swap_var,command=self.set_layout);view.add_separator()
        view.add_checkbutton(label='HD 그래픽 사용',accelerator='F1',variable=self.hd_var,command=self.set_hd);view.add_command(label='전체 화면',accelerator='F11',command=self.fullscreen)
        sizes=tk.Menu(view,tearoff=False);view.add_cascade(label='창 크기',menu=sizes)
        for size in ('960x680','1280x850','1600x1000'):sizes.add_command(label=size.replace('x',' × '),command=lambda s=size:self.root.geometry(s))
        settings=tk.Menu(bar,tearoff=False);bar.add_cascade(label='설정',menu=settings)
        settings.add_command(label='키보드 · 패드 설정…',command=self.controls_dialog)
        settings.add_command(label='단축키 · 빠른 진행 설정…',command=self.shortcuts_dialog)
        settings.add_command(label='전투 진동 설정…',command=self.rumble_dialog)
        settings.add_checkbutton(label='60프레임 우선',variable=self.auto_quality_var,command=self.set_auto_quality)
        help_menu=tk.Menu(bar,tearoff=False);bar.add_cascade(label='도움말',menu=help_menu)
        help_menu.add_command(label='조작 안내',command=self.help_dialog);help_menu.add_command(label='프로그램 · 오픈소스 정보',command=self.about_dialog)
        self.update_shortcut_labels()

    def build_toolbar(self):
        toolbar=ttk.Frame(self.root,padding=(8,7));self.toolbar=toolbar;toolbar.pack(fill='x')
        ttk.Button(toolbar,text='롬 열기',command=self.open_rom).pack(side='left',padx=3)
        self.play_button=ttk.Button(toolbar,textvariable=self.pause_var,command=self.toggle_pause);self.play_button.pack(side='left',padx=3)
        self.reset_button=ttk.Button(toolbar,text='다시 시작',command=self.restart);self.reset_button.pack(side='left',padx=3)
        ttk.Separator(toolbar,orient='vertical').pack(side='left',fill='y',padx=7)
        self.save_button=ttk.Button(toolbar,text='저장',command=self.quick_save);self.save_button.pack(side='left',padx=3)
        self.load_button=ttk.Button(toolbar,text='불러오기',command=self.quick_load);self.load_button.pack(side='left',padx=3)
        self.slot_label=ttk.Label(toolbar,text='1번 칸');self.slot_label.pack(side='left',padx=4)
        ttk.Separator(toolbar,orient='vertical').pack(side='left',fill='y',padx=7)
        ttk.Checkbutton(toolbar,text='HD 그래픽',variable=self.hd_var,command=self.set_hd).pack(side='left',padx=3)
        ttk.Button(toolbar,text='HD 미리보기',command=self.start_demo).pack(side='left',padx=8)
        ttk.Label(toolbar,text='소리').pack(side='left',padx=(10,3));ttk.Scale(toolbar,from_=0,to=100,variable=self.volume_var,command=self.set_volume,length=100).pack(side='left')
        self.update_buttons()

    def build_layout_toolbar(self):
        bar=ttk.Frame(self.root,padding=(10,2,8,6));self.layout_toolbar=bar;bar.pack(fill='x')
        ttk.Label(bar,text='화면 구성').pack(side='left',padx=(0,10))
        for value,label in LAYOUTS:
            ttk.Radiobutton(bar,text=label,value=value,variable=self.layout_var,style='Toolbutton',command=lambda m=value:self.choose_layout(m)).pack(side='left',padx=2)
        ttk.Separator(bar,orient='vertical').pack(side='left',fill='y',padx=9)
        self.swap_button=ttk.Checkbutton(bar,text='화면 교환',variable=self.swap_var,command=self.set_layout);self.swap_button.pack(side='left',padx=4)
        ttk.Button(bar,text='전체 화면',command=self.fullscreen).pack(side='left',padx=8)

    def persist(self):
        self.settings.update(hd=self.hd_var.get(),volume=int(self.volume_var.get()),layout=self.layout_var.get(),swap=self.swap_var.get(),slot=self.slot_var.get(),auto_pause=self.auto_pause_var.get())
        write_settings(self.config_path,self.settings)

    def refresh_recent(self):
        self.recent_menu.delete(0,'end')
        entries=[p for p in self.settings['recent'] if isinstance(p,str) and Path(p).exists()][:6]
        for path in entries:self.recent_menu.add_command(label=Path(path).name,command=lambda p=path:self.start_session(p))
        if not entries:self.recent_menu.add_command(label='최근 게임 없음',state='disabled')

    def send(self,op,**data):
        if self.pipe:
            try:self.pipe.send(dict(op=op,**data))
            except (BrokenPipeError,EOFError,OSError):pass

    def stop_worker(self):
        self.release_shortcuts()
        self.rumble.stop()
        if self.process:
            self.send('quit');self.process.join(2)
            if self.process.is_alive():self.process.terminate();self.process.join(.5)
            self.process.close();self.process=None
        if self.pipe:self.pipe.close();self.pipe=None
        if self.memory:
            self.memory.close();self.memory.unlink();self.memory=None
        self.loaded=False;self.opening=False;self.last_input=None;self.touch=None;self.held.clear()

    def start_session(self,rom,demo=False,state=None,state_frame=64700,paused=False):
        path=Path(rom).resolve()
        if not path.is_file():messagebox.showerror('롬 열기','롬 파일을 찾을 수 없습니다.',parent=self.root);return
        if path.suffix.lower()!='.nds':messagebox.showerror('롬 열기','.nds 형식의 롬을 선택해주세요.',parent=self.root);return
        self.stop_worker();self.current_rom=path;self.demo=demo;self.paused=paused;self.session_error=False;self.latest=None;self.photos=[];self.opening=True
        self.status_var.set(f'{path.name} 여는 중…');self.root.title(f'{path.stem} — 슈퍼로봇대전 W HD');self.request_redraw();self.update_buttons()
        self.memory=shared_memory.SharedMemory(create=True,size=FRAME_BYTES);self.lock=self.ctx.Lock();self.pipe,child=self.ctx.Pipe()
        self.render_width=self.desired_render_width()
        config=dict(rom=str(path),demo=demo,hd=self.hd_var.get(),volume=int(self.volume_var.get()),paused=paused,state=str(state) if state else None,state_frame=state_frame,save_root=str(self.args.save_root) if self.args.save_root else None,legacy_timing=bool(getattr(self.args,'legacy_timing',False)),profile_render=str(self.args.profile_render) if getattr(self.args,'profile_render',None) else None,render_width=self.render_width)
        config['hd_auto_quality']=self.auto_quality_var.get()
        self.process=self.ctx.Process(target=worker_main,args=(child,self.memory.name,self.lock,config),daemon=False);self.process.start();child.close()
        self.settings['recent']=[str(path)]+[p for p in self.settings['recent'] if p!=str(path)];self.settings['recent']=self.settings['recent'][:6];self.persist();self.refresh_recent();self.canvas.focus_set()

    def set_auto_quality(self):
        self.settings['hd_auto_quality']=self.auto_quality_var.get();self.persist()
        self.send('quality',value=self.auto_quality_var.get());self.canvas.focus_set()

    def open_rom(self):
        if self.dialog:return
        old=self.pause_for_dialog()
        path=filedialog.askopenfilename(parent=self.root,title='Nintendo DS 롬 열기',initialdir=str(self.current_rom.parent if self.current_rom else CANONICAL.parent),filetypes=[('Nintendo DS 롬','*.nds'),('모든 파일','*.*')])
        if path:self.start_session(path)
        else:self.restore_after_dialog(old)

    def start_demo(self):
        if not self.dialog:self.start_session(CANONICAL,True)

    def restart(self):
        if self.current_rom and not self.dialog:self.start_session(self.current_rom,self.demo)

    def toggle_pause(self):
        if self.loaded and not self.dialog:
            self.set_fast_forward(False)
            self.rumble.stop()
            self.paused=not self.paused;self.send('pause',value=self.paused);self.update_buttons();self.canvas.focus_set()

    def toggle_hd(self):
        self.hd_var.set(not self.hd_var.get());self.set_hd()

    def set_hd(self):
        self.send('hd',value=self.hd_var.get());self.persist();self.canvas.focus_set()

    def set_volume(self,value):
        self.settings['volume']=round(float(value));self.send('volume',value=self.settings['volume'])

    def set_slot(self):self.slot_label.config(text=f'{self.slot_var.get()}번 칸');self.persist()
    def choose_layout(self,value):self.layout_var.set(value);self.swap_var.set(False);self.set_layout()
    def set_layout(self):
        self.touch=None;self.held.clear();self.persist();self.request_redraw()
        if self.fit_job:self.root.after_cancel(self.fit_job)
        self.fit_job=self.root.after(150,self.fit_window_content)
        self.swap_button.config(state='disabled' if self.layout_var.get()=='top' else 'normal')
        self.view_menu.entryconfigure(5,state='disabled' if self.layout_var.get()=='top' else 'normal')

    def rumble_dialog(self):
        if self.dialog:self.dialog.lift();return
        old=self.pause_for_dialog();dialog=tk.Toplevel(self.root);self.dialog=dialog
        dialog.title('전투 진동');dialog.transient(self.root);dialog.resizable(False,False)
        body=ttk.Frame(dialog,padding=20);body.pack(fill='both',expand=True)
        enabled=tk.BooleanVar(value=self.settings['rumble_enabled']);strength=tk.IntVar(value=self.settings['rumble_strength'])
        beam=tk.BooleanVar(value=self.settings['rumble_beam'])
        ttk.Checkbutton(body,text='전투 진동 사용',variable=enabled,command=lambda:self.rumble.stop()).pack(anchor='w')
        ttk.Checkbutton(body,text='빔 연출 잔진동',variable=beam).pack(anchor='w',pady=(6,0))
        ttk.Label(body,text='진동 강도').pack(anchor='w',pady=(14,4))
        ttk.Scale(body,from_=0,to=100,variable=strength,length=300).pack(fill='x')
        status=tk.StringVar(value='타격은 강하게, 빔 발사 연출은 짧고 빠르게 진동합니다.')
        ttk.Label(body,textvariable=status,wraplength=340).pack(pady=12)
        def test():
            ok=self.rumble.play(self.pad,self.settings['pad_enabled'] and enabled.get(),strength.get(),low=1.,high=1.,duration=180)
            status.set('테스트 진동을 보냈습니다.' if ok else '진동 지원 패드를 연결하고 게임 패드 사용을 켜주세요.')
        def finish(apply=False):
            self.rumble.stop()
            if apply:self.settings.update(rumble_enabled=enabled.get(),rumble_strength=round(strength.get()),rumble_beam=beam.get());self.persist()
            dialog.destroy();self.dialog=None;self.restore_after_dialog(old)
        row=ttk.Frame(body);row.pack(fill='x');ttk.Button(row,text='진동 테스트',command=test).pack(side='left')
        ttk.Button(row,text='적용',command=lambda:finish(True)).pack(side='right',padx=4)
        ttk.Button(row,text='취소',command=finish).pack(side='right')
        dialog.protocol('WM_DELETE_WINDOW',finish)

    def quick_save(self):
        if self.loaded and not self.dialog:self.send('save',slot=self.slot_var.get());self.canvas.focus_set()

    def quick_load(self):
        if self.loaded and not self.dialog:self.release_shortcuts();self.send('load',slot=self.slot_var.get());self.canvas.focus_set()

    def pause_for_dialog(self):
        self.release_shortcuts()
        self.rumble.stop()
        old=self.paused
        if self.loaded:self.paused=True;self.send('pause',value=True);self.send('input',buttons=[],touch=None);self.update_buttons()
        self.held.clear();self.touch=None;return old

    def restore_after_dialog(self,old):
        if self.loaded:self.paused=old;self.send('pause',value=old);self.update_buttons()
        self.canvas.focus_set()

    def save_state_file(self):
        if not self.loaded or self.dialog:return
        old=self.pause_for_dialog();path=filedialog.asksaveasfilename(parent=self.root,title='중간 저장 내보내기',initialdir=str(self.save_dir),defaultextension='.state',filetypes=[('중간 저장','*.state')])
        if path:self.send('save',path=path)
        self.restore_after_dialog(old)

    def load_state_file(self):
        if not self.loaded or self.dialog:return
        old=self.pause_for_dialog();path=filedialog.askopenfilename(parent=self.root,title='중간 저장 불러오기',initialdir=str(self.save_dir),filetypes=[('중간 저장','*.state'),('모든 파일','*.*')])
        if path:self.send('load',path=path)
        else:self.restore_after_dialog(old)

    def screenshot(self):
        if not self.latest or self.dialog:return
        old=self.pause_for_dialog();path=filedialog.asksaveasfilename(parent=self.root,title='게임 화면 저장',defaultextension='.png',initialfile='SRWW_HD.png',filetypes=[('PNG 그림','*.png')])
        if path:
            width,height=max(self.canvas.winfo_width(),1),max(self.canvas.winfo_height(),1);image=Image.new('RGB',(width,height),'#10151f')
            for source,rect in zip(self.latest,screen_rectangles(width,height,self.layout_var.get(),self.swap_var.get())):
                if rect:image.paste(source.resize(rect[2:],Image.Resampling.LANCZOS),rect[:2])
            image.save(path);self.status_var.set('게임 화면을 저장했습니다.')
        self.restore_after_dialog(old)

    def update_buttons(self):
        self.pause_var.set('계속' if self.paused else '일시정지')
        for name in ('play_button','reset_button','save_button','load_button'):
            button=getattr(self,name,None)
            if button:button.config(state='normal' if self.loaded else 'disabled')
        if hasattr(self,'slot_label'):self.slot_label.config(text=f'{self.slot_var.get()}번 칸')
        state='normal' if self.loaded else 'disabled'
        for i in (3,4,5):self.file_menu.entryconfigure(i,state=state)
        for i in (0,1,5,6):self.game_menu.entryconfigure(i,state=state)

    def refresh_slots(self):
        for i in range(1,6):
            path=self.save_dir/f'slot_{i}.state' if self.save_dir else None
            try:label=datetime.fromtimestamp(path.stat().st_mtime,timezone(timedelta(hours=9))).strftime('%m/%d %H:%M') if path else '저장 없음'
            except OSError:label='저장 없음'
            self.slot_menu.entryconfigure(i-1,label=f'{i}번 · {label}')

    def request_redraw(self):self.dirty=True

    def window_configured(self,event):
        if event.widget is not self.root or self.closed:return
        size=(event.width,event.height)
        if size==getattr(self,'configured_size',None):return
        self.configured_size=size
        if self.fit_job:self.root.after_cancel(self.fit_job)
        self.fit_job=self.root.after(150,self.fit_window_content)

    def fit_window_content(self):
        self.fit_job=None
        if self.closed or self.root.state()!='normal' or bool(self.root.attributes('-fullscreen')):return
        aspect={'large_horizontal':16/9,'large_vertical':1,'equal_horizontal':8/3,'equal_vertical':2/3,'top':4/3}.get(self.layout_var.get(),16/9)
        chrome=self.root.winfo_height()-self.canvas.winfo_height()
        if self.canvas.winfo_height()<10:return
        width=max(900,self.root.winfo_width());height=round(width/aspect)+chrome
        if height<600:height=600;width=round((height-chrome)*aspect)
        # Keep every pixel and the DS aspect ratio. Shrink the window's unused
        # letterbox height rather than cropping or stretching the game screens.
        if height>self.root.winfo_screenheight()-80 or width>self.root.winfo_screenwidth()-80:return
        if abs(height-self.root.winfo_height())>1 or abs(width-self.root.winfo_width())>1:
            self.root.geometry(f'{width}x{height}');self.request_redraw()

    def desired_render_width(self):
        rects=screen_rectangles(max(1,self.canvas.winfo_width()),max(1,self.canvas.winfo_height()),self.layout_var.get(),self.swap_var.get())
        width=max((rect[2] for rect in rects if rect),default=DEFAULT_WIDTH)
        return clamp_width(math.ceil(width/32)*32)

    def draw(self):
        draw_started=time.perf_counter()
        self.dirty=False;width,height=self.canvas.winfo_width(),self.canvas.winfo_height();self.canvas.delete('all');self.photos=[]
        if not self.latest:
            if self.gpu is not None:self.gpu.clear()
            text='게임 화면을 준비하고 있습니다…' if self.opening else '슈퍼로봇대전 W HD'
            self.canvas.create_text(width/2,height/2-20,text=text,fill='#e6edf7',font=('맑은 고딕',22))
            self.canvas.create_text(width/2,height/2+25,text='파일 → 롬 열기  또는  HD 미리보기',fill='#9faec3',font=('맑은 고딕',12));return
        self.rects=screen_rectangles(width,height,self.layout_var.get(),self.swap_var.get())
        desired=self.desired_render_width()
        if desired!=self.render_width and self.loaded and time.perf_counter()-self.resolution_changed_at>.3:
            self.render_width=desired;self.resolution_changed_at=time.perf_counter();self.send('resolution',width=desired)
        if self.gpu is None and self.gpu_error is None and not getattr(self.args,'software_display',False) and self.canvas.winfo_viewable():
            try:self.gpu=GPUDisplay(self.canvas)
            except Exception as error:self.gpu_error=repr(error)
        if self.gpu is not None:
            self.gpu.draw(self.latest,self.rects)
        else:
            for number,(source,rect) in enumerate(zip(self.latest,self.rects)):
                if rect is None:continue
                x,y,w,h=rect;image=source.resize((w,h),Image.Resampling.LANCZOS);photo=ImageTk.PhotoImage(image);self.photos.append(photo)
                self.canvas.create_image(x,y,image=photo,anchor='nw')
        self.metrics.present(self.received_frame,(time.perf_counter()-draw_started)*1000)

    def has_input_focus(self):
        return self.gpu.focused() if self.gpu is not None else self.root.focus_displayof() is not None

    def bound_shortcut(self,event,callback):
        self.tk_key_seen[event.keysym,True]=time.perf_counter()
        return self.shortcut(callback)

    def note_tk_key(self,event,down):
        key=(event.keysym,down)
        if self.gpu is not None and time.perf_counter()-self.gpu.forwarded_keys.get(key,-10)<.04:return 'break'
        self.tk_key_seen[key]=time.perf_counter()

    def flush_game_input(self,pad=None):
        if not self.loaded:return
        active=self.has_input_focus() and not self.dialog
        buttons=(key_buttons(self.held,self.settings['keys'])|(pad if pad is not None else getattr(self,'last_pad_buttons',set()))) if active else set()
        touch=self.touch if active else None;value=(tuple(sorted(buttons)),touch)
        if value!=self.last_input:
            self.send('input',buttons=list(buttons),touch=touch,sent_at=time.perf_counter());self.last_input=value

    def mouse_down(self,event):self.tk_pointer_seen=('down',event.x,event.y,time.perf_counter());self.canvas.focus_set();self.touch=touch_position(event.x,event.y,self.rects[1]);self.flush_game_input()
    def mouse_drag(self,event):self.touch=touch_position(event.x,event.y,self.rects[1]);self.flush_game_input()
    def mouse_up(self,event):
        self.tk_pointer_seen=('up',getattr(event,'x',0),getattr(event,'y',0),time.perf_counter());self.touch=None;self.flush_game_input()
    def double_click(self,event):
        self.tk_pointer_seen=('down',event.x,event.y,time.perf_counter())
        if self.dialog or not self.latest:return 'break'
        if any(rect and rect[0]<=event.x<rect[0]+rect[2] and rect[1]<=event.y<rect[1]+rect[3] for rect in self.rects):
            self.touch=None;self.canvas.focus_set();self.fullscreen()
        return 'break'
    def shortcut(self,callback):
        if not self.dialog:callback()
        return 'break'
    def key_down(self,event):
        if not getattr(event,'from_sdl',False):self.tk_key_seen[event.keysym,True]=time.perf_counter()
        if self.dialog or event.state&0x000c:return
        key=event.keysym.lower() if len(event.keysym)==1 else event.keysym
        action=next((name for name,value in self.settings['hotkeys'].items() if value and value==key),None)
        if action:
            repeated=key in self.action_keys_down;self.action_keys_down.add(key)
            if action=='fast_forward':self.set_fast_forward(True)
            elif not repeated:self.run_action(action)
            return 'break'
        if getattr(event,'from_sdl',False) or self.root.focus_get() is self.canvas:
            self.held.add(event.keysym.lower() if len(event.keysym)==1 else event.keysym);self.flush_game_input()
    def key_up(self,event):
        if not getattr(event,'from_sdl',False):self.tk_key_seen[event.keysym,False]=time.perf_counter()
        key=event.keysym.lower() if len(event.keysym)==1 else event.keysym
        self.held.discard(key);self.action_keys_down.discard(key);self.flush_game_input()
        if key==self.settings['hotkeys']['fast_forward']:self.set_fast_forward(self.pad_fast_forward)
    def focus_lost(self,event):
        self.release_shortcuts()
        self.rumble.stop()
        self.held.clear();self.touch=None;self.flush_game_input()
    def fullscreen(self):
        entering=not bool(self.root.attributes('-fullscreen'));self.touch=None
        if entering:
            self.window_geometry=self.root.geometry();self.window_state=self.root.state();self.root.config(menu='')
            self.toolbar.pack_forget();self.layout_toolbar.pack_forget();self.footer.pack_forget();self.root.attributes('-fullscreen',True)
        else:
            self.root.attributes('-fullscreen',False);self.root.config(menu=self.menu_bar)
            self.toolbar.pack(fill='x',before=self.canvas);self.layout_toolbar.pack(fill='x',before=self.canvas);self.footer.pack(fill='x')
            self.root.geometry(self.window_geometry)
            if self.window_state=='zoomed':self.root.state('zoomed')
        self.canvas.focus_set();self.request_redraw()
    def leave_fullscreen(self):
        if bool(self.root.attributes('-fullscreen')):self.fullscreen()

    def init_gamepads(self):
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT']='1';os.environ['SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS']='1'
        try:
            import pygame
            self.pygame=pygame;pygame.display.init();pygame.joystick.init();self.refresh_devices()
        except Exception:self.pygame=None;self.pad_status.set('패드 사용 불가 · 키보드 사용 가능')

    def refresh_devices(self):
        if not getattr(self,'pygame',None):return
        self.rumble.stop()
        self.devices=[]
        try:
            for i in range(self.pygame.joystick.get_count()):
                pad=self.pygame.joystick.Joystick(i);pad.init();self.devices.append(pad)
        except self.pygame.error:pass
        preferred=self.pad_selection.get() if self.dialog and getattr(self,'pad_selection',None) else self.settings.get('pad_name','');self.pad=next((p for p in self.devices if p.get_name()==preferred),self.devices[0] if self.devices else None)
        if self.pad is not None:
            guid=self.pad.get_guid();profiles=self.settings.setdefault('pad_profiles',{})
            if guid not in profiles:
                profiles[guid]=self.controller_defaults();self.persist()
        self.pad_status.set(self.pad.get_name() if self.pad and self.settings['pad_enabled'] else '패드 연결 안 됨' if not self.pad else '패드 꺼짐')
        self.last_device_refresh=time.perf_counter()

    def controller_defaults(self):
        if self.pad is not None:
            try:
                from pygame._sdl2 import controller
                controller.init();device=controller.Controller.from_joystick(self.pad)
                return sdl_pad_mapping(device.get_mapping())
            except Exception:pass
        return dict(DEFAULT_PAD)

    def active_pad_mapping(self):
        try:guid=self.pad.get_guid() if self.pad is not None else None
        except Exception:guid=None
        return self.settings.get('pad_profiles',{}).get(guid,self.settings['pad'])

    def poll_pad(self):
        self.pad_fast_forward=False
        if not getattr(self,'pygame',None):return set()
        pygame=self.pygame
        try:
            # SDL's window event pump can reenter Tk with the GIL released.
            # Read controllers directly; Tk exclusively owns native messages.
            sdl_pad_state.update(pygame)
            if pygame.joystick.get_count()!=len(self.devices) or time.perf_counter()-self.last_device_refresh>3:self.refresh_devices()
            if not self.pad:
                self.pad_button_snapshot=(None,set());return set()
            instance=self.pad.get_instance_id()
            held={i for i in range(self.pad.get_numbuttons()) if self.pad.get_button(i)}
            previous_id,previous=getattr(self,'pad_button_snapshot',(None,set()))
            self.pad_button_snapshot=(instance,held)
            pressed=held-previous if previous_id==instance else set()
            if pressed and self.capture and self.capture[0] in ('pad','shortcut_pad'):self.assign_capture(min(pressed))
            enabled=self.pad_enabled_draft.get() if self.dialog and getattr(self,'pad_enabled_draft',None) else self.settings['pad_enabled']
            if not enabled:return set()
            if not self.dialog and self.has_input_focus():
                self.pad_fast_forward=self.settings['pad_hotkeys']['fast_forward'] in held
                for name,button in self.settings['pad_hotkeys'].items():
                    if button in pressed:self.run_action(name)
            axes=[self.pad.get_axis(i) for i in range(self.pad.get_numaxes())];hats=[self.pad.get_hat(i) for i in range(self.pad.get_numhats())]
            result=pad_buttons(held,axes,hats,self.pad_draft if self.pad_draft is not None else self.active_pad_mapping(),self.settings['deadzone'])
            if self.dialog and hasattr(self,'input_preview'):
                labels=[label for _,label,index in BUTTONS if index in result];self.input_preview.set('입력: '+', '.join(labels) if labels else '패드 입력을 기다리고 있습니다.')
            return result
        except (pygame.error,SystemError,KeyError):
            self.rumble.stop();self.pad=None;self.devices=[];self.pad_button_snapshot=(None,set())
            self.pad_status.set('패드 재연결 중 · 키보드 사용 가능')
            return set()

    def controls_dialog(self):
        if self.dialog:self.dialog.lift();return
        old=self.pause_for_dialog();dialog=tk.Toplevel(self.root);self.dialog=dialog;dialog.title('키보드 · 패드 설정');dialog.transient(self.root);dialog.resizable(False,False)
        draft=copy.deepcopy(self.settings['keys']);self.pad_draft=copy.deepcopy(self.active_pad_mapping());self.mapping_draft=draft;self.mapping_buttons={}
        body=ttk.Frame(dialog,padding=18);body.pack(fill='both',expand=True)
        ttk.Label(body,text='버튼을 누른 뒤 사용할 키 또는 패드 버튼을 입력하세요.',font=('맑은 고딕',10)).grid(row=0,column=0,columnspan=3,sticky='w',pady=(0,12))
        for column,text in enumerate(('DS 버튼','키보드','게임 패드')):ttk.Label(body,text=text).grid(row=1,column=column,padx=12,pady=5)
        for row,(name,label,_) in enumerate(BUTTONS,2):
            ttk.Label(body,text=label).grid(row=row,column=0,sticky='w',padx=(0,20),pady=3)
            button=ttk.Button(body,width=18,text=self.key_label(draft[name]),command=lambda n=name:self.begin_capture('key',n));button.grid(row=row,column=1,padx=6);self.mapping_buttons['key',name]=button
            if name in DEFAULT_PAD:
                button=ttk.Button(body,width=18,text=f"버튼 {self.pad_draft[name]+1}",command=lambda n=name:self.begin_capture('pad',n));button.grid(row=row,column=2,padx=6);self.mapping_buttons['pad',name]=button
            else:ttk.Label(body,text='방향 패드 / 왼쪽 스틱').grid(row=row,column=2,padx=6)
        self.capture_text=tk.StringVar(value='프로그램 기능은 설정 → 단축키 · 빠른 진행 설정에서 바꿀 수 있습니다.');ttk.Label(body,textvariable=self.capture_text,wraplength=520).grid(row=14,column=0,columnspan=3,sticky='w',pady=(12,6))
        self.input_preview=tk.StringVar(value='패드 입력을 기다리고 있습니다.');ttk.Label(body,textvariable=self.input_preview).grid(row=15,column=0,columnspan=3,sticky='w')
        enabled=tk.BooleanVar(value=self.settings['pad_enabled']);self.pad_enabled_draft=enabled;ttk.Checkbutton(body,text='게임 패드 사용',variable=enabled).grid(row=16,column=0,columnspan=3,sticky='w',pady=(12,3))
        names=['자동 선택']+[p.get_name() for p in self.devices];device=tk.StringVar(value=self.settings['pad_name'] if self.settings['pad_name'] in names else '자동 선택');self.pad_selection=device
        ttk.Label(body,text='패드 선택').grid(row=17,column=0,sticky='w');ttk.Combobox(body,textvariable=device,values=names,state='readonly',width=35).grid(row=17,column=1,columnspan=2,sticky='ew',padx=6,pady=6)
        def choose_device(event=None):
            self.pad=next((p for p in self.devices if p.get_name()==device.get()),self.devices[0] if self.devices else None)
            self.pad_draft.clear();self.pad_draft.update(self.active_pad_mapping() if self.pad and self.pad.get_guid() in self.settings.get('pad_profiles',{}) else self.controller_defaults());self.refresh_mapping_labels()
        for child in body.winfo_children():
            if isinstance(child,ttk.Combobox):child.bind('<<ComboboxSelected>>',choose_device)
        actions=ttk.Frame(body);actions.grid(row=18,column=0,columnspan=3,sticky='ew',pady=(14,0))
        def finish(save):
            if save:
                self.settings['keys']=draft;self.settings['pad']=dict(self.pad_draft);
                if self.pad:self.settings.setdefault('pad_profiles',{})[self.pad.get_guid()]=dict(self.pad_draft)
                self.settings['pad_enabled']=enabled.get();self.settings['pad_name']='' if device.get()=='자동 선택' else device.get();self.persist()
            self.capture=None;self.pad_draft=None;self.dialog=None;dialog.grab_release();dialog.destroy();self.refresh_devices();self.restore_after_dialog(old)
        def defaults():
            draft.clear();draft.update(DEFAULT_KEYS);self.pad_draft.clear();self.pad_draft.update(self.controller_defaults());self.refresh_mapping_labels()
        ttk.Button(actions,text='기본값',command=defaults).pack(side='left');ttk.Button(actions,text='취소',command=lambda:finish(False)).pack(side='right',padx=4);ttk.Button(actions,text='적용',command=lambda:finish(True)).pack(side='right',padx=4)
        dialog.bind('<KeyPress>',self.capture_key);dialog.protocol('WM_DELETE_WINDOW',lambda:finish(False));dialog.grab_set();dialog.focus_set()

    @staticmethod
    def key_label(key):return {'Return':'Enter','space':'Space','Shift_R':'오른쪽 Shift','Shift_L':'왼쪽 Shift','Up':'↑','Down':'↓','Left':'←','Right':'→'}.get(key,key.upper() if len(key)==1 else key)
    def begin_capture(self,kind,name):
        self.capture=(kind,name);self.capture_text.set(f'{dict((n,label) for n,label,_ in BUTTONS)[name]}에 사용할 {"키" if kind=="key" else "패드 버튼"}를 누르세요. Esc로 취소');self.mapping_buttons[kind,name].config(text='입력 기다림…');self.dialog.focus_set()
    def capture_key(self,event):
        if not self.capture:return
        if event.keysym=='Escape':self.capture=None;self.refresh_mapping_labels();return 'break'
        if self.capture[0]!='key':return 'break'
        key=event.keysym.lower() if len(event.keysym)==1 else event.keysym
        if key in ('F1','F11') or key in self.settings['hotkeys'].values() or event.state&0x000c:self.capture_text.set('이 키는 프로그램 단축키로 사용 중입니다. 다른 키를 눌러주세요.');return 'break'
        self.assign_capture(key);return 'break'
    def assign_capture(self,value):
        if not self.capture:return
        if self.capture[0] in ('shortcut_key','shortcut_pad'):self.assign_shortcut_capture(value);return
        if self.capture[0]=='pad' and value in self.settings['pad_hotkeys'].values():self.capture_text.set('이 버튼은 프로그램 단축키로 사용 중입니다. 다른 버튼을 눌러주세요.');return
        kind,name=self.capture;mapping=self.mapping_draft if kind=='key' else self.pad_draft;old=mapping[name]
        for other,current in list(mapping.items()):
            if other!=name and current==value:mapping[other]=old
        mapping[name]=value;self.capture=None;self.refresh_mapping_labels();self.capture_text.set('설정한 내용은 적용 버튼을 누르면 저장됩니다.')
    def refresh_mapping_labels(self):
        for (kind,name),button in self.mapping_buttons.items():button.config(text=self.key_label(self.mapping_draft[name]) if kind=='key' else f'버튼 {self.pad_draft[name]+1}')

    def help_dialog(self):
        keys=self.settings['hotkeys'];labels=dict(fast_forward='빠른 진행 · 누르는 동안',quick_save='현재 칸에 중간 저장',quick_load='현재 칸 불러오기',pause_resume='일시정지 / 계속',pause='일시정지',resume='계속')
        mapping='\n'.join(f'{self.key_label(key)}: {labels[name]}' for name,key in keys.items() if key)
        old=self.pause_for_dialog();messagebox.showinfo('조작 안내','게임 화면을 클릭한 뒤 키보드나 패드로 조작하세요.\n아래 화면은 마우스로 터치할 수 있습니다.\n\n'+mapping+'\nF1: HD 켜기 / 끄기\nF11: 전체 화면\nCtrl+O: 롬 열기\nCtrl+D: HD 미리보기\nCtrl+R: 다시 시작\n\n설정 → 단축키 · 빠른 진행 설정에서 키와 패드 버튼을 지정할 수 있습니다.\n빠른 진행 중에는 소리와 진동을 잠시 끕니다.\n미리보기 저장과 일반 게임 저장은 따로 보관됩니다.',parent=self.root);self.restore_after_dialog(old)
    def about_dialog(self):
        old=self.pause_for_dialog();messagebox.showinfo('프로그램 정보','슈퍼로봇대전 W HD\n\nDeSmuME libretro 기반 · GPL-2.0-or-later\nhttps://github.com/libretro/desmume\n\n기체 파츠·컷인·초상화·지도·배경과 글자를 HD로 표시합니다.\n원본과 일치하는 자료를 교체하며 미확인 연출은 원본으로 표시합니다.\n\n수정한 원본 소스와 빌드 정보는 프로그램 폴더에 포함되어 있습니다.',parent=self.root);self.restore_after_dialog(old)

    def receive(self,message):
        event=message.get('event')
        if event=='input_ack':self.metrics.acknowledge(message);return
        if event=='rumble':
            if message.get('reason')=='beam_stream' and not self.settings['rumble_beam']:return
            if not message.get('duration'):self.rumble.stop()
            elif self.loaded and not self.paused and not self.dialog and self.has_input_focus():
                self.rumble.play(self.pad,self.settings['pad_enabled'] and self.settings['rumble_enabled'],self.settings['rumble_strength'],message['low'],message['high'],message['duration'])
            return
        if event=='loaded':
            self.loaded=True;self.opening=False;self.save_dir=Path(message['save_dir']);self.paused=message['paused'];self.demo=message['demo'];self.update_buttons();self.refresh_slots();self.canvas.focus_set()
        elif event=='frame':
            if self.memory and self.lock.acquire(False):
                try:
                    revision=message.get('bottom_revision')
                    size=tuple(message.get('render_size',(DEFAULT_WIDTH,DEFAULT_WIDTH*3//4)));rendered_frame=message.get('frame',0)
                    if len(self.memory.buf)>=TOP_BYTES+BOTTOM_BYTES+16:
                        w,h,actual_frame,actual_revision=struct.unpack_from('<IIII',self.memory.buf,TOP_BYTES+BOTTOM_BYTES)
                        if MIN_WIDTH<=w<=MAX_WIDTH and h==w*3//4:size=(w,h);rendered_frame=actual_frame;revision=actual_revision
                    count=size[0]*size[1]*4
                    bottom_changed=self.latest is None or size!=self.latest[0].size or revision is None or revision!=self.last_bottom_revision
                    top_bytes=bytes(self.memory.buf[:count])
                    bottom_bytes=bytes(self.memory.buf[TOP_BYTES:TOP_BYTES+count]) if bottom_changed else None
                finally:self.lock.release()
                # Release the worker's frame lock before allocating/resizing
                # images, so display scaling cannot stall emulation.
                top=RGBFrame(top_bytes,size);bottom=RGBFrame(bottom_bytes,size) if bottom_changed else self.latest[1]
                self.last_bottom_revision=revision
                self.received_frame=rendered_frame
                self.latest=(top,bottom);self.dirty=True
        elif event in ('paused','demo_finished','state_loaded'):
            self.rumble.stop()
            self.paused=message.get('value',message.get('paused',True));self.demo=message.get('demo',self.demo);self.update_buttons()
            if event=='state_loaded':self.status_var.set('저장한 게임을 불러왔습니다. 계속 버튼을 눌러 진행하세요.')
        elif event=='saved':self.status_var.set(f'저장했습니다 · {Path(message["path"]).name}');self.refresh_slots()
        elif event=='hd':self.hd_var.set(message['value'])
        elif event=='status':
            self.metrics.worker={name:message.get(name) for name in ('emulation_fps','composition_fps','render_ms','render_p95_ms')}
            self.metrics.worker['emulated_frame']=message.get('frame')
            self.paused=message['paused'];self.demo=message['demo'];self.update_buttons()
            speed=f' · 빠른 진행 {message.get("speed",1)}배' if message.get('speed',1)>1 else ''
            self.status_var.set(f'{"미리보기 · " if self.demo else ""}{"일시정지" if self.paused else "실행 중"}{speed}  |  HD {"켜짐" if message["hd"] else "꺼짐"}  |  저장 {self.slot_var.get()}번')
        elif event in ('command_error','error'):
            self.rumble.stop()
            if event=='error':self.loaded=False;self.opening=False;self.session_error=True;self.update_buttons()
            messagebox.showerror('게임 실행' if event=='error' else '요청을 처리하지 못했습니다',message['message'],parent=self.root)
        elif event=='audio_unavailable':self.status_var.set('소리 장치를 사용할 수 없습니다. 게임은 계속할 수 있습니다.')
        elif event=='closed':self.rumble.stop();self.loaded=False;self.opening=False;self.update_buttons()

    def poll(self):
        if self.closed:return
        try:
            if self.pipe:
                # The pixel buffer already contains the latest frame. Never
                # decode that same buffer for every queued frame notification.
                pending_frame=None;deadline=time.perf_counter()+.004
                while self.pipe.poll():
                    message=self.pipe.recv()
                    if message.get('event')=='frame':pending_frame=message
                    else:self.receive(message)
                    if time.perf_counter()>=deadline:break
                if pending_frame:self.receive(pending_frame)
        except (EOFError,BrokenPipeError,OSError):pass
        if self.process and not self.process.is_alive() and (self.loaded or self.opening):
            self.rumble.stop()
            self.loaded=False;self.opening=False;self.update_buttons();self.status_var.set('게임 실행이 종료되었습니다. 롬을 다시 열 수 있습니다.')
        if self.gpu is not None:self.gpu.events(self)
        self.physical_keyboard.poll(self)
        pad=self.poll_pad()
        active=self.has_input_focus() and not self.dialog
        self.set_fast_forward(active and (self.pad_fast_forward or self.settings['hotkeys']['fast_forward'] in self.action_keys_down))
        self.last_pad_buttons=pad;self.flush_game_input(pad)
        if self.dirty:self.draw()
        if self.metrics.path is not None:
            self.metrics.worker.update(focus_widget=str(self.root.focus_get()),held=sorted(self.held),sdl_keyboard_events=self.gpu.keyboard_events if self.gpu else 0,physical_keyboard_events=self.physical_keyboard.events,foreground=self.has_input_focus(),render_width=self.latest[0].width if self.latest else self.render_width)
        self.metrics.update('gpu' if self.gpu is not None else 'software')
        self.root.after(1 if self.gpu is not None else 4,self.poll)

    def close(self):
        if self.closed:return
        self.closed=True;self.settings['geometry']=self.window_geometry if bool(self.root.attributes('-fullscreen')) else self.root.geometry();self.persist();self.stop_worker()
        if getattr(self,'pygame',None):self.pygame.quit()
        if self.timer_precision is not None:self.timer_precision.timeEndPeriod(1);self.timer_precision=None
        self.root.destroy()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--demo',action='store_true');parser.add_argument('--rom',type=Path);parser.add_argument('--state',type=Path);parser.add_argument('--state-frame',type=int,default=64700);parser.add_argument('--paused',action='store_true');parser.add_argument('--no-start',action='store_true');parser.add_argument('--config',type=Path);parser.add_argument('--save-root',type=Path);parser.add_argument('--software-display',action='store_true');parser.add_argument('--legacy-timing',action='store_true');parser.add_argument('--metrics',type=Path);parser.add_argument('--profile-render',type=Path)
    args=parser.parse_args()
    try:
        import ctypes;ctypes.windll.user32.SetProcessDPIAware()
    except Exception:pass
    root=tk.Tk();EmulatorWindow(root,args);root.mainloop()

if __name__=='__main__':
    mp.freeze_support()
    try:main()
    except Exception:
        (HERE/'player_ui_error.log').write_text(traceback.format_exc(),encoding='utf-8');raise
