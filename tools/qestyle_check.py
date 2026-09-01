#!/usr/bin/env python3
"""Consistency gate for the audit — run before pushing.

Each check here corresponds to something that silently broke in a previous pass:
lectures that were never audited, a report describing a lecture that does not
exist, a header whose score does not match its own table, a reviewer quietly
editing a measured count, a proposed rule cited without its tag, a hand-written
table still quoting a reach the last rule fix moved, a period whose numbers
outlived any record of the corpus commits they were measured on.

    python3 tools/qestyle_check.py --root lectures --data lectures/data --corpus ../quantecon

Exits non-zero if any check fails — and a check whose input is missing *fails*,
it does not skip. Four checks used to note "absent, not checked" and let the run
go green; deleting ``lectures/data/`` outright produced ``All checks passed``
(issue #15). Every file under ``--data`` is committed, so its absence during a
gate run is a broken tree, not a context in which the check does not apply.

The one input that can legitimately be missing is the corpus: a past period's
clones do not exist, and CI fetches one SHA per series. That skip is an explicit
``--no-corpus``, never inferred from an empty directory, so a clone that half
failed is an error and a deliberate omission is a flag — and it is printed next
to the verdict, not scrolled past above it.
"""

from __future__ import annotations

import argparse
import csv
import datetime
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from qestyle_rules import PROPOSED                     # noqa: E402
from qestyle_scan import SERIES, checker_digest        # noqa: E402
from qestyle_score import compute, parse_report        # noqa: E402
from qestyle_report import (HISTORY_FIELDS, MECHANICAL_HISTORY,   # noqa: E402
                            MECHANICAL_SCORES, reviewed_counts, summarise)

RULE_RE = re.compile(r"\bqe-(?:writing|math|code|jax|fig|ref|link|admon)-\d{3}\b")
LEGACY_RE = re.compile(r"\bqe-(?:math|writing)-A\d\b|\[(?:W[1-8]|M(?:1[0-4]|[1-9]))\]")


class Checker:
    def __init__(self):
        self.failures = []
        self.notes = []
        self.skips = []

    def fail(self, check, detail):
        self.failures.append((check, detail))

    def note(self, msg):
        self.notes.append(msg)

    def skip(self, msg):
        """A check that did not run because a flag said not to.

        Kept apart from ``note`` so it prints beside the verdict rather than
        among the passes: "All checks passed" and "one check was switched off"
        must never be readable as the same line.
        """
        self.skips.append(msg)

    def report(self):
        by_check = {}
        for check, detail in self.failures:
            by_check.setdefault(check, []).append(detail)
        for msg in self.notes:
            print(f"  {msg}")
        if self.skips:
            print()
            for msg in self.skips:
                print(f"SKIPPED {msg}")
        if not self.failures:
            print("\nAll checks passed." if not self.skips else
                  f"\nAll checks passed ({len(self.skips)} skipped by flag).")
            return 0
        print()
        for check, details in by_check.items():
            print(f"FAIL {check} ({len(details)})")
            for d in details[:12]:
                print(f"     {d}")
            if len(details) > 12:
                print(f"     ... {len(details) - 12} more")
        return 1


def check_coverage(ck, root, corpus):
    """Every corpus lecture has a report, and every report has a lecture.

    A series whose clone is absent is a failure, not a note: with ``--corpus``
    given, the caller has said the corpus is there, so an empty directory means
    a clone that failed or a sparse pattern that matched nothing — the exact
    state in which this check used to print a note and let the gate pass.
    ``--no-corpus`` is the way to say the corpus is deliberately not present.
    """
    for series in SERIES:
        src = os.path.join(corpus, series, "lectures")
        rep = os.path.join(root, series)
        if not os.path.isdir(src):
            ck.fail("coverage",
                    f"{series}: {src} is not a directory — the corpus is absent or "
                    f"the clone is incomplete (pass --no-corpus to skip on purpose)")
            continue
        lectures = {f[:-3] for f in os.listdir(src) if f.endswith(".md")}
        reports = {os.path.basename(p)[:-3] for p in glob.glob(os.path.join(rep, "*.md"))
                   if os.path.basename(p) != "index.md"}
        for miss in sorted(lectures - reports):
            ck.fail("coverage", f"{series}/{miss}: lecture has no report")
        for extra in sorted(reports - lectures):
            ck.fail("coverage", f"{series}/{extra}: report has no lecture in the corpus")
        ck.note(f"{series}: {len(lectures)} lectures, {len(reports)} reports")


def check_scores(ck, root):
    """Header overall score and priority must follow from the score table."""
    n = 0
    for path in sorted(glob.glob(os.path.join(root, "lecture-*", "*.md"))):
        if os.path.basename(path) == "index.md":
            continue
        n += 1
        scores, declared, priority, _ = parse_report(path)
        overall, prio = compute(scores)
        if overall is None:
            ck.fail("score-arithmetic", f"{path}: no parsable category scores")
            continue
        if declared != f"{overall:.1f} / 10":
            ck.fail("score-arithmetic",
                    f"{path}: header {declared!r} vs categories {overall:.1f}")
        if priority != prio:
            ck.fail("priority-bucket", f"{path}: header {priority!r} vs rule {prio!r}")
    if n == 0:
        # Every check below walks the same glob; an empty walk would let all of
        # them pass over a tree that has no reports in it.
        ck.fail("score-arithmetic",
                f"{root}: no per-lecture reports under lecture-*/ — wrong --root, "
                f"or the reports are missing")
        return                             # "checked on 0 reports" is not a pass
    ck.note(f"score arithmetic checked on {n} reports")


