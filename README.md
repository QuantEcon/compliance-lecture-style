# QuantEcon Lecture Style Compliance

A standing record of how the QuantEcon lecture corpus conforms to the house style
guide — scored against the conventions in
[`QuantEcon.manual`](https://github.com/QuantEcon/QuantEcon.manual/tree/main/manual/styleguide)
using the rule registry from
[`QuantEcon/action-style-guide`](https://github.com/QuantEcon/action-style-guide), and
re-measured in place each pass. 348 lectures, 5 series, two passes on the record.

## 📊 Read the ledger

**Published site:** https://quantecon.github.io/compliance-lecture-style/

A Jupyter Book with the cross-series synthesis, the charts and the cross-pass trend, the
scoring spec, and a drill-down report for every lecture in the corpus.

## What this repo is

A `compliance-{domain}` repository — in QEP-3's words, a *"standing record of a domain's
conformance with a named standard: rubric + runbook, findings and scores re-measured in
place per pass; versioned history seeded from each absorbed audit"*.

The boundary rule that gives this repo its shape is **the audit is the event; the
compliance repo is the ledger**. A one-off examination publishes as a dated `audit-*`
repo and freezes there. When examinations acquire a cadence, an owner and a runbook, the
standing record they accumulate is a `compliance-*` repo, assembled from one or more
audits. A second rule separates it from `status-*`: *status reports what machines
observe; compliance records what a rubric adjudicates* — the numbers here are measured by
program, but what counts as a finding is settled by [the rubric](lectures/spec.md).

In practice that means nothing here is re-issued. A pass does not replace the last one, it
joins it: a period is a row in `lectures/data/history.csv`, and the comparison across rows
is the point of keeping the record at all.

The type is **proposed, not settled**: QEP-3 is still an open PR,
[QuantEcon/qeps#7](https://github.com/QuantEcon/qeps/pull/7), and its Adoption section
names this migration as the type's first instance. Cite it that way in anything written
here.

## Where this came from

This ledger is assembled from
[`audit.2026-05.style-guide`](https://github.com/QuantEcon/audit.2026-05.style-guide) —
the dated repo that ran the May-2026 examination and grew the pipeline, the rubric and the
runbook around it.

- **That repo keeps its name.** QEP-3's invariant is that renames fix names, they never
  transmute types, so a rename to `audit-lectures-style-guide` was proposed and then
  rejected in favour of assembling this repository alongside it. The audit repo is
  archived once absorbed, and nothing a reader depends on *for reading* changes: its
  published report stays live at <https://quantecon.github.io/audit.2026-05.style-guide/>
  as the May-2026 record, and its issues stay readable. What archiving does take away is
  writing — the issues become read-only, no new comments and no reopening, which is why the
  four still open move here (below). The naming decision is
  [#2](https://github.com/QuantEcon/audit.2026-05.style-guide/issues/2), the assembly
  itself [#7](https://github.com/QuantEcon/audit.2026-05.style-guide/issues/7).
- **Both passes are here.** [`lectures/data/history.csv`](lectures/data/history.csv) holds
  the 2026-05 and the 2026-08 rows, and both were measured with the current code — so the
  trend is a like-for-like comparison of two corpus snapshots, not of two vintages of
  checker.
- **The open questions moved with it.** Archiving locks a repo's issues, so the four
  questions still open against the audit — the `{doc}` link form for same-series
  references, the near-empty MEDIUM band, how lectures shared between `lecture-dp` and
  `lecture-python.myst` are counted, and the rubric's weights now that rule reach is
  measured — continue here as
  [#1–#4](https://github.com/QuantEcon/compliance-lecture-style/issues/1).

## Scope

- **348 lectures** across 5 series: `lecture-python-intro`,
  `lecture-python-programming`, `lecture-python.myst`, `lecture-python-advanced.myst`,
  `lecture-dp`
- **7 in-scope rule categories**: Writing, Math, Code, Figures, References, Links,
  Admonitions (the 7 `qe-jax-*` rules are out of scope — they target `lecture-jax`)
- **41 of the 49 rules are checked by program** — 36 of the 42 in-scope registry rules
  plus 5 of the 7 proposed in [issue #18](https://github.com/QuantEcon/action-style-guide/issues/18);
  the remaining 8 are genuine judgment calls and are reviewed by reading
- **The judgment layer is complete** — every lecture has a review overlay in `reviews/`,
  and each overlay records the version of the lecture it judged
- **Corpus snapshot pinned per series** — [`lectures/data/snapshot.json`](lectures/data/snapshot.json)
  for the current pass, and [`lectures/data/snapshot_history.csv`](lectures/data/snapshot_history.csv)
  for every recorded period, which is what makes an earlier period reproducible

## Scoreboard

<!-- qe:readme-scoreboard -->
| Series | Lectures | Overall | HIGH | weakest category |
|--------|---------:|--------:|-----:|------------------|
| lecture-python-advanced.myst | 68 | 7.4 | 43 | Writing (4.6) |
| lecture-python.myst | 145 | 7.7 | 81 | Writing (4.5) |
| lecture-dp | 52 | 7.7 | 34 | Writing (4.7) |
| lecture-python-programming | 27 | 8.0 | 20 | Writing (4.1) |
| lecture-python-intro | 56 | 8.1 | 19 | Writing (5.2) |
| **Corpus** | **348** | **7.7** | **197** | Writing (4.6) |
<!-- /qe:readme-scoreboard -->

No lecture in this pass is HIGH on its overall score — every one of them is HIGH because a
category fell below the bar. So the triage question is *which category* rather than *which
lecture*, and Writing is the binding constraint on most of them, then Math.

## How it works

```
corpus snapshot ──► tools/qestyle_scan.py ──► lectures/data/*.csv
                                                    │
                          tools/qestyle_draft.py ◄───┤   per-lecture reports
                                                    │
                          tools/qestyle_score.py ◄───┤   scores + priority
                                                    │
                          tools/qestyle_report.py ◄──┘   aggregate tables
```

The numbers live in `lectures/data/`. The per-lecture reports, the scoreboard, the
triage page and the charts are all derived from them, so they cannot disagree.
`tools/qestyle_check.py` is the gate that asserts it.

## Running a pass

A pass is three skills, split along the one seam that matters — the mechanical layers run
the whole corpus in seconds, the judgment layer costs about five agent-minutes a lecture:

- **`/pass-measure`** — corpus, scan, draft, score, splice, gate, build, and print the
  review queue. Seconds, no judgment calls, every number reproducible from the pinned
  snapshot.
- **`/pass-review`** — the judgment layer: the 8 judgment-only rules read against each
  lecture and written to `reviews/<series>/<stem>.json`. Budgeted and resumable; it stops
  when the budget is spent, not when the corpus is finished.
- **`/pass-publish`** — close a period: re-measure the previous snapshot with the current
  code, write the series prose, append the history row, gate, build, PR, deploy.

`tools/qestyle_status.py` says where a pass stands. It joins
`lectures/data/lecture_blobs.csv` — one git blob SHA per lecture at the pinned
snapshot — against each overlay's `source.blob`, so the queue is *fresh / stale /
missing* rather than merely *reviewed / not reviewed*, and review cost tracks corpus
churn instead of corpus size.

[`UPDATE.md`](UPDATE.md) is the reference runbook; the methodology is
[`lectures/spec.md`](lectures/spec.md) §8–§10.

## Repository layout

```
.
├── README.md                  ← this file
├── ROADMAP.md                 ← project direction, open decisions, phased plan
├── UPDATE.md                  ← runbook: how to run a pass and refresh the ledger
├── CLAUDE.md                  ← read-me-first orientation for agents
├── requirements.txt           ← Jupyter Book build dependencies (needs Python 3.12+)
├── tools/                     ← the pipeline: rule checks, scoring, reports, the gate
│   ├── qestyle_status.py      ← coverage, staleness and the review queue
│   └── VERIFICATION.md        ← how each of the 41 checks was verified
├── reviews/                   ← one judgment overlay per lecture, version-stamped
├── .claude/skills/            ← pass-measure · pass-review · pass-publish
├── contributions/             ← source behind the action-style-guide issues (#18–#21)
├── .github/workflows/         ← build + deploy to GitHub Pages
└── lectures/                  ← Jupyter Book source
    ├── _config.yml, _toc.yml
    ├── data/                  ← the numbers; everything else is derived from these
    ├── intro.md               ← front-page triage (where to focus)
    ├── details.md             ← full findings & remediation plan
    ├── spec.md                ← rubric, methodology, deterministic coverage
    ├── charts.md              ← visual summary, built from data/ at build time
    ├── appendix.md            ← feedback to the style guide & action-style-guide
    └── lecture-<series>/      ← per-series "Summary" + per-lecture reports
```

**This repository is the source of truth for the published ledger** — the site is built
from `lectures/` by `.github/workflows/deploy.yml` on every push to `main`.

## Related

- Contribution issues opened against `action-style-guide`:
  [#18](https://github.com/QuantEcon/action-style-guide/issues/18) (new rules),
  [#19](https://github.com/QuantEcon/action-style-guide/issues/19) (deterministic-checker
  scope), [#20](https://github.com/QuantEcon/action-style-guide/issues/20) (bulk audit
  mode), [#21](https://github.com/QuantEcon/action-style-guide/issues/21) (corpus offer)
- Style guide source:
  https://github.com/QuantEcon/QuantEcon.manual/tree/main/manual/styleguide
