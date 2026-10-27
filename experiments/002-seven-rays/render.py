#!/usr/bin/env python3
"""Visual Experiment 002: Bailey's Seven Rays. Pillow + NumPy + FFmpeg."""
from __future__ import annotations
import argparse, json, math, random, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE=Path(__file__).resolve().parent
S=json.loads((HERE/'scene.json').read_text())
W,H=S['resolution']; FPS=S['fps']; DURATION=S['duration_seconds']
TAU=math.tau
IVORY=(232,236,225); PALE=(160,183,203); GOLD=(238,194,115)
COLORS=[(227,173,123),(222,207,138),(131,199,193),(199,168,220),(112,174,216),(221,164,182),(138,184,157)]
XS=[126,252,378,512,646,772,898]; RY=296; SRC=(512,128)
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
TITLE=ImageFont.truetype(FB,45); SUB=ImageFont.truetype(F,18); CAP=ImageFont.truetype(FB,24)
LABEL=ImageFont.truetype(FB,12); MINI=ImageFont.truetype(F,12)

def ease(x):
    x=max(0.,min(1.,x));return x*x*(3-2*x)
def fade(t,a,b): return ease((t-a)/(b-a))
def window(t,a,b,w=.7): return fade(t,a,a+w)*(1-fade(t,b-w,b))
def line(d,a,b,color,alpha=190,width=2):
    d.line((*a,*b),fill=(*color,int(max(0,min(255,alpha)))),width=width)
def dot(d,x,y,r,color,alpha=225):
    d.ellipse((x-r,y-r,x+r,y+r),fill=(*color,int(max(0,min(255,alpha)))))
def text(d,xy,s,font,color,alpha=255):
    d.text(xy,s,font=font,fill=(*color,int(max(0,min(255,alpha)))))
def center(d,s,y,font,color,alpha=255):
    b=d.textbbox((0,0),s,font=font)
    text(d,((W-(b[2]-b[0]))/2,y),s,font,color,alpha)

rng=random.Random(1982)
y,x=np.mgrid[0:H,0:W]
b=np.empty((H,W,3),dtype=np.uint8)
b[:,:,0]=9+(7*y/H).astype(np.uint8)
b[:,:,1]=19+(11*y/H).astype(np.uint8)
b[:,:,2]=36+(17*y/H).astype(np.uint8)
v=np.clip(1-.24*((x-W/2)**2/(W/2)**2+(y-H/2)**2/(H/2)**2),.73,1)
b=np.uint8(b*v[...,None]); BASE=Image.fromarray(b,'RGB').convert('RGBA')
d=ImageDraw.Draw(BASE,'RGBA')
for i in range(128):
    sx=rng.randrange(18,W-18);sy=rng.randrange(20,H-73);sr=rng.choice((1,1,1,2))
    dot(d,sx,sy,sr,(220,231,244),rng.randrange(32,111))
for rx,ry in [(230,105),(350,158),(465,210)]:
    d.arc((SRC[0]-rx,SRC[1]-ry,SRC[0]+rx,SRC[1]+ry),190,348,fill=(117,147,174,23),width=1)
GLOW=Image.new('RGBA',(240,240));gd=ImageDraw.Draw(GLOW,'RGBA')
gd.ellipse((34,34,206,206),fill=(*GOLD,98));GLOW=GLOW.filter(ImageFilter.GaussianBlur(32))

def source(im,visible):
    if visible<=0:return
    glow=GLOW.copy(); glow.putalpha(glow.getchannel('A').point(lambda z:int(z*visible)))
    im.alpha_composite(glow,(SRC[0]-120,SRC[1]-120))
    d=ImageDraw.Draw(im,'RGBA');sx,sy=SRC
    for r,a in [(53,66),(40,110),(26,210)]:
        d.ellipse((sx-r,sy-r,sx+r,sy+r),outline=(*GOLD,int(a*visible)),width=2 if r==26 else 1)
    dot(d,sx,sy,13,GOLD,242*visible)
    center(d,'ONE LIFE',59,LABEL,IVORY,227*visible)

