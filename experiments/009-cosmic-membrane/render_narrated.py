"""Render Experiment 009 via local Chromium's Canvas and ffmpeg.

Dependencies: playwright, Chromium and ffmpeg. The offline scratch narration
can be generated with espeak; replace it with a recorded voice for production.
"""
from pathlib import Path
import base64
import subprocess
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
FRAMES = ROOT / "frames"
FRAMES.mkdir(exist_ok=True)
VOICE = ROOT / "narration.wav"
SCRIPT = ("In Gurdjieff's cosmology, life forms Earth's sensitive membrane. "
          "Planetary influences pass through living things toward Earth. "
          "Yet life also radiates outward. The Sun, planets, and Moon receive "
          "different kinds of influences from this living world.")

if not VOICE.exists():
    subprocess.run(["espeak", "-v", "en-us", "-s", "150", "-w", str(VOICE), SCRIPT], check=True)
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path="/usr/bin/chromium",
                                args=["--no-sandbox", "--disable-dev-shm-usage"])
    page = browser.new_page(viewport={"width": 1024, "height": 650})
    page.set_content((ROOT / "index.html").read_text(), wait_until="domcontentloaded")
    page.evaluate("() => document.getElementById('play').click()")
    for frame in range(16 * 12):
        b64 = page.evaluate("""time => {
            window.renderAt(time);
            return document.getElementById("scene").toDataURL("image/png").split(",")[1];
        }""", frame / 12)
        (FRAMES / f"{frame:04}.png").write_bytes(base64.b64decode(b64))
    browser.close()

subprocess.run([
    "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
    "-framerate", "12", "-i", str(FRAMES / "%04d.png"), "-i", str(VOICE),
    "-filter_complex", "[1:a]atempo=1.15,apad=pad_dur=16[a]",
    "-map", "0:v", "-map", "[a]", "-t", "16",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "24",
    "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
    str(ROOT / "narrated_preview.mp4"),
], check=True)