def check_agreement(ck, root, data):
    """A report may not cite a count the evidence layer did not measure."""
    path = os.path.join(data, "violations.csv")
    if not os.path.exists(path):
        ck.fail("report-csv-agreement",
                f"{path}: absent, so no cited count can be held to a measurement")
        return
    measured = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            measured[(r["series"], r["lecture"], r["rule"])] = int(r["count"])
    n = 0
    for rp in sorted(glob.glob(os.path.join(root, "lecture-*", "*.md"))):
        if os.path.basename(rp) == "index.md":
            continue
        series = os.path.basename(os.path.dirname(rp))
        stem = os.path.basename(rp)[:-3]
        with open(rp, encoding="utf-8") as fh:
            text = fh.read()
        for m in re.finditer(
            r"\*\*\[(qe-[a-z]+-\d{3})(?: \(proposed\))?\]\*\* —[^\n]*?"
            r"\*Count:\* (\d+)", text
        ):
            rule, cited = m.group(1), int(m.group(2))
            want = measured.get((series, stem, rule))
            n += 1
            if want is None:
                ck.fail("report-csv-agreement",
                        f"{rp}: cites {rule} which violations.csv does not record")
            elif want != cited:
                ck.fail("report-csv-agreement",
                        f"{rp}: {rule} cited as {cited}, measured {want}")
    ck.note(f"{n} cited counts cross-checked against violations.csv")


def check_conventions(ck, root):
    """The conventions that were deliberately applied and are easy to regress."""
    n_prop = 0
    for path in sorted(glob.glob(os.path.join(root, "**", "*.md"), recursive=True)):
        # Skip build output: jupyter-book copies the sources into _build/html/_sources,
        # and the runbook has people build before re-running this gate.
        if "_build" in path.split(os.sep):
            continue
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        base = os.path.basename(path)
        for m in LEGACY_RE.finditer(text):
            ck.fail("conventions", f"{path}: legacy/placeholder rule id {m.group(0)!r}")
        if re.search(r"^# Style Audit —", text, re.M):
            ck.fail("conventions", f"{path}: '# Style Audit —' title prefix")
        if "Spec version" in text:
            ck.fail("conventions", f"{path}: 'Spec version' metadata line")
        for m in re.finditer(r"(?i)carry-forward|carries forward|carried forward", text):
            ck.fail("conventions", f"{path}: two-pass wording {m.group(0)!r}")
        if path.startswith(os.path.join(root, "lecture-")):
            if base == "index.md":
                if not re.match(r"^# Summary\s*$", text.split("\n")[0]):
                    ck.fail("conventions", f"{path}: series index H1 must be '# Summary'")
            else:
                want = f"# {base[:-3]}"
                if text.split("\n")[0].strip() != want:
                    ck.fail("conventions",
                            f"{path}: H1 must be the bare lecture stem ({want!r})")
        # Proposed rules must carry the tag wherever they are cited.
        if base == "spec.md":
            continue
        for m in RULE_RE.finditer(text):
            rule = m.group(0)
            if rule not in PROPOSED:
                continue
            tail = text[m.end():m.end() + 26]
            if "(proposed)" in tail:
                n_prop += 1
                continue
            # A section that is itself about the proposed rules does not need to
            # repeat the tag on every row.
            line_start = text.rfind("\n", 0, m.start()) + 1
            line = text[line_start:text.find("\n", m.end())]
            heads = re.findall(r"^#{1,6} .*$", text[:m.start()], re.M)
            context = (heads[-1] if heads else "") + " " + line
            if "proposed" in context.lower():
                n_prop += 1
                continue
            ck.fail("conventions", f"{path}: {rule} cited without a (proposed) tag")
    ck.note(f"{n_prop} tagged citations of proposed rules")


def check_snapshot(ck, root, data):
    """Report headers must name the snapshot the evidence came from."""
    path = os.path.join(data, "snapshot.json")
    if not os.path.exists(path):
        ck.fail("snapshot", f"{path}: absent, so no report header can be held to a pin")
        return
    with open(path, encoding="utf-8") as fh:
        snap = json.load(fh).get("snapshot", {})
    # An empty commit is what `qestyle_scan.git_snapshot` writes when a clone
    # could not be resolved. The comparison below used to skip on it — `elif
    # want and …` — so a corpus that failed to resolve passed all 348 headers.
    # Fail it once per series here, and compare unconditionally below.
    for series in SERIES:
        if not snap.get(series, {}).get("commit"):
            ck.fail("snapshot",
                    f"{path}: no commit pinned for {series} — the scan could not "
                    f"resolve its clone")
    for rp in sorted(glob.glob(os.path.join(root, "lecture-*", "*.md"))):
        if os.path.basename(rp) == "index.md":
            continue
        series = os.path.basename(os.path.dirname(rp))
        want = snap.get(series, {}).get("commit", "")[:10]
        if not want:
            continue                       # already failed once for the series
        with open(rp, encoding="utf-8") as fh:
            head = fh.read(1200)
        m = re.search(r"\*\*Corpus snapshot:\*\*\s*`([0-9a-f]+)`", head)
        if not m:
            ck.fail("snapshot", f"{rp}: no corpus-snapshot line")
        elif m.group(1) != want:
            ck.fail("snapshot", f"{rp}: snapshot {m.group(1)} != {want}")


