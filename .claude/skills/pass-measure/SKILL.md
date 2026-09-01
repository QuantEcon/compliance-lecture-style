---
name: pass-measure
description: Run the mechanical half of a lecture style-compliance pass in this ledger — get the corpus at its pinned snapshot, scan it, draft every per-lecture report, derive scores, splice the aggregate tables, run the gate, build the book, and print the review queue. Use when asked to refresh the measurements, re-scan or re-measure the corpus, re-run the checks after changing a rule, update the reports to a newer corpus, or see where a pass stands and what is left to review. Runs the whole corpus in seconds at almost no token cost and makes no judgment calls; the judgment layer is /pass-review and publishing a period is /pass-publish.
---

# Measure a pass

Corpus → scan → draft → score → splice → gate → build → queue. The whole 348-lecture corpus
in seconds at essentially no token cost, with **no judgment calls anywhere in it**: every
number this skill produces is reproducible from a pinned corpus snapshot.

| Layer | What it is | Owner |
|-------|-----------|-------|
| **Evidence** | 41 of 49 rules measured over a pinned commit per series | `tools/qestyle_scan.py` — this skill |
| **Scoring** | overall score + priority bucket, arithmetic from the rubric | `tools/qestyle_draft.py`, `qestyle_score.py` — this skill |
| **Judgment** | the 8 judgment-only rules, Strengths, Actions, `scanner_doubts` | [`pass-review`](../pass-review/SKILL.md) — budgeted and expensive |

Closing a period — re-measuring the *previous* snapshot with current code, the series prose,
the history row, the PR, the deploy — is [`pass-publish`](../pass-publish/SKILL.md).
**This skill stops at a green gate and a clean build.** Pushing to `main` deploys the site.

Two standing rules, both enforced by the gate:

- **Never hand-edit a number.** `lectures/data/*.csv` is the source of every figure; the
  per-lecture reports, the scoreboard, the triage page and the charts are generated from it.
  A count that looks wrong is a detector defect — fix the check and re-run, never the report.
- **Never write inside a marker.** Anything between `<!-- qe:NAME -->` and `<!-- /qe:NAME -->`
  is overwritten by the next `--splice`. Hand-written prose goes outside.

The rubric is [`lectures/spec.md`](../../../lectures/spec.md) §4–§6 and is not restated here.
[`UPDATE.md`](../../../UPDATE.md) stays the reference; this skill is the procedure. **Change
one and check the other.**

---

## 1. Check what already exists

A previous pass may have left the corpus, the venv and hundreds of overlays in place. Redoing
any of it is waste; trusting it without checking is worse.

```bash
ls -d .corpus/*/ 2>/dev/null | wc -l          # 6 = 5 series + action-style-guide
.venv/bin/python -V                           # must be 3.12+
ls reviews/*/*.json 2>/dev/null | wc -l       # overlays already written
.venv/bin/python tools/qestyle_status.py      # coverage, staleness, queue depth
```

`qestyle_status.py` needs `lectures/data/lecture_blobs.csv`, which only exists once a scan has
run under the provenance contract (§4). If it says so, that is a first run, not a fault.

Then confirm the clones are still at the pinned commits — existing numbers mean nothing
otherwise:

```bash
.venv/bin/python - <<'PY'
import json, subprocess
for s, m in json.load(open('lectures/data/snapshot.json'))['snapshot'].items():
    live = subprocess.run(['git', '-C', f'.corpus/{s}', 'rev-parse', 'HEAD'],
                          capture_output=True, text=True).stdout.strip()
    print('OK   ' if live == m['commit'] else 'DRIFT', s, m['commit'][:10],
          live[:10] or '(absent)')
PY
```

`DRIFT` is not automatically wrong — advancing the snapshot is the point of a refresh — but
it means every existing report header now disagrees with the corpus, so the full sequence
below has to run, not a subset.

## 2. Get the corpus, into `.corpus/`

**Clone inside the working directory.** A path under the repo needs no permission prompt, so
an unattended run cannot stall waiting for an approval nobody is there to give — that has
stalled two past runs, and it is the same reason subagents need auto mode ON to read a corpus
living outside the tree. `.corpus/` is already in `.gitignore`. Every tool takes `--corpus`, so
the path costs nothing.

