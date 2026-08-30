#!/usr/bin/env python3
"""Build the aggregate audit documents from the per-lecture data.

`UPDATE.md` Step 5 used to say "update the cross-repo documents **by hand** from
the series averages" — which is how the scoreboard, the triage page and the
README drifted apart from the per-lecture reports. This tool derives every
aggregate number from ``lectures/data/*.csv`` and splices the generated tables
into the marked regions of the prose documents, so the numbers cannot disagree.

    python3 tools/qestyle_report.py --summarise      # write series_summary.csv
    python3 tools/qestyle_report.py --history 2026-08 --summarise
    python3 tools/qestyle_report.py --splice         # rewrite marked table blocks

Marked regions look like::

    <!-- qe:scoreboard -->
    ...generated...
    <!-- /qe:scoreboard -->
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import textwrap

from qestyle_draft import escape_roles                        # noqa: E402

CATS = ["writing", "math", "code", "figures", "references", "links", "admonitions"]
CAT_LABEL = {"writing": "Writing", "math": "Math", "code": "Code",
             "figures": "Figures", "references": "References", "links": "Links",
             "admonitions": "Admon"}
SERIES_ORDER = ["lecture-python-intro", "lecture-python-programming",
                "lecture-python.myst", "lecture-python-advanced.myst", "lecture-dp"]
SHORT = {"lecture-python-intro": "intro", "lecture-python-programming": "programming",
         "lecture-python.myst": "python.myst",
         "lecture-python-advanced.myst": "advanced", "lecture-dp": "dp"}
PRIOS = ["HIGH", "MEDIUM", "LOW", "NONE"]

# Editorial framing for the "biggest wins" table: what the fix means in plain
# words, and whether it is a scriptable sweep or needs a human pass.
WIN_COPY = {
    "qe-fig-005": ("Name your figures",
                   "Add a `name:` so figures can be cross-referenced with `numref`", "🔧"),
    "qe-code-002": ("Greek letters in code",
                    "Use `α`, `β`, `γ` instead of `alpha`, `beta`, `gamma`", "🔧"),
    "qe-fig-001": ("Figure sizes",
                   "Drop `figsize=` overrides — let the site defaults apply", "🔧"),
    "qe-writing-006": ("Heading capitalization",
                       "Section headings → sentence case (first word + proper nouns only)", "🔧"),
    "qe-fig-003": ("Plot titles → captions",
                   "Move `ax.set_title(...)` out of the plot into the figure caption", "✋"),
    "qe-fig-008": ("Line widths",
                   "Pass `lw=2` on line plots for consistent weight", "🔧"),
    "qe-writing-008": ("Collapse double spaces",
                       "Reduce runs of spaces between words to one", "🔧"),
    "qe-math-002": ("Transpose notation",
                    "Replace `'` and `^T` with `^\\top`", "🔧"),
    "qe-math-010": ("Expectation notation",
                    "Use `\\mathbb{E}` / `\\mathbb{P}` / `\\mathbb{V}` with braces", "🔧"),
    "qe-link-002": ("Cross-series links",
                    "Replace raw `quantecon.org` URLs with `{doc}` references", "🔧"),
    "qe-ref-001": ("Narrative citations",
                   "Use `{cite:t}` where the author name is part of the sentence", "✋"),
    "qe-fig-006": ("Axis labels",
                   "Lowercase axis labels (`'Time'` → `'time'`)", "🔧"),
    "qe-math-003": ("Matrix brackets",
                    "Use `bmatrix` rather than `pmatrix` or `array`", "🔧"),
    "qe-math-004": ("Un-bold vectors",
                    "Drop `\\mathbf` / `\\boldsymbol` from matrices and vectors", "🔧"),
    "qe-fig-004": ("Caption style",
                   "Sentence case, six words or fewer", "✋"),
    "qe-fig-002": ("Static images",
                   "Regenerate bundled PNGs from code", "✋"),
    "qe-math-011": ("Distribution names",
                    "Plain `N` rather than `\\mathcal{N}`", "🔧"),
    "qe-writing-009": ("IID",
                       'Write "IID", not "i.i.d." or "iid"', "🔧"),
    "qe-fig-007": ("Figure spines",
                   "Keep the box — stop hiding spines", "🔧"),
    "qe-code-003": ("Install cells",
                    "Move `!pip install` to the top with `hide-output`", "🔧"),
    "qe-code-004": ("Timing",
                    "Replace `time.time()` with `qe.Timer`", "🔧"),
}


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def summarise(data_dir):
    """Per-series category means, overall means and priority counts."""
    scores = read_csv(os.path.join(data_dir, "scores.csv"))
    out = []
    for series in SERIES_ORDER:
        rows = [r for r in scores if r["series"] == series]
        if not rows:
            continue
        rec = {"series": series, "lectures": len(rows)}
        for c in CATS:
            vals = [num(r[c]) for r in rows if num(r[c]) is not None]
            rec[c] = round(sum(vals) / len(vals), 1) if vals else ""
        ov = [num(r["overall"]) for r in rows if num(r["overall"]) is not None]
        rec["overall"] = round(sum(ov) / len(ov), 1) if ov else ""
        for p in PRIOS:
            rec[p] = sum(1 for r in rows if r["priority"] == p)
        out.append(rec)
    # corpus row
    tot = {"series": "TOTAL", "lectures": len(scores)}
    for c in CATS:
        vals = [num(r[c]) for r in scores if num(r[c]) is not None]
        tot[c] = round(sum(vals) / len(vals), 1) if vals else ""
    ov = [num(r["overall"]) for r in scores if num(r["overall"]) is not None]
    tot["overall"] = round(sum(ov) / len(ov), 1) if ov else ""
    for p in PRIOS:
        tot[p] = sum(1 for r in scores if r["priority"] == p)
    out.append(tot)
    return out


def write_summary(data_dir, rows):
    path = os.path.join(data_dir, "series_summary.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["series", "lectures"] + CATS
                           + ["overall"] + PRIOS)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return path


def append_history(data_dir, period, rows):
    """Append this pass to the cross-period time series (kept, never rewritten)."""
    path = os.path.join(data_dir, "history.csv")
    fields = ["period", "series", "lectures"] + CATS + ["overall"] + PRIOS
    existing = read_csv(path) if os.path.exists(path) else []
    existing = [r for r in existing if r.get("period") != period]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for r in existing:
            w.writerow({k: r.get(k, "") for k in fields})
        for r in rows:
            w.writerow({**{k: "" for k in fields}, "period": period,
                        **{k: v for k, v in r.items() if k in fields}})
    return path


# ---------------------------------------------------------------------------
# Generated table blocks
# ---------------------------------------------------------------------------

def link(series):
    return f"[{series}]({series}/index.md)"


def block_scoreboard(rows, *, readme=False):
    """README landing scoreboard: one line per series, worst first."""
    body = [r for r in rows if r["series"] != "TOTAL"]
    total = next(r for r in rows if r["series"] == "TOTAL")
    body.sort(key=lambda r: r["overall"])
    lines = ["| Series | Lectures | Overall | HIGH | weakest category |",
             "|--------|---------:|--------:|-----:|------------------|"]
    for r in body:
        weak = min((c for c in CATS if r[c] != ""), key=lambda c: r[c])
        name = r["series"] if readme else link(r["series"])
        lines.append(f"| {name} | {r['lectures']} | {r['overall']} | {r['HIGH']} | "
                     f"{CAT_LABEL[weak]} ({r[weak]}) |")
    weak = min((c for c in CATS if total[c] != ""), key=lambda c: total[c])
    lines.append(f"| **Corpus** | **{total['lectures']}** | **{total['overall']}** | "
                 f"**{total['HIGH']}** | {CAT_LABEL[weak]} ({total[weak]}) |")
    return "\n".join(lines)


def block_full_scoreboard(rows):
    """details.md: every category, every series, plus priority counts."""
    body = [r for r in rows if r["series"] != "TOTAL"]
    total = next(r for r in rows if r["series"] == "TOTAL")
    body.sort(key=lambda r: r["overall"])
    head = ("| # | Series | Lectures | " + " | ".join(CAT_LABEL[c] for c in CATS)
            + " | **Overall** | HIGH | MEDIUM | LOW | NONE |")
    rule = "|---|--------|----------|" + "|".join(["---"] * len(CATS)) + \
           "|-------------|------|--------|-----|------|"
    lines = [head, rule]
    for i, r in enumerate(body, 1):
        weak = min((c for c in CATS if r[c] != ""), key=lambda c: r[c])
        cells = []
        for c in CATS:
            v = r[c]
            if v == "":
                cells.append("N/A")
            elif c == weak:
                cells.append(f"**{v}**")
            else:
                cells.append(str(v))
        lines.append(f"| {i} | {link(r['series'])} | {r['lectures']} | "
                     + " | ".join(cells)
                     + f" | **{r['overall']}** | {r['HIGH']} | {r['MEDIUM']} | "
                     f"{r['LOW']} | {r['NONE']} |")
    cells = [f"**{total[c]}**" if total[c] != "" else "N/A" for c in CATS]
    lines.append(f"|   | **TOTAL / corpus average** | **{total['lectures']}** | "
                 + " | ".join(cells)
                 + f" | **{total['overall']}** | **{total['HIGH']}** | "
                 f"**{total['MEDIUM']}** | **{total['LOW']}** | **{total['NONE']}** |")
    return "\n".join(lines)


def block_systemic(data_dir, top=None):
    """details.md: every recurring rule, ranked by lectures affected."""
    reach = read_csv(os.path.join(data_dir, "rule_reach.csv"))
    titles = {r["rule"]: escape_roles(r["title"])
              for r in read_csv(os.path.join(data_dir, "rule_titles.csv"))}
    per = read_csv(os.path.join(data_dir, "series_rule_reach.csv"))
    counts = read_csv(os.path.join(data_dir, "series_summary.csv"))
    n_series = {r["series"]: int(r["lectures"]) for r in counts}
    total = n_series.get("TOTAL", 0)
    reach.sort(key=lambda r: -int(r["lectures_affected"]))
    if top:
        reach = reach[:top]
    out = []
    for i, r in enumerate(reach, 1):
        rule = r["rule"]
        tag = " (proposed)" if r["proposed"] == "1" else ""
        title = titles.get(rule, "")
        out.append(f"### {i}. `{rule}`{tag} — {title} "
                   f"({r['lectures_affected']} / {total} lectures, "
                   f"{r['total_occurrences']} occurrences)")
        parts = []
        for s in sorted((p for p in per if p["rule"] == rule),
                        key=lambda p: -int(p["lectures_affected"])):
            n = n_series.get(s["series"], 0)
            parts.append(f"`{s['series']}` {s['lectures_affected']} / {n}")
        out.append("- " + " · ".join(parts))
        out.append("")
    return "\n".join(out).rstrip()


def block_wins(data_dir, limit=8):
    """intro.md: highest-reach fixes, in plain words."""
    reach = read_csv(os.path.join(data_dir, "rule_reach.csv"))
    counts = read_csv(os.path.join(data_dir, "series_summary.csv"))
    total = next(int(r["lectures"]) for r in counts if r["series"] == "TOTAL")
    reach.sort(key=lambda r: -int(r["lectures_affected"]))
    lines = ["| Fix this | What it means | Lectures helped | Effort |",
             "|----------|---------------|-----------------|--------|"]
    shown = 0
    for r in reach:
        copy = WIN_COPY.get(r["rule"])
        if not copy:
            continue
        name, what, effort = copy
        tag = " *(proposed)*" if r["proposed"] == "1" else ""
        lines.append(f"| **{name}**{tag} | {what} | **{r['lectures_affected']}** | {effort} |")
        shown += 1
        if shown >= limit:
            break
    lines.append("")
    lines.append(f"Reach is out of {total} lectures. 🔧 = scriptable sweep · ✋ = needs a human pass.")
    return "\n".join(lines)


def block_focus(rows, data_dir):
    """intro.md: series ranked worst → best, with a needs-work count."""
    body = [r for r in rows if r["series"] != "TOTAL"]
    body.sort(key=lambda r: r["overall"])
    lines = ["| Attention | Series | Score | Needs work | Weakest categories |",
             "|-----------|--------|-------|-----------|--------------------|"]
    for r in body:
        needs = r["HIGH"] + r["MEDIUM"]
        share = needs / r["lectures"] if r["lectures"] else 0
        flag = "🔴 **High**" if share >= 0.5 else ("🟠 **Some**" if share >= 0.2 else "🟢 **Low**")
        weak = sorted((c for c in CATS if r[c] != ""), key=lambda c: r[c])[:2]
        weak_txt = ", ".join(f"{CAT_LABEL[c]} ({r[c]})" for c in weak)
        lines.append(f"| {flag} | [{r['series']}]({r['series']}/index.md) | {r['overall']} | "
                     f"{needs} / {r['lectures']} | {weak_txt} |")
    return "\n".join(lines)


def block_high_list(data_dir):
    """details.md: every HIGH-priority lecture, worst first."""
    scores = read_csv(os.path.join(data_dir, "scores.csv"))
    high = [r for r in scores if r["priority"] == "HIGH"]
    high.sort(key=lambda r: (num(r["overall"]) or 0, r["series"], r["lecture"]))
    lines = ["| Series | Lecture | " + " | ".join(CAT_LABEL[c] for c in CATS)
             + " | Overall | Floor |",
             "|--------|---------|" + "|".join(["---"] * len(CATS)) + "|---------|-------|"]
    for r in high:
        vals = [num(r[c]) for c in CATS if num(r[c]) is not None]
        floor = min(vals) if vals else ""
        cells = [(str(num(r[c])) if num(r[c]) is not None
                  else ("—" if r[c] in ("N/A", "") else "—")) for c in CATS]
        lines.append(f"| {SHORT.get(r['series'], r['series'])} | "
                     f"[{r['lecture']}]({r['series']}/{r['lecture']}.md) | "
                     + " | ".join(cells) + f" | **{r['overall']}** | {floor} |")
    return "\n".join(lines)


def block_snapshot(data_dir):
    """A pinned record of exactly what was audited."""
    with open(os.path.join(data_dir, "snapshot.json"), encoding="utf-8") as fh:
        meta = json.load(fh)
    lines = ["| Series | Lectures | Snapshot commit | Snapshot date |",
             "|--------|---------:|-----------------|---------------|"]
    for s in SERIES_ORDER:
        snap = meta["snapshot"].get(s, {})
        lines.append(f"| `{s}` | {meta['per_series'].get(s, '')} | "
                     f"`{snap.get('commit','')[:10]}` | {snap.get('date','')} |")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Per-series blocks (spliced into lectures/<series>/index.md)
# ---------------------------------------------------------------------------

def _review_coverage(series):
    """How many of a series' lectures have a judgment-review overlay."""
    import glob
    return len(glob.glob(os.path.join("reviews", series, "*.json")))