SNAPSHOT_HISTORY_FIELDS = ["period", "series", "basis", "commit", "committed",
                           "lectures", "checker"]
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
BASES = ("pinned", "recovered")
# The digest that stamps a `snapshot_history.csv` row is `qestyle_scan`'s to compute, and
# the gate re-derives it through that same helper. Hashing the three tool files a second
# time here would give the column two definitions, and the day they drifted the gate
# would go red on rows that were in fact correct.


def _history_totals(data):
    """{period: TOTAL lecture count} from `history.csv`."""
    path = os.path.join(data, "history.csv")
    if not os.path.exists(path):
        return {}
    out = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["series"] == "TOTAL":
                out[r["period"]] = int(r["lectures"])
    return out


def check_snapshot_history(ck, data):
    """Every period's corpus pins, and the code that measured them.

    `history.csv` and `rule_reach_history.csv` carry a period's numbers, and
    `snapshot.json` carries commits — but only the current pass's, because the
    scan overwrites it. Until `snapshot_history.csv` existed no earlier period
    could be re-measured from the corpus it was actually measured on: a day-
    resolution date could not tell `99a5a21` (50 lectures) from `6a7bc1c` (52).

    Unlike the other data-dependent checks here, a missing file is a failure and
    not a note. A record that can go quietly missing is the exact thing this file
    exists to stop.
    """
    path = os.path.join(data, "snapshot_history.csv")
    if not os.path.exists(path):
        ck.fail("snapshot-history",
                f"{path}: absent, so no period's corpus pins are recorded")
        return
    with open(path, newline="", encoding="utf-8") as fh:
        header = fh.readline().rstrip("\r\n")
        fh.seek(0)
        rows = list(csv.DictReader(fh))
    want_header = ",".join(SNAPSHOT_HISTORY_FIELDS)
    if header != want_header:
        ck.fail("snapshot-history",
                f"{path}: header is {header!r}, must be {want_header!r}")
        return
    if not rows:
        # Nothing below can run on an empty file — `max(periods)` would raise and
        # crash the gate instead of reporting the failure it just recorded.
        ck.fail("snapshot-history", f"{path}: header only, no pins recorded")
        return
    # Rows are written sorted, so an unsorted file was hand-edited or hand-merged.
    keys = [(r.get("period", ""), r.get("series", "")) for r in rows]
    if keys != sorted(keys):
        ck.fail("snapshot-history",
                f"{path}: rows are not sorted by (period, series)")
    # csv.DictReader parks surplus fields under the None key, so a row wider than
    # the header would otherwise pass as long as its first seven values are valid.
    for i, r in enumerate(rows, start=2):
        if None in r:
            ck.fail("snapshot-history",
                    f"{path}:{i}: {len(r[None])} field(s) beyond the header")

    digest = checker_digest()
    if not digest:
        ck.fail("snapshot-history",
                "qestyle_scan.checker_digest() is empty, so the checker column "
                "cannot be held to the tools in this tree")

    by_period = {}
    for i, r in enumerate(rows, start=2):
        where = f"{path}:{i} {r['period'] or '?'}/{r['series'] or '?'}"
        by_period.setdefault(r["period"], []).append(r)
        if r["basis"] not in BASES:
            ck.fail("snapshot-history",
                    f"{where}: basis {r['basis']!r}, must be "
                    f"{' or '.join(repr(b) for b in BASES)}")
        if not COMMIT_RE.match(r["commit"] or ""):
            ck.fail("snapshot-history",
                    f"{where}: commit {r['commit']!r} is not a 40-hex commit")
        try:
            when = datetime.datetime.fromisoformat(r["committed"])
        except (TypeError, ValueError):
            ck.fail("snapshot-history",
                    f"{where}: committed {r['committed']!r} is not ISO-8601")
        else:
            if when.tzinfo is None:
                ck.fail("snapshot-history",
                        f"{where}: committed {r['committed']!r} carries no UTC "
                        "offset")
        if not (r["lectures"] or "").isdigit() or int(r["lectures"] or 0) < 1:
            ck.fail("snapshot-history",
                    f"{where}: lectures {r['lectures']!r} is not a positive integer")
        if digest and r["checker"] != digest:
            ck.fail("snapshot-history",
                    f"{where}: checker {r['checker']!r}, but the tools in this "
                    f"tree hash to {digest}")

    # One row per series per period, and the period's rows must add up to the
    # corpus size `history.csv` reports for it.
    totals = _history_totals(data)
    for period in sorted(by_period):
        seen = [r["series"] for r in by_period[period]]
        for miss in sorted(set(SERIES) - set(seen)):
            ck.fail("snapshot-history", f"{period}: no pin for {miss}")
        for extra in sorted(set(seen) - set(SERIES)):
            ck.fail("snapshot-history",
                    f"{period}: {extra!r} is not one of the five pipeline series")
        for dup in sorted({s for s in seen if seen.count(s) > 1}):
            ck.fail("snapshot-history", f"{period}: {dup} pinned {seen.count(dup)} times")
        if period in totals:
            got = sum(int(r["lectures"]) for r in by_period[period]
                      if (r["lectures"] or "").isdigit())
            if got != totals[period]:
                ck.fail("snapshot-history",
                        f"{period}: pinned lectures sum to {got}, history.csv "
                        f"TOTAL is {totals[period]}")

    # A period with numbers but no pins is the state being eliminated, so the
    # period sets have to match in both directions and in both histories.
    periods = set(by_period)
    if not totals:
        ck.fail("snapshot-history",
                f"{os.path.join(data, 'history.csv')}: absent, so the pinned "
                "periods cannot be held to the measured ones")
    reach = set(_reach_history(data))
    if not reach:
        ck.fail("snapshot-history",
                f"{os.path.join(data, 'rule_reach_history.csv')}: absent, so the "
                "pinned periods cannot be held to the measured ones")
    for label, other in (("history.csv", set(totals)),
                         ("rule_reach_history.csv", reach)):
        if not other:
            continue
        for p in sorted(other - periods):
            ck.fail("snapshot-history",
                    f"{p}: {label} carries this period's numbers, but nothing "
                    "pins the corpus they came from")
        for p in sorted(periods - other):
            ck.fail("snapshot-history",
                    f"{p}: pinned here, but {label} has no numbers for it")

    # The newest period is the one `snapshot.json` still describes; they are two
    # records of the same measurement and may not disagree.
    snap_path = os.path.join(data, "snapshot.json")
    newest = max(periods)
    if not os.path.exists(snap_path):
        ck.fail("snapshot-history",
                f"{snap_path}: absent, so the {newest} pins have nothing to agree with")
    else:
        with open(snap_path, encoding="utf-8") as fh:
            meta = json.load(fh)
        snap, per_series = meta.get("snapshot", {}), meta.get("per_series", {})
        for r in sorted(by_period[newest], key=lambda r: r["series"]):
            series = r["series"]
            want = snap.get(series, {}).get("commit", "")
            if want != r["commit"]:
                ck.fail("snapshot-history",
                        f"{newest}/{series}: pinned {r['commit'] or '(none)'}, "
                        f"snapshot.json has {want or '(none)'}")
            n = per_series.get(series)
            if n is not None and str(n) != r["lectures"]:
                ck.fail("snapshot-history",
                        f"{newest}/{series}: pinned at {r['lectures']} lectures, "
                        f"snapshot.json has {n}")

    ck.note(f"{len(rows)} corpus pins checked across "
            f"{len(periods)} period{'' if len(periods) == 1 else 's'} "
            f"({', '.join(sorted(periods))}), checker digest "
            f"{digest or 'unavailable'}")


