"""Bewegende reels voor Hola Smile (frame voor frame, 30 fps). Gebruikt de kleuren en fonts van holasmile_style.

render_motion(scenes, out): scenes = [(seconden, functie(t, p) -> Image), ...]
  t = seconden sinds begin scene, p = voortgang 0..1 in de scene.
"""
import sys, os, math, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from holasmile_style import *
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

FPS = 30


def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def pop(x): x = max(0.0, min(1.0, x)); return 1 + 0.18 * math.sin(math.pi * x) * (1 - x) if x < 1 else 1.0


class Photo:
    """Laadt een liggende foto één keer en maakt er beelden van."""
    def __init__(self, path):
        im = Image.open(path); im = ImageOps.exif_transpose(im).convert("RGB")
        self.im = im
        bg = ImageOps.fit(im, (W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(40))
        self.bg = ImageEnhance.Brightness(bg).enhance(0.35)

    def card(self, w, zoom=1.0):
        """Foto op breedte w, met lichte zoom (Ken Burns) vanuit het midden."""
        ar = self.im.height / self.im.width; h = int(w * ar)
        zw, zh = int(self.im.width / zoom), int(self.im.height / zoom)
        x0, y0 = (self.im.width - zw) // 2, (self.im.height - zh) // 2
        return self.im.crop((x0, y0, x0 + zw, y0 + zh)).resize((w, h), Image.LANCZOS)


def rounded(im, r=36):
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.size[0], im.size[1]), r, fill=255)
    return m


def place(canvas, im, cx, cy, r=36, border=GOLD, label=None):
    x, y = int(cx - im.width / 2), int(cy - im.height / 2)
    canvas.paste(im, (x, y), rounded(im, r))
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle((x, y, x + im.width, y + im.height), r, outline=border, width=5)
    if label:
        f = sans(34, "Medium"); tw = d.textlength(label, font=f) + 56
        d.rounded_rectangle((x + 28, y + 28, x + 28 + tw, y + 92), 32, fill=BG)
        d.text((x + 28 + tw / 2, y + 60), label, font=f, fill=GOLD_L, anchor="mm")
    return x, y


def big_text(d, y, text, size=96, fill=CREAM, scale=1.0, italic=False, maxw=920):
    f = (serif_i if italic else serif)(max(10, int(size * scale)), "SemiBold" if not italic else "Medium")
    return ctext(d, y, text, f, fill=fill, maxw=maxw)


def twinkle(d, t, pts):
    for i, (x, y, r) in enumerate(pts):
        s = 0.5 + 0.5 * math.sin(t * 6 + i * 1.7)
        if s > 0.15: sparkle(d, x, y, r * s)


def render_motion(scenes, out, workdir):
    os.makedirs(workdir, exist_ok=True)
    tmp = os.path.join(workdir, "video.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", tmp],
                         stdin=subprocess.PIPE)
    for dur, fn in scenes:
        n = int(round(dur * FPS))
        for i in range(n):
            p.stdin.write(fn(i / FPS, i / max(1, n - 1)).convert("RGB").tobytes())
    p.stdin.close(); p.wait()
    subprocess.run(f"ffmpeg -y -loglevel error -i {tmp} -f lavfi -i anullsrc=r=44100:cl=stereo -shortest "
                   f"-map 0:v -map 1:a -c:v copy -c:a aac -movflags +faststart {out}", shell=True, check=True)


def still_sheet(scenes, times, path):
    """Contactblad: per (scene-index, voortgang) een still."""
    s = Image.new("RGB", (300 * len(times), 533), "white")
    for i, (si, pr) in enumerate(times):
        dur, fn = scenes[si]
        s.paste(fn(pr * dur, pr).convert("RGB").resize((300, 533)), (i * 300, 0))
    s.save(path)


# ---------- Vaste bewegende afsluiter ----------
def cta_motion(t, p):
    im, d = base()
    d.text((W / 2, 420), "Hola Smile", font=serif(int(120 * pop(min(1, t / 0.35))), "SemiBold"), fill=CREAM, anchor="mm")
    d.text((W / 2, 535), "CLINIC · ZUNDERT", font=sans(30, "Medium"), fill=GOLD, anchor="mm")
    rule(d, 630)
    # kleurwaaier vult zich tab voor tab
    n = len(SHADES); w = 760; gap = 16; tw = (w - gap * (n - 1)) / n; x0 = W / 2 - w / 2
    for i, c in enumerate(SHADES):
        k = ease((t - 0.2 - i * 0.09) / 0.25)
        if k <= 0: continue
        x = x0 + i * (tw + gap); hh = 190 * k
        d.rounded_rectangle((x, 740 + 190 - hh, x + tw, 930), int(tw / 2), fill=c,
                            outline=GOLD_L if i == n - 1 else None, width=6 if i == n - 1 else 0)
    if t > 1.0:
        ctext(d, 1060, "Jouw stralende glimlach\nbegint met één afspraak.", serif(58, "SemiBold"))
    pulse = 1 + 0.03 * math.sin(t * 7) if t > 1.3 else 1
    if t > 1.3:
        bw, bh = 720 * pulse, 130 * pulse
        d.rounded_rectangle((W / 2 - bw / 2, 1405 - bh / 2, W / 2 + bw / 2, 1405 + bh / 2), 65, fill=GOLD)
        d.text((W / 2, 1405), "Boek via de link in bio", font=sans(44, "Medium"), fill=BG, anchor="mm")
        d.text((W / 2, 1550), "of stuur ons SMILE in een DM", font=sans(34), fill=CREAM, anchor="mm")
    twinkle(d, t, [(220, 330, 20), (860, 300, 26), (900, 1250, 16), (180, 1180, 14)])
    wordmark(d); return im