def quadratic(a,b,c,u):
    v=1-u
    return (v*v*a[0]+2*u*v*b[0]+u*u*c[0],v*v*a[1]+2*u*v*b[1]+u*u*c[1])

def spoke(d,i,t,amount):
    col=COLORS[i]; end=(XS[i],RY-23)
    guide=(SRC[0]+(XS[i]-SRC[0])*.52,179)
    intro=fade(t,3+i*.16,5.6+i*.16)
    nodes=83;end_idx=max(1,int((nodes-1)*intro))
    for j in range(end_idx):
        a=quadratic((SRC[0],SRC[1]+30),guide,end,j/(nodes-1))
        z=quadratic((SRC[0],SRC[1]+30),guide,end,(j+1)/(nodes-1))
        alpha=amount*(.78+.22*math.cos(j*.21)**2)
        if i==0:line(d,a,z,col,alpha,3)
        if i==1:
            line(d,(a[0]-2,a[1]),(z[0]-2,z[1]),col,alpha,1)
            line(d,(a[0]+2,a[1]),(z[0]+2,z[1]),col,alpha,1)
        if i==2 and j%10<6:line(d,a,z,col,alpha,2)
        if i==3:line(d,a,z,col,alpha if j%10<5 else alpha*.25,2)
        if i==4 and j%8==0:dot(d,*a,2.0,col,alpha)
        if i==5 and j%12 in (0,1,2,7,8):line(d,a,z,col,alpha,2)
        if i==6 and j%12<7:line(d,a,z,col,alpha,2)
    amount*=intro
    if amount<=0:return
    px,py=XS[i],RY
    d.ellipse((px-19,py-19,px+19,py+19),outline=(*col,int(amount)),width=2)
    d.ellipse((px-10,py-10,px+10,py+10),fill=(*col,int(amount*.13)))
    dot(d,px,py,3,col,amount)
    text(d,(px-5,py-9),str(i+1),LABEL,IVORY,amount)
    names=['WILL','LOVE-WISDOM','INTELLIGENCE','HARMONY','KNOWLEDGE','DEVOTION','ORDER']
    bb=d.textbbox((0,0),names[i],font=MINI)
    text(d,(px-(bb[2]-bb[0])/2,332),names[i],MINI,PALE,amount)

def partition(d,t):
    val=window(t,9.4,16.8,.7)
    if not val:return
    for xa,xb,title,count,col in [(90,414,'RAYS OF ASPECT','THREE',GOLD),(476,938,'RAYS OF ATTRIBUTE','FOUR',PALE)]:
        y=367
        line(d,(xa,y),(xb,y),col,val*150,2)
        line(d,(xa,y),(xa,y-14),col,val*150,2)
        line(d,(xb,y),(xb,y-14),col,val*150,2)
        box=d.textbbox((0,0),title,font=LABEL)
        text(d,((xa+xb-box[2]+box[0])/2,379),title,LABEL,col,val*210)
        box=d.textbbox((0,0),count,font=MINI)
        text(d,((xa+xb-box[2]+box[0])/2,401),count,MINI,PALE,val*160)

def forms(d,t):
    val=window(t,16.6,24.5,.7)
    if not val:return
    # Qualitative modification INSIDE a bounded form, not moving particles or transferred material.
    for k,(cx,cy,i) in enumerate([(340,415,1),(512,415,3),(684,415,6)]):
        col=COLORS[i]
        d.ellipse((cx-42,cy-42,cx+42,cy+42),outline=(175,189,204,int(135*val)),width=2)
        d.ellipse((cx-32,cy-32,cx+32,cy+32),fill=(45,65,85,int(90*val)))
        for q in range(9):
            angle=TAU*q/9
            rr=12+4*math.sin(q*.7+i*1.2)
            x=cx+rr*math.cos(angle);y=cy+rr*math.sin(angle)
            dot(d,x,y,1.5+(q%3==0),col,val*(120+110*fade(t,17,20)))
        if i==1:
            d.ellipse((cx-21,cy-21,cx+21,cy+21),outline=(*col,int(190*val)),width=2)
        if i==3:
            for q in range(6):
                aa=TAU*q/6
                line(d,(cx,cy),(cx+27*math.cos(aa),cy+27*math.sin(aa)),col,160*val,2)
        if i==6:
            for q in range(-24,25,12):
                line(d,(cx-20,cy+q),(cx+20,cy+q),col,170*val,2)
        center_text=f'FORM {k+1}'
        box=d.textbbox((0,0),center_text,font=LABEL)
        text(d,(cx-(box[2]-box[0])/2,467),center_text,LABEL,PALE,180*val)

