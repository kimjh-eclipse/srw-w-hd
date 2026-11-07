"""FHD presentation for the custom DeSmuME cut-in bridge."""
from pathlib import Path
from collections import OrderedDict
import zlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from hd_parts import PartsRenderer
from hd_portraits import PortraitRenderer
from hd_backgrounds import BackgroundRenderer
from hd_fonts import FontRenderer
from menu_scene import MenuScene
from hd_scenario_backgrounds import ScenarioBackgrounds
from hd_map_tiles import MapTilesRenderer
from hd_map_icons import MapIconRenderer
from hd_localized_screens import LocalizedScreens
from hd_ui_labels import UILabelRenderer
from hd_battle_backgrounds import BattleBackgroundRenderer
from render_resolution import clamp_width,DEFAULT_WIDTH,MAX_WIDTH,MAX_HEIGHT

ROOT=Path(__file__).resolve().parent.parent

class HDRenderer:
    def __init__(self,async_parts=False,dynamic_parts=False,gpu_composition=False):
        self.size=None;self.async_parts=async_parts
        self.gpu_composition=False;self.gpu_error=None
        if gpu_composition:
            try:
                from gpu_surface import backend
                backend();self.gpu_composition=True
            except Exception as error:self.gpu_error=str(error)
        self.art=Image.open(ROOT/'graphics/kazuma_cutin_hd.png').convert('RGBA').resize((MAX_WIDTH,MAX_HEIGHT),Image.Resampling.LANCZOS)
        self.parts_renderer=PartsRenderer(async_prepare=async_parts,dynamic_parts=dynamic_parts)
        self.backgrounds=BackgroundRenderer(async_prepare=async_parts);self.portraits=PortraitRenderer();self.cutins={1:self.art};self.cutin_references={}
        self.text_renderer=FontRenderer();self.bottom_text_renderer=FontRenderer();self.menu_scene=MenuScene(self.parts_renderer)
        self.scenario_backgrounds=ScenarioBackgrounds(async_prepare=async_parts)
        self.map_tiles=MapTilesRenderer()
        self.map_icons=MapIconRenderer()
        self.localized_screens=LocalizedScreens()
        self.ui_labels=UILabelRenderer()
        self.battle_backgrounds=BattleBackgroundRenderer(async_prepare=async_parts)
        path=ROOT/'graphics/cutins_library.json'
        if path.exists():
            import json
            for item in json.loads(path.read_text())['cutins']:
                self.cutins[item['id']]=Image.open(ROOT/'graphics'/item['image']).convert('RGBA').resize((MAX_WIDTH,MAX_HEIGHT),Image.Resampling.LANCZOS)
                self.cutin_references[item['id']]=Image.open(ROOT/'graphics/portraits'/(item['name']+'_native.png')).convert('RGBA')
        self.original_cutins=dict(self.cutins)
        self.font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',24)
        self.small=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',19)
        self.panels={}
        for enabled in (0,1):
            for paused in (0,1):
                panel=Image.new('RGB',(480,1080),(15,18,26));d=ImageDraw.Draw(panel)
                for y,text,font,color in [(120,'슈퍼로봇대전 W',self.font,(236,239,248)),(164,'HD 기체 · 배경 · 초상화',self.font,(102,194,255)),
                    (215,'고해상도 ON' if enabled else '고해상도 OFF',self.small,(150,208,177)),
                    (760,'방향키 이동   Z 확인   X 취소',self.small,(220,225,237)),
                    (798,'Enter 시작   A / S 좌우 버튼',self.small,(220,225,237)),
                    (836,'F1 원본 / HD 전환',self.small,(220,225,237)),
                    (874,'Space 일시정지 / 계속',self.small,(220,225,237)),
                    (912,'F5 중간 저장   F8 불러오기',self.small,(220,225,237)),
                    (950,'R 미리보기 다시 보기',self.small,(220,225,237))]:d.text((30,y),text,font=font,fill=color)
                if paused:d.text((30,280),'일시정지 · Space 계속',font=self.small,fill=(255,209,115))
                self.panels[(enabled,paused)]=panel
        self.set_resolution(DEFAULT_WIDTH)

    def set_resolution(self,width):
        width=clamp_width(width)
        size=(width,width*3//4)
        if self.size==size:return
        self.size=size;scale=width/256
        import hd_parts,hd_backgrounds,menu_scene,hd_scenario_backgrounds
        hd_parts.SCALE=scale;hd_backgrounds.SCALE=scale;menu_scene.SCALE=scale;hd_scenario_backgrounds.SCALE=scale
        self.parts_renderer.cache.clear();self.parts_renderer.scaled.clear();self.parts_renderer.material_maps.clear()
        self.cutins={key:art.resize(size,Image.Resampling.LANCZOS) for key,art in self.original_cutins.items()};self.art=self.cutins[1]
        self.backgrounds.close();self.backgrounds=BackgroundRenderer(async_prepare=self.async_parts)
        for future in self.scenario_backgrounds.pending.values():future.cancel()
        self.scenario_backgrounds.pending.clear();self.scenario_backgrounds.art.clear();self.scenario_backgrounds.generation+=1
        self.menu_scene.width=width;self.menu_scene.art.clear();self.menu_scene.group_key=None;self.menu_scene.grid_key=None
        self.bottom_frame_key=None

    def render_top(self,native,layer_ids,hd,paused=False,robot=None,obj=None,parts=None,owners=None,bgpriors=None,bgparts=None,part_palettes=None,backgrounds=None,unknown=None,bg_layout=None):
        if hd[10]:self.parts_renderer.schedule_unknown(unknown)
        header=native[:16];border=native[124:132]
        yellow=np.count_nonzero((header[:,:,0]>=160)&(header[:,:,1]>=120)&(header[:,:,2]<96))>=8
        cyan=np.count_nonzero((border[:,:,0]<64)&(border[:,:,1]>96)&(border[:,:,2]>96))>=80
        battle_layout=bg_layout is not None and len(bg_layout)==4 and bg_layout[3][2]==0x06018000 and bg_layout[2][2]==0x06010000
        is_battle=bool(hd[0]) or (battle_layout and yellow and cyan)
        self.text_renderer.set_battle_scan(is_battle)
        if hd[10]:self.text_renderer.recognize(native)
        hud_mask=getattr(self.text_renderer,'hud_mask',None) if hd[10] else None
        self.backgrounds.hud_mask=hud_mask;self.battle_backgrounds.hud_mask=hud_mask
        menu_kind=self.menu_scene.identify(backgrounds,parts) if hd[10] and not hd[0] else None
        if self.gpu_composition:
            from gpu_surface import Surface
        if menu_kind:
            native_top=Surface(self.size) if self.gpu_composition else Image.new('RGB',self.size)
            if menu_kind=='favorite':native_top.paste(Image.fromarray(native[160:192]).resize((self.size[0],self.size[1]//6),Image.Resampling.NEAREST),(0,self.size[1]*5//6))
            top=native_top
        else:
            display_native=self.text_renderer.clean_native(native) if hd[0]==1 else native[:192]
            if hud_mask is not None and hud_mask.any():
                display_native=display_native.copy();healed=self.text_renderer._heal_native(native)
                display_native[hud_mask]=healed[hud_mask]
            native_top=Surface.from_native(display_native,self.size) if self.gpu_composition else Image.fromarray(display_native).resize(self.size,Image.Resampling.NEAREST)
            top=native_top.copy() if hd[0] else native_top
        top.hud_clean=hud_mask is not None and bool(hud_mask.any())
        if hd[10]:
            parts=self.menu_scene.compose(top,native,backgrounds,parts,obj)
            if self.menu_scene.last_scene is None:
                self.battle_backgrounds.compose(top,native,layer_ids,bg_layout)
                replaced={row[1][0] for row in self.battle_backgrounds.last_rows}
                self.backgrounds.compose(top,native,layer_ids,[row for row in (backgrounds or ()) if row[3] not in replaced])
            if self.menu_scene.last_scene is None and not is_battle:self.scenario_backgrounds.compose(top,native)
            if self.menu_scene.last_scene is None and not is_battle:
                terrain=self.map_tiles.compose(top,native)
                if terrain or self.map_tiles.phase(native[:192]) is not None:self.map_icons.compose(top,native,background=getattr(self.map_tiles,'last_background',None) if terrain else None)
        if parts is not None:
            self.parts_renderer.compose(top,parts,obj,layer_ids,owners,bgpriors,bgparts,part_palettes,allow_native_fallback=paused)
        if hd[0]:
            x=hd[1] if hd[1]<256 else hd[1]-512
            y=hd[2] if hd[2]<256 else hd[2]-512
            art=self.cutins.get(int(hd[0]),self.art)
            position=(round(-x*self.size[0]/256),round(-y*self.size[1]/192))
            if hd[0]==1:top.paste(art,position,art)
            else:
                reference=Image.new('RGBA',(256,192));reference.paste(self.cutin_references[int(hd[0])],(-x,-y));expected=np.asarray(reference)
                visible=(expected[:,:,3]>0)&(layer_ids==hd[5])
                viewport=Image.new('RGBA',self.size);viewport.paste(art,position)
                mask=np.asarray(Image.fromarray(visible.astype('uint8')*255).resize(self.size,Image.Resampling.NEAREST),dtype='uint16')
                mask=Image.fromarray((mask*np.asarray(viewport.getchannel('A'),dtype='uint16')//255).astype('uint8'))
                top.paste(viewport,(0,0),mask)
        if hd[0]==1:
            ui=((layer_ids==4)|(layer_ids==0))&(np.arange(192)[:,None]>=120)
            if self.text_renderer.last_matches:ui&=~self.text_renderer.last_mask
            if ui.any():
                mask=Image.fromarray(ui.astype('uint8')*255).resize(top.size,Image.Resampling.NEAREST)
                top.paste(native_top,(0,0),mask)
            self.text_renderer.compose(top,native,only_text=True)
        if hd[10]:self.portraits.compose(top,native)
        if hd[10] and hd[0]!=1:self.text_renderer.compose(top,native)
        if hd[10]:self.ui_labels.compose(top,native)
        if hd[10]:self.localized_screens.compose(top,native)
        return top

    def render_bottom(self,native,hd):
        source=native[192:384]
        pending=(hasattr(self,'bottom_portraits') and bool(self.bottom_portraits.pending)) or bool(self.scenario_backgrounds.pending)
        self.scenario_backgrounds.refresh()
        if hasattr(self.map_tiles,'refresh'):self.map_tiles.refresh()
        self.map_icons.refresh()
        self.localized_screens.refresh()
        key=(bool(hd[10]),zlib.crc32(source.tobytes()),self.scenario_backgrounds.generation,getattr(self.map_tiles,'generation',0),self.map_icons.stamp,self.localized_screens.generation)
        if not pending and getattr(self,'bottom_frame_key',None)==key:return self.bottom_frame
        if self.gpu_composition:
            from gpu_surface import Surface
            bottom=Surface.from_native(source,self.size)
        else:bottom=Image.fromarray(source).resize(self.size,Image.Resampling.NEAREST)
        if hd[10]:
            self.scenario_backgrounds.compose(bottom,source)
            terrain=self.map_tiles.compose(bottom,source)
            if terrain or self.map_tiles.phase(source) is not None:self.map_icons.compose(bottom,source,background=getattr(self.map_tiles,'last_background',None) if terrain else None)
            if not hasattr(self,'bottom_portraits'):self.bottom_portraits=PortraitRenderer()
            self.bottom_portraits.compose(bottom,source)
            self.bottom_text_renderer.compose(bottom,source)
            self.ui_labels.compose(bottom,source)
            self.localized_screens.compose(bottom,source)
        self.bottom_frame_key=key;self.bottom_frame=bottom;self.bottom_generation=getattr(self,'bottom_generation',0)+1
        return bottom

    def render(self,native,layer_ids,hd,paused=False,robot=None,obj=None,parts=None,owners=None,bgpriors=None,bgparts=None,part_palettes=None,backgrounds=None,unknown=None,bg_layout=None):
        top=self.render_top(native,layer_ids,hd,paused,robot,obj,parts,owners,bgpriors,bgparts,part_palettes,backgrounds,unknown,bg_layout)
        if hasattr(top,'to_pil'):top=top.to_pil()
        if top.size!=(1440,1080):top=top.resize((1440,1080),Image.Resampling.LANCZOS)
        canvas=Image.new('RGB',(1920,1080));canvas.paste(top,(0,0))
        canvas.paste(self.panels[(int(bool(hd[10])),int(bool(paused)))],(1440,0))
        bottom=self.render_bottom(native,hd)
        bottom=bottom.resize((480,360),Image.Resampling.LANCZOS)
        canvas.paste(bottom,(1440,360))
        return canvas
