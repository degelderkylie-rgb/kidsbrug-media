import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from holasmile_style import *

# Reeks: Mythe of feit. Opbouw: haak (stelling) -> stempel -> uitleg met kleurwaaier -> wat wel helpt -> afsluiter.
CLAIM = "Whitening tandpasta maakt je tanden witter."


def sA(stamped):
    im, d = base()
    kicker(d, 380, "Mythe of feit?")
    ctext(d, 540, "Bijna iedereen gelooft dit…", serif(72, "SemiBold"))
    y = quote_card(d, 780, CLAIM)
    if stamped:
        stamp(d, y + 110, "MYTHE")
        ctext(d, y + 330, "Nou ja… grotendeels.", serif_i(52), fill=GOLD_L)
    for x, yy, r in [(170, 420, 18), (910, 450, 12)]: sparkle(d, x, yy, r)
    wordmark(d); return im


def sB(n):
    im, d = base()
    ctext(d, 340, "Wat whitening tandpasta wél doet:", serif(70, "SemiBold"))
    ctext(d, 550, "Het poetst aanslag aan de buitenkant weg.", sans(42), fill=MUTED, maxw=820)
    shade_guide(d, 780, active=1, w=820, labels=False)
    if n >= 2:
        ctext(d, 1180, "Maar de kleur van je tand zelf\nverandert er nauwelijks door.", serif(58, "SemiBold"), fill=CREAM)
        ctext(d, 1420, "Koffie, thee, roken en leeftijd\nzitten dieper.", serif_i(48), fill=GOLD_L)
    wordmark(d); return im


def sC():
    im, d = base()
    ctext(d, 320, "Met een professionele\nbleekbehandeling", serif(70, "SemiBold"))
    shade_guide(d, 720, active=5, w=820, labels=False)
    ctext(d, 1140, "werk je ook aan de\nverkleuring zelf.", serif(64, "SemiBold"))
    ctext(d, 1400, "Bij ons in 40 minuten,\nterwijl jij ontspant in een massagestoel.", sans(38), fill=MUTED, maxw=860)
    wordmark(d); return im


def sD():
    im, d = base()
    kicker(d, 360, "Wat wél helpt")
    ctext(d, 480, "Langer genieten van je glimlach", serif(66, "SemiBold"))
    listing(d, 760, ["Spoel met water na koffie of thee", "Wacht 30 min met poetsen na iets zuurs",
                     "Een professionele behandeling voor diepere verkleuring"])
    wordmark(d); return im


frames = {"A1": lambda: sA(False), "A2": lambda: sA(True), "B1": lambda: sB(1), "B2": lambda: sB(2),
          "C": sC, "D": sD, "E": cta}
scenes = [("1", [("A1", 2.4), ("A2", 2.2)]), ("2", [("B1", 1.6), ("B2", 2.6)]),
          ("3", [("C", 3.0)]), ("4", [("D", 3.6)]), ("5", [("E", 3.6)])]

COVER = lambda: cover("Maakt whitening tandpasta je tanden witter?", kick="Mythe of feit", shade=2)

if __name__ == "__main__":
    work = sys.argv[1]; out = sys.argv[2]
    save_frames(frames, f"{work}/frames")
    save_cover(COVER(), out.replace(".mp4", "-cover.jpg") if out.endswith(".mp4") else f"{work}/cover.jpg")
    if "--sheet" in sys.argv: contact_sheet(f"{work}/frames", ["A1", "A2", "B2", "C", "D", "E"], f"{work}/sheet.png")
    else: render_reel(scenes, f"{work}/frames", f"{work}/parts", out)
