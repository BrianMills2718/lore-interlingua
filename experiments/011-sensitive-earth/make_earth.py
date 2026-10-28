"""Generate an original painterly globe texture for the film, no external imagery."""
import numpy as np, cv2
from scipy.ndimage import gaussian_filter,map_coordinates
from pathlib import Path
from PIL import Image
N=620
rng=np.random.default_rng(5319)
Y,X=np.mgrid[:N,:N].astype(np.float32)
rr=np.sqrt((X-310)**2+(Y-310)**2);disk=rr<=231

def noise(sigma):
    x=rng.normal(size=(N,N)).astype(np.float32)
    x=gaussian_filter(x,sigma,mode='reflect')
    x=x/np.std(x)
    return x

warpX=22*noise(31)+7*noise(11)+2*noise(4)
warpY=19*noise(39)+9*noise(14)+2*noise(5)
coords=np.array([np.clip(Y+warpY,0,N-1),np.clip(X+warpX,0,N-1)])
land=np.zeros((N,N),np.float32)
polys=[[(121,202),(164,167),(230,145),(298,164),(326,206),(273,263),(241,313),(190,295),(153,250)],
[(305,117),(361,124),(417,157),(458,204),(449,279),(416,306),(409,367),(374,391),(331,334),(335,271),(289,206)],
[(173,338),(213,322),(289,337),(308,386),(270,444),(227,502),(179,474),(151,414)],
[(399,383),(464,382),(507,424),(506,472),(455,510),(401,488)]]
for poly in polys: cv2.fillPoly(land,[np.array(poly,dtype=np.int32)],1)
land=map_coordinates(land,coords,order=1,mode='nearest')
land=gaussian_filter(land,2)
coastNoise=noise(6)*.16+noise(16)*.10+noise(2)*.07
landMask=np.clip((land+coastNoise-.48)*5,0,1)
# relief: water deep blue; green-grey olive land with gold topography
h=noise(31)*.13+noise(9)*.05+noise(2)*.018
sea=np.stack([19+10*h+5*noise(60),56+28*h,79+27*h],axis=-1)
forest=noise(36)*.6+noise(12)*.3+noise(4)*.14
ter=np.stack([77+26*forest,110+25*forest,78+21*forest],axis=-1)
ter += np.maximum(0,noise(19)-.55)[...,None]*np.array([19,10,1])
col=sea*(1-landMask[...,None])+ter*landMask[...,None]
coast=np.exp(-np.abs(land+coastNoise-.5)*23)*disk
col+=coast[...,None]*np.array([35,23,10])
# cloud fields, not an additional metaphysical layer
cloud=np.clip((noise(18)+.5*noise(7)-1.7)*.13,0,.20)
col=col*(1-cloud[...,None])+np.array([188,204,188])*cloud[...,None]
# spherical relief and edge shading
u=(X-310)/231;v=(Y-310)/231
r2=np.clip(u*u+v*v,0,1)
edge=np.sqrt(np.clip(1-r2,0,1))
shading=(.65+.3*edge+.15*(-.6*u-.8*v))
shading=np.clip(shading,.18,1.1)
col*=shading[...,None]
alpha=(disk*255).astype('uint8')
arr=np.dstack([np.uint8(np.clip(col,0,255)),alpha])
Image.fromarray(arr,'RGBA').save(Path(__file__).resolve().parent/'earth_surface.png')
print('wrote',Path(__file__).resolve().parent/'earth_surface.png')
