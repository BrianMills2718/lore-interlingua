"""Original generative ambient score: no borrowed recording or composition.
Synthetic pads / wind / bells; crafted for this film's 86-second structure.
"""
from pathlib import Path
import numpy as np
from scipy.signal import butter,sosfilt
import soundfile as sf

SR=44100;DUR=86
rng=np.random.default_rng(19153)
t=np.arange(SR*DUR,dtype=np.float64)/SR
sigL=np.zeros(len(t),dtype=np.float64)
sigR=np.zeros(len(t),dtype=np.float64)

def smooth(a,b):
    return np.clip((t-a)/(b-a),0,1)**2 * (3-2*np.clip((t-a)/(b-a),0,1))
def envelope(start,end,fade=5):return smooth(start,start+fade)*(1-smooth(end-fade,end))

def pad(notes,start,end,level=.11):
    global sigL,sigR
    env=envelope(start,end,7)
    for k,f in enumerate(notes):
        for v,detune in enumerate([-0.004,0.004]):
            f2=f*(1+detune)
            phase=(k*.89+v*.51)
            a=np.sin(2*np.pi*t*f2+phase)+.25*np.sin(2*np.pi*t*f2*2+phase*1.1)+.07*np.sin(2*np.pi*t*f2*3+phase*1.2)
            # slight harmonic modulation, different pan positions
            a*=env*level/(len(notes)*2)*(0.7+.3*np.sin(2*np.pi*t*(.047+k*.003)+phase))
            if (k+v)%2: sigL+=a*.95;sigR+=a*.6
            else:sigR+=a*.95;sigL+=a*.6

# Broad modal movement, never a borrowed melody
pad([82.41,123.47,164.81,196.0,246.94],0,31,.33)
pad([65.41,98.0,164.81,196.0,293.66],18,54,.32)
pad([73.42,110.0,146.83,220,329.63],37,73,.34)
pad([82.41,123.47,164.81,220,293.66],58,86,.37)
# Low fundamental / sub swell
sigL+=np.sin(2*np.pi*41.205*t)*envelope(0,86,8)*.028
sigR+=np.sin(2*np.pi*41.26*t)*envelope(0,86,8)*.028

# Filtering white noise into broad slow texture (orchestral air, not hiss)
noise=rng.standard_normal(len(t)).astype(np.float64)
filtered=sosfilt(butter(3,800,fs=SR,output='sos'),noise)
filtered/=max(np.std(filtered),1e-10)
breath=.017*(.6+.4*np.sin(2*np.pi*.063*t+.3)**2)*envelope(0,86,3)
sigL+=filtered*breath*.85
sigR+=np.roll(filtered,2300)*breath*.7

# Bells are short, synthetic harmonic bursts; distinct pitches / restrained impact

def bell(at,f,amp=.05,pan=.5,decay=3.1):
    global sigL,sigR
    start=int(at*SR);end=min(len(t),start+int(9*SR))
    if start<0 or start>=end:return
    q=np.arange(end-start,dtype=np.float64)/SR
    a=(1-np.exp(-q*140))*np.exp(-q/decay)
    tone=(np.sin(2*np.pi*f*q)+.35*np.sin(2*np.pi*f*2.008*q+.3)+.17*np.sin(2*np.pi*f*3.98*q+.7))*a
    tone*=amp
    sigL[start:end]+=tone*np.sqrt(1-pan)
    sigR[start:end]+=tone*np.sqrt(pan)

for at,f,pan,amp in [(4,329.6,.25,.018),(13,246.9,.7,.024),(21,370,.2,.026),(25,329.6,.55,.026),
 (29,440,.75,.025),(35,293.7,.37,.024),(41,392,.3,.037),(46,493.9,.68,.043),
 (53,329.6,.4,.03),(58,440,.6,.036),(63,587.3,.23,.042),(67,659.3,.77,.041),
 (71,493.9,.42,.04),(76,440,.5,.035),(81,329.6,.5,.023)]:bell(at,f,amp,pan)

# Quiet emphasis on reception and outward radiation; noise rises in scene transitions
for center,span,amp in [(19,7,.016),(31,6,.019),(45,7,.021),(60,8,.03),(70,6,.018)]:
    gl=np.exp(-.5*((t-center)/(span/2))**2)
    sigL+=filtered*gl*amp
    sigR+=np.roll(filtered,5600)*gl*amp

# Fade to silence; maintain headroom
fade_out=1-smooth(82,86)
sigL*=fade_out;sigR*=fade_out
stereo=np.stack([sigL,sigR],axis=-1)
# gentle soft-clip to prevent a peak from dominating mastering
stereo=np.tanh(stereo*1.45)
peak=max(np.max(np.abs(stereo)),.001)
stereo=stereo/max(peak/0.84,1)
path=Path(__file__).resolve().parent/'original_score.wav'
sf.write(path,stereo,SR,subtype='PCM_16')
print('Audio',path,stereo.shape,'peak',float(np.max(np.abs(stereo))),'RMS',float(np.sqrt(np.mean(stereo**2))))
