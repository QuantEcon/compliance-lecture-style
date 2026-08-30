## Summary

Building mechanical checkers for 41 of the 49 rules turned up a pattern worth reporting: **most of the effort was not writing patterns, it was deciding what the rule meant.** Nineteen of the 41 checks needed fixing after their first adversarial sampling, and the fixes were usually not regex corrections — they were decisions the rule definition had left to the implementer.

We then audited the rule files directly, asking one question per rule: *when someone sits down to write a checker for this, what does the definition fail to tell them?* Result: **144 distinct gaps across 42 of the in-scope rules.** Four rules came back needing nothing.

This issue proposes changes to the **format** of the rule definitions, not to the rules themselves. Every rule here is a good rule. The problem is that two people implementing the same rule will disagree on its counts, and neither will be wrong.

## The one rule that gets it right

`qe-fig-003` (no embedded matplotlib titles) is the only rule in the registry with an explicit exemption clause:

> **Exceptions:** `ax.set_title()` may be used ... when inside `exercise` or `solution` directives

It is also the only figure rule that came out of adversarial sampling with **zero false positives** (0 FP / 15 TP). That is not a coincidence, and it is the whole argument of this issue: one sentence naming the legitimate exception was worth more than any amount of care in the implementation.

By contrast, the rules with no exemption clause accumulated them by discovery:

| Rule | FPs / TPs sampled | The exemption nobody had written down |
|------|------------------:|--------------------------------------|
| `qe-fig-008` | 149 / 15 | a `plot()` call spans lines, so `linewidth=2` was two lines below the match |
| `qe-fig-005` | 99 / 15 | a cell that only *defines* a plotting helper renders nothing |
| `qe-fig-004` | 70 / 60 | `$\bar\pi_t$` is one word, not five; `Taylor-rule` is one word, not two |
| `qe-fig-002` | 36 / 20 | a screenshot or a photo of a GPU cannot be code-generated |
| `qe-fig-007` | 25 / 12 | `spines['bottom'].set_position(...)` moves an axis; it removes nothing |
| `qe-code-003` | 24 / 5 | a `{code-block} java` sample is not this lecture's dependency |
| `qe-code-002` | 22 / 12 | `alpha=` in a drawing call is opacity; `from scipy.stats import beta` cannot be renamed |
| `qe-math-004` | 4 / 11 | `\mathbf{1}\{X_t = x\}` is an indicator function, not a vector |

A shipped checker with `qe-fig-008`'s original behaviour would have told authors to add `lw=2` to plots that already had it, 149 times in a 15-hit sample.

**In fairness:** 55 of the 144 gaps map to a false positive we actually hit. The other 89 are ambiguities that happened not to bite — real, but not yet costly. We are not claiming the registry is broken; we are claiming it under-determines its own counts.

## Where the gaps are

| Class | Count | What it looks like |
|-------|------:|--------------------|
| **Scope / region** | 32 | which parts of a lecture the rule governs |
| **Conflated IDs** | 24 | one rule ID covering two failures with different severities |
| **Counting unit** | 23 | what constitutes one violation |
| **Exemptions** | 22 | the legitimate exception is not named |
| **Canonical form** | 12 | which spelling is preferred; legacy forms unmentioned |
| **Units / thresholds** | 10 | a threshold with no stated measurement |
| **Metadata** | 9 | fields a generated checker would need |

Four illustrations, each with the measurement behind it:

**A rule can be unimplementable as written.** `qe-fig-009` says figures should be "80–100% of text width". MyST offers four options that could express that and three are in use. `:width:` as a percentage *is* a share of text width; `:scale:` is a share of the image's own pixel size. We checked `:scale:` first and got 13 hits, all false — every one a deliberately scaled-down screenshot. Restricting to `:width:` was semantically right and left the rule with a reach of **one lecture**, because the corpus contains 18 `:scale:` values and a single `:width:`. The rule as written measures a quantity the corpus does not record. One field — *which option is measured* — would have settled it either way.

**A rule can describe 3% of its subject.** `qe-fig-005` requires a `name` field on "every figure", and describes figure *directives*. The corpus has 16 directive `:name:` values against **515 `mystnb` `figure.name`** entries on code cells. Nearly all QuantEcon figures are code-generated, and the rule does not mention that case at all.

**A threshold without a tokeniser is not a threshold.** `qe-writing-002` says "> 30–40 words as a rough guideline". On this corpus, 420 paragraph blocks exceed 40 words and 2,010 exceed 30 — the endpoint alone swings the finding count **4.8×**. `qe-fig-004`'s "5–6 words maximum" has the same problem, and it is where the 70 false positives came from.

