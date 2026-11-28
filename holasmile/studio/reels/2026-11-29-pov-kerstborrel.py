import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from holasmile_motion import *

# Reeks: Humor / herkenbaar (POV), MET BEWEGING. Strateeg: tweede feestdagenreel met humor en een herkenbaar verhaal, haak in de eerste seconde.
# Opbouw: POV kerstborrel + vragen van collega's die binnenploppen -> jij: 'nee hoor...' -> het geheim (kleurwaaier schuift naar wit)
# -> uitleg één afspraak -> afsluiter. Elke tekst minstens 2,5 s in beeld (alle tekst staat er uiterlijk 0,9 s na de start van een scene). Geen sfeerbeeld.
SP = [(170, 330, 22), (910, 360, 16), (920, 1520, 18), (150, 1460, 14)]


def bubble(d, x, y, name, text, s=1.0, right=False):
    """Chatbubbel in de familie-app; s = schaal voor het binnenploppen."""
    if s <= 0: return
    fn, ft = sans(int(28 * s), "Medium"), sans(int(40 * s))
    w = max(d.textlength(text, font=ft), d.textlength(name, font=fn)) + 70 * s; h = 140 * s
    x0 = x - w if right else x
    d.rounded_rectangle((x0, y, x0 + w, y + h), int(34 * s), fill=GOLD if right else BG2, outline=(84, 70, 48), width=2)
    d.text((x0 + 35 * s, y + 26 * s), name, font=fn, fill=BG if right else GOLD_L)
    d.text((x0 + 35 * s, y + 68 * s), text, font=ft, fill=BG if right else CREAM)


def phone(d, y0=860, y1=1660):
    d.rounded_rectangle((170, y0, W - 170, y1), 70, fill=CARD, outline=GOLD, width=5)
    d.rounded_rectangle((W / 2 - 80, y0 + 28, W / 2 + 80, y0 + 48), 10, fill=BG)
    d.text((W / 2, y0 + 100), "Familie", font=sans(34, "Medium"), fill=CREAM, anchor="mm")
    d.line((210, y0 + 145, W - 210, y0 + 145), fill=(84, 70, 48), width=2)



def popk(t, start): return 0 if t < start else pop(min(1, (t - start) / 0.25))


def speech(d, x, y, text, s=1.0, right=False):
    """Tekstballon van een collega; s = schaal voor het binnenploppen."""
    if s <= 0: return
    ft = sans(int(44 * s), "Medium")
    w = d.textlength(text, font=ft) + 80 * s; h = 110 * s
    x0 = x - w if right else x
    d.rounded_rectangle((x0, y, x0 + w, y + h), int(40 * s), fill=BG2, outline=GOLD, width=3)
    tx = x0 + (w - 70 * s if right else 60 * s)
    d.polygon([(tx - 18 * s, y + h - 2), (tx + 18 * s, y + h - 2), (tx + (22 if right else -22) * s, y + h + 34 * s)], fill=BG2)
    d.text((x0 + 40 * s, y + h / 2), text, font=ft, fill=CREAM, anchor="lm")


def s1(t, p):  # haak meteen in beeld
    im, d = base()
    kicker(d, 250, "POV")
    big_text(d, 380, "Je komt binnen op\nde kerstborrel", 100, scale=pop(min(1, t / 0.3)))
    speech(d, 130, 860, "Was je op vakantie?", popk(t, 0.3))
    speech(d, W - 130, 1100, "Nieuwe kapper?", popk(t, 0.6), right=True)
    speech(d, 130, 1340, "Je ziet er zo fris uit!", popk(t, 0.9))
    twinkle(d, t, SP[:2]); wordmark(d); return im


def s2(t, p):
    im, d = base()
    dx = int((1 - ease(t / 0.35)) * 500)
    ctext(d, 420, "Jij:", serif_i(80, "Medium"), fill=GOLD_L, cx=W / 2 + dx)
    big_text(d, 560, "\u201cNee hoor,\ngewoon uitgerust.\u201d", 100, scale=pop(min(1, max(0, t - 0.2) / 0.3)))
    if t > 0.6:
        ctext(d, 1120, "(en je lacht net\niets breder dan vorig jaar)", serif_i(60, "Medium"), fill=MUTED, maxw=900)
    sparkle(d, W / 2, 1500, 30 + 10 * math.sin(t * 6))
    twinkle(d, t, SP); wordmark(d); return im


def s3(t, p):  # het geheim: kleurwaaier schuift naar wit
    im, d = base()
    kicker(d, 260, "Het geheim")
    big_text(d, 390, "Je liet je tanden\nbleken bij Hola Smile.", 92, scale=pop(min(1, t / 0.3)))
    shade_slider(d, 860, 0.5 + 5.5 * ease((t - 0.3) / 1.4))
    if t > 0.5:
        ctext(d, 1270, "Resultaten verschillen per persoon.", sans(42), fill=MUTED)
    twinkle(d, t, SP[2:]); wordmark(d); return im


def shade_slider(d, y, pos, w=820, cx=W / 2):
    n = len(SHADES); gap = 16; tw = (w - gap * (n - 1)) / n; x0 = cx - w / 2
    for i, c in enumerate(SHADES):
        x = x0 + i * (tw + gap)
        d.rounded_rectangle((x, y, x + tw, y + 190), int(tw / 2), fill=c)
    x = x0 + pos * (tw + gap)
    d.rounded_rectangle((x - 6, y - 6, x + tw + 6, y + 196), int(tw / 2) + 6, outline=GOLD_L, width=6)
    mx = x + tw / 2
    d.polygon([(mx - 18, y + 250), (mx + 18, y + 250), (mx, y + 222)], fill=GOLD_L)


def s4(t, p):
    im, d = base()
    kicker(d, 260, "Zo werkt het")
    big_text(d, 390, "In één afspraak,\nvoor de feestdagen.", 96, scale=pop(min(1, t / 0.3)))
    shade_guide(d, 820, active=5, w=820, labels=False)
    if t > 0.4:
        ctext(d, 1160, "Rondes van 20 minuten\nonder de nieuwste LED-lamp.", sans(50), fill=MUTED, maxw=900)
    twinkle(d, t, SP[:2]); wordmark(d); return im


scenes = [(3.6, s1), (3.2, s2), (3.4, s3), (3.2, s4), (3.4, cta_motion)]

COVER = lambda: cover("De kerstborrel", sub="Was je op\nvakantie?", kick="POV", shade=5)

if __name__ == "__main__":
    work = sys.argv[1]; out = sys.argv[2]
    COVER().save(out.replace(".mp4", "-cover.jpg") if out.endswith(".mp4") else f"{work}/cover.jpg", "JPEG", quality=90)
    if "--sheet" in sys.argv:
        os.makedirs(work, exist_ok=True)
        still_sheet(scenes, [(0, 0.0), (0, 0.2), (0, 1), (1, 0.1), (1, 1), (2, 0.1), (2, 1), (3, 1), (4, 1)], f"{work}/sheet.png")
    else: render_motion(scenes, out, work)
