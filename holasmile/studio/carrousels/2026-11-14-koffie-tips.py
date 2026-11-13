import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from holasmile_style import *

# Soort: Tips (bewaarwaardig). 6 slides: omslag, 4 punten, afsluiter. Nieuwe versie na feedback Kylie (12 nov):
# ALLE tekst binnen het middelste vierkant (x 130-950, y 135-1215) en een echt voor/na-beeld op omslag en afsluiter.
# De foto's staan NIET in git: haal ze privé uit het dashboard naar holasmile/fotos/ (zie STUDIO.md). Foto's nooit bewerken.
FOTO = "klant01"
HERE = os.path.join(os.path.dirname(__file__), "..", "..", "fotos")
VOOR, NA = os.path.join(HERE, f"{FOTO}-voor.jpg"), os.path.join(HERE, f"{FOTO}-na.jpg")
T = 6; X0, X1, Y0, Y1 = 130, 950, 135, 1215; MW = X1 - X0
POINTS = [
    ("Drink met een rietje", "Koude koffie of ijsthee? Met een rietje raakt minder kleur je tanden."),
    ("Spoel direct met water", "Een slok water na je koffie spoelt het meeste weg."),
    ("Niet meteen poetsen", "Wacht even na iets zuurs, zodat je glazuur tot rust komt."),
    ("Plan een opfrisser", "Drink je dagelijks koffie? Dan zie je verkleuring sneller terugkomen."),
]


def foot(d, n):
    d.text((X0, 1185), "Hola Smile Clinic", font=serif(28), fill=GOLD, anchor="lm")
    d.text((X1, 1185), f"{n}/{T}", font=sans(24, "Medium"), fill=MUTED, anchor="rm")


def pair(im, y, w, gap=20, side=False):
    """Voor/na naast of onder elkaar, liggend 16:9, ongewijzigd (alleen geschaald)."""
    h = int(w * 9 / 16)
    if side:
        x = (CW - (2 * w + gap)) / 2
        photo_frame(im, VOOR, (x, y, x + w, y + h), label="VOOR", r=26)
        photo_frame(im, NA, (x + w + gap, y, x + 2 * w + gap, y + h), label="NA", r=26)
        return y + h
    x = (CW - w) / 2
    photo_frame(im, VOOR, (x, y, x + w, y + h), label="VOOR", r=28)
    photo_frame(im, NA, (x, y + h + gap, x + w, y + 2 * h + gap), label="NA", r=28)
    return y + 2 * h + gap


def s_cover():
    im, d = cbase()
    kicker(d, 150, "Bewaar deze post", cx=CW / 2)
    y = ctext(d, 245, "Koffie zonder\ngele tanden?", serif(68, "SemiBold"), maxw=MW, cx=CW / 2)
    ctext(d, y + 8, "4 tips die echt helpen", serif_i(42), fill=GOLD_L, maxw=MW, cx=CW / 2)
    y = pair(im, 470, 520, gap=18); d = ImageDraw.Draw(im)
    d.text((CW / 2, y + 30), "Echte klant · geen filter      Swipe  ›", font=sans(26, "Medium"), fill=MUTED, anchor="mm")
    sparkle(d, 175, 190, 16); sparkle(d, 905, 215, 11)
    foot(d, 1); return im


def s_point(n, num, title, body):
    im, d = cbase()
    tf, bf = serif(66, "SemiBold"), sans(40)
    tl, bl = wrap(d, title, tf, MW), wrap(d, body, bf, MW)
    h = 110 + 50 + len(tl) * tf.size * 1.18 + 30 + len(bl) * bf.size * 1.45
    y = Y0 + (Y1 - 80 - Y0 - h) / 2
    d.ellipse((X0, y, X0 + 110, y + 110), outline=GOLD, width=4)
    d.text((X0 + 55, y + 55), str(num), font=serif(58, "SemiBold"), fill=GOLD_L, anchor="mm")
    y = cwrap_text(d, X0, y + 160, title, tf, maxw=MW, gap=1.18)
    cwrap_text(d, X0, y + 30, body, bf, fill=MUTED, maxw=MW, gap=1.45)
    foot(d, n); return im


def s_closing():
    im, d = cbase()
    ctext(d, 150, "Toch al verkleurd?\nDaar helpen wij je mee.", serif(58, "SemiBold"), maxw=MW, cx=CW / 2)
    y = pair(im, 340, 385, gap=20, side=True); d = ImageDraw.Draw(im)
    ctext(d, y + 25, "Eén afspraak · geen filter", serif_i(40), fill=GOLD_L, cx=CW / 2)
    ctext(d, y + 85, "Resultaten verschillen per persoon.", sans(26), fill=MUTED, cx=CW / 2)
    shade_guide(d, 760, active=6, w=520, cx=CW / 2, labels=False)
    d.rounded_rectangle((230, 985, 850, 1080), 48, fill=GOLD)
    d.text((CW / 2, 1032), "Boek via de link in bio", font=sans(36, "Medium"), fill=BG, anchor="mm")
    d.text((CW / 2, 1120), "of stuur ons SMILE in een DM", font=sans(28), fill=CREAM, anchor="mm")
    foot(d, T); return im


slides = [s_cover] + [lambda i=i, t=t, b=b: s_point(i + 2, i + 1, t, b) for i, (t, b) in enumerate(POINTS)] + [s_closing]

if __name__ == "__main__":
    paths = save_carousel(slides, sys.argv[1])
    if len(sys.argv) > 2: carousel_sheet(paths, sys.argv[2])
    print("\n".join(paths))
