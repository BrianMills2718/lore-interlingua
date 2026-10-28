"""Reproducible offline high-definition film render. Run `python render.py`.
Requires Chromium/Playwright and FFmpeg; all art generated locally. No remote assets.
"""
from pathlib import Path
import base64,subprocess,time,sys,os
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent
FPS=24
DURATION=86
TOTAL=FPS*DURATION
VIDEO=R/'picture_only.mp4'
FINAL=R/'Gurdjieff_The_Sensitive_Earth_86s.mp4'
FF=['ffmpeg','-hide_banner','-loglevel','error','-y']
start=time.monotonic()
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu','--disable-background-timer-throttling'])
 page=browser.new_page(viewport={'width':1280,'height':790},device_scale_factor=1)
 errors=[]
 page.on('pageerror',lambda ex: errors.append(str(ex)))
 page.set_content((R/'film.html').read_text(),wait_until='load')
 page.locator('#play').click()
 page.wait_for_function('window.earthTextureLoaded?.()',timeout=15000)
 ff=subprocess.Popen(FF+['-threads','4','-f','image2pipe','-vcodec','mjpeg','-framerate',str(FPS),'-i','pipe:0','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart','-an',str(VIDEO)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
 try:
  for i in range(TOTAL):
   data=page.evaluate('(time) => {window.renderAt(time);return document.getElementById("film").toDataURL("image/jpeg",.90).split(",")[1]}',i/FPS)
   ff.stdin.write(base64.b64decode(data))
   if (i+1)%120==0:
    print(f'render {i+1}/{TOTAL} ({100*(i+1)/TOTAL:.0f}%) elapsed {time.monotonic()-start:.1f}s',flush=True)
  ff.stdin.close()
  ec=ff.wait()
  if ec:raise RuntimeError(f'ffmpeg encoding failed {ff.stderr.read().decode()}')
 finally:
  browser.close()
 if errors:raise RuntimeError('Browser exceptions: '+'; '.join(errors))
print('Video created',VIDEO,VIDEO.stat().st_size,flush=True)
subprocess.run(FF+['-i',str(VIDEO),'-i',str(R/'original_score.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-ar','44100','-shortest','-movflags','+faststart','-metadata','title=The Sensitive Earth | Gurdjieff via Ouspensky','-metadata','comment=Original animated visual interpretation; not astrophysics',str(FINAL)],check=True)
print('SUCCESS',FINAL,FINAL.stat().st_size,'total_s',time.monotonic()-start,flush=True)
