import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from holasmile_motion import *

# Reeks: Mythe of feit, MET BEWEGING. Onderwerp: "tanden bleken is iets voor de zomer".
# Opbouw: stelling + stempel MYTHE -> sfeerbeeld lachend koppel (kerstlicht) -> momenten van december komen één voor één binnen
# -> kleurwaaier schuift naar licht -> afsluiter. Elke tekst minstens 2,5 s in beeld. Eén sfeerbeeld: post krijgt het AI-label.
S = os.path.join(os.path.dirname(__file__), "..", "..", "sfeer-lokaal")
KOPPEL = Fullbleed(os.path.join(S, "koppel-kerst.png"), (0.02, 0.0, 0.62, 1.0))
CLAIM = "Tanden bleken doe je\nvoor de zomer."
SP = [(170, 330, 22), (910, 360, 16), (900, 1500, 18), (160, 1450, 14)]


def shade_slider(d, y, pos, w=820, cx=W / 2):
    n = len(SHADES); gap = 16; tw = (w - gap * (n - 1)) / n; x0 = cx - w / 2
    for i, c in enumerate(SHADES):
        x = x0 + i * (tw + gap)
        d.rounded_rectangle((x, y, x + tw, y + 190), int(tw / 2), fill=c)
    x = x0 + pos * (tw + gap)
    d.rounded_rectangle((x - 6, y - 6, x + tw + 6, y + 196), int(tw / 2) + 6, outline=GOLD_L, width=6)
    mx = x + tw / 2
    d.polygon([(mx - 18, y + 250), (mx + 18, y + 250), (mx, y + 222)], fill=GOLD_L)


def s1(t, p):  # haak: stelling knalt erin, stempel MYTHE slaat erop
    im, d = base()
    kicker(d, 300, "Mythe of feit?")
    big_text(d, 470, CLAIM, 84, scale=pop(min(1, t / 0.3)), maxw=900)
    if t > 0.9:
        k = ease((t - 0.9) / 0.25); s = 1 + 1.2 * (1 - k)
        f = serif(int(110 * s), "Bold"); tw = d.textlength("MYTHE", font=f) + 100 * s; hh = 170 * s; cy = 1000
        d.rounded_rectangle((W / 2 - tw / 2, cy - hh / 2, W / 2 + tw / 2, cy + hh / 2), 26, outline=RED, width=8)
        d.text((W / 2, cy + 4), "MYTHE", font=f, fill=RED, anchor="mm")
        ctext(d, 1190, "Juist in december\nsta je op elke foto.", serif_i(62), fill=GOLD_L)
    twinkle(d, t, SP); wordmark(d); return im


def s2(t, p):  # sfeerbeeld, tekst onder de gezichten
    im = KOPPEL.frame(1.0 + 0.12 * p); d = ImageDraw.Draw(im)
    big_text(d, 1430, "Lachen doe je\nnu het meest.", 92, scale=pop(min(1, t / 0.35)))
    ai_note(d); return im


MOMENTS = ["Het kerstdiner", "De familiefoto", "Oud en nieuw"]


def s3(t, p):
    im, d = base()
    kicker(d, 280, "Denk maar aan")
    y = 480
    for i, it in enumerate(MOMENTS):
        st = 0.1 + i * 0.3
        if t <= st: break
        k = ease((t - st) / 0.3); x = 150 - (1 - k) * 500
        d.ellipse((x, y + 10, x + 90, y + 100), outline=GOLD, width=4)
        d.text((x + 45, y + 55), str(i + 1), font=serif(46, "SemiBold"), fill=GOLD_L, anchor="mm")
        d.text((x + 140, y + 55), it, font=serif(76, "SemiBold"), fill=CREAM, anchor="lm")
        y += 260
    if t > 0.8:
        ctext(d, 1340, "Dan wil je voluit lachen.", serif_i(60), fill=GOLD_L)
    twinkle(d, t, SP[2:]); wordmark(d); return im


def s4(t, p):  # kleurwaaier schuift van geel naar licht
    im, d = base()
    big_text(d, 280, "Lichter in\néén afspraak.", 100, scale=pop(min(1, t / 0.3)))
    shade_slider(d, 700, 0.5 + 3.5 * ease((t - 0.4) / 1.3))
    ctext(d, 1090, "Rondes van 20 minuten\nonder de LED-lamp.\nResultaat verschilt per persoon.", sans(48), fill=MUTED, maxw=920)
    twinkle(d, t, SP[:2]); wordmark(d); return im


scenes = [(3.6, s1), (2.8, s2), (3.2, s3), (3.4, s4), (3.0, cta_motion)]

COVER = lambda: cover("Tanden bleken,\nalleen in de zomer?", kick="Mythe of feit", shade=3)

if __name__ == "__main__":
    work = sys.argv[1]; out = sys.argv[2]
    COVER().save(out.replace(".mp4", "-cover.jpg") if out.endswith(".mp4") else f"{work}/cover.jpg", "JPEG", quality=90)
    if "--sheet" in sys.argv:
        os.makedirs(work, exist_ok=True)
        still_sheet(scenes, [(0, 0.0), (0, 0.15), (0, 1), (1, 0.1), (1, 1), (2, 0.2), (2, 1), (3, 0.2), (3, 1), (4, 1)], f"{work}/sheet.png")
    else: render_motion(scenes, out, work)
