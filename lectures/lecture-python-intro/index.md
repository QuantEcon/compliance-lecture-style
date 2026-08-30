# Summary

Style audit of the **lecture-python-intro** series.

<!-- qe:series-meta -->
- **Audit date:** 2026-08-23
- **Corpus snapshot:** `a12d17c0ef`
- **Lectures audited:** 56
- **Average overall score:** 8.1 / 10
- **Average per-category scores:** writing 5.2, math 8.6, code 7.3, figures 6.5, references 9.3, links 9.7, admon 10.0
- **JAX:** out of scope — the `qe-jax-*` rules target `lecture-jax`.
- **Judgment-review coverage:** all lectures reviewed.
<!-- /qe:series-meta -->

<!-- qe:series-narrative -->
**Writing, at 5.2, is the weakest category here, and it is very nearly the whole HIGH
list.** Eighteen of the 19 HIGH lectures are HIGH only because Writing sits at or below the
≤ 4 floor; the nineteenth, `markov_chains_I`, is floored by Math (3.0) instead. Three of
the 18 — `geom_series`, `french_rev` and `eigen_I` — are also floored by Figures, and no
lecture in the series is floored by Code, References, Links or Admonitions at all.

Underneath Writing are four rules, and no single one of them accounts for a lecture.
`qe-writing-008` (39 / 56, 709 occurrences of repeated spaces) is the largest raw count and
the only one that sweeps cleanly, but every one of the 18 floored lectures also breaks at
least one rule that has to be read: `qe-writing-001` (30 / 56) in 16 of them,
`qe-writing-006` (13 / 56) in 11, `qe-writing-004` (18 / 56) in 9. Across the 18 that is 85
hand-edited sites, against 338 whitespace occurrences a script handles. The 2026-05 pass,
done by reading, put Writing at 7.5 here and left Figures as the weakest category; corpus
Writing moved 6.6 → 4.6 over the same interval, so the reordering is not particular to this
series.

By every other measure this is the strongest series in the corpus: the highest overall (8.1
against 7.7), the smallest share of HIGH lectures (19 of 56, against 197 of 348), nothing
below 7.2 — only `lecture-python-programming` also has no lecture under 7.0 — and neither a
build-risk violation nor any of the corpus's four structural findings. Math especially is
not the problem: 8.6, second only to `lecture-python-programming`, against 7.0 corpus-wide,
with `qe-math-002` (4 / 56, 13 occurrences) where `lecture-python-advanced.myst` has it in
20 of its 68. Figures (6.5) sits exactly on the corpus mean and Code (7.3) just under it.
<!-- /qe:series-narrative -->

## Priority distribution

<!-- qe:series-priority -->
| Priority | Count | % |
|----------|-------|---|
| HIGH     | 19    | 33.9% |
| MEDIUM   | 0     | 0.0% |
| LOW      | 28    | 50.0% |
| NONE     | 9     | 16.1% |
<!-- /qe:series-priority -->

## Top systemic issues across the series

Ranked by how many of the series' lectures each rule reaches.

<!-- qe:series-systemic -->
1. **`qe-fig-005`** — Descriptive figure names for cross-referencing — **46 / 56** lectures, 174 occurrences.
2. **`qe-writing-008`** — Remove excessive whitespace between words — **39 / 56** lectures, 709 occurrences.
3. **`qe-fig-008`** — Use lw=2 for line charts — **35 / 56** lectures, 217 occurrences.
4. **`qe-fig-001`** — Do not set figure size unless necessary — **30 / 56** lectures, 91 occurrences.
5. **`qe-writing-001`** — Use one sentence per paragraph — **30 / 56** lectures, 54 occurrences.
6. **`qe-writing-004`** — Avoid unnecessary capitalization in narrative text — **18 / 56** lectures, 40 occurrences.
7. **`qe-fig-004`** — Caption formatting conventions — **17 / 56** lectures, 72 occurrences.
8. **`qe-fig-003`** — No matplotlib embedded titles — **15 / 56** lectures, 36 occurrences.
9. **`qe-ref-001`** — Use correct citation style — **15 / 56** lectures, 48 occurrences.
10. **`qe-writing-006`** — Capitalize lecture titles properly — **13 / 56** lectures, 31 occurrences.
<!-- /qe:series-systemic -->

## Clean across the series

Checked rules with no violation anywhere in the series — the conventions this series
already holds to.

