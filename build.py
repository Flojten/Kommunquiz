"""Bygger quiz-data från Kolada-utdrag i data/ och skriver index.html från template.html."""
import json, pathlib

ROOT = pathlib.Path(__file__).parent
DATA = ROOT / "data"

# Nyckeltal som används i quizet. Frågetexterna är egna, siffrorna Koladas.
KPIS = [
    {"id": "N01951", "year": 2025, "decimals": 0, "unit": "invånare",
     "label": "Invånare totalt, antal", "short": "Befolkning",
     "high": "Vilken kommun har flest invånare?",
     "low": "Vilken kommun har minst antal invånare?",
     "minGapRel": 0.12},
    {"id": "N00901", "year": 2026, "decimals": 2, "unit": "%",
     "label": "Skattesats till kommun (%)", "short": "Kommunalskatt",
     "high": "Vilken kommun har högst kommunal skattesats?",
     "low": "Vilken kommun har lägst kommunal skattesats?",
     "minGapAbs": 0.4,
     "note": "Gotland är inte med, eftersom kommunen också tar ut regionens skatt."},
    {"id": "N15419", "year": 2025, "decimals": 1, "unit": "%",
     "short": "Skola åk 9", "label": "Elever i åk 9 som uppnått betygskriterierna i alla ämnen, kommunala skolor, andel (%)",
     "high": "I vilken kommun klarade störst andel av niondeklassarna betygskriterierna i alla ämnen?",
     "low": "I vilken kommun klarade minst andel av niondeklassarna betygskriterierna i alla ämnen?",
     "minGapAbs": 4},
    {"id": "N09809", "year": 2025, "decimals": 1, "unit": "%",
     "short": "Bibliotek", "label": "Aktiva låntagare i kommunala bibliotek, andel (%) av befolkningen",
     "high": "I vilken kommun är störst andel av invånarna aktiva bibliotekslåntagare?",
     "low": "I vilken kommun är minst andel av invånarna aktiva bibliotekslåntagare?",
     "minGapAbs": 3},
]

def read_pairs(path):
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if ";" in line:
            k, v = line.split(";", 1)
            out[k.strip()] = float(v)
    return out

names = {k: v for k, v in (l.split(";", 1) for l in (DATA / "municipalities.txt").read_text(encoding="utf-8").splitlines() if l)}
pop = read_pairs(DATA / "N01951.txt")

kpis = []
for k in KPIS:
    vals = read_pairs(DATA / f"{k['id']}.txt")
    nat = vals.pop("0000", None)
    vals = {m: round(v, k["decimals"]) for m, v in vals.items() if m in names}
    kpis.append({**k, "national": None if nat is None else round(nat, k["decimals"]), "values": vals})
    print(k["id"], len(vals), "kommuner, riket:", nat)

payload = {
    "municipalities": [{"id": m, "name": n, "pop": int(pop.get(m, 0))} for m, n in names.items()],
    "kpis": kpis,
}
assert len(payload["municipalities"]) == 290

html = (ROOT / "template.html").read_text(encoding="utf-8")
html = html.replace("/*__QUIZ_DATA__*/null", json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
(ROOT / "index.html").write_text(html, encoding="utf-8")
(ROOT / "quiz-data.json").write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
print("index.html", len(html), "bytes")
