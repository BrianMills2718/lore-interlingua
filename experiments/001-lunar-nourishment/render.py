#!/usr/bin/env python3
"""Visual Experiment 001: art-directed rendering from a semantic scene manifest.

Dependencies: Pillow, numpy, ffmpeg. No third-party visual or audio assets.
Example: python render.py --out /tmp/scene.mp4 --contact /tmp/scene.png
"""
from __future__ import annotations
import argparse
import json
import math
import random
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
SPEC = json.loads((HERE / "scene.json").read_text())
W, H = SPEC["resolution"]
FPS, DURATION = SPEC["fps"], SPEC["duration_seconds"]
TAU = math.tau
SUN, PLANET, EARTH, MOON = (140, 155), (580, 120), (422, 283), (832, 287)
INK = (12, 21, 39)
IVORY = (234, 233, 223)
PALE = (169, 183, 206)
TEAL = (91, 199, 200)
GOLD = (241, 199, 120)
FONT_PATH = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
F_TITLE = ImageFont.truetype(FONT_BOLD, 42)
F_SUB = ImageFont.truetype(FONT_PATH, 18)
F_SMALL = ImageFont.truetype(FONT_BOLD, 13)
F_CAP = ImageFont.truetype(FONT_PATH, 27)
F_MINI = ImageFont.truetype(FONT_PATH, 12)
RNG = random.Random(2217)


def smooth(x):
    x = max(0., min(1., x))
    return x*x*(3-2*x)


def ramp(t, a, b):
    return smooth((t-a)/(b-a))


def interval(t, a, b, fade=.7):
    return ramp(t, a, a+fade)*(1-ramp(t, b-fade, b))


def curve(a, b, c, d, u):
    v = 1-u
    return (v*v*v*a[0]+3*v*v*u*b[0]+3*v*u*u*c[0]+u*u*u*d[0],
            v*v*v*a[1]+3*v*v*u*b[1]+3*v*u*u*c[1]+u*u*u*d[1])


def pathpoints(a,b,c,d,n=70):
    return [curve(a,b,c,d,i/(n-1)) for i in range(n)]


# Astronomical graphic; stars and orbital guides are decoration, not ontology.
yy, xx = np.mgrid[0:H, 0:W]
base = np.empty((H, W, 3), dtype=np.uint8)
base[:,:,0] = 10 + (7*yy/H).astype(np.uint8)
base[:,:,1] = 20 + (12*yy/H).astype(np.uint8)
base[:,:,2] = 38 + (17*yy/H).astype(np.uint8)
vig = np.clip(1-0.27*((xx-W/2)**2/(W/2)**2 + (yy-H/2)**2/(H/2)**2), .72, 1)
base = np.uint8(base*vig[...,None])
BACKGROUND = Image.fromarray(base, 'RGB').convert('RGBA')
_bgdraw = ImageDraw.Draw(BACKGROUND,'RGBA')
STARS = [(RNG.randrange(18,W-18),RNG.randrange(12,H-74),RNG.choice([1,1,1,2]),RNG.randrange(37,130)) for _ in range(130)]
for sx,sy,sr,sa in STARS:
    _bgdraw.ellipse((sx-sr/2,sy-sr/2,sx+sr/2,sy+sr/2),fill=(221,232,255,sa))
for size in (275, 365, 465):
    _bgdraw.arc((EARTH[0]-size, EARTH[1]-size*.62, EARTH[0]+size,EARTH[1]+size*.62), 195, 346, fill=(118,143,173,27),width=1)


def glow(color, r):
    canvas = Image.new('RGBA', (r*6,r*6))
    d=ImageDraw.Draw(canvas,'RGBA')
    q=3*r
    d.ellipse((q-r,q-r,q+r,q+r), fill=(*color,110))
    return canvas.filter(ImageFilter.GaussianBlur(max(9,r*.68)))

GLOW_EARTH = glow(TEAL,94)
GLOW_MOON = glow(GOLD,74)
GLOW_SUN = glow(GOLD,50)


def compose_glow(im,sprite,pos,strength=1):
    if strength<=0:return
    s = sprite if strength>.99 else sprite.copy()
    if strength<.99:
        al=s.getchannel('A').point(lambda z:int(z*strength))
        s.putalpha(al)
    im.alpha_composite(s,(int(pos[0]-s.width/2),int(pos[1]-s.height/2)))


