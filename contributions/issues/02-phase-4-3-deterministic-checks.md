## Summary

Phase 4.3 in the [roadmap](https://github.com/QuantEcon/action-style-guide/blob/main/docs/developer/roadmap.md) (and §2.C of [IMPROVEMENTS.md](https://github.com/QuantEcon/action-style-guide/blob/main/IMPROVEMENTS.md)) targets **~13 mechanical rules via regex**, to remove hallucination risk and cut per-rule LLM cost.

This issue originally argued from corpus evidence that the number should be **22**. That estimate has since been settled by building the checks: **41 of the 49 rules are mechanically checkable.** 36 of the 42 in-scope registry rules, plus 5 of the 7 rules proposed in [#18](https://github.com/QuantEcon/action-style-guide/issues/18). The 8 that are not are genuine judgment and are listed below.

A working reference implementation exists — one function per rule, plus the MyST lexer they need — in the lecture style compliance ledger under [`tools/`](https://github.com/QuantEcon/compliance-lecture-style/tree/main/tools). It runs the whole 348-lecture corpus in seconds. **It is offered for adoption rather than as something to maintain separately**; see [§ What's being asked](#whats-being-asked).

## What is mechanically checkable

| Category | Checked | Not checked |
|----------|--------:|-------------|
| Writing | 4 / 8 | `qe-writing-002`, `-003`, `-005`, `-007` |
| Math | 8 / 9 | `qe-math-009` |
| Code | 5 / 6 | `qe-code-001` |
| Figures | 11 / 11 | — |
| References | 1 / 1 | — |
| Links | 2 / 2 | — |
| Admonitions | 5 / 5 | — |
| Proposed (#18) | 5 / 7 | `qe-math-014`, `qe-math-015` |
| **Total** | **41 / 49** | **8** |

The 7 `qe-jax-*` rules are out of scope for this corpus (they target `lecture-jax`), so the in-scope registry denominator is 42, not 49.

## Measured reach, 348 lectures

Prioritisation by corpus frequency, from `lectures/data/rule_reach.csv` at a pinned snapshot (one commit per series):

| Rule | Lectures | Occurrences |
|------|---------:|------------:|
| `qe-fig-005` — figures without a `name:` | 273 / 348 | 1,115 |
| `qe-writing-008` — repeated spaces | 237 | 7,044 |
| `qe-fig-001` — unnecessary `figsize=` | 224 | 892 |
| `qe-fig-008` — missing `lw=2` | 216 | 1,382 |
| `qe-writing-001` — one sentence per paragraph | 173 | 442 |
| `qe-fig-003` — embedded matplotlib titles | 165 | 630 |
| `qe-writing-006` — Title Case in H2+ headings | 146 | 781 |
| `qe-math-002` — `'` / `^T` for transpose | 122 | 2,129 |
| `qe-ref-001` — `{cite}` vs `{cite:t}` | 110 | 298 |
| `qe-code-002` — Greek spelled out in code | 106 | 579 |
| `qe-math-010` *(proposed)* — `\mathbb{E}` with braces | 105 | 1,167 |
| `qe-writing-004` — capitalised common nouns | 105 | 339 |

Six checked rules have **zero** hits corpus-wide, which is a result rather than a gap: `qe-admon-001`, `qe-admon-004`, `qe-admon-005`, `qe-code-006`, `qe-fig-009`, `qe-fig-011`. All 244 proof-family directives in the corpus carry the `prf:` prefix, for instance.

## Two findings that matter for the checker design

**1. Regex over the raw file is not enough — it needs a lexer.** Most wrong counts during development were structural, not pattern errors, and each corrupted several rules at once:

- `{math}` directive bodies (1,783 blocks in 172 lectures) look like code unless typed as maths. Every math rule was blind to them and every code rule was reading LaTeX.
- Display math closed at the end of a content line (`… p}$$`), or wrapped in a blockquote (`> $$`), inverts a naive `$$` state machine and mistypes the rest of the file.
- Inline maths spanning a line break (`$N(0,\n\sigma^2)$`) is invisible to a line-oriented match, so its LaTeX reads as narrative.
- A gated `{exercise-start}` is a *marker*, not a container — its fence closes immediately and `{exercise-end}` is separate. Treating it as a container makes every later directive look nested.
- HTML comments are not published and should not be scanned.

**2. Precision needs adversarial sampling, not just a passing test.** Every check here was reviewed by opening at least ten flagged occurrences in the source and judging them against the rule text. Nineteen of the 41 needed fixing, several badly:

| Rule | False positives found | Cause |
|------|----------------------:|-------|
| `qe-fig-008` | 149 / 15 sampled | Multi-line `plot(...)` judged on its first line, missing `linewidth=2` two lines down |
| `qe-math-010` | 207 / 24 | Two branches double-counting; bare `E` matched `E` as a matrix name |
| `qe-fig-005` | 99 / 15 | Cells that only *define* a plotting helper counted as rendering |
| `qe-math-011` | 79 / 18 | `\mathcal{G}` is a sigma-algebra, not a distribution |
| `qe-fig-004` | 70 / 60 | LaTeX tokenised into words, so `$\bar\pi_t$` counted as five |
| `qe-fig-002` | 36 / 20 | Screenshots and photographs flagged as "should be code-generated" |
| `qe-writing-006` | 52 / 40 | Possessives (`Newton's`) and hyphenated surnames (`Gram-Schmidt`) defeated the proper-noun list |

A shipped checker with `qe-fig-008`'s original behaviour would have told authors to add `lw=2` to plots that already had it, 149 times. The full table, with the fix for each, is in [`tools/VERIFICATION.md`](https://github.com/QuantEcon/compliance-lecture-style/blob/main/tools/VERIFICATION.md).

Three checks remain deliberately heuristic and say so where they fire: `qe-writing-004` and `qe-writing-006` consult curated proper-noun and common-noun lists, and `qe-math-002` has to tell a transpose apostrophe from a derivative, and a `^T` transpose from a terminal date — `Y^T` is a data history in several lectures.

## A correction to this issue's earlier evidence

The original body cited [`lecture-python.myst/divergence_measures.md:134`](https://github.com/QuantEcon/lecture-python.myst/blob/main/lectures/divergence_measures.md#L134) as `\begin{align}` inside `$$`, a Tier-1 build-risk example for `qe-math-006`.

Checked mechanically, **there is no `align` inside `$$` anywhere in the 348-lecture corpus.** That line is a *bare* top-level `\begin{align}`, which MyST's amsmath extension handles. It is a convention outlier — 17 bare alignment blocks against 6,094 `$$` blocks and 1,783 `{math}` directives — but not a build breaker, and a checker should report the two shapes differently.

The genuine build-risk finding in the corpus is elsewhere: `lecture-python-programming/python_by_example.md:499` and `:549` have `{exercise-start}` fences that are never closed, each swallowing the rest of its exercise including a nested `{hint}` at the same tick count. Those are the only two malformed gated directives in roughly 690.

## Labelled test data

`lectures/data/violations.csv` is per-lecture, per-rule counts with line numbers, at a pinned commit per series — 348 lectures across 7 categories. That is a regression fixture set, not a prose summary:

```csv
series,lecture,rule,count,proposed,build_risk
lecture-dp,lqcontrol,qe-math-002,85,0,0
lecture-dp,lqcontrol,qe-math-003,17,0,0
```

Useful as:

- **Regression corpus** — run a candidate check over the same commits and diff against these counts.
- **False-positive validation** — a lecture absent from a rule's rows should not fire.
- **Precision/recall measurement** per rule, per series.

`lectures/data/snapshot.json` pins the commits, so the fixtures are reproducible rather than approximate.

## What's being asked

1. Should Phase 4.3's scope be **41 rules** rather than ~13, using the measured prioritisation above?
2. Would the team rather **adopt `tools/qestyle_rules.py` and `qestyle_lex.py`** than reimplement? They are dependency-free Python, one function per rule, and the lexer is the part worth having. Maintaining them in a compliance ledger is the wrong home — this is a checker, and `action-style-guide` is where checkers live. Related: [#20](https://github.com/QuantEcon/action-style-guide/issues/20).
3. Should the corpus be ingested as test data — referenced by commit SHA, or vendored into `tests/fixtures/`?
4. Should the two genuine build-risk findings ship as their own small PR, separate from the larger Phase 4.3 effort?

## References

- **Compliance ledger (the tools, the data and the reports):** https://github.com/QuantEcon/compliance-lecture-style
- **Measured coverage (spec §9):** https://quantecon.github.io/compliance-lecture-style/spec.html
- **Detector verification:** [`tools/VERIFICATION.md`](https://github.com/QuantEcon/compliance-lecture-style/blob/main/tools/VERIFICATION.md)
- **Existing Phase 4.3:** [`docs/developer/roadmap.md`](https://github.com/QuantEcon/action-style-guide/blob/main/docs/developer/roadmap.md), [`IMPROVEMENTS.md §2.C`](https://github.com/QuantEcon/action-style-guide/blob/main/IMPROVEMENTS.md)
