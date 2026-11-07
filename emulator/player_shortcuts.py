"""Configurable keyboard/controller actions, separate from DS game inputs."""
import copy
import tkinter as tk
from tkinter import ttk
from player_controls import SHORTCUTS,DEFAULT_HOTKEYS,DEFAULT_PAD_HOTKEYS

class ShortcutMixin:
    def init_shortcuts(self):
        self.action_keys_down=set();self.fast_forward=False;self.pad_fast_forward=False

    def set_fast_forward(self,value):
        value=bool(value and self.loaded and not self.paused and not self.dialog)
        if value==self.fast_forward:return
        self.fast_forward=value;self.rumble.stop()
        self.send('speed',value=self.settings['fast_forward_speed'] if value else 1)

    def release_shortcuts(self):
        self.action_keys_down.clear();self.pad_fast_forward=False;self.set_fast_forward(False)

    def run_action(self,name):
        if not self.loaded or self.dialog:return
        if name=='quick_save':self.quick_save()
        elif name=='quick_load':self.quick_load()
        elif name=='pause_resume':self.toggle_pause()
        elif name=='pause' and not self.paused:self.toggle_pause()
        elif name=='resume' and self.paused:self.toggle_pause()

    def update_shortcut_labels(self):
        for index,name in ((0,'pause_resume'),(5,'quick_save'),(6,'quick_load')):
            self.game_menu.entryconfigure(index,accelerator=self.key_label(self.settings['hotkeys'][name]) or '미지정')

    def shortcuts_dialog(self):
        if self.dialog:self.dialog.lift();return
        old=self.pause_for_dialog();dialog=tk.Toplevel(self.root);self.dialog=dialog
        dialog.title('단축키 · 빠른 진행 설정');dialog.transient(self.root);dialog.resizable(False,False)
        self.shortcut_draft=copy.deepcopy(self.settings['hotkeys']);self.pad_shortcut_draft=copy.deepcopy(self.settings['pad_hotkeys']);self.shortcut_buttons={}
        body=ttk.Frame(dialog,padding=18);body.pack(fill='both',expand=True)
        ttk.Label(body,text='설정할 칸을 누른 뒤 키 또는 패드 버튼을 누르세요.').grid(row=0,column=0,columnspan=4,sticky='w',pady=(0,12))
        for column,label in enumerate(('기능','키보드','게임패드','')):ttk.Label(body,text=label).grid(row=1,column=column,padx=8)
        for row,(name,label) in enumerate(SHORTCUTS,2):
            ttk.Label(body,text=label).grid(row=row,column=0,sticky='w',pady=5)
            for column,kind in ((1,'shortcut_key'),(2,'shortcut_pad')):
                button=ttk.Button(body,width=19,command=lambda k=kind,n=name:self.begin_shortcut_capture(k,n));button.grid(row=row,column=column,padx=5);self.shortcut_buttons[kind,name]=button
            ttk.Button(body,text='지우기',command=lambda n=name:self.clear_shortcut(n)).grid(row=row,column=3,padx=5)
        self.shortcut_note=tk.StringVar(value='빠른 진행은 누르는 동안 작동합니다. 저장·불러오기는 현재 선택한 저장 칸을 사용합니다.')
        ttk.Label(body,textvariable=self.shortcut_note,wraplength=600).grid(row=8,column=0,columnspan=4,sticky='w',pady=12)
        ttk.Label(body,text='빠른 진행 배속').grid(row=9,column=0,sticky='w');speed=tk.StringVar(value=str(self.settings['fast_forward_speed'])+'배')
        ttk.Combobox(body,textvariable=speed,values=('2배','4배','8배','16배'),state='readonly',width=16).grid(row=9,column=1,sticky='w',padx=5)
        ttk.Label(body,text='실제 속도는 기기 성능에 따라 달라집니다.').grid(row=10,column=0,columnspan=4,sticky='w',pady=6)
        actions=ttk.Frame(body);actions.grid(row=11,column=0,columnspan=4,sticky='ew',pady=(12,0))
        def finish(save=False):
            if save:
                if any(value and value in self.settings['keys'].values() for value in self.shortcut_draft.values()):
                    self.shortcut_note.set('게임 조작 키와 겹치는 항목이 있습니다. 다른 키로 바꿔주세요.');return
                self.settings.update(hotkeys=self.shortcut_draft,pad_hotkeys=self.pad_shortcut_draft,fast_forward_speed=int(speed.get()[:-1]));self.persist();self.update_shortcut_labels()
            self.capture=None;self.dialog=None;dialog.grab_release();dialog.destroy();self.restore_after_dialog(old)
        def defaults():
            self.shortcut_draft=copy.deepcopy(DEFAULT_HOTKEYS);self.pad_shortcut_draft=copy.deepcopy(DEFAULT_PAD_HOTKEYS);speed.set('4배');self.refresh_shortcut_labels()
        ttk.Button(actions,text='기본값',command=defaults).pack(side='left');ttk.Button(actions,text='취소',command=finish).pack(side='right');ttk.Button(actions,text='적용',command=lambda:finish(True)).pack(side='right',padx=6)
        self.refresh_shortcut_labels();dialog.bind('<KeyPress>',self.capture_shortcut_key);dialog.protocol('WM_DELETE_WINDOW',finish);dialog.grab_set();dialog.focus_set()

    def clear_shortcut(self,name):
        self.shortcut_draft[name]='';self.pad_shortcut_draft[name]=None;self.capture=None;self.refresh_shortcut_labels()

    def refresh_shortcut_labels(self):
        for (kind,name),button in self.shortcut_buttons.items():
            value=self.shortcut_draft[name] if kind=='shortcut_key' else self.pad_shortcut_draft[name]
            button.config(text=(self.key_label(value) if value else '미지정') if kind=='shortcut_key' else ('미지정' if value is None else f'버튼 {value+1}'))

    def begin_shortcut_capture(self,kind,name):
        self.capture=(kind,name);self.shortcut_buttons[kind,name].config(text='입력 기다림…');self.shortcut_note.set('Esc: 취소 · 게임 조작에 쓰는 키/버튼은 먼저 조작 설정에서 바꿔주세요.');self.dialog.focus_set()

    def capture_shortcut_key(self,event):
        if not self.capture:return 'break'
        if event.keysym=='Escape':self.capture=None;self.refresh_shortcut_labels();return 'break'
        if self.capture[0]=='shortcut_key':
            if event.state&0x000c or event.keysym in ('F1','F11'):
                self.shortcut_note.set('이 키는 프로그램에서 사용 중입니다. 다른 키를 눌러주세요.');return 'break'
            self.assign_shortcut_capture(event.keysym.lower() if len(event.keysym)==1 else event.keysym)
        return 'break'

    def assign_shortcut_capture(self,value):
        kind,name=self.capture;keys=kind=='shortcut_key';mapping=self.shortcut_draft if keys else self.pad_shortcut_draft
        if value in self.settings['keys' if keys else 'pad'].values():
            self.shortcut_note.set('게임 조작과 겹칩니다. 다른 키/버튼을 선택하거나 조작 설정을 먼저 바꿔주세요.');return
        old=mapping[name]
        for other,current in mapping.items():
            if other!=name and current==value:mapping[other]=old
        mapping[name]=value;self.capture=None;self.refresh_shortcut_labels();self.shortcut_note.set('적용 버튼을 누르면 저장됩니다.')