def block_series_meta(rows, data_dir, series):
    r = next((x for x in rows if x["series"] == series), None)
    if not r:
        return "_no data_"
    with open(os.path.join(data_dir, "snapshot.json"), encoding="utf-8") as fh:
        meta = json.load(fh)
    snap = meta["snapshot"].get(series, {})
    scored = [f"{CAT_LABEL[c].lower()} {r[c]}" for c in CATS if r[c] != ""]
    na = [CAT_LABEL[c].lower() for c in CATS if r[c] == ""]
    lines = [
        f"- **Audit date:** {snap.get('date', '')}",
        f"- **Corpus snapshot:** `{snap.get('commit', '')[:10]}`",
        f"- **Lectures audited:** {r['lectures']}",
        f"- **Average overall score:** {r['overall']} / 10",
        f"- **Average per-category scores:** {', '.join(scored)}"
        + (f"  *({', '.join(na)} not in scope for this series)*" if na else ""),
        "- **JAX:** out of scope — the `qe-jax-*` rules target `lecture-jax`.",
    ]
    cov = _review_coverage(series)
    n = r["lectures"]
    note = ("all lectures reviewed" if cov >= n else
            f"**{cov} of {n} reviewed** — scores for the unreviewed "
            f"{n - cov} reflect the 41 measured rules only, so they are not "
            f"directly comparable with the reviewed ones")
    lines.append(f"- **Judgment-review coverage:** {note}.")
    return "\n".join(lines)


