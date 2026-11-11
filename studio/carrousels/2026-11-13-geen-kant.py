import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from kidsbrug_style import *

T = 7
POINTS = [
    ("Jullie zien hetzelfde", "Eén kalender, één kostenoverzicht, één map met documenten. Niemand heeft een eigen versie."),
    ("Wijzigen gaat samen", "Een wissel verandert niet stilletjes. Wil iemand iets wijzigen, dan stuurt die een verzoek en zegt de ander ja of nee."),
    ("Niets verdwijnt", "Afspraken, verzoeken en gesprekken blijven bewaard. Niemand kan achteraf iets wissen. Ook jij niet."),
    ("Een rustige toon", "Een berichtenfilter helpt om berichten rustig en zakelijk te houden, ook op een slechte dag."),
    ("Geen rechter", "KidsBrug helpt jullie afspraken bij te houden. Voor juridisch advies ga je naar een bemiddelaar of advocaat."),
]
slides = [lambda: slide_cover("KidsBrug kiest\ngeen kant.", "Zo blijft het eerlijk voor jullie allebei", kicker="Vertrouwen", total=T)]
for i, (t, b) in enumerate(POINTS):
    slides.append(lambda i=i, t=t, b=b: slide_point(i + 2, T, None, t, b))
slides.append(lambda: slide_closing(T, T, "Eén plek. Twee ouders.\nEén kind dat rust verdient."))

if __name__ == "__main__":
    paths = save_carousel(slides, sys.argv[1])
    if len(sys.argv) > 2: carousel_sheet(paths, sys.argv[2])
    print("\n".join(paths))
