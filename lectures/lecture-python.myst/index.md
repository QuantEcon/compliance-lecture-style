# Summary

Style audit of the **lecture-python.myst** series.

<!-- qe:series-meta -->
- **Audit date:** 2026-08-24
- **Corpus snapshot:** `e25fdf2345`
- **Lectures audited:** 145
- **Average overall score:** 7.7 / 10
- **Average per-category scores:** writing 4.5, math 7.0, code 7.6, figures 6.5, references 9.5, links 9.8, admon 10.0
- **JAX:** out of scope — the `qe-jax-*` rules target `lecture-jax`.
- **Judgment-review coverage:** all lectures reviewed.
<!-- /qe:series-meta -->

<!-- qe:series-narrative -->
**Writing is the binding constraint.** At 4.5 it is the weakest of the seven categories —
as it was in 2026-05, when it scored 5.9 — and it is now at or below the 4-point floor in
**72 of the 81 HIGH lectures**. Math floors 26 and Figures 8; Code, References, Links and
Admonitions floor none. In **49** of the 81, Writing is the *only* floored category, so a
Writing pass is the one action that can clear more than half this series' HIGH list on its
own. Two very different jobs sit under it. `qe-writing-006` (sentence case below H1, the
highest-weighted Writing rule) appears in 59 of the 72 and `qe-writing-008` (runs of extra
whitespace, the lowest-weighted) in 60, and both are mechanical; but 57 of the 72 also
carry `qe-writing-001` or `qe-writing-004`, which want an editor rather than a script.

At 145 lectures this series is 42 % of the corpus and holds 81 of its 197 HIGH lectures,
and it scores like the corpus largely because it *is* the corpus: overall 7.7 against 7.7,
math 7.0 against 7.0, figures 6.5 against 6.5. The floor proportions match too — Writing
89 %, Math 32 %, Figures 10 % of the HIGH list, the same three shares as corpus-wide. The
extremes are what distinguish it. `cross_product_trick` at **5.5** is the lowest-scoring
lecture in all 348, and `qe-writing-008` at **2,569 occurrences across 89 lectures** is the
largest count of any rule in any series — 36 % of the corpus total for that rule, with
`ak2` alone at 197. Math and Figures both edged up since 2026-05 (6.6 → 7.0 and 6.3 → 6.5)
while Writing fell 1.4 points; the series grew from 110 lectures to 145 over the same
interval, so part of that movement is composition rather than regression.

