## Summary

action-style-guide is built around **per-lecture review** triggered by `@qe-style-checker lecture_name`. It works well for that use case — author commits a lecture, action flags + fixes issues, PR ready.

A different use case surfaced during the [May 2026 lecture audit](https://github.com/QuantEcon/audit.2026-05.style-guide): **bulk / cross-series synthesis**. The audit produced:

- Per-lecture scores (0–10) per category
- Series-level rollups: average scores, priority distribution, top systemic issues, lecture ranking
- Cross-series synthesis: which rules are most violated overall, which lectures are highest-priority across all series, what the remediation order should be

The audit was done by orchestrating subagents against the existing rules under a [scoring rubric / report template spec](https://quantecon.github.io/audit.2026-05.style-guide/spec.html). It works, but it's an ad-hoc framework outside any official tool.

**The question:** does this bulk-audit / synthesis capability belong inside action-style-guide, alongside a sibling tool, or out of scope?

## What the bulk capability adds

The per-lecture review answers: *"What rules does this one file violate?"*

The bulk audit answers:

- *"Which lectures across the entire series should we prioritise fixing first?"* (scoring + ranking)
- *"What patterns are systemic across the corpus?"* (cross-cutting rule frequency)
- *"Where should we invest deterministic-check development effort?"* (rule × violation-count data)
- *"Has the corpus improved between audit N and audit N+1?"* (regression-style measurement)

These are management / triage views, distinct from the author-facing PR feedback action-style-guide provides today.

## What it would look like as a feature

A sketch of the API surface:

```bash
# Single-lecture review (existing)
qestyle lecture.md --categories writing,math

# New: series-level audit
qestyle audit ./lectures \
  --categories writing,math \
  --output ./audit-output \
  --report markdown
```

Output:

```
audit-output/
├── spec.md                (copy of spec used)
├── index.md               (series rollup: averages, top issues, ranking)
├── lecture-name-1.md      (per-lecture report)
├── lecture-name-2.md
└── ...
```

For cross-series synthesis, a second pass aggregates multiple `audit-output/` folders into a top-level report.

This builds on existing infrastructure:

- Same rule definitions (`rules/*.md`)
- Same `StyleReviewer` engine
- New output formatter on top of existing violation data
- Phase 6.3 (batch processing) already in the roadmap is adjacent

## Design options

### Option A — Inside action-style-guide as `qestyle audit`

- Reuses existing `reviewer.py`, rule files, fix detection
- Shares maintenance with the per-lecture review
- Phase 6.3 in the roadmap (batch processing) is the natural integration point
- **Risk:** scope creep; the LLM-call cost for 299 lectures × 49 rules is non-trivial ($24–116 per full audit using current per-rule architecture)

### Option B — Sibling tool that consumes action-style-guide's rule definitions

- Lives in its own repo (`QuantEcon/lecture-style-audits`?)
- Pulls rule definitions from `action-style-guide` as a versioned dependency
- Independent release cadence
- **Risk:** rule definitions become a shared interface — coordination overhead

### Option C — Out of scope for action-style-guide entirely

- Bulk audits remain an ad-hoc orchestration exercise (as the May 2026 audit was)
- Each audit produces its own `audit.YYYY-MM.{topic}` repo
- **Risk:** every audit reinvents the orchestration; calibration drift between subagents is hard to mitigate without shared infrastructure

Since this issue was filed, the second half of that pattern has been proposed. QuantEcon's
repository-naming standard QEP-3 ([open PR](https://github.com/QuantEcon/qeps/pull/7), not
yet accepted) registers a `compliance-{domain}` type for the standing record a repeated
audit turns into, on the rule that the audit is the event and the compliance repo is the
ledger. The May 2026 audit is its first instance: the dated repo keeps its name and is
archived, and the findings now live in `compliance-lecture-style`, re-measured in place per
pass. That settles where the *output* lives. It says nothing about where the *tooling*
should live, which is what this issue asks.

## Cost considerations

A full audit of 299 lectures × ~16 mechanical rules (per the Phase 4.3-extended scope from [#19 — Phase 4.3 acceleration](https://github.com/QuantEcon/action-style-guide/issues/19)) running through deterministic checks would be cents. Subjective/style rules running through Claude at current per-rule architecture would be **$24–116** depending on average lecture length. Sampling strategies (audit a random 20 % per quarter, full audit annually) make this manageable.

Bulk-audit mode + Phase 4.3 together would dramatically lower the cost of regular audits, making "audit every release" feasible.

## What's being asked

1. Does the team see bulk audit / cross-series synthesis as part of action-style-guide's scope?
2. If yes — option A (in-tree), option B (sibling), or something else?
3. If no — is the ad-hoc-per-audit pattern (one `audit.YYYY-MM.{topic}` repo per audit) acceptable, or is there a better orchestration target?
4. Is `qestyle audit ./lectures` the right API surface, or does the team prefer something different (e.g., a separate `qestyle-audit` binary, GitHub Action mode, scheduled workflow)?

## References

- **May 2026 audit output:** https://github.com/QuantEcon/audit.2026-05.style-guide
- **Scoring rubric, as maintained since:** https://quantecon.github.io/compliance-lecture-style/spec.html
- **Repository types for audits and standing records (QEP-3, open PR):** https://github.com/QuantEcon/qeps/pull/7
- **Existing batch-processing plan:** [`docs/developer/roadmap.md` Phase 6.3](https://github.com/QuantEcon/action-style-guide/blob/main/docs/developer/roadmap.md)