SCORE_COLS = HISTORY_FIELDS[2:]            # lectures, the categories, overall, priorities


def check_reach_history(ck, data):
    """The newest period's reach rows are what the current-period files say now.

    `rule_reach_history.csv` is written by `qestyle_scan.py --append-history`, an
    optional flag, and the file is committed — so a scan run without it leaves the
    previous run's rows *present* under the current period's label, not absent.
    `rule_reach.csv` moves and the history does not, and every check that reads
    the history (the trend chart, the narrative claims) is happy with the stale
    row (issue #21). Both files are written from the same counts, so the newest
    period's rows must equal `rule_reach.csv` per rule, and its `corpus_size`
    must be the lecture count `snapshot.json` recorded.
    """
    hist_path = os.path.join(data, "rule_reach_history.csv")
    cur_path = os.path.join(data, "rule_reach.csv")
    snap_path = os.path.join(data, "snapshot.json")
    per = _reach_history(data)
    if not per:
        ck.fail("reach-history", f"{hist_path}: absent or empty")
        return
    missing = [p for p in (cur_path, snap_path) if not os.path.exists(p)]
    if missing:
        for p in missing:
            ck.fail("reach-history", f"{p}: absent, so the newest reach rows cannot be "
                                     f"held to it")
        return
    newest = max(per)
    hist = per[newest]
    with open(cur_path, newline="", encoding="utf-8") as fh:
        cur = {r["rule"]: (int(r["lectures_affected"]), int(r["total_occurrences"]))
               for r in csv.DictReader(fh)}
    with open(snap_path, encoding="utf-8") as fh:
        n = json.load(fh).get("n_lectures")
    for rule in sorted(set(cur) - set(hist)):
        ck.fail("reach-history", f"{newest}: {rule} is in rule_reach.csv but has no "
                                 f"history row — --append-history was not run")
    for rule in sorted(set(hist) - set(cur)):
        ck.fail("reach-history", f"{newest}: {rule} has a history row but is not in "
                                 f"rule_reach.csv — the history is from another run")
    sizes = {v[3] for v in hist.values()}
    if n is None or sizes != {int(n)}:
        ck.fail("reach-history", f"{newest}: corpus_size {sorted(sizes)} in the history, "
                                 f"snapshot.json has n_lectures {n}")
    for rule in sorted(set(cur) & set(hist)):
        reach, occ, share, size = hist[rule]
        if (reach, occ) != cur[rule]:
            ck.fail("reach-history",
                    f"{newest}: {rule} history says {reach}/{occ}, rule_reach.csv says "
                    f"{cur[rule][0]}/{cur[rule][1]} — re-run the scan with "
                    f"--append-history")
        elif size and round(reach / size * 100, 1) != share:
            ck.fail("reach-history",
                    f"{newest}: {rule} share_pct {share} is not round(100 × {reach} / "
                    f"{size}, 1) = {round(reach / size * 100, 1)}")
    ck.note(f"{len(hist)} reach rows for {newest} held to rule_reach.csv and snapshot.json")


