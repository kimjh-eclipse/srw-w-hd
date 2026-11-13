"""FHD presentation for the custom DeSmuME cut-in bridge."""
from pathlib import Path
from collections import OrderedDict
import os
import zlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageChops
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
from painted_edges import clean_alpha,cutin_visibility
from cutin_assets import CutinAssets

from asset_paths import asset_root
ROOT=asset_root(Path(__file__).resolve().parent.parent)

def character_cutin(spec,identifier):
    """Presentation role follows the asset family, including compact pilots."""
    return identifier==1 or spec.get('presentation_role')=='pilot_foreground' or spec.get('name','').startswith('compact_pilot_bg_') or spec.get('image','').startswith('compact_pilot_cutins/')

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
        self.map_tiles=MapTilesRenderer(async_prepare=async_parts)
        self.map_icons=MapIconRenderer()
        self.localized_screens=LocalizedScreens()
        self.ui_labels=UILabelRenderer()
        self.battle_backgrounds=BattleBackgroundRenderer(async_prepare=async_parts)
        self.cutins=CutinAssets(ROOT,self.art,MAX_WIDTH)
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
        self.cutins.set_width(width);self.art=self.cutins[1]
        self.backgrounds.viewports.clear();self.backgrounds.mask_plans.clear()
        self.scenario_backgrounds.generation+=1
        self.menu_scene.width=width;self.menu_scene.art.clear();self.menu_scene.group_key=None;self.menu_scene.grid_key=None
        self.bottom_frame_key=None

    def cutin_gradient(self,cutin,live):
        """Brightness -> colour table for a grey cut-in the game colours through its palette.

        The picture's ROM palette is a rising grey ramp over slots 1-15 and
        the game puts a coloured, animated ramp in the bank it uses. A grey
        level of the HD picture is placed between the ramp's slots and takes
        the live colours of those slots. Returns a 256x1 picture or None.
        """
        if live is None or os.environ.get('SRWW_CUTIN_TINT','1')=='0':return None
        tables=self.__dict__.get('runtime_palettes')
        if tables is None:
            import json
            try:tables=json.loads((ROOT/'graphics/cutin_runtime_palettes.json').read_text(encoding='utf-8'))
            except (OSError,ValueError):tables={}
            self.runtime_palettes=tables;self.gradient_cache=OrderedDict()
        entry=tables.get(str(cutin))
        if entry is None:return None
        bank,colours=live;key=(cutin,bank,colours.tobytes());found=self.gradient_cache.pop(key,None)
        if found is None:
            ramp=np.asarray(entry['ramp'],dtype='float64')*255/31;levels=np.unique(ramp)
            slots=np.array([np.flatnonzero(ramp==level).mean()+1 for level in levels])          # slot (1-15) each grey level stands for
            position=np.interp(np.arange(256,dtype='float64'),levels,slots)
            values=np.asarray(colours,dtype='uint32');rgb=np.stack([(values&31)*255/31,((values>>5)&31)*255/31,((values>>10)&31)*255/31],-1)
            table=np.stack([np.interp(position,np.arange(16),rgb[:,channel]) for channel in range(3)],-1)
            found=Image.fromarray(np.clip(np.rint(table),0,255).astype('uint8')[None,:,:])
        self.gradient_cache[key]=found
        while len(self.gradient_cache)>64:self.gradient_cache.popitem(last=False)
        return found

    def render_top(self,native,layer_ids,hd,paused=False,robot=None,obj=None,parts=None,owners=None,bgpriors=None,bgparts=None,part_palettes=None,backgrounds=None,unknown=None,bg_layout=None,sub_parts=None,cutin_layers=None,effect_foreground=None,window=None,cutin_palettes=None):
        self.frame_number=getattr(self,'frame_number',0)+1;self.text_renderer.frame_token=self.frame_number
        if effect_foreground is not None:
            # No blending BG anywhere on this frame: skip every per-layer test.
            from foreground_blend import active
            if not active(effect_foreground).any():effect_foreground=None
        from foreground_blend import begin_frame
        begin_frame(effect_foreground,bgpriors)
        cutins=[hd] if hd[0] else []
        if hd[10] and cutin_layers is not None:
            planes=[row for row in cutin_layers if row[0] and int(row[0]) in self.cutins]
            if planes:
                # Back to front: native ties put the smaller BG number on top.
                cutins=sorted(planes,key=lambda row:(int(row[6]),int(row[5])),reverse=True)
        stage=self.localized_screens.stage_key(native)
        if stage is not None:
            from stage_cache import begin_stage
            if begin_stage(stage):self.parts_renderer.prefetched_groups.clear()
        self.sub_parts=sub_parts
        self.sub_paused=paused
        parts_layer_ids=layer_ids
        if hd[10]:self.parts_renderer.schedule_unknown(unknown)
        border=native[124:132]
        cyan=np.count_nonzero((border[:,:,0]<64)&(border[:,:,1]>96)&(border[:,:,2]>96))>=80
        battle_layout=bg_layout is not None and len(bg_layout)==4 and bg_layout[3][2]==0x06018000 and bg_layout[2][2]==0x06010000
        # HP labels disappear during attacks, but the battle dialogue frame
        # and its dedicated VRAM banks remain. Keep scanning only text areas
        # instead of treating every animated star/beam as a possible glyph.
        is_battle=bool(hd[0]) or battle_layout
        self.text_renderer.set_battle_scan(is_battle)
        if hd[10]:self.text_renderer.recognize(native)
        hud_mask=getattr(self.text_renderer,'hud_mask',None) if hd[10] else None
        self.backgrounds.hud_mask=hud_mask;self.battle_backgrounds.hud_mask=hud_mask
        if os.environ.get('SRWW_WINDOW_MASK','1')=='0':window=None
        self.backgrounds.window=window;self.battle_backgrounds.window=window
        menu_kind=self.menu_scene.identify(backgrounds,parts) if hd[10] and not hd[0] else None
        if self.gpu_composition:
            from gpu_surface import Surface
        if menu_kind:
            native_top=Surface(self.size) if self.gpu_composition else Image.new('RGB',self.size)
            if menu_kind=='favorite':native_top.paste(Image.fromarray(native[160:192]).resize((self.size[0],self.size[1]//6),Image.Resampling.NEAREST),(0,self.size[1]*5//6))
            top=native_top
        else:
            display_native=self.text_renderer.clean_native(native) if hd[0] or is_battle else native[:192]
            if hud_mask is not None and hud_mask.any():
                display_native=display_native.copy();healed=self.text_renderer._heal_native(native)
                display_native[hud_mask]=healed[hud_mask]
            native_top=Surface.from_native(display_native,self.size) if self.gpu_composition else Image.fromarray(display_native).resize(self.size,Image.Resampling.NEAREST)
            top=native_top.copy() if hd[0] else native_top
        top.hud_clean=hud_mask is not None and bool(hud_mask.any())
        if hd[10]:
            parts=self.menu_scene.compose(top,native,backgrounds,parts,obj)
            if self.menu_scene.last_scene is None:
                restoration=None;restore_layer=None
                if hd[0]>1 and bgpriors is not None:
                    behind=[i for i in range(4) if int(bgpriors[i])>min(int(row[6]) for row in cutins)]
                    if behind:
                        restoration=np.zeros_like(layer_ids,dtype=bool)
                        for row in cutins:
                            if row[0]<=1:continue
                            area=layer_ids==row[5]
                            rect=self.cutins.specs.get(int(row[0]),{}).get('restore_rect')
                            if rect:
                                x=int(row[1]);y=int(row[2]);x=x if x<256 else x-512;y=y if y<256 else y-512
                                yy,xx=np.indices(area.shape)
                                left,upper,right,lower=rect
                                area&=(xx>=left-x)&(xx<right-x)&(yy>=upper-y)&(yy<lower-y)
                            restoration|=area
                        known=self.battle_backgrounds.matched_layers|{int(row[3]) for row in (backgrounds or ())}
                        candidates=[i for i in behind if i in known]
                        # Empty/effect BG planes may sit between the portrait
                        # and the actual scenery. Erase against a real matched
                        # backdrop, rather than leaving old native edge pixels.
                        restore_layer=max(candidates or behind,key=lambda i:(int(bgpriors[i]),i))
                        parts_layer_ids=layer_ids.copy();parts_layer_ids[restoration]=restore_layer
                for bg in (self.battle_backgrounds,self.backgrounds):
                    bg.restoration_mask=restoration;bg.restoration_layer=restore_layer
                self.battle_backgrounds.compose(top,native,layer_ids,bg_layout)
                replaced={row[1][0] for row in self.battle_backgrounds.last_rows}
                self.backgrounds.compose(top,native,layer_ids,[row for row in (backgrounds or ()) if row[3] not in replaced])
            if self.menu_scene.last_scene is None and not is_battle:self.scenario_backgrounds.compose(top,native)
            if self.menu_scene.last_scene is None and not is_battle:
                terrain=self.map_tiles.compose(top,native)
                if terrain or self.map_tiles.phase(native[:192]) is not None:self.map_icons.compose(top,native,background=getattr(self.map_tiles,'last_background',None) if terrain else None)
        draw_cutins=[]
        for cutin in cutins:
            spec=self.cutins.specs.get(int(cutin[0]),{})
            layer=int(cutin[5])
            if spec.get('repeat_native_plane') and bg_layout is not None and tuple(bg_layout[layer][5:7])==(256,256):
                # Full opaque 256x256 BG pictures wrap in DS hardware. A
                # single shifted HD rectangle leaves a native strip at seams.
                for x in (int(cutin[1])%256,int(cutin[1])%256-256):
                    for y in (int(cutin[2])%256,int(cutin[2])%256-256):
                        copy=list(cutin);copy[1]=x;copy[2]=y;draw_cutins.append(copy)
            else:draw_cutins.append(cutin)
        def draw_cutin(top,cutin):
            x=int(cutin[1]);y=int(cutin[2]);x=x if x<256 else x-512;y=y if y<256 else y-512
            art=self.cutins.get(int(cutin[0]),self.art)
            position=(round(-x*self.size[0]/256),round(-y*self.size[1]/192))
            presentation=character_cutin(self.cutins.specs.get(int(cutin[0]),{}),int(cutin[0]))
            visible=np.array(cutin_visibility(layer_ids,int(cutin[5]),int(cutin[6]),bgpriors,None if presentation else owners,None if presentation else obj))
            foreground=None;foreground_mask=None
            if effect_foreground is not None:
                from foreground_blend import eligibility,gpu_plane
                foreground_mask=eligibility(effect_foreground,layer_ids,bgpriors,int(cutin[6]),int(cutin[5]))
                if foreground_mask.any():
                    visible[foreground_mask]=255
                    if self.gpu_composition:foreground=gpu_plane(effect_foreground,layer_ids,bgpriors,int(cutin[6]),int(cutin[5]))
            if window is not None:
                # The game has shut this BG out inside a window (a full-screen
                # flash): the HD picture must stay out of it as well.
                visible[((window>>int(cutin[5]))&1)==0]=0
            # Native dialogue cells are opaque DS tiles. They must not
            # punch rectangular holes through a painted foreground cut-in;
            # transparent HD lettering is drawn after the complete scene.
            for tx,ty,char in self.text_renderer.last_matches:
                if ty<120:continue
                tw=self.text_renderer.last_sizes[tx,ty];th=self.text_renderer.last_heights[tx,ty]
                visible[max(0,ty-2):min(192,ty+th+2),max(0,tx-2):min(256,tx+tw+2)]=255
            visible=Image.fromarray(visible)
            region,box=self.cutins.region(int(cutin[0]))
            left,upper=position[0]+box[0],position[1]+box[1]
            rect=(left,upper,left+region.width,upper+region.height)
            if self.gpu_composition:
                # Keep native visibility in its 256x192 texture. The GPU
                # combines it with the cached painted alpha, avoiding a
                # full-screen RGBA canvas and several large array copies.
                mode=1;gradient=self.cutin_gradient(int(cutin[0]),None if cutin_palettes is None else cutin_palettes.get(int(cutin[5])))
                if foreground is None and effect_foreground is not None:
                    # The cut-in's own BG may be the blended layer (it fades in
                    # or out): mix the HD picture with what is behind it by the
                    # coefficients the DS used on each scanline.
                    from foreground_blend import self_plane
                    foreground=self_plane(effect_foreground,layer_ids,int(cutin[5]))
                    if foreground is not None:mode=2
                top.draw(region,rect,mask=visible,mask_rect=(0,0,*self.size),alpha=True,foreground=foreground,foreground_rect=(0,0,*self.size),foreground_mode=mode,gradient=gradient)
            else:
                if foreground_mask is not None and foreground_mask.any():
                    from foreground_blend import blend_part
                    scale=self.size[0]/256
                    region=blend_part(region,effect_foreground,foreground_mask,(1/scale,0,left/scale,0,1/scale,upper/scale))
                mask=visible.resize(self.size,Image.Resampling.NEAREST).crop(rect)
                top.paste(region,(left,upper),ImageChops.multiply(mask,region.getchannel('A')))
        pilots=[row for row in draw_cutins if character_cutin(self.cutins.specs.get(int(row[0]),{}),int(row[0]))]
        planes=[(int(row[6]),int(row[5]),lambda target,row=row:draw_cutin(target,row)) for row in draw_cutins if not any(row is pilot for pilot in pilots)]
        if parts is not None:
            # BG effects/cut-ins and OBJ parts share one native priority order.
            # A cloudy BG must not be drawn over an already painted front OBJ.
            self.parts_renderer.compose(top,parts,obj,parts_layer_ids,owners,bgpriors,bgparts,part_palettes,allow_native_fallback=paused,effect_foreground=effect_foreground,background_planes=planes,window=window)
        else:
            for _,_,paint in sorted(planes,key=lambda row:row[:2],reverse=True):paint(top)
        # Character presentation is above units/weapons, below final dialogue.
        # Mechanical cut-ins and opaque effect BGs retain native priority.
        for pilot in pilots:draw_cutin(top,pilot)
        if hd[10] and is_battle and cyan:
            # Dialogue is a final presentation plane, above every HD asset.
            # Native ownership alone is insufficient: raster changes and
            # transparent BG effects can leave another layer ID in this strip.
            # Repair native glyphs before restoring the UI; HD text and faces
            # are painted below, after its frame and background are in place.
            ui=Image.fromarray(self.text_renderer.clean_native(native)[128:192])
            upper=round(128*self.size[1]/192)
            if hasattr(top,'draw'):top.draw(ui,(0,upper,*self.size),nearest=True)
            else:top.paste(ui.resize((self.size[0],self.size[1]-upper),Image.Resampling.NEAREST),(0,upper))
        if hd[0]:self.text_renderer.compose(top,native,only_text=True)
        if hd[10]:self.portraits.compose(top,native)
        # Battle effects already cover the repaired native lettering. Never
        # paint old opaque glyph beds back above HD smoke, flashes or beams.
        if hd[10] and not hd[0]:self.text_renderer.compose(top,native,only_text=is_battle)
        if hd[10]:self.ui_labels.compose(top,native)
        if hd[10]:self.localized_screens.compose(top,native)
        return top

    def render_bottom(self,native,hd):
        source=native[192:384];self.bottom_text_renderer.frame_token=getattr(self,'frame_number',0)
        pending=(hasattr(self,'bottom_portraits') and bool(self.bottom_portraits.pending)) or bool(self.scenario_backgrounds.pending) or bool(self.map_tiles.pending) or bool(self.parts_renderer.pending)
        self.scenario_backgrounds.refresh()
        if hasattr(self.map_tiles,'refresh'):self.map_tiles.refresh()
        self.map_icons.refresh()
        self.localized_screens.refresh()
        sub=getattr(self,'sub_parts',None)
        part_key=tuple(zlib.crc32(v if isinstance(v,bytes) else v.tobytes()) for v in sub) if sub is not None else None
        key=(bool(hd[10]),zlib.crc32(source.tobytes()),self.scenario_backgrounds.generation,getattr(self.map_tiles,'generation',0),self.map_icons.stamp,self.localized_screens.generation,part_key,self.parts_renderer.ready_generation)
        if not pending and getattr(self,'bottom_frame_key',None)==key:return self.bottom_frame
        if self.gpu_composition:
            from gpu_surface import Surface
            bottom=Surface.from_native(source,self.size)
        else:bottom=Image.fromarray(source).resize(self.size,Image.Resampling.NEAREST)
        if hd[10]:
            self.scenario_backgrounds.compose(bottom,source)
            terrain=self.map_tiles.compose(bottom,source)
            if terrain or self.map_tiles.phase(source) is not None:self.map_icons.compose(bottom,source,background=getattr(self.map_tiles,'last_background',None) if terrain else None)
            if sub is not None:
                parts,owners,oam,palettes,layers,priorities=sub
                self.parts_renderer.compose(bottom,parts,oam,layers,owners,priorities,None,palettes,allow_native_fallback=getattr(self,'sub_paused',False))
            if not hasattr(self,'bottom_portraits'):self.bottom_portraits=PortraitRenderer()
            self.bottom_portraits.compose(bottom,source)
            self.bottom_text_renderer.compose(bottom,source)
            self.ui_labels.compose(bottom,source)
            self.localized_screens.compose(bottom,source)
        self.bottom_frame_key=key;self.bottom_frame=bottom;self.bottom_generation=getattr(self,'bottom_generation',0)+1
        return bottom

    def render(self,native,layer_ids,hd,paused=False,robot=None,obj=None,parts=None,owners=None,bgpriors=None,bgparts=None,part_palettes=None,backgrounds=None,unknown=None,bg_layout=None,sub_parts=None,cutin_layers=None,effect_foreground=None,window=None,cutin_palettes=None):
        top=self.render_top(native,layer_ids,hd,paused,robot,obj,parts,owners,bgpriors,bgparts,part_palettes,backgrounds,unknown,bg_layout,sub_parts,cutin_layers,effect_foreground,window,cutin_palettes)
        if hasattr(top,'to_pil'):top=top.to_pil()
        if top.size!=(1440,1080):top=top.resize((1440,1080),Image.Resampling.LANCZOS)
        canvas=Image.new('RGB',(1920,1080));canvas.paste(top,(0,0))
        canvas.paste(self.panels[(int(bool(hd[10])),int(bool(paused)))],(1440,0))
        bottom=self.render_bottom(native,hd)
        bottom=bottom.resize((480,360),Image.Resampling.LANCZOS)
        canvas.paste(bottom,(1440,360))
        return canvas
