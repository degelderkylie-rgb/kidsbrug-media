import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from holasmile_motion import *

# Reeks: Humor / herkenbaar (POV), MET BEWEGING. Strateeg: feestdagenreel met humor en een herkenbaar verhaal, haak in de eerste seconde.
# Opbouw: POV + familie-app met berichtjes die binnenploppen -> iedereen kijkt naar de boom -> jij zoomt in op je tanden (vergrootglas
# over de kleurwaaier) -> dit jaar lach je voluit (waaier schuift naar wit) -> afsluiter. Elke tekst minstens 2,5 s in beeld. Geen sfeerbeeld.
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


def s1(t, p):  # haak meteen in beeld
    im, d = base()
    kicker(d, 250, "POV")
    big_text(d, 380, "De kerstfoto's\nkomen binnen", 104, scale=pop(min(1, t / 0.3)))
    phone(d)
    bubble(d, 220, 1040, "Tante Ria", "24 foto's", popk(t, 0.4))
    bubble(d, 220, 1220, "Mama", "Wat een mooie dag!", popk(t, 1.0))
    bubble(d, W - 220, 1400, "Jij", "Even kijken...", popk(t, 1.6), right=True)
    twinkle(d, t, SP[:2]); wordmark(d); return im


def s2(t, p):
    im, d = base()
    dx = int((1 - ease(t / 0.35)) * 500)
    ctext(d, 330, "Iedereen kijkt\nnaar de kerstboom.", serif(96, "SemiBold"), cx=W / 2 + dx)
    # eenvoudige gouden kerstboom die opbouwt
    for i in range(4):
        k = ease((t - 0.3 - i * 0.18) / 0.3)
        if k <= 0: continue
        top = 760 + i * 150; half = 120 + i * 85
        d.polygon([(W / 2, top), (W / 2 - half * k, top + 230), (W / 2 + half * k, top + 230)], fill=GOLD if i % 2 else GOLD_L)
    if t > 1.0:
        d.rectangle((W / 2 - 40, 1440, W / 2 + 40, 1520), fill=(120, 90, 50)); sparkle(d, W / 2, 735, 40)
    twinkle(d, t, SP); wordmark(d); return im


def s3(t, p):  # vergrootglas over de kleurwaaier
    im, d = base()
    big_text(d, 300, "Jij zoomt meteen\nin op je tanden.", 96, scale=pop(min(1, t / 0.3)))
    shade_guide(d, 900, active=None, w=820, labels=False)
    n = len(SHADES); tw = (820 - 16 * (n - 1)) / n; x0 = W / 2 - 410
    pos = 3.0 - 2.5 * ease((t - 0.3) / 1.2)  # schuift naar de gele kant
    cx = x0 + pos * (tw + 16) + tw / 2; cy = 995
    r = 150; d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=GOLD_L, width=12)
    d.line((cx + r * 0.7, cy + r * 0.7, cx + r * 1.4, cy + r * 1.4), fill=GOLD_L, width=26)
    if t > 0.5:
        ctext(d, 1330, "Herkenbaar?", serif_i(76), fill=GOLD_L)
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
    kicker(d, 260, "Dit jaar")
    big_text(d, 390, "lach je gewoon\nvoluit.", 104, scale=pop(min(1, t / 0.3)))
    shade_slider(d, 760, 0.5 + 5.5 * ease((t - 0.3) / 1.3))
    if t > 0.4:
        ctext(d, 1150, "Tanden bleken in één afspraak,\nmet rondes van 20 minuten\nonder de LED-lamp.", sans(50), fill=MUTED, maxw=900)
    twinkle(d, t, SP[:2]); wordmark(d); return im


scenes = [(3.4, s1), (3.0, s2), (3.0, s3), (3.2, s4), (3.4, cta_motion)]

COVER = lambda: cover("POV: de kerstfoto's\nkomen binnen", sub="en jij zoomt in\nop je tanden", kick="Herkenbaar?", shade=1)

if __name__ == "__main__":
    work = sys.argv[1]; out = sys.argv[2]
    COVER().save(out.replace(".mp4", "-cover.jpg") if out.endswith(".mp4") else f"{work}/cover.jpg", "JPEG", quality=90)
    if "--sheet" in sys.argv:
        os.makedirs(work, exist_ok=True)
        still_sheet(scenes, [(0, 0.0), (0, 0.15), (0, 1), (1, 0.1), (1, 1), (2, 0.1), (2, 1), (3, 1), (4, 1)], f"{work}/sheet.png")
    else: render_motion(scenes, out, work)
