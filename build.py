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
     "guess": "Hur många invånare har {kommun}?",
     "minGapRel": 0.12},
    {"id": "N00901", "year": 2026, "decimals": 2, "unit": "%",
     "label": "Skattesats till kommun (%)", "short": "Kommunalskatt",
     "high": "Vilken kommun har högst kommunal skattesats?",
     "low": "Vilken kommun har lägst kommunal skattesats?",
     "guess": "Vilken kommunal skattesats har {kommun}?",
     "vs": "den kommunala skattesatsen",
     "minGapAbs": 0.4, "exclude": ["0980"],
     "note": "Gotland är inte med, eftersom kommunen också tar ut regionens skatt."},
    {"id": "N15419", "year": 2025, "decimals": 1, "unit": "%",
     "short": "Skola åk 9", "label": "Elever i åk 9 som uppnått betygskriterierna i alla ämnen, kommunala skolor,  andel (%)",
     "high": "I vilken kommun klarade störst andel av niondeklassarna betygskriterierna i alla ämnen?",
     "low": "I vilken kommun klarade minst andel av niondeklassarna betygskriterierna i alla ämnen?",
     "guess": "Hur stor andel av niondeklassarna i de kommunala skolorna i {kommun} klarade betygskriterierna i alla ämnen?",
     "vs": "andelen niondeklassare i kommunala skolor som klarade betygskriterierna i alla ämnen",
     "minGapAbs": 4},
    {"id": "N09809", "year": 2025, "decimals": 1, "unit": "%",
     "short": "Bibliotek", "label": "Aktiva låntagare i kommunala bibliotek, andel (%) av befolkningen",
     "high": "I vilken kommun är störst andel av invånarna aktiva bibliotekslåntagare?",
     "low": "I vilken kommun är minst andel av invånarna aktiva bibliotekslåntagare?",
     "guess": "Hur stor andel av invånarna i {kommun} är aktiva bibliotekslåntagare?",
     "vs": "andelen invånare som är aktiva bibliotekslåntagare",
     "minGapAbs": 3},
    {"id": "N05401", "year": 2025, "decimals": 0, "unit": "%", "election": True,
     "short": "Valdeltagande", "label": "Valdeltagande i senaste kommunalvalet, andel (%)",
     "high": "I vilken kommun röstade störst andel i kommunvalet?",
     "low": "I vilken kommun röstade minst andel i kommunvalet?",
     "guess": "Hur stor andel av de röstberättigade i {kommun} röstade i kommunvalet?",
     "vs": "valdeltagandet i kommunvalet",
     "minGapAbs": 3},
    {"id": "N02926", "year": 2025, "decimals": 1, "unit": "%",
     "short": "Utrikes födda", "label": "Utrikes födda, andel (%)",
     "high": "I vilken kommun är störst andel av invånarna födda utomlands?",
     "low": "I vilken kommun är minst andel av invånarna födda utomlands?",
     "guess": "Hur stor andel av invånarna i {kommun} är födda utomlands?",
     "vs": "andelen invånare som är födda utomlands",
     "minGapAbs": 3},
    {"id": "N01982", "year": 2025, "decimals": 1, "unit": "%",
     "short": "Utbildning", "label": "Invånare 25-64 år med eftergymnasial utbildning, andel (%)",
     "high": "I vilken kommun har störst andel av de vuxna (25–64 år) läst vidare efter gymnasiet?",
     "low": "I vilken kommun har minst andel av de vuxna (25–64 år) läst vidare efter gymnasiet?",
     "guess": "Hur stor andel av de vuxna (25–64 år) i {kommun} har läst vidare efter gymnasiet?",
     "vs": "andelen vuxna (25–64 år) som har läst vidare efter gymnasiet",
     "minGapAbs": 4},
    {"id": "N00959", "year": 2025, "decimals": 1, "unit": "år", "suffix": "år",
     "short": "Medelålder", "label": "Medelålder, år",
     "high": "Vilken kommun har högst medelålder?",
     "low": "Vilken kommun har lägst medelålder?",
     "guess": "Vilken medelålder har invånarna i {kommun}?",
     "vs": "medelåldern",
     "minGapAbs": 1.5},
    {"id": "N00999", "year": 2025, "decimals": 1, "unit": "per 1 000", "suffix": "/1 000 inv.",
     "short": "Nya företag", "label": "Nystartade företag, antal/1000 inv, 16-64 år",
     "high": "I vilken kommun startas flest nya företag i förhållande till antalet invånare?",
     "low": "I vilken kommun startas minst antal nya företag i förhållande till antalet invånare?",
     "guess": "Hur många nya företag startades per 1 000 invånare (16–64 år) i {kommun}?",
     "vs": "antalet nystartade företag per invånare",
     "minGapRel": 0.15,
     "note": "Antal nystartade företag per 1 000 invånare i åldern 16–64 år."},
    {"id": "N03920", "year": 2025, "decimals": 1, "unit": "%",
     "short": "Arbetslöshet", "label": "Arbetslösa av befolkningen, 18-65 år, andel (%)",
     "high": "I vilken kommun är störst andel av invånarna (18–65 år) arbetslösa?",
     "low": "I vilken kommun är minst andel av invånarna (18–65 år) arbetslösa?",
     "guess": "Hur stor andel av invånarna (18–65 år) i {kommun} är arbetslösa?",
     "vs": "andelen arbetslösa (18–65 år)",
     "minGapRel": 0.2},
    {"id": "N31807", "year": 2025, "decimals": 1, "unit": "%",
     "short": "Ekonomiskt bistånd", "label": "Invånare som någon gång under året erhållit ekonomiskt bistånd, andel (%) av bef.",
     "high": "I vilken kommun fick störst andel av invånarna ekonomiskt bistånd från kommunen under året?",
     "low": "I vilken kommun fick minst andel av invånarna ekonomiskt bistånd från kommunen under året?",
     "guess": "Hur stor andel av invånarna i {kommun} fick ekonomiskt bistånd från kommunen under året?",
     "vs": "andelen invånare som fick ekonomiskt bistånd",
     "minGapRel": 0.25},
    {"id": "N85084", "year": 2025, "decimals": 1, "unit": "km", "suffix": "km",
     "short": "Natur", "label": "Medelavstånd till skyddad natur, km",
     "high": "I vilken kommun har invånarna i genomsnitt längst till skyddad natur?",
     "low": "I vilken kommun har invånarna i genomsnitt närmast till skyddad natur?",
     "guess": "Hur långt har invånarna i {kommun} i genomsnitt till skyddad natur?",
     "vs": "medelavståndet till skyddad natur",
     "minGapRel": 0.3},
    {"id": "N07540", "year": 2025, "decimals": 0, "unit": "per 100 000", "suffix": "/100 000 inv.",
     "short": "Brott", "label": "Anmälda brott totalt, antal/100 000 inv",
     "high": "I vilken kommun anmäldes flest brott i förhållande till antalet invånare?",
     "low": "I vilken kommun anmäldes minst antal brott i förhållande till antalet invånare?",
     "guess": "Hur många brott anmäldes per 100 000 invånare i {kommun}?",
     "vs": "antalet anmälda brott per invånare",
     "minGapRel": 0.2,
     "note": "Anmälda brott per 100 000 invånare. Brotten räknas där de begicks, inte där den misstänkta bor."},
    {"id": "N00957", "year": 2025, "decimals": 1, "unit": "dagar", "suffix": "dagar",
     "short": "Ohälsotal", "label": "Ohälsotal, dagar",
     "high": "I vilken kommun får invånarna ersättning från Försäkringskassan för flest sjukdagar per person?",
     "low": "I vilken kommun får invånarna ersättning från Försäkringskassan för minst antal sjukdagar per person?",
     "guess": "Hur många sjukdagar per person fick invånarna i {kommun} ersättning för från Försäkringskassan?",
     "vs": "antalet ersatta sjukdagar per person (ohälsotalet)",
     "minGapRel": 0.15,
     "note": "Ohälsotalet: dagar med sjukpenning, rehabiliteringspenning och sjuk- eller aktivitetsersättning per försäkrad 16–64 år."},
    {"id": "N13800", "year": 2025, "decimals": 0, "unit": "%",
     "short": "Fritids", "label": "Barn 6-12 år inskrivna i fritidshem, andel  (%)",
     "high": "I vilken kommun går störst andel av barnen 6–12 år på fritids?",
     "low": "I vilken kommun går minst andel av barnen 6–12 år på fritids?",
     "guess": "Hur stor andel av barnen 6–12 år i {kommun} går på fritids?",
     "vs": "andelen barn 6–12 år som går på fritids",
     "minGapAbs": 6},
    {"id": "N01994", "year": 2025, "decimals": 1, "unit": "%",
     "short": "Unga invånare", "label": "Invånare 0-19 år, andel (%)",
     "high": "I vilken kommun är störst andel av invånarna under 20 år?",
     "low": "I vilken kommun är minst andel av invånarna under 20 år?",
     "guess": "Hur stor andel av invånarna i {kommun} är under 20 år?",
     "vs": "andelen invånare under 20 år",
     "minGapAbs": 1.5},
    {"id": "N02937", "year": 2025, "decimals": 1, "unit": "per km²", "suffix": "inv./km²",
     "short": "Befolkningstäthet", "label": "Invånare per kvadratkilometer, inv/kvm",
     "high": "Vilken kommun har flest invånare per kvadratkilometer?",
     "low": "Vilken kommun har minst antal invånare per kvadratkilometer?",
     "guess": "Hur många invånare per kvadratkilometer har {kommun}?",
     "vs": "befolkningstätheten",
     "minGapRel": 0.3},
    {"id": "N07945", "year": 2025, "decimals": 1, "unit": "%",
     "short": "Elbilar", "label": "Elbilar, andel (%)",
     "high": "I vilken kommun är störst andel av bilarna elbilar?",
     "low": "I vilken kommun är minst andel av bilarna elbilar?",
     "guess": "Hur stor andel av bilarna i {kommun} är elbilar?",
     "vs": "andelen elbilar",
     "minGapRel": 0.2},
    {"id": "N07935", "year": 2025, "decimals": 0, "unit": "per 1 000", "suffix": "/1 000 inv.",
     "short": "Bilar", "label": "Bilar, antal/1000 inv",
     "high": "I vilken kommun finns flest bilar i förhållande till antalet invånare?",
     "low": "I vilken kommun finns minst antal bilar i förhållande till antalet invånare?",
     "guess": "Hur många bilar finns det per 1 000 invånare i {kommun}?",
     "vs": "antalet bilar per invånare",
     "minGapRel": 0.1},
    {"id": "N07956", "year": 2025, "decimals": 1, "unit": "%",
     "short": "Hyresrätter", "label": "Hyresrätter i bostadsbeståndet, andel (%)",
     "high": "I vilken kommun är störst andel av bostäderna hyresrätter?",
     "low": "I vilken kommun är minst andel av bostäderna hyresrätter?",
     "guess": "Hur stor andel av bostäderna i {kommun} är hyresrätter?",
     "vs": "andelen hyresrätter",
     "minGapAbs": 5},
    {"id": "N00401", "year": 2025, "decimals": 1, "unit": "ton", "suffix": "ton/inv.",
     "short": "Utsläpp", "label": "Utsläpp till luft av växthusgaser totalt, ton CO2-ekv/inv",
     "high": "I vilken kommun släpps mest växthusgaser ut i förhållande till antalet invånare?",
     "low": "I vilken kommun släpps minst växthusgaser ut i förhållande till antalet invånare?",
     "guess": "Hur många ton växthusgaser släpptes ut per invånare i {kommun}?",
     "vs": "utsläppen av växthusgaser per invånare",
     "minGapRel": 0.3,
     "note": "Utsläpp inom kommunens gränser i ton koldioxidekvivalenter per invånare."},
    {"id": "N02799", "year": 2025, "decimals": 1, "unit": "per 1 000", "suffix": "/1 000 inv.",
     "short": "Födda barn", "label": "Födda barn, antal/1000 inv",
     "high": "I vilken kommun föddes flest barn i förhållande till antalet invånare?",
     "low": "I vilken kommun föddes minst antal barn i förhållande till antalet invånare?",
     "guess": "Hur många barn föddes per 1 000 invånare i {kommun}?",
     "vs": "antalet födda barn per invånare",
     "minGapRel": 0.15},
    {"id": "N00989", "year": 2025, "decimals": 1, "unit": "%",
     "short": "Skulder", "label": "Skuldsatta invånare 18+ hos Kronofogden, andel (%)",
     "high": "I vilken kommun har störst andel av de vuxna skulder hos Kronofogden?",
     "low": "I vilken kommun har minst andel av de vuxna skulder hos Kronofogden?",
     "guess": "Hur stor andel av de vuxna i {kommun} har skulder hos Kronofogden?",
     "vs": "andelen vuxna med skulder hos Kronofogden",
     "minGapRel": 0.2},
    {"id": "N45850", "year": 2025, "decimals": 1, "unit": "per inv.", "suffix": "nätter/inv.",
     "short": "Turism", "label": "Gästnätter, antal nätter, totalt per invånare, antal/inv",
     "high": "Vilken kommun har flest övernattande gäster i förhållande till antalet invånare?",
     "low": "Vilken kommun har minst antal övernattande gäster i förhållande till antalet invånare?",
     "guess": "Hur många gästnätter per invånare hade {kommun}?",
     "vs": "antalet gästnätter per invånare",
     "minGapRel": 0.3, "minCount": 240,
     "note": "Gästnätter på hotell, vandrarhem, campingar och liknande per invånare."},
    {"id": "U09800", "year": 2025, "decimals": 1, "unit": "per inv.", "suffix": "ggr/inv.",
     "short": "Idrott", "label": "Deltagartillfällen i idrottsföreningar, antal/inv 7-20 år",
     "high": "I vilken kommun idrottar barn och unga (7–20 år) oftast i en förening?",
     "low": "I vilken kommun idrottar barn och unga (7–20 år) mest sällan i en förening?",
     "guess": "Hur många gånger idrottade barn och unga (7–20 år) i {kommun} i en förening under året, i snitt?",
     "vs": "antalet idrottstillfällen i förening per barn och ungdom (7–20 år)",
     "minGapRel": 0.2,
     "note": "Antal deltagartillfällen i idrottsföreningar under året per invånare 7–20 år."},
]

# Kommuner som aldrig ska vara med i ett visst nyckeltal anges i "exclude".
# "guess" är frågetexten för "Gissa siffran"; {kommun} byts mot kommunens namn.
# "vs" används i läget "Min kommun mot riket": "Är <vs> i <kommun> högre eller lägre än i riket?"
#   Saknas för befolkning, där rikets värde är en summa och inte går att jämföra med.
# "minCount" sänker kravet på antal kommuner med värde (standard 250) för nyckeltal där Kolada döljer små kommuner.
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
