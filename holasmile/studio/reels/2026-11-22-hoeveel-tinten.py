import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from holasmile_motion import *

# Reeks: Vraag van een klant — "Hoeveel tinten lichter word ik?" MET BEWEGING, elke tekst minstens 2,5 s in beeld.
# Feiten (STUDIO.md): Pakket 1 = 1 ronde van 20 min, gemiddeld 2-4 tinten lichter; "tot 10 tinten lichter" alleen met
# "resultaat verschilt per persoon". Geen totale duur, geen prijzen. Geen sfeerbeelden (die zitten deze week al op 2).
SP = [(170, 330, 22), (910, 360, 16), (900, 1500, 18), (160, 1450, 14)]


def shade_slider(d, y, pos, w=820, cx=W / 2):
    """Kleurwaaier met een gouden markering die vloeiend naar positie pos (0..6) schuift."""
    n = len(SHADES); gap = 16; tw = (w - gap * (n - 1)) / n; x0 = cx - w / 2
    for i, c in enumerate(SHADES):
        x = x0 + i * (tw + gap)
        d.rounded_rectangle((x, y, x + tw, y + 190), int(tw / 2), fill=c)
    x = x0 + pos * (tw + gap)
    d.rounded_rectangle((x - 6, y - 6, x + tw + 6, y + 196), int(tw / 2) + 6, outline=GOLD_L, width=6)
    mx = x + tw / 2
    d.polygon([(mx - 18, y + 250), (mx + 18, y + 250), (mx, y + 222)], fill=GOLD_L)


def s1(t, p):  # haak: de vraag knalt erin, markering wiebelt over de waaier
    im, d = base()
    kicker(d, 300, "Vraag van een klant")
    big_text(d, 470, "Hoeveel tinten\nlichter word ik?", 100, scale=pop(min(1, t / 0.3)))
    shade_slider(d, 880, 3 + 2.6 * math.sin(t * 2.2))
    if t > 0.6:
        ctext(d, 1270, "Het eerlijke antwoord:", serif_i(60), fill=GOLD_L)
    twinkle(d, t, SP); wordmark(d); return im


def s2(t, p):  # het hangt af van je startkleur
    im, d = base()
    big_text(d, 420, "Dat hangt af van\nje startkleur.", 100, scale=pop(min(1, t / 0.3)))
    shade_slider(d, 860, 0)
    if t > 0.5:
        ctext(d, 1260, "Iedereen begint\nergens anders.", serif_i(60), fill=GOLD_L)
    twinkle(d, t, SP[2:]); wordmark(d); return im


def s3(t, p):  # 1 ronde: gemiddeld 2-4 tinten
    im, d = base()
    kicker(d, 300, "Pakket 1")
    big_text(d, 450, "1 ronde van 20 min", 84, scale=pop(min(1, t / 0.3)))
    shade_slider(d, 700, 3.0 * ease((t - 0.3) / 1.4))
    if t > 0.4:
        dx = int((1 - ease((t - 0.4) / 0.35)) * 500)
        ctext(d, 1090, "gemiddeld", serif_i(58), fill=GOLD_L, cx=W / 2 + dx)
        ctext(d, 1210, "2 tot 4 tinten lichter", serif(80, "SemiBold"), cx=W / 2 + dx)
    twinkle(d, t, SP[:2]); wordmark(d); return im


def s4(t, p):  # meer rondes: tot 10 tinten, met de verplichte zin
    im, d = base()
    kicker(d, 300, "Meer rondes?")
    big_text(d, 450, "Tot 10 tinten\nlichter", 104, scale=pop(min(1, t / 0.3)))
    shade_slider(d, 760, 3.0 + 3.0 * ease((t - 0.3) / 1.2))
    if t > 0.5:
        ctext(d, 1150, "Resultaat verschilt per persoon.", sans(40, "Medium"), fill=CREAM)
        ctext(d, 1290, "Welk pakket bij jou past,\nbekijken we samen.", serif(56, "SemiBold"))
    twinkle(d, t, SP[2:]); wordmark(d); return im


scenes = [(3.0, s1), (3.0, s2), (3.2, s3), (3.4, s4), (3.4, cta_motion)]

COVER = lambda: cover("Hoeveel tinten\nlichter word ik?", kick="Vraag van een klant", shade=5)

if __name__ == "__main__":
    work = sys.argv[1]; out = sys.argv[2]
    COVER().save(out.replace(".mp4", "-cover.jpg") if out.endswith(".mp4") else f"{work}/cover.jpg", "JPEG", quality=90)
    if "--sheet" in sys.argv:
        os.makedirs(work, exist_ok=True)
        still_sheet(scenes, [(0, 0.0), (0, 1), (1, 0.1), (1, 1), (2, 0.2), (2, 1), (3, 1), (4, 1)], f"{work}/sheet.png")
    else: render_motion(scenes, out, work)
