# KidsBrug Contentstudio

Deze repository is de openbare opslag voor de reels van KidsBrug, plus het gereedschap om ze te maken.
Metricool haalt de video's op via `https://raw.githubusercontent.com/degelderkylie-rgb/kidsbrug-media/main/reels/<bestand>.mp4`.

## Onderdelen

- Dashboard (goedkeuren door Kylie): https://claude.ai/artifact/Vh314yJdhdhmt9C9xrfxxe
  - Database-collectie `posts`, één document per post, id `YYYY-MM-DD-HHMM`.
  - Velden: `date` (YYYY-MM-DD), `time` (HH:MM, Europe/Brussels), `format` ("REEL"), `networks` (["instagram","facebook"]),
    `series`, `hook`, `caption`, `firstComment`, `previewAsset` (asset-id in het dashboard), `mediaUrl` (openbare GitHub-link), `coverUrl` + `coverAsset` (omslagfoto), `music` (Instagram-muziek, titel + artiest; laat leeg, Kylie kiest zelf),
    `status` ("wacht" | "aanpassen" | "ingepland" | "overgeslagen"), `feedback` (Kylie's opmerking bij "aanpassen"), `createdBy`.
  - `meta/briefing`: `{date, message}` ochtendbericht aan Kylie. `meta/strateeg`: `{week, works[], weak[], plan[]}`. `meta/team`: `{lastRun}`.
  - Kylie keurt goed in het dashboard; het dashboard plant dan zelf in Metricool in. Plan nooit zelf in zonder haar akkoord.
- Metricool-merk KidsBrug: brandId `7752204`, tijdzone `Europe/Brussels`, netwerken Instagram (@kidsbrug) en Facebook.

## Reels maken (vaste KidsBrug-huisstijl)

Alle reels gebruiken `studio/kidsbrug_style.py`. Dat is exact de stijl van de eerste KidsBrug-reels
("47 berichtjes", "Ik heb wél gebeld", "Dezelfde vraag, voor de 100e keer"): warme crème achtergrond, Lora-koppen,
Poppins-appjes, bruin/roze/salie/goud, telefoon-mockup met app-scherm, woordmerk onderaan, zachte fades. Wijk daar niet van af.

Vaste opbouw (15 tot 20 seconden), zie `studio/reels/2026-11-11-wisselmoment.py` als voorbeeld:
1. **POV-haak** (4-5 s): kop "POV: ..." en 3-4 appjes die één voor één verschijnen (`bubble`, ex links met label "Ex", jij rechts).
2. **Herkenning** (2-3 s): "En daar gaan we weer." of vergelijkbaar, korte heen-en-weer appjes.
3. **Oplossing** (4-6 s): "Met KidsBrug ..." met `phone()` en het echte app-scherm voor die functie.
4. **Vertrouwen** (3,4 s): `checklist()` met 4 punten en een afsluitende zin in bruin.
5. **Afsluiter** (3,8 s): `cta()`, altijd dezelfde.

Maak een nieuw script in `studio/reels/YYYY-MM-DD-onderwerp.py` (kopieer het voorbeeld), bekijk eerst het contactblad:
```
python3 studio/reels/<script>.py <werkmap> x --sheet                       # stills -> <werkmap>/sheet.png, bekijk die
python3 studio/reels/<script>.py <werkmap> reels/kidsbrug-YYYY-MM-DD-onderwerp.mp4
```
**Omslagfoto (verplicht):** de reel begint met een fade vanuit crème, dus het eerste beeld is leeg. Elke reel krijgt daarom
een eigen omslag via `cover()` (POV-kop + 2 appjes, alles binnen het middelste 3:4-vlak voor het profielraster). Het script
schrijft die automatisch als `reels/kidsbrug-YYYY-MM-DD-onderwerp-cover.jpg`. Zet in de post `coverUrl` (openbare GitHub-link)
en `coverAsset` (asset-id in het dashboard); het dashboard geeft hem mee aan Metricool als omslag.

Gebruik in Poppins-tekst geen tekens als ✓ of → (die vallen weg); het vinkje in `checklist()` werkt wel.
Benodigd: Pillow, ffmpeg, Lora- en Poppins-fonts in /usr/share/fonts/truetype/google-fonts/.

## Carrousels (maandag, woensdag, vrijdag om 12:30)

Naast 2 reels per dag komt er 3 keer per week een carrousel (swipe-post, 4:5, 1080x1350) in dezelfde huisstijl,
gemaakt met de carrousel-functies in `studio/kidsbrug_style.py`: `slide_cover`, `slide_point`, `slide_phone`, `slide_closing`.
Voorbeelden: `studio/carrousels/2026-11-12-...py` (tips), `2026-11-14-...py` (zo werkt het, met telefoonschermen), `2026-11-17-...py` (vertrouwen).

- Wissel drie soorten af: **Tips voor ouders** (bewaarwaardig, kindgericht), **Zo werkt KidsBrug** (één functie in 3 stappen met telefoon),
  **Vertrouwen** (privacy, EU, wat KidsBrug wel en niet is; dit stelt ook bemiddelaars gerust die het profiel bekijken).
- 6 of 7 slides: omslag (kicker + kop), de punten, vaste afsluiter `slide_closing`.
- Bestanden: `carrousels/kidsbrug-YYYY-MM-DD-onderwerp-<n>.jpg`. Maak ze met
  `python3 studio/carrousels/<script>.py carrousels/kidsbrug-YYYY-MM-DD-onderwerp <werkmap>/sheet.jpg` en bekijk het contactblad.
- Post-document: id `YYYY-MM-DD-1230`, `format` "CAROUSEL", `mediaUrls` (lijst openbare links, in volgorde), `previewAssets` (lijst asset-id's),
  geen `music`, geen omslag. Caption en eerste reactie volgen dezelfde regels als reels (5 hashtags, vaste belofte, "Bewaar deze post" bij tips).
- Beweer niets over KidsBrug dat niet in de functielijst hieronder of in eerdere posts staat.

## Inhoud en toon

- Doelgroep: gescheiden ouders in Nederland en België. Toon: rustig, herkenbaar, nooit beschuldigend naar de ex.
- Werkt het best (data okt-nov 2026): reels met één herkenbaar ruziemoment, daarna één functie die het oplost. Reels halen ~5x meer bereik dan foto-posts.
- Functies van KidsBrug: gedeelde kalender en wisselschema, wijziging aanvragen met ja/nee, kosten delen met bonnetje en automatische verdeling,
  toestemmingen zwart op wit, bellen zonder je nummer te delen met belgeschiedenis, berichtenfilter voor een rustige toon, documenten op één plek.
- Vaste belofte: "KidsBrug komt binnenkort. De eerste 30 gezinnen die zich nu inschrijven, krijgen 6 maanden gratis toegang." gevolgd door "👉 Link in bio of reageer BRUG". Geen andere beloftes of termijnen verzinnen.
- Caption-opbouw zoals de eerdere reels: POV-zin met emoji, 2-3 korte herkenbare zinnen, wat KidsBrug doet, "Minder ... Meer rust voor je kind. 💛", de vaste belofte, en een afsluitende vraag ("Herkenbaar? Tag iemand die dit ook kent.").
- Hashtags: precies 5, alleen in de caption (Instagram staat sinds december 2025 maximaal 5 toe; hashtags in de eerste reactie tellen mee, dus daar nooit hashtags). Vast: #coouderschap #gescheidenouders #scheidenmetkinderen, plus 2 die bij het onderwerp passen (bv. #wisselschema #tweehuizen, #kinderkosten #ouderschapsplan, #samenouderschap, #coouderschapbelgie). Ochtend en avond hoeven niet te verschillen; het onderwerp bepaalt de 2 wisselende.
- Eerste reactie (veld `firstComment`): een vraag over het onderwerp + "Reageer BRUG en je krijgt de link om je in te schrijven voor de wachtlijst." (ManyChat stuurt de link bij BRUG).
- Geen juridisch of medisch advies, geen echte namen, geen kinderen in beeld.
- Gebruik geen dagen/data in een reel die niet kloppen met het moment van posten.
