# Summary

Style audit of the **lecture-python-programming** series.

<!-- qe:series-meta -->
- **Audit date:** 2026-08-21
- **Corpus snapshot:** `ceec881028`
- **Lectures audited:** 27
- **Average overall score:** 8.0 / 10
- **Average per-category scores:** writing 4.1, math 9.0, code 8.4, figures 7.3, links 9.8, admon 9.9  *(references not in scope for this series)*
- **JAX:** out of scope — the `qe-jax-*` rules target `lecture-jax`.
- **Judgment-review coverage:** all lectures reviewed.
<!-- /qe:series-meta -->

<!-- qe:series-narrative -->
Writing is the whole story here. At **4.1** it is the lowest cell in the entire
series-by-category grid — below the corpus's 4.6, below `lecture-python.myst`'s 4.5 — and
it is the only category at the floor anywhere in the series. All **20 HIGH lectures are
HIGH because Writing fell to or below 4**, and not one of them for any other reason: no
Math floor, no Figures floor, no lecture with two categories at the floor. Every other
series mixes them — `lecture-python.myst` has 26 Math floors and 24 double-floored
lectures, `lecture-dp` 14 and 12.

One rule carries most of that load: `qe-writing-006` — Title Case in H2+ headings —
(23 / 27, 178 headings). That is 85 % of the series against 49 % in `lecture-python.myst`
and 4 % in `lecture-python-advanced.myst`, and those 178 headings are 23 % of every
`qe-writing-006` occurrence in the corpus from under 8 % of its lectures. The weight sits
in the tutorial lectures — `getting_started` (17), `python_essentials` (14), `functions`
(13), `numpy` (12) — and every one of the 20 HIGH lectures carries it. Behind it are three
cheaper mechanical rules, `qe-writing-008` (16 / 27, 43 occurrences), `qe-writing-001`
(15 / 27, 29) and `qe-writing-004` (6 / 27, 14), plus a judgment backlog led by
`qe-writing-005`, found in 23 of the 27 lectures. Since 2026-05 the published Writing
figure has gone from 5.7 to 4.1 and HIGH from 5 to 20 over one added lecture — but that is
the judgment layer, not the lectures: the 2026-05 row folds in no review overlay and this one
folds one into all 27. Both rows are re-measured with the current code
([spec](../spec.md)), so the evidence layer *is* comparable, and on that basis
(`history_mechanical.csv`) Writing here is 5.7 → 5.7 and HIGH 5 → 5 — unchanged, from an
already lower base than the corpus.