Blobless sparse clones: the pass only ever reads `lectures/*.md`. Measured — 840 KB per
series, 18 MB for all six.

```bash
CORPUS=.corpus; mkdir -p $CORPUS
for r in lecture-python-intro lecture-python-programming lecture-python.myst \
         lecture-python-advanced.myst lecture-dp action-style-guide; do
  [ -d $CORPUS/$r ] && continue
  git clone --depth 1 --filter=blob:none --sparse \
      https://github.com/QuantEcon/$r $CORPUS/$r
  git -C $CORPUS/$r sparse-checkout set --no-cone '/lectures/*.md' \
      '/lectures/_config.yml' '/lectures/_static/*.bib' '/style_checker/rules/*.md'
done
R=$CORPUS/action-style-guide/style_checker/rules      # 8 category files; --rules wants this
```

**The `.bib` is part of the corpus, not an extra.** Any rule that checks a citation against
the bibliography needs `lectures/_static/quant-econ.bib`, and a clone without it resolves
*zero* keys — silently, in both directions: a fail-closed check reports no findings and a
fail-open one reports all of them, and neither says why. The sparse pattern above carries it;
do not trim it out.

If the build environment is missing or older than 3.12 (`quantecon-book-theme==0.15.1` will
not resolve on 3.11):

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements.txt
```

## 3. Pin or verify the snapshot

The snapshot is **observed, not declared**: `qestyle_scan.py` records whatever each clone's
`HEAD` is into `lectures/data/snapshot.json` — and, for the period, into
`lectures/data/snapshot_history.csv` (§4) — and stamps it into every report header. So
decide what you want *before* scanning: whatever the clones are sitting on is what gets
recorded as this period's pins.

**To re-measure the current snapshot** (a rule change, a detector fix, a re-run), put each
series back on its pinned commit. Fetching a single SHA into the depth-1 blobless clone is
enough — no `--unshallow`, no worktrees:

```bash
for s in lecture-python-intro lecture-python-programming lecture-python.myst \
         lecture-python-advanced.myst lecture-dp; do
  SHA=$(.venv/bin/python -c "import json;print(json.load(open('lectures/data/snapshot.json'))['snapshot']['$s']['commit'])")
  git -C .corpus/$s fetch --depth 1 --filter=blob:none origin $SHA
  git -C .corpus/$s checkout --detach FETCH_HEAD
done
```

**To advance the snapshot** (a corpus refresh), take each series to current `HEAD` instead:

```bash
for s in lecture-python-intro lecture-python-programming lecture-python.myst \
         lecture-python-advanced.myst lecture-dp; do
  git -C .corpus/$s fetch --depth 1 --filter=blob:none origin HEAD
  git -C .corpus/$s checkout --detach FETCH_HEAD
done
```

Advancing invalidates every report header at once, and the gate's snapshot check will say so.
That is the intended failure mode, not a problem to work around: re-run steps 4–8.

## 4. Scan

```bash
CORPUS=.corpus; R=$CORPUS/action-style-guide/style_checker/rules; P=YYYY-MM
.venv/bin/python tools/qestyle_scan.py --corpus $CORPUS --out lectures/data --rules $R \
    --period $P --append-history lectures/data/rule_reach_history.csv \
    --evidence $CORPUS/evidence
