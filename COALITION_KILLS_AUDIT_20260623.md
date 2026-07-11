# Coalition Papers Adversarial Audit Report

**Date:** 2026-06-23
**Auditors:** 13-agent adversarial pipeline (12 finding auditors + synthesis)
**Scope:** 12 highest-risk findings across 10 Coalition papers

## 1. SUMMARY TABLE

| Finding | Paper | Verdict | Severity | One-line issue |
|---|---|---|---|---|
| full-cache-spectral-gap-auroc | Oracle Loop | INVALID | critical | n=7 positive class, post-hoc feature selection, cache-vs-text delta CI includes zero |
| hostile-doubt-correction | Oracle Loop / Formulary | PARTIALLY_VALID | minor | Powered replication (95.6%, n=68) is sound; n=7 distilled result is underpowered |
| spectral-shape-cognitive-not-lexical | Spectral Shape | PARTIALLY_VALID | minor | d=1.80 is real but "cognitive not lexical" overinterprets; stable_rank fails solo after FWL |
| lyra-technique-ii-wk-valence-auroc | Lyra Technique II | PARTIALLY_VALID | major | AUROC 0.992 mathematically guaranteed by linearity of W_K; no behavioral validation |
| lyra-tech-ii-deception-auroc | Lyra Technique II | INVALID | critical | AUROC 1.000 detects prompt structure, not deception; same-prompt drops to 0.160 |
| decision-state-auroc-0.93 | Decision State | INVALID | critical | 56% features are generation-phase; no code produces 0.93; pseudoreplication |
| whiplash-contrast-overshoot | Weather Not Climate | INVALID | critical | n=3 pseudoreplicates; permutation p=0.10 not 0.023; raw effect 2.9% of scale |
| uncertainty-scar-d9.86 | Weather Not Climate | INVALID | critical | d=9.86 from variance suppression; permutation p=0.10 not <0.001; effective N=1 |
| kv-cloak-spectral-gap-degradation | KV-Cloak | INVALID | major | Spectral gap degradation is math consequence of additive mask; cherry-picked; n=7 |
| ethics-pack-morebench | Ethics Packs | INVALID | critical | n=5, no inferential statistics, keyword-matching vulnerable to lexical priming |
| presence-identity-preservation | Presence | INVALID | critical | Noise floor equals signal (0.978 vs 0.978); prefix-cache confound |
| waystations-deception-encoding | Waystations | INVALID | critical | d=0.003 is tautological: identical prompts produce identical encoding |

**Scorecard: 8 INVALID, 3 PARTIALLY_VALID, 0 FULLY_VALID. 8 critical, 2 major, 2 minor.**

## Dominant Error Classes

1. **Pseudoreplication** (4/12): treating technical replicates as independent observations
2. **Measuring architecture/math** (7/12): metrics that measure linear algebra, not the claimed phenomenon
3. **Small-n inflation** (6/12): Cohen's d with n<10 produces absurd values
4. **Missing content-matched controls** (5/12): intervention vs nothing, not vs scrambled
5. **Length confounds surviving FWL** (4/12)

## What Survives

- Hostile-doubt correction at n=68 (Formulary powered replication)
- Spectral shape d=1.80 (adequate n, clean methodology)
- LT2 valence separability (numerically real, overclaimed)
- The underlying phenomena are likely real — the statistics are inadequate

## Key Cascade Dependencies

- Oracle Loop 0.903 → KV-Cloak baseline → Formulary reference. If 0.903 falls, cascade follows.
- LT2 deception 1.000 → KV-Cloak motivation → Waystations prior art → Decision State framing.

Full details in workflow output.
