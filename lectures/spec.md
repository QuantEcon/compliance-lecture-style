# Scoring rubric

This file is the rubric this record is scored against, and the report template every pass writes to. It *complements* the per-rule LLM review provided by [QuantEcon/action-style-guide](https://github.com/QuantEcon/action-style-guide) by adding:

- per-lecture scoring on a 0–10 scale
- severity-bucketed prioritisation across a lecture series
- cross-series synthesis and remediation roadmaps

It is not a replacement for `action-style-guide`; it consumes the same rule definitions and produces a different output format (scored reports rather than PR-with-fixes).

Every pass is scored against the rubric as it stands, and the previous pass is re-measured with the current code rather than quoted from its old report — so a change here moves the published history as well as the current numbers, and the trend measures the lectures rather than the method. §10 has the commands.

---

## 1. Authoritative rule source

The 49 canonical rules live in [`QuantEcon/action-style-guide/style_checker/rules/`](https://github.com/QuantEcon/action-style-guide/tree/main/style_checker/rules) across 8 category files:

`writing-rules.md`, `math-rules.md`, `code-rules.md`, `jax-rules.md`, `figures-rules.md`, `references-rules.md`, `links-rules.md`, `admonitions-rules.md`.

This rubric uses **qe-\* IDs verbatim**. It does not redefine rules.

---

## 2. Rules in scope

Tables organised by category. **Audit weight** is how heavily a rule influences the score for its category — driven by visibility to readers and frequency of occurrence. **Detect-by** indicates whether the rule is mechanically detectable (a regex / AST check is possible), partially mechanical (regex with judgment), or judgment-only (LLM reading required).

### 2.1 Writing (`qe-writing-*`) — 8 rules

| Rule | Title | Type | Audit weight | Detect-by |
|------|-------|------|--------------|-----------|
| qe-writing-001 | One sentence per paragraph | rule | High | Partial (regex on blank-line-separated blocks; respect lists / code / math) |
| qe-writing-002 | Keep writing clear, concise, valuable | style | Medium | Judgment |
| qe-writing-003 | Maintain logical flow | style | Medium | Judgment |
| qe-writing-004 | Avoid unnecessary capitalisation in narrative text | rule | High | Partial (needs curated proper-noun list) |
| qe-writing-005 | Bold for definitions, italic for emphasis | rule | Medium | Judgment |
| qe-writing-006 | Capitalise lecture titles properly (Title Case for H1, sentence case for H2+) | rule | **Very high** | Partial (H1 / H2 detection + proper-noun list) |
| qe-writing-007 | Use visual elements to enhance understanding | style | Low | Judgment |
| qe-writing-008 | Remove excessive whitespace between words | rule | Low | Mechanical (regex `  +` outside code / math / tables) |

### 2.2 Math (`qe-math-*`) — 9 rules

| Rule | Title | Type | Audit weight | Detect-by |
|------|-------|------|--------------|-----------|
| qe-math-001 | UTF-8 unicode in narrative, LaTeX in math envs | rule | High | Partial (math-env tokeniser) |
| qe-math-002 | Use `\top` for transpose | rule | **Very high** | Partial (regex with derivative-prime exception) |
| qe-math-003 | Square brackets for matrices (`bmatrix`) | rule | High | Mechanical (regex on `pmatrix`/`matrix`/`vmatrix`/`Bmatrix`) |
| qe-math-004 | No bold face for matrices / vectors | rule | High | Mechanical (regex on `\mathbf{`/`\boldsymbol{`/`\bm{`) |
| qe-math-005 | Curly brackets for sequences | rule | Medium | Partial (detect `[x_t]_{t=0}^∞` pattern) |
| qe-math-006 | `aligned` not `align` inside `$$` | rule | **Very high** *(build-risk)* | Mechanical (regex `\$\$.*\\begin\{align\}`) |
| qe-math-007 | Automatic equation numbering, not `\tag` | rule | High | Mechanical (regex `\\tag\{`) |
| qe-math-008 | Explain special notation (`\mathbb{1}` etc.) | rule | Medium | Partial (presence + context check) |
| qe-math-009 | Prefer simpler notation | style | Low | Judgment |

### 2.3 Code (`qe-code-*`) — 6 rules

| Rule | Title | Type | Audit weight | Detect-by |
|------|-------|------|--------------|-----------|
| qe-code-001 | PEP8 unless closer to mathematical notation | style | Medium | Judgment (with `ruff` as backstop) |
| qe-code-002 | Unicode Greek letters in code | rule | Medium | Mechanical (regex on identifiers in code cells) |
| qe-code-003 | Package installation at lecture top | rule | High | Partial (needs Anaconda allowlist) |
| qe-code-004 | Use `quantecon.Timer` context manager | migrate | Low | Mechanical (detect `time.time()` / `tic`/`toc`) |
| qe-code-005 | Use `quantecon.timeit` for benchmarking | migrate | Low | Mechanical (detect `%timeit` / `%%timeit`) |
| qe-code-006 | Binary packages require installation notes | rule | Medium | Partial (needs binary-package allowlist) |

### 2.4 JAX (`qe-jax-*`) — 7 rules

| Rule | Title | Type | Audit weight | Detect-by |
|------|-------|------|--------------|-----------|
| qe-jax-001 | Functional programming patterns | style | Medium | Judgment |
| qe-jax-002 | NamedTuple for model parameters | rule | High | Partial (AST: detect parameter classes) |
| qe-jax-003 | `generate_path` for sequence generation | style | Low | Judgment |
| qe-jax-004 | Functional update patterns (`.at[].set()`) | migrate | High | Mechanical (regex on in-place updates) |
| qe-jax-005 | `jax.lax` for control flow | style | Medium | Judgment |
| qe-jax-006 | Explicit PRNG key management | migrate | High | Mechanical (regex on `np.random.*`) |
| qe-jax-007 | Consistent function naming for updates | style | Low | Judgment |

> **Scope note:** JAX rules only apply to lectures that import or use JAX. Use `N/A` for the JAX category in non-JAX lectures.

### 2.5 Figures (`qe-fig-*`) — 11 rules

| Rule | Title | Type | Audit weight | Detect-by |
|------|-------|------|--------------|-----------|
| qe-fig-001 | Do not set figure size unless necessary | style | Low | Mechanical (detect `figsize=`) |
| qe-fig-002 | Prefer code-generated figures | style | Low | Mechanical (detect static image refs) |
| qe-fig-003 | No matplotlib embedded titles | rule | High | Mechanical (regex `ax\.set_title|fig\.suptitle`) |
| qe-fig-004 | Caption formatting conventions | rule | Medium | Mechanical (case + length) |
| qe-fig-005 | Descriptive figure names for cross-referencing | rule | Medium | Partial (label format + descriptiveness) |
| qe-fig-006 | Lowercase axis labels | rule | Medium | Mechanical (regex on `set_xlabel`/`set_ylabel`) |
| qe-fig-007 | Keep figure box and spines | rule | Medium | Mechanical (regex on `spines[*].set_visible(False)`) |
| qe-fig-008 | Use `lw=2` for line charts | rule | Low | Mechanical (AST on `plot()` calls) |
| qe-fig-009 | Figure sizing 80–100 % of text width | rule | Low | Mechanical (figure metadata) |
| qe-fig-010 | Plotly figures require `{only} latex` directive | rule | High | Mechanical (detect plotly + check for directive) |
| qe-fig-011 | Use `image` directive when nested in other directives | rule | Medium | Partial (directive nesting) |

### 2.6 References (`qe-ref-*`) — 1 rule

| Rule | Title | Type | Audit weight | Detect-by |
|------|-------|------|--------------|-----------|
| qe-ref-001 | Correct citation style (`{cite}` vs `{cite:t}`) | rule | Medium | Judgment (author-name parsing) |

### 2.7 Links (`qe-link-*`) — 2 rules

| Rule | Title | Type | Audit weight | Detect-by |
|------|-------|------|--------------|-----------|
| qe-link-001 | Markdown links for same-series references | style | Medium | Partial (URL pattern + same-series detection) |
| qe-link-002 | `{doc}` links for cross-series references | rule | High | Mechanical (regex on known intersphinx URLs) |

### 2.8 Admonitions (`qe-admon-*`) — 5 rules

| Rule | Title | Type | Audit weight | Detect-by |
|------|-------|------|--------------|-----------|
| qe-admon-001 | Gated syntax for executable code in exercises | rule | High | Mechanical (parse directive structure) |
| qe-admon-002 | `:class: dropdown` for solutions | style | Low | Mechanical (parse solution directives) |
| qe-admon-003 | Tick-count management for nested directives | rule | **Very high** *(build-risk)* | Mechanical (parse fences) |
| qe-admon-004 | `prf:` prefix for proof directives | rule | High | Mechanical (regex on proof-family directives) |
| qe-admon-005 | Link solutions to exercises | rule | Medium | Mechanical (label cross-check) |

---

## 3. Ledger-only addendum rules (proposed for action-style-guide)

These rules are **specified in the QuantEcon manual style guide** ([`QuantEcon.manual/manual/styleguide/`](https://github.com/QuantEcon/QuantEcon.manual/tree/main/manual/styleguide)) but are **not yet encoded as rules in `action-style-guide`**. They are scored each pass using the permanent IDs proposed below (each tagged **(proposed)** wherever it appears in the report) and are measured over the whole corpus — 348 lectures, one pinned commit per series (see [the synthesis](intro.md) for counts). The reach below is read from `lectures/data/rule_reach.csv` rather than estimated; the five mechanised rules carry counts, the two judgment rules cannot.

| Proposed ID | Title | Source | Audit weight | Detect-by | Lectures | Occurrences |
|-------------|-------|--------|--------------|-----------|---------:|------------:|
| **qe-writing-009** | Write "IID" — not "i.i.d." or "iid" | `writing.md` §General writing advice; `math.md` §IID | Medium | Mechanical (case-sensitive regex `\bi\.i\.d\.\b|\biid\b`) | 30 / 348 | 61 |
| **qe-math-010** | Blackboard `\mathbb{P}`, `\mathbb{E}`, `\mathbb{V}` for probability, expectation, variance — with braces | `math.md` §Probability, expectation, variance | **Very high** | Mechanical (regex catches bare `E[`, `E_t`, `\mathbb E` missing braces, `\Pr(`, `\Var(`) | 124 / 348 | 1,608 |
| **qe-math-011** | Distribution names: plain letters (`N`, `U`); `\mathrm{…}` for multi-letter — never `\mathcal` / `\mathbb` | `math.md` §Distribution names | High | Mechanical (regex on `\mathcal\{N\}` / `\{\\cal N\}`) | 34 / 348 | 134 |
| **qe-math-012** | Multiplication: `\cdot` or juxtaposition — never `*` in math | `math.md` §Multiplication in equations | Medium | Mechanical (regex `\*` inside `$…$` / `$$…$$`) | 4 / 348 | 6 |
| **qe-math-013** | Reference equations via `` {eq}`label` ``; do not hand-write numeric equation references | `math.md` §end | Medium | Partial (detect numeric refs near labelled equations) | 6 / 348 | 6 |
| **qe-math-014** | Braces `\{…\}` for events, parentheses `(…)` for sets when using `\mathbb{P}` | `math.md` §Probability, expectation, variance | Low | Judgment | — | not mechanically checkable |
| **qe-math-015** | Lowercase for densities/PMFs (`f`, `g`, `p`), uppercase for CDFs (`F`) | `math.md` §Density and mass functions | Low | Judgment | — | not mechanically checkable |

> **Status:** these are proposed as rules `qe-writing-009` and `qe-math-010`–`qe-math-015` in [`action-style-guide` issue #18](https://github.com/QuantEcon/action-style-guide/issues/18). The two weakest-evidence rules (`qe-math-014`, `qe-math-015`) may be deferred.

---

## 4. Scoring rubric

Each in-scope category is scored **0–10** using the rubric below. Be calibrated and consistent — do not be lenient.

| Score | Meaning |
|-------|---------|
| **10** | Fully compliant. No deviations found. |
| **9**  | Excellent. At most 1–2 trivial / stylistic-preference deviations. |
| **8**  | Good. A few isolated minor issues, no systemic pattern. |
| **7**  | Mostly compliant. A handful of inconsistencies across the file. |
| **6**  | Acceptable. Multiple violations but the file is readable and the core conventions hold. |
| **5**  | Mixed. Several **systemic** issues (a rule violated repeatedly throughout). |
| **4**  | Below standard. Many violations; one or more rules ignored entirely. |
| **3**  | Significantly out of style. Multiple rules ignored entirely. |
| **2**  | Major rework needed. Most rules in this dimension are violated. |
| **1**  | Almost entirely non-conformant. |
| **0**  | Reserved — only if the file is effectively empty or has no relevant content. |

**Categories not applicable to a given lecture** (e.g., JAX in a non-JAX lecture, Code in a pure-prose lecture, Math in a history lecture) are scored `N/A` and excluded from the overall.

**Overall score** = mean of in-scope category scores, rounded to 1 decimal.

**Priority bucket** (derived from overall):
- **HIGH** — overall ≤ 5.0, or any single in-scope category ≤ 4
- **MEDIUM** — overall 5.1 – 7.0
- **LOW** — overall 7.1 – 8.5
- **NONE** — overall ≥ 8.6

---

## 5. Severity definitions for individual findings

Each issue listed in a report is tagged:

- **Critical** — violates a build-risk rule (`qe-math-006` `align` inside `$$`, `qe-admon-003` tick mismatch, broken `{eq}` refs). One occurrence is enough.
- **High** — systemic violation (repeated 5+ times) **or** isolated violation of a Very-High-weight rule (`qe-writing-006`, `qe-math-002`, `qe-math-006`, `qe-admon-003`).
- **Medium** — repeated violation (2–4 instances) **or** isolated violation of a High-weight rule.
- **Low** — isolated single-occurrence stylistic violation; preference-level item.

---

## 6. Per-lecture report template

Each lecture audit must be a markdown file with **this exact structure**. Keep it compact — total length ~40–80 lines depending on category coverage.

```markdown
# <lecture filename without extension>

- **Series:** <series name>
- **File:** `lectures/<filename>.md`
- **Audit date:** YYYY-MM-DD
- **Corpus snapshot:** `<10-char commit of the series at audit time>`
- **Categories audited:** writing, math, code, jax, figures, references, links, admonitions  *(or a subset)*
- **Overall score:** X.X / 10
- **Priority:** HIGH | MEDIUM | LOW | NONE

## Score breakdown

| Category     | Score | One-line note |
|--------------|-------|---------------|
| Writing      | X/10  | … |
| Math         | X/10  | … |
| Code         | X/10  | … |
| JAX          | N/A   | not a JAX lecture |
| Figures      | X/10  | … |
| References   | X/10  | … |
| Links        | X/10  | … |
| Admonitions  | X/10  | … |

## Issues

### Critical
- **[qe-…-…]** — short description. *Example:* `lectures/x.md:NNN`. *Count:* N occurrences.

### High severity
- **[qe-…-…]** — …

### Medium severity
- **[qe-…-…]** — …

### Low severity
- **[qe-…-…]** — …

(Use "_None found._" under any empty severity heading.)

## Strengths
- …

## Recommended actions
1. …
2. …
```

**Rules for filling it in:**
- Rule IDs use the canonical `qe-…-…` form. Proposed addendum rules (§3) use their proposed permanent IDs tagged **(proposed)**, e.g. `qe-math-010 (proposed)`.
- Cite at least one concrete example or line number for every Critical/High/Medium issue.
- If a category is not applicable to the lecture, write `N/A` in the score column and note the reason.
- Output filename: same stem as input lecture, e.g. `lectures/cobweb.md` → `cobweb.md`.
- Do **not** include the lecture's own content in the report — only findings.

---

## 7. Per-series README template

Each series folder gets a `README.md` with this structure:

```markdown
# Summary

- **Audit date:** YYYY-MM-DD
- **Corpus snapshot:** `<10-char commit>`
- **Lectures audited:** N
- **Categories audited:** …
- **Average overall score:** X.X / 10
- **Average per-category scores:** writing X.X, math X.X, code X.X, …

## Priority distribution

| Priority | Count | % |
|----------|-------|---|
| HIGH     | …     | … |
| MEDIUM   | …     | … |
| LOW      | …     | … |
| NONE     | …     | … |

## Top systemic issues across the series

1. **[qe-…-…]** — short description — appears in N / total lectures.
2. …

## Lectures ranked by priority (lowest score first)

| # | Lecture | Writing | Math | Code | JAX | Fig | Ref | Link | Adm | Overall | Priority |
|---|---------|---------|------|------|-----|-----|-----|------|-----|---------|----------|
| 1 | [name](name.md) | … | … | … | … | … | … | … | … | X.X | HIGH |
| … |

## Series-level recommendations
- …
```

If only a subset of categories were audited, drop the unused columns rather than filling with N/A.

---

## 8. How a pass is produced

A pass has three layers. Keeping them separate is what makes two passes
comparable: the first two layers are code, so re-running them on the same
snapshot gives byte-identical output, and only the third involves judgment.

### 8.1 Evidence layer — measured, not judged

`tools/qestyle_scan.py` runs every mechanically-detectable rule (§9) over a
**pinned corpus snapshot** — one commit per series, recorded in
`lectures/data/snapshot.json` and in each report header. It emits per-lecture,
per-rule counts with line numbers. It measures only; it never scores.

Pinning the snapshot matters. In the previous pass the corpus moved underneath
the audit: two `lecture-dp` lectures were added on the audit date and went
unaudited, and one report described a lecture (`supply_demand_foundations_v2`)
that does not exist in any of the five repositories' history. Neither failure is
possible when the inputs are a commit and a program.

### 8.2 Scoring layer — arithmetic

`tools/qestyle_draft.py` turns evidence into a draft report: severity per §5,
category scores from the weighted violation load, and the overall score and
priority bucket per §4. `tools/qestyle_score.py --fix` then recomputes the
header from each report's own score table, so a report cannot contradict itself.
Run `--check` to assert this holds; it failed on 94 of 299 reports in the
previous pass, with a further 35 carrying a priority the rule does not give.

Category scores are a declining function of violation load: each violated rule
contributes its audit weight (§2) times a saturating repetition factor, capped
per weight class so that a lecture whose only deviations are low-weight cannot
be scored alongside one that ignores a very-high-weight rule throughout.

### 8.3 Review layer — judgment

Reviewers take the drafts and the lecture sources and add what code cannot
measure: the six in-scope registry rules and two proposed rules that are
genuine judgment calls (§9), plus the per-lecture **Strengths** and
**Recommended actions**. Reviewer instructions:

1. Read this spec first. Do not re-interpret rules.
2. Treat the drafted mechanical counts as authoritative. If one looks wrong,
   report it as a scanner defect — do not quietly edit the number, or the
   report stops matching the CSVs.
3. Score the judgment-only rules by reading the lecture. For files over 1500
   lines, read the head, a middle slice and the tail.
4. Adjust a drafted category score only for a judgment reason, and say what it
   was in the category's one-line note.
5. Be consistent: the same deviation gets the same rule ID, severity and
   wording across every report you write.
6. Do **not** modify any lecture file.

## 9. Deterministic coverage — measured

`action-style-guide` roadmap Phase 4.3 planned deterministic checkers for "~13"
rules; [issue #19](https://github.com/QuantEcon/action-style-guide/issues/19)
argued from this corpus that 22 were reachable. Implementing them settled the
question: **41 of the 49 rules are mechanically checkable** — 36 of the 42
in-scope registry rules, plus 5 of the 7 proposed rules. The implementations
live in `tools/qestyle_rules.py`, one function per rule.

### Mechanised (41)

| Category | Checked | Rules |
|----------|--------:|-------|
| Writing | 4 / 8 | `qe-writing-001`, `qe-writing-004`, `qe-writing-006`, `qe-writing-008` |
| Math | 8 / 9 | `qe-math-001`–`qe-math-008` |
| Code | 5 / 6 | `qe-code-002`–`qe-code-006` |
| Figures | 11 / 11 | `qe-fig-001`–`qe-fig-011` |
| References | 1 / 1 | `qe-ref-001` |
| Links | 2 / 2 | `qe-link-001`, `qe-link-002` |
| Admonitions | 5 / 5 | `qe-admon-001`–`qe-admon-005` |
| Proposed | 5 / 7 | `qe-writing-009`, `qe-math-010`–`qe-math-013` |

Several needed a real MyST lexer rather than a regex over the raw file — a
transpose apostrophe must not be counted in prose, a `{math}` directive body is
mathematics and not code, display math can be closed at the end of a content
line or wrapped in a blockquote, and a gated `{exercise-start}` is a marker
rather than a container. `tools/qestyle_lex.py` handles that structure.

Three of the checks are heuristic and say so where they fire: `qe-writing-004`
and `qe-writing-006` consult curated proper-noun and common-noun lists;
`qe-math-002` counts an apostrophe as transpose only on a matrix-like base and
counts `^T` only where the superscript is followed by a factor rather than a
relation, because `Y^T` is a data history in several lectures.

### Judgment-only (8) — the review layer's job

`qe-writing-002` (clear, concise, valuable), `qe-writing-003` (logical flow),
`qe-writing-005` (bold for definitions, italic for emphasis), `qe-writing-007`
(visual elements), `qe-math-009` (prefer simpler notation), `qe-code-001` (PEP8
unless closer to mathematical notation), plus proposed `qe-math-014` (braces for
events) and `qe-math-015` (case for densities vs CDFs).

### JAX (7) — out of scope

`qe-jax-001`–`qe-jax-007` target `lecture-jax`, which is not part of this
corpus. Reports mark the JAX category **out of scope**, which is distinct from
`N/A` ("not applicable to this lecture").

---

## 10. Reproducing a pass

```bash
# 1. evidence, from a pinned snapshot
python3 tools/qestyle_scan.py --corpus ../quantecon --out lectures/data \
    --period YYYY-MM --append-history lectures/data/rule_reach_history.csv

# 2. draft every per-lecture report
python3 tools/qestyle_draft.py --corpus ../quantecon --out lectures --date YYYY-MM-DD

# 3. review pass (judgment rules, strengths, actions)  -- see 8.3

# 4. derive scores, then the aggregate documents
python3 tools/qestyle_score.py --root lectures --fix --csv lectures/data/scores.csv
python3 tools/qestyle_report.py --summarise --history YYYY-MM --splice
```

`UPDATE.md` is the full runbook, including the TOC regeneration and the
consistency checks to run before pushing.
