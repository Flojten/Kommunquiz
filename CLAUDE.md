# Kommunquiz (Kommunkampen)

Quizsida där spelaren väljer vilken av fyra kommuner som har högst eller lägst värde på ett nyckeltal från Koladas API v3 (`https://api.kolada.se/v3/`).

## Struktur
- `data/municipalities.txt` – kommunkod;namn för Sveriges 290 kommuner.
- `data/<KPI-id>.txt` – kommunkod;värde (kön "T"). `0000` är riket.
- `data/years.txt` – KPI-id;år som fetch_kolada.py valt. Går före `year` i `KPIS`.
- `fetch_kolada.py` – hämtar kommunlistan och alla nyckeltal i `KPIS` från API:et (paginering via `next_url`, utan regioner och `G`-grupper) och väljer senaste året där minst 250 kommuner har värde. Skriver inget om något steg misslyckas.
- `.github/workflows/pages.yml` – hämtar data, bygger, committar ändrad data och publicerar på GitHub Pages vid push till main, varje måndag och manuellt.
- `build.py` – läser data/, definierar nyckeltal och frågetexter i `KPIS` (`exclude` för kommuner som ska uteslutas, `suffix` för enhet efter siffran, `election` för valdata, `minCount` för nyckeltal där små kommuner saknar värde, `guess` för frågetypen "Gissa siffran"), bäddar in datan i `template.html` och skriver `index.html` och `quiz-data.json`.
- `template.html` – hela sidan (HTML, CSS, JS) med platshållaren `/*__QUIZ_DATA__*/null`.
- `index.html` – genererad fil, redigeras inte för hand.

## Frågetyper
- **Högst/lägst** – vilken av fyra kommuner har högst eller lägst värde.
- **Gissa siffran** (cirka 30 % av frågorna) – gissa en kommuns värde med ett reglage som går i percentilordning bland kommunerna (mitten är medianen). Rätt om gissningen ligger inom ±10 percentiler från det verkliga värdet. Kräver `guess` med `{kommun}` i `KPIS`.

## Bygga
```
python3 fetch_kolada.py   # valfritt, hämtar färsk data
python3 build.py
```
Öppna sedan `index.html` i en webbläsare.

## Regler
- Ange alltid "Källa: Kolada" där data visas. Om vi räknar om värden (snitt, kvoter) får Kolada inte anges som källa för de bearbetade siffrorna.
- Filtrera bort kommuner som saknar värde för ett nyckeltal i stället för att visa tomma eller nollvärden.
- Visa alltid vilket år en siffra gäller.
- Gotland (0980) utesluts ur skattefrågor, eftersom kommunen även tar ut regionens skatt.
- Frågetexterna skrivs för hand på enkel svenska. Kolada-titlar visas bara som källrad.
- Varje fråga kräver en tydlig skillnad mellan rätt svar och tvåan (`minGapRel` eller `minGapAbs`).
- Sidan ska fungera på mobil och surfplatta och i både ljust och mörkt tema.

## Nästa steg
1. Läget "Min kommun mot riket".

## Hitta nya nyckeltal
Kolada nås inte från alla miljöer. Sök via `https://api.kolada.se/v3/kpi?title=<ord>` och välj nyckeltal med `municipality_type` `K` eller `A`. `label` måste vara Koladas titel ordagrant; fetch_kolada.py varnar annars. Kontrollera att `minGapRel`/`minGapAbs` släpper igenom en rimlig andel slumpade fyrgrupper (ungefär 35–70 %).
