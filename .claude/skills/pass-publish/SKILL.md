---
name: pass-publish
description: Publish the ledger — close a compliance period and deploy the site. Re-measures the previous snapshot with the current code, writes the series narratives, appends the period to the trend, runs the gate, builds the book, opens the PR, watches the deploy to completion and tags the pass. Use when asked to publish the ledger, close the period, close out a pass, add a period to the trend, or deploy the site.
---

# Close a period and publish the ledger

This is the last of three skills. Run them in order:

| Skill | Cost | What it leaves behind |
|-------|------|-----------------------|
| `pass-measure` | seconds | the corpus pinned, every number measured, every report drafted, the review queue printed |
| `pass-review` | ~5 agent-minutes per lecture | the judgment overlays in `reviews/<series>/<stem>.json` |
| **`pass-publish`** | **minutes** | **a period closed, the site deployed** |

Everything here is cheap and mechanical **except the decision to run it**. Merging deploys
the published site, so treat this skill as the deliberate act it is.

Reference: [`UPDATE.md`](../../../UPDATE.md) · methodology:
[`lectures/spec.md`](../../../lectures/spec.md) §8–§10.

---

## What publishing means here

This repository is a **ledger**, not an audit. Publishing is *updating a standing record*,
not issuing a new report. The consequences are practical, not rhetorical:

- **A period does not replace the last one — it joins it.** Its numbers land in
  `lectures/data/history.csv` and `lectures/data/rule_reach_history.csv`, and the trend
  chart in `lectures/charts.md` reads both at build time. The point of the record is the
  comparison, which is why Step 2 exists.
- **The dated `audit-*` repositories absorbed into this ledger stay published.** The May
  2026 pass remains readable at
  <https://quantecon.github.io/audit.2026-05.style-guide/> as a frozen record of its own
  examination, and its issues stay citable after the repo is archived. Nothing published
  here supersedes them; this ledger *continues* them.
