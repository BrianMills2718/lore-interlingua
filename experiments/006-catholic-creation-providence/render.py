#!/usr/bin/env python3
"""Render Film 006: a single Catholic creation and providence narrative.
Original procedural graphics, no external media or copyrighted audio.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, math, random, subprocess, wave, pathlib, textwrap, os, argparse, sys, time

ROOT = pathlib.Path(__file__).resolve().parent
W, H = 960, 540
FPS, DURATION = 20, 84
S = math.sin
C = math.cos
TWOPI = math.tau
rng = random.Random(20261028)
SERIF = '/usr/share/fonts/truetype/ebgaramond/EBGaramond12-Regular.ttf'
ITALIC = '/usr/share/fonts/truetype/ebgaramond/EBGaramond12-Italic.ttf'
SANS = '/usr/share/fonts/truetype/lato/Lato-Regular.ttf'
SANS_BOLD = '/usr/share/fonts/truetype/lato/Lato-Bold.ttf'
F= lambda n, f=SERIF: ImageFont.truetype(f, n)
TITLE=F(46); TITLESUB=F(21, ITALIC); CAP=F(29); SM=F(16,SANS); SMALL=F(13,SANS); NUMBER=F(13,SANS_BOLD)

# Palette: organic etching on twilight slate; never a code for good/evil.
INK=(224,216,189); GILT=(225,196,126); BARK=(77,61,50); BARK_HI=(153,122,81)
LEAF1=(84,125,99); LEAF2=(113,149,111); LEAF3=(156,170,119)
WATER=(112,175,191); WATER_HI=(196,219,217)

# Smooth envelopes for narrative attention and camera movement.
def clamp(v,a=0,b=1):return max(a,min(b,v))
def smooth(v):
 v=clamp(v);return v*v*(3-2*v)
def window(t,a,b,c,d):return smooth((t-a)/(b-a))* (1-smooth((t-c)/(d-c)))
def lerp(a,b,u):return a+(b-a)*u

# Deliberately chosen single continuous habitat; coordinates stable throughout.
GROUND=386
TREE_X=652
TREE_Y=397
PERSON_X=521
# Fixed organic twig network via recursion. Slight asymmetry, organic continuity.
branches=[]
def make_branch(x,y,angle,length,width,depth,key):
 if depth<=0 or length<5:
  return
 nx=x+math.cos(angle)*length; ny=y+math.sin(angle)*length
 branches.append((x,y,nx,ny,width,depth))
 if depth>1:
  r = random.Random(key)
  for i,sign in enumerate((-1,1)):
   bend=(.30+.31*r.random())*sign
   make_branch(nx,ny,angle+bend,length*(.71+.09*r.random()),max(.9,width*.70),depth-1,key*31+19+i)
  if depth>=3 and r.random()>.48:
   make_branch(nx,ny,angle+(.05*r.random()-.025),length*.62,max(.9,width*.52),depth-1,key*19+7)
make_branch(TREE_X,TREE_Y,-math.pi/2,85,15,6,13)
endpoints=[(x2,y2) for x1,y1,x2,y2,w,d in branches if d==1]
# Dense crown, using marks that remain attached to the same tree over time.
leaves=[]
for i in range(320):
 x,y=rng.choice(endpoints)
 ox=rng.gauss(0,19); oy=rng.gauss(0,15)
 leaves.append((x+ox,y+oy,rng.uniform(3,8),rng.random()*6.28,rng.random(),rng.random()))
# distant terrain static design

def create_bg():
 arr=np.zeros((H,W,3),dtype=np.uint8)
 for y in range(H):
  if y < GROUND:
   v=y/GROUND
   c=np.array((8,19,34))*(1-v)+np.array((39,57,68))*v
  else:
   v=(y-GROUND)/(H-GROUND)
   c=np.array((48,65,58))*(1-v)+np.array((35,41,42))*v
  arr[y,:,:]=np.maximum(0,np.minimum(255,c)).astype(np.uint8)
 bg=Image.fromarray(arr,'RGB').convert('RGBA'); d=ImageDraw.Draw(bg,'RGBA')
 # distant woodcuts, engraved slopes
 hills=[[(0,370),(80,333),(210,360),(350,326),(520,360),(690,315),(780,344),(960,322),(960,440),(0,440)],
        [(0,383),(145,360),(310,382),(440,353),(560,373),(715,354),(880,365),(960,348),(960,449),(0,449)]]
 d.polygon(hills[0],fill=(18,42,54,185));d.polygon(hills[1],fill=(38,58,54,205))
 # ground / soil cross-section (organic entanglement visible)
 d.polygon([(0,GROUND),(W,GROUND),(W,H),(0,H)],fill=(38,49,44,255))
 for k in range(9):
  yy=GROUND+14+k*17
  pts=[(x,int(yy+4*math.sin(x/79+.91*k)+2*math.cos(x/33+.8*k))) for x in range(0,W+2,4)]
  d.line(pts,fill=(160,135,95,max(12,40-2*k)),width=1)
 # decorative contour of soil not magical streams
 for i in range(110):
  x=rng.randint(0,W); y=rng.randint(GROUND+10,H-7); size=rng.choice([1,1,2]);
  d.ellipse((x-size,y-size,x+size,y+size),fill=(197,173,126,rng.randint(16,51)))
 # stream valley at lower left, natural water
 d.polygon([(0,426),(92,429),(166,443),(212,460),(232,502),(247,540),(0,540)],fill=(45,83,92,230))
 # faint engraved branches on distant hills
 for i in range(24):
  x=20+i*43; y=370+10*C(i*1.9); d.line([(x,y),(x-5,y-13)],fill=(74,89,76,75),width=1)
 # distant moon? no; constellation would confuse setting so omit.
 return bg
BG=create_bg()

# Air and rainfall; local causal processes rather than a cosmic source.
DROPS=[(rng.randint(-20,W+20),rng.randint(0,GROUND),rng.random(),rng.random()) for _ in range(110)]
SEEDS=[(rng.random()*W,rng.random()*H,rng.random()*6.28,rng.random()) for _ in range(65)]

# Text authored as brief integral complements to sustained movement.
CAPTIONS=[
 (0,9,"A living world. A world of real causes."),
 (9,19,"Sunlight warms the leaves. Rain reaches the soil."),
 (19,31,"Roots take up water. A human hand tends the tree."),
 (31,43,"These are causes within creation."),
 (43,55,"But existence is not another substance flowing through them."),
 (55,68,"Catholic teaching: God sustains all things in being, at every moment."),
 (68,79,"The world depends on its Creator—and still genuinely acts."),
 (79,84,"Creation is sustained. Creation is unfolding.")
]

def line(ctx,pts,color,width=1):
 ctx.line([(int(x),int(y)) for x,y in pts],fill=color,width=max(1,int(width)),joint='curve')

def draw_sun(d,t):
 x=463+10*math.sin(t/50); y=108+2*math.sin(t/24)
 for rr,a in [(63,10),(46,18)]:d.ellipse((x-rr,y-rr,x+rr,y+rr),outline=(246,215,149,a),width=2)
 d.ellipse((x-20,y-20,x+20,y+20),fill=(218,190,124,212),outline=(249,223,161,140),width=2)
 for k in range(14):
  angle=TWOPI*k/14+0.03*math.sin(t/4)
  a=27; b=35+3*math.sin(t/3+k)
  line(d,[(x+a*C(angle),y+a*S(angle)),(x+b*C(angle),y+b*S(angle))],(234,205,145,93),1)

def draw_sky(d,t):
 # Cloud strips drift continuously; not stage cards.
 for n in range(6):
  # Hairline atmospheric cloud strokes; never anonymous circles/nodes.
  x=((n*232 +t*(2.1+n*.37))%(W+370))-185
  y=114+(n*73)%165
  pts=[(x+j*7,y+2.5*math.sin(j*.21+n*1.2)) for j in range(29)]
  line(d,pts,(151,178,179,33),2)
  line(d,[(xx,yy+6) for xx,yy in pts[4:-4]],(136,161,170,19),1)
 for i,(x,y,a,b) in enumerate(SEEDS):
  xx=(x+t*(1+b)*1.8)%W
  d.ellipse((xx,y,xx+1.2,y+1.2),fill=(236,228,192,int(35+20*(1+math.sin(t+i))/2)))

def draw_rain(d,t):
 # Rain changes intensity across time: ongoing water cycle, not divine emission.
 k=window(t,5,11,17,23)+0.5*window(t,54,58,62,67)
 if k<=.02:return
 for i,(x,y,p,spd) in enumerate(DROPS):
  yy=(y+t*(130+75*spd))%GROUND
  xx=(x-0.21*t*(130+75*spd))%W
  d.line([(xx,yy),(xx-3,yy+8)],fill=(178,207,206,int(clamp(k)* (75+90*p))),width=1)

def draw_roots(d,t):
 # Root arbor, individual thick roots not arbitrary symbolic nodes.
 for j in range(12):
  side=(-1)**j
  base=TREE_X + (j%3-1)*6
  pts=[(base,GROUND-3),(base+side*(13+j*.8),GROUND+15),(base+side*(25+2*j),GROUND+43+3*C(j)),(base+side*(40+3*j),GROUND+71+(j%3)*6)]
  line(d,pts,(107,91,67,190),3 if j<8 else 2)
  # smaller fine root tips
  xx,yy=pts[-1];line(d,[(xx,yy),(xx+side*17,yy+8)],(145,126,90,100),1)

def draw_tree(d,t):
 # Trunk; animated fine leaves, not continuous structural teleporting of nodes.
 for j,(x,y,xx,yy,w,depth) in enumerate(branches):
  width=max(1,int(w))
  line(d,[(x,y),(xx,yy)],(49,43,39,230),width+2)
  line(d,[(x,y),(xx,yy)],(147,117,79,235),width)
  if depth>=4:
   line(d,[(x-1,y),(xx-1,yy)],(193,155,102,100),1)
 growth=.75+.25*smooth(t/75)
 for j,(x,y,sz,phase,p,q) in enumerate(leaves):
  xx=x+2.6*math.sin(t*.6+phase+q*2)
  yy=y+1.5*math.sin(t*.44+phase)
  rad=max(1.1,sz*growth*(.9+.12*math.sin(t*.31+phase)))
  palette=[LEAF1,LEAF2,LEAF3]
  r,g,b=palette[j%3]
  # botanical etched oval leaves, irregular hues, translucent underlying network
  d.ellipse((xx-rad*1.36,yy-rad*.72,xx+rad*1.25,yy+rad*.72),fill=(r,g,b,200),outline=(176,188,127,140),width=1)
  if j%4==0:
   d.line((xx-rad*.6,yy,xx+rad*.75,yy),fill=(199,203,147,100),width=1)
 # fruit appears only late, not a metaphysical signal; natural development over time
 f=smooth((t-64)/13)
 if f>.01:
  for x,y in [(615,282),(686,310),(742,251),(573,318)]:
   rad=4.4*f;d.ellipse((x-rad,y-rad,x+rad,y+rad),fill=(184,128,79,int(225*f)),outline=(245,189,111,int(180*f)))

def draw_human(d,t):
 x=PERSON_X;y=376
 # Human with visible body, action and intention, not abstract 'free will' symbol.
 # silhouette: natural tunic and shoulders
 d.ellipse((x-9,y-64,x+9,y-45),fill=(190,162,130,247),outline=(59,52,52,230))
 d.polygon([(x-10,y-43),(x+14,y-42),(x+18,y-4),(x-18,y-4)],fill=(97,110,103,235),outline=(172,148,116,130))
 for side in [-1,1]:
  line(d,[(x+side*9,y-6),(x+side*12,y+15),(x+side*18,y+17)],(146,130,110,238),5)
 # animate arm and watering jug in later segment
 pour=smooth((t-19)/6)*(1-smooth((t-32)/5))
 hx=x+12+pour*20; hy=y-37-pour*4
 line(d,[(x+10,y-36),(hx,hy),(hx+12,hy-3)],(183,153,121,255),5)
 # left arm on hip
 line(d,[(x-11,y-37),(x-21,y-21),(x-14,y-15)],(174,153,126,220),4)
 if pour>.06:
  bx=hx+16;by=hy-5
  d.rounded_rectangle((bx-4,by-8,bx+15,by+7),radius=4,fill=(114,143,143,int(220*pour)),outline=(205,217,191,int(230*pour)),width=2)
  d.arc((bx+10,by-6,bx+27,by+7),0,220,fill=(217,226,192,int(200*pour)),width=2)
  # watering stream to small ground cover near tree
  for k in range(11):
   f=(k/10+t*.77)%1
   xx=bx+25+f*95; yy=by+12+f*f*118
   d.ellipse((xx-1,yy-1,xx+2,yy+3),fill=(146,205,216,int(165*pour)))

def draw_stream(d,t):
 # Winding water contours left foreground; movement distinct from world-support metaphor.
 for k in range(9):
  pts=[]
  for xx in range(0,250,7):
   center=442+(xx/250)**2*100
   yy=center+k*7+2.4*math.sin(xx*.047-t*(1.3+.14*k)+k)
   pts.append((xx,yy))
  line(d,pts,(141,195,207,70+6*k),1 if k%3 else 2)
 for i in range(14):
  x=((i*48+t*21) %280)-20
  y=442+(x/250)**2*100+i%5*5
  d.ellipse((x,y,x+3,y+1),fill=(209,218,201,99))

def draw_physical_flows(d,t):
 # short-lived blue pulses represent water *within* creation, no divine pipes.
 a=window(t,19,22,33,37)
 if a>.02:
  for k in range(22):
   p=(t*.16+k/22)%1
   yy=GROUND+32-p*197
   xx=TREE_X+(13 if p<.5 else -10)+8*math.sin(p*5+k*.2)
   d.ellipse((xx-1.7,yy-1.7,xx+1.7,yy+1.7),fill=(138,196,214,int(130*a)))
 # sun leaf warm highlights; no mythic energy link
 a=window(t,10,13,26,30)
 if a>.02:
  for k in range(10):
   x=230+k*30+8*math.sin(k*1.5+t/12)
   y=160+k*13
   d.line((x,y,x+40,y+28),fill=(237,208,135,int(a*35)),width=1)

def draw_grounding(d,t):
 # Simultaneously revealed, distributed contour of being: no beam or packets.
 a=smooth((t-42)/10)*(.72+.08*math.sin(t*.19))
 if a<.01:return
 for i,(x,y,sz,phase,p,q) in enumerate(leaves[::5]):
  xx=x+2.6*math.sin(t*.6+phase+q*2)
  yy=y+1.5*math.sin(t*.44+phase)
  rr=sz*1.6
  d.arc((xx-rr,yy-rr*.8,xx+rr,yy+rr*.8),185,335,fill=(240,208,137,int(80*a)),width=1)
 for j,(x,y,xx,yy,w,depth) in enumerate(branches):
  if depth>=3 or j%3==0:line(d,[(x+1.4,y),(xx+1.4,yy)],(222,193,132,int(120*a)),1)
 # No enclosing rectangle standing in for God; gold appears on *created* things.
 for yy in [GROUND-2,GROUND+1]:
  line(d,[(0,yy),(W,yy)],(210,185,129,int(50*a)),1)
 for dx,dy,rx,ry in [(PERSON_X,326,12,13),(PERSON_X,356,18,31),(463,108,21,21)]:
  d.arc((dx-rx,dy-ry,dx+rx,dy+ry),10,168,fill=(234,198,128,int(74*a)),width=1)
 for x in range(20,210,15):
  d.line((x,446+math.sin(t+x*.11)*2,x+8,445+math.sin(t+x*.11)*2),fill=(233,205,143,int(50*a)),width=1)

# labels integrated in the moving scene; fewer than a slide of paragraphs.
def label(d,x,y,text_,start,end,t,accent=None):
 a=window(t,start,start+1.7,end-2.1,end)
 if a<.01:return
 col=accent or (214,210,189)
 d.text((x,y),text_,font=SM,fill=(*col,int(210*a)),stroke_width=0)

def screen_of(x,y,t):
 cx,cy,z=camera_pose(t)
 return W/2+(x-cx)*z, H/2+(y-cy)*z

def overlay(d,t):
 # Film identification not a sequence of static title cards.
 d.text((34,23),'CATHOLIC CREATION  /  PROVIDENCE',font=SM,fill=(215,212,189,170))
 d.line((34,52,360,52),fill=(226,196,137,72),width=1)
 if t<8:
  alpha=int(255*(1-smooth((t-5.5)/2.5)))
  d.text((34,76),'The world that is',font=TITLE,fill=(241,229,198,alpha))
  d.text((34,122),'continually created',font=TITLE,fill=(241,229,198,alpha))
  d.text((36,185),'A visual interpretation of Catholic teaching',font=TITLESUB,fill=(216,201,167,int(alpha*.78)))
 # A single landscape, not multiple new cards.
 for px,py,word,a,b,color in [(470,180,'SUNLIGHT',10,25,(236,213,156)),(60,438,'RUNNING WATER',16,33,(167,208,214)),(665,406,'ROOTS  •  GROWTH',18,40,(182,209,175)),(516,295,'CREATURELY ACTION',22,37,(208,199,173))]:
  sx,sy=screen_of(px,py,t)
  if 30<sx<W-130 and 90<sy<440:label(d,sx,sy,word,a,b,t,color)
 a=window(t,45,49,78,82)
 if a>.01:
  d.text((220,233),'SUSTAINED IN BEING',font=F(23,ITALIC),fill=(239,206,144,int(a*234)),anchor='mm')
 # Caption scrim lower quarter; transparently over world, avoid covering subject.
 d.rectangle((0,448,W,H),fill=(5,12,20,175))
 d.line((29,455,W-29,455),fill=(220,188,123,78),width=1)
 for a,b,txt in CAPTIONS:
  if a<=t<b:
   fade=min(1,(t-a)/.75,(b-t)/.7)
   a2=int(238*smooth(fade))
   # Avoid labels above 80 chars visually; split by natural clause for last segments.
   if len(txt)>75:
    pre=txt.replace('all things in being, at every moment.','all things in being, at every moment.')
    fnt=F(25)
   else: fnt=CAP
   d.text((W//2,486),txt,font=fnt,fill=(242,231,204,a2),anchor='mm')
 d.text((36,H-22),'CCC 295–308   •   A VISUAL INTERPRETATION',font=SMALL,fill=(178,183,181,135))
 d.text((W-35,H-22),'06   /   '+str(int(t)).zfill(2),font=SMALL,fill=(187,180,150,150),anchor='ra')

def camera_pose(t):
 # Camera is part of the continuous explanation: move from the whole organism
 # to its real physical causes, then back to its all-encompassing dependence.
 poses=[(0,480,270,1.03),(9,480,275,1.09),(16,555,330,1.23),
        (26,565,412,1.47),(34,566,399,1.38),(43,535,280,1.07),
        (52,485,265,1.01),(61,485,266,1.01),(72,533,285,1.17),(84,526,289,1.19)]
 for a,b in zip(poses,poses[1:]):
  if a[0]<=t<=b[0]:
   u=smooth((t-a[0])/(b[0]-a[0]));return (lerp(a[1],b[1],u),lerp(a[2],b[2],u),lerp(a[3],b[3],u))
 return poses[-1][1:]

def camera(im,t):
 cx,cy,z=camera_pose(t)
 sx=W/z;sy=H/z
 box=(cx-sx/2,cy-sy/2,cx+sx/2,cy+sy/2)
 return im.transform((W,H),Image.Transform.EXTENT,box,resample=Image.Resampling.BICUBIC,fillcolor=(8,18,30))

def render_at(t):
 im=BG.copy();d=ImageDraw.Draw(im,'RGBA')
 draw_sky(d,t)
 draw_sun(d,t)
 draw_rain(d,t)
 draw_roots(d,t)
 draw_tree(d,t)
 draw_human(d,t)
 draw_stream(d,t)
 draw_physical_flows(d,t)
 draw_grounding(d,t)
 im=camera(im,t)
 overlay(ImageDraw.Draw(im,'RGBA'),t)
 return im.convert('RGB')

def write_audio(path):
 # Original ambient score; no melody, external recording, or claimed real-world sound.
 sr=24000;n=int(DURATION*sr)
 rng_=np.random.default_rng(125)
 t=np.arange(n,dtype=np.float32)/sr
 sig=np.zeros(n,dtype=np.float32)
 freqs=[110.,164.8138,196.,261.6256]
 for j,f in enumerate(freqs):
  phase=2*np.pi*f*t
  env=.65+.35*np.sin(2*np.pi*(.011+j*.003)*t+2*j)
  sig+= (np.sin(phase)+.18*np.sin(2*phase))*.017*env
 # Rain texture, controlled, non-figurative
 noise=rng_.normal(0,1,n).astype(np.float32)
 smooth_noise=np.convolve(noise,np.ones(80,dtype=np.float32)/80,'same')
 for a,b,scale in [(7,21,.021),(53,64,.008)]:
  mask=np.maximum(0,np.minimum(1,(t-a)/3))*np.maximum(0,np.minimum(1,(b-t)/3))
  sig+=smooth_noise*mask*scale
 sig*=np.minimum(1,t/2.5)*np.minimum(1,(DURATION-t)/3.5)
 sig=np.int16(np.clip(sig,-.87,.87)*32767)
 with wave.open(str(path),'wb') as wf:
  wf.setnchannels(1);wf.setsampwidth(2);wf.setframerate(sr);wf.writeframes(sig.tobytes())


def main():
 parser=argparse.ArgumentParser();parser.add_argument('--preview',action='store_true');parser.add_argument('--seconds',type=int,default=DURATION)
 a=parser.parse_args()
 if a.preview:
  ts=[3,15,27,38,49,62,73,81]
  thumbs=[]
  for t in ts:
   im=render_at(t);im.save(ROOT/f'frame_{t:02}.jpg',quality=89)
   thumbs.append(im.resize((480,270)))
  sheet=Image.new('RGB',(960,1080));
  for i,img in enumerate(thumbs):sheet.paste(img,((i%2)*480,(i//2)*270))
  sheet.save(ROOT/'contact-sheet.jpg',quality=92)
  print('Wrote contact-sheet.jpg');return
 out=str(ROOT/'catholic_creation_providence.mp4');temp=str(ROOT/'silent.mp4');audio=str(ROOT/'ambient.wav')
 args=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',temp]
 p=subprocess.Popen(args,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
 N=a.seconds*FPS
 try:
  for n in range(N):
   p.stdin.write(render_at(n/FPS).tobytes())
   if (n+1)%(FPS*10)==0:print(f'Frames {n+1}/{N}',flush=True)
 finally:
  p.stdin.close()
 rc=p.wait();err=p.stderr.read().decode()
 if rc:raise RuntimeError(err)
 write_audio(audio)
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',temp,'-i',audio,'-c:v','copy','-c:a','aac','-b:a','112k','-shortest','-movflags','+faststart',out],check=True)
 print('Rendered',out,os.stat(out).st_size)

if __name__=='__main__':main()