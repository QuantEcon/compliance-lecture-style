# Summary

Style audit of the **lecture-python-advanced.myst** series.

<!-- qe:series-meta -->
- **Audit date:** 2026-08-19
- **Corpus snapshot:** `b83d6da399`
- **Lectures audited:** 68
- **Average overall score:** 7.4 / 10
- **Average per-category scores:** writing 4.6, math 5.8, code 7.3, figures 6.3, references 9.2, links 9.2, admon 10.0
- **JAX:** out of scope — the `qe-jax-*` rules target `lecture-jax`.
- **Judgment-review coverage:** all lectures reviewed.
<!-- /qe:series-meta -->

<!-- qe:series-narrative -->
The lowest-scoring series in the corpus — 7.4 against a corpus mean of 7.7, with 43 of its
68 lectures at HIGH. Every one of those 43 is HIGH on a category floor rather than on its
overall: the lowest overall here is 5.6. The floor is **Writing**, not Math. Writing
averages 4.6 and sits at or below the ≤ 4 floor in **36 of the 43** HIGH lectures; Math
(5.8) floors 23 of them, Figures (6.3) 7. Writing was 7.3 in 2026-05; the fall to 4.6 is
the judgment layer, which that row does not fold in and this one folds into all 68 lectures,
so it is the series being assessed against more rules rather than a regression. Like for
like, on the evidence layer alone (`history_mechanical.csv`), Writing here is 7.3 → 7.4 and
Math 6.0 → 6.1. Exactly one full lecture reaches NONE (`supply_demand_var`, 8.6);
the other four are `intro`, `status`, `zreferences` and `troubleshooting`.

Most of what is under that Writing floor does not appear in the systemic table above.
`qe-writing-008` (53 / 68, 2,223 occurrences) has the largest count in the series and the
lowest audit weight — it is a whitespace rule. The mechanical rules that actually move the
score are far smaller: `qe-writing-001` (42 / 68, 155 occurrences) and `qe-writing-004`
(24 / 68, 109 occurrences), both High weight. The rest is judgment-only and so carries no
mechanical count at all — bold-and-italic use is flagged in 55 of the 68 lectures with 356
findings, clarity in 56, logical flow in 56, visual elements in 60. That is the densest
judgment load of any series, and no sweep touches it.

Math is what makes this series distinctive rather than what makes it worst. 5.8 is the
lowest Math average of any series against a corpus 7.0, and Math is at the floor in 23 of
the 43 HIGH lectures here against 64 of 197 corpus-wide. Two rules carry nearly all of it:
`qe-math-002` (20 / 68, 671 occurrences) and `qe-math-010` *(proposed)* (33 / 68, 682 occurrences),
each roughly 42 % of that rule's corpus-wide total and each at the highest per-lecture
density in the corpus — 34 and 21 occurrences per affected lecture. 648 of the 671
transpose findings and 553 of the 682 operator findings fall inside the 23 Math-floored
lectures, concentrated in the LQ, filtering and robustness material: `hs_recursive_models`
(5.6, the series minimum and the second-lowest score in the corpus) carries 154 and 76 of
them by itself, `robustness` 117, `doubts_or_variability` 148.

