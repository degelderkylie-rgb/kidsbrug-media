import sys, os, subprocess; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from holasmile_style import *

# Sinterklaas-filmpje ZONDER tekst (wens Kylie 17 nov): Sint in de stoel -> Sint kijkt blij in de spiegel -> eindbeeld met logo.
# Gebruik: python3 sinterklaas-zonder-tekst.py <clip_stoel.mp4> <clip_spiegel.mp4> <uit.mp4> [logo.png]
# Zonder logo-bestand komt het tekstwoordmerk in het eindbeeld (tijdelijk, tot het echte logo er is).
IN_A, IN_B, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
LOGO = sys.argv[4] if len(sys.argv) > 4 else None
work = os.path.splitext(OUT)[0] + "-werk"; os.makedirs(work, exist_ok=True)


def endcard(path):
    im, d = base()
    if LOGO:
        lg = Image.open(LOGO).convert("RGBA"); lg.thumbnail((760, 760), Image.LANCZOS)
        im.paste(lg, ((W - lg.width) // 2, (H - lg.height) // 2 - 60), lg)
    else:
        d.text((W / 2, 860), "Hola Smile", font=serif(140, "SemiBold"), fill=CREAM, anchor="mm")
        d.text((W / 2, 990), "CLINIC · ZUNDERT", font=sans(40, "Medium"), fill=GOLD, anchor="mm")
        rule(d, 1080)
    im.save(path, "PNG")


endcard(f"{work}/end.png")
D, X, E = 4.0, 0.5, 3.0  # clipduur, overgang, eindbeeld
v = "scale=1080:1920:flags=lanczos,fps=30,setsar=1,format=yuv420p"
flt = (f"[0:v]{v},trim=0:{D},setpts=PTS-STARTPTS[a];[1:v]{v},trim=0:{D},setpts=PTS-STARTPTS[b];"
       f"[2:v]{v},trim=0:{E},setpts=PTS-STARTPTS[c];"
       f"[a][b]xfade=transition=fade:duration={X}:offset={D - X}[ab];"
       f"[ab][c]xfade=transition=fade:duration={X}:offset={2 * D - 2 * X}[v]")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", IN_A, "-i", IN_B, "-loop", "1", "-t", str(E), "-i", f"{work}/end.png",
                "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-filter_complex", flt, "-map", "[v]", "-map", "3:a",
                "-shortest", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-c:a", "aac", "-movflags", "+faststart", OUT], check=True)
print(OUT)