<!-- qe:series-clean -->
- **`qe-admon-003`** — Use tick count management for nested directives
- **`qe-code-005`** — Use quantecon timeit for benchmarking
- **`qe-fig-010`** — Plotly figures require latex directive
- **`qe-math-006`** — Use aligned environment correctly for PDF compatibility
- **`qe-math-007`** — Use automatic equation numbering, not manual tags
- **`qe-math-008`** — Explain special notation (vectors/matrices)
- **`qe-math-013`** *(proposed)* — Reference equations via `` {eq}`label` ``
<!-- /qe:series-clean -->

## Series-level recommendations

<!-- qe:series-recommendations -->
1. **`qe-writing-008` — collapse repeated spaces** (39 / 56, 709 occurrences). Free and
   scriptable, so do it first; 338 of the occurrences are inside the 18 Writing-floored
   lectures, 89 of them in `french_rev` alone. On its own it clears no HIGH lecture — each
   of the 18 also breaks a rule that needs reading.
2. **`qe-writing-006` — sentence-case the headings** (13 / 56, 31 headings). The best ratio
   of floored lectures reached to work done in the series: it reaches 11 of the 18, and 29
   of the 31 headings are in those 11. Scriptable, but the check is heuristic and leans on
   a curated proper-noun list, so read the diff before committing it.
3. **`qe-writing-004` — drop the mid-sentence capitals** (18 / 56, 40 sites). Reaches 9 of
   the 18, concentrated in `time_series_with_matrices` (7 sites) and `eigen_I` (5). Same
   heuristic caveat, and small enough to check by hand.
4. **`qe-writing-001` — one sentence per paragraph** (30 / 56, 54 blocks). The largest
   single blocker — 16 of the 18 — but a reading pass rather than a sweep, because
   splitting a paragraph changes its rhythm. 31 of the 54 blocks sit in the floored
   lectures.
5. **Take the floored lectures cheapest first.** On top of the sweeps,
   `observed_distributions` and `laffer_adaptive` need one hand-edited site each,
   `msy_fishery` two (and no whitespace work at all), then `cagan_ree`, `networks`,
   `solow`, `tax_smooth`, `unpleasant` and `greek_square` at three each. The tail is
   `time_series_with_matrices` (9 sites), `complex_and_trig` (8) and `french_rev` (8).
6. **`qe-fig-005` — name the figures** (46 / 56, 174 figures). The widest-reaching rule in
   the series, a pure sweep, and it unlocks `{numref}` cross-referencing — but it lifts the
   series average, not the HIGH list. The three Figures floors are `geom_series`,
   `french_rev` and `eigen_I`; `qe-fig-005` is only 14 of their 135 figure findings, and
   all three are floored by Writing regardless. `qe-fig-008` (35 / 56, 217 calls) and
   `qe-fig-001` (30 / 56, 91 overrides) are the same kind of item: broad, cheap, no effect
   on priority.
