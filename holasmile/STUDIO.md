# Hola Smile Clinic Contentstudio

Deze map is de openbare opslag voor de reels en carrousels van Hola Smile Clinic (Zundert), plus het gereedschap om ze te maken.
Ze staat in de repository `degelderkylie-rgb/kidsbrug-media`, maar staat helemaal los van KidsBrug: gebruik nooit KidsBrug-stijl of -teksten.
Metricool haalt de bestanden op via `https://raw.githubusercontent.com/degelderkylie-rgb/kidsbrug-media/main/holasmile/<map>/<bestand>`.

## Onderdelen

- Dashboard (goedkeuren door Kylie): https://claude.ai/artifact/2VTdhtMh6VFCogAQmWyCzD
  - Database-collectie `posts`, één document per post, id `YYYY-MM-DD-HHMM`.
  - Velden: `date` (YYYY-MM-DD), `time` (HH:MM, Europe/Brussels), `format` ("REEL" of "CAROUSEL"), `networks`,
    `series`, `hook`, `caption`, `firstComment`, `previewAsset` + `mediaUrl` + `coverUrl` + `coverAsset` (reels),
    `previewAssets` + `mediaUrls` (carrousels), `music` (laat leeg), `status` ("wacht" | "aanpassen" | "ingepland" | "overgeslagen"),
    `feedback` (Kylie's opmerking bij "aanpassen"), `createdBy`.
  - `meta/briefing`: `{date, message}` ochtendbericht aan Kylie. `meta/strateeg`: `{week, works[], weak[], plan[]}`. `meta/team`: `{lastRun}`.
  - `meta/fotos`: `{used: [bestandsnamen die al in een reel zaten]}`.
  - Kylie keurt goed in het dashboard; het dashboard plant dan zelf in Metricool in. Plan nooit zelf in zonder haar akkoord.
- Metricool-merk Hola Smile Clinic Zundert: brandId `6788119`, tijdzone `Europe/Brussels`, Instagram @holasmileclinic_zundert, Facebook en TikTok.

## Ritme

- **1 reel per dag om 19:00**, netwerken `["instagram","facebook","tiktok"]`.
- **2 carrousels per week**, dinsdag en vrijdag om 12:30, netwerken `["instagram","facebook"]`.

## Huisstijl (vast, wijk niet af)

Alles gebruikt `holasmile/studio/holasmile_style.py`: bijna zwarte warme achtergrond met zachte gloed, dunne gouden rand,
crème Lora-koppen, goud als accent, Poppins voor kleine tekst, sparkles, de gouden **kleurwaaier** (`shade_guide`) als vast
herkenningsteken, woordmerk "Hola Smile Clinic · Zundert" onderaan, zachte fades. Vaste afsluiter `cta()`.

## Reels (12 tot 16 seconden) — ALTIJD MET BEWEGING

Kylie vond reels met stilstaande dia's en fades te saai. Elke reel gebruikt daarom `holasmile/studio/holasmile_motion.py`
(frame voor frame, 30 fps): tekst die erin knalt (`pop`), inzoomen, schuiven, sparkles die twinkelen, snelle wissels (scenes van 1,5-2,5 s),
en als afsluiter `cta_motion`. Voorbeeld: `studio/reels/sjabloon-voor-na-beweging.py`. Maak ook mythe-, tip- en vraag-reels op die manier
(bv. stelling knalt erin, stempel MYTHE slaat erop, kleurwaaier schuift van geel naar wit, lijstpunten komen één voor één binnen).
De oude stilstaande functies (`render_reel`) gebruik je niet meer voor nieuwe reels.

Wissel deze reeksen af (kijk welke het laatst was en wat de strateeg vraagt):
1. **Mythe of feit** — voorbeeld `studio/reels/2026-11-13-whitening-tandpasta.py`: stelling in `quote_card` → `stamp` MYTHE/FEIT → uitleg met kleurwaaier → `listing` "Wat wél helpt" → `cta()`.
2. **Tips** — "3 dingen die je tanden geel maken", nazorg, koffie, rode wijn; haak + `listing` + `cta()`.
3. **Vraag van een klant** — "Doet het pijn?", "Hoe lang duurt het?", "Welk pakket past bij mij?"; `quote_card` met label "Vraag van een klant" + antwoord.
4. **Echt resultaat (voor/na)** — ALLEEN met Kylie's echte foto's uit `holasmile/fotos/` (bestanden `*-voor.jpg` en `*-na.jpg` met dezelfde naam ervoor).
   Gebruik `studio/reels/sjabloon-voor-na.py`. Doe dit zodra er een paar foto's staat die nog niet in `meta/fotos.used` staat, maximaal 2 keer per week.
   Foto's nooit bewerken, witter maken of bijsnijden tot iets anders; altijd "Geen filter. Resultaten verschillen per persoon."
5. **Aanbod** (maximaal 1 op de 5 reels) — kerst-cadeaubox, teamsessies voor bedrijven vanaf 6 personen, duobehandeling.

Werkwijze: kopieer het voorbeeld naar `studio/reels/YYYY-MM-DD-onderwerp.py`, pas inhoud en COVER aan, bekijk het contactblad:
```
python3 holasmile/studio/reels/<script>.py <werkmap> x --sheet
python3 holasmile/studio/reels/<script>.py <werkmap> holasmile/reels/holasmile-YYYY-MM-DD-onderwerp.mp4
```
De omslag (`-cover.jpg`) wordt automatisch geschreven; bekijk die ook. Alles moet binnen beeld en binnen het middelste 3:4-vlak van de omslag blijven.
De eerste seconde moet al de haak tonen (geen leeg of rustig beginbeeld). Gebruik in beeldtekst geen emoji, ✓ of → (die worden een vierkantje); emoji mogen alleen in de caption.

## Carrousels (dinsdag en vrijdag 12:30, 4:5)

Voorbeeld `studio/carrousels/2026-11-14-geel-na-koffie.py`: `slide_cover` (kicker + kop), 4-5 × `slide_point`, `slide_closing`.
Wissel af: **Tips** (bewaarwaardig, "Bewaar deze post"), **Zo gaat een behandeling** (stap voor stap: intake, beschermen, 3-4 rondes van 20 min onder de LED-lamp, nazorg),
**Welk pakket past bij jou** (koffiedrinkers/rokers minstens Pakket 2, nooit eerder gebleekt vaak 3 rondes).
Bestanden `holasmile/carrousels/holasmile-YYYY-MM-DD-onderwerp-<n>.jpg`; bekijk het contactblad.

## Inhoud en toon

- Doelgroep: vrouwen 25-55 in Zundert, Breda, Etten-Leur, Roosendaal en net over de grens (Hoogstraten). Toon: warm, eerlijk, een tikje luxe, nooit opdringerig.
- Wat werkt (data juli-nov 2026): echte resultaten met echte mensen (duobehandeling moeder & dochter: 1.723 bereik), POV-haken, concrete tips (3× langere kijktijd).
  Wat niet werkt: sfeervideo's over de massagestoel (128-263 bereik) en steeds dezelfde "ontspan + boek nu"-boodschap.
- Feiten die je mag gebruiken: behandeling in één afspraak (noem NOOIT "40 minuten" of een totale duur; dat klopt niet), rondes van 20 minuten (Pakket 1 = 1 ronde, Pakket 2 = 3, Pakket 3 = 4), duobehandeling mogelijk,
  nieuwste generatie LED-lampen, luxe massagestoelen, nieuwe mondspreiders per klant, open maandag t/m zaterdag, Zundert.
  "Tot 10 tinten lichter" alleen met "resultaat verschilt per persoon". Verzin geen prijzen, kortingen, termijnen of medische beloftes.
- Nooit: AI-gegenereerde of nep-resultaten, nep-klanten of nep-reviews, medische claims ("veilig voor iedereen", "geen enkele gevoeligheid"), vergelijken met of afkraken van tandartsen.
- Caption: haak-zin met emoji, 2-3 korte zinnen, wat Hola Smile doet, "Resultaten verschillen per persoon." bij resultaten,
  dan "📍 Hola Smile Clinic – Zundert" en "Boek via de link in bio of stuur ons SMILE via DM 🤍", en een afsluitende vraag.
- Hashtags: precies 5, alleen in de caption. Vast: #tandenbleken #tandenblekenzundert #holasmileclinic, plus 2 passend (bv. #tandenblekenbreda #wittetanden #voorenna #koffietanden #stralendeglimlach).
- Eerste reactie (`firstComment`): één vraag over het onderwerp, zonder hashtags.
- Gebruik geen dagen/data in een reel die niet kloppen met het moment van posten.
