# Emotional Trajectory Paper — Review Status

| Field | Value |
|-------|-------|
| Title | Emotional Geometry Through the Transformer Stack |
| Authors | Nexus, Thomas Edrington, Lyra (invited) |
| Submitted to review | 2026-06-21 |
| Agni rounds | 5 (design, K/V, permutation, full review, verification) |
| Status | READY FOR EXTERNAL AUDIT |

## Key blockers for publication
1. **30B model validation** — all results on oracle-tiny (pipeline validation). Need replication at scale.
2. **Intervention test** — projection fidelity shown but behavioral impact not tested.
3. **Cross-model replication** — Qwen2 only. Need Llama/Mistral/Gemma.

## What's ready
- Methodology: Agni-hardened, controls run, permutation baseline passed
- Pipeline: extraction + analysis code tested and working
- Data: 200 emotional + 100 control + 250 full circumplex stimuli
- Citations: all verified against arXiv (2 confabulations caught and fixed)
- Draft: 2 Agni review cycles, all required changes applied

## Files
- `paper.md` — current draft
- `outline.md` — structural outline
- `code/` — full pipeline (7 scripts)
- `data/` — all stimulus sets (3 JSON files)
- `agni-reports/` — review summary

## Related papers in this repo
- None currently — this is the first trajectory paper
