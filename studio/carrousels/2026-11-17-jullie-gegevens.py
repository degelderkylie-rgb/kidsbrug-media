import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from kidsbrug_style import *

T = 7
POINTS = [
    ("Opgeslagen in de EU", "Alles wat jullie in KidsBrug zetten, staat versleuteld op servers in de Europese Unie."),
    ("Alleen jullie twee", "Jullie gezin is van jullie. Alleen de ouders die samen een gezin delen, kunnen erin."),
    ("Je nummer blijft privé", "Je belt met elkaar via KidsBrug, zonder je telefoonnummer te delen."),
    ("Niets verdwijnt stilletjes", "Afspraken, verzoeken en gesprekken blijven bewaard. Niemand kan achteraf iets wissen. Ook jij niet."),
    ("Geen vervanging voor advies", "KidsBrug helpt jullie afspraken bij te houden. Voor juridisch advies ga je naar een bemiddelaar of advocaat."),
]
slides = [lambda: slide_cover("Wat gebeurt er met jullie gegevens?", "Eerlijk antwoord, in 5 punten", kicker="Vertrouwen", total=T)]
for i, (t, b) in enumerate(POINTS):
    slides.append(lambda i=i, t=t, b=b: slide_point(i + 2, T, None, t, b))
slides.append(lambda: slide_closing(T, T, "Rust begint bij vertrouwen."))

if __name__ == "__main__":
    paths = save_carousel(slides, sys.argv[1])
    if len(sys.argv) > 2: carousel_sheet(paths, sys.argv[2])
    print("\n".join(paths))