def frame(t):
    im=BASE.copy(); d=ImageDraw.Draw(im,'RGBA')
    intro=window(t,0,3.05,.55)
    if intro:
        text(d,(77,178),'ONE LIFE',TITLE,IVORY,intro*250)
        text(d,(77,233),'SEVEN QUALITIES',TITLE,IVORY,intro*250)
        line(d,(79,298),(437,298),GOLD,150*intro,2)
        text(d,(80,319),S['attribution'],SUB,PALE,220*intro)
        text(d,(80,353),'VISUAL EXPERIMENT 002',MINI,GOLD,190*intro)
    present=fade(t,2.9,4.0)
    if present:
        source(im,present)
        d=ImageDraw.Draw(im,'RGBA')
        strength=window(t,3.1,24.7,.6)*160
        for i in range(7):spoke(d,i,t,strength)
        partition(d,t)
        forms(d,t)
        line(d,(68,63),(955,63),PALE,58*present,1)
        text(d,(70,39),'QUALITIES OF MANIFESTATION',LABEL,IVORY,200*present)
        stages=[(3,10,'01  DIFFERENTIATE'),(10,16.6,'02  CLASSIFY'),(16.6,24,'03  QUALIFY')]
        for a,b,name in stages:
            z=window(t,a,b,.55)
            if z:text(d,(821,40),name,MINI,GOLD,200*z)
        # Caption band is commentary; visual encoding above is independently inspectable.
        d.rounded_rectangle((49,495,975,558),radius=11,fill=(10,19,34,194),outline=(127,147,169,39))
        for a,b,head,desc in [
            (3,10,'One Life, seven distinct rays','Differentiation without material depletion.'),
            (10,16.6,'Three Rays of Aspect; four of Attribute','Two classes within a sevenfold expression.'),
            (16.6,24,'The rays qualify manifested forms','Properties are conditioned; no substance is consumed.')]:
            z=window(t,a,b,.55)
            if z:
                text(d,(70,501),head,CAP,IVORY,245*z)
                text(d,(72,535),desc,MINI,PALE,188*z)
    return im.convert('RGB')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',default=str(HERE/'visual-experiment-002.mp4'))
    ap.add_argument('--contact',default=str(HERE/'contact-sheet.jpg'))
    ap.add_argument('--samples',type=int,default=0)
    args=ap.parse_args()
    sheet=Image.new('RGB',(1024,864),(8,14,26))
    for k,t in enumerate([1.5,6.4,12.2,18.6,22]):
        im=frame(t);im.thumbnail((512,288));sheet.paste(im,((k%2)*512,(k//2)*288))
    Path(args.contact).parent.mkdir(parents=True,exist_ok=True)
    sheet.save(args.contact,quality=91)
    total=args.samples if args.samples>0 else FPS*DURATION
    Path(args.out).parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24',
         '-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-vcodec','libx264',
         '-pix_fmt','yuv420p','-preset','veryfast','-crf','20','-movflags','+faststart',args.out]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for i in range(total):proc.stdin.write(frame(i/FPS).tobytes())
        proc.stdin.close();err=proc.stderr.read().decode();code=proc.wait()
        if code:raise RuntimeError('ffmpeg failed: '+err)
    finally:
        if proc.poll() is None:proc.kill()
    print(f'Wrote {total} frames at {FPS} fps to {args.out}')

if __name__=='__main__':main()
