---
name: pass-review
description: Run the judgment layer of a lecture style pass — take a budget of lectures off the review queue, read each against the 8 judgment-only rules, and write its reviews/<series>/<stem>.json overlay. Use when asked to review the next batch of lectures, continue or resume the judgment pass, work through the review queue, top up review coverage after a corpus refresh, or write strengths and recommended actions for lectures. Budgeted and resumable by design: it stops when the budget is spent, not when the corpus is finished.
---

# Review a batch

## The budget is the interface

**This skill takes a budget — a number of lectures, default 10 — and stops when the budget
is spent, not when the work is done.** Say the budget back at the start of the run, and stop
at it even if the queue is long and the session still has room.

That is not caution, it is arithmetic. Measured in this repo: **one overlay costs about five
agent-minutes**, so the full corpus of 348 lectures is on the order of **30 agent-hours**. No
session holds that, at any concurrency — and concurrency does not reduce the total. It only
raises the burn rate and the amount of work in flight when the session dies. Two concurrent
reviewer agents exhausted a session limit in under half an hour, mid-batch.

Everything else in a pass is cheap: [`pass-measure`](../pass-measure/SKILL.md) scans, drafts,
scores, splices, gates and builds the whole corpus in seconds at essentially no token cost.
This skill is the entire expensive part. It is built to be run many times on a small budget,
never once on a large one.

Read [`lectures/spec.md`](../../../lectures/spec.md) §8.3 before reviewing anything. It is the
reviewer's brief and this skill does not restate it.

## What you are judging

Eight rules, and only these eight — everything else in the rubric is already measured by
program and is not yours to re-count:

`qe-writing-002` (clear, concise, valuable) · `qe-writing-003` (logical flow) ·
`qe-writing-005` (bold for definitions, italic for emphasis) · `qe-writing-007` (visual
elements) · `qe-math-009` (prefer simpler notation) · `qe-code-001` (PEP8 unless closer to
mathematical notation) · `qe-math-014` *(proposed)* · `qe-math-015` *(proposed)*

Plus the per-lecture **Strengths** and **Recommended actions** prose, and any
**`scanner_doubts`** — which are the most valuable thing this skill produces (see below).

---

## 1. Get the queue from the tool, never from a file

```bash
.venv/bin/python tools/qestyle_status.py                 # coverage and staleness
.venv/bin/python tools/qestyle_status.py --queue 10      # the next N lectures to review
```

`qestyle_status.py` joins `lectures/data/lecture_blobs.csv` (written by the scan: one row per
lecture, `series,lecture,blob`) against each overlay's `source.blob`, and classifies every
lecture as **fresh** (blobs equal), **stale** (blobs differ — the lecture has been edited since
it was judged) or **missing** (no overlay). The queue is that join, recomputed from disk on
every run.

**Never hand-maintain a queue file.** A previous pass committed `.claude/review-queue.json` as
its worst-first list; it went stale repeatedly and was deleted rather than left to mislead a
resume (commit `42cd094`). A queue is derived state — treat it the way the numbers are treated.

If `lecture_blobs.csv` is missing, or the corpus is not checked out at the commits
`lectures/data/snapshot.json` pins, the queue is not trustworthy: run
[`pass-measure`](../pass-measure/SKILL.md) first and come back.

**Order worst-first, but even out coverage first.** Put a series with little or no coverage
ahead of one that is nearly done. An uneven judgment layer makes the cross-series scoreboard
partly a ranking of review coverage, which is the one thing the scoreboard must not be.

## 2. Review in batches of about ten

**One agent at a time by default.** Sequential is slower per hour and far more predictable,
which is what matters when the work spans sessions. Up to **three concurrent agents only on
disjoint series** — disjoint is the load-bearing part: agents writing into one `reviews/<series>/`
directory contend, and cross-file findings within a series (a notation that drifts between
lectures, a convention two lectures apart disagree on) need one agent that has seen the whole
series.

Each reviewer gets: the batch, the lecture sources at the pinned commit, and the drafted report
`lectures/<series>/<stem>.md` for the mechanical counts. For a file over 1500 lines, read the
head, a middle slice and the tail (spec §8.3).

**Auto mode must be ON if the corpus lives outside the working directory** — subagents cannot
read outside it otherwise, every corpus read is denied, and the run stalls. This has bitten two
passes. Cloning into `.corpus/` (gitignored) removes the question entirely; every tool takes
`--corpus`, so the path is free.

