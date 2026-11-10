import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from kidsbrug_style import *

def sA(n):
    im, d = base()
    ctext(d, 230, "POV: jullie hadden 18:00 afgesproken. Toch?", serif(84, "SemiBold"), maxw=900)
    msgs = [("Ik sta klaar met de tas. Waar blijf je?", True, None),
            ("Het was toch 19:00?", False, "Ex"),
            ("We zeiden 18:00!", True, None),
            ("Staat in de chat van vorige week.", False, "Ex")]
    y = 680
    for t, me, l in msgs[:n]: y = bubble(d, y, t, me, l)
    wordmark(d); return im

def sB(n):
    im, d = base()
    ctext(d, 230, "En dan ga je scrollen…", serif(84, "SemiBold"), maxw=900)
    ctext(d, 360, "Ergens tussen 600 berichtjes.", serif(56), fill=BROWN)
    y = 640
    seq = [("Hoe laat was het nou?", True), ("Kijk zelf maar.", False), ("Ik zie het nergens!", True), ("Laat maar.", True)]
    for t, me in seq[:n]: y = bubble(d, y, t, me, big=True)
    wordmark(d); return im

def sC(n):
    im, d = base()
    ctext(d, 220, "Met KidsBrug staat het gewoon in de kalender.", serif(72, "SemiBold"), maxw=920)
    d, (x0, y0, x1, y1) = phone(im, top=640, h=1120, title="Wisselschema")
    days = ["ma", "di", "wo", "do", "vr", "za", "zo"]; cw = (x1 - x0 - 6 * 10) / 7
    for i, dn in enumerate(days):
        cx = x0 + i * (cw + 10)
        d.text((cx + cw / 2, y0 + 10), dn, font=sans(22, "Medium"), fill=MUTED, anchor="mt")
        d.rounded_rectangle((cx, y0 + 50, cx + cw, y0 + 130), 20, fill=ROSE if i < 6 else SAGE)
        d.text((cx + cw / 2, y0 + 90), str(10 + i), font=sans(28, "Medium"), fill=DARK, anchor="mm")
    chip(d, x0, y0 + 160, "Bij mama", ROSE); chip(d, x0 + 170, y0 + 160, "Bij papa", SAGE)
    y = y0 + 250
    if n == 1:
        card(d, (x0, y, x1, y + 250), fill=WHITE, outline=GOLD)
        d.text((x0 + 30, y + 55), "Zondag 16 november", font=sans(28, "Medium"), fill=MUTED, anchor="lm")
        d.text((x0 + 30, y + 130), "Wissel om 18:00", font=serif(54, "SemiBold"), fill=DARK, anchor="lm")
        d.text((x0 + 30, y + 200), "Mama brengt naar papa", font=sans(28), fill=MUTED, anchor="lm")
    else:
        card(d, (x0, y, x1, y + 400))
        d.text((x0 + 30, y + 55), "Verzoek van papa", font=sans(26, "Medium"), fill=MUTED, anchor="lm")
        d.text((x0 + 30, y + 125), "Wissel om 19:00?", font=serif(50, "SemiBold"), fill=DARK, anchor="lm")
        d.text((x0 + 30, y + 190), "Ik ben pas om 18:30 thuis.", font=sans(28), fill=DARK, anchor="lm")
        if n == 2:
            d.rounded_rectangle((x0 + 30, y + 260, x0 + 280, y + 350), 45, fill=BROWN)
            d.text((x0 + 155, y + 305), "Goedkeuren", font=sans(28, "Medium"), fill=WHITE, anchor="mm")
            d.rounded_rectangle((x0 + 300, y + 260, x0 + 520, y + 350), 45, fill=CHIP)
            d.text((x0 + 410, y + 305), "Weigeren", font=sans(28, "Medium"), fill=DARK, anchor="mm")
        else:
            d.rounded_rectangle((x0 + 30, y + 260, x1 - 30, y + 350), 45, fill=SAGE)
            d.text(((x0 + x1) / 2, y + 305), "Goedgekeurd door mama", font=sans(28, "Medium"), fill=DARK, anchor="mm")
            ctext(d, y + 440, "Zwart op wit.\nVoor jullie allebei.", serif(42), fill=BROWN, maxw=560)
    wordmark(d); return im

def sD():
    im, d = base()
    checklist(d, "Elke afspraak staat vast:", ["Wie brengt", "Hoe laat", "Waar", "Wie iets wijzigde"],
              "Geen discussie.\nGewoon wat jullie afspraken.", "En jullie zien allebei hetzelfde.")
    return im

frames = {"A1": lambda: sA(1), "A2": lambda: sA(2), "A3": lambda: sA(3), "A4": lambda: sA(4),
          "B2": lambda: sB(2), "B4": lambda: sB(4),
          "C1": lambda: sC(1), "C2": lambda: sC(2), "C3": lambda: sC(3), "D": sD, "E": cta}
scenes = [("1", [("A1", 1.0), ("A2", 1.0), ("A3", 0.9), ("A4", 1.6)]), ("2", [("B2", 1.0), ("B4", 1.5)]),
          ("3", [("C1", 1.8), ("C2", 1.6), ("C3", 2.2)]), ("4", [("D", 3.4)]), ("5", [("E", 3.8)])]

if __name__ == "__main__":
    work = sys.argv[1]; out = sys.argv[2]
    save_frames(frames, f"{work}/frames")
    if "--sheet" in sys.argv: contact_sheet(f"{work}/frames", ["A4", "B4", "C1", "C2", "C3", "D", "E"], f"{work}/sheet.png")
    else: render_reel(scenes, f"{work}/frames", f"{work}/parts", out)
