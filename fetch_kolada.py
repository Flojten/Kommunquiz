"""Hämtar kommunlistan och nyckeltalen i build.KPIS från Koladas API v3 och skriver data/.

För varje nyckeltal väljs det senaste året där minst MIN_MUNICIPALITIES kommuner (eller minCount i KPIS) har värde.
Valt år sparas i data/years.txt och används av build.py. Inget skrivs om något steg misslyckas.

    python3 fetch_kolada.py
"""
import datetime, json, re, sys, time, urllib.error, urllib.request

from build import DATA, KPIS

API = "https://api.kolada.se/v3"
PER_PAGE = 5000
MIN_MUNICIPALITIES = 250
YEARS_BACK = 6


def get_json(url):
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "kommunquiz"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except (urllib.error.URLError, TimeoutError) as e:
            if isinstance(e, urllib.error.HTTPError) and e.code < 500 and e.code != 429:
                raise
            if attempt == 3:
                raise
            time.sleep(2 ** (attempt + 1))


def get_all(url):
    """Följer next_url tills alla sidor är hämtade."""
    rows = []
    while url:
        page = get_json(url)
        rows += page.get("values", [])
        url = page.get("next_url")
    return rows


def is_municipality(mid):
    # Riket (0000), regioner (0001–0025) och grupper (G...) är inte kommuner.
    return bool(re.fullmatch(r"\d{4}", mid)) and int(mid) > 25


def fetch_municipalities():
    rows = get_all(f"{API}/municipality?per_page={PER_PAGE}")
    names = {r["id"]: r["title"] for r in rows
             if is_municipality(r["id"]) and r.get("type", "K") == "K"}
    if len(names) != 290:
        sys.exit(f"Väntade 290 kommuner från Kolada, fick {len(names)}")
    return dict(sorted(names.items()))


def fetch_kpi_year(kpi, year):
    """Returnerar {kommunkod: värde} för kön T. 0000 (riket) tas med."""
    out = {}
    for row in get_all(f"{API}/data/kpi/{kpi}/year/{year}?per_page={PER_PAGE}"):
        mid = row.get("municipality") or row.get("municipality_id")
        if not mid or not (mid == "0000" or is_municipality(mid)):
            continue
        for v in row.get("values", []):
            if v.get("gender") == "T" and v.get("value") is not None:
                out[mid] = float(v["value"])
    return out


def check_title(k):
    """Varnar om label inte längre stämmer med Koladas titel, t.ex. vid fel id."""
    page = get_json(f"{API}/kpi/{k['id']}")
    rows = page.get("values", [page]) if isinstance(page, dict) else page
    title = rows[0].get("title") if rows else None
    if title != k["label"]:
        print(f"  VARNING {k['id']}: Kolada kallar nyckeltalet \"{title}\", label är \"{k['label']}\"")


def fetch_kpi(kpi, min_count=MIN_MUNICIPALITIES):
    this_year = datetime.date.today().year
    for year in range(this_year + 1, this_year - YEARS_BACK, -1):
        vals = fetch_kpi_year(kpi, year)
        n = sum(1 for m in vals if m != "0000")
        if n >= min_count:
            return year, vals
        if n:
            print(f"  {kpi} {year}: bara {n} kommuner, provar året innan")
    sys.exit(f"Hittade inget år med minst {min_count} kommuner för {kpi}")


def fmt(v):
    return str(int(v)) if v == int(v) else repr(v)


def main():
    names = fetch_municipalities()
    files = {"municipalities.txt": "".join(f"{m};{n}\n" for m, n in names.items())}
    years = {}
    for k in KPIS:
        check_title(k)
        year, vals = fetch_kpi(k["id"], k.get("minCount", MIN_MUNICIPALITIES))
        vals = {m: v for m, v in vals.items() if m == "0000" or m in names}
        years[k["id"]] = year
        files[f"{k['id']}.txt"] = "".join(f"{m};{fmt(v)}\n" for m, v in sorted(vals.items()))
        print(f"{k['id']} {year}: {len(vals) - ('0000' in vals)} kommuner, riket: {vals.get('0000')}")
    files["years.txt"] = "".join(f"{kid};{y}\n" for kid, y in years.items())

    DATA.mkdir(exist_ok=True)
    for name, text in files.items():
        (DATA / name).write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
