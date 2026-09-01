# Roadmap

Living document for the QuantEcon lecture style-compliance ledger. Tracks strategic
direction, open design decisions, and pending work.

**Last updated:** 2026-08-31

> **Program coordination has moved.** Program-level direction — the style-guide
> consolidation (rules database, linter, AI review agent), repo naming, cadence, and
> tooling decisions — now lives in the planning hub **`QuantEcon/project-style-guide`**
> (private), the program's home of record. This file records this ledger's own context and
> follow-ups; where its phases overlap program planning, **the hub supersedes**.

---

## Where we are today

- **A pass is reproducible.** A pass is a pipeline (`tools/qestyle_*.py`) over a
  **pinned corpus snapshot**, not a reading exercise: 41 of the 49 rules are checked by
  program, scores and priority buckets are derived arithmetically from the rubric, and
  `tools/qestyle_check.py` gates the result. Same commits in, same numbers out.
- **Corpus refreshed to 348 lectures** across the 5 series (from 300 at the previous
  snapshot). 49 lectures were added and 1 report was retired.
- **First real time series.** The same checks were run over both the previous and the
  current snapshot, so `lectures/data/rule_reach_history.csv` holds a like-for-like
  comparison and `charts.md` plots it. This is the thing the project has been aiming at
  since the shift to a durable model — and the first evidence that any rule is
  *improving* rather than just being counted.
- **The judgment layer is complete and stamped.** All 348 lectures have a review overlay
  in `reviews/<series>/<stem>.json`, and every overlay records the commit and blob it
  judged. That stamp is what makes the *next* pass incremental — see §2.4.
- **Tier 2 dashboard live** — Jupyter Book on GitHub Pages at
  **https://quantecon.github.io/compliance-lecture-style/**, with the synthesis, 5
  charts (now including the cross-pass trend), the spec, and a report per lecture. Chart
  data is no longer inline: it is read from `lectures/data/` at build time.