7. **`markov_chains_I` — the one Math floor** (3.0). 22 of its 23 math findings are
   `qe-math-004` (4 / 56, 15 occurrences) and `qe-math-010` *(proposed)* (8 / 56, 100 occurrences),
   and the latter is still a proposed rule rather than a registry one. So this lecture's
   priority turns partly on
   [`action-style-guide` #18](https://github.com/QuantEcon/action-style-guide/issues/18);
   `qe-math-004` is worth doing either way.
8. **Do the work upstream, in `QuantEcon/lecture-python-intro`.** This repository only
   measures. One file needs care about where the edit lands: `short_path` is byte-identical
   with the `lecture-dp` copy at this snapshot, so fixing it once clears both series. It is
   the only substantive shared file here — `status` and `zreferences` also match another
   series byte for byte but are boilerplate, while `lake_model`, `lln_clt` and `mle` share
   a filename with `lecture-python.myst` and have diverged, so each of those copies needs
   its own edit.
<!-- /qe:series-recommendations -->

## Lectures ranked by priority (lowest score first)

Scores are 0–10 per category; **Overall** is the mean of the in-scope categories, and
**Priority** follows [spec §4](../spec.md). A dash means the category is not applicable to
that lecture. Click a lecture for its full report.

<!-- qe:series-ranked -->
| # | Lecture | Writing | Math | Code | Figures | References | Links | Admon | Overall | Priority |
|---|---------|---|---|---|---|---|---|---|---------|----------|
| 1 | [geom_series](geom_series.md) | 3 | 8.5 | 7.5 | 4 | — | 10 | 10 | **7.2** | HIGH |
| 2 | [linear_equations](linear_equations.md) | 5.5 | 6.5 | 7.5 | 6 | — | 7.5 | 10 | **7.2** | LOW |
| 3 | [networks](networks.md) | 4 | 6 | 7 | 5 | 8.5 | 10 | 10 | **7.2** | HIGH |
| 4 | [french_rev](french_rev.md) | 3 | 10 | 7.5 | 3 | 7.5 | 10 | 10 | **7.3** | HIGH |
| 5 | [eigen_I](eigen_I.md) | 3.5 | 10 | 7.5 | 3.5 | — | 10 | 10 | **7.4** | HIGH |
| 6 | [heavy_tails](heavy_tails.md) | 6 | 5.5 | 6 | 5 | 10 | 9 | 10 | **7.4** | LOW |
| 7 | [inflation_history](inflation_history.md) | 3 | 10 | 6 | 4.5 | 8.5 | 10 | 10 | **7.4** | HIGH |
| 8 | [markov_chains_I](markov_chains_I.md) | 6 | 3 | 7 | 7.5 | 9 | 9 | 10 | **7.4** | HIGH |
| 9 | [time_series_with_matrices](time_series_with_matrices.md) | 3 | 6 | 7.5 | 7 | 10 | 8 | 10 | **7.4** | HIGH |
| 10 | [business_cycle](business_cycle.md) | 6 | — | 7 | 7 | — | 10 | — | **7.5** | LOW |
| 11 | [bivariate_dist](bivariate_dist.md) | 6.5 | 5.5 | 6 | 5 | 10 | 10 | 10 | **7.6** | LOW |
| 12 | [mobility](mobility.md) | 4.5 | 6 | 8.5 | 7.5 | 7 | 10 | 10 | **7.6** | LOW |
| 13 | [greek_square](greek_square.md) | 4 | 7.5 | 7 | 6.5 | 9 | 10 | 10 | **7.7** | HIGH |
| 14 | [monte_carlo](monte_carlo.md) | 5.5 | 5 | 7.5 | 8 | — | 10 | 10 | **7.7** | LOW |
| 15 | [inequality](inequality.md) | 4 | 9 | 6.5 | 5 | 10 | 10 | 10 | **7.8** | HIGH |
| 16 | [intro_supply_demand](intro_supply_demand.md) | 4.5 | 10 | 7.5 | 6.5 | — | 8 | 10 | **7.8** | LOW |
| 17 | [lln_clt](lln_clt.md) | 8 | 4.5 | 7.5 | 8 | — | 9 | 10 | **7.8** | LOW |
| 18 | [long_run_growth](long_run_growth.md) | 5 | — | 7.5 | 6 | 8.5 | 10 | 10 | **7.8** | LOW |
| 19 | [simple_linear_regression](simple_linear_regression.md) | 4.5 | 8.5 | 7.5 | 6.5 | — | 10 | 9.5 | **7.8** | LOW |
| 20 | [solow](solow.md) | 4 | 8 | 7 | 8 | — | 10 | 10 | **7.8** | HIGH |
| 21 | [tax_smooth](tax_smooth.md) | 3 | 9.5 | 6 | 6 | 10 | 10 | 10 | **7.8** | HIGH |
| 22 | [ar1_processes](ar1_processes.md) | 6 | 7.5 | 6 | 7 | 9 | 10 | 10 | **7.9** | LOW |
| 23 | [complex_and_trig](complex_and_trig.md) | 3 | 9.5 | 7 | 5.5 | 10 | 10 | 10 | **7.9** | HIGH |
| 24 | [equalizing_difference](equalizing_difference.md) | 5 | 8 | 7.5 | 5.5 | 9 | 10 | 10 | **7.9** | LOW |
| 25 | [laffer_adaptive](laffer_adaptive.md) | 4 | 10 | 7 | 6 | 8.5 | 10 | 10 | **7.9** | HIGH |
| 26 | [lake_model](lake_model.md) | 4.5 | 10 | 7.5 | 5.5 | — | 10 | 10 | **7.9** | LOW |
| 27 | [money_inflation_nonlinear](money_inflation_nonlinear.md) | 3 | 9.5 | 6.5 | 6.5 | 10 | 10 | 10 | **7.9** | HIGH |
| 28 | [olg](olg.md) | 4.5 | 9.5 | 7 | 6.5 | 10 | 8 | 10 | **7.9** | LOW |
| 29 | [prob_dist](prob_dist.md) | 5 | 7 | 7 | 8.5 | — | 10 | 10 | **7.9** | LOW |
| 30 | [unpleasant](unpleasant.md) | 3.5 | 8 | 7.5 | 6 | 10 | 10 | 10 | **7.9** | HIGH |
| 31 | [lp_intro](lp_intro.md) | 3.5 | 6.5 | 7.5 | 8.5 | 10 | 10 | 10 | **8.0** | HIGH |
| 32 | [msy_fishery](msy_fishery.md) | 3.5 | 10 | 6 | 6.5 | 10 | 10 | 10 | **8.0** | HIGH |
| 33 | [supply_demand_multiple_goods](supply_demand_multiple_goods.md) | 4.5 | 9.5 | 6.5 | 7.5 | — | 10 | 10 | **8.0** | LOW |
| 34 | [cons_smooth](cons_smooth.md) | 4.5 | 10 | 7.5 | 6 | 9 | 10 | 10 | **8.1** | LOW |
| 35 | [cagan_adaptive](cagan_adaptive.md) | 5 | 10 | 7 | 6.5 | 9 | 10 | 10 | **8.2** | LOW |
| 36 | [mle](mle.md) | 5 | 10 | 7 | 7.5 | — | 10 | 10 | **8.2** | LOW |
| 37 | [money_inflation](money_inflation.md) | 4.5 | 9.5 | 7.5 | 6 | 10 | 10 | 10 | **8.2** | LOW |
| 38 | [scalar_dynam](scalar_dynam.md) | 4.5 | 10 | 6 | 8.5 | — | 10 | 10 | **8.2** | LOW |
| 39 | [supply_demand_heterogeneity](supply_demand_heterogeneity.md) | 4.5 | 9.5 | 7 | — | — | 10 | 10 | **8.2** | LOW |
| 40 | [pv](pv.md) | 4.5 | 10 | 8.5 | 7 | — | 10 | 10 | **8.3** | LOW |
| 41 | [eigen_II](eigen_II.md) | 4.5 | 9.5 | 7.5 | — | 9 | 10 | 10 | **8.4** | LOW |
| 42 | [markov_chains_II](markov_chains_II.md) | 6.5 | 10 | 7.5 | 6.5 | 8.5 | 10 | 10 | **8.4** | LOW |
| 43 | [observed_distributions](observed_distributions.md) | 4 | 10 | 7.5 | 7 | 10 | 10 | 10 | **8.4** | HIGH |
| 44 | [about](about.md) | 8 | — | — | — | — | 9 | — | **8.5** | LOW |
| 45 | [cagan_ree](cagan_ree.md) | 4 | 10 | 8.5 | 7 | 10 | 10 | 10 | **8.5** | HIGH |
| 46 | [input_output](input_output.md) | 7.5 | 10 | 7.5 | 6 | 8.5 | 10 | 10 | **8.5** | LOW |
| 47 | [short_path](short_path.md) | 5.5 | 10 | 7.5 | 8 | — | 10 | 10 | **8.5** | LOW |
| 48 | [schelling](schelling.md) | 5 | 10 | 7 | 9 | 10 | 9 | 10 | **8.6** | NONE |
| 49 | [bayes_intro](bayes_intro.md) | 7.5 | 9.5 | 10 | 5.5 | — | 10 | 10 | **8.8** | NONE |
| 50 | [cobweb](cobweb.md) | 7.5 | 10 | 7.5 | 6.5 | 10 | 10 | 10 | **8.8** | NONE |
| 51 | [troubleshooting](troubleshooting.md) | 8.5 | — | — | 9 | — | 9 | — | **8.8** | NONE |
| 52 | [commod_price](commod_price.md) | 7.5 | 10 | 9 | 8 | 10 | 10 | 10 | **9.2** | NONE |
| 53 | [fitting_distributions](fitting_distributions.md) | 6.5 | 10 | 10 | 8.5 | — | 10 | 10 | **9.2** | NONE |
| 54 | [intro](intro.md) | 10 | — | — | — | — | 10 | — | **10.0** | NONE |
| 55 | [status](status.md) | 10 | — | — | — | — | 10 | — | **10.0** | NONE |
| 56 | [zreferences](zreferences.md) | 10 | — | — | — | — | 10 | — | **10.0** | NONE |
<!-- /qe:series-ranked -->
