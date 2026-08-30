# Appendix — feedback to the style guide & action-style-guide

A pass does more than score lectures — it also feeds back into the tooling and conventions it scores against. This page is the standing summary of that feedback: four issues filed from the May 2026 audit, and three drafts from the 2026-08 pass that are not yet filed. The source material (issue bodies, ready-to-merge rule entries) lives in this repo under [`contributions/`](https://github.com/QuantEcon/compliance-lecture-style/tree/main/contributions).

## How the pieces fit

- The **[QuantEcon manual style guide](https://github.com/QuantEcon/QuantEcon.manual/tree/main/manual/styleguide)** is the human-readable source of conventions.
- **[`action-style-guide`](https://github.com/QuantEcon/action-style-guide)** is the tool that enforces them — a registry of `qe-*` rules checked at PR time. This ledger scores lectures against that registry (see the [scoring spec](spec.md)).
- Where a pass found a convention in the manual that **isn't yet a coded rule**, or a way to make the tool **catch more, faster**, it became feedback. Four issues capture it.
- Where a pass found that a rule's *text* does not settle a question its own counts depend on, that became feedback too — three drafts from this pass, not yet filed.

## Four issues opened

| Issue | What it proposes |
|-------|------------------|
| [#18 — 7 new style rules](https://github.com/QuantEcon/action-style-guide/issues/18) | Encode 7 conventions the manual documents but the registry is missing (see table below). |
| [#19 — Phase 4.3 acceleration](https://github.com/QuantEcon/action-style-guide/issues/19) | Extend the planned deterministic-checker scope beyond the ~13 rules originally planned. The issue first argued for 22; building the checks settled it at **41 of 49**, and it now also offers the implementation for adoption. |
| [#20 — bulk-audit mode](https://github.com/QuantEcon/action-style-guide/issues/20) | A design discussion: should cross-series scoring / synthesis (what produced this report) live inside `action-style-guide`, a sibling tool, or stay ad-hoc? |
| [#21 — corpus offer](https://github.com/QuantEcon/action-style-guide/issues/21) | Offers this labelled corpus as test / evaluation fixtures for the tool. Now stronger than when filed: `lectures/data/violations.csv` carries per-lecture, per-rule counts with line numbers at a pinned commit per series, rather than prose summaries. |

## Proposed new rules (issue #18)

Seven conventions documented in the manual but not yet in the registry. They appear throughout this report tagged **(proposed)**. The five that are mechanically checkable are recommended for adoption; the last two are judgment calls and may be deferred.

Evidence is now measured rather than estimated — counts come from
`lectures/data/rule_reach.csv` over 348 lectures at a pinned snapshot. Five of the seven
are implemented as checks; the last two are judgment calls and are reviewed by reading, so
they carry no mechanical count.

| Proposed ID | Convention | Lectures | Occurrences |
|-------------|-----------|---------:|------------:|
| `qe-math-010` | `\mathbb{P}` / `\mathbb{E}` / `\mathbb{V}` (with braces) for probability, expectation, variance | **124 / 348** | 1,608 |
| `qe-writing-009` | Write "IID", not "i.i.d." / "iid" | 30 | 61 |
| `qe-math-011` | Plain letters for distribution names (`N`, not `\mathcal{N}`) | 34 | 134 |
| `qe-math-013` | Reference equations via `` {eq}`label` `` | 6 | 6 |
| `qe-math-012` | `\cdot` or juxtaposition for multiplication — never `*` | 4 | 6 |
| `qe-math-014` *(judgment)* | Braces `\{…\}` for events, parentheses `(…)` for sets under `\mathbb{P}` | — | not mechanically checkable |
| `qe-math-015` *(judgment)* | Lowercase for densities/PMFs, uppercase for CDFs | — | not mechanically checkable |

`qe-math-010` is the strongest case in the set by a wide margin. `qe-math-012` and
`qe-math-013` turned out much narrower than the original estimates once their checks were
tightened against false positives — `qe-math-012` was firing on `\operatorname*` and on
convolution notation, and `qe-math-013` on references into other authors' papers, where a
numeric equation reference is the only thing that can be cited.

Ready-to-merge rule entries for each are in [`contributions/rule-drafts/`](https://github.com/QuantEcon/compliance-lecture-style/tree/main/contributions/rule-drafts).

## Direct feedback to a lecture repo

Two findings are build-breaking and were flagged for `lecture-python.myst` regardless of the tooling discussion (also on the [front page](intro.md#fix-immediately)):

- [`lecture-python-programming/python_by_example.md:499` and `:549`](https://github.com/QuantEcon/lecture-python-programming/blob/main/lectures/python_by_example.md#L499) — two `{exercise-start}` fences that are never closed, each swallowing the rest of its exercise including a nested `{hint}` at the same tick count (`qe-admon-003`). The only two malformed gated directives in roughly 690 across the corpus.
- [`cross_product_trick.md:133`](https://github.com/QuantEcon/lecture-python.myst/blob/main/lectures/cross_product_trick.md#L133) — malformed `` {eq}`eq:Kalman102} `` reference. `lecture-dp` carries a byte-identical copy, so one upstream fix clears both.
- [`ifp_advanced.md:158`](https://github.com/QuantEcon/lecture-python.myst/blob/main/lectures/ifp_advanced.md#L158) — raw `\label{a:y0}` inside `$$`, which MyST does not resolve (`qe-math-007`). `lecture-dp` has the same defect at the same line, but its copy of this lecture has diverged from the upstream one — so each needs its own fix.

> **Withdrawn.** An earlier pass reported `divergence_measures.md:134` as `\begin{align}` inside `$$`, breaking the PDF build. Re-measured mechanically, there is no `align` inside `$$` anywhere in the corpus — that line is a bare top-level `\begin{align}`, which MyST's amsmath extension handles. It remains a convention outlier and is reported as one under `qe-math-006`, but no issue should be filed calling it a build break.

## Three questions this pass could not answer for itself

Three drafts came out of the 2026-08 pass and are **not yet filed** — they need a home once
the rule registry is consolidated. All three are places where the checker deliberately
answers a *narrower* question than the rule asks, because the rule's text does not settle the
wider one, and guessing would either flood the report or hide real drift. Each carries the
cost of both readings, so whoever answers can see what they are choosing between.

| Draft | The question | What turns on it |
|---|---|---|
| [`05-rule-format-for-checkability`](https://github.com/QuantEcon/compliance-lecture-style/blob/main/contributions/issues/05-rule-format-for-checkability.md) | Should a rule definition carry the exemptions and scope its own counts depend on? | 144 under-specification gaps across 42 in-scope rules. `qe-fig-003`, the only rule with an explicit exemption clause, is also the only figure rule with zero false positives. |
| [`06-ref-001-author-name-citations`](https://github.com/QuantEcon/compliance-lecture-style/blob/main/contributions/issues/06-ref-001-author-name-citations.md) | What makes a citation "narrative" — the author's name in the sentence, or the citation's position? | 299 author-name sites are undetermined under the current text; the two readings need different fixes, and repairing one deletes true findings under the other. |
| [`07-fig-008-line-width-tolerance`](https://github.com/QuantEcon/compliance-lecture-style/blob/main/contributions/issues/07-fig-008-line-width-tolerance.md) | Does `lw=2` mean every line, or the primary lines? | 264 `plot()` calls across 84 lectures set some other width, spread over twenty-one distinct values. Just over half carry a de-emphasis signal and read as deliberate; the rest read as drift. |

## Status

All four issues are open. **The bodies in `contributions/issues/` are now ahead of the
live issues** — this pass rewrote #19 around the measured 41-of-49 result, and the links in
all four now point at this repository, but `action-style-guide` was not in this pass's
GitHub scope, so nothing was pushed. The `rule-drafts/` here are written as
**transcription inputs** for a consolidated rule database rather than as a PR against
`action-style-guide`. Program-level direction for the style guide is coordinated in
`QuantEcon/project-style-guide`, a private planning hub, and is recorded there rather than
here. See
[`contributions/README.md`](https://github.com/QuantEcon/compliance-lecture-style/blob/main/contributions/README.md)
for the re-sync command and the per-issue status.
