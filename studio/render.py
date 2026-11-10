"""Render a reel HTML to MP4 (1080x1920, 30fps) or grab preview stills.
usage: render.py page.html out.mp4            -> full video
       render.py page.html --stills 1.5,5,12 -> JPEG stills next to page
"""
import sys, subprocess, os, pathlib
from playwright.sync_api import sync_playwright

page_path = pathlib.Path(sys.argv[1]).resolve()
FPS = 30

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--force-color-profile=srgb"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
    pg.goto(page_path.as_uri())
    pg.evaluate("document.fonts.ready")
    dur = pg.evaluate("window.REEL_DURATION")
    if sys.argv[2] == "--stills":
        for ts in sys.argv[3].split(","):
            pg.evaluate(f"renderAt({ts})")
            pg.screenshot(path=str(page_path.with_name(f"{page_path.stem}_{ts}.jpg")), type="jpeg", quality=92)
    else:
        out = sys.argv[2]; tmp = out + ".part.mp4"
        ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS),
            "-c:v", "mjpeg", "-i", "-", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
            "-shortest", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", tmp], stdin=subprocess.PIPE)
        n = int(round(dur * FPS))
        for i in range(n):
            pg.evaluate(f"renderAt({i / FPS})")
            ff.stdin.write(pg.screenshot(type="jpeg", quality=92))
        ff.stdin.close()
        if ff.wait() == 0:
            os.replace(tmp, out)
            print("ok", out, n, "frames")
    b.close()
