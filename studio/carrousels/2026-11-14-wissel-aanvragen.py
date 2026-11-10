import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from kidsbrug_style import *

T = 6

def week(d, x0, y0, x1, hl=None):
    days = ["ma", "di", "wo", "do", "vr", "za", "zo"]; cw = (x1 - x0 - 6 * 8) / 7
    for i, dn in enumerate(days):
        cx = x0 + i * (cw + 8)
        d.text((cx + cw / 2, y0), dn, font=sans(20, "Medium"), fill=MUTED, anchor="mt")
        d.rounded_rectangle((cx, y0 + 36, cx + cw, y0 + 106), 18, fill=ROSE if i < 6 else SAGE,
                            outline=BROWN if hl == i else None, width=4)
        d.text((cx + cw / 2, y0 + 71), str(17 + i), font=sans(24, "Medium"), fill=DARK, anchor="mm")

def s_cal(d, box):
    x0, y0, x1, y1 = box
    week(d, x0, y0, x1, hl=6)
    chip(d, x0, y0 + 130, "Bij mama", ROSE, 20); chip(d, x0 + 150, y0 + 130, "Bij papa", SAGE, 20)
    card(d, (x0, y0 + 210, x1, y0 + 400), fill=WHITE, outline=GOLD)
    d.text((x0 + 26, y0 + 255), "Zondag 23 november", font=sans(24, "Medium"), fill=MUTED, anchor="lm")
    d.text((x0 + 26, y0 + 315), "Wissel om 18:00", font=serif(42, "SemiBold"), fill=DARK, anchor="lm")
    d.rounded_rectangle((x0 + 26, y0 + 345, x0 + 270, y0 + 390), 22, fill=BROWN)
    d.text((x0 + 148, y0 + 367), "Wijziging vragen", font=sans(20, "Medium"), fill=WHITE, anchor="mm")

def s_req(d, box):
    x0, y0, x1, y1 = box
    d.text((x0, y0 + 10), "Nieuwe tijd", font=sans(22, "Medium"), fill=MUTED, anchor="lt")
    card(d, (x0, y0 + 46, x1, y0 + 126), fill=CHIP)
    d.text((x0 + 24, y0 + 86), "Zondag 23 nov · 19:00", font=sans(28, "Medium"), fill=DARK, anchor="lm")
    d.text((x0, y0 + 160), "Waarom?", font=sans(22, "Medium"), fill=MUTED, anchor="lt")
    card(d, (x0, y0 + 196, x1, y0 + 330), fill=CHIP)
    cwrap_text(d, x0 + 24, y0 + 216, "Ik ben pas om 18:30 terug van mijn werk.", sans(26), maxw=x1 - x0 - 48)
    d.rounded_rectangle((x0, y0 + 370, x1, y0 + 440), 35, fill=BROWN)
    d.text(((x0 + x1) / 2, y0 + 405), "Verzoek versturen", font=sans(26, "Medium"), fill=WHITE, anchor="mm")

def s_ok(d, box):
    x0, y0, x1, y1 = box
    card(d, (x0, y0, x1, y0 + 330))
    d.text((x0 + 26, y0 + 45), "Verzoek van papa", font=sans(22, "Medium"), fill=MUTED, anchor="lm")
    d.text((x0 + 26, y0 + 105), "Wissel om 19:00?", font=serif(42, "SemiBold"), fill=DARK, anchor="lm")
    d.text((x0 + 26, y0 + 160), "Ik ben pas om 18:30 terug.", font=sans(24), fill=DARK, anchor="lm")
    d.rounded_rectangle((x0 + 26, y0 + 220, x1 - 26, y0 + 296), 38, fill=SAGE)
    d.text(((x0 + x1) / 2, y0 + 258), "Goedgekeurd door mama", font=sans(24, "Medium"), fill=DARK, anchor="mm")
    d.text((x0, y0 + 370), "De kalender past zich vanzelf aan.", font=sans(24), fill=MUTED, anchor="lt")

slides = [
    lambda: slide_cover("Een wissel aanvragen in KidsBrug", "in 3 stappen", kicker="Zo werkt het", total=T),
    lambda: slide_phone(2, T, "1. Kies de dag in de kalender", "Wisselschema", s_cal),
    lambda: slide_phone(3, T, "2. Stel je wijziging voor", "Wijziging vragen", s_req),
    lambda: slide_phone(4, T, "3. De ander zegt ja of nee", "Verzoeken", s_ok),
    lambda: slide_point(5, T, None, "Waarom zo en niet via WhatsApp?",
                        "Elke vraag en elk antwoord blijft staan. Niemand hoeft te zoeken wat er is afgesproken, en de kalender klopt altijd voor jullie allebei."),
    lambda: slide_closing(T, T, "Zwart op wit. Voor jullie allebei."),
]

if __name__ == "__main__":
    paths = save_carousel(slides, sys.argv[1])
    if len(sys.argv) > 2: carousel_sheet(paths, sys.argv[2])
    print("\n".join(paths))
