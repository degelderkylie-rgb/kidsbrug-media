import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from kidsbrug_style import *

def sA(n):
    im, d = base()
    ctext(d, 230, "POV: één appje over de gymtas, en het is weer ruzie.", serif(80, "SemiBold"), maxw=900)
    msgs = [("De gymtas was weer vergeten.", False, "Ex"),
            ("Jij had hem toch?", True, None),
            ("Nee, jij.", False, "Ex"),
            ("Altijd moet ik alles doen!!", True, None)]
    y = 720
    for t, me, l in msgs[:n]: y = bubble(d, y, t, me, l)
    wordmark(d); return im

def sB(n):
    im, d = base()
    ctext(d, 230, "En daar gaan we weer.", serif(84, "SemiBold"), maxw=900)
    ctext(d, 360, "Over een gymtas.", serif(56), fill=BROWN)
    y = 640
    seq = [("Laat ook maar.", True), ("Prima.", False), ("Ik ben er klaar mee.", True), ("Ik ook.", False)]
    for t, me in seq[:n]: y = bubble(d, y, t, me, big=True)
    wordmark(d); return im

def sC(n):
    im, d = base()
    ctext(d, 220, "Met KidsBrug blijft de toon rustig.", serif(72, "SemiBold"), maxw=920)
    d, (x0, y0, x1, y1) = phone(im, top=640, h=1120, title="Berichten")
    f = sans(28, "Medium")
    def msg(y, text, me):
        tw = d.textlength(text, font=f) + 60
        x = x1 - tw if me else x0
        d.rounded_rectangle((x, y, x + tw, y + 76), 32, fill=ME_BUBBLE if me else CHIP)
        d.text((x + 30, y + 38), text, font=f, fill=DARK, anchor="lm")
        return y + 100
    y = msg(y0 + 20, "De gymtas was weer vergeten.", False)
    if n < 3:
        d.text((x0, y + 20), "Jij typt:", font=sans(24, "Medium"), fill=MUTED, anchor="lt"); y += 50
        card(d, (x0, y + 10, x1, y + 110), fill=WHITE, outline=ROSE)
        d.text((x0 + 30, y + 60), "Altijd moet ik alles doen!!", font=f, fill=DARK, anchor="lm")
        y += 150
        if n == 2:
            card(d, (x0, y, x1, y + 400), fill=WHITE, outline=GOLD)
            d.text((x0 + 30, y + 55), "Berichtenfilter", font=sans(26, "Medium"), fill=MUTED, anchor="lm")
            d.text((x0 + 30, y + 125), "Even checken", font=serif(50, "SemiBold"), fill=DARK, anchor="lm")
            d.text((x0 + 30, y + 190), "Dit klinkt misschien scherp.", font=sans(28), fill=DARK, anchor="lm")
            d.rounded_rectangle((x0 + 30, y + 260, x0 + 280, y + 350), 45, fill=BROWN)
            d.text((x0 + 155, y + 305), "Aanpassen", font=sans(28, "Medium"), fill=WHITE, anchor="mm")
            d.rounded_rectangle((x0 + 300, y + 260, x1 - 30, y + 350), 45, fill=CHIP)
            d.text(((x0 + 300 + x1 - 30) / 2, y + 305), "Toch sturen", font=sans(28, "Medium"), fill=DARK, anchor="mm")
    else:
        y = msg(y, "Kun jij hem voortaan meegeven?", True)
        y = msg(y, "Is goed. Zet ik op mijn lijstje.", False)
        ctext(d, y + 60, "Zelfde vraag.\nGeen ruzie.", serif(42), fill=BROWN, maxw=560)
    wordmark(d); return im

def sD():
    im, d = base()
    checklist(d, "Berichten blijven:", ["Rustig", "Zakelijk", "Bewaard", "Over je kind"],
              "Minder ruzie.\nMeer rust voor je kind.", "Ook op een slechte dag.")
    return im

frames = {"A1": lambda: sA(1), "A2": lambda: sA(2), "A3": lambda: sA(3), "A4": lambda: sA(4),
          "B2": lambda: sB(2), "B4": lambda: sB(4),
          "C1": lambda: sC(1), "C2": lambda: sC(2), "C3": lambda: sC(3), "D": sD, "E": cta}
scenes = [("1", [("A1", 1.0), ("A2", 1.0), ("A3", 0.9), ("A4", 1.6)]), ("2", [("B2", 1.0), ("B4", 1.5)]),
          ("3", [("C1", 1.6), ("C2", 2.0), ("C3", 2.2)]), ("4", [("D", 3.4)]), ("5", [("E", 3.8)])]

COVER = lambda: cover("POV: één appje, en het is weer ruzie.", [("De gymtas was weer vergeten.", False, "Ex"), ("Altijd moet ik alles doen!!", True, None)])

if __name__ == "__main__":
    work = sys.argv[1]; out = sys.argv[2]
    save_frames(frames, f"{work}/frames")
    save_cover(COVER(), out.replace(".mp4", "-cover.jpg") if out.endswith(".mp4") else f"{work}/cover.jpg")
    if "--sheet" in sys.argv: contact_sheet(f"{work}/frames", ["A4", "B4", "C1", "C2", "C3", "D", "E"], f"{work}/sheet.png")
    else: render_reel(scenes, f"{work}/frames", f"{work}/parts", out)
