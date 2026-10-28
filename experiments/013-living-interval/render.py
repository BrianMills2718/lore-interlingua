"""Render the completed 176s film from its offline canvas, plus original stereo sound.

Requires installed playwright, Chromium (/usr/bin/chromium) and ffmpeg. Uses an
MJPEG pipe to avoid writing thousands of individual frame files. Frame time is
explicitly set, making output reproducible rather than wall-clock-dependent.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import base64,subprocess,time,os

ROOT=Path(__file__).resolve().parent
FPS=24
DURATION=176
TOTAL=FPS*DURATION
FF=['ffmpeg','-hide_banner','-loglevel','error','-y']
VIDEO=ROOT/'picture_only.mp4'
FINAL=ROOT/'Gurdjieff_The_Living_Interval_176s.mp4'
start=time.monotonic()
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu','--disable-background-timer-throttling'])
    page=b.new_page(viewport={'width':1280,'height':790},device_scale_factor=1)
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content((ROOT/'film.html').read_text(encoding='utf-8'),wait_until='load')
    page.locator('#play').click()
    page.wait_for_function('window.textureReady?.()',timeout=18000)
    ff=subprocess.Popen(FF+['-threads','3','-f','image2pipe','-vcodec','mjpeg','-framerate',str(FPS),'-i','pipe:0',
     '-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart','-an',str(VIDEO)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for i in range(TOTAL):
            d=page.evaluate('(t)=>{window.renderAt(t);return document.getElementById("film").toDataURL("image/jpeg",.88).split(",")[1]}',i/FPS)
            ff.stdin.write(base64.b64decode(d))
            if (i+1)%240==0:print(f'frame {i+1}/{TOTAL} | {100*(i+1)/TOTAL:.1f}% | {time.monotonic()-start:.1f}s',flush=True)
        ff.stdin.close()
        code=ff.wait(timeout=90)
        if code:raise RuntimeError(ff.stderr.read().decode()[:2500])
    finally:b.close()
    if errors:raise RuntimeError('Browser errors: '+ '; '.join(errors))
print('Picture encoded',VIDEO.stat().st_size,'bytes; time',time.monotonic()-start,flush=True)
subprocess.run(FF+['-i',str(VIDEO),'-i',str(ROOT/'original_score.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','160k','-ar','32000','-shortest','-movflags','+faststart','-metadata','title=The Living Interval — Gurdjieff via Ouspensky','-metadata','comment=Hierarchy, triadic forces, cosmic octave and organic mediation within one artist-directed world; not empirical astrophysics',str(FINAL)],check=True)
print('FINAL',FINAL,FINAL.stat().st_size,'bytes', 'elapsed',round(time.monotonic()-start,1),flush=True)
