# Summary

Style audit of the **lecture-dp** series.

<!-- qe:series-meta -->
- **Audit date:** 2026-08-07
- **Corpus snapshot:** `c30490a2f4`
- **Lectures audited:** 52
- **Average overall score:** 7.7 / 10
- **Average per-category scores:** writing 4.7, math 6.6, code 7.7, figures 6.4, references 9.3, links 9.5, admon 10.0
- **JAX:** out of scope — the `qe-jax-*` rules target `lecture-jax`.
- **Judgment-review coverage:** all lectures reviewed.
<!-- /qe:series-meta -->

<!-- qe:series-narrative -->
**Writing is the floor under this series, and that is new.** At 4.7 it is the weakest of the
seven categories measured here, and it sits at or below the ≤ 4 threshold in **30 of the 34
HIGH lectures** — against Math's 14 and Figures' 2. Nineteen lectures are HIGH on Writing and
nothing else. In the previous pass Math and Figures tied as the weakest at 6.4 and Writing
scored 7.0; Math and Figures have barely moved since (6.6 and 6.4) while Writing fell to 4.7
and the HIGH list grew from 15 to 34. That fall is not particular to this series — the corpus
Writing mean went 6.6 → 4.6 over the same interval, and at 4.7 `lecture-dp` is marginally
*above* it. Every one of the 34 is HIGH on a category floor, never on the overall — the
lowest overall in the series is 5.7. The series mean, 7.7, is exactly the corpus
mean, but 65.4 % of its lectures are HIGH against 57 % corpus-wide — the second-largest share
of any series, behind `lecture-python-programming`.

What sits under Writing divides into a scriptable half and a reading half, and the reading
half is the larger one. Repeated spaces dominate the mechanical side:
**`qe-writing-008`** **(40 / 52, 1,578 occurrences)**, a per-lecture density second only to
`lecture-python-advanced.myst`. Then **`qe-writing-001`** **(23 / 52, 45)**,
**`qe-writing-006`** **(22 / 52, 146)** and **`qe-writing-004`** **(14 / 52, 28)**. By
reading: `qe-writing-003` (logical flow) reaches 45 of the 52 lectures, `qe-writing-002` 39,
`qe-writing-007` 36, `qe-writing-005` 31. **All 30 Writing-floored lectures carry findings
from both halves** — not one of them can be cleared by a sweep alone. That is what separates
this series from `lecture-python-programming`, where a single heading sweep would empty the
HIGH list.

Math is the second problem and a far more concentrated one: at 6.6 it is the lowest in the
corpus after `lecture-python-advanced.myst`, and nearly all of it is one rule.
**`qe-math-002`** — transpose notation — **(14 / 52, 416 occurrences)** reaches fewer lectures
than four of the figure rules but averages about thirty sites in each, and it lands where it
counts: 12 of the 14 Math-floored lectures carry it, holding 381 of its 416 occurrences.
`lqcontrol` alone has 85, `lagrangian_lqdp` 69, `tax_smoothing_2` 59, `cross_product_trick`
52, `markov_jump_lq` 47. Past it the Math findings thin out quickly: the next largest is
**`qe-math-010`** **(20 / 52, 132)**, itself a proposed rule — so this is one rule and not a
cluster.