**A caveat this series shares with `lecture-dp`.** 31 of these 145 filenames also exist in
`lecture-dp`, which syncs them from here; 16 of the 31 are HIGH here and 15 are HIGH in
both. Only **6 are byte-identical** at this snapshot (`cross_product_trick`,
`ifp_discrete`, `ifp_opi`, `lq_inventories`, `mccall_model_with_separation`,
`os_numerical`) — for those, this repo is where a fix belongs and both copies clear. The
other 25 share an origin and have since diverged, so the same defect usually appears in
both but each copy needs its own edit. Whether the corpus totals should de-duplicate the 6
is open as
[compliance-lecture-style#3](https://github.com/QuantEcon/compliance-lecture-style/issues/3).
<!-- /qe:series-narrative -->

## Priority distribution

<!-- qe:series-priority -->
| Priority | Count | % |
|----------|-------|---|
| HIGH     | 81    | 55.9% |
| MEDIUM   | 1     | 0.7% |
| LOW      | 46    | 31.7% |
| NONE     | 17    | 11.7% |
<!-- /qe:series-priority -->

## Top systemic issues across the series

Ranked by how many of the series' lectures each rule reaches.

<!-- qe:series-systemic -->
1. **`qe-fig-005`** — Descriptive figure names for cross-referencing — **110 / 145** lectures, 446 occurrences.
2. **`qe-fig-001`** — Do not set figure size unless necessary — **107 / 145** lectures, 462 occurrences.
3. **`qe-writing-008`** — Remove excessive whitespace between words — **89 / 145** lectures, 2569 occurrences.
4. **`qe-fig-003`** — No matplotlib embedded titles — **79 / 145** lectures, 329 occurrences.
5. **`qe-writing-006`** — Capitalize lecture titles properly — **71 / 145** lectures, 410 occurrences.
6. **`qe-fig-008`** — Use lw=2 for line charts — **69 / 145** lectures, 393 occurrences.
7. **`qe-writing-001`** — Use one sentence per paragraph — **65 / 145** lectures, 165 occurrences.
8. **`qe-math-010`** *(proposed)* — Blackboard \mathbb{P}, \mathbb{E}, \mathbb{V} with braces — **60 / 145** lectures, 689 occurrences.
9. **`qe-writing-004`** — Avoid unnecessary capitalization in narrative text — **43 / 145** lectures, 148 occurrences.
10. **`qe-ref-001`** — Use correct citation style — **36 / 145** lectures, 105 occurrences.
<!-- /qe:series-systemic -->

## Clean across the series

Checked rules with no violation anywhere in the series — the conventions this series
already holds to.

<!-- qe:series-clean -->
- **`qe-admon-002`** — Use dropdown class for solutions
- **`qe-admon-003`** — Use tick count management for nested directives
<!-- /qe:series-clean -->

## Series-level recommendations

<!-- qe:series-recommendations -->
1. **`qe-writing-006` — sentence-case the headings below H1** (71 / 145, 410 headings).
   The highest-weighted Writing rule in the spec, and present in 59 of the 72
   Writing-floored lectures — the best return per heading edited. Scriptable against the
   curated proper-noun list in `tools/qestyle_rules.py`, but that list is heuristic, so
   read the diff before it lands. `linear_models` (25), `markov_asset` and
   `linear_algebra` (18 each) are the densest.
2. **`qe-writing-008` — collapse repeated spaces** (89 / 145, 2,569 occurrences). The
   largest count of any rule in any series in the corpus, and present in 60 of the 72. It
   is the *lowest*-weighted Writing rule, so it moves a score less than its size suggests
   — but it is entirely safe to automate, which is why it ranks here rather than lower.
   `ak2` holds 197 of them and `var_dmd` 180.
3. **`qe-writing-001` and `qe-writing-004`** (65 / 145, 165 blocks; 43 / 145, 148 words).
   Reading passes rather than sweeps: splitting a paragraph and deciding what is a proper
   noun both need an editor. Unavoidable, though — 57 of the 72 Writing-floored lectures
   carry one or the other, so items 1–2 alone will not lift them off the floor. Items 1–3
   together are the only route to the **49** lectures floored on Writing alone, and a
   precondition for the 23 floored on Writing plus something else.
4. **`qe-math-010` *(proposed)* — expectation and probability operators, with braces**
   (60 / 145, 689 occurrences). The largest Math finding, and present in 19 of the 26
   Math-floored lectures. A mechanical substitution, but it edits equations, so review it
   rather than running `sed` blind. `util_rand_resp` (113) and `prob_matrix` (81) dominate.
5. **`qe-math-004` — un-bold the vectors and matrices** (18 / 145, 509 occurrences) and
   **`qe-math-002` — `^\top` for transpose** (24 / 145, 494). Narrow and dense rather than
   broad: three lectures hold 370 of the 509 (`hansen_singleton_1983` 143, `lln_clt` 121,
   `mle` 106), and `linear_algebra` alone holds 114 of the 494. Good single sittings. With
   item 4 they cover the Math floor — of which only six lectures (`affine_risk_prices`,
   `hansen_singleton_1983`, `imp_sample`, `likelihood_bayes`, `likelihood_var`, `mle`) are
   floored on Math alone.
6. **The figure rules, for the average rather than the triage.** `qe-fig-005` — name the
   figures (110 / 145, 446 figures) and `qe-fig-001` — drop `figsize=` (107 / 145, 462
   overrides) are the two largest reaches in the series and pure sweeps, but Figures is the
   floor in only 8 lectures and just two of those (`ak_aiyagari`, `sargent_surico`) are
   floored on Figures alone. `qe-fig-003` — titles into captions (79 / 145, 329 calls) is a
   reading pass instead: each `ax.set_title(...)` becomes a caption someone has to write.
   `two_computation` (28) and `navy_captain` (20) are the heaviest.
7. **Two structural one-line fixes, independent of the HIGH list.**
   `cross_product_trick.md:133` has `` {eq}`eq:Kalman102} `` — mismatched braces, pointing
   at a bare `align*` block that carries no label — and `ifp_advanced.md:158` has a raw
   `\label{a:y0}` inside `$$`, which MyST does not resolve. Both change what the build
   produces, and both exist in the `lecture-dp` copies too.
8. **Sequence the sweeps here before `lecture-dp` runs its own**, and get the two proposed
   rules encoded upstream. This series is the sync source for the 31 shared filenames, so
   a fix landed in `lecture-dp` on one of the 6 byte-identical lectures is overwritten by
   the next sync; for the 25 diverged copies the sweeps have to run in both repos. And
   `qe-math-010` *(proposed)* (item 4) and `qe-writing-009` *(proposed)* (15 / 145, 27 occurrences) are scored here
   from the manual style guide but are not encoded in `action-style-guide` — they are
   proposed in [issue #18](https://github.com/QuantEcon/action-style-guide/issues/18).
   Sweeping 689 occurrences with nothing in CI to hold the line means measuring the same
   debt again next period.
9. **Start with the four lowest:** `cross_product_trick` (5.5, the corpus minimum),
   `qr_decomp` (5.9), `navy_captain` (6.0) and `two_auctions` (6.0). The first is
   byte-identical to its `lecture-dp` copy, so fixing it here clears both.
<!-- /qe:series-recommendations -->

## Lectures ranked by priority (lowest score first)

Scores are 0–10 per category; **Overall** is the mean of the in-scope categories, and
**Priority** follows [spec §4](../spec.md). A dash means the category is not applicable to
that lecture. Click a lecture for its full report.

<!-- qe:series-ranked -->
| # | Lecture | Writing | Math | Code | Figures | References | Links | Admon | Overall | Priority |
|---|---------|---|---|---|---|---|---|---|---------|----------|
| 1 | [cross_product_trick](cross_product_trick.md) | 3.5 | 3 | — | — | — | 10 | — | **5.5** | HIGH |
| 2 | [qr_decomp](qr_decomp.md) | 3 | 3 | 7.5 | — | — | 10 | — | **5.9** | HIGH |
| 3 | [navy_captain](navy_captain.md) | 3 | 6.5 | 7.5 | 3 | — | 10 | — | **6.0** | HIGH |
| 4 | [two_auctions](two_auctions.md) | 3 | 4.5 | 6.5 | 3 | 10 | 9 | — | **6.0** | HIGH |
| 5 | [likelihood_var](likelihood_var.md) | 4.5 | 3.5 | 7.5 | 5 | — | 10 | — | **6.1** | HIGH |
| 6 | [prob_matrix](prob_matrix.md) | 3 | 3 | 5.5 | 5 | — | 10 | 10 | **6.1** | HIGH |
| 7 | [two_computation](two_computation.md) | 5.5 | 3 | 6 | 3 | 10 | 10 | — | **6.2** | HIGH |
| 8 | [rs_inventory_q](rs_inventory_q.md) | 3 | 6.5 | 7.5 | 5 | — | 10 | — | **6.4** | HIGH |
| 9 | [linear_models](linear_models.md) | 3 | 3 | 6 | 8 | — | 9 | 10 | **6.5** | HIGH |
| 10 | [multivariate_normal](multivariate_normal.md) | 3 | 3 | 7.5 | 5.5 | — | 10 | 10 | **6.5** | HIGH |
| 11 | [perm_income_cons](perm_income_cons.md) | 3 | 4 | 7.5 | 5.5 | 10 | 9 | — | **6.5** | HIGH |
| 12 | [likelihood_ratio_process](likelihood_ratio_process.md) | 3 | 3 | 7 | 3.5 | 10 | 10 | 10 | **6.6** | HIGH |
| 13 | [lagrangian_lqdp](lagrangian_lqdp.md) | 3 | 3 | 7 | — | 10 | 7.5 | 10 | **6.8** | HIGH |
| 14 | [prob_meaning](prob_meaning.md) | 3 | 7.5 | 6 | 4.5 | — | 10 | 10 | **6.8** | HIGH |
| 15 | [ifp_advanced](ifp_advanced.md) | 3 | 3 | 7 | 7 | 8.5 | 10 | 10 | **6.9** | HIGH |
| 16 | [kalman_2](kalman_2.md) | 5 | 7.5 | 7.5 | 4.5 | — | 10 | — | **6.9** | MEDIUM |
| 17 | [linear_algebra](linear_algebra.md) | 3 | 4.5 | 7.5 | 5.5 | 10 | 7.5 | 10 | **6.9** | HIGH |
| 18 | [markov_asset](markov_asset.md) | 3 | 4.5 | 7.5 | 6.5 | 8.5 | 8 | 10 | **6.9** | HIGH |
| 19 | [misspecified_recovery](misspecified_recovery.md) | 3 | 3 | 5.5 | 6.5 | 10 | 10 | 10 | **6.9** | HIGH |
| 20 | [multi_hyper](multi_hyper.md) | 3.5 | 6.5 | 7.5 | 7 | — | 10 | — | **6.9** | HIGH |
| 21 | [pandas_panel](pandas_panel.md) | 3.5 | — | 7.5 | 4.5 | — | 9 | 10 | **6.9** | HIGH |
| 22 | [stats_examples](stats_examples.md) | 3 | 4.5 | 7 | 7 | — | 10 | 10 | **6.9** | HIGH |
| 23 | [ols](ols.md) | 3 | 7 | 7.5 | 5 | 7.5 | 9 | 10 | **7.0** | HIGH |
| 24 | [perm_income](perm_income.md) | 3 | 4 | 7.5 | 6 | 8.5 | 10 | 10 | **7.0** | HIGH |
| 25 | [phillips_lost_conquest](phillips_lost_conquest.md) | 3.5 | 6 | 7.5 | 4.5 | 7.5 | 10 | 10 | **7.0** | HIGH |
| 26 | [wald_friedman_2](wald_friedman_2.md) | 3 | 6 | 7.5 | 5 | 9 | 8.5 | 10 | **7.0** | HIGH |
| 27 | [finite_markov](finite_markov.md) | 3 | 3.5 | 8 | 6.5 | 10 | 9 | 10 | **7.1** | HIGH |
| 28 | [lln_clt](lln_clt.md) | 3.5 | 3 | 6.5 | 7 | 10 | 10 | 10 | **7.1** | HIGH |
| 29 | [lq_inventories](lq_inventories.md) | 3 | 3 | 7.5 | 7 | 10 | 10 | 10 | **7.2** | HIGH |
| 30 | [mccall_model](mccall_model.md) | 3 | 7.5 | 6 | 6 | 10 | 8 | 10 | **7.2** | HIGH |
| 31 | [mle](mle.md) | 4.5 | 3 | 7.5 | 5.5 | 10 | 10 | 10 | **7.2** | HIGH |
| 32 | [sargent_surico](sargent_surico.md) | 6.5 | 5.5 | 4.5 | 4 | 10 | 10 | 10 | **7.2** | HIGH |
| 33 | [var_subsets](var_subsets.md) | 6.5 | 7 | 5 | 5 | — | 10 | 10 | **7.2** | LOW |
| 34 | [ge_arrow](ge_arrow.md) | 3 | 3 | 7.5 | 7.5 | 10 | 10 | 10 | **7.3** | HIGH |
| 35 | [opt_transport](opt_transport.md) | 3 | 3 | 7 | 8 | 10 | 10 | 10 | **7.3** | HIGH |
| 36 | [pricing_information](pricing_information.md) | 5.5 | 4.5 | 5 | 6 | 10 | 10 | 10 | **7.3** | LOW |
| 37 | [util_rand_resp](util_rand_resp.md) | 4 | 4 | 7.5 | 9.5 | 9 | 10 | — | **7.3** | HIGH |
| 38 | [von_neumann_model](von_neumann_model.md) | 3 | 5 | 7.5 | 7 | 8.5 | 10 | 10 | **7.3** | HIGH |
| 39 | [affine_risk_prices](affine_risk_prices.md) | 4.5 | 4 | 8.5 | 5.5 | 9 | 10 | 10 | **7.4** | HIGH |
| 40 | [blackwell_kihlstrom](blackwell_kihlstrom.md) | 3.5 | 3 | 8.5 | 7.5 | 9 | 10 | 10 | **7.4** | HIGH |
| 41 | [imp_sample](imp_sample.md) | 4.5 | 4 | 10 | 8.5 | — | 10 | — | **7.4** | HIGH |
| 42 | [likelihood_ratio_process_2](likelihood_ratio_process_2.md) | 3 | 9.5 | 7.5 | 4 | 7.5 | 10 | 10 | **7.4** | HIGH |
| 43 | [markov_perf](markov_perf.md) | 4 | 5 | 7 | 6 | 10 | 10 | 10 | **7.4** | HIGH |
| 44 | [odu](odu.md) | 3 | 9 | 7.5 | 5 | 9 | 8.5 | 10 | **7.4** | HIGH |
| 45 | [ross_recovery](ross_recovery.md) | 3.5 | 5.5 | 6.5 | 6 | 10 | 10 | 10 | **7.4** | HIGH |
| 46 | [uncertainty_traps](uncertainty_traps.md) | 3 | 5.5 | 7.5 | 6.5 | 9 | 10 | 10 | **7.4** | HIGH |
| 47 | [inventory_q](inventory_q.md) | 3 | 6 | 10 | 6 | 10 | 10 | — | **7.5** | HIGH |
| 48 | [lqcontrol](lqcontrol.md) | 4.5 | 5 | 7.5 | 5.5 | 10 | 10 | 10 | **7.5** | LOW |
| 49 | [mccall_risk](mccall_risk.md) | 6.5 | 6 | 5.5 | 7 | — | 10 | 10 | **7.5** | LOW |
| 50 | [measurement_models](measurement_models.md) | 3 | 4 | 6 | 9.5 | 10 | 10 | 10 | **7.5** | HIGH |
| 51 | [phillips_priors](phillips_priors.md) | 4.5 | 7 | 8.5 | 5.5 | 7 | 10 | 10 | **7.5** | LOW |
| 52 | [samuelson](samuelson.md) | 6.5 | 9.5 | 7.5 | 5 | 8.5 | 8 | — | **7.5** | LOW |
| 53 | [wald_friedman](wald_friedman.md) | 3 | 8.5 | 7.5 | 4.5 | 10 | 9 | 10 | **7.5** | HIGH |
| 54 | [ak_aiyagari](ak_aiyagari.md) | 5 | 10 | 8 | 4 | 8.5 | 10 | — | **7.6** | HIGH |
| 55 | [cass_fiscal](cass_fiscal.md) | 3 | 9 | 7.5 | 4 | 10 | 10 | 10 | **7.6** | HIGH |
| 56 | [hansen_singleton_1983](hansen_singleton_1983.md) | 6 | 3 | 7 | 9.5 | 10 | 10 | — | **7.6** | HIGH |
| 57 | [olg_adaptive_money](olg_adaptive_money.md) | 3.5 | 7.5 | 6.5 | 6 | 10 | 10 | 10 | **7.6** | HIGH |
| 58 | [os_stochastic](os_stochastic.md) | 3 | 7 | 7.5 | 7.5 | 10 | 8 | 10 | **7.6** | HIGH |
| 59 | [ar1_turningpts](ar1_turningpts.md) | 3 | 7.5 | 8.5 | 8 | 9 | 10 | — | **7.7** | HIGH |
| 60 | [cass_koopmans_2](cass_koopmans_2.md) | 3 | 9.5 | 8.5 | 6 | 10 | 7 | 10 | **7.7** | HIGH |
| 61 | [kalman](kalman.md) | 5 | 4.5 | 8.5 | 7 | 9 | 10 | 10 | **7.7** | LOW |
| 62 | [long_run_risk_operator](long_run_risk_operator.md) | 3 | 7 | 7.5 | 6.5 | 10 | 10 | 10 | **7.7** | HIGH |
| 63 | [phillips_learning](phillips_learning.md) | 5 | 7.5 | 8.5 | 6 | 7 | 10 | 10 | **7.7** | LOW |
| 64 | [phillips_two_stories](phillips_two_stories.md) | 3 | 10 | 8.5 | 5 | 7.5 | 10 | 10 | **7.7** | HIGH |
| 65 | [back_prop](back_prop.md) | 3 | 7.5 | 7.5 | 9 | — | 10 | 10 | **7.8** | HIGH |
| 66 | [ifp_opi](ifp_opi.md) | 5 | 10 | 7 | 6 | — | 9 | 10 | **7.8** | LOW |
| 67 | [likelihood_bayes](likelihood_bayes.md) | 5.5 | 4 | 7.5 | 7.5 | 10 | 10 | 10 | **7.8** | HIGH |
| 68 | [ls_learning](ls_learning.md) | 4.5 | 5 | 8.5 | 6.5 | 10 | 10 | 10 | **7.8** | LOW |
| 69 | [mccall_q](mccall_q.md) | 4 | 9.5 | 7 | 7 | 9 | 10 | — | **7.8** | HIGH |
| 70 | [newton_method](newton_method.md) | 4 | 9.5 | 7 | 6 | — | 10 | 10 | **7.8** | HIGH |
| 71 | [os_numerical](os_numerical.md) | 4.5 | 9.5 | 7.5 | 5.5 | — | 10 | 10 | **7.8** | LOW |
| 72 | [re_with_feedback](re_with_feedback.md) | 3 | 8.5 | 7 | 6 | 10 | 10 | 10 | **7.8** | HIGH |
| 73 | [sir_model](sir_model.md) | 4.5 | 7.5 | 8.5 | 8.5 | — | 10 | — | **7.8** | LOW |
| 74 | [svd_intro](svd_intro.md) | 3 | 9.5 | 7.5 | 6.5 | — | 10 | 10 | **7.8** | HIGH |
| 75 | [var_dmd](var_dmd.md) | 3 | 9.5 | — | — | 7.5 | 9 | 10 | **7.8** | HIGH |
| 76 | [eig_circulant](eig_circulant.md) | 3 | 7.5 | 10 | 7 | — | 10 | 10 | **7.9** | HIGH |
| 77 | [exchangeable](exchangeable.md) | 3.5 | 7 | 7.5 | 7.5 | 10 | 10 | 10 | **7.9** | HIGH |
| 78 | [information_market_equilibrium](information_market_equilibrium.md) | 4 | 5.5 | 8.5 | 7.5 | 10 | 10 | 10 | **7.9** | HIGH |
| 79 | [kalman_filter_var](kalman_filter_var.md) | 5.5 | 7.5 | 5.5 | 6.5 | 10 | 10 | 10 | **7.9** | LOW |
| 80 | [lake_model](lake_model.md) | 5.5 | 6.5 | 7.5 | 5.5 | 10 | 10 | 10 | **7.9** | LOW |
| 81 | [learning_approximation](learning_approximation.md) | 5.5 | 8 | 5.5 | 6.5 | 10 | 10 | 10 | **7.9** | LOW |
| 82 | [mccall_fitted_vfi](mccall_fitted_vfi.md) | 6 | 8 | 7 | 5.5 | 9 | 10 | 10 | **7.9** | LOW |
| 83 | [phillips_drifts_volatilities](phillips_drifts_volatilities.md) | 3.5 | 9.5 | 8 | 4.5 | 10 | 10 | 10 | **7.9** | HIGH |
| 84 | [phillips_escaping_nash](phillips_escaping_nash.md) | 5 | 9.5 | 8.5 | 4.5 | 7.5 | 10 | 10 | **7.9** | LOW |
| 85 | [rational_expectations](rational_expectations.md) | 3.5 | 5 | 7.5 | 10 | 9 | 10 | 10 | **7.9** | HIGH |
| 86 | [robust_permanent_income](robust_permanent_income.md) | 3.5 | 9 | 6.5 | 6 | 10 | 10 | 10 | **7.9** | HIGH |
| 87 | [aiyagari_egm](aiyagari_egm.md) | 3 | 8.5 | 10 | 5.5 | 9 | 10 | 10 | **8.0** | HIGH |
| 88 | [cass_koopmans_1](cass_koopmans_1.md) | 3 | 9.5 | 8.5 | 6 | 10 | 9 | 10 | **8.0** | HIGH |
| 89 | [divergence_measures](divergence_measures.md) | 4.5 | 6.5 | 8.5 | 6.5 | 10 | 10 | 10 | **8.0** | LOW |
| 90 | [hansen_singleton_1982](hansen_singleton_1982.md) | 6 | 5 | 5.5 | 9.5 | 10 | 10 | 10 | **8.0** | LOW |
| 91 | [ifp_egm_transient_shocks](ifp_egm_transient_shocks.md) | 4 | 10 | 7.5 | 5.5 | 9 | 10 | 10 | **8.0** | HIGH |
| 92 | [jv](jv.md) | 3 | 10 | 7.5 | 6.5 | 9 | 10 | 10 | **8.0** | HIGH |
| 93 | [marimon_mcgrattan_sargent](marimon_mcgrattan_sargent.md) | 4 | 9.5 | 6.5 | 7.5 | 8.5 | 10 | 10 | **8.0** | HIGH |
| 94 | [market_diffusion](market_diffusion.md) | 6.5 | 7 | 4.5 | 8 | 10 | 10 | 10 | **8.0** | LOW |
| 95 | [mccall_model_with_sep_markov](mccall_model_with_sep_markov.md) | 5.5 | 10 | 7 | 5.5 | — | 10 | 10 | **8.0** | LOW |
| 96 | [mix_model](mix_model.md) | 5 | 9 | 7 | 7 | — | 10 | 10 | **8.0** | LOW |
| 97 | [theil_1](theil_1.md) | 4.5 | 6.5 | 8.5 | 6.5 | 10 | 10 | 10 | **8.0** | LOW |
| 98 | [troubleshooting](troubleshooting.md) | 6 | — | — | 9 | — | 9 | — | **8.0** | LOW |
| 99 | [ak2](ak2.md) | 3.5 | 10 | 8.5 | 5 | 10 | 10 | 10 | **8.1** | HIGH |
| 100 | [cass_fiscal_2](cass_fiscal_2.md) | 4 | 10 | 7.5 | 5.5 | 10 | 10 | 10 | **8.1** | HIGH |
| 101 | [chow_business_cycles](chow_business_cycles.md) | 5.5 | 6.5 | 8.5 | 6.5 | 10 | 10 | 10 | **8.1** | LOW |
| 102 | [ifp_egm](ifp_egm.md) | 3 | 9.5 | 7.5 | 6.5 | 10 | 10 | 10 | **8.1** | HIGH |
| 103 | [lq_robust_bewley](lq_robust_bewley.md) | 6.5 | 5.5 | 7.5 | 7.5 | 10 | 10 | 10 | **8.1** | LOW |
| 104 | [merging_of_opinions](merging_of_opinions.md) | 4.5 | 7 | 8.5 | 7.5 | 9 | 10 | 10 | **8.1** | LOW |
| 105 | [os_time_iter](os_time_iter.md) | 4.5 | 7.5 | 7.5 | 8 | 9 | 10 | 10 | **8.1** | LOW |
| 106 | [phillips_self_confirming](phillips_self_confirming.md) | 5.5 | 7 | 8.5 | 6 | 10 | 10 | 10 | **8.1** | LOW |
| 107 | [rand_resp](rand_resp.md) | 3.5 | 9.5 | 7.5 | — | 10 | 10 | — | **8.1** | HIGH |
| 108 | [rational_learning_re](rational_learning_re.md) | 5.5 | 7.5 | 7 | 7 | 10 | 10 | 10 | **8.1** | LOW |
| 109 | [theil_2](theil_2.md) | 4.5 | 7.5 | 6.5 | 8.5 | 10 | 10 | 10 | **8.1** | LOW |
| 110 | [wealth_dynamics](wealth_dynamics.md) | 3 | 9.5 | 8 | 6.5 | 10 | 10 | 10 | **8.1** | HIGH |
| 111 | [aiyagari](aiyagari.md) | 4.5 | 8.5 | 8.5 | 7 | 10 | 9 | 10 | **8.2** | LOW |
| 112 | [bayes_nonconj](bayes_nonconj.md) | 5 | 10 | 8.5 | 6.5 | — | 9 | 10 | **8.2** | LOW |
| 113 | [endogenous_lake](endogenous_lake.md) | 5.5 | 7.5 | 8.5 | 6 | 10 | 10 | 10 | **8.2** | LOW |
| 114 | [mccall_persist_trans](mccall_persist_trans.md) | 6.5 | 6 | 7 | 8 | 10 | 10 | 10 | **8.2** | LOW |
| 115 | [survival_recursive_preferences](survival_recursive_preferences.md) | 5 | 9.5 | 8.5 | 4.5 | 10 | 10 | 10 | **8.2** | LOW |
| 116 | [house_auction](house_auction.md) | 3 | 10 | 7 | — | 10 | 10 | 10 | **8.3** | HIGH |
| 117 | [lq_permanent_income](lq_permanent_income.md) | 5.5 | 7.5 | 8.5 | 6.5 | 10 | 10 | 10 | **8.3** | LOW |
| 118 | [hoist_failure](hoist_failure.md) | 5.5 | 6.5 | 8.5 | 8 | 10 | 10 | 10 | **8.4** | LOW |
| 119 | [ifp_discrete](ifp_discrete.md) | 5.5 | 7 | 7.5 | 8.5 | 10 | 10 | 10 | **8.4** | LOW |
| 120 | [kesten_processes](kesten_processes.md) | 5.5 | 5 | 10 | 8 | 10 | 10 | 10 | **8.4** | LOW |
| 121 | [lq_robust_smoothing](lq_robust_smoothing.md) | 5.5 | 7.5 | 8.5 | 7.5 | 10 | 10 | 10 | **8.4** | LOW |
| 122 | [organization_capital](organization_capital.md) | 4.5 | 7 | 8.5 | 9 | 10 | 10 | 10 | **8.4** | LOW |
| 123 | [phillips_adaptive](phillips_adaptive.md) | 5.5 | 9.5 | 8.5 | 6.5 | 8.5 | 10 | 10 | **8.4** | LOW |
| 124 | [phillips_credibility](phillips_credibility.md) | 5 | 9.5 | 9 | 7 | 8.5 | 10 | 10 | **8.4** | LOW |
| 125 | [phillips_misspecified](phillips_misspecified.md) | 5.5 | 9.5 | 8.5 | 6.5 | 8.5 | 10 | 10 | **8.4** | LOW |
| 126 | [morris_learn](morris_learn.md) | 3 | 9.5 | 8.5 | 10 | 8.5 | 10 | 10 | **8.5** | HIGH |
| 127 | [os_egm](os_egm.md) | 4 | 9.5 | 7 | 9 | 10 | 10 | 10 | **8.5** | HIGH |
| 128 | [phillips_credible_policies](phillips_credible_policies.md) | 6.5 | 9.5 | 8.5 | 6 | 10 | 9 | 10 | **8.5** | LOW |
| 129 | [ar1_bayes](ar1_bayes.md) | 7 | 10 | 7.5 | 8 | 10 | 8 | 10 | **8.6** | NONE |
| 130 | [bounded_rationality](bounded_rationality.md) | 5.5 | 10 | 8.5 | 6.5 | 10 | 10 | 10 | **8.6** | NONE |
| 131 | [career](career.md) | 6 | 9.5 | 8.5 | 6.5 | 10 | 10 | 10 | **8.6** | NONE |
| 132 | [exchange_rate_learning](exchange_rate_learning.md) | 5 | 9.5 | 10 | 5.5 | 10 | 10 | 10 | **8.6** | NONE |
| 133 | [lq_bewley_complete_markets](lq_bewley_complete_markets.md) | 6 | 10 | 8.5 | 6 | 10 | 10 | 10 | **8.6** | NONE |
| 134 | [mccall_model_with_separation](mccall_model_with_separation.md) | 7 | 8.5 | 6.5 | 8.5 | 10 | 10 | 10 | **8.6** | NONE |
| 135 | [os_egm_jax](os_egm_jax.md) | 8 | 10 | 6.5 | 7 | — | 10 | 10 | **8.6** | NONE |
| 136 | [unemployment_linear](unemployment_linear.md) | 6 | 8 | 8.5 | 8.5 | 9 | 10 | 10 | **8.6** | NONE |
| 137 | [genetic_classifier](genetic_classifier.md) | 6 | 10 | 8.5 | 7 | 10 | 10 | 10 | **8.8** | NONE |
| 138 | [harrison_kreps](harrison_kreps.md) | 6.5 | 8 | 8.5 | — | 10 | 10 | 10 | **8.8** | NONE |
| 139 | [os](os.md) | 5.5 | 9.5 | 8.5 | 8 | 10 | 10 | 10 | **8.8** | NONE |
| 140 | [prospects_bounded_rationality](prospects_bounded_rationality.md) | 6.5 | 10 | 7.5 | 8.5 | 10 | 10 | — | **8.8** | NONE |
| 141 | [inventory_dynamics](inventory_dynamics.md) | 5.5 | 10 | 9.5 | 7 | 10 | 10 | 10 | **8.9** | NONE |
| 142 | [unemployment_shocks](unemployment_shocks.md) | 6.5 | 9.5 | 7.5 | 10 | — | 10 | 10 | **8.9** | NONE |
| 143 | [status](status.md) | 10 | — | 9 | — | — | 10 | — | **9.7** | NONE |
| 144 | [intro](intro.md) | 10 | — | — | — | — | 10 | — | **10.0** | NONE |
| 145 | [zreferences](zreferences.md) | 10 | — | — | — | — | 10 | — | **10.0** | NONE |
<!-- /qe:series-ranked -->
