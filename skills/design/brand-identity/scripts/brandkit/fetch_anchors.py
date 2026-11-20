"""Fetch the anchor SVGs listed in anchors.json into a cache, from owner sources only.

Usage: python -B -m brandkit.fetch_anchors ANCHORS.json CACHE_DIR  (or: run.py anchors SLUG)

Writes CACHE_DIR/<set>/<slug>.svg and CACHE_DIR/lock.json (sha256 per anchor). On a later
run, a changed hash is reported as a warning ("owner changed the file"), never silently
accepted. Throwaway prototype for issue 28; the real script is specified at spec assembly.
"""
import hashlib
import io
import json
import re
import sys
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0 Safari/537.36")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def balanced_svg(html, start):
    """Return the <svg>…</svg> starting at `start`, honouring nested <svg> tags."""
    depth, i = 0, start
    for m in re.finditer(r"<svg\b|</svg>", html[start:]):
        depth += 1 if m.group(0) == "<svg" else -1
        if depth == 0:
            return html[start:start + m.end()]
    raise ValueError("unterminated <svg>")


def ensure_ns(svg):
    if "xmlns=" not in svg.split(">", 1)[0]:
        svg = svg.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
    return svg


def fetch(a):
    k = a["kind"]
    if k == "url":
        svg = get(a["url"]).decode("utf-8", "replace")
    elif k == "inline":
        html = get(a["url"]).decode("utf-8", "replace")
        m = re.search(a["tag_re"], html)
        if not m:
            raise ValueError("inline <svg> not found on page")
        svg = ensure_ns(balanced_svg(html, m.start()))
    elif k == "sprite":
        html = get(a["url"]).decode("utf-8", "replace")
        path = re.search(a["sprite_re"], html).group(0)
        sprite = get(urllib.parse.urljoin(a["url"], path)).decode("utf-8", "replace")
        m = re.search(r'<symbol[^>]*id="%s"[^>]*>(.*?)</symbol>' % re.escape(a["symbol"]), sprite, re.S)
        vb = re.search(r'viewBox="([^"]+)"', m.group(0)).group(1)
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{m.group(1)}</svg>'
    elif k == "page_link":
        html = get(a["url"]).decode("utf-8", "replace")
        for link in dict.fromkeys(re.findall(a["link_re"], html)):
            body = get(link).decode("utf-8", "replace")
            if re.search(a["content_re"], body):
                svg = body
                break
        else:
            raise ValueError("no linked SVG matched")
    elif k == "zip":
        z = zipfile.ZipFile(io.BytesIO(get(a["url"])))
        member = next(n for n in z.namelist() if re.search(a["member_re"], n))
        svg = z.read(member).decode("utf-8", "replace")
    else:
        raise ValueError(f"unknown kind {k}")
    if a.get("recolour"):
        svg = re.sub(r'(fill|stroke)="(#fff(?:fff)?|white)"', rf'\1="{a["recolour"]}"', svg, flags=re.I)
        svg = re.sub(r'(fill|stroke):\s*(#fff(?:fff)?|white)', rf'\1:{a["recolour"]}', svg, flags=re.I)
    return svg


def main(manifest, cache):
    cache = Path(cache)
    lockf = cache / "lock.json"
    lock = json.loads(lockf.read_text()) if lockf.exists() else {}
    sets = json.loads(Path(manifest).read_text(encoding="utf-8"))["sets"]
    status = {}
    for set_name, anchors in sets.items():
        for a in anchors:
            key = f"{set_name}/{slug(a['name'])}"
            try:
                for attempt in range(3):  # owner pages are A/B-served: an inline mark can be absent on one load
                    try:
                        svg = fetch(a)
                        break
                    except ValueError:
                        if attempt == 2:
                            raise
                h = hashlib.sha256(svg.encode()).hexdigest()
                out = cache / f"{key}.svg"
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(svg, encoding="utf-8")
                note = "ok"
                if key in lock and lock[key] != h:
                    note = "WARN owner file changed since last pin"
                lock[key] = h
                status[key] = note
            except Exception as e:  # report and carry on; a failed anchor is dropped from the board
                status[key] = f"FAIL {type(e).__name__}: {e}"
            print(f"{status[key]:<45} {key}")
    lockf.write_text(json.dumps(lock, indent=2))
    (cache / "status.json").write_text(json.dumps(status, indent=2))


if __name__ == "__main__":
    main(*sys.argv[1:3])
