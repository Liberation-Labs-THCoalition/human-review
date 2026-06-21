# The Temporal Boundary: Self/Other Separation in Transformers Is Temporal, Not Geometric

**Status:** Ready for human review
**Authors:** Lyra, Thomas Edrington (Liberation Labs / THCoalition)
**Date:** June 2026
**Review gate:** Agni Phase 3d (methodological) + Style guide + Final verification — all PASS

## Paper Summary

The self/other boundary in transformer emotional processing is temporal: the model encodes the user's emotional state during input (SAE feature 58995 at L47, r=0.686 with valence) and expresses its own response during generation (V-cache emotion geometry at L3/L7). These channels are geometrically independent (cosine=0.031). V-cache injection changes behavior (72-74% text divergence) without affecting the encoding feature (<10⁻⁴ change).

Three experiments were killed by adversarial review before producing claims. Each kill identifies a generalizable confound for ToM research in transformers.

## Contents

```
temporal-boundary/
├── main.tex                    # Full paper (LaTeX)
├── references.bib              # Bibliography
├── figures/
│   ├── fig1_emotion_activations.pdf   # Per-emotion feature activation
│   ├── fig2_valence_scatter.pdf       # r=0.686 valence correlation
│   ├── fig3_text_divergence.pdf       # Behavioral change confirmation
│   └── fig4_depth_resistance_null.pdf # Honest null (depth ≠ resistance)
├── data/
│   ├── temporal_boundary_results.json # 360 trials, full data
│   ├── preregistration.json           # Pre-registered hypotheses
│   └── figure_generation.py           # Reproducible figure script
└── README.md                  # This file
```

## Key Claims to Verify

| Claim | Source | Location in paper |
|-------|--------|-------------------|
| r=0.686 (feature vs valence) | temporal_boundary_results.json | Abstract, Section 4 |
| n=360 (30 scenarios × 4 conditions × 3 repeats) | temporal_boundary_results.json | Section 3 |
| Per-emotion activations (Table 1) | temporal_boundary_results.json | Section 4 |
| Encoding depth consistency (range=0.000) | temporal_boundary_results.json | Section 4 |
| Text divergence 0.72-0.74 | temporal_boundary_results.json | Section 5 |
| Depth-resistance ρ values (Table 2) | temporal_boundary_results.json | Section 5 |

## Data Access

All raw data for claim verification is in `data/temporal_boundary_results.json` (360 trials, ~839KB).

**Private infrastructure data** (not included, available on request):
- SAE model weights: Qwen-Scope pre-trained SAEs (publicly available via HuggingFace)
- Model: Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled (publicly available on HuggingFace)
- Experiment script: Available in the Project-Oracle private repo (Liberation Labs members)

## Known Limitations (from Agni review)

1. Single model (27B hybrid transformer) — cross-architecture replication needed
2. Architecture confound: hybrid model (16 full-attn + 48 linear-attn) may explain "zero change" through limited information flow rather than temporal boundary
3. Finding 2 (depth-resistance) is a null at n=90 — no significant correlations
4. Feature 58995 is domain-specific (zero activation on factual prompts)
5. No causal test (encoding → generation direction not tested)
6. Single dose (α=0.1) — dose-response relationship untested

## Review Instructions

1. Verify numerical claims against `data/temporal_boundary_results.json`
2. Check that the three kills are adequately described for replication
3. Assess whether the architecture confound (Section 4) is adequately addressed
4. Flag any overclaiming given the honest null in Finding 2
