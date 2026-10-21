# Kommunquiz (Kommunkampen)

Quizsida där spelaren väljer vilken av fyra kommuner som har högst eller lägst värde på ett nyckeltal från Koladas API v3 (`https://api.kolada.se/v3/`).

## Struktur
- `data/municipalities.txt` – kommunkod;namn för Sveriges 290 kommuner.
- `data/<KPI-id>.txt` – kommunkod;värde (kön "T"). `0000` är riket.
- `build.py` – läser data/, definierar nyckeltal och frågetexter i `KPIS`, bäddar in datan i `template.html` och skriver `index.html` och `quiz-data.json`.
- `template.html` – hela sidan (HTML, CSS, JS) med platshållaren `/*__QUIZ_DATA__*/null`.
- `index.html` – genererad fil, redigeras inte för hand.

## Bygga
```
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
1. Skript som hämtar data från API:et i stället för manuellt sparade filer (paginering via `next_url`, filtrera bort `G`-grupper och regioner `0001`–`0025`).
2. GitHub Action som hämtar data och bygger om sidan varje vecka, plus GitHub Pages.
3. Fler nyckeltal, läget "Min kommun mot riket" och frågetypen "Gissa siffran".
