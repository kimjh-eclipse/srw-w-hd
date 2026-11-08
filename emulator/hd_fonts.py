"""Exact Korean 1.0.8 bitmap glyph recognition and scalable text presentation.

This uses the patch's KS X 1001 glyph order, not OCR or inferred dialogue.
Unknown, clipped and partially revealed glyphs remain native.
"""
from pathlib import Path
from collections import OrderedDict
import hashlib,zlib
import unicodedata,threading
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from asset_paths import asset_root
ROOT =asset_root(Path(__file__).resolve().parent.parent)
_native_scanners=threading.local()


class FontRenderer:
    def __init__(self):
        # Prepared recognition data is sufficient for distribution: neither
        # the Japanese source ROM nor a second Korean ROM belongs in the app.
        with np.load(ROOT/'graphics/fonts/text_patterns.npz',allow_pickle=False) as source:
            self.keys=source['keys'];self.characters=source['characters'].tolist()
            self.narrow_keys=source['narrow_keys'];self.narrow_characters=source['narrow_characters'].tolist()
        with np.load(ROOT / 'graphics/fonts/hud_glyphs.npz') as source:
            self.compact_patterns = {np.packbits((a == 14) | (a == 15)).tobytes(): str(ch)
                                     for a, ch in zip(source['indices'], source['characters'])}
        self.compact_keys = np.array(sorted(self.compact_patterns), dtype='V8')
        self.compact_characters = [self.compact_patterns[k.tobytes()] for k in self.compact_keys]
        with np.load(ROOT/'graphics/fonts/battle_hud_glyphs.npz') as source:
            hud={np.packbits(a>=13).tobytes():str(ch) for a,ch in zip(source['indices'],source['characters'])}
            labels={np.packbits(a>0).tobytes():str(ch) for a,ch in zip(source['labels'],source['label_names'])}
            self.hud_patterns=[(str(ch),a>=13,a>0) for a,ch in zip(source['indices'],source['characters'])]
        self.hud_keys=np.array(sorted(hud),dtype='V16');self.hud_characters=[hud[k.tobytes()] for k in self.hud_keys]
        self.hud_label_keys=np.array(sorted(labels),dtype='V32');self.hud_label_characters=[labels[k.tobytes()] for k in self.hud_label_keys]
        self.forecast_patterns=[]
        forecast=ROOT/'graphics/fonts/forecast_glyphs.npz'
        if forecast.exists():
            with np.load(forecast,allow_pickle=False) as source:
                self.forecast_patterns=[(str(ch),a>1,a>0) for a,ch in zip(source['indices'],source['characters'])]
        self.font_path = 'C:/Windows/Fonts/malgun.ttf'
        self.fonts = {}
        if not hasattr(_native_scanners,'glyph_tables'):_native_scanners.glyph_tables={}
        if self.font_path not in _native_scanners.glyph_tables:_native_scanners.glyph_tables[self.font_path]=(OrderedDict(),{})
        self.glyph_images,self.fonts=_native_scanners.glyph_tables[self.font_path]
        if not hasattr(_native_scanners,'glyph_shapes'):_native_scanners.glyph_shapes={}
        self.glyph_shapes=_native_scanners.glyph_shapes.setdefault(self.font_path,OrderedDict())
        self.last_key = None
        self.last_native_key = None
        self.last_matches = []
        self.last_mask = None
        self.overlay_key = None
        self.overlay = None
        self.overlay_patches = []
        self.layout_key = None
        self.layout_patches = []
        self.battle_scan=False;self.active_rows=None

    def set_battle_scan(self,value):
        value=bool(value)
        if value==self.battle_scan:return
        self.battle_scan=value;self.active_rows=np.r_[0:16,120:192] if value else None
        self.scan_mask=np.zeros((192,256),dtype=bool) if value else None
        if value:self.scan_mask[:16]=True;self.scan_mask[120:]=True;self.scan_mask[136:184,:56]=False
        self.last_native_key=None;self.last_key=None;self.overlay_key=None
        self.primary_mode=False;self.primary_key=None

    def _scan_active(self,mask,height,width,keys,characters,minimum=1,maximum=144):
        if not self.battle_scan:return self._scan(mask,height,width,keys,characters,minimum,maximum)
        result=[]
        for top,bottom in ((0,16),(120,192)):
            for x,y,char,w,h,pattern in self._scan(mask[top:bottom],height,width,keys,characters,minimum,maximum):result.append((x,y+top,char,w,h,pattern))
        return result

    @staticmethod
    def _add(glyphs, data, char, width=12):
        pixels = np.unpackbits(np.frombuffer(data, dtype='uint8')).reshape(12, 16)
        if pixels[:, width:].any() or pixels.sum() == 0:
            return
        key = np.packbits(pixels[:, :width]).tobytes()
        if key in glyphs and glyphs[key] != char:
            glyphs[key] = None  # Never guess between identical bitmap glyphs.
        else:
            glyphs[key] = char

    @staticmethod
    def _scan(mask, height, width, keys, characters, minimum=1, maximum=144):
        scanner=getattr(_native_scanners,'instance',None)
        if scanner is None:
            try:
                from native_font_scan import NativeFontScanner
                scanner=NativeFontScanner()
            except (OSError,ImportError):scanner=False
            _native_scanners.instance=scanner
        if scanner is not False:
            try:return scanner.scan(mask,height,width,keys,characters,minimum,maximum)
            except (OSError,RuntimeError,MemoryError):
                scanner.close();_native_scanners.instance=False
        return FontRenderer._scan_numpy(mask,height,width,keys,characters,minimum,maximum)

    @staticmethod
    def _scan_numpy(mask, height, width, keys, characters, minimum=1, maximum=144):
        windows = np.lib.stride_tricks.sliding_window_view(mask, (height, width))
        integral = np.pad(mask, ((1, 0), (1, 0))).astype('int32').cumsum(0).cumsum(1)
        count = (integral[height:, width:] - integral[:-height, width:]
                 - integral[height:, :-width] + integral[:-height, :-width])
        ys, xs = np.where((count >= minimum) & (count <= maximum))
        packed = np.packbits(windows[ys, xs].reshape(-1, height*width), axis=1)
        values = packed.view(keys.dtype).reshape(-1)
        indices = np.searchsorted(keys, values)
        valid = indices < len(keys)
        valid[valid] &= keys[indices[valid]] == values[valid]
        return [(int(x), int(y), characters[i], width, height,
                 windows[y, x].copy())
                for x, y, i in zip(xs[valid], ys[valid], indices[valid])]

    def recognize(self, native):
        native = np.asarray(native)[:192]
        checked=native if self.active_rows is None else native[self.scan_mask]
        native_key = hashlib.blake2b(checked.tobytes(), digest_size=16).digest()
        if native_key == self.last_native_key:
            return self.last_matches
        pixel_scanner=getattr(_native_scanners,'pixels',None)
        if pixel_scanner is None:
            try:
                from native_font_pixels import NativeFontPixels
                pixel_scanner=NativeFontPixels()
            except (OSError,ImportError):pixel_scanner=False
            _native_scanners.pixels=pixel_scanner
        if pixel_scanner is not False:
            bright,white,selected_green,hud_ink,hud_gold=pixel_scanner.masks(native)
        else:
            red, green, blue = native[:,:,0], native[:,:,1], native[:,:,2]
            low = np.minimum(np.minimum(red, green), blue)
            high = np.maximum(np.maximum(red, green), blue)
            neutral = high.astype('int16') - low < 8
            bright = (low >= 80) & neutral
            white = (low >= 232) & neutral
            selected_green=(red<48)&(green>=48)&(blue<48)
            hud_ink=((green[:32]>=232)&(blue[:32]>=232)&(red[:32]>=80))|((red[:32]>=128)&(green[:32]<64)&(blue[:32]<64))|((red[:32]>=128)&(green[:32]>=128)&(blue[:32]<64))
            hud_gold=(red[:32]>=180)&(green[:32]>=64)&(blue[:32]<64)
        if self.battle_scan:bright&=self.scan_mask;white&=self.scan_mask
        # A translucent button exposes animated gray pixels behind its text.
        # Thresholding all bright grays merges those pixels into the glyph and
        # makes exact recognition alternate between HD and native lettering.
        # Test the actual solid DS foreground colors first, independently.
        red5=native[:,:,0]>>3;green5=native[:,:,1]>>3;blue5=native[:,:,2]>>3
        neutral5=(red5==green5)&(green5==blue5)
        foregrounds=[neutral5&(red5==31),neutral5&(red5==20),(red5==31)&(green5==0)&(blue5==0)]
        if self.battle_scan:
            for foreground in foregrounds:foreground&=self.scan_mask
        strong_green=(red5<6)&(green5>=24)&(blue5<6)
        primary_signal=hashlib.blake2b(b''.join(m.tobytes() for m in foregrounds)+hud_ink.tobytes()+hud_gold.tobytes(),digest_size=16).digest()
        primary_key=(primary_signal,tuple(self._selected_run(selected_green,*run[:3]) for run in getattr(self,'menu_runs',())))
        if getattr(self,'primary_mode',False) and primary_key==getattr(self,'primary_key',None):
            self.last_native_key=native_key;return self.last_matches
        key = hashlib.blake2b(bright.tobytes()+white.tobytes()+selected_green.tobytes()+hud_ink.tobytes()+hud_gold.tobytes()+b''.join(m.tobytes() for m in foregrounds), digest_size=16).digest()
        self.last_native_key = native_key
        if key == self.last_key and not getattr(self,'primary_mode',False):
            return self.last_matches
        masks=[]
        for candidate_mask in foregrounds:
            if candidate_mask.any() and not any(np.array_equal(candidate_mask,previous) for previous in masks):masks.append(candidate_mask)
        full = []
        narrow = []
        for mask in masks:
            full.extend(self._scan_active(mask, 12, 12, self.keys, self.characters, 5, 100))
            narrow.extend(self._scan_active(mask, 12, 8, self.narrow_keys, self.narrow_characters, 1, 80))
        self.primary_mode=any(row[2].isalnum() for row in full+narrow) or bool(hud_ink.any() and hud_gold.any())
        if not self.primary_mode:
            for mask in (bright,white):
                if not mask.any() or any(np.array_equal(mask,previous) for previous in masks):continue
                masks.append(mask);full.extend(self._scan_active(mask,12,12,self.keys,self.characters,5,100));narrow.extend(self._scan_active(mask,12,8,self.narrow_keys,self.narrow_characters,1,80))
        text_rows = {y for x, y, ch, w, h, ink in full}
        positions = {(x, y) for x, y, ch, w, h, ink in narrow}
        hud_labels=self._scan(hud_gold,16,16,self.hud_label_keys,self.hud_label_characters,5,200)
        hud=[];hud_erasers=[]
        hp=next((row for row in hud_labels if row[2]=='HP'),None)
        en=next((row for row in hud_labels if row[2]=='EN'),None)
        if hp and en and en[0]-hp[0]==128 and hp[1]==en[1]:
            y=hp[1];xs=list(range(hp[0]+16,hp[0]+120,8))+list(range(en[0]+16,min(249,en[0]+80),8))
            cells=np.stack([hud_ink[y:y+16,x:x+8] for x in xs]);taken=set()
            for char,ink,opaque in self.hud_patterns:
                for index in np.flatnonzero(np.all(cells[:,opaque]==ink[opaque],axis=1)):
                    if int(index) not in taken:
                        hud.append((xs[int(index)],y,char,8,16,ink));hud_erasers.append((xs[int(index)],y,opaque));taken.add(int(index))
            hud+=hud_labels
            for x,yy,ch,w,h,ink in hud_labels:
                padded=np.pad(ink,2);erase=np.logical_or.reduce([padded[dy:dy+h,dx:dx+w] for dy in range(5) for dx in range(5)])
                hud_erasers.append((x,yy,erase))
        candidates = hud+full + [row for row in narrow if row[1] in text_rows or
                             any((row[0]+dx, row[1]) in positions for dx in (-16, -8, 8, 16))]
        compact=[]
        # The compact HUD has a white face AND a gray bevel (indices 15/14).
        # Separate exact-color menu masks split every digit in half. Scan the
        # complete bevel only for the compact font, including warning colors.
        compact_masks=masks+[bright,(red5>=10)&(green5<2)&(blue5<2),
                             (red5>=10)&(green5>=10)&(blue5<2)]
        for mask in compact_masks:
            if mask.any():compact.extend(self._scan_active(mask,8,8,self.compact_keys,self.compact_characters,5,60))
        positions = {(x, y) for x, y, ch, w, h, ink in compact}
        candidates.extend(row for row in compact if row[1] in text_rows or
                          any((row[0]+dx, row[1]) in positions for dx in (-16, -8, 8, 16)))
        if not self.battle_scan and sum(y<24 for x,y,ch,*_ in compact)>=8 and self.forecast_patterns:
            # Large percentages are assembled from flipped 16x8 pieces. They
            # are a different ROM font from both the compact HP and battle HUD.
            cyan=(native[:,:,1]>=180)&(native[:,:,2]>=180)
            for left,right in ((0,72),(184,256)):
                windows=np.lib.stride_tricks.sliding_window_view(cyan[76:100,left:right],(16,16))
                for char,ink,opaque in self.forecast_patterns:
                    ys,xs=np.where(np.all(windows[:,:,opaque]==ink[opaque],axis=2))
                    for yy,xx in zip(ys,xs):
                        x,y=left+int(xx),76+int(yy)
                        candidates.insert(0,(x,y,char,16,16,ink));hud_erasers.append((x,y,opaque))
        anchors={(x,y) for x,y,ch,*_ in candidates if ch.isalnum()}
        candidates=[row for row in candidates if row[2] not in ('_','―','━','─','—') or any((row[0]+dx,row[1]) in anchors for dx in (-16,-12,-8,8,12,16))]
        occupied = np.zeros(bright.shape, dtype=bool)
        accepted = []
        sizes, heights = {}, {}
        mask = np.zeros(bright.shape, dtype=bool)
        for x, y, char, width, height, ink in candidates:
            if occupied[y:y+height, x:x+width].any():
                continue
            occupied[y:y+height, x:x+width] = True
            # Only the matched bitmap is ink. Neutral button gradients are
            # background, even when they share the dim text brightness range.
            mask[y:y+height, x:x+width] |= ink
            accepted.append((x, y, char))
            sizes[x, y], heights[x, y] = width, height
        self.last_sizes, self.last_heights = sizes, heights
        self.last_ink = mask.copy()
        padded = np.pad(mask, 2)
        mask = np.logical_or.reduce([padded[dy:dy+192, dx:dx+256]
                                     for dy in range(5) for dx in range(5)])
        self.hud_mask=np.zeros((192,256),dtype=bool);self.hud_positions={(x,y) for x,y,*_ in hud}
        for x,y,erase in hud_erasers:self.hud_mask[y:y+erase.shape[0],x:x+erase.shape[1]]|=erase
        mask|=self.hud_mask
        self.menu_glyphs=set();self.menu_runs=[];lines={}
        for x,y,char in accepted:
            if heights[x,y]==12:lines.setdefault(y,[]).append((x,sizes[x,y]))
        for y,cells in lines.items():
            runs=[]
            for x,w in sorted(cells):
                if runs and x<=runs[-1][1]+8:runs[-1][1]=max(runs[-1][1],x+w);runs[-1][2].append(x)
                else:runs.append([x,x+w,[x]])
            for left,right,xs in runs:
                self.menu_runs.append((left,right,y,xs))
                if not self._selected_run(selected_green,left,right,y):continue
                # A selected button has a solid green center. Repair its whole
                # text strip so no old bitmap/outline survives between strokes.
                mask[max(0,y-2):min(192,y+14),max(0,left-2):min(256,right+2)]=True
                self.menu_glyphs.update((x,y) for x in xs)
        self.menu_repairs=[]
        # Treat a selected button as one background, including words separated
        # by spaces. Sampling at each glyph edge can sample its black shadow.
        for y,cells in lines.items():
            selected=[x+sizes[x,y]/2 for x,_ in cells if (x,y) in self.menu_glyphs]
            if not selected:continue
            spans=[span for left,right,yy,xs in self.menu_runs if yy==y and any((x,y) in self.menu_glyphs for x in xs)
                   if (span:=self._selected_span(selected_green,left,right,y)) is not None]
            for green_row in strong_green[y+8:min(192,y+16)]:
                changes=np.flatnonzero(np.diff(np.pad(green_row.astype('int8'),1)))
                spans.extend((int(l),int(r)) for l,r in zip(changes[::2],changes[1::2]) if r-l>=12 and any(l<=cx<r for cx in selected))
            if not spans:continue
            button_left,button_right=max(spans,key=lambda span:span[1]-span[0])
            members=[(x,w) for x,w in cells if button_left<=x+w/2<button_right]
            if not members:continue
            for x,w in members:self.menu_glyphs.add((x,y))
            left=max(0,min(x for x,w in members)-2);right=min(256,max(x+w for x,w in members)+2)
            mask[max(0,y-2):min(192,y+14),left:right]=True
            self.menu_repairs.append((left,max(0,y-2),right,min(192,y+14),button_left,button_right))
        self.last_key, self.last_matches, self.last_mask = key, accepted, mask
        self.primary_key=(primary_signal,tuple(self._selected_run(selected_green,*run[:3]) for run in self.menu_runs))
        return accepted

    @staticmethod
    def _selected_run(green,left,right,y):
        if y+12>192:return False
        strip=green[y+8:min(192,y+16),max(0,left-2):min(256,right+2)]
        return bool(strip.size and np.any(strip.mean(1)>=.8)) or FontRenderer._selected_span(green,left,right,y) is not None

    @staticmethod
    def _selected_span(green,left,right,y):
        # The game's opaque bitmap bed may hide every green pixel beneath a
        # word. Find the button beside the word, bridging only its text cell;
        # selection must not depend on seeing a bright row through the letters.
        l=max(0,left-4);r=min(256,right+4);spans=[]
        for row in green[max(0,y-2):min(192,y+14)]:
            blocked_left=np.flatnonzero(~row[:l]);blocked_right=np.flatnonzero(~row[r:])
            a=int(blocked_left[-1])+1 if len(blocked_left) else 0
            b=r+int(blocked_right[0]) if len(blocked_right) else 256
            if b-a>=24 and np.count_nonzero(row[a:b])>=8:spans.append((a,b))
        if len(spans)<3:return None
        a,b=np.median(spans,axis=0).astype('int32')
        return int(a),int(b)

    def _glyph(self, char, width, height, color, compact=False, button=False):
        key = char, width, height, color, compact,button
        if key not in self.glyph_images:
            shape_key=char,width,height,compact,button
            shape=self.glyph_shapes.pop(shape_key,None)
            if shape is None:
                shape=self._glyph_shape(char,width,height,compact,button)
            self.glyph_shapes[shape_key]=shape
            while len(self.glyph_shapes)>8192:self.glyph_shapes.popitem(last=False)
            render_width,stroke,outline,fill=shape
            image=Image.new('RGBA',(render_width,height));draw=ImageDraw.Draw(image)
            if outline is not None:draw.bitmap(outline[0],outline[1],fill=(8,16,20))
            if not stroke or tuple(color)!=(8,16,20,255):draw.bitmap(fill[0],fill[1],fill=color)
            if render_width!=width:image=image.resize((width,height),Image.Resampling.LANCZOS)
            self.glyph_images[key]=image
            while len(self.glyph_images)>8192:self.glyph_images.popitem(last=False)
        else:self.glyph_images.move_to_end(key)
        return self.glyph_images[key]

    def _glyph_shape(self,char,width,height,compact,button):
        """Cache FreeType coverage independently of the changing native color."""
        size = max(6, round(height * (.72 if compact else .80 if button else .94)))
        if size not in self.fonts:self.fonts[size] = ImageFont.truetype(self.font_path, size)
        font = self.fonts[size];stroke = 0 if button else max(1, height//45)
        box = font.getbbox(char);render_width = max(width, box[2]-box[0]+2*stroke+2)
        x = (render_width - (box[2]-box[0])) // 2 - box[0]
        y = (height - (box[3]-box[1])) // 2 - box[1]
        def mask(amount):
            coverage,offset=font.getmask2(char,'L',stroke_width=amount,stroke_filled=True)
            bitmap=Image.frombytes('L',coverage.size,bytes(coverage))
            return (x+offset[0],y+offset[1]),bitmap
        return render_width,stroke,mask(stroke) if stroke else None,mask(0)

    def prewarm_ui(self):
        """Prepare common UI characters before emulation starts, at all supported sizes."""
        import math
        from render_resolution import MIN_WIDTH,MAX_WIDTH
        words='이동공격변형정신능력레벨기력원공원방요청상태지형방어회피전투행동원군데모사격격투명중기술우주공간파일럿기체무기성장개조자금경험치카즈마발호크지원소비불굴집중응원표시전환항목추가확인취소저장불러오기특수리스트'
        ascii_chars='0123456789HPENPARTSLRSELON/?:+-%±·.,!「」'
        white=(255,255,255,255)
        for screen in range(MIN_WIDTH,MAX_WIDTH+1,32):
            scale=screen/256
            sizes={math.floor(12*scale),math.ceil(12*scale)}
            for w in sizes:
                for h in sizes:
                    for char in set(words+ascii_chars):
                        self._glyph(char,w,h,white);self._glyph(char,w,h,white,button=True)
            for native_h in (8,12,16):
                for w in {math.floor(8*scale),math.ceil(8*scale)}:
                    for h in {math.floor(native_h*scale),math.ceil(native_h*scale)}:
                        for char in set(ascii_chars):self._glyph(char,w,h,white,compact=native_h in (8,16))

    def _heal_plan(self):
        signature=self.last_mask.tobytes()
        if getattr(self,'heal_mask_key',None)!=signature:
            keep=~self.last_mask;columns=np.arange(keep.shape[1])[None,:]
            left=np.maximum.accumulate(np.where(keep,columns,-1),axis=1)
            right=np.minimum.accumulate(np.where(keep,columns,keep.shape[1])[:,::-1],axis=1)[:,::-1]
            first=keep.argmax(1)[:,None];last=keep.shape[1]-1-keep[:,::-1].argmax(1)[:,None]
            left=np.where(left<0,first,left);right=np.where(right>=keep.shape[1],last,right)
            rows,xs=np.where(self.last_mask&keep.any(1)[:,None]);left=left[rows,xs];right=right[rows,xs]
            weights=np.divide(xs-left,right-left,out=np.zeros(len(xs),dtype='float64'),where=right!=left)
            self.heal_plan=(rows,xs,left,right,weights[:,None])
            self.heal_mask_key=signature
        return self.heal_plan

    def _underlay_key(self,native):
        rows,xs,left,right,weights=self._heal_plan()
        selected=b''.join(native[top:bottom,sample_left:sample_right].tobytes() for left,top,right,bottom,sample_left,sample_right in getattr(self,'menu_repairs',()))
        return hashlib.blake2b(native[rows,left].tobytes()+native[rows,right].tobytes()+native[self.last_mask.all(1)].tobytes()+selected,digest_size=16).digest()

    def _heal_native(self, native):
        native=np.asarray(native)[:192]
        healed=native.copy();rows,xs,left,right,weights=self._heal_plan()
        a=native[rows,left].astype('float64');b=native[rows,right].astype('float64')
        healed[rows,xs]=(a+(b-a)*weights).astype('uint8')
        for left,top,right,bottom,sample_left,sample_right in getattr(self,'menu_repairs',()):
            samples=native[top:bottom,sample_left:sample_right].astype('int16')
            green=(samples[:,:,1]>samples[:,:,0]+16)&(samples[:,:,1]>samples[:,:,2]+16)
            for yy in range(bottom-top):
                if np.count_nonzero(green[yy])<4:continue
                color=np.median(samples[yy][green[yy]],axis=0).astype('uint8')
                erase=self.last_mask[top+yy,left:right]
                healed[top+yy,left:right][erase]=color
        return healed

    def clean_native(self,native):
        """Erase glyphs at native resolution before an HD scene is composited."""
        native=np.asarray(native)[:192]
        if not self.recognize(native):return native
        key=(self.last_mask.tobytes(),self._underlay_key(native))
        if getattr(self,'erased_native_key',None)!=key:
            self.erased_native_pixels=self._heal_native(native)[self.last_mask]
            self.erased_native_key=key
        result=native.copy();result[self.last_mask]=self.erased_native_pixels
        return result

    def compose(self, target, native, background=None, only_text=False):
        native = np.asarray(native)[:192]
        matches = self.recognize(native)
        if not matches:
            return
        mask=self.last_mask
        sx,sy=target.width/256,target.height/192
        geometry=tuple((x,y,char,self.last_sizes[x,y],self.last_heights[x,y]) for x,y,char in matches)
        layout_key=(geometry,target.size,hashlib.blake2b(native[self.last_ink].tobytes(),digest_size=8).digest(),tuple(sorted(self.menu_glyphs)))
        if not only_text:
            background_key=None if background is None else hashlib.blake2b(background.tobytes(),digest_size=16).digest()
            overlay_key=(layout_key,self._underlay_key(native),background_key,bool(getattr(target,'hud_clean',False)),hasattr(target,'draw'))
            if overlay_key==self.overlay_key:
                self._paint_overlay(target)
                return
        if self.layout_key != layout_key:
            positions=tuple((x,y,self.last_sizes[x,y],self.last_heights[x,y]) for x,y,char in matches)
            if getattr(self,'field_positions',None)!=positions:
                rectangles=[]
                for x,y,w,h in positions:
                    rect=[max(0,x-2),max(0,y-2),min(256,x+w+2),min(192,y+h+2)]
                    again=True
                    while again:
                        again=False
                        for previous in rectangles[:]:
                            if rect[0]<previous[2] and previous[0]<rect[2] and rect[1]<previous[3] and previous[1]<rect[3]:
                                rectangles.remove(previous);rect=[min(rect[0],previous[0]),min(rect[1],previous[1]),max(rect[2],previous[2]),max(rect[3],previous[3])];again=True
                    rectangles.append(rect)
                self.field_groups=[(tuple(rect),[i for i,(x,y,w,h) in enumerate(positions) if rect[0]<=x and rect[1]<=y and x+w<=rect[2] and y+h<=rect[3]]) for rect in rectangles]
                self.field_positions=positions
            if not hasattr(self,'field_cache'):self.field_cache=OrderedDict();self.foreground_colors=OrderedDict()
            self.layout_patches=[];self.hud_rectangles=set()
            for rectangle,indices in self.field_groups:
                left,top,right,bottom=rectangle;box=round(left*sx),round(top*sy),round(right*sx),round(bottom*sy)
                glyphs=[]
                for i in indices:
                    x,y,char=matches[i];w,h=self.last_sizes[x,y],self.last_heights[x,y]
                    ink=native[y:y+h,x:x+w][self.last_ink[y:y+h,x:x+w]].tobytes()
                    color=self.foreground_colors.get(ink)
                    if color is None:
                        color=tuple(int(v) for v in np.median(np.frombuffer(ink,dtype='uint8').reshape(-1,3),axis=0))+(255,)
                        self.foreground_colors[ink]=color
                        while len(self.foreground_colors)>256:self.foreground_colors.popitem(last=False)
                    glyphs.append((x,y,char,w,h,color,(x,y) in self.menu_glyphs))
                key=(rectangle,target.size,tuple(glyphs),mask[top:bottom,left:right].tobytes())
                patch=self.field_cache.pop(key,None)
                if patch is None:
                    text=Image.new('RGBA',(box[2]-box[0],box[3]-box[1]))
                    for x,y,char,w,h,color,button in glyphs:
                        xx,yy=round(x*sx),round(y*sy);width,height=round((x+w)*sx)-xx,round((y+h)*sy)-yy
                        text.alpha_composite(self._glyph(char,width,height,color,compact=h in (8,16),button=button),(xx-box[0],yy-box[1]))
                    alpha=Image.fromarray(mask[top:bottom,left:right].astype('uint8')*255).resize(text.size,Image.Resampling.NEAREST)
                    patch=(rectangle,box[:2],alpha,text)
                self.field_cache[key]=patch;self.layout_patches.append(patch)
                if all((matches[i][0],matches[i][1]) in self.hud_positions for i in indices):self.hud_rectangles.add(rectangle)
                while len(self.field_cache)>128:self.field_cache.popitem(last=False)
            self.layout_key = layout_key
        if only_text:
            for rectangle,position,alpha,text in self.layout_patches:target.paste(text,position,text)
            return
        healed=self._heal_native(native) if background is None else None
        self.overlay_patches = []
        for (left, top, right, bottom), position, alpha, text in self.layout_patches:
            if getattr(target,'hud_clean',False) and (left,top,right,bottom) in self.hud_rectangles:
                self.overlay_patches.append((position,text));continue
            if background is None and hasattr(target,'draw'):
                # Upload native-sized background repair and cached HD lettering
                # separately. Avoid expanding/compositing a new RGBA patch on
                # the CPU whenever a number, selection or backdrop changes.
                base=Image.fromarray(healed[top:bottom,left:right])
                self.overlay_patches.append((position,base,alpha,text));continue
            if background is None:
                patch = Image.fromarray(healed[top:bottom, left:right]).convert('RGBA').resize(
                    text.size, Image.Resampling.NEAREST)
            else:
                patch = background.crop((position[0], position[1], position[0]+text.width, position[1]+text.height)).convert('RGBA')
            patch.putalpha(alpha)
            patch.alpha_composite(text)
            self.overlay_patches.append((position, patch))
        self.overlay_key = overlay_key
        self._paint_overlay(target)

    def _paint_overlay(self,target):
        for entry in self.overlay_patches:
            if len(entry)==2:
                position,patch=entry;target.paste(patch,position,patch)
            else:
                position,base,alpha,text=entry;x,y=position
                target.draw(base,(x,y,x+alpha.width,y+alpha.height),mask=alpha,nearest=True)
                target.paste(text,position,text)