def check_score_history(ck, data, reviews):
    """A score row records its judgment coverage, and has a like-for-like twin.

    A lecture assessed against more rules scores lower. The 2026-08 corpus mean sat
    above 2026-05's until the review overlays landed and below it afterwards, with
    the lectures unchanged — so a score row is not comparable with another unless
    both say how much of the judgment layer they fold in (issue #16). Two records
    make that checkable: `history.csv` carries `reviewed` per row, and
    `history_mechanical.csv` carries the same row from the evidence layer alone,
    which is comparable across periods whatever the coverage was.

    The latest period is also held to the current-period files it was summarised
    from, so a `--history` step that was skipped, or run before `qestyle_score`,
    leaves a stale row the gate can see (the score half of issue #21).
    """
    hist = os.path.join(data, "history.csv")
    mech = os.path.join(data, MECHANICAL_HISTORY)
    for path, want in ((hist, HISTORY_FIELDS + ["reviewed"]), (mech, HISTORY_FIELDS)):
        if not os.path.exists(path):
            ck.fail("score-history", f"{path}: absent")
            continue
        with open(path, newline="", encoding="utf-8") as fh:
            header = next(csv.reader(fh), [])
        if header != want:
            ck.fail("score-history",
                    f"{path}: header is {','.join(header)!r}, must be {','.join(want)!r}")
    if any(c == "score-history" for c, _ in ck.failures):
        return

    def load(path):
        with open(path, newline="", encoding="utf-8") as fh:
            return {(r["period"], r["series"]): r for r in csv.DictReader(fh)}

    H, M = load(hist), load(mech)
    if set(H) != set(M):
        for k in sorted(set(H) - set(M)):
            ck.fail("score-history", f"{'/'.join(k)}: in history.csv, no like-for-like "
                                     f"row in {MECHANICAL_HISTORY}")
        for k in sorted(set(M) - set(H)):
            ck.fail("score-history", f"{'/'.join(k)}: in {MECHANICAL_HISTORY}, no row in "
                                     f"history.csv")

    by_period = {}
    for (period, series), r in H.items():
        by_period.setdefault(period, {})[series] = r
        n = r.get("lectures") or ""
        k = r.get("reviewed") or ""
        if not (k.isdigit() and n.isdigit() and 0 <= int(k) <= int(n)):
            ck.fail("score-history",
                    f"{period}/{series}: reviewed {k!r} is not an integer in "
                    f"[0, {n or '?'}]")
            continue
        # A row with no judgment layer *is* an evidence-layer row: the two files
        # must agree on it exactly, or one of them was written from other scores.
        m = M.get((period, series))
        if int(k) == 0 and m is not None:
            diff = [c for c in SCORE_COLS if r.get(c, "") != m.get(c, "")]
            if diff:
                ck.fail("score-history",
                        f"{period}/{series}: reviewed=0 but differs from "
                        f"{MECHANICAL_HISTORY} on {', '.join(diff)}")
    for period, rows in sorted(by_period.items()):
        tot = rows.get("TOTAL")
        if tot is None:
            ck.fail("score-history", f"{period}: no TOTAL row in history.csv")
            continue
        for col in ("lectures", "reviewed"):
            parts = [int(r[col]) for s, r in rows.items()
                     if s != "TOTAL" and (r.get(col) or "").isdigit()]
            if (tot.get(col) or "").isdigit() and sum(parts) != int(tot[col]):
                ck.fail("score-history",
                        f"{period}: TOTAL {col} is {tot[col]}, the series sum to "
                        f"{sum(parts)}")

    # The newest period must be what the current-period files summarise to now.
    newest = max(by_period) if by_period else None
    if newest:
        for label, name, table, needs_reviewed in (
                ("history.csv", "scores.csv", H, True),
                (MECHANICAL_HISTORY, MECHANICAL_SCORES, M, False)):
            src = os.path.join(data, name)
            if not os.path.exists(src):
                ck.fail("score-history", f"{src}: absent, so the {newest} rows of {label} "
                                         f"cannot be held to it")
                continue
            # Only now: reviewed_counts() reads scores.csv, so computing it before
            # the guard above would crash the gate on the very file it reports on.
            extra = reviewed_counts(data, reviews) if needs_reviewed else None
            for rec in summarise(data, name):
                row = table.get((newest, rec["series"]))
                if row is None:
                    ck.fail("score-history", f"{newest}/{rec['series']}: summarised from "
                                             f"{name}, but {label} has no row for it")
                    continue
                diff = [c for c in SCORE_COLS if str(rec.get(c, "")) != row.get(c, "")]
                if diff:
                    ck.fail("score-history",
                            f"{newest}/{rec['series']}: {label} differs from {name} as "
                            f"summarised now on {', '.join(diff)} — re-run "
                            f"qestyle_score then qestyle_report --history {newest}")
                if extra is not None and str(extra.get(rec["series"], 0)) != row.get("reviewed", ""):
                    ck.fail("score-history",
                            f"{newest}/{rec['series']}: reviewed is {row.get('reviewed')!r}, "
                            f"but {extra.get(rec['series'], 0)} overlays are folded into "
                            f"scores.csv now")
    cov = ", ".join(f"{p} {rows['TOTAL'].get('reviewed', '?')}/{rows['TOTAL'].get('lectures', '?')}"
                    for p, rows in sorted(by_period.items()) if "TOTAL" in rows)
    ck.note(f"{len(H)} score rows checked against their like-for-like twins; judgment "
            f"coverage {cov}")