- **The repository type is proposed, not settled.** `compliance-{domain}` is registered in
  QEP-3 ([QuantEcon/qeps#7](https://github.com/QuantEcon/qeps/pull/7)), which is still an
  open PR. Cite it that way in anything you write into the book.

So: no "new report" language, no re-issuing, no version numbering of the ledger itself. A
period is a row.

---

## Step 0 — Preconditions

Publish only when all three hold. Check them, do not assume them.

```bash
.venv/bin/python tools/qestyle_status.py --reviews reviews --data lectures/data
```

**1. The review queue is empty, or its remainder is a deliberate, stated choice.**
`qestyle_status.py` joins `lectures/data/lecture_blobs.csv` against each overlay's
`source.blob` and classes every lecture:

| | |
|---|---|
| **fresh** | the overlay's `source.blob` is the lecture's current blob — the judgment was made against this text |
| **stale** | the lecture changed since it was judged |
| **unstamped** | an overlay with no `source` key: it records a judgment but not the text judged, so freshness is undecidable. `tools/qestyle_backfill_provenance.py` stamps these from the pinned snapshot |
| **unknown** | stamped, but the lecture has no current blob on record |
| **missing** | never judged |

It is a report, not a gate: read-only and always exit 0, so the queue being non-empty will
not stop you. Publishing with a remainder is allowed — it is often the right call late in a
period — but it is a decision, so **name it in the PR body**: how many stale, how many
missing, and why they are being left. An unstated remainder silently makes the cross-series
scoreboard partly a ranking of review coverage, which is the one thing it must not be.

The same report prints the period, the pinned snapshot, the **recorded pins** — every
period's commits with its `basis` and `checker` digest, read straight from
`snapshot_history.csv` — and the open reviewer doubts. Two periods sharing a digest were
measured by the same instrument and are comparable; two that do not, are not, which is the
Step 1 decision in one line. Read the doubts before publishing too: they are the most
productive source of detector defects in the project, and one that lands a rule fix sends
you back to Step 1.

**2. The gate passes.**

```bash
CORPUS=.corpus
.venv/bin/python tools/qestyle_check.py --root lectures --data lectures/data --corpus $CORPUS
```

Must print `All checks passed`. `--corpus` is not optional: the coverage check — a lecture
with no report, a report with no lecture — only runs when it is given.

**3. The build is clean at 0 warnings.**

```bash
.venv/bin/jupyter-book build lectures --path-output /tmp/bk
```

Zero is the standing state, so **any warning means something regressed**. The usual cause
is `escape_roles()` in `qestyle_draft.py` meeting a MyST role it does not know: that is
what took this build from 478 warnings to 0, and both its failure modes are written up in
[`tools/VERIFICATION.md`](../../../tools/VERIFICATION.md).

---

## Step 1 — Re-measure the previous snapshot with the current code

**This is not optional after any detector change** — and since the pins landed, the gate
says so rather than leaving it to judgment: every `snapshot_history.csv` row must carry the
digest of `qestyle_scan.py` + `qestyle_lex.py` + `qestyle_rules.py` as they are in this
tree, so an un-re-measured period is a red gate. (Measured: one comment line appended to
`qestyle_lex.py` fails all 10 rows.)

Reach is comparable across periods only if both periods were measured by the same program.
Skip this step and a detector fix reads as a corpus improvement: the rule looks like it got
better because the checker changed, the trend chart shows a fall nobody earned, and the
sentence in `intro.md` that quotes it is wrong in a way no gate can catch — the digest
catches the *staleness*, never the wrong sentence.

Reconstruct the previous period's corpus as a worktree per series, kept under `.corpus/`,
which is gitignored, so the working tree stays clean.

The pins are **in the repo**: `lectures/data/snapshot_history.csv`, written by the scan
beside `--append-history`, header `period,series,basis,commit,committed,lectures,checker`,
one row per series per period. Read them from there — nothing here carries a SHA inline.

```bash
set -euo pipefail
CORPUS=.corpus; P=2026-05; PREV=.corpus/.prev-$P; mkdir -p $PREV
for r in lecture-python-intro lecture-python-programming lecture-python.myst \
         lecture-python-advanced.myst lecture-dp; do
  SHA=$(awk -F, -v p=$P -v s=$r '$1==p && $2==s {print $4}' \
          lectures/data/snapshot_history.csv)
  [ -n "$SHA" ] || { echo "no recorded pin for $P/$r — recover one, never guess"; exit 1; }
  # Skip when already complete; do NOT mask a real fetch failure with `|| true`.
  if [ "$(git -C $CORPUS/$r rev-parse --is-shallow-repository)" = true ]; then
    git -C $CORPUS/$r fetch --unshallow --filter=blob:none
  fi
  git -C $CORPUS/$r worktree add --no-checkout "$PWD/$PREV/$r" $SHA
  git -C $PREV/$r sparse-checkout set --no-cone '/lectures/*.md' '/lectures/_static/*.bib'
  git -C $PREV/$r checkout
done
```

`basis` says where a row came from: **`pinned`** — recorded by the scan at the moment it
measured that period; **`recovered`** — established afterwards and verified against that
period's recorded rule reach. Those are the only two legal values, because a pin that could
not be verified is not written at all. So an **empty result is information**: that period
has no trustworthy pin, and the answer is to recover one and verify it (below), never to
fall back to a date. The 2026-05 rows are `recovered`; how they were established is
[`tools/VERIFICATION.md`](../../../tools/VERIFICATION.md) § How the 2026-05 pins were recovered
(the pin table is also in `ROADMAP.md` § 2.4).

- **Use an absolute path for `worktree add`.** It resolves relative to the clone, not to
  this repo, and a relative path silently lands the worktree somewhere else.
- **Never reconstruct a past snapshot from a date.** `git log --until=YYYY-MM-DD` fills the
  unspecified time-of-day from the wall clock at the moment it runs, so it is not a function of
  its arguments: two runs 26 minutes apart returned cutoffs 1,584 seconds apart. The recipe here
  previously used `--until=2026-05-31`, which yields a 301-lecture corpus and three wrong pins.
  Three separate date reconstructions of 2026-05 were tried and all three were wrong — and one
  of them matched every per-series lecture count while still being wrong on two series, so a
  count is not a check. Use the recorded pin.
- **Verify before you trust a recovered pin.** Re-measure the candidate and compare against that
  period's rows in `rule_reach_history.csv`: a correct pin set reproduces them exactly, all 35
  rules on both columns. That is the only check that discriminates — and it is the check a
  `recovered` row asserts has already been run, which is why an unverified candidate must
  never be written into `snapshot_history.csv` to "save" it.
- **Carry `_static/*.bib` into the worktree.** Any rule that checks a citation against the
  bibliography resolves *zero* keys without it, and fails silently in both directions: a
  fail-closed check reports no findings, a fail-open one reports all of them, and neither
  says why. One file per series, and the previous period needs it as much as the current one
  or the trend row is meaningless.

Then measure it — **into a throwaway `--out`**:

```bash
.venv/bin/python tools/qestyle_scan.py --corpus $PREV --out /tmp/d05 \
    --period 2026-05 --append-history lectures/data/rule_reach_history.csv
```

`--out /tmp/d05` is load-bearing. `--out lectures/data` would overwrite the *current*
period's `violations.csv`, `rule_reach.csv` and `snapshot.json` with the old snapshot's
numbers, and the gate would then fail every per-lecture report against them. Only
`--append-history` is meant to touch the repo — and it now writes **two** files: this
period's reach into the path you give it, and the period's pins into
`snapshot_history.csv` in the same directory. Both replace that period's rows rather than
adding a second set, so a re-measure rewrites the period in both.

That second file is written from what the scan actually read, so pointing it at the wrong
worktrees overwrites good pins with bad ones under the same period label. A re-measure
refreshes each row's `checker` and **carries its `basis` over** when the commit is
unchanged: the scan only read that pin back from this very file, so writing it as
`pinned` would claim it had witnessed a commit it never did. A row whose commit *did*
change is a new pin and is written as `pinned` — right when the reconstruction verified,
wrong when it did not. So verify first, then read the diff:

```bash
git diff lectures/data/snapshot_history.csv
```

With a correct reconstruction nothing but `checker` moves. A moved `basis`, `commit`,
`committed` or `lectures` means you measured a different tree than the record names — stop,
and re-check the pins before committing anything.

The gate keeps one net under this: a period's pinned `lectures` must sum to that period's
`history.csv` TOTAL. Scanning the 2026-08 corpus under `--period 2026-05` fails with
`2026-05: pinned lectures sum to 348, history.csv TOTAL is 300`. But it is a net for *size*
only — the near-miss candidate that matched all five per-series counts and the 300 total
would pass it and still be wrong on two series. The 35-rule reach fingerprint remains the
check that discriminates.

A re-measure moves the previous period's own numbers, including its lecture count — that is
expected, and it is the point. `history.csv` records 2026-05 at **300** lectures because
that is what the current code counts over the May snapshot.

---

## Step 2 — Series narratives

Each `lectures/<series>/index.md` carries five generated regions and **two hand-written
ones**: `<!-- qe:series-narrative -->` and `<!-- qe:series-recommendations -->`. They use
marker syntax but are not in `SERIES_BLOCKS`, so `--splice` never regenerates them — you
write them, from the data, for this period.

They are also the ledger's **one blind spot**, and it is worth understanding why before you
trust anything in them. `tools/qestyle_check.py` strips *every* `<!-- qe:… -->` region with
`SPLICE_RE` before it looks for hand-written claims, on the assumption that a marked region
is generated. These two are not. So a reach figure inside them is checked by nothing.

Verify every figure you quoted:

```bash
.venv/bin/python - <<'PY'
import csv, collections, re, pathlib
per = collections.defaultdict(dict)
for r in csv.DictReader(open('lectures/data/series_rule_reach.csv')):
    per[r['series']][r['rule']] = int(r['lectures_affected'])
n = {r['series']: int(r['lectures'])
     for r in csv.DictReader(open('lectures/data/series_summary.csv'))}
bad = 0
for s in per:
    t = pathlib.Path(f'lectures/{s}/index.md').read_text()
    for m in re.finditer(r'`(qe-[a-z]+-\d{3})`[^(\n]*\((\d+)\s*/\s*(\d+)', t):
        rule, a, b = m.group(1), int(m.group(2)), int(m.group(3))
        if per[s].get(rule) != a or b != n[s]:
            print(f'  MISMATCH {s} {rule}: prose {a}/{b}, data '
                  f'{per[s].get(rule)}/{n[s]}'); bad += 1
print('all reach claims check out' if not bad else f'{bad} mismatches')
PY
```

**Run it even when you are confident.** It caught a reach figure written from memory that a
rule fix had since changed, and it earns its keep every time a detector moves.

Two limits of the snippet, so you do not over-trust it either:

- It only matches a `(N / M` form on the same line as a backticked rule id. A figure written
  as "31 of 52 lectures", or split across a line break, is invisible to it — read the prose
  as well as running the check.
- It says nothing about occurrence counts, only lecture reach. Those come from the same
  `series_rule_reach.csv` column, so check them by eye against `total_occurrences`.

Content notes for the narratives:

- Write what the data says about **this** series and how it moved since the last period.
  Never "well written"; never a claim that would be true of any series.
- `lecture-dp` shares filenames with `lecture-python.myst`, and only some of those are still
  byte-identical. The identical ones are one finding counted twice and one upstream fix
  clears both; the diverged ones each need their own fix. How they should be counted is an
  open question — [`compliance-lecture-style#3`](https://github.com/QuantEcon/compliance-lecture-style/issues/3).
  Say which situation a lecture is in rather than implying the corpus totals are unaffected.
- Any proposed rule cited outside a section that is itself about proposed rules carries its
  **(proposed)** tag. The gate checks this one.

---

## Step 3 — The history row

Two files carry the trend, and they are written by two different tools. Both need the
period:

```bash
.venv/bin/python tools/qestyle_score.py  --root lectures --fix --csv lectures/data/scores.csv
.venv/bin/python tools/qestyle_report.py --summarise --history 2026-08 --splice
```

`--history PERIOD` appends this period's per-series scores to `lectures/data/history.csv`.
It reads `scores.csv`, so **run `qestyle_score.py` first** or you will record the previous
run's arithmetic under this period's label. `qestyle_scan.py --period P --append-history …`
(Step 1, and in `pass-measure`) is the other half: per-rule reach into
`rule_reach_history.csv`, and the period's pins into `snapshot_history.csv` beside it.

**Both are idempotent within a period.** Each drops every existing row whose `period` equals
the one being written before it writes:

```python
existing = [r for r in existing if r.get("period") != period]      # qestyle_report
rows = [r for r in csv.DictReader(fh) if r["period"] != args.period]  # qestyle_scan
```

So re-running inside a period **replaces** the period rather than duplicating it, and you
can re-measure as many times as you like before publishing. A closed period is only ever
re-opened by re-running it under its own label.

The corollary is the trap: **the period label is the row's identity.** `2026-9` and
`2026-09` are different periods, so a mistyped label does not correct the row — it adds a
phantom one, and the trend chart grows a column that nothing measured. Check
`cut -d, -f1 lectures/data/history.csv | sort -u` after writing.

---

## Step 4 — Prose the gate cannot check

The gate verifies the trend table and the counts tables. It cannot verify a number written
into a *sentence* — except for four tallies it does cover, each of which had already broken
twice by the time it was covered:

| Checked | Not checked |
|---------|-------------|
| A trend row `A% → B%` in a table naming one rule | Any other figure in a sentence |
| A counts table whose header names *Lectures* and *Occurrences* | Anything inside a fenced code block (`FENCE_RE` strips them) |
| The trend sentence's tallies: *N rules measurable in both snapshots*, *N improved*, *N held level*, *N got worse* | Anything inside a `<!-- qe:… -->` region — including the two hand-written series regions (Step 2) |
| 31 line-width claims in `appendix.md` and `contributions/issues/07-…`, held to `fig_line_widths.csv` | Occurrence totals quoted in prose |

**After any rule change, re-read the narrative claims in `lectures/intro.md`,
`lectures/details.md` and `README.md` by hand.** A rule fix moves reach; hand-written
sentences do not follow. The corpus-size sentence in `intro.md` ("The corpus grew from 300
to 348 lectures") is exactly this shape — true only until the next scan, checked by nothing.

The same applies to the lecture count anywhere it appears in prose. It changes every period
(300 → 348 across the two measured so far). Take it from `snapshot.json`; never bring the
previous period's number across.

---

## Step 5 — Build, PR, merge, deploy

```bash
.venv/bin/jupyter-book build lectures
ls lectures/_build/jupyter_execute/*.png | wc -l    # expect 5 — the charts rendered
```

Then the PR. There is **no PR template in this repo** as it stands; check
`.github/pull_request_template.md`, `.github/PULL_REQUEST_TEMPLATE.md`,
`.github/PULL_REQUEST_TEMPLATE/` and `docs/` before writing one from scratch, and mirror its
headings if one has appeared.

```bash
git switch -c publish-2026-08
git add -A && git commit    # subject: "Close the 2026-08 period"
git push -u origin publish-2026-08
gh pr create --repo QuantEcon/compliance-lecture-style --base main \
    --title "Close the 2026-08 period"
```

A useful body says: what moved since the last period (from the trend, not from memory), the
review-queue remainder from Step 0 and why it is being left, and any detector change that
required the Step 1 re-measure.

> **No closing keyword before an `owner/repo#N` reference** — in the commit subject, the
> commit body, or the PR body. GitHub's auto-linker fires on `fix`/`closes`/`resolves`/… even
> as a noun and even followed by a colon, and a squash merge carries the PR body onto `main`,
> giving the same text a second chance to fire. Write "Ports the fix from …", "See …". This
> matters here because a publish PR naturally references the migrated open questions
> ([#1–#4](https://github.com/QuantEcon/compliance-lecture-style/issues/1)) and the absorbed
> audit's execution tracker, none of which this PR closes.

**Merging deploys the site.** `.github/workflows/deploy.yml` runs on every push to `main`,
builds `lectures/` and publishes to <https://quantecon.github.io/compliance-lecture-style/>.
There is no separate release step and no staging site, so the merge *is* the publication.
Watch the run to completion rather than assuming it:

```bash
gh run watch "$(gh run list --repo QuantEcon/compliance-lecture-style \
    --workflow deploy.yml --limit 1 --json databaseId -q '.[0].databaseId')" --exit-status
```

Then **verify against the published URL, not against `main`** — a green workflow proves the
artifact uploaded, not that the page a reader loads has moved. Check the commit Pages is
actually serving, then spot-check a figure that is new this period:

```bash
gh run list --repo QuantEcon/compliance-lecture-style --workflow deploy.yml --branch main \
    --limit 1 --json headSha,conclusion -q '.[0] | .headSha, .conclusion'
curl -sf https://quantecon.github.io/compliance-lecture-style/intro.html | grep -c '<a string this period changed>'
```

(Not `gh api …/pages/builds/latest`: that endpoint describes the legacy Jekyll build path
and returns 404 for a site published by `actions/deploy-pages`, which this one is. The
deploy run's `headSha` is the commit its artifact was built from.)

Pick the grep target from something the period actually moved — a corpus size, a scoreboard
figure — not from boilerplate that was on the page before the deploy. A count of `1` against
text that never changed proves nothing.

The deploy job takes the `github-pages` environment and the `pages` concurrency group with
`cancel-in-progress: false`, so two publishes queue rather than race. If a run hangs in
`build`, cancelling and re-running is safe as long as it has not reached `deploy`.

---

## Step 6 — Tag the published pass

`snapshot_history.csv` now makes a period's *inputs* reproducible — the corpus commits, and
a digest of the code that measured them. The tag names the other half: the ledger tree that
produced the period, `tools/` and `reviews/` and `lectures/spec.md` together, in one O(1)
reference.

Tag the commit Pages actually served, not whatever `main` has become by the time you get
here:

```bash
git fetch origin main --tags
COMMIT=$(gh run list --repo QuantEcon/compliance-lecture-style --workflow deploy.yml \
           --branch main --status success --limit 1 --json headSha -q '.[0].headSha')
[ -n "$COMMIT" ] || { echo "no successful deploy run to tag"; exit 1; }
git tag -a pass/2026-08 $COMMIT -m "Ledger tree that produced the 2026-08 period"
git push origin pass/2026-08
```

It costs nothing and it pairs with the `checker` column. The digest names the scanner that
measured the recorded periods — the gate holds every row to one, so a green ledger asserts a
single ruler across all of them — and the tag is how you get that scanner, and everything
around it, back: `git show pass/2026-08:tools/qestyle_rules.py`, no archaeology.

**It backfills nothing.** Do not invent a retroactive `pass/2026-05`. `tools/` first appears
in this repository at `f609536` ("Rebuild the audit as a reproducible pipeline; refresh to
the 2026-08 corpus"), so no 2026-05-era tree holds the pipeline at all — a tag there would
name a tree that could not have produced that period's numbers, which is worse than no tag.
Tagging starts with the first period published after this step existed; earlier periods are
covered by `snapshot_history.csv` and by nothing else.

---

## Step 7 — The contributions loop

[`contributions/issues/*.md`](../../../contributions/) are the **bodies of live issues** on
`QuantEcon/action-style-guide`. Editing one here does not update GitHub. Re-sync explicitly:

```bash
gh issue edit <n> --repo QuantEcon/action-style-guide \
    --body-file contributions/issues/<file>.md
```

| Issue | File |
|-------|------|
| [#18](https://github.com/QuantEcon/action-style-guide/issues/18) | `issues/01-new-style-rules.md` |
| [#19](https://github.com/QuantEcon/action-style-guide/issues/19) | `issues/02-phase-4-3-deterministic-checks.md` |
| [#20](https://github.com/QuantEcon/action-style-guide/issues/20) | `issues/03-bulk-audit-mode.md` |
| [#21](https://github.com/QuantEcon/action-style-guide/issues/21) | `issues/04-corpus-offer.md` |

`05-rule-format-for-checkability`, `06-ref-001-author-name-citations` and
`07-fig-008-line-width-tolerance` have **no home issue yet** and so nothing to re-sync.

**When corpus counts change**, the issue bodies and the appendix quote per-rule evidence that
has moved. Take the new numbers from `lectures/data/rule_reach.csv` — the
`lectures_affected` and `total_occurrences` columns — and **do not re-estimate them**. Then
update, in this order: the proposed-rule table in `lectures/appendix.md`, the affected issue
bodies, the rationale blocks in `contributions/rule-drafts/`, the lecture count in
`contributions/README.md`, and finally the live issues with the command above. The gate holds
`07-…`'s line-width figures to `fig_line_widths.csv`, so it will catch that one file; the
others are on you.

**`action-style-guide` is usually outside this session's GitHub access.** If you cannot run
`gh issue edit`, say so plainly and leave the re-sync as a named open item — do not write
prose that implies the live issues were updated.

---

## Traps

- **Publishing with the previous period un-remeasured.** The single most expensive mistake
  available here, because it produces a plausible number rather than an error. If any file
  in `tools/` changed since the last publish, Step 1 is mandatory. The gate catches the
  three files whose content the `checker` digest covers — `qestyle_scan.py`,
  `qestyle_lex.py`, `qestyle_rules.py` — and only those: a change in `qestyle_draft.py` or
  `qestyle_score.py` leaves every digest intact, so that one is still on you.
- **`--out lectures/data` on the previous-period scan.** Overwrites the current period's
  numbers with the old snapshot's. Use a throwaway directory. Note that this does *not*
  protect `snapshot_history.csv`, which is written beside `--append-history` on purpose —
  that is the one file a previous-period re-measure is meant to update in the repo.
- **A pin written into `snapshot_history.csv` that nothing verified.** The file has two
  bases and deliberately no third: `pinned` (the scan recorded it as it measured) or
  `recovered` (checked against that period's recorded reach, 35 of 35 rules on both
  columns). A plausible candidate typed in by hand gives a wrong answer the shape of a
  right one — three date reconstructions of 2026-05 were wrong, one of them matching every
  lecture count. If a period cannot be verified, it stays out of the file.
- **A reach figure inside `qe:series-narrative` or `qe:series-recommendations`.** Neither the
  splicer nor the gate touches those regions. Step 2's snippet is the only thing that does.
- **`gh run watch` on the wrong run.** `--limit 1` picks the newest run in the repo, which
  may be someone else's push. Pin the run id from the push you just made, or filter with
  `--workflow deploy.yml` as above.
- **Assuming green means published.** Check the URL.
