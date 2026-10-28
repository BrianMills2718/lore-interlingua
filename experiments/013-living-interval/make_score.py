"""Original, deterministic, 176-second ambient score. No sampled/copyrighted music.

Sound design follows the picture's increasing density of constraints as an artistic
metaphor. No note sequence or tempo asserts a fact about cosmological laws.
"""
from pathlib import Path
import numpy as np
from scipy.signal import butter, sosfilt
import soundfile as sf

SR=32000
DUR=176
r=np.random.default_rng(12027)
t=np.arange(SR*DUR,dtype=np.float32)/SR
left=np.zeros(t.shape,dtype=np.float32)
right=np.zeros(t.shape,dtype=np.float32)

def smooth(a,b):
    u=np.clip((t-a)/(b-a),0,1)
    return u*u*(3-2*u)
def envelop(a,b,fade=8):return smooth(a,a+fade)*(1-smooth(b-fade,b))

def pad(notes,a,b,amp=.30):
    env=envelop(a,b)*amp
    for i,fr in enumerate(notes):
        # Detuned low harmonics create a hovering, non-tuneful sound field.
        wave=np.sin(2*np.pi*(fr*.998)*t+i*.71)+.77*np.sin(2*np.pi*(fr*1.002)*t+i*.63+.8)
        wave+=.24*np.sin(2*np.pi*fr*2.002*t+i*.61)
        wave*=env*(.66+.34*np.cos(2*np.pi*(.026+i*.002)*t+i))/len(notes)*.18
        left[:]+=wave*(.67 if i%2 else .91)
        right[:]+=wave*(.91 if i%2 else .67)

# One long harmonic fabric with changing density, not a recognizably borrowed melody.
pad([55.0,82.41,110,164.81],0,60,.66)
pad([61.74,92.50,123.47,185.0,246.94],36,98,.68)
pad([65.41,98.0,146.83,196,293.66],82,156,.69)
pad([55.0,82.41,110,164.81,220.0],136,176,.66)
# Deep ground pitch that persists through all seven worlds.
left+=.022*np.sin(2*np.pi*41.2*t)*envelop(0,176)
right+=.022*np.sin(2*np.pi*41.31*t)*envelop(0,176)

noise=r.standard_normal(len(t)).astype(np.float32)
filtered=sosfilt(butter(3,580,fs=SR,output='sos'),noise).astype(np.float32)
filtered/=max(float(filtered.std()),1e-6)
air=envelop(0,176,5)*(.009+.004*np.sin(2*np.pi*.016*t)**2)
left+=filtered*air
right+=np.roll(filtered,1300)*air*.85

def bell(at,fr,amp=.025,decay=4,pan=.5):
    start=int(at*SR);end=min(len(t),start+int(9*SR))
    if start<0 or start>=end:return
    q=np.arange(end-start,dtype=np.float32)/SR
    attack=1-np.exp(-q*100)
    decay_env=np.exp(-q/decay)*attack
    tone=(np.sin(2*np.pi*fr*q)+.32*np.sin(2*np.pi*fr*2.008*q+.31)+.13*np.sin(2*np.pi*fr*3.92*q+.7))*decay_env*amp
    left[start:end]+=tone*np.sqrt(1-pan)
    right[start:end]+=tone*np.sqrt(pan)

# Metallic landmarks mark worlds, not literal ticking of 1/3/6/12/24/48/96 laws.
for at,fr,amp,pan in [(3,293.66,.017,.3),(11,220,.018,.71),(15,329.63,.023,.3),(22,261.63,.021,.7),
 (27,370,.023,.28),(34,440,.03,.75),(40,329.63,.025,.35),(47,493.88,.036,.65),
 (52,392,.029,.35),(60,587.33,.031,.68),(64,349.23,.033,.22),(73,523.25,.036,.7),
 (78,392,.035,.39),(86,440,.032,.74),(94,493.88,.04,.29),(99,659.25,.04,.7),
 (105,587.33,.028,.5),(110,392,.028,.3),(117,329.63,.03,.7),(120,220,.025,.55)]:bell(at,fr,amp,4.2,pan)

# Subtle time-like interference increases in density toward the end of the ray.
for at in np.arange(55,164,.79):
    density=np.clip((at-54)/110,0,1)
    if r.random()>.21+.62*density:continue
    st=int(at*SR);length=int(.45*SR)
    if st+length>len(t):continue
    q=np.arange(length,dtype=np.float32)/SR
    click=(r.standard_normal(length).astype(np.float32)*np.exp(-q*13)*.0008+np.sin(2*np.pi*(246.94+40*density)*q)*np.exp(-q*17)*.0035)
    left[st:st+length]+=click*(.55+.35*density)
    right[st:st+length]+=click*(.65+.35*density)

# End resumes the simpler fabric rather than climaxing in invented doctrine.
fade=1-smooth(170,176)
left*=fade;right*=fade
stereo=np.tanh(np.stack([left,right],axis=1)*2.4)
peak=float(np.max(np.abs(stereo)))
if peak>.87:stereo*=.87/peak
path=Path(__file__).parent/'original_score.wav'
sf.write(path,stereo,SR,subtype='PCM_16')
print('Original stereo score',path,stereo.shape,'peak',float(np.max(np.abs(stereo))),'rms',float(np.sqrt(np.mean(stereo**2))))
