"""Persistent player preferences and device-independent DS input mappings."""
from pathlib import Path
import copy,json,tempfile,os,time

BUTTONS=[('up','위',4),('down','아래',5),('left','왼쪽',6),('right','오른쪽',7),('a','A · 확인',8),('b','B · 취소',0),('x','X',9),('y','Y',1),('l','L',10),('r','R',11),('start','Start',3),('select','Select',2)]
DEFAULT_KEYS=dict(up='Up',down='Down',left='Left',right='Right',a='z',b='x',x='c',y='v',l='a',r='s',start='Return',select='Shift_R')
DEFAULT_PAD=dict(a=0,b=1,x=2,y=3,l=4,r=5,start=7,select=6)
SHORTCUTS=[('fast_forward','빠른 진행 · 누르는 동안'),('quick_save','중간 저장'),('quick_load','중간 불러오기'),('pause_resume','일시정지 / 계속'),('pause','일시정지'),('resume','계속')]
DEFAULT_HOTKEYS=dict(fast_forward='Tab',quick_save='F5',quick_load='F8',pause_resume='space',pause='Pause',resume='F6')
DEFAULT_PAD_HOTKEYS={name:None for name,_ in SHORTCUTS}
LAYOUTS=[('large_horizontal','메인 크게 · 가로'),('large_vertical','메인 크게 · 세로'),('equal_horizontal','같은 크기 · 가로'),('equal_vertical','같은 크기 · 세로')]
LAYOUT_ALIASES=dict(side='large_horizontal',stack='equal_vertical')
DEFAULTS=dict(keys=DEFAULT_KEYS,pad=DEFAULT_PAD,pad_enabled=True,pad_name='',deadzone=.3,layout='large_horizontal',swap=False,hd=True,volume=70,slot=1,recent=[],auto_pause=False,geometry='1280x850')
DEFAULTS.update(rumble_enabled=True,rumble_strength=95,rumble_beam=True)
DEFAULTS.update(hd_auto_quality=True)
DEFAULTS.update(pad_profiles={})
DEFAULTS.update(hotkeys=DEFAULT_HOTKEYS,pad_hotkeys=DEFAULT_PAD_HOTKEYS,fast_forward_speed=4)

def read_settings(path):
    result=copy.deepcopy(DEFAULTS)
    try:
        stored=json.loads(Path(path).read_text(encoding='utf-8'))
        for name in result:
            if name in stored and isinstance(stored[name],type(result[name])):result[name]=stored[name]
        result['keys']={**DEFAULT_KEYS,**{k:v for k,v in result['keys'].items() if k in DEFAULT_KEYS and isinstance(v,str)}}
        result['pad']={**DEFAULT_PAD,**{k:v for k,v in result['pad'].items() if k in DEFAULT_PAD and isinstance(v,int) and v>=0}}
    except (OSError,ValueError,TypeError):pass
    result['layout']=LAYOUT_ALIASES.get(result['layout'],result['layout'])
    result['layout']=result['layout'] if result['layout'] in tuple(k for k,_ in LAYOUTS)+('top',) else 'large_horizontal'
    result['volume']=max(0,min(100,result['volume']));result['slot']=max(1,min(5,result['slot']))
    result['rumble_strength']=max(0,min(100,result['rumble_strength']))
    result['hotkeys']={name:result['hotkeys'].get(name,default) for name,default in DEFAULT_HOTKEYS.items()}
    result['hotkeys']={name:key if isinstance(key,str) and key not in ('F1','F11','Escape') and key not in result['keys'].values() else '' for name,key in result['hotkeys'].items()}
    result['pad_hotkeys']={name:value if type(value) is int and value>=0 and value not in result['pad'].values() else None for name in DEFAULT_PAD_HOTKEYS for value in [result['pad_hotkeys'].get(name)]}
    result['fast_forward_speed']=result['fast_forward_speed'] if result['fast_forward_speed'] in (2,4,8,16) else 4
    return result