def block_series_priority(rows, data_dir, series):
    r = next((x for x in rows if x["series"] == series), None)
    if not r:
        return "_no data_"
    n = r["lectures"]
    lines = ["| Priority | Count | % |", "|----------|-------|---|"]
    for p in PRIOS:
        lines.append(f"| {p:<8} | {r[p]:<5} | {r[p] / n * 100:.1f}% |")
    return "\n".join(lines)


def block_series_systemic(rows, data_dir, series):
    per = [r for r in read_csv(os.path.join(data_dir, "series_rule_reach.csv"))
           if r["series"] == series]
    titles = {r["rule"]: escape_roles(r["title"])
              for r in read_csv(os.path.join(data_dir, "rule_titles.csv"))}
    prop = {r["rule"] for r in read_csv(os.path.join(data_dir, "rule_reach.csv"))
            if r["proposed"] == "1"}
    r = next((x for x in rows if x["series"] == series), None)
    n = r["lectures"] if r else 0
    per.sort(key=lambda x: -int(x["lectures_affected"]))
    out = []
    for i, x in enumerate(per[:10], 1):
        tag = " *(proposed)*" if x["rule"] in prop else ""
        out.append(f"{i}. **`{x['rule']}`**{tag} — {titles.get(x['rule'], '')} — "
                   f"**{x['lectures_affected']} / {n}** lectures, "
                   f"{x['total_occurrences']} occurrences.")
    return "\n".join(out) if out else "_No violations measured in this series._"


