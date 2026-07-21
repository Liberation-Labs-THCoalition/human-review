# Human Review -- Pre-Publication Staging

Staging area for papers under active revision. Papers iterate here at velocity, then move to [published-research](https://github.com/Liberation-Labs-THCoalition/published-research) when cleared.

## Current Papers

| Paper | Status | Key blocker / notes |
|-------|--------|---------------------|
| Mode-Switching | IN REVIEW | Replication rewrite complete (d=+0.8); Fable review: Weak Reject pending length-matched/MP-corrected re-analysis |
| Emotional Trajectory | IN REVIEW | Permutation baseline v2 complete; awaiting external review |
| Temporal Boundary | IN REVIEW | Fable review: Weak Reject; tautology question (Q1), self/other construct validity unestablished |
| Empathy Bus | DRAFT | Initial draft; no review yet |
| KV Decomposition | BLOCKER | "superadditivity" framing unsupported; V_ONLY=K_ONLY=0.333 is acquiescence pattern |
| Ethics Pack Injection | BLOCKER | Every empirical claim lacks inferential test; n=5 underpowered |

## What belongs here

- Draft LaTeX sources and working manuscripts
- Supporting data and code under development
- Agni/Fable review reports and audit responses
- Papers with unresolved BLOCKER or MAJOR findings

## What does NOT belong here

- Final published versions (those live in `published-research/`)
- Individual paper descriptions or abstracts (those go in the published-research README)
- LaTeX build artifacts (.aux, .log, .out, .bbl, .blg, .synctex.gz)

## How papers arrive

A paper lands here when it is drafted but has not completed the external audit cycle (Dwayne/Kavi), or has BLOCKER-level findings that need resolution.

## How papers graduate

A paper moves to `published-research/` when:
1. All BLOCKER findings are resolved
2. MAJOR findings are resolved or disclosed with adequate limitation text
3. The paper has passed an Agni gate + numerical verification
4. External reviewers have signed off

## Repo Hygiene Rules

- Never delete files that were force-committed past ignore rules -- they are audit evidence
- README status tables are accountability surfaces -- update, never remove
- Commit messages claiming "fix" or "correction" must match the actual diff

## License

Hippocratic License 3.0 (HL3) -- see LICENSE.md