**A caveat specific to this series.** 31 of these 52 lectures share a filename with a lecture
in `lecture-python.myst`, the repository `lecture-dp` syncs from — but only **6 are
byte-identical** at this snapshot (`cross_product_trick`, `ifp_discrete`, `ifp_opi`,
`lq_inventories`, `mccall_model_with_separation`, `os_numerical`). For those 6 a finding here
and a finding there are the same finding, and one upstream fix clears both; the other 25 share
an origin and have since diverged, so the same defect usually needs two edits. Only two of the
6 are HIGH here — `cross_product_trick` (5.7, the series' lowest) and `lq_inventories` (7.4).
It is worth recording how the two independent passes over identical bytes came out: all six
pairs differ in at least one judgment-heavy category — Writing in four, Code in two, Math in
one — while Figures, References, Links and Admonitions agree exactly, no overall differs by
more than 0.2, and all six land in the same priority bucket. Whether the corpus totals should
de-duplicate those six is open —
[`compliance-lecture-style#3`](https://github.com/QuantEcon/compliance-lecture-style/issues/3).
<!-- /qe:series-narrative -->

## Priority distribution

<!-- qe:series-priority -->
| Priority | Count | % |
|----------|-------|---|
| HIGH     | 34    | 65.4% |
| MEDIUM   | 0     | 0.0% |
| LOW      | 9     | 17.3% |
| NONE     | 9     | 17.3% |
<!-- /qe:series-priority -->

## Top systemic issues across the series

Ranked by how many of the series' lectures each rule reaches.

<!-- qe:series-systemic -->
1. **`qe-fig-005`** — Descriptive figure names for cross-referencing — **42 / 52** lectures, 164 occurrences.
2. **`qe-writing-008`** — Remove excessive whitespace between words — **40 / 52** lectures, 1578 occurrences.
3. **`qe-fig-008`** — Use lw=2 for line charts — **38 / 52** lectures, 219 occurrences.
4. **`qe-fig-001`** — Do not set figure size unless necessary — **31 / 52** lectures, 102 occurrences.
5. **`qe-fig-003`** — No matplotlib embedded titles — **30 / 52** lectures, 105 occurrences.
6. **`qe-writing-001`** — Use one sentence per paragraph — **23 / 52** lectures, 45 occurrences.
7. **`qe-writing-006`** — Capitalize lecture titles properly — **22 / 52** lectures, 146 occurrences.
8. **`qe-math-010`** *(proposed)* — Blackboard \mathbb{P}, \mathbb{E}, \mathbb{V} with braces — **20 / 52** lectures, 132 occurrences.
9. **`qe-ref-001`** — Use correct citation style — **20 / 52** lectures, 45 occurrences.
10. **`qe-link-002`** — Use doc links for cross-series references — **15 / 52** lectures, 53 occurrences.
<!-- /qe:series-systemic -->

## Clean across the series

Checked rules with no violation anywhere in the series — the conventions this series
already holds to.

<!-- qe:series-clean -->
- **`qe-admon-002`** — Use dropdown class for solutions
- **`qe-admon-003`** — Use tick count management for nested directives
- **`qe-fig-004`** — Caption formatting conventions
- **`qe-fig-007`** — Keep figure box and spines
- **`qe-fig-010`** — Plotly figures require latex directive
- **`qe-link-001`** — Use markdown style links for lectures in same lecture series
- **`qe-math-012`** *(proposed)* — Multiplication via \cdot or juxtaposition, never *
<!-- /qe:series-clean -->

## Series-level recommendations

<!-- qe:series-recommendations -->
Ordered by HIGH lectures cleared per unit of work, not by size of the finding.

1. **`qe-math-002` on the four HIGH lectures Writing does not floor** — `tax_smoothing_2`
   (59 occurrences), `markov_jump_lq` (47), `tax_smoothing_1` (11), `lqramsey` (10). These
   are the only lectures in the series where Math work on its own can move the bucket;
   every other HIGH lecture is also floored by Writing and stays HIGH until a reading pass
   lands there. Mostly a mechanical `'` → `\top` rewrite, but the check has to tell a
   transpose apostrophe from a derivative, so each site wants an eye. `tax_smoothing_2`
   needs its Figures floor cleared too — `qe-fig-003` (9 embedded titles) and `qe-fig-006`
   (9 axis labels); `lqramsey`'s Math is as much **`qe-math-010`** *(proposed)* (19) as
   transpose.

2. **`qe-math-002` across the other ten Math-floored lectures** — **(14 / 52, 416
   occurrences)** series-wide, 381 of them inside Math-floored lectures. `lqcontrol` holds
   85, `lagrangian_lqdp` 69. Same scripted-with-review work as item 1, and it lifts the Math
   mean, but these lectures stay HIGH on Writing regardless, so it buys score rather than
   bucket. `lqcontrol` and `lq_inventories` also carry **`qe-math-003`** (17 `pmatrix`
   environments each) — a clean regex, worth doing in the same edit.

3. **Fix the synced lectures upstream, not here.** `cross_product_trick` is byte-identical
   to the `lecture-python.myst` copy and carries the series' only build-risk finding —
   `qe-math-006`, five `align` environments inside `$$` — plus the malformed
   `` {eq}`eq:Kalman102} `` at line 133. Both belong in `lecture-python.myst`; an edit here
   is overwritten at the next sync. Three more want a re-sync rather than an edit, because
   the upstream copy is already ahead: `mccall_q` (six `qe-writing-006` headings and four
   repeated spaces that upstream no longer has), `os_egm` and `os_egm_jax` (each carries a
   `qe-code-003` the upstream copy does not — the missing install cell). By contrast
   `ifp_advanced` has diverged, so its raw `\label{a:y0}` at line 158 (`qe-math-007`) needs
   its own edit here even though the same defect sits at the same line upstream.

4. **The Writing reading pass — the only route that clears the 30.** `qe-writing-003` (45 of
   52 lectures), `qe-writing-002` (39), `qe-writing-007` (36), `qe-writing-005` (31) are
   judgment rules; no script helps, and every Writing-floored lecture carries at least one of
   them. Work down from the lowest overalls, where the mechanical half is thick enough to
   fold into the same edit: `smoothing` (6.0), `perm_income_cons` (6.5), `rs_inventory_q`
   (6.5), `cons_news` (6.6), `lqcontrol` (6.6). Pair it with **`qe-writing-008`** **(40 / 52,
   1,578 occurrences)** and **`qe-writing-006`** **(22 / 52, 146)** in the same pass — both
   are near-scripted, but on their own they clear no lecture out of HIGH in this series.

5. **Figures sweeps — broad, cheap, and low-leverage on the HIGH list.**
   **`qe-fig-005`** **(42 / 52, 164)**, **`qe-fig-008`** **(38 / 52, 219)** and
   **`qe-fig-001`** **(31 / 52, 102)** are scriptable; **`qe-fig-003`** **(30 / 52, 105)** is
   a reading pass, because each embedded title has to be rewritten as a caption. Only two
   lectures are Figures-floored — `smoothing_tax` (20 `qe-fig-008` sites, the most in the
   series) and `tax_smoothing_2` — so this raises the series mean rather than shortening the
   HIGH list.

6. **Leave `qe-ref-001` (20 / 52, 45) and `qe-link-002` (15 / 52, 53) last.** References at
   9.3 and Links at 9.5 are already near the top of their range, and neither rule floors a
   lecture anywhere in the series. `tax_smoothing_1` holds 9 of the 45 citation findings if
   one lecture is wanted for a first pass.
<!-- /qe:series-recommendations -->

## Lectures ranked by priority (lowest score first)

Scores are 0–10 per category; **Overall** is the mean of the in-scope categories, and
**Priority** follows [spec §4](../spec.md). A dash means the category is not applicable to
that lecture. Click a lecture for its full report.

<!-- qe:series-ranked -->
| # | Lecture | Writing | Math | Code | Figures | References | Links | Admon | Overall | Priority |
|---|---------|---|---|---|---|---|---|---|---------|----------|
| 1 | [cross_product_trick](cross_product_trick.md) | 4 | 3 | — | — | — | 10 | — | **5.7** | HIGH |
| 2 | [smoothing](smoothing.md) | 3 | 3 | 7.5 | 5 | 10 | 7.5 | — | **6.0** | HIGH |
| 3 | [tax_smoothing_1](tax_smoothing_1.md) | 4.5 | 4 | 7 | 6 | 7.5 | 9 | — | **6.3** | HIGH |
| 4 | [markov_jump_lq](markov_jump_lq.md) | 5 | 3 | 7.5 | 5.5 | 8.5 | 9 | — | **6.4** | HIGH |
| 5 | [perm_income_cons](perm_income_cons.md) | 3 | 4 | 7.5 | 5.5 | 10 | 9 | — | **6.5** | HIGH |
| 6 | [rs_inventory_q](rs_inventory_q.md) | 3 | 6 | 8.5 | 5 | — | 10 | — | **6.5** | HIGH |
| 7 | [tax_smoothing_2](tax_smoothing_2.md) | 5.5 | 3.5 | 7.5 | 4 | 8.5 | 10 | — | **6.5** | HIGH |
| 8 | [cons_news](cons_news.md) | 3 | 4.5 | 8.5 | 6 | 10 | 7.5 | — | **6.6** | HIGH |
| 9 | [lqcontrol](lqcontrol.md) | 3 | 3 | 7.5 | 4.5 | 10 | 8 | 10 | **6.6** | HIGH |
| 10 | [lagrangian_lqdp](lagrangian_lqdp.md) | 3 | 3 | 7 | — | 10 | 7.5 | 10 | **6.8** | HIGH |
| 11 | [ifp_advanced](ifp_advanced.md) | 3 | 3 | 6.5 | 7 | 8.5 | 10 | 10 | **6.9** | HIGH |
| 12 | [amss2](amss2.md) | 3.5 | 5.5 | 8.5 | 6 | 8.5 | 10 | — | **7.0** | HIGH |
| 13 | [perm_income](perm_income.md) | 3 | 4 | 7.5 | 6 | 8.5 | 10 | 10 | **7.0** | HIGH |
| 14 | [discrete_dp](discrete_dp.md) | 4 | 7 | 6.5 | 6 | 9 | 7 | 10 | **7.1** | HIGH |
| 15 | [dyn_stack](dyn_stack.md) | 4 | 5 | 8.5 | 5 | 10 | 7.5 | 10 | **7.1** | HIGH |
| 16 | [smoothing_tax](smoothing_tax.md) | 3.5 | 6 | 7.5 | 4 | 10 | 9 | 10 | **7.1** | HIGH |
| 17 | [amss3](amss3.md) | 3.5 | 5.5 | 8.5 | 5.5 | 7.5 | 10 | 10 | **7.2** | HIGH |
| 18 | [calvo](calvo.md) | 3 | 5.5 | 8.5 | 7 | 8.5 | 8 | 10 | **7.2** | HIGH |
| 19 | [inventory_q](inventory_q.md) | 4 | 5.5 | 7.5 | 6 | 10 | 10 | — | **7.2** | HIGH |
| 20 | [mccall_model](mccall_model.md) | 3 | 7 | 6.5 | 6 | 10 | 8 | 10 | **7.2** | HIGH |
| 21 | [amss](amss.md) | 3.5 | 3.5 | 8 | 6 | 10 | 10 | 10 | **7.3** | HIGH |
| 22 | [opt_tax_recur](opt_tax_recur.md) | 4 | 5 | 8.5 | 4.5 | 9 | 10 | 10 | **7.3** | HIGH |
| 23 | [calvo_machine_learn](calvo_machine_learn.md) | 4 | 3 | 6.5 | 8 | 10 | 10 | 10 | **7.4** | HIGH |
| 24 | [lq_inventories](lq_inventories.md) | 4 | 3 | 7.5 | 7 | 10 | 10 | 10 | **7.4** | HIGH |
| 25 | [odu](odu.md) | 3 | 9 | 7.5 | 5 | 9 | 8 | 10 | **7.4** | HIGH |
| 26 | [mccall_q](mccall_q.md) | 3 | 9.5 | 7 | 7 | 9 | 10 | — | **7.6** | HIGH |
| 27 | [chang_ramsey](chang_ramsey.md) | 3 | 10 | 8.5 | 6 | 8.5 | 10 | — | **7.7** | HIGH |
| 28 | [os_stochastic](os_stochastic.md) | 3 | 7.5 | 8 | 7.5 | 10 | 8 | 10 | **7.7** | HIGH |
| 29 | [ifp_egm_transient_shocks](ifp_egm_transient_shocks.md) | 3.5 | 9.5 | 7.5 | 5.5 | 9 | 10 | 10 | **7.9** | HIGH |
| 30 | [lqramsey](lqramsey.md) | 6.5 | 3 | 7.5 | 8 | 10 | 10 | 10 | **7.9** | HIGH |
| 31 | [os_numerical](os_numerical.md) | 4.5 | 10 | 7.5 | 5.5 | — | 10 | 10 | **7.9** | LOW |
| 32 | [calvo_abreu](calvo_abreu.md) | 4 | 9 | 7.5 | 9 | 8.5 | 10 | — | **8.0** | HIGH |
| 33 | [ifp_egm](ifp_egm.md) | 3 | 9 | 7.5 | 6.5 | 10 | 10 | 10 | **8.0** | HIGH |
| 34 | [ifp_opi](ifp_opi.md) | 5 | 10 | 8 | 6 | — | 9 | 10 | **8.0** | LOW |
| 35 | [jv](jv.md) | 3.5 | 9.5 | 7.5 | 6.5 | 9 | 10 | 10 | **8.0** | HIGH |
| 36 | [mccall_model_with_sep_markov](mccall_model_with_sep_markov.md) | 5 | 10 | 7.5 | 5.5 | — | 10 | 10 | **8.0** | LOW |
| 37 | [tax_smoothing_3](tax_smoothing_3.md) | 6 | 8.5 | 10 | 5 | 8.5 | 10 | — | **8.0** | LOW |
| 38 | [un_insure](un_insure.md) | 4.5 | 9.5 | 7.5 | 5.5 | 9 | 10 | 10 | **8.0** | LOW |
| 39 | [mccall_fitted_vfi](mccall_fitted_vfi.md) | 7 | 8 | 7.5 | 5.5 | 9 | 10 | 10 | **8.1** | LOW |
| 40 | [os_egm_jax](os_egm_jax.md) | 7 | 10 | 5.5 | 7 | — | 10 | 10 | **8.2** | LOW |
| 41 | [os_time_iter](os_time_iter.md) | 5.5 | 7.5 | 8 | 8 | 9 | 10 | 10 | **8.3** | LOW |
| 42 | [chang_credible](chang_credible.md) | 3 | 10 | 8.5 | 9.5 | 10 | 10 | — | **8.5** | HIGH |
| 43 | [ifp_discrete](ifp_discrete.md) | 6 | 7 | 8 | 8.5 | 10 | 10 | 10 | **8.5** | LOW |
| 44 | [mccall_model_with_separation](mccall_model_with_separation.md) | 6.5 | 8.5 | 6.5 | 8.5 | 10 | 10 | 10 | **8.6** | NONE |
| 45 | [mccall_persist_trans](mccall_persist_trans.md) | 9.5 | 6.5 | 6 | 8 | 10 | 10 | 10 | **8.6** | NONE |
| 46 | [os_egm](os_egm.md) | 5.5 | 9.5 | 7.5 | 9 | 10 | 10 | 10 | **8.8** | NONE |
| 47 | [career](career.md) | 8 | 9.5 | 8.5 | 6.5 | 10 | 10 | 10 | **8.9** | NONE |
| 48 | [os](os.md) | 6 | 9 | 9 | 8 | 10 | 10 | 10 | **8.9** | NONE |
| 49 | [short_path](short_path.md) | 7.5 | 10 | 8.5 | 8 | — | 10 | 10 | **9.0** | NONE |
| 50 | [intro](intro.md) | 10 | — | — | — | — | 10 | — | **10.0** | NONE |
| 51 | [status](status.md) | 10 | — | — | — | — | 10 | — | **10.0** | NONE |
| 52 | [zreferences](zreferences.md) | 10 | — | — | — | — | 10 | — | **10.0** | NONE |
<!-- /qe:series-ranked -->
