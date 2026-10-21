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
     "minGapAbs": 0.4, "exclude": ["0980"],
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
    {"id": "N05401", "year": 2025, "decimals": 0, "unit": "%", "election": True,
     "short": "Valdeltagande", "label": "Valdeltagande i senaste kommunalvalet, andel (%)",
     "high": "I vilken kommun röstade störst andel i kommunvalet?",
     "low": "I vilken kommun röstade minst andel i kommunvalet?",
     "minGapAbs": 3},
    {"id": "N02926", "year": 2025, "decimals": 1, "unit": "%",
     "short": "Utrikes födda", "label": "Utrikes födda, andel (%)",
     "high": "I vilken kommun är störst andel av invånarna födda utomlands?",
     "low": "I vilken kommun är minst andel av invånarna födda utomlands?",
     "minGapAbs": 3},
    {"id": "N01982", "year": 2025, "decimals": 1, "unit": "%",
     "short": "Utbildning", "label": "Invånare 25-64 år med eftergymnasial utbildning, andel (%)",
     "high": "I vilken kommun har störst andel av de vuxna (25–64 år) läst vidare efter gymnasiet?",
     "low": "I vilken kommun har minst andel av de vuxna (25–64 år) läst vidare efter gymnasiet?",
     "minGapAbs": 4},
    {"id": "N00959", "year": 2025, "decimals": 1, "unit": "år", "suffix": "år",
     "short": "Medelålder", "label": "Medelålder, år",
     "high": "Vilken kommun har högst medelålder?",
     "low": "Vilken kommun har lägst medelålder?",
     "minGapAbs": 1.5},
    {"id": "N00999", "year": 2025, "decimals": 1, "unit": "per 1 000", "suffix": "per 1 000 inv.",
     "short": "Nya företag", "label": "Nystartade företag, antal/1000 inv, 16-64 år",
     "high": "I vilken kommun startas flest nya företag i förhållande till antalet invånare?",
     "low": "I vilken kommun startas minst antal nya företag i förhållande till antalet invånare?",
     "minGapRel": 0.15,
     "note": "Antal nystartade företag per 1 000 invånare i åldern 16–64 år."},
    {"id": "N03920", "year": 2025, "decimals": 1, "unit": "%",
     "short": "Arbetslöshet", "label": "Arbetslösa av befolkningen, 18-65 år, andel (%)",
     "high": "I vilken kommun är störst andel av invånarna (18–65 år) arbetslösa?",
     "low": "I vilken kommun är minst andel av invånarna (18–65 år) arbetslösa?",
     "minGapRel": 0.2},
    {"id": "N31807", "year": 2025, "decimals": 1, "unit": "%",
     "short": "Ekonomiskt bistånd", "label": "Invånare som någon gång under året erhållit ekonomiskt bistånd, andel (%) av bef.",
     "high": "I vilken kommun fick störst andel av invånarna ekonomiskt bistånd från kommunen under året?",
     "low": "I vilken kommun fick minst andel av invånarna ekonomiskt bistånd från kommunen under året?",
     "minGapRel": 0.25},
    {"id": "N85084", "year": 2025, "decimals": 1, "unit": "km", "suffix": "km",
     "short": "Natur", "label": "Medelavstånd till skyddad natur, km",
     "high": "I vilken kommun har invånarna i genomsnitt längst till skyddad natur?",
     "low": "I vilken kommun har invånarna i genomsnitt närmast till skyddad natur?",
     "minGapRel": 0.3},
]

# Kommuner som aldrig ska vara med i ett visst nyckeltal anges i "exclude".
# "election" betyder att Kolada redovisar det senaste kommunvalet för varje år; build.py skriver ut vilket val det är.
# fetch_kolada.py skriver valt år per nyckeltal till data/years.txt; det går före "year" ovan.

def read_pairs(path):
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if ";" in line:
            k, v = line.split(";", 1)
            out[k.strip()] = float(v)
    return out

def main():
    names = {k: v for k, v in (l.split(";", 1) for l in (DATA / "municipalities.txt").read_text(encoding="utf-8").splitlines() if l)}
    pop = read_pairs(DATA / "N01951.txt")
    years_file = DATA / "years.txt"
    years = {k: int(v) for k, v in read_pairs(years_file).items()} if years_file.exists() else {}

    kpis = []
    for k in KPIS:
        k = {**k, "year": years.get(k["id"], k["year"])}
        if k.get("election"):
            k["note"] = f"Gäller kommunvalet {k['year'] - (k['year'] - 2022) % 4}."
        vals = read_pairs(DATA / f"{k['id']}.txt")
        nat = vals.pop("0000", None)
        vals = {m: round(v, k["decimals"]) for m, v in vals.items()
                if m in names and m not in k.get("exclude", ())}
        kpis.append({**k, "national": None if nat is None else round(nat, k["decimals"]), "values": vals})
        print(k["id"], kpis[-1]["year"], len(vals), "kommuner, riket:", nat)

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


if __name__ == "__main__":
    main()