def globe(radius,kind):
    rr=radius*2+12
    img=Image.new('RGBA',(rr,rr))
    pix=ImageDraw.Draw(img,'RGBA')
    cx=cy=radius+6
    if kind=='earth':
        pix.ellipse((cx-radius,cy-radius,cx+radius,cy+radius),fill=(34,77,100,255),outline=(117,178,191,180),width=2)
        # Abstract banded continents: a recognizable Earth, not literal geography.
        for phase in range(-75,76,9):
            angle=phase/90*math.pi/2
            y=cy+math.sin(angle)*radius*.89
            rx=math.sqrt(max(0,radius**2-(y-cy)**2))
            if rx<5:continue
            k=math.sin(phase*.21)+math.cos(phase*.41)*.4
            xc=cx+rx*(.23*math.sin(phase*.065))
            length=rx*(.18+.3*(k+1)/2)
            pix.rounded_rectangle((xc-length,y-2.7,xc+length,y+2.7),radius=3,fill=(104,147,130,112))
        for i in range(14):
            theta=i*TAU/14
            x=cx+radius*.66*math.cos(theta); y=cy+radius*.68*math.sin(theta)
            pix.ellipse((x-2,y-2,x+2,y+2),fill=(201,222,194,75))
        pix.arc((cx-radius*.8,cy-radius*.86,cx+radius*.73,cy+radius*.75),195,305,fill=(234,246,247,105),width=2)
    elif kind=='moon':
        pix.ellipse((cx-radius,cy-radius,cx+radius,cy+radius),fill=(119,134,157,255),outline=(207,212,220,170),width=2)
        craters=[(-.35,-.27,.19),(.38,.32,.12),(.13,-.45,.11),(-.17,.38,.14),(.43,-.20,.1)]
        for ox,oy,q in craters:
            x=cx+ox*radius;y=cy+oy*radius;r=q*radius
            pix.ellipse((x-r,y-r,x+r,y+r),outline=(65,82,105,94),width=2)
            pix.arc((x-r+2,y-r+2,x+r-2,y+r-2),210,330,fill=(212,222,228,70),width=2)
    elif kind=='sun':
        pix.ellipse((cx-radius,cy-radius,cx+radius,cy+radius),fill=(215,168,91,255),outline=(255,235,162,190),width=2)
        for i in range(9):
            a=i*TAU/9
            pix.arc((cx-radius*.74,cy-radius*.74,cx+radius*.74,cy+radius*.74),i*40,i*40+25,fill=(255,239,191,58),width=3)
    else:
        pix.ellipse((cx-radius,cy-radius,cx+radius,cy+radius),fill=(103,112,156,255),outline=(186,190,225,140),width=2)
        pix.arc((cx-radius*.72,cy-radius*.79,cx+radius*.72,cy+radius*.8),38,250,fill=(216,199,228,89),width=3)
    return img

EARTH_IMG = globe(91,'earth')
MOON_IMG = globe(57,'moon')
SUN_IMG = globe(35,'sun')
PLANET_IMG = globe(24,'planet')

def place(im,sprite,center):
    im.alpha_composite(sprite,(int(center[0]-sprite.width/2),int(center[1]-sprite.height/2)))


def stroke(draw,points,color,width=2):
    draw.line(points,fill=color,width=width,joint='curve')


def linepath(draw,pts,c,opacity,width=2):
    if opacity>0:stroke(draw,pts,(*c,int(255*opacity)),width)

# Curved paths deliberately avoid suggesting straight physical pipes.
INCOMING=[
    ((164,167),(198,152),(272,184),(365,240)),
    ((574,141),(560,194),(515,180),(472,218)),
]
TO_MOON=((493,310),(595,275),(710,277),(775,290))
TO_SUN=((366,259),(250,211),(210,186),(176,173))
TO_PLANET=((432,216),(477,146),(506,126),(555,122))