**A rule can be silently inverted to make it checkable.** `qe-writing-004` forbids capitalising words that "aren't proper nouns", and names no proper-noun authority. In an economics corpus dense with eponyms, that oracle does not exist. Our implementation gave up on the rule as stated and inverted it: it fires only on a hand-curated 200-word common-noun list. The published count is therefore *a floor for a curated vocabulary*, not a measurement of the rule — and nothing in the registry tells a reader that.

## Proposal

Add machine-readable fields to the rule format. In priority order by measured value:

### 1. `Applies-in:` — the region list *(32 gaps)*

The single largest source of guessing. A rule should name the regions it governs:

```
**Applies-in:** narrative, list-item
**Not-in:** heading, caption, table-cell, inline-math, display-math, code-cell, directive-option
```

Region vocabulary: `narrative`, `heading`, `caption`, `list-item`, `table-cell`, `blockquote`, `inline-math`, `display-math`, `code-cell`, `display-code`, `directive-option`, `directive-body`, `frontmatter`.

Two sub-questions matter enough to be their own fields:

```
**Applies-in-directives:** yes | no | [note, exercise, solution, prf:*]
**Executable-only:** true | false
```

Evidence: 27% of `qe-writing-001` hits corpus-wide (119 of 442) sit inside a directive body — so whether directives are in scope changes the published count. `qe-code-003`'s 24-FP class was reading imports from non-executed and non-Python cells.

### 2. `Exceptions:` — required on every rule *(22 gaps)*

Make it mandatory, with `none known` as an explicit permitted value, so silence becomes a recorded decision rather than an omission. `qe-fig-003` is the proof this works.

### 3. `Counting-unit:` and `Threshold:` *(23 + 10 gaps)*

```
**Counting-unit:** occurrence | line | paragraph-block | heading | directive | figure | code-cell | lecture
**Threshold:** {quantity: words, tokenizer: <named>, operator: ">", value: 35}
```

Counting units are genuinely inconsistent today: `qe-math-008` counts once per lecture while every other math rule counts per occurrence, and nothing says so. Two tools will not agree on any count without this field.

Thresholds need a **named tokeniser**, shipped as a spec rather than left to each implementer: inline maths is one token; a hyphenated compound is one word; a role (`{cite}`, `{numref}`) is one word.

### 4. Split the conflated IDs *(24 gaps)*

Several IDs cover more than one failure, with different severities and different units. `qe-math-006` is the clearest: `align` nested inside `$$` breaks a PDF build, while a bare top-level `\begin{align}` is a convention preference. One is critical and one is cosmetic, and our checker had to invent the distinction in code.

Give each its own sub-ID with its own severity and unit:

```
qe-code-003a  non-Anaconda import with no install cell     severity: correctness
qe-code-003b  install cell not the first executable cell   severity: convention
qe-code-003c  install cell missing hide-output             severity: cosmetic
```

Candidates with the most need: `qe-code-003` (4 sub-rules), `qe-ref-001` (4), `qe-math-006` (2), `qe-math-008` (2), `qe-admon-003` (2), `qe-code-002` (2).

### 5. `Canonical:` / `Legacy-forms:` *(12 gaps)*

State the closed set of spellings in scope, including legacy TeX forms that the corpus contains and the registry does not mention:

```
**Prohibited:** \mathbf{}, \boldsymbol{}, \bm{}, \pmb{}, \textbf{}, {\bf …}, {\boldmath …}
**Canonical:** the plain letter
```

