# QuantEcon Lecture Style Compliance

A standing record of how the QuantEcon lecture corpus conforms to the style guide, scored
against 7 rule categories from the
[`action-style-guide`](https://github.com/QuantEcon/action-style-guide) registry. Each
pass re-measures the whole corpus and updates this record in place: the scores and
findings here are the **2026-08** pass, with the change since the previous pass, 2026-05,
measured alongside them.

This page is for triage — *where should we put our attention?* Start here, then open a
[series report](#where-to-focus-first) for the detail, the [charts](charts.md) for a
visual overview, or the [full findings](details.md) for the complete breakdown.

---

## Where to focus first

Series ranked worst → best. **Needs work** counts the HIGH + MEDIUM lectures; the rest
are LOW or NONE.

<!-- qe:focus -->
| Attention | Series | Score | Needs work | Weakest categories |
|-----------|--------|-------|-----------|--------------------|
| 🔴 **High** | [lecture-python-advanced.myst](lecture-python-advanced.myst/index.md) | 7.4 | 43 / 68 | Writing (4.6), Math (5.8) |
| 🔴 **High** | [lecture-python.myst](lecture-python.myst/index.md) | 7.7 | 82 / 145 | Writing (4.5), Figures (6.5) |
| 🔴 **High** | [lecture-dp](lecture-dp/index.md) | 7.7 | 34 / 52 | Writing (4.7), Figures (6.4) |
| 🔴 **High** | [lecture-python-programming](lecture-python-programming/index.md) | 8.0 | 20 / 27 | Writing (4.1), Figures (7.3) |
| 🟠 **Some** | [lecture-python-intro](lecture-python-intro/index.md) | 8.1 | 19 / 56 | Writing (5.2), Figures (6.5) |
<!-- /qe:focus -->

**Every HIGH-priority lecture in this pass is HIGH because a category fell below the bar,
not because of a low overall score** — all 197 of them, while no lecture in the corpus has
an overall score at or below 5.0. So the useful triage question is not *which lectures* but
*which category*: Writing is the binding constraint, at or below the floor in 176 of the 197
HIGH lectures against Math's 64 and Figures' 20. Fix a category across a series and a large
block of HIGH lectures clears at once.

---

## The biggest wins

Fix one of these *once* and it lifts dozens of lectures. Ordered by reach.

<!-- qe:wins -->
| Fix this | What it means | Lectures helped | Effort |
|----------|---------------|-----------------|--------|
| **Name your figures** | Add a `name:` so figures can be cross-referenced with `numref` | **273** | 🔧 |
| **Collapse double spaces** | Reduce runs of spaces between words to one | **237** | 🔧 |
| **Figure sizes** | Drop `figsize=` overrides — let the site defaults apply | **224** | 🔧 |
| **Line widths** | Pass `lw=2` on line plots for consistent weight | **196** | 🔧 |
| **Plot titles → captions** | Move `ax.set_title(...)` out of the plot into the figure caption | **165** | ✋ |
| **Heading capitalization** | Section headings → sentence case (first word + proper nouns only) | **132** | 🔧 |
| **Expectation notation** *(proposed)* | Use `\mathbb{E}` / `\mathbb{P}` / `\mathbb{V}` with braces | **124** | 🔧 |
| **Narrative citations** | Use `{cite:t}` where the author name is part of the sentence | **106** | ✋ |

Reach is out of 348 lectures. 🔧 = scriptable sweep · ✋ = needs a human pass.
<!-- /qe:wins -->

The mechanical sweeps at the top of that list touch most of the corpus and need no
judgment — they are the highest-leverage place to start. The
[remediation plan](details.md#remediation-plan) has the ordered list and the exact
lectures.

---

## Fix immediately ⚠️

Four findings are structural rather than stylistic — they change what the build
produces, so they are worth fixing regardless of the broader effort.

| Where | Problem | Why it matters |
|-------|---------|----------------|
| [`lecture-python-programming` · `python_by_example.md:499` and `:549`](https://github.com/QuantEcon/lecture-python-programming/blob/main/lectures/python_by_example.md#L499) | Two `{exercise-start}` fences are never closed, so the directive swallows the rest of the exercise, including a nested `{hint}` at the same tick count (`qe-admon-003`) | These are the only two malformed gated directives in 690 across the corpus. The exercise and its hint do not render as intended. |
| [`lecture-python.myst` · `cross_product_trick.md:133`](https://github.com/QuantEcon/lecture-python.myst/blob/main/lectures/cross_product_trick.md#L133) | `` {eq}`eq:Kalman102} `` — mismatched braces, and the label is attached to a bare `align*` block that carries no label | The cross-reference silently fails to render. |
| [`lecture-dp` · `cross_product_trick.md:133`](https://github.com/QuantEcon/lecture-dp/blob/main/lectures/cross_product_trick.md#L133) | The same defect — `lecture-dp` syncs this lecture from `lecture-python.myst` | Fixing it upstream fixes both. |
| [`lecture-python.myst` · `ifp_advanced.md:158`](https://github.com/QuantEcon/lecture-python.myst/blob/main/lectures/ifp_advanced.md#L158) (and the `lecture-dp` copy) | Raw LaTeX `\label{a:y0}` inside a `$$` block (`qe-math-007`) | MyST does not resolve `\label`; the equation cannot be referenced with `` {eq}` ` ``. |

```{note}
**A correction to the previous pass.** It reported `divergence_measures.md:134` as
`\begin{align}` inside a `$$ … $$` block that "breaks the PDF build". Re-checked
mechanically against the pinned snapshot, **there is no `align` inside `$$` anywhere in
the corpus** — not in that file and not in any of the other 347 lectures. The block at
that line is a *bare* top-level `\begin{align}`, which MyST's amsmath extension handles.
It is still a convention outlier — 17 bare alignment blocks against 6,094 `$$` blocks and
1,783 `{math}` directives — and it is reported under `qe-math-006` as such, but it is not
the build breaker the earlier report described.
```

---

## What changed since the previous pass

The same checks were run over both corpus snapshots, so the comparison is a measurement
of the lectures rather than of the method. See the
[trend chart](charts.md#change-since-the-previous-pass) for every rule.

The corpus grew from 300 to 348 lectures. Of the 35 rules measurable in both snapshots,
**26 improved as a share of the corpus, 5 held level and 4 got worse.** The four largest
improvements and all four regressions:

| Direction | Rule | Share of corpus |
|-----------|------|-----------------|
| 🟢 Improving | `qe-writing-008` — remove excessive whitespace between words | 78% → 68% |
| 🟢 Improving | `qe-writing-006` — capitalize lecture titles properly | 47% → 38% |
| 🟢 Improving | `qe-fig-008` — figure-directive option conventions | 62% → 56% |
| 🟢 Improving | `qe-writing-001` — use one sentence per paragraph | 55% → 50% |
| 🔴 Worsening | `qe-fig-004` — caption formatting conventions | 9% → 17% |
| 🔴 Worsening | `qe-fig-001` — do not set figure size unless necessary | 62% → 64% |
| 🔴 Worsening | `qe-fig-003` — no matplotlib embedded titles | 46% → 47% |
| 🔴 Worsening | `qe-code-002` — use unicode Greek letters in code | 18% → 19% |

Three of the four regressions are in Figures, for the same reason: new lectures add figures
faster than the figure conventions are applied to them. Only `qe-fig-004` moved materially
— it doubled because the newer lectures do add captions, which is progress, but write them
in Title Case and over the six-word limit. The other two drifted by under three points.

`qe-code-002` is the one to read carefully, because it moved by a single point and only
after the check was widened mid-pass to see a Greek name carrying an English prefix
(`target_mu`, `c_gamma`). Both snapshots were re-measured with that wider check, so the
comparison is still like for like — but the honest reading is that this rule was *always*
drifting slightly and the pass could not see it until the last day. The reach it reports
now, 66 of 348 lectures, is four times what the pass first measured.

---

## How this pass was measured

41 of the 49 rules — 36 of the 42 in-scope registry rules plus 5 of the 7 proposed — are
checked by program, over a **pinned corpus snapshot**: one commit
per series, recorded in every report header and in
[`lectures/data/snapshot.json`](https://github.com/QuantEcon/compliance-lecture-style/blob/main/lectures/data/snapshot.json).
Scores and priority buckets are then derived arithmetically from the rubric. The 8
judgment-only rules are reviewed by reading. [Spec §8](spec.md) describes the layers and
why they are separate; [§9](spec.md) lists exactly which rules fall where.

That matters for reading the numbers: a category scoring 10 means *no mechanical
violation was measured in it*, not that a human declared it perfect.

<!-- qe:review-coverage -->
```{note}
**Every one of the 348 lectures has been through the judgment layer**, so the scores
below are comparable across series and the cross-series comparison stands on its own.
Per-series coverage is still published on each series' Summary page, and the
*within-series* ranking and the rule-reach numbers were always sound — those are
measured over the whole corpus by the same code. This retires the caveat tracked in
[audit.2026-05.style-guide#5](https://github.com/QuantEcon/audit.2026-05.style-guide/issues/5).
```

```{warning}
**Score levels are not comparable with the previous period, which is why the trend above
is reported on rule reach and not on scores.** The 2026-08 row of `history.csv` folds a
judgment overlay into **348 of 348** lectures; the 2026-05 row folds one into **0 of
300** (the `reviewed` column). A lecture assessed against more rules scores lower, so
the published corpus mean moved 8.2 → 7.7, Writing 6.6 → 4.6 and the HIGH count 102 →
197 — movement that is the judgment layer landing on one period and not the other, not
the lectures changing. Like for like — the evidence layer alone, measured identically
over both snapshots and recorded in `history_mechanical.csv` — the corpus moved 8.2 →
8.4 overall, Writing 6.6 → 7.1 and HIGH 102 → 85 lectures. Compare score levels across
periods only where the `reviewed` column agrees, or use the like-for-like table; never
read the published columns as a trend across a coverage change.
```
<!-- /qe:review-coverage -->

---

## Navigating this report

- **Series reports** (sidebar) — per-series detail: scores, ranked lectures, and every
  lecture's own report. *Start here once you've picked a series above.*
- **[Charts](charts.md)** — heatmap, rule reach, the cross-pass trend, priority mix.
- **[Full findings](details.md)** — the complete scoreboard, every recurring rule, every
  HIGH lecture, and the remediation plan.
- **[Scoring rubric](spec.md)** — the rubric, the pass methodology, and the measured
  deterministic coverage.
- **[Appendix — feedback](appendix.md)** — what these passes fed back to the style guide
  and `action-style-guide` (proposed rules and tooling, issues #18–#21).

> Rules are cited by their `action-style-guide` IDs (e.g. `qe-fig-001`). Seven are tagged
> **(proposed)** — documented in the style guide but not yet in the rule registry
> ([issue #18](https://github.com/QuantEcon/action-style-guide/issues/18)).
