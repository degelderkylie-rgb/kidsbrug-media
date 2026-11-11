import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from kidsbrug_style import *

def sA(n):
    im, d = base()
    ctext(d, 230, "POV: “Je zei toch dat het goed was?”", serif(84, "SemiBold"), maxw=900)
    msgs = [("Ze gaat zaterdag mee op kamp, hè.", False, "Ex"),
            ("Kamp? Daar weet ik niks van.", True, None),
            ("Je zei vorige maand dat het goed was.", False, "Ex"),
            ("Dat heb ik nooit gezegd.", True, None)]
    y = 680
    for t, me, l in msgs[:n]: y = bubble(d, y, t, me, l)
    wordmark(d); return im

def sB(n):
    im, d = base()
    ctext(d, 230, "En daar gaan we weer.", serif(84, "SemiBold"), maxw=900)
    ctext(d, 360, "Wie zei wat, en wanneer?", serif(56), fill=BROWN)
    y = 640
    seq = [("Jij zei ja.", False), ("Ik zei: we hebben het erover.", True), ("Dat is hetzelfde.", False), ("Echt niet.", True)]
    for t, me in seq[:n]: y = bubble(d, y, t, me, big=True)
    wordmark(d); return im

def sC(n):
    im, d = base()
    ctext(d, 220, "Met KidsBrug vraag je het zwart op wit.", serif(72, "SemiBold"), maxw=920)
    d, (x0, y0, x1, y1) = phone(im, top=640, h=1120, title="Toestemmingen")
    cx = x0
    for i, c in enumerate(["Open", "Akkoord", "Alles"]):
        f = sans(24, "Medium"); tw = d.textlength(c, font=f) + 44; sel = i == (0 if n == 1 else 1)
        d.rounded_rectangle((cx, y0, cx + tw, y0 + 54), 27, fill=BROWN if sel else CHIP)
        d.text((cx + 22, y0 + 27), c, font=f, fill=WHITE if sel else DARK, anchor="lm"); cx += tw + 14
    y = y0 + 100
    card(d, (x0, y, x1, y + 430), fill=WHITE if n == 2 else (250, 246, 240), outline=GOLD if n == 2 else None)
    d.text((x0 + 30, y + 55), "Vraag van papa", font=sans(26, "Medium"), fill=MUTED, anchor="lm")
    d.text((x0 + 30, y + 125), "Mee op weekendkamp?", font=serif(42, "SemiBold"), fill=DARK, anchor="lm")
    d.text((x0 + 30, y + 190), "Met de scouting, za en zo.", font=sans(28), fill=DARK, anchor="lm")
    d.text((x0 + 30, y + 235), "Ophalen zondag om 16:00.", font=sans(28), fill=DARK, anchor="lm")
    if n == 1:
        d.rounded_rectangle((x0 + 30, y + 300, x0 + 260, y + 390), 45, fill=BROWN)
        d.text((x0 + 145, y + 345), "Akkoord", font=sans(28, "Medium"), fill=WHITE, anchor="mm")
        d.rounded_rectangle((x0 + 280, y + 300, x0 + 540, y + 390), 45, fill=CHIP)
        d.text((x0 + 410, y + 345), "Niet akkoord", font=sans(28, "Medium"), fill=DARK, anchor="mm")
    else:
        d.rounded_rectangle((x0 + 30, y + 300, x1 - 30, y + 390), 45, fill=SAGE)
        d.text(((x0 + x1) / 2, y + 345), "Akkoord gegeven door mama", font=sans(28, "Medium"), fill=DARK, anchor="mm")
        ctext(d, y + 480, "Wie vroeg wat.\nWie zei ja.\nVoor jullie allebei.", serif(42), fill=BROWN, maxw=560)
    wordmark(d); return im

def sD():
    im, d = base()
    checklist(d, "Elke toestemming staat vast:", ["Wat er gevraagd is", "Door wie", "Het antwoord", "Wanneer"],
              "Geen “dat zei je toch”.\nGewoon zwart op wit.", "En niemand kan het achteraf wissen.")
    return im

frames = {"A1": lambda: sA(1), "A2": lambda: sA(2), "A3": lambda: sA(3), "A4": lambda: sA(4),
          "B2": lambda: sB(2), "B4": lambda: sB(4), "C1": lambda: sC(1), "C2": lambda: sC(2), "D": sD, "E": cta}
scenes = [("1", [("A1", 1.1), ("A2", 1.0), ("A3", 1.0), ("A4", 1.5)]), ("2", [("B2", 1.0), ("B4", 1.6)]),
          ("3", [("C1", 2.4), ("C2", 2.6)]), ("4", [("D", 3.4)]), ("5", [("E", 3.8)])]

COVER = lambda: cover("POV: “Je zei toch dat het goed was?”", [("Ze gaat zaterdag op kamp, hè.", False, "Ex"), ("Daar weet ik niks van.", True, None)])

if __name__ == "__main__":
    work = sys.argv[1]; out = sys.argv[2]
    save_frames(frames, f"{work}/frames")
    save_cover(COVER(), out.replace(".mp4", "-cover.jpg") if out.endswith(".mp4") else f"{work}/cover.jpg")
    if "--sheet" in sys.argv: contact_sheet(f"{work}/frames", ["A4", "B4", "C1", "C2", "D", "E"], f"{work}/sheet.png")
    else: render_reel(scenes, f"{work}/frames", f"{work}/parts", out)
