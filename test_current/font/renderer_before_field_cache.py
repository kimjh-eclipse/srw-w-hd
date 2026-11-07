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

ROOT = Path(__file__).resolve().parent.parent
_native_scanners=threading.local()


class FontRenderer:
    def __init__(self):
        rom = (ROOT / 'baseline/SRWW_Korean_1.0.8.nds').read_bytes()
        glyphs = {}
        narrow = {}
        original = (ROOT / 'inputs/SRWW_Japan.nds').read_bytes()
        # The Japanese table has a two-byte Shift-JIS key and twelve bitmap rows.
        for off in range(0x445fc, 0x4d530, 26):
            try:
                ch = original[off:off+2].decode('cp932')
            except UnicodeError:
                continue
            normalized = unicodedata.normalize('NFKC', ch)
            ch = normalized if len(normalized) == 1 else ch
            if ch == '・':
                ch = '·'
            if len(ch) == 1 and (ch.isascii() or unicodedata.category(ch)[0] in 'PS'):
                data = rom[off+2:off+26]
                pixels = np.unpackbits(np.frombuffer(data, dtype='uint8')).reshape(12, 16)
                if not pixels[:, 8:].any():
                    self._add(narrow, data, ch, 8)
                else:
                    self._add(glyphs, data, ch)
        chars = [bytes((a, b)).decode('cp949')
                 for a in range(0xb0, 0xc9) for b in range(0xa1, 0xff)]
        for i, ch in enumerate(chars):
            off = 0x4d530 + i * 26
            self._add(glyphs, rom[off+2:off+26], ch)
        glyphs = {k: v for k, v in glyphs.items() if v is not None}
        self.keys = np.array(sorted(glyphs), dtype='V18')
        self.characters = [glyphs[k.tobytes()] for k in self.keys]
        narrow = {k: v for k, v in narrow.items() if v is not None}
        self.narrow_keys = np.array(sorted(narrow), dtype='V12')
        self.narrow_characters = [narrow[k.tobytes()] for k in self.narrow_keys]
        with np.load(ROOT / 'graphics/fonts/hud_glyphs.npz') as source:
            self.compact_patterns = {np.packbits((a == 14) | (a == 15)).tobytes(): str(ch)
                                     for a, ch in zip(source['indices'], source['characters'])}
        self.compact_keys = np.array(sorted(self.compact_patterns), dtype='V8')
        self.compact_characters = [self.compact_patterns[k.tobytes()] for k in self.compact_keys]
        self.font_path = 'C:/Windows/Fonts/malgun.ttf'
        self.fonts = {}
        self.glyph_images = OrderedDict()
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
        red, green, blue = native[:,:,0], native[:,:,1], native[:,:,2]
        low = np.minimum(np.minimum(red, green), blue)
        high = np.maximum(np.maximum(red, green), blue)
        neutral = high.astype('int16') - low < 32
        bright = (low >= 80) & neutral
        white = (low >= 232) & neutral
        if self.battle_scan:bright&=self.scan_mask;white&=self.scan_mask
        key = hashlib.blake2b(bright.tobytes()+white.tobytes(), digest_size=16).digest()
        self.last_native_key = native_key
        if key == self.last_key:
            return self.last_matches
        masks = (bright,) if np.array_equal(bright, white) else (bright, white)
        full = []
        narrow = []
        for mask in masks:
            full.extend(self._scan_active(mask, 12, 12, self.keys, self.characters, 5, 100))
            narrow.extend(self._scan_active(mask, 12, 8, self.narrow_keys, self.narrow_characters, 1, 80))
        text_rows = {y for x, y, ch, w, h, ink in full}
        positions = {(x, y) for x, y, ch, w, h, ink in narrow}
        candidates = full + [row for row in narrow if row[1] in text_rows or
                             any((row[0]+dx, row[1]) in positions for dx in (-16, -8, 8, 16))]
        compact = self._scan_active(bright, 8, 8, self.compact_keys, self.compact_characters, 5, 60)
        positions = {(x, y) for x, y, ch, w, h, ink in compact}
        candidates.extend(row for row in compact if row[1] in text_rows or
                          any((row[0]+dx, row[1]) in positions for dx in (-16, -8, 8, 16)))
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
        padded = np.pad(mask, 1)
        mask = np.logical_or.reduce([padded[dy:dy+192, dx:dx+256]
                                     for dy in range(3) for dx in range(3)])
        self.last_key, self.last_matches, self.last_mask = key, accepted, mask
        return accepted

    def _glyph(self, char, width, height, color):
        key = char, width, height, color
        if key not in self.glyph_images:
            size = max(8, round(height * .94))
            if size not in self.fonts:
                self.fonts[size] = ImageFont.truetype(self.font_path, size)
            font = self.fonts[size]
            stroke = max(1, height//45)
            box = font.getbbox(char)
            render_width = max(width, box[2]-box[0]+2*stroke+2)
            image = Image.new('RGBA', (render_width, height))
            draw = ImageDraw.Draw(image)
            box = draw.textbbox((0, 0), char, font=font)
            x = (render_width - (box[2]-box[0])) // 2 - box[0]
            y = (height - (box[3]-box[1])) // 2 - box[1]
            draw.text((x, y), char, font=font, fill=color,
                      stroke_width=stroke, stroke_fill=(8, 16, 20))
            if render_width != width:
                image = image.resize((width, height), Image.Resampling.LANCZOS)
            self.glyph_images[key] = image
            while len(self.glyph_images) > 1024:
                self.glyph_images.popitem(last=False)
        else:
            self.glyph_images.move_to_end(key)
        return self.glyph_images[key]

    def _heal_plan(self):
        signature=self.last_mask.tobytes()
        if getattr(self,'heal_mask_key',None)!=signature:
            rows=[];targets=[];lefts=[];rights=[];weights=[]
            for y in np.flatnonzero(self.last_mask.any(1)):
                keep=np.flatnonzero(~self.last_mask[y]);xs=np.flatnonzero(self.last_mask[y])
                if not len(keep):continue
                slots=np.searchsorted(keep,xs);left=keep[np.maximum(slots-1,0)];right=keep[np.minimum(slots,len(keep)-1)]
                rows.extend([y]*len(xs));targets.extend(xs);lefts.extend(left);rights.extend(right)
                weights.extend(np.divide(xs-left,right-left,out=np.zeros(len(xs),dtype='float64'),where=right!=left))
            self.heal_plan=tuple(np.asarray(a,dtype='intp') for a in (rows,targets,lefts,rights))+(np.asarray(weights,dtype='float64')[:,None],)
            self.heal_mask_key=signature
        return self.heal_plan

    def _underlay_key(self,native):
        rows,xs,left,right,weights=self._heal_plan()
        return hashlib.blake2b(native[rows,left].tobytes()+native[rows,right].tobytes()+native[self.last_mask.all(1)].tobytes(),digest_size=16).digest()

    def _heal_native(self, native):
        healed=native.copy();rows,xs,left,right,weights=self._heal_plan()
        a=native[rows,left].astype('float64');b=native[rows,right].astype('float64')
        healed[rows,xs]=(a+(b-a)*weights).astype('uint8')
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
        layout_key=(geometry,target.size,hashlib.blake2b(native[self.last_ink].tobytes(),digest_size=8).digest())
        if not only_text:
            background_key=None if background is None else hashlib.blake2b(background.tobytes(),digest_size=16).digest()
            overlay_key=(layout_key,self._underlay_key(native),background_key)
            if overlay_key==self.overlay_key:
                for position,patch in self.overlay_patches:target.paste(patch,position,patch)
                return
        if self.layout_key != layout_key:
            text = Image.new('RGBA', target.size)
            for x, y, char in matches:
                left, top = round(x*sx), round(y*sy)
                cell_width = self.last_sizes[x, y]
                cell_height = self.last_heights[x, y]
                width, height = round((x+cell_width)*sx)-left, round((y+cell_height)*sy)-top
                cell = native[y:y+cell_height, x:x+cell_width]
                foreground = self.last_ink[y:y+cell_height, x:x+cell_width]
                color = tuple(int(v) for v in np.median(cell[foreground], axis=0)) + (255,)
                text.alpha_composite(self._glyph(char, width, height, color), (left, top))
            rectangles = []
            for x, y, char in matches:
                rect = [max(0, x-1), max(0, y-1), min(256, x+self.last_sizes[x, y]+1), min(192, y+self.last_heights[x, y]+1)]
                again = True
                while again:
                    again = False
                    for previous in rectangles[:]:
                        if (rect[0] < previous[2] and previous[0] < rect[2] and
                                rect[1] < previous[3] and previous[1] < rect[3]):
                            rectangles.remove(previous)
                            rect = [min(rect[0], previous[0]), min(rect[1], previous[1]),
                                    max(rect[2], previous[2]), max(rect[3], previous[3])]
                            again = True
                rectangles.append(rect)
            self.layout_patches = []
            for left, top, right, bottom in rectangles:
                box = round(left*sx), round(top*sy), round(right*sx), round(bottom*sy)
                alpha = Image.fromarray(mask[top:bottom, left:right].astype('uint8')*255).resize(
                    (box[2]-box[0], box[3]-box[1]), Image.Resampling.NEAREST)
                self.layout_patches.append(((left, top, right, bottom), box[:2], alpha, text.crop(box)))
            self.layout_key = layout_key
        if only_text:
            for rectangle,position,alpha,text in self.layout_patches:target.paste(text,position,text)
            return
        healed=self._heal_native(native) if background is None else None
        self.overlay_patches = []
        for (left, top, right, bottom), position, alpha, text in self.layout_patches:
            if background is None:
                patch = Image.fromarray(healed[top:bottom, left:right]).convert('RGBA').resize(
                    text.size, Image.Resampling.NEAREST)
            else:
                patch = background.crop((position[0], position[1], position[0]+text.width, position[1]+text.height)).convert('RGBA')
            patch.putalpha(alpha)
            patch.alpha_composite(text)
            self.overlay_patches.append((position, patch))
        self.overlay_key = overlay_key
        for position, patch in self.overlay_patches:
            target.paste(patch, position, patch)
