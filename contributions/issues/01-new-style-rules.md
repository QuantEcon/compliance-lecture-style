## Summary

A recent cross-series style audit of QuantEcon lecture content ([QuantEcon/audit.2026-05.style-guide](https://github.com/QuantEcon/audit.2026-05.style-guide) — 5 series, 299 lectures) surfaced **7 conventions that are documented in the [QuantEcon manual style guide](https://github.com/QuantEcon/QuantEcon.manual/tree/main/manual/styleguide) but are not yet encoded as rules in this repository**. This issue proposes adding them.

The proposals are split into two tiers:

- **5 strong-evidence rules** — each violated repeatedly across the corpus, with a clear style-guide source.
- **2 weaker-evidence rules** — documented in the style guide but with thinner corpus evidence. Included for completeness; the team may want to defer or skip these.

Ready-to-merge rule entries (in the existing `style_checker/rules/*.md` format) are linked from each item below.

---

## Strong-evidence proposals (5)

### 1. `qe-writing-009` — Write "IID", not "i.i.d." or "iid"

- **Style-guide source:** [`writing.md` § General writing advice](https://github.com/QuantEcon/QuantEcon.manual/blob/main/manual/styleguide/writing.md); [`math.md` § IID](https://github.com/QuantEcon/QuantEcon.manual/blob/main/manual/styleguide/math.md)
- **Type:** `rule` (mechanical — case-sensitive regex)
- **Corpus evidence:** ~30 lectures across the corpus use "i.i.d." or "iid" in narrative text; concentrated in `lecture-python.myst` (21 / 110)
- **Proposed implementation:** Phase 4.3 candidate. Case-sensitive regex `\bi\.i\.d\.\b|\biid\b` outside fenced code / inline code / math blocks.
- **Ready-to-merge rule entry:** `qe-writing-009-IID.md` (in the contribution PR)

### 2. `qe-math-010` — Use `\mathbb{P}`, `\mathbb{E}`, `\mathbb{V}` for probability, expectation, variance

- **Style-guide source:** [`math.md` § Probability, expectation, and variance](https://github.com/QuantEcon/QuantEcon.manual/blob/main/manual/styleguide/math.md)
- **Type:** `rule` (mechanical — regex catches bare `E[`, `E_t`, `\mathbb E` without braces, `\Pr(`, `\Var(`)
- **Corpus evidence:** **~60 lectures** across the corpus. Highest counts: `lecture-python.myst` (21 / 110), `lecture-python-advanced.myst` (17 / 55), `lecture-dp` (17 / 50). This is the single most violated math convention in the corpus that isn't already a coded rule.
- **Proposed implementation:** Phase 4.3 candidate. Regex with awareness of math-environment boundaries.
- **Ready-to-merge rule entry:** `qe-math-010-blackboard-PEV.md`

### 3. `qe-math-011` — Plain letters for distribution names; `\mathrm{…}` for multi-letter — never `\mathcal{N}` or `\mathbb{N}`

- **Style-guide source:** [`math.md` § Distribution names](https://github.com/QuantEcon/QuantEcon.manual/blob/main/manual/styleguide/math.md)
- **Type:** `rule` (mechanical)
- **Corpus evidence:** **~30 lectures**. Concentrated in `lecture-python-advanced.myst` (14 / 55) and `lecture-dp` (9 / 50). Most violations are `\mathcal{N}(\mu, \sigma^2)` for the normal distribution.
- **Proposed implementation:** Phase 4.3 candidate. Regex `\\mathcal\{N\}|\{\\cal N\}|\\mathbb\{N\}` for normal-distribution misuses; multi-letter distributions need `\\text\{Beta\}|\\operatorname\{Beta\}` → `\\mathrm{Beta}` checks.
- **Ready-to-merge rule entry:** `qe-math-011-distribution-naming.md`

### 4. `qe-math-012` — Multiplication: `\cdot` or juxtaposition — never `*` inside math

- **Style-guide source:** [`math.md` § Multiplication in equations](https://github.com/QuantEcon/QuantEcon.manual/blob/main/manual/styleguide/math.md)
- **Type:** `rule` (mechanical)
- **Corpus evidence:** ~5 confirmed lectures (low frequency) — but it's a clear, unambiguous rule with zero judgment cost.
- **Proposed implementation:** Phase 4.3 candidate. Regex `\*` inside `$…$` / `$$…$$` blocks. Care needed to avoid false positives in non-math contexts (markdown emphasis, code).
- **Ready-to-merge rule entry:** `qe-math-012-multiplication.md`

### 5. `qe-math-013` — Reference equations via `` {eq}`label` ``

- **Style-guide source:** [`math.md` § end (auto-numbering example)](https://github.com/QuantEcon/QuantEcon.manual/blob/main/manual/styleguide/math.md)
- **Type:** `rule` (partial — regex flags candidates, judgment confirms)
- **Corpus evidence:** Moderate. Repeatedly observed (manual "see equation (3)" or "(eq. above)" references in older lectures despite labelled equations being available). Currently `qe-math-007` bans `\tag` (manual numbering) but doesn't positively require the `{eq}` reference syntax.
- **Proposed implementation:** Phase 4.3 candidate (partial). Detect numeric refs ("equation N", "(N)") near labelled equations.
- **Ready-to-merge rule entry:** `qe-math-013-equation-refs.md`

---

## Weaker-evidence proposals (2) — for the team's consideration

These are documented in the style guide but have thinner corpus evidence. The team may prefer to defer or skip them.

### 6. `qe-math-014` — Braces `\{…\}` for events; parentheses `(…)` for sets when using `\mathbb{P}`

- **Style-guide source:** [`math.md` § Probability, expectation, and variance](https://github.com/QuantEcon/QuantEcon.manual/blob/main/manual/styleguide/math.md)
- **Type:** `style` (judgment — distinguishing an "event" from a "set" requires reading)
- **Corpus evidence:** Limited. The rule was identified during the audit but few clear violations were tallied (was scored under our audit ID `qe-math-A2` with note "limited evidence").
- **Recommendation:** Could be folded into `qe-math-010` as a sub-rule rather than a separate rule, or deferred until a future audit confirms it's a real source of inconsistency.
- **Ready-to-merge rule entry:** `qe-math-014-events-vs-sets.md`

### 7. `qe-math-015` — Lowercase letters for densities/PMFs; uppercase for CDFs

- **Style-guide source:** [`math.md` § Density and mass functions](https://github.com/QuantEcon/QuantEcon.manual/blob/main/manual/styleguide/math.md)
- **Type:** `style` (judgment — requires understanding which function is being referenced)
- **Corpus evidence:** Limited. Identified during the audit but few clean violations were observed.
- **Recommendation:** Defer until evidence of systemic deviation accumulates. Useful as a documented convention even if not enforced.
- **Ready-to-merge rule entry:** `qe-math-015-density-CDF-case.md`

---

## Why now?

These rules are already enforced informally in code review and via the [QuantEcon manual style guide](https://github.com/QuantEcon/QuantEcon.manual/tree/main/manual/styleguide). Adding them to action-style-guide:

1. **Catches them at PR time** rather than post-publication — the audit found 90+ lectures violating rules #1–#4 alone.
2. **Closes the gap** between the human-readable style guide and the machine-enforceable rule registry.
3. **Provides corpus-validated targets** for Phase 4.3 deterministic checking (most of these are pure regex; see [#19 — Phase 4.3 acceleration](https://github.com/QuantEcon/action-style-guide/issues/19)).

## What's being asked

1. Are any of these rules already on the team's radar / in a draft branch?
2. Are there reasons (style debate, false-positive risk, scope) to exclude any?
3. If the team is open to adding them, the ready-to-merge rule entries can be submitted as a single PR against `style_checker/rules/writing-rules.md` and `style_checker/rules/math-rules.md`.

## References

- **May 2026 audit — the pass these counts come from:** https://github.com/QuantEcon/audit.2026-05.style-guide
- **Corpus data, re-measured each pass:** https://github.com/QuantEcon/compliance-lecture-style
- **Rule mapping (spec §3):** https://quantecon.github.io/compliance-lecture-style/spec.html
- **Style guide source:** https://github.com/QuantEcon/QuantEcon.manual/tree/main/manual/styleguide
