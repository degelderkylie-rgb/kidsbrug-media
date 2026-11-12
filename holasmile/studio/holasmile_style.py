"""Hola Smile Clinic reel- en carrousel-huisstijl.

Donker (bijna zwart, warm), goud, crème tekst, Lora (serif) voor koppen, Poppins voor kleine tekst.
Vaste herkenning: de goudkleurige kleurwaaier (shade guide) van geel naar wit, dunne gouden lijnen, kleine sparkles,
woordmerk "Hola Smile Clinic" onderaan. Zachte fades tussen stilstaande beelden.

Gebruik in een reel-script:
    import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    from holasmile_style import *
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import subprocess, os, math

W, H = 1080, 1920
BG = (20, 17, 14); BG2 = (32, 27, 22); CARD = (38, 32, 26)
GOLD = (201, 163, 92); GOLD_L = (228, 199, 140); CREAM = (245, 236, 220); MUTED = (170, 156, 136)
RED = (196, 96, 80); OK = (150, 178, 120)
GF = "/usr/share/fonts/truetype/google-fonts/"
DJ = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
# kleurwaaier: van geel/getint naar stralend wit
SHADES = [(196, 160, 96), (210, 180, 120), (222, 198, 146), (232, 214, 172), (240, 228, 198), (247, 241, 226), (253, 251, 245)]


def serif(sz, w="Medium"):
    f = ImageFont.truetype(GF + "Lora-Variable.ttf", sz)
    try: f.set_variation_by_name(w)
    except Exception: pass
    return f


def serif_i(sz, w="Medium"):
    f = ImageFont.truetype(GF + "Lora-Italic-Variable.ttf", sz)
    try: f.set_variation_by_name(w)
    except Exception: pass
    return f


def sans(sz, w="Regular"):
    return ImageFont.truetype(GF + f"Poppins-{w}.ttf", sz)


def _glow(im, w, h):
    """Zachte warme gloed in het midden, zodat het donker niet plat oogt."""
    g = Image.new("RGBA", (w, h), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.ellipse((w * 0.05, h * 0.18, w * 0.95, h * 0.72), fill=(120, 90, 50, 46))
    g = g.filter(ImageFilter.GaussianBlur(160)); im.paste(g, (0, 0), g)


def base(w=W, h=H, frame=True):
    im = Image.new("RGB", (w, h), BG); _glow(im, w, h)
    d = ImageDraw.Draw(im)
    if frame: d.rounded_rectangle((40, 40, w - 40, h - 40), 36, outline=(70, 58, 40), width=2)
    return im, d


def wrap(d, text, font, maxw):
    out = []
    for para in text.split("\n"):
        line = ""
        for w in para.split():
            t = (line + " " + w).strip()
            if d.textlength(t, font=font) <= maxw: line = t
            else: out.append(line); line = w
        out.append(line)
    return out


def ctext(d, y, text, font, fill=CREAM, maxw=880, gap=1.22, cx=W / 2):
    lines = wrap(d, text, font, maxw); lh = font.size * gap
    for i, l in enumerate(lines): d.text((cx, y + i * lh), l, font=font, fill=fill, anchor="ma")
    return y + len(lines) * lh


def sparkle(d, x, y, r=22, fill=GOLD_L):
    """Vierpuntige ster."""
    pts = []
    for i in range(8):
        a = math.pi / 4 * i - math.pi / 2; rr = r if i % 2 == 0 else r * 0.28
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    d.polygon(pts, fill=fill)


def rule(d, y, w=220, cx=W / 2):
    d.line((cx - w / 2, y, cx - 18, y), fill=GOLD, width=2); d.line((cx + 18, y, cx + w / 2, y), fill=GOLD, width=2)
    sparkle(d, cx, y, 10)


def kicker(d, y, text, cx=W / 2):
    f = sans(28, "Medium"); t = text.upper(); tw = d.textlength(t, font=f) + 70
    d.rounded_rectangle((cx - tw / 2, y, cx + tw / 2, y + 64), 32, outline=GOLD, width=2)
    d.text((cx, y + 33), t, font=f, fill=GOLD_L, anchor="mm")
    return y + 64


def wordmark(d, y=1810, cx=W / 2):
    d.text((cx, y), "Hola Smile Clinic", font=serif(40), fill=GOLD, anchor="mm")
    d.text((cx, y + 44), "ZUNDERT", font=sans(20, "Medium"), fill=MUTED, anchor="mm")


def shade_guide(d, y, active=None, w=820, cx=W / 2, labels=True):
    """De kleurwaaier: 7 tabs van geel naar wit. active=index -> gouden rand + pijl eronder."""
    n = len(SHADES); gap = 16; tw = (w - gap * (n - 1)) / n; x0 = cx - w / 2
    for i, c in enumerate(SHADES):
        x = x0 + i * (tw + gap)
        d.rounded_rectangle((x, y, x + tw, y + 190), int(tw / 2), fill=c,
                            outline=GOLD_L if i == active else None, width=6 if i == active else 0)
        if labels: d.text((x + tw / 2, y + 225), f"{n - i}", font=sans(22, "Medium"), fill=MUTED, anchor="mm")
    if active is not None:
        x = x0 + active * (tw + gap) + tw / 2
        d.polygon([(x - 16, y + 270), (x + 16, y + 270), (x, y + 248)], fill=GOLD_L)
    return y + 290


def stamp(d, y, text, ok=False, cx=W / 2):
    """Stempel MYTHE / FEIT."""
    f = serif(92, "Bold"); col = OK if ok else RED; tw = d.textlength(text, font=f) + 90
    d.rounded_rectangle((cx - tw / 2, y, cx + tw / 2, y + 150), 24, outline=col, width=7)
    d.text((cx, y + 78), text, font=f, fill=col, anchor="mm")
    return y + 150


def card(d, box, fill=CARD, r=34, outline=(84, 70, 48)):
    d.rounded_rectangle(box, r, fill=fill, outline=outline, width=2)


def quote_card(d, y, text, label=None, maxw=780):
    """Kaartje met een vraag of uitspraak (bv. 'Doet het pijn?'), gecentreerd."""
    f = serif_i(54); lines = wrap(d, text, f, maxw - 100); lh = f.size * 1.3
    h = int(80 + lh * len(lines) + (50 if label else 0)); x0 = (W - maxw) / 2
    card(d, (x0, y, x0 + maxw, y + h))
    yy = y + 40
    if label: d.text((x0 + 50, yy + 10), label.upper(), font=sans(22, "Medium"), fill=GOLD, anchor="lm"); yy += 50
    for i, l in enumerate(lines): d.text((W / 2, yy + i * lh), l, font=f, fill=CREAM, anchor="ma")
    return y + h


def listing(d, y, items, numbered=True, x=150, maxw=780):
    """Genummerde (of vinkjes-)lijst met gouden cirkels."""
    for i, t in enumerate(items):
        f = serif(50); lines = wrap(d, t, f, maxw - 130); h = max(110, int(40 + len(lines) * f.size * 1.25))
        d.ellipse((x, y + h / 2 - 45, x + 90, y + h / 2 + 45), outline=GOLD, width=3)
        if numbered: d.text((x + 45, y + h / 2), str(i + 1), font=serif(46, "SemiBold"), fill=GOLD_L, anchor="mm")
        else: d.text((x + 45, y + h / 2), "✓", font=ImageFont.truetype(DJ, 40), fill=GOLD_L, anchor="mm")
        ty = y + h / 2 - (len(lines) * f.size * 1.25) / 2
        for j, l in enumerate(lines): d.text((x + 130, ty + j * f.size * 1.25), l, font=f, fill=CREAM, anchor="la")
        y += h + 40
    return y


def fit_photo(path, box_w, box_h):
    im = Image.open(path); im = ImageOps.exif_transpose(im).convert("RGB")
    return ImageOps.fit(im, (box_w, box_h), Image.LANCZOS, centering=(0.5, 0.5))


def photo_frame(im, path, box, label=None, r=40):
    """Foto (bv. voor of na) in een afgeronde gouden lijst, optioneel met label VOOR/NA."""
    x0, y0, x1, y1 = [int(v) for v in box]
    ph = fit_photo(path, x1 - x0, y1 - y0)
    m = Image.new("L", ph.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, ph.size[0], ph.size[1]), r, fill=255)
    im.paste(ph, (x0, y0), m)
    d = ImageDraw.Draw(im); d.rounded_rectangle((x0, y0, x1, y1), r, outline=GOLD, width=4)
    if label:
        f = sans(30, "Medium"); tw = d.textlength(label, font=f) + 50
        d.rounded_rectangle((x0 + 30, y0 + 30, x0 + 30 + tw, y0 + 90), 30, fill=BG)
        d.text((x0 + 30 + tw / 2, y0 + 60), label, font=f, fill=GOLD_L, anchor="mm")
    return d


def cta():
    """Vaste afsluiter."""
    im, d = base()
    for x, y, r in [(250, 330, 18), (830, 300, 26), (900, 520, 14)]: sparkle(d, x, y, r)
    d.text((W / 2, 430), "Hola Smile", font=serif(120, "SemiBold"), fill=CREAM, anchor="mm")
    d.text((W / 2, 545), "CLINIC · ZUNDERT", font=sans(30, "Medium"), fill=GOLD, anchor="mm")
    rule(d, 640)
    shade_guide(d, 740, active=6, w=760, labels=False)
    ctext(d, 1080, "Een stralende glimlach\nin 40 minuten.", serif(62, "SemiBold"))
    d.rounded_rectangle((180, 1340, 900, 1470), 65, fill=GOLD)
    d.text((W / 2, 1405), "Boek via de link in bio", font=sans(44, "Medium"), fill=BG, anchor="mm")
    d.text((W / 2, 1550), "of stuur ons SMILE in een DM", font=sans(34), fill=CREAM, anchor="mm")
    wordmark(d)
    return im


def cover(title, sub=None, kick=None, shade=None):
    """Omslagfoto voor het Instagram-raster: alles binnen het middelste 3:4-vlak (y 240-1680)."""
    im, d = base()
    y = 420
    if kick: y = kicker(d, y, kick) + 60
    y = ctext(d, y, title, serif(100, "SemiBold"), maxw=880)
    if sub: y = ctext(d, y + 30, sub, serif_i(56), fill=GOLD_L, maxw=860)
    if shade is not None: shade_guide(d, max(y + 100, 1080), active=shade, w=760, labels=False)
    for x, yy, r in [(170, 330, 20), (900, 360, 14)]: sparkle(d, x, yy, r)
    wordmark(d, y=1600)
    return im


def save_cover(im, path):
    im.save(path, "JPEG", quality=90)


def save_frames(frames, outdir):
    os.makedirs(outdir, exist_ok=True)
    for k, f in frames.items(): f().save(f"{outdir}/{k}.png")


def contact_sheet(outdir, keys, path):
    s = Image.new("RGB", (360 * len(keys), 640), "white")
    for i, k in enumerate(keys): s.paste(Image.open(f"{outdir}/{k}.png").resize((360, 640)), (i * 360, 0))
    s.save(path)


def render_reel(scenes, framedir, partsdir, out, X=0.25, F=0.3):
    """scenes: [(naam, [(frame, seconden), ...]), ...]. Zachte fade tussen frames, fade in/uit naar donker per scene."""
    BGC = "0x14110E"; os.makedirs(partsdir, exist_ok=True)
    for name, states in scenes:
        inp, fc = [], []
        for i, (k, dur) in enumerate(states):
            inp += ["-framerate", "30", "-i", f"{framedir}/{k}.png"]
            L = dur + (X if i < len(states) - 1 else 0)
            fc.append(f"[{i}]format=yuv420p,loop=-1:1,trim=duration={L},setpts=PTS-STARTPTS,fps=30[s{i}]")
        cur, off = "s0", 0
        for i in range(1, len(states)):
            off += states[i - 1][1]
            fc.append(f"[{cur}][s{i}]xfade=transition=fade:duration={X}:offset={off}[x{i}]"); cur = f"x{i}"
        total = sum(d for _, d in states)
        fc.append(f"[{cur}]fade=t=in:st=0:d={F}:color={BGC},fade=t=out:st={total-F}:d={F}:color={BGC},trim=duration={total}[v]")
        tmp = f"{partsdir}/tmp_{name}.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inp, "-filter_complex", ";".join(fc), "-map", "[v]", "-r", "30",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", tmp], check=True)
        os.rename(tmp, f"{partsdir}/{name}.mp4")
    lst = f"{partsdir}/list.txt"
    open(lst, "w").write("".join(f"file '{os.path.abspath(partsdir)}/{n}.mp4'\n" for n, _ in scenes))
    tmp = out + ".tmp.mp4"
    subprocess.run(f"ffmpeg -y -loglevel error -f concat -safe 0 -i {lst} -c copy {partsdir}/joined.mp4 && "
                   f"ffmpeg -y -loglevel error -i {partsdir}/joined.mp4 -f lavfi -i anullsrc=r=44100:cl=stereo -shortest "
                   f"-map 0:v -map 1:a -c:v copy -c:a aac -movflags +faststart {tmp}", shell=True, check=True)
    os.replace(tmp, out)


# ---------------- Carrousels (staand 4:5, 1080x1350) ----------------
CW, CH = 1080, 1350


def cbase():
    return base(CW, CH)


def cwrap_text(d, x, y, text, font, fill=CREAM, maxw=820, gap=1.3):
    lines = wrap(d, text, font, maxw); lh = font.size * gap
    for i, l in enumerate(lines): d.text((x, y + i * lh), l, font=font, fill=fill, anchor="la")
    return y + len(lines) * lh


def cfooter(d, n, total):
    d.text((120, CH - 100), "Hola Smile Clinic", font=serif(32), fill=GOLD, anchor="lm")
    d.text((CW - 120, CH - 100), f"{n}/{total}", font=sans(26, "Medium"), fill=MUTED, anchor="rm")


def slide_cover(title, sub=None, kick=None, total=6):
    im, d = cbase()
    y = 300
    if kick: y = kicker(d, y, kick, cx=CW / 2) + 70
    y = ctext(d, y, title, serif(90, "SemiBold"), maxw=860, cx=CW / 2)
    if sub: ctext(d, y + 30, sub, serif_i(50), fill=GOLD_L, maxw=820, cx=CW / 2)
    sparkle(d, 180, 230, 18); sparkle(d, 900, 260, 12)
    d.text((CW / 2, CH - 210), "Swipe  ›", font=sans(30, "Medium"), fill=MUTED, anchor="mm")
    cfooter(d, 1, total); return im


def slide_point(n, total, num, title, body):
    """Punt met nummer (of vinkje bij num=None) in een gouden cirkel, kop en uitleg, verticaal gecentreerd."""
    im, d = cbase()
    tf, bf = serif(70, "SemiBold"), sans(40)
    tl, bl = wrap(d, title, tf, 820), wrap(d, body, bf, 820)
    h = 120 + 60 + len(tl) * tf.size * 1.18 + 36 + len(bl) * bf.size * 1.45
    y = max(140, (CH - 120 - h) / 2)
    d.ellipse((120, y, 240, y + 120), outline=GOLD, width=4)
    if num is None: d.text((180, y + 60), "✓", font=ImageFont.truetype(DJ, 56), fill=GOLD_L, anchor="mm")
    else: d.text((180, y + 60), str(num), font=serif(64, "SemiBold"), fill=GOLD_L, anchor="mm")
    y = cwrap_text(d, 120, y + 180, title, tf, maxw=820, gap=1.18)
    cwrap_text(d, 120, y + 36, body, bf, fill=MUTED, maxw=820, gap=1.45)
    cfooter(d, n, total); return im


def slide_closing(n, total, line):
    im, d = cbase()
    ctext(d, 200, line, serif(66, "SemiBold"), maxw=860, cx=CW / 2)
    shade_guide(d, 520, active=6, w=700, cx=CW / 2, labels=False)
    d.rounded_rectangle((200, 900, 880, 1020), 60, fill=GOLD)
    d.text((CW / 2, 960), "Boek via de link in bio", font=sans(40, "Medium"), fill=BG, anchor="mm")
    d.text((CW / 2, 1090), "of stuur ons SMILE in een DM", font=sans(32), fill=CREAM, anchor="mm")
    cfooter(d, n, total); return im


def save_carousel(slides, outprefix):
    paths = []
    for i, f in enumerate(slides, 1):
        p = f"{outprefix}-{i}.jpg"; f().save(p, "JPEG", quality=90); paths.append(p)
    return paths


def carousel_sheet(paths, path):
    s = Image.new("RGB", (324 * len(paths), 405), "white")
    for i, p in enumerate(paths): s.paste(Image.open(p).resize((324, 405)), (i * 324, 0))
    s.save(path)