# The generated regions of a narrative document are `qestyle_report --splice`'s
# business; these regexes strip them so only hand-written prose is examined.
SPLICE_RE = re.compile(r"<!-- qe:[A-Za-z0-9_-]+ -->.*?<!-- /qe:[A-Za-z0-9_-]+ -->", re.S)
FENCE_RE = re.compile(r"^(```|~~~).*?^\1", re.S | re.M)
# Spelled-out counts appear in the narrative ("eleven distinct values"); the gate has to
# read them to hold them to the CSV.
NUMBER_WORDS = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen "
    "fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}


def _as_int(word):
    """A count written as a digit, a number word, or a hyphenated one ("twenty-one")."""
    if word.isdigit():
        return int(word)
    if word in NUMBER_WORDS:
        return NUMBER_WORDS[word]
    tens, _, units = word.partition("-")
    if tens in NUMBER_WORDS and units in NUMBER_WORDS:
        return NUMBER_WORDS[tens] + NUMBER_WORDS[units]
    return None
INT_RE = re.compile(r"\d[\d,]*(?:\.\d+)?")


def _reach_history(data):
    """{period: {rule: (reach, occurrences, share_pct, corpus_size)}}."""
    path = os.path.join(data, "rule_reach_history.csv")
    if not os.path.exists(path):
        return {}
    per = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            per.setdefault(r["period"], {})[r["rule"]] = (
                int(r["lectures_affected"]), int(r["total_occurrences"]),
                float(r["share_pct"]), int(r["corpus_size"]))
    return per


def _table_rows(text):
    """Markdown table rows as (header_cells, row_cells)."""
    header, out = None, []
    for line in text.split("\n"):
        s = line.strip()
        if not s.startswith("|"):
            header = None
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        if header is None:
            header = cells
            continue
        out.append((header, cells))
    return out


