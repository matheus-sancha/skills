"""Google Fonts access: search the catalogue and fetch a family with its licence.

- Search uses fonts.google.com/metadata/fonts, the JSON the site itself loads. It is not a documented
  API, so if it fails, fall back to an exact family name.
- Files come from the public google/fonts repository (ofl/, apache/, ufl/), the source of fonts.google.com.
  The family's METADATA.pb licence must be OFL, APACHE2 or UFL; the licence text is saved beside the font.
- No API key is needed. Fetched fonts go to the run's .cache/fonts/ and reach the user only in the kit's
  type/ folder, with the licence file.

Usage:
  python -B -m brandkit.fonts search [--query TEXT] [--category "Serif"] [--variable] [--limit 20]
  python -B -m brandkit.fonts get "Family Name" DEST_DIR [--italics]
"""
import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

META = "https://fonts.google.com/metadata/fonts"
RAW = "https://raw.githubusercontent.com/google/fonts/main"
LICENCES = {"OFL": ("ofl", "OFL.txt"), "APACHE2": ("apache", "LICENSE.txt"), "UFL": ("ufl", "UFL.txt")}
OVERUSED = {"Inter", "Roboto", "Open Sans", "Poppins", "Montserrat"}


def _get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": "brand-identity-skill"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    return data if binary else data.decode("utf-8")


def search(query=None, category=None, variable=False, limit=20):
    fams = json.loads(_get(META))["familyMetadataList"]
    out = []
    for f in fams:
        if query and query.lower() not in f["family"].lower():
            continue
        if category and f["category"].lower() != category.lower():
            continue
        if variable and not f.get("axes"):
            continue
        out.append({"family": f["family"], "category": f["category"],
                    "axes": [a["tag"] for a in f.get("axes", [])], "styles": len(f.get("fonts", {})),
                    "overused": f["family"] in OVERUSED})
    return out[:limit]


def _slug(family):
    return re.sub(r"[^a-z0-9]", "", family.lower())


def get(family, dest, italics=False):
    slug = _slug(family)
    for lic, (folder, lic_file) in LICENCES.items():
        try:
            meta = _get(f"{RAW}/{folder}/{slug}/METADATA.pb")
        except Exception:
            continue
        m = re.search(r'^license: "(\w+)"', meta, re.M)
        if not m or m.group(1) not in LICENCES:
            raise SystemExit(f"{family}: licence {m.group(1) if m else '?'} not allowed")
        files = sorted(set(re.findall(r'filename: "([^"]+)"', meta)))
        if not italics:
            files = [f for f in files if "italic" not in f.lower()] or files
        dest = Path(dest); dest.mkdir(parents=True, exist_ok=True)
        saved = []
        for fn in files:
            (dest / fn).write_bytes(_get(f"{RAW}/{folder}/{slug}/{urllib.parse.quote(fn)}", binary=True))
            saved.append(fn)
        lic_name = f"{lic_file.split('.')[0]}-{slug}.txt"
        (dest / lic_name).write_bytes(_get(f"{RAW}/{folder}/{slug}/{lic_file}", binary=True))
        return {"family": family, "licence": m.group(1), "files": saved, "licence_file": lic_name}
    raise SystemExit(f"{family}: not found in google/fonts (check the exact family name with 'search')")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search"); s.add_argument("--query"); s.add_argument("--category")
    s.add_argument("--variable", action="store_true"); s.add_argument("--limit", type=int, default=20)
    g = sub.add_parser("get"); g.add_argument("family"); g.add_argument("dest"); g.add_argument("--italics", action="store_true")
    a = ap.parse_args()
    if a.cmd == "search":
        for r in search(a.query, a.category, a.variable, a.limit):
            print(f"{r['family']:<32} {r['category']:<12} axes={','.join(r['axes']) or '-':<14}"
                  f"{' (overused: avoid)' if r['overused'] else ''}")
    else:
        print(json.dumps(get(a.family, a.dest, a.italics), indent=1))
