"""Run folder and state.json (references/state.md). Revisions are <name>.r<N>.<ext>, never overwritten."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

STAGES = ["brief", "audit", "territory", "routes", "refine", "system", "kit"]
FOLDERS = ["02-audit", "03-territory/boards", "04-routes", "05-refine/lockups", "06-system", "07-kit", ".cache"]


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_dir(slug, root="brand"):
    return Path(root) / slug


def load(slug, root="brand"):
    return json.loads((run_dir(slug, root) / "state.json").read_text(encoding="utf-8"))


def save(st, root="brand"):
    st["updated_at"] = now()
    p = run_dir(st["slug"], root) / "state.json"
    p.write_text(json.dumps(st, indent=1), encoding="utf-8")


def init(slug, entry="full", root="brand"):
    d = run_dir(slug, root)
    if (d / "state.json").exists():
        return load(slug, root)
    for f in FOLDERS:
        (d / f).mkdir(parents=True, exist_ok=True)
    if entry == "byom":
        (d / "02-intake/source").mkdir(parents=True, exist_ok=True)
    stages = {s: {"status": "todo", "current_rev": None} for s in STAGES}
    if entry == "byom":
        stages["territory"]["status"] = stages["routes"]["status"] = "skipped"
        stages["intake"] = stages.pop("audit")
    st = {"schema": 1, "slug": slug, "entry": entry, "stage": "brief", "stages": stages, "decisions": [],
          "routes": [], "budget": {"replacements_used": 0}, "probe": None,
          "connectors": {"miro": False, "figma": False, "hyperframes": False},
          "created_at": now(), "updated_at": now()}
    (d / "run-log.md").write_text(f"# Run log: {slug}\n\nentry: {entry}\n", encoding="utf-8")
    save(st, root)
    return st


def next_rev(folder, name, ext):
    """Next free revision: name.r1.ext, name.r2.ext ..."""
    folder = Path(folder)
    n = [int(m.group(1)) for p in folder.glob(f"{name}.r*.{ext}")
         if (m := re.match(rf"{re.escape(name)}\.r(\d+)\.{re.escape(ext)}$", p.name))]
    return f"r{max(n, default=0) + 1}"


def decide(st, stage, text, by="user"):
    st["decisions"].append({"id": f"D{len(st['decisions']) + 1}", "stage": stage, "text": text, "by": by, "at": now()})
    return st


def set_stage(st, stage, status, rev=None):
    st["stages"][stage]["status"] = status
    if rev:
        st["stages"][stage]["current_rev"] = rev
    if status in ("in_progress", "awaiting_user"):
        st["stage"] = stage
    return st


def reopen(st, stage):
    order = [s for s in st["stages"]]
    i = order.index(stage)
    st["stages"][stage]["status"] = "in_progress"
    for s in order[i + 1:]:
        if st["stages"][s]["status"] not in ("todo", "skipped"):
            st["stages"][s]["status"] = "stale"
    st["stage"] = stage
    return st


def log(slug, stage, rev, action, hard_fails="none", flags="none", redraws="", user="—", root="brand"):
    t = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    entry = (f"\n## {t} · {stage}" + (f" · {rev}" if rev else "") + f"\naction: {action}\n"
             f"hard fails: {hard_fails} · flags: {flags}\n" + (f"redraws: {redraws} · " if redraws else "") + f"user: {user}\n")
    with open(run_dir(slug, root) / "run-log.md", "a", encoding="utf-8") as f:
        f.write(entry)


def status_line(st):
    last = st["decisions"][-1]["text"] if st["decisions"] else "no decisions yet"
    shown = [r["id"] for r in st["routes"] if r["status"] in ("shown", "chosen")]
    return (f"{st['slug']}: stage {st['stage']} ({st['stages'].get(st['stage'], {}).get('status', st['stage'])}); "
            f"routes shown {shown or 'none'}.\nLast decision: {last}")


def summary(st, root="brand"):
    rs = st["routes"]
    rows = ["", "## Summary", "", "| measure | value |", "|---|---|",
            f"| routes tried | {len(rs)} |",
            f"| routes shown | {sum(r['status'] in ('shown', 'chosen', 'rejected') for r in rs)} |",
            f"| routes withheld | {sum(r['status'] == 'withheld' for r in rs)} |",
            "| redraws per route | " + (", ".join("%s:%s" % (r["id"], r.get("redraws", 0)) for r in rs) or "—") + " |",
            f"| reopened stages | {sum('reopen' in d['text'].lower() for d in st['decisions'])} |",
            f"| probe tier | {(st.get('probe') or {}).get('tier', '—')} |"]
    with open(run_dir(st["slug"], root) / "run-log.md", "a", encoding="utf-8") as f:
        f.write("\n".join(rows) + "\n")