`lecture-dp` syncs several lectures from `lecture-python.myst` (`cross_product_trick`,
`ifp_advanced`, `inventory_q`, `rs_inventory_q`, …). If a batch contains both copies, judge them
consistently and recommend the fix upstream — a fix applied in `lecture-dp` is overwritten by
the next sync. How the shared copies should be *counted* is open as
[compliance-lecture-style#3](https://github.com/QuantEcon/compliance-lecture-style/issues/3);
review both, do not deduplicate them yourself.

## 3. Write each overlay the moment that lecture is finished

Not at the end of the batch. An API error mid-batch has cost a whole batch before.

`reviews/<series>/<stem>.json`:

```json
{
  "series": "lecture-dp",
  "lecture": "lqcontrol",
  "judgment": [
    {"rule": "qe-writing-002", "count": 4, "lines": [138, 156],
     "detail": "sentences of 45+ words carrying two ideas each"}
  ],
  "strengths": ["Equation labels and {eq} cross-references used consistently"],
  "actions": ["Replace every apostrophe transpose with ^\\top"],
  "scanner_doubts": [],
  "source": {"commit": "c30490a2f48867d155d92c3c94a6cd6bfbda82a5",
             "blob": "3610065f629241c8b6c4acebd97354c9a925a0bd"}
}
```

**`source` is not optional in practice.** Copy `commit` from `lectures/data/snapshot.json` for
that series and `blob` from that lecture's row in `lectures/data/lecture_blobs.csv`:

```bash
.venv/bin/python - <<'PY'
import csv, json
series, stem = 'lecture-dp', 'lqcontrol'          # <- the lecture you just finished
blob = next(r['blob'] for r in csv.DictReader(open('lectures/data/lecture_blobs.csv'))
            if r['series'] == series and r['lecture'] == stem)
commit = json.load(open('lectures/data/snapshot.json'))['snapshot'][series]['commit']
print(json.dumps({"commit": commit, "blob": blob}))
PY
```

That stamp is the whole reason this skill can be run incrementally. An overlay with no `source`
still counts as coverage, but it can never be shown to be current, so it returns to the queue on
every refresh forever — and the review cost goes back to scaling with corpus *size* instead of
corpus *churn*. Stamped, a refresh only re-reviews what actually changed.

Measured over 2026-05 → 2026-08: 186 of the 348 lectures were byte-identical, 114 edited and 48
new, so the queue would have been **162 of 348** — roughly **13.5 agent-hours against 29**. Worth
knowing before you plan a session: that is a 53 % saving, not the order-of-magnitude one an
earlier note here claimed. It is also a function of cadence — three months touches half the
corpus, a month touches far less — so **the first pass after a long gap should be budgeted as
close to a full one**.

### Reviewer rules that matter

- **Never re-count a mechanical rule.** The drafted counts are authoritative. A count that looks
  wrong goes in `scanner_doubts` — never quietly edited, or the report stops matching the CSVs
  and the gate fails.
- **Omit a rule that is satisfied.** Two or three judgment findings per lecture is typical, and
  none is a legitimate answer. Invented findings are worse than no findings.
- **Strengths must be specific to that lecture** — a named section, an equation label, a figure,
  a convention the lecture actually holds to. Never "well written", never anything that would be
  true of any lecture in the corpus.
- **Be consistent across reports.** The same deviation gets the same rule ID, the same severity
  and the same wording every time you write it.
- **Adjust a drafted category score only for a judgment reason**, and say what it was.
- **Do not modify any lecture file**, in this repo or in the corpus.
- Cite a proposed rule with its **(proposed)** tag. The gate checks this.

## 4. Commit each batch

```bash
SERIES=lecture-dp          # the series this batch belongs to
git add "reviews/$SERIES"
git commit -m "Review $SERIES: 10 overlays (lqcontrol, jv, odu, …)"
```

The overlay is the durable unit and is useful the moment it is written — it does not need the
reports regenerated to be worth committing. Overlays are deliberately decoupled from the counts,
so fixing a check and re-running the measure step never destroys review work. A session that
dies after a commit has lost nothing; a session that dies before one has lost the batch.

## 5. Refresh once, at the end of the session — not per batch

The refresh rewrites all 348 per-lecture reports. Run it per batch and a 348-file diff lands on
top of every ten overlays, burying the review work in the history and making the branch unreadable
for whoever picks it up next.

## 6. End the session deliberately

Overlays committed but not folded in are safe. A dirty tree is not. So finish with:

```bash
CORPUS=.corpus; R=$CORPUS/action-style-guide/style_checker/rules
.venv/bin/python tools/qestyle_draft.py --corpus $CORPUS --out lectures --date YYYY-MM-DD \
    --rules $R --reviews reviews --judgment-csv lectures/data/judgment.csv
.venv/bin/python tools/qestyle_score.py --root lectures --fix --csv lectures/data/scores.csv
.venv/bin/python tools/qestyle_report.py --summarise --history YYYY-MM --splice
.venv/bin/python tools/qestyle_check.py --root lectures --data lectures/data --corpus $CORPUS
.venv/bin/jupyter-book build lectures --path-output /tmp/bk
```

Then commit the refreshed reports and **push the branch** (not `main` — publishing a period is
[`pass-publish`](../pass-publish/SKILL.md)'s job).

Two things to watch, both caused by reviewer prose:

- **`--reviews reviews` is load-bearing.** Omit it and the draft silently discards every overlay
  ever written.
- **The build is clean, so any warning is a regression** — and the usual cause is a MyST role or
  an unbalanced backtick in a `detail`, `strengths` or `actions` string. `escape_roles()` in
  `tools/qestyle_draft.py` is what renders reviewer prose literally; its two failure modes (a
  role name outside the allowlist, and an unbounded target running away across a stray backtick)
  are written up in [`tools/VERIFICATION.md`](../../../tools/VERIFICATION.md).

The gate must print **All checks passed**.

---

## `scanner_doubts` — the most productive output of this skill

Around **thirty verified detector and lexer fixes have come from reviewer doubts, and none from
any other source.** Nothing else a reviewer writes improves the next pass as much. Treat the
field as a first-class deliverable, not a leftover.

A useful doubt names two things:

1. **the pattern** — what the check appears to be doing wrong, stated as a rule about inputs, not
   as "this count looks high"; and
2. **the exact input it mishandles** — file, line, and the literal text, so the next reader can
   reproduce it in one command.

If you go on to propose a fix, **measure it in both directions**: additions *and* removals, over
the whole corpus, with a canary list of known-real findings that must survive. Removing false
positives is worthless if it also removes true ones, and twice a fix that measured well in
aggregate was deleting genuine findings. Three counting traps that have each cost real time here:
a removal is the **set difference between the two versions' hits**, not "everything the new
version does not flag"; **de-duplicating hits into a set will lie to you**, because identical
detail strings collapse and an 8-occurrence change can read as 380 — count occurrences, not set
members; and a **one-character placeholder reads as an initial**, so substituting a link or inline
maths with `"X"` makes the following full stop look like an abbreviation and stops sentence
detection.

**Read [`tools/VERIFICATION.md`](../../../tools/VERIFICATION.md) before "fixing" anything.** It
records every fix that was made, the eight lexer bugs, a *Known limitations, accepted deliberately*
section, and — just as important — the fixes that were **verified and then rejected** because they
deleted real findings. Those must not be re-proposed. Two current examples, both on
`qe-writing-004`: exempting markdown link labels and quoted titles (60 of 64 removals correct, 4
genuine findings lost), and treating `<capitalised noun> <number>` as a section reference (clean
mechanics, wrong premise — `var_dmd.md` writes the same three headings both ways).

Also check whether the doubt is already an open question before writing it up as new:
[compliance-lecture-style#1](https://github.com/QuantEcon/compliance-lecture-style/issues/1) covers
the `{doc}` link form for same-series references under `qe-link-001/002`, and
[#3](https://github.com/QuantEcon/compliance-lecture-style/issues/3) covers the shared
`lecture-dp` / `lecture-python.myst` lectures.

**File the doubt; do not stop the batch to fix the detector.** Adjudicating a doubt is measured
work with its own verification write-up, and it belongs in a separate run — the batch is budgeted
for reading lectures.

---

## Tempo

This skill is designed to be run **repeatedly on a small budget** — by hand between other work,
or on a schedule — and never as a marathon. Its fault tolerance comes from two properties, and
both must be preserved:

- **The queue is recomputed from disk on every run**, so no run inherits another run's state.
- **Overlays are committed as they land**, so a dead session loses at most one batch.

Together those mean the cost of an interrupted session is bounded and small, which is what makes
a 30-agent-hour job tractable at all.

For a **scheduled or otherwise unattended run**: clone the corpus into `.corpus/` (gitignored)
rather than a sibling directory. A path under the working directory needs no permission prompt, so
the run cannot stall waiting for an approval that nobody is there to give. Every tool takes
`--corpus`, so the path costs nothing. **Canary any scheduled run on a budget of 2** — one full
cycle, queue through commit — before trusting it with a larger one.

Re-arm a standing resume only if a session limit is what stopped you. It exists to carry work
across a credit window, not to keep an appointment.