- **The ledger is being assembled.** This repo becomes
  `QuantEcon/compliance-lecture-style`; `audit.2026-05.style-guide` keeps its name and is
  archived once absorbed, so nothing published from the May-2026 pass moves or breaks.
  Decision in [audit#2](https://github.com/QuantEcon/audit.2026-05.style-guide/issues/2),
  execution in [audit#7](https://github.com/QuantEcon/audit.2026-05.style-guide/issues/7).
  See §1.
- **4 issues open** against `action-style-guide`
  ([#18](https://github.com/QuantEcon/action-style-guide/issues/18) new rules,
  [#19](https://github.com/QuantEcon/action-style-guide/issues/19) deterministic-checker
  scope, [#20](https://github.com/QuantEcon/action-style-guide/issues/20) bulk audit
  mode, [#21](https://github.com/QuantEcon/action-style-guide/issues/21) corpus offer).
  #19 now has an answer from implementation — see §4.1.

---

## 1. Naming and repository type: settled

> **Decision ([audit#2](https://github.com/QuantEcon/audit.2026-05.style-guide/issues/2),
> 2026-08-26).** No rename, ever. The living document moves to a new repository,
> **`QuantEcon/compliance-lecture-style`**. `audit.2026-05.style-guide` keeps its name for
> life, is **archived** once the ledger has absorbed it, and stays published — its Pages
> site and its issue threads remain readable and citable. Execution is tracked in
> [audit#7](https://github.com/QuantEcon/audit.2026-05.style-guide/issues/7).

**This reverses the 2026-08 leaning**, recorded in this file until now, to rename this repo
to `audit-lectures-style-guide`. Two things were wrong with that name.

The first is grammatical. `audit.YYYY-MM.{topic}` names one examination at one time, and the
date is not decoration — it is the part that makes `audit` true. `audit-lectures-style-guide`
kept the prefix and dropped the date, so it went on claiming to be an audit while describing
something that had stopped being one: a record re-measured in place, with a time series
attached.

The second is structural. QEP-3
([QuantEcon/qeps#7](https://github.com/QuantEcon/qeps/pull/7)) states the invariant
**"renames fix names; they never transmute types"**. A rename is the remedy for a repo whose
name is wrong. This repo's name was not wrong for what it was — it had outgrown its type,
which is a different problem with a different remedy: succession. A new repo of the right
type, the old one archived where it stands, rather than one repository claiming two types
across its own history.

**The type is `compliance-{domain}`.** QEP-3 registers it as a "standing record of a domain's
conformance with a named standard: rubric + runbook, findings and scores re-measured in place
per pass; versioned history seeded from each absorbed audit", governed by the boundary rule
**"the audit is the event; the compliance repo is the ledger"**. That is a description of
what `lectures/data/` has been doing for two passes, written down independently. QEP-3's own
Adoption section names this migration as its first instance. **QEP-3 is not accepted** — it is
an open PR whose comment window has not been announced — so the type is cited as proposed, not
as settled policy, here and everywhere else in the repo.

**Why not `status-{domain}`.** QEP-3's other boundary rule is that "`status-*` reports what
machines observe; `compliance-*` records what a rubric adjudicates". With 41 of the 49 rules
measured by program, `status-` is superficially tempting. But the measurements are not the
published output: the published output is an overall score, a priority bucket and a
per-lecture judgment, all of which come from the rubric in `lectures/spec.md`, and 8 of the
rules are read by a person rather than counted. Publishing that under `status-` would present
adjudication as observation — laundering opinion as fact — which is precisely the confusion
the two types exist to prevent.

**What made this a ledger** is that `lectures/data/` began accumulating across passes.
`history.csv` and `rule_reach_history.csv` now hold one row per period, and the trend chart is
built from them: the same checks over two pinned snapshots, so the comparison measures the
lectures rather than the method. A new dated repo per period either loses that series or
requires copying it by hand at every pass. The dated convention and a cross-period time series
pull in opposite directions, and the series is worth more.

The immediate prompt was that this pass left the repo named for 2026-05 while holding a
2026-08 snapshot — not a stable end state under any of the options.

**The dated convention is not retired.** It remains the right fit for genuinely episodic
audits — a security review of a release, a one-time deep dive. Style-guide compliance turned
out to be a persistent concern with a time series attached, which is a different shape. That
distinction is the whole of QEP-3's boundary rule, and the 2026-05 audit is the worked example
of the first half of it.

---

## 2. Open design decisions

### 2.1 Repo name

**Settled: `QuantEcon/compliance-lecture-style`** — see §1. It reads as "compliance, of the
lectures, against the style guide", takes the type prefix the repo actually is rather than one
it has outgrown, and leaves room for a sibling (`compliance-lecture-accessibility`) without a
date and without implying a one-off.

The alternatives, kept only as a record of what was considered:

| Considered | Why it lost |
|---|---|
| `QuantEcon/audit-lectures-style-guide` | The 2026-08 leaning, now reversed. Keeps the `audit-` prefix while dropping the date that prefix's grammar requires, and getting there by rename would have transmuted the type instead of fixing the name. |
| Keep `audit.YYYY-MM.style-guide` | Right for the 2026-05 event, and the audit repo does keep it — but as the name of the *living* document it goes stale the moment a pass refreshes it, as it had. |
| `QuantEcon/style-audits` (plural) | Implies recurring snapshots, which is the right instinct, but still says "audit" of a standing record and matches no registered type. |
| `QuantEcon/lecture-style-audit` | Singular reads as one-shot; same type problem. |
| `QuantEcon/lecture-quality` | Vague — "quality" has no operational definition here. |
| `QuantEcon/style-compliance` | Closest in spirit. The objection recorded against it — that "compliance" reads as regulatory — turned out to be the point. It loses only on the type prefix and on not naming the corpus. |
| `QuantEcon/status-lecture-style` | A registered type, but the wrong one — see §1. |

### 2.2 Time-series storage

Largely settled in practice: `lectures/data/*.csv` holds the current pass, and
`history.csv` / `rule_reach_history.csv` hold one row per period. That is the hybrid
(option D) the earlier analysis preferred — markdown for humans, CSV for charts. The
remaining question is only whether per-pass markdown snapshots are worth keeping
alongside, or whether git history is enough. **Leaning:** git history is enough.

### 2.3 Migration

The options as they were framed:

- **α** — rename this repo. Preserves history and the 4 issue cross-links; breaks the
  Pages URL.
- **β** — archive this repo as the baseline; create the durable repo and bring
  `lectures/data/` across. Cleaner conceptually; loses the per-lecture git history.
- **γ** — keep both: this repo as the 2026-05 reference, the new one going forward.

**Outcome: β — and it costs less than β was thought to.** Both of the costs charged against
it turn out not to apply.

- The ledger is assembled from this tree at the head of the 2026-08 pass, so **the git
  history comes with it**. Nothing is re-created from a copy.
- The audit repo is **archived, not deleted**. GitHub keeps serving an archived repo's Pages
  site and keeps its issues readable, so the May-2026 report stays at
  <https://quantecon.github.io/audit.2026-05.style-guide/>, the four cross-links posted into
  `action-style-guide` still resolve, and the decision records stay where they were written.

So **zero links break** — the cost that decided against β, and the cost that α was chosen to
avoid, is not paid by either party. What α would have cost is the thing that could not be
undone: a repository whose history claims one type and whose name claims another.

The one real cost is that **archiving locks issues** — no new comments, no reopening — so
anything still open had to move. Four questions did:

| Ledger issue | Was | Subject |
|---|---|---|
| [#1](https://github.com/QuantEcon/compliance-lecture-style/issues/1) | audit#1 | `qe-link-001/002`: the `{doc}` link form for same-series references |
| [#2](https://github.com/QuantEcon/compliance-lecture-style/issues/2) | audit#3 | Spec §4: the MEDIUM priority band is structurally almost empty |
| [#3](https://github.com/QuantEcon/compliance-lecture-style/issues/3) | audit#4 | How lectures shared between `lecture-dp` and `lecture-python.myst` are counted |
| [#4](https://github.com/QuantEcon/compliance-lecture-style/issues/4) | audit#6 | Revisit the audit weights now that rule reach is measured |

[audit#2](https://github.com/QuantEcon/audit.2026-05.style-guide/issues/2) (the naming
decision) and [audit#5](https://github.com/QuantEcon/audit.2026-05.style-guide/issues/5) (the
coverage caveat, since resolved) stay on the audit repo. They are records of what was decided
between May and August 2026, not open questions, and a locked issue is a perfectly good home
for a record.

**γ describes the end state, not the mechanism.** Both repositories exist and both stay
published; only one of them is still written to.

### 2.4 Cadence + automation

Two changes since this section was last written are what make a scheduled cadence affordable.
Both are prerequisites, not conveniences.

**The pass is split into three skills, along its cost seam.** A single skill could not run a
pass. Measured here: the mechanical layers run the whole 348-lecture corpus in seconds at
essentially no token cost, while the judgment layer costs about five agent-minutes per lecture
— on the order of 30 agent-hours for the corpus. Two concurrent reviewer agents exhausted a
session limit in under half an hour, mid-batch. So the split follows the cost, not the
workflow:

| Skill | Cost | What it does |
|---|---|---|
| `/pass-measure` | seconds, ~free | corpus, snapshot, scan, draft, score, splice, gate, build, and print the review queue |
| `/pass-review` | ~5 agent-minutes per lecture | the judgment layer: budgeted, resumable, with a hard stop at the budget |
| `/pass-publish` | minutes | close a period — re-measure the previous snapshot with current code, series prose, history row, gate, build, PR, deploy |

**Review cost now scales with churn, not with corpus size.** `tools/qestyle_scan.py` writes
`lectures/data/lecture_blobs.csv` — one git blob SHA per lecture at the pinned snapshot — and
every overlay records the `commit` and `blob` it judged. `tools/qestyle_status.py` joins the
two and classes each lecture **fresh**, **stale** or **missing**. Before this, an overlay
recorded a judgment but not the text judged, so the only answerable queue was "lectures with
no overlay at all" and every corpus refresh re-reviewed the entire corpus. All 348 overlays
are now stamped.

The saving has since been **measured** rather than estimated, by diffing the two snapshots'
blob tables — now kept per period as `lectures/data/blobs/<period>.csv`
([#17](https://github.com/QuantEcon/compliance-lecture-style/issues/17)), so the figures
below are a two-file diff anyone can re-run, and were re-derived from those files exactly. Over 2026-05 → 2026-08 — a three-month interval — **186** of the 348 lectures were
byte-identical, **114** had been edited and **48** were new, so a churn-scaled queue would have
been **162 of 348 (47 %)**: about **13.5 agent-hours rather than 29**, a 53 % saving. Real, but
only half of it. An earlier estimate here said "single-digit agent-hours", which the measurement
does not support.

**These counts are exact, and were not on the first two attempts.** The 2026-05 pinned commits
were not recorded anywhere — `snapshot.json` only ever held the current period — so the baseline
had to be recovered. They are recorded now, in
[`lectures/data/snapshot_history.csv`](lectures/data/snapshot_history.csv) with `basis=recovered`. Two date-cutoff reconstructions were tried and both were wrong: one yielded
298 lectures, the other 301. A third matched all five per-series lecture counts *and* the
300 total and was **still wrong on two series**, which is why a lecture count is not a usable
check. The pins below are the set that reproduces the recorded 2026-05 rule reach exactly — 35
of 35 rules, on both lectures affected and total occurrences:

| series | commit | committed | lectures |
|---|---|---|---|
| `lecture-python-intro` | `576cd1776110adad5160e304b6f202d694b58a97` | 2026-05-29T14:07:01+10:00 | 50 |
| `lecture-python-programming` | `a2b929f15e703b6942e8b80a29011c51f234b1e0` | 2026-05-13T18:45:09+08:00 | 26 |
| `lecture-python.myst` | `2944402a4c4a3101e92e2824e10b0dc212265264` | 2026-05-29T14:27:37+10:00 | 110 |
| `lecture-python-advanced.myst` | `6320d7142b5b807ec33fd2063d509ce8dbb9a302` | 2026-05-28T15:28:02+10:00 | 62 |
| `lecture-dp` | `6a7bc1c467d7472e008607a3e12bb177dd2fb0c5` | 2026-05-28T17:28:17+10:00 | 52 |

They are now in [`lectures/data/snapshot_history.csv`](lectures/data/snapshot_history.csv), one
row per series per period, so no future measurement has to re-derive them — that was
[#13](https://github.com/QuantEcon/compliance-lecture-style/issues/13). How they were established,
what was rejected, and the alternative that also fits are in
[`tools/VERIFICATION.md`](tools/VERIFICATION.md).

**The saving is a function of cadence, and that is the operational point.** Three months
touches half the corpus; a monthly pass touches far less, so frequent passes are
disproportionately cheaper per period than infrequent ones. The first refresh after a long
gap is close to a full pass and should be budgeted as one.

**That second change is what unblocks Phase 3.** A cadence was never really gated on the
scripts — those have been cheap for a while. It was gated on every period costing a full
corpus of judgment. It no longer does.

What remains:

- **Schedule the mechanical half.** A scheduled GitHub Action or Routine that runs
  `/pass-measure` and opens a PR with the diff. The review budget stays human-triggered:
  `/pass-review` is the only expensive part of a pass and should be spent deliberately.
- **Trigger, as an alternative or an addition:** run before each lecture-series release, as a
  quality gate.
- **Agree an interval — still open.** The 2026-05 → 2026-08 gap was one quarter and 49 new
  lectures (the pass's own figure — §1's blob diff counts 50 against a date-reconstructed
  baseline; see the note there). Whether a quarter is the right period, or whether a pass should hang off each
  series release instead, has not been decided.

`action-style-guide` [#20](https://github.com/QuantEcon/action-style-guide/issues/20) is
no longer a blocker for cadence, though it would still be the better long-term home for
the checks.

---

## 3. Dashboard

Tier 2 (Jupyter Book + charts) is live and now reads from `lectures/data/`, which is what
Tier 3 would have needed anyway. Remaining Tier 3 ideas, in order of likely value:

1. **Sortable / filterable lecture table** — the HIGH list is long enough that scanning
   it in markdown is work.
2. **Per-rule drill-down page** — one page per rule, listing every lecture and line. The
   data is already in `violations.csv`.
3. **Score-delta chart** — which lectures improved or regressed between passes. Needs
   `scores.csv` from two passes; available from the next pass onward.
4. **Category floor view** — since every HIGH lecture is triggered by a single weak
   category, a view grouped by *which* category would match how the work actually gets
   done.

Build these only if the Tier 2 pages are being used.

---

## 4. Pending external work

### 4.1 `action-style-guide` issues

| Issue | Status |
|-------|--------|
| [#18](https://github.com/QuantEcon/action-style-guide/issues/18) — 7 new style rules | Open. 5 of the 7 are now implemented as checks here and carry measured corpus evidence; `qe-math-014` and `qe-math-015` remain judgment-only and weak-evidence, and are still the two candidates to defer. |
| [#19](https://github.com/QuantEcon/action-style-guide/issues/19) — deterministic-checker scope | **Answered by implementation.** The issue argued the planned "~13" rules should be 22. Building them showed **41 of 49** are mechanically checkable — 36 of the 42 in-scope registry rules plus 5 proposed. The 8 that are not are listed in [spec §9](lectures/spec.md). The issue body should be updated with this result. |
| [#20](https://github.com/QuantEcon/action-style-guide/issues/20) — bulk audit mode | Open. Still the right long-term home for the checks: `tools/qestyle_rules.py` is a working reference implementation that could be contributed rather than maintained here. |
| [#21](https://github.com/QuantEcon/action-style-guide/issues/21) — corpus as test fixtures | Open, no action required. `lectures/data/violations.csv` is now a labelled fixture set with line numbers, which is more useful than the offer as originally framed. |

### 4.2 Findings to file against lecture repos

Small and structural; worth an issue each regardless of audit cadence.

- `lecture-python-programming/lectures/python_by_example.md:499` and `:549` — two
  `{exercise-start}` fences never closed, so each swallows the rest of its exercise
  including a nested `{hint}` at the same tick count (`qe-admon-003`). The only two
  malformed gated directives in ~690 across the corpus.
- `lecture-python.myst/lectures/cross_product_trick.md:133` — malformed
  `` {eq}`eq:Kalman102} `` reference. `lecture-dp` carries a synced copy with the same
  defect; fixing upstream fixes both.
- `lecture-python.myst/lectures/ifp_advanced.md:158` — raw `\label{a:y0}` inside `$$`,
  which MyST does not resolve (`qe-math-007`). Same synced-copy situation.

> **Withdrawn.** The previous report's headline build-risk finding —
> `divergence_measures.md:134` as `\begin{align}` inside `$$`, "breaks the PDF build" —
> does not hold. There is no `align` inside `$$` anywhere in the corpus. That line is a
> bare top-level `\begin{align}`, which MyST's amsmath extension handles. It remains a
> convention outlier (17 bare alignment blocks against 6,094 `$$` blocks) and is reported
> as one, but no issue should be filed calling it a build break.

---

## 5. Phased plan

### Phase 0 — Stabilise findings ✅
Audit published, spec published, 4 contribution issues opened.

### Phase 1 — Tier 2 dashboard ✅
Jupyter Book with `quantecon-book-theme`, per-lecture reports committed, charts, sidebar
TOC, GitHub Pages deploy. Chart data externalised to `lectures/data/` (was a Phase 1
follow-up; done).

### Phase 2 — Repo naming and type ✅ decided, migration in progress
No rename. The living document is being assembled as
`QuantEcon/compliance-lecture-style`; `audit.2026-05.style-guide` keeps its name and is
archived once absorbed. Decided in
[audit#2](https://github.com/QuantEcon/audit.2026-05.style-guide/issues/2), executed under
[audit#7](https://github.com/QuantEcon/audit.2026-05.style-guide/issues/7). See §1 for the
reasoning and §2.3 for why zero links break.

### Phase 3 — Cadence ◐ in progress
Two passes have run on pinned snapshots with a like-for-like comparison between them; the
procedure is documented in `UPDATE.md` and gated by `tools/qestyle_check.py`. The blocker was
never the scripts — it was that every period cost a full corpus of judgment, and the
provenance stamp has made a refresh churn-scaled instead (§2.4). What remains is agreeing an
interval and putting `/pass-measure` on a schedule.

### Phase 4 — Tier 3 dashboard (conditional)
See §3. Only if the Tier 2 pages are being used.

### Phase 5 — Automation ◐ partly delivered
The evidence and scoring layers are scripts, and the pass is now packaged as three skills
split along its cost seam (§2.4), so most of what Phase 5 anticipated exists. What is left is
running the mechanical half on a schedule and opening its PR automatically — and, longer term,
moving the checks into `action-style-guide` per #20 rather than maintaining them here.

---

## 6. Risks + known concerns

- **Scoring drift — largely mitigated.** The previous pass showed the failure mode
  clearly: 94 of 299 reports carried an overall score that did not match their own
  categories, 35 carried a priority bucket the rubric does not give, one report described
  a lecture that does not exist, and the largest series was scored noticeably more
  leniently than the others. Scores are now arithmetic and evidence is measured, so this
  class of error cannot recur silently. It remains possible in the 8 judgment-only rules —
  and see calibration drift, below, for the form it now takes.
- **Calibration drift between periods — new, and unmitigated.** Incremental review buys the
  affordable cadence in §2.4, and it costs this. When only changed lectures are re-reviewed,
  the judgment layer stops being one sitting's work under one calibration: a series page can
  hold a judgment made in 2026-08 beside one made a year later, by a different reviewer
  reading the same eight rules with a different sense of where the line sits. The provenance
  stamp records *which text* was judged, not *which calibration* judged it, so drift will
  never surface as a stale overlay. It would surface as a trend — a series moving up or down
  without its content moving — which is exactly the signal the trend chart exists to carry,
  and would be read as improvement. Nothing guards against this today. The candidates are
  re-reviewing a fixed sample each period as a control, or re-reviewing a whole series
  whenever spec §8.3 changes; neither has been tried.
- **Heuristic checks need maintenance.** `qe-writing-004` and `qe-writing-006` depend on
  curated proper-noun and common-noun lists; `qe-math-002` has to tell a transpose
  apostrophe from a derivative and a `^T` transpose from a terminal date. All three were
  tightened against adversarial review of real hits, and all three will need extending as
  lectures are added. They are the most likely source of a wrong count.
- **The MEDIUM band barely populates.** Applied consistently, spec §4's "any single
  in-scope category ≤ 4 → HIGH" catches nearly every lecture before its *overall* falls
  into the 5.1–7.0 MEDIUM range — every HIGH lecture in this pass was triggered by the
  category floor, no lecture in the corpus has an overall at or below 5.0, and exactly one
  lecture in 348 lands in MEDIUM at all (`kalman_2`, overall 6.9). The 4-bucket scheme is
  effectively 3 buckets. Worth revisiting §4 in the spec: either widen
  MEDIUM, or replace the flat floor with something graduated. Open as
  [#2](https://github.com/QuantEcon/compliance-lecture-style/issues/2).
- **Review cost, and what it scales with.** The mechanical layer runs the whole corpus in
  seconds at no token cost. The judgment layer is the entire expense — about five
  agent-minutes a lecture — and it used to scale with corpus *size*, because nothing recorded
  which text an overlay had judged. With the provenance stamp it scales with corpus *churn*
  (§2.4). The residual risk moves to the stamp itself: an unstamped overlay returns to the
  queue forever, and a wrongly-stamped one silently stays out of it.
- **Lecture content evolves.** Counts go stale immediately after each pass. Pinning the
  snapshot means a stale number is at least an *honest* number about a known commit.
- **Duplicated lectures inflate counts.** `lecture-dp` syncs several lectures verbatim
  from `lecture-python.myst`, so their findings appear twice in the corpus totals. This is
  disclosed in `details.md` but not corrected for; deciding whether to de-duplicate is a
  scoping question for the next pass, open as
  [#3](https://github.com/QuantEcon/compliance-lecture-style/issues/3).

---

## 7. Design notes worth preserving

- **Why the evidence layer came first.** Every defect found in the previous pass was a
  bookkeeping failure, not a taste failure — arithmetic, coverage, a hallucinated file.
  Those are exactly the failures a program does not make, and they were consuming the
  credibility that the judgment calls needed.
- **Why scores are derived rather than asserted.** The rubric already defines the overall
  score as a mean and the priority bucket as a threshold rule. Anything that *defines* a
  number should compute it; asking a reviewer to also arrive at it by hand only creates a
  second opinion to reconcile.
- **Why the trend is reported on rule reach, not on scores.** Reach is a count of
  lectures matching a fixed program, so it is comparable across passes by construction.
  Score levels depend on the scoring function, so a change to that function would show up
  as a spurious trend. Both are recorded, but reach is the honest headline. The same holds
  one layer up: a score row also depends on how much of the judgment layer it folds in —
  the 2026-08 corpus mean sat above 2026-05's until the overlays landed and below it after,
  with the lectures unchanged — which is why every `history.csv` row carries `reviewed` and
  `history_mechanical.csv` carries its evidence-layer twin
  ([#16](https://github.com/QuantEcon/compliance-lecture-style/issues/16)).
- **Why bare `align` is reported differently from `align` inside `$$`.** They fail
  differently — one is a nested math environment that breaks a PDF build, the other is a
  supported MyST form that merely departs from the corpus convention. Collapsing them is
  what produced a headline finding that did not survive checking.
- **Why Tier 3 waits on Tier 2 being used.** Dashboards become maintenance burdens.
  Prove the use case on the familiar stack first.