def block_series_clean(rows, data_dir, series):
    """Rules with no violation anywhere in the series — the series' strengths."""
    per = {r["rule"] for r in read_csv(os.path.join(data_dir, "series_rule_reach.csv"))
           if r["series"] == series}
    titles = {r["rule"]: escape_roles(r["title"])
              for r in read_csv(os.path.join(data_dir, "rule_titles.csv"))}
    checked = {r["rule"] for r in read_csv(os.path.join(data_dir, "rule_reach.csv"))}
    all_checked = sorted(set(titles) & (checked | per))
    prop = {r["rule"] for r in read_csv(os.path.join(data_dir, "rule_titles.csv"))
            if r["proposed"] == "1"}
    clean = [r for r in all_checked if r not in per]
    if not clean:
        return "_Every checked rule is violated somewhere in this series._"
    return "\n".join(
        f"- **`{r}`**{' *(proposed)*' if r in prop else ''} — {titles.get(r, '')}"
        for r in clean)


def block_series_ranked(rows, data_dir, series):
    scores = [r for r in read_csv(os.path.join(data_dir, "scores.csv"))
              if r["series"] == series]
    scores.sort(key=lambda r: (num(r["overall"]) or 0, r["lecture"]))
    head = "| # | Lecture | " + " | ".join(CAT_LABEL[c] for c in CATS) \
           + " | Overall | Priority |"
    rule = "|---|---------|" + "|".join(["---"] * len(CATS)) + "|---------|----------|"
    lines = [head, rule]
    for i, r in enumerate(scores, 1):
        cells = [(f"{num(r[c]):g}" if num(r[c]) is not None else "—") for c in CATS]
        lines.append(f"| {i} | [{r['lecture']}]({r['lecture']}.md) | "
                     + " | ".join(cells)
                     + f" | **{r['overall']}** | {r['priority']} |")
    return "\n".join(lines)