def check_narrative(ck, root, data):
    """A hand-written table may not quote a corpus number that has since moved.

    The gate already holds the per-lecture reports to `violations.csv`, but the
    narrative documents mirror the same numbers in prose that nothing regenerates
    — and a rule fix moves reach without touching the sentence quoting it. This
    caught `qe-code-002` still being described at its pre-fix reach.
    """
    per = _reach_history(data)
    if not per:
        ck.fail("narrative-claims",
                f"{os.path.join(data, 'rule_reach_history.csv')}: absent or empty, so "
                f"no hand-written figure can be held to a measurement")
        return
    periods = sorted(per)
    now, before = per[periods[-1]], per.get(periods[-2], {}) if len(periods) > 1 else {}

    docs = [p for p in sorted(glob.glob(os.path.join(root, "*.md"))) if os.path.exists(p)]
    docs += sorted(glob.glob(os.path.join(root, "lecture-*", "index.md")))
    if os.path.exists("README.md"):
        docs.append("README.md")

    n = 0
    for path in docs:
        with open(path, encoding="utf-8") as fh:
            text = FENCE_RE.sub("", SPLICE_RE.sub("", fh.read()))
        for header, cells in _table_rows(text):
            row = " ".join(cells)
            ids = set(RULE_RE.findall(row))
            if len(ids) != 1:
                continue
            rule = ids.copy().pop()

            # A trend row: "A% -> B%" spans the previous pass and this one.
            trend = re.search(r"(\d+)\s*%\s*(?:\u2192|->)\s*(\d+)\s*%", row)
            if trend:
                n += 1
                for label, cited, table in (("previous", int(trend.group(1)), before),
                                            ("current", int(trend.group(2)), now)):
                    want = table.get(rule)
                    if want is None:
                        ck.fail("narrative-claims",
                                f"{path}: {rule} cites a {label} share, but that "
                                f"period has no measurement for it")
                    elif abs(round(want[2]) - cited) > 1:
                        ck.fail("narrative-claims",
                                f"{path}: {rule} {label} share cited as {cited}%, "
                                f"measured {want[2]}%")
                continue

            # A counts table, declared as such by its own header.
            head = " ".join(header).lower()
            if "lecture" not in head or "occurrence" not in head:
                continue
            want = now.get(rule)
            if want is None:
                continue
            reach, occ, share, corpus = want
            allowed = {reach, occ, corpus, round(share)}
            body = re.sub(r"\u00a7\s*\d+(\.\d+)*|#\d+", "", RULE_RE.sub("", row))
            n += 1
            for m in INT_RE.finditer(body):
                if "." in m.group(0):
                    continue
                cited = int(m.group(0).replace(",", ""))
                if cited not in allowed:
                    ck.fail("narrative-claims",
                            f"{path}: {rule} row cites {cited}, which is none of its "
                            f"measured reach ({reach}), occurrences ({occ}) or "
                            f"corpus size ({corpus})")
    # The trend *sentence*, not a table: "Of the 35 rules measurable in both
    # snapshots, 28 improved as a share of the corpus, 4 held level and 3 got
    # worse." Two rule fixes this pass moved those counts and the sentence did not
    # follow, both times — so it is checked too.
    if len(periods) > 1:
        shared = sorted(set(before) & set(now))
        want = {
            "measurable in both snapshots": len(shared),
            "improved": sum(1 for r in shared if now[r][2] < before[r][2]),
            "held level": sum(1 for r in shared if now[r][2] == before[r][2]),
            "got worse": sum(1 for r in shared if now[r][2] > before[r][2]),
        }
        pats = {
            "measurable in both snapshots": r"(\d+)\s+rules?\s+measurable in both snapshots",
            "improved": r"(\d+)\s+improved",
            "held level": r"(\d+)\s+held level",
            "got worse": r"(\d+)\s+got worse",
        }
        for path in docs:
            with open(path, encoding="utf-8") as fh:
                text = FENCE_RE.sub("", SPLICE_RE.sub("", fh.read()))
            flat = " ".join(text.split())
            for label, pat in pats.items():
                for m in re.finditer(pat, flat):
                    n += 1
                    if int(m.group(1)) != want[label]:
                        ck.fail("narrative-claims",
                                f"{path}: says {m.group(1)} {label}, "
                                f"the history gives {want[label]}")

    ck.note(f"{n} hand-written corpus claims cross-checked against "
            f"rule_reach_history.csv")


def check_line_width_claims(ck, root, data):
    """The appendix's line-width figures must come from `fig_line_widths.csv`.

    `qe-fig-008` asks for ``lw=2`` but the check only answers the unambiguous half of that,
    so the spread of widths the corpus uses is the evidence behind a rule-scope question the
    report cites. Those numbers move whenever the check's exemptions move — the keyword-bundle
    and ``ls='none'`` exemptions each shifted them once — and nothing regenerates the
    sentence quoting them.
    """
    path = os.path.join(data, "fig_line_widths.csv")
    if not os.path.exists(path):
        ck.fail("line-width-claims",
                f"{path}: absent, so no line-width figure can be held to a measurement")
        return
    widths, classes = {}, {}
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            (widths if r["kind"] == "width" else classes)[r["key"]] = (
                int(r["calls"]), int(r["lectures"]))

    # The published appendix carries the summary; the contribution draft carries the full
    # tables and is the one whose numbers a checker change moves first.
    docs = [os.path.join(root, "appendix.md"),
            os.path.join("contributions", "issues",
                         "07-fig-008-line-width-tolerance.md")]
    n = 0
    for doc in docs:
        if os.path.exists(doc):
            with open(doc, encoding="utf-8") as fh:
                n += _line_width_claims(
                    ck, doc, FENCE_RE.sub("", SPLICE_RE.sub("", fh.read())),
                    widths, classes)
    ck.note(f"{n} line-width claims cross-checked against fig_line_widths.csv")


