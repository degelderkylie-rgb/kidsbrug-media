import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from kidsbrug_style import *

DOCS = [("Ouderschapsplan", "PDF", GOLD), ("Schoolrapport", "PDF", SAGE), ("Inschrijving sportclub", "PDF", ROSE), ("Zwemdiploma", "Foto", SAGE)]

def sA(n):
    im, d = base()
    ctext(d, 230, "POV: “Dat staat níet in het ouderschapsplan.”", serif(80, "SemiBold"), maxw=900)
    msgs = [("Zo hebben we dat nooit afgesproken.", False, "Ex"),
            ("Wel! Stuur het even, dan kijken we.", True, None),
            ("Heb ik niet meer. Jij toch?", False, "Ex"),
            ("Ergens in een mail. Van 2 jaar terug.", True, None)]
    y = 720
    for t, me, l in msgs[:n]: y = bubble(d, y, t, me, l)
    wordmark(d); return im

def sB(n):
    im, d = base()
    ctext(d, 230, "Dan maar zoeken…", serif(84, "SemiBold"), maxw=900)
    ctext(d, 360, "Mails, mapjes, twee huizen.", serif(56), fill=BROWN, maxw=900)
    y = 640
    seq = [("Gevonden?", False), ("Nog niet.", True), ("Ik ook niet.", False), ("Laat maar zitten.", True)]
    for t, me in seq[:n]: y = bubble(d, y, t, me, big=True)
    wordmark(d); return im

def sC(n):
    im, d = base()
    ctext(d, 220, "Met KidsBrug staat alles op één plek.", serif(72, "SemiBold"), maxw=920)
    d, (x0, y0, x1, y1) = phone(im, top=640, h=1120, title="Documenten")
    y = y0 + 10
    if n == 1:
        for t, kind, col in DOCS:
            card(d, (x0, y, x1, y + 130))
            d.rounded_rectangle((x0 + 22, y + 25, x0 + 102, y + 105), 18, fill=col)
            d.text((x0 + 62, y + 65), kind, font=sans(20, "Medium"), fill=DARK, anchor="mm")
            d.text((x0 + 125, y + 48), t, font=sans(28, "Medium"), fill=DARK, anchor="lm")
            d.text((x0 + 125, y + 90), "Gedeeld met jullie allebei", font=sans(22), fill=MUTED, anchor="lm")
            y += 150
    else:
        card(d, (x0, y, x1, y + 470), fill=WHITE, outline=GOLD)
        d.rounded_rectangle((x0 + 30, y + 30, x0 + 130, y + 130), 22, fill=GOLD)
        d.text((x0 + 80, y + 80), "PDF", font=sans(26, "Medium"), fill=DARK, anchor="mm")
        d.text((x0 + 155, y + 62), "Ouderschapsplan", font=serif(42, "SemiBold"), fill=DARK, anchor="lm")
        d.text((x0 + 155, y + 108), "Gedeeld met jullie allebei", font=sans(24), fill=MUTED, anchor="lm")
        for i, w in enumerate([440, 400, 460, 300]):
            d.rounded_rectangle((x0 + 30, y + 180 + i * 50, x0 + 30 + w, y + 200 + i * 50), 10, fill=CHIP)
        d.rounded_rectangle((x0 + 30, y + 380, x1 - 30, y + 450), 35, fill=SAGE)
        d.text(((x0 + x1) / 2, y + 415), "Openen", font=sans(28, "Medium"), fill=DARK, anchor="mm")
        ctext(d, y + 520, "Eén keer opslaan.\nAltijd terugvinden.", serif(42), fill=BROWN, maxw=560)
    wordmark(d); return im

def sD():
    im, d = base()
    checklist(d, "Alles op één plek:", ["Ouderschapsplan", "Schoolpapieren", "Inschrijvingen", "Diploma’s"],
              "Niet meer zoeken.\nGewoon openen.", "En jullie zien allebei hetzelfde.")
    return im

frames = {"A1": lambda: sA(1), "A2": lambda: sA(2), "A3": lambda: sA(3), "A4": lambda: sA(4),
          "B2": lambda: sB(2), "B4": lambda: sB(4), "C1": lambda: sC(1), "C2": lambda: sC(2), "D": sD, "E": cta}
scenes = [("1", [("A1", 1.1), ("A2", 1.0), ("A3", 1.0), ("A4", 1.5)]), ("2", [("B2", 1.0), ("B4", 1.6)]),
          ("3", [("C1", 2.4), ("C2", 2.4)]), ("4", [("D", 3.4)]), ("5", [("E", 3.8)])]

COVER = lambda: cover("POV: “Dat staat níet in het ouderschapsplan.”", [("Stuur het even, dan kijken we.", True, None), ("Heb ik niet meer. Jij toch?", False, "Ex")])

if __name__ == "__main__":
    work = sys.argv[1]; out = sys.argv[2]
    save_frames(frames, f"{work}/frames")
    save_cover(COVER(), out.replace(".mp4", "-cover.jpg") if out.endswith(".mp4") else f"{work}/cover.jpg")
    if "--sheet" in sys.argv: contact_sheet(f"{work}/frames", ["A4", "B4", "C1", "C2", "D", "E"], f"{work}/sheet.png")
    else: render_reel(scenes, f"{work}/frames", f"{work}/parts", out)
