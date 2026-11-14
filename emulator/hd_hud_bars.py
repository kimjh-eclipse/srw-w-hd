"""HD redraw of the small battle HUD in the sub screen: the yellow "HP" label
and the slanted HP gauge under it (IMG4651/PLT4650, a BG layer, not OBJ).

The label is found by its exact native bitmap; the gauge sits directly under
it. Every frame the gauge is measured from the native pixels (row by row: the
slanted left/right edges, where the fill colour gives way to the track
colour, and each row's colours), so damage animation and any fill length are
followed. The HD picture draws the same slant as a straight edge and blends
the row colours vertically. The covered native area is first painted with the
panel's own row colour so no native step shows around the HD shapes.
"""
import os
import numpy as np
from PIL import Image,ImageDraw,ImageFont

HUD_BARS=os.environ.get('SRWW_HUD_BARS','1')!='0'
YELLOW=(255,255,0);ORANGE=(255,174,0)
# Yellow (Y) / orange (O) cells of the 14x6 native label, black outline left out.
LABEL=('YOK.YOKYYYYYOK',
       'YOK.YOKYOKKYOK',
       'YYYYYOKYYYYYOK',
       'YOKKYOKYOKKKKK',
       'YOK.YOKYOK....',
       'KKK.KKKKKK....')
LABEL_W,LABEL_H=14,6
BAR_W,BAR_H=72,5


def _label_mask():
    m=np.array([[c=='Y' for c in row] for row in LABEL]);o=np.array([[c=='O' for c in row] for row in LABEL]);return m,o


def _label_black():
    return np.array([[c=='K' for c in row] for row in LABEL])


