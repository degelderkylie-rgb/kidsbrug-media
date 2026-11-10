"""KidsBrug reel-huisstijl (dezelfde stijl als de eerste reels: 47 berichtjes, Ik heb wél gebeld, Dezelfde vraag).

Warme crème achtergrond, Lora (serif) voor koppen, Poppins voor appjes en labels, bruin/roze/salie/goud accenten,
gecentreerde tekst, telefoon-mockup met app-scherm, woordmerk "KidsBrug" onderaan, zachte fades tussen stilstaande beelden.

Gebruik in een reel-script:
    import sys; sys.path.insert(0, "<repo>/studio")
    from kidsbrug_style import *
    def sA(n): im,d=base(); ...; wordmark(d); return im
    save_frames({"A1": lambda: sA(1), ...}, "frames")
    render_reel([("1",[("A1",1.0),("A2",1.7)]), ...], "frames", "parts", "reels/kidsbrug-YYYY-MM-DD-onderwerp.mp4")
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import subprocess, os

W, H = 1080, 1920
BG = (245, 239, 230); BROWN = (139, 115, 85); DARK = (59, 42, 30); MUTED = (140, 125, 110)
WHITE = (255, 253, 250); ROSE = (233, 201, 193); SAGE = (201, 213, 192); GOLD = (232, 213, 160)
ME_BUBBLE = (232, 220, 205); CHIP = (242, 234, 224)
GF = "/usr/share/fonts/truetype/google-fonts/"
CHK = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)


def serif(sz, w="Medium"):
    f = ImageFont.truetype(GF + "Lora-Variable.ttf", sz)
    try: f.set_variation_by_name(w)
    except Exception: pass
    return f


def sans(sz, w="Regular"):
    return ImageFont.truetype(GF + f"Poppins-{w}.ttf", sz)


def base():
    im = Image.new("RGB", (W, H), BG)
    return im, ImageDraw.Draw(im)


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


def ctext(d, y, text, font, fill=DARK, maxw=900, gap=1.22):
    lines = wrap(d, text, font, maxw); lh = font.size * gap
    for i, l in enumerate(lines):
        d.text((W / 2, y + i * lh), l, font=font, fill=fill, anchor="ma")
    return y + len(lines) * lh


def wordmark(d, y=1830):
    d.text((W / 2, y), "KidsBrug", font=serif(40), fill=BROWN, anchor="mm")


def card(d, box, fill=(250, 246, 240), r=26, outline=None):
    d.rounded_rectangle(box, r, fill=fill, outline=outline, width=2)


def phone(im, top=620, w=660, h=1140, title="Kalender"):
    """Telefoon-mockup. Geeft (draw, (x0,y0,x1,y1)) terug: het vrije vlak onder de titel."""
    x0 = (W - w) // 2; x1 = x0 + w; y1 = top + h
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle((x0 + 10, top + 30, x1 + 10, y1 + 30), 70, fill=(90, 70, 50, 70))
    sh = sh.filter(ImageFilter.GaussianBlur(28)); im.paste(sh, (0, 0), sh)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((x0, top, x1, y1), 72, fill=(40, 32, 26))
    sx0, sy0, sx1, sy1 = x0 + 18, top + 18, x1 - 18, y1 - 18
    d.rounded_rectangle((sx0, sy0, sx1, sy1), 56, fill=WHITE)
    d.rounded_rectangle((W / 2 - 80, sy0 + 18, W / 2 + 80, sy0 + 52), 17, fill=(40, 32, 26))
    d.text((sx0 + 40, sy0 + 95), "KidsBrug", font=serif(30), fill=BROWN, anchor="ls")
    d.text((sx0 + 40, sy0 + 165), title, font=serif(46, "SemiBold"), fill=DARK, anchor="ls")
    return d, (sx0 + 40, sy0 + 205, sx1 - 40, sy1 - 40)


def bubble(d, y, text, me, label=None, big=False, maxw=760):
    """Appje. me=True: rechts, beige. me=False: links, wit, met optioneel label ("Ex"). Lange tekst loopt door op 2 regels."""
    f = sans(40 if big else 34, "Medium")
    lines = wrap(d, text, f, maxw - 90)
    tw = max(d.textlength(l, font=f) for l in lines); w = int(tw + 90)
    lh = f.size * 1.4; top_pad = 48 if label else 0
    h = int(top_pad + 52 + lh * len(lines)) if (label or len(lines) > 1) else (110 if big else 100)
    x = W - 110 - w if me else 110
    d.rounded_rectangle((x, y, x + w, y + h), 40, fill=ME_BUBBLE if me else WHITE)
    if label:
        d.text((x + 45, y + 32), label, font=sans(24, "Medium"), fill=MUTED, anchor="lm")
    if label or len(lines) > 1:
        for i, l in enumerate(lines):
            d.text((x + 45, y + top_pad + 26 + lh * (i + 0.5)), l, font=f, fill=DARK, anchor="lm")
    else:
        d.text((x + 45, y + h / 2), text, font=f, fill=DARK, anchor="lm")
    return y + h + 30


def chip(d, x, y, text, fill=SAGE, size=22):
    f = sans(size, "Medium"); tw = d.textlength(text, font=f) + 36
    d.rounded_rectangle((x, y, x + tw, y + size + 18), (size + 18) // 2, fill=fill)
    d.text((x + 18, y + (size + 18) / 2), text, font=f, fill=DARK, anchor="lm")
    return x + tw


def checklist(d, title, items, closing, sub=None):
    ctext(d, 240, title, serif(84, "SemiBold"), maxw=900)
    y = 560
    for t in items:
        d.rounded_rectangle((180, y, 900, y + 140), 40, fill=WHITE)
        d.ellipse((215, y + 35, 285, y + 105), fill=SAGE)
        d.text((250, y + 70), "✓", font=CHK, fill=DARK, anchor="mm")
        d.text((320, y + 70), t, font=serif(54), fill=DARK, anchor="lm")
        y += 175
    ctext(d, y + 60, closing, serif(60, "SemiBold"), fill=BROWN)
    if sub: d.text((W / 2, y + 290), sub, font=sans(32), fill=MUTED, anchor="mm")
    wordmark(d)


def cta():
    """Vaste wachtlijst-afsluiter."""
    im, d = base()
    d.text((W / 2, 400), "KidsBrug", font=serif(110, "SemiBold"), fill=DARK, anchor="mm")
    ctext(d, 500, "Rust voor jou.\nRust voor je kind.", serif(52), fill=BROWN)
    card(d, (110, 760, 970, 1250), fill=WHITE, r=40)
    d.text((W / 2, 840), "BINNENKORT LIVE", font=sans(32, "Medium"), fill=BROWN, anchor="mm")
    d.text((W / 2, 950), "Schrijf je nu in", font=serif(84, "SemiBold"), fill=DARK, anchor="mm")
    d.text((W / 2, 1065), "De eerste 30 gezinnen krijgen", font=serif(46), fill=DARK, anchor="mm")
    d.text((W / 2, 1135), "6 maanden gratis", font=serif(56, "SemiBold"), fill=DARK, anchor="mm")
    d.rounded_rectangle((200, 1360, 880, 1480), 60, fill=BROWN)
    d.text((W / 2, 1420), "Link in bio", font=sans(48, "Medium"), fill=WHITE, anchor="mm")
    d.text((W / 2, 1560), "kidsbrug.nl · kidsbrug.be", font=sans(30), fill=MUTED, anchor="mm")
    return im


def save_frames(frames, outdir):
    os.makedirs(outdir, exist_ok=True)
    for k, f in frames.items(): f().save(f"{outdir}/{k}.png")


def contact_sheet(outdir, keys, path):
    s = Image.new("RGB", (360 * len(keys), 640), "white")
    for i, k in enumerate(keys): s.paste(Image.open(f"{outdir}/{k}.png").resize((360, 640)), (i * 360, 0))
    s.save(path)


def render_reel(scenes, framedir, partsdir, out, X=0.25, F=0.3):
    """scenes: [(naam, [(frame, seconden), ...]), ...]. Zachte fade tussen frames, fade in/uit naar crème per scene."""
    BGC = "0xF5EFE6"; os.makedirs(partsdir, exist_ok=True)
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


def cover(title, msgs, sub=None):
    """Omslagfoto (JPG) voor het Instagram-raster. Alles staat binnen het middelste 3:4-vlak (y 240-1680),
    want Instagram knipt de boven- en onderkant weg in het profielraster.
    msgs: [(tekst, me, label), ...] appjes onder de kop."""
    im, d = base()
    y = ctext(d, 400, title, serif(96, "SemiBold"), maxw=900)
    if sub: y = ctext(d, y + 20, sub, serif(56), fill=BROWN)
    y = max(y + 110, 900)
    for t, me, l in msgs: y = bubble(d, y, t, me, l, big=True)
    wordmark(d, y=1560)
    return im


def save_cover(im, path):
    im.save(path, "JPEG", quality=90)


# ---------------- Carrousels (staand 4:5, 1080x1350) ----------------
CW, CH = 1080, 1350


def cbase():
    im = Image.new("RGB", (CW, CH), BG)
    return im, ImageDraw.Draw(im)


def cwrap_text(d, x, y, text, font, fill=DARK, maxw=860, gap=1.3, anchor="la"):
    lines = wrap(d, text, font, maxw); lh = font.size * gap
    for i, l in enumerate(lines): d.text((x, y + i * lh), l, font=font, fill=fill, anchor=anchor)
    return y + len(lines) * lh


def cfooter(d, n, total):
    """Woordmerk links onder, paginateller rechts onder, en een swipe-hint op slide 1."""
    d.text((110, CH - 90), "KidsBrug", font=serif(34), fill=BROWN, anchor="lm")
    d.text((CW - 110, CH - 90), f"{n}/{total}", font=sans(26, "Medium"), fill=MUTED, anchor="rm")


def ccenter(d, y, text, font, fill=DARK, maxw=880, gap=1.22):
    lines = wrap(d, text, font, maxw); lh = font.size * gap
    for i, l in enumerate(lines): d.text((CW / 2, y + i * lh), l, font=font, fill=fill, anchor="ma")
    return y + len(lines) * lh


def slide_cover(title, sub=None, kicker=None, total=6):
    """Eerste slide: grote kop, die ook als omslag in het raster staat (alles binnen het middelste 3:4-vlak)."""
    im, d = cbase()
    y = 300
    if kicker:
        f = sans(28, "Medium"); tw = d.textlength(kicker.upper(), font=f) + 60
        d.rounded_rectangle((CW / 2 - tw / 2, y, CW / 2 + tw / 2, y + 64), 32, fill=ROSE)
        d.text((CW / 2, y + 32), kicker.upper(), font=f, fill=DARK, anchor="mm"); y += 120
    y = ccenter(d, y, title, serif(88, "SemiBold"), maxw=880)
    if sub: ccenter(d, y + 30, sub, serif(48), fill=BROWN, maxw=820)
    d.text((CW / 2, CH - 230), "Swipe", font=sans(30, "Medium"), fill=MUTED, anchor="mm")
    d.text((CW / 2, CH - 190), "›  ›  ›", font=sans(30, "Medium"), fill=MUTED, anchor="mm")
    cfooter(d, 1, total); return im


def slide_point(n, total, num, title, body, extra=None):
    """Tip of stap: nummer (of vinkje bij num=None) in een cirkel, kop, uitleg, optioneel een voorbeeld-kaartje.
    De inhoud staat verticaal gecentreerd."""
    im, d = cbase()
    tf, bf, ef = serif(76, "SemiBold"), sans(44), sans(38, "Medium")
    tl, bl = wrap(d, title, tf, 860), wrap(d, body, bf, 860)
    el = wrap(d, extra, ef, 760) if extra else []
    h = 130 + 50 + len(tl) * tf.size * 1.18 + 40 + len(bl) * bf.size * 1.45 + ((60 + 70 + len(el) * ef.size * 1.5) if el else 0)
    y = max(140, (CH - 130 - h) / 2)
    d.ellipse((110, y, 240, y + 130), fill=SAGE)
    if num is None: d.text((175, y + 65), "✓", font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64), fill=DARK, anchor="mm")
    else: d.text((175, y + 65), str(num), font=serif(70, "SemiBold"), fill=DARK, anchor="mm")
    y = cwrap_text(d, 110, y + 180, title, tf, maxw=860, gap=1.18)
    y = cwrap_text(d, 110, y + 40, body, bf, fill=MUTED, maxw=860, gap=1.45)
    if el:
        card(d, (110, y + 60, CW - 110, y + 60 + 70 + ef.size * 1.5 * len(el)), fill=WHITE, r=36)
        cwrap_text(d, 150, y + 95, extra, ef, fill=DARK, maxw=760, gap=1.5)
    cfooter(d, n, total); return im


def slide_phone(n, total, title, screen_title, draw_screen):
    """Slide met een (kleinere) telefoon. draw_screen(d, (x0,y0,x1,y1)) tekent het app-scherm."""
    im, d = cbase()
    ccenter(d, 120, title, serif(66, "SemiBold"), maxw=900)
    dd, box = phone(im, top=300, w=600, h=880, title=screen_title)
    draw_screen(dd, box)
    d = ImageDraw.Draw(im)
    cfooter(d, n, total); return im


def slide_closing(n, total, line):
    """Laatste slide: vaste afsluiter met wachtlijst."""
    im, d = cbase()
    ccenter(d, 190, line, serif(64, "SemiBold"), maxw=880)
    card(d, (110, 520, 970, 940), fill=WHITE, r=40)
    d.text((CW / 2, 590), "BINNENKORT LIVE", font=sans(30, "Medium"), fill=BROWN, anchor="mm")
    d.text((CW / 2, 690), "Schrijf je nu in", font=serif(76, "SemiBold"), fill=DARK, anchor="mm")
    d.text((CW / 2, 790), "De eerste 30 gezinnen krijgen", font=serif(42), fill=DARK, anchor="mm")
    d.text((CW / 2, 855), "6 maanden gratis", font=serif(52, "SemiBold"), fill=DARK, anchor="mm")
    d.rounded_rectangle((220, 1010, 860, 1120), 55, fill=BROWN)
    d.text((CW / 2, 1065), "Link in bio · reageer BRUG", font=sans(40, "Medium"), fill=WHITE, anchor="mm")
    cfooter(d, n, total); return im


def save_carousel(slides, outprefix):
    """slides: lijst van functies die een Image teruggeven. Schrijft outprefix-1.jpg ... -N.jpg en geeft de paden terug."""
    paths = []
    for i, f in enumerate(slides, 1):
        p = f"{outprefix}-{i}.jpg"; f().save(p, "JPEG", quality=90); paths.append(p)
    return paths


def carousel_sheet(paths, path):
    s = Image.new("RGB", (324 * len(paths), 405), "white")
    for i, p in enumerate(paths): s.paste(Image.open(p).resize((324, 405)), (i * 324, 0))
    s.save(path)