```

Writes `snapshot.json` (one pinned commit per series, *this period only*), `violations.csv`
(per lecture, per rule, count), `rule_reach.csv` and `series_rule_reach.csv`,
`rule_titles.csv` (from `--rules`), `fig_line_widths.csv`, and **`lecture_blobs.csv`** —
header exactly `series,lecture,blob`, one row per scanned lecture, the git blob SHA of
that lecture's `.md` at the pinned commit. That last file is the provenance side of the
review queue (§9); a lecture whose SHA could not be read is omitted rather than written
blank — an empty blob would compare equal to an unstamped overlay and read as fresh — so a
file short of the lecture count means the scan warned about something.

Three things the scan refuses, all fail-closed: `--period` and `--append-history` are
**required** (a scan without them measured a period and recorded nothing anyone could
re-measure against); a series whose checkout cannot be resolved to a commit **stops the
scan** instead of writing an empty pin into every report header; and the only way past the
second is `--unpinned`, for a directory that is deliberately not a checkout — a candidate
extracted with `git archive` — which measures and writes no pin and no blob table.

`--evidence` dumps per-lecture JSON (counts, line numbers, sample matches) for reviewers to
read. Keep it under `.corpus/` for the same permission reason as the corpus itself —
`UPDATE.md` still writes `/tmp/evidence`, which is fine only when someone is present to
approve the reads.

**`--append-history` writes two files, and is no longer optional in practice.** Beside this
period's per-rule reach at the path you give it, it writes `snapshot_history.csv` into the
same directory — header exactly `period,series,basis,commit,committed,lectures,checker`, one
row per series per period: the corpus commit, its full committer instant (`git %cI`, not a
date — day resolution cannot tell two same-day commits apart, and that ambiguity is what
produced [#13](https://github.com/QuantEcon/compliance-lecture-style/issues/13)), the lecture
count, and a digest of `qestyle_scan.py` + `qestyle_lex.py` + `qestyle_rules.py` identifying
the code that measured the period. `snapshot.json` is overwritten every pass and holds the
current period alone; this file is the cross-period record, and it is what
[`pass-publish`](../pass-publish/SKILL.md) Step 1 reads to reconstruct a previous snapshot.
Beside it, `lectures/data/blobs/$P.csv` — `lecture_blobs.csv` filed by period, so the churn
between any two periods is a diff of two of these and never a reconstruction; the gate holds
the newest one byte-identical to `lecture_blobs.csv` and every one to its period's pins.

Both writes live inside the `--append-history` block, so **a scan run without the flag
records no pins for the period at all** — it measures, and leaves nothing anyone can
re-measure against — and leaves the previous run's reach rows in place under this period's
label. Always pass it; the gate fails when the newest period's `rule_reach_history.csv` rows
are not what `rule_reach.csv` says now
([#21](https://github.com/QuantEcon/compliance-lecture-style/issues/21)). Both are
idempotent: they replace the rows for `$P` rather than adding a second set, so re-running
inside a period rewrites it.

**`--append-history` only re-measures *this* period.** If you changed a detector, the
previous period's rows in `rule_reach_history.csv` were produced by the old code, so the
trend now compares two different rulers and reads a detector fix as a corpus improvement.
The `checker` column is what stops that being silent, and the gate enforces it: **every** row
in `snapshot_history.csv` must carry the digest of the three scanner files as they are in
this tree, so touching any of them turns `qestyle_check.py` red on every period recorded
until each has been re-measured with the new code. Measured: appending a single comment line
to `qestyle_lex.py` failed all 10 rows. The scan above fixes this period's rows; the earlier
periods are [`pass-publish`](../pass-publish/SKILL.md) Step 1's job, and until that runs, the
gate stays red and the trend is not quotable.

## 5. Draft every per-lecture report

```bash
.venv/bin/python tools/qestyle_draft.py --corpus $CORPUS --out lectures --date YYYY-MM-DD \
    --rules $R --reviews reviews --judgment-csv lectures/data/judgment.csv
```

**`--reviews reviews` is load-bearing.** It folds the existing overlays back into the reports.
Omit it and you silently discard every review ever written — the files survive on disk, but
the 348 reports come out with no judgment section and the whole expensive layer vanishes from
the published book. `--judgment-csv` writes the merged reviewer findings to
`lectures/data/judgment.csv`.

**`qestyle_draft.py` only writes; it never deletes.** A lecture removed upstream keeps its
report forever, and the gate's coverage check fails on it. Retire them explicitly:

```bash
.venv/bin/python - <<'PY'
import os, glob
for s in os.listdir('lectures'):
    if not s.startswith('lecture-'):
        continue
    have = {f[:-3] for f in os.listdir(f'.corpus/{s}/lectures') if f.endswith('.md')}
    for p in glob.glob(f'lectures/{s}/*.md'):
        stem = os.path.basename(p)[:-3]
        if stem != 'index' and stem not in have:
            os.remove(p); print('retired', p)