`{\bf …}` occurs 30+ times in the corpus (17 as `{\bf 1}` alone) and was missed until found by hand. `{\cal …}` occurs 94 times and is the same story for `qe-math-011`. Where a rule names a mapping (`qe-code-002`'s Greek letters), **ship it as data** rather than three examples and "etc." — the capitalised forms `Sigma`, `Psi`, `Gamma` were missed entirely because the examples were all lowercase, and `lambda` can never be renamed because it is a Python keyword.

### 6. `Detectable:` and `Vocabulary:`

```
**Detectable:** deterministic | proxy | llm-review | human-only
**Vocabulary:** <name of a shipped word list, or none>
```

`Type: rule | style` currently conflates "has a measurable proxy" (`qe-writing-002` has a word threshold) with "cannot be measured at all" (`qe-writing-003`: "no jumps", "minimize distractions"). A generator reading the registry cannot tell them apart.

`Vocabulary:` matters because three writing rules depend on curated word lists that today live in each implementer's code. Ship them once — proper nouns, common nouns, sentence-boundary abbreviations, title-case stop words — and every checker agrees.

### 7. `Defers-to:` / `Related:`

For overlapping jurisdiction. `qe-math-004` and `qe-math-008` both have a claim on `\mathbf{1}`; neither mentions the other; we arbitrated it in code. Same for `qe-code-004` vs `qe-code-005` over a benchmark loop, and `qe-fig-011` vs `qe-fig-004`/`005`.

### 8. `Fixtures:` — make the examples machine-checkable

The ✅/❌ blocks are already there and are the best part of the format. Label them so a checker can be validated against the registry:

````markdown
```markdown
<!-- qe:bad expect=1 -->
## Binary Packages With Python Frontends
<!-- qe:ok -->
## Binary packages with Python frontends
```
````

## A worked example

`qe-code-003` rewritten in the proposed format. It had 7 gaps — the most of any rule — and every one closes with a field:

```markdown
### Rule: qe-code-003
**Type:** rule
**Detectable:** deterministic
**Title:** Package installation at lecture top

**Applies-in:** code-cell
**Executable-only:** true
**Languages:** [python]
**Counting-unit:** code-cell

**Sub-rules:**
- qe-code-003a  a non-Anaconda import with no install cell   severity: correctness
- qe-code-003b  install cell is not the first code cell      severity: convention
                position: {anchor: first_code_cell, tolerance_cells: 1}
- qe-code-003c  install cell missing hide-output             severity: cosmetic

**Package-manifest:** <url to a pinned environment.yml>
**Identifier-space:** distribution name, PEP 503 normalised (lowercase; `-`, `_`, `.`
  equivalent; version specifiers and extras stripped)
**Accepted-commands:** ["!pip install", "%pip install", "!conda install"]

**Exceptions:**
- Cells tagged `no-execute` or `skip-execution` do not create an install obligation.
- Modules the lecture writes itself (`%%writefile foo.py`) are not installable packages.
- The Python standard library is always considered present.
```

Two of those fields fix live false positives on the current corpus. `Identifier-space` fixes `networks.md`, where `import quantecon_book_networks` is reported as uninstalled while line 20 reads `!pip install quantecon-book-networks==1.6` — a plain substring test cannot bridge the `-`/`_` difference. `Package-manifest` replaces a 90-name allowlist we had to invent, in which every entry is an unreviewed policy decision embedded in code.

## Cost, and what not to do

**This is not a request to rewrite 49 rules at once.** The fields are additive and the format stays prose-with-markers, so a rule with no `Applies-in:` behaves exactly as today. Suggested order:

1. `Exceptions:` on every rule — cheapest, and highest measured value.
2. `Applies-in:` / `Counting-unit:` on the rules that already have mechanical checkers.
3. Sub-IDs for the 6 conflated rules — the only change that affects rule identity, so worth deciding deliberately.
4. Shipped vocabularies and tokenisers.

**What we would not do:** put regexes in the registry. We tried the equivalent and it was the wrong layer — most of our wrong counts were structural, not pattern errors. A `{math}` directive body typed as code, display math closed at the end of a content line, inline maths spanning a line break, a gated `{exercise-start}` treated as a container: six lexer bugs, each corrupting several rules at once. The registry should specify *what* is measured and *where*; how to parse MyST belongs in one shared lexer, not in 49 rule entries.

## Offer

The reference implementation is in [`tools/`](https://github.com/QuantEcon/compliance-lecture-style/tree/main/tools) of the lecture style compliance ledger — one function per rule plus the MyST lexer, dependency-free, running the whole 348-lecture corpus in seconds. Per-rule false-positive rates and fixes are in [`tools/VERIFICATION.md`](https://github.com/QuantEcon/compliance-lecture-style/blob/main/tools/VERIFICATION.md); labelled per-lecture counts with line numbers are in `lectures/data/violations.csv` at a pinned commit per series.

It is offered for adoption rather than parallel maintenance — see [#19](https://github.com/QuantEcon/action-style-guide/issues/19). If the format changes proposed here land, the checkers should be regenerated from the registry rather than maintained by hand, and most of this issue becomes unnecessary.

## References

- Rule files audited: `style_checker/rules/{writing,math,code,figures,links,references,admonitions,jax}-rules.md`
- Compliance ledger (the reference implementation and its data): https://github.com/QuantEcon/compliance-lecture-style
- Measured coverage and the judgment-only set: [`lectures/spec.md`](https://quantecon.github.io/compliance-lecture-style/spec.html) §9
- Related: [#18](https://github.com/QuantEcon/action-style-guide/issues/18) (7 proposed rules — all seven would want these fields from the start), [#19](https://github.com/QuantEcon/action-style-guide/issues/19) (deterministic-checker scope), [#20](https://github.com/QuantEcon/action-style-guide/issues/20) (where checkers should live)
