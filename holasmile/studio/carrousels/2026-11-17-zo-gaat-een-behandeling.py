import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from holasmile_style import *

# Zo gaat een behandeling (reeks "Zo gaat een behandeling"), di 17 nov 12:30.
# Opbouw zoals koffie-tips-v2: volledige 4:5, grote beelden. Elke stap bovenaan een groot sfeerbeeld (label "Sfeerbeeld"),
# onderaan stapnummer + uitleg in grote letters. Omslag en afsluiter met groot echt voor/na-beeld (klant02).
# Sfeerbeelden (AI/Canva) staan niet in git: holasmile/sfeer-lokaal/. Post krijgt het AI-label.
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
FOTO = "klant02"
VOOR, NA = [os.path.join(ROOT, "fotos", f"{FOTO}-{k}.jpg") for k in ("voor", "na")]
S = lambda n: os.path.join(ROOT, "sfeer-lokaal", n)
T = 6
POINTS = [
    ("Even kennismaken", "We bekijken samen je tanden en kiezen het pakket dat bij jou past.", S("canva-duo-warm.png"), (0.0, 0.20, 1.0, 0.58)),
    ("Goed beschermd", "Je tandvlees wordt afgeschermd en je krijgt een nieuwe mondspreider, alleen voor jou.", S("canva-duo-close.png"), (0.0, 0.30, 1.0, 0.68)),
    ("Rondes van 20 minuten", "Onder de nieuwste LED-lamp, terwijl jij ontspant in een luxe massagestoel.", S("canva-groep.png"), (0.0, 0.40, 1.0, 0.78)),
    ("Tips voor thuis", "Je gaat naar huis met tips om je glimlach zo lang mogelijk te laten stralen.", S("vrouw-goud.png"), (0.49, 0.18, 1.0, 0.42)),
]
PH = 730  # hoogte fotovlak bovenaan


def top_photo(im, path, box, h=PH):
    """box = (x0, y0, x1, y1) als fractie van de foto; daarna passend gemaakt op CW x h."""
    ph = Image.open(path).convert("RGB"); W0, H0 = ph.size
    ph = ph.crop((int(box[0] * W0), int(box[1] * H0), int(box[2] * W0), int(box[3] * H0)))
    ph = ImageOps.fit(ph, (CW, h), Image.LANCZOS, centering=(0.5, 0.5))
    im.paste(ph, (0, 0))
    # zachte overgang naar donker
    g = Image.new("L", (1, 160)); [g.putpixel((0, i), int(255 * i / 159)) for i in range(160)]
    g = g.resize((CW, 160)); dark = Image.new("RGB", (CW, 160), BG); im.paste(dark, (0, h - 160), g)
    d = ImageDraw.Draw(im); f = sans(24, "Medium"); tw = d.textlength("Sfeerbeeld", font=f) + 36
    d.rounded_rectangle((CW - 40 - tw, 36, CW - 40, 80), 22, fill=BG)
    d.text((CW - 40 - tw / 2, 58), "Sfeerbeeld", font=f, fill=MUTED, anchor="mm")


def foot(d, n):
    d.text((80, CH - 60), "Hola Smile Clinic", font=serif(30), fill=GOLD, anchor="lm")
    d.text((CW - 80, CH - 60), f"{n}/{T}", font=sans(26, "Medium"), fill=MUTED, anchor="rm")


def s_cover():
    im = Image.new("RGB", (CW, CH), BG); d = ImageDraw.Draw(im)
    kicker(d, 50, "Stap voor stap", cx=CW / 2)
    ctext(d, 135, "Zo gaat bleken bij ons", serif(76, "SemiBold"), maxw=980, cx=CW / 2)
    w = 840; h = int(w * 608 / 1080); x = (CW - w) // 2
    photo_frame(im, VOOR, (x, 285, x + w, 285 + h), label="VOOR", r=30)
    photo_frame(im, NA, (x, 285 + h + 16, x + w, 285 + 2 * h + 16), label="NA", r=30); d = ImageDraw.Draw(im)
    d.text((CW / 2, CH - 60), "Alles in één afspraak  ·  Swipe  ›", font=sans(32, "Medium"), fill=GOLD_L, anchor="mm")
    return im


def s_point(n, num, title, body, path, box):
    im = Image.new("RGB", (CW, CH), BG); top_photo(im, path, box); d = ImageDraw.Draw(im)
    y = PH - 40
    d.ellipse((80, y, 200, y + 120), fill=BG, outline=GOLD, width=5)
    d.text((140, y + 60), str(num), font=serif(66, "SemiBold"), fill=GOLD_L, anchor="mm")
    d.text((230, y + 60), f"Stap {num}", font=sans(34, "Medium"), fill=GOLD, anchor="lm")
    y = cwrap_text(d, 80, y + 150, title, serif(78, "SemiBold"), maxw=920, gap=1.12)
    cwrap_text(d, 80, y + 20, body, sans(44), fill=MUTED, maxw=920, gap=1.4)
    foot(d, n); return im


def s_closing():
    im = Image.new("RGB", (CW, CH), BG); d = ImageDraw.Draw(im)
    ctext(d, 60, "Zin in een stralende lach?", serif(80, "SemiBold"), maxw=980, cx=CW / 2)
    ctext(d, 165, "Echt resultaat van een klant", serif_i(46), fill=GOLD_L, maxw=980, cx=CW / 2)
    w = 980; h = int(w * 608 / 1080); x = (CW - w) // 2
    photo_frame(im, NA, (x, 260, x + w, 260 + h), label="NA", r=30); d = ImageDraw.Draw(im)
    ctext(d, 260 + h + 22, "Echte klant · geen filter · resultaten verschillen per persoon", sans(28), fill=MUTED, cx=CW / 2)
    d.rounded_rectangle((170, 940, 910, 1060), 60, fill=GOLD)
    d.text((CW / 2, 1000), "Boek via de link in bio", font=sans(46, "Medium"), fill=BG, anchor="mm")
    d.text((CW / 2, 1120), "of stuur ons SMILE in een DM", font=sans(36), fill=CREAM, anchor="mm")
    foot(d, T); return im


slides = [s_cover] + [lambda i=i, p=p: s_point(i + 2, i + 1, *p) for i, p in enumerate(POINTS)] + [s_closing]

if __name__ == "__main__":
    paths = save_carousel(slides, sys.argv[1])
    if len(sys.argv) > 2: carousel_sheet(paths, sys.argv[2])
    print("\n".join(paths))
