import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from holasmile_motion import *

# Bewegende voor/na-reel 13 nov, klant06 (uit sjabloon-voor-na-beweging.py).
# De foto's staan NIET in git (privé): haal ze eerst uit het dashboard naar holasmile/fotos/ (zie STUDIO.md).
# Verzin niets over de klant. Foto's nooit bewerken of witter maken.
FOTO = "klant06"
HOOK = "Wacht tot je\nhet NA ziet…"
HERE = os.path.join(os.path.dirname(__file__), "..", "..", "fotos")
V, N = Photo(os.path.join(HERE, f"{FOTO}-voor.jpg")), Photo(os.path.join(HERE, f"{FOTO}-na.jpg"))
CW_ = 1000; CY = 1000  # fotobreedte en verticaal midden


def s1(t, p):  # haak: tekst knalt erin, voor-foto zoomt langzaam in
    im = V.bg.copy(); d = ImageDraw.Draw(im)
    place(im, V.card(CW_, 1.0 + 0.10 * p), W / 2, CY, label="VOOR"); d = ImageDraw.Draw(im)
    big_text(d, 330, HOOK, 104, scale=pop(min(1, t / 0.3)))
    return im


def s2(t, p):  # gouden schuif onthult het na-beeld
    im = V.bg.copy()
    k = ease(p); a, b = V.card(CW_, 1.1), N.card(CW_, 1.1)
    mix = a.copy(); cut = int(b.width * k); mix.paste(b.crop((0, 0, cut, b.height)), (0, 0))
    x, y = place(im, mix, W / 2, CY, label="NA" if k > 0.5 else "VOOR"); d = ImageDraw.Draw(im)
    lx = x + cut; d.line((lx, y - 20, lx, y + b.height + 20), fill=GOLD_L, width=8)
    d.ellipse((lx - 34, CY - 34, lx + 34, CY + 34), fill=GOLD); d.text((lx, CY), "‹ ›", font=sans(30, "Medium"), fill=BG, anchor="mm")
    big_text(d, 330, HOOK, 104)
    return im


def s3(t, p):  # na-beeld, zoom + sparkles
    im = N.bg.copy()
    place(im, N.card(CW_, 1.1 + 0.08 * p), W / 2, CY, label="NA"); d = ImageDraw.Draw(im)
    big_text(d, 330, "Geen filter.", 110, scale=pop(min(1, t / 0.3)))
    big_text(d, 1380, "Echt resultaat.", 64, fill=GOLD_L, italic=True)
    twinkle(d, t, [(170, 760, 30), (930, 740, 22), (900, 1250, 26), (150, 1230, 18)])
    return im


def s4(t, p):  # snel heen en weer: voor / na / voor / na
    na = int(t / 0.28) % 2 == 1
    ph = N if na else V; im = ph.bg.copy()
    place(im, ph.card(CW_, 1.12), W / 2, CY, label="NA" if na else "VOOR"); d = ImageDraw.Draw(im)
    big_text(d, 330, "Nog een keer?", 104)
    return im


def s5(t, p):  # beide onder elkaar
    im, d = base()
    big_text(d, 200, "Voor en na", 96, scale=pop(min(1, t / 0.3)))
    k = ease(t / 0.4)
    place(im, V.card(900), W / 2 - (1 - k) * 600, 640, label="VOOR")
    place(im, N.card(900), W / 2 + (1 - k) * 600, 1180, label="NA"); d = ImageDraw.Draw(im)
    ctext(d, 1500, "Eén afspraak bij Hola Smile Clinic", sans(38, "Medium"), fill=GOLD_L)
    ctext(d, 1565, "Resultaten verschillen per persoon.", sans(30), fill=MUTED)
    wordmark(d); return im


scenes = [(1.6, s1), (1.5, s2), (2.0, s3), (2.3, s4), (2.6, s5), (3.2, cta_motion)]


def COVER():
    im = N.bg.copy(); d = ImageDraw.Draw(im)
    kicker(d, 300, "Echt resultaat")
    big_text(d, 400, "Voor en na", 104)
    place(im, V.card(760), W / 2, 790, r=30, label="VOOR")
    place(im, N.card(760), W / 2, 1250, r=30, label="NA"); d = ImageDraw.Draw(im)
    ctext(d, 1520, "Geen filter", serif_i(54), fill=GOLD_L)
    return im


if __name__ == "__main__":
    work = sys.argv[1]; out = sys.argv[2]
    COVER().save(out.replace(".mp4", "-cover.jpg") if out.endswith(".mp4") else f"{work}/cover.jpg", "JPEG", quality=90)
    if "--sheet" in sys.argv:
        os.makedirs(work, exist_ok=True)
        still_sheet(scenes, [(0, 0.15), (0, 1), (1, 0.5), (2, 0.6), (3, 0.1), (3, 0.5), (4, 1), (5, 1)], f"{work}/sheet.png")
    else: render_motion(scenes, out, work)