Everything else here is the corpus's best. Math **9.0**, Code **8.4** and Figures **7.3**
are each the highest of the five series; `qe-code-002` has zero violations in this series
against 66 lectures and 798 occurrences corpus-wide; no math build-risk rule fires
anywhere. Hence the pairing that defines the series: the second-highest mean overall
(**8.0**, behind `lecture-python-intro`'s 8.1) alongside the **highest HIGH share of any
series** — 20 of 27, 74 %, against 57 % across the corpus. Its one build-risk finding is
also the corpus's only one of that kind: `python_by_example` holds both `qe-admon-003`
occurrences in the corpus (1 / 27, 2 occurrences), `{exercise-start}` fences at lines 499
and 549 that are never closed.
<!-- /qe:series-narrative -->

## Priority distribution

<!-- qe:series-priority -->
| Priority | Count | % |
|----------|-------|---|
| HIGH     | 20    | 74.1% |
| MEDIUM   | 0     | 0.0% |
| LOW      | 5     | 18.5% |
| NONE     | 2     | 7.4% |
<!-- /qe:series-priority -->

## Top systemic issues across the series

Ranked by how many of the series' lectures each rule reaches.

<!-- qe:series-systemic -->
1. **`qe-writing-006`** — Capitalize lecture titles properly — **23 / 27** lectures, 178 occurrences.
2. **`qe-fig-005`** — Descriptive figure names for cross-referencing — **21 / 27** lectures, 128 occurrences.
3. **`qe-writing-008`** — Remove excessive whitespace between words — **16 / 27** lectures, 43 occurrences.
4. **`qe-writing-001`** — Use one sentence per paragraph — **15 / 27** lectures, 29 occurrences.
5. **`qe-fig-008`** — Use lw=2 for line charts — **14 / 27** lectures, 63 occurrences.
6. **`qe-fig-001`** — Do not set figure size unless necessary — **9 / 27** lectures, 22 occurrences.
7. **`qe-writing-004`** — Avoid unnecessary capitalization in narrative text — **6 / 27** lectures, 14 occurrences.
8. **`qe-fig-002`** — Prefer code-generated figures — **5 / 27** lectures, 15 occurrences.
9. **`qe-fig-003`** — No matplotlib embedded titles — **5 / 27** lectures, 11 occurrences.
10. **`qe-code-003`** — Package installation at lecture top — **3 / 27** lectures, 3 occurrences.
<!-- /qe:series-systemic -->

## Clean across the series

Checked rules with no violation anywhere in the series — the conventions this series
already holds to.

<!-- qe:series-clean -->
- **`qe-admon-002`** — Use dropdown class for solutions
- **`qe-code-002`** — Use Unicode symbols for Greek letters in code
- **`qe-code-005`** — Use quantecon timeit for benchmarking
- **`qe-fig-004`** — Caption formatting conventions
- **`qe-fig-010`** — Plotly figures require latex directive
- **`qe-link-001`** — Use markdown style links for lectures in same lecture series
- **`qe-math-003`** — Use square brackets for matrix notation
- **`qe-math-004`** — Do not use bold face for matrices or vectors
- **`qe-math-005`** — Use curly brackets for sequences
- **`qe-math-006`** — Use aligned environment correctly for PDF compatibility
- **`qe-math-007`** — Use automatic equation numbering, not manual tags
- **`qe-math-008`** — Explain special notation (vectors/matrices)
- **`qe-math-011`** *(proposed)* — Distribution names in plain letters, not \mathcal / \mathbb
- **`qe-math-013`** *(proposed)* — Reference equations via `` {eq}`label` ``
- **`qe-ref-001`** — Use correct citation style
- **`qe-writing-009`** *(proposed)* — Write "IID" — not "i.i.d." or "iid"
<!-- /qe:series-clean -->

## Series-level recommendations

<!-- qe:series-recommendations -->
Ordered by HIGH lectures cleared per unit of work. The projections below re-score the
series with `tools/qestyle_draft.py`'s own model, which reproduces all 27 published
Writing scores exactly; they are projections, not measurements.

1. **`qe-writing-006` — sentence-case the H2+ headings** (23 / 27, 178 headings). A
   scriptable sweep, and the highest-leverage single action available in this series:
   clearing this rule and nothing else takes it from 20 HIGH to 3 and lifts Writing from
   4.1 to 5.7. The sweep needs the 376-entry proper-noun allowlist in
   `tools/qestyle_rules.py` so `Python`, `Jupyter`, `Anaconda`, `NumPy` and `Polars`
   survive it — that list is already curated from this corpus.
2. **Finish Writing with the other three mechanical rules** — `qe-writing-008`
   (16 / 27, 43 occurrences), `qe-writing-001` (15 / 27, 29) and `qe-writing-004`
   (6 / 27, 14). Eighty-six occurrences between them, all sweepable. On the same
   projection these clear the last three HIGH lectures — `python_essentials`,
   `python_oop`, `writing_good_code` — and empty the series' HIGH list without a single
   judgment finding being touched. Whitespace is trivial here: 43 occurrences against
   2,569 in `lecture-python.myst`.
3. **Close the two `{exercise-start}` fences in `python_by_example.md`**, lines 499 and
   549 (`qe-admon-003`, 1 / 27, 2 occurrences). Out of leverage order deliberately — it
   clears no HIGH lecture. But it is two lines, it is a build defect rather than a style
   one (each fence swallows the rest of its exercise, including a nested `{hint}` at the
   same tick count), and it is the only `qe-admon-003` violation in the corpus.
4. **Figures — worth doing, but not for this series' sake.** `qe-fig-005`
   (21 / 27, 128 occurrences), `qe-fig-008` (14 / 27, 63) and `qe-fig-001` (9 / 27, 22),
   heaviest in `workspace` (17), `matplotlib` (13) and `getting_started` (12). Clearing
   all three lifts Figures from 7.3 to 9.4 and still leaves all 20 HIGH lectures HIGH,
   because nothing here is floored by Figures. Do them inside the corpus-wide sweep —
   `qe-fig-005` reaches 273 of the 348 lectures — rather than at the top of this list.
5. **Treat the judgment backlog as editorial work, not remediation.** `qe-writing-005` is
   found in 23 of the 27 lectures, `qe-writing-003` in 23, `qe-writing-002` in 21 and
   `qe-code-001` in 19 — reading passes, roughly five agent-minutes a lecture, and they
   are recorded in `judgment.csv` rather than in the mechanical reach table. None of them
   gates a priority bucket here, since item 2 already empties the HIGH list. Schedule
   them for the prose, not for the score.

**Where the fixes belong.** Every lecture edit is a PR in
[`QuantEcon/lecture-python-programming`](https://github.com/QuantEcon/lecture-python-programming);
this ledger measures the corpus, it does not patch it. Two cross-repo notes. `pandas_panel`
shares a filename with `lecture-python.myst`'s copy — the blobs differ at this snapshot,
but the two measure identically on all seven rules they share, the `lecture-python.myst`
copy carrying one extra `qe-link-002` — so mirror any fix rather than fixing one side.
And leave the code conventions alone: `qe-code-002` is at zero here, `qe-code-005` is
clean, and `qe-code-004` is one lecture (1 / 27, 10 occurrences) — `polars`, ten
`time.perf_counter()` calls. On code, this series is where the other four should be
looking, not the reverse.
<!-- /qe:series-recommendations -->

## Lectures ranked by priority (lowest score first)

Scores are 0–10 per category; **Overall** is the mean of the in-scope categories, and
**Priority** follows [spec §4](../spec.md). A dash means the category is not applicable to
that lecture. Click a lecture for its full report.

<!-- qe:series-ranked -->
| # | Lecture | Writing | Math | Code | Figures | References | Links | Admon | Overall | Priority |
|---|---------|---|---|---|---|---|---|---|---------|----------|
| 1 | [about_py](about_py.md) | 3 | — | 10 | 7.5 | — | 8 | — | **7.1** | HIGH |
| 2 | [python_by_example](python_by_example.md) | 3 | 9 | 7.5 | 6.5 | — | 10 | 7.5 | **7.2** | HIGH |
| 3 | [pandas](pandas.md) | 3 | — | 7 | 6.5 | — | 10 | 10 | **7.3** | HIGH |
| 4 | [pandas_panel](pandas_panel.md) | 3.5 | — | 8.5 | 4.5 | — | 10 | 10 | **7.3** | HIGH |
| 5 | [jax_intro](jax_intro.md) | 3 | — | 7.5 | 7 | — | 10 | 10 | **7.5** | HIGH |
| 6 | [numpy](numpy.md) | 3 | 8 | 7 | 7 | — | 10 | 10 | **7.5** | HIGH |
| 7 | [matplotlib](matplotlib.md) | 4 | 10 | 7 | 4.5 | — | 10 | 10 | **7.6** | HIGH |
| 8 | [numba](numba.md) | 3 | 7.5 | 8.5 | 7.5 | — | 9 | 10 | **7.6** | HIGH |
| 9 | [names](names.md) | 3 | — | 8.5 | 7 | — | 10 | 10 | **7.7** | HIGH |
| 10 | [workspace](workspace.md) | 4.5 | — | 8.5 | 5.5 | — | 10 | 10 | **7.7** | LOW |
| 11 | [scipy](scipy.md) | 3 | 7.5 | 8.5 | 8 | — | 10 | 10 | **7.8** | HIGH |
| 12 | [writing_good_code](writing_good_code.md) | 3 | 9.5 | 7 | 7.5 | — | 10 | 10 | **7.8** | HIGH |
| 13 | [getting_started](getting_started.md) | 3 | — | 10 | 7 | — | 10 | 10 | **8.0** | HIGH |
| 14 | [autodiff](autodiff.md) | 7 | 7.5 | 7.5 | 6.5 | — | 10 | 10 | **8.1** | LOW |
| 15 | [polars](polars.md) | 4.5 | — | 9 | 7 | — | 10 | 10 | **8.1** | LOW |
| 16 | [python_oop](python_oop.md) | 3 | 10 | 7.5 | 8 | — | 10 | 10 | **8.1** | HIGH |
| 17 | [sympy](sympy.md) | 4 | 8 | 8.5 | 10 | — | 8 | 10 | **8.1** | HIGH |
| 18 | [functions](functions.md) | 3 | 10 | 8.5 | 7.5 | — | 10 | 10 | **8.2** | HIGH |
| 19 | [oop_intro](oop_intro.md) | 4 | — | 9 | — | — | 10 | 10 | **8.2** | HIGH |
| 20 | [troubleshooting](troubleshooting.md) | 5.5 | — | — | 9 | — | 10 | — | **8.2** | LOW |
| 21 | [need_for_speed](need_for_speed.md) | 3 | — | 10 | 8.5 | — | 10 | 10 | **8.3** | HIGH |
| 22 | [numpy_vs_numba_vs_jax](numpy_vs_numba_vs_jax.md) | 3 | 10 | 8.5 | 8.5 | — | 10 | 10 | **8.3** | HIGH |
| 23 | [python_essentials](python_essentials.md) | 3 | 10 | 8.5 | — | — | 10 | 10 | **8.3** | HIGH |
| 24 | [python_advanced_features](python_advanced_features.md) | 4.5 | — | 8.5 | 9 | — | 10 | 10 | **8.4** | LOW |
| 25 | [debugging](debugging.md) | 3.5 | 10 | 10 | 9 | — | 10 | 10 | **8.8** | HIGH |
| 26 | [status](status.md) | 10 | — | 9 | — | — | 10 | — | **9.7** | NONE |
| 27 | [intro](intro.md) | 10 | — | — | — | — | 10 | — | **10.0** | NONE |
<!-- /qe:series-ranked -->