def _wrap(text, width=88):
    """Wrap a generated paragraph to the width the hand-written prose uses."""
    return textwrap.fill(text, width=width, break_long_words=False,
                         break_on_hyphens=False)


def block_review_coverage(rows, data_dir):
    """The coverage caveat on `intro.md`, with the gap measured rather than asserted.

    A lecture assessed against more rules scores lower, so an uneven judgment
    layer makes the cross-series scoreboard partly a ranking of coverage. The
    size of that effect moves every time an overlay lands, which is exactly why
    this paragraph is generated and not written.
    """
    scores = read_csv(os.path.join(data_dir, "scores.csv"))
    have, lack = [], []
    for r in scores:
        overlay = os.path.join("reviews", r["series"], r["lecture"] + ".json")
        (have if os.path.exists(overlay) else lack).append(r)

    def stats(group):
        vals = [float(r["overall"]) for r in group if r["overall"]]
        high = sum(1 for r in group if r["priority"] == "HIGH")
        return sum(vals) / len(vals), 100.0 * high / len(group)

    n, k = len(scores), len(have)
    # What follows the headline sentence is part of the same block on purpose. Whether the
    # cross-series comparison is provisional *is* a fact about coverage, so it cannot be
    # left as hand-written prose beside a generated number — at full coverage the standing
    # "provisional until coverage evens out" paragraph became false while the generated
    # sentence above it was already correct.
    # The admonition itself is emitted here, not written around the markers in ``intro.md``.
    # Which admonition is right is also a fact about coverage: a warning at full coverage
    # reads as a caveat that no longer applies, and nothing outside this function knows
    # whether it applies.
    # The two branches cite deliberately different places. The completed-coverage sentence
    # is a historical citation — `audit.2026-05.style-guide#5` is the *record* of the caveat
    # it retires, and an archived repo keeps its issues readable forever, so that link stays
    # good. The partial-coverage branches describe a live question about the pass being
    # measured right now, and a locked issue on an archived repo cannot receive one; they
    # point at this ledger's own issues instead. No ledger issue covers coverage
    # comparability today, so the reference is to the tracker as a whole, not to a number
    # that does not exist. Keep every link label a single unbroken token: ``_wrap`` will not
    # split one, and this repo's prose has no link broken across a line.
    def _admonition(kind, body):
        return "```{" + kind + "}\n" + _wrap(body) + "\n```"

    if not lack:
        return _admonition("note",
            f"**Every one of the {n} lectures has been through the judgment layer**, so "
            f"the scores below are comparable across series and the cross-series "
            f"comparison stands on its own. Per-series coverage is still published on each "
            f"series' Summary page, and the *within-series* ranking and the rule-reach "
            f"numbers were always sound — those are measured over the whole corpus by the "
            f"same code. This retires the caveat tracked in "
            f"[audit.2026-05.style-guide#5]"
            f"(https://github.com/QuantEcon/audit.2026-05.style-guide/issues/5)."
        )
    if not have:
        return _admonition("warning",
            "**No lecture has been through the judgment layer yet**, so every score below "
            "reflects the measured rules only, and the cross-series comparison is a "
            "ranking of the deterministic evidence alone. Coverage is tracked in this "
            "ledger's [issues](https://github.com/QuantEcon/compliance-lecture-style/issues)."
        )

    a, b = stats(have), stats(lack)
    return _admonition("warning",
        f"**Review coverage is incomplete in this pass, and it moves the scores.** "
        f"The judgment layer has reached **{k} of the {n} lectures**; a lecture "
        f"assessed against more rules scores lower — not because it is worse, but "
        f"because more of it was looked at. The gap is large enough to matter: the "
        f"{k} reviewed average **{a[0]:.2f}** with {a[1]:.0f} % HIGH, the {n - k} "
        f"unreviewed **{b[0]:.2f}** with {b[1]:.0f} % HIGH. So **the cross-series "
        f"comparison below is provisional** wherever coverage differs between series, and "
        f"the per-series coverage is published on each series' Summary page. Treat the "
        f"*within-series* ranking and the rule-reach numbers as sound — those are measured "
        f"over the whole corpus by the same code — and treat a small gap between two "
        f"series' overall scores as noise until coverage evens out. This gap is tracked "
        f"in this ledger's "
        f"[issues](https://github.com/QuantEcon/compliance-lecture-style/issues)."
    )


