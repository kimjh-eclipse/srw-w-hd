"""Interactive unit/weapon replay selector with isolated player data."""
import argparse,json,multiprocessing as mp,sys,os
from pathlib import Path
from types import SimpleNamespace
import tkinter as tk
from tkinter import ttk
from runtime_paths import APP_DIR,FROZEN
from hd_emulator import EmulatorWindow,CANONICAL


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--workspace',type=Path)
    parser.add_argument('--rom',type=Path)
    parser.add_argument('--unit',type=int,help='open this unit right away')
    parser.add_argument('--weapon',type=int,help='with --unit: play this weapon from the start')
    opts=parser.parse_args()
    candidates=[opts.workspace,APP_DIR,APP_DIR.parent.parent]
    ROOT=next((p for p in candidates if p and (p/'test_current/parts/named_unit_catalog.json').exists()),None)
    if ROOT is None:
        from tkinter import messagebox
        root=tk.Tk();root.withdraw()
        messagebox.showerror('테스트 자료 없음','기체별 테스트 자료가 있는 작업 폴더가 필요합니다.\n--workspace 옵션으로 폴더를 지정하세요.',parent=root)
        root.destroy();return
    if FROZEN:os.environ['SRWW_TEST_WORKSPACE']=str(ROOT)
    rom=opts.rom or ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds'
    if not rom.exists():raise FileNotFoundError('테스트 ROM을 찾을 수 없습니다: '+str(rom))
    catalog=json.loads((ROOT/'test_current/parts/named_unit_catalog.json').read_text(encoding='utf-8'))
    names={r['unit_id']:r.get('name_ko') or r['name_ja'] for r in catalog['units']}
    weapons={r['weapon_id']:r.get('name_ko') or r['name_ja'] for r in catalog['weapons']}
    scenes={}
    START='처음부터 · '
    # Every unit and weapon can be played from the first frame of its attack:
    # the start state is built on demand (attack_start.py) and kept in a cache.
    for record in catalog['units']:
        if record.get('weapon_ids') and record.get('primary_image') is not None:
            for index,wid in enumerate(record['weapon_ids']):
                scenes.setdefault(record['unit_id'],{})[f'{START}{index+1:02d} {weapons.get(wid,str(wid))}']=('start',record['unit_id'],wid)
    for path in (ROOT/'test_current/combat/named_attacks').rglob('*.state'):
        unit=next((int(p[5:]) for p in path.parts if p.startswith('unit_') and p[5:].isdigit()),None)
        if unit is None or path.stem=='capture':continue
        weapon=next((int(p.split('_')[1]) for p in path.parts if p.startswith('weapon_') and p.endswith('_capture')),None)
        label='저장 장면 · '+(weapons.get(weapon,str(weapon))+' · ' if weapon is not None else '')+path.stem
        if 'native_reference' in path.parts:label+=' · 원본 재생 기반'
        scenes.setdefault(unit,{})[label]=path
    out=ROOT/'test_current/gui/unit_review';out.mkdir(parents=True,exist_ok=True)
    initial=ROOT/'test_current/combat/named_attacks/unit_413/native_reference/diagnostic_preview/weapon_1613_capture/frame_360.state'
    args=SimpleNamespace(config=out/'settings.json',save_root=out/'isolated_saves',metrics=out/'metrics.json',profile_render=None,software_display=False,legacy_timing=False,no_start=False,demo=False,rom=rom,state=initial,state_frame=0,paused=False)
    root=tk.Tk();app=EmulatorWindow(root,args)
    panel=ttk.Frame(root,padding=4);panel.pack(fill='x',before=app.canvas)
    labels={f'{names.get(uid,uid)} [{uid}]':uid for uid in sorted(scenes,key=lambda n:(n!=413,n))}
    unit=tk.StringVar(value=next(iter(labels)));scene=tk.StringVar()
    ttk.Label(panel,text='기체').pack(side='left');units=ttk.Combobox(panel,textvariable=unit,values=list(labels),state='readonly',width=29);units.pack(side='left')
    ttk.Label(panel,text=' 장면').pack(side='left');frames=ttk.Combobox(panel,textvariable=scene,state='readonly',width=47);frames.pack(side='left',fill='x',expand=True)
    def refresh(event=None):
        options=sorted(scenes[labels[unit.get()]],key=lambda s:(not s.startswith(START),s));frames['values']=options;scene.set(options[0])
    status=tk.StringVar(value='')
    cache=out/'attack_starts';cache.mkdir(exist_ok=True)
    def load():
        choice=scenes[labels[unit.get()]][scene.get()]
        if not isinstance(choice,tuple):
            status.set('');app.start_session(rom,state=choice,state_frame=0,paused=False);return
        _,uid,wid=choice;target=cache/f'unit_{uid}_weapon_{wid}.state'
        if target.exists():
            status.set('');app.start_session(rom,state=target,state_frame=0,paused=False);return
        status.set('공격 시작 장면 만드는 중… (몇 초)');open_button.state(['disabled'])
        import threading
        def work():
            from attack_start import build_in_child
            result=build_in_child(ROOT,rom,uid,wid,target)
            def done():
                open_button.state(['!disabled'])
                if result.get('ok') and target.exists():status.set('');app.start_session(rom,state=target,state_frame=0,paused=False)
                else:status.set('열 수 없음: '+result.get('reason','알 수 없는 오류'))
            root.after(0,done)
        threading.Thread(target=work,daemon=True).start()
    open_button=ttk.Button(panel,text='장면 열기',command=load);open_button.pack(side='left')
    ttk.Label(panel,textvariable=status,foreground='#b04020').pack(side='left',padx=6)
    ttk.Label(panel,text='진단 재생 · 세이브 분리').pack(side='right');units.bind('<<ComboboxSelected>>',refresh);refresh()
    # Match the selector to the scene initially displayed.
    for label,path in scenes[413].items():
        if path==initial:scene.set(label);break
    if opts.unit is not None and opts.unit in scenes:
        unit.set(next(k for k,v in labels.items() if v==opts.unit));refresh()
        if opts.weapon is not None:
            pick=next((k for k,v in scenes[opts.unit].items() if isinstance(v,tuple) and v[2]==opts.weapon),None)
            if pick:scene.set(pick)
        root.after(500,load)
    def title():
        if app.closed:return
        root.title('슈퍼로봇대전 W HD · 기체별 전투 테스트');root.after(500,title)
    root.after(250,title);root.mainloop()


if __name__=='__main__':mp.freeze_support();main()