PY
```

If a lecture is gone for good rather than renamed, delete its `reviews/<series>/<stem>.json`
too. Nothing checks for an orphan overlay, so it will sit in the coverage count indefinitely.

## 6. Score, splice, TOC

```bash
.venv/bin/python tools/qestyle_score.py --root lectures --fix --csv lectures/data/scores.csv
# The same reports drafted WITHOUT --reviews, into a throwaway root, scored beside them:
# the evidence layer alone, which is the only score comparable across periods.
MECH=.corpus/.mechanical; rm -rf $MECH; mkdir -p $MECH
.venv/bin/python tools/qestyle_draft.py --corpus $CORPUS --out $MECH --date YYYY-MM-DD --rules $R
.venv/bin/python tools/qestyle_score.py --root $MECH --fix --csv lectures/data/scores_mechanical.csv
.venv/bin/python tools/qestyle_report.py --summarise --history $P --splice
.venv/bin/python tools/qestyle_toc.py --root lectures --check || \
  .venv/bin/python tools/qestyle_toc.py --root lectures
```

The second draft is the evidence layer alone. `--history $P` writes this period's row into
`history.csv` **with a `reviewed` column** (lectures whose score folds in an overlay) and
its like-for-like twin into `history_mechanical.csv`, and exits if `scores_mechanical.csv`
is missing. A lecture assessed against more rules scores lower, so a score row is only a
trend against another with the same `reviewed`; the mechanical twin always is
([#16](https://github.com/QuantEcon/compliance-lecture-style/issues/16)). The gate holds
both files to the current `scores*.csv` and to each other.

`--fix` recomputes each report's overall score and priority bucket from its own score table,
so a header can never contradict its categories. `--splice` regenerates the marked table
regions in `README.md`, `lectures/intro.md`, `lectures/details.md`, `lectures/spec.md` and
each series `index.md`; the marker inventory is in `UPDATE.md` § Step 5. `--history $P`
replaces this period's rows in `history.csv`, which is what `charts.md` plots — rewriting the
current period, not closing it (§4). The TOC only needs regenerating when lectures were added
or removed, which is what `--check` tells you.

`charts.md` needs no step at all: it reads `lectures/data/*.csv` at build time.

**Prose outside the markers does not follow the numbers.** A rule fix moves reach and leaves
every sentence quoting it untouched. The gate covers the tables and the trend sentence's
tallies; it cannot check a figure written into an ordinary sentence, so re-read the narrative
claims in `intro.md`, `details.md` and `README.md` yourself after anything moves.

## 7. Gate

```bash
.venv/bin/python tools/qestyle_check.py --root lectures --data lectures/data --corpus $CORPUS
```

**It must print `All checks passed`.** Nothing goes any further until it does. It asserts
coverage both ways, score arithmetic, priority buckets, report↔CSV agreement (i.e. that nobody
edited a measured count), the naming conventions, the **(proposed)** tag on the seven
unregistered rules, snapshot pinning, and the hand-written narrative figures — the `intro.md`
trend row, any counts table headed *Lectures* / *Occurrences*, and the trend sentence's own
tallies. At the 2026-08 pass that was 2,376 cited counts, 22 hand-written corpus claims and 31
line-width claims cross-checked. It exits non-zero on any failure and names the file.

It also fails on a **missing input** rather than skipping the check — every file under `--data`
is committed, so its absence is a broken tree, not a context where the check does not apply
([#15](https://github.com/QuantEcon/compliance-lecture-style/issues/15)). `--corpus` is
required and a series missing under it fails; the one deliberate skip is `--no-corpus`, for a
tree whose corpus genuinely is not present, and it prints `SKIPPED …` beside the verdict so it
cannot be read as a pass.

## 8. Build

The book is vanilla jupyter-book + `quantecon-book-theme`, not the QuantEcon build container.
`lectures/_build/` is gitignored, so building in place is safe:

```bash
.venv/bin/jupyter-book build lectures 2>&1 | tee /tmp/qe-build.log | tail -20
grep -c WARNING /tmp/qe-build.log                    # 0 — grep exits 1 on no match, as wanted
ls lectures/_build/jupyter_execute/*.png | wc -l     # 5 charts
```

**The build is at 0 warnings and must stay there.** A new warning *class* is a regression and
so is a jump in the *count* — this build was at 478 before `escape_roles()` in
`qestyle_draft.py` started rendering MyST roles in reviewer prose literally, so a climb that
tracks review coverage is that function failing. Its two failure modes (a role name outside the
allowlist, an unbounded target running away across a stray backtick) are written up in
[`tools/VERIFICATION.md`](../../../tools/VERIFICATION.md). Add `--path-output /tmp/bk` if you
want the output out of the tree; the PNG path moves with it.

## 9. Print the review queue

```bash
.venv/bin/python tools/qestyle_status.py                 # coverage and staleness
.venv/bin/python tools/qestyle_status.py --queue 10      # the next N lectures to review
```

`qestyle_status.py` joins `lectures/data/lecture_blobs.csv` against each overlay's
`source.blob` and classifies every lecture as **fresh** (blobs equal), **stale** (the lecture
was edited after it was judged), **missing** (no overlay), **unstamped** (an overlay with no
`source` key — never counted as fresh, because nothing records which text it judged) or
**unknown** (stamped, but the lecture has no row in `lecture_blobs.csv`). It is a report, not a
gate: read-only, and it always exits 0. Hand the queue to
[`pass-review`](../pass-review/SKILL.md); this skill does not review anything.

It also prints the **recorded pins**: one row per period from `snapshot_history.csv`, with
abbreviated commits, the `basis` and the `checker` digest — the quickest way to see whether
an earlier period is still comparable with this one.

And it prints the **open reviewer doubts**, grouped by series. Read those before touching
`tools/qestyle_rules.py` — around thirty verified detector and lexer fixes have come from
reviewer doubts and none from any other source.

Never hand-maintain a queue file. A previous pass committed one and it went stale repeatedly.
The queue is derived state, like the numbers.

**Provenance backfill.** After any pass whose overlays were written before the `source` key
existed, stamp them:

```bash
.venv/bin/python tools/qestyle_backfill_provenance.py --reviews reviews \
    --data lectures/data --dry-run
.venv/bin/python tools/qestyle_backfill_provenance.py --reviews reviews --data lectures/data
```

It stamps only overlays that have no `source` (`--force` restamps, and should be needed
approximately never). **Run it before advancing the snapshot, not after.** It asserts that the
overlay judged the currently pinned blob; run it against a newer corpus and it launders stale
reviews into fresh ones, which is the one wrong answer the whole scheme exists to prevent.

## 10. Stop

Green gate, clean build, queue printed. Commit, and stop.

**Pushing to `main` deploys the site** — that is [`pass-publish`](../pass-publish/SKILL.md)'s
decision, made once a period is actually closed, not a side effect of a measurement refresh.
Work on a branch and leave it there.

---

## If you changed a rule check

The cheap loop. No review work is lost — overlays are deliberately decoupled from the counts:

```bash
.venv/bin/python tools/qestyle_scan.py --corpus $CORPUS --out lectures/data --rules $R \
    --period $P --append-history lectures/data/rule_reach_history.csv
.venv/bin/python tools/qestyle_draft.py --corpus $CORPUS --out lectures --date YYYY-MM-DD \
    --rules $R --reviews reviews --judgment-csv lectures/data/judgment.csv
.venv/bin/python tools/qestyle_score.py --root lectures --fix --csv lectures/data/scores.csv
.venv/bin/python tools/qestyle_report.py --summarise --history $P --splice
.venv/bin/python tools/qestyle_check.py --root lectures --data lectures/data --corpus $CORPUS
```

Then re-read every sentence quoting a number that moved (§6), and remember that the previous
period's history rows are still measured with the old code (§4).

### Before trusting a new or changed check

Sample it adversarially. **This is where the real defects are, not in the regex** — 19 of the
41 checks needed fixing when first sampled, and `qe-fig-008` had **149 false positives in 15
sampled hits**; shipping it would have told authors to add `lw=2` to plots that already had it.

```bash
cd tools && ../.venv/bin/python - <<'PY'
import sys, glob; sys.path.insert(0, '.')
from qestyle_lex import lex
from qestyle_rules import CHECKS
rule = 'qe-fig-003'
for f in glob.glob('../.corpus/lecture-python.myst/lectures/*.md'):
    for h in CHECKS[rule](lex(f, 'lecture-python.myst')):
        print(f'{f}:{h.line}: {h.detail}')
PY
```

Open **at least ten hits in the source** and judge them against the canonical rule text. If
total reach is small, read every hit rather than sampling. Then record the outcome in
[`tools/VERIFICATION.md`](../../../tools/VERIFICATION.md) — **including a check that needed
nothing**, so the table is a record of what was verified and not a list of only the broken ones.

Read `VERIFICATION.md` before "fixing" anything. It carries the eight lexer bugs, a *Known
limitations, accepted deliberately* section, and the fixes that were verified and then
**rejected** for deleting real findings. Do not re-propose those.

### Measurement traps that have actually cost time

- **Most wrong counts are structural, not regex errors.** Before blaming a pattern, check how
  `qestyle_lex.py` typed the region. Past bugs: `{math}` directive bodies typed as code (1,783
  blocks); display maths closed at the end of a content line (`… p}$$`); blockquoted `> $$`;
  inline maths spanning a line break; a gated `{exercise-start}` treated as a container; HTML
  comments scanned. Two lexer invariants keep breaking and are worth knowing: `_strip_py` must
  preserve line structure (collapsing a docstring joins the lines around it and pulls indented
  code to column zero, so an indented `plt.show()` reads as top-level), and masking must use
  NUL rather than spaces (spaces fabricate the double-space `qe-writing-008` fires on).
- **Judge every fix in both directions.** Removing false positives is worthless if it removes
  true positives too. Keep a canary list of known-real findings that must survive — twice, a
  fix that measured well in aggregate was deleting genuine ones.
- **A removal is the set difference between the two versions' hits**, not "everything the new
  version does not flag". A query built the wrong way reported 256 lost `qe-fig-008` findings;
  every one carried `lw=` and had never been a hit under either version.
- **De-duplicating hits into a set will lie to you.** Identical detail strings collapse, and an
  8-occurrence change reads as 380. Count occurrences, not set members.
- **A one-character placeholder reads as an initial.** Substituting a link or inline maths with
  `"X"` makes the following full stop look like it follows an initial, and sentence detection
  stops. This has bitten twice, in `_count_sentences` and in `check_fig_004`; both sites carry
  the lesson in a comment.
- Two about regexes: an optional-brace pattern like `\{?…\}?` lets the engine backtrack past
  your guard — use an explicit alternation; and a lookahead placed after an *optional* group is
  defeated the same way, so check the text after the match instead (`tag_proposed` does).

### Other traps in the pipeline

- **`lecture-dp` syncs lectures from `lecture-python.myst`** (`cross_product_trick`,
  `ifp_advanced`, `inventory_q`, `rs_inventory_q`, …), so their findings appear twice in the
  corpus totals. Fix upstream; a fix applied in `lecture-dp` is overwritten by the next sync.
  How the shared copies should be *counted* is open as
  [compliance-lecture-style#3](https://github.com/QuantEcon/compliance-lecture-style/issues/3).
- **`qestyle_check` skips `lectures/_build`** — it used to scan its own build output and fail.
  Any new check that walks markdown must skip that directory too.
- **The lecture count changes between passes** (299 in 2026-05, 348 in 2026-08). Never write a
  corpus count from memory; the scan reports it and the gate checks it.
- **`contributions/issues/*.md` mirror live `action-style-guide` issues.** Editing one here does
  not update GitHub, and that repo is usually outside the session's access — say so rather than
  implying a re-sync happened.