BLOCKS = {
    "scoreboard": lambda rows, d: block_scoreboard(rows, readme=False),
    "readme-scoreboard": lambda rows, d: block_scoreboard(rows, readme=True),
    "full-scoreboard": lambda rows, d: block_full_scoreboard(rows),
    "systemic": lambda rows, d: block_systemic(d),
    "wins": lambda rows, d: block_wins(d),
    "focus": lambda rows, d: block_focus(rows, d),
    "high-list": lambda rows, d: block_high_list(d),
    "snapshot": lambda rows, d: block_snapshot(d),
    "review-coverage": block_review_coverage,
}

SERIES_BLOCKS = {
    "series-meta": block_series_meta,
    "series-priority": block_series_priority,
    "series-systemic": block_series_systemic,
    "series-clean": block_series_clean,
    "series-ranked": block_series_ranked,
}


def splice(path, rows, data_dir):
    """Replace every ``<!-- qe:NAME -->…<!-- /qe:NAME -->`` region in *path*."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    series = os.path.basename(os.path.dirname(os.path.abspath(path)))
    changed = []
    todo = list(BLOCKS.items())
    if series in SERIES_ORDER:
        todo += [(name, (lambda fn: lambda rows, d: fn(rows, d, series))(fn))
                 for name, fn in SERIES_BLOCKS.items()]
    for name, fn in todo:
        pat = re.compile(
            r"(<!--\s*qe:" + re.escape(name) + r"\s*-->\n)(.*?)(\n<!--\s*/qe:"
            + re.escape(name) + r"\s*-->)", re.S)
        if not pat.search(text):
            continue
        new = fn(rows, data_dir)
        text = pat.sub(lambda m: m.group(1) + new + m.group(3), text)
        changed.append(name)
    if changed:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
    return changed


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", default="lectures/data")
    ap.add_argument("--summarise", action="store_true")
    ap.add_argument("--history", default="", metavar="PERIOD",
                    help="append this pass to history.csv under PERIOD (e.g. 2026-08)")
    ap.add_argument("--splice", action="store_true")
    ap.add_argument("--targets", nargs="*", default=[
        "README.md", "lectures/intro.md", "lectures/details.md", "lectures/spec.md"]
        + [f"lectures/{s}/index.md" for s in SERIES_ORDER])
    ap.add_argument("--emit", default="", help="print one block by name and exit")
    args = ap.parse_args()

    rows = summarise(args.data)
    if args.summarise:
        print("wrote", write_summary(args.data, rows))
    if args.emit:
        print(BLOCKS[args.emit](rows, args.data))
        return 0
    if args.history:
        print("wrote", append_history(args.data, args.history, rows))
    if args.splice:
        for t in args.targets:
            if not os.path.exists(t):
                continue
            done = splice(t, rows, args.data)
            if done:
                print(f"{t}: spliced {', '.join(done)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
