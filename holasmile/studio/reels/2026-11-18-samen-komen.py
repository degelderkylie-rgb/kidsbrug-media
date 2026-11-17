import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from holasmile_motion import *

# Reel 18 nov: Vraag van een klant "Kunnen we ook samen komen?" -> duobehandeling. MET BEWEGING.
# Sfeerbeelden (Canva, AI) uit holasmile/sfeer-lokaal/ (niet in git). Geen klanten, geen resultaten: alleen sfeer.
# Beelden staan als kaart in het midden, tekst erboven en eronder: nooit tekst over gezichten. Elke tekst >= 2,5 s in beeld.
S = os.path.join(os.path.dirname(__file__), "..", "..", "sfeer-lokaal")


class Card:
    """Sfeerbeeld als afgeronde kaart (uitsnede box als fractie), met lichte zoom."""
    def __init__(self, path, box, w=900, h=800):
        im = Image.open(path).convert("RGB"); w0, h0 = im.size
        im = im.crop((int(box[0] * w0), int(box[1] * h0), int(box[2] * w0), int(box[3] * h0)))
        self.im = ImageOps.fit(im, (int(w * 1.12), int(h * 1.12)), Image.LANCZOS); self.w, self.h = w, h

    def get(self, zoom):
        z = max(1.0, min(1.12, zoom)); cw, ch = int(self.w * 1.12 / z), int(self.h * 1.12 / z)
        x0, y0 = (self.im.width - cw) // 2, (self.im.height - ch) // 2
        return self.im.crop((x0, y0, x0 + cw, y0 + ch)).resize((self.w, self.h), Image.LANCZOS)


WARM = Card(os.path.join(S, "canva-duo-warm.png"), (0.0, 0.22, 1.0, 0.75))
CLOSE = Card(os.path.join(S, "canva-duo-close.png"), (0.0, 0.25, 1.0, 0.78))


def photo(im, c, zoom, cy):
    place(im, c.get(zoom), W / 2, cy, r=40)
    d = ImageDraw.Draw(im)
    d.text((W / 2, cy + c.h / 2 + 34), "Sfeerbeeld", font=sans(24), fill=MUTED, anchor="mm")
    return d


def s1(t, p):  # haak: de vraag knalt erin, kaart schuift omhoog
    im, d = base()
    kicker(d, 200, "Vraag van een klant")
    f = serif_i(int(78 * pop(min(1, t / 0.3))))
    ctext(d, 300, "“Kunnen we ook\nsamen komen?”", f, maxw=900)
    k = ease(t / 0.6)
    d = photo(im, WARM, 1.0 + 0.10 * p, 1180 + (1 - k) * 150)
    twinkle(d, t, [(150, 260, 20), (930, 250, 16)]); wordmark(d); return im


def s2(t, p):  # antwoord
    im, d = base()
    big_text(d, 200, "Ja! Dat heet een\nduobehandeling.", 84, scale=pop(min(1, t / 0.3)))
    d = photo(im, CLOSE, 1.10 - 0.10 * p, 900)
    ctext(d, 1440, "Naast elkaar, samen onder\nde LED-lamp, in één afspraak.", serif(54, "SemiBold"), fill=GOLD_L)
    twinkle(d, t, [(140, 190, 18), (940, 210, 22)]); wordmark(d); return im


ITEMS = ["Met je moeder\nof dochter", "Met je beste\nvriendin", "Met je partner"]


def s3(t, p):  # voor wie, punten één voor één
    im, d = base()
    kicker(d, 260, "Samen stralen")
    big_text(d, 380, "Leuk om samen\nte doen:", 92, scale=pop(min(1, t / 0.3)))
    y = 720
    for i, it in enumerate(ITEMS):
        k = ease((t - 0.3 - i * 0.3) / 0.3)
        if k <= 0: break
        x = 170 - (1 - k) * 400
        d.ellipse((x, y + 10, x + 90, y + 100), outline=GOLD, width=4)
        d.text((x + 45, y + 55), str(i + 1), font=serif(46, "SemiBold"), fill=GOLD_L, anchor="mm")
        cwrap_text(d, x + 140, y, it, serif(64, "SemiBold"), maxw=700, gap=1.15)
        y += 250
    shade_guide(d, 1450, active=6, w=700, labels=False)
    twinkle(d, t, [(170, 300, 18), (910, 280, 24), (920, 1700, 14)]); wordmark(d); return im


scenes = [(3.0, s1), (3.0, s2), (3.8, s3), (3.8, cta_motion)]


def COVER():
    im, d = base()
    kicker(d, 300, "Vraag van een klant")
    ctext(d, 390, "“Kunnen we ook\nsamen komen?”", serif_i(84), maxw=900)
    d = photo(im, WARM, 1.04, 1150)
    wordmark(d); return im


if __name__ == "__main__":
    work = sys.argv[1]; out = sys.argv[2]; os.makedirs(work, exist_ok=True)
    COVER().save(out.replace(".mp4", "-cover.jpg") if out.endswith(".mp4") else f"{work}/cover.jpg", "JPEG", quality=90)
    if "--sheet" in sys.argv:
        still_sheet(scenes, [(0, 0.0), (0, 0.1), (0, 1), (1, 0.1), (1, 1), (2, 0.15), (2, 1), (3, 1)], f"{work}/sheet.png")
    else: render_motion(scenes, out, work)
