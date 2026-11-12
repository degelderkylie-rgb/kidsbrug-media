import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from holasmile_style import *

# SJABLOON voor/na-reveal met Kylie's echte foto's uit holasmile/fotos/.
# Kopieer naar studio/reels/YYYY-MM-DD-onderwerp.py en vul VOOR, NA, HOOK, CONTEXT in.
# Regels: alleen echte foto's, nooit bewerken of witter maken, altijd "Resultaten verschillen per persoon".
HERE = os.path.join(os.path.dirname(__file__), "..", "..")
VOOR = os.path.join(HERE, "fotos", "NAAM-voor.jpg")
NA = os.path.join(HERE, "fotos", "NAAM-na.jpg")
HOOK = "Ze dronk elke dag koffie.\nKijk naar het verschil."
CONTEXT = "1 afspraak · 3 rondes van 20 minuten"
BOX = (110, 560, 970, 1420)  # vierkant fotovlak


def sA():
    im, d = base()
    kicker(d, 200, "Echt resultaat")
    ctext(d, 320, HOOK, serif(66, "SemiBold"))
    photo_frame(im, VOOR, BOX, "VOOR"); d = ImageDraw.Draw(im)
    wordmark(d); return im


def sB():
    im, d = base()
    kicker(d, 200, "Echt resultaat")
    ctext(d, 320, HOOK, serif(66, "SemiBold"))
    photo_frame(im, NA, BOX, "NA"); d = ImageDraw.Draw(im)
    for x, y, r in [(150, 600, 26), (930, 640, 18), (900, 1380, 22)]: sparkle(d, x, y, r)
    wordmark(d); return im


def sC():
    im, d = base()
    ctext(d, 220, "Voor en na", serif(80, "SemiBold"))
    photo_frame(im, VOOR, (110, 400, 970, 860), "VOOR", r=34)
    photo_frame(im, NA, (110, 900, 970, 1360), "NA", r=34); d = ImageDraw.Draw(im)
    ctext(d, 1430, CONTEXT, sans(36, "Medium"), fill=GOLD_L)
    ctext(d, 1500, "Geen filter. Resultaten verschillen per persoon.", sans(30), fill=MUTED)
    wordmark(d); return im


frames = {"A": sA, "B": sB, "C": sC, "E": cta}
scenes = [("1", [("A", 2.2), ("B", 2.6)]), ("2", [("C", 4.0)]), ("3", [("E", 3.6)])]


def COVER():
    im, d = base()
    kicker(d, 300, "Echt resultaat")
    ctext(d, 420, "Voor en na", serif(110, "SemiBold"))
    photo_frame(im, VOOR, (140, 640, 530, 1150), "VOOR", r=30)
    photo_frame(im, NA, (550, 640, 940, 1150), "NA", r=30); d = ImageDraw.Draw(im)
    ctext(d, 1230, "Geen filter", serif_i(54), fill=GOLD_L)
    wordmark(d, y=1600); return im


if __name__ == "__main__":
    work = sys.argv[1]; out = sys.argv[2]
    save_frames(frames, f"{work}/frames")
    save_cover(COVER(), out.replace(".mp4", "-cover.jpg") if out.endswith(".mp4") else f"{work}/cover.jpg")
    if "--sheet" in sys.argv: contact_sheet(f"{work}/frames", ["A", "B", "C", "E"], f"{work}/sheet.png")
    else: render_reel(scenes, f"{work}/frames", f"{work}/parts", out)
