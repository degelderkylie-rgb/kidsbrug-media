# KidsBrug Contentstudio

Deze repository is de openbare opslag voor de reels van KidsBrug, plus het gereedschap om ze te maken.
Metricool haalt de video's op via `https://raw.githubusercontent.com/degelderkylie-rgb/kidsbrug-media/main/reels/<bestand>.mp4`.

## Onderdelen

- Dashboard (goedkeuren door Kylie): https://claude.ai/artifact/Vh314yJdhdhmt9C9xrfxxe
  - Database-collectie `posts`, één document per post, id `YYYY-MM-DD-HHMM`.
  - Velden: `date` (YYYY-MM-DD), `time` (HH:MM, Europe/Brussels), `format` ("REEL"), `networks` (["instagram","facebook"]),
    `series`, `hook`, `caption`, `firstComment`, `previewAsset` (asset-id in het dashboard), `mediaUrl` (openbare GitHub-link),
    `status` ("wacht" | "aanpassen" | "ingepland" | "overgeslagen"), `feedback` (Kylie's opmerking bij "aanpassen"), `createdBy`.
  - `meta/briefing`: `{date, message}` ochtendbericht aan Kylie. `meta/strateeg`: `{week, works[], weak[], plan[]}`. `meta/team`: `{lastRun}`.
  - Kylie keurt goed in het dashboard; het dashboard plant dan zelf in Metricool in. Plan nooit zelf in zonder haar akkoord.
- Metricool-merk KidsBrug: brandId `7752204`, tijdzone `Europe/Brussels`, netwerken Instagram (@kidsbrug) en Facebook.

## Reels maken

`studio/render.py` zet een HTML-pagina om naar een MP4 (1080x1920, 30 fps, stille audiospoor):

```
python3 studio/render.py studio/werk/reel-x.html reels/kidsbrug-YYYY-MM-DD-onderwerp.mp4
python3 studio/render.py studio/werk/reel-x.html --stills 2,6,12   # eerst stills bekijken
```

Een reel-pagina gebruikt `style.css` en `engine.js` (zie `studio/voorbeelden/`). Elke `.scene` heeft `data-start`/`data-end`
(seconden), de laatste scene `data-hold`. Elementen met `data-in` (seconden na scenestart) komen in beeld (`data-fx`: up, pop, left, right).
Bouwstenen: `.kicker`, `.h1`, `.h2`, `.body`, `.hl`, `.chat` met `.b.me`/`.b.them`, `.card` met `.row`, `.feat`, `.cal`, `.cta` met `.btn`.
Houd reels 14 tot 19 seconden. Tekst blijft in het midden; onderaan 420px vrij laten voor de Instagram-knoppen.

Benodigd: google-chrome, playwright (Python), ffmpeg.

## Inhoud en toon

- Doelgroep: gescheiden ouders in Nederland en België. Toon: rustig, herkenbaar, nooit beschuldigend naar de ex.
- Werkt het best (data okt-nov 2026): reels met één herkenbaar ruziemoment, daarna één functie die het oplost. Reels halen ~5x meer bereik dan foto-posts.
- Functies van KidsBrug: gedeelde kalender en wisselschema, wijziging aanvragen met ja/nee, kosten delen met bonnetje en automatische verdeling,
  toestemmingen zwart op wit, bellen zonder je nummer te delen met belgeschiedenis, berichtenfilter voor een rustige toon, documenten op één plek.
- Vaste afsluiter: "Zet je op de wachtlijst via de link in bio. De eerste 30 gezinnen krijgen gratis toegang." Geen andere beloftes of termijnen verzinnen.
- Captions eindigen met een vraag of een emoji-reactie. 4 tot 6 hashtags, o.a. #coouderschap #gescheidenouders #tweehuizen #scheidenmetkinderen #ouderschapsplan.
- Geen juridisch of medisch advies, geen echte namen, geen kinderen in beeld.
- Gebruik geen dagen/data in een reel die niet kloppen met het moment van posten.
