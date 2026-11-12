import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from holasmile_style import *

# Voor/na-reveal 14 nov (klant06). Gemaakt uit het sjabloon met Kylie's echte foto's uit holasmile/fotos/.
# Kopieer naar studio/reels/YYYY-MM-DD-onderwerp.py en vul VOOR, NA, HOOK, CONTEXT in.
# De foto's zijn liggend (ongeveer 16:9, 1080x608); de vlakken hieronder zijn daarop afgestemd.
# Verzin niets over de klant (geen koffie, roken of aantal rondes als je dat niet weet): houd HOOK en CONTEXT algemeen.
# Regels: alleen echte foto's, nooit bewerken of witter maken, altijd "Resultaten verschillen per persoon".
HERE = os.path.join(os.path.dirname(__file__), "..", "..")
VOOR = os.path.join(HERE, "fotos", "klant06-voor.jpg")
NA = os.path.join(HERE, "fotos", "klant06-na.jpg")
HOOK = "Kijk wat één afspraak\nkan doen."
CONTEXT = "Eén afspraak bij Hola Smile Clinic"
BOX = (90, 700, 990, 1206)  # liggend fotovlak (900x506)


def sA():
    im, d = base()
    kicker(d, 300, "Echt resultaat")
    ctext(d, 430, HOOK, serif(72, "SemiBold"))
    photo_frame(im, VOOR, BOX, "VOOR"); d = ImageDraw.Draw(im)
    ctext(d, 1290, "Wacht op het na-beeld…", serif_i(54), fill=GOLD_L)
    wordmark(d); return im


def sB():
    im, d = base()
    kicker(d, 300, "Echt resultaat")
    ctext(d, 430, HOOK, serif(72, "SemiBold"))
    photo_frame(im, NA, BOX, "NA"); d = ImageDraw.Draw(im)
    for x, y, r in [(140, 680, 26), (950, 700, 18), (930, 1230, 22)]: sparkle(d, x, y, r)
    ctext(d, 1290, "Geen filter.", serif_i(54), fill=GOLD_L)
    wordmark(d); return im


def sC():
    im, d = base()
    ctext(d, 220, "Voor en na", serif(80, "SemiBold"))
    photo_frame(im, VOOR, (110, 380, 970, 864), "VOOR", r=34)
    photo_frame(im, NA, (110, 900, 970, 1384), "NA", r=34); d = ImageDraw.Draw(im)
    ctext(d, 1450, CONTEXT, sans(36, "Medium"), fill=GOLD_L)
    ctext(d, 1520, "Geen filter. Resultaten verschillen per persoon.", sans(30), fill=MUTED)
    wordmark(d); return im


frames = {"A": sA, "B": sB, "C": sC, "E": cta}
scenes = [("1", [("A", 2.2), ("B", 2.6)]), ("2", [("C", 4.0)]), ("3", [("E", 3.6)])]


def COVER():
    im, d = base()
    kicker(d, 290, "Echt resultaat")
    ctext(d, 390, "Voor en na", serif(100, "SemiBold"))
    photo_frame(im, VOOR, (200, 560, 880, 943), "VOOR", r=30)
    photo_frame(im, NA, (200, 970, 880, 1353), "NA", r=30); d = ImageDraw.Draw(im)
    ctext(d, 1400, "Geen filter", serif_i(52), fill=GOLD_L)
    wordmark(d, y=1600); return im


if __name__ == "__main__":
    work = sys.argv[1]; out = sys.argv[2]
    save_frames(frames, f"{work}/frames")
    save_cover(COVER(), out.replace(".mp4", "-cover.jpg") if out.endswith(".mp4") else f"{work}/cover.jpg")
    if "--sheet" in sys.argv: contact_sheet(f"{work}/frames", ["A", "B", "C", "E"], f"{work}/sheet.png")
    else: render_reel(scenes, f"{work}/frames", f"{work}/parts", out)
