#!/usr/bin/env python3
"""Scan the QuantEcon lecture corpus for mechanically-detectable style violations.

This is the evidence layer of the audit. It measures; it does not score. Every
count it emits is reproducible from a pinned corpus snapshot, which removes the
per-pass judgment drift that the mechanical rules used to be exposed to (see
`ROADMAP.md` § Risks). Scoring against the rubric in `lectures/spec.md` still
happens in the review pass, informed by this evidence.

Usage
-----
    python3 tools/qestyle_scan.py --corpus /path/to/quantecon --out lectures/data

Expects each series checked out at ``<corpus>/<series>/lectures/*.md``.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from qestyle_lex import lex                                    # noqa: E402
from qestyle_rules import (                                    # noqa: E402
    BUILD_RISK, CATEGORY, CHECKS, PROPOSED, count_citations, load_rule_titles,
    plot_line_widths, run_all,
)

SERIES = [
    "lecture-python-intro",
    "lecture-python-programming",
    "lecture-python.myst",
    "lecture-python-advanced.myst",
    "lecture-dp",
]


def applicability(doc):
    """Which audit categories apply to this lecture.

    ``N/A`` means the category has nothing to score (no code cells, no maths).
    JAX is always ``out of scope`` for these five series — that is a scope
    decision, not an inapplicability.
    """
    code = doc.code_text()
    math = doc.math_text()
    n_code = len([l for l in doc.lines if l.kind == "code"])
    has_plot = bool(re.search(r"\b(?:plt|ax|axes|fig)\b|matplotlib|plotly", code))
    has_fig_directive = any(n in ("figure", "image") for _, n, _, _, _ in doc.directives)
    cites, cites_t = count_citations(doc)
    has_admon = any(
        n in ("exercise", "exercise-start", "solution", "solution-start", "note",
              "warning", "admonition", "tip", "important", "hint", "prf:theorem",
              "prf:proof", "prf:definition", "prf:lemma", "prf:example")
        for _, n, _, _, _ in doc.directives
    )
    return {
        "writing": True,
        "math": len(math.strip()) > 40,
        "code": n_code > 3,
        "jax": "out of scope",
        "figures": has_plot or has_fig_directive,
        "references": (cites + cites_t) > 0,
        "links": True,
        "admonitions": has_admon,
    }


def lecture_files(corpus, series):
    """Every lecture ``.md`` in one series, as paths, in a stable order.

    One list, used by both the scan and the blob stamping, so the two cannot
    disagree about which files the pass looked at.
    """
    root = os.path.join(corpus, series, "lectures")
    return [os.path.join(root, f)
            for f in sorted(os.listdir(root)) if f.endswith(".md")]


def scan_series(corpus, series, files=None):
    files = lecture_files(corpus, series) if files is None else files
    out = []
    for path in files:
        fn = os.path.basename(path)
        doc = lex(path, series)
        hits = run_all(doc)
        cites, cites_t = count_citations(doc)
        rec = {
            "line_widths": [[w, k] for _, w, k in plot_line_widths(doc)],
            "series": series,
            "lecture": fn[:-3],
            "lines": doc.n_lines,
            "code_lines": len([l for l in doc.lines if l.kind == "code"]),
            "math_lines": len([l for l in doc.lines if l.kind == "math"]),
            "cite": cites,
            "cite_t": cites_t,
            "applicable": applicability(doc),
            "violations": {
                rule: {
                    "count": len(hs),
                    "lines": sorted({h.line for h in hs})[:24],
                    "samples": [h.detail for h in hs[:4]],
                }
                for rule, hs in sorted(hits.items())
            },
        }
        out.append(rec)
    return out


def git_snapshot(corpus, series):
    try:
        sha = subprocess.run(
            ["git", "-C", os.path.join(corpus, series), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True).stdout.strip()
        date = subprocess.run(
            ["git", "-C", os.path.join(corpus, series), "log", "-1",
             "--format=%ad", "--date=short"],
            capture_output=True, text=True, check=True).stdout.strip()
        return {"commit": sha, "date": date}
    except Exception:
        return {"commit": "", "date": ""}


def git_blobs(corpus, series, commit):
    """Git blob SHA of every lecture ``.md`` in one series at the pinned commit.

    What the *commit* holds — not necessarily what was scanned. Used only to
    check the working tree against the pin (see ``working_blobs``); the SHA
    written to ``lecture_blobs.csv`` is the one hashed from the scanned file.
    One ``ls-tree`` per series, not one per file.

    Returns ``{stem: sha}``, empty if git or the tree cannot be read.
    """
    if not commit:
        return {}
    try:
        out = subprocess.run(
            ["git", "-C", os.path.join(corpus, series), "ls-tree", "-z",
             commit, "--", "lectures/"],
            capture_output=True, text=True, check=True).stdout
    except Exception as exc:
        print(f"warning: no blob SHAs for {series}: {exc}", file=sys.stderr)
        return {}
    blobs = {}
    for entry in out.split("\0"):
        if not entry:
            continue
        meta, _, name = entry.partition("\t")
        fields = meta.split()
        if len(fields) != 3 or fields[1] != "blob" or not name.endswith(".md"):
            continue
        blobs[os.path.basename(name)[:-3]] = fields[2]
    return blobs


def _names(stems, limit=6):
    return ", ".join(stems[:limit]) + (" ..." if len(stems) > limit else "")


def warn_if_dirty(series, commit, working, committed):
    """Warn when the text that was scanned is not the text the pin holds.

    Not fatal — the blob table is still correct, because it now describes the
    scanned text — but a dirty corpus means the pass no longer reproduces from
    ``snapshot.json`` alone, which is worth knowing before the numbers are
    published.
    """
    if not committed:
        return
    changed = sorted(s for s, sha in working.items()
                     if s in committed and committed[s] != sha)
    extra = sorted(set(working) - set(committed))
    gone = sorted(set(committed) - set(working))
    if not (changed or extra or gone):
        return
    parts = []
    if changed:
        parts.append(f"{len(changed)} modified ({_names(changed)})")
    if extra:
        parts.append(f"{len(extra)} not in the commit ({_names(extra)})")
    if gone:
        parts.append(f"{len(gone)} in the commit but not on disk ({_names(gone)})")
    print(f"warning: {series} working tree differs from pinned commit "
          f"{commit[:8]}: " + "; ".join(parts) + " — the blob SHAs written for this "
          "series describe the text that was scanned, not the commit",
          file=sys.stderr)


def working_blobs(corpus, series, files, commit):
    """Git blob SHA of the working-tree text of every lecture in one series.

    The scan lexes the file on disk, so the SHA stamped beside its counts has to
    describe *that* text. Reading it from the pinned commit is right only while
    the checkout is clean, and wrong silently when it is not: the overlay would
    name a version the reviewer never read, and — because the stamp matches the
    commit the next scan also reports — ``qestyle_status.py`` would call that
    review fresh forever, which is the one wrong answer this table must never
    give. So hash what was actually read.

    ``git hash-object`` computes the object name git itself would store,
    applying the same clean filters, so on a clean checkout this is identical to
    ``ls-tree`` at the pin — verified over all 348 lectures. One subprocess per
    series, not one per file.

    Returns ``{stem: sha}``, empty if git cannot be run; the caller warns and
    writes the rows it does have rather than losing the scan.
    """
    root = os.path.join(corpus, series)
    rel = [os.path.relpath(p, root) for p in files]
    if not rel:
        return {}
    try:
        out = subprocess.run(["git", "-C", root, "hash-object", "--"] + rel,
                             capture_output=True, text=True, check=True).stdout
    except Exception as exc:
        print(f"warning: no blob SHAs for {series}: {exc}", file=sys.stderr)
        return {}
    shas = out.split()
    if len(shas) != len(rel):
        print(f"warning: no blob SHAs for {series}: git hash-object returned "
              f"{len(shas)} SHAs for {len(rel)} files", file=sys.stderr)
        return {}
    blobs = {os.path.basename(p)[:-3]: sha for p, sha in zip(files, shas)}
    warn_if_dirty(series, commit, blobs, git_blobs(corpus, series, commit))
    return blobs


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--corpus", required=True,
                    help="directory holding the five series checkouts")
    ap.add_argument("--out", default="lectures/data", help="output directory")
    ap.add_argument("--evidence", default="",
                    help="optional directory for per-lecture evidence JSON")
    ap.add_argument("--rules", default="",
                    help="action-style-guide style_checker/rules dir, for rule titles")
    ap.add_argument("--period", default="",
                    help="label for this pass, e.g. 2026-08")
    ap.add_argument("--append-history", default="", metavar="PATH",
                    help="append this pass's rule reach to a cross-period CSV")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    records, snapshot, blobs = [], {}, {}
    for series in SERIES:
        snapshot[series] = git_snapshot(args.corpus, series)
        # One file list, hashed and scanned — the SHA describes the text lexed
        # on the line below it, whatever state the checkout is in.
        files = lecture_files(args.corpus, series)
        blobs[series] = working_blobs(args.corpus, series, files,
                                      snapshot[series]["commit"])
        recs = scan_series(args.corpus, series, files)
        records.extend(recs)
        print(f"{series:32s} {len(recs):4d} lectures", file=sys.stderr)

    # --- per-lecture per-rule counts -------------------------------------
    with open(os.path.join(args.out, "violations.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["series", "lecture", "rule", "count", "proposed", "build_risk"])
        for r in records:
            for rule, v in r["violations"].items():
                w.writerow([r["series"], r["lecture"], rule, v["count"],
                            int(rule in PROPOSED), int(rule in BUILD_RISK)])

    # --- corpus-wide rule reach ------------------------------------------
    reach, total = {}, {}
    for r in records:
        for rule, v in r["violations"].items():
            reach[rule] = reach.get(rule, 0) + 1
            total[rule] = total.get(rule, 0) + v["count"]
    with open(os.path.join(args.out, "rule_reach.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["rule", "category", "lectures_affected", "total_occurrences", "proposed"])
        rule_cat = {ru: c for c, rs in CATEGORY.items() for ru in rs}
        for rule in sorted(reach, key=lambda k: -reach[k]):
            w.writerow([rule, rule_cat.get(rule, ""), reach[rule], total[rule],
                        int(rule in PROPOSED)])

    # --- per-series rule reach -------------------------------------------
    with open(os.path.join(args.out, "series_rule_reach.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["series", "rule", "lectures_affected", "total_occurrences"])
        per = {}
        for r in records:
            for rule, v in r["violations"].items():
                k = (r["series"], rule)
                a, b = per.get(k, (0, 0))
                per[k] = (a + 1, b + v["count"])
        for (s, rule) in sorted(per):
            w.writerow([s, rule, per[(s, rule)][0], per[(s, rule)][1]])

    # --- explicit plot() line widths --------------------------------------
    # ``qe-fig-008`` asks for ``lw=2`` but the check only answers the unambiguous half of
    # that — whether a width is set at all — because the rule's text does not settle
    # whether a reference line or a faint sample path may differ. The spread of values the
    # corpus actually uses is what the rule-scope question in
    # ``contributions/issues/07-fig-008-line-width-tolerance.md`` costs both readings
    # against, so it is measured here rather than typed into the prose.
    widths, width_files, kinds, kind_files = {}, {}, {}, {}
    for r in records:
        lec = (r["series"], r["lecture"])
        for val, kind in r["line_widths"]:
            key = "%g" % float(val)
            widths[key] = widths.get(key, 0) + 1
            width_files.setdefault(key, set()).add(lec)
            kinds[kind] = kinds.get(kind, 0) + 1
            kind_files.setdefault(kind, set()).add(lec)
            if kind != "house":
                kinds["other"] = kinds.get("other", 0) + 1
                kind_files.setdefault("other", set()).add(lec)
    with open(os.path.join(args.out, "fig_line_widths.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["key", "kind", "calls", "lectures"])
        for key in sorted(widths, key=lambda k: float(k)):
            w.writerow([key, "width", widths[key], len(width_files[key])])
        # ``other`` is the union over every non-house width, so its lecture count is not the
        # sum of the per-width ones — a lecture using both 1.5 and 0.8 is one lecture.
        for kind in ("house", "other", "emphasis", "de-emphasised", "plain"):
            if kind in kinds:
                w.writerow([kind, "class", kinds[kind], len(kind_files[kind])])

    # --- cross-period rule reach ------------------------------------------
    # Reach measured by the same code over a pinned snapshot is comparable
    # across passes, which score levels alone are not.
    if args.append_history and args.period:
        path = args.append_history
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        fields = ["period", "corpus_size", "rule", "lectures_affected",
                  "total_occurrences", "share_pct"]
        rows = []
        if os.path.exists(path):
            with open(path, newline="", encoding="utf-8") as fh:
                rows = [r for r in csv.DictReader(fh) if r["period"] != args.period]
        with open(path, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=fields)
            w.writeheader()
            for r in rows:
                w.writerow({k: r.get(k, "") for k in fields})
            n = len(records)
            for rule in sorted(reach, key=lambda k: -reach[k]):
                w.writerow({"period": args.period, "corpus_size": n, "rule": rule,
                            "lectures_affected": reach[rule],
                            "total_occurrences": total[rule],
                            "share_pct": round(reach[rule] / n * 100, 1)})
        print(f"appended {args.period} to {path}", file=sys.stderr)

    # --- lecture provenance ------------------------------------------------
    # One row per scanned lecture, naming the blob of the exact text this pass
    # lexed — hashed from that file, not read from the pinned commit. A
    # review overlay records the blob it judged (see
    # ``tools/qestyle_backfill_provenance.py``), so the next pass can ask which
    # lectures actually changed instead of re-reviewing all 348 — the review
    # queue then scales with corpus churn rather than corpus size.
    # A lecture whose SHA could not be read is left out rather than written with
    # an empty one: an empty blob would compare equal to an unstamped overlay and
    # read as fresh, which is the one wrong answer this file must never give.
    missing = []
    with open(os.path.join(args.out, "lecture_blobs.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["series", "lecture", "blob"])
        for r in sorted(records, key=lambda r: (r["series"], r["lecture"])):
            sha = blobs.get(r["series"], {}).get(r["lecture"], "")
            if not sha:
                missing.append(f"{r['series']}/{r['lecture']}")
                continue
            w.writerow([r["series"], r["lecture"], sha])
    if missing:
        print(f"warning: no blob SHA for {len(missing)} of {len(records)} lectures: "
              + ", ".join(missing[:6]) + (" ..." if len(missing) > 6 else ""),
              file=sys.stderr)

    # --- rule titles -------------------------------------------------------
    rules_dir = args.rules or os.path.join(
        args.corpus, "action-style-guide", "style_checker", "rules")
    if os.path.isdir(rules_dir):
        titles = load_rule_titles(rules_dir)
        with open(os.path.join(args.out, "rule_titles.csv"), "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["rule", "title", "proposed"])
            for rule in sorted(titles):
                w.writerow([rule, titles[rule], int(rule in PROPOSED)])

    meta = {
        "snapshot": snapshot,
        "n_lectures": len(records),
        "n_rules_checked": len(CHECKS),
        "per_series": {s: sum(1 for r in records if r["series"] == s) for s in SERIES},
    }
    with open(os.path.join(args.out, "snapshot.json"), "w") as fh:
        json.dump(meta, fh, indent=2, sort_keys=True)

    if args.evidence:
        for series in SERIES:
            os.makedirs(os.path.join(args.evidence, series), exist_ok=True)
        for r in records:
            p = os.path.join(args.evidence, r["series"], r["lecture"] + ".json")
            with open(p, "w") as fh:
                json.dump(r, fh, indent=1, sort_keys=True)

    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
