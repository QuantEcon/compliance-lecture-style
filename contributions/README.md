# Contributions to action-style-guide

Feedback this ledger has fed back to [QuantEcon/action-style-guide](https://github.com/QuantEcon/action-style-guide) and the [QuantEcon style guide](https://github.com/QuantEcon/QuantEcon.manual/tree/main/manual/styleguide). This folder is the source material behind the four issues opened from the May 2026 audit, plus three drafts from the 2026-08 pass that are not yet filed; the reader-facing summary is the [Feedback appendix](../lectures/appendix.md) in the report.

## Issues posted

All four are open on `action-style-guide`. The files here are the bodies, and are now ahead of the live issues — see [Status & next steps](#status--next-steps).

| Issue | Title | Body | Type |
|-------|-------|------|------|
| [#18](https://github.com/QuantEcon/action-style-guide/issues/18) | Proposal: 7 new style rules surfaced by lecture audit | [`issues/01-new-style-rules.md`](issues/01-new-style-rules.md) | Concrete proposal |
| [#19](https://github.com/QuantEcon/action-style-guide/issues/19) | Phase 4.3 acceleration: 41 of 49 rules are mechanically checkable + corpus test data | [`issues/02-phase-4-3-deterministic-checks.md`](issues/02-phase-4-3-deterministic-checks.md) | Extension of existing plan |
| [#20](https://github.com/QuantEcon/action-style-guide/issues/20) | Discussion: bulk audit / cross-series synthesis mode — where should it live? | [`issues/03-bulk-audit-mode.md`](issues/03-bulk-audit-mode.md) | Design question |
| [#21](https://github.com/QuantEcon/action-style-guide/issues/21) | Offer: labelled lecture corpus with per-rule violation counts as test fixtures | [`issues/04-corpus-offer.md`](issues/04-corpus-offer.md) | Resource offer |
| *(not yet posted)* | Proposal: rule-definition format changes so the registry determines its own counts | [`issues/05-rule-format-for-checkability.md`](issues/05-rule-format-for-checkability.md) | Concrete proposal |
| *(not yet posted)* | Question: what `qe-ref-001` means by a narrative citation — 299 author-name sites are undetermined under the current text | [`issues/06-ref-001-author-name-citations.md`](issues/06-ref-001-author-name-citations.md) | Rule-definition question |
| *(not yet posted)* | Question: does `qe-fig-008`'s `lw=2` mean every line, or the primary lines — 264 calls in 78 lectures set some other width | [`issues/07-fig-008-line-width-tolerance.md`](issues/07-fig-008-line-width-tolerance.md) | Rule-definition question |

### Not yet posted

`issues/05-rule-format-for-checkability.md`, `issues/06-ref-001-author-name-citations.md`
and `issues/07-fig-008-line-width-tolerance.md` all came out of the 2026-08 pass and have
**no issue number yet** — they need filing against whichever repo ends up owning the rule registry
(`action-style-guide` today, the consolidated `QuantEcon/style-guide` under the current
program direction).

`05` is the one contribution here that is about the *format* of the rule
definitions rather than their content: 144 under-specification gaps across 42 of the
in-scope rules, measured by auditing the rule files against a working implementation of 41
of them. The single strongest datum is that `qe-fig-003` — the only rule in the registry
carrying an explicit exemption clause — is also the only figure rule with zero false
positives.

`06` and `07` are the two places where our checker deliberately answers a *narrower* question
than the rule asks, because the rule's text does not settle the wider one — narrative
citations in the first case, line widths other than 2 in the second. Both carry the cost of
each reading, so whoever answers can see what they are choosing between.

## Rule entry drafts

Each file under [`rule-drafts/`](rule-drafts/) holds one proposed rule in action-style-guide's rules-file format (Type / Title / Description / Check for / Examples), ready to append to `style_checker/rules/<category>-rules.md` once the team accepts it. **Not yet submitted as a PR** — pending discussion on issue [#18](https://github.com/QuantEcon/action-style-guide/issues/18).

| Proposed ID | Category | File | Evidence |
|-------------|----------|------|----------|
| `qe-writing-009` | writing | [`rule-drafts/qe-writing-009-IID.md`](rule-drafts/qe-writing-009-IID.md) | Measured: 30 / 348 lectures, 61 occurrences |
| `qe-math-010` | math | [`rule-drafts/qe-math-010-blackboard-PEV.md`](rule-drafts/qe-math-010-blackboard-PEV.md) | Measured: **124 / 348**, 1,608 occurrences — strongest of the seven |
| `qe-math-011` | math | [`rule-drafts/qe-math-011-distribution-naming.md`](rule-drafts/qe-math-011-distribution-naming.md) | Measured: 34 / 348, 134 occurrences |
| `qe-math-012` | math | [`rule-drafts/qe-math-012-multiplication.md`](rule-drafts/qe-math-012-multiplication.md) | Measured: 4 / 348, 6 occurrences — narrower than first estimated |
| `qe-math-013` | math | [`rule-drafts/qe-math-013-equation-refs.md`](rule-drafts/qe-math-013-equation-refs.md) | Measured: 6 / 348, 6 occurrences — narrower than first estimated |
| `qe-math-014` | math | [`rule-drafts/qe-math-014-events-vs-sets.md`](rule-drafts/qe-math-014-events-vs-sets.md) | Judgment-only — no mechanical check possible |
| `qe-math-015` | math | [`rule-drafts/qe-math-015-density-CDF-case.md`](rule-drafts/qe-math-015-density-CDF-case.md) | Judgment-only — no mechanical check possible |

Each rule-draft has two sections: the **rule entry** (ready to paste into the rules file) and the **rationale** (for the issue / PR discussion, not the rules file).

## Status & next steps

- **#18 (new rules)** — open. The program direction has since evolved: rules are being consolidated into the `QuantEcon/style-guide` rule database (coordinated in the private hub `QuantEcon/project-style-guide`), and `action-style-guide` is slated to be split & retired. The `rule-drafts/` here are **transcription inputs for that consolidation**, not a PR against `action-style-guide`. The two weakest-evidence rules (`qe-math-014`, `qe-math-015`) may be deferred.
- **#19 (Phase 4.3)** — the body has been rewritten. The original asked whether scope should go from ~13 to 22 rules; building the checks answered it: **41 of 49 are mechanically checkable**, and the issue now also offers `tools/qestyle_rules.py` and `qestyle_lex.py` for adoption rather than parallel maintenance. **The live issue still carries the old "22 rules" text and needs re-syncing.**
- **#20 (bulk-audit mode)** — open design question on where cross-series synthesis should live.
- **#21 (corpus offer)** — no action required from the team; the published corpus is offered as test/eval data.

**These bodies are ahead of the live issues.** The 2026-08 pass rewrote #19, and this
assembly retargeted the repository links in all four — but the corpus counts quoted in #18,
#20 and #21 are still the May 2026 ones, so re-syncing does not refresh them.
`action-style-guide` is not in this pass's GitHub scope, so nothing was pushed. Someone with
access needs to run:

```bash
for n in 18:01-new-style-rules 19:02-phase-4-3-deterministic-checks \
         20:03-bulk-audit-mode 21:04-corpus-offer; do
  gh issue edit "${n%%:*}" --repo QuantEcon/action-style-guide \
     --body-file "contributions/issues/${n#*:}.md"
done
```

The bodies link to this repository and to its published pages, and those links now point at
`compliance-lecture-style`. There is no rename coming:
[#2](https://github.com/QuantEcon/audit.2026-05.style-guide/issues/2) settled on
assembling a separate ledger and leaving `audit.2026-05.style-guide` archived under its own
name. So the loop above is a single run — once this assembly has landed, from a checkout of
the ledger, by someone with access to `action-style-guide`.

## Provenance

First generated in the May 2026 style audit ([repo](https://github.com/QuantEcon/audit.2026-05.style-guide) · [report](https://quantecon.github.io/audit.2026-05.style-guide/)), and maintained here since that audit was absorbed into this ledger. See [`../UPDATE.md`](../UPDATE.md) for how a pass is reproduced.
