import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from kidsbrug_style import *

def sA(n):
    im, d = base()
    ctext(d, 230, "POV: je hoort pas achteraf dat er een oudergesprek was.", serif(80, "SemiBold"), maxw=900)
    msgs = [("Was er gisteren een oudergesprek op school?", True, None),
            ("Ja. Stond in de mail van de juf.", False, "Ex"),
            ("Die mail krijg ik niet.", True, None),
            ("Dan had je het moeten vragen.", False, "Ex")]
    y = 720
    for t, me, l in msgs[:n]: y = bubble(d, y, t, me, l)
    wordmark(d); return im

def sB(n):
    im, d = base()
    ctext(d, 230, "En daar gaan we weer.", serif(84, "SemiBold"), maxw=900)
    ctext(d, 360, "Wie had het moeten zeggen?", serif(56), fill=BROWN)
    y = 640
    seq = [("Je had het kunnen doorsturen.", True), ("Je had het kunnen vragen.", False), ("Altijd mijn schuld.", True), ("Laat maar.", False)]
    for t, me in seq[:n]: y = bubble(d, y, t, me, big=True)
    wordmark(d); return im

EVENTS = [("Do 19 nov", "Oudergesprek school", "19:30", ROSE), ("Za 21 nov", "Zwemles", "10:00", SAGE), ("Zo 22 nov", "Wissel", "18:00", GOLD)]

def sC(n):
    im, d = base()
    ctext(d, 220, "Met KidsBrug staat het in jullie gedeelde kalender.", serif(72, "SemiBold"), maxw=920)
    d, (x0, y0, x1, y1) = phone(im, top=640, h=1120, title="Kalender")
    y = y0 + 10
    if n == 1:
        for day, t, tm, col in EVENTS:
            card(d, (x0, y, x1, y + 150))
            d.rounded_rectangle((x0, y, x0 + 14, y + 150), 7, fill=col)
            d.text((x0 + 40, y + 45), day, font=sans(24, "Medium"), fill=MUTED, anchor="lm")
            d.text((x0 + 40, y + 100), t, font=sans(30, "Medium"), fill=DARK, anchor="lm")
            d.text((x1 - 25, y + 100), tm, font=sans(28, "Medium"), fill=DARK, anchor="rm")
            y += 172
    else:
        card(d, (x0, y, x1, y + 380), fill=WHITE, outline=GOLD)
        d.text((x0 + 30, y + 55), "Donderdag 19 november", font=sans(28, "Medium"), fill=MUTED, anchor="lm")
        d.text((x0 + 30, y + 130), "Oudergesprek", font=serif(54, "SemiBold"), fill=DARK, anchor="lm")
        d.text((x0 + 30, y + 200), "School, 19:30", font=sans(28), fill=DARK, anchor="lm")
        chip(d, x0 + 30, y + 270, "Toegevoegd door mama", ROSE, size=26)
        if n == 3:
            ctext(d, y + 450, "Allebei op de hoogte.\nVan tevoren.", serif(42), fill=BROWN, maxw=560)
    wordmark(d); return im

def sD():
    im, d = base()
    checklist(d, "In de kalender staat:", ["Schoolafspraken", "Wissels", "Activiteiten", "Wie wat toevoegde"],
              "Niemand hoort het\nmeer achteraf.", "Jullie zien allebei hetzelfde.")
    return im

frames = {"A1": lambda: sA(1), "A2": lambda: sA(2), "A3": lambda: sA(3), "A4": lambda: sA(4),
          "B2": lambda: sB(2), "B4": lambda: sB(4),
          "C1": lambda: sC(1), "C2": lambda: sC(2), "C3": lambda: sC(3), "D": sD, "E": cta}
scenes = [("1", [("A1", 1.1), ("A2", 1.0), ("A3", 0.9), ("A4", 1.6)]), ("2", [("B2", 1.0), ("B4", 1.5)]),
          ("3", [("C1", 2.0), ("C2", 1.6), ("C3", 2.2)]), ("4", [("D", 3.4)]), ("5", [("E", 3.8)])]

COVER = lambda: cover("POV: je hoort pas achteraf dat er een oudergesprek was.", [("Was er gisteren een oudergesprek?", True, None), ("Stond in de mail van de juf.", False, "Ex")])

if __name__ == "__main__":
    work = sys.argv[1]; out = sys.argv[2]
    save_frames(frames, f"{work}/frames")
    save_cover(COVER(), out.replace(".mp4", "-cover.jpg") if out.endswith(".mp4") else f"{work}/cover.jpg")
    if "--sheet" in sys.argv: contact_sheet(f"{work}/frames", ["A4", "B4", "C1", "C2", "C3", "D", "E"], f"{work}/sheet.png")
    else: render_reel(scenes, f"{work}/frames", f"{work}/parts", out)
