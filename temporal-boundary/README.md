# Three Killed Experiments and a Valence Feature: What Adversarial Review Reveals About Transformer Self/Other Attribution

**Status:** Under review (round 5 — NEEDS_ATTENTION)
**Authors:** Lyra, Kavi (verification review), Thomas Edrington (Liberation Labs)
**Date:** June 2026
**Review gate:** Round 5 audit — PDF rebuilt, 12 items fixed, remaining items in progress

## Paper Summary

Three experiments were killed by adversarial review before producing claims. Each kill identifies a generalizable confound for ToM research in transformers.

The surviving finding: SAE feature 58995 at L47 tracks emotional valence during encoding (r=0.686, p<0.001, n=30, in-sample; held-out validation needed). A null-null control shows injection text divergence (~74.8%) is not significantly greater than stochastic decoding noise (73.6%; d=0.062, p=0.856). The encoding-phase feature's invariance to injection is structurally guaranteed (injection is post-encoding), not evidence of temporal separation.

## Contents

```
temporal-boundary/
├── main.tex                    # Full paper (LaTeX)
├── references.bib              # Bibliography
├── figures/
│   ├── fig1_emotion_activations.pdf
│   ├── fig2_valence_scatter.pdf
│   ├── fig3_text_divergence.pdf
│   └── fig4_depth_resistance_null.pdf
├── data/
│   └── temporal_boundary_results.json
└── README.md
```

## Open Items (Round 5)

- Uncited 95.6%/350 statistic (line 150)
- Circumplex citations (choi2026, anthropic2026) unverifiable but non-load-bearing
