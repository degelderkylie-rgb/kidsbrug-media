import sys, os, glob; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from holasmile_motion import *

# Sinterklaas-reel: twee clips van Kylie (Sint in de stoel onder de LED-lamp, Sint met duim omhoog) + Hola-afsluiter.
# Clips staan als losse frames (30 fps, 1080x1920) in <framedir>/c1 en c2. Tekst onderaan, nooit over het gezicht.
FR = sys.argv[3] if len(sys.argv) > 3 and not sys.argv[3].startswith("--") else "."
C1 = sorted(glob.glob(os.path.join(FR, "c1", "*.jpg")))
C2 = sorted(glob.glob(os.path.join(FR, "c2", "*.jpg")))

g = Image.new("L", (1, H))
for y in range(H): g.putpixel((0, y), int(min(225, max(0, (y - 1150) * 0.42))))
SHADE = g.resize((W, H))


def clip(frames, t):
    im = Image.open(frames[min(len(frames) - 1, int(t * FPS))]).convert("RGB")
    im.paste(Image.new("RGB", (W, H), BG), (0, 0), SHADE)
    return im, ImageDraw.Draw(im)


def s1(t, p):  # haak: Sint ligt in onze stoel
    im, d = clip(C1, t)
    kicker(d, 1390, "Bezoek in Zundert")
    big_text(d, 1480, "Kijk wie er in\nonze stoel lag…", 92, scale=pop(min(1, t / 0.3)))
    twinkle(d, t, [(150, 1420, 18), (930, 1440, 22)]); return im


def s2(t, p):  # duim omhoog
    im, d = clip(C2, t)
    big_text(d, 1440, "Goedgekeurd\ndoor de Sint!", 100, scale=pop(min(1, t / 0.3)))
    twinkle(d, t, [(140, 1380, 20), (940, 1400, 24), (900, 1760, 14)]); return im


def s3(t, p):  # pakjesavond
    im, d = base()
    kicker(d, 360, "Pakjesavond")
    big_text(d, 470, "Ook stralend\naan tafel op\n5 december?", 100, scale=pop(min(1, t / 0.3)))
    n = len(SHADES); w = 760; gap = 16; tw = (w - gap * (n - 1)) / n; x0 = W / 2 - w / 2
    for i, c in enumerate(SHADES):
        k = ease((t - 0.3 - i * 0.09) / 0.25)
        if k <= 0: continue
        x = x0 + i * (tw + gap); hh = 190 * k
        d.rounded_rectangle((x, 1060 + 190 - hh, x + tw, 1250), int(tw / 2), fill=c)
    ctext(d, 1380, "Plan je afspraak op tijd.", serif_i(60), fill=GOLD_L)
    twinkle(d, t, [(180, 330, 22), (900, 300, 18), (880, 1600, 16)]); wordmark(d); return im


scenes = [(len(C1) / FPS, s1), (len(C2) / FPS, s2), (3.0, s3), (3.8, cta_motion)]


def COVER():
    im, d = clip(C2, 3.2)
    kicker(d, 1300, "Bezoek in Zundert")
    big_text(d, 1390, "De Sint kwam\nlangs!", 100)
    return im


if __name__ == "__main__":
    work = sys.argv[1]; out = sys.argv[2]; os.makedirs(work, exist_ok=True)
    COVER().save(out.replace(".mp4", "-cover.jpg") if out.endswith(".mp4") else f"{work}/cover.jpg", "JPEG", quality=90)
    if "--sheet" in sys.argv:
        still_sheet(scenes, [(0, 0.0), (0, 0.1), (0, 1), (1, 0.1), (1, 0.8), (2, 0.1), (2, 1), (3, 1)], f"{work}/sheet.png")
    else: render_motion(scenes, out, work)
