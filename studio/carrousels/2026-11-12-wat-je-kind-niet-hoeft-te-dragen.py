import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from kidsbrug_style import *

T = 7
TIPS = [
    ("Geen boodschappen voor de andere ouder", "Je kind is geen postbode. Regel afspraken rechtstreeks met elkaar.",
     "Zeg maar tegen papa dat hij vrijdag op tijd moet zijn."),
    ("Geen vragen over het andere huis", "Vraag hoe het was, niet wat de ander deed of zei.", None),
    ("Geen keuze tussen jullie", "\"Bij wie wil je zijn?\" voelt voor een kind als kiezen tegen iemand.", None),
    ("Geen ruzie waar het bij is", "Ook niet via de telefoon in de keuken. Kinderen horen meer dan je denkt.", None),
    ("Geen zorgen over geld", "Wie wat betaalt, is iets tussen jullie twee.", None),
]

slides = [lambda: slide_cover("5 dingen die je kind níet hoeft te dragen", "na een scheiding", kicker="Tip", total=T)]
for i, (t, b, ex) in enumerate(TIPS):
    slides.append(lambda i=i, t=t, b=b, ex=ex: slide_point(i + 2, T, i + 1, t, b, (f"Niet: “{ex}”" if ex else None)))
slides.append(lambda: slide_closing(T, T, "Minder ruis tussen jullie. Meer rust voor je kind."))

if __name__ == "__main__":
    out = sys.argv[1]  # bv. carrousels/kidsbrug-2026-11-12-wat-je-kind-niet-hoeft-te-dragen
    paths = save_carousel(slides, out)
    if len(sys.argv) > 2: carousel_sheet(paths, sys.argv[2])
    print("\n".join(paths))
