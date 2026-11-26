import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from holasmile_motion import *

# Reeks: Vraag van een klant, MET BEWEGING. Onderwerp: "Is het wel hygiënisch?" (nog niet aan bod in de laatste 14 dagen).
# Opbouw: vraagkaart knalt erin -> verzegeld zakje 'NIEUW' schuift binnen (nieuwe mondspreider per klant)
# -> 'Zo werken wij' met punten één voor één -> afsluiter. Elke tekst minstens 2,5 s in beeld. Geen sfeerbeeld, geen gezichten.
SP = [(170, 330, 22), (910, 360, 16), (920, 1520, 18), (150, 1460, 14)]


def s1(t, p):  # haak: de vraag knalt meteen in beeld
    im, d = base()
    kicker(d, 300, "Vraag van een klant")
    s = pop(min(1, t / 0.3))
    f = serif_i(int(80 * s), "Medium")
    ctext(d, 560, "“Is tanden bleken\nbij jullie wel\nhygiënisch?”", f, maxw=900)
    if t > 0.9:
        k = ease((t - 0.9) / 0.4)
        ctext(d, 1130 + int((1 - k) * 80), "Goeie vraag.", serif(70, "SemiBold"), fill=GOLD_L)
        ctext(d, 1260 + int((1 - k) * 80), "Dit is ons antwoord.", sans(46), fill=MUTED)
    twinkle(d, t, SP); wordmark(d); return im


def pack(d, cx, cy, s=1.0):
    """Verzegeld zakje met een mondspreider-silhouet en label NIEUW."""
    w, h = 520 * s, 380 * s
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), int(40 * s), fill=CARD, outline=GOLD, width=5)
    for i in range(9):  # gekartelde sealrand bovenaan
        x = cx - w / 2 + 30 * s + i * (w - 60 * s) / 8
        d.line((x, cy - h / 2 + 22 * s, x + 14 * s, cy - h / 2 + 40 * s), fill=GOLD, width=3)
    # mondspreider: twee bogen
    d.arc((cx - 150 * s, cy - 80 * s, cx + 150 * s, cy + 140 * s), 200, 340, fill=CREAM, width=int(16 * s))
    d.arc((cx - 150 * s, cy - 40 * s, cx + 150 * s, cy + 180 * s), 20, 160, fill=CREAM, width=int(16 * s))
    f = sans(int(34 * s), "Medium"); tw = d.textlength("NIEUW", font=f) + 50 * s
    d.rounded_rectangle((cx + w / 2 - tw - 20 * s, cy - h / 2 + 60 * s, cx + w / 2 - 20 * s, cy - h / 2 + 120 * s), int(30 * s), fill=GOLD)
    d.text((cx + w / 2 - 20 * s - tw / 2, cy - h / 2 + 90 * s), "NIEUW", font=f, fill=BG, anchor="mm")


def s2(t, p):  # nieuwe mondspreider per klant
    im, d = base()
    big_text(d, 340, "Elke klant krijgt\neen nieuwe\nmondspreider.", 90, scale=pop(min(1, t / 0.3)))
    k = ease((t - 0.3) / 0.5)
    if k > 0:
        pack(d, W / 2 + int((1 - k) * 700), 1090, 1.0)
    if t > 0.6:
        ctext(d, 1420, "Uit de verpakking,\nspeciaal voor jou.", serif_i(58), fill=GOLD_L)
    twinkle(d, t, SP[2:]); wordmark(d); return im


def s3(t, p):  # zo werken wij, punten één voor één
    im, d = base()
    kicker(d, 300, "Zo werken wij")
    items = ["Nieuwe mondspreider per klant", "Nieuwste generatie LED-lampen",
             "Rondes van 20 minuten, alles in één afspraak"]
    y = 470
    for i, it in enumerate(items):
        if t <= i * 0.3: break
        dx = int((1 - ease((t - i * 0.3) / 0.3)) * 600)
        f = serif(50); lines = wrap(d, it, f, 700); h = max(110, int(40 + len(lines) * f.size * 1.25))
        x = 110 + dx; cy = y + h / 2
        d.ellipse((x, cy - 45, x + 90, cy + 45), outline=GOLD, width=3)
        d.text((x + 45, cy), str(i + 1), font=serif(46, "SemiBold"), fill=GOLD_L, anchor="mm")
        ty = cy - len(lines) * f.size * 1.25 / 2
        for j, l in enumerate(lines): d.text((x + 130, ty + j * f.size * 1.25), l, font=f, fill=CREAM, anchor="la")
        y += h + 50
    if t > 0.9:
        shade_guide(d, 1200, active=5, w=700, labels=False)
    twinkle(d, t, SP[2:]); wordmark(d); return im


scenes = [(3.4, s1), (3.4, s2), (3.6, s3), (3.4, cta_motion)]

COVER = lambda: cover("Is tanden bleken\nwel hygiënisch?", sub="ons eerlijke antwoord", kick="Vraag van een klant", shade=5)

if __name__ == "__main__":
    work = sys.argv[1]; out = sys.argv[2]
    COVER().save(out.replace(".mp4", "-cover.jpg") if out.endswith(".mp4") else f"{work}/cover.jpg", "JPEG", quality=90)
    if "--sheet" in sys.argv:
        os.makedirs(work, exist_ok=True)
        still_sheet(scenes, [(0, 0.0), (0, 0.15), (0, 1), (1, 0.1), (1, 1), (2, 0.1), (2, 1), (3, 1)], f"{work}/sheet.png")
    else: render_motion(scenes, out, work)
