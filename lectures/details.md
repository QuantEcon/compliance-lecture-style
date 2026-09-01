# Full findings & remediation plan

The complete cross-series breakdown behind the [front-page triage](intro.md). Start with
the front page to decide *where* to focus; come here for the full numbers, every recurring
rule, every HIGH-priority lecture, and the ordered remediation plan.

Every table on this page is generated from
[`lectures/data/*.csv`](https://github.com/QuantEcon/compliance-lecture-style/tree/main/lectures/data)
by `tools/qestyle_report.py`, so it cannot disagree with the per-lecture reports.

---

## What was audited

One commit per series, pinned at audit time. Re-running the pipeline against these commits
reproduces every number on this page exactly.

<!-- qe:snapshot -->
| Series | Lectures | Snapshot commit | Snapshot date |
|--------|---------:|-----------------|---------------|
| `lecture-python-intro` | 56 | `a12d17c0ef` | 2026-08-23 |
| `lecture-python-programming` | 27 | `ceec881028` | 2026-08-21 |
| `lecture-python.myst` | 145 | `e25fdf2345` | 2026-08-24 |
| `lecture-python-advanced.myst` | 68 | `b83d6da399` | 2026-08-19 |
| `lecture-dp` | 52 | `c30490a2f4` | 2026-08-07 |
<!-- /qe:snapshot -->

---

## Full scoreboard

Average score per category, per series (0–10). **Bold** marks each series' weakest
category.

<!-- qe:full-scoreboard -->
| # | Series | Lectures | Writing | Math | Code | Figures | References | Links | Admon | **Overall** | HIGH | MEDIUM | LOW | NONE |
|---|--------|----------|---|---|---|---|---|---|---|-------------|------|--------|-----|------|
| 1 | [lecture-python-advanced.myst](lecture-python-advanced.myst/index.md) | 68 | **4.6** | 5.8 | 7.3 | 6.3 | 9.2 | 9.2 | 10.0 | **7.4** | 43 | 0 | 20 | 5 |
| 2 | [lecture-python.myst](lecture-python.myst/index.md) | 145 | **4.5** | 7.0 | 7.6 | 6.5 | 9.5 | 9.8 | 10.0 | **7.7** | 81 | 1 | 46 | 17 |
| 3 | [lecture-dp](lecture-dp/index.md) | 52 | **4.7** | 6.6 | 7.7 | 6.4 | 9.3 | 9.5 | 10.0 | **7.7** | 34 | 0 | 9 | 9 |
| 4 | [lecture-python-programming](lecture-python-programming/index.md) | 27 | **4.1** | 9.0 | 8.4 | 7.3 | N/A | 9.8 | 9.9 | **8.0** | 20 | 0 | 5 | 2 |
| 5 | [lecture-python-intro](lecture-python-intro/index.md) | 56 | **5.2** | 8.6 | 7.3 | 6.5 | 9.3 | 9.7 | 10.0 | **8.1** | 19 | 0 | 28 | 9 |
|   | **TOTAL / corpus average** | **348** | **4.6** | **7.0** | **7.5** | **6.5** | **9.4** | **9.6** | **10.0** | **7.7** | **197** | **1** | **108** | **42** |
<!-- /qe:full-scoreboard -->

See the [charts](charts.md) for the visual version.

---

## Every recurring rule

All rules with at least one violation in the corpus, ranked by how many lectures they
reach. Rules tagged **(proposed)** are documented in the style guide but not yet in the
`action-style-guide` registry.

<!-- qe:systemic -->
### 1. `qe-fig-005` — Descriptive figure names for cross-referencing (273 / 348 lectures, 1115 occurrences)
- `lecture-python.myst` 110 / 145 · `lecture-python-advanced.myst` 54 / 68 · `lecture-python-intro` 46 / 56 · `lecture-dp` 42 / 52 · `lecture-python-programming` 21 / 27

### 2. `qe-writing-008` — Remove excessive whitespace between words (237 / 348 lectures, 7122 occurrences)
- `lecture-python.myst` 89 / 145 · `lecture-python-advanced.myst` 53 / 68 · `lecture-dp` 40 / 52 · `lecture-python-intro` 39 / 56 · `lecture-python-programming` 16 / 27

### 3. `qe-fig-001` — Do not set figure size unless necessary (224 / 348 lectures, 892 occurrences)
- `lecture-python.myst` 107 / 145 · `lecture-python-advanced.myst` 47 / 68 · `lecture-dp` 31 / 52 · `lecture-python-intro` 30 / 56 · `lecture-python-programming` 9 / 27

### 4. `qe-fig-008` — Use lw=2 for line charts (196 / 348 lectures, 1194 occurrences)
- `lecture-python.myst` 69 / 145 · `lecture-python-advanced.myst` 40 / 68 · `lecture-dp` 38 / 52 · `lecture-python-intro` 35 / 56 · `lecture-python-programming` 14 / 27

### 5. `qe-writing-001` — Use one sentence per paragraph (175 / 348 lectures, 448 occurrences)
- `lecture-python.myst` 65 / 145 · `lecture-python-advanced.myst` 42 / 68 · `lecture-python-intro` 30 / 56 · `lecture-dp` 23 / 52 · `lecture-python-programming` 15 / 27

### 6. `qe-fig-003` — No matplotlib embedded titles (165 / 348 lectures, 630 occurrences)
- `lecture-python.myst` 79 / 145 · `lecture-python-advanced.myst` 36 / 68 · `lecture-dp` 30 / 52 · `lecture-python-intro` 15 / 56 · `lecture-python-programming` 5 / 27

### 7. `qe-writing-006` — Capitalize lecture titles properly (132 / 348 lectures, 768 occurrences)
- `lecture-python.myst` 71 / 145 · `lecture-python-programming` 23 / 27 · `lecture-dp` 22 / 52 · `lecture-python-intro` 13 / 56 · `lecture-python-advanced.myst` 3 / 68

### 8. `qe-math-010` (proposed) — Blackboard \mathbb{P}, \mathbb{E}, \mathbb{V} with braces (124 / 348 lectures, 1608 occurrences)
- `lecture-python.myst` 60 / 145 · `lecture-python-advanced.myst` 33 / 68 · `lecture-dp` 20 / 52 · `lecture-python-intro` 8 / 56 · `lecture-python-programming` 3 / 27

### 9. `qe-ref-001` — Use correct citation style (106 / 348 lectures, 291 occurrences)
- `lecture-python.myst` 36 / 145 · `lecture-python-advanced.myst` 35 / 68 · `lecture-dp` 20 / 52 · `lecture-python-intro` 15 / 56

### 10. `qe-writing-004` — Avoid unnecessary capitalization in narrative text (105 / 348 lectures, 339 occurrences)
- `lecture-python.myst` 43 / 145 · `lecture-python-advanced.myst` 24 / 68 · `lecture-python-intro` 18 / 56 · `lecture-dp` 14 / 52 · `lecture-python-programming` 6 / 27

### 11. `qe-link-002` — Use doc links for cross-series references (73 / 348 lectures, 205 occurrences)
- `lecture-python-advanced.myst` 26 / 68 · `lecture-python.myst` 20 / 145 · `lecture-dp` 15 / 52 · `lecture-python-intro` 9 / 56 · `lecture-python-programming` 3 / 27

### 12. `qe-code-002` — Use Unicode symbols for Greek letters in code (66 / 348 lectures, 798 occurrences)
- `lecture-python.myst` 32 / 145 · `lecture-python-advanced.myst` 17 / 68 · `lecture-python-intro` 10 / 56 · `lecture-dp` 7 / 52

### 13. `qe-math-002` — Use \top for transpose notation (63 / 348 lectures, 1597 occurrences)
- `lecture-python.myst` 24 / 145 · `lecture-python-advanced.myst` 20 / 68 · `lecture-dp` 14 / 52 · `lecture-python-intro` 4 / 56 · `lecture-python-programming` 1 / 27

### 14. `qe-fig-006` — Lowercase axis labels (60 / 348 lectures, 298 occurrences)
- `lecture-python.myst` 21 / 145 · `lecture-python-advanced.myst` 15 / 68 · `lecture-dp` 12 / 52 · `lecture-python-intro` 11 / 56 · `lecture-python-programming` 1 / 27

### 15. `qe-fig-004` — Caption formatting conventions (60 / 348 lectures, 189 occurrences)
- `lecture-python.myst` 34 / 145 · `lecture-python-intro` 17 / 56 · `lecture-python-advanced.myst` 9 / 68

### 16. `qe-math-003` — Use square brackets for matrix notation (46 / 348 lectures, 363 occurrences)
- `lecture-python.myst` 21 / 145 · `lecture-python-advanced.myst` 15 / 68 · `lecture-dp` 6 / 52 · `lecture-python-intro` 4 / 56

### 17. `qe-fig-002` — Prefer code-generated figures (38 / 348 lectures, 104 occurrences)
- `lecture-python-advanced.myst` 12 / 68 · `lecture-python.myst` 10 / 145 · `lecture-python-intro` 6 / 56 · `lecture-dp` 5 / 52 · `lecture-python-programming` 5 / 27

### 18. `qe-math-011` (proposed) — Distribution names in plain letters, not \mathcal / \mathbb (34 / 348 lectures, 134 occurrences)
- `lecture-python-advanced.myst` 18 / 68 · `lecture-python.myst` 10 / 145 · `lecture-dp` 5 / 52 · `lecture-python-intro` 1 / 56

### 19. `qe-math-004` — Do not use bold face for matrices or vectors (33 / 348 lectures, 584 occurrences)
- `lecture-python.myst` 18 / 145 · `lecture-python-advanced.myst` 6 / 68 · `lecture-dp` 5 / 52 · `lecture-python-intro` 4 / 56

### 20. `qe-code-004` — Use quantecon Timer context manager (31 / 348 lectures, 144 occurrences)
- `lecture-python.myst` 15 / 145 · `lecture-dp` 8 / 52 · `lecture-python-advanced.myst` 4 / 68 · `lecture-python-intro` 3 / 56 · `lecture-python-programming` 1 / 27

### 21. `qe-writing-009` (proposed) — Write "IID" — not "i.i.d." or "iid" (30 / 348 lectures, 61 occurrences)
- `lecture-python.myst` 15 / 145 · `lecture-python-advanced.myst` 10 / 68 · `lecture-dp` 4 / 52 · `lecture-python-intro` 1 / 56

### 22. `qe-code-003` — Package installation at lecture top (25 / 348 lectures, 32 occurrences)
- `lecture-python.myst` 8 / 145 · `lecture-dp` 6 / 52 · `lecture-python-advanced.myst` 6 / 68 · `lecture-python-programming` 3 / 27 · `lecture-python-intro` 2 / 56

### 23. `qe-math-001` — Prefer UTF-8 unicode for simple parameter mentions, be consistent (15 / 348 lectures, 28 occurrences)
- `lecture-python.myst` 9 / 145 · `lecture-dp` 3 / 52 · `lecture-python-advanced.myst` 1 / 68 · `lecture-python-intro` 1 / 56 · `lecture-python-programming` 1 / 27

### 24. `qe-fig-007` — Keep figure box and spines (13 / 348 lectures, 71 occurrences)
- `lecture-python-intro` 6 / 56 · `lecture-python.myst` 4 / 145 · `lecture-python-advanced.myst` 2 / 68 · `lecture-python-programming` 1 / 27

### 25. `qe-link-001` — Use markdown style links for lectures in same lecture series (12 / 348 lectures, 21 occurrences)
- `lecture-python.myst` 7 / 145 · `lecture-python-advanced.myst` 3 / 68 · `lecture-python-intro` 2 / 56

### 26. `qe-math-005` — Use curly brackets for sequences (7 / 348 lectures, 14 occurrences)
- `lecture-python.myst` 3 / 145 · `lecture-dp` 2 / 52 · `lecture-python-advanced.myst` 1 / 68 · `lecture-python-intro` 1 / 56

### 27. `qe-code-005` — Use quantecon timeit for benchmarking (7 / 348 lectures, 13 occurrences)
- `lecture-dp` 3 / 52 · `lecture-python.myst` 3 / 145 · `lecture-python-advanced.myst` 1 / 68

### 28. `qe-math-013` (proposed) — Reference equations via `` {eq}`label` `` (6 / 348 lectures, 6 occurrences)
- `lecture-dp` 3 / 52 · `lecture-python-advanced.myst` 2 / 68 · `lecture-python.myst` 1 / 145

### 29. `qe-math-006` — Use aligned environment correctly for PDF compatibility (5 / 348 lectures, 14 occurrences)
- `lecture-python.myst` 3 / 145 · `lecture-dp` 1 / 52 · `lecture-python-advanced.myst` 1 / 68

### 30. `qe-math-012` (proposed) — Multiplication via \cdot or juxtaposition, never * (4 / 348 lectures, 6 occurrences)
- `lecture-python-intro` 2 / 56 · `lecture-python-programming` 1 / 27 · `lecture-python.myst` 1 / 145

### 31. `qe-fig-010` — Plotly figures require latex directive (4 / 348 lectures, 4 occurrences)
- `lecture-python-advanced.myst` 3 / 68 · `lecture-python.myst` 1 / 145

### 32. `qe-math-008` — Explain special notation (vectors/matrices) (3 / 348 lectures, 3 occurrences)
- `lecture-dp` 1 / 52 · `lecture-python-advanced.myst` 1 / 68 · `lecture-python.myst` 1 / 145

### 33. `qe-math-007` — Use automatic equation numbering, not manual tags (2 / 348 lectures, 2 occurrences)
- `lecture-dp` 1 / 52 · `lecture-python.myst` 1 / 145

### 34. `qe-admon-003` — Use tick count management for nested directives (1 / 348 lectures, 2 occurrences)
- `lecture-python-programming` 1 / 27

### 35. `qe-admon-002` — Use dropdown class for solutions (1 / 348 lectures, 1 occurrences)
- `lecture-python-intro` 1 / 56
<!-- /qe:systemic -->

---

## All HIGH-priority lectures

HIGH = overall ≤ 5.0 **or** any single in-scope category ≤ 4 (spec §4). In this pass every
HIGH lecture was triggered by the category floor; none has an overall at or below 5.0. The
**Floor** column is the weakest category's score — the thing to fix.

<!-- qe:high-list -->
| Series | Lecture | Writing | Math | Code | Figures | References | Links | Admon | Overall | Floor |
|--------|---------|---|---|---|---|---|---|---|---------|-------|
| python.myst | [cross_product_trick](lecture-python.myst/cross_product_trick.md) | 3.5 | 3.0 | — | — | — | 10.0 | — | **5.5** | 3.0 |
| advanced | [hs_recursive_models](lecture-python-advanced.myst/hs_recursive_models.md) | 3.0 | 3.0 | — | — | 8.5 | 8.0 | — | **5.6** | 3.0 |
| dp | [cross_product_trick](lecture-dp/cross_product_trick.md) | 4.0 | 3.0 | — | — | — | 10.0 | — | **5.7** | 3.0 |
| python.myst | [qr_decomp](lecture-python.myst/qr_decomp.md) | 3.0 | 3.0 | 7.5 | — | — | 10.0 | — | **5.9** | 3.0 |
| dp | [smoothing](lecture-dp/smoothing.md) | 3.0 | 3.0 | 7.5 | 5.0 | 10.0 | 7.5 | — | **6.0** | 3.0 |
| advanced | [entropy](lecture-python-advanced.myst/entropy.md) | 3.0 | 3.0 | — | 7.0 | 8.5 | 8.5 | — | **6.0** | 3.0 |
| advanced | [smoothing](lecture-python-advanced.myst/smoothing.md) | 3.0 | 3.0 | 7.5 | 5.0 | 10.0 | 7.5 | — | **6.0** | 3.0 |
| python.myst | [navy_captain](lecture-python.myst/navy_captain.md) | 3.0 | 6.5 | 7.5 | 3.0 | — | 10.0 | — | **6.0** | 3.0 |
| python.myst | [two_auctions](lecture-python.myst/two_auctions.md) | 3.0 | 4.5 | 6.5 | 3.0 | 10.0 | 9.0 | — | **6.0** | 3.0 |
| advanced | [knowing_forecasts_of_others](lecture-python-advanced.myst/knowing_forecasts_of_others.md) | 3.0 | 3.0 | 6.0 | 9.0 | 7.5 | 8.0 | — | **6.1** | 3.0 |
| advanced | [match_transport](lecture-python-advanced.myst/match_transport.md) | 3.0 | 9.5 | 4.5 | 3.0 | 8.5 | 8.0 | — | **6.1** | 3.0 |
| python.myst | [likelihood_var](lecture-python.myst/likelihood_var.md) | 4.5 | 3.5 | 7.5 | 5.0 | — | 10.0 | — | **6.1** | 3.5 |
| python.myst | [prob_matrix](lecture-python.myst/prob_matrix.md) | 3.0 | 3.0 | 5.5 | 5.0 | — | 10.0 | 10.0 | **6.1** | 3.0 |
| advanced | [five_preferences](lecture-python-advanced.myst/five_preferences.md) | 3.0 | 6.0 | 7.0 | 4.0 | 7.0 | 10.0 | — | **6.2** | 3.0 |
| python.myst | [two_computation](lecture-python.myst/two_computation.md) | 5.5 | 3.0 | 6.0 | 3.0 | 10.0 | 10.0 | — | **6.2** | 3.0 |
| dp | [tax_smoothing_1](lecture-dp/tax_smoothing_1.md) | 4.5 | 4.0 | 7.0 | 6.0 | 7.5 | 9.0 | — | **6.3** | 4.0 |
| advanced | [markov_jump_lq](lecture-python-advanced.myst/markov_jump_lq.md) | 5.0 | 3.0 | 7.0 | 5.5 | 8.5 | 9.0 | — | **6.3** | 3.0 |
| advanced | [tax_smoothing_1](lecture-python-advanced.myst/tax_smoothing_1.md) | 4.0 | 4.5 | 7.0 | 6.0 | 7.5 | 9.0 | — | **6.3** | 4.0 |
| dp | [markov_jump_lq](lecture-dp/markov_jump_lq.md) | 5.0 | 3.0 | 7.5 | 5.5 | 8.5 | 9.0 | — | **6.4** | 3.0 |
| advanced | [asset_pricing_lph](lecture-python-advanced.myst/asset_pricing_lph.md) | 3.0 | 3.0 | 5.5 | 7.5 | 8.5 | 7.5 | 10.0 | **6.4** | 3.0 |
| advanced | [rob_markov_perf](lecture-python-advanced.myst/rob_markov_perf.md) | 3.5 | 4.0 | 6.5 | 8.0 | 9.0 | 7.5 | — | **6.4** | 3.5 |
| advanced | [tax_smoothing_2](lecture-python-advanced.myst/tax_smoothing_2.md) | 5.0 | 3.5 | 7.5 | 4.0 | 8.5 | 10.0 | — | **6.4** | 3.5 |
| python.myst | [rs_inventory_q](lecture-python.myst/rs_inventory_q.md) | 3.0 | 6.5 | 7.5 | 5.0 | — | 10.0 | — | **6.4** | 3.0 |
| dp | [perm_income_cons](lecture-dp/perm_income_cons.md) | 3.0 | 4.0 | 7.5 | 5.5 | 10.0 | 9.0 | — | **6.5** | 3.0 |
| dp | [rs_inventory_q](lecture-dp/rs_inventory_q.md) | 3.0 | 6.0 | 8.5 | 5.0 | — | 10.0 | — | **6.5** | 3.0 |
| dp | [tax_smoothing_2](lecture-dp/tax_smoothing_2.md) | 5.5 | 3.5 | 7.5 | 4.0 | 8.5 | 10.0 | — | **6.5** | 3.5 |
| advanced | [black_litterman](lecture-python-advanced.myst/black_litterman.md) | 3.0 | 3.0 | 7.0 | 4.0 | 10.0 | 8.5 | 10.0 | **6.5** | 3.0 |
| python.myst | [linear_models](lecture-python.myst/linear_models.md) | 3.0 | 3.0 | 6.0 | 8.0 | — | 9.0 | 10.0 | **6.5** | 3.0 |
| python.myst | [multivariate_normal](lecture-python.myst/multivariate_normal.md) | 3.0 | 3.0 | 7.5 | 5.5 | — | 10.0 | 10.0 | **6.5** | 3.0 |
| python.myst | [perm_income_cons](lecture-python.myst/perm_income_cons.md) | 3.0 | 4.0 | 7.5 | 5.5 | 10.0 | 9.0 | — | **6.5** | 3.0 |
| dp | [cons_news](lecture-dp/cons_news.md) | 3.0 | 4.5 | 8.5 | 6.0 | 10.0 | 7.5 | — | **6.6** | 3.0 |
| dp | [lqcontrol](lecture-dp/lqcontrol.md) | 3.0 | 3.0 | 7.5 | 4.5 | 10.0 | 8.0 | 10.0 | **6.6** | 3.0 |
| advanced | [additive_functionals](lecture-python-advanced.myst/additive_functionals.md) | 5.5 | 3.5 | 7.0 | 3.5 | 9.0 | 7.5 | 10.0 | **6.6** | 3.5 |
| advanced | [cons_news](lecture-python-advanced.myst/cons_news.md) | 3.0 | 4.5 | 8.5 | 6.0 | 10.0 | 7.5 | — | **6.6** | 3.0 |
| python.myst | [likelihood_ratio_process](lecture-python.myst/likelihood_ratio_process.md) | 3.0 | 3.0 | 7.0 | 3.5 | 10.0 | 10.0 | 10.0 | **6.6** | 3.0 |
| dp | [lagrangian_lqdp](lecture-dp/lagrangian_lqdp.md) | 3.0 | 3.0 | 7.0 | — | 10.0 | 7.5 | 10.0 | **6.8** | 3.0 |
| advanced | [amss2](lecture-python-advanced.myst/amss2.md) | 3.5 | 5.5 | 7.5 | 6.0 | 8.5 | 10.0 | — | **6.8** | 3.5 |
| advanced | [dyn_stack](lecture-python-advanced.myst/dyn_stack.md) | 3.5 | 4.0 | 7.5 | 5.0 | 10.0 | 7.5 | 10.0 | **6.8** | 3.5 |
| advanced | [robustness](lecture-python-advanced.myst/robustness.md) | 3.0 | 3.0 | 7.5 | 6.5 | 10.0 | 7.5 | 10.0 | **6.8** | 3.0 |
| python.myst | [lagrangian_lqdp](lecture-python.myst/lagrangian_lqdp.md) | 3.0 | 3.0 | 7.0 | — | 10.0 | 7.5 | 10.0 | **6.8** | 3.0 |
| python.myst | [prob_meaning](lecture-python.myst/prob_meaning.md) | 3.0 | 7.5 | 6.0 | 4.5 | — | 10.0 | 10.0 | **6.8** | 3.0 |
| dp | [ifp_advanced](lecture-dp/ifp_advanced.md) | 3.0 | 3.0 | 6.5 | 7.0 | 8.5 | 10.0 | 10.0 | **6.9** | 3.0 |
| advanced | [cagan_rational_expectations](lecture-python-advanced.myst/cagan_rational_expectations.md) | 5.5 | 3.0 | 6.0 | 5.5 | 8.5 | 10.0 | 10.0 | **6.9** | 3.0 |
| python.myst | [ifp_advanced](lecture-python.myst/ifp_advanced.md) | 3.0 | 3.0 | 7.0 | 7.0 | 8.5 | 10.0 | 10.0 | **6.9** | 3.0 |
| python.myst | [linear_algebra](lecture-python.myst/linear_algebra.md) | 3.0 | 4.5 | 7.5 | 5.5 | 10.0 | 7.5 | 10.0 | **6.9** | 3.0 |
| python.myst | [markov_asset](lecture-python.myst/markov_asset.md) | 3.0 | 4.5 | 7.5 | 6.5 | 8.5 | 8.0 | 10.0 | **6.9** | 3.0 |
| python.myst | [misspecified_recovery](lecture-python.myst/misspecified_recovery.md) | 3.0 | 3.0 | 5.5 | 6.5 | 10.0 | 10.0 | 10.0 | **6.9** | 3.0 |
| python.myst | [multi_hyper](lecture-python.myst/multi_hyper.md) | 3.5 | 6.5 | 7.5 | 7.0 | — | 10.0 | — | **6.9** | 3.5 |
| python.myst | [pandas_panel](lecture-python.myst/pandas_panel.md) | 3.5 | — | 7.5 | 4.5 | — | 9.0 | 10.0 | **6.9** | 3.5 |
| python.myst | [stats_examples](lecture-python.myst/stats_examples.md) | 3.0 | 4.5 | 7.0 | 7.0 | — | 10.0 | 10.0 | **6.9** | 3.0 |
| dp | [amss2](lecture-dp/amss2.md) | 3.5 | 5.5 | 8.5 | 6.0 | 8.5 | 10.0 | — | **7.0** | 3.5 |
| dp | [perm_income](lecture-dp/perm_income.md) | 3.0 | 4.0 | 7.5 | 6.0 | 8.5 | 10.0 | 10.0 | **7.0** | 3.0 |
| advanced | [stationary_densities](lecture-python-advanced.myst/stationary_densities.md) | 4.0 | 6.0 | 7.0 | 5.5 | 9.0 | 7.5 | 10.0 | **7.0** | 4.0 |
| advanced | [subjective_beliefs_business_cycles](lecture-python-advanced.myst/subjective_beliefs_business_cycles.md) | 3.0 | 3.0 | 7.0 | 7.0 | 9.0 | 10.0 | 10.0 | **7.0** | 3.0 |
| python.myst | [ols](lecture-python.myst/ols.md) | 3.0 | 7.0 | 7.5 | 5.0 | 7.5 | 9.0 | 10.0 | **7.0** | 3.0 |
| python.myst | [perm_income](lecture-python.myst/perm_income.md) | 3.0 | 4.0 | 7.5 | 6.0 | 8.5 | 10.0 | 10.0 | **7.0** | 3.0 |
| python.myst | [phillips_lost_conquest](lecture-python.myst/phillips_lost_conquest.md) | 3.5 | 6.0 | 7.5 | 4.5 | 7.5 | 10.0 | 10.0 | **7.0** | 3.5 |
| python.myst | [wald_friedman_2](lecture-python.myst/wald_friedman_2.md) | 3.0 | 6.0 | 7.5 | 5.0 | 9.0 | 8.5 | 10.0 | **7.0** | 3.0 |
| dp | [discrete_dp](lecture-dp/discrete_dp.md) | 4.0 | 7.0 | 6.5 | 6.0 | 9.0 | 7.0 | 10.0 | **7.1** | 4.0 |
| dp | [dyn_stack](lecture-dp/dyn_stack.md) | 4.0 | 5.0 | 8.5 | 5.0 | 10.0 | 7.5 | 10.0 | **7.1** | 4.0 |
| dp | [smoothing_tax](lecture-dp/smoothing_tax.md) | 3.5 | 6.0 | 7.5 | 4.0 | 10.0 | 9.0 | 10.0 | **7.1** | 3.5 |
| advanced | [BCG_incomplete_mkts](lecture-python-advanced.myst/BCG_incomplete_mkts.md) | 3.0 | 7.5 | 7.5 | 4.5 | 10.0 | 10.0 | — | **7.1** | 3.0 |
| advanced | [amss3](lecture-python-advanced.myst/amss3.md) | 3.5 | 5.5 | 7.5 | 5.5 | 7.5 | 10.0 | 10.0 | **7.1** | 3.5 |
| advanced | [calvo](lecture-python-advanced.myst/calvo.md) | 3.0 | 5.5 | 7.5 | 7.0 | 8.5 | 8.0 | 10.0 | **7.1** | 3.0 |
| advanced | [smoothing_tax](lecture-python-advanced.myst/smoothing_tax.md) | 4.0 | 5.5 | 7.5 | 4.0 | 10.0 | 9.0 | 10.0 | **7.1** | 4.0 |
| programming | [about_py](lecture-python-programming/about_py.md) | 3.0 | — | 10.0 | 7.5 | — | 8.0 | — | **7.1** | 3.0 |
| python.myst | [finite_markov](lecture-python.myst/finite_markov.md) | 3.0 | 3.5 | 8.0 | 6.5 | 10.0 | 9.0 | 10.0 | **7.1** | 3.0 |
| python.myst | [lln_clt](lecture-python.myst/lln_clt.md) | 3.5 | 3.0 | 6.5 | 7.0 | 10.0 | 10.0 | 10.0 | **7.1** | 3.0 |
| dp | [amss3](lecture-dp/amss3.md) | 3.5 | 5.5 | 8.5 | 5.5 | 7.5 | 10.0 | 10.0 | **7.2** | 3.5 |
| dp | [calvo](lecture-dp/calvo.md) | 3.0 | 5.5 | 8.5 | 7.0 | 8.5 | 8.0 | 10.0 | **7.2** | 3.0 |
| dp | [inventory_q](lecture-dp/inventory_q.md) | 4.0 | 5.5 | 7.5 | 6.0 | 10.0 | 10.0 | — | **7.2** | 4.0 |
| dp | [mccall_model](lecture-dp/mccall_model.md) | 3.0 | 7.0 | 6.5 | 6.0 | 10.0 | 8.0 | 10.0 | **7.2** | 3.0 |
| advanced | [calvo_machine_learn](lecture-python-advanced.myst/calvo_machine_learn.md) | 3.5 | 3.0 | 6.0 | 8.0 | 10.0 | 10.0 | 10.0 | **7.2** | 3.0 |
| advanced | [lucas_asset_pricing_dles](lecture-python-advanced.myst/lucas_asset_pricing_dles.md) | 5.5 | 4.0 | 8.5 | 7.0 | 8.5 | 10.0 | — | **7.2** | 4.0 |
| advanced | [permanent_income_dles](lecture-python-advanced.myst/permanent_income_dles.md) | 4.0 | 7.5 | 7.5 | 8.0 | 8.5 | 8.0 | — | **7.2** | 4.0 |
| advanced | [risk_aversion_or_mistaken_beliefs](lecture-python-advanced.myst/risk_aversion_or_mistaken_beliefs.md) | 5.0 | 3.0 | 9.0 | 3.5 | 10.0 | 10.0 | 10.0 | **7.2** | 3.0 |
| intro | [geom_series](lecture-python-intro/geom_series.md) | 3.0 | 8.5 | 7.5 | 4.0 | — | 10.0 | 10.0 | **7.2** | 3.0 |
| intro | [networks](lecture-python-intro/networks.md) | 4.0 | 6.0 | 7.0 | 5.0 | 8.5 | 10.0 | 10.0 | **7.2** | 4.0 |
| programming | [python_by_example](lecture-python-programming/python_by_example.md) | 3.0 | 9.0 | 7.5 | 6.5 | — | 10.0 | 7.5 | **7.2** | 3.0 |
| python.myst | [lq_inventories](lecture-python.myst/lq_inventories.md) | 3.0 | 3.0 | 7.5 | 7.0 | 10.0 | 10.0 | 10.0 | **7.2** | 3.0 |
| python.myst | [mccall_model](lecture-python.myst/mccall_model.md) | 3.0 | 7.5 | 6.0 | 6.0 | 10.0 | 8.0 | 10.0 | **7.2** | 3.0 |
| python.myst | [mle](lecture-python.myst/mle.md) | 4.5 | 3.0 | 7.5 | 5.5 | 10.0 | 10.0 | 10.0 | **7.2** | 3.0 |
| python.myst | [sargent_surico](lecture-python.myst/sargent_surico.md) | 6.5 | 5.5 | 4.5 | 4.0 | 10.0 | 10.0 | 10.0 | **7.2** | 4.0 |
| dp | [amss](lecture-dp/amss.md) | 3.5 | 3.5 | 8.0 | 6.0 | 10.0 | 10.0 | 10.0 | **7.3** | 3.5 |
| dp | [opt_tax_recur](lecture-dp/opt_tax_recur.md) | 4.0 | 5.0 | 8.5 | 4.5 | 9.0 | 10.0 | 10.0 | **7.3** | 4.0 |
| advanced | [amss](lecture-python-advanced.myst/amss.md) | 4.0 | 4.0 | 7.0 | 6.0 | 10.0 | 10.0 | 10.0 | **7.3** | 4.0 |
| advanced | [gorman_heterogeneous_households](lecture-python-advanced.myst/gorman_heterogeneous_households.md) | 3.0 | 8.0 | 5.0 | 5.0 | 10.0 | 10.0 | 10.0 | **7.3** | 3.0 |
| advanced | [growth_in_dles](lecture-python-advanced.myst/growth_in_dles.md) | 3.0 | 7.5 | 7.5 | 7.0 | 9.0 | 10.0 | — | **7.3** | 3.0 |
| intro | [french_rev](lecture-python-intro/french_rev.md) | 3.0 | 10.0 | 7.5 | 3.0 | 7.5 | 10.0 | 10.0 | **7.3** | 3.0 |
| programming | [pandas](lecture-python-programming/pandas.md) | 3.0 | — | 7.0 | 6.5 | — | 10.0 | 10.0 | **7.3** | 3.0 |
| programming | [pandas_panel](lecture-python-programming/pandas_panel.md) | 3.5 | — | 8.5 | 4.5 | — | 10.0 | 10.0 | **7.3** | 3.5 |
| python.myst | [ge_arrow](lecture-python.myst/ge_arrow.md) | 3.0 | 3.0 | 7.5 | 7.5 | 10.0 | 10.0 | 10.0 | **7.3** | 3.0 |
| python.myst | [opt_transport](lecture-python.myst/opt_transport.md) | 3.0 | 3.0 | 7.0 | 8.0 | 10.0 | 10.0 | 10.0 | **7.3** | 3.0 |
| python.myst | [util_rand_resp](lecture-python.myst/util_rand_resp.md) | 4.0 | 4.0 | 7.5 | 9.5 | 9.0 | 10.0 | — | **7.3** | 4.0 |
| python.myst | [von_neumann_model](lecture-python.myst/von_neumann_model.md) | 3.0 | 5.0 | 7.5 | 7.0 | 8.5 | 10.0 | 10.0 | **7.3** | 3.0 |
| dp | [calvo_machine_learn](lecture-dp/calvo_machine_learn.md) | 4.0 | 3.0 | 6.5 | 8.0 | 10.0 | 10.0 | 10.0 | **7.4** | 3.0 |
| dp | [lq_inventories](lecture-dp/lq_inventories.md) | 4.0 | 3.0 | 7.5 | 7.0 | 10.0 | 10.0 | 10.0 | **7.4** | 3.0 |
| dp | [odu](lecture-dp/odu.md) | 3.0 | 9.0 | 7.5 | 5.0 | 9.0 | 8.0 | 10.0 | **7.4** | 3.0 |
| advanced | [BCG_complete_mkts](lecture-python-advanced.myst/BCG_complete_mkts.md) | 3.0 | 7.5 | 7.0 | 6.0 | 10.0 | 8.0 | 10.0 | **7.4** | 3.0 |
| advanced | [classical_filtering](lecture-python-advanced.myst/classical_filtering.md) | 4.5 | 3.5 | 10.0 | — | 8.5 | 8.0 | 10.0 | **7.4** | 3.5 |
| advanced | [doubts_or_variability](lecture-python-advanced.myst/doubts_or_variability.md) | 4.0 | 3.0 | 7.0 | 9.0 | 9.0 | 10.0 | 10.0 | **7.4** | 3.0 |
| advanced | [orth_proj](lecture-python-advanced.myst/orth_proj.md) | 4.0 | 3.0 | 10.0 | 7.0 | 10.0 | 8.0 | 10.0 | **7.4** | 3.0 |
| intro | [eigen_I](lecture-python-intro/eigen_I.md) | 3.5 | 10.0 | 7.5 | 3.5 | — | 10.0 | 10.0 | **7.4** | 3.5 |
| intro | [inflation_history](lecture-python-intro/inflation_history.md) | 3.0 | 10.0 | 6.0 | 4.5 | 8.5 | 10.0 | 10.0 | **7.4** | 3.0 |
| intro | [markov_chains_I](lecture-python-intro/markov_chains_I.md) | 6.0 | 3.0 | 7.0 | 7.5 | 9.0 | 9.0 | 10.0 | **7.4** | 3.0 |
| intro | [time_series_with_matrices](lecture-python-intro/time_series_with_matrices.md) | 3.0 | 6.0 | 7.5 | 7.0 | 10.0 | 8.0 | 10.0 | **7.4** | 3.0 |
| python.myst | [affine_risk_prices](lecture-python.myst/affine_risk_prices.md) | 4.5 | 4.0 | 8.5 | 5.5 | 9.0 | 10.0 | 10.0 | **7.4** | 4.0 |
| python.myst | [blackwell_kihlstrom](lecture-python.myst/blackwell_kihlstrom.md) | 3.5 | 3.0 | 8.5 | 7.5 | 9.0 | 10.0 | 10.0 | **7.4** | 3.0 |
| python.myst | [imp_sample](lecture-python.myst/imp_sample.md) | 4.5 | 4.0 | 10.0 | 8.5 | — | 10.0 | — | **7.4** | 4.0 |
| python.myst | [likelihood_ratio_process_2](lecture-python.myst/likelihood_ratio_process_2.md) | 3.0 | 9.5 | 7.5 | 4.0 | 7.5 | 10.0 | 10.0 | **7.4** | 3.0 |
| python.myst | [markov_perf](lecture-python.myst/markov_perf.md) | 4.0 | 5.0 | 7.0 | 6.0 | 10.0 | 10.0 | 10.0 | **7.4** | 4.0 |
| python.myst | [odu](lecture-python.myst/odu.md) | 3.0 | 9.0 | 7.5 | 5.0 | 9.0 | 8.5 | 10.0 | **7.4** | 3.0 |
| python.myst | [ross_recovery](lecture-python.myst/ross_recovery.md) | 3.5 | 5.5 | 6.5 | 6.0 | 10.0 | 10.0 | 10.0 | **7.4** | 3.5 |
| python.myst | [uncertainty_traps](lecture-python.myst/uncertainty_traps.md) | 3.0 | 5.5 | 7.5 | 6.5 | 9.0 | 10.0 | 10.0 | **7.4** | 3.0 |
| advanced | [chang_ramsey](lecture-python-advanced.myst/chang_ramsey.md) | 3.0 | 9.0 | 8.5 | 6.0 | 8.5 | 10.0 | — | **7.5** | 3.0 |
| advanced | [hansen_richard_1987](lecture-python-advanced.myst/hansen_richard_1987.md) | 4.0 | 4.0 | 5.0 | 9.5 | 10.0 | 10.0 | 10.0 | **7.5** | 4.0 |
| advanced | [irfs_in_hall_model](lecture-python-advanced.myst/irfs_in_hall_model.md) | 3.0 | 8.5 | 7.5 | 7.0 | 9.0 | 10.0 | — | **7.5** | 3.0 |
| advanced | [lqramsey](lecture-python-advanced.myst/lqramsey.md) | 4.0 | 3.0 | 7.5 | 8.0 | 10.0 | 10.0 | 10.0 | **7.5** | 3.0 |
| programming | [jax_intro](lecture-python-programming/jax_intro.md) | 3.0 | — | 7.5 | 7.0 | — | 10.0 | 10.0 | **7.5** | 3.0 |
| programming | [numpy](lecture-python-programming/numpy.md) | 3.0 | 8.0 | 7.0 | 7.0 | — | 10.0 | 10.0 | **7.5** | 3.0 |
| python.myst | [inventory_q](lecture-python.myst/inventory_q.md) | 3.0 | 6.0 | 10.0 | 6.0 | 10.0 | 10.0 | — | **7.5** | 3.0 |
| python.myst | [measurement_models](lecture-python.myst/measurement_models.md) | 3.0 | 4.0 | 6.0 | 9.5 | 10.0 | 10.0 | 10.0 | **7.5** | 3.0 |
| python.myst | [wald_friedman](lecture-python.myst/wald_friedman.md) | 3.0 | 8.5 | 7.5 | 4.5 | 10.0 | 9.0 | 10.0 | **7.5** | 3.0 |
| dp | [mccall_q](lecture-dp/mccall_q.md) | 3.0 | 9.5 | 7.0 | 7.0 | 9.0 | 10.0 | — | **7.6** | 3.0 |
| programming | [matplotlib](lecture-python-programming/matplotlib.md) | 4.0 | 10.0 | 7.0 | 4.5 | — | 10.0 | 10.0 | **7.6** | 4.0 |
| programming | [numba](lecture-python-programming/numba.md) | 3.0 | 7.5 | 8.5 | 7.5 | — | 9.0 | 10.0 | **7.6** | 3.0 |
| python.myst | [ak_aiyagari](lecture-python.myst/ak_aiyagari.md) | 5.0 | 10.0 | 8.0 | 4.0 | 8.5 | 10.0 | — | **7.6** | 4.0 |
| python.myst | [cass_fiscal](lecture-python.myst/cass_fiscal.md) | 3.0 | 9.0 | 7.5 | 4.0 | 10.0 | 10.0 | 10.0 | **7.6** | 3.0 |
| python.myst | [hansen_singleton_1983](lecture-python.myst/hansen_singleton_1983.md) | 6.0 | 3.0 | 7.0 | 9.5 | 10.0 | 10.0 | — | **7.6** | 3.0 |
| python.myst | [olg_adaptive_money](lecture-python.myst/olg_adaptive_money.md) | 3.5 | 7.5 | 6.5 | 6.0 | 10.0 | 10.0 | 10.0 | **7.6** | 3.5 |
| python.myst | [os_stochastic](lecture-python.myst/os_stochastic.md) | 3.0 | 7.0 | 7.5 | 7.5 | 10.0 | 8.0 | 10.0 | **7.6** | 3.0 |
| dp | [chang_ramsey](lecture-dp/chang_ramsey.md) | 3.0 | 10.0 | 8.5 | 6.0 | 8.5 | 10.0 | — | **7.7** | 3.0 |
| dp | [os_stochastic](lecture-dp/os_stochastic.md) | 3.0 | 7.5 | 8.0 | 7.5 | 10.0 | 8.0 | 10.0 | **7.7** | 3.0 |
| intro | [greek_square](lecture-python-intro/greek_square.md) | 4.0 | 7.5 | 7.0 | 6.5 | 9.0 | 10.0 | 10.0 | **7.7** | 4.0 |
| programming | [names](lecture-python-programming/names.md) | 3.0 | — | 8.5 | 7.0 | — | 10.0 | 10.0 | **7.7** | 3.0 |
| python.myst | [ar1_turningpts](lecture-python.myst/ar1_turningpts.md) | 3.0 | 7.5 | 8.5 | 8.0 | 9.0 | 10.0 | — | **7.7** | 3.0 |
| python.myst | [cass_koopmans_2](lecture-python.myst/cass_koopmans_2.md) | 3.0 | 9.5 | 8.5 | 6.0 | 10.0 | 7.0 | 10.0 | **7.7** | 3.0 |
| python.myst | [long_run_risk_operator](lecture-python.myst/long_run_risk_operator.md) | 3.0 | 7.0 | 7.5 | 6.5 | 10.0 | 10.0 | 10.0 | **7.7** | 3.0 |
| python.myst | [phillips_two_stories](lecture-python.myst/phillips_two_stories.md) | 3.0 | 10.0 | 8.5 | 5.0 | 7.5 | 10.0 | 10.0 | **7.7** | 3.0 |
| advanced | [calvo_abreu](lecture-python-advanced.myst/calvo_abreu.md) | 4.0 | 8.5 | 6.5 | 9.0 | 8.5 | 10.0 | — | **7.8** | 4.0 |
| advanced | [lu_tricks](lecture-python-advanced.myst/lu_tricks.md) | 3.0 | 6.5 | 8.5 | 8.5 | 10.0 | 8.0 | 10.0 | **7.8** | 3.0 |
| intro | [inequality](lecture-python-intro/inequality.md) | 4.0 | 9.0 | 6.5 | 5.0 | 10.0 | 10.0 | 10.0 | **7.8** | 4.0 |
| intro | [solow](lecture-python-intro/solow.md) | 4.0 | 8.0 | 7.0 | 8.0 | — | 10.0 | 10.0 | **7.8** | 4.0 |
| intro | [tax_smooth](lecture-python-intro/tax_smooth.md) | 3.0 | 9.5 | 6.0 | 6.0 | 10.0 | 10.0 | 10.0 | **7.8** | 3.0 |
| programming | [scipy](lecture-python-programming/scipy.md) | 3.0 | 7.5 | 8.5 | 8.0 | — | 10.0 | 10.0 | **7.8** | 3.0 |
| programming | [writing_good_code](lecture-python-programming/writing_good_code.md) | 3.0 | 9.5 | 7.0 | 7.5 | — | 10.0 | 10.0 | **7.8** | 3.0 |
| python.myst | [back_prop](lecture-python.myst/back_prop.md) | 3.0 | 7.5 | 7.5 | 9.0 | — | 10.0 | 10.0 | **7.8** | 3.0 |
| python.myst | [likelihood_bayes](lecture-python.myst/likelihood_bayes.md) | 5.5 | 4.0 | 7.5 | 7.5 | 10.0 | 10.0 | 10.0 | **7.8** | 4.0 |
| python.myst | [mccall_q](lecture-python.myst/mccall_q.md) | 4.0 | 9.5 | 7.0 | 7.0 | 9.0 | 10.0 | — | **7.8** | 4.0 |
| python.myst | [newton_method](lecture-python.myst/newton_method.md) | 4.0 | 9.5 | 7.0 | 6.0 | — | 10.0 | 10.0 | **7.8** | 4.0 |
| python.myst | [re_with_feedback](lecture-python.myst/re_with_feedback.md) | 3.0 | 8.5 | 7.0 | 6.0 | 10.0 | 10.0 | 10.0 | **7.8** | 3.0 |
| python.myst | [svd_intro](lecture-python.myst/svd_intro.md) | 3.0 | 9.5 | 7.5 | 6.5 | — | 10.0 | 10.0 | **7.8** | 3.0 |
| python.myst | [var_dmd](lecture-python.myst/var_dmd.md) | 3.0 | 9.5 | — | — | 7.5 | 9.0 | 10.0 | **7.8** | 3.0 |
| dp | [ifp_egm_transient_shocks](lecture-dp/ifp_egm_transient_shocks.md) | 3.5 | 9.5 | 7.5 | 5.5 | 9.0 | 10.0 | 10.0 | **7.9** | 3.5 |
| dp | [lqramsey](lecture-dp/lqramsey.md) | 6.5 | 3.0 | 7.5 | 8.0 | 10.0 | 10.0 | 10.0 | **7.9** | 3.0 |
| advanced | [repeat_mh](lecture-python-advanced.myst/repeat_mh.md) | 4.0 | 6.0 | 7.0 | 8.5 | 10.0 | 10.0 | 10.0 | **7.9** | 4.0 |
| intro | [complex_and_trig](lecture-python-intro/complex_and_trig.md) | 3.0 | 9.5 | 7.0 | 5.5 | 10.0 | 10.0 | 10.0 | **7.9** | 3.0 |
| intro | [laffer_adaptive](lecture-python-intro/laffer_adaptive.md) | 4.0 | 10.0 | 7.0 | 6.0 | 8.5 | 10.0 | 10.0 | **7.9** | 4.0 |
| intro | [money_inflation_nonlinear](lecture-python-intro/money_inflation_nonlinear.md) | 3.0 | 9.5 | 6.5 | 6.5 | 10.0 | 10.0 | 10.0 | **7.9** | 3.0 |
| intro | [unpleasant](lecture-python-intro/unpleasant.md) | 3.5 | 8.0 | 7.5 | 6.0 | 10.0 | 10.0 | 10.0 | **7.9** | 3.5 |
| python.myst | [eig_circulant](lecture-python.myst/eig_circulant.md) | 3.0 | 7.5 | 10.0 | 7.0 | — | 10.0 | 10.0 | **7.9** | 3.0 |
| python.myst | [exchangeable](lecture-python.myst/exchangeable.md) | 3.5 | 7.0 | 7.5 | 7.5 | 10.0 | 10.0 | 10.0 | **7.9** | 3.5 |
| python.myst | [information_market_equilibrium](lecture-python.myst/information_market_equilibrium.md) | 4.0 | 5.5 | 8.5 | 7.5 | 10.0 | 10.0 | 10.0 | **7.9** | 4.0 |
| python.myst | [phillips_drifts_volatilities](lecture-python.myst/phillips_drifts_volatilities.md) | 3.5 | 9.5 | 8.0 | 4.5 | 10.0 | 10.0 | 10.0 | **7.9** | 3.5 |
| python.myst | [rational_expectations](lecture-python.myst/rational_expectations.md) | 3.5 | 5.0 | 7.5 | 10.0 | 9.0 | 10.0 | 10.0 | **7.9** | 3.5 |
| python.myst | [robust_permanent_income](lecture-python.myst/robust_permanent_income.md) | 3.5 | 9.0 | 6.5 | 6.0 | 10.0 | 10.0 | 10.0 | **7.9** | 3.5 |
| dp | [calvo_abreu](lecture-dp/calvo_abreu.md) | 4.0 | 9.0 | 7.5 | 9.0 | 8.5 | 10.0 | — | **8.0** | 4.0 |
| dp | [ifp_egm](lecture-dp/ifp_egm.md) | 3.0 | 9.0 | 7.5 | 6.5 | 10.0 | 10.0 | 10.0 | **8.0** | 3.0 |
| dp | [jv](lecture-dp/jv.md) | 3.5 | 9.5 | 7.5 | 6.5 | 9.0 | 10.0 | 10.0 | **8.0** | 3.5 |
| intro | [lp_intro](lecture-python-intro/lp_intro.md) | 3.5 | 6.5 | 7.5 | 8.5 | 10.0 | 10.0 | 10.0 | **8.0** | 3.5 |
| intro | [msy_fishery](lecture-python-intro/msy_fishery.md) | 3.5 | 10.0 | 6.0 | 6.5 | 10.0 | 10.0 | 10.0 | **8.0** | 3.5 |
| programming | [getting_started](lecture-python-programming/getting_started.md) | 3.0 | — | 10.0 | 7.0 | — | 10.0 | 10.0 | **8.0** | 3.0 |
| python.myst | [aiyagari_egm](lecture-python.myst/aiyagari_egm.md) | 3.0 | 8.5 | 10.0 | 5.5 | 9.0 | 10.0 | 10.0 | **8.0** | 3.0 |
| python.myst | [cass_koopmans_1](lecture-python.myst/cass_koopmans_1.md) | 3.0 | 9.5 | 8.5 | 6.0 | 10.0 | 9.0 | 10.0 | **8.0** | 3.0 |
| python.myst | [ifp_egm_transient_shocks](lecture-python.myst/ifp_egm_transient_shocks.md) | 4.0 | 10.0 | 7.5 | 5.5 | 9.0 | 10.0 | 10.0 | **8.0** | 4.0 |
| python.myst | [jv](lecture-python.myst/jv.md) | 3.0 | 10.0 | 7.5 | 6.5 | 9.0 | 10.0 | 10.0 | **8.0** | 3.0 |
| python.myst | [marimon_mcgrattan_sargent](lecture-python.myst/marimon_mcgrattan_sargent.md) | 4.0 | 9.5 | 6.5 | 7.5 | 8.5 | 10.0 | 10.0 | **8.0** | 4.0 |
| programming | [python_oop](lecture-python-programming/python_oop.md) | 3.0 | 10.0 | 7.5 | 8.0 | — | 10.0 | 10.0 | **8.1** | 3.0 |
| programming | [sympy](lecture-python-programming/sympy.md) | 4.0 | 8.0 | 8.5 | 10.0 | — | 8.0 | 10.0 | **8.1** | 4.0 |
| python.myst | [ak2](lecture-python.myst/ak2.md) | 3.5 | 10.0 | 8.5 | 5.0 | 10.0 | 10.0 | 10.0 | **8.1** | 3.5 |
| python.myst | [cass_fiscal_2](lecture-python.myst/cass_fiscal_2.md) | 4.0 | 10.0 | 7.5 | 5.5 | 10.0 | 10.0 | 10.0 | **8.1** | 4.0 |
| python.myst | [ifp_egm](lecture-python.myst/ifp_egm.md) | 3.0 | 9.5 | 7.5 | 6.5 | 10.0 | 10.0 | 10.0 | **8.1** | 3.0 |
| python.myst | [rand_resp](lecture-python.myst/rand_resp.md) | 3.5 | 9.5 | 7.5 | — | 10.0 | 10.0 | — | **8.1** | 3.5 |
| python.myst | [wealth_dynamics](lecture-python.myst/wealth_dynamics.md) | 3.0 | 9.5 | 8.0 | 6.5 | 10.0 | 10.0 | 10.0 | **8.1** | 3.0 |
| programming | [functions](lecture-python-programming/functions.md) | 3.0 | 10.0 | 8.5 | 7.5 | — | 10.0 | 10.0 | **8.2** | 3.0 |
| programming | [oop_intro](lecture-python-programming/oop_intro.md) | 4.0 | — | 9.0 | — | — | 10.0 | 10.0 | **8.2** | 4.0 |
| programming | [need_for_speed](lecture-python-programming/need_for_speed.md) | 3.0 | — | 10.0 | 8.5 | — | 10.0 | 10.0 | **8.3** | 3.0 |
| programming | [numpy_vs_numba_vs_jax](lecture-python-programming/numpy_vs_numba_vs_jax.md) | 3.0 | 10.0 | 8.5 | 8.5 | — | 10.0 | 10.0 | **8.3** | 3.0 |
| programming | [python_essentials](lecture-python-programming/python_essentials.md) | 3.0 | 10.0 | 8.5 | — | — | 10.0 | 10.0 | **8.3** | 3.0 |
| python.myst | [house_auction](lecture-python.myst/house_auction.md) | 3.0 | 10.0 | 7.0 | — | 10.0 | 10.0 | 10.0 | **8.3** | 3.0 |
| intro | [observed_distributions](lecture-python-intro/observed_distributions.md) | 4.0 | 10.0 | 7.5 | 7.0 | 10.0 | 10.0 | 10.0 | **8.4** | 4.0 |
| dp | [chang_credible](lecture-dp/chang_credible.md) | 3.0 | 10.0 | 8.5 | 9.5 | 10.0 | 10.0 | — | **8.5** | 3.0 |
| advanced | [chang_credible](lecture-python-advanced.myst/chang_credible.md) | 3.0 | 10.0 | 8.5 | 9.5 | 10.0 | 10.0 | — | **8.5** | 3.0 |
| intro | [cagan_ree](lecture-python-intro/cagan_ree.md) | 4.0 | 10.0 | 8.5 | 7.0 | 10.0 | 10.0 | 10.0 | **8.5** | 4.0 |
| python.myst | [morris_learn](lecture-python.myst/morris_learn.md) | 3.0 | 9.5 | 8.5 | 10.0 | 8.5 | 10.0 | 10.0 | **8.5** | 3.0 |
| python.myst | [os_egm](lecture-python.myst/os_egm.md) | 4.0 | 9.5 | 7.0 | 9.0 | 10.0 | 10.0 | 10.0 | **8.5** | 4.0 |
| programming | [debugging](lecture-python-programming/debugging.md) | 3.5 | 10.0 | 10.0 | 9.0 | — | 10.0 | 10.0 | **8.8** | 3.5 |
<!-- /qe:high-list -->

---

## Remediation plan

Ordered by return on effort. The first block is mechanical and can be scripted; the second
needs a reading pass; the third is small and structural.

### 1. Scriptable sweeps — do these first

1. **Figure names** (`qe-fig-005`) — add `mystnb.figure.name` metadata to every
   figure-producing code cell and `:name:` to every `{figure}`/`{image}` directive. Reaches
   the largest share of the corpus of any single rule and unlocks `{numref}`
   cross-referencing.
2. **Greek letters in code** (`qe-code-002`) — `alpha` → `α` and friends, in code cells
   only. `lecture-python-programming` is already fully compliant and is the model.
3. **Line widths** (`qe-fig-008`) — add `lw=2` to line plots.
4. **Figure sizes** (`qe-fig-001`) — drop `figsize=` overrides and let the series
   `_config.yml` defaults apply; keep only where a plot genuinely needs a different aspect.
5. **Excess whitespace** (`qe-writing-008`) — collapse runs of spaces between words. The
   single largest raw count in the corpus, and entirely safe to automate.
6. **Heading capitalisation** (`qe-writing-006`) — H2 and below to sentence case. Needs a
   proper-noun allowlist; `tools/qestyle_rules.py` already carries one curated from this
   corpus.
7. **Transpose and expectation notation** (`qe-math-002`, `qe-math-010` *(proposed)*) —
   `'` and `^T` → `^\top`; bare `E[·]` → `\mathbb{E}[·]`. Concentrated in the older LQ and
   filtering lectures of `lecture-python-advanced.myst` and `lecture-dp`, so it is best
   done as one careful pass over that cluster rather than corpus-wide.
8. **Cross-series links** (`qe-link-002`) — raw `*.quantecon.org` URLs → `{doc}` with the
   intersphinx prefix.

### 2. Needs a reading pass

9. **Plot titles → captions** (`qe-fig-003`) — `ax.set_title(...)` moved into the figure
   caption. Mechanical to find, but each caption has to be written. Titles inside
   `exercise`/`solution` regions are exempt and are already excluded from the counts.
10. **Caption conventions** (`qe-fig-004`) — sentence case, six words or fewer. The only
    rule that got materially worse since the previous pass.
11. **Narrative citations** (`qe-ref-001`) — `{cite}` → `{cite:t}` where the author name is
    part of the sentence. Needs judgment on each site.
12. **One sentence per paragraph** (`qe-writing-001`) — splitting a paragraph changes its
    rhythm, so this is an editorial pass, not a sweep.

### 3. Structural — small and worth doing now

13. The four findings on the [front page](intro.md#fix-immediately): two unclosed
    `{exercise-start}` fences, two malformed `` {eq}` ` `` references, and a raw
    `\label{}` inside `$$`.
14. **Shared lectures between `lecture-dp` and `lecture-python.myst`.** 31 filenames
    appear in both series, but only **6 are byte-identical** at this snapshot:
    `cross_product_trick`, `ifp_discrete`, `ifp_opi`, `lq_inventories`,
    `mccall_model_with_separation`, `os_numerical`. Those 6 account for 217 of the corpus's
    18,587 findings — **1.2 % genuinely counted twice**, which is the honest size of the
    double-count. The other 25 share an origin and have diverged, so their findings are
    about different files even where the defect is the same. For the identical 6, fix
    upstream and both clear; for the diverged 25, each copy needs its own fix. Worth a
    decision on whether the corpus totals should de-duplicate the 6 —
    [#3](https://github.com/QuantEcon/compliance-lecture-style/issues/3).

---

## Corrections to the previous pass

This pass re-measured the corpus with a program rather than by reading, which surfaced
several defects in the previous report. They are listed here rather than quietly dropped,
because they say something about how a pass should be run.

| What the previous pass said | What re-measurement found |
|-----------------------------|---------------------------|
| `divergence_measures.md:134` has `\begin{align}` inside `$$`, breaking the PDF build | There is no `align` inside `$$` anywhere in the corpus. That line is a bare top-level `\begin{align}`, which MyST handles — a convention outlier, not a build break. |
| 299 lectures audited | 299 reports were written, but one of them (`supply_demand_foundations_v2`) describes a lecture that exists in no repository's history, and two real `lecture-dp` lectures (`inventory_q`, `rs_inventory_q`) were never audited. Net real coverage was 298 of 300. |
| Per-lecture overall scores | 94 of 299 headers did not equal the mean of their own in-scope categories, which is how spec §4 defines the overall score. Discrepancies ran up to 1.2 points. |
| Per-lecture priority buckets | 35 of 299 did not follow spec §4 from their own scores — mostly lectures with a category at 4 that were filed MEDIUM rather than HIGH. |
| `lecture-python.myst` is "in great shape — 86% of lectures are clean" | The same series was reported as having `qe-writing-006` in 87 of 110 lectures and `qe-code-002` in 94 of 110. Both cannot hold under the §4 rubric. Measured consistently, `lecture-python.myst` sits mid-field, not top. |
| `qe-admon-*` clean across `lecture-python-programming` | `python_by_example.md` has two unclosed `{exercise-start}` fences (`qe-admon-003`, a build-risk rule). |

None of these are surprising for a pass done by reading 299 files. They are the reason the
mechanical layer now exists, and the reason `tools/qestyle_check.py` runs as a gate: every
row above corresponds to a check that now fails loudly.

---

## Coverage and its limits

- **41 of 49 rules are measured by program** (36 of the 42 in-scope registry rules plus 5
  of the 7 proposed); the 8 judgment-only rules (spec §9) are
  reviewed by reading. A category scoring 10 means no mechanical violation was measured,
  not that every rule in it was verified by a human.
- **Review coverage is complete in this pass and was absent in the previous one, and scores
  depend on it.** A lecture assessed against more rules scores lower. Every 2026-08 lecture
  folds in a judgment overlay, so the scoreboard above is comparable *across series*; the
  2026-05 rows of `history.csv` fold in none (its `reviewed` column), so score levels are
  not comparable *across the two periods*, and the [front page](intro.md) says so with the
  like-for-like figures from `history_mechanical.csv` — the evidence layer alone, on which
  the corpus improved. The rule-reach tables are unaffected, because those are measured over
  every lecture by the same code.
- **Three checks are heuristic** and say so where they fire: `qe-writing-004` and
  `qe-writing-006` depend on curated proper-noun and common-noun lists, and `qe-math-002`
  has to distinguish a transpose apostrophe from a derivative and a `^T` transpose from a
  terminal date. They will need extending as the corpus grows.
- **JAX is out of scope**, not `N/A` — the 7 `qe-jax-*` rules target `lecture-jax`, which
  is not part of this corpus.
- **Counts are absolute, not per-line.** A 2,000-line lecture and a 200-line lecture with
  the same number of violations of a rule score the same for it, which follows the spec's
  severity definitions (§5) rather than any notion of density.
