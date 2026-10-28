"""Render the 16-second, subtitle-only semantic-parsimony cut.

Requires Playwright + local Chromium (/usr/bin/chromium) and ffmpeg.
No speech synthesis or internet connection is used.
"""
from pathlib import Path
import base64
import subprocess
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
frames = HERE / "silent_frames"
frames.mkdir(exist_ok=True)
with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True, executable_path="/usr/bin/chromium",
        args=["--no-sandbox", "--disable-dev-shm-usage"])
    page = browser.new_page(viewport={"width": 1024, "height": 650})
    exceptions = []
    page.on("pageerror", lambda exc: exceptions.append(str(exc)))
    page.set_content((HERE / "index.html").read_text(), wait_until="domcontentloaded")
    assert not page.locator("#paths").is_checked()
    assert page.locator("#captions").is_checked()
    page.locator("#key").check()
    assert page.locator("#researchKey").is_visible()
    page.locator("#key").uncheck()
    assert not page.locator("#researchKey").is_visible()
    page.locator("#play").click()
    for i in range(192):
        frame64 = page.evaluate(
            't => {window.renderAt(t); return document.getElementById("scene").toDataURL("image/png").split(",")[1]}',
            i / 12)
        (frames / f"{i:04}.png").write_bytes(base64.b64decode(frame64))
    browser.close()
    if exceptions:
        raise RuntimeError("Browser errors: " + "; ".join(exceptions))
subprocess.run([
    "ffmpeg", "-y", "-v", "error", "-framerate", "12",
    "-i", str(frames / "%04d.png"),
    "-c:v", "libx264", "-crf", "25", "-pix_fmt", "yuv420p",
    "-movflags", "+faststart", "-an",
    str(HERE / "subtitled_silent.mp4")], check=True)
