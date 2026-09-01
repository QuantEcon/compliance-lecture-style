# CLAUDE.md

Guidance for Claude Code (and other agents) working in this repo. Keep it short — the
authoritative detail lives in `UPDATE.md`, `lectures/spec.md` and `ROADMAP.md`; this file
is the read-me-first orientation and the guardrails.

## What this is

The **standing conformance ledger** for QuantEcon lecture style: a record of how the lecture
corpus measures against the style guide, re-measured in place each pass rather than re-issued.
It's a Jupyter Book published to GitHub Pages
(<https://quantecon.github.io/compliance-lecture-style/>), built from `lectures/` by
`.github/workflows/deploy.yml` on every push to `main`.

Under QEP-3 ([QuantEcon/qeps#7](https://github.com/QuantEcon/qeps/pull/7) — still an open PR,
so cite the type as proposed, not as settled policy) this is a `compliance-{domain}` repo: the
audit is the event, the ledger is the standing record assembled from it. The 2026-05 audit that
seeded this one keeps its own name, is archived once absorbed, and stays published at
<https://quantecon.github.io/audit.2026-05.style-guide/>; the decision record is
[audit#2](https://github.com/QuantEcon/audit.2026-05.style-guide/issues/2), summarised in
[`ROADMAP.md`](ROADMAP.md) §1. "Audit" is still the right word for a *pass* and for the
May-2026 event — not for this repository.

## Read first

Three skills, split along the one seam that matters: the mechanical layers run the whole
corpus in seconds at almost no token cost, while the judgment layer costs about five
agent-minutes a lecture — roughly 30 agent-hours for 348. No session holds a whole pass, so
don't start one as if it could.

- **`/pass-measure`** (`.claude/skills/pass-measure/SKILL.md`) — corpus, snapshot, scan,
  draft, score, splice, gate, build, and print the review queue. Use it for anything
  mechanical: a rule change, a corpus refresh, or just "where does the pass stand".
- **`/pass-review`** (`.claude/skills/pass-review/SKILL.md`) — the judgment layer. Takes a
  budget of lectures off the queue, writes `reviews/<series>/<stem>.json`, and stops when the
  budget is spent rather than when the corpus is finished. Run it often and small.
- **`/pass-publish`** (`.claude/skills/pass-publish/SKILL.md`) — close a period: re-measure
  the previous snapshot with current code, write the series prose, append the history row,
  gate, build, PR, deploy. The deliberate act; everything else stops at a branch.
- **[`UPDATE.md`](UPDATE.md)** — the runbook: how to run a pass, the consistency gate, how to
  maintain `contributions/`, how to open a new period. **Follow it before any structural
  change**, and if a skill and the runbook disagree, fix one of them.
- **[`lectures/spec.md`](lectures/spec.md)** §8–§10 — the pass methodology (evidence /
  scoring / review layers), the measured deterministic coverage, and the exact commands.
  §8.3 is the reviewer's brief.
- **[`ROADMAP.md`](ROADMAP.md)** — direction and the open decisions.
- **`QuantEcon/project-style-guide`** (private hub) — program-level direction. Where this
  repo's docs and the hub overlap, **the hub is the home of record**.

## The one thing to understand

**The numbers are not written, they are derived.** `lectures/data/*.csv` is the source:
`tools/qestyle_scan.py` measures the corpus into it, and the per-lecture reports, the
scoreboard, the triage page and the charts are all generated from it.

```
corpus snapshot → qestyle_scan → data/*.csv → qestyle_draft → per-lecture reports
                                            → qestyle_score → scores.csv
                                            → qestyle_report → spliced tables
                                            → qestyle_check  → the gate
```

So: **never hand-edit a number.** If a count looks wrong, fix the check in
`tools/qestyle_rules.py` and re-run — editing the report instead makes it disagree with
the CSVs, and `tools/qestyle_check.py` will fail.

## Non-negotiable conventions

Enforce everywhere. `tools/qestyle_check.py` asserts all of these; run it before pushing.

- **Rule IDs:** canonical `qe-*` only (e.g. `qe-fig-001`). Never legacy `W#`/`M#` or
  `qe-*-A#` placeholders.
- **Proposed rules:** the 7 not-yet-registered rules (`qe-writing-009`,
  `qe-math-010`–`qe-math-015`) always carry a **(proposed)** tag where cited. A section
  that is itself about the proposed rules need not repeat the tag on every row.
- **Titles:** per-lecture report H1 = bare lecture stem (`# lqcontrol`); each series
  `index.md` H1 = `# Summary`. No `# Style Audit —` prefix.
- **No `Spec version` line** in report headers. Every report header *does* carry a
  **Corpus snapshot** line naming the commit it was measured against.
- **Review overlays record what they judged.** Each `reviews/<series>/<stem>.json` carries
  `"source": {"commit": …, "blob": …}` — the series snapshot commit and the git blob SHA of
  the lecture `.md` it was written against. `tools/qestyle_status.py` joins that against
  `lectures/data/lecture_blobs.csv` to tell a fresh overlay from a stale one, which is what
  makes review cost scale with corpus *churn* instead of corpus *size*. Never hand-stamp it:
  the scan writes the blobs, and `tools/qestyle_backfill_provenance.py` stamps older overlays
  — before the snapshot advances, never after, or it launders stale reviews into fresh ones.
- **A score row carries its coverage.** Every `history.csv` row has a `reviewed` column —
  how many of its lectures fold in a judgment overlay — and a twin row in
  `history_mechanical.csv` measured from the evidence layer alone. A lecture assessed
  against more rules scores lower, so **never compare score levels across periods whose
  `reviewed` differs**; quote the mechanical twin or rule reach. Both files are written by
  `qestyle_report.py --history`, which needs `scores_mechanical.csv` (a draft made without
  `--reviews`, scored) beside `scores.csv`; the gate holds each row to both.
- **JAX is out of scope** — distinct from `N/A` ("not applicable to this lecture").
- **One pass, no process narrative.** A report describes the corpus at one pinned
  snapshot; it never narrates how the pass was run in "v1/v2" or "two-pass" terms.
  Comparing *against a previous period* is different and is wanted — that is what
  `data/history.csv`, `data/rule_reach_history.csv` and the trend chart are for.
- **Spliced regions are generated.** Anything between `<!-- qe:NAME -->` and
  `<!-- /qe:NAME -->` is overwritten by `tools/qestyle_report.py --splice`. Write prose
  outside the markers.

## Operational gotchas

- **The build needs Python 3.12+.** `quantecon-book-theme==0.15.1` requires it; a 3.11
  environment fails to resolve. Build is vanilla `jupyter-book` +
  `quantecon-book-theme` — *not* the QuantEcon build container. `lectures/charts.md`
  executes at build time and reads `lectures/data/`, so `matplotlib`/`numpy` must stay in
  `requirements.txt`.
- **The corpus is not in this repo.** `/pass-measure` §2 clones the 5 series plus
  `action-style-guide` into `.corpus/` (gitignored) as blobless sparse checkouts — ~840 KB a
  series, because only `lectures/*.md` and `_static/quant-econ.bib` are needed. Clone *inside*
  the working directory: a path under the repo needs no permission prompt, so an unattended
  run can't stall waiting for an approval nobody is there to give. Do not clone them whole,
  and do not drop the `.bib` — without it every citation check resolves zero keys, silently.
- **A corpus outside the tree needs auto mode ON** if you fan work out to subagents;
  otherwise every cross-repo read is denied and the run stalls. This stalled the original
  run once, and is the reason `.corpus/` now lives here.
- **`lecture-dp` syncs lectures from `lecture-python.myst`** (`cross_product_trick`,
  `ifp_advanced`, `inventory_q`, `rs_inventory_q`, …). Their findings appear twice in the
  corpus totals; fix upstream and both clear. How they *should* be counted is open as
  [compliance-lecture-style#3](https://github.com/QuantEcon/compliance-lecture-style/issues/3).
- **`contributions/` mirrors live `action-style-guide` issues #18–#21.** Editing a body here
  does not update GitHub — re-sync with `gh issue edit` (see `UPDATE.md`). Re-syncing needs a
  session with GitHub access to that repo; if this one hasn't got it, say so plainly and leave
  the re-sync as a named open item rather than writing prose implying the live issues moved.
- **Pushing to `main` deploys the site.** That is `/pass-publish`'s call, not a side effect of
  a measurement refresh: work on a branch, and when you do push, watch the run with
  `gh run watch`.

## Layout

- `tools/` — the pipeline: `qestyle_lex` (MyST lexer) · `qestyle_rules` (one function per
  checkable rule) · `qestyle_scan` (evidence + `lecture_blobs.csv`) · `qestyle_draft` (report
  drafts) · `qestyle_score` (scores) · `qestyle_report` (aggregate tables) · `qestyle_check`
  (gate) · `qestyle_toc` · `qestyle_status` (coverage, staleness, review queue) ·
  `qestyle_backfill_provenance` · `VERIFICATION.md` (what each check was sampled against —
  read it before "fixing" a detector)
- `lectures/` — published book: `intro` (triage) · `details` · `charts` · `spec` ·
  `appendix` · `data/` (the numbers) · `lecture-<series>/` (`index` = Summary +
  per-lecture reports)
- `reviews/<series>/<stem>.json` — the judgment overlays, folded back into the reports by
  `qestyle_draft --reviews reviews`
- `contributions/` — issue bodies + rule drafts (root, not published)
- `.claude/skills/pass-measure/` · `pass-review/` · `pass-publish/` — the three pass skills;
  keep them in step with `UPDATE.md`
- `.corpus/` (sparse corpus checkout) · `.venv/` (build environment) — both gitignored
- `README.md` · `ROADMAP.md` · `UPDATE.md` · `CLAUDE.md` — root docs

## Commits

Follow the global commit conventions (co-author trailer; neutral cross-repo issue
references — no closing keywords before `owner/repo#N`). Commit/push only when asked.
