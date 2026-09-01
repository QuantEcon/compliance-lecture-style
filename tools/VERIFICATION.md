# Verification — detectors, and the pins a period is measured at

**All 41 checks have now been sampled.** Every check in `qestyle_rules.py` was reviewed
adversarially against the real corpus before its counts were published: for each rule, at least ten flagged occurrences were
opened in the lecture source and judged against the canonical rule text, and the corpus
was probed for forms the check might miss. Where a rule's total reach was small enough,
every hit in the corpus was read rather than a sample. The table records the verdict *before* fixes
and what the fix was, because the false positives are the interesting part — a wrong
count is worse than a missing one when the number ends up in a published report.

Verified against the 2026-08 snapshot (`lectures/data/snapshot.json`).

| Rule | Verdict before fix | FP / TP sampled | What was wrong, and the fix |
|------|--------------------|-----------------|------------------------------|
| `qe-writing-006` | needs-fix | 52 / 40 | Possessives (`Newton's`) and hyphenated surnames (`Gram-Schmidt`, `Metropolis-Hastings`) defeated the proper-noun lookup; country names were missing. Added `_is_proper()` (strips possessives, splits hyphens, treats any `X's` as a name) and extended the list. Also added the rule's other half — an H1 that is *not* Title Case.. **A later review found two residual false-positive shapes:** `_is_proper` required *every* hyphen-part to be allowlisted, so `Student-t` failed on the bare `t`, and `jagannathan` was missing while `hansen` was present. A single letter in a hyphenated name is a mathematical label, not a word that should have been lowercased, so single-letter parts are now accepted — which also covers `F-test` and `p-value` — and both surnames were added. Removed exactly 3 occurrences (`qe-writing-006` 1, `qe-fig-004` 2: the `Student-t` heading and caption in `mcmc`, the `Hansen-Jagannathan` caption in `doubts_or_variability`) with no collateral: `First-Order Conditions`, `Back-of-the-Envelope Calculations` and `Multi-Step-Forward` are still flagged |
| `qe-writing-008` | broken | 12 / 28 | Masking inline code and maths with single spaces manufactured double spaces out of correctly-spaced prose. The lexer now masks with NUL, and cross-line inline maths is resolved before masking. |
| `qe-writing-009` | needs-fix | 3 / 12 | Fired on MyST anchor definitions (`(iid-theorem)=`) and on role targets (``{ref}`IID <iid-theorem>` ``). Anchors are skipped and inline code is masked. |
| `qe-writing-001` | added after | — | Not present at review time; added as a paragraph-block sentence counter with an abbreviation list. |
| `qe-writing-004` | added after | — | Not present at review time; added, firing only on a curated common-noun list so an unlisted surname cannot be mistaken for a violation. |
| `qe-math-001` | added after | — | Not present at review time; added. Its first form of false positive — inline maths spanning a line break — is fixed in the lexer. |
| `qe-math-002` | broken, and later **still false at scale** | 22 / 14 | The `^T` branch was ~88 % false: summation limits (`\sum_{t=0}^T`), terminal dates, data histories (`Y^T`), discount factors (`\delta^T`). It now requires a matrix-like base *and* a following factor rather than a relation. The apostrophe branch missed lowercase vectors (`c'x`, `x_t'`), now covered. **A later review found three more false-positive classes, all from guards that one branch had and the others did not:** `^\prime` carried no guard at all, so every `u^\prime(c)` derivative counted (49 occurrences); `prime_vec` had no relation guard, so `\sum_{w' \in W}`, `\max_{a' \in \Gamma}` and `\sum_{s' \in S}` counted as transposes (109); and neither apostrophe branch excluded a *double* prime, so second derivatives `H''(p)`, `W''(\hat I)`, `S''(\bar R)` counted (23). Occurrences 2,129 → 1,865, reach 97 → 93; 264 removed, 0 added. |
| `qe-math-003` | sound | 1 / 12 | One false positive: `\left\{\begin{array}{ll}…\right.` is a case distinction. Now excluded. |
| `qe-math-004` | needs-fix | 4 / 11 | Indicator functions (`\mathbf{1}\{X_t = x\}`) are not vectors, and the legacy `{\bf …}` spelling was missed. Both fixed; the indicator guard looks at the next source line too. |
| `qe-math-005` | broken | 1 / 0 | Matched matrix-by-elements notation and missed the real violation, which is written with parentheses (`(k_t)_{t \geq 0}`). Rewritten. |
| `qe-math-006` | needs-fix | 0 / 0 | Reported nothing, because there is no `align` inside `$$` anywhere in the corpus — which is itself the finding that withdrew the previous pass's headline build-risk claim. Now also reports bare top-level amsmath blocks, with distinct wording and non-Critical severity. |
| `qe-math-007` | sound | 0 / 0 | Extended to `\label{}` and `\eqno`, which MyST also does not resolve. |
| `qe-math-008` | broken | 8 / 8 | Every hit was an indicator function; genuine ones vectors written `\mathbf 1` were missed. Rewritten to detect ones-vector usage in any spelling and report only the *unexplained* case, leaving the bold spelling to `qe-math-004`. |
| `qe-math-010` *(proposed)* | needs-fix, then **undercounting** | 207 / 24 | Double-counted `\mathbb E` in two branches, and the bare-`E` branch fired on `E` as a matrix name. Branches now mask each other, and the bare-letter branch is gated on the lecture actually applying `E` as an operator. **A later review found the opposite failure:** `[PEV]\b` never fires before a subscript, because `_` is a word character — so `\mathbb E_t`, the corpus's usual conditional expectation, was invisible. Now `[PEV](?![A-Za-z])`, which still rejects `\mathbb Exp`. The Roman branch also missed `\textrm{…}`, `{\rm …}` and the name `Prob` while catching `\mathrm{…}` and `\Prob` — same notation, same rule — so those were added. Reach 105 → 117, occurrences 1,167 → 1,396; 232 hits added, all corroborated against their own source line, 0 false positives found. |
| `qe-math-011` *(proposed)* | broken, then **undercounting** | 79 / 18 | `\mathcal{G}` and `\mathcal{B}` are sigma-algebras, not distributions. Restricted to `N`/`U` *and* to a distribution context (after `\sim`, or applied to a parameter list). **A later review found that gate misfiring on one spelling:** the bare-`\mathcal` alternative did not consume the closing brace, so `{\mathcal N}(0,1)` presented the gate with `}` and was refused, while `{\cal N}(0,1)` and `\mathcal{N}(0,1)` passed. A brace-wrapped alternative now mirrors the `\cal` one. Reach 24 → 34, occurrences 86 → 140; 54 hits added, 0 false positives found. |
| `qe-math-012` *(proposed)* | broken | 18 / 5 | Fired on `\operatorname*`, on a standalone `$*$` naming the symbol, and on convolution notation. All three excluded. |
| `qe-math-013` *(proposed)* | broken | 16 / 20 | "equation (44) of {cite}`BEGS1`" is a reference into someone else's paper, where a number is the only citable thing. External-source references are now skipped. |
| `qe-code-002` | broken | 22 / 12 | `alpha=` in a drawing call is matplotlib's opacity; capitalised Greek (`Sigma`, `Psi`, `Gamma`) was missed entirely. Opacity is judged per cell (the kwarg is often on a continuation line) and capitalised forms were added. |
| `qe-code-003` | broken | 24 / 5 | Imports were read from the whole code text, so docstring prose ("from the urn without replacement") and a `{code-block} java` sample were reported as uninstalled dependencies. Now per-cell, Python-only, skipping `no-execute` cells and modules the lecture writes itself; and every install cell is position-checked, not only the first. |
| `qe-code-004` | needs-fix | 3 / 22 | Missed `from time import time` usage, `timeit.default_timer` and the `%time` magic. Added. |
| `qe-code-005` | needs-fix | 0 / 10 | Only caught `%timeit`, not the hand-rolled benchmark loop the rule's own example shows. Added a cell-level check for a timing read inside a loop that accumulates or averages. |
| `qe-code-006` | sound | 0 / 0 | Hardened anyway: package detection now reads real code only, and the warning must actually name the package. |
| `qe-fig-001` | needs-fix | 5 / 28 | Counted *reads* of `rcParams` and `style.use('default')` (a reset), and missed `rcParams.update(...)`. Now only writes count. |
| `qe-fig-002` | needs-fix | 36 / 20 | Flagged screenshots and photographs — a terminal capture or a photo of a GPU cannot be code-generated. Those asset families are excluded. |
| `qe-fig-003` | needs-fix | 0 / 15 | Missed `ax.set(title=…)` and `ax.title.set_text(…)`, ~73 lines corpus-wide. Added; the exercise/solution exemption was already correct. |
| `qe-fig-004` | broken | 70 / 60 | Tokenised LaTeX into words, so `$\bar\pi_t$` counted as five; split hyphenated compounds; and repeated the possessive bug. Maths is masked, compounds are one token, and the proper-noun test now routes through `_is_proper()`. |
| `qe-fig-005` | needs-fix | 99 / 15 | Counted cells that only *define* a plotting helper. A cell renders a figure only if a plotting or render call sits at column zero; `_strip_py` also had to stop collapsing docstrings, which was pulling indented code to column zero. (Reach had already been extended during development from `{figure}` directives to code-cell `mystnb.figure.name` metadata, where most QuantEcon figures live — 44 lectures to 293.) |
| `qe-fig-006` | needs-fix | 7 / 12 | `Im` for the imaginary part is correctly capitalised, and a hyphenated first word (`Taylor-rule`) defeated the proper-noun lookup. |
| `qe-fig-007` | needs-fix | 25 / 12 | `spines['bottom'].set_position(('data', 0))` moves an axis; it does not remove the box. Only removal counts now. |
| `qe-fig-008` | broken | 149 / 15 | A `plot(...)` call spanning several lines was judged on its first line, so `linewidth=2` two lines down was missed. The check now assembles the whole argument list by balancing parentheses. |
| `qe-fig-010` | sound | 0 / 4 | — |
| `qe-link-001` | needs-fix | 2 / 21 | A PDF under `/_static/` is a downloadable asset, not a sibling lecture. Asset paths are skipped. |
| `qe-link-002` | needs-fix | 0 / 25 | Missed hosts that occur in the corpus. Added `python-intro`, `dp`, `networks` and `dle` to the known series domains. |
| `qe-ref-001` | broken, and the fix was **dead code** | 11 / 29 | `and` was treated as an author-position verb, so a list of parenthetical citations was flagged twice over. Removed, list contexts (`include`, `see`) exempted, and findings de-duplicated to one per citation site. **A later review found the exemption never fired.** It tested `s[:m.start() + 1]`, but `NARRATIVE_LEAD` *consumes* the cue word — for `"…reading, see {cite}`x`"` the slice was `'…reading, s'`, so `see\s*$` could not match, and the exemption only worked via the `[.!?]\s+` alternative. Now tested against `s[:m.start()] + m.group(0)` minus the role, which includes the cue. Removed 16 occurrences across 5 lectures, 0 added; every one read as a genuine `see {cite}` reference pointer (`estspec.md:51`, `lqcontrol.md:262` "See {cite}`HansenSargent2008` for details", the two `knowing_forecasts_of_others` footnotes). |
| `qe-fig-009` | broken | 13 / 0 | Counted `:scale:`, which is relative to the image's own pixel size — a screenshot at `:scale: 50` says nothing about how wide it renders, and every one of the 13 hits was a scaled-down screenshot. Restricted to `:width:` as a percentage, which *is* a share of the text width. The corpus has exactly one such value (`100%`), so the rule is now correctly silent. |
| `qe-fig-011` | sound | 0 / 0 | Exhaustively checked: the only nestings in the corpus are `{image}` inside `{prf:example}`, which is what the rule asks for. |
| `qe-admon-001` | broken | 4 / 0 | Counted plain ```` ```python ```` display blocks, which are shown rather than run. The rule is about *executable* cells, so the check now requires a `{code-cell}`. All four hits were display blocks. |
| `qe-admon-002` | sound | 0 / 1 | The single hit is genuine — a `:::{solution-start}` colon fence with no `:class: dropdown`. |
| `qe-admon-003` | sound | 0 / 2 | Both hits read in source and confirmed: `python_by_example.md` has two `{exercise-start}` fences that are never closed. |
| `qe-admon-004` | sound | 0 / 0 | Exhaustively checked: all 244 proof-family directives in the corpus carry the `prf:` prefix. A genuine clean result, not a dead check. |
| `qe-admon-005` | sound | 0 / 0 | Zero hits confirmed live rather than dead — a synthetic solution label with no matching exercise does fire the check. |

## Lexer bugs found along the way

Most false counts turned out to be structural rather than regex errors. Each of these
would have corrupted several rules at once:

1. **`{math}` directive bodies were typed as code.** 1,783 blocks across 172 lectures —
   every math rule was blind to them and every code rule was reading LaTeX. This alone
   moved `qe-math-002` in `lqcontrol` from 11 hits to 61.
2. **Display math closed at the end of a content line** (`… p}$$`) left the `$$` state
   machine inverted, so the rest of the lecture was typed as the wrong region.
3. **Blockquoted display math** (`> $$`) did the same.
4. **Inline maths spanning a line break** (`$N(0,\n\sigma^2)$`) was invisible, so its
   LaTeX looked like narrative text.
5. **Gated `{exercise-start}` treated as a container.** It is a marker: its fence closes
   immediately and `{exercise-end}` is a separate fence. Treating it as a container made
   every later directive look nested, and made `in_exercise` far too broad — which
   suppressed real `qe-fig-003` findings and invented `qe-admon-003` ones.
6. **HTML comments were scanned.** Commented-out prose and maths never reach the page.
8. **A `{code-cell}`'s YAML metadata block was typed as Python.** A cell may open with a
   `---` … `---` mystnb block, and its body is options, not code:
   `caption: Inflation spectra $f_{\pi\pi}(\omega,t)$` was scanned as Python and counted
   as a spelled-out Greek variable. The `:key: value` option spelling was already typed
   `option`; the block spelling was not. Fixed with a three-state flag while a code fence
   is open. `qe-code-002` lost 41 occurrences across 13 lectures, reach 49 → 38, and no
   other rule moved — every removal a `caption:` or `name:` line, with real code on
   neighbouring lines kept (`robust_permanent_income` 5 → 3, `var_subsets` 38 → 37).

   Note what this does *not* fix: a caption's mathematics is now in an `option` region, and
   no math rule reads those. Six captions in that one lecture write a bare `E(...)` where
   the prose writes `\mathbb{E}`. Whether the math rules should read caption text is a
   scope question, not a bug, and is unresolved.
7. **An inline-code span could run across a paragraph break.** `STREAM_CODE_RE` was
   written `` (`+)((?:[^`]|\n(?!\s*\n))*?)\1 `` — but `` [^`] `` matches a newline
   itself, so the `\n(?!\s*\n)` guard beside it was dead code and an unbalanced
   backtick paired with one hundreds of lines away. One stray `` `shock' `` at
   `five_preferences.md:166` — a backtick closed with a typographic apostrophe — masked
   **381 of that file's 798 narrative lines**, leaving 18 inline math spans where there
   are 318. Fixed to `` [^`\n] ``, so a newline is only ever consumed through the
   guarded alternative and a span still spans one line break but never a blank line.
   Corpus effect: `qe-writing-008` +79 occurrences, `qe-math-011` +2, `qe-math-001` +1,
   `qe-math-010` +1 — all in that one file, all real, all previously invisible. Three
   lectures have odd narrative backtick parity; only this one lost lines to it.

## Known limitations, accepted deliberately

Not every gap found is worth closing. These are left in, because closing them would trade a
measured undercount for an unmeasured false-positive rate — and the false-positive rate is
the number this audit's credibility rests on.

- **`qe-math-010`'s bare-letter branch requires a delimiter.** It counts `E[…]`, `E_t(…)`,
  `E\{…\}` but not `E_0 \sum` or `E \tilde\theta_t^2`, so a lecture that writes every
  expectation without brackets is undercounted. Loosening it would have to treat a lone `E`
  as an operator, and in this corpus `E` is very often a matrix. The same pattern computes
  the `e_is_operator` gate, so in a file where *every* expectation is delimiter-free the
  branch switches off entirely — `tax_smoothing_1` (lines 70, 203, 354) and
  `tax_smoothing_2` (122) are the known instances, both scoring 0 on the branch. The
  explicit-notation branches (`\mathbb E`, Roman spellings) are unaffected and do fire
  there.
- **`qe-ref-001` cannot see a bare author-year reference.** A reference written as plain
  prose — "Rosen and Topel (1988)" with no `{cite}` role — is invisible to a check that
  looks at roles. `match_transport` (1421) and `smoothing` (761, 791) score a clean
  References mark while containing exactly that.
- **`:load:` code cells are outside the scanner's reach.** A cell that executes a file from
  `_static/lecture_specific/` has no source in the lecture, so no `qe-code-*` or `qe-fig-*`
  rule can inspect it. `rob_markov_perf` (453) loads the non-robust MPE that every
  comparison in that lecture is measured against.
- **`qe-writing-006` depends on a curated noun list.** Any surname absent from
  `PROPER_NOUNS` reads as a lowercase word that should have been capitalised, and
  `_is_proper` requires *every* hyphen-part to be known — so `Rosen-Topel` fails on its
  second half. Two false positives are known in `hs_recursive_models` (1695, 1892).

Each of these is a reason to read the cited lines before trusting a category score, not a
reason to distrust the corpus totals.

- **`qe-math-002`: the primed next-period state is now handled per lecture.** The
  apostrophe is genuinely ambiguous in this corpus — a transpose in the LQ lectures, a
  continuation state in the dynamic-programming ones, and `arellano.md:147` says so
  outright: "a prime denotes a next period value". No pattern can separate them at the
  occurrence level, so the check now decides per *file*. Three forms cannot be anything
  but a transpose: a prime on a closing delimiter (`(A+B)'`, `\end{bmatrix}'`), a prime
  juxtaposed with the factor that follows it (`x_t' R x_t`), and a prime on the repeat of
  the symbol before it (`CC'`, `U_t U_t'`). A lecture writing any of them uses the
  apostrophe as a transpose, so the rest of its apostrophes count; a lecture writing none
  of them does not, and none of its apostrophes count. Removed 242 occurrences across 13
  lectures — `atkeson_1991` 71 (Math 5.0 → 9.5, HIGH → LOW), `tsyrennikov_2013` 50,
  `arellano` 31, `repeat_mh` 25 — with 0 added and all eight canary transposes intact.
  **The first version of this gate covered only the bare-apostrophe branches**, so the
  same next-period-state class survived in the `^\prime` spelling: `navy_captain` scored
  6 on `\pi^{\prime}` and `z^{\prime}` in a file whose line 633 *defines* the prime as
  the posterior after one more draw, and whose `\top` and `^T` counts are both zero.
  `lprime` is now gated on the same flag and can also supply evidence for it. −8, and
  the 230 legitimate `^\prime` hits in eight other files are untouched because those
  files carry bare-apostrophe evidence.
  Not extended: a `^\prime` on a `}` as *evidence*. A brace before it is usually a
  subscript's closing brace rather than a transposed group, so `Q_{r}^\prime` — next
  period's Q in `mccall_q` — falsely switched that file's branches back on and added a
  hit. Measured, reverted, and left as a comment on `DELIM_PRIME`.
- **The three `qe-math-002` branches still double-count the same site.** `x_t' R x_t` is
  reported once by the `prime` branch for `x_t'` and again by `prime_vec` for `t'`.
  `check_math_010` solved the same problem by having its branches mask each other after
  each pass; `check_math_002` should do the same.

- **`qe-ref-001` treats a line-initial citation as sentence-initial.** The check runs per
  source line, so `^\s*\{cite\}` fires on a wrapped paragraph continuation. 167 citations
  are line-initial across 80 lectures; for 90 the previous line does not end a sentence.
  Not fixed, and deliberately: many of those 90 are *correct* findings reached by the wrong
  mechanism — `chang_ramsey.md:581` wraps mid-sentence after "the insights of Kydland and
  Prescott", so the citation genuinely wants `{cite:t}`. Repairing the line-break heuristic
  alone would delete them. The real fix is author-name detection, which is the upstream
  definition question in `contributions/issues/06-…`.

### The `qe-math-002` evidence pass disagreed with its own counting pass

`os_time_iter` scored 8 findings, all of them `u'` — the derivative of utility, composed
with a policy as `(u' \circ \sigma^*)`. Its whole Math score rested on them.

The per-file evidence gate asks whether a lecture uses the apostrophe as a transpose at all.
One of its signals is `)'` on a closing delimiter. `os_time_iter`'s only such site is
`(v^*)'(x)` at line 109 — which is precisely the shape `fn_paren` exists to exempt, because
a parenthesised *function name* applied to an argument is a derivative. The counting pass
applied that exemption; the evidence pass did not. So the gate opened on a site the counter
would have thrown away, and every ordinary derivative prime in the file was then counted.

The two passes now share the exemption. 16 occurrences removed — `os_time_iter` in both the
series that carry it — reach 66 → 64, nothing added, and all nine canary lectures unchanged.

The general lesson, which cost two other bugs today: **when a check has an evidence phase and
a counting phase, they have to agree about what the evidence is.** A signal the counter
rejects must not be allowed to unlock the counter.

### Four smaller fixes from the intro series, and one claim that did not reproduce

- **`qe-math-002` could not see `)^T`.** `supT` admitted only a bare capital or a braced
  `DECORATED` base, so `(h_1 \cdot B^T \vec\beta)^T \vec\mu` and
  `\big(z_t - \hat E z_t\big)^T` went uncounted. Adding `\)` adds exactly those two
  sites. `\}` was measured too and **stays out**: it would admit 64 summation limits of
  the form `\sum_{t=0}^{T}`.
- **`qe-code-003` compared an import name to a distribution name.** PEP 503 makes `-` and
  `_` equivalent, so `!pip install pandas-datareader` did not answer
  `import pandas_datareader`. Both sides are normalised now: 4 occurrences, reach 29 → 25,
  the others being `myst_nb` and `quantecon_book_networks`.
- **`monte` and `carlo` were missing from `PROPER_NOUNS`.** Five false positives — two
  headings and, unexpectedly, three `qe-fig-004` captions, because that rule shares
  `_is_proper`. A reminder that the noun list is load-bearing for more than one rule.
- **MyST `%` line comments were not masked.** `money_inflation` has a commented-out draft
  derivation at 443-447 whose LaTeX was read as narrative — that lecture's entire Math
  finding. Now typed `raw` outside code fences, so `%%time` in a cell is untouched.
  `qe-math-001` −2, `qe-writing-008` −1.

**One claim in the same report did not reproduce, and that is worth recording.** It said
`supT`'s `\^\{?T\}?` suffered the optional-brace backtracking hazard documented above for
`\prime`, making `(1+r)^{T+1}` look like `^T`. Measured against the corpus, rewriting it as
an explicit alternation changes **nothing** — 16 hits before and after — because the
following-factor lookahead already rejects `+`. The `)`-base half of that doubt was real and
is fixed; the backtracking half was not, and the reviewer's own predicted total (+7) was
also high, the true figure being +2. Filed doubts are evidence, not conclusions.

While in the lexer: `cell_meta` was never initialised before the main loop. It happened to
work, because the only read is inside `if in_code_fence:` and a fence open always assigns
it first, but it was one control-flow change away from a `NameError`. Initialised properly,
and the stray assignment that an earlier patch left in the HTML-comment branch — where it
meant nothing — is gone.

### `qe-writing-006` never looked at the first word of a heading

Sentence case allows the first word of a heading a capital, so `check_writing_006` skipped
`words[0]`. That also skipped the capital *inside* a hyphenated first word: `## Set-Up`,
`## Q-Learning`, `## Root-Finding in one dimension` all want a lowercase second part and
none was flagged. This is a **false negative**, which makes it rarer than the false
positives most of this file records, and more valuable.

A hyphenated first word is now judged on its parts after the first — but only where the
offending part is not itself a proper noun, which is what keeps `Non-Gorman heterogeneous
households` and `Black-Litterman starting point` correct. Eleven surnames that appear only
inside hyphenated compounds went into `PROPER_NOUNS` for the same reason: `_is_proper` can
clear a compound only when *every* part is listed, so `Modigliani-Miller` failed on
`miller`.

Net: **8 genuine findings added** (`Set-Up` ×3, `Q-Learning` ×4, `Root-Finding`), **2 false
positives cleared** (`Modigliani-Miller`, an unstable `Bray` feedback), and nothing else
moved. It took three passes to get there — the first flagged all 39 hyphenated first words
including every surname, the second cleared the listed surnames but still flagged
`Non-Gorman`, and only the third asked whether the offending *part* was a name.

### A reviewer disagreement worth recording, not resolving

Two reviewers reached opposite conclusions about exempting `<capitalised common noun>
<number>` from `qe-writing-004` — `Example 2`, `Step 3`, `Representation 3`. The first
measured the exemption at 71 removals and **rejected** it, because `var_dmd` writes
"Representation 3" capitalised eight times and lowercase eight times for the same three
headings, which is the inconsistency the rule exists to find. The second measured a broader
version at 339 → 260, read all 79 suppressed hits, and reported none as genuine.

Both are right about the data, and the data does not settle it. `var_dmd`'s capitalised uses
all refer to its own section headings `## Representation 1/2/3`; its lowercase uses are
generic prose. Whether a reference to a numbered section takes a capital — "see Chapter 4"
— is an editorial convention the style guide does not state. So this is a rule-definition
question of the same kind as `qe-ref-001`'s narrative citations, not a detector defect, and
it stays unfixed until the guide says which it wants.

### `qe-math-011` flagged the null space as a distribution

All 8 hits in `svd_intro` were `{\mathcal N}(X)`, the null space of a matrix, and line 129
says so outright: *"let ${\mathcal C}$ denote a column space, ${\mathcal N}$ denote a null
space, and ${\mathcal R}$ denote a row space"*. The `DIST_AFTER` gate accepted any `(` as a
parameter list, so an operator applied to a matrix looked like a law applied to parameters.

A declaration override was available — the mechanism `qe-math-002` uses — but the data
suggested something better. Splitting every hit in the corpus by argument shape is a clean
partition: all 8 comma-less arguments are `svd_intro`'s null space, and all 134 genuine
distribution sites carry a comma (`{\cal N}(0,I)`, `\mathcal N(\mu, \sigma^2)`). So a
parameter list now has to have more than one parameter. A name introduced by `\sim` needs no
parameters at all and is unaffected.

That generalises where a declaration would not: any lecture using `\mathcal N` for a null
space is now handled, whether or not it says so. 8 removed, reach 35 → 34, nothing added.

### `qe-code-002` counted other people's parameter names

`qe.LQ(Q, R, A, B, C, beta=β, T=T)` was reported as a spelled-out Greek variable. It is a
keyword argument of QuantEcon.py's `LQ`, and the author cannot rename it — they are already
passing `β`, having complied with the rule for their own variable. The same shape appears as
`qe.LQMarkov(..., beta=β)` and `qe.tauchen(rho=ρ, sigma=ν)`.

The reviewer's diagnosis of the *mechanism* was wrong, and checking it was what found the
real one. It blamed the imported-name exemption being switched off by its own `=` guard, but
in `lqcontrol` `beta` is never imported — `LQ` is. The exemption was not misfiring; it simply
did not apply, and no rule covered the case. Applying the reviewer's fix as described changed
nothing at all: 0 files, measured.

The exemption is therefore **callee-based**: a Greek name used as a keyword argument is
exempt when the enclosing callee is an imported name. A lecture's own `def f(alpha=0.5)` is
still its own naming choice and still counts. Removed 99 occurrences across 42 lectures,
reach 85 → 49, with `likelihood_ratio_process.md:541`'s real `beta = np.array(...)` intact.

The callee lookup is per line, so a keyword argument on a continuation line of a multi-line
call has no visible `(` and is not exempted — `dyn_stack` keeps 1 of its 4 hits for that
reason. That is the conservative direction (a retained false positive, not a lost finding),
and it is the fourth instance of the single-line/multi-line hazard recorded here.

### `qe-code-003` could not see the install cell it asks about

`_python_blocks` dropped every non-executing cell, on the reasoning that illustrative code
is not a dependency. But `!pip install jax` under `:tags: [skip-execution]` is the standard
idiom in the GPU lectures — the cell is skipped *because the build image already has the
package* — so the rule reported "no install cell" for the three lectures that use it
(`two_computation`, `ak_aiyagari`, `back_prop`).

Getting this right took two corrections, and both are worth recording because each was a
new false positive rather than a miss:

1. Including skipped cells made the rule then demand `hide-output` on them. A cell that
   never runs has no output to hide, so that requirement is now waived for
   `skip-execution` / `no-execute`.
2. Including *all* non-executing cells pulled in `:class: no-execute` blocks, and
   `getting_started` — the installation tutorial — uses those to show the reader how to
   install QuantEcon.py. The rule reported them as install cells "not near the top" of a
   585-line file. They are not this lecture's dependencies at all.

So the two spellings are now distinguished, because they mean different things:
`skip-execution` on a `{code-cell}` is *this lecture's* install, deferred; `no-execute` on a
`{code-block}` is example code for the reader. Only the first is ever an install cell.
Result: 3 occurrences removed, reach 32 → 29, nothing added, no other rule moved.

### `qe-code-002` was reading docstring prose as code

`check_code_002` called `_strip_py(l.raw)` **one line at a time**. The docstring regexes are
multi-line, so an *interior* line of a triple-quoted string carries no quote characters and
stripping it in isolation masks nothing — the English and LaTeX inside numpydoc prose was
being counted as spelled-out Greek variables. All 11 hits in `von_neumann_model` were of that
kind, in a lecture whose code already uses `α`, `β` and `γ` correctly; `samuelson` was flagged
for `Y_t = \alpha (1 + \beta) Y_{t-1}` written inside a docstring.

`check_code_003` in the same file had always stripped per cell. This now matches it, mapping
the stripped body back onto line numbers — safe because `_strip_py` preserves line structure,
which is itself a fix from an earlier pass. Removed 28 occurrences across 9 lectures, reach
89 → 85, and no other rule moved. `sargent_surico` went 89 → 87, keeping its real code hits
(`def lucas_filter(x, beta=0.95)`).

Worth noticing that this is the third distinct bug caused by looking at one line where the
construct spans several — the others being the display-math state machine and the
unbalanced-backtick masking. When a check consults `l.raw`, ask what the enclosing cell or
paragraph looks like first.

### An author's stated convention beats the heuristic

`var_dmd` scored 28 `qe-math-002` findings and line 75 says, in prose, *"here $'$ is part of
the name of the matrix $X'$ and does not indicate matrix transposition"*. Line 120 settles
it beyond argument — `\hat A = X' X^\top (X X^\top)^{-1}` uses the prime as a name and
`\top` as the transpose on one line — and the file uses `\top` 92 times.

The per-file evidence gate could not see this: `FOLLOWING_FACTOR` cannot tell a transposed
matrix in a product from a prime-*named* matrix in a product, so `X' X^+` at line 97 read as
evidence. A ratio test would have been the wrong instrument — `linear_algebra` has 114 prime
hits against a single `\top` and its primes really are violations.

So a *declaration* now overrides the heuristic. `PRIME_NOT_TRANSPOSE` looks for the author
saying it: "does not indicate … transpose", "part of the name", "denotes a next period".
Three lectures in the corpus declare one — `var_dmd`, `arellano` and `opt_tax_recur` — and
the last two were already handled by the evidence rule. Effect: `var_dmd` 28 → 0, and not
one other file moved.

### `qe-code-002` and imported names

A name the lecture *imports* is not a variable it chose to spell out: `from scipy.stats
import beta` binds a distribution, `from sympy import Lambda` binds a class, and renaming
either to `β`/`Λ` breaks the import and means something else. This was reported six separate
times before being fixed. Names bound by an `import` in the file are now exempt: **105
occurrences removed across 21 lectures**, reach 106 → 88. Sampled across `lln_clt`,
`bayes_intro`, `scipy`, `imp_sample` and `equalizing_difference` — every one a library call,
and several of those files already use `β`/`γ` correctly for their own variables.

The reviewer argued the exemption "cannot produce a false negative". At *name* scope that is
true; at *file* scope it is not, and the corpus contains exactly one counterexample:
`likelihood_ratio_process.md:541` writes `beta = np.array(...)` for a type-II error
probability, shadowing the import with a variable that genuinely should be `β`. The
exemption therefore does not apply on a line that *assigns* the name, which keeps that one
finding. 105 false positives out of, 1 true positive kept.

### Two fixes that were verified, then rejected

Both came from reviewer doubts, both reproduced exactly, and both were rejected because
they fail the both-directions test. Recording them so they are not re-proposed, and so a
narrower version has somewhere to start.

- **`qe-writing-004` on markdown link labels and quoted titles.** 60 of its 64 removals are
  correct — a label reproducing a lecture or book title is not the author's capitalisation.
  But 4 occurrences on 3 lines are genuine: `[Envelope Theorem](…/Envelope_theorem)` in
  `os.md:501`, `[Pareto Distribution]` in `mle.md:298`, `[Gershgorin Circle Theorem]` in
  `eigen_II.md:457`. In each the linked article's own title is lowercase — Wikipedia slugs
  preserve case, and the same set contains genuinely Title-Case slugs like
  `Golden_Rule_savings_rate` — and the corpus writes the same term lowercase elsewhere
  ("envelope theorem" 10×, including `os_time_iter.md:113` linking the *same URL* with a
  lowercase label). That is the rule's own *inconsistent capitalisation* bullet. A patch
  that exempts link labels must first distinguish a reproduced title from an author's own
  words, and the URL slug is the available signal.
- **`qe-writing-004` on "Example N" as a section reference.** The mechanics were clean —
  71 removed, 0 added, no offset or backtracking trap — but the premise is wrong. The
  claim is that `<capitalised common noun> <number>` names a labelled item and is never
  the rule's business. The corpus disagrees: `var_dmd.md` writes "Representation 3"
  capitalised 8 times and "representation 3" lowercase 8 times for the *same three
  headings*, three lines apart. That is precisely the inconsistency the rule exists to
  find, so the 71 removals include real findings.

### `qe-math-010`: a thin space hid the operator, and a calligraphic letter never was one

Two independent faults, both from reviewer doubts, both in the same check. Net **1397 → 1414
occurrences, reach unchanged at 118**: 25 added, 8 removed.

**`\!` and friends are thin spaces, not content.** `E_0\!\left\{` is the same construction
as `E_0\left\{`, and the check missed it because the `applied` pattern allowed only
whitespace between the letter and the bracket. `hansen_singleton_1982` and `_1983` write the
padded form throughout — 25 occurrences across the two — and in `hansen_singleton_1983` an
informal `E_0\{\cdot\}` two lines away *was* being caught, so the report contradicted
itself on the same page. The pattern now steps over runs of `\!`, `\,`, `\;`, `\:`, `\>`
and `\ ` on either side of an optional `\left`.

**`\mathcal{E|P|V}` had zero true positives corpus-wide.** A calligraphic letter is
conventionally a *set*, not an operator, and all 8 hits were set names. Two lectures say so
in their own text: `information_market_equilibrium` defines
`\mathcal{P} = \{ p(\mu_y) : y \in Y \}` outright, and `theil_1` writes
`f : S_1 \times \mathcal{E} \to S_1` for the shock space. The alternative is gone rather
than gated — there was nothing to keep.

### `qe-fig-008` asked a scatter plot to set its line width

`lw` governs the width of a line, so a `plot()` call that draws no line has nothing to set
it on. The check flagged them all the same, and the reviewer doubt named the shape exactly:
`plt.plot(fp_mult, fp_mult, 'o')` marking fixed points, `ax.plot(250, 120, "*", ...)`
marking a single point on a phase diagram. **1382 → 1258 occurrences, reach 216 → 202**:
124 removed, 0 added, and no removed hit draws a line.

The exemption reads the positional format string and clears the call only when it carries a
marker character and no line style. Three things about it were wrong first, and each is a
distinct trap:

- **Keying on quotes swallowed keywords.** Matching any quoted string exempted
  `ax.plot(x, y, color='C1')`, which draws a plain solid line. The format string is
  *positional* — a comma, then the quote, nothing in between — so the match has to be too.
- **`1`–`4` are markers, and admitting them exempted `'C1'`.** They are tri_down, tri_up,
  tri_left and tri_right. Nothing in the corpus uses them; what the corpus does have is
  `ax.plot(x, y, 'C1')`, a *colour* spec that still draws a solid line. Dropping the four
  digits from the marker class restored that one real finding — which is why the final total
  is 1258 rather than the 1257 the looser version measured.
- **A nested call's string argument is not a format string.** The call text is assembled
  across up to twelve source lines, so a search over the whole of it reaches inside nested
  calls: `ax[2].plot(plot_grid, policy_curve(policies['MH'], 'd1'), ...)` in
  `tsyrennikov_2013` would read `'d1'` as a thin-diamond marker. The assembler now records
  each character's nesting level and the search runs over the top-level arguments only.

Eleven cases pin the behaviour — `'o'`, `'ko'`, `'C1'`, `'C1o'`, `'o-'`, `'k--'`, no format
string, `lw=2`, `color='C1'`, and the nested-call form with and without a real format string
after it.

One measurement mistake here is worth recording, because it looked alarming and was
entirely an artifact of the query. Asked whether any exempted call still draws a line, a
first attempt scanned every line *outside the new hit set* and reported 256 — but a call
carrying `lw=` was never a hit under either version of the rule, so it cannot be a lost
finding. Every sample the query printed turned out to contain `lw=`. **A removal has to be
measured as a set difference between the two rules' hits, not as everything the new rule
does not flag.**

### `qe-writing-006` and eighteen author surnames

Same shape as the earlier heading fixes: a sentence-case check flagging eponyms. The
reviewers' doubts named them in ones and twos across several batches, and enumerating every
flagged heading word against the corpus turned up the rest — the check fires only on
headings, so the population is small enough to read in full.

Added to `PROPER_NOUNS`: `coleman`, `reffett`, `groves`, `clarke`, `singleton`, `jones`,
`manuelli`, `kiyotaki`, `wright`, `rosen`, `topel`, `metropolis`, `gibbs`, `hicks`,
`hicksian`, `pearce`, `stacchetti`, `newcomb`, `benford`, `breeden`, `chaudhuri`,
`mukerjee`, `greenberg`, `lanke`, `leysieffer`, `warner`, `wecker`, `shorrocks`, `hopfield`,
`riesz`, `engel`, `gumbel`. **787 → 768 occurrences, reach 143 → 132.**

`within` went to `STOP_SMALL`, not to the surname list. `Metropolis-within-Gibbs` needs
*every* part of the compound cleared, and "within" is a preposition in the same family as
the `with`, `by` and `from` already there — listing it as a proper noun to make one heading
pass would have been the wrong repair in the right place.

Two checks kept this honest. Every heading in the corpus using an ambiguous word —
`groves`, `singleton`, `metropolis`, `jones`, `clarke`, `wright`, `white` — was read before
the name went in, and all were eponyms except one: `python_by_example.md:39`, "The Task:
Plotting a White Noise Process". "White noise" is not a proper noun and that heading is a
real violation, so `white` was left out. And 7 of the 26 changed hits come back as *new*
hits with the surname dropped from the reason list — `'Original Wecker Method'
(Wecker, Method)` becomes `(Method)`, still a finding because `Method` should be lowercase.
The fix narrows the reason; it does not clear the heading.

### `qe-code-002` only ever saw a Greek name that stood completely alone

The largest single correction in this pass, and the one most often reported: five overlays
raised it independently, `hansen_richard_1987`'s at length. `GREEK_RE` ended in `(?![\w])`,
so only a Greek word that was a *whole* identifier counted. In this corpus a Greek name
almost never stands alone — it carries a subscript or a plural. `hansen_richard_1987` writes
`mu_m`, `mu_vec`, `mu_low`, `mu_unc`, `alphas`, `alphas_dynamic` and was reported clean on
all of them while the same file writes `σ_m`, `σ`, `βs`, `αs` and `δ, γ`; line 426 is
`mu_m = -0.5 * σ_m**2`, one Greek letter spelled out and the other in unicode inside a single
expression. `kalman_2.md:511` is the same thing in one line of arguments:
`mu_0=μ_sim_0, Sigma_0=Σ_sim_0`.

`GREEK_RE` now consumes an optional `s` or `_<suffix>`. **307 → 700 occurrences, reach
38 → 57**: 400 added across 32 lectures, 7 removed.

Consuming the suffix rather than merely allowing it is what makes the rest work: `m.end()`
becomes the end of the whole identifier, so the existing keyword-argument test sees `mu_0=`
where before it saw `mu` followed by `_0=`. Three exemptions had to come with it, and each
was measured:

- **The 7 removals are the fix working.** They are all `beta=β` on a *continuation* line —
  `qe.nnash(A, B1, …,` / `M2, beta=β)` in `markov_perf`, `LQ(econ.Q, …,` /
  `econ.C, N=econ.W, beta=econ.beta)` in `gorman_heterogeneous_households`. The rule already
  meant to exempt a library's own parameter name, but `_enclosing_callee` was given a single
  line, and a continuation line contains no callee. It is now given the whole cell and this
  line's offset into it.
- **A Greek word is also a distribution's name.** `sargent_surico` defines `beta_prior`
  returning `stats.beta(...)`, `gamma_prior` returning `stats.gamma(...)`, and `beta_np` /
  `gamma_np` returning `dist.Beta(...)` / `dist.Gamma(...)`. `γ_np` would be a
  mistranslation, not a fix. 24 such additions are gated on the cell actually calling a
  distribution of that name from a stats namespace, rather than on the name alone — and a
  blanket "Greek word used as a function name" exemption was rejected, because it would have
  cost `market_diffusion.md:159`'s `def mu(self, a)`, which is a real finding.
- **`chi2` is not `chi` with a subscript.** A trailing digit is excluded from the suffix, so
  scipy's chi-squared does not become a Greek variable.
- **The import-shadowing carve-out is for the bare name only.** `lln_clt`'s
  `beta_dist = beta(2, 2)` does not shadow the imported `beta`; it stores its result under a
  different name, and that name is a distribution's.

Twelve unit cases pin the behaviour, including the two that pull in opposite directions:
`def beta_prior(m, s): return stats.beta(m, s)` is exempt, `def sigma_star(x)` is not.

**Known limitation.** A lecture that imports `beta` or `gamma` from `scipy.stats` *and* uses
`beta_*` for its own discount factor would have that name exempted. Two occurrences changed
hands on this test, both correctly; the exposure is small and the direction is conservative.

### Three doubts from one `lecture-dp` batch, each measured before it was believed

All three came with a number attached, all three reproduced, and all three were narrower than
the obvious fix.

**`qe-fig-008` could not see a keyword bundle.** `lqcontrol` builds all four of its panels as
`p_args = {'lw': 2, 'alpha': 0.7}` and then `ax.plot(x, y, 'k-', **p_args)`. The width the
rule asks for *is* set, one cell-line away, and the lecture was reported 18 times for a
convention it follows. A `**name` splat is now exempt where the same cell binds `name` to a
dict literal or a `dict(...)` call that sets `lw` or `linewidth`. **1258 → 1198, reach
216 → 197**: 60 removed across `lqcontrol`, `lqramsey`, `money_inflation`,
`dovis_accounting_mf`, `robustness` and `python_advanced_features`; 0 added. Orthogonal to
the marker-only exemption above — the two together take the rule from 1382 to 1198.

**`R^T(s_{t+T}, \ldots, s_t)` is a function of T arguments, not a transpose.**
`smoothing_tax` says so in the two lines above the display — "the cumulative return earned
from … rolling over the proceeds each period thereafter" — and computes it with `np.cumprod`.
The signature that separates the two readings is a *top-level comma or conditioning bar*
inside the group: `A^T(B + C)` has neither and stays a transpose. **1599 → 1597**, touching
only the two byte-identical copies of that one file.

Two wider fixes for the same site were measured and rejected, and are recorded so they are
not re-proposed: dropping `(` from the `supT` lookahead (37 → 25 on the branch) and a
function-name-aware variant (37 → 31) both silence genuine transposes in
`calvo_machine_learn` — `\vec{\mu}^T (M - F) \vec{\mu}` among them.

**`qe-math-008` looked only inside one source line.** `_math_spans` yields one span per line,
so `mccall_model`'s `\sigma(w) := \mathbf{1}` with `\left\{` underneath presented the
indicator test with an empty string. `check_math_004` already looks one span ahead for
exactly this shape; this now matches it.

Reading the survivors then found two more false positives in a rule that only had seven hits,
so both were fixed in the same pass:

- `two_computation` writes `\mathbf{1}^{\text{work}}_t` — an indicator with a label, whose
  `_t` sits one group past the superscript. The test now steps over an optional superscript.
- `lln_clt` writes ``$X = \mathbf 1\{U < p\}$ where $\mathbf 1$ is the
  [indicator function](…)``. The first occurrence carries its argument and was already
  exempt; the second is the symbol being *defined*, and the sentence defining it says what it
  is. A nearby "indicator function" now takes the occurrence out of scope.

**7 → 3 occurrences, reach 7 → 3.** The three survivors are real: `blackwell_kihlstrom`'s
`\mathbf{1}\mathbf{1}^\top` outer product, and `discrete_dp`'s
`[\ldots] \mathbf{1}` in both copies.

Ten unit cases cover the three fixes, including the two canaries that must keep firing:
`A^T(B + C)`, and a bare unexplained `z \mathbf{1}`.

### Two doubts from the intro batch, and a line-width question referred rather than fixed

**A one-character placeholder is indistinguishable from an initial.** `_count_sentences`
substitutes a role or a markdown link with `"X"` before looking for sentence boundaries, and
the abbreviation guard two lines down then discards the following full stop as an initial. So
a paragraph whose first sentence ended in a link — `solow`'s *"… using
[scipy.optimize.minimize_scalar](url). We will use $-c^*(s)$ since …"* — counted as one
sentence and was reported clean. Two letters fix it. **442 → 448 occurrences, reach
173 → 175**: 7 added, and the one "removal" is the same paragraph in `need_for_speed` whose
count went from 2 to 3. All 7 read as genuine two-sentence paragraphs.

**`linestyle=''` says outright that the call draws no line.** Same reasoning as the
marker-only format string, stated by the keyword instead: 14 further `qe-fig-008` occurrences,
every one a `marker='o'` scatter. With the marker-only and keyword-bundle exemptions, the rule
now stands at **1184 occurrences over 195 lectures**, from 1382 over 216.

**And the part that is not a detector question at all.** `qe-fig-008` asks for `lw=2`; the
check only ever asked whether a width is set. Whether a value *other than* 2 is a violation
depends on something the rule's text does not say — whether a faint reference line or one of
fifty sample paths is in scope. Both readings were costed rather than guessed:
264 calls across 84 lectures set some other width, of which 152 also dash, grey or fade the
line and read as deliberate. That went to
`contributions/issues/07-fig-008-line-width-tolerance.md` as a rule-definition question, the
same treatment `qe-ref-001` got.

The numbers in it are **measured, not typed.** `qestyle_scan` now writes
`data/fig_line_widths.csv` — every explicit width, with each non-house value labelled by the
only mechanical signal for "this was deliberate" — and the gate holds both the appendix's
summary and the draft's tables to that file. 31 claims cross-checked. It was worth doing
immediately: a first hand-typed pass had the lecture count at 78 (a filename set collapses
the two series' copies of a shared lecture; the pipeline counts series-lecture pairs, so 84),
`lw=1` at 60 rather than 66, and the deliberate split at 101/130 rather than 119/112. **Every
one of those five numbers was wrong, and the gate caught all five on its first run.**

### `qe-fig-004` could not see where a MyST figure keeps its caption

The check read `:caption:`, and **not one** of the 144 `{figure}` and `{image}` directives in
this corpus uses it. A MyST figure's caption is the directive *body*:

```
```{figure} /_static/.../poverty_trap_1.png
:name: poverty_trap_1

Poverty Trap
```
```

The cause was one line in the lexer. `open_blocks[-1][4].append(raw)` sat inside the
`if in_code_fence:` branch, so a directive body was accumulated only when the directive was a
code cell — `doc.blocks` carried an empty body for every figure in the corpus. Accumulating
it for the other directives too changed **no other check's count**, measured across all 41.

`qe-fig-004` now takes the first paragraph after the option lines: **179 → 189 occurrences**,
10 added, 0 removed. Among them the three `networks` captions the lecture's own reviewer had
flagged by hand — `poverty_trap_1` and `poverty_trap_2` both read "Poverty Trap", which is
why `` {numref}`poverty_trap_1` `` and `` {numref}`poverty_trap_2` `` render
indistinguishably — and four `entropy` captions running to 13, 29 and 31 words.

Body captions are longer and more sentence-like than option captions, which exposed three
false positives in the Title-Case half of the check that had never had the chance to fire:

- **A sentence's first word is capitalised because it opens a sentence.** `entropy` 526 is two
  sentences over 31 words, and "Under" opened the second.
- **Exempt by position, not by spelling.** A first attempt exempted every *occurrence* of a
  word that opens a sentence somewhere, which let "Price of Gold" off in `french_rev`'s
  "Price Level and Price of Gold" — the caption's own first word is the same word.
- **The full stop has to survive an abbreviation.** "U.S. Treasury yields" is one sentence, so
  `Treasury` is a real finding. The existing `ABBREV` list and a single-letter test cover it.

And then the same trap that had just been fixed in `_count_sentences`, in a second place:
inline maths was replaced by a **one-character** placeholder, so the full stop after
`$g \geq 0$` looked like it followed an initial and stopped ending its sentence. Two letters.
That is twice now that a single-character stand-in has broken sentence detection — the lesson
is in the code at both sites.

Eight cases pin the behaviour, including the `:caption:` form that still has to work and the
legend after a second blank line that is not the caption.

### One more escaping trap: a bounded target is what keeps a generic role safe

Broadening `escape_roles` to any role name (for `{prf:theorem}`) had a failure that only
appeared in the build. `perm_income_cons`'s reviewer prose quotes inline maths *inside* a code
span — ``` `c_0 = (1-\beta) E_0 \sum_{t=0}^\infty \beta^j y_{t}` ``` — and `{t}` matched as
a role name whose target ran from that code span's closing backtick to the next backtick 90
characters later, swallowing a real `` {eq}`old12` `` on the way and emitting
`` {eq}` ``old12` `` into the page. Four build warnings, in four lectures.

A role's target is a *label*: `[^`\n\s$]{1,80}`. Bounding it that way makes the runaway
match impossible, and requiring at least two characters in the generic role name keeps
`$x_{it}$` out of reach as well. The regression is in the test suite as the real string.

**Build warnings: 6 → 0.** Bounding the target also caught the last two, `cross_product_trick`'s malformed `` {eq}`eq:Kalman102} `` in both series' copies: the stray `}` is not whitespace, so the label pattern matches it and the whole thing is rendered literally. That corpus defect is still real and still reported upstream — the report simply no longer asks Sphinx to resolve it.

### Three doubts that closed out `lecture-python.myst`, and three rejected alternatives

The batch that finished the largest series filed three, each with a before/after and each with
the *wider* version already measured and rejected. That is the shape a useful doubt has.

**`qe-math-010` matched the operator spellings case-sensitively**, so `\operatorname{cov}`,
`{\rm var}`, `\text{cov}` and `\mathrm{corr}` were all invisible, and `Cor` never saw
`\mathrm{Corr}`. **1414 → 1489, reach 118 → 124**: 75 added across 11 lectures, 0 removed.
Several sit on the same line as the correct form — `phillips_self_confirming` 180 writes
`\frac{\operatorname{cov}(U_t, y_t)}{\mathbb{V}[U_t]}` — which is the clearest evidence
there is. **`E` stays case-sensitive**, tested and rejected: `[Ee]` adds exactly two hits, both
`\mathrm{e}` for Euler's number in `solow`.

**`qe-fig-008` only ever looked at `.plot(`.** `semilogx`, `semilogy`, `loglog` and `step` draw
line charts too, and the module's own `PLOT_CALL` already counts them as figure-producing, so
the rule was inconsistent with its own neighbour. **1184 → 1194**, 10 added across 7 lectures,
0 removed — `arma`'s spectral density, `heavy_tails`'s two log-log tails, three `prob_dist`
CDF steps. **`axhline`/`axvline` tested and rejected at +172**: a reference line is
deliberately thin, which is the same judgment the marker-only exemption makes.

**`qe-ref-001` lost the participial lead to its own clause-end exemption.**
`Following {cite}`Lucas1978`, we suppose that …` opens with a participial phrase whose object
*is* the citation, so the author's name has to read as part of the sentence — and the comma
closing the phrase was cancelling the finding. **282 → 291**, 9 added across 8 lectures, 0
removed, every one of the form `Following {cite}`X`,`. The general version — dropping the
exemption for any governing preposition — was measured at **+165 across 86 files** and
rejected: most of those are source references like "on page 35 of `` {cite}`sargent2002big` ``",
which is exactly what `contributions/issues/06-ref-001-author-name-citations.md` refers
upstream rather than deciding. The participle is the case both readings of the rule agree on.

Two more from the same batch, both correctly *not* implemented. Adding `xarray` to `ANACONDA`
would clear the corpus's single `qe-code-003` hit (32 → 31) and cost the rule its whole
service, since `xarray` reaches that lecture only as a transitive dependency of `arviz` — the
one-word lecture-side fix is better. And `qe-math-010` cannot see LaTeX operators inside
matplotlib label strings (`rational_learning_re` writes a bare `$E_t$` in four of them), which
is a scope decision about what surface the maths rules cover, not a defect.

### The last three doubts, put through three adversarial lenses each

The final batch's three doubts were measured, then attacked: for each patch, one reader hunted
a false-positive class in the additions, one hunted a lost or double-reported finding, and one
checked whether the named mechanism was really the cause. Seven of the nine lenses reported.
**Every one of the three patches needed changing, and one was rejected outright** — which is
the strongest argument yet for the layer. A measurement pass alone would have landed all three.

#### `qe-math-010`: the operator juxtaposed, with no delimiter at all

The bare-letter branch required the operator letter to be *applied* to a delimiter. Three
shapes carry it without one: the `\big` family of openers, `E \sum` / `E_0 \prod`, and a
subscripted `E` juxtaposed with a subscripted symbol. **1489 → 1608 occurrences, reach
unchanged at 124**: 119 added, 0 removed, every one read.

Three things the lenses changed:

- **The doubt's numbers were a gate claim wearing a pattern claim's clothes.** Its two
  headline lines — `tax_smoothing_3:80`, `un_insure:34` — are not reachable by *any* pattern
  change: those files contain no `E[` anywhere, so the per-file `e_is_operator` gate switches
  the whole branch off. The doubt had silently widened the gate too, which is where its 33
  file-paths and 12-off-zero came from. Widening it measures +168 / −0 and moves reach
  124 → 136, and the 61 extra additions were read and are genuine — but it takes seven
  lectures off a clean 0 on this rule. **That is a scoring decision, not a detector decision,
  and it wants its own pass.** Recorded, not implemented.
- **`\bigr` is not an opener.** The proposed `\bigg?[lrm]?` matched `\bigr`, `\Bigm` and
  friends as readily as `\bigl`, while `NOT_A_PRODUCT_PRIME` two hundred lines up in the
  same file already carries exactly that curated distinction. Zero corpus instances either
  way, so the fix is measurement-neutral — but a file disagreeing with itself about which
  macros open a group is a defect waiting for its input. Now `\[bB]igg?l?`.
- **The safety argument was an observation dressed as a guard.** The comment justified the
  mandatory subscript with "a matrix `E` is not time-indexed", but the pattern accepts *any*
  subscript: `E_{ij} a_{kl}` matches. The 73-of-73 read is real evidence and every juxtaposed
  `E` in this corpus is genuinely time-indexed — but that is a fact about the corpus, and the
  comment now says so, with the instruction to restrict the subscript if it ever needs to be
  load-bearing. A unit case pins the accepting behaviour so the next reader sees it.

One lens found something the measurement pass had missed and it is now fixed: the operand
bound was `[A-Za-z]`, so a **Greek** operand stayed invisible beside a counted Latin one *on
the same line*. `cagan_rational_expectations:1223` writes
`a_{2t} = \mu_t - E_{t-1}\mu_t = \mu_t - E_{t-1}x_t` and was reported once of two. Admitting
a Greek macro as the operand adds those 12. That same-page self-contradiction is this
project's strongest evidence class, and it was being *created* by the patch meant to remove it.

#### `qe-code-002`: refuted as specified, adopted with three changes

The mechanism reproduced exactly — the lookbehind rejects a preceding `_`, so `mu_vec` was
caught and `target_mu` was not, and `hansen_richard_1987:658` is
`def mv_weights(mu_vec, Sigma, target_mu)`, contradicting itself inside one signature. But all
three lenses refused it as written.

- **The tail guard was a silent regression on the rule's own core case.** The patch ended in
  `(?![\w])`, and `\w` matches unicode letters, so `sigma_ε` — one Greek letter spelled out
  and the other not, in a single identifier — *stopped* matching. That mixed spelling is what
  the rule is for; `mu_m = -0.5 * σ_m**2` is the evidence this whole family of fixes was built
  on. Invisible in the diff (the corpus has no such token today), so it measured −0. Two of
  the guards were also mutually redundant and each individually dead. Now one guard,
  `(?![A-Za-z0-9])`, which still excludes `chi2`, and `sigma_ε` matches again.
- **A conceded false positive was a class the project had already built a gate for.**
  `fitting_distributions` went from clean to 1 hit on `'gamma': fit_gamma(price)` — scipy's
  **Gamma** distribution, sibling to `fit_normal` and `fit_lognormal`. It leaked because
  `DIST_CALL` is *cell*-scoped: the `def` sits in the cell that calls `scipy.stats.gamma` and
  the call site is 31 lines later in another cell, so the report exempted the definition and
  flagged the call of the same name. The gate is now **name**-scoped — a name a distribution
  cell `def`s is exempt wherever it is used. Making `DIST_CALL` file-scoped instead was
  measured and rejected: it costs 28 real findings.
- **`mu` is also the economics abbreviation for marginal utility.** `ifp_egm:556` is
  `def compute_mu_k(k)` whose docstring reads "compute marginal utility u'(σ(...))", eight
  lines under `u_prime = lambda c: c**(-γ)`. A cell binding `u_prime` or `marginal_utility`
  has said which `mu` it means, so a *suffixed* `mu` there is exempt — a bare `mu` still is
  not, and `robust_permanent_income:675`'s `mu = np.exp(log_mu)` is still a finding. This
  removes 4 pre-existing false positives as well as 12 new ones.

Final: **700 → 798 occurrences, reach 57 → 66**; 102 added, 4 removed, all four of the
removals verified as marginal-utility false positives in the two synced copies of `ifp_egm`.

And the doubt's own second guard — "skip identifiers the file `def`s" — is **rejected in every
form.** Blanket, it deletes the `market_diffusion:159` `def mu(self, a)` canary (8 removals),
which is the exemption this project already rejected once. Narrowed to mixed English/Greek
names it still deletes 7 findings; narrowed to distribution names, 4. Its cost is 45 surviving
additions of the `def compute_res_wage_given_beta(β)` shape, kept because the rule already
counts identical sites at HEAD. Do not re-propose it. Its `tv_beta` example is not a finding
either: `merging_of_opinions` imports `beta as beta_dist`, so the file-level import exemption
already excludes all three.

#### `qe-ref-001`: verified, then rejected

The shape is real and would be valuable: prose writes the author and year by hand and *then*
adds a plain `{cite}` for the same work, so the page prints
"Shavell and Weiss (1979) [Shavell and Weiss, 1979]" — the reference twice. Measured
291 → 330, +39 / −0. It is still rejected, on three counts, and the third is the one that
settles it.

- **The patch as specified is a no-op.** The replacement text compiles the new pattern and
  builds the de-duplication set, and then contains no loop over either. Applied verbatim it
  measures 291, +0, leaving an unused regex and an unused set. The lens had to reconstruct the
  missing branch from the prose to reproduce the number at all.
- **The confirmation checked the wrong half.** "37 of 39 machine-confirmed" was confirmed by
  finding a capitalised token from the line inside the cite key — which tests the *author*
  half of "author-year" and never the *year* half, and the year is the half the
  rendered-duplication argument rests on.
- **3 of the 39 have a year that does not match the cited entry, so the page does not print
  anything twice and the prescribed fix corrupts the sentence.**
  `smoothing_tax:87` reads "Secretary of Treasury Albert Gallatin (1807) `` {cite}`Gallatin` ``";
  the entry is `year = {1837}`, a collected volume whose title carries "November, 1807". So the
  page renders two *different* years, and "use `{cite:t}` alone" would drop the given name and
  misdate the report by thirty years. That line is the only `qe-ref-001` hit in either copy of
  that lecture, so 2 of the 10 "newly reached" lectures are reached solely by a false positive.
  `re_with_feedback:68` is the same shape — "Blanchard and Khan (1981)" against
  `year = 1980` and a different spelling of the surname.

Two further classes the measurement pass under-counted: the possessive — "Ryoo and Rosen's
(2004)" ×2, where `{cite:t}` cannot emit "'s" and the prescribed fix is ungrammatical — and
the given name, ~6 sites rather than the 1 disclosed. And the guard is not "a capitalised
author surname" but any capital-initial run of non-space characters, markup included:
`black_litterman:41` matches `**Black-Litterman** (1992)`, which is the *model's* name.

**The minimum change to adopt is a year match against the bibliography.** The first reading of
this was that the corpus is a sparse checkout of `lectures/*.md` with no `.bib` in it, so the
patch could not be verified here at any effort. **That was wrong, and it is worth recording as
a mistake rather than quietly fixing:** the `.bib` is not absent, it is merely not
*checked out*, and one command produces it —

```bash
git -C <corpus>/lecture-python-advanced.myst sparse-checkout add '/lectures/_static/*.bib'
```

Both disputed entries were then read directly and both false positives are confirmed:
`@incollection{Gallatin, year = {1837}, title = {Report on the Finances**, November, 1807}}`,
so "Gallatin (1807)" against a 1837 entry renders two different years; and
`@Article{Blanchard_Khan, author={Blanchard, … and Kahn, Charles M}, year=1980}`, so the
lecture's "Blanchard and Khan (1981)" differs in both the year and the spelling.

So the rule is **unblocked, not unverifiable**.

Two of the nine lenses died before reporting, both on this patch, and were re-run once the
bibliography was available. Re-running an adversarial lens against an *already rejected* patch
looked like it could only confirm the verdict — a refutation lens is prompted to refute, so it
cannot reverse one — and that reasoning was right about the verdict and wrong about the value.
The re-run resolved the year question completely and found two defects nobody had seen.

**The year question is closed: 36 of 39 match, 3 mismatch, 0 unresolved.** Every addition was
resolved against its own series' `quant-econ.bib`, and the mismatches are only the two shapes
already recorded (`smoothing_tax:87` in both series, `re_with_feedback:68`). Two further *name*
disagreements exist that a year gate cannot see: `BCG_incomplete_mkts:79` writes "Clemente"
against `author = {Bisin, Alberto and Gian Luca Clementi and Piero Gottardi}`, and
`hs_recursive_models:2197` writes "Hansen, Sargent, and Roberts (1991)" against
`sargent1991observable`, whose author order is `Sargent, Thomas and Hansen, Lars Peter and
Roberts, Will` — so with `bibtex_reference_style: author_year` the prescribed fix would rename
who comes first.

**The wrapped author list — the fix would print the name twice.** This is the finding that
matters, and no earlier pass saw it. Where the hand-written author phrase straddles a source
line break, the pattern matches only the tail surname. `ak2.md:29-30` reads

```
We'll present the version  that was   analyzed  in chapter 2 of Auerbach and
Kotlikoff (1987) {cite}`auerbach1987dynamic`.
```

so the finding quotes `'Kotlikoff (1987) {cite}'` and acting on it leaves *"in chapter 2 of
Auerbach and {cite:t}`auerbach1987dynamic`"*, which renders **"in chapter 2 of Auerbach and
Auerbach and Kotlikoff (1987)"** — the fix creating the duplication the rule exists to remove.
Three occurrences (`ak2` twice, `BCG_incomplete_mkts` once, where it leaves a dangling "used by
Bisin,"). The patch's own comment discloses the *mirror* of this case,
`black_litterman:545-546`, and calls it "measured and left out": the guard separates the two
only by which fragment lands on which line, and it admits the three whose message is wrong
while excluding the one that is accidentally right.

**The one mechanism the patch does spell out is dead code.** The `cited` set works on a
synthetic line but fires **0 times across all 348 lectures** — no `AUTHOR_YEAR_CITE` role
offset coincides with a `NARRATIVE_TRAIL` or `NARRATIVE_LEAD` one. An unexercised guard is
exactly the failure already recorded against this same rule, whose `see`/`include` exemption
was dead code until a later review caught it.

Counting every addition whose message is wrong or whose premise fails — 3 year/name mismatch,
3 wrapped, 2 possessive, 1 markup, 3 given-name-only — gives **12 of 39**, and 3 of the 10
newly-reached lectures are reached *only* by a defective finding. Interaction with the two
patches that landed the same day was checked by AST-level reference extraction and is empty:
`check_ref_001` touches only `NARRATIVE_LEAD` and `NARRATIVE_TRAIL`.

The second re-run lens confirmed the mechanism — this is not one of the wrong-mechanism doubts,
and adding only the missing branch reproduces 291 → 330 exactly — and then took the patch apart
on *shape*. **Four of the five guard elements the comment justifies are dead code.** Stripped in
turn over the whole corpus: the `(?<![A-Za-z0-9])` lookbehind, the `[a-z]?` year suffix, the
1600–2099 range and the `cited` set each change the count by **nothing**. Only the two `\s*`
are load-bearing. And the `[A-Z]` capital requirement — three sentences of the comment —
suppresses **exactly one site, a true positive**. Bare `\(\d{4}\)\s*\{cite\}`` measures 331;
a *correctly anchored* guard, `\b[A-Z][\w’'\-]*`, measures 329 **and** excludes the
`**Black-Litterman**` false positive that the proposed regex admits. **The proposed guard is
measurably worse than the guard it claims to be.**

Why: `[^\s(]*` is unbounded and unanchored, and the lookbehind blocks only `[A-Za-z0-9]`, so
the capital is taken from inside a token whenever punctuation or markup precedes it — a code
span, inline maths, `_emphasis_`, a closing paren, a URL fragment, even a preceding cite key.
`Equation (1979) {cite}` matches; the comment's own counter-example fails only in lowercase.

Two further defects the first pass did not see:

- **24 of 39 details would print a truncated author.** `[^\s(]*` cannot cross a space, so every
  multi-author site matches the final surname only: `'Roberts (1991)'` for "Hansen, Sargent,
  and Roberts (1991)", `'Gottardi (2018)'` for "Bisin, Clemente, and Gottardi (2018)". The
  wrapped-line class above is the same defect at its worst, not a separate one — a reviewer
  reads the sample as the finding.
- **The de-duplication is one-directional and breaks on reorder.** `NARRATIVE_TRAIL` assigns
  into `flagged` and never consults `cited`, so with the branches in the other order the
  synthetic case reports twice; and when both do fire, the surviving message is TRAIL's, so the
  comment's "the finding carries its own wording" fails in exactly the case the set exists for.
  `ak2.md:335` is one verb away from exercising it.

And one instance no branch catches at all: `muth_kalman.md:58` writes
``Milton Friedman {cite}`Friedman1956` (1956) posited that`` — the same duplication with the
year *after* the role.

**What would make it adoptable**, now five conditions rather than two:

1. Make it a **new rule**, not `qe-ref-001`. That check's docstring is role choice; this is
   rendered duplication. Folding it in mixes two definitions inside one count that
   `contributions/issues/06-…` quotes upstream, and silently decides 15 clause-end sites — 31
   of the 39 sit after a governing preposition, the class already measured at +165 and rejected.
2. Anchor the author guard (`\b[A-Z][\w’'\-]*`), which makes the lookbehind, the year range
   and `[a-z]?` unnecessary rather than dead, and drops the markup false positive.
3. Gate on the bibliography year — measured at **327 / reach 114, +36 / −0** with both bibs
   available. The check must **raise** on a missing bib, never skip: a clone without it resolves
   zero keys, and then a fail-closed gate reports no findings while a fail-open one reports all
   of them, both silently.
4. Skip a match whose author phrase continues before it, on the same line or the previous one,
   and quote the **whole** hand-written phrase in the detail.
5. Handle the possessive, the given name, the ampersand and the epigraph attribution — at nine
   or more sites `{cite:t}` alone cannot express the fix at all.

The underlying defect is real in 27 of the 39 sites and it is still the cleanest addition this
rule has left. **The runbook defect that fell out of this is fixed independently of it:**
`UPDATE.md` and the pass skill cloned the corpus without `_static/*.bib` in four places, so a
fresh clone by the documented procedure could not have verified any citation against the
bibliography. Both snapshots now carry it, because a rule that reads the bib must read it in
the previous period too or the trend row is meaningless.

### The build's warnings: 478 down to 23

Almost all of them were one thing. Reviewer prose and the detectors' own sample text quote
MyST roles from the corpus — `` {cite}`Hall1978` ``, `` {eq}`label` ``, `` {doc}`ifp_egm` ``
— and left bare, Sphinx tries to resolve every one against a book that does not contain the
cited work. 615 such roles across the 348 reports produced 478 of the build's warnings, and
the count grew with every batch of overlays (263 → 309 → 391 → 478), heading for roughly 700
at full coverage. At that level the build stops being a usable signal for a real problem.

`escape_roles()` in `qestyle_draft.py` now wraps them as literal spans at every point prose
reaches a report — mechanical sample text, reviewer finding detail, strengths, actions and
rule titles — and `qestyle_report.py` does the same for the titles it splices into the series
tables. Build warnings: **478 → 23**.

Two things had to be right, and neither is obvious:

- **The space padding is load-bearing.** ``` ``{doc}`x``` ``` closes on a run of three
  backticks and does not parse as a code span. `` `` {doc}`x` `` `` does. The hand-written
  prose in `intro.md` already used the padded form, which is the clue.
- **One dangling backtick was upstream, not a rendering problem.** `qe-ref-001`'s detail
  quoted `m.group(0)`, and that match *ends* in a backtick, so the sample carried a stray one
  that no escaping could close. Fixed in the detector.

Worth recording how the measurement went wrong twice, because the same trap is easy to fall
into again: the first count treated the escaped form as unescaped — the padding space defeats
a `` (?<!`) `` lookbehind — which made a working fix look like it had done nothing. The
warning count is the only ground truth here.

The 23 that remain are hand-written prose quoting examples in `intro.md`, `appendix.md` and
`cross_product_trick`'s malformed `eq:Kalman102}` target, plus three `mcmc` theorem labels
that genuinely do not exist in this book. That is the "few dozen standing" level the runbook
describes, and a new warning is now visible against it.

## How the 2026-05 pins were recovered

Everything above verifies a *detector*. This verifies a *pin* — which corpus commits a
period's published numbers were measured from — because the ledger's promise is that the
same commits in produce the same numbers out, and a period whose commits are not on record
cannot keep it.

`snapshot.json` names the commits of the pass that is running and is overwritten by the
next one, so when `lectures/data/snapshot_history.csv` was introduced the 2026-08 pins were
still on disk and 2026-05's were not. They were re-established from the corpus history and
written with `basis` = `recovered`. That value is a claim, and the file has exactly two
legal values precisely so that it cannot be used to smuggle in a guess — there is no third
value for "probably". This is what earning `recovered` meant.

| series | commit | committed (`%cI`) | lectures |
|---|---|---|---|
| `lecture-python-intro` | `576cd1776110adad5160e304b6f202d694b58a97` | 2026-05-29T14:07:01+10:00 | 50 |
| `lecture-python-programming` | `a2b929f15e703b6942e8b80a29011c51f234b1e0` | 2026-05-13T18:45:09+08:00 | 26 |
| `lecture-python.myst` | `2944402a4c4a3101e92e2824e10b0dc212265264` | 2026-05-29T14:27:37+10:00 | 110 |
| `lecture-python-advanced.myst` | `6320d7142b5b807ec33fd2063d509ce8dbb9a302` | 2026-05-28T15:28:02+10:00 | 62 |
| `lecture-dp` | `6a7bc1c467d7472e008607a3e12bb177dd2fb0c5` | 2026-05-28T17:28:17+10:00 | 52 |

300 lectures, matching `history.csv`'s `2026-05,TOTAL,300`.

**What was verified.** Re-measuring that set with the current code reproduces the recorded
2026-05 rows of `rule_reach_history.csv`: **35 rules of 35 exact, on both
`lectures_affected` and `total_occurrences`**, same rule set, same corpus size of 300. Not
one row moves. The lecture counts and committer dates in the table are read back from the
corpus, not transcribed.

**How.** Extract each candidate read-only — `git archive <commit> lectures/ | tar -x -C
<dir>`, which disturbs no clone and needs no checkout — then measure and diff:

```bash
python3 tools/qestyle_scan.py --corpus /tmp/corpus2605 --out /tmp/out2605 \
    --rules .corpus/action-style-guide/style_checker/rules \
    --period 2026-05 --append-history /tmp/out2605/rule_reach_history.csv --unpinned
# --unpinned because an archive extraction is not a checkout: without it the scan
# stops rather than write an empty pin, which is what a *pass* should do.
# then compare /tmp/out2605/rule_reach_history.csv against the 2026-05 rows of
# lectures/data/rule_reach_history.csv, on lectures_affected and total_occurrences
```

Note the `--out` and `--append-history` both under `/tmp`: re-measuring an old period must
not overwrite the current period's `violations.csv` or `snapshot.json`.

### What was rejected, and why a lecture count is not a check

A candidate matching **all five per-series lecture counts and the 300 total** was still
wrong, on two series, and 10 of the 35 reach rows mismatched. Three of those rows were kept
in the record — `qe-math-010` 107/1507 against 108/1538, `qe-math-012` 5/7 against 6/14,
`qe-code-003` 26/33 against 27/34 — and all three are reproduced exactly by one wrong
commit: `lecture-python.myst` at `5175665`, which carries 110 lectures like the pin and
lands on the same calendar day, nine hours earlier. Swapped into the otherwise correct set
it moves nine rules:

| rule | recorded | with `5175665` swapped in |
|---|---|---|
| `qe-math-010` | 107 / 1507 | 108 / 1538 |
| `qe-math-012` | 5 / 7 | 6 / 14 |
| `qe-code-003` | 26 / 33 | 27 / 34 |
| `qe-math-006` | 5 / 14 | 6 / 15 |
| `qe-writing-009` | 33 / 67 | 34 / 70 |
| `qe-code-002` | 54 / 558 | 54 / 555 |
| `qe-writing-001` | 165 / 417 | 165 / 419 |
| `qe-writing-004` | 94 / 296 | 94 / 298 |
| `qe-writing-008` | 233 / 7391 | 233 / 7404 |

The tenth mismatching row, `qe-math-003` at 41/334 against 40/333, is not one this swap
produces: it comes from the second wrong series, `lecture-python-intro`. Ten of that
series' eighteen same-count commits add exactly that row and no other, and three kept rows
cannot choose between them, so the second commit is not recoverable from the record. Its
contribution would also lift `qe-writing-001` and `qe-writing-008` slightly above the
figures tabulated here, which are the `lecture-python.myst` swap's alone. The lesson does
not depend on naming it.

**A lecture count is not a check.** Two commits a few hours apart, with the same number of
`lectures/*.md` and the same total across the corpus, differ by 31 occurrences on one rule
and double another. The reach fingerprint is the check.

### The recorded ambiguity, which the fingerprint does not resolve

`lecture-python.myst` also matches **35 of 35** at `30c5c431` — measured, not assumed. That
commit is 72 seconds earlier than `2944402a` and is not textually identical to it: the two
differ by 13 insertions and 11 deletions in `lectures/stats_examples.md`, a change no rule
happens to see. So on the evidence of the measurement alone the two are interchangeable,
and `2944402a` was chosen on evidence from outside it:

- it is the upstream repository's own `publish-2026may29` tag (`git tag --points-at`
  returns exactly that), so it is the commit the series itself declares it published; and
- its **consistency window** — the interval after the pin in which no lecture in any of the
  five series changed, i.e. how long the five-series snapshot stayed a coherent picture of
  the corpus — is 64,096 s (17.8 h), ending at `lecture-python-intro` `f0bd029` on
  2026-05-30T08:15:53+10:00. For `30c5c431` the window is **72 seconds**, closed by
  `2944402a` itself. A snapshot taken 72 seconds before its own series moves is a snapshot
  of nothing in particular.

This is worth stating plainly rather than burying: **the reach fingerprint verifies a set,
it does not uniquely identify one.** Five further `lecture-python-programming` commits, one
of them differing from the pin by 5 files and 57 insertions / 51 deletions of `.md` text,
also reproduce all 35 rows exactly. What the fingerprint establishes is that the recorded
set reproduces the recorded numbers — which is the whole of what the ledger promises — not
that no other set would. Where it ties, the tie is broken by the publish tag and the
window, and that reasoning belongs in the record next to the pin.

### `git log --until=<bare date>` must never establish a pin

Git resolves a bare date to that date **at the current local time of day**, so
`--until=2026-05-29` behaves as the explicit form below with the wall clock pasted in, and
the cutoff moves through the day with it — which is why two runs 26 minutes apart once
returned cutoffs 1,584 seconds apart. All three candidates below carry 110 lectures, and
which one comes back depends only on when the command is run:

| cutoff | returns | committed |
|---|---|---|
| `2026-05-29T06:00:00+10:00` | `5175665` | 2026-05-29T05:28:50+10:00 |
| `2026-05-29T14:27:00+10:00` | `30c5c431` | 2026-05-29T14:26:25+10:00 |
| `2026-05-29T16:44:00+10:00` | `2944402a` | 2026-05-29T14:27:37+10:00 |

A morning run yields the candidate that is wrong on nine reach rows; a run inside a
72-second window yields the one that is right on all 35 but is not the tagged commit; an
afternoon run yields the pin. Run bare at 16:44 local time, `git log -1 --until=2026-05-29`
returned `2944402a`; asked for the same date at its own midnight,
`--until=2026-05-29T00:00:00+10:00`, it returned a commit from **2026-04-28** — a month
earlier. Two spellings of one date, a month apart, neither of them wrong about anything
except what was asked.

The same trap at day resolution is what produced the discrepancy this record exists to
settle: in `lecture-dp`, `99a5a21` (2026-05-28T13:56:07+10:00) carries **50** lectures and
`6a7bc1c` (2026-05-28T17:28:17+10:00) carries **52** — the same calendar day, with
`rs_inventory_q.md` and `inventory_q.md` synced in at 17:27 and 17:28. A date cannot
separate them; a `%cI` timestamp can, which is why `committed` is stored to the second and
never to the day.

### The instrument is part of the record

Both periods' rows carry the same `checker` digest — a sha256 over `qestyle_scan.py`,
`qestyle_lex.py` and `qestyle_rules.py` read in that order, truncated to 12 hex characters;
`277dcd9edf30` at the time of the recovery run. That the two agree is the reason the
recovery is worth anything: the recovered 2026-05 rows are reproduced by *today's* code,
and comparing two periods at all assumes the same instrument measured both.

How much the instrument moves is not a hypothetical, and the check is cheap. Extracting
`tools/` at `f609536` and running it over the **unchanged** 2026-08 corpus — same five
pinned commits, same 348 lectures, only the code differing, six days of it:

| | `f609536` | today |
|---|---|---|
| rules reported | 37 | 35 |
| rules whose reach moved | — | **19 of 37** |
| `qe-code-002` | 106 / 579 | 66 / 798 |
| `qe-fig-008` | 239 / 1363 | 196 / 1194 |
| `qe-admon-001` | 4 / 4 | silent |
| `qe-fig-009` | 9 / 13 | silent |
| total occurrences | 19,249 | 19,101 (**−0.8 %**) |

Half the rules moved, two went silent, and the corpus-wide total moved less than one per
cent — so no aggregate sanity check would have noticed, and nothing outside this column
records which instrument produced a row. When two periods' digests differ, their trend row
compares two measurements rather than two corpora. `tools/qestyle_status.py` prints the
digest beside each period's pins, and names any period in `history.csv` that has none.


## The 2026-05 score row folds no judgment layer, and what that did to the trend

`history.csv` now carries `reviewed` per row and `history_mechanical.csv` the evidence-layer
twin ([#16](https://github.com/QuantEcon/compliance-lecture-style/issues/16)). The 2026-08
rows were written by `qestyle_report.py --history 2026-08` from `scores.csv` and a
`scores_mechanical.csv` drafted without `--reviews`. The 2026-05 rows predate both records
and were backfilled once, by hand, on this basis:

- **Every overlay in `reviews/` is stamped with a 2026-08 pin** — 348 of 348 carry a
  `source.commit` equal to that series' 2026-08 commit in `snapshot_history.csv`; none
  carries a 2026-05 commit.
- **The 2026-05 TOTAL row never moved while the overlays landed.** Across every commit of
  `history.csv` it took two values, both before any overlay existed and differing only by
  detector fixes (`bf8e14e` → `e173e1f`: Figures 6.3 → 6.4, HIGH 104 → 102). The 2026-08
  TOTAL row took 25, walking from `8.3 / 98 HIGH` to `7.7 / 197 HIGH` as overlays were folded
  in. A row that folds no overlay is an evidence-layer row, so its `reviewed` is 0 and its
  `history_mechanical.csv` twin is itself.
- **The mechanical draft reproduces the published one exactly when the overlays are added
  back.** Drafting the pinned 2026-08 corpus into a scratch root *with* `--reviews reviews`
  and scoring it gives a `scores.csv` byte-identical to the committed one; the same command
  without `--reviews` is what `scores_mechanical.csv` is. Measured 2026-09-01 at `d3a5956`.

The result, corpus TOTAL:

| basis | 2026-05 | 2026-08 | movement |
|---|---|---|---|
| published (`history.csv`, `reviewed` 0 → 348) | 8.2 · Writing 6.6 · HIGH 102 | 7.7 · Writing 4.6 · HIGH 197 | down |
| evidence layer (`history_mechanical.csv`) | 8.2 · Writing 6.6 · HIGH 102 | 8.4 · Writing 7.1 · HIGH 85 | **up** |

Per series, like for like, Writing was flat or up everywhere (intro 7.5 → 7.7, programming
5.7 → 5.7, python.myst 5.9 → 7.0, advanced 7.3 → 7.4, dp 7.0 → 7.0) where the published
columns had it falling by 1.6 to 2.7 points. The sign of the headline was the coverage.

## Re-measure at checker `6b5150d246fa` (2026-09-01)

The scan-side bundle ([#24](https://github.com/QuantEcon/compliance-lecture-style/issues/24):
`git_snapshot` stops on an unresolved clone, `--period`/`--append-history` required, per-period
blob tables, deterministic tie order in the reach tables) moved the checker digest from
`aef064f3b260`, so both periods were re-measured with it:

- **2026-08**, from `.corpus/` at the pins: `violations.csv`, `lecture_blobs.csv`,
  `snapshot.json` and every per-lecture report byte-identical; `rule_reach.csv` and the
  2026-08 rows of `rule_reach_history.csv` value-identical (tied rows reordered, once, into
  the stable order the writer now uses). `blobs/2026-08.csv` equals `lecture_blobs.csv`.
- **2026-05**, from `snapshot_history.csv`'s pins as worktrees under `.corpus/.prev-2026-05/`
  (sparse: `lectures/*.md` and `_static/*.bib`; `lecture-python-programming` has no `.bib` at
  either pin): the 2026-05 rows of `rule_reach_history.csv` value-identical, **35 of 35 on
  both columns**; `snapshot_history.csv` moved on `checker` only, `basis` stayed `recovered`.
  `blobs/2026-05.csv` written for the first time — 300 rows, per-series counts equal to the
  pins — and the churn it gives against `blobs/2026-08.csv` is exactly the record's:
  186 unchanged, 114 edited, 48 new, 0 removed.

## Reproducing this

```bash
cd tools
python3 - <<'PY'
import sys, glob; sys.path.insert(0, '.')
from qestyle_lex import lex
from qestyle_rules import CHECKS
rule = 'qe-fig-003'
for f in glob.glob('/path/to/quantecon/lecture-python.myst/lectures/*.md'):
    for h in CHECKS[rule](lex(f, 'lecture-python.myst')):
        print(f"{f}:{h.line}: {h.detail}")
PY
```

Then open each cited line and judge it against
`action-style-guide/style_checker/rules/`. A rule is only as good as the sample someone
actually read.

## Costed follow-ups

Measured changes that were deliberately **not** landed, and one stale bullet, brought across
from the two session files that recorded them — `.claude/RESUME.md` and
`.claude/pending-patches.json`, both deleted once this section existed. The verdicts those
files carried are in *The last three doubts* above; what is here is only the part that was
costed and left for a later pass. None of it needs measuring again from nothing — it needs
deciding.

### 1. Widening `qe-math-010`'s per-file `e_is_operator` gate

The landed patch changed the *pattern* only. The gate that switches the whole bare-letter
branch off in a file with no `E[` anywhere is unchanged, and it is what keeps
`tax_smoothing_1` (70, 203, 354), `tax_smoothing_2` (122), `tax_smoothing_3` (80) and
`un_insure` (34) at zero on this rule. Feeding the `\big`-family and big-operator shapes into
the gate as evidence was measured against the patch **as first filed** (1489 → 1596, before
the Greek-operand correction the lenses added, so these totals do not compose with the 1608
that landed):

| Variant | Occurrences | Added / removed | File-paths | Reach |
|---|---|---|---|---|
| gate widened to A+B evidence | 1489 → 1601 | +112 / −0 | 30 | 124 → 136 |
| gate widened, with branch C | 1489 → 1657 | +168 / −0 | 33 (12 off zero) | 124 → 136 |

The 61 additions the widening contributes were read individually and none is a false positive
(`perm_income_cons:94`, `markov_jump_lq:94`, `supply_demand_var:112`, `tax_smoothing_1:354`).
The reason it was held back is not doubt about the findings: it takes seven `lecture-dp` and
advanced lectures off a clean 0 and so moves category scores. **That is a scoring decision,
not a detector one, and it wants its own pass** — and, being a scoring decision, it should land
in the same pass as the history row that explains the step.

**Unresolved, and worth an hour before anyone quotes a number.** The gate pattern is a
hand-copied duplicate of `applied` rather than `applied` itself, so the gate and the branch it
guards can disagree. The two session files disagree about what simply reusing `applied` costs:
`pending-patches.json` recorded **+1**, one further file whose gate flips on `E_0\!\left\{`,
attributing it to the gate copy lacking the `THIN` steps; `RESUME.md` recorded **+27
occurrences and reach 124 → 129**, attributing it to `applied` also accepting `(`. They were
written in the same session and neither measurement script survives the container. Re-measure;
do not cite either figure.

### 2. What `qe-math-010` still does not count, by construction

Both were measured, judged genuine, and left out of the landed patch on purpose:

- **Dropping the mandatory subscript on `E`** adds **39** matches — `Eq_a` and `Ex_a`
  (`hansen_jagannathan_1991:340`), `Er_v^*` (:602), `Ev_t v_t'` (`hs_recursive_models:1429`),
  `E w_{st}^2 = .5` (`supply_demand_var:146`). Spot-checked in context they look genuine, but
  39 unread additions do not belong in a patch justified by a read of every one. It is a
  separate doubt, and it is the one that would test the "a matrix `E` is not time-indexed"
  argument, since without the subscript that argument is gone.
- **Branch C takes a single Latin letter as the operand**, which is the shape the doubt filed,
  so a macro operand is still invisible: `E_t\mu_{t+j}` (`cagan_rational_expectations:172`).
  Branch B covers `\sum` and `\prod`, not `\int`.

### 3. The `qe-ref-001` author-year duplication, as a new rule

Costed and adjudicated in full above; not repeated here. Two things to know before picking it
up: the write-up in *The last three doubts* lists **five** adoption conditions and is the
current version — the session brief recorded four, missing the possessive / given-name /
ampersand / epigraph class, which is the one where `{cite:t}` alone cannot express the fix at
all. And the bibliography is available (`sparse-checkout add '/lectures/_static/*.bib'`), so
the year gate — 327 / reach 114, +36 / −0 — is measurable now; it is unblocked, not
unverifiable.

The pattern as filed was

```python
AUTHOR_YEAR_CITE = re.compile(
    r"(?<![A-Za-z0-9])[A-Z][^\s(]*\s*\((?:1[6-9]|20)\d\d[a-z]?\)\s*\{cite\}`")
```

recorded so nobody rebuilds it from the prose — but note that everything in it except the two
`\s*` measures no change, and the analysis above replaces its author guard with an anchored
`\b[A-Z][\w’'\-]*`, which measures 329 against its 331 and drops the `**Black-Litterman**`
false positive it admits. Start from the conditions, not from this line.

### 4. The `qe-math-010` bullet under *Known limitations* is now partly stale

It reads "It counts `E[…]`, `E_t(…)`, `E\{…\}` but not `E_0 \sum` or `E \tilde\theta_t^2`".
The first half stopped being true when the `\big`-family, big-operator and juxtaposition
branches landed: `E_0 \sum` is counted wherever the file's gate is on. What survives is the
second sentence — the *evidence gate*, with those `tax_smoothing` lines as its live instances,
and `E \tilde\theta_t^2` as a macro operand branch C does not take (item 2). Rewrite it when
item 1 is decided; they are the same decision seen from two sides.