def pulse(draw, path, phase, count, color, shape='circle', alpha=220):
    for j in range(count):
        u=((phase-j/count) % 1)
        if u<.075 or u>.925:continue
        x,y=curve(*path,u)
        a=int(alpha*min(1,u/.2,(1-u)/.2))
        r=3.5 if shape=='circle' else 3.2
        if shape=='diamond':
            draw.polygon([(x,y-r*1.7),(x+r*1.4,y),(x,y+r*1.7),(x-r*1.4,y)],fill=(*color,a))
        elif shape=='dash':
            draw.line((x-2,y-4,x+2,y+4),fill=(*color,a),width=3)
        else:
            draw.ellipse((x-r,y-r,x+r,y+r),fill=(*color,a))


def label(draw,text,center,y,color=PALE):
    box=draw.textbbox((0,0),text,font=F_SMALL)
    draw.text((center-(box[2]-box[0])/2,y),text,font=F_SMALL,fill=(*color,210))


def render(t):
    im=BACKGROUND.copy()
    g=ImageDraw.Draw(im,'RGBA')
    entry=ramp(t,.7,2.7)
    body=ramp(t,2.5,3.6)
    # Epigraph appears only at opening. Other scenes have no qualification overlays.
    intro=interval(t,0,3.45,.9)
    if intro>0:
        g.text((74,170),'THE EARTH',font=F_TITLE,fill=(*IVORY,int(255*intro)))
        g.text((74,223),'AS TRANSMITTER',font=F_TITLE,fill=(*IVORY,int(255*intro)))
        g.line((75,285,382,285),fill=(*GOLD,int(160*intro)),width=2)
        g.text((77,311),SPEC['attribution'],font=F_SUB,fill=(*PALE,int(217*intro)))
        g.text((77,343),'Visual Experiment 001',font=F_MINI,fill=(*GOLD,int(180*intro)))
    if body==0: return im.convert('RGB')
    # All overlays below are art directed; the semantic roles live in scene.json.
    compose_glow(im,GLOW_SUN,SUN,.18*body)
    compose_glow(im,GLOW_EARTH,EARTH,(.17+.22*ramp(t,9,13))*body)
    compose_glow(im,GLOW_MOON,MOON,(.09+.45*ramp(t,16,21))*body)
    g=ImageDraw.Draw(im,'RGBA')
    # Planets and labelled celestial actors.
    place(im,SUN_IMG,SUN)
    place(im,PLANET_IMG,PLANET)
    place(im,EARTH_IMG,EARTH)
    place(im,MOON_IMG,MOON)
    g=ImageDraw.Draw(im,'RGBA')
    ring=(.32+.50*ramp(t,8,11))*body
    for rad in (100,110):
        g.arc((EARTH[0]-rad,EARTH[1]-rad,EARTH[0]+rad,EARTH[1]+rad),205,517,fill=(*TEAL,int(115*ring)),width=3 if rad==100 else 1)
    # Biosphere: independently moving marks attached to an enclosing sphere.
    for j in range(38):
        a=TAU*j/38+t*.045
        r=101+2*math.sin(j*4.3+t*.5)
        x=EARTH[0]+math.cos(a)*r; y=EARTH[1]+math.sin(a)*r
        alpha=int(115*ring*(.70+.30*math.sin(j*.8+t*.7)**2))
        g.ellipse((x-1.5,y-1.5,x+1.5,y+1.5),fill=(*TEAL,alpha))
    # incoming (causal-semantic mediation, animated via a learned transient marker).
    incoming = interval(t,4,15,1.)
    for p in INCOMING:
        linepath(g,pathpoints(*p),(86,191,212),.19*incoming,1)
        if incoming>0:pulse(g,p,t*.17,7,TEAL,'circle',int(210*incoming))
    # received influence continues *across* the living layer into Earth.
    if incoming>0:
        q=((387,232),(398,241),(405,251),(417,266))
        linepath(g,pathpoints(*q),TEAL,.11*incoming,1)
        pulse(g,q,t*.22,3,(139,229,226),'circle',int(155*incoming))
    # outgoing is a distinct event from reception; avoid a one-for-one conversion animation.
    nourishment=interval(t,13.1,29,.9)
    linepath(g,pathpoints(*TO_MOON),GOLD,.28*nourishment,2)
    if nourishment:pulse(g,TO_MOON,t*.155,8,GOLD,'diamond',int(228*nourishment))
    # later differentiated streams to Sun / planets use different shape convention.
    diversification=ramp(t,21.3,23.8)
    if diversification:
        linepath(g,pathpoints(*TO_SUN),(221,178,131),.22*diversification,1)
        linepath(g,pathpoints(*TO_PLANET),(188,164,227),.22*diversification,1)
        pulse(g,TO_SUN,t*.135,5,(241,199,120),'dash',int(191*diversification))
        pulse(g,TO_PLANET,t*.15,5,(188,164,227),'circle',int(191*diversification))
    label(g,'SUN',SUN[0],204)
    label(g,'PLANETARY WORLD',PLANET[0],158)
    label(g,'EARTH',EARTH[0],409)
    label(g,'ORGANIC LIFE',EARTH[0],431,TEAL)
    label(g,'MOON',MOON[0],368)
    # Subtle field indicator rather than a claim of a measured physical magnitude.
    if t>=15:
        a=ramp(t,16,21)
        g.arc((MOON[0]-72,MOON[1]-72,MOON[0]+72,MOON[1]+72),190,505,fill=(*GOLD,int(126*a)),width=2)
    # Visual consistency: design/hierarchy/captions, not additional unsupported cosmology.
    g.line((68,64,956,64),fill=(150,165,185,73),width=1)
    g.text((70,35),'A COSMIC EXCHANGE',font=F_SMALL,fill=(*IVORY,190))
    stages=[(3.1,9,'01  RECEIVE'),(9,15,'02  MEDIATE'),(15,22,'03  NOURISH'),(22,29,'04  DIFFERENTIATE')]
    for a,b,s in stages:
        v=interval(t,a,b,.55)
        if v>0:g.text((810,35),s,font=F_MINI,fill=(*GOLD,int(225*v)))
    # Caption floor; the copy is separate from the encoded relationships.
    captions=[(3.25,9,'Celestial influences reach Earth','through the living surface.'),
              (9,15,'Organic life receives and transmits','different forms of influence.'),
              (15,22,'Its radiations nourish the Moon','within a larger cosmic system.'),
              (22,28,'Different celestial recipients','require different radiations.')]
    g.rounded_rectangle((50,478,974,552),radius=10,fill=(12,20,35,186),outline=(110,133,154,35),width=1)
    for a,b,major,minor in captions:
        v=interval(t,a,b,.55)
        if v<=0:continue
        g.text((72,488),major,font=F_CAP,fill=(*IVORY,int(246*v)))
        g.text((73,527),minor,font=F_MINI,fill=(*PALE,int(196*v)))
    # editorial ending, not a second qualification/disclaimer
    if t>25.5:
        v=ramp(t,25.5,27.3)
        g.text((740,454),'CHAPTER 7 · OUSPENSKY',font=F_MINI,fill=(*PALE,int(140*v)))
    return im.convert('RGB')


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',default=str(HERE/'visual-experiment-001.mp4'))
    ap.add_argument('--contact',default=str(HERE/'contact-sheet.jpg'))
    ap.add_argument('--samples',type=int,default=0,help='Render first N frames only (smoke test).')
    args=ap.parse_args()
    from PIL import ImageOps
    ts=[1.5,6.4,12.2,18.2,24.2]
    thumbs=[]
    for t in ts:
        im=render(t)
        im.thumbnail((512,288))
        thumbs.append(im)
    sheet=Image.new('RGB',(1024,864),(8,14,26))
    for i,im in enumerate(thumbs):
        x=(i%2)*512;y=(i//2)*288
        sheet.paste(im,(x,y))
    Path(args.contact).parent.mkdir(parents=True,exist_ok=True)
    sheet.save(args.contact,quality=90)
    n=args.samples or int(FPS*DURATION)
    Path(args.out).parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-vcodec','rawvideo',
         '-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
         '-an','-vcodec','libx264','-pix_fmt','yuv420p','-preset','veryfast','-crf','20',
         '-movflags','+faststart',str(args.out)]
    ff=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for i in range(n):
            ff.stdin.write(render(i/FPS).tobytes())
        ff.stdin.close()
        err=ff.stderr.read().decode()
        code=ff.wait()
        if code: raise RuntimeError('ffmpeg failed: '+err)
    finally:
        if ff.poll() is None: ff.kill()
    print(f'Wrote {n} frames at {FPS} fps: {args.out}')
    print(f'Contact sheet: {args.contact}')

if __name__=='__main__':main()
