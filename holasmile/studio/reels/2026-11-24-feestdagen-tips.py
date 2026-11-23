import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from holasmile_motion import *

# Reeks: Tips, MET BEWEGING (feedback Kylie: elke tekst minstens 2,5 s in beeld).
# Onderwerp: stralend de feestdagen door (lippenstift, water, op tijd plannen). Opbouw: haak + kleurwaaier schuift naar wit -> 3 tips (nummer knalt erin) -> afsluiter.
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


def s1(t, p):  # haak meteen in beeld, kleurwaaier schuift van geel naar wit
    im, d = base()
    kicker(d, 300, "Feestdagen eraan?")
    big_text(d, 470, "3 tips voor een\nstralende lach", 100, scale=pop(min(1, t / 0.3)))
    pos = 0.5 + 4.5 * ease((t - 0.4) / 1.4)
    shade_slider(d, 860, pos)
    if t > 0.8:
        ctext(d, 1260, "Op elke kerstfoto.", serif_i(60), fill=GOLD_L)
    twinkle(d, t, SP); wordmark(d); return im


def tip(num, title, body):
    def scene(t, p):
        im, d = base()
        kicker(d, 300, f"Tip {num} van 3")
        s = pop(min(1, t / 0.3))
        d.text((W / 2, 560), str(num), font=serif(int(260 * s), "SemiBold"), fill=GOLD_L, anchor="mm")
        rule(d, 740)
        dx = int((1 - ease(t / 0.35)) * 500)
        ctext(d, 850, title, serif(88, "SemiBold"), cx=W / 2 + dx, maxw=940)
        if t > 0.3:
            ctext(d, 1330, body, sans(54), fill=MUTED, maxw=860)
        twinkle(d, t, SP[(num - 1) % 2 * 2:(num - 1) % 2 * 2 + 2]); wordmark(d); return im
    return scene


s2 = tip(1, "Kies lippenstift\nmet een blauwe\nondertoon", "Koel rood of bes laat\nje tanden witter lijken.")
s3 = tip(2, "Drink water\ntussen je glazen", "Een slokje water spoelt kleur\nvan wijn en koffie weg.")
s4 = tip(3, "Plan je\nbleekafspraak\nop tijd", "Eén afspraak, rondes van\n20 minuten onder de LED-lamp.")

scenes = [(3.6, s1), (3.0, s2), (3.0, s3), (3.0, s4), (3.4, cta_motion)]

COVER = lambda: cover("Feestdagen eraan?\n3 tips voor een\nstralende lach", kick="Tips", shade=5)

if __name__ == "__main__":
    work = sys.argv[1]; out = sys.argv[2]
    COVER().save(out.replace(".mp4", "-cover.jpg") if out.endswith(".mp4") else f"{work}/cover.jpg", "JPEG", quality=90)
    if "--sheet" in sys.argv:
        os.makedirs(work, exist_ok=True)
        still_sheet(scenes, [(0, 0.0), (0, 0.15), (0, 1), (1, 0.05), (1, 1), (2, 1), (3, 1), (4, 1)], f"{work}/sheet.png")
    else: render_motion(scenes, out, work)
