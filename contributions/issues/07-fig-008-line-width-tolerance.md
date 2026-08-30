# `qe-fig-008`: does "use `lw=2`" mean every line, or the primary lines?

**Repo:** `action-style-guide` · **Rule:** `qe-fig-008` (line charts should use `lw=2`)
**Status:** a rule-definition question, not a bug report. Measured against the 348-lecture
corpus at the 2026-08 snapshot.

## The question

`qe-fig-008` asks line charts to use `lw=2`. Our checker answers the narrow, unambiguous
question — *is a line width set at all?* — and reports a `plot()` call that sets none. It does
not check the value, because the rule's scope on that point is genuinely unclear to us, and
guessing would either flood the report or hide real drift.

Two readings, both defensible:

1. **Every line.** `lw=2` is the house width; anything else is drift and should be flagged.
2. **The primary lines.** `lw=2` is the width for the data being discussed; a reference line,
   a grid of faint sample paths, or a deliberately emphasised line may differ.

## What the corpus does

Counting only `plot()` calls that set a width explicitly. These figures are measured, not
typed: [`tools/qestyle_scan.py`](https://github.com/QuantEcon/compliance-lecture-style/blob/main/tools/qestyle_scan.py)
writes them to [`lectures/data/fig_line_widths.csv`](https://github.com/QuantEcon/compliance-lecture-style/blob/main/lectures/data/fig_line_widths.csv) and the
consistency gate holds this table to that file, so they cannot drift when the checker's
exemptions move.

| | calls |
|---|---:|
| `lw=2` | 1,011 |
| some other value | 264 |

The 264 spread across **84 lectures** and twenty-one distinct values — `lw=1` ×66, `1.5` ×48,
`0.8` ×42, `0.5` ×27, `2.2` ×13, `1.2` ×11, `2.5` ×11, `0.7` ×6, `1.3` ×6, `1.8` ×6,
`1.6` ×5, `3` ×5, `0.75` ×4, `0.4` ×3, `1.4` ×3, `0.9` ×2, `15` ×2, `0.25` ×1, `0.6` ×1,
`2.4` ×1, `4` ×1.

Splitting them by whether the call looks deliberate — below the house width *and* also
dashing, greying or fading the line:

| | calls |
|---|---:|
| below 2 and carrying a de-emphasis signal | 119 |
| above 2 (emphasis) | 33 |
| below 2 with no such signal | 112 |

So on reading 1 the rule gains **264 occurrences across 84 lectures**, which would put it
among the widest-reaching rules in the corpus. On reading 2 roughly **152** of those are
deliberate and the remaining **112** are the finding — but "deliberate" there is our
heuristic, not the rule's, which is the whole point of asking.

Concrete examples of the two shapes:

- Deliberate: `ax.plot(range(N), np.zeros(N), 'k--', lw=0.5)` (`heavy_tails.md:1001`) — a
  zero reference line. `ax.plot(t_grid, pth, lw=0.7, alpha=0.55, color='C0')`
  (`market_diffusion.md:610`) — one of many sample paths.
- Drift: `ax.plot(t_seq, π_seq, label=r'$\pi_t$', lw=1.5)` (`cagan_adaptive.md:715`) — the
  lecture's main series, at 1.5 for no stated reason, in a file whose other figures use 2.

## What we would like the rule to say

Either is workable for us; the value is in it being written down.

- If **every line**, say so and we will check the value. The report gains 264 occurrences
  across 84 lectures, which is a real but one-off cleanup.
- If **primary lines**, the rule needs a sentence naming what makes a line secondary —
  "reference lines, faint sample paths and annotations may use a lighter width" would be
  enough to make it checkable, and we would gate on exactly that.

## Two things we did fix

Independent of the above, and noted only so the numbers in the report reconcile. Both are
checker bugs on our side, not rule questions.

A call can set the width through a keyword bundle — `p_args = {'lw': 2, 'alpha': 0.7}` then
`ax.plot(x, y, 'k-', **p_args)`. `lqcontrol` builds all four of its panels this way and we
were reporting it 18 times for a convention it follows. Our checker now resolves a `**name`
splat against a dict bound in the same cell: 60 occurrences across 6 lectures, no additions.

And a call that says outright that it draws no line — `linestyle=''`, `ls='none'` — has no
width to set. 14 further occurrences, all of them `marker='o'` scatters.

With those and a marker-only-format-string exemption, `qe-fig-008` moved from 1,382
occurrences over 216 lectures to 1,184 over 195. The value question above is the only part
still open.
