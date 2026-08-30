#!/usr/bin/env python3
"""Report the state of the current pass — coverage, review queue, trend.

The judgment layer is the expensive half of a pass, so the question that opens
every session is "what still needs reviewing?". That used to be answered by a
hand-written session brief, which within a day of being written was carrying a
decision that had already been reversed. This tool derives the answer instead:
the state lives in git and in ``lectures/data``; a report reads it back.

    python3 tools/qestyle_status.py
    python3 tools/qestyle_status.py --queue 20        # just the next 20 stems
    python3 tools/qestyle_status.py --json

Freshness comes from ``lectures/data/lecture_blobs.csv`` (written by
``qestyle_scan.py``, one blob SHA per lecture at the pinned snapshot) joined
against each overlay's ``source.blob``. An overlay with no ``source`` key is
*unstamped* — counted on its own line and never as fresh, because nothing
records which text it judged.

That file is also where the lecture universe comes from, so a lecture with no
row in it would be absent from the coverage table and the queue alike rather
than reported as missing. ``snapshot.json`` counted the same lectures
independently; the two are cross-checked and any shortfall is a problem, since
"queue empty" over half a corpus is the worst thing this report could say.

Read-only, and always exits 0: it is a report, not a gate.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import textwrap

SERIES_ORDER = ["lecture-python-intro", "lecture-python-programming",
                "lecture-python.myst", "lecture-python-advanced.myst", "lecture-dp"]
CATS = ["writing", "math", "code", "figures", "references", "links", "admonitions"]
PRIOS = ["HIGH", "MEDIUM", "LOW", "NONE"]
STATUSES = ["fresh", "stale", "unstamped", "unknown", "missing"]
BACKFILL = "tools/qestyle_backfill_provenance.py"
SCOL = 30                                  # width of the series column
WRAP = 88


def rank(series):
    """Sort key putting the five known series in book order, strays after."""
    return (SERIES_ORDER.index(series) if series in SERIES_ORDER
            else len(SERIES_ORDER), series)


# --- loading -------------------------------------------------------------
#
# Every loader returns ``None`` for "file not there" and records why in
# ``sources``, so a half-built tree degrades to a message instead of a
# traceback. Nothing here writes.

def read_rows(path, sources):
    """CSV rows as dicts, or None if absent/unreadable."""
    if not os.path.exists(path):
        sources[path] = "absent"
        return None
    try:
        with open(path, newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
    except OSError as exc:
        sources[path] = f"unreadable ({exc.__class__.__name__})"
        return None
    sources[path] = f"{len(rows)} rows"
    return rows


def read_json(path, sources):
    if not os.path.exists(path):
        sources[path] = "absent"
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            obj = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        sources[path] = f"unreadable ({exc.__class__.__name__})"
        return None
    sources[path] = "read"
    return obj


def load_blobs(data, sources):
    """{(series, lecture): blob}, or None if lecture_blobs.csv is absent."""
    rows = read_rows(os.path.join(data, "lecture_blobs.csv"), sources)
    if rows is None:
        return None
    out = {}
    for r in rows:
        series, lecture = (r.get("series") or "").strip(), (r.get("lecture") or "").strip()
        if series and lecture:
            out[(series, lecture)] = (r.get("blob") or "").strip()
    return out


def load_scores(data, sources):
    """{(series, lecture): (overall, priority)} from scores.csv."""
    rows = read_rows(os.path.join(data, "scores.csv"), sources) or []
    out = {}
    for r in rows:
        key = ((r.get("series") or "").strip(), (r.get("lecture") or "").strip())
        try:
            overall = float(r.get("overall", ""))
        except (TypeError, ValueError):
            overall = None
        out[key] = (overall, (r.get("priority") or "").strip())
    return out


def load_overlays(reviews, problems):
    """{(series, lecture): {blob, commit, doubts, path}} for every overlay.

    Keyed on where the file *is*, not on the ``series``/``lecture`` it names
    inside. Two paths cannot collide, so a copy-pasted overlay whose ``lecture``
    field was never updated can no longer silently overwrite the review it was
    copied from — it is loaded under its own name, and the disagreement between
    its fields and its location is reported instead.
    """
    out = {}
    if not os.path.isdir(reviews):
        problems.append(f"{reviews}/ is not a directory — no overlays read")
        return out
    for series in sorted(os.listdir(reviews)):
        sdir = os.path.join(reviews, series)
        if not os.path.isdir(sdir):
            continue
        for fn in sorted(os.listdir(sdir)):
            if not fn.endswith(".json"):
                continue
            path = os.path.join(sdir, fn)
            try:
                with open(path, encoding="utf-8") as fh:
                    ov = json.load(fh)
            except (OSError, json.JSONDecodeError) as exc:
                problems.append(f"{path}: {exc.__class__.__name__}, skipped")
                continue
            if not isinstance(ov, dict):
                problems.append(f"{path}: not a JSON object, skipped")
                continue
            src = ov.get("source")
            src = src if isinstance(src, dict) else {}
            doubts = [d for d in (ov.get("scanner_doubts") or []) if str(d).strip()]
            key = (series, fn[:-5])
            named = (str(ov.get("series") or ""), str(ov.get("lecture") or ""))
            if (named[0] and named[0] != key[0]) or (named[1] and named[1] != key[1]):
                problems.append(
                    f"{path}: names {named[0] or '?'}/{named[1] or '?'} inside but sits "
                    f"at {key[0]}/{key[1]} — read under its path; one of the two is wrong")
            out[key] = {
                "blob": (str(src.get("blob") or "")).strip() or None,
                "commit": (str(src.get("commit") or "")).strip() or None,
                "doubts": len(doubts),
                "path": path,
            }
    return out


# --- classification ------------------------------------------------------

def same_blob(a, b):
    """Blob SHAs match. Abbreviations count: a prefix is not a stale review."""
    if a == b:
        return True
    n = min(len(a), len(b))
    return n >= 7 and a[:n] == b[:n]


def classify(key, blobs, overlays):
    """fresh | stale | unstamped | unknown | missing for one lecture."""
    ov = overlays.get(key)
    if ov is None:
        return "missing"
    if ov["blob"] is None:
        return "unstamped"
    current = blobs.get(key) if blobs is not None else None
    if not current:
        return "unknown"
    return "fresh" if same_blob(current, ov["blob"]) else "stale"


def shortfall(per, snapshot, basis, problems):
    """Series where the lecture list is short of the pinned snapshot.

    ``keys`` — and therefore the coverage table *and* the queue — come from the
    lecture list, so a lecture with no row in it is not ``missing``: it is
    absent, present in neither. An interrupted or partial scan would then read
    as a finished one, and the queue would say "empty" about a corpus half of
    which had never been looked at. ``snapshot.json`` counted the same lectures
    independently, so it is the check: any series listing fewer lectures than
    the snapshot declares is a shortfall, and goes to ``problems``.

    Returns ``{series: (declared, listed)}`` for the short series only.
    """
    def as_int(value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    short = {}
    for series, declared in (snapshot.get("per_series") or {}).items():
        n = as_int(declared)
        if n is None:
            continue
        listed = per.get(series, {}).get("lectures", 0)
        if listed < n:
            short[series] = (n, listed)

    listed_total = sum(row.get("lectures", 0) for row in per.values())
    declared_total = as_int(snapshot.get("n_lectures"))
    where = basis or "the lecture list"
    if short:
        gap = sum(n - listed for n, listed in short.values())
        detail = ", ".join(f"{s} lists {listed} of {n}"
                           for s, (n, listed) in sorted(short.items(),
                                                        key=lambda kv: rank(kv[0])))
        problems.append(
            f"SHORTFALL: {where} is short {n_of(gap, 'lecture')} of "
            f"snapshot.json ({detail}). Absent from both the coverage table and the "
            f"queue, so an empty queue here is not evidence that "
            f"nothing needs reviewing. Re-run tools/qestyle_scan.py.")
    elif declared_total is not None and listed_total < declared_total:
        problems.append(
            f"SHORTFALL: {where} lists {listed_total} lectures, snapshot.json counted "
            f"{declared_total}. {n_of(declared_total - listed_total, 'lecture')} in "
            f"neither the coverage table nor the queue. Re-run tools/qestyle_scan.py.")
    return short


def build(data, reviews):
    """Everything the report and the JSON both need, measured once."""
    sources, problems = {}, []
    blobs = load_blobs(data, sources)
    snapshot = read_json(os.path.join(data, "snapshot.json"), sources) or {}
    scores = load_scores(data, sources)
    history = read_rows(os.path.join(data, "history.csv"), sources) or []
    overlays = load_overlays(reviews, problems)

    # ``if blobs`` and not ``if blobs is not None``: a present but empty blob
    # table is no lecture list at all, and must not out-rank a readable
    # scores.csv the way a header-only file used to.
    if blobs:
        keys, basis = set(blobs), "lecture_blobs.csv"
    elif scores:
        keys, basis = set(scores), "scores.csv"
    else:
        keys, basis = set(), ""
    keys = sorted(keys, key=lambda k: (rank(k[0]), k[1]))

    status = {k: classify(k, blobs, overlays) for k in keys}
    orphans = sorted(set(overlays) - set(keys), key=lambda k: (rank(k[0]), k[1]))

    per = {}
    for series, lecture in keys:
        row = per.setdefault(series, dict.fromkeys(STATUSES, 0))
        row[status[(series, lecture)]] += 1
        row["lectures"] = row.get("lectures", 0) + 1

    short = shortfall(per, snapshot, basis, problems)

    periods = sorted({r.get("period", "") for r in history} - {""})
    return {
        "data": data,
        "history_path": os.path.join(data, "history.csv"),
        "period": periods[-1] if periods else None,
        "periods": periods,
        "snapshot": snapshot.get("snapshot") or {},
        "snapshot_per_series": snapshot.get("per_series") or {},
        "snapshot_total": snapshot.get("n_lectures"),
        "shortfall": short,
        "basis": basis,
        "blobs": blobs,
        "scores": scores,
        "history": history,
        "overlays": overlays,
        "keys": keys,
        "status": status,
        "orphans": orphans,
        "per": per,
        "sources": sources,
        "problems": problems,
    }


def totals(per):
    tot = dict.fromkeys(STATUSES, 0)
    tot["lectures"] = 0
    for row in per.values():
        for k in list(STATUSES) + ["lectures"]:
            tot[k] += row.get(k, 0)
    return tot


def queue(st):
    """Lectures needing review, worst-first.

    Missing overlays before stale ones; then the series with the least fresh
    coverage before one that is nearly done; then ascending overall score, so
    the weakest lecture in the weakest series is reviewed first. A lecture with
    no score yet (new to the corpus) sorts ahead of every scored one.
    """
    need = [(s, l) for (s, l) in st["keys"] if st["status"][(s, l)] in ("missing", "stale")]
    cov, deficit = {}, {}
    for series, row in st["per"].items():
        n = row.get("lectures", 0)
        cov[series] = (row.get("fresh", 0) / n) if n else 1.0
        deficit[series] = row.get("missing", 0) + row.get("stale", 0)

    def key(entry):
        series, lecture = entry
        overall = (st["scores"].get(entry) or (None, ""))[0]
        return (0 if st["status"][entry] == "missing" else 1,
                cov.get(series, 1.0), -deficit.get(series, 0), rank(series),
                -1.0 if overall is None else overall, lecture)

    return sorted(need, key=key)


def doubts(st):
    """[(series, lecture, n)] for overlays raising at least one doubt."""
    out = [(s, l, ov["doubts"]) for (s, l), ov in st["overlays"].items() if ov["doubts"]]
    return sorted(out, key=lambda e: (rank(e[0]), -e[2], e[1]))


# --- plain-text report ---------------------------------------------------

def head(title):
    print()
    print(title)
    print("-" * len(title))


def n_of(n, singular, plural=None):
    """``1 overlay`` / ``2 overlays`` — counts read wrong without this."""
    return f"{n} {singular if n == 1 else (plural or singular + 's')}"


def note(text, indent="  "):
    """One wrapped note, so a long tool path does not run off the screen."""
    print(textwrap.fill(" ".join(text.split()), width=WRAP,
                        initial_indent=indent, subsequent_indent=indent))


def print_period(st):
    head("period and snapshot")
    if st["period"]:
        print(f"  current period    {st['period']}   (latest row in history.csv)")
    else:
        why = ("history.csv absent" if st["sources"].get(st["history_path"]) == "absent"
               else "no period column or no rows in history.csv")
        print(f"  current period    unknown — {why}")
    snap = st["snapshot"]
    if not snap:
        print("  snapshot.json absent or empty — no pinned commits to report")
        return
    print()
    print(f"  {'series':<{SCOL}}{'lectures':>9}  {'commit':<10}date")
    for series in sorted(snap, key=rank):
        info = snap[series] or {}
        n = st["per"].get(series, {}).get("lectures", 0)
        print(f"  {series:<{SCOL}}{n:>9}  {str(info.get('commit',''))[:8]:<10}"
              f"{info.get('date','')}")
    tot = totals(st["per"])
    print(f"  {'TOTAL':<{SCOL}}{tot['lectures']:>9}")
    declared = st["snapshot_per_series"]
    for series, n in sorted(declared.items(), key=lambda kv: rank(kv[0])):
        seen = st["per"].get(series, {}).get("lectures", 0)
        if seen != n:
            print(f"  note: snapshot.json says {series} has {n} lectures, "
                  f"{st['basis'] or 'the data'} shows {seen}")


def list_failures(st):
    """Why each candidate lecture list is unusable — naming only the ones that are.

    ``sources`` already records what happened to every file read, so the message
    can say *absent* or *0 rows* about the file that actually failed instead of
    blaming both.
    """
    out = []
    for name, usable in (("lecture_blobs.csv", bool(st["blobs"])),
                         ("scores.csv", bool(st["scores"]))):
        if usable:
            continue
        why = st["sources"].get(os.path.join(st["data"], name), "not read")
        out.append(f"{name} ({why})")
    return out


def print_shortfall(st):
    """One line where a wrong conclusion would otherwise be drawn."""
    if not st["shortfall"]:
        return
    gap = sum(n - listed for n, listed in st["shortfall"].values())
    note(f"! {n_of(gap, 'lecture')} counted in snapshot.json but absent from "
         f"{st['basis'] or 'the lecture list'} — not listed below and not queued. "
         f"See the problems under `inputs`.")


def print_coverage(st):
    head("judgment-layer coverage")
    if not st["keys"]:
        note("no lecture list: " + " and ".join(list_failures(st)) +
             ", so coverage cannot be computed. Run tools/qestyle_scan.py first.")
        print_shortfall(st)
        return
    cols = ["lectures"] + STATUSES
    print(f"  {'series':<{SCOL}}" + "".join(f"{c:>11}" for c in cols))
    for series in sorted(st["per"], key=rank):
        row = st["per"][series]
        print(f"  {series:<{SCOL}}" + "".join(f"{row.get(c, 0):>11}" for c in cols))
    tot = totals(st["per"])
    print(f"  {'TOTAL':<{SCOL}}" + "".join(f"{tot[c]:>11}" for c in cols))
    print()
    note(f"lecture list from {st['basis']}; an overlay is fresh when its source.blob "
         f"equals that lecture's current blob.")
    print_shortfall(st)
    if not st["blobs"]:
        why = "is absent" if st["blobs"] is None else "has no lecture rows"
        note(f"lecture_blobs.csv {why}, so no overlay can be shown fresh or stale. "
             "Re-run tools/qestyle_scan.py — it writes that file alongside the rest.")
    if tot["unstamped"]:
        note(f"unstamped ({n_of(tot['unstamped'], 'overlay')}): no source stamp, so the "
             f"overlay records a judgment but not the text it judged and freshness cannot "
             f"be decided. {BACKFILL} adds the stamp from the pinned snapshot; nothing "
             f"unstamped is counted as fresh here.")
    if tot["unknown"]:
        note(f"unknown ({n_of(tot['unknown'], 'overlay')}): stamped, but with no current "
             f"blob on record for the lecture, so freshness cannot be decided.")
    if st["orphans"]:
        note(f"{n_of(len(st['orphans']), 'overlay')} with no lecture in the corpus "
             f"(renamed or deleted upstream):")
        for series, lecture in st["orphans"][:12]:
            print(f"    {series}/{lecture}")
        if len(st["orphans"]) > 12:
            print(f"    ... {len(st['orphans']) - 12} more")


def print_queue(st, limit=20):
    q = queue(st)
    tot = totals(st["per"])
    head("review queue")
    if not st["keys"]:
        print("  no lecture list, so no queue — see the coverage section.")
        return
    print("  worst-first: missing overlays before stale ones, then the series with the "
          "least")
    print("  fresh coverage, then ascending overall score within a series.")
    print()
    if not q:
        print("  empty — nothing listed is missing or stale.")
        print_shortfall(st)
        if tot["unstamped"]:
            note(f"But {n_of(tot['unstamped'], 'overlay')} unstamped, so this queue is a "
                 f"lower bound: run {BACKFILL}, re-run the scan, and read it again.")
        return
    n_missing = sum(1 for e in q if st["status"][e] == "missing")
    print(f"  {n_of(len(q), 'lecture')} to review ({n_missing} missing, "
          f"{len(q) - n_missing} stale)")
    for i, (series, lecture) in enumerate(q[:limit], 1):
        overall = (st["scores"].get((series, lecture)) or (None, ""))[0]
        cell = "  -  " if overall is None else f"{overall:5.1f}"
        print(f"  {i:>4}. {series + '/' + lecture:<52}{cell}  "
              f"{st['status'][(series, lecture)]}")
    if len(q) > limit:
        print(f"        ... {len(q) - limit} more — `--queue {len(q)}` prints them all")
    if tot["unstamped"]:
        note(f"{n_of(tot['unstamped'], 'unstamped overlay')} not in this queue — "
             f"see the coverage note.")


def print_doubts(st):
    rows = doubts(st)
    head("recorded reviewer doubts")
    print("  Doubts a reviewer raised about the detectors themselves. This is where "
          "rule bugs")
    print("  surface — read them before changing tools/qestyle_rules.py.")
    note("Recorded, not open: the overlay schema has no field marking a doubt "
         "adjudicated, so this tool counts every doubt ever written down and cannot "
         "tell a resolved one from an outstanding one. tools/VERIFICATION.md is the "
         "adjudication record — most of these were answered there.")
    print()
    if not rows:
        print("  none recorded.")
        return
    n = sum(c for _, _, c in rows)
    print(f"  {n_of(n, 'doubt')} across {n_of(len(rows), 'lecture')}")
    for series in sorted({s for s, _, _ in rows}, key=rank):
        here = [(l, c) for s, l, c in rows if s == series]
        line = ", ".join(f"{l} ({c})" if c > 1 else l for l, c in here)
        print(f"  {series}  —  {n_of(len(here), 'lecture')}, "
              f"{n_of(sum(c for _, c in here), 'doubt')}")
        print(textwrap.fill(line, width=WRAP, initial_indent="    ",
                            subsequent_indent="    "))


def print_trend(st):
    head("trend")
    rows = [r for r in st["history"] if (r.get("series") or "") == "TOTAL"]
    if not rows:
        print("  history.csv absent, or it has no TOTAL row.")
        return
    cols = ["lectures"] + CATS + ["overall"] + PRIOS
    label = {"admonitions": "admon", "references": "refs", "MEDIUM": "MED"}
    print(f"  {'period':<9}" + "".join(f"{label.get(c, c):>8}" for c in cols))
    for r in sorted(rows, key=lambda r: r.get("period", "")):
        print(f"  {r.get('period',''):<9}"
              + "".join(f"{(r.get(c) or '-'):>8}" for c in cols))


def print_sources(st, data, reviews):
    head("inputs")
    overlay_glob = os.path.join(reviews, "<series>", "<stem>.json")
    width = max([40] + [len(p) + 2 for p in list(st["sources"]) + [overlay_glob]])
    for path in sorted(st["sources"]):
        print(f"  {path:<{width}}{st['sources'][path]}")
    print(f"  {overlay_glob:<{width}}{n_of(len(st['overlays']), 'overlay')}")
    for p in st["problems"]:
        # A problem usually names a path; keep it in one piece to be pasteable.
        print(textwrap.fill(" ".join(p.split()), width=WRAP,
                            initial_indent="  ! ", subsequent_indent="    ",
                            break_long_words=False, break_on_hyphens=False))


# --- json ----------------------------------------------------------------

def cell(value):
    """A history cell as JSON: a number where it is one, else null, else text.

    The value is passed through, never recomputed — history.csv is the record.
    """
    text = (value or "").strip()
    if not text:
        return None
    try:
        return int(text) if text.lstrip("-").isdigit() else float(text)
    except ValueError:
        return text


def as_json(st, limit):
    q = queue(st)
    tot = totals(st["per"])
    return {
        "period": st["period"],
        "snapshot": {
            s: {"commit": (info or {}).get("commit"),
                "date": (info or {}).get("date"),
                "lectures": st["per"].get(s, {}).get("lectures", 0)}
            for s, info in st["snapshot"].items()
        },
        "coverage": {
            "basis": st["basis"] or None,
            "blobs_available": bool(st["blobs"]),
            "shortfall": {s: {"snapshot": n, "listed": listed}
                          for s, (n, listed) in st["shortfall"].items()},
            "by_series": {s: {c: st["per"][s].get(c, 0) for c in ["lectures"] + STATUSES}
                          for s in st["per"]},
            "total": {c: tot[c] for c in ["lectures"] + STATUSES},
            "orphans": [{"series": s, "lecture": l} for s, l in st["orphans"]],
            "backfill_tool": BACKFILL if tot["unstamped"] else None,
        },
        "queue": [
            {"series": s, "lecture": l, "status": st["status"][(s, l)],
             "overall": (st["scores"].get((s, l)) or (None, ""))[0]}
            for s, l in (q if limit is None else q[:limit])
        ],
        "queue_total": len(q),
        "doubts": {
            "total": sum(c for _, _, c in doubts(st)),
            "lectures": len(doubts(st)),
            "by_lecture": [{"series": s, "lecture": l, "count": c}
                           for s, l, c in doubts(st)],
        },
        "trend": [
            {k: (r.get(k) if k == "period" else cell(r.get(k)))
             for k in ["period", "lectures"] + CATS + ["overall"] + PRIOS}
            for r in sorted((r for r in st["history"]
                             if (r.get("series") or "") == "TOTAL"),
                            key=lambda r: r.get("period", ""))
        ],
        "inputs": st["sources"],
        "problems": st["problems"],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", default="lectures/data", help="measured CSVs and snapshot")
    ap.add_argument("--reviews", default="reviews", help="judgment overlays")
    ap.add_argument("--queue", type=int, default=None, metavar="N",
                    help="print only the next N lectures as <series>/<stem>, one per line")
    ap.add_argument("--json", action="store_true", help="machine-readable, no prose")
    args = ap.parse_args()

    st = build(args.data, args.reviews)

    if args.json:
        print(json.dumps(as_json(st, args.queue), indent=2, sort_keys=False))
        return 0

    if args.queue is not None:
        for series, lecture in queue(st)[:max(args.queue, 0)]:
            print(f"{series}/{lecture}")
        return 0

    print("QuantEcon Lecture Style Compliance — pass status")
    print(f"derived from {args.data}/ and {args.reviews}/; nothing here is hand-maintained")
    print_period(st)
    print_coverage(st)
    print_queue(st)
    print_doubts(st)
    print_trend(st)
    print_sources(st, args.data, args.reviews)
    return 0


if __name__ == "__main__":
    sys.exit(main())
