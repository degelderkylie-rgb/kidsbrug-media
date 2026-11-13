import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from holasmile_motion import *

# Reeks: Mythe of feit, MET BEWEGING (feedback Kylie: trager, elke tekst minstens 2,5 s in beeld).
# Opbouw: stelling knalt erin -> stempel MYTHE slaat erop -> kleurwaaier schuift van geel naar wit -> wat wél helpt -> afsluiter.
CLAIM = "Whitening tandpasta maakt je tanden witter."
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


def s1(t, p):  # haak: stelling knalt erin, stempel MYTHE slaat erop
    im, d = base()
    kicker(d, 300, "Mythe of feit?")
    big_text(d, 520, CLAIM, 92, scale=pop(min(1, t / 0.3)), maxw=880)
    if t > 1.0:
        k = ease((t - 1.0) / 0.25); s = 1 + 1.2 * (1 - k)
        f = serif(int(110 * s), "Bold"); tw = d.textlength("MYTHE", font=f) + 100 * s; hh = 170 * s; cy = 1080
        d.rounded_rectangle((W / 2 - tw / 2, cy - hh / 2, W / 2 + tw / 2, cy + hh / 2), 26, outline=RED, width=8)
        d.text((W / 2, cy + 4), "MYTHE", font=f, fill=RED, anchor="mm")
        ctext(d, 1260, "Nou ja… grotendeels.", serif_i(58), fill=GOLD_L)
    twinkle(d, t, SP); wordmark(d); return im


def s2(t, p):  # kleurwaaier schuift van geel naar wit
    im, d = base()
    ctext(d, 260, "Whitening tandpasta poetst\nvooral aanslag weg.", serif(66, "SemiBold"))
    pos = 1.0 if t < 1.4 else 1.0 + 4.0 * ease((t - 1.4) / 1.0)
    shade_slider(d, 640, pos)
    ctext(d, 1000, "De kleur van je tand zelf\nverandert nauwelijks.", sans(42), fill=MUTED)
    if t > 1.4:
        big_text(d, 1240, "Professioneel bleken\nwerkt aan die kleur.", 70, scale=pop(min(1, (t - 1.4) / 0.3)))
    twinkle(d, t, SP[:2]); wordmark(d); return im


def s3(t, p):  # wat wél helpt, punten één voor één
    im, d = base()
    kicker(d, 300, "Wat wél helpt")
    items = ["Spoel met water na koffie of thee", "Wacht even met poetsen na iets zuurs",
             "Professioneel bleken voor diepere verkleuring"]
    y = 470
    for i, it in enumerate(items):
        if t <= i * 0.35: break
        dx = int((1 - ease((t - i * 0.35) / 0.3)) * 600)
        f = serif(50); lines = wrap(d, it, f, 650); h = max(110, int(40 + len(lines) * f.size * 1.25))
        x = 150 + dx; cy = y + h / 2
        d.ellipse((x, cy - 45, x + 90, cy + 45), outline=GOLD, width=3)
        d.text((x + 45, cy), str(i + 1), font=serif(46, "SemiBold"), fill=GOLD_L, anchor="mm")
        ty = cy - len(lines) * f.size * 1.25 / 2
        for j, l in enumerate(lines): d.text((x + 130, ty + j * f.size * 1.25), l, font=f, fill=CREAM, anchor="la")
        y += h + 40
    twinkle(d, t, SP[2:]); wordmark(d); return im


scenes = [(3.6, s1), (4.0, s2), (3.4, s3), (3.4, cta_motion)]

COVER = lambda: cover("Maakt whitening tandpasta je tanden witter?", kick="Mythe of feit", shade=2)

if __name__ == "__main__":
    work = sys.argv[1]; out = sys.argv[2]
    COVER().save(out.replace(".mp4", "-cover.jpg") if out.endswith(".mp4") else f"{work}/cover.jpg", "JPEG", quality=90)
    if "--sheet" in sys.argv:
        os.makedirs(work, exist_ok=True)
        still_sheet(scenes, [(0, 0.0), (0, 0.15), (0, 1), (1, 0.2), (1, 1), (2, 0.1), (2, 1), (3, 1)], f"{work}/sheet.png")
    else: render_motion(scenes, out, work)
