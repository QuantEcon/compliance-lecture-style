# UPDATE.md — how to run a pass and refresh the ledger

This is the reference runbook for running a pass and updating every document in this
repo. Pair it with [`ROADMAP.md`](ROADMAP.md) (direction and open decisions) and the
[scoring spec](lectures/spec.md) (the rubric, the pass methodology, and the measured
deterministic coverage).

---

## Source of truth

**This git repository is the single source of truth for the ledger.** The published
site at <https://quantecon.github.io/compliance-lecture-style/> is built from
`lectures/` by `.github/workflows/deploy.yml` on every push to `main`.

**This repo is a standing record, not an audit.** An audit is an event: it happens
once, publishes, and freezes. A ledger is re-measured in place, pass after pass —
`lectures/data/history.csv` already holds 2026-05 and 2026-08, and the next period
becomes another row rather than a new document. The word *audit* stays right for an
individual pass and for the May-2026 event; it is wrong as a description of this
repository. The repository type `compliance-{domain}` is registered in
[QEP-3](https://github.com/QuantEcon/qeps/pull/7), which is still an **open PR** — cite
it as proposed, not as settled policy.

The May-2026 audit this ledger was seeded from keeps its own name, its published site at
<https://quantecon.github.io/audit.2026-05.style-guide/> and its issues, all of which
stay readable after that repo is archived. Links in this file that still point there
point at that frozen event on purpose.

Within the repo, the ordering is: `lectures/data/*.csv` is the source of the numbers,
per-lecture reports are the source of the scores, and the aggregate pages
(`intro.md`, `details.md`, `charts.md`, `README.md`) are **generated from those** —
never edited by hand in their table regions. Section [§ Step 5](#step-5--derive-scores-and-splice-the-aggregates)
explains how.

---

## A new period runs in place

- **Correcting or refreshing the current period** → run the pass below and push.
- **A new period** → run the same pass, in this same repo. Running in place is what makes
  this a ledger rather than a shelf of dated reports: the period *joins* the record — a row
  in `lectures/data/history.csv` and in `lectures/data/rule_reach_history.csv`, which is
  what the trend chart plots — instead of replacing the period before it. Nothing is
  renamed, re-issued or version-numbered per period.
- **A genuinely episodic audit** — a different subject, examined once, with no cadence
  behind it — still wants its own dated repo, which freezes when it publishes.
  [§ Standing up a separate audit](#standing-up-a-separate-audit) is that recipe.

The audits absorbed into this ledger are not renamed either: under QEP-3 a rename fixes a
name, it never transmutes a type. `audit.2026-05.style-guide` keeps its name for life, is
archived once absorbed, and stays citable — see
[#2](https://github.com/QuantEcon/audit.2026-05.style-guide/issues/2) for the decision and
`ROADMAP.md` for the reasoning.

---

## Inputs

| Input | Where | Role |
|-------|-------|------|
| The 5 lecture series | cloned into the working tree as `.corpus/<series>/lectures/*.md` | The lectures being measured |
| Canonical rules | `.corpus/action-style-guide/style_checker/rules/*.md` (8 category files) | Rule definitions — **never redefined here**, only consumed |
| Scoring spec | `lectures/spec.md` | Rubric, severity tiers, pass methodology, report templates |
| Review overlays | `reviews/<series>/<stem>.json` | The judgment layer from previous passes, folded back into every report |
| The tools | `tools/qestyle_*.py` | The evidence, scoring, reporting and status layers |

JAX rules are **out of scope** for this corpus (they target `lecture-jax`).

### Getting the corpus

Blobless sparse clones keep this to a few megabytes per series — a pass only ever reads
`lectures/*.md`. Clone **into the working tree**, at `.corpus/` (already gitignored):
a path under the repo needs no permission prompt, so an unattended run cannot stall
waiting for an approval nobody is there to give. Every tool takes `--corpus`, so the
location costs nothing.

```bash
CORPUS=.corpus; mkdir -p $CORPUS
for r in lecture-python-intro lecture-python-programming lecture-python.myst \
         lecture-python-advanced.myst lecture-dp action-style-guide; do
  [ -d $CORPUS/$r ] && continue
  git clone --depth 1 --filter=blob:none --sparse \
      https://github.com/QuantEcon/$r $CORPUS/$r
  git -C $CORPUS/$r sparse-checkout set --no-cone '/lectures/*.md' '/lectures/_config.yml' \
      '/lectures/_static/*.bib' '/style_checker/rules/*.md'
done
R=$CORPUS/action-style-guide/style_checker/rules      # the 8 category files; --rules wants this
```

The snapshot is **observed, not declared** — `qestyle_scan.py` records whatever each
clone's `HEAD` is — so put each series where you want it before scanning. To re-measure
the pinned snapshot, fetch the recorded SHA into the shallow clone and detach onto it; to
advance the snapshot, fetch `HEAD` instead. Both recipes are in
[`pass-measure`](.claude/skills/pass-measure/SKILL.md) § 3.

To re-measure a **past** snapshot (which is how the trend chart gets its earlier point),
add history and check the date out into a worktree — once per series `$r`, kept under the
gitignored `.corpus/` so the working tree stays clean:

```bash
PREV=.corpus/.prev-YYYY-MM; mkdir -p $PREV
# Skip the fetch when the clone is already complete, but let a genuine fetch
# failure stop the script: `&& … || true` would swallow it and leave you
# reconstructing a period from a clone missing the commit you need.
if [ "$(git -C $CORPUS/$r rev-parse --is-shallow-repository)" = true ]; then
  git -C $CORPUS/$r fetch --unshallow --filter=blob:none
fi
# The pins are recorded: lectures/data/snapshot_history.csv, header
#   period,series,basis,commit,committed,lectures,checker
# one row per series per period. Read the SHA from there — never reconstruct it
# from a date. `--until=YYYY-MM-DD` fills the unspecified time-of-day from the
# wall clock at the moment you run it, so a bare date resolves to a different
# commit depending on the hour: two runs 26 minutes apart returned cutoffs
# 1,584 seconds apart. The `committed` column is a full instant with an offset
# for exactly that reason.
#
# And for a period with no recorded pin, a date cutoff GENERATES A CANDIDATE —
# it never establishes a pin, even in the deterministic form
# `--until='YYYY-MM-DD 23:59:59 +1000'`. Two deterministic cutoffs gave 298 and
# 301 lectures; a third matched all five per-series counts AND the 300 total and
# was still wrong on two series. A candidate becomes a pin only when re-measuring
# it reproduces that period's rows in `rule_reach_history.csv` — all 35 rules,
# both columns. Nothing weaker discriminates. That is what `basis=recovered`
# records, and an unverifiable pin is not written at all.
SHA=$(awk -F, -v p=YYYY-MM -v s=$r '$1==p && $2==s {print $4}' \
        lectures/data/snapshot_history.csv)
# Stop, do not fall through: `worktree add` with an empty SHA succeeds and checks
# out the clone's CURRENT head, giving you today's corpus wearing a past period's
# label. This snippet has no `set -e`, so the braces-and-exit form is required.
[ -n "$SHA" ] || { echo "no recorded pin for that period — recover one, never guess"; exit 1; }
git -C $CORPUS/$r worktree add --no-checkout "$PWD/$PREV/$r" $SHA
git -C $PREV/$r sparse-checkout set --no-cone '/lectures/*.md' '/lectures/_static/*.bib'
git -C $PREV/$r checkout
```

`worktree add` resolves a relative path against the *clone*, not against this repo, so
the absolute `$PWD/…` is load-bearing. Scan a reconstructed period into a **throwaway
`--out`** — `--out lectures/data` would overwrite the current period's numbers with the
old snapshot's.

`snapshot_history.csv` holds only pins that are known good: `basis` is `pinned` (recorded
by the scan at the time it measured the period) or `recovered` (established afterwards and
verified against that period's recorded rule reach). There is deliberately no third value
for a guess, so a **missing row means the period has no verified pin** — recover one and
verify it against `rule_reach_history.csv` — [`pass-publish`](.claude/skills/pass-publish/SKILL.md)
Step 1 — rather than falling back to a date.

---

## The process

The pass has three layers — evidence (code), scoring (arithmetic), review (judgment).
[Spec §8](lectures/spec.md) explains why they are separate; this section is the
mechanics.

> **Working with an agent?** The same process ships as three invokable skills, split along
> the one seam that matters — the mechanical layers run the whole corpus in seconds at
> essentially no token cost, while the judgment layer costs about **five agent-minutes per
> lecture**, roughly 30 agent-hours for all 348. No session holds that, so it is budgeted
> separately.
>
> | Skill | Cost | What it does |
> |-------|------|--------------|
> | [`/pass-measure`](.claude/skills/pass-measure/SKILL.md) | seconds | corpus, scan, draft, score, splice, gate, build, and print the review queue — Steps 1–2 and 5–8, stopping short of the deploy |
> | [`/pass-review`](.claude/skills/pass-review/SKILL.md) | ~5 agent-min per lecture | the judgment layer, incremental and resumable, with a hard budget — Step 3 |
> | [`/pass-publish`](.claude/skills/pass-publish/SKILL.md) | minutes | close a period: re-measure the previous snapshot with current code, write the series prose, append the history row, gate, build, PR, deploy, tag the pass — Step 4 and the closing half of Step 8 |
>
> Each carries the environment checks and the known traps. **This file stays the reference;
> the skills are the procedure. Change one, check the other.**

> **The `.bib` is part of the corpus, not an extra.** Any rule that checks a citation against
> the bibliography — an in-text author-year against the entry's own `year`, say — needs
> `_static/quant-econ.bib`, and a clone without it resolves *zero* keys. That fails silently in
> both directions: a fail-closed check reports no findings and a fail-open one reports all of
> them, and neither says why. It is carried for **both** snapshots, because a rule that reads
> the bib must read it in the previous period too or the trend row is meaningless. The cost is
> one file per series.

### Step 1 — Measure the corpus

```bash
.venv/bin/python tools/qestyle_scan.py --corpus $CORPUS --out lectures/data --rules $R \
    --period YYYY-MM --append-history lectures/data/rule_reach_history.csv \
    --evidence $CORPUS/evidence
```

This pins one commit per series into `lectures/data/snapshot.json`, writes
per-lecture per-rule counts to `violations.csv`, corpus and per-series reach to
`rule_reach.csv` / `series_rule_reach.csv`, rule titles to `rule_titles.csv`, the
spread of explicit `plot()` line widths to `fig_line_widths.csv`, one blob SHA per
lecture to `lecture_blobs.csv` (the provenance side of the review queue — see Step 3),
and appends this pass to `rule_reach_history.csv` — plus this period's pins, one row per
series, to `lectures/data/snapshot_history.csv` beside it: commit, full committer instant,
lecture count, and the digest of the code that measured them. `--evidence` dumps
per-lecture JSON (counts, line numbers, sample matches) for the review layer to read;
keep it under
`.corpus/` for the same permission reason as the corpus itself.

`--append-history` is idempotent — it replaces this period's rows rather than adding a
second set, in both files it writes — but it only ever measures *this* period. If a
detector changed, the previous period's rows were produced by the old code and the trend
is comparing two rulers — a
detector fix then reads as a corpus improvement. Re-measuring the previous snapshot with
current code (§ Getting the corpus, and [`pass-publish`](.claude/skills/pass-publish/SKILL.md)
Step 1) is what fixes that; until it has run, do not quote the trend.

> **`--append-history` is not optional in practice.** Both cross-period files are written
> from inside its block, so a scan run without it measures the period and records no pins
> for it — which is the gap that produced
> [#13](https://github.com/QuantEcon/compliance-lecture-style/issues/13). All four scan
> invocations in this file and in the skills pass it; keep it that way.

> The lecture count changes between periods — `history.csv` records 300 for 2026-05 and
> 348 for 2026-08. Never bring a count across from the previous period or write one from
> memory; the scan measures it and the gate checks it.

### Step 2 — Draft every per-lecture report

```bash
.venv/bin/python tools/qestyle_draft.py --corpus $CORPUS --out lectures --date YYYY-MM-DD \
    --rules $R --reviews reviews --judgment-csv lectures/data/judgment.csv
```

One report per lecture at `lectures/<series>/<stem>.md`, following the
[spec §6](lectures/spec.md) template: header with the pinned snapshot, score table,
severity-bucketed issue list with line numbers.

**`--reviews reviews` is load-bearing.** It folds the existing overlays back into the
reports. Omit it and the whole judgment layer silently vanishes from the published book —
the overlay files survive on disk, but the reports come out without them.
`--judgment-csv` writes the merged reviewer findings to `lectures/data/judgment.csv`.

The drafter only ever writes; it never deletes. A lecture removed upstream keeps its
report, and the Step 6 coverage check fails on it — retire those reports (and their
overlays, if the lecture is gone rather than renamed) by hand.

### Step 3 — Review pass

Reviewers add what the scanner cannot measure: the 6 judgment-only registry rules and 2
judgment-only proposed rules (spec §9), plus per-lecture **Strengths** and **Recommended
actions**, written to `reviews/<series>/<stem>.json`. Reviewer instructions are
[spec §8.3](lectures/spec.md).

**Take the queue from the tool, never from a file.**

```bash
.venv/bin/python tools/qestyle_status.py                 # coverage, staleness, open doubts
.venv/bin/python tools/qestyle_status.py --queue 10      # just the next N as <series>/<stem>
```

`qestyle_status.py` is read-only and always exits 0 — a report, not a gate. `--data` and
`--reviews` override the two roots; `--json` gives the same content machine-readably.

**Every overlay records the text it judged.** It carries an optional
`"source": {"commit": "<series snapshot commit>", "blob": "<blob sha>"}`, and
`qestyle_status.py` joins that against `lectures/data/lecture_blobs.csv` from Step 1 to
class each lecture **fresh** (blobs equal), **stale** (edited since it was judged),
**missing** (no overlay), **unstamped** (an overlay with no `source`, never counted as
fresh) or **unknown** (stamped, but no current blob on record).

That join is the whole reason a refresh is affordable. Without a `source` key an overlay
records a judgment but not the text it judged, so the only queue anyone can compute is
"lectures with no overlay at all" — and every corpus refresh re-reviews the whole corpus,
348 lectures at ~5 agent-minutes each, about 30 agent-hours. With it the queue is
"missing **or stale**", and review cost scales with corpus *churn* rather than corpus
*size*. Measured over 2026-05 → 2026-08: 186 of the 348 lectures were byte-identical, 114 had
been edited and 48 were new, so the queue would have been 162 of 348 — about 13.5 agent-hours of
review against 29. A 53 % saving, and it scales with cadence: three months touches half the
corpus, a month far less, so the first pass after a long gap should be budgeted as close to a
full one. (The 2026-05 baseline these are measured against is `recovered` rather than recorded at
the time; it is in `lectures/data/snapshot_history.csv`, and how it was established is in
[`tools/VERIFICATION.md`](tools/VERIFICATION.md) § How the 2026-05 pins were recovered.)

Overlays written before the `source` key existed are stamped in bulk:

```bash
.venv/bin/python tools/qestyle_backfill_provenance.py --reviews reviews \
    --data lectures/data --dry-run
.venv/bin/python tools/qestyle_backfill_provenance.py --reviews reviews --data lectures/data
```

It stamps only overlays with no `source` (`--force` restamps, and should be needed
approximately never). **Run it before advancing the snapshot, not after** — it asserts
that the overlay judged the currently pinned blob, so against a newer corpus it launders
stale reviews into fresh ones, which is the one wrong answer the scheme exists to prevent.

> 🔑 **Sandbox gotcha:** subagents can only read outside the working directory when
> **auto mode is ON**. With auto mode off every read of the corpus is denied and the
> run stalls. This bit the original pass, and is the second reason the corpus lives at
> `.corpus/` inside the tree.

Reviewers must **not** edit a mechanical count. If one looks wrong it is a scanner
defect: fix `tools/qestyle_rules.py`, re-run Steps 1–2, and note it. Otherwise the
reports stop matching the CSVs and Step 6 will catch it. A reviewer's recorded
`scanner_doubts` are where those defects surface — `qestyle_status.py` prints the open
ones, and they should be read before anything in `tools/qestyle_rules.py` is changed.

### Step 4 — Write the series summaries

One `lectures/<series>/index.md` per series, H1 `# Summary`, following the
[spec §7](lectures/spec.md) template. Its five tables — meta, priority distribution,
systemic rules, clean lectures, ranked lectures — are spliced from
`lectures/data/scores.csv` in Step 5, so write the prose first and let the numbers land.

Two regions in each series index, `<!-- qe:series-narrative -->` and
`<!-- qe:series-recommendations -->`, use marker syntax but are **not** regenerated: they
are hand-written, per period, from the data. They are also the ledger's one blind spot —
`qestyle_check.py` strips every `<!-- qe:… -->` region before it looks for hand-written
claims, on the assumption that a marked region is generated, so a reach figure inside
these two is checked by nothing. Verify those figures against
`lectures/data/series_rule_reach.csv` by hand.

### Step 5 — Derive scores and splice the aggregates

```bash
.venv/bin/python tools/qestyle_score.py --root lectures --fix --csv lectures/data/scores.csv
.venv/bin/python tools/qestyle_report.py --summarise --history YYYY-MM --splice
```

`qestyle_score.py --fix` recomputes each report's overall score and priority bucket
from its own score table, so a header can never contradict its categories.
`qestyle_report.py --splice` regenerates the marked table regions in `README.md`,
`lectures/intro.md`, `lectures/details.md`, `lectures/spec.md` and each series
`index.md`. Run `qestyle_score.py` first: `--history` reads `scores.csv`, so the other
order records the previous run's arithmetic under this period's label.

| Marker | What it generates |
|--------|-------------------|
| `<!-- qe:readme-scoreboard -->` | README landing scoreboard |
| `<!-- qe:focus -->` | intro.md "where to focus" table |
| `<!-- qe:wins -->` | intro.md highest-reach fixes |
| `<!-- qe:full-scoreboard -->` | details.md full scoreboard |
| `<!-- qe:systemic -->` | details.md every recurring rule, ranked |
| `<!-- qe:high-list -->` | details.md every HIGH-priority lecture |
| `<!-- qe:snapshot -->` | details.md pinned-snapshot table |
| `<!-- qe:review-coverage -->` | intro.md coverage caveat — how far the judgment layer has reached, and what reviewed and unreviewed lectures actually average. Generated because it moves with every overlay that lands: the admonition emits **its own fence**, because whether the caveat is a `warning` or a `note` is itself a fact about coverage. Write no coverage-dependent prose beside it. |
| `<!-- qe:series-meta -->`, `-priority`, `-systemic`, `-clean`, `-ranked` | the five generated tables in each series `index.md` |
| `<!-- qe:scoreboard -->` | the non-README scoreboard variant; defined, currently placed nowhere |

`<!-- qe:series-narrative -->` and `<!-- qe:series-recommendations -->` are **not** in
that set — they look like markers but are hand-written (Step 4).

**Prose outside the markers is hand-written** — rewrite it to match the new numbers, and
re-read it after any rule change: a detector fix moves reach and leaves every sentence
quoting it untouched. Never edit inside a generated marker; the next `--splice`
overwrites it.

`charts.md` needs no step: it reads `lectures/data/*.csv` at build time.

### Step 6 — Check consistency

```bash
.venv/bin/python tools/qestyle_check.py --root lectures --data lectures/data --corpus $CORPUS
```

It must print `All checks passed`; nothing goes further until it does. `--corpus` is
required, and a series missing under it is a failure — the only way to run without the
corpus is the explicit `--no-corpus`, which prints a `SKIPPED` line beside the verdict.
Every other input is committed, so a missing file under `--data` fails rather than skips
(that used to be a note, and deleting `lectures/data/` gave a green gate —
[#15](https://github.com/QuantEcon/compliance-lecture-style/issues/15)). At the 2026-08
pass this cross-checked 2,376 cited counts, 22 hand-written corpus claims and 31 line-width
claims. See [§ Consistency checks](#consistency-checks).

### Step 7 — Regenerate the TOC (only if lectures were added or removed)

```bash
.venv/bin/python tools/qestyle_toc.py --root lectures --check || \
  .venv/bin/python tools/qestyle_toc.py --root lectures
```

`--check` reports whether the TOC is already correct, which is the answer most passes get.

### Step 8 — Build, and close the period

```bash
.venv/bin/jupyter-book build lectures 2>&1 | tee /tmp/qe-build.log | tail -20
grep -c WARNING /tmp/qe-build.log                 # 0 — grep exits 1 on no match, as wanted
ls lectures/_build/jupyter_execute/*.png | wc -l  # 5 — the charts rendered
```

**The build is at 0 warnings and must stay there.** A new warning *class* is a regression
and so is a jump in the *count*: this build was at 478 before `escape_roles()` in
`qestyle_draft.py` began rendering MyST roles in reviewer prose literally, so a warning
count that tracks review coverage is that function failing. Both of its failure modes are
written up in [`tools/VERIFICATION.md`](tools/VERIFICATION.md). `lectures/_build/` is
gitignored, so building in place is safe.

The build uses **vanilla jupyter-book + `quantecon-book-theme`** (pinned in
`requirements.txt`) — not the QuantEcon build container. It needs **Python 3.12+**
(`quantecon-book-theme` 0.15.1 requires it), and `charts.md` executes at build time, so
`matplotlib`/`numpy` must stay in `requirements.txt`. A venv is already in place at
`.venv/`, which is why every command above is prefixed with `.venv/bin/`; rebuild it with
`uv venv --python 3.12 .venv && uv pip install --python .venv/bin/python -r requirements.txt`.

A measurement refresh stops here: commit on a branch and leave it. **Closing a period is a
separate, deliberate act** — it re-measures the previous snapshot with the current code
(§ Getting the corpus), writes the series narratives (Step 4), appends the history row,
and only then opens the PR. `.github/workflows/deploy.yml` runs on every push to `main`,
so **the merge is the publication** — there is no staging site and no separate release
step.

```bash
gh pr create --repo QuantEcon/compliance-lecture-style --base main \
    --title "Close the <period> period"
# after merge, watch the deploy and then check the published URL, not main:
gh run watch "$(gh run list --repo QuantEcon/compliance-lecture-style \
    --workflow deploy.yml --limit 1 --json databaseId -q '.[0].databaseId')" --exit-status
```

Green means the artifact uploaded, not that a reader's page has moved — verify against
<https://quantecon.github.io/compliance-lecture-style/> with a grep for something this
period actually changed. Once it has, tag the published tree `pass/YYYY-MM`: the pins and
the `checker` digest say what was measured and by which code, and the tag is the O(1) name
for the tree — `tools/`, `reviews/`, `spec.md` — that produced the period. It does not
backfill 2026-05 — no 2026-05-era tree contains `tools/` at all; `pass/2026-08` was applied
after the fact to a verified tree, and its annotation says so.
[`pass-publish`](.claude/skills/pass-publish/SKILL.md) is the full procedure — the tag
command, and the no-closing-keyword rule for the PR body.

---

## Consistency checks

`tools/qestyle_check.py` asserts the things that silently broke in the previous pass:

| Check | What it catches |
|-------|-----------------|
| **Coverage** | A lecture in the corpus with no report, or a report with no lecture. The previous pass missed 2 `lecture-dp` lectures and carried a report for `supply_demand_foundations_v2`, which exists in no repository's history. |
| **Score arithmetic** | A header whose overall score is not the mean of its own in-scope categories (95 of 299 reports in the previous pass). |
| **Priority buckets** | A priority that is not what spec §4 gives for that score and category floor (24 of 299). |
| **Report ↔ CSV agreement** | A per-lecture report citing a count that `violations.csv` does not have — i.e. a reviewer edited a mechanical number. |
| **Conventions** | Legacy `W#`/`M#` or `qe-*-A#` rule IDs; a proposed rule cited without its **(proposed)** tag; a `# Style Audit —` title prefix; a `Spec version` line; two-pass or "carry-forward" narrative. |
| **Snapshot** | Reports whose pinned snapshot does not match `snapshot.json`. |
| **Corpus pins** | A period carrying numbers that nothing pins a corpus for, or a `snapshot_history.csv` row that could not reproduce one: a `basis` outside `pinned`/`recovered`, a commit that is not 40 hex, a `committed` with no UTC offset, per-series lecture counts that do not sum to that period's `history.csv` TOTAL, or a `checker` that is not the digest of `qestyle_scan.py` + `qestyle_lex.py` + `qestyle_rules.py` in this tree — that last one goes red on *every* recorded period the moment a scanner file changes, and stays red until each has been re-measured. Missing file is a failure, not a note. |
| **Line-width claims** | The figures behind the `qe-fig-008` rule-scope question, in `appendix.md` and in `contributions/issues/07-…`, held to `fig_line_widths.csv`. `qe-fig-008` only asks whether a width is set, so the spread of values is separate evidence — and it moves whenever the check's exemptions move. A first hand-typed pass had five of these numbers wrong and this check caught all five. |
| **Narrative claims** | A hand-written figure the data has since moved: the `intro.md` trend row (`A% → B%`), any counts table whose header names *Lectures* and *Occurrences*, and the trend sentence's own tallies (*N rules measurable in both snapshots*, *N improved*, *N held level*, *N got worse*). The report↔CSV check does not reach any of these, and a rule fix moves reach without touching the prose quoting it — which happened twice in the 2026-08 pass before the sentence tallies were covered. |

Run it after any agent pass. It exits non-zero on any failure.

**A missing input is a failure, not a skip.** Each of the data-dependent rows above used to
print `<file> absent, … not checked` and let the run pass, so a scan run without
`--append-history`, followed by the gate, was green and checked nothing about the narrative;
an empty `lectures/data/` was green outright
([#15](https://github.com/QuantEcon/compliance-lecture-style/issues/15)). Now every file under
`--data` is required, `snapshot.json` must pin a commit for all five series (an empty commit is
what the scan writes when a clone did not resolve, and it used to skip the comparison), and a
tree with no per-lecture reports under `--root` fails rather than "checking" zero of them. The
single legitimate skip is the corpus — a past period's clones do not exist — and it is the
explicit `--no-corpus` flag, reported as `SKIPPED` next to the verdict, never inferred from an
empty directory.

---

## Maintaining the contributions & feedback loop

[`contributions/`](contributions/) holds the source behind the four
`action-style-guide` issues
([#18–#21](https://github.com/QuantEcon/action-style-guide/issues/18)) plus 7
ready-to-merge rule drafts. The published [appendix](lectures/appendix.md) is the
reader-facing summary. Keep them consistent.

**Sync rule.** The files in `contributions/issues/` are the issue *bodies*. If you
edit one, re-push it so the record and GitHub agree (mapping: #18←01, #19←02,
#20←03, #21←04):

```bash
gh issue edit <n> --repo QuantEcon/action-style-guide --body-file contributions/issues/<file>.md
```

**When corpus counts change.** The issues and the appendix cite per-rule evidence
counts. Take the new numbers from `lectures/data/rule_reach.csv` — do not re-estimate
them — then update the appendix's proposed-rule table, the affected issue bodies, the
rationale blocks in `contributions/rule-drafts/`, and the lecture count in
`contributions/README.md`. Re-sync the live issues afterwards.

**Lifecycle.** As the team responds:

- *Rule accepted* → per the program direction (coordinated in
  `QuantEcon/project-style-guide`, a private hub), accepted rules are transcribed into
  the consolidated `QuantEcon/style-guide` rule database — the `rule-drafts/` entries
  here are the transcription inputs. Record the outcome in `contributions/README.md`;
  once a rule ships in the registry the checkers consume, drop its **(proposed)** tag
  across the published pages (`grep -rl '(proposed)' lectures`) and move it out of
  `PROPOSED` in `tools/qestyle_rules.py`.
- *Issue resolved/closed* → record the outcome in `contributions/README.md`.

**A new period.** `contributions/` belongs to the period that raised it — don't bring old
issues across blind. Open fresh issues only for gaps the new pass surfaces, and reference
any rules adopted since the previous period.

`action-style-guide` is often outside a session's GitHub access. If `gh issue edit` cannot
run, say so and leave the re-sync as a named open item — never write prose implying the
live issues were updated.

---

## Repository layout

```
compliance-lecture-style/
├── README.md                     repo landing (scoreboard + links)
├── ROADMAP.md                    direction, phases, open decisions
├── UPDATE.md                     this runbook — the reference
├── CLAUDE.md                     read-me-first orientation for agents
├── requirements.txt              build deps (pinned; needs Python 3.12+)
├── .claude/skills/               the procedure, as three invokable skills
│   ├── pass-measure/             scan → draft → score → splice → gate → build → queue
│   ├── pass-review/              the judgment layer, budgeted and resumable
│   └── pass-publish/             close a period and deploy
├── tools/                        the pass pipeline
│   ├── qestyle_lex.py            MyST lexer (regions: text / code / math / directives)
│   ├── qestyle_rules.py          one function per mechanically-checkable rule
│   ├── qestyle_scan.py           evidence layer → lectures/data/*.csv
│   ├── qestyle_draft.py          drafts every per-lecture report
│   ├── qestyle_score.py          derives overall score + priority; writes scores.csv
│   ├── qestyle_report.py         builds and splices the aggregate tables
│   ├── qestyle_check.py          consistency gate (run before pushing)
│   ├── qestyle_status.py         coverage, staleness and the review queue (read-only)
│   ├── qestyle_backfill_provenance.py  stamps unstamped overlays with what they judged
│   ├── qestyle_toc.py            regenerates lectures/_toc.yml
│   └── VERIFICATION.md           how each check was sampled, and what was rejected
├── reviews/<series>/<stem>.json  the judgment overlays — one per lecture, with provenance
├── contributions/                source behind the action-style-guide issues (#18–#21)
├── .github/workflows/deploy.yml  build + deploy to GitHub Pages
└── lectures/                     Jupyter Book source (published)
    ├── _config.yml, _toc.yml, _static/
    ├── data/                     the numbers — everything else is derived from these
    │   ├── snapshot.json         pinned corpus commit per series, this period only
    │   ├── violations.csv        per lecture, per rule, count
    │   ├── lecture_blobs.csv     series,lecture,blob — each lecture's git blob SHA at the
    │   │                         pinned commit; joined against an overlay's source.blob
    │   │                         to decide whether its judgment is still fresh
    │   ├── rule_reach.csv        corpus-wide reach per rule
    │   ├── series_rule_reach.csv per-series reach per rule
    │   ├── rule_titles.csv       rule id → title
    │   ├── fig_line_widths.csv   every explicit plot() lw=, by value and by class
    │   ├── judgment.csv          the merged reviewer findings from reviews/
    │   ├── scores.csv            per-lecture category scores, overall, priority
    │   ├── series_summary.csv    per-series averages + priority counts
    │   ├── history.csv           per-period series scores (2026-05, 2026-08, …)
    │   ├── rule_reach_history.csv per-period rule reach (feeds the trend chart)
    │   └── snapshot_history.csv  every period's pinned commits, one row per series
    │                             per period — the cross-period pin record, and the
    │                             only thing that makes an earlier period
    │                             reproducible (snapshot.json is this period alone)
    ├── intro.md                  front-page triage      ← spliced in Step 5
    ├── details.md                full findings          ← spliced in Step 5
    ├── charts.md                 visual summary         ← reads data/ at build time
    ├── spec.md                   rubric, methodology, deterministic coverage
    ├── appendix.md               feedback to style guide & action-style-guide
    └── lecture-<series>/
        ├── index.md              series "Summary" rollup   ← Step 4 prose, Step 5 tables
        └── <stem>.md             one per lecture            ← Steps 2–3
```

---

## Known follow-ups

- `actions/deploy-pages@v4` runs on Node 20 (GitHub deprecation mid-2026) — bump when
  convenient.
- The 8 judgment-only rules (spec §9) are the remaining manual cost of a pass, and the
  reason `/pass-review` is budgeted separately. `qe-code-001` could plausibly be
  delegated to `ruff`.
- `qe-math-002` and `qe-writing-004`/`006` are heuristic. The proper-noun and
  common-noun lists in `tools/qestyle_rules.py` are curated from this corpus and will
  need extending as lectures are added.
- Corpus defects to file against the lecture repos — the malformed
  `` {eq}`eq:Kalman102} `` in `cross_product_trick.md:133`, the two unclosed
  `{exercise-start}` fences in `python_by_example.md`, the raw `\label` in
  `ifp_advanced.md:158` — are tracked in `ROADMAP.md` § *Findings to file against lecture
  repos*, and published in [`lectures/intro.md`](lectures/intro.md) § *Fix immediately*
  and [`lectures/appendix.md`](lectures/appendix.md). Don't restate them here; keep the
  one list.
- Four open questions were migrated here from the absorbed audit repo: archiving locks a
  repo's issues, so open work cannot stay there. They are
  [compliance-lecture-style#1–#4](https://github.com/QuantEcon/compliance-lecture-style/issues/1):
  the `{doc}` link form for same-series references, the near-empty MEDIUM priority band in
  spec §4, how lectures shared between `lecture-dp` and `lecture-python.myst` are counted,
  and revisiting the weights now that rule reach is measured.

---

## Standing up a separate audit

```bash
NEW=audit-YYYY-MM-topic          # dashes: QEP-3 reserves dots for content variants
gh repo create QuantEcon/$NEW --public --clone
# bring across the machinery and the history, not the findings:
cp -r tools requirements.txt ROADMAP.md UPDATE.md CLAUDE.md .github .claude ../$NEW/
mkdir -p ../$NEW/lectures/data
cp lectures/_config.yml lectures/spec.md lectures/charts.md ../$NEW/lectures/
cp -r lectures/_static ../$NEW/lectures/
cp lectures/data/rule_reach_history.csv lectures/data/history.csv \
   lectures/data/snapshot_history.csv ../$NEW/lectures/data/
# then run Steps 1–8 and enable Pages:
gh api -X POST repos/QuantEcon/$NEW/pages -f build_type=workflow
```

**The name takes the dash form.** QEP-3 registers dated audits as `audit-YYYY-MM-topic`
and reserves dots for content variants, so `audit.2026-05.style-guide` and the other
dotted names are grandfathered, not the pattern to copy. Rename nothing that already
exists to match: renames fix names, they never transmute types.

Use this only for a genuinely **separate** audit — a different subject, examined once,
with no cadence behind it. A one-off examination publishes as a dated repo and freezes;
that is the whole point of the `audit-*` form. The next period of *this* subject is not
that: it runs in place here (Steps 1–8), because that is what a ledger is. If a separate
audit later acquires a cadence, an owner and a runbook, it becomes a `compliance-*` repo
assembled from the audits it absorbs — the audits keep their names and stay published.

If the new audit does track something over time, bring `rule_reach_history.csv`,
`history.csv` **and `snapshot_history.csv`** across — those are the files whose *old* rows
matter. The third is the one that is easy to miss, and the costly one to miss: the other
two carry a period's numbers but not the commits they were measured over, so a fork that
leaves it behind cannot re-measure a single period it inherited — it starts life with
[#13](https://github.com/QuantEcon/compliance-lecture-style/issues/13) already in it.
Generate everything else fresh.
