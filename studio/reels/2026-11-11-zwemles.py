import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from kidsbrug_style import *

def sA(n):
    im, d = base()
    ctext(d, 230, "POV: “Wie betaalde de zwemles ook alweer?”", serif(84, "SemiBold"), maxw=900)
    msgs = [("Wie betaalde de zwemles ook alweer?", False, "Ex"),
            ("Ik. In september.", True, None),
            ("Heb je het bonnetje nog?", False, "Ex"),
            ("…", True, None)]
    y = 700
    for t, me, l in msgs[:n]: y = bubble(d, y, t, me, l)
    wordmark(d); return im

ITEMS = [("Zwemles", "€ 145", "Papa"), ("Winterjas", "€ 59", "Mama"), ("Schoolreis", "€ 32", "Mama"), ("Verjaardag", "€ 25", "Papa")]

def sB(n):
    im, d = base()
    ctext(d, 230, "En daar gaan we weer.", serif(84, "SemiBold"), maxw=900)
    ctext(d, 360, "Wie betaalde wat?", serif(56), fill=BROWN)
    y = 600
    for t, a, _ in ITEMS[:n]:
        d.rounded_rectangle((150, y, 930, y + 140), 40, fill=WHITE)
        d.text((200, y + 70), t, font=serif(52), fill=DARK, anchor="lm")
        d.text((700, y + 70), a, font=sans(40, "Medium"), fill=DARK, anchor="rm")
        d.ellipse((790, y + 35, 860, y + 105), fill=ROSE)
        d.text((825, y + 70), "?", font=sans(40, "Medium"), fill=DARK, anchor="mm")
        y += 170
    wordmark(d); return im

def sC(n):
    im, d = base()
    ctext(d, 220, "Met KidsBrug staat het er gewoon in.", serif(72, "SemiBold"), maxw=920)
    d, (x0, y0, x1, y1) = phone(im, top=640, h=1120, title="Kosten")
    cx = x0
    for i, c in enumerate(["Alles", "Deze maand", "Open"]):
        f = sans(24, "Medium"); tw = d.textlength(c, font=f) + 44; sel = i == 1
        d.rounded_rectangle((cx, y0, cx + tw, y0 + 54), 27, fill=BROWN if sel else CHIP)
        d.text((cx + 22, y0 + 27), c, font=f, fill=WHITE if sel else DARK, anchor="lm"); cx += tw + 14
    y = y0 + 90
    if n == 1:
        for t, a, who in ITEMS:
            card(d, (x0, y, x1, y + 150))
            d.text((x0 + 25, y + 45), t, font=sans(28, "Medium"), fill=DARK, anchor="lm")
            d.text((x1 - 25, y + 45), a, font=sans(28, "Medium"), fill=DARK, anchor="rm")
            nx = chip(d, x0 + 25, y + 85, f"Betaald door {who.lower()}", SAGE if who == "Papa" else ROSE)
            chip(d, nx + 10, y + 85, "Bonnetje erbij", GOLD)
            y += 168
    else:
        card(d, (x0, y, x1, y + 330), fill=WHITE, outline=GOLD)
        d.text(((x0 + x1) / 2, y + 70), "Saldo november", font=sans(28, "Medium"), fill=MUTED, anchor="mm")
        d.text(((x0 + x1) / 2, y + 160), "€ 39,50", font=serif(72, "SemiBold"), fill=DARK, anchor="mm")
        d.text(((x0 + x1) / 2, y + 245), "mama betaalt papa · 50/50", font=sans(28), fill=MUTED, anchor="mm")
        y += 370
        ctext(d, y + 20, "Automatisch verdeeld.\nZoals jullie afspraken.", serif(42), fill=BROWN, maxw=560)
    wordmark(d); return im

def sD():
    im, d = base()
    checklist(d, "Elke uitgave staat vast:", ["Wat het was", "Hoeveel", "Wie betaalde", "Het bonnetje"],
              "Geen gedoe meer\nover geld.", "Jullie zien allebei hetzelfde overzicht.")
    return im

frames = {"A1": lambda: sA(1), "A2": lambda: sA(2), "A3": lambda: sA(3), "A4": lambda: sA(4),
          "B2": lambda: sB(2), "B4": lambda: sB(4), "C1": lambda: sC(1), "C2": lambda: sC(2), "D": sD, "E": cta}
scenes = [("1", [("A1", 1.1), ("A2", 0.9), ("A3", 0.9), ("A4", 1.3)]), ("2", [("B2", 1.0), ("B4", 1.6)]),
          ("3", [("C1", 2.2), ("C2", 2.4)]), ("4", [("D", 3.4)]), ("5", [("E", 3.8)])]

if __name__ == "__main__":
    work = sys.argv[1]; out = sys.argv[2]
    save_frames(frames, f"{work}/frames")
    if "--sheet" in sys.argv: contact_sheet(f"{work}/frames", ["A4", "B4", "C1", "C2", "D", "E"], f"{work}/sheet.png")
    else: render_reel(scenes, f"{work}/frames", f"{work}/parts", out)