class HudBars:
    def __init__(self):
        self.yellow,self.orange=_label_mask();self.black=_label_black();self.cache={}

    def find_labels(self,native):
        r,g,b=native[:,:,0],native[:,:,1],native[:,:,2]
        yellow=(r==255)&(g==255)&(b==0);orange=(r==255)&(g==174)&(b==0);black=(r|g|b)==0
        if yellow.sum()<self.yellow.sum():return []
        found=[]
        # Candidate corners: a yellow pixel whose 14x6 window has the label's exact
        # yellow, orange and black-outline cells (the panel cells are not checked).
        ys,xs=np.nonzero(yellow[:-LABEL_H+1,:-LABEL_W+1])
        for y,x in zip(ys,xs):
            win=(slice(y,y+LABEL_H),slice(x,x+LABEL_W))
            if np.array_equal(yellow[win],self.yellow) and np.array_equal(orange[win],self.orange) and np.all(black[win][self.black]):
                found.append((int(x),int(y)))
        return found

    @staticmethod
    def panel_colour(native,y,x):
        return tuple(int(v) for v in native[y,max(0,x-1)])

    def measure_bar(self,native,x,y):
        """Rows of the gauge under a label at (x,y): left, right, split, fill and track colours."""
        rows=[];start=x-1
        family=lambda c:'red' if c[0]>c[1]+40 else 'green' if c[1]>c[0]+40 else 'light'
        for r in range(BAR_H):
            yy=y+LABEL_H+r
            if yy>=native.shape[0]:return None
            line=native[yy,start:start+BAR_W+4].astype(int)
            # Gauge colours all carry red; the teal panel and its cyan rim have none.
            bar=np.flatnonzero(line[:,0]>0)
            panel=[tuple(c) for c in line if c[0]==0 and c[1]>0]
            if not len(bar) or not panel:return None
            bg=max(set(panel),key=panel.count)
            left,right=int(bar[0]),int(bar[-1])
            colours=[tuple(int(v) for v in c) for c in line[left:right+1]]
            rows.append(dict(left=start+left,right=start+right+1,bg=bg,y=yy,colours=colours))
        # The fill/track boundary is one column for all rows; rows holding both a
        # green and a red pixel give it (light highlight rows cannot).
        splits=[]
        for row in rows:
            fam=[family(c) for c in row['colours']]
            if 'green' in fam and 'red' in fam:splits.append(row['left']+max(i for i,f in enumerate(fam) if f=='green')+1)
        any_green=any(family(c)=='green' for row in rows for c in row['colours'])
        for row in rows:
            split=int(np.median(splits)) if splits else (row['right'] if any_green else row['left'])
            left_part=row['colours'][1:max(1,split-row['left'])] or row['colours']
            right_part=row['colours'][max(0,split-row['left']):] or left_part
            row['split']=min(max(split,row['left']),row['right'])
            row['fill']=max(set(left_part),key=left_part.count);row['track']=max(set(right_part),key=right_part.count)
            if not splits and not any_green:row['fill']=row['track']
        return rows

    def bar_image(self,rows,scale):
        left=min(r['left'] for r in rows);right=max(r['right'] for r in rows);top=rows[0]['y']
        w,h=(right-left)*scale,BAR_H*scale
        out=np.zeros((h,w,4),dtype='float32')
        # Panel colour first so the native steps are covered.
        for i,r in enumerate(rows):out[i*scale:(i+1)*scale,:,:3]=r['bg'];out[i*scale:(i+1)*scale,:,3]=255
        xs=(np.arange(w)+.5)/scale+left
        for hy in range(h):
            t=min(max((hy+.5)/scale-.5,0),BAR_H-1);i0=int(np.floor(t));i1=min(i0+1,BAR_H-1);f=t-i0
            lerp=lambda key:rows[i0][key]*(1-f)+rows[i1][key]*f
            mix=lambda key:np.array(rows[i0][key],dtype='float32')*(1-f)+np.array(rows[i1][key],dtype='float32')*f
            l,rr,s=lerp('left'),lerp('right'),lerp('split')
            # Coverage of each HD pixel between the slanted edges (1 HD px soft edge).
            cover=np.clip((xs-l)*scale+.5,0,1)*np.clip((rr-xs)*scale+.5,0,1)
            fill_part=np.clip((s-xs)*scale+.5,0,1)
            colour=mix('fill')[None,:]*fill_part[:,None]+mix('track')[None,:]*(1-fill_part[:,None])
            out[hy,:,:3]=out[hy,:,:3]*(1-cover[:,None])+colour*cover[:,None]
        return Image.fromarray(out.clip(0,255).astype('uint8'),'RGBA'),(left,top)

    def label_image(self,native,x,y,scale):
        key=('label',scale,tuple(self.panel_colour(native,y+r,x) for r in range(LABEL_H)))
        if key in self.cache:return self.cache[key]
        w,h=LABEL_W*scale,LABEL_H*scale;image=Image.new('RGBA',(w,h))
        draw=ImageDraw.Draw(image)
        for r in range(LABEL_H):draw.rectangle((0,r*scale,w,(r+1)*scale-1),fill=key[2][r]+(255,))
        # The native letters fill a 12x5 block (orange edge in the 13th column):
        # draw the word large, crop to its ink and fit it to that block.
        font=ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf',96);box=font.getbbox('HP')
        glyph=Image.new('L',(box[2]-box[0]+4,box[3]-box[1]+4));ImageDraw.Draw(glyph).text((2-box[0],2-box[1]),'HP',font=font,fill=255)
        glyph=glyph.crop(glyph.getbbox()).resize((12*scale,5*scale),Image.Resampling.LANCZOS)
        edge=max(1,scale//2)
        layer=lambda colour,dx,dy:Image.composite(Image.new('RGBA',(w,h),colour+(255,)),Image.new('RGBA',(w,h)),self._place(glyph,w,h,dx,dy))
        image=Image.alpha_composite(image,layer((0,0,0),scale,scale))       # black outline, lower right
        image=Image.alpha_composite(image,layer(ORANGE,edge,0))            # orange right edge
        image=Image.alpha_composite(image,layer(YELLOW,0,0))
        self.cache[key]=image
        while len(self.cache)>64:self.cache.pop(next(iter(self.cache)))
        return image

    def compose(self,target,native):
        if not HUD_BARS:return 0
        native=np.asarray(native)[:192]
        labels=self.find_labels(native)
        if not labels:return 0
        scale=round(target.size[0]/256)
        for x,y in labels:
            label=self.label_image(native,x,y,scale)
            self._put(target,label,(x*scale,y*scale))
            rows=self.measure_bar(native,x,y)
            if rows:
                bar,(left,top)=self.bar_image(rows,scale)
                self._put(target,bar,(left*scale,top*scale))
        return len(labels)

    @staticmethod
    def _place(glyph,w,h,dx,dy):
        mask=Image.new('L',(w,h));mask.paste(glyph,(dx,dy));return mask

    @staticmethod
    def _put(target,image,position):
        if hasattr(target,'draw'):target.draw(image,(position[0],position[1],position[0]+image.width,position[1]+image.height),alpha=True)
        else:target.paste(image,position,image)
