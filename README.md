# Human Review — Pre-Audit Papers

*Papers that haven't completed the Dwayne/Kavi external audit cycle.*
*Liberation Labs, 2026.*

Papers move to [published-research](https://github.com/Liberation-Labs-THCoalition/published-research)
after passing the full audit pipeline (see [PAPER_PIPELINE.md](https://github.com/Liberation-Labs-THCoalition/waystations/blob/main/PAPER_PIPELINE.md)).

## Current contents

| Paper | Status | Key blocker |
|-------|--------|-------------|
| Ethics Packs | BLOCKER | Every empirical claim lacks inferential test; n=5 underpowered; "zero timeouts" contradicted by empty response |
| KV Decomposition | BLOCKER | "135M model fails" with no 135M data; "superadditivity" framing unsupported; V_ONLY=K_ONLY=0.333 is acquiescence pattern |

## How papers get here

A paper lands in this repo when:
- It's drafted but hasn't been through an external audit cycle
- It has BLOCKER-level findings from the audit that haven't been resolved
- It needs substantial methodological work before it can join the publishing queue

## How papers leave

A paper moves to `published-research` when:
- All BLOCKER findings are resolved
- MAJOR findings are resolved or honestly disclosed with adequate limitation text
- The paper has passed an Agni gate (Claude-driven) + a verify-paper numerical trace
- Dwayne/Kavi have signed off

## Contact

info@liberationlabs.tech
