import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from holasmile_style import *

# Soort: Tips (bewaarwaardig). 6 slides: omslag, 4 punten, afsluiter.
T = 6
POINTS = [
    ("Drink met een rietje", "Koude koffie of ijsthee? Met een rietje raakt minder kleur je tanden."),
    ("Spoel direct met water", "Een slok water na je koffie spoelt het meeste weg."),
    ("Niet meteen poetsen", "Wacht ongeveer 30 minuten na iets zuurs, zodat je glazuur tot rust komt."),
    ("Plan een opfrisser", "Drink je dagelijks koffie? Dan zie je verkleuring sneller terugkomen."),
]

slides = [lambda: slide_cover("Koffie zonder\ngele tanden?", "4 tips die echt helpen", kick="Bewaar deze post", total=T)]
for i, (t, b) in enumerate(POINTS):
    slides.append(lambda i=i, t=t, b=b: slide_point(i + 2, T, i + 1, t, b))
slides.append(lambda: slide_closing(T, T, "Toch al verkleurd?\nDaar helpen wij je mee."))

if __name__ == "__main__":
    paths = save_carousel(slides, sys.argv[1])
    if len(sys.argv) > 2: carousel_sheet(paths, sys.argv[2])
    print("\n".join(paths))