**A caveat specific to this series.** 23 of these 68 lectures share a filename with
`lecture-dp`, and **18 are byte-identical** at this snapshot — three times the
byte-identical overlap between `lecture-dp` and `lecture-python.myst`, and the largest in
the corpus. Those 18 hold 1,780 of this series' 5,605 mechanical findings, and 15 of them
are HIGH here. Their mechanical counts agree exactly across the two series, which is the
check working; the judgment overlays differ in every one of the 18, and 12 land on a
different overall. So for these a finding here and a finding in `lecture-dp` are the same
finding, and one upstream edit clears both. Whether the corpus totals should de-duplicate
them is still open —
[compliance-lecture-style#3](https://github.com/QuantEcon/compliance-lecture-style/issues/3).
The other five shared names (`cons_news`, `opt_tax_recur`, `intro`, `status`,
`zreferences`) have diverged, so each copy needs its own edit.
<!-- /qe:series-narrative -->

## Priority distribution

<!-- qe:series-priority -->
| Priority | Count | % |
|----------|-------|---|
| HIGH     | 43    | 63.2% |
| MEDIUM   | 0     | 0.0% |
| LOW      | 20    | 29.4% |
| NONE     | 5     | 7.4% |
<!-- /qe:series-priority -->

## Top systemic issues across the series

Ranked by how many of the series' lectures each rule reaches.

<!-- qe:series-systemic -->
1. **`qe-fig-005`** — Descriptive figure names for cross-referencing — **54 / 68** lectures, 203 occurrences.
2. **`qe-writing-008`** — Remove excessive whitespace between words — **53 / 68** lectures, 2223 occurrences.
3. **`qe-fig-001`** — Do not set figure size unless necessary — **47 / 68** lectures, 215 occurrences.
4. **`qe-writing-001`** — Use one sentence per paragraph — **42 / 68** lectures, 155 occurrences.
5. **`qe-fig-008`** — Use lw=2 for line charts — **40 / 68** lectures, 302 occurrences.
6. **`qe-fig-003`** — No matplotlib embedded titles — **36 / 68** lectures, 149 occurrences.
7. **`qe-ref-001`** — Use correct citation style — **35 / 68** lectures, 93 occurrences.
8. **`qe-math-010`** *(proposed)* — Blackboard \mathbb{P}, \mathbb{E}, \mathbb{V} with braces — **33 / 68** lectures, 682 occurrences.
9. **`qe-link-002`** — Use doc links for cross-series references — **26 / 68** lectures, 94 occurrences.
10. **`qe-writing-004`** — Avoid unnecessary capitalization in narrative text — **24 / 68** lectures, 109 occurrences.
<!-- /qe:series-systemic -->

## Clean across the series

Checked rules with no violation anywhere in the series — the conventions this series
already holds to.

<!-- qe:series-clean -->
- **`qe-admon-002`** — Use dropdown class for solutions
- **`qe-admon-003`** — Use tick count management for nested directives
- **`qe-math-007`** — Use automatic equation numbering, not manual tags
- **`qe-math-012`** *(proposed)* — Multiplication via \cdot or juxtaposition, never *
<!-- /qe:series-clean -->

## Series-level recommendations

<!-- qe:series-recommendations -->
1. **Writing first — it clears more HIGH lectures than anything else here.** 17 of the 43
   HIGH lectures have Writing as their *only* floored category, so they clear on this work
   alone; a further 15 need it alongside Math. It is three different jobs, cheapest first:
   - `qe-writing-008` (53 / 68, 2,223 occurrences) — a scriptable regex sweep, Low audit
     weight. The largest number in the series and the smallest effect on the score. Worth
     doing, in its own commit, but it will not lift a lecture off the floor by itself.
   - `qe-writing-001` (42 / 68, 155 occurrences) and `qe-writing-004` (24 / 68, 109
     occurrences) — both High weight, both reading passes. Splitting a paragraph changes
     its rhythm, and the capitalisation check is heuristic, so every hit needs an eye.
   - The judgment-only writing rules — bold-and-italic use in 55 of the 68 lectures,
     clarity in 56, logical flow in 56, visual elements in 60. No script exists, and none
     can. This is the bulk of the 4.6 and it is a per-lecture reading pass.
2. **Math second — one notation pass over the LQ, filtering and robustness cluster.**
   `qe-math-002` (20 / 68, 671 occurrences) and `qe-math-010` *(proposed)* (33 / 68, 682 occurrences)
   are both Very-high weight and both concentrated in the 23 Math-floored lectures, which
   hold 648 and 553 of those occurrences. Semi-scriptable: `'` → `^\top` has a
   derivative-prime exception, so a blind substitution is wrong. `qe-math-011` *(proposed)* (18 / 68, 95
   occurrences) and `qe-math-003` (15 / 68, 113 occurrences) fall out of the same pass.
   On its own this clears only the 4 lectures whose sole floor is Math
   (`cagan_rational_expectations`, `classical_filtering`, `lucas_asset_pricing_dles`,
   `markov_jump_lq`) — but combined with item 1 it reaches 36 of the 43.
3. **`qe-math-010` *(proposed)* and `qe-math-011` *(proposed)* belong in the registry before the rewrite, and that
   part is upstream work.** Both are proposed rules rather than registry rules, offered in
   [action-style-guide#18](https://github.com/QuantEcon/action-style-guide/issues/18).
   Rewriting 682 operator occurrences against a rule the PR-time checker does not enforce
   leaves nothing to hold them in place afterwards. `qe-math-010` *(proposed)* is the strongest case in
   that set of seven, and this series is its single largest concentration — the evidence
   for adopting it is here.
4. **Coordinate the 18 byte-identical lectures with `lecture-dp`.** 15 of them are HIGH
   here — 13 Writing-floored, 7 Math-floored — and they include the two largest whitespace
   sites in the series, `calvo` at 242 occurrences and `calvo_machine_learn` at 193. One
   edit, two PRs, same subject and title in both repos. Doing them independently doubles
   the reading and drives the two copies further apart.
5. **Figures last.** All 7 Figures-floored lectures also have Writing or Math at the floor,
   so none of them clears on Figures work alone. `qe-fig-001` (47 / 68, 215 occurrences)
   and `qe-fig-008` (40 / 68, 302 occurrences) are Low-weight mechanical sweeps;
   `qe-fig-005` (54 / 68, 203 occurrences) needs a name chosen per figure, and
   `qe-fig-003` (36 / 68, 149 occurrences) a caption written per title, so both are
   reading passes despite being mechanically detected.
6. **Start with `hs_recursive_models`** (5.6), then `entropy` and `smoothing` (6.0 each)
   and `knowing_forecasts_of_others` (6.1) — all four are Writing and Math at the floor
   together. `match_transport` (6.1) is the exception in the bottom five: its Math is 9.5
   and its floors are Writing and Figures.
7. **Not urgent.** The series' only `build_risk` row — `qe-math-006` in `asset_pricing_lph`,
   2 occurrences — is a bare top-level `\begin{align}`, which this pass reclassified
   corpus-wide as a convention outlier rather than a build break.
<!-- /qe:series-recommendations -->

## Lectures ranked by priority (lowest score first)

Scores are 0–10 per category; **Overall** is the mean of the in-scope categories, and
**Priority** follows [spec §4](../spec.md). A dash means the category is not applicable to
that lecture. Click a lecture for its full report.

<!-- qe:series-ranked -->
| # | Lecture | Writing | Math | Code | Figures | References | Links | Admon | Overall | Priority |
|---|---------|---|---|---|---|---|---|---|---------|----------|
| 1 | [hs_recursive_models](hs_recursive_models.md) | 3 | 3 | — | — | 8.5 | 8 | — | **5.6** | HIGH |
| 2 | [entropy](entropy.md) | 3 | 3 | — | 7 | 8.5 | 8.5 | — | **6.0** | HIGH |
| 3 | [smoothing](smoothing.md) | 3 | 3 | 7.5 | 5 | 10 | 7.5 | — | **6.0** | HIGH |
| 4 | [knowing_forecasts_of_others](knowing_forecasts_of_others.md) | 3 | 3 | 6 | 9 | 7.5 | 8 | — | **6.1** | HIGH |
| 5 | [match_transport](match_transport.md) | 3 | 9.5 | 4.5 | 3 | 8.5 | 8 | — | **6.1** | HIGH |
| 6 | [five_preferences](five_preferences.md) | 3 | 6 | 7 | 4 | 7 | 10 | — | **6.2** | HIGH |
| 7 | [markov_jump_lq](markov_jump_lq.md) | 5 | 3 | 7 | 5.5 | 8.5 | 9 | — | **6.3** | HIGH |
| 8 | [tax_smoothing_1](tax_smoothing_1.md) | 4 | 4.5 | 7 | 6 | 7.5 | 9 | — | **6.3** | HIGH |
| 9 | [asset_pricing_lph](asset_pricing_lph.md) | 3 | 3 | 5.5 | 7.5 | 8.5 | 7.5 | 10 | **6.4** | HIGH |
| 10 | [rob_markov_perf](rob_markov_perf.md) | 3.5 | 4 | 6.5 | 8 | 9 | 7.5 | — | **6.4** | HIGH |
| 11 | [tax_smoothing_2](tax_smoothing_2.md) | 5 | 3.5 | 7.5 | 4 | 8.5 | 10 | — | **6.4** | HIGH |
| 12 | [black_litterman](black_litterman.md) | 3 | 3 | 7 | 4 | 10 | 8.5 | 10 | **6.5** | HIGH |
| 13 | [additive_functionals](additive_functionals.md) | 5.5 | 3.5 | 7 | 3.5 | 9 | 7.5 | 10 | **6.6** | HIGH |
| 14 | [cons_news](cons_news.md) | 3 | 4.5 | 8.5 | 6 | 10 | 7.5 | — | **6.6** | HIGH |
| 15 | [amss2](amss2.md) | 3.5 | 5.5 | 7.5 | 6 | 8.5 | 10 | — | **6.8** | HIGH |
| 16 | [dyn_stack](dyn_stack.md) | 3.5 | 4 | 7.5 | 5 | 10 | 7.5 | 10 | **6.8** | HIGH |
| 17 | [robustness](robustness.md) | 3 | 3 | 7.5 | 6.5 | 10 | 7.5 | 10 | **6.8** | HIGH |
| 18 | [cagan_rational_expectations](cagan_rational_expectations.md) | 5.5 | 3 | 6 | 5.5 | 8.5 | 10 | 10 | **6.9** | HIGH |
| 19 | [stationary_densities](stationary_densities.md) | 4 | 6 | 7 | 5.5 | 9 | 7.5 | 10 | **7.0** | HIGH |
| 20 | [subjective_beliefs_business_cycles](subjective_beliefs_business_cycles.md) | 3 | 3 | 7 | 7 | 9 | 10 | 10 | **7.0** | HIGH |
| 21 | [BCG_incomplete_mkts](BCG_incomplete_mkts.md) | 3 | 7.5 | 7.5 | 4.5 | 10 | 10 | — | **7.1** | HIGH |
| 22 | [amss3](amss3.md) | 3.5 | 5.5 | 7.5 | 5.5 | 7.5 | 10 | 10 | **7.1** | HIGH |
| 23 | [calvo](calvo.md) | 3 | 5.5 | 7.5 | 7 | 8.5 | 8 | 10 | **7.1** | HIGH |
| 24 | [smoothing_tax](smoothing_tax.md) | 4 | 5.5 | 7.5 | 4 | 10 | 9 | 10 | **7.1** | HIGH |
| 25 | [calvo_machine_learn](calvo_machine_learn.md) | 3.5 | 3 | 6 | 8 | 10 | 10 | 10 | **7.2** | HIGH |
| 26 | [hs_invertibility_example](hs_invertibility_example.md) | 5.5 | 7 | 7.5 | 5 | 8.5 | 10 | — | **7.2** | LOW |
| 27 | [lucas_asset_pricing_dles](lucas_asset_pricing_dles.md) | 5.5 | 4 | 8.5 | 7 | 8.5 | 10 | — | **7.2** | HIGH |
| 28 | [permanent_income_dles](permanent_income_dles.md) | 4 | 7.5 | 7.5 | 8 | 8.5 | 8 | — | **7.2** | HIGH |
| 29 | [risk_aversion_or_mistaken_beliefs](risk_aversion_or_mistaken_beliefs.md) | 5 | 3 | 9 | 3.5 | 10 | 10 | 10 | **7.2** | HIGH |
| 30 | [tsyrennikov_2013](tsyrennikov_2013.md) | 4.5 | 5.5 | 5.5 | 5 | 10 | 10 | 10 | **7.2** | LOW |
| 31 | [amss](amss.md) | 4 | 4 | 7 | 6 | 10 | 10 | 10 | **7.3** | HIGH |
| 32 | [dovis_accounting_mf](dovis_accounting_mf.md) | 5 | 4.5 | 7 | 4.5 | 10 | 10 | 10 | **7.3** | LOW |
| 33 | [gorman_heterogeneous_households](gorman_heterogeneous_households.md) | 3 | 8 | 5 | 5 | 10 | 10 | 10 | **7.3** | HIGH |
| 34 | [growth_in_dles](growth_in_dles.md) | 3 | 7.5 | 7.5 | 7 | 9 | 10 | — | **7.3** | HIGH |
| 35 | [BCG_complete_mkts](BCG_complete_mkts.md) | 3 | 7.5 | 7 | 6 | 10 | 8 | 10 | **7.4** | HIGH |
| 36 | [classical_filtering](classical_filtering.md) | 4.5 | 3.5 | 10 | — | 8.5 | 8 | 10 | **7.4** | HIGH |
| 37 | [discrete_dp](discrete_dp.md) | 6 | 7 | 6.5 | 6 | 9 | 7 | 10 | **7.4** | LOW |
| 38 | [doubts_or_variability](doubts_or_variability.md) | 4 | 3 | 7 | 9 | 9 | 10 | 10 | **7.4** | HIGH |
| 39 | [opt_tax_recur](opt_tax_recur.md) | 4.5 | 5.5 | 8.5 | 4.5 | 9 | 10 | 10 | **7.4** | LOW |
| 40 | [orth_proj](orth_proj.md) | 4 | 3 | 10 | 7 | 10 | 8 | 10 | **7.4** | HIGH |
| 41 | [arma](arma.md) | 4.5 | 7.5 | 8.5 | 6.5 | 10 | 8 | — | **7.5** | LOW |
| 42 | [chang_ramsey](chang_ramsey.md) | 3 | 9 | 8.5 | 6 | 8.5 | 10 | — | **7.5** | HIGH |
| 43 | [hansen_richard_1987](hansen_richard_1987.md) | 4 | 4 | 5 | 9.5 | 10 | 10 | 10 | **7.5** | HIGH |
| 44 | [info_projection](info_projection.md) | 4.5 | 5 | 6 | 8 | 9 | 10 | 10 | **7.5** | LOW |
| 45 | [irfs_in_hall_model](irfs_in_hall_model.md) | 3 | 8.5 | 7.5 | 7 | 9 | 10 | — | **7.5** | HIGH |
| 46 | [lqramsey](lqramsey.md) | 4 | 3 | 7.5 | 8 | 10 | 10 | 10 | **7.5** | HIGH |
| 47 | [tax_smoothing_3](tax_smoothing_3.md) | 5.5 | 8.5 | 7.5 | 5 | 8.5 | 10 | — | **7.5** | LOW |
| 48 | [calvo_abreu](calvo_abreu.md) | 4 | 8.5 | 6.5 | 9 | 8.5 | 10 | — | **7.8** | HIGH |
| 49 | [cattle_cycles](cattle_cycles.md) | 7 | 7 | 9 | 5 | 8.5 | 10 | — | **7.8** | LOW |
| 50 | [lu_tricks](lu_tricks.md) | 3 | 6.5 | 8.5 | 8.5 | 10 | 8 | 10 | **7.8** | HIGH |
| 51 | [repeat_mh](repeat_mh.md) | 4 | 6 | 7 | 8.5 | 10 | 10 | 10 | **7.9** | HIGH |
| 52 | [hansen_jagannathan_1991](hansen_jagannathan_1991.md) | 6.5 | 5 | 5.5 | 9 | 10 | 10 | 10 | **8.0** | LOW |
| 53 | [un_insure](un_insure.md) | 4.5 | 9.5 | 7.5 | 5.5 | 9 | 10 | 10 | **8.0** | LOW |
| 54 | [arellano](arellano.md) | 5.5 | 8.5 | 6.5 | 7 | 9 | 10 | 10 | **8.1** | LOW |
| 55 | [coase](coase.md) | 6 | 9 | 6 | 7 | 8.5 | 10 | 10 | **8.1** | LOW |
| 56 | [estspec](estspec.md) | 5 | 9.5 | 7.5 | 5 | 10 | 10 | 10 | **8.1** | LOW |
| 57 | [muth_kalman](muth_kalman.md) | 6 | 6 | 10 | 5.5 | 10 | 9 | 10 | **8.1** | LOW |
| 58 | [atkeson_1991](atkeson_1991.md) | 5.5 | 9.5 | 7 | 5.5 | 10 | 10 | 10 | **8.2** | LOW |
| 59 | [matsuyama](matsuyama.md) | 5 | 10 | 7 | 6.5 | 10 | 9 | 10 | **8.2** | LOW |
| 60 | [mcmc](mcmc.md) | 7 | 5.5 | 7.5 | 8 | 10 | 10 | 10 | **8.3** | LOW |
| 61 | [rosen_schooling_model](rosen_schooling_model.md) | 5.5 | 10 | 7.5 | 6 | 9 | 10 | 10 | **8.3** | LOW |
| 62 | [lucas_model](lucas_model.md) | 6 | 9.5 | 7.5 | 7.5 | 10 | 8 | 10 | **8.4** | LOW |
| 63 | [chang_credible](chang_credible.md) | 3 | 10 | 8.5 | 9.5 | 10 | 10 | — | **8.5** | HIGH |
| 64 | [supply_demand_var](supply_demand_var.md) | 8 | 8.5 | 7.5 | 6 | 10 | 10 | 10 | **8.6** | NONE |
| 65 | [troubleshooting](troubleshooting.md) | 8.5 | — | — | 9 | — | 9 | — | **8.8** | NONE |
| 66 | [intro](intro.md) | 10 | — | — | — | — | 10 | — | **10.0** | NONE |
| 67 | [status](status.md) | 10 | — | — | — | — | 10 | — | **10.0** | NONE |
| 68 | [zreferences](zreferences.md) | 10 | — | — | — | — | 10 | — | **10.0** | NONE |
<!-- /qe:series-ranked -->