def _line_width_claims(ck, doc, text, widths, classes):
    """Hold one document's line-width figures to the CSV. Returns the number checked."""
    n = 0
    # ``| `lw=2` | 977 |`` and ``| some other value | 264 |``
    for label, key in (("lw=2", "house"), ("some other value", "other")):
        m = re.search(r"\|\s*`?" + re.escape(label) + r"`?\s*\|\s*([\d,]+)\s*\|", text)
        if m and key in classes:
            n += 1
            cited = int(m.group(1).replace(",", ""))
            if cited != classes[key][0]:
                ck.fail("line-width-claims",
                        f"{doc}: {label} cited as {cited} calls, "
                        f"measured {classes[key][0]}")

    # ``264 `plot()` calls across 84 lectures set some other width, spread over twenty
    # distinct values`` — the appendix's one-sentence form.
    m = re.search(r"(\d+) `plot\(\)` calls across (\d+) lectures", text)
    if m and "other" in classes:
        n += 2
        if int(m.group(1)) != classes["other"][0]:
            ck.fail("line-width-claims",
                    f"{doc}: says {m.group(1)} calls set another width, "
                    f"measured {classes['other'][0]}")
        if int(m.group(2)) != classes["other"][1]:
            ck.fail("line-width-claims",
                    f"{doc}: says {m.group(2)} lectures, "
                    f"measured {classes['other'][1]}")
    m = re.search(r"spread over ([\w-]+)\s*\n?\s*distinct values", text)
    if m:
        n += 1
        n_vals = len([k for k in widths if float(k) != 2])
        if _as_int(m.group(1)) != n_vals:
            ck.fail("line-width-claims",
                    f"{doc}: says {m.group(1)!r} distinct values, measured {n_vals}")

    # ``spread across **84 lectures** and twenty distinct values`` — the draft's form.
    m = re.search(r"spread across \*\*(\d+) lectures\*\* and (\w+) distinct values", text)
    if m and "other" in classes:
        n += 2
        if int(m.group(1)) != classes["other"][1]:
            ck.fail("line-width-claims",
                    f"{doc}: says {m.group(1)} lectures use another width, "
                    f"measured {classes['other'][1]}")
        n_vals = len([k for k in widths if float(k) != 2])
        if _as_int(m.group(2)) != n_vals:
            ck.fail("line-width-claims",
                    f"{doc}: says {m.group(2)!r} distinct values, measured {n_vals}")

    # ``— `lw=1` x60, `1.5` x48, …``
    for val, cited in re.findall(r"`(?:lw=)?([0-9.]+)`\s*(?:\u00d7|x)\s*(\d+)", text):
        key = "%g" % float(val)
        if key in widths:
            n += 1
            if int(cited) != widths[key][0]:
                ck.fail("line-width-claims",
                        f"{doc}: lw={key} cited {cited} times, "
                        f"measured {widths[key][0]}")

    # The deliberate/drift split.
    for label, key in (("de-emphasis signal", "de-emphasised"),
                       ("above 2 (emphasis)", "emphasis"),
                       ("no such signal", "plain")):
        m = re.search(r"\|[^|\n]*" + re.escape(label) + r"[^|\n]*\|\s*(\d+)\s*\|", text)
        if m and key in classes:
            n += 1
            if int(m.group(1)) != classes[key][0]:
                ck.fail("line-width-claims",
                        f"{doc}: {key} cited as {m.group(1)}, "
                        f"measured {classes[key][0]}")

    # ``the report gains 264 occurrences across 84 lectures``
    m = re.search(r"gains \*{0,2}(\d+)\*{0,2} occurrences\s*\n?\s*across (\d+) lectures", text)
    if m and "other" in classes:
        n += 2
        if int(m.group(1)) != classes["other"][0]:
            ck.fail("line-width-claims",
                    f"{doc}: reading-1 cost cited as {m.group(1)} occurrences, "
                    f"measured {classes['other'][0]}")
        if int(m.group(2)) != classes["other"][1]:
            ck.fail("line-width-claims",
                    f"{doc}: reading-1 cost cited as {m.group(2)} lectures, "
                    f"measured {classes['other'][1]}")

    # ``roughly **152** of those are deliberate and the remaining **112** are the finding``
    m = re.search(r"roughly \*\*(\d+)\*\* of those are deliberate and the remaining "
                  r"\*\*(\d+)\*\*", text)
    if m and {"emphasis", "de-emphasised", "plain"} <= set(classes):
        n += 2
        want = classes["emphasis"][0] + classes["de-emphasised"][0]
        if int(m.group(1)) != want:
            ck.fail("line-width-claims",
                    f"{doc}: says {m.group(1)} deliberate, measured {want}")
        if int(m.group(2)) != classes["plain"][0]:
            ck.fail("line-width-claims",
                    f"{doc}: says {m.group(2)} the finding, "
                    f"measured {classes['plain'][0]}")

    return n


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default="lectures")
    ap.add_argument("--data", default="lectures/data")
    ap.add_argument("--reviews", default="reviews",
                    help="directory of judgment overlays, for the `reviewed` column")
    # One or the other, never neither: an omitted --corpus used to skip the
    # coverage check silently, which is the fail-open shape this gate exists to
    # refuse. Saying "no corpus" has to be a decision someone typed.
    where = ap.add_mutually_exclusive_group(required=True)
    where.add_argument("--corpus", metavar="DIR",
                       help="directory holding one clone per series; a series "
                            "missing under it is a failure")
    where.add_argument("--no-corpus", action="store_true",
                       help="skip the corpus coverage check on purpose (the corpus "
                            "genuinely is not present, e.g. a past period)")
    args = ap.parse_args()

    ck = Checker()
    if args.no_corpus:
        ck.skip("coverage: --no-corpus, so lecture/report coverage was not checked "
                "against the corpus")
    else:
        check_coverage(ck, args.root, args.corpus)
    check_scores(ck, args.root)
    check_agreement(ck, args.root, args.data)
    check_conventions(ck, args.root)
    check_snapshot(ck, args.root, args.data)
    check_snapshot_history(ck, args.data)
    check_score_history(ck, args.data, args.reviews)
    check_reach_history(ck, args.data)
    check_narrative(ck, args.root, args.data)
    check_line_width_claims(ck, args.root, args.data)
    return ck.report()


if __name__ == "__main__":
    sys.exit(main())
