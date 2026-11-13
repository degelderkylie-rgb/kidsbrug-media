import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from holasmile_motion import *

# Reeks: Vraag van een klant — "Hoe lang duurt tanden bleken?" MET BEWEGING, elke tekst minstens 2,5 s in beeld.
# Feiten (STUDIO.md): één afspraak, rondes van 20 min, Pakket 1 = 1 ronde, Pakket 2 = 3 rondes, Pakket 3 = 4 rondes.
# NOOIT een totale duur of "40 minuten" noemen.
SP = [(170, 330, 22), (910, 360, 16), (900, 1500, 18), (160, 1450, 14)]


def s1(t, p):  # haak: de vraag knalt erin
    im, d = base()
    kicker(d, 420, "Vraag van een klant")
    big_text(d, 600, "Hoe lang duurt\ntanden bleken?", 112, scale=pop(min(1, t / 0.3)))
    # vraagteken-kaartje wiebelt
    a = math.sin(t * 5) * 6
    d.text((W / 2 + a, 1150), "?", font=serif(220, "SemiBold"), fill=GOLD, anchor="mm")
    twinkle(d, t, SP); wordmark(d); return im


def s2(t, p):  # één afspraak
    im, d = base()
    big_text(d, 560, "Alles gebeurt in\néén afspraak.", 100, scale=pop(min(1, t / 0.3)))
    ctext(d, 900, "bij Hola Smile Clinic in Zundert", serif_i(52), fill=GOLD_L)
    shade_guide(d, 1100, active=min(6, int(t / 0.35)), w=760, labels=False)
    twinkle(d, t, SP); wordmark(d); return im


def s3(t, p):  # rondes van 20 minuten: gouden ring loopt vol
    im, d = base()
    big_text(d, 330, "Je bleekt in rondes\nvan 20 minuten", 84, scale=pop(min(1, t / 0.3)))
    cx, cy, r = W / 2, 1000, 230
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(70, 58, 40), width=22)
    k = ease(min(1, t / 2.4))
    if k > 0: d.arc((cx - r, cy - r, cx + r, cy + r), -90, -90 + 360 * k, fill=GOLD, width=22)
    d.text((cx, cy - 20), f"{int(round(20 * k))}", font=serif(150, "SemiBold"), fill=CREAM, anchor="mm")
    d.text((cx, cy + 90), "MIN", font=sans(36, "Medium"), fill=GOLD_L, anchor="mm")
    ctext(d, 1340, "onder de nieuwste LED-lamp", serif_i(52), fill=GOLD_L)
    twinkle(d, t, SP[2:]); wordmark(d); return im


PAKKETTEN = [("Pakket 1", 1), ("Pakket 2", 3), ("Pakket 3", 4)]


def s4(t, p):  # pakketten komen één voor één binnen, rondes als bolletjes
    im, d = base()
    kicker(d, 300, "Hoeveel rondes?")
    y = 470
    for i, (naam, n) in enumerate(PAKKETTEN):
        t0 = i * 0.4
        if t <= t0: break
        dx = int((1 - ease((t - t0) / 0.3)) * 700)
        card(d, (140 + dx, y, 940 + dx, y + 190))
        d.text((200 + dx, y + 70), naam, font=serif(56, "SemiBold"), fill=CREAM, anchor="lm")
        d.text((200 + dx, y + 140), f"{n} {'ronde' if n == 1 else 'rondes'} van 20 min", font=sans(34), fill=MUTED, anchor="lm")
        for j in range(n):
            s = pop(min(1, max(0, (t - t0 - 0.3 - j * 0.12) / 0.25)))
            if t - t0 - 0.3 - j * 0.12 <= 0: continue
            bx = 870 + dx - j * 62; rr = 22 * s
            d.ellipse((bx - rr, y + 95 - rr, bx + rr, y + 95 + rr), fill=GOLD)
        y += 230
    if t > 0.8:
        ctext(d, 1220, "Welk pakket bij jou past,\nbekijken we samen.", serif(58, "SemiBold"))
        ctext(d, 1430, "Resultaat verschilt per persoon.", sans(32), fill=MUTED)
    twinkle(d, t, SP[2:]); wordmark(d); return im


scenes = [(2.6, s1), (2.6, s2), (3.0, s3), (4.0, s4), (3.4, cta_motion)]

COVER = lambda: cover("Hoe lang duurt tanden bleken?", kick="Vraag van een klant", shade=4)

if __name__ == "__main__":
    work = sys.argv[1]; out = sys.argv[2]
    COVER().save(out.replace(".mp4", "-cover.jpg") if out.endswith(".mp4") else f"{work}/cover.jpg", "JPEG", quality=90)
    if "--sheet" in sys.argv:
        os.makedirs(work, exist_ok=True)
        still_sheet(scenes, [(0, 0.0), (0, 1), (1, 0.5), (2, 0.3), (2, 1), (3, 0.15), (3, 1), (4, 1)], f"{work}/sheet.png")
    else: render_motion(scenes, out, work)
