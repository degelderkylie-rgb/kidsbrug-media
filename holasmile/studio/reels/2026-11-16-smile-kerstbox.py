import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from holasmile_motion import *

# Reel: Smile Kerstbox (aanbod). Sfeerbeelden van lachende mensen (AI/Canva, niet in git: holasmile/sfeer-lokaal/).
# Geen klanten, geen resultaten: alleen sfeer. Post krijgt het AI-label.
S = os.path.join(os.path.dirname(__file__), "..", "..", "sfeer-lokaal")
KOPPEL = Fullbleed(os.path.join(S, "koppel-kerst.png"), (0.02, 0.0, 0.62, 1.0))
VROUW = Fullbleed(os.path.join(S, "vrouw-goud.png"), (0.55, 0.06, 1.0, 0.46))
GROEP = Fullbleed(os.path.join(S, "canva-groep.png"), (0.0, 0.15, 1.0, 0.95))


def s1(t, p):
    im = KOPPEL.frame(1.0 + 0.12 * p); d = ImageDraw.Draw(im)
    big_text(d, 1390, "Op zoek naar een\nkerstcadeau dat\nécht straalt?", 88, scale=pop(min(1, t / 0.35)))
    ai_note(d); return im


def s2(t, p):
    im = VROUW.frame(1.12 - 0.10 * p); d = ImageDraw.Draw(im)
    big_text(d, 150, "Geef een stralende\nglimlach cadeau.", 96, scale=pop(min(1, t / 0.35)))
    twinkle(d, t, [(160, 560, 26), (930, 520, 20)]); ai_note(d); return im


ITEMS = ["Cadeaubon voor een\nbleekbehandeling", "Glow Powder & Glow\nWhitening Serum gratis\nbij elk pakket", "Ook als kerstpakket\nvoor je team"]


def s3(t, p):
    im, d = base()
    kicker(d, 240, "Smile Kerstbox")
    big_text(d, 380, "Dit zit erin:", 96, scale=pop(min(1, t / 0.3)))
    y = 700
    for i, it in enumerate(ITEMS):
        k = ease((t - 0.4 - i * 0.7) / 0.35)
        if k <= 0: break
        x = 150 - (1 - k) * 300
        d.ellipse((x, y + 10, x + 80, y + 90), outline=GOLD, width=4)
        d.text((x + 40, y + 50), str(i + 1), font=serif(44, "SemiBold"), fill=GOLD_L, anchor="mm")
        cwrap_text(d, x + 130, y, it, serif(62, "SemiBold"), maxw=760, gap=1.2)
        y += 330
    twinkle(d, t, [(170, 300, 18), (910, 280, 24)]); wordmark(d); return im


def s4(t, p):
    im = GROEP.frame(1.0 + 0.10 * p); d = ImageDraw.Draw(im)
    big_text(d, 150, "Voor je moeder,\nje vriendin of\nje collega's.", 92, scale=pop(min(1, t / 0.35)))
    ai_note(d); return im


def s5(t, p):
    im, d = base()
    d.text((W / 2, 400), "Hola Smile", font=serif(int(120 * pop(min(1, t / 0.35))), "SemiBold"), fill=CREAM, anchor="mm")
    d.text((W / 2, 515), "CLINIC · ZUNDERT", font=sans(30, "Medium"), fill=GOLD, anchor="mm")
    rule(d, 610)
    ctext(d, 720, "Bestel je\nSmile Kerstbox", serif(92, "SemiBold"))
    if t > 0.6:
        pl = 1 + 0.03 * math.sin(t * 7); bw, bh = 760 * pl, 136 * pl
        d.rounded_rectangle((W / 2 - bw / 2, 1120 - bh / 2, W / 2 + bw / 2, 1120 + bh / 2), 68, fill=GOLD)
        d.text((W / 2, 1120), "Stuur KERST in een DM", font=sans(48, "Medium"), fill=BG, anchor="mm")
        d.text((W / 2, 1260), "of boek via de link in bio", font=sans(36), fill=CREAM, anchor="mm")
    twinkle(d, t, [(220, 330, 20), (860, 300, 26), (900, 1420, 16), (180, 1380, 14)])
    wordmark(d); return im


scenes = [(2.9, s1), (2.7, s2), (3.4, s3), (2.7, s4), (3.4, s5)]


def COVER():
    im = KOPPEL.frame(1.08); d = ImageDraw.Draw(im)
    kicker(d, 1180, "Smile Kerstbox")
    big_text(d, 1280, "Geef een glimlach\ncadeau", 96)
    return im


if __name__ == "__main__":
    work = sys.argv[1]; out = sys.argv[2]; os.makedirs(work, exist_ok=True)
    COVER().save(out.replace(".mp4", "-cover.jpg") if out.endswith(".mp4") else f"{work}/cover.jpg", "JPEG", quality=90)
    if "--sheet" in sys.argv: still_sheet(scenes, [(0, 0.1), (0, 1), (1, 0.5), (2, 0.3), (2, 1), (3, 0.5), (4, 1)], f"{work}/sheet.png")
    else: render_motion(scenes, out, work)