def sdl_pad_mapping(sdl_mapping):
    """Translate SDL semantic button names to this joystick's physical indices."""
    result=dict(DEFAULT_PAD)
    names=dict(a='a',b='b',x='x',y='y',l='leftshoulder',r='rightshoulder',start='start',select='back',up='dpup',down='dpdown',left='dpleft',right='dpright')
    for name,semantic in names.items():
        value=sdl_mapping.get(semantic,'')
        if isinstance(value,str) and value.startswith('b') and value[1:].isdigit():result[name]=int(value[1:])
    return result

def write_settings(path,settings):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    # Each player owns its temporary file, even when sharing one config.
    fd,name=tempfile.mkstemp(prefix=path.stem+'-',suffix='.tmp',dir=path.parent);temp=Path(name)
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as stream:stream.write(json.dumps(settings,ensure_ascii=False,indent=2))
        for attempt in range(10):
            try:temp.replace(path);break
            except PermissionError:
                if attempt==9:raise
                time.sleep(.01)
    finally:temp.unlink(missing_ok=True)

def key_buttons(held,mapping):
    return {index for name,_,index in BUTTONS if mapping.get(name) in held}

def pad_buttons(buttons,axes,hats,mapping,deadzone=.3):
    result={index for name,_,index in BUTTONS if name in mapping and mapping[name] in buttons}
    x=axes[0] if len(axes)>0 else 0;y=axes[1] if len(axes)>1 else 0
    # A deliberate D-pad direction takes precedence over analog stick drift.
    if any(hx for hx,_ in hats) or result&{6,7}:x=0
    if any(hy for _,hy in hats) or result&{4,5}:y=0
    if x < -deadzone:result.add(6)
    if x > deadzone:result.add(7)
    if y < -deadzone:result.add(4)
    if y > deadzone:result.add(5)
    for hx,hy in hats:
        if hx<0:result.add(6)
        if hx>0:result.add(7)
        if hy>0:result.add(4)
        if hy<0:result.add(5)
    return result

def screen_rectangles(width,height,layout='large_horizontal',swap=False):
    """Return physical top/bottom display rectangles, preserving 4:3."""
    gap=0;pad=0;w=max(1,width);h=max(1,height)
    layout=LAYOUT_ALIASES.get(layout,layout)
    if layout=='top':
        scale=min(w/4,h/3);rw,rh=round(4*scale),round(3*scale)
        return [(round(pad+(w-rw)/2),round(pad+(h-rh)/2),rw,rh),None]
    vertical=layout in ('large_vertical','equal_vertical');factor=3 if layout in ('large_vertical','large_horizontal') else 1
    if vertical:
        scale=max(.01,min(w/(4*factor),(h-gap)/(3*(factor+1))))
        stage_w,stage_h=4*factor*scale,3*(factor+1)*scale+gap
        x=pad+(w-stage_w)/2;y=pad+(h-stage_h)/2
        main=(round(x),round(y),round(4*factor*scale),round(3*factor*scale))
        result=[main,(round(x+2*(factor-1)*scale),main[1]+main[3]+gap,round(4*scale),round(3*scale))]
    else:
        scale=max(.01,min((w-gap)/(4*(factor+1)),h/(3*factor)))
        stage_w,stage_h=4*(factor+1)*scale+gap,3*factor*scale
        x=pad+(w-stage_w)/2;y=pad+(h-stage_h)/2
        main=(round(x),round(y),round(4*factor*scale),round(3*factor*scale))
        result=[main,(main[0]+main[2]+gap,round(y+1.5*(factor-1)*scale),round(4*scale),round(3*scale))]
    if swap and layout!='top':result.reverse()
    return result

def touch_position(x,y,rectangle):
    if not rectangle:return None
    left,top,w,h=rectangle
    if not (left<=x<left+w and top<=y<top+h):return None
    return (max(-32767,min(32767,round(((x-left)/w*2-1)*32767))),max(-32767,min(32767,round(((y-top)/h*2-1)*32767))))
