import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from kidsbrug_style import *

# Feedback Kylie (12 nov): "de tekst past niet volledig op het scherm".
# Daarom: kortere teksten, kleinere letters en ruimere marges, zodat alles ook in een
# vierkante uitsnede (dashboard, Facebook) en het 3:4-profielraster ruim binnen beeld blijft.
T = 7
POINTS = [
    ("Jullie zien hetzelfde", "Eén kalender, één kostenoverzicht, één map met documenten."),
    ("Wijzigen gaat samen", "Een wissel verandert niet stilletjes. De ander zegt ja of nee."),
    ("Niets verdwijnt", "Niemand kan achteraf iets wissen. Ook jij niet."),
    ("Een rustige toon", "Een berichtenfilter houdt berichten rustig, ook op een slechte dag."),
    ("Geen rechter", "Voor juridisch advies ga je naar een bemiddelaar of advocaat."),
]
M, MW = 150, 780  # marge links en maximale tekstbreedte


def point(n, total, title, body):
    im, d = cbase()
    tf, bf = serif(66, "SemiBold"), sans(40)
    tl, bl = wrap(d, title, tf, MW), wrap(d, body, bf, MW)
    h = 110 + 50 + len(tl) * tf.size * 1.18 + 36 + len(bl) * bf.size * 1.45
    y = (CH - h) / 2 - 20
    d.ellipse((M, y, M + 110, y + 110), fill=SAGE)
    d.text((M + 55, y + 55), "✓", font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 54), fill=DARK, anchor="mm")
    y = cwrap_text(d, M, y + 160, title, tf, maxw=MW, gap=1.18)
    cwrap_text(d, M, y + 36, body, bf, fill=MUTED, maxw=MW, gap=1.45)
    cfooter(d, n, total); return im


slides = [lambda: slide_cover("KidsBrug kiest\ngeen kant.", "Eerlijk voor jullie allebei", kicker="Vertrouwen", total=T)]
for i, (t, b) in enumerate(POINTS):
    slides.append(lambda i=i, t=t, b=b: point(i + 2, T, t, b))
slides.append(lambda: slide_closing(T, T, "Twee ouders.\nEén kind dat rust verdient."))

if __name__ == "__main__":
    paths = save_carousel(slides, sys.argv[1])
    if len(sys.argv) > 2: carousel_sheet(paths, sys.argv[2])
    print("\n".join(paths))
